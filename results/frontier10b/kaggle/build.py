"""Reproducible, isolated interventions on the immutable V37 baseline."""
import hashlib
import json
import tarfile
import io
import gzip
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = '94c1c2c05ae7cde8fca9ee3957b01112c1cbab82c7434aae6a5f24fa7485bc4c'
ANCHOR = 'if 288 <= step < 696:_R37_HORIZONS[player] = 4'

PRESSURE = '''
# Original experiment, Arturo-GA / Kaggriculture Lab, 2026-09-12, Apache-2.0.
# Public ripe output is a pressure scenario, never a claim about hidden stock.
def _lab_pressure_horizon(obs):
    rival = obs['farms'][1-int(obs['player'])]
    public_yield = {}
    for row in rival['tiles']:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            item = tile.get('crop') or {'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG'}.get(tile.get('animal'))
            if item:
                public_yield[item] = public_yield.get(item, 0) + max(0, int(tile.get('yield_units', 0)))
    shed = obs['private']['shed']
    inv = obs['market']['inventory']
    risk = 0
    for item in ('MILK', 'WOOL', 'STRAWBERRY', 'MELON'):
        stock = min(12, max(0, int(shed.get(item, 0))))
        batch = min(24, public_yield.get(item, 0))
        if stock and batch:
            risk += stock * max(0, _r37_market_price(item, inv[item]) -
                                  _r37_market_price(item, inv[item] + batch))
    return 8 if risk >= 100 else (6 if risk >= 25 else 4)
'''


def build():
    baseline = (ROOT/'baseline/v37.py').read_bytes()
    assert hashlib.sha256(baseline).hexdigest() == EXPECTED, 'Baseline changed'
    source = baseline.decode('utf-8')
    assert source.count(ANCHOR) == 1
    candidates = {'v37': source}
    for horizon in (2, 6, 8):
        candidates['h'+str(horizon)] = source.replace(ANCHOR, ANCHOR[:-1]+str(horizon))
    candidates['matched6'] = source.replace(ANCHOR,
        'if 288 <= step < 696:_R37_HORIZONS[player] = 6 if 336 <= step < 648 and state["streak"] >= 6 else 4')
    # Helpers precede the parent that calls them, preserving the final callable export.
    candidates['pressure'] = source.replace('def _r37_similarity(observation):',
        PRESSURE+'\n\ndef _r37_similarity(observation):').replace(ANCHOR,
        'if 288 <= step < 696:_R37_HORIZONS[player] = _lab_pressure_horizon(observation)')
    out = ROOT/'candidates'
    out.mkdir(exist_ok=True)
    manifest = {'baseline_sha256': hashlib.sha256(baseline).hexdigest(), 'candidates': {}}
    for name, text in candidates.items():
        compile(text, name+'.py', 'exec')
        data = text.encode('utf-8')
        (out/(name+'.py')).write_bytes(data)
        manifest['candidates'][name] = hashlib.sha256(data).hexdigest()
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/build.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


def package(name, destination):
    data = (ROOT/'candidates'/(name+'.py')).read_bytes()
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode='w') as archive:
        info = tarfile.TarInfo('main.py')
        info.size, info.mtime, info.mode = len(data), 0, 0o644
        archive.addfile(info, io.BytesIO(data))
    Path(destination).write_bytes(gzip.compress(buf.getvalue(), mtime=0))


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
