"""Diagnostic ablation: only restore the V37 wheat opening in frozen V41."""
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path

source=Path('candidates/v41_review.py').read_bytes()
assert hashlib.sha256(source).hexdigest()=='8951ff93742015cba535b125223cf2e541bb7b602080fc4584f30c2613d210f3'
new=b"_R42_OPENING=[['BUY_PRODUCT', 'WHEAT', 5], ['BUY_PRODUCT', 'WHEAT', 10], ['SELL', 'WHEAT', 60]]"
old=b"_R42_OPENING=[['BUY_PRODUCT', 'WHEAT', 13], ['BUY_PRODUCT', 'WHEAT', 30], ['SELL', 'WHEAT', 30]]"
assert source.count(new)==1
data=source.replace(new,old)
Path('candidates/v41_old_opening.py').write_bytes(data)
plan=dict(created_utc=datetime.now(timezone.utc).isoformat(),scope='Post-hoc diagnostic ablation after observing V41 superiority; not fresh holdout, not a release candidate.',
    source_sha256=hashlib.sha256(data).hexdigest(),changed='Only _R42_OPENING: BUY 5/10, SELL 60 becomes BUY 13/30, SELL 30. All V41 guards and later policy remain.',
    candidates=['v41_review','v41_old_opening'],opponents=['frontier2_early'],seeds=list(range(92001,92005)),seats=[0,1],engine='official 1.32.7')
path=Path('results/review_v41/ablation_plan.json')
assert not path.exists()
path.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print(json.dumps(plan,indent=2))
