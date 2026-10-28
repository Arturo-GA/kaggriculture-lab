"""Read-only current ladder/episodes and a bounded replay sample for loss diagnosis."""
from collections import Counter
from datetime import datetime,timezone
import gzip,hashlib,json
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
from live_report import leaderboard
from research_f16 import plain


def main():
    root=Path('results/frontier17');root.mkdir(exist_ok=True)
    raw=Path('vendor/research_f17');raw.mkdir(parents=True,exist_ok=True)
    replays=Path('vendor/live_f16');replays.mkdir(exist_ok=True)
    api=KaggleApi();api.authenticate();teams,cuts=leaderboard(api)
    ranked=sorted(teams.values(),key=lambda t:t['rank'])
    result=dict(checked_utc=datetime.now(timezone.utc).isoformat(),cuts=cuts,own=teams.get('16639155'),
        top100_cut=ranked[99],submissions=[],selected_replays=[])
    for s in api.competition_submissions('kaggriculture')[:2]:
        rows=[]
        for e in api.competition_list_episodes(s.ref):
            if not str(e.state).endswith('COMPLETED') or not str(e.type).endswith('PUBLIC'):continue
            me=next(a for a in e.agents if a.submission_id==s.ref);op=next(a for a in e.agents if a.submission_id!=s.ref)
            t=teams.get(str(op.team_id),{})
            rows.append(dict(id=e.id,created=str(e.create_time),seat=me.index,my=me.reward,op=op.reward,
                margin=me.reward-op.reward,op_name=op.team_name,op_sub=op.submission_id,op_score=t.get('score'),op_rank=t.get('rank')))
        rows.sort(key=lambda r:r['created'])
        sub=dict(id=s.ref,status=str(s.status),score=s.public_score,games=len(rows),wins=sum(r['margin']>0 for r in rows),
            losses=sum(r['margin']<0 for r in rows),ties=sum(r['margin']==0 for r in rows),episodes=rows)
        result['submissions'].append(sub)
        print(json.dumps({k:v for k,v in sub.items() if k!='episodes'}),flush=True)
        if s.ref==56609913:
            selected=sorted([r for r in rows if r['margin']<0],key=lambda r:r['margin'])
            selected+=sorted([r for r in rows if r['margin']>=0],key=lambda r:r['margin'])[:4]
        else:
            selected=sorted([r for r in rows if r['margin']<0 and (r['op_score'] or 0)>=2400],key=lambda r:-(r['op_score'] or 0))[:8]
        for r in selected:
            result['selected_replays'].append(dict(r,submission=s.ref,candidate='f16_repaired' if s.ref==56609913 else 'f15_e81'))
    (root/'live_snapshot.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (root/'episodes.json').write_text(json.dumps(result['selected_replays'],indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('top100',result['top100_cut'],'selected',len(result['selected_replays']),flush=True)
    for r in result['selected_replays']:
        path=replays/f"episode-{r['id']}-replay.json";zipped=Path(str(path)+'.gz')
        if not zipped.exists():
            if not path.exists():api.competition_episode_replay(r['id'],path=str(replays),quiet=True)
            data=path.read_bytes();assert json.loads(data)['info']['EpisodeId']==r['id']
            with gzip.open(zipped,'wb') as f:f.write(data)
            path.unlink()
        print('replay',r['id'],r['candidate'],r['op_name'],r['op_score'],r['margin'],flush=True)
    kernels=plain(api.kernels_list(search='kaggriculture',sort_by='dateRun',page_size=40))
    (raw/'kernels.json').write_text(json.dumps(kernels,indent=2,ensure_ascii=False),encoding='utf-8')
    print('updated notebooks',json.dumps([{k:v.get(k) for k in ['ref','title','last_run_time']} for v in kernels if str(v.get('last_run_time',''))>'2026-09-27T12:32:00'],ensure_ascii=False),flush=True)
    topics=plain(api.competition_list_topics('kaggriculture',sort_by='recent',page=1))
    (raw/'topics.json').write_text(json.dumps(topics,indent=2,ensure_ascii=False),encoding='utf-8')
    print('topics saved',flush=True)


if __name__=='__main__':main()
