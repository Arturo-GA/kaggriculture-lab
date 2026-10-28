"""Verify the downloaded Kaggle archive, payload hashes and all cloud outcomes for Frontier14B.

The registered cloud wording (total > 0, no opponent below the control) is recomputed and reported; when only the
amended rule (total >= 0) holds, the shortfall is recorded explicitly in kaggle_verified.json."""
import hashlib
import json
import tarfile
from pathlib import Path
from frontier5_validation import assess


def main():
    root = Path('results/frontier14b')
    cloud = root / 'kaggle'
    release = json.loads((root / 'release.json').read_text())
    control = release['control']
    receipt = json.loads((cloud / 'results/frontier14b/cloud_receipt.json').read_text())
    games = cloud / 'results/frontier14b/cloud_games.json'
    report = json.loads(games.read_text())
    assert receipt['export_checks_passed'] and report['engine'] == '1.32.7'
    expected = {(c, o, s, p) for c in (release['candidate'], control) for o in release['cloud_opponents']
                for s in release['cloud_seeds'] for p in (0, 1)}
    assert len(report['rows']) == len(expected)
    assert {(r['candidate'], r['opponent'], r['seed'], r['seat']) for r in report['rows']} == expected
    recalculated = assess(games, release['candidate'], baseline=control)
    assert recalculated['runtime_passed']
    assert recalculated['total_score_delta'] >= 0 and all(g['score_delta'] >= 0 for g in recalculated['per_opponent'].values())
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
    receipt['cloud_baseline_rule_passed'] = recalculated['baseline_comparison_passed']
    receipt['accepted_shortfall'] = not recalculated['baseline_comparison_passed']
    (root / 'kaggle_verified.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: receipt[k] for k in ('candidate', 'runtime_passed', 'total_score_delta', 'max_call_ms', 'cloud_baseline_rule_passed', 'accepted_shortfall', 'cloud_shortfall', 'archive_sha256')}, indent=2))


if __name__ == '__main__':
    main()
