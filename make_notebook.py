"""Embed only required project files. No credentials or downloaded opponents."""
import base64
import json
import zlib
from pathlib import Path


def cell(kind, source):
    result = dict(cell_type=kind,metadata={},source=source.splitlines(keepends=True))
    if kind == 'code':
        result.update(execution_count=None,outputs=[])
    return result


def main():
    files = ['baseline/v37.py','build.py','evaluate.py','cloud_experiment.py']
    payload = {name:Path(name).read_text(encoding='utf-8') for name in files}
    encoded = base64.b64encode(zlib.compress(json.dumps(payload).encode('utf-8'))).decode()
    cells = [cell('markdown', '# Kaggriculture Lab — CPU Policy Search\n\n'
        'Experimento privado. Conserva V37 y compara anticipación de ventas de 2, 6 y 8 turnos, '
        'más reglas de presión rival y semejanza sostenida de granjas. Selecciona en tres semillas y valida en cuatro nuevas, '
        'siempre en ambos asientos. matched6 se preseleccionó tras el panel local de rivales públicos; '
        'el ganador exploratorio también se registra. Si matched6 falla la validación empaqueta V37.\n\n'
        'No se ha entrenado una red neuronal ni se promete superar 3000. '
        'La ejecución produce `submission.tar.gz`, `main.py` y recibos JSON; no envía al leaderboard. '
        'El agente conserva íntegra su licencia Apache-2.0 y atribuciones. '
        'Investigación y código: https://github.com/Arturo-GA/kaggriculture-lab\n'),
        cell('code', 'from pathlib import Path\nimport base64, json, zlib, os\n'
             'os.chdir("/kaggle/working")\n'
             f'payload = json.loads(zlib.decompress(base64.b64decode({encoded!r})))\n'
             'for name, source in payload.items():\n'
             '    path = Path(name)\n    path.parent.mkdir(parents=True, exist_ok=True)\n'
             '    path.write_bytes(source.encode("utf-8"))\n'
             'print("Project extracted:", list(payload))\n'),
        cell('code','import importlib.metadata, subprocess, sys\n'
             'if importlib.metadata.version("kaggle-environments") != "1.32.7":\n'
             '    subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "kaggle-environments==1.32.7"], check=True)\n'
             'subprocess.run([sys.executable, "cloud_experiment.py"], check=True)\n'),
        cell('code','from IPython.display import FileLink, display\n'
             'print(Path("results/cloud_receipt.json").read_text())\n'
             'display(FileLink("submission.tar.gz"))\n'
             'display(FileLink("main.py"))\n')]
    notebook = dict(nbformat=4,nbformat_minor=5,cells=cells,
                   metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                             'language_info':{'name':'python','version':'3.12'}})
    out = Path('kaggle')
    out.mkdir(exist_ok=True)
    (out/'experiment.ipynb').write_bytes((json.dumps(notebook,ensure_ascii=False,indent=1)+'\n').encode('utf-8'))
    metadata = dict(id='jarturo/kaggriculture-lab-cpu-search',title='Kaggriculture Lab CPU Search',
                    code_file='experiment.ipynb',language='python',kernel_type='notebook',
                    is_private=True,enable_gpu=False,enable_internet=True,
                    dataset_sources=[],competition_sources=['kaggriculture'],kernel_sources=[])
    (out/'kernel-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    for c in cells:
        if c['cell_type']=='code':
            compile(''.join(c['source']),'notebook-cell','exec')
    print('Notebook built:',out/'experiment.ipynb')


if __name__ == '__main__':
    main()
