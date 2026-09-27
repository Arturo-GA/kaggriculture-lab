"""Bundle exact frozen sources and acceptance evidence in a private, self-contained notebook."""
import base64,hashlib,json,lzma
from pathlib import Path
from make_notebook import cell

ROOT=Path('results/frontier16/repaired')
KERNEL='jarturo/kaggriculture-frontier16-queue'


def main():
    plan=json.loads((ROOT/'plan.json').read_text())
    name=plan['candidate'];control=plan['control'];names=list(dict.fromkeys([name,control]+plan['cloud_opponents']))
    gate=json.loads((ROOT/'holdout_summary.json').read_text())
    assert gate['registered_gate_passed'] and gate['sha256']==plan['hashes'][name]
    hashes={n:hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest() for n in names}
    assert all(h==plan['hashes'][n] for n,h in hashes.items())
    evidence=['plan.json','holdout_summary.json']
    receipt_hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in evidence}
    release=dict(candidate=name,control=control,kernel=KERNEL,source_sha256=hashes,local_receipts=receipt_hashes,
        cloud_opponents=plan['cloud_opponents'],cloud_seeds=plan['cloud_seeds'],cloud_gate=plan['cloud_gate'],
        attribution=plan['attribution'],limitations=plan['limitations'],local_gate_passed=True)
    (ROOT/'release.json').write_text(json.dumps(release,indent=2)+'\n',encoding='utf-8')
    files=['candidates/'+n+'.py' for n in names]+['evaluate.py','frontier5_validation.py','cloud_frontier16.py',
        'NOTICE.md','attribution/frontier16/LICENSE.txt','attribution/frontier16/NOTICE.txt','attribution/frontier16/LAB_NOTICE.md']+[str(ROOT/n).replace('\\','/') for n in ['release.json']+evidence]
    payload={n:Path(n).read_bytes().decode('utf-8') for n in files}
    encoded=base64.b64encode(lzma.compress(json.dumps(payload,ensure_ascii=False).encode('utf-8'),preset=9)).decode()
    cells=[cell('markdown','# Kaggriculture — Frontier16: bounded market queue assignment\n\n'
        'Public base: Farmer John and the Idle Seller (lynnsakurai, Apache-2.0), with all inherited notices. '
        'Arturo-GA adds an original subset dynamic program for stock-covered sale slots, the attributed E081 '
        'window-head sale integration, a behavior-preserving empty-slot compatibility fix, and error observability.\n\n'
        'The frozen local holdout uses eight unseen seeds and ten opponents, including the unmodified public base '
        'as an ablation control. This notebook verifies fresh official-engine games and exports an archive only '
        'when its predeclared runtime and paired-score gates pass. No rating or medal is promised. '
        'It does not submit to the competition automatically.\n'),
        cell('code','from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
            f'payload=json.loads(lzma.decompress(base64.b64decode({encoded!r})))\n'
            'for name,data in payload.items():\n    p=Path(name)\n    p.parent.mkdir(parents=True,exist_ok=True)\n'
            '    p.write_bytes(data.encode("utf-8"))\nprint("extracted",len(payload),"files")\n'),
        cell('code','import importlib.metadata,subprocess,sys\n'
            'if importlib.metadata.version("kaggle-environments")!="1.32.7":\n'
            '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
            'subprocess.run([sys.executable,"cloud_frontier16.py"],check=True)\n'),
        cell('code','from IPython.display import display,FileLink\n'
            'print(Path("results/frontier16/repaired/cloud_receipt.json").read_text())\n'
            'if Path("submission.tar.gz").exists():display(FileLink("submission.tar.gz"))\n')]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),'cell','exec')
    nb=dict(nbformat=4,nbformat_minor=5,cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'}})
    data=(json.dumps(nb,ensure_ascii=False,indent=1)+'\n').encode('utf-8');assert len(data)<1000000,len(data)
    out=Path('kaggle_frontier16');out.mkdir(exist_ok=True);(out/'experiment.ipynb').write_bytes(data)
    meta=dict(id=KERNEL,title='Kaggriculture Frontier16 queue',code_file='experiment.ipynb',language='python',kernel_type='notebook',is_private=True,
        enable_gpu=False,enable_internet=True,dataset_sources=[],competition_sources=['kaggriculture'],kernel_sources=[])
    (out/'kernel-metadata.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    decoded=json.loads(lzma.decompress(base64.b64decode(encoded)))
    assert set(decoded)==set(files)
    for n,text in decoded.items():assert text.encode('utf-8')==Path(n).read_bytes()
    print(json.dumps(dict(notebook_bytes=len(data),candidate=name,sha256=hashes[name],kernel=KERNEL),indent=2))


if __name__=='__main__':main()
