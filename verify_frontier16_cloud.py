"""Recompute cloud checks and verify every archive member against frozen local bytes."""
import hashlib,json,tarfile
from pathlib import Path
from frontier5_validation import assess
from cloud_frontier16 import ROOT


def main():
    cloud=ROOT/'kaggle';release=json.loads((ROOT/'release.json').read_text())
    receipt=json.loads((cloud/ROOT/'cloud_receipt.json').read_text())
    games=cloud/ROOT/'cloud_games.json';report=json.loads(games.read_text())
    name=release['candidate'];control=release['control']
    expected={(c,o,s,p) for c in [name,control] for o in release['cloud_opponents'] for s in release['cloud_seeds'] for p in (0,1)}
    assert report['engine']=='1.32.7' and report['complete'] and len(report['rows'])==len(expected)
    assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in report['rows']}==expected
    check=assess(games,name,baseline=control);thresholds=release['cloud_gate']
    assert check['runtime_passed'] and check['total_score_delta']>=thresholds['total_min']
    assert all(g['score_delta']>=thresholds['opponent_floor'] for g in check['per_opponent'].values())
    assert receipt['export_checks_passed']
    for k,v in check.items():assert receipt[k]==v,k
    for r in report['rows']:
        assert r['sha256']==release['source_sha256'][r['candidate']]
        assert r['opponent_sha256']==release['source_sha256'][r['opponent']]
        assert r['status']==['DONE','DONE'] and r['calls']==719 and r['steps']==720
    for path,h in release['local_receipts'].items():assert hashlib.sha256((cloud/ROOT/path).read_bytes()).hexdigest()==h
    source=Path('candidates',name+'.py').read_bytes();assert source==(cloud/'main.py').read_bytes()
    archive=cloud/'submission.tar.gz';assert hashlib.sha256(archive.read_bytes()).hexdigest()==receipt['archive_sha256']
    with tarfile.open(archive,'r:gz') as tf:
        assert tf.getnames()==['main.py','LICENSE.txt','NOTICE.txt']
        members={n:tf.extractfile(n).read() for n in tf.getnames()}
    assert members['main.py']==source
    assert members['LICENSE.txt']==Path('attribution/frontier16/LICENSE.txt').read_bytes()
    expected_notice=Path('attribution/frontier16/NOTICE.txt').read_bytes()+b'\n\n--- Kaggriculture Lab modifications ---\n'+Path('attribution/frontier16/LAB_NOTICE.md').read_bytes()
    assert members['NOTICE.txt']==expected_notice
    assert receipt['archive_members_sha256']=={n:hashlib.sha256(data).hexdigest() for n,data in members.items()}
    receipt['verified']=True
    (ROOT/'kaggle_verified.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:receipt[k] for k in ['candidate','games','total_score_delta','max_call_ms','archive_sha256','verified']},indent=2))


if __name__=='__main__':main()
