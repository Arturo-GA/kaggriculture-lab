"""Publish the verified delivery change as the next private Frontier version."""
import base64
import hashlib
import json
from pathlib import Path
import lzma
from make_notebook import cell


def main():
    root=Path('results/frontier2');choice=json.loads((root/'selection.json').read_text());name=choice['candidate']
    digest=hashlib.sha256(Path('candidates',name+'.py').read_bytes()).hexdigest();assert digest==choice['sha256']
    receipts={}
    for split in ('holdout','official'):
        path=root/(split+'_summary.json');summary=json.loads(path.read_text())['candidates'][name]
        assert summary['gate_passed'] and summary['candidate_sha256']==[digest]
        receipts[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    plan=json.loads((root/'plan.json').read_text())
    release=dict(candidate=name,kernel='jarturo/kaggriculture-frontier-joint-planner',
        source_sha256={n:hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest() for n in (name,'frontier','ml_critic')},
        cloud_seeds=plan['cloud_seeds'],local_receipts=receipts,
        cloud_rule='32 official games. Frontier2 and Frontier against Frontier and ml_critic in both seats. '
                   'Positive total paired score delta and no family regression, no reported errors, every call below 1000 ms.',
        limitation='Local improvements do not establish gold strength or guarantee higher live rating.')
    (root/'release.json').write_text(json.dumps(release,indent=2)+'\n')
    names=['candidates/'+n+'.py' for n in (name,'frontier','ml_critic')]+['build.py','evaluate.py','cloud_frontier2.py',
            'results/frontier2/release.json','LICENSE','NOTICE.md']
    payload={n:base64.b64encode(Path(n).read_bytes()).decode() for n in names}
    encoded=base64.b64encode(lzma.compress(json.dumps(payload).encode())).decode()
    cells=[cell('markdown','# Kaggriculture — Frontier: Early Delivery\n\n'
        'Esta versión entrega productos valiosos cuando una ruta pasa por el almacén y los vende '
        'en ese mismo turno. Conserva el fertilizante para tareas posteriores. También reconoce '
        'cultivos finitos maduros con rendimiento cero que todavía pueden regarse y cosecharse.\n\n'
        'El nuevo planificador se usa directamente: el selector anterior se entrenó para otra opción '
        'y no se reutiliza para decidir sobre esta. La producción de los días anteriores conserva '
        'la base pública V37 y las modificaciones atribuidas.\n\n'
        'Panel reservado: 109 victorias, 8 empates y 3 derrotas frente a 87, 24 y 9 del Frontier '
        'anterior, en 120 partidas por candidato. La mejora de resultados se concentra contra '
        'nuestras versiones anteriores; no demuestra fuerza de gold. Este notebook añade 32 '
        'partidas oficiales nuevas antes de exportar y no envía una submission automáticamente.\n\n'
        'Informe: https://github.com/Arturo-GA/kaggriculture-lab/blob/main/FRONTIER2_RESULTS.es.md\n'),
        cell('code','from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
             f'payload=json.loads(lzma.decompress(base64.b64decode({encoded!r})))\n'
             'for name,data in payload.items():\n    path=Path(name)\n    path.parent.mkdir(parents=True,exist_ok=True)\n    path.write_bytes(base64.b64decode(data))\n'),
        cell('code','import importlib.metadata,subprocess,sys\n'
             'if importlib.metadata.version("kaggle-environments") != "1.32.7":\n'
             '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
             'subprocess.run([sys.executable,"cloud_frontier2.py"],check=True)\n'),
        cell('code','from IPython.display import display,FileLink\n'
             'print(Path("results/frontier2/cloud_receipt.json").read_text())\n'
             'display(FileLink("submission.tar.gz"))\ndisplay(FileLink("main.py"))\n')]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),'cell','exec')
    out=Path('kaggle_frontier2');out.mkdir(exist_ok=True)
    nb=dict(nbformat=4,nbformat_minor=5,cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                                                           'language_info':{'name':'python','version':'3.12'}})
    data=(json.dumps(nb,ensure_ascii=False,indent=1)+'\n').encode()
    assert len(data)<1000000,'Kaggle limits notebook source size'
    (out/'experiment.ipynb').write_bytes(data)
    metadata=dict(id=release['kernel'],title='Kaggriculture Frontier Joint Planner',code_file='experiment.ipynb',
                  language='python',kernel_type='notebook',is_private=True,enable_gpu=False,enable_internet=True,
                  dataset_sources=[],competition_sources=['kaggriculture'],kernel_sources=[])
    (out/'kernel-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(release,indent=2))


if __name__=='__main__':main()
