"""Push one private final notebook, verify it, submit once, then reconcile."""
import time
from datetime import datetime,timezone
from pathlib import Path
from release_f21 import ROOT,KERNEL,read,write,digest,prepare,verify,submit
from research_top100 import api,limited
from research_f16 import plain

def main():
    if not (ROOT/'release.json').exists():prepare()
    client=api();intent=ROOT/'notebook_push_intent.json';pushed=ROOT/'notebook_push.json'
    if not pushed.exists():
        assert not intent.exists(),'Uncertain earlier push: reconcile the remote kernel before retrying.'
        write(intent,dict(kernel=KERNEL,created_utc=datetime.now(timezone.utc).isoformat(),authorization=read(ROOT/'selection.json')['authorization']))
        result=plain(client.kernels_push('kaggle_frontier21'));write(pushed,result)
        assert not result.get('error'),result
        print('Private notebook pushed',result,flush=True)
    limited(client.kernels_pull,KERNEL,path=str(ROOT/'remote_metadata'),metadata=True,quiet=True)
    metadata=read(ROOT/'remote_metadata'/'kernel-metadata.json')
    local=Path('kaggle_frontier21/experiment.ipynb');remote=ROOT/'remote_metadata'/metadata['code_file']
    cells=lambda p:[(c['cell_type'],''.join(c['source'])) for c in read(p)['cells']]
    assert metadata['id']==KERNEL and metadata['is_private'] is True and cells(local)==cells(remote)
    write(ROOT/'kaggle_private_verified.json',dict(id=metadata['id'],is_private=True,notebook_cells_match=True,
        local_sha256=digest(local),remote_sha256=digest(remote),version=read(pushed)['version_number'],
        checked_utc=datetime.now(timezone.utc).isoformat()))
    for _ in range(24):
        status=plain(limited(client.kernels_status,KERNEL));write(ROOT/'notebook_status.json',status)
        print('Notebook status',status['status']['name_'],flush=True)
        if status['status']['name_']=='COMPLETE':break
        assert status['status']['name_'] in ('RUNNING','QUEUED'),status
        time.sleep(20)
    else:raise RuntimeError('Cloud verification incomplete; no submission sent.')
    limited(client.kernels_output,KERNEL,path=str(ROOT/'kaggle'),file_pattern=r'.*(?:\.tar\.gz|\.json)$',force=True,quiet=True)
    verify();submit()
    for _ in range(20):
        submit() # Existing receipt: only reconcile, never send another POST.
        receipt=read(ROOT/'submission_receipt.json')
        active=plain(limited(client.competition_team_submissions,16639155))
        write(ROOT/'active_after_submission.json',dict(active=active,checked_utc=datetime.now(timezone.utc).isoformat()))
        if receipt['status'].endswith('.COMPLETE') and {s['id'] for s in active}=={receipt['id'],56719762}:
            print('FINAL SUBMISSION COMPLETE',receipt['id'],flush=True);return
        assert not receipt.get('error'),receipt
        time.sleep(20)
    raise RuntimeError('Submission already sent; reconcile its saved id, do not submit again.')

if __name__=='__main__':main()
