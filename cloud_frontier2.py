"""Verify improved Frontier against its two deployed predecessors before export."""
import hashlib
import json
from pathlib import Path
from evaluate import run
from build import package


def main():
    release=json.loads(Path('results/frontier2/release.json').read_text());name=release['candidate']
    for n,h in release['source_sha256'].items():assert hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest()==h
    rows=run([name,'frontier'],['frontier','ml_critic'],release['cloud_seeds'],2,'results/frontier2/cloud_games.json')
    controls={(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']=='frontier'}
    selected=[r for r in rows if r['candidate']==name];groups={}
    for r in selected:
        c=controls[r['opponent'],r['seed'],r['seat']]
        g=groups.setdefault(r['opponent'],dict(games=0,wins=0,ties=0,losses=0,score_delta=0.))
        g['games']+=1;g['wins']+=r['win'];g['ties']+=r['tie'];g['losses']+=1-r['win']-r['tie']
        g['score_delta']+=r['win']+.5*r['tie']-c['win']-.5*c['tie']
    errors=[(r['opponent'],r['seed'],r['seat'],k,v) for r in selected for k,v in r['telemetry'].items()
            if ('error' in k or 'fallback' in k) and v]
    max_ms=max(r['max_call_ms'] for r in selected)
    passed=not errors and max_ms<1000 and sum(g['score_delta'] for g in groups.values())>0 and all(g['score_delta']>=0 for g in groups.values())
    receipt=dict(passed=passed,candidate=name,games=len(rows),per_opponent=groups,errors=errors,
                 max_call_ms=max_ms,source_sha256=release['source_sha256'][name],leaderboard_submitted=False)
    if passed:
        Path('main.py').write_bytes(Path('candidates',name+'.py').read_bytes());package(name,'submission.tar.gz')
        receipt['archive_sha256']=hashlib.sha256(Path('submission.tar.gz').read_bytes()).hexdigest()
    Path('results/frontier2/cloud_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)
    assert passed,'No archive exported: cloud improvement or runtime criterion failed'


if __name__=='__main__':main()
