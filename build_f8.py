"""Assemble Frontier8 candidates from the public wave of 19 September 2026 (all pinned by hash, all git-ignored).

Bases (extracted as data by extract_public_agents.py / outputs of `kaggle kernels pull`):
  tschinkel      Thomas Tschinkel, "The 2945 Farm" v9/4 (Apache-2.0)
  gluzdov_shock  Dmitrii Gluzdov, "A Smaller Market Shock" = v9/4 + temporary opening wheat crop
  lynn_v2        Arlene (lynnsakurai), "Farming Score V2" = v9/4 + final effective-queue closure
  tetsu_dp       tetsutani, "Demand-Preserving Turn Sale Timing" = Ahmed Berat Ozer V50 + 22-unit opening
Lab layer: frontier5_lockstep.py (lockstep sale ordering against a copy), unchanged.  The v9/4 lineage has no
`_RACE_STATE` (V44+ race layer), so an empty dict is defined before the layer; every file already ends on its real
entry point (`agent`), which the Kaggle loader takes as the last callable.
"""
import hashlib
import json
from pathlib import Path

PINS = {
    'tschinkel': '4f3ca95dd12d9a94',
    'gluzdov_shock': 'd5460fc2e5488e0a',
    'lynn_v2': '177d78bdf00aa965',
    'tetsu_dp': '1aa3717b3201997a',
}


def load(name):
    data = Path('candidates', name + '.py').read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest.startswith(PINS[name]), (name, digest)
    return data.decode('utf-8')


def tail_after(base, derived, name):
    """Text a derivative appended after the common base (both must share the whole base as a prefix)."""
    stem = base.rstrip('\r\n')
    assert derived.startswith(stem), name + ' is not a pure append on the base'
    return derived[len(stem):]


tsch = load('tschinkel')
gluz = load('gluzdov_shock')
lynn = load('lynn_v2')
tetsu = load('tetsu_dp')
lock = Path('frontier5_lockstep.py').read_text(encoding='utf-8')
EQ_BLOCK = tail_after(tsch, lynn, 'lynn_v2')
ALT_BLOCK = tail_after(tsch, gluz, 'gluzdov_shock')
assert 'def _eq_close(' in EQ_BLOCK and '_ALT_MODE' in ALT_BLOCK
SHIM = "\n# Frontier8: the v9/4 lineage has no V44+ race state; the lockstep layer only reads it when present\n_RACE_STATE=globals().get('_RACE_STATE',{})\n"

stack = gluz.rstrip('\r\n') + '\n' + EQ_BLOCK
VARIANTS = {
    'f8_stack': (stack, 'v9/4 + Gluzdov opening crop + Arlene queue closure (public layers only)'),
    'f8_stack_lock': (stack.rstrip('\r\n') + '\n' + SHIM + lock, 'f8_stack + Lab lockstep sale ordering'),
    'f8_lynn_lock': (lynn.rstrip('\r\n') + '\n' + SHIM + lock, 'lynn_v2 + Lab lockstep sale ordering'),
    'f8_tetsu_lock': (tetsu.rstrip('\r\n') + '\n' + lock, 'tetsu_dp (V50 lineage) + Lab lockstep sale ordering'),
}


def write(name, src):
    compile(src.replace('\r\n', '\n'), name, 'exec')
    Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
    print('wrote', name, len(src))


if __name__ == '__main__':
    manifest = {'pins': {k: hashlib.sha256(Path('candidates', k + '.py').read_bytes()).hexdigest() for k in PINS}, 'variants': {}}
    for name, (src, note) in VARIANTS.items():
        write(name, src)
        manifest['variants'][name] = dict(sha256=hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest(), note=note)
    Path('results/frontier8').mkdir(parents=True, exist_ok=True)
    Path('results/frontier8/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))
