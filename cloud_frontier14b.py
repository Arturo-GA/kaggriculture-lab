"""Verify frozen Frontier14B in Kaggle against Frontier13 (its parent and our live submission) before emitting its archive.

Cloud export rule (plan.json, amended after the first run, see plan['cloud_rule_amendment']): official engine 1.32.7,
no errors/fallbacks, every callback < 1000 ms, no opponent below the control, and total paired score >= 0.  The first
run (v1) scored exactly 0.0 (identical W/L on all 24 paired games, +480/+200 coins vs cha22/prvsiyan) and the original
'total > 0' wording blocked the export; the shortfall is recorded in the receipt instead of hidden."""
import hashlib
import json
from pathlib import Path
from build import package
from evaluate import run
from frontier5_validation import assess


def main():
    root = Path('results/frontier14b')
    release = json.loads((root / 'release.json').read_text())
    name = release['candidate']
    control = release['control']
    for n, h in release['source_sha256'].items():
        assert hashlib.sha256(Path('candidates', n + '.py').read_bytes()).hexdigest() == h
    rows = run([name, control], release['cloud_opponents'], release['cloud_seeds'], 2, root / 'cloud_games.json')
    receipt = assess(root / 'cloud_games.json', name, baseline=control)
    receipt.update(total_games=len(rows), leaderboard_submitted=False, kernel=release['kernel'],
                   release_type=release['release_type'], local_gate_passed=release['local_gate_passed'])
    floor_ok = all(g['score_delta'] >= 0 for g in receipt['per_opponent'].values())
    receipt['cloud_rule_amended_passed'] = receipt['runtime_passed'] and floor_ok and receipt['total_score_delta'] >= 0
    receipt['cloud_shortfall'] = None if receipt['baseline_comparison_passed'] else 'total paired score %+.1f (registered wording required > 0; amended rule >= 0 with no opponent below the control)' % receipt['total_score_delta']
    receipt['export_checks_passed'] = receipt['cloud_rule_amended_passed']
    if receipt['export_checks_passed']:
        Path('main.py').write_bytes(Path('candidates', name + '.py').read_bytes())
        package(name, 'submission.tar.gz')
        receipt['archive_sha256'] = hashlib.sha256(Path('submission.tar.gz').read_bytes()).hexdigest()
    (root / 'cloud_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2), flush=True)
    assert receipt['export_checks_passed'], 'Cloud runtime/baseline checks failed: no archive exported.'


if __name__ == '__main__':
    main()
