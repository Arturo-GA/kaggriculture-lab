"""Extract the agent embedded in every notebook (or script, or tar payload) under a folder, dedupe by SHA-256 against every
known agent (candidates/*.py and earlier reports) and report lineage.

usage: python scan_public_agents.py <folder with one subfolder per notebook> <name prefix> <report.json>
New single-file agents are written to candidates/<prefix>_<owner>_<sha6>.py (git-ignored third-party sources);
multi-file packages to vendor/<prefix>_agents/<name>/."""
import ast, base64, gzip, hashlib, io, json, lzma, re, sys, tarfile, zlib
from pathlib import Path
sys.path.insert(0, '.')
import extract_public_agents as E

known = {}
for f in Path('candidates').glob('*.py'):
    known.setdefault(hashlib.sha256(f.read_bytes()).hexdigest(), f.stem)
for p in ('results/public_agents.json', 'outputs/session/gold/new_agents_0920.json', 'outputs/session/gold/new_agents_0923.json'):
    try:
        for k, v in json.loads(Path(p).read_text(encoding='utf-8')).items():
            h = (v or {}).get('agent_sha256') or (v or {}).get('sha256') if isinstance(v, dict) else None
            if h: known.setdefault(h, k)
    except Exception as e:
        print('skip', p, e)

def _utf8(b):
    try:
        b.decode('utf-8'); return True
    except UnicodeDecodeError:
        return False

def decode_all(blob):
    raw = blob.encode() if isinstance(blob, str) else blob
    for dec in (base64.b85decode, base64.b64decode, lambda b: b):
        try: s1 = dec(raw)
        except Exception: continue
        for inf in (gzip.decompress, zlib.decompress, lzma.decompress, lambda b: b):
            try: s2 = inf(s1)
            except Exception: continue
            try:
                tf = tarfile.open(fileobj=io.BytesIO(s2), mode='r:*')
                files = {m.name: tf.extractfile(m).read() for m in tf.getmembers() if m.isfile()}
                if any(n.endswith('main.py') for n in files):
                    return files
            except Exception:
                pass
            if len(s2) > 10000 and bytes([0]) not in s2[:1000] and b'def ' in s2 and b'obs' in s2 and _utf8(s2):
                return {'main.py': s2}
    return None

def source_blob(cells):
    for cell in sorted(cells, key=len, reverse=True)[:4]:
        try: tree = ast.parse(cell)
        except SyntaxError: continue
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'SOURCE_BLOB' for t in node.targets):
                v = node.value
                try:
                    parts = ast.literal_eval(v.args[0]) if isinstance(v, ast.Call) else ast.literal_eval(v)
                except Exception:
                    continue
                blob = ''.join(parts) if not isinstance(parts, str) else parts
                for dec in (base64.b85decode, base64.b64decode):
                    try: return {'main.py': zlib.decompress(dec(blob))}
                    except Exception: pass
    return None

def big_strings(tree):
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, (str, bytes)) and len(n.value) > 5000:
            out.append(n.value)
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'join' and n.args and isinstance(n.args[0], (ast.Tuple, ast.List)):
            parts = [e.value for e in n.args[0].elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
            if len(parts) == len(n.args[0].elts) and sum(map(len, parts)) > 5000:
                out.append(''.join(parts))
    return sorted(out, key=len, reverse=True)

def multi(cells):
    """Largest decodable payload (tar with several files, or a single main.py) among big string literals."""
    best = None
    for cell in sorted(cells, key=len, reverse=True)[:4]:
        try: tree = ast.parse(cell)
        except SyntaxError:
            try: tree = ast.parse(chr(10).join(l for l in cell.split(chr(10)) if not l.startswith(('%', '!'))))
            except SyntaxError: continue
        blobs = big_strings(tree)
        for b in blobs[:6]:
            files = decode_all(b)
            if files and (best is None or len(files) > len(best)):
                best = files
    return best

bases = {}
for b in ('gluzdov_omw', 'pipe16', 'metav4', 'v53', 'v52', 'tschinkel', 'v50', 'lynn_v2', 'prvsiyan_guard', 'tetsu_dp', 'yummers2', 'hanif_sos', 'gluzdov_mwss'):
    p = Path('candidates', b + '.py')
    if p.exists():
        bases[b] = set(p.read_bytes().decode('utf-8', 'replace').replace('\r\n', '\n').split('\n'))

report = {}
FOLDER, PREFIX, REPORT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
for folder in sorted(p for p in FOLDER.iterdir() if p.is_dir()):
    nbs = list(folder.glob('*.ipynb')); pys = list(folder.glob('*.py'))
    meta = json.loads((folder / 'kernel-metadata.json').read_text(encoding='utf-8')) if (folder / 'kernel-metadata.json').exists() else {}
    title = meta.get('title', '')
    files = None
    if nbs:
        data = json.loads(nbs[0].read_text(encoding='utf-8'))
        cells = [''.join(c['source']) for c in data['cells'] if c['cell_type'] == 'code']
        m = None
        try: m = multi(cells)
        except Exception as e: print(folder.name, 'multi error', repr(e)[:100])
        if m and len(m) > 1: files = m
        else:
            a = None
            try: a = E.auto_extract(cells)
            except Exception: pass
            sb = None
            try: sb = source_blob(cells)
            except Exception: pass
            files = {'main.py': a} if a else (sb or m)
    elif pys:
        src = pys[0].read_bytes()
        try: files = multi([src.decode('utf-8', 'replace')])
        except Exception as e: print(folder.name, 'script multi error', repr(e)[:100])
        if not files and b'def agent' in src: files = {'main.py': src}
    if not files:
        report[folder.name] = dict(title=title, agent=None); continue
    main = next(v for k, v in files.items() if k.endswith('main.py'))
    h = hashlib.sha256(main).hexdigest()
    lines = set(main.decode('utf-8', 'replace').replace('\r\n', '\n').split('\n'))
    sims = sorted(((len(lines & s) / max(1, len(lines | s)), b) for b, s in bases.items()), reverse=True)[:2]
    entry = dict(title=title, sha256=h, bytes=len(main), files=sorted(files), known=known.get(h), closest=[(b, round(j, 3)) for j, b in sims])
    if len(files) > 1:
        entry['multi_file'] = True
    if h not in known:
        name = PREFIX + '_' + folder.name.split('_', 1)[0][:14] + '_' + h[:6]
        if len(files) == 1:
            Path('candidates', name + '.py').write_bytes(main)
            entry['candidate'] = name
        else:
            d = Path('vendor', PREFIX + '_agents', name); d.mkdir(parents=True, exist_ok=True)
            for k, v in files.items():
                (d / Path(k).name).write_bytes(v)
            entry['candidate_dir'] = str(d)
        known[h] = name
    report[folder.name] = entry
REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding='utf-8')
for k, v in report.items():
    if not v.get('agent', True) is None and 'sha256' in v:
        tag = v.get('candidate') or v.get('candidate_dir') or ('= ' + str(v['known']))
        print(f"{k[:58]:58s} {v['bytes']:8d} {v['sha256'][:12]} {'MULTI ' if v.get('multi_file') else ''}{tag} | {v['closest']}")
    else:
        print(f"{k[:58]:58s} (no agent) | {v['title'][:50]}")
