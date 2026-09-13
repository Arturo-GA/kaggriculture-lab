"""Public elite fixed-stream stress tests; never equate these to live elite bots."""
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
import contextlib
import hashlib
import io
import json
from pathlib import Path
import time

import accelerator


def replay_check():
    sim=accelerator.load();audit=json.loads(Path('results/gold/audit.json').read_text());rows=[]
    for row in audit['episodes']:
        data=json.loads(Path(row['path']).read_text())
        streams=[sim.Stream([step[seat]['action'] for step in data['steps'][1:]]) for seat in (0,1)]
        rewards=list(sim.run_episode(*streams,seed=row['seed']))
        exact=rewards==row['rewards']
        record=dict(episode=row['id'],cpp_rewards=rewards,recorded_rewards=row['rewards'],cpp_exact=exact)
        if not exact:
            with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                from kaggle_environments import make
                env=make('kaggriculture',configuration=dict(data['configuration'],seed=row['seed']),debug=True)
                policies=[(lambda obs,config,s=s:[step[s]['action'] for step in data['steps'][1:]][obs['step']]) for s in (0,1)]
                final=env.run(policies)[-1]
            record['official_rewards']=[r['reward'] for r in final]
            record['official_exact']=record['official_rewards']==row['rewards']
            assert record['official_exact'],record
        rows.append(record)
    receipt=dict(passed=True,backend='official',games=len(rows),cpp_mismatches=sum(not r['cpp_exact'] for r in rows),rows=rows)
    Path('results/gold/replay_verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt


def game(job):
    candidate,team,ep=job
    elite_seat=next(a['seat'] for a in ep['agents'] if a['submission_id']==team['submission_id'])
    seat=1-elite_seat
    data=json.loads(Path('vendor/gold',f"episode-{ep['id']}-replay.json").read_text())
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    path=Path('candidates',candidate+'.py');fn=get_last_callable(path.read_text(encoding='utf-8'))
    calls=[];prefix=hashlib.sha256()
    def measured(obs,config):
        t=time.perf_counter();action=fn(obs,config)
        calls.append((time.perf_counter()-t)*1000)
        if obs['step']<696:prefix.update(json.dumps(action,sort_keys=True).encode())
        return action
    def recorded(obs,config):return data['steps'][obs['step']+1][elite_seat]['action']
    policies=[None,None];policies[seat]=measured;policies[elite_seat]=recorded
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        env=make('kaggriculture',configuration=dict(data['configuration'],seed=data['info']['seed']),debug=True)
        final=env.run(policies)[-1]
    assert [r['status'] for r in final]==['DONE','DONE'] and len(env.steps)==720
    rewards=[r['reward'] for r in final];margin=rewards[seat]-rewards[elite_seat]
    return dict(candidate=candidate,team=team['team_name'],team_id=team['team_id'],rank=team['rank'],
                episode=ep['id'],seat=seat,rewards=rewards,margin=margin,win=int(margin>0),tie=int(margin==0),
                prefix_sha256=prefix.hexdigest(),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                calls=len(calls),max_call_ms=max(calls),telemetry=getattr(fn,'telemetry',{}))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--candidates',nargs='+',required=True)
    parser.add_argument('--ranks',nargs='+',type=int,required=True);parser.add_argument('--output',required=True)
    parser.add_argument('--workers',type=int,default=4);args=parser.parse_args()
    receipt=Path('results/gold/replay_verification.json')
    if not receipt.exists():replay_check()
    assert json.loads(receipt.read_text())['passed']
    audit=json.loads(Path('results/gold/audit.json').read_text())
    jobs=[(c,t,e) for c in args.candidates for t in audit['selected'] if t['rank'] in args.ranks for e in t['episodes']]
    report=dict(engine='official-1.32.7',scope='Adaptive candidate vs fixed public elite action stream. Not the private reacting agent.',
                expected_games=len(jobs),complete=False,rows=[])
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for f in as_completed([pool.submit(game,j) for j in jobs]):
            row=f.result();report['rows'].append(row);report['complete']=len(report['rows'])==len(jobs)
            Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
            print(f"{len(report['rows'])}/{len(jobs)} {row['candidate']} rank={row['rank']} ep={row['episode']} margin={row['margin']}",flush=True)


if __name__=='__main__':main()
