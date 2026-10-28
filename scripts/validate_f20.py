"""Freeze and assess one candidate against both active releases and a public league."""
import argparse,hashlib,json,random
from datetime import datetime,timezone
from pathlib import Path
from statistics import mean
from research_top100 import write

ROOT=Path('results/frontier20')
CANDIDATE='f20_delivery'
CONTROLS=['f19_market1','f19_market2']
OPPONENTS=CONTROLS+['n30b_lynnsakurai_2f6da4','n30b_haodou092_531a42',
    'n30b_haideptry_1eb093','n30b_evgendvorkin_8ddb01','n25_abhinav0370_127ed3',
    'n23_arsgorynich_4f8637','d25_llccqq624_c26402','d25_tschinkel_b87a27']

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def points(row):return row['win']+.5*row['tie']

def prepare():
    path=ROOT/'plan.json';assert not path.exists()
    # Selection among the two new delivery prototypes is already determined:
    # both completed all32 development games; 32 points beats31 points.
    dev=read(ROOT/'development.json')['rows']
    scores={n:sum(points(r) for r in dev if r['candidate']==n) for n in (CANDIDATE,'f20_woolfast')}
    assert all(sum(r['candidate']==n for r in dev)==32 for n in scores)
    assert scores[CANDIDATE]>scores['f20_woolfast']
    plan=dict(created_utc=datetime.now(timezone.utc).isoformat(),candidate=CANDIDATE,candidates=[CANDIDATE],controls=CONTROLS,control='f19_market2',
        opponents=OPPONENTS,seeds=list(range(20101,20109)),seats=[0,1],workers=5,engine='1.32.7',
        development_selection=scores,
        thresholds=dict(min_total_delta=4,min_nonmirror_delta=0,min_each_opponent_delta=-2,min_head_score=9,min_positive_seeds=3,max_call_ms=1000),
        hashes={n:digest(Path('candidates',n+'.py')) for n in set(OPPONENTS+[CANDIDATE])},
        authorization='Arturo: solo una submission privada; revisar todas las derrotas de las últimas dos submissions y enviar en cuanto haya una mejora validada.',
        caveat='Eight seeds are the independent clusters. Public opponents share ancestry; paired local gains and replay diagnostics do not assure a top300-400 rank or a silver medal.')
    write(path,plan);print(json.dumps(plan,indent=2))

def assess():
    assert not (ROOT/'selection_decision.json').exists()
    plan=read(ROOT/'plan.json');d=read(ROOT/'holdout.json');rows=d['rows']
    names=plan['candidates']+plan['controls'];expected={(c,o,s,p) for c in names for o in plan['opponents'] for s in plan['seeds'] for p in plan['seats']}
    assert d['complete'] and d['engine']==plan['engine'] and len(rows)==len(expected)
    assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in rows}==expected
    for r in rows:
        assert r['sha256']==plan['hashes'][r['candidate']] and r['opponent_sha256']==plan['hashes'][r['opponent']]
        assert r['steps']==720 and r['calls']==719 and r['status']==['DONE','DONE']
        assert r['margin']==r['rewards'][r['seat']]-r['rewards'][1-r['seat']]
        assert r['win']==int(r['margin']>0) and r['tie']==int(r['margin']==0)
    for n,h in plan['hashes'].items():assert digest(Path('candidates',n+'.py'))==h
    totals={n:sum(points(r) for r in rows if r['candidate']==n) for n in names}
    by_op={n:{o:sum(points(r) for r in rows if r['candidate']==n and r['opponent']==o) for o in plan['opponents']} for n in names}
    cand=[r for r in rows if r['candidate']==CANDIDATE];comparisons={}
    for control in plan['controls']:
        indexed={(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']==control}
        gains={s:sum(points(r)-points(indexed[r['opponent'],r['seed'],r['seat']]) for r in cand if r['seed']==s) for s in plan['seeds']}
        rg=random.Random(20300930);values=list(gains.values());boot=sorted(sum(rg.choice(values) for _ in values) for _ in range(10000))
        comparisons[control]=dict(score_delta=totals[CANDIDATE]-totals[control],
            nonmirror_delta=sum(by_op[CANDIDATE][o]-by_op[control][o] for o in plan['opponents'] if o not in plan['controls']),
            per_opponent_delta={o:by_op[CANDIDATE][o]-by_op[control][o] for o in plan['opponents']},
            per_seed_delta=gains,positive_seeds=sum(v>0 for v in gains.values()),
            paired_seed_bootstrap_95=[boot[250],boot[9750]],
            mean_paired_margin_gain=mean(r['margin']-indexed[r['opponent'],r['seed'],r['seat']]['margin'] for r in cand))
    th=plan['thresholds'];errors=[r for r in cand if any(v and ('error' in k.lower() or 'fallback' in k.lower()) for k,v in r['telemetry'].items())]
    checks=dict(total_delta=all(v['score_delta']>=th['min_total_delta'] for v in comparisons.values()),
        nonmirror=all(v['nonmirror_delta']>=th['min_nonmirror_delta'] for v in comparisons.values()),
        opponent_floor=all(min(v['per_opponent_delta'].values())>=th['min_each_opponent_delta'] for v in comparisons.values()),
        direct_duels=all(by_op[CANDIDATE][c]>=th['min_head_score'] for c in plan['controls']),
        positive_worlds=all(v['positive_seeds']>=th['min_positive_seeds'] for v in comparisons.values()),
        zero_errors=not errors,latency=max(r['max_call_ms'] for r in cand)<th['max_call_ms'])
    evidence=dict(pass_gate=all(checks.values()),checks=checks,comparisons=comparisons,max_call_ms=max(r['max_call_ms'] for r in cand),error_games=len(errors),
        wlt=[sum(r['margin']>0 for r in cand),sum(r['margin']<0 for r in cand),sum(r['margin']==0 for r in cand)])
    summary=dict(complete=True,games=len(rows),scores=totals,per_opponent_scores=by_op,candidates={CANDIDATE:evidence},
        plan_sha256=digest(ROOT/'plan.json'),holdout_sha256=digest(ROOT/'holdout.json'))
    write(ROOT/'holdout_summary.json',summary)
    selected=[CANDIDATE] if evidence['pass_gate'] else []
    decision=dict(selected=selected,source_plans={CANDIDATE:(ROOT/'plan.json').as_posix()},decided_utc=datetime.now(timezone.utc).isoformat(),
        authorization=plan['authorization'],caveat=plan['caveat'],validation_status={CANDIDATE:'passed_all_frozen_criteria' if selected else 'failed_frozen_criteria'})
    write(ROOT/'selection_decision.json',decision)
    if selected:write(ROOT/'release_selection.json',decision)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','assess']);a=p.parse_args()
    prepare() if a.mode=='prepare' else assess()
