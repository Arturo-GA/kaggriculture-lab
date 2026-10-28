"""Send the verified Frontier13 archive once, or refresh its recorded submission status.

Use --submit only for Arturo's explicit request, quoting it with --authorization. Without --submit this is
read-only on Kaggle. An uncertain upload is never automatically repeated. --slot 2 records a second copy of the
same archive in the other tracked slot (its own receipt and intent files).
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--submit', action='store_true')
    p.add_argument('--authorization', default='', help="Arturo's words and date authorizing this upload")
    p.add_argument('--slot', type=int, default=1, choices=(1, 2))
    args = p.parse_args()
    root = Path('results/frontier13')
    verified = json.loads((root / 'kaggle_verified.json').read_text())
    assert verified['verified'] and verified['export_checks_passed']
    archive = root / 'kaggle/submission.tar.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == verified['archive_sha256']
    description = 'Frontier13 %s on cha22 127ed3e6' % verified['sha256'][:8] + (' - second slot' if args.slot == 2 else '')
    suffix = '' if args.slot == 1 else '_2'
    api = KaggleApi()
    api.authenticate()
    receipt_path = root / ('submission_receipt%s.json' % suffix)
    intent_path = root / ('submission_intent%s.json' % suffix)
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else None
    submissions = api.competition_submissions('kaggriculture') or []
    matches = [s for s in submissions if s and (s.ref == receipt['id'] if receipt else s.description == description)]
    if matches:
        s = matches[0]
        receipt = dict(receipt or {}, id=s.ref, status=str(s.status), description=s.description,
                       filename=s.file_name, public_score=s.public_score, error=s.error_description, date=str(s.date),
                       checked_utc=datetime.now(timezone.utc).isoformat(), archive_sha256=verified['archive_sha256'],
                       candidate_sha256=verified['sha256'], leaderboard_submitted=True)
        write(receipt_path, receipt)
        print(json.dumps(receipt, indent=2))
        return
    if receipt:
        print(json.dumps(receipt, indent=2))
        return
    if not args.submit:
        raise RuntimeError('No matching submission visible; no upload attempted.')
    assert args.authorization.strip(), 'Record the explicit authorization (--authorization) before uploading.'
    assert not intent_path.exists(), 'Earlier attempt has uncertain state. Inspect Kaggle before retrying; do not duplicate.'
    intent = dict(created_utc=datetime.now(timezone.utc).isoformat(), description=description,
                  archive_sha256=verified['archive_sha256'], candidate_sha256=verified['sha256'],
                  authorization=args.authorization)
    write(intent_path, intent)
    response = api.competition_submit(str(archive), description, 'kaggriculture', quiet=True)
    assert response.ref > 0, response.message
    receipt = dict(id=response.ref, status='SUBMITTED', message=response.message, description=description,
                   checked_utc=datetime.now(timezone.utc).isoformat(), archive_sha256=verified['archive_sha256'],
                   candidate_sha256=verified['sha256'], leaderboard_submitted=True, authorization=args.authorization)
    write(receipt_path, receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
