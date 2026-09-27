"""Deterministic export of an accepted F17; never calls Kaggle or submits."""
import gzip,hashlib,io,json,tarfile
from pathlib import Path

ROOT=Path('results/frontier17')


def package(output):
    plan=json.loads((ROOT/'plan.json').read_text())
    source=Path('candidates',plan['candidate']+'.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()==plan['hashes'][plan['candidate']]
    files={'main.py':source,'LICENSE.txt':Path('attribution/frontier16/LICENSE.txt').read_bytes(),
        'NOTICE.txt':Path('attribution/frontier16/NOTICE.txt').read_bytes()+b'\n\n'+Path('attribution/frontier16/LAB_NOTICE.md').read_bytes()+b'\n\n'+Path('attribution/frontier17/LAB_NOTICE.md').read_bytes()}
    raw=io.BytesIO()
    with tarfile.open(fileobj=raw,mode='w') as tf:
        for name,data in files.items():
            info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o644;info.mtime=0
            tf.addfile(info,io.BytesIO(data))
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as gz:gz.write(raw.getvalue())
    with tarfile.open(output,'r:gz') as tf:
        assert tf.getnames()==list(files)
        for name,data in files.items():assert tf.extractfile(name).read()==data
    return dict(archive_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
        source_sha256=hashlib.sha256(source).hexdigest(),members_sha256={n:hashlib.sha256(d).hexdigest() for n,d in files.items()})


def main():
    gate=json.loads((ROOT/'holdout_summary.json').read_text());assert gate['pass_gate']
    plan=json.loads((ROOT/'plan.json').read_text())
    receipt=package(ROOT/'local/submission.tar.gz')
    receipt.update(candidate=plan['candidate'],local_gate_passed=True,cloud_verified=False,leaderboard_submitted=False,
        note='Prepared locally. No notebook upload, notebook run or competition submission is performed by this script.')
    (ROOT/'local_package.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
