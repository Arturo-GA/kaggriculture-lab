"""Export the locally accepted candidate with preserved attribution; do not claim cloud verification."""
import ast,base64,hashlib,json,lzma,tarfile
from pathlib import Path
from cloud_frontier16 import ROOT,package


def main():
    plan=json.loads((ROOT/'plan.json').read_text());gate=json.loads((ROOT/'holdout_summary.json').read_text())
    assert gate['registered_gate_passed']
    candidate=plan['candidate'];source=Path('candidates',candidate+'.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()==gate['sha256']==plan['hashes'][candidate]
    notebook=Path('kaggle_frontier16/experiment.ipynb');nb=json.loads(notebook.read_text(encoding='utf-8'))
    code=''.join(nb['cells'][1]['source']);tree=ast.parse(code)
    assign=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='payload' for t in n.targets))
    encoded=assign.value.args[0].args[0].args[0].value
    payload=json.loads(lzma.decompress(base64.b64decode(encoded)))
    for name,text in payload.items():assert text.encode('utf-8')==Path(name).read_bytes(),name
    assert payload['candidates/'+candidate+'.py'].encode('utf-8')==source
    out=ROOT/'local';out.mkdir(exist_ok=True);archive=out/'submission.tar.gz'
    hashes=package(candidate,archive)
    with tarfile.open(archive,'r:gz') as tf:
        assert tf.getnames()==['main.py','LICENSE.txt','NOTICE.txt']
        assert tf.extractfile('main.py').read()==source
        assert {n:hashlib.sha256(tf.extractfile(n).read()).hexdigest() for n in tf.getnames()}==hashes
    receipt=dict(candidate=candidate,source_sha256=gate['sha256'],local_gate_passed=True,
        cloud_verified=False,leaderboard_submitted=False,archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        archive_members_sha256=hashes,notebook_sha256=hashlib.sha256(notebook.read_bytes()).hexdigest(),
        notebook_bytes=notebook.stat().st_size,notebook_payload_files=list(payload),notebook_payload_verified=True,
        kaggle_upload_status='Blocked by automatic approval review; explicit authorization for this notebook and destination is required.')
    (ROOT/'local_package.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
