"""Private experiment: joint final-day planning, with a learned abstention gate."""
import base64
import hashlib
import json
from pathlib import Path
import zlib
from make_notebook import cell


def main():
    digest=hashlib.sha256(Path('candidates/frontier.py').read_bytes()).hexdigest()
    receipts={}
    for split in ('holdout','official'):
        path=Path('results/gold','frontier_'+split+'_summary.json')
        summary=json.loads(path.read_text())['candidates']['frontier']
        assert summary['outcomes_gate_passed'] and summary['candidate_sha256']==[digest]
        if split=='official':assert summary['latency_gate_passed']
        receipts[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    latency=json.loads(Path('results/gold/frontier_latency.json').read_text())
    assert latency['passed'] and latency['source_sha256']==digest
    gold=json.loads(Path('results/gold/frontier_gold_holdout.json').read_text())
    assert gold['complete'] and all(r['source_sha256']==digest for r in gold['rows'] if r['candidate']=='frontier')
    release=dict(candidate='frontier',kernel='jarturo/kaggriculture-frontier-joint-planner',
        source_sha256={n:hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest() for n in ('frontier','ml_critic','matched6')},
        local_receipts=receipts,cloud_seeds=[87001,87002,87003,87004],
        cloud_rule='32 official games: frontier and ml_critic against ml_critic and matched6, both seats. '
                   'No per-family score regression, no reported errors, and every candidate call below 1000 ms.',
        status='experimental; local improvement is mainly against our own agent; no gold strength claim',
        latency_receipt_sha256=hashlib.sha256(Path('results/gold/frontier_latency.json').read_bytes()).hexdigest())
    Path('results/gold/frontier_release.json').write_text(json.dumps(release,indent=2)+'\n')
    names=['candidates/frontier.py','candidates/ml_critic.py','candidates/matched6.py','build.py','evaluate.py',
           'cloud_frontier.py','results/gold/frontier_release.json','LICENSE','NOTICE.md']
    # Preserve all frozen runtime bytes exactly across Windows and Kaggle Linux.
    payload={n:base64.b64encode(Path(n).read_bytes()).decode() for n in names}
    encoded=base64.b64encode(zlib.compress(json.dumps(payload).encode())).decode()
    cells=[cell('markdown','# Kaggriculture — Frontier Joint Planner\n\n'
        'Planificador propio de contratación, fertilizante, cosecha, rutas de regreso y prioridad de ventas '
        'del último día, construido sobre nuestra versión V37 + ML anterior. Un selector entrenado puede '
        'conservar el controlador anterior. Usa información observable; no lleva replays de rivales.\n\n'
        'La mejora local de victorias se concentra frente a nuestro agente anterior. El selector no ha '
        'demostrado más victorias que usar siempre el planificador. Analizamos partidas públicas del top 27; '
        'no conocemos su código privado y reproducir una secuencia no equivale a enfrentarse a su agente. '
        'No hay garantía de gold ni de mejora del rating.\n\n'
        'Este notebook ejecuta 32 partidas oficiales antes de exportar. No envía al leaderboard automáticamente. '
        'Fuentes y experimentos: https://github.com/Arturo-GA/kaggriculture-lab\n'),
        cell('code','from pathlib import Path\nimport base64,json,zlib,os\nos.chdir("/kaggle/working")\n'
             f'payload=json.loads(zlib.decompress(base64.b64decode({encoded!r})))\n'
             'for name,data in payload.items():\n    path=Path(name)\n    path.parent.mkdir(parents=True,exist_ok=True)\n    path.write_bytes(base64.b64decode(data))\n'),
        cell('code','import importlib.metadata,subprocess,sys\n'
             'if importlib.metadata.version("kaggle-environments") != "1.32.7":\n'
             '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
             'subprocess.run([sys.executable,"cloud_frontier.py"],check=True)\n'),
        cell('code','from IPython.display import display,FileLink\n'
             'print(Path("results/gold/frontier_cloud_receipt.json").read_text())\n'
             'display(FileLink("submission.tar.gz"))\ndisplay(FileLink("main.py"))\n')]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),'notebook-cell','exec')
    nb=dict(nbformat=4,nbformat_minor=5,cells=cells,metadata={
        'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
        'language_info':{'name':'python','version':'3.12'}})
    out=Path('kaggle_frontier');out.mkdir(exist_ok=True)
    (out/'experiment.ipynb').write_bytes((json.dumps(nb,ensure_ascii=False,indent=1)+'\n').encode())
    metadata=dict(id=release['kernel'],title='Kaggriculture Frontier Joint Planner',code_file='experiment.ipynb',
                  language='python',kernel_type='notebook',is_private=True,enable_gpu=False,enable_internet=True,
                  dataset_sources=[],competition_sources=['kaggriculture'],kernel_sources=[])
    (out/'kernel-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(release,indent=2))


if __name__=='__main__':main()
