"""Verify the frozen Frontier16 release in Kaggle and export only on its registered gate."""
import gzip,hashlib,io,json,tarfile
from pathlib import Path
from evaluate import run
from frontier5_validation import assess

ROOT=Path('results/frontier16/repaired')


def validate_games(path,release):
    report=json.loads(Path(path).read_text())
    expected={(c,o,s,p) for c in [release['candidate'],release['control']] for o in release['cloud_opponents'] for s in release['cloud_seeds'] for p in (0,1)}
    assert report['complete'] and report['engine']=='1.32.7' and len(report['rows'])==len(expected)
    assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in report['rows']}==expected
    for r in report['rows']:
        assert r['sha256']==release['source_sha256'][r['candidate']]
        assert r['opponent_sha256']==release['source_sha256'][r['opponent']]
        assert r['status']==['DONE','DONE'] and r['steps']==720 and r['calls']==719
    return report['rows']


def package(candidate,output):
    files={'main.py':Path('candidates',candidate+'.py').read_bytes(),
           'LICENSE.txt':Path('attribution/frontier16/LICENSE.txt').read_bytes(),
           'NOTICE.txt':Path('attribution/frontier16/NOTICE.txt').read_bytes()+b'\n\n--- Kaggriculture Lab modifications ---\n'+Path('attribution/frontier16/LAB_NOTICE.md').read_bytes()}
    raw=io.BytesIO()
    with tarfile.open(fileobj=raw,mode='w') as tf:
        for name,data in files.items():
            info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o644;info.mtime=0
            tf.addfile(info,io.BytesIO(data))
    with open(output,'wb') as out:
        with gzip.GzipFile(fileobj=out,mode='wb',mtime=0,filename='') as gz:gz.write(raw.getvalue())
    return {n:hashlib.sha256(data).hexdigest() for n,data in files.items()}


def main():
    release=json.loads((ROOT/'release.json').read_text());name=release['candidate'];control=release['control']
    for n,h in release['source_sha256'].items():
        assert hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest()==h
    for path,h in release['local_receipts'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h
    assert release['local_gate_passed']
    gate=json.loads((ROOT/'holdout_summary.json').read_text())
    assert gate['registered_gate_passed'] and gate['sha256']==release['source_sha256'][name]
    run([name,control],release['cloud_opponents'],release['cloud_seeds'],2,ROOT/'cloud_games.json')
    rows=validate_games(ROOT/'cloud_games.json',release)
    receipt=assess(ROOT/'cloud_games.json',name,baseline=control)
    thresholds=release['cloud_gate']
    passed=receipt['runtime_passed'] and receipt['total_score_delta']>=thresholds['total_min'] and all(
        g['score_delta']>=thresholds['opponent_floor'] for g in receipt['per_opponent'].values())
    export=passed
    receipt.update(total_games=len(rows),leaderboard_submitted=False,kernel=release['kernel'],
        cloud_gate_passed=passed,export_checks_passed=export,local_gate_passed=release['local_gate_passed'],
        validation_origin='Executed in this Kaggle notebook run',
        cloud_games_sha256=hashlib.sha256((ROOT/'cloud_games.json').read_bytes()).hexdigest())
    if export:
        Path('main.py').write_bytes(Path('candidates',name+'.py').read_bytes())
        receipt['archive_members_sha256']=package(name,'submission.tar.gz')
        receipt['archive_sha256']=hashlib.sha256(Path('submission.tar.gz').read_bytes()).hexdigest()
    (ROOT/'cloud_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2),flush=True)
    assert passed,'Registered cloud checks failed; no archive exported.'


if __name__=='__main__':main()
