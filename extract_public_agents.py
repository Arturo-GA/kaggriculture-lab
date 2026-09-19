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
    'v46': ('ahmedberatozer/kaggriculture-v46-first-turn-microstructure-and-s', 'auto'),
    'pipe7': ('nathanjacob/kaggriculture-pipe-7-wheat-microstructure', 'auto'),
    'pipe8': ('nathanjacob/kaggriculture-pipe-8-clean-opening', 'auto'),
    'beyond48': ('jaxa623/2780-beyond-48-0-128-128-worlds-with-95-cis', 'auto'),
    'orderseq': ('uninhibitedscholar/kaggriculture-beyond-48-order-sequencing', 'auto'),
    'seyit2820': ('seyitkaangunes/kaggriculture-2820-score', 'auto'),
    'aurax_v6': ('aurax7/kaggriculture-shop-router-reactive-v6', 'auto'),
    'xman_top1': ('xuanzhang001/kaggriculture-auto-top1', 'auto'),
    'open78': ('ayodejiibrahimlateef/kaggriculture-cloning-v45-open-78-experiment', 'auto'),
    'purerl': ('hesoponyo/pure-rl-agent-bc-ppo-self-play', 'auto'),
    'evgen': ('evgendvorkin/kaggriculture', 'auto'),
    'tetsu_market2': ('tetsutani/market-smart-farming-kaggriculture', 'auto'),
    'v48': ('ahmedberatozer/kaggriculture-v48-clear-the-queue', 'auto'),
    # 19 September 2026 wave (Frontier8)
    'tschinkel': ('thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots', 'auto'),
    'v49': ('ahmedberatozer/kaggriculture-v49-funded-sale-timing-and-worker', 'auto'),
    'v50': ('ahmedberatozer/kaggriculture-v50-early-yarn-commit', 'auto'),
    'tetsu_dp': ('tetsutani/demand-preserving-turn-sale-timing', 'auto'),
    'gluzdov_shock': ('dmitriigluzdov/kaggriculture-a-smaller-market-shock', 'auto'),
    'lynn_v2': ('lynnsakurai/farming-score-v2-a-better-approach', 'auto'),
    'yummers': ('romantamrazov/kaggriculture-yummers', 'auto'),
    'alperen_rhythm': ('alperen5252525/kaggriculture-market-rhythm-sale-policy', 'auto'),
    'alperen_first': ('alperen5252525/kaggriculture-first-in-line-stock-into-income', 'auto'),
    'melon_squeeze': ('goodpjw2008/kaggriculture-melon-threshold-squeeze-2749', 'auto'),
    'ziheng_best': ('zihengedie/best-version', 'auto'),
    'k0013': ('ghazarosbarseghyan91/kaggriculture-k0013-v46-advance6', 'auto'),
    'aurax_v7': ('aurax7/kaggriculture-shop-router-reactive-v7', 'auto'),
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


def _decode_blob(blob):
    """Try the encodings public notebooks use for an embedded main.py: base85/base64, gzip/zlib/lzma, tar."""
    import lzma
    raw = blob.encode() if isinstance(blob, str) else blob
    for decode in (base64.b85decode, base64.b64decode, lambda b: b):
        try:
            step1 = decode(raw)
        except Exception:
            continue
        for inflate in (gzip.decompress, zlib.decompress, lzma.decompress, lambda b: b):
            try:
                step2 = inflate(step1)
            except Exception:
                continue
            try:
                tf = tarfile.open(fileobj=io.BytesIO(step2), mode='r:*')
                member = [m for m in tf.getnames() if m.endswith('main.py')]
                if member:
                    return tf.extractfile(member[0]).read()
            except Exception:
                pass
            if b'def agent' in step2 and b'\x00' not in step2[:1000]:
                return step2
    return None


def auto_extract(cells):
    for c in cells:
        if c.startswith('%%writefile main.py'):
            return c.split('\n', 1)[1].encode('utf-8')
    for cell in sorted(cells, key=len, reverse=True)[:4]:
        try:
            tree = ast.parse(cell)
        except SyntaxError:
            continue
        names = {t.id for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
        if 'SOURCE_BYTES' in names:
            value = assign(tree, 'SOURCE_BYTES')
            return b''.join(ast.literal_eval(value.args[0])) if isinstance(value, ast.Call) else ast.literal_eval(value)
        if 'AGENT_SOURCE' in names:
            value = assign(tree, 'AGENT_SOURCE')
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                return value.value.encode('utf-8')
        blobs = sorted((n.value for n in ast.walk(tree) if isinstance(n, ast.Constant)
                        and isinstance(n.value, (str, bytes)) and len(n.value) > 5000), key=len, reverse=True)
        for blob in blobs:
            data = _decode_blob(blob)
            if data is not None:
                return data
    return None


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
    elif kind == 'auto':
        data = auto_extract(cells)
        assert data is not None, ref
    else:
        raise ValueError(kind)
    compile(data.decode('utf-8').replace('\r\n', '\n'), ref, 'exec')
    return notebook, data


def main(names=None):
    """Extract every source, or only `names` (merged into the existing record file so older pulls keep their hashes)."""
    path = Path('results/public_agents.json')
    records = json.loads(path.read_text(encoding='utf-8')) if names and path.exists() else {}
    Path('candidates').mkdir(exist_ok=True)
    for name, (ref, kind) in SOURCES.items():
        if names and name not in names:
            continue
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
    import sys
    main(sys.argv[1:] or None)
