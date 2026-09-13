"""Full-policy counterfactual data: same prefix, five complete continuations."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path

import accelerator
from build_ml_policy import NAMES
from evaluate_fast import game

ROOT = Path(__file__).resolve().parent


def context(job):
    seed, opponent, seat = job
    rows = [game((candidate, opponent, seed, seat), capture_ml=True) for candidate in NAMES]
    assert len({r['prefix_sha256'] for r in rows}) == 1, ('Prefix mismatch', job)
    assert all(r['decision_features'] == rows[0]['decision_features'] for r in rows), ('Feature mismatch', job)
    assert rows[0]['decision_features'] is not None
    for row in rows:
        assert row['telemetry'].get('ml_decisions') == 1, ('No model decision', job)
        errors = {k: v for k, v in row['telemetry'].items() if ('error' in k or 'fallback' in k) and v}
        assert not errors, (job, errors)
    return dict(seed=seed, opponent=opponent, seat=seat,
                opponent_sha256=rows[0]['opponent_sha256'],
                prefix_sha256=rows[0]['prefix_sha256'], features=rows[0]['decision_features'],
                options=[{k: r[k] for k in ('candidate', 'sha256', 'rewards', 'margin', 'win', 'tie',
                                           'seconds', 'max_call_ms', 'telemetry')}
                         for r in rows])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--split', choices=['train', 'selection', 'pilot'], required=True)
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    plan_path = ROOT / 'results/ml/plan.json'
    plan = json.loads(plan_path.read_text())
    seeds = plan['training_seeds'] if args.split == 'train' else plan['selection_seeds']
    opponents = plan['training_opponents']
    if args.split == 'pilot':
        seeds, opponents = [70001], ['matched6']
    jobs = [(s, o, p) for s in seeds for o in opponents for p in plan['seats']]
    accelerator.load()
    build = json.loads((ROOT / 'results/ml/build_forced.json').read_text())
    meta = dict(split=args.split, expected_contexts=len(jobs), complete=False,
                feature_schema_sha256=build['features_sha256'],
                policy_sha256=build['policy_sha256'], candidates=build['candidates'],
                plan_sha256=hashlib.sha256(plan_path.read_bytes()).hexdigest())
    out = ROOT / 'results/ml' / (args.split + '.jsonl')
    meta_path = out.with_suffix('.meta.json')
    existing = []
    if out.exists():
        old = json.loads(meta_path.read_text())
        assert old['candidates'] == meta['candidates'] and old['plan_sha256'] == meta['plan_sha256']
        existing = [json.loads(line) for line in out.read_text().splitlines() if line]
    done = {(r['seed'], r['opponent'], r['seat']) for r in existing}
    assert done <= set(jobs)
    meta_path.write_text(json.dumps(meta, indent=2) + '\n')
    with out.open('a', encoding='utf-8') as stream, ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(context, job) for job in jobs if job not in done]
        count = len(done)
        for future in as_completed(futures):
            row = future.result()
            stream.write(json.dumps(row, separators=(',', ':')) + '\n')
            stream.flush()
            count += 1
            print(f"{args.split} {count}/{len(jobs)} seed={row['seed']} rival={row['opponent']} seat={row['seat']} "
                  f"margins={[o['margin'] for o in row['options']]}", flush=True)
    meta.update(complete=True, contexts=count, games=count * len(NAMES))
    meta_path.write_text(json.dumps(meta, indent=2) + '\n')


if __name__ == '__main__':
    main()
