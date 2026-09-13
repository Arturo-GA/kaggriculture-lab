"""Diagnose the slowest holdout games without changing policy or test outcomes."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import time

import accelerator


def profile(row):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
    paths=[Path('candidates',row[k]+'.py') for k in ('candidate','opponent')]
    policies=[get_last_callable(p.read_text(encoding='utf-8')) for p in paths]
    env=accelerator.load().Game(row['seed'])
    config=dict(episodeSteps=720,seed=row['seed'],boardSize=10,turnsPerDay=24,
                shedCapacity=100,maxMarketOrdersPerTurn=10,townShopSellInterval=4,
                townCenterSellInterval=24,farmHandCostMult=1)
    timings=[]
    while not env.done:
        actions=[None,None]
        for i,fn in enumerate(policies):
            seat=row['seat'] if i==0 else 1-row['seat']
            start=time.perf_counter()
            obs=env.observe(seat)
            observed=time.perf_counter()
            cpu=time.process_time()
            actions[seat]=fn(obs,config)
            end_cpu=time.process_time()
            end=time.perf_counter()
            if i==0:timings.append(dict(step=env.step_count,observation_ms=(observed-start)*1000,
                                       call_ms=(end-observed)*1000,cpu_ms=(end_cpu-cpu)*1000,
                                       combined_ms=(end-start)*1000))
        env.step(*actions)
    rewards=[env.reward(i) for i in (0,1)]
    assert rewards==row['rewards'],('Outcome mismatch',row['candidate'],row['seed'])
    return dict(candidate=row['candidate'],opponent=row['opponent'],seed=row['seed'],seat=row['seat'],
                original_combined_max_ms=row['max_call_ms'],rewards=rewards,
                sha256=hashlib.sha256(paths[0].read_bytes()).hexdigest(),
                max_call_ms=max(t['call_ms'] for t in timings),
                max_combined_ms=max(t['combined_ms'] for t in timings),
                decision=timings[336],slowest_calls=sorted(timings,key=lambda r:-r['call_ms'])[:3])


def main():
    holdout=json.loads(Path('results/ml/holdout.json').read_text())
    jobs=[]
    for name in ('ml_critic','matched6'):
        jobs+=sorted([r for r in holdout['rows'] if r['candidate']==name],
                     key=lambda r:-r['max_call_ms'])[:3]
    rows=[]
    for job in jobs:
        row=profile(job);rows.append(row)
        print(json.dumps(row),flush=True)
    result=dict(passed=all(r['max_combined_ms']<1000 for r in rows),
                protocol='Serial reruns of the three slowest holdout contexts for each frozen policy; '
                         'separate observation generation, policy wall time and CPU time. No tuning.',
                games=len(rows),rows=rows)
    Path('results/ml/latency_diagnosis.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    main()
