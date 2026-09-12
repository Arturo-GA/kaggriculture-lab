"""Paired official-engine games. No replay opponents or hidden observations."""
import argparse
import contextlib
import hashlib
import importlib.metadata
import io
import json
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent


def game(job):
    candidate, opponent, seed, seat = job
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    paths = [ROOT/'candidates'/(candidate+'.py'),
             ROOT/'candidates'/(opponent+'.py') if opponent != 'starter' else None]
    timings, policies, diagnostics = [], [], []
    for path in paths:
        calls = []
        timings.append(calls)
        if path is None:
            policies.append('starter')
            diagnostics.append(None)
            continue
        fn = get_last_callable(path.read_text(encoding='utf-8'), path=str(path))
        assert fn is fn.__globals__['agent']
        diagnostics.append(fn)
        def measured(obs, config, fn=fn, calls=calls):
            begin = time.perf_counter()
            action = fn(obs, config)
            calls.append((time.perf_counter()-begin)*1000)
            json.dumps(action, allow_nan=False)
            return action
        policies.append(measured)
    if seat == 1:
        policies.reverse()
    begin = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        env = make('kaggriculture', configuration={'episodeSteps':720, 'seed': seed}, debug=True)
        final = env.run(policies)[-1]
    status = [row['status'] for row in final]
    rewards = [row['reward'] for row in final]
    assert status == ['DONE','DONE'], (job, status)
    assert len(env.steps) == 720, (job, len(env.steps))
    margin = rewards[seat]-rewards[1-seat]
    return dict(candidate=candidate, opponent=opponent, seed=seed, seat=seat,
                rewards=rewards, margin=margin, win=int(margin>0), tie=int(margin==0),
                status=status, steps=len(env.steps), seconds=time.perf_counter()-begin,
                max_call_ms=max(timings[0]), calls=len(timings[0]),
                telemetry=dict(getattr(diagnostics[0], 'telemetry', {})),
                sha256=hashlib.sha256(paths[0].read_bytes()).hexdigest())


def run(candidates, opponents, seeds, workers, output):
    jobs = [(c,o,s,p) for c in candidates for o in opponents for s in seeds for p in (0,1)]
    rows = []
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(game, job) for job in jobs]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            out.write_text(json.dumps({'engine':importlib.metadata.version('kaggle-environments'),
                'expected_games':len(jobs), 'complete':len(rows)==len(jobs),
                'rows':rows},indent=2)+'\n')
            print(f"{len(rows)}/{len(jobs)} {row['candidate']} vs {row['opponent']} seed={row['seed']} seat={row['seat']} margin={row['margin']:.0f} max_ms={row['max_call_ms']:.1f}", flush=True)
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidates', nargs='+', default=['h6','h8','pressure'])
    parser.add_argument('--opponents', nargs='+', default=['v37'])
    parser.add_argument('--seeds', nargs='+', type=int, default=[101,202,303,404])
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--output', default='results/screen.json')
    args = parser.parse_args()
    run(args.candidates,args.opponents,args.seeds,args.workers,args.output)
