"""Reproduce results and apply the pre-holdout promotion requirements."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent


def summarize(path):
    data = json.loads(path.read_text())
    assert data['complete'] and len(data['rows']) == data['expected_games']
    groups = defaultdict(list)
    for row in data['rows']:
        assert row['steps'] == 720 and row['status'] == ['DONE', 'DONE']
        groups[row['candidate'], row['opponent']].append(row)
    return dict(games=len(data['rows']), engine=data['engine'], groups=[
        dict(candidate=c, opponent=o, games=len(rows), wins=sum(r['win'] for r in rows),
             ties=sum(r['tie'] for r in rows), mean_margin=mean(r['margin'] for r in rows),
             waits=sum(r['telemetry'].get('gate_waits', 0) for r in rows),
             additional_advance_units=sum(r['telemetry'].get('lead_units', 0) for r in rows),
             max_call_ms=max(r['max_call_ms'] for r in rows))
        for (c, o), rows in sorted(groups.items())])


def main():
    files = ('market_gate_screen', 'market_gate2_screen', 'market_lead_screen', 'market_lead_holdout')
    result = {name: summarize(ROOT / 'results' / (name + '.json')) for name in files}
    plan = json.loads((ROOT / 'results/market_lead_plan.json').read_text())
    data = json.loads((ROOT / 'results/market_lead_holdout.json').read_text())['rows']
    assert {r['seed'] for r in data} == set(plan['seeds'])
    assert len(data) == plan['expected_games']
    assert hashlib.sha256((ROOT / 'candidates/belief_lead12.py').read_bytes()).hexdigest() == plan['candidate_sha256']
    candidates = [r for r in data if r['candidate'] == plan['candidate']]
    assert all(r['sha256'] == plan['candidate_sha256'] for r in candidates)
    controls = {(r['opponent'], r['seed'], r['seat']): r for r in data if r['candidate'] == plan['control']}
    external = defaultdict(list)
    for row in candidates:
        if row['opponent'] == 'matched6':
            continue
        ctrl = controls[row['opponent'], row['seed'], row['seat']]
        points = lambda r: r['win'] + 0.5 * r['tie']
        external[row['opponent']].append((points(row) - points(ctrl), row['margin'] - ctrl['margin']))
    paired = {o: dict(improved_outcomes=sum(v > 0 for v, m in rows),
                      worse_outcomes=sum(v < 0 for v, m in rows),
                      mean_margin_difference=mean(m for v, m in rows))
              for o, rows in sorted(external.items())}
    direct = [r for r in candidates if r['opponent'] == 'matched6']
    conditions = dict(
        head_to_head_advantage=sum(r['win'] for r in direct) > sum(1 - r['win'] - r['tie'] for r in direct),
        external_improvement=any(p['improved_outcomes'] for p in paired.values()),
        no_external_regressions=not any(p['worse_outcomes'] for p in paired.values()),
        positive_external_margin=sum(m for rows in external.values() for v, m in rows) > 0,
        no_errors=not any(v for r in candidates for k, v in r['telemetry'].items() if 'error' in k or 'fallback' in k),
        timing=max(r['max_call_ms'] for r in candidates) < 1000,
    )
    result['paired_holdout'] = paired
    result['promotion'] = dict(conditions=conditions, passes_screen_gate=all(conditions.values()),
                               released=False, retained='matched6',
                               note='No new competitive submission. A passing screen would still require official-engine confirmation on additional seeds.')
    result['valid_strategy_games'] = sum(result[n]['games'] for n in files)
    result['excluded_initial_games'] = 24
    result['excluded_initial_reason'] = 'Official loader selected the parent alias instead of the experimental wrapper; fixed and covered by a regression test. Do not use these games as evidence for the gates.'
    out = ROOT / 'results/market_research_summary.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(games=result['valid_strategy_games'], paired=paired, promotion=result['promotion']), indent=2))


if __name__ == '__main__':
    main()
