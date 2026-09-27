"""Summarize exactly reconstructed losses and the preregistered paired holdout."""
import hashlib,json
from collections import Counter
from pathlib import Path
from evaluate import write_json_atomic

ROOT=Path('results/frontier17')


def loss_summary():
    data=json.loads((ROOT/'replay_audit.json').read_text(encoding='utf-8'))
    assert data['complete'] and all(r['reproduced_exactly'] for r in data['rows'])
    rows=[]
    for r in data['rows']:
        if r['candidate']!='f16_repaired':continue
        s=r['seat'];o=1-s;led=r['money']
        items=sorted({k.split('_',1)[1] for m in led for k in m if k.startswith('SELL_')})
        net={}
        for item in items:
            mine=led[s].get('SELL_'+item,0)-led[s].get('BUY_PRODUCT_'+item,0)
            theirs=led[o].get('SELL_'+item,0)-led[o].get('BUY_PRODUCT_'+item,0)
            net[item]=dict(ours=mine,rival=theirs,delta=mine-theirs,
                sold_ours=r['units'][s].get('SELL_'+item,0),sold_rival=r['units'][o].get('SELL_'+item,0))
        capex=lambda m:sum(v for k,v in m.items() if not k.startswith(('SELL_','BUY_PRODUCT_')))
        expense_delta=capex(led[o])-capex(led[s])
        assert sum(v['delta'] for v in net.values())+expense_delta==r['margin']
        rows.append(dict(episode=r['id'],opponent=r['op_name'],opponent_team_rating_at_snapshot=r['op_score'],
            margin=r['margin'],net_by_item=net,capex_and_wage_advantage=expense_delta,
            same_counts_day15=r['snapshots']['360'][str(s)]['layout']==r['snapshots']['360'][str(o)]['layout'],
            same_counts_day27=r['snapshots']['648'][str(s)]['layout']==r['snapshots']['648'][str(o)]['layout'],
            own_physical=r['physical'][s]))
    losses=[r for r in rows if r['margin']<0]
    out=dict(exact_reproductions=len(data['rows']),f16_losses=len(losses),f16_small_wins=len(rows)-len(losses),
        losses_with_equal_counts_day15_and27=sum(r['same_counts_day15'] and r['same_counts_day27'] for r in losses),
        note='Same crop/animal counts is not identical coordinates or labor scheduling. Gross resale revenue is offset by input purchases. No financial causal attribution from revenue differences alone.',rows=rows)
    write_json_atomic(ROOT/'loss_summary.json',json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    return out


def holdout_summary():
    path=ROOT/'holdout.json'
    if not path.exists():return None
    d=json.loads(path.read_text(encoding='utf-8'));p=json.loads((ROOT/'plan.json').read_text(encoding='utf-8'))
    if not d['complete']:return dict(complete=False,done=len(d['rows']),expected=d['expected_games'])
    assert len(d['rows'])==p['expected_games']==d['expected_games']
    assert d['engine']=='1.32.7'
    for name,h in p['hashes'].items():assert hashlib.sha256(Path('candidates',name+'.py').read_bytes()).hexdigest()==h
    score=lambda r:r['win']+.5*r['tie']
    index={(r['candidate'],r['opponent'],r['seed'],r['seat']):r for r in d['rows']}
    assert len(index)==len(d['rows'])
    by=[];errors=[];seed_delta=Counter()
    for opponent in p['opponents']:
        pair=[]
        for seed in p['seeds']:
            for seat in p['seats']:
                a=index[p['candidate'],opponent,seed,seat];b=index[p['control'],opponent,seed,seat]
                for r in (a,b):
                    assert r['status']==['DONE','DONE'] and r['steps']==720 and r['calls']==719
                    assert r['sha256']==p['hashes'][r['candidate']] and r['opponent_sha256']==p['hashes'][opponent]
                    bad={k:v for k,v in r['telemetry'].items() if v and ('error' in k.lower() or 'fallback' in k.lower())}
                    if bad:errors.append(dict(candidate=r['candidate'],opponent=opponent,seed=seed,seat=seat,counters=bad))
                pair.append((a,b));seed_delta[seed]+=score(a)-score(b)
        record=dict(opponent=opponent,games=len(pair),candidate_score=sum(score(a) for a,b in pair),
            control_score=sum(score(b) for a,b in pair),candidate_wtl=[sum(a['win'] for a,b in pair),sum(a['tie'] for a,b in pair),sum(not(a['win'] or a['tie']) for a,b in pair)],
            control_wtl=[sum(b['win'] for a,b in pair),sum(b['tie'] for a,b in pair),sum(not(b['win'] or b['tie']) for a,b in pair)],
            candidate_mean_margin=sum(a['margin'] for a,b in pair)/len(pair),control_mean_margin=sum(b['margin'] for a,b in pair)/len(pair),
            lost_control_wins=sum(score(a)<score(b) for a,b in pair),gained=sum(score(a)>score(b) for a,b in pair))
        record['delta']=record['candidate_score']-record['control_score'];by.append(record)
    total=sum(r['delta'] for r in by);direct=next(r for r in by if r['opponent']==p['control'])
    nonmirror=total-direct['delta'];max_ms=max(r['max_call_ms'] for r in d['rows'] if r['candidate']==p['candidate'])
    g=p['gate'];checks=dict(total=total>=g['score_delta_min'],nonmirror=nonmirror>=g['nonmirror_delta_min'],
        families=all(r['delta']>=g['per_opponent_floor'] for r in by),direct=direct['candidate_score']/direct['games']>=g['head_to_head_score_min'],
        no_errors=not errors,runtime=max_ms<g['max_call_ms'])
    out=dict(complete=True,pass_gate=all(checks.values()),checks=checks,paired_score_delta=total,nonmirror_delta=nonmirror,
        candidate_score=sum(r['candidate_score'] for r in by),control_score=sum(r['control_score'] for r in by),
        games_per_agent=sum(r['games'] for r in by),independent_seeds=len(p['seeds']),max_call_ms=max_ms,
        seed_paired_deltas=dict(seed_delta),errors=errors,by_opponent=by)
    write_json_atomic(ROOT/'holdout_summary.json',json.dumps(out,indent=2)+'\n');return out


if __name__=='__main__':
    s=loss_summary();print(json.dumps({k:v for k,v in s.items() if k!='rows'},ensure_ascii=False))
    print(json.dumps(holdout_summary(),indent=2))
