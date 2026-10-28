"""Final bounded development and fresh-seed holdout, with an authorized fallback."""
import argparse,random
from datetime import datetime,timezone
from pathlib import Path
from release_f20 import read,write,digest

ROOT=Path('results/frontier21')
AUTH='osea puede ser un poquito mejor vasta y si no puedes envia la que empata nomas'

def validate(data,names,opponents,seeds,hashes):
    rows=data['rows'];expected={(n,o,s,p) for n in names for o in opponents for s in seeds for p in (0,1)}
    assert data['complete'] and data['engine']=='1.32.7' and len(rows)==len(expected)
    assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in rows}==expected
    for r in rows:
        assert r['status']==['DONE','DONE'] and r['steps']==720 and r['calls']==719
        assert r['sha256']==hashes[r['candidate']] and r['opponent_sha256']==hashes[r['opponent']]
        assert r['margin']==r['rewards'][r['seat']]-r['rewards'][1-r['seat']]
        assert r['win']==int(r['margin']>0) and r['tie']==int(r['margin']==0)
    for n,h in hashes.items():assert digest(Path('candidates',n+'.py'))==h
    return rows

def points(r):return r['win']+.5*r['tie']
def errors(rows):return [r for r in rows if any(v and ('error' in k.lower() or 'fallback' in k.lower()) for k,v in r['telemetry'].items())]

def fallback(reason):
    assert not (ROOT/'release.json').exists()
    write(ROOT/'selection.json',dict(selected='f20_fill',mode='authorized_tied_fallback',reason=reason,
        authorization=AUTH,created_utc=datetime.now(timezone.utc).isoformat(),
        source_sha256=digest('candidates/f20_fill.py'),proof='results/frontier20/value_gate/holdout_summary.json',
        caveat='Tied149/160 point outcomes with f20_value; no demonstrated incremental improvement over that active agent. Passed the earlier paired gates against Market1 and Market2. Explicitly authorized as final fallback.'))

def prepare():
    p=read(ROOT/'development_plan.json');names=list(p['candidates'])+[p['control']]
    hashes=read('results/frontier20/value_gate/plan.json')['hashes']
    hashes.update({n:v['sha256'] for n,v in p['candidates'].items()})
    hashes={n:hashes[n] for n in set(names+p['opponents'])}
    rows=validate(read(ROOT/'development.json'),names,p['opponents'],p['seeds'],hashes)
    scores={n:sum(points(r) for r in rows if r['candidate']==n) for n in names}
    eligible=[n for n in p['candidates'] if scores[n]>scores[p['control']] and not errors([r for r in rows if r['candidate']==n])]
    eligible.sort(key=lambda n:(-scores[n],p['candidates'][n]['cap']))
    write(ROOT/'development_summary.json',dict(scores=scores,eligible=eligible,selected=eligible[:1],
        data_sha256=digest(ROOT/'development.json'),interpretation='Adaptive development on known earlier loss worlds, not independent validation.'))
    print('Development',scores,'selected',eligible[:1])
    if not eligible:fallback('Neither larger residual lot improved development win/tie points.');return
    assert not (ROOT/'holdout_plan.json').exists()
    name=eligible[0];opponents=p['opponents']+['n30b_lynnsakurai_2f6da4']
    write(ROOT/'holdout_plan.json',dict(candidate=name,control=p['control'],opponents=opponents,seeds=list(range(21101,21109)),
        seats=[0,1],engine='1.32.7',games=192,workers=5,created_utc=datetime.now(timezone.utc).isoformat(),
        hashes={n:digest(Path('candidates',n+'.py')) for n in set([name,p['control']]+opponents)},
        thresholds=dict(min_total_delta=2,min_nonmirror_delta=0,min_each_opponent_delta=-1,min_head_score=9,min_positive_seeds=3,max_call_ms=1000),
        authorization=AUTH,fallback='f20_fill if any criterion fails; user explicitly permits tied fallback.',
        caveat='Eight independent seed clusters and related public opponents; local improvements do not guarantee a leaderboard rating or medal.'))

def assess():
    p=read(ROOT/'holdout_plan.json');name=p['candidate'];control=p['control'];names=[name,control]
    rows=validate(read(ROOT/'holdout.json'),names,p['opponents'],p['seeds'],p['hashes'])
    by={n:{(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']==n} for n in names}
    delta={k:points(r)-points(by[control][k]) for k,r in by[name].items()}
    per_op={o:sum(d for k,d in delta.items() if k[0]==o) for o in p['opponents']}
    per_seed={s:sum(d for k,d in delta.items() if k[1]==s) for s in p['seeds']}
    direct=sum(points(r) for k,r in by[name].items() if k[0]==control)
    nonmirror=sum(d for o,d in per_op.items() if o not in (control,'f19_market2'))
    t=p['thresholds'];candidate=list(by[name].values())
    checks=dict(total_delta=sum(delta.values())>=t['min_total_delta'],nonmirror=nonmirror>=t['min_nonmirror_delta'],
        opponent_floor=min(per_op.values())>=t['min_each_opponent_delta'],direct_duels=direct>=t['min_head_score'],
        positive_worlds=sum(d>0 for d in per_seed.values())>=t['min_positive_seeds'],zero_errors=not errors(candidate),
        latency=max(r['max_call_ms'] for r in candidate)<t['max_call_ms'])
    rng=random.Random(20260930);values=list(per_seed.values());boot=sorted(sum(rng.choice(values) for _ in values) for _ in range(10000))
    report=dict(complete=True,games=len(rows),scores={n:sum(points(r) for r in by[n].values()) for n in names},
        checks=checks,pass_gate=all(checks.values()),delta=sum(delta.values()),nonmirror_delta=nonmirror,
        per_opponent_delta=per_op,per_seed_delta=per_seed,head_to_head=direct,paired_seed_bootstrap_95=[boot[250],boot[9750]],
        max_call_ms=max(r['max_call_ms'] for r in candidate),error_games=len(errors(candidate)),
        plan_sha256=digest(ROOT/'holdout_plan.json'),holdout_sha256=digest(ROOT/'holdout.json'))
    write(ROOT/'holdout_summary.json',report);print(__import__('json').dumps(report,indent=2))
    if report['pass_gate']:
        write(ROOT/'selection.json',dict(selected=name,mode='measured_improvement',authorization=AUTH,
            created_utc=datetime.now(timezone.utc).isoformat(),source_sha256=p['hashes'][name],proof=(ROOT/'holdout_summary.json').as_posix(),
            caveat=p['caveat']))
    else:fallback('New candidate failed one or more frozen fresh-seed criteria; preserve that result and use the user-authorized tied alternative.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['prepare','assess']);a=ap.parse_args()
    prepare() if a.mode=='prepare' else assess()
