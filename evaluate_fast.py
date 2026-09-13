"""Optional accelerated live-policy screen; final confirmation uses evaluate.py."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import contextlib
import hashlib
import io
import json
from pathlib import Path
import time

import accelerator

ROOT = Path(__file__).resolve().parent


def game(job, capture_ml=False):
    candidate, opponent, seed, seat = job
    kagsim = accelerator.load()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
    paths = [ROOT / 'candidates' / (name + '.py') for name in (candidate, opponent)]
    policies = [get_last_callable(p.read_text(encoding='utf-8')) for p in paths]
    configuration = {'episodeSteps': 720, 'seed': seed, 'boardSize': 10, 'turnsPerDay': 24,
                     'shedCapacity': 100, 'maxMarketOrdersPerTurn': 10,
                     'townShopSellInterval': 4, 'townCenterSellInterval': 24, 'farmHandCostMult': 1}
    env = kagsim.Game(seed)
    calls = []
    prefix = hashlib.sha256()
    begin = time.perf_counter()
    while not env.done:
        actions = [None, None]
        for index, fn in enumerate(policies):
            player = seat if index == 0 else 1 - seat
            start = time.perf_counter()
            actions[player] = fn(env.observe(player), configuration)
            if index == 0:
                calls.append((time.perf_counter() - start) * 1000)
            json.dumps(actions[player], allow_nan=False)
        if capture_ml and env.step_count < 336:
            prefix.update(json.dumps(actions, sort_keys=True, separators=(',', ':')).encode())
        env.step(*actions)
    rewards = [env.reward(0), env.reward(1)]
    margin = rewards[seat] - rewards[1 - seat]
    assert len(calls) == 719
    telemetry = dict(getattr(policies[0], 'telemetry', {}))
    impl = policies[0].__globals__.get('_IMPL')
    if impl is not None:
        telemetry.update({'chassis_' + k: v for k, v in impl.chassis.diagnostics.items()})
    result = dict(candidate=candidate, opponent=opponent, seed=seed, seat=seat,
                rewards=rewards, margin=margin, win=int(margin > 0), tie=int(margin == 0),
                status=['DONE', 'DONE'], steps=720, seconds=time.perf_counter() - begin,
                max_call_ms=max(calls), calls=len(calls), telemetry=telemetry,
                shops=list(env.observe(0)['town']['unlocked_shops']),
                sha256=hashlib.sha256(paths[0].read_bytes()).hexdigest(),
                opponent_sha256=hashlib.sha256(paths[1].read_bytes()).hexdigest(),
                entrypoints=[f.__name__ for f in policies])
    if capture_ml:
        state = policies[0].__globals__['_ML_PLAYERS'][seat]
        result['decision_features'] = state['features']
        result['prefix_sha256'] = prefix.hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidates', nargs='+', required=True)
    parser.add_argument('--opponents', nargs='+', required=True)
    parser.add_argument('--seeds', nargs='+', type=int, required=True)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    accelerator.load()  # fail before launching workers if receipt is missing
    build = json.loads((ROOT / 'results/cppsim_build.json').read_text())
    jobs = [(c, o, s, p) for c in args.candidates for o in args.opponents
            for s in args.seeds for p in (0, 1)]
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    report = dict(engine='kagsim-0.4.0 / Kaggriculture-1.32.7', backend='cpp',
                  revision=build['revision'], binary_sha256=build['binary_sha256'],
                  expected_games=len(jobs), complete=False, rows=[])
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(game, job) for job in jobs]
        for future in as_completed(futures):
            row = future.result()
            report['rows'].append(row)
            report['complete'] = len(report['rows']) == len(jobs)
            out.write_text(json.dumps(report, indent=2) + '\n')
            print(f"{len(report['rows'])}/{len(jobs)} {row['candidate']} vs {row['opponent']} "
                  f"seed={row['seed']} seat={row['seat']} margin={row['margin']:.0f} "
                  f"waits={row['telemetry'].get('gate_waits', 0)}", flush=True)


if __name__ == '__main__':
    main()
