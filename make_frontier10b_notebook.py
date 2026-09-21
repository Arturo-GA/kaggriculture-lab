"""Bundle the frozen Frontier10B source, its public control and opponents, and the official cloud verification."""
import base64
import hashlib
import json
import lzma
from pathlib import Path
from make_notebook import cell

KERNEL = 'jarturo/kaggriculture-frontier10b-v53-lockstep'


def main():
    root = Path('results/frontier10b')
    selected = json.loads((root / 'selection.json').read_text())
    name = selected['candidate']
    digest = hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest()
    assert digest == selected['sha256']
    plan = json.loads((root / 'plan.json').read_text())
    control = plan['control']
    gate = json.loads((root / 'holdout_summary.json').read_text())
    # the gate registered in plan.json before the holdout ran
    minimum = 8  # registered in plan.json before the holdout
    assert gate['sha256'] == digest and gate['runtime_passed'] and gate['total_score_delta'] >= minimum and gate['mirror_score'] >= .5
    assert all(row['score_delta'] >= -2.0 for row in gate['per_opponent'].values())
    receipts = {'holdout_summary.json': hashlib.sha256((root / 'holdout_summary.json').read_bytes()).hexdigest()}
    opponents = plan['cloud_opponents']
    names = [name, control] + [o for o in opponents if o != control]
    release = dict(candidate=name, kernel=KERNEL, control=control,
                   source_sha256={n: hashlib.sha256(Path('candidates', n + '.py').read_bytes()).hexdigest() for n in names},
                   cloud_opponents=opponents, cloud_seeds=plan['cloud_seeds'], local_receipts=receipts,
                   release_type='candidate', local_gate_passed=True, gate=plan['rule'], attribution=plan['attribution'],
                   limitations='Local panels are small and dominated by public tape lineages; no rating or medal guarantee.')
    (root / 'release.json').write_text(json.dumps(release, indent=2) + '\n', encoding='utf-8')
    files = ['candidates/' + n + '.py' for n in names] + [
        'build.py', 'evaluate.py', 'frontier5_validation.py', 'cloud_frontier10b.py',
        'results/frontier10b/release.json', 'results/frontier10b/holdout_summary.json',
        'results/frontier10b/plan.json', 'LICENSE', 'NOTICE.md']
    payload = {n: Path(n).read_bytes().decode('utf-8') for n in files}
    encoded = base64.b64encode(lzma.compress(json.dumps(payload).encode('utf-8'), preset=9)).decode()
    cells = [cell('markdown', '# Kaggriculture — Frontier v10B: orden lockstep sobre V53\n\n'
                  'Candidato construido sobre el agente público Kaggriculture V53 de Ahmed Berat Özer (Apache-2.0). Enlaza su punto '
                  'de entrada público y añade la capa de Kaggriculture Lab que ordena nuestras ventas del turno contra una copia '
                  'con el precio exacto del motor, sin cambiar qué se vende ni cuándo.\n\n'
                  'Este notebook reproduce partidas oficiales en la nube contra el agente público sin modificar como control '
                  'emparejado y contra rivales públicos de la misma ola, exige ausencia de errores, latencia inferior a 1000 ms y la '
                  'puerta registrada en plan.json, y solo entonces escribe `submission.tar.gz`. No envía nada al leaderboard '
                  'automáticamente. No se promete rating ni medalla.\n'),
             cell('code', 'from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
                  f'payload=json.loads(lzma.decompress(base64.b64decode({encoded!r})))\n'
                  'for name,data in payload.items():\n    p=Path(name)\n    p.parent.mkdir(parents=True,exist_ok=True)\n'
                  '    p.write_bytes(data.encode("utf-8"))\nprint("extracted",len(payload),"files")\n'),
             cell('code', 'import importlib.metadata,subprocess,sys\n'
                  'if importlib.metadata.version("kaggle-environments") != "1.32.7":\n'
                  '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
                  'subprocess.run([sys.executable,"cloud_frontier10b.py"],check=True)\n'),
             cell('code', 'from IPython.display import display,FileLink\n'
                  'print(Path("results/frontier10b/cloud_receipt.json").read_text())\n'
                  'display(FileLink("submission.tar.gz"))\ndisplay(FileLink("main.py"))\n')]
    for c in cells:
        if c['cell_type'] == 'code':
            compile(''.join(c['source']), 'cell', 'exec')
    nb = dict(nbformat=4, nbformat_minor=5, cells=cells,
              metadata={'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                        'language_info': {'name': 'python', 'version': '3.12'}})
    data = (json.dumps(nb, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    assert len(data) < 1000000, len(data)
    out = Path('kaggle_frontier10b')
    out.mkdir(exist_ok=True)
    (out / 'experiment.ipynb').write_bytes(data)
    metadata = dict(id=KERNEL, title='Kaggriculture Frontier10B V53 Lockstep', code_file='experiment.ipynb',
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
