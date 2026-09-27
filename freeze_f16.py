"""Freeze the exploration winner and register untouched holdout seeds before evaluation."""
import collections, datetime, hashlib, json
from pathlib import Path

ROOT=Path('results/frontier16')


def digest(name):
    return hashlib.sha256(Path('candidates',name+'.py').read_bytes()).hexdigest()


def main():
    assert not (ROOT/'plan.json').exists(), 'Do not overwrite a registered plan.'
    report=json.loads((ROOT/'variant_screen.json').read_text())
    assert report['complete']
    summary={}
    for r in report['rows']:
        g=summary.setdefault(r['candidate'],{}).setdefault(r['opponent'],dict(games=0,wins=0,ties=0,margin_sum=0))
        g['games']+=1;g['wins']+=r['win'];g['ties']+=r['tie'];g['margin_sum']+=r['margin']
    (ROOT/'screen_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    parent='f16_new_both'
    assert digest(parent)=='70419c322214bff4e11fbb8f79882eff8c9cf915eae4f9e783d8a2f39d645529'
    data=Path('candidates',parent+'.py').read_bytes()+b'\n'+Path('frontier16_observability.py').read_text(encoding='utf-8').encode()
    compile(data,'f16_selected','exec')
    Path('candidates/f16_selected.py').write_bytes(data)
    opponents=['f15_e81','n27_lynnsakurai_031656','g25_mooman0222_a62376','g25_mooman0222_baf0d3',
               'n23_arsgorynich_4f8637','n23_prvsiyan_178ae0','g25_wangyh_v44','n25_abhinav0370_127ed3',
               'n23_kenanzhang9_b52378','v43']
    plan=dict(registered_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate='f16_selected',control='f15_e81',
        public_base='n27_lynnsakurai_031656',screen_parent=parent,screen_parent_sha256=digest(parent),
        selection='Highest win-plus-half-tie score among six variants on exploration seeds 16001..16004; 15/16.',
        opponents=opponents,holdout_seeds=list(range(16101,16109)),cloud_seeds=list(range(16201,16205)),
        cloud_opponents=['f15_e81','n27_lynnsakurai_031656'],
        hashes={n:digest(n) for n in ['f16_selected']+opponents},
        gate=dict(total_min=6,mirror_min=.65,public_base_min=.5,opponent_floor=-2,ablation_min=0),
        cloud_gate=dict(total_min=0,opponent_floor=0,callback_max_ms=1000),
        rule='Official 1.32.7 engine, complete 720-step games, 719 callbacks, no recorded errors/fallbacks; callbacks <1000 ms. Paired W+0.5T versus F15 >=+6; direct F15 score >=65%; direct public base >=50%; no rival delta below -2; total delta versus unmodified public base >=0.',
        attribution='Apache-2.0 public Farmer John and the Idle Seller by lynnsakurai (03165654), inherited notices preserved; Arturo-GA original queue DP and integration of mooman0222 MIT E081 window-head idea.',
        limitations='Public lineage panel, only eight independent worlds; no calibrated mapping to live rating and no access to private top agents.')
    (ROOT/'plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    (ROOT/'selection.json').write_text(json.dumps(dict(candidate=plan['candidate'],sha256=digest(plan['candidate']),screen_parent=parent),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(candidate=plan['candidate'],sha256=digest(plan['candidate']),games=3*len(opponents)*8*2),indent=2))


if __name__=='__main__':main()
