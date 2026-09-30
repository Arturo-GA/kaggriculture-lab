"""Finish exactly the already-authorized first private release, with receipts."""
from datetime import datetime,timezone
import time
from release_f20 import ROOT,KERNEL,read,write,verify,submit
from admit_f20_experimental import AUTHORIZATION
from research_top100 import api,limited
from research_f16 import plain

def main():
    client=api()
    for _ in range(30):
        status=plain(limited(client.kernels_status,KERNEL))
        write(ROOT/'notebook_status.json',status)
        name=status['status']['name_']
        print('Private notebook:',name,flush=True)
        if name=='COMPLETE':break
        assert name in ('RUNNING','QUEUED'),status
        time.sleep(30)
    else:raise RuntimeError('Cloud verification not complete; no submission sent.')
    limited(client.kernels_output,KERNEL,path=str(ROOT/'kaggle'),file_pattern=r'.*(?:\.tar\.gz|\.json)$',force=True,quiet=True)
    verify()
    submit('f20_value',AUTHORIZATION)
    for _ in range(20):
        submit('f20_value',AUTHORIZATION) # Existing receipt: read-only reconciliation.
        receipt=read(ROOT/'f20_value_submission_receipt.json')
        active=plain(limited(client.competition_team_submissions,16639155))
        write(ROOT/'active_after_submission.json',dict(active=active,checked_utc=datetime.now(timezone.utc).isoformat()))
        if receipt['status'].endswith('.COMPLETE') and {s['id'] for s in active}=={receipt['id'],56714342}:
            print('SUBMISSION COMPLETE',receipt['id'],flush=True)
            return
        assert not receipt.get('error'),receipt
        time.sleep(30)
    raise RuntimeError('Submission already sent; reconcile its saved id without submitting again.')

if __name__=='__main__':main()
