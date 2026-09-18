"""Verify the downloaded Kaggle archive, payload hashes and all cloud outcomes for Frontier7."""
import hashlib
import json
import tarfile
from pathlib import Path
from frontier5_validation import assess


def main():
    root = Path('results/frontier7')
    cloud = root / 'kaggle'
    release = json.loads((root / 'release.json').read_text())
    control = release['control']
    receipt = json.loads((cloud / 'results/frontier7/cloud_receipt.json').read_text())
    games = cloud / 'results/frontier7/cloud_games.json'
    report = json.loads(games.read_text())
    assert receipt['export_checks_passed'] and report['engine'] == '1.32.7'
    expected = {(c, o, s, p) for c in (release['candidate'], control) for o in release['cloud_opponents']
                for s in release['cloud_seeds'] for p in (0, 1)}
    assert len(report['rows']) == len(expected)
    assert {(r['candidate'], r['opponent'], r['seed'], r['seat']) for r in report['rows']} == expected
    recalculated = assess(games, release['candidate'], baseline=control)
    assert recalculated['runtime_passed'] and recalculated['baseline_comparison_passed']
    for key, value in recalculated.items():
        assert receipt[key] == value, key
    for r in report['rows']:
        assert r['sha256'] == release['source_sha256'][r['candidate']]
        assert r['opponent_sha256'] == release['source_sha256'][r['opponent']]
        assert r['status'] == ['DONE', 'DONE'] and r['calls'] == 719
    source = Path('candidates', release['candidate'] + '.py').read_bytes()
    assert source == (cloud / 'main.py').read_bytes()
    archive = cloud / 'submission.tar.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == receipt['archive_sha256']
    with tarfile.open(archive, 'r:gz') as tf:
        assert tf.getnames() == ['main.py'] and tf.extractfile('main.py').read() == source
    receipt['verified'] = True
    (root / 'kaggle_verified.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
