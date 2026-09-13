"""Verify exact artifact bytes and recompute paired cloud outcomes."""
import hashlib
import json
from pathlib import Path
import tarfile


def main():
    root=Path('results/frontier2/kaggle')
    receipt=json.loads((root/'results/frontier2/cloud_receipt.json').read_text())
    games=json.loads((root/'results/frontier2/cloud_games.json').read_text())
    assert receipt['passed'] and games['complete'] and games['engine']=='1.32.7'
    assert len(games['rows'])==games['expected_games']==32
    source=Path('candidates',receipt['candidate']+'.py').read_bytes()
    assert (root/'main.py').read_bytes()==source and hashlib.sha256(source).hexdigest()==receipt['source_sha256']
    archive=root/'submission.tar.gz';assert hashlib.sha256(archive.read_bytes()).hexdigest()==receipt['archive_sha256']
    with tarfile.open(archive,'r:gz') as tf:assert tf.getnames()==['main.py'] and tf.extractfile('main.py').read()==source
    controls={(r['opponent'],r['seed'],r['seat']):r for r in games['rows'] if r['candidate']=='frontier'}
    selected=[r for r in games['rows'] if r['candidate']==receipt['candidate']];assert len(selected)==len(controls)==16
    for r in games['rows']:assert r['status']==['DONE','DONE'] and r['steps']==720 and r['calls']==719
    deltas=[]
    for opponent in ('frontier','ml_critic'):
        group=[r for r in selected if r['opponent']==opponent]
        delta=sum(r['win']+.5*r['tie']-controls[r['opponent'],r['seed'],r['seat']]['win']
                  -.5*controls[r['opponent'],r['seed'],r['seat']]['tie'] for r in group)
        assert delta==receipt['per_opponent'][opponent]['score_delta'] and delta>=0;deltas.append(delta)
    assert sum(deltas)>0
    for r in selected:
        assert r['sha256']==receipt['source_sha256'] and r['max_call_ms']<1000
        assert not [(k,v) for k,v in r['telemetry'].items() if ('error' in k or 'fallback' in k) and v]
    output=dict(verified=True,kernel='jarturo/kaggriculture-frontier-joint-planner',**receipt)
    Path('results/frontier2/kaggle_verified.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
