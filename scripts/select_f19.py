"""Apply the frozen holdout criteria and deterministic, predeclared ranking."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

import assess_f18

ROOT = Path('results/frontier19')


def main():
    assert not (ROOT / 'selection_decision.json').exists(), 'Selection already frozen'
    assess_f18.ROOT = ROOT
    assess_f18.main()
    plan = json.loads((ROOT / 'plan.json').read_text())
    assessment = json.loads((ROOT / 'holdout_summary.json').read_text())
    rows = json.loads((ROOT / 'holdout.json').read_text())['rows']
    control = {(r['opponent'], r['seed'], r['seat']): r for r in rows if r['candidate'] == plan['control']}
    ranks = []
    for name in plan['candidates']:
        rs = [r for r in rows if r['candidate'] == name]
        gains = [r['margin'] - control[r['opponent'], r['seed'], r['seat']]['margin'] for r in rs]
        ranks.append(dict(candidate=name, pass_gate=assessment['candidates'][name]['pass_gate'],
                          score_delta=assessment['candidates'][name]['score_delta'],
                          mean_paired_margin_gain=mean(gains),
                          sha256=plan['hashes'][name]))
    eligible = sorted((r for r in ranks if r['pass_gate']),
                      key=lambda r: (-r['score_delta'], -r['mean_paired_margin_gain'], r['candidate']))
    selected = [r['candidate'] for r in eligible[:2]]
    source_plans = {n: (ROOT / 'plan.json').as_posix() for n in selected}
    supplement = None
    if len(selected) == 1:
        folder = ROOT / 'supplement'
        assert (folder / 'holdout_summary.json').exists(), 'Second-slot confirmation is still pending'
        supplemental_plan = json.loads((folder / 'plan.json').read_text())
        supplemental = json.loads((folder / 'holdout_summary.json').read_text())
        extra_rows = json.loads((folder / 'holdout.json').read_text())['rows']
        baseline = mean(r['margin'] for r in extra_rows if r['candidate'] == supplemental_plan['control'])
        extra_ranks = [dict(candidate=n, score_delta=r['score_delta'],
                           mean_paired_margin_gain=mean(x['margin'] for x in extra_rows if x['candidate'] == n) - baseline)
                       for n, r in supplemental['candidates'].items() if r['pass_gate']]
        extra_ranks.sort(key=lambda r: (-r['score_delta'], -r['mean_paired_margin_gain'], r['candidate']))
        if extra_ranks:
            name = extra_ranks[0]['candidate']
            selected.append(name)
            source_plans[name] = (folder / 'plan.json').as_posix()
        supplement = dict(ranking=extra_ranks,
                          plan_sha256=hashlib.sha256((folder / 'plan.json').read_bytes()).hexdigest(),
                          holdout_sha256=hashlib.sha256((folder / 'holdout.json').read_bytes()).hexdigest())
    decision = dict(selected=selected, source_plans=source_plans, supplement=supplement,
                    ranking=eligible, all_candidates=ranks,
                    decided_utc=datetime.now(timezone.utc).isoformat(),
                    plan_sha256=hashlib.sha256((ROOT / 'plan.json').read_bytes()).hexdigest(),
                    holdout_sha256=hashlib.sha256((ROOT / 'holdout.json').read_bytes()).hexdigest(),
                    authorization=plan['authorization'],
                    caveat='Sequential research campaign. First and supplemental panels have different fresh seeds and opponent counts; do not compare their raw win rates. Correlated public rivals and small money differences. No leaderboard rank prediction.')
    (ROOT / 'selection_decision.json').write_text(json.dumps(decision, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(decision, indent=2))
    if len(decision['selected']) != 2:
        raise RuntimeError('Fewer than two candidates passed. Do not relax this frozen gate or duplicate a submission.')


if __name__ == '__main__':
    main()
