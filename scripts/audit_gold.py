"""Download a dated, rank-stratified sample of public elite episodes for analysis."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

OUT=Path('results/gold'); RAW=Path('vendor/gold')
RANKS=(1,2,3,5,8,13,21,27)


def download(episode_id):
    path=RAW/f'episode-{episode_id}-replay.json'
    if not path.exists():
        api=KaggleApi();api.authenticate()
        api.competition_episode_replay(episode_id,path=str(RAW),quiet=True)
    data=json.loads(path.read_text(encoding='utf-8'))
    return dict(id=episode_id,path=path.as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                engine=data['module_version'],steps=len(data['steps']),seed=data['info']['seed'],
                rewards=data['rewards'],teams=data['info']['TeamNames'])


def main():
    OUT.mkdir(parents=True,exist_ok=True);RAW.mkdir(parents=True,exist_ok=True)
    api=KaggleApi();api.authenticate()
    board=api.competition_leaderboard_view('kaggriculture',page_size=27)
    snapshot=[dict(rank=i+1,team_id=r.team_id,team_name=r.team_name,score=r.score,
                   submission_date=str(r.submission_date)) for i,r in enumerate(board)]
    report=dict(retrieved_utc=datetime.now(timezone.utc).isoformat(),selection_ranks=RANKS,
                scope='Provisional gold-range teams; public behavioral observations, not private agent code.',
                leaderboard=snapshot,selected=[],episodes=[],complete=False)
    out=OUT/'audit.json';out.write_text(json.dumps(report,indent=2)+'\n')
    for rank in RANKS:
        team=snapshot[rank-1]
        submissions=api.competition_team_submissions(team['team_id'])
        best=max(submissions,key=lambda s:float(s.public_score or '-inf'))
        episodes=api.competition_list_episodes(best.id)
        chosen=[e for e in episodes if str(e.state).endswith('COMPLETED')
                and str(e.type).endswith('EPISODE_TYPE_PUBLIC')][:3]
        item=dict(**team,submission_id=best.id,submission_score=best.public_score,
                  episodes=[dict(id=e.id,created=str(e.create_time),agents=[dict(submission_id=a.submission_id,
                           seat=a.index,team_id=a.team_id,team_name=a.team_name,reward=a.reward) for a in e.agents])
                           for e in chosen])
        report['selected'].append(item)
        out.write_text(json.dumps(report,indent=2)+'\n')
        print(f"rank={rank} team={team['team_name']} submission={best.id} episodes={len(chosen)}",flush=True)
    ids=sorted({e['id'] for t in report['selected'] for e in t['episodes']})
    with ThreadPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(download,i) for i in ids]):
            row=future.result();report['episodes'].append(row)
            out.write_text(json.dumps(report,indent=2)+'\n')
            print(f"Downloaded {row['id']} ({len(report['episodes'])}/{len(ids)})",flush=True)
    report['complete']=True
    out.write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
