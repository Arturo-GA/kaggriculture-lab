"""Summarize the frozen second panel; never package or submit an agent."""
from collections import Counter, defaultdict
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent


def summarize(filename):
    report = json.loads((ROOT / 'results' / filename).read_text())
    rows = report['rows']
    assert report['complete'] and len(rows) == report['expected_games'], filename
    groups = defaultdict(list)
    for row in rows:
        assert row['status'] == ['DONE', 'DONE'] and row['steps'] == 720
        groups[row['candidate'], row['opponent']].append(row)
    return {
        'games': len(rows),
        'engine': report['engine'],
        'max_call_ms': max(r['max_call_ms'] for r in rows),
        'groups': [dict(candidate=c, opponent=o, games=len(items),
                        seeds=len({r['seed'] for r in items}),
                        wins=sum(r['win'] for r in items),
                        ties=sum(r['tie'] for r in items),
                        mean_margin=mean(r['margin'] for r in items),
                        worst_margin=min(r['margin'] for r in items),
                        first_shops=dict(Counter((r.get('shops') or ['not_recorded'])[0]
                                                 for r in items)))
                   for (c, o), items in sorted(groups.items())],
    }


def main():
    result = {name: summarize(name + '.json') for name in
              ('panel_v2', 'routes14_screen', 'routes14_holdout')}
    data = json.loads((ROOT / 'results/routes14_holdout.json').read_text())['rows']
    control = {(r['opponent'], r['seed'], r['seat']): r for r in data
               if r['candidate'] == 'matched6'}
    differences = defaultdict(list)
    for r in data:
        if r['candidate'] != 'routes14' or r['opponent'] == 'matched6':
            continue
        other = control[r['opponent'], r['seed'], r['seat']]
        points = lambda x: x['win'] + 0.5 * x['tie']
        differences[r['opponent']].append(points(r) - points(other))
    result['paired_external_outcomes'] = {
        opponent: dict(improvements=sum(v > 0 for v in values),
                       regressions=sum(v < 0 for v in values),
                       unchanged=sum(v == 0 for v in values))
        for opponent, values in sorted(differences.items())}
    result['interpretation'] = {
        'promote_routes14': False,
        'retained_candidate': 'matched6',
        'reason': 'No demonstrated head-to-head advantage; regressions on an external opponent.',
        'decision_timing': 'Conservative interpretation after inspecting the holdout, not a preregistered statistical test.',
        'limitations': 'Eight holdout seeds; seats are dependent. Different policies can change shop draws even with the same seed. No claimed leaderboard gain.',
    }
    (ROOT / 'results/routes14_summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
