"""Paired outcomes, seed-cluster uncertainty and predeclared release gates."""
import argparse
from collections import Counter
import json
from pathlib import Path

import numpy as np


def summarize(path):
    report = json.loads(Path(path).read_text())
    assert report['complete'] and len(report['rows']) == report['expected_games']
    rows = report['rows']
    base = {(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']=='matched6'}
    result = dict(source=str(path), games=len(rows), candidates={})
    for candidate in sorted({r['candidate'] for r in rows}):
        selected = [r for r in rows if r['candidate']==candidate]
        assert {(r['opponent'],r['seed'],r['seat']) for r in selected} == set(base)
        groups = {}
        errors = []
        by_seed = {}
        for row in selected:
            key = row['opponent'],row['seed'],row['seat']
            control = base[key]
            score = row['win'] + .5*row['tie']
            delta = score - control['win'] - .5*control['tie']
            group = groups.setdefault(row['opponent'],dict(games=0,wins=0,ties=0,losses=0,
                win_delta=0,score_delta=0.0,margin_delta_sum=0.0))
            group['games'] += 1
            group['wins'] += row['win']
            group['ties'] += row['tie']
            group['losses'] += 1-row['win']-row['tie']
            group['win_delta'] += row['win']-control['win']
            group['score_delta'] += delta
            group['margin_delta_sum'] += row['margin']-control['margin']
            by_seed.setdefault(row['seed'],[]).append(delta)
            errors.extend([(key,k,v) for k,v in row['telemetry'].items()
                           if ('error' in k or 'fallback' in k) and v])
            assert row['status']==['DONE','DONE'] and row['steps']==720 and row['calls']==719
        total = {k:sum(g[k] for g in groups.values()) for k in next(iter(groups.values()))}
        rng = np.random.default_rng(20260912)
        seed_means = np.asarray([np.mean(by_seed[s]) for s in sorted(by_seed)])
        samples = rng.choice(seed_means, size=(10000,len(seed_means)), replace=True).mean(axis=1)
        latency = max(r['max_call_ms'] for r in selected)
        outcomes_passed = (total['win_delta']>0 and all(g['win_delta']>=0 and g['score_delta']>=0
                                             for g in groups.values()) and not errors)
        passed = outcomes_passed and latency<1000
        result['candidates'][candidate] = dict(total=total,per_opponent=groups,errors=errors,
            outcomes_gate_passed=outcomes_passed,latency_gate_passed=latency<1000,
            max_call_ms=latency,gate_passed=passed,seed_clusters=len(seed_means),
            paired_score_delta_mean=float(seed_means.mean()),
            seed_bootstrap_95_percentile_interval=np.quantile(samples,[.025,.975]).tolist(),
            choices=dict(Counter(str(r['telemetry'].get('ml_option','native')) for r in selected)),
            changed_horizon_calls=sum(r['telemetry'].get('ml_changed_horizons',0) for r in selected),
            candidate_sha256=sorted({r['sha256'] for r in selected}))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    result=summarize(args.input)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
