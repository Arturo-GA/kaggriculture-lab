"""Assess the Frontier12 router holdout against the registered gate (two paired controls) and write summary + selection."""
import datetime, hashlib, json
from pathlib import Path
from frontier5_validation import assess

root = Path('results/frontier12')
plan = json.loads((root / 'plan.json').read_text(encoding='utf-8'))
name = plan['candidate']
controls = plan['controls']
rows = json.loads((root / 'holdout.json').read_text(encoding='utf-8'))['rows']
pts = lambda r: 1.0 if r['margin'] > 0 else (0.5 if r['margin'] == 0 else 0.0)
summary = assess(root / 'holdout.json', name, baseline=plan['control'])   # runtime, errors, latency, per-opponent vs the main control
totals = {}
per = {}
for c in [name] + controls:
    rs = [r for r in rows if r['candidate'] == c]
    totals[c] = sum(pts(r) for r in rs)
    d = {}
    for r in rs:
        d.setdefault(r['opponent'], []).append(pts(r))
    per[c] = {o: sum(v) for o, v in d.items()}
better = max(controls, key=lambda c: totals[c]); weaker = min(controls, key=lambda c: totals[c])
worst = {o: max(per[c][o] for c in controls) for o in per[name]}
gate = dict(
    total_vs_better=totals[name] - totals[better], total_vs_weaker=totals[name] - totals[weaker],
    total_ok=(totals[name] >= totals[better] + 4) and (totals[name] >= totals[weaker] + 8),
    per_opponent_ok=all(per[name][o] >= worst[o] - 2.0 for o in per[name]),
    per_opponent_shortfalls={o: per[name][o] - worst[o] for o in per[name] if per[name][o] < worst[o]},
    runtime_ok=summary['runtime_passed'], max_call_ms=summary['max_call_ms'], errors=summary['errors'])
gate['registered_gate_passed'] = gate['total_ok'] and gate['per_opponent_ok'] and gate['runtime_ok']
summary.update(totals=totals, per_opponent_points={c: per[c] for c in per}, controls=controls, better_control=better,
               registered_gate=gate, registered_gate_passed=gate['registered_gate_passed'])
(root / 'holdout_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
print('totals', totals, '| better control', better)
print(json.dumps({k: v for k, v in gate.items() if k != 'errors'}, indent=1))
if gate['registered_gate_passed']:
    sha = hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest()
    assert sha == plan['candidate_sha256'] == summary['sha256']
    sel = dict(candidate=name, sha256=sha, selected_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), version=plan.get('version'),
               basis='World/branch router (%s); registered gate passed on fresh seeds %s: %s points vs %s (%s) and %s (%s).' % (
                   plan.get('version'), plan['holdout_seeds'], totals[name], totals[controls[0]], controls[0], totals[controls[1]], controls[1]))
    (root / 'selection.json').write_text(json.dumps(sel, indent=2) + '\n', encoding='utf-8')
    print('selection written')
