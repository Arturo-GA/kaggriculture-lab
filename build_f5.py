"""Assemble Frontier5 candidates: public V46 base (pinned) + demand-aware livestock layer variants.

Inputs: candidates/v46.py (from extract_public_agents.py, git-ignored) and frontier5_geese.py.
"""
import hashlib
import json
import re
from pathlib import Path

V46_SHA256 = '735c370383b70d3bf3aac792f2c147e0afc99166fc9f253ede10e8a030acedb6'

v46 = Path('candidates/v46.py').read_bytes()
assert hashlib.sha256(v46).hexdigest() == V46_SHA256, 'Public V46 source changed; re-extract and re-verify'
v46 = v46.decode('utf-8')
geese = Path('frontier5_geese.py').read_text(encoding='utf-8')


def write(name, src, overrides=None):
    for k, v in (overrides or {}).items():
        pat = r'^%s=.*$' % re.escape(k)
        assert re.search(pat, src, flags=re.M), k
        src = re.sub(pat, '%s=%r' % (k, v), src, count=1, flags=re.M)
    compile(src.replace('\r\n', '\n'), name, 'exec')
    Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
    print('wrote', name, len(src))


VARIANTS = {
    'f5_geese': ({}, 'geese for all post-day-6 cows and sheep when no yarn store and <=1 milk shop known at step 144'),
    'f5_geese_sheep': ({'_GZ_SPECIES': ('SHEEP',), '_GZ_MAX_MILK_KNOWN': 9}, 'geese only for post-day-6 sheep when no yarn store known'),
    'f5_geese_any': ({'_GZ_MAX_MILK_KNOWN': 9}, 'geese for post-day-6 cows and sheep whenever no yarn store known'),
}

if __name__ == '__main__':
    manifest = {'v46_sha256': V46_SHA256, 'variants': {}}
    for name, (overrides, note) in VARIANTS.items():
        write(name, v46 + '\n' + geese, overrides)
        manifest['variants'][name] = dict(sha256=hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest(), note=note)
    Path('results/frontier5').mkdir(parents=True, exist_ok=True)
    Path('results/frontier5/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))
