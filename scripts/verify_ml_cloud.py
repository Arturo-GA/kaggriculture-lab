"""Verify the downloaded archive, frozen source and cloud game receipts."""
import hashlib
import json
from pathlib import Path
import tarfile


def main():
    root=Path('results/ml/kaggle')
    receipt=json.loads((root/'results/ml/cloud_receipt.json').read_text())
    games=json.loads((root/'results/ml/cloud_games.json').read_text())
    assert receipt['passed'] and games['complete']
    assert games['engine']=='1.32.7' and len(games['rows'])==games['expected_games']==16
    source=(root/'main.py').read_bytes()
    assert source==Path('candidates/ml_critic.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()==receipt['source_sha256']
    archive=root/'submission.tar.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==receipt['archive_sha256']
    with tarfile.open(archive,'r:gz') as tf:
        assert tf.getnames()==['main.py']
        assert tf.extractfile('main.py').read()==source
    for row in games['rows']:
        assert row['status']==['DONE','DONE'] and row['steps']==720 and row['calls']==719
        assert not [(k,v) for k,v in row['telemetry'].items() if ('error' in k or 'fallback' in k) and v]
    selected=[r for r in games['rows'] if r['candidate']=='ml_critic']
    controls={(r['seed'],r['seat']):r for r in games['rows'] if r['candidate']=='matched6'}
    assert len(selected)==8 and len(controls)==8
    wins_delta=sum(r['win']-controls[r['seed'],r['seat']]['win'] for r in selected)
    assert wins_delta==receipt['win_delta'] and wins_delta>0
    assert max(r['max_call_ms'] for r in selected)<1000
    output=dict(verified=True,kernel='jarturo/kaggriculture-learned-option-critic',
                source_identical_to_frozen_local=True,
                leaderboard_submitted=False,**receipt)
    Path('results/ml/kaggle_verified.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    main()
