"""Official-engine portability check and explicit experimental archive export."""
import hashlib
import json
from pathlib import Path
from build import package
from evaluate import run


def main():
    release=json.loads(Path('results/gold/frontier_release.json').read_text())
    for name,digest in release['source_sha256'].items():
        assert hashlib.sha256(Path('candidates',name+'.py').read_bytes()).hexdigest()==digest
    rows=run(['frontier','ml_critic'],['ml_critic','matched6'],release['cloud_seeds'],2,
             'results/gold/frontier_cloud_games.json')
    selected=[r for r in rows if r['candidate']=='frontier']
    controls={(r['opponent'],r['seed'],r['seat']):r for r in rows if r['candidate']=='ml_critic'}
    groups={}
    for r in selected:
        c=controls[r['opponent'],r['seed'],r['seat']]
        g=groups.setdefault(r['opponent'],dict(games=0,wins=0,ties=0,score_delta=0.))
        g['games']+=1;g['wins']+=r['win'];g['ties']+=r['tie']
        g['score_delta']+=r['win']+.5*r['tie']-c['win']-.5*c['tie']
    errors=[(r['opponent'],r['seed'],r['seat'],k,v) for r in selected for k,v in r['telemetry'].items()
            if ('error' in k or 'fallback' in k) and v]
    max_ms=max(r['max_call_ms'] for r in selected)
    passed=not errors and max_ms<1000 and all(g['score_delta']>=0 for g in groups.values())
    receipt=dict(passed=passed,candidate='frontier',games=len(rows),per_opponent=groups,errors=errors,
                 max_call_ms=max_ms,source_sha256=release['source_sha256']['frontier'],
                 leaderboard_submitted=False)
    if passed:
        Path('main.py').write_bytes(Path('candidates/frontier.py').read_bytes())
        package('frontier','submission.tar.gz')
        receipt['archive_sha256']=hashlib.sha256(Path('submission.tar.gz').read_bytes()).hexdigest()
    Path('results/gold/frontier_cloud_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)
    assert passed,'Cloud check failed; no archive exported'


if __name__=='__main__':main()
