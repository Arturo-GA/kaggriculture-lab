"""Apply the gate registered in results/frontier15/plan.json to the holdout and write holdout_summary.json."""
import json
from pathlib import Path
from frontier5_validation import assess


def main():
    root = Path('results/frontier15')
    plan = json.loads((root / 'plan.json').read_text(encoding='utf-8'))
    gate = plan['gate']
    summary = assess(root / 'holdout.json', plan['candidate'], baseline=plan['control'])
    assert summary['sha256'] == plan['candidate_sha256'], 'candidate changed after the plan was registered'
    rows = json.loads((root / 'holdout.json').read_text(encoding='utf-8'))['rows']
    control = {(r['opponent'], r['seed'], r['seat']): r for r in rows if r['candidate'] == plan['control']}
    mine = [r for r in rows if r['candidate'] == plan['candidate']]
    summary['paired_margin_gain'] = sum(r['margin'] - control[(r['opponent'], r['seed'], r['seat'])]['margin'] for r in mine) / len(mine)
    cha22 = summary['per_opponent'][gate['cha22']]
    summary['cha22_score'] = (cha22['wins'] + .5 * cha22['ties']) / cha22['games']
    checks = dict(
        total=summary['total_score_delta'] >= gate['total_min'],
        mirror=summary['mirror_score'] >= gate['mirror_min'],
        cha22=summary['cha22_score'] >= gate['cha22_min'],
        floor=all(g['score_delta'] >= gate['opponent_floor'] for g in summary['per_opponent'].values()),
        runtime=summary['runtime_passed'])
    summary['gate_checks'] = checks
    summary['registered_gate_passed'] = all(checks.values())
    for extra in plan.get('holdout_extra_candidates', []):
        s = assess(root / 'holdout.json', extra, baseline=plan['control'])
        summary.setdefault('extra_candidates', {})[extra] = dict(total_score_delta=s['total_score_delta'], mirror_score=s['mirror_score'],
                                                                 per_opponent={k: v['score_delta'] for k, v in s['per_opponent'].items()},
                                                                 max_call_ms=s['max_call_ms'], runtime_passed=s['runtime_passed'])
    (root / 'holdout_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k not in ('per_opponent', 'errors', 'extra_candidates')}, indent=2))
    for k, g in summary['per_opponent'].items():
        print('%-28s %2d-%2d-%2d  delta %+5.1f  margin %+7.0f' % (k, g['wins'], g['losses'], g['ties'], g['score_delta'], g['mean_margin']))
    for k, v in summary.get('extra_candidates', {}).items():
        print('extra', k, v['total_score_delta'], v['mirror_score'], v['per_opponent'])


if __name__ == '__main__':
    main()
