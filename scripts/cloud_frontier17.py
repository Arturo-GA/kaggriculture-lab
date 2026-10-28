"""Fresh Kaggle runtime check for the frozen F17, export only if it passes."""
import hashlib,json
from pathlib import Path
from evaluate import run
from pack_frontier17 import package,ROOT


def main():
    release=json.loads((ROOT/'release.json').read_text())
    plan=json.loads((ROOT/'plan.json').read_text());local=json.loads((ROOT/'holdout_summary.json').read_text())
    assert local['pass_gate']
    for name,h in release['source_sha256'].items():assert hashlib.sha256(Path('candidates',name+'.py').read_bytes()).hexdigest()==h
    for name,h in release['evidence_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
    name=plan['candidate'];control=plan['control'];seeds=release['cloud_seeds'];rivals=release['cloud_opponents']
    run([name,control],rivals,seeds,2,ROOT/'cloud_games.json')
    report=json.loads((ROOT/'cloud_games.json').read_text())
    expected={(c,o,s,p) for c in (name,control) for o in rivals for s in seeds for p in (0,1)}
    assert report['complete'] and report['engine']=='1.32.7'
    rows=report['rows'];assert len(rows)==len(expected)
    assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in rows}==expected
    errors=[]
    for r in rows:
        assert r['sha256']==release['source_sha256'][r['candidate']] and r['opponent_sha256']==release['source_sha256'][r['opponent']]
        assert r['status']==['DONE','DONE'] and r['steps']==720 and r['calls']==719
        if any(v and ('error' in k.lower() or 'fallback' in k.lower()) for k,v in r['telemetry'].items()):errors.append(r)
    scores={c:sum(r['win']+.5*r['tie'] for r in rows if r['candidate']==c) for c in (name,control)}
    max_ms=max(r['max_call_ms'] for r in rows if r['candidate']==name)
    passed=not errors and max_ms<1000 and scores[name]>=scores[control]
    receipt=dict(cloud_gate_passed=passed,scores=scores,max_call_ms=max_ms,error_games=len(errors),
        games=len(rows),source_sha256=release['source_sha256'],leaderboard_submitted=False,
        cloud_games_sha256=hashlib.sha256((ROOT/'cloud_games.json').read_bytes()).hexdigest())
    if passed:receipt.update(package('submission.tar.gz'))
    (ROOT/'cloud_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2));assert passed,'Cloud gate failed; no archive exported.'


if __name__=='__main__':main()
