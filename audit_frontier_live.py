"""Match the newest public submission's actions to our local artifact."""
import contextlib
import io
import json
from datetime import datetime,timezone
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi


def main():
    api=KaggleApi();api.authenticate();out=Path('results/frontier2');out.mkdir(exist_ok=True)
    subs=api.competition_submissions('kaggriculture');latest=subs[0]
    report=dict(retrieved_utc=datetime.now(timezone.utc).isoformat(),
        submissions=[{k:str(getattr(s,k,'')) for k in ('ref','date','status','public_score')} for s in subs[:3]],rows=[])
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
    raw=Path('vendor/frontier2');raw.mkdir(exist_ok=True)
    episodes=[e for e in api.competition_list_episodes(latest.ref) if str(e.state).endswith('COMPLETED')
              and str(e.type).endswith('EPISODE_TYPE_PUBLIC')][:6]
    for ep in episodes:
        path=raw/f'episode-{ep.id}-replay.json'
        if not path.exists():api.competition_episode_replay(ep.id,path=str(raw),quiet=True)
        data=json.loads(path.read_text(encoding='utf-8'))
        seat=next(a.index for a in ep.agents if a.submission_id==latest.ref)
        fn=get_last_callable(Path('candidates/frontier.py').read_text(encoding='utf-8'))
        config=dict(data['configuration'],seed=data['info']['seed']);mismatches=[]
        for step in range(719):
            obs=dict(data['steps'][step][0]['observation'])
            obs.update(data['steps'][step][seat]['observation']);obs['player']=seat;obs['step']=step
            got=fn(obs,config)
            expected=data['steps'][step+1][seat]['action']
            if got!=expected:mismatches.append(step)
        row=dict(episode=ep.id,seat=seat,rewards=data['rewards'],
                 exact_frontier_actions=not mismatches,mismatch_count=len(mismatches),
                 first_mismatch=mismatches[0] if mismatches else None,
                 opponent=next(a.team_name for a in ep.agents if a.index!=seat),snapshots={})
        for step in (432,576,648,696,719):
            obs=data['steps'][step][0]['observation'];farms=obs['farms']
            row['snapshots'][step]=dict(own_money=farms[seat]['money'],rival_money=farms[1-seat]['money'],
                gap=farms[seat]['money']-farms[1-seat]['money'])
        report['rows'].append(row);print(json.dumps(row,ensure_ascii=True),flush=True)
        (out/'live_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'live_audit.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
