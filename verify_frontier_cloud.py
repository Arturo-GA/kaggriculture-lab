"""Verify downloaded source, archive contents and independently recomputed outcomes."""
import hashlib
import json
from pathlib import Path
import tarfile


def main():
    root=Path('results/gold/kaggle')
    receipt=json.loads((root/'results/gold/frontier_cloud_receipt.json').read_text())
    games=json.loads((root/'results/gold/frontier_cloud_games.json').read_text())
    assert receipt['passed'] and games['complete'] and games['engine']=='1.32.7'
    assert len(games['rows'])==games['expected_games']==32
    source=Path('candidates/frontier.py').read_bytes()
    assert (root/'main.py').read_bytes()==source
    digest=hashlib.sha256(source).hexdigest();assert digest==receipt['source_sha256']
    archive=root/'submission.tar.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==receipt['archive_sha256']
    with tarfile.open(archive,'r:gz') as tf:
        assert tf.getnames()==['main.py'] and tf.extractfile('main.py').read()==source
    controls={(r['opponent'],r['seed'],r['seat']):r for r in games['rows'] if r['candidate']=='ml_critic'}
    selected=[r for r in games['rows'] if r['candidate']=='frontier'];assert len(selected)==len(controls)==16
    for r in games['rows']:
        assert r['status']==['DONE','DONE'] and r['steps']==720 and r['calls']==719
    for r in selected:
        assert r['sha256']==digest and r['max_call_ms']<1000
        assert not [(k,v) for k,v in r['telemetry'].items() if ('error' in k or 'fallback' in k) and v]
    for opponent in ('ml_critic','matched6'):
        group=[r for r in selected if r['opponent']==opponent]
        delta=sum(r['win']+.5*r['tie']-controls[r['opponent'],r['seed'],r['seat']]['win']
                  -.5*controls[r['opponent'],r['seed'],r['seat']]['tie'] for r in group)
        assert delta>=0 and delta==receipt['per_opponent'][opponent]['score_delta']
    output=dict(verified=True,kernel='jarturo/kaggriculture-frontier-joint-planner',
                source_identical_to_frozen_local=True,**receipt)
    Path('results/gold/frontier_kaggle_verified.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
