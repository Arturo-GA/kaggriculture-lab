"""Build a separate private Kaggle kernel from a verified, frozen candidate."""
import base64
import hashlib
import json
from pathlib import Path
import zlib

from make_notebook import cell


def main():
    candidate = 'ml_critic'
    source_hash = hashlib.sha256(Path('candidates',candidate+'.py').read_bytes()).hexdigest()
    receipts = {}
    latency_path=Path('results/ml/latency_diagnosis.json')
    latency=json.loads(latency_path.read_text())
    assert latency['passed']
    assert all(r['sha256']==source_hash for r in latency['rows'] if r['candidate']==candidate)
    for split in ('holdout','official'):
        path=Path('results/ml',split+'_summary.json')
        summary=json.loads(path.read_text())['candidates'][candidate]
        assert summary['outcomes_gate_passed'] and summary['candidate_sha256']==[source_hash]
        if split=='official':assert summary['latency_gate_passed']
        receipts[split]=hashlib.sha256(path.read_bytes()).hexdigest()
    release=dict(candidate=candidate,source_sha256={name:hashlib.sha256(Path('candidates',name+'.py').read_bytes()).hexdigest()
                  for name in (candidate,'matched6')},local_receipts=receipts,
                  latency_diagnosis_sha256=hashlib.sha256(latency_path.read_bytes()).hexdigest(),
                  latency_resolution='Original parallel holdout latency failure retained. Frozen policy '
                                     'must pass serial reruns of slowest contexts AND official-engine timing; '
                                     'cloud must independently satisfy the same 1000 ms limit.',
                  cloud_seeds=[75001,75002,75003,75004],kernel='jarturo/kaggriculture-learned-option-critic')
    Path('results/ml/release_plan.json').write_text(json.dumps(release,indent=2)+'\n')
    names=['candidates/ml_critic.py','candidates/matched6.py','build.py','evaluate.py',
           'cloud_ml.py','results/ml/release_plan.json','LICENSE','NOTICE.md']
    payload={name:Path(name).read_text(encoding='utf-8') for name in names}
    encoded=base64.b64encode(zlib.compress(json.dumps(payload).encode())).decode()
    cells=[cell('markdown','# Kaggriculture — Learned Option Critic\n\n'
        'Modelo entrenado para decidir si conserva la política original o cambia la anticipación de ventas. '
        'Seleccionado con partidas separadas y confirmado localmente. Este notebook verifica el agente '
        'con el motor oficial en ocho duelos y ocho controles adicionales antes de exportar. '
        'No envía automáticamente al leaderboard. El bot exportado usa solo Python estándar.\n\n'
        'La mejora de victorias local se concentra frente a matched6; una opción fija de ocho turnos '
        'también es competitiva. Las pruebas locales no garantizan un rating superior. '
        'Código, fuentes, resultados y limitaciones: https://github.com/Arturo-GA/kaggriculture-lab\n'),
        cell('code','from pathlib import Path\nimport base64,json,zlib,os\nos.chdir("/kaggle/working")\n'
             f'payload=json.loads(zlib.decompress(base64.b64decode({encoded!r})))\n'
             'for name,source in payload.items():\n    path=Path(name)\n    path.parent.mkdir(parents=True,exist_ok=True)\n    path.write_bytes(source.encode("utf-8"))\n'),
        cell('code','import importlib.metadata,subprocess,sys\n'
             'if importlib.metadata.version("kaggle-environments") != "1.32.7":\n'
             '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
             'subprocess.run([sys.executable,"cloud_ml.py"],check=True)\n'),
        cell('code','from IPython.display import display,FileLink\n'
             'print(Path("results/ml/cloud_receipt.json").read_text())\n'
             'display(FileLink("submission.tar.gz"))\ndisplay(FileLink("main.py"))\n')]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),'notebook-cell','exec')
    notebook=dict(nbformat=4,nbformat_minor=5,cells=cells,
                  metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                            'language_info':{'name':'python','version':'3.12'}})
    out=Path('kaggle_ml');out.mkdir(exist_ok=True)
    (out/'experiment.ipynb').write_bytes((json.dumps(notebook,ensure_ascii=False,indent=1)+'\n').encode())
    metadata=dict(id=release['kernel'],title='Kaggriculture Learned Option Critic',code_file='experiment.ipynb',
                  language='python',kernel_type='notebook',is_private=True,enable_gpu=False,enable_internet=True,
                  dataset_sources=[],competition_sources=['kaggriculture'],kernel_sources=[])
    (out/'kernel-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(release,indent=2))


if __name__=='__main__':
    main()
