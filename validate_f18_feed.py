"""Fresh four-world validation of the loss-derived fix, against its frozen parent."""
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
from evaluate import run


def main():
    root=Path('results/frontier18/feed');root.mkdir(exist_ok=True)
    assert not (root/'plan.json').exists(),'Use resume_eval.py if interrupted.'
    candidates=['f18_feed'];control='f18_small'
    opponents=['f17_selected','f16_repaired','f17_robust','n25_abhinav0370_127ed3','n23_kenanzhang9_b52378','v43']
    seeds=list(range(18301,18305))
    plan=dict(registered_at=datetime.now(timezone.utc).isoformat(),candidates=candidates,control=control,opponents=opponents,
              seeds=seeds,seats=[0,1],expected_games=96,
              hashes={n:hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest() for n in sorted(set(candidates+[control]+opponents))},
              gate=dict(score_delta_min=1,nonmirror_delta_min=0,per_opponent_floor=-1,head_to_head_score_min=0,
                        positive_seed_deltas_min=1,errors=0,max_call_ms=1000),
              selection='One narrowly scoped starvation fix, frozen after diagnosis on live episode114306320 and before seeds18301..18304. Original loss is excluded from gate. Parent must also pass its broader 8-world panel.',
              limitations='Four worlds only; seats and related rival policies correlated. No rating prediction. No head-to-head gate because no direct parent opponent in this supplementary panel.')
    (root/'plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    run(candidates+[control],opponents,seeds,2,str(root/'holdout.json'))


if __name__=='__main__':main()
