"""Shared local/cloud acceptance checks for a frozen Frontier3 candidate."""
import argparse
import hashlib
import json
from pathlib import Path


def assess(path,candidate,baseline='frontier2_early',latency=True):
    report=json.loads(Path(path).read_text(encoding='utf-8'))
    assert report['complete'] and len(report['rows'])==report['expected_games']
    rows=report['rows'];selected=[r for r in rows if r['candidate']==candidate]
    controls={(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']==baseline}
    assert len(selected)==len(controls)>0
    assert {(r['opponent'],r['seed'],r['seat']) for r in selected}==set(controls)
    source=hashlib.sha256(Path('candidates',candidate+'.py').read_bytes()).hexdigest()
    groups={};errors=[]
    for r in selected:
        key=r['opponent'],r['seed'],r['seat'];c=controls[key]
        assert r['sha256']==source
        assert r['status']==['DONE','DONE'] and r['calls']==719 and r['steps']==720
        g=groups.setdefault(r['opponent'],dict(games=0,wins=0,ties=0,losses=0,score_delta=0.,margin_sum=0.))
        g['games']+=1;g['wins']+=r['win'];g['ties']+=r['tie'];g['losses']+=1-r['win']-r['tie']
        g['score_delta']+=r['win']+.5*r['tie']-c['win']-.5*c['tie'];g['margin_sum']+=r['margin']
        errors.extend([dict(context=list(key),key=k,value=v) for k,v in r['telemetry'].items()
            if v and ('error' in k or 'fallback' in k or k=='opening_day1_hire_shortfalls')])
    for g in groups.values():g['mean_margin']=g.pop('margin_sum')/g['games']
    v41=groups['v41_review'];v41_score=(v41['wins']+.5*v41['ties'])/v41['games']
    maximum=max(r['max_call_ms'] for r in selected)
    outcomes=not errors and sum(g['score_delta'] for g in groups.values())>0 and all(g['score_delta']>=0 for g in groups.values()) and v41_score>=.5
    runtime=not errors and (not latency or maximum<1000)
    baseline_comparison=sum(g['score_delta'] for g in groups.values())>0 and all(g['score_delta']>=0 for g in groups.values())
    return dict(candidate=candidate,sha256=source,games=len(selected),per_opponent=groups,errors=errors,
        v41_score=v41_score,max_call_ms=maximum,outcomes_passed=outcomes,
        latency_required=latency,passed=outcomes and (not latency or maximum<1000),
        runtime_passed=runtime,baseline_comparison_passed=baseline_comparison,
        v41_gate_passed=v41_score>=.5)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--candidate',required=True)
    p.add_argument('--output',required=True);p.add_argument('--exploratory',action='store_true');a=p.parse_args()
    r=assess(a.input,a.candidate,latency=not a.exploratory)
    Path(a.output).write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps(r,indent=2))
    assert r['passed'],'Frozen candidate failed acceptance criteria; do not export.'
