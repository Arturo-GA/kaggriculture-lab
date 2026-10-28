"""Verify the Kaggle run of the Frontier12 router: engine, row hashes (the kernel rebuilt the router from its parts), runtime,
paired results against the control; then package the archive locally from the identical candidate bytes.

The registered cloud rule (total > 0, no opponent below the control) is evaluated and reported; a shortfall on one opponent is
recorded as such in kaggle_verified.json instead of silently passing.  usage: verify_frontier12_cloud.py [--accept-shortfall]
"""
import hashlib
import json
import sys
import tarfile
from pathlib import Path
from build import package
from frontier5_validation import assess


def main():
    accept = '--accept-shortfall' in sys.argv
    root = Path('results/frontier12')
    cloud = root / 'kaggle'
    release = json.loads((root / 'release.json').read_text())
    name, control = release['candidate'], release['control']
    receipt = json.loads((cloud / 'results/frontier12/cloud_receipt.json').read_text())
    games = cloud / 'results/frontier12/cloud_games.json'
    report = json.loads(games.read_text())
    assert report['engine'] == '1.32.7' and report['complete']
    expected = {(c, o, s, p) for c in (name, control) for o in release['cloud_opponents'] for s in release['cloud_seeds'] for p in (0, 1)}
    assert len(report['rows']) == len(expected)
    assert {(r['candidate'], r['opponent'], r['seed'], r['seat']) for r in report['rows']} == expected
    recalculated = assess(games, name, baseline=control)
    for key, value in recalculated.items():
        assert receipt[key] == value, key
    assert recalculated['runtime_passed'], 'runtime failed in Kaggle'
    for r in report['rows']:
        assert r['sha256'] == release['source_sha256'][r['candidate']], (r['candidate'], 'hash')
        assert r['opponent_sha256'] == release['source_sha256'][r['opponent']], (r['opponent'], 'hash')
        assert r['status'] == ['DONE', 'DONE'] and r['calls'] == 719
    kernel_build = json.loads((cloud / 'results/frontier12/build.json').read_text())
    assert kernel_build['sha256'] == release['source_sha256'][name], 'the kernel rebuilt a different router'
    source = Path('candidates', name + '.py').read_bytes()
    assert hashlib.sha256(source).hexdigest() == release['source_sha256'][name]
    shortfalls = {o: g['score_delta'] for o, g in recalculated['per_opponent'].items() if g['score_delta'] < 0}
    baseline_ok = recalculated['baseline_comparison_passed']
    if not baseline_ok and not accept:
        raise SystemExit('cloud baseline rule failed on %s (total %+.1f); rerun with --accept-shortfall to record it' % (shortfalls, recalculated['total_score_delta']))
    archive = root / 'submission.tar.gz'
    package(name, archive)
    with tarfile.open(archive, 'r:gz') as tf:
        assert tf.getnames() == ['main.py'] and tf.extractfile('main.py').read() == source
    receipt.update(verified=True, archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(), archive_path=str(archive),
                   archive_built='locally from candidates/%s.py, byte-identical to the router the kernel rebuilt (hash checked)' % name,
                   cloud_baseline_rule_passed=baseline_ok, cloud_shortfalls=shortfalls,
                   accepted_shortfall=(not baseline_ok) and accept)
    (root / 'kaggle_verified.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: receipt[k] for k in ('runtime_passed', 'total_score_delta', 'mirror_score', 'max_call_ms', 'cloud_baseline_rule_passed', 'cloud_shortfalls', 'accepted_shortfall', 'archive_sha256')}, indent=2))


if __name__ == '__main__':
    main()
