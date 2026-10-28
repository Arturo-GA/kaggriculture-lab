"""Send the verified Frontier5 archive once, or refresh its recorded submission status.

Use --submit only for Arturo's explicit request. Without it, this is read-only
on Kaggle. An uncertain upload is never automatically repeated.
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
    args = p.parse_args()
    root = Path('results/frontier5')
    verified = json.loads((root / 'kaggle_verified.json').read_text())
    assert verified['verified'] and verified['export_checks_passed']
    archive = root / 'kaggle/submission.tar.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == verified['archive_sha256']
    description = 'Frontier5 lockstep %s on V46' % verified['sha256'][:8]
    api = KaggleApi()
    api.authenticate()
    receipt_path = root / 'submission_receipt.json'
    intent_path = root / 'submission_intent.json'
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
    assert not intent_path.exists(), 'Earlier attempt has uncertain state. Inspect Kaggle before retrying; do not duplicate.'
    intent = dict(created_utc=datetime.now(timezone.utc).isoformat(), description=description,
                  archive_sha256=verified['archive_sha256'], candidate_sha256=verified['sha256'],
                  authorization='Arturo, 17 de septiembre de 2026: "prosigue porfavor" (enviar el archivo verificado de Frontier5)')
    write(intent_path, intent)
    response = api.competition_submit(str(archive), description, 'kaggriculture', quiet=True)
    assert response.ref > 0, response.message
    receipt = dict(id=response.ref, status='SUBMITTED', message=response.message, description=description,
                   checked_utc=datetime.now(timezone.utc).isoformat(), archive_sha256=verified['archive_sha256'],
                   candidate_sha256=verified['sha256'], leaderboard_submitted=True)
    write(receipt_path, receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
