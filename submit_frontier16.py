"""Submit the verified Frontier16 archive once; subsequent invocations only refresh its receipt."""
import argparse
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

ROOT=Path('results/frontier16/repaired')


def write(path,data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def main():
    p=argparse.ArgumentParser();p.add_argument('--submit',action='store_true');p.add_argument('--authorization',default='')
    args=p.parse_args()
    verified=json.loads((ROOT/'kaggle_verified.json').read_text())
    assert verified['verified'] and verified['export_checks_passed']
    private=json.loads((ROOT/'kaggle_private_verified.json').read_text())
    assert private['id']=='jarturo/kaggriculture-frontier16-queue' and private['is_private'] is True
    archive=ROOT/'kaggle/submission.tar.gz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==verified['archive_sha256']
    source=Path('candidates',verified['candidate']+'.py')
    assert hashlib.sha256(source.read_bytes()).hexdigest()==verified['sha256']
    description='Frontier16 %s (%s) on Idle Seller 03165654' % (verified['sha256'][:8],verified['candidate'])
    receipt_path=ROOT/'submission_receipt.json';intent_path=ROOT/'submission_intent.json'
    receipt=json.loads(receipt_path.read_text()) if receipt_path.exists() else None
    api=KaggleApi();api.authenticate()
    submissions=api.competition_submissions('kaggriculture') or []
    matches=[s for s in submissions if s and (s.ref==receipt['id'] if receipt else s.description==description)]
    if matches:
        s=matches[0]
        receipt=dict(receipt or {},id=s.ref,status=str(s.status),description=s.description,filename=s.file_name,
            public_score=s.public_score,error=s.error_description,date=str(s.date),checked_utc=datetime.now(timezone.utc).isoformat(),
            archive_sha256=verified['archive_sha256'],candidate_sha256=verified['sha256'],leaderboard_submitted=True)
        write(receipt_path,receipt);print(json.dumps(receipt,indent=2));return
    if receipt:print(json.dumps(receipt,indent=2));return
    if not args.submit:raise RuntimeError('No matching submission visible; no upload attempted.')
    assert args.authorization.strip(),'Record explicit user authorization before submitting.'
    assert not intent_path.exists(),'Earlier upload is uncertain. Inspect Kaggle; do not duplicate.'
    write(intent_path,dict(created_utc=datetime.now(timezone.utc).isoformat(),description=description,
        authorization=args.authorization,archive_sha256=verified['archive_sha256'],candidate_sha256=verified['sha256']))
    response=api.competition_submit(str(archive),description,'kaggriculture',quiet=True)
    assert response.ref>0,response.message
    receipt=dict(id=response.ref,status='SUBMITTED',message=response.message,description=description,
        checked_utc=datetime.now(timezone.utc).isoformat(),archive_sha256=verified['archive_sha256'],
        candidate_sha256=verified['sha256'],leaderboard_submitted=True,authorization=args.authorization)
    write(receipt_path,receipt);print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
