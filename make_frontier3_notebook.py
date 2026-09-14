"""Bundle exact checked source, attribution and official cloud verification."""
import base64
import hashlib
import json
import lzma
from pathlib import Path
from make_notebook import cell


def main():
    root=Path('results/frontier3');selected=json.loads((root/'selection.json').read_text())
    name=selected['candidate'];digest=hashlib.sha256(Path('candidates',name+'.py').read_bytes()).hexdigest()
    assert digest==selected['sha256']
    decision=json.loads((root/'release_decision.json').read_text())
    assert decision['candidate_sha256']==digest and decision['release_type']=='experimental'
    receipts={}
    for split in ('holdout','official'):
        path=root/(split+'_summary.json');r=json.loads(path.read_text())
        assert r['runtime_passed'] and r['baseline_comparison_passed'] and r['sha256']==digest
        receipts[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    plan=json.loads((root/'plan.json').read_text())
    names=[name,'frontier2_early','matched6','v41_review']
    release=dict(candidate=name,kernel='jarturo/kaggriculture-frontier-joint-planner',
        source_sha256={n:hashlib.sha256(Path('candidates',n+'.py').read_bytes()).hexdigest() for n in names},
        cloud_opponents=['v41_review','matched6','frontier2_early'],cloud_seeds=plan['cloud_seeds'],local_receipts=receipts,
        release_type='experimental',local_strategy_gate_passed=all(json.loads((root/(s+'_summary.json')).read_text())['passed'] for s in ('holdout','official')),
        review_decision=decision,
        gate='Original strategy gate remains >=50% versus V41. Experimental export decision made after the local official failure: require positive paired score versus Frontier2, no family regression, callbacks <1000ms, no reported errors or first-dawn hire shortfalls. Preserve the failed V41 gate; no claim of full acceptance.',
        attribution='Opening and cash/seed guards adapted from credited V41; own general-day integration and shared terminal capacity allocation. Old ML critic remains, not retrained.',
        limitations='Small, specific opponent panel; no rating or medal guarantee. Cargo retained at game end still has zero cash value.')
    (root/'release.json').write_text(json.dumps(release,indent=2)+'\n',encoding='utf-8')
    files=['candidates/'+n+'.py' for n in names]+['build.py','evaluate.py','frontier3_validation.py','cloud_frontier3.py',
        'results/frontier3/release.json','results/frontier3/holdout_summary.json','results/frontier3/official_summary.json','results/frontier3/plan.json','results/frontier3/release_decision.json','LICENSE','NOTICE.md']
    payload={n:base64.b64encode(Path(n).read_bytes()).decode() for n in files}
    encoded=base64.b64encode(lzma.compress(json.dumps(payload).encode())).decode()
    cells=[cell('markdown','# Kaggriculture — Frontier v3: Funded Opening\n\n'
        'Versión experimental con apertura comercial revisada, reserva de caja para la primera contratación '
        'diaria y validación de siembras según semillas disponibles. El cierre distribuye la capacidad '
        'compartida del almacén entre los trabajadores y conserva carga que no cabe.\n\n'
        'La apertura y protecciones de financiación proceden del V41 compartido por Arturo, con créditos '
        'a Ahmed Berat Ozer, Rayk Kretzschmar y los autores anteriores. La integración y asignación de '
        'capacidad son de Kaggriculture Lab. Se conserva el critic anterior sin reentrenamiento.\n\n'
        'Los resultados locales constan en el manifiesto. Este notebook añade 24 partidas oficiales '
        'contra V41, la primera submission y Frontier v2 antes de exportar. Retener carga no garantiza '
        'poder venderla antes del cierre. No se promete rating ni medalla.\n\n'
        '**Resultado adverso conservado:** 3/8 victorias oficiales locales contra V41; no se alcanzó '
        'el criterio predefinido de 50 %. Se publica como experimento por la mejora frente a nuestras '
        'versiones anteriores. La decisión de exportar es posterior a ese resultado y no convierte '
        'el criterio original en aprobado. No se ajustó el agente con las semillas reservadas.\n\n'
        'Este notebook crea el archivo de submission; no lo envía automáticamente al leaderboard.\n'),
        cell('code','from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
            f'payload=json.loads(lzma.decompress(base64.b64decode({encoded!r})))\n'
            'for name,data in payload.items():\n    p=Path(name)\n    p.parent.mkdir(parents=True,exist_ok=True)\n    p.write_bytes(base64.b64decode(data))\n'),
        cell('code','import importlib.metadata,subprocess,sys\n'
            'if importlib.metadata.version("kaggle-environments") != "1.32.7":\n'
            '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
            'subprocess.run([sys.executable,"cloud_frontier3.py"],check=True)\n'),
        cell('code','from IPython.display import display,FileLink\n'
            'print(Path("results/frontier3/cloud_receipt.json").read_text())\n'
            'display(FileLink("submission.tar.gz"))\ndisplay(FileLink("main.py"))\n')]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),'cell','exec')
    nb=dict(nbformat=4,nbformat_minor=5,cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'}})
    data=(json.dumps(nb,ensure_ascii=False,indent=1)+'\n').encode();assert len(data)<1000000
    out=Path('kaggle_frontier3');out.mkdir(exist_ok=True)
    (out/'experiment.ipynb').write_bytes(data)
    metadata=dict(id=release['kernel'],title='Kaggriculture Frontier Joint Planner',code_file='experiment.ipynb',
        language='python',kernel_type='notebook',is_private=True,enable_gpu=False,enable_internet=True,
        dataset_sources=[],competition_sources=['kaggriculture'],kernel_sources=[])
    (out/'kernel-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    # Independently decode and compare every embedded file before upload.
    decoded=json.loads(lzma.decompress(base64.b64decode(encoded)))
    assert set(decoded)==set(files)
    for name,data in decoded.items():assert base64.b64decode(data)==Path(name).read_bytes()
    print(json.dumps(dict(notebook_bytes=(out/'experiment.ipynb').stat().st_size,release=release),indent=2))


if __name__=='__main__':main()
