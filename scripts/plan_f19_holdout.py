"""Freeze candidate hashes and comparison criteria before observing new worlds."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from research_top100 import write
def main():
    root=Path('results/frontier19');path=root/'plan.json';assert not path.exists()
    candidates=['f19_market2','f19_robust','f19_balanced','f19_pressure'];control='f18_small'
    opponents=['f18_small','f17_selected','n30_lynnsakurai_031656','d25_tschinkel_b87a27','d25_boatlee_c4a696']
    plan=dict(registered_at=datetime.now(timezone.utc).isoformat(),candidates=candidates,control=control,
        opponents=opponents,seeds=list(range(19101,19109)),seats=[0,1],expected_games=400,
        hashes={n:hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest() for n in sorted(set(candidates+opponents+[control]))},
        gate=dict(score_delta_min=2,nonmirror_delta_min=-1,per_opponent_floor=-2,head_to_head_score_min=9,positive_seed_deltas_min=3,errors=0,max_call_ms=1000),
        selection='At most two locally promising policies by paired score improvement, then mean paired margin, provided they pass every criterion. No retuning on 19101..19108. Failures remain recorded.',
        limitations='Five reactive rivals include correlated public families. Eight independent seeds and correlated seats. Wins plus half ties are not Kaggle rating; no top200 guarantee. Public top200 replays are descriptive and frozen-rival tests are diagnostic only.',
        authorization='haz el mismo analisis para tener una estrategia que apunte al top 200-300 de la copetencia manda 2 plazas')
    write(path,plan);print(json.dumps(plan,indent=2))
if __name__=='__main__':main()
