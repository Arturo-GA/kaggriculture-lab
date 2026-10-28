"""Register an untouched paired panel before running the F18 market candidates."""
from datetime import datetime, timezone
import hashlib, json
from pathlib import Path
from evaluate import run

ROOT = Path('results/frontier18')


def main():
    path = ROOT/'plan.json'
    assert not path.exists(), 'Plan exists: use resume_eval.py for an interrupted run.'
    candidates = ['f18_small', 'f18_micro_robust']
    control = 'f17_selected'
    opponents = ['f17_selected', 'f16_repaired', 'f17_robust',
                 'n25_abhinav0370_127ed3', 'n23_kenanzhang9_b52378', 'v43']
    seeds = list(range(18101,18109))
    hashes = {n:hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest()
              for n in sorted(set(candidates+[control]+opponents))}
    plan = dict(registered_at=datetime.now(timezone.utc).isoformat(), candidates=candidates, control=control,
                opponents=opponents, seeds=seeds, seats=[0,1], expected_games=288, hashes=hashes,
                gate=dict(score_delta_min=4, nonmirror_delta_min=0, per_opponent_floor=-1,
                          head_to_head_score_min=9, positive_seed_deltas_min=3, errors=0, max_call_ms=1000),
                selection='Four exploration seeds 18001..18004. Freeze small-volume and two-scenario market approaches before fresh 18101..18108 worlds. No post-holdout tuning.',
                limitations='Six public or synthetic rival policies; eight independent worlds with correlated seats. Local score is wins plus half ties, not Kaggle rating. Private top100 code unavailable.')
    path.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    run(candidates+[control], opponents, seeds, 5, str(ROOT/'holdout.json'))


if __name__ == '__main__':
    main()
