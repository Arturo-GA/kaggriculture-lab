"""Bundle the frozen Frontier9 source, its public control and opponents, and the official cloud verification."""
import base64
import hashlib
import json
import lzma
from pathlib import Path
from make_notebook import cell

KERNEL = 'jarturo/kaggriculture-frontier9-preemption'


def main():
    root = Path('results/frontier9')
    selected = json.loads((root / 'selection.json').read_text())
    name = selected['candidate']
    digest = hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest()
    assert digest == selected['sha256']
    plan = json.loads((root / 'plan.json').read_text())
    control = plan['control']
    receipts = {}
    accepted = plan['round2']['accepted_regression']
    gate = json.loads((root / ('holdout2_summary_%s.json' % name)).read_text())
    assert gate['sha256'] == digest and gate['runtime_passed'] and gate['total_score_delta'] > 0 and gate['mirror_score'] >= .5
    for opponent, row in gate['per_opponent'].items():
        assert row['score_delta'] >= accepted.get(opponent, 0.0), opponent
    for fname in ('holdout2_summary_%s.json' % name, 'replication_v48_lineage_summary.json'):
        receipts[fname] = hashlib.sha256((root / fname).read_bytes()).hexdigest()
    opponents = plan['cloud_opponents']
    names = [name, control] + [o for o in opponents if o != control]
    release = dict(candidate=name, kernel=KERNEL, control=control,
                   source_sha256={n: hashlib.sha256(Path('candidates', n + '.py').read_bytes()).hexdigest() for n in names},
                   cloud_opponents=opponents, cloud_seeds=plan['cloud_seeds'], local_receipts=receipts,
                   release_type='candidate', local_gate_passed=True,
                   gate='Paired against our deployed Frontier8 agent (f8_stack_lock) on the same opponents, seeds and seats on '
                        'the official engine: positive total paired score, no per-opponent regression, no reported errors or '
                        'fallbacks, every callback below 1000 ms, and at least 50% score in the direct mirror against Frontier8.',
                   attribution='Base: Frontier8 = Thomas Tschinkel, The 2945 Farm v9/4 (Apache-2.0) and its upstream authors, with the '
                               'public layers of Dmitrii Gluzdov (opening wheat crop) and Arlene/lynnsakurai (queue closure) and the '
                               'Kaggriculture Lab lockstep ordering. Frontier9 adds one Lab change: bounded pre-emption of glutted '
                               'strawberry, milk and wool lots inside the public RACEGATE reservation (window min(4, lot / town drain), taking the whole stock of the item). '
                               'A one-day carrot feed reserve, a longer window, a best-response sale scheduler and an adaptive window were measured and are not part of this candidate.',
                   known_regression='Against the V48-lineage sale-policy agents (alperen_first, alperen_rhythm) the candidate is about one world in sixteen worse than Frontier8 (measured on the holdout and replicated on 16 fresh seeds). The strict no-regression criterion therefore failed on one opponent; Arturo decides.',
                   limitations='Local panels are small and dominated by public tape lineages; no rating or medal guarantee.')
    (root / 'release.json').write_text(json.dumps(release, indent=2) + '\n', encoding='utf-8')
    files = ['candidates/' + n + '.py' for n in names] + [
        'build.py', 'evaluate.py', 'frontier5_validation.py', 'cloud_frontier9.py',
        'results/frontier9/release.json', 'results/frontier9/holdout2_summary_%s.json' % name,
        'results/frontier9/replication_v48_lineage_summary.json', 'results/frontier9/plan.json', 'LICENSE', 'NOTICE.md']
    payload = {n: Path(n).read_bytes().decode('utf-8') for n in files}
    encoded = base64.b64encode(lzma.compress(json.dumps(payload).encode('utf-8'), preset=9)).decode()
    cells = [cell('markdown', '# Kaggriculture — Frontier v9: adelanto acotado de ventas\n\n'
                  'Candidato construido sobre Frontier8 (agente público The 2945 Farm v9/4 de Thomas Tschinkel, Apache-2.0, con las '
                  'capas públicas de Dmitrii Gluzdov y Arlene y el orden lockstep de Kaggriculture Lab). Añade un cambio propio: '
                  'los lotes de fresa, leche y lana que la capa pública RACEGATE retiene en un libro saturado pueden venderse '
                  'hasta min(4, lote / drenaje del pueblo) turnos antes del turno de la ruta, llevando todo el stock del producto, para no ser adelantados por rivales '
                  'con la misma ruta.\n\n'
                  'Este notebook reproduce partidas oficiales en la nube contra Frontier8 como control emparejado y contra rivales '
                  'públicos, exige ausencia de errores, latencia inferior a 1000 ms y ninguna regresión por rival, y solo entonces '
                  'escribe `submission.tar.gz`. No envía nada al leaderboard automáticamente. No se promete rating ni medalla.\n'),
             cell('code', 'from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
                  f'payload=json.loads(lzma.decompress(base64.b64decode({encoded!r})))\n'
                  'for name,data in payload.items():\n    p=Path(name)\n    p.parent.mkdir(parents=True,exist_ok=True)\n'
                  '    p.write_bytes(data.encode("utf-8"))\nprint("extracted",len(payload),"files")\n'),
             cell('code', 'import importlib.metadata,subprocess,sys\n'
                  'if importlib.metadata.version("kaggle-environments") != "1.32.7":\n'
                  '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
                  'subprocess.run([sys.executable,"cloud_frontier9.py"],check=True)\n'),
             cell('code', 'from IPython.display import display,FileLink\n'
                  'print(Path("results/frontier9/cloud_receipt.json").read_text())\n'
                  'display(FileLink("submission.tar.gz"))\ndisplay(FileLink("main.py"))\n')]
    for c in cells:
        if c['cell_type'] == 'code':
            compile(''.join(c['source']), 'cell', 'exec')
    nb = dict(nbformat=4, nbformat_minor=5, cells=cells,
              metadata={'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                        'language_info': {'name': 'python', 'version': '3.12'}})
    data = (json.dumps(nb, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    assert len(data) < 1000000, len(data)
    out = Path('kaggle_frontier9')
    out.mkdir(exist_ok=True)
    (out / 'experiment.ipynb').write_bytes(data)
    metadata = dict(id=KERNEL, title='Kaggriculture Frontier9 Preemption', code_file='experiment.ipynb',
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
