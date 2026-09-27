"""Apply the recorded Frontier16 gates; preserve failures without relaxing thresholds."""
import argparse,hashlib,json
from pathlib import Path
from frontier5_validation import assess


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',default='results/frontier16/repaired');args=parser.parse_args()
    root=Path(args.root);plan=json.loads((root/'plan.json').read_text())
    report=json.loads((root/'holdout.json').read_text())
    names=[plan['candidate'],plan['control'],plan['public_base']]
    expected={(c,o,s,p) for c in names for o in plan['opponents'] for s in plan['holdout_seeds'] for p in (0,1)}
    assert report['engine']=='1.32.7' and report['complete']
    assert len(report['rows'])==len(expected)
    assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in report['rows']}==expected
    for r in report['rows']:
        assert r['sha256']==plan['hashes'][r['candidate']]
        assert r['opponent_sha256']==plan['hashes'][r['opponent']]
    candidate=plan['candidate'];gate=plan['gate']
    result=assess(root/'holdout.json',candidate,baseline=plan['control'])
    ablation=assess(root/'holdout.json',candidate,baseline=plan['public_base'])
    result['legacy_zero_regression_gate_passed']=result.pop('passed')
    result['legacy_zero_regression_baseline_passed']=result.pop('baseline_comparison_passed')
    target=result['per_opponent'][plan['public_base']]
    result['public_base_score']=(target['wins']+.5*target['ties'])/target['games']
    result['ablation_score_delta']=ablation['total_score_delta']
    result['ablation_per_opponent']={k:g['score_delta'] for k,g in ablation['per_opponent'].items()}
    result['ablation_mean_paired_margin']={o:sum(r['margin'] for r in report['rows'] if r['candidate']==candidate and r['opponent']==o)/target['games']-sum(r['margin'] for r in report['rows'] if r['candidate']==plan['public_base'] and r['opponent']==o)/target['games'] for o in plan['opponents']}
    result['gate_checks']=dict(runtime=result['runtime_passed'],total=result['total_score_delta']>=gate['total_min'],
        mirror=result['mirror_score']>=gate['mirror_min'],public_base=result['public_base_score']>=gate['public_base_min'],
        family_floor=all(g['score_delta']>=gate['opponent_floor'] for g in result['per_opponent'].values()),
        own_layer=ablation['total_score_delta']>=gate['ablation_min'])
    result['registered_gate_passed']=all(result['gate_checks'].values())
    # Clustered uncertainty: the independent unit is the seed, not its two seats.
    controls={(r['opponent'],r['seed'],r['seat']):r for r in report['rows'] if r['candidate']==plan['control']}
    per_seed={s:0. for s in plan['holdout_seeds']}
    for r in report['rows']:
        if r['candidate']!=candidate:continue
        c=controls[(r['opponent'],r['seed'],r['seat'])]
        per_seed[r['seed']]+=r['win']+.5*r['tie']-c['win']-.5*c['tie']
    result['paired_delta_by_seed']=per_seed
    result['independent_seed_count']=len(per_seed)
    (root/'holdout_summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
    assert result['registered_gate_passed'],'Frozen Frontier16 failed its original gate; do not claim acceptance.'


if __name__=='__main__':main()
