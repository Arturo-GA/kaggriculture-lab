"""Verify downloaded Kaggle outputs against the evaluated local source."""
import hashlib
import json
import statistics
import tarfile
from pathlib import Path


def main():
    root = Path('results/kaggle')
    receipt = json.loads((root/'results/cloud_receipt.json').read_text())
    source = (root/'main.py').read_bytes()
    assert source == Path('candidates/matched6.py').read_bytes()
    assert hashlib.sha256(source).hexdigest() == receipt['source_sha256']
    archive = root/'submission.tar.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == receipt['archive_sha256']
    with tarfile.open(archive,'r:gz') as tf:
        assert tf.getnames() == ['main.py']
        assert tf.extractfile('main.py').read() == source
    batches = {}
    for name in ('screen','holdout','smoke'):
        data = json.loads((root/f'results/cloud_{name}.json').read_text())
        assert data['engine'] == '1.32.7'
        assert data['complete'] and len(data['rows']) == data['expected_games']
        assert all(r['status']==['DONE','DONE'] and r['steps']==720 for r in data['rows'])
        batches[name] = data['rows']
    matches = [r for r in batches['holdout'] if r['candidate']=='matched6']
    output = dict(kernel='jarturo/kaggriculture-lab-cpu-search',version=2,status='COMPLETE',
                  verified=True,counts={k:len(v) for k,v in batches.items()},
                  holdout_wins=sum(r['win'] for r in matches),holdout_games=len(matches),
                  holdout_mean_margin=statistics.mean(r['margin'] for r in matches),
                  max_call_ms=max(r['max_call_ms'] for batch in batches.values() for r in batch),
                  source_sha256=receipt['source_sha256'],archive_sha256=receipt['archive_sha256'],
                  source_identical_to_local=True,leaderboard_submitted=False)
    Path('results/kaggle_run.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    main()
