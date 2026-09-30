"""Fresh, smaller panel for the second slot after only Market2 passed round one."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from evaluate import run

ROOT = Path('results/frontier19/supplement')


def main():
    ROOT.mkdir(exist_ok=True)
    assert not (ROOT / 'plan.json').exists(), 'The supplemental plan is immutable'
    first = json.loads(Path('results/frontier19/holdout_summary.json').read_text())
    assert [n for n, r in first['candidates'].items() if r['pass_gate']] == ['f19_market2']
    parent = Path('candidates/f18_small.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == 'd9289a3e55624596ab5c2a8368359542e09249ae7fd64391d506bf82daeec135'
    raw = parent + b'\n' + Path('frontier18_feed.py').read_bytes() + b"\n_F19_MARKET_MODE='last'\n_F19_MARKET_DEPTH=1\n" + Path('frontier19_market.py').read_bytes()
    target = Path('candidates/f19_market1.py')
    assert not target.exists()
    compile(raw, str(target), 'exec')
    target.write_bytes(raw)
    candidates = ['f19_market1', 'f19_market8']
    opponents = ['f18_small', 'f17_selected', 'n30_lynnsakurai_031656']
    plan = dict(registered_at=datetime.now(timezone.utc).isoformat(),
                candidates=candidates, control='f18_small', opponents=opponents,
                seeds=list(range(19301, 19309)), seats=[0, 1], expected_games=144,
                hashes={n: hashlib.sha256(Path('candidates', n + '.py').read_bytes()).hexdigest()
                        for n in sorted(set(candidates + opponents))},
                gate=dict(score_delta_min=2, nonmirror_delta_min=-1, per_opponent_floor=-2,
                          head_to_head_score_min=9, positive_seed_deltas_min=3,
                          errors=0, max_call_ms=1000),
                selection='One candidate for the second slot, ranked by paired score gain then paired mean margin, after all criteria pass. The first slot remains the original passing Market2. No retuning on 19301..19308.',
                reason='Round one preserves the Robust failure (-3 against Lynn). Compare direct response and deeper iterative response in new worlds. The two weaker production rivals tied in round one and are omitted here to focus on the stronger relevant opponents.',
                limitations='This is an adaptive research campaign with multiple candidates; passing a later panel does not erase earlier failures or establish rating. Eight new seeds; correlated public families.',
                authorization='haz el mismo analisis para tener una estrategia que apunte al top 200-300 de la copetencia manda 2 plazas')
    (ROOT / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(plan, indent=2), flush=True)
    run(candidates + ['f18_small'], opponents, plan['seeds'], 5, ROOT / 'holdout.json')
    import assess_f18
    assess_f18.ROOT = ROOT
    assess_f18.main()


if __name__ == '__main__':
    main()
