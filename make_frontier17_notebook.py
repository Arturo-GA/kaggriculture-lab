"""Prepare a private notebook locally; uploading is a separate explicit action."""
import base64,hashlib,json,lzma
from pathlib import Path
from make_notebook import cell

ROOT=Path('results/frontier17')


def main():
    plan=json.loads((ROOT/'plan.json').read_text());gate=json.loads((ROOT/'holdout_summary.json').read_text())
    assert gate['pass_gate']
    names=[plan['candidate'],plan['control']]
    hashes={n:hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest() for n in names}
    assert all(h==plan['hashes'][n] for n,h in hashes.items())
    evidence=['plan.json','holdout_summary.json']
    release=dict(kernel='jarturo/kaggriculture-frontier17-input-market',source_sha256=hashes,
        cloud_opponents=[plan['control']],cloud_seeds=[17201,17202,17203,17204],
        cloud_rule='Official engine, complete games, zero reported errors, <1000ms, score no lower than F16 control.',
        evidence_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in evidence})
    (ROOT/'release.json').write_text(json.dumps(release,indent=2)+'\n',encoding='utf-8')
    files=['candidates/'+n+'.py' for n in names]+['evaluate.py','pack_frontier17.py','cloud_frontier17.py',
        'attribution/frontier16/LICENSE.txt','attribution/frontier16/NOTICE.txt','attribution/frontier16/LAB_NOTICE.md',
        'attribution/frontier17/LAB_NOTICE.md']+[str(ROOT/n).replace('\\','/') for n in evidence+['release.json']]
    payload={n:Path(n).read_bytes().decode('utf-8') for n in files}
    blob=base64.b64encode(lzma.compress(json.dumps(payload,ensure_ascii=False).encode('utf-8'),preset=9)).decode()
    cells=[cell('markdown','# Frontier17 — input-market search\n\nPrivate research candidate. '
        'Original Arturo-GA modifications remove selected cross-turn speculative pairs and search inventory-neutral '
        'input orders using visible own cash, inventory and public farm similarity. All inherited notices are retained. '
        'The local evaluation uses eight new seeds and eight opponents; recorded-rival diagnostics are not used '
        'as a competitive validation gate. No rating, medal or eligibility ruling is claimed.\n\n'
        'This notebook performs 16 fresh official-engine games against F16 and exports only on passing its checks. '
        'It never submits to the competition automatically.\n'),
        cell('code','from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
            f'payload=json.loads(lzma.decompress(base64.b64decode({blob!r})))\n'
            'for name,data in payload.items():\n    p=Path(name)\n    p.parent.mkdir(parents=True,exist_ok=True)\n    p.write_bytes(data.encode("utf-8"))\n'
            'print("Files extracted:",len(payload))\n'),
        cell('code','import importlib.metadata,subprocess,sys\n'
            'if importlib.metadata.version("kaggle-environments")!="1.32.7":\n'
            '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
            'subprocess.run([sys.executable,"cloud_frontier17.py"],check=True)\n'),
        cell('code','from IPython.display import display,FileLink\nprint(Path("results/frontier17/cloud_receipt.json").read_text())\n'
            'if Path("submission.tar.gz").exists():display(FileLink("submission.tar.gz"))\n')]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),'cell','exec')
    data=(json.dumps(dict(nbformat=4,nbformat_minor=5,cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'}}),indent=1,ensure_ascii=False)+'\n').encode()
    assert len(data)<1000000
    folder=Path('kaggle_frontier17');folder.mkdir(exist_ok=True);(folder/'experiment.ipynb').write_bytes(data)
    metadata=dict(id=release['kernel'],title='Kaggriculture Frontier17 input market',code_file='experiment.ipynb',language='python',
        kernel_type='notebook',is_private=True,enable_gpu=False,enable_internet=True,dataset_sources=[],competition_sources=['kaggriculture'],kernel_sources=[])
    (folder/'kernel-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    restored=json.loads(lzma.decompress(base64.b64decode(blob)))
    assert set(restored)==set(files)
    for n,s in restored.items():assert s.encode('utf-8')==Path(n).read_bytes()
    receipt=dict(kernel=release['kernel'],is_private=True,notebook_bytes=len(data),notebook_sha256=hashlib.sha256(data).hexdigest(),
        source_sha256=hashes,payload_verified=True,uploaded=False,cloud_verified=False,leaderboard_submitted=False)
    (ROOT/'notebook_prepared.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
