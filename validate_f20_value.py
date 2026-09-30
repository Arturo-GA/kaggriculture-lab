"""Second, explicitly adaptive candidate; preserve the first failed holdout."""
import argparse
from datetime import datetime,timezone
from pathlib import Path
import validate_f20 as base

ROOT=Path('results/frontier20/value_gate')
NAMES=['f20_value','f20_fill']

def prepare():
    ROOT.mkdir(parents=True,exist_ok=True);assert not (ROOT/'plan.json').exists()
    dev=base.read(Path('results/frontier20/value_development.json'))
    assert dev['complete'] and len(dev['rows'])==16
    original=base.read(Path('results/frontier20/plan.json'))
    plan=dict(original,created_utc=datetime.now(timezone.utc).isoformat(),candidates=NAMES,
        seeds=list(range(20201,20209)),
        development_selection={n:sum(base.points(r) for r in dev['rows'] if r['candidate']==n) for n in NAMES},
        adaptive_history='The first candidate failed its original nonmirror criterion against Market1. Seed20104 exposed unnecessary urgency while wool prices stayed flat. The new economic guard and the preexisting fill-only ablation tied4/8 in development on20002/20104, with different losses. These are NOT holdout seeds. Both are frozen as finalists; thresholds, opponents and eight-seed sample size stay unchanged, with new seeds20201-20208. Exactly one candidate may be submitted.',
        selection_rule='Among candidates passing every unchanged gate: highest total points, then highest nonmirror points, then prefer f20_fill because it preserves the existing physical production policy. No additional candidate selection by margin.',
        hashes={n:base.digest(Path('candidates',n+'.py')) for n in set(original['opponents']+NAMES)})
    plan.pop('candidate',None)
    base.write(ROOT/'plan.json',plan);print('Frozen',NAMES,plan['seeds'])

def assess():
    assert base.read(Path('results/frontier20/selection_decision.json'))['selected']==[]
    import random
    from statistics import mean
    assert not (ROOT/'selection_decision.json').exists()
    plan=base.read(ROOT/'plan.json');data=base.read(ROOT/'holdout.json');rows=data['rows']
    names=plan['candidates']+plan['controls']
    expected={(n,o,s,p) for n in names for o in plan['opponents'] for s in plan['seeds'] for p in plan['seats']}
    assert data['complete'] and data['engine']==plan['engine'] and len(rows)==len(expected)==640
    assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in rows}==expected
    for r in rows:
        assert r['sha256']==plan['hashes'][r['candidate']] and r['opponent_sha256']==plan['hashes'][r['opponent']]
        assert r['steps']==720 and r['calls']==719 and r['status']==['DONE','DONE']
        assert r['margin']==r['rewards'][r['seat']]-r['rewards'][1-r['seat']]
        assert r['win']==int(r['margin']>0) and r['tie']==int(r['margin']==0)
    for n,h in plan['hashes'].items():assert base.digest(Path('candidates',n+'.py'))==h
    totals={n:sum(base.points(r) for r in rows if r['candidate']==n) for n in names}
    by_op={n:{o:sum(base.points(r) for r in rows if r['candidate']==n and r['opponent']==o) for o in plan['opponents']} for n in names}
    candidates={};th=plan['thresholds']
    for name in plan['candidates']:
        cand=[r for r in rows if r['candidate']==name];comparisons={}
        for control in plan['controls']:
            indexed={(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']==control}
            gains={s:sum(base.points(r)-base.points(indexed[r['opponent'],r['seed'],r['seat']]) for r in cand if r['seed']==s) for s in plan['seeds']}
            rg=random.Random(20300930);values=list(gains.values());boot=sorted(sum(rg.choice(values) for _ in values) for _ in range(10000))
            comparisons[control]=dict(score_delta=totals[name]-totals[control],
                nonmirror_delta=sum(by_op[name][o]-by_op[control][o] for o in plan['opponents'] if o not in plan['controls']),
                per_opponent_delta={o:by_op[name][o]-by_op[control][o] for o in plan['opponents']},
                per_seed_delta=gains,positive_seeds=sum(v>0 for v in gains.values()),paired_seed_bootstrap_95=[boot[250],boot[9750]],
                mean_paired_margin_gain=mean(r['margin']-indexed[r['opponent'],r['seed'],r['seat']]['margin'] for r in cand))
        errors=[r for r in cand if any(v and ('error' in k.lower() or 'fallback' in k.lower()) for k,v in r['telemetry'].items())]
        checks=dict(total_delta=all(v['score_delta']>=th['min_total_delta'] for v in comparisons.values()),
            nonmirror=all(v['nonmirror_delta']>=th['min_nonmirror_delta'] for v in comparisons.values()),
            opponent_floor=all(min(v['per_opponent_delta'].values())>=th['min_each_opponent_delta'] for v in comparisons.values()),
            direct_duels=all(by_op[name][c]>=th['min_head_score'] for c in plan['controls']),
            positive_worlds=all(v['positive_seeds']>=th['min_positive_seeds'] for v in comparisons.values()),
            zero_errors=not errors,latency=max(r['max_call_ms'] for r in cand)<th['max_call_ms'])
        candidates[name]=dict(pass_gate=all(checks.values()),checks=checks,comparisons=comparisons,
            max_call_ms=max(r['max_call_ms'] for r in cand),error_games=len(errors),
            wlt=[sum(r['margin']>0 for r in cand),sum(r['margin']<0 for r in cand),sum(r['margin']==0 for r in cand)])
    summary=dict(complete=True,games=len(rows),scores=totals,per_opponent_scores=by_op,candidates=candidates,
        plan_sha256=base.digest(ROOT/'plan.json'),holdout_sha256=base.digest(ROOT/'holdout.json'))
    base.write(ROOT/'holdout_summary.json',summary)
    eligible=[n for n in NAMES if candidates[n]['pass_gate']]
    eligible.sort(key=lambda n:(totals[n],sum(by_op[n][o] for o in plan['opponents'] if o not in plan['controls']),n=='f20_fill'),reverse=True)
    decision=dict(selected=eligible[:1],eligible=eligible,source_plans={n:(ROOT/'plan.json').as_posix() for n in NAMES},
        decided_utc=datetime.now(timezone.utc).isoformat(),authorization=plan['authorization'],caveat=plan['caveat'],
        previous_failed_plan='results/frontier20/plan.json',adaptive_history=plan['adaptive_history'],selection_rule=plan['selection_rule'])
    base.write(ROOT/'selection_decision.json',decision)
    if decision['selected']:
        base.write(ROOT/'release_selection.json',decision)
        out=Path('results/frontier20/release_selection.json')
        if out.exists():
            existing=base.read(out)
            assert existing.get('validation_status')=='experimental_controls_pending_user_requested'
            # Preserve the first release and all frozen thresholds. Any second
            # submission needs a separate improvement check against that release.
            base.write(ROOT/'post_experimental_recommendation.json',dict(decision,
                already_released=existing['selected'],second_submission_authorized_only_if_improved=True))
        else:base.write(out,decision)
    print(__import__('json').dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','assess']);a=p.parse_args()
    prepare() if a.mode=='prepare' else assess()
