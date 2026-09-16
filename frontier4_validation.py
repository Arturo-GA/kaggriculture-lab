"""Shared local/cloud acceptance checks for a frozen Frontier4 candidate against its V45 control."""
import argparse
import hashlib
import json
from pathlib import Path


def assess(path, candidate, baseline='v45', latency=True):
    report = json.loads(Path(path).read_text(encoding='utf-8'))
    assert report['complete'] and len(report['rows']) == report['expected_games']
    rows = report['rows']
    selected = [r for r in rows if r['candidate'] == candidate]
    controls = {(r['opponent'], r['seed'], r['seat']): r for r in rows if r['candidate'] == baseline}
    assert len(selected) == len(controls) > 0
    assert {(r['opponent'], r['seed'], r['seat']) for r in selected} == set(controls)
    source = hashlib.sha256(Path('candidates', candidate + '.py').read_bytes()).hexdigest()
    groups = {}
    errors = []
    for r in selected:
        key = r['opponent'], r['seed'], r['seat']
        c = controls[key]
        assert r['sha256'] == source
        assert r['status'] == ['DONE', 'DONE'] and r['calls'] == 719 and r['steps'] == 720
        g = groups.setdefault(r['opponent'], dict(games=0, wins=0, ties=0, losses=0, score_delta=0., margin_sum=0.))
        g['games'] += 1
        g['wins'] += r['win']
        g['ties'] += r['tie']
        g['losses'] += 1 - r['win'] - r['tie']
        g['score_delta'] += r['win'] + .5 * r['tie'] - c['win'] - .5 * c['tie']
        g['margin_sum'] += r['margin']
        errors.extend([dict(context=list(key), key=k, value=v) for k, v in r['telemetry'].items()
                       if v and ('error' in k or 'fallback' in k)])
    for g in groups.values():
        g['mean_margin'] = g.pop('margin_sum') / g['games']
    maximum = max(r['max_call_ms'] for r in selected)
    total = sum(g['score_delta'] for g in groups.values())
    mirror = groups.get(baseline)
    mirror_score = (mirror['wins'] + .5 * mirror['ties']) / mirror['games'] if mirror else None
    baseline_comparison = total > 0 and all(g['score_delta'] >= 0 for g in groups.values())
    runtime = not errors and (not latency or maximum < 1000)
    return dict(candidate=candidate, sha256=source, games=len(selected), per_opponent=groups, errors=errors,
                mirror_score=mirror_score, total_score_delta=total, max_call_ms=maximum,
                latency_required=latency, runtime_passed=runtime,
                baseline_comparison_passed=baseline_comparison,
                passed=runtime and baseline_comparison and (mirror_score is None or mirror_score >= .5))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('input')
    p.add_argument('--candidate', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--exploratory', action='store_true')
    a = p.parse_args()
    r = assess(a.input, a.candidate, latency=not a.exploratory)
    Path(a.output).write_text(json.dumps(r, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(r, indent=2))
    assert r['passed'], 'Frozen candidate failed acceptance criteria; do not export.'
