"""Extract public Kaggriculture agents from pulled notebooks as data, without executing notebook cells.

Pull first (outputs stay outside Git):
  python -m kaggle kernels pull ahmedberatozer/kaggriculture-v45-first-turn-wheat-round-trip -p vendor/pub/ahmedberatozer_kaggriculture-v45-first-turn-wheat-round-trip -m
Each agent is written to candidates/<name>.py (git-ignored) with its SHA-256 recorded in results/public_agents.json.
"""
import ast
import base64
import glob
import gzip
import hashlib
import io
import json
import tarfile
import zlib
from pathlib import Path

SOURCES = {
    'v43': ('ahmedberatozer/kaggriculture-v43-recovering-lost-harvests', 'bytes'),
    'v44': ('ahmedberatozer/kaggriculture-v44-winning-the-same-turn-sale-race', 'bytes'),
    'v45': ('ahmedberatozer/kaggriculture-v45-first-turn-wheat-round-trip', 'bytes'),
    'pipe4': ('nathanjacob/beyond-v43-what-the-top-clusters-do-on-turn-1', 'b85gz'),
    'pipe5': ('nathanjacob/kaggriculture-pipe-5-terminal-boost', 'b85gz'),
    'lynn_v5': ('lynnsakurai/farming-score-v5-timing-optimized', 'writefile'),
    'aurax_v5': ('aurax7/kaggriculture-shop-router-reactive-v5', 'writefile'),
    'alperen_v62': ('alperen5252525/v62-metabalance-kaggriculture', 'writefile'),
    'harvestforge': ('salemali7/kaggriculture-2900', 'writefile'),
}


def code_cells(ref):
    folder = Path('vendor/pub', ref.replace('/', '_'))
    notebook = next(folder.glob('*.ipynb'))
    data = json.loads(notebook.read_text(encoding='utf-8'))
    return notebook, [''.join(c['source']) for c in data['cells'] if c['cell_type'] == 'code']


def assign(tree, name):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return node.value
    raise KeyError(name)


def extract(ref, kind):
    notebook, cells = code_cells(ref)
    if kind == 'writefile':
        data = next(c.split('\n', 1)[1] for c in cells if c.startswith('%%writefile main.py')).encode('utf-8')
    elif kind == 'bytes':
        tree = ast.parse(max(cells, key=len))
        expected = ast.literal_eval(assign(tree, 'EXPECTED_MAIN_SHA256'))
        value = assign(tree, 'SOURCE_BYTES')
        data = b''.join(ast.literal_eval(value.args[0]))
        assert hashlib.sha256(data).hexdigest() == expected, ref
    elif kind == 'b85gz':
        tree = ast.parse(max(cells, key=len))
        expected = ast.literal_eval(assign(tree, 'EXPECTED_SHA256'))
        blobs = sorted((n.value for n in ast.walk(tree) if isinstance(n, ast.Constant)
                        and isinstance(n.value, str) and len(n.value) > 10000), key=len, reverse=True)
        data = None
        for blob in blobs:
            for decode in (base64.b85decode, base64.b64decode):
                for inflate in (gzip.decompress, zlib.decompress):
                    try:
                        candidate = inflate(decode(blob))
                    except Exception:
                        continue
                    if b'def agent' in candidate or b'def _' in candidate[:20000]:
                        data = candidate
                        break
                if data is not None:
                    break
            if data is not None:
                break
        assert data is not None, ref
        if hashlib.sha256(data).hexdigest() != expected:
            print('warning: declared hash differs for', ref, '(kept as evaluation opponent only)')
    else:
        raise ValueError(kind)
    compile(data.decode('utf-8').replace('\r\n', '\n'), ref, 'exec')
    return notebook, data


def main():
    records = {}
    Path('candidates').mkdir(exist_ok=True)
    for name, (ref, kind) in SOURCES.items():
        try:
            notebook, data = extract(ref, kind)
        except StopIteration:
            print('skip', name, '(notebook not pulled)')
            continue
        Path('candidates', name + '.py').write_bytes(data)
        records[name] = dict(url='https://www.kaggle.com/code/' + ref, bytes=len(data),
                             agent_sha256=hashlib.sha256(data).hexdigest(),
                             notebook_sha256=hashlib.sha256(notebook.read_bytes()).hexdigest(),
                             use='evaluation and, for v45, the Frontier4 base; excluded from Git')
        print(name, records[name]['agent_sha256'][:16], len(data))
    Path('results').mkdir(exist_ok=True)
    Path('results/public_agents.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
