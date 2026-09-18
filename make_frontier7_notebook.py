"""Bundle the frozen Frontier7 source, its V48 control and opponents, and the official cloud verification."""
import base64
import hashlib
import json
import lzma
from pathlib import Path
from make_notebook import cell

KERNEL = 'jarturo/kaggriculture-frontier7-v48-lockstep'
CONTROL = 'v48'


def main():
    root = Path('results/frontier7')
    selected = json.loads((root / 'selection.json').read_text())
    name = selected['candidate']
    digest = hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest()
    assert digest == selected['sha256']
    receipts = {}
    for split in ('holdout', 'official'):
        path = root / (split + '_summary.json')
        r = json.loads(path.read_text())
        assert r['runtime_passed'] and r['baseline_comparison_passed'] and r['sha256'] == digest
        receipts[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    plan = json.loads((root / 'plan.json').read_text())
    opponents = plan['cloud_opponents']
    names = [name, CONTROL] + [o for o in opponents if o != CONTROL]
    release = dict(candidate=name, kernel=KERNEL, control=CONTROL,
                   source_sha256={n: hashlib.sha256(Path('candidates', n + '.py').read_bytes()).hexdigest() for n in names},
                   cloud_opponents=opponents, cloud_seeds=plan['cloud_seeds'], local_receipts=receipts,
                   release_type='candidate', local_gate_passed=True,
                   gate='Paired against the unmodified public V48 on the same opponents, seeds and seats: positive total '
                        'paired score, no per-opponent regression, no reported errors or fallbacks, every callback below '
                        '1000 ms, and at least 50% score in the direct V48 mirror.',
                   attribution='Base agent: Ahmed Berat Ozer V48 "Clear the Queue" (Apache-2.0), which carries V46, the '
                               'Seyit Kaan Gunes layers integrated in V47 and the upstream authors credited in its source. '
                               'Frontier7 binds the V48 entry point and appends the Kaggriculture Lab lockstep sale ordering '
                               '(replays the engine market per unit against a copy of our own orders and keeps the best '
                               'permutation of our SELL orders). The Kaggriculture Lab hold-and-release layer for milk and '
                               'wool was measured negative and is not part of this candidate.',
                   limitations='Local panels are small and dominated by public tape lineages; no rating or medal guarantee.')
    (root / 'release.json').write_text(json.dumps(release, indent=2) + '\n', encoding='utf-8')
    files = ['candidates/' + n + '.py' for n in names] + [
        'build.py', 'evaluate.py', 'frontier5_validation.py', 'cloud_frontier7.py',
        'results/frontier7/release.json', 'results/frontier7/holdout_summary.json',
        'results/frontier7/official_summary.json', 'results/frontier7/plan.json', 'LICENSE', 'NOTICE.md']
    payload = {n: Path(n).read_bytes().decode('utf-8') for n in files}
    encoded = base64.b64encode(lzma.compress(json.dumps(payload).encode('utf-8'), preset=9)).decode()
    cells = [cell('markdown', '# Kaggriculture — Frontier v7: V48 + Lockstep\n\n'
                  'Candidato construido sobre el V48 público de Ahmed Berat Özer (Apache-2.0; integra las capas de Seyit '
                  'Kaan Güneş publicadas en V47). Añade el ordenamiento lockstep de ventas de Kaggriculture Lab: cuando la '
                  'granja rival es una copia (similitud ≥ 0,90), reproduce la liquidación unidad a unidad del motor contra '
                  'nuestras propias órdenes y conserva la permutación de ventas con mejor margen modelado, sin añadir ni '
                  'cambiar cantidades. La capa propia de retención de leche y lana se midió negativa y no forma parte de '
                  'este candidato.\n\n'
                  'Este notebook reproduce partidas oficiales en la nube contra el V48 sin modificar como control emparejado '
                  'y contra rivales públicos, exige ausencia de errores, latencia inferior a 1000 ms y ninguna regresión por rival, '
                  'y solo entonces escribe `submission.tar.gz`. No envía nada al leaderboard automáticamente. '
                  'No se promete rating ni medalla.\n'),
             cell('code', 'from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
                  f'payload=json.loads(lzma.decompress(base64.b64decode({encoded!r})))\n'
                  'for name,data in payload.items():\n    p=Path(name)\n    p.parent.mkdir(parents=True,exist_ok=True)\n'
                  '    p.write_bytes(data.encode("utf-8"))\nprint("extracted",len(payload),"files")\n'),
             cell('code', 'import importlib.metadata,subprocess,sys\n'
                  'if importlib.metadata.version("kaggle-environments") != "1.32.7":\n'
                  '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
                  'subprocess.run([sys.executable,"cloud_frontier7.py"],check=True)\n'),
             cell('code', 'from IPython.display import display,FileLink\n'
                  'print(Path("results/frontier7/cloud_receipt.json").read_text())\n'
                  'display(FileLink("submission.tar.gz"))\ndisplay(FileLink("main.py"))\n')]
    for c in cells:
        if c['cell_type'] == 'code':
            compile(''.join(c['source']), 'cell', 'exec')
    nb = dict(nbformat=4, nbformat_minor=5, cells=cells,
              metadata={'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                        'language_info': {'name': 'python', 'version': '3.12'}})
    data = (json.dumps(nb, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    assert len(data) < 1000000, len(data)
    out = Path('kaggle_frontier7')
    out.mkdir(exist_ok=True)
    (out / 'experiment.ipynb').write_bytes(data)
    metadata = dict(id=KERNEL, title='Kaggriculture Frontier7 V48 Lockstep', code_file='experiment.ipynb',
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
