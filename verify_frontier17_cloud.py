"""Independently verify cloud games and the exact frozen Frontier17 archive."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tarfile

ROOT = Path('results/frontier17')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    cloud = ROOT / 'kaggle'
    release = json.loads((ROOT / 'release.json').read_text())
    plan = json.loads((ROOT / 'plan.json').read_text())
    receipt = json.loads((cloud / ROOT / 'cloud_receipt.json').read_text())
    games = cloud / ROOT / 'cloud_games.json'
    report = json.loads(games.read_text())
    name, control = plan['candidate'], plan['control']
    expected = {(c, o, s, p) for c in (name, control)
                for o in release['cloud_opponents']
                for s in release['cloud_seeds'] for p in (0, 1)}
    rows = report['rows']
    assert report['engine'] == '1.32.7' and report['complete']
    assert len(rows) == len(expected)
    assert {(r['candidate'], r['opponent'], r['seed'], r['seat'])
            for r in rows} == expected
    for r in rows:
        assert r['sha256'] == release['source_sha256'][r['candidate']]
        assert r['opponent_sha256'] == release['source_sha256'][r['opponent']]
        assert r['status'] == ['DONE', 'DONE'] and r['steps'] == 720 and r['calls'] == 719
        assert not any(v and ('error' in k.lower() or 'fallback' in k.lower())
                       for k, v in r['telemetry'].items())
    scores = {c: sum(r['win'] + .5 * r['tie'] for r in rows if r['candidate'] == c)
              for c in (name, control)}
    max_ms = max(r['max_call_ms'] for r in rows if r['candidate'] == name)
    assert max_ms < 1000 and scores[name] >= scores[control]
    assert receipt['cloud_gate_passed'] and receipt['scores'] == scores
    assert receipt['max_call_ms'] == max_ms and receipt['error_games'] == 0
    assert receipt['games'] == len(rows) and receipt['cloud_games_sha256'] == digest(games)
    assert json.loads((ROOT / 'holdout_summary.json').read_text())['pass_gate']
    for path, h in release['evidence_sha256'].items():
        assert digest(ROOT / path) == h and digest(cloud / ROOT / path) == h
    for candidate, h in release['source_sha256'].items():
        assert digest(Path('candidates', candidate + '.py')) == h
    source = Path('candidates', name + '.py').read_bytes()
    archive = cloud / 'submission.tar.gz'
    assert digest(archive) == receipt['archive_sha256']
    assert archive.read_bytes() == (ROOT / 'local/submission.tar.gz').read_bytes()
    with tarfile.open(archive, 'r:gz') as tf:
        assert tf.getnames() == ['main.py', 'LICENSE.txt', 'NOTICE.txt']
        assert all(m.isfile() for m in tf.getmembers())
        members = {n: tf.extractfile(n).read() for n in tf.getnames()}
    assert members['main.py'] == source
    assert receipt['source_sha256'] == release['source_sha256'][name]
    assert members['LICENSE.txt'] == Path('attribution/frontier16/LICENSE.txt').read_bytes()
    expected_notice = (Path('attribution/frontier16/NOTICE.txt').read_bytes() + b'\n\n'
                       + Path('attribution/frontier16/LAB_NOTICE.md').read_bytes() + b'\n\n'
                       + Path('attribution/frontier17/LAB_NOTICE.md').read_bytes())
    assert members['NOTICE.txt'] == expected_notice
    assert receipt['members_sha256'] == {
        n: hashlib.sha256(data).hexdigest() for n, data in members.items()}
    verified = dict(receipt, candidate=name, sha256=release['source_sha256'][name],
                    total_score_delta=scores[name] - scores[control], verified=True,
                    export_checks_passed=True, checked_utc=datetime.now(timezone.utc).isoformat())
    (ROOT / 'kaggle_verified.json').write_text(
        json.dumps(verified, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(verified, indent=2))


if __name__ == '__main__':
    main()
