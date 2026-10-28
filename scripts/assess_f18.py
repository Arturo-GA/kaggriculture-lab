"""Evaluate the predeclared F18 gate on the complete, hashed paired panel."""
import hashlib, json
from pathlib import Path
from research_top100 import write

ROOT=Path('results/frontier18')


def main():
    plan=json.loads((ROOT/'plan.json').read_text());report=json.loads((ROOT/'holdout.json').read_text())
    rows=report['rows'];control=plan['control'];names=plan['candidates']+[control];gate=plan['gate']
    expected={(c,o,s,p) for c in names for o in plan['opponents'] for s in plan['seeds'] for p in plan['seats']}
    assert report['complete'] and report['engine']=='1.32.7'
    assert len(rows)==len(expected)==plan['expected_games']
    assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in rows}==expected
    for n,h in plan['hashes'].items():assert hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest()==h
    for r in rows:
        assert r['sha256']==plan['hashes'][r['candidate']] and r['opponent_sha256']==plan['hashes'][r['opponent']]
        assert r['status']==['DONE','DONE'] and r['steps']==720 and r['calls']==719
        assert r['margin']==r['rewards'][r['seat']]-r['rewards'][1-r['seat']]
        assert r['win']==int(r['margin']>0) and r['tie']==int(r['margin']==0)
    score=lambda rs:sum(r['win']+.5*r['tie'] for r in rs)
    group={n:[r for r in rows if r['candidate']==n] for n in names}
    out=dict(complete=True,engine=report['engine'],games=len(rows),scores={n:score(group[n]) for n in names},candidates={},
             plan_sha256=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest(),
             holdout_sha256=hashlib.sha256((ROOT/'holdout.json').read_bytes()).hexdigest())
    base=group[control]
    for n in plan['candidates']:
        rs=group[n]
        per_op={o:score([r for r in rs if r['opponent']==o])-score([r for r in base if r['opponent']==o]) for o in plan['opponents']}
        per_seed={s:score([r for r in rs if r['seed']==s])-score([r for r in base if r['seed']==s]) for s in plan['seeds']}
        delta=score(rs)-score(base);nonmirror=sum(v for k,v in per_op.items() if k!=control)
        head=score([r for r in rs if r['opponent']==control])
        errors=[r for r in rs if any(v and ('error' in k.lower() or 'fallback' in k.lower()) for k,v in r['telemetry'].items())]
        max_ms=max(r['max_call_ms'] for r in rs)
        checks=dict(score_delta=delta>=gate['score_delta_min'],nonmirror=nonmirror>=gate['nonmirror_delta_min'],
                    opponent_floor=min(per_op.values())>=gate['per_opponent_floor'],head_to_head=head>=gate['head_to_head_score_min'],
                    positive_worlds=sum(v>0 for v in per_seed.values())>=gate['positive_seed_deltas_min'],
                    zero_errors=len(errors)==gate['errors'],latency=max_ms<gate['max_call_ms'])
        out['candidates'][n]=dict(pass_gate=all(checks.values()),checks=checks,score_delta=delta,nonmirror_delta=nonmirror,
            head_to_head_score=head,per_opponent_delta=per_op,per_seed_delta=per_seed,max_call_ms=max_ms,error_games=len(errors),
            wlt=[sum(r['win'] for r in rs),sum(r['margin']<0 for r in rs),sum(r['tie'] for r in rs)])
    out['both_pass']=all(r['pass_gate'] for r in out['candidates'].values())
    write(ROOT/'holdout_summary.json',out);print(json.dumps(out,indent=2))


if __name__=='__main__':main()
