"""Bundle the frozen Frontier8 source, its public control and opponents, and the official cloud verification."""
import base64
import hashlib
import json
import lzma
from pathlib import Path
from make_notebook import cell

KERNEL = 'jarturo/kaggriculture-frontier8-stack-lockstep'


def main():
    root = Path('results/frontier8')
    selected = json.loads((root / 'selection.json').read_text())
    name = selected['candidate']
    digest = hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest()
    assert digest == selected['sha256']
    plan = json.loads((root / 'plan.json').read_text())
    control = plan['control']
    receipts = {}
    for split in ('holdout', 'official'):
        path = root / (split + '_summary.json')
        r = json.loads(path.read_text())
        assert r['runtime_passed'] and r['baseline_comparison_passed'] and r['sha256'] == digest
        receipts[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    opponents = plan['cloud_opponents']
    names = [name, control] + [o for o in opponents if o != control]
    release = dict(candidate=name, kernel=KERNEL, control=control,
                   source_sha256={n: hashlib.sha256(Path('candidates', n + '.py').read_bytes()).hexdigest() for n in names},
                   cloud_opponents=opponents, cloud_seeds=plan['cloud_seeds'], local_receipts=receipts,
                   release_type='candidate', local_gate_passed=True,
                   gate='Paired against the strongest unmodified public agent of 19 September 2026 (Arlene, Farming Score '
                        'V2 = The 2945 Farm v9/4 + queue closure) on the same opponents, seeds and seats: positive total '
                        'paired score, no per-opponent regression, no reported errors or fallbacks, every callback below '
                        '1000 ms, and at least 50% score in the direct mirror against that control.',
                   attribution='Base agent: Thomas Tschinkel, The 2945 Farm v9/4 (Apache-2.0), with the upstream authors '
                               'credited in its source (Ahmed Berat Ozer, yhay81, prvsiyan, Dmitrii Gluzdov, aurax7, '
                               'tetsutani and others). Public layers stacked on it: Dmitrii Gluzdov, temporary opening wheat '
                               'crop (A Smaller Market Shock); Arlene (lynnsakurai), final effective-queue closure (Farming '
                               'Score V2). Kaggriculture Lab layer: lockstep sale ordering against a copy '
                               '(frontier5_lockstep.py).',
                   limitations='Local panels are small and dominated by public tape lineages; no rating or medal guarantee.')
    (root / 'release.json').write_text(json.dumps(release, indent=2) + '\n', encoding='utf-8')
    files = ['candidates/' + n + '.py' for n in names] + [
        'build.py', 'evaluate.py', 'frontier5_validation.py', 'cloud_frontier8.py',
        'results/frontier8/release.json', 'results/frontier8/holdout_summary.json',
        'results/frontier8/official_summary.json', 'results/frontier8/plan.json', 'LICENSE', 'NOTICE.md']
    payload = {n: Path(n).read_bytes().decode('utf-8') for n in files}
    encoded = base64.b64encode(lzma.compress(json.dumps(payload).encode('utf-8'), preset=9)).decode()
    cells = [cell('markdown', '# Kaggriculture — Frontier v8: capas públicas apiladas + Lockstep\n\n'
                  'Candidato construido sobre el agente público "The 2945 Farm" v9/4 de Thomas Tschinkel (Apache-2.0). '
                  'Apila dos capas públicas del 19 de septiembre (cultivo temporal de trigo en la apertura, de Dmitrii '
                  'Gluzdov; cierre efectivo de la cola de órdenes, de Arlene) y añade el ordenamiento lockstep de ventas de '
                  'Kaggriculture Lab: contra una copia reproduce la liquidación unidad a unidad del motor y conserva la '
                  'permutación de ventas con mejor margen modelado, sin añadir ni cambiar cantidades.\n\n'
                  'Este notebook reproduce partidas oficiales en la nube contra el mejor agente público sin modificar como '
                  'control emparejado y contra rivales públicos, exige ausencia de errores, latencia inferior a 1000 ms y '
                  'ninguna regresión por rival, y solo entonces escribe `submission.tar.gz`. No envía nada al leaderboard '
                  'automáticamente. No se promete rating ni medalla.\n'),
             cell('code', 'from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
                  f'payload=json.loads(lzma.decompress(base64.b64decode({encoded!r})))\n'
                  'for name,data in payload.items():\n    p=Path(name)\n    p.parent.mkdir(parents=True,exist_ok=True)\n'
                  '    p.write_bytes(data.encode("utf-8"))\nprint("extracted",len(payload),"files")\n'),
             cell('code', 'import importlib.metadata,subprocess,sys\n'
                  'if importlib.metadata.version("kaggle-environments") != "1.32.7":\n'
                  '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
                  'subprocess.run([sys.executable,"cloud_frontier8.py"],check=True)\n'),
             cell('code', 'from IPython.display import display,FileLink\n'
                  'print(Path("results/frontier8/cloud_receipt.json").read_text())\n'
                  'display(FileLink("submission.tar.gz"))\ndisplay(FileLink("main.py"))\n')]
    for c in cells:
        if c['cell_type'] == 'code':
            compile(''.join(c['source']), 'cell', 'exec')
    nb = dict(nbformat=4, nbformat_minor=5, cells=cells,
              metadata={'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                        'language_info': {'name': 'python', 'version': '3.12'}})
    data = (json.dumps(nb, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    assert len(data) < 1000000, len(data)
    out = Path('kaggle_frontier8')
    out.mkdir(exist_ok=True)
    (out / 'experiment.ipynb').write_bytes(data)
    metadata = dict(id=KERNEL, title='Kaggriculture Frontier8 Stack Lockstep', code_file='experiment.ipynb',
                    language='python', kernel_type='notebook', is_private=True, enable_gpu=False,
                    enable_internet=True, dataset_sources=[], competition_sources=['kaggriculture'], kernel_sources=[])
    (out / 'kernel-metadata.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    decoded = json.loads(lzma.decompress(base64.b64decode(encoded)))
    assert set(decoded) == set(files)
    for n, text in decoded.items():
        assert text.encode('utf-8') == Path(n).read_bytes()
    print(json.dumps(dict(notebook_bytes=len(data), release=release), indent=2))


if __name__ == '__main__':
    main()
