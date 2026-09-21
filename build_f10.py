"""Assemble Frontier10 candidates: the public wave of 20 September 2026 + the Kaggriculture Lab layers.

Public bases (extracted as data, pinned by hash, excluded from Git):
  metav4       Thomas Tschinkel, "The Metav4 Farm: Submission v13" (Apache-2.0)
  pipe16       Nathan Jacob, "Pipe-16: Idle Workers" = Metav4 v13 + HybridOpening (after Dmitrii Gluzdov)
  degnon_best  "V54 - Productive Idle Workers" (the same bytes are distributed by four notebooks)
  gluzdov_omw  Dmitrii Gluzdov, "One More Wheat"
  prvsiyan_guard  prvsiyan, "Kaggriculture Frontier | The Soil Remembers Rain" (21 Sep, Apache-2.0) = One More Wheat
               byte-identical + a 16-line visible-price guard (keep the step-91 wheat when its price is below 31)
Lab layers: the bounded full-lot pre-emption inside the public RACEGATE reservation (build_f9.py) and, optionally, the
lockstep sale ordering (frontier5_lockstep.py).  The Metav4 lineage keeps the RACEGATE re-implementation unchanged,
so the Frontier9 patch applies verbatim; its files already end on their real entry point.
"""
import hashlib
import json
from pathlib import Path

import build_f9 as f9

PINS = {
    'metav4': '9d63494603f88219',
    'pipe16': '827ddf2997fa442e',
    'degnon_best': 'fd39dffa68e2171f',
    'gluzdov_omw': '10f58185b916392c',
    'v53': '20fe549dd4573b9f',
    'prvsiyan_guard': '5fbb75c9c40e6d9e',
}


def load(name):
    data = Path('candidates', name + '.py').read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest.startswith(PINS[name]), (name, digest)
    return data.decode('utf-8')


def preempt(src, kmax, full=True):
    """The Frontier9 RACEGATE patch applied to another base of the same lineage (line endings of the base are kept)."""
    crlf = chr(13) + chr(10) in src
    text = src.replace(chr(13) + chr(10), chr(10)) if crlf else src
    assert text.count(f9.MARKER) == 1 and text.count(f9.OLD_SKIP) == 1
    head, tail = text.split(f9.MARKER, 1)
    assert tail.count(f9.OLD_END) == 1
    tail = tail.replace(f9.OLD_SKIP, f9.NEW_SKIP).replace(f9.OLD_END, f9.NEW_END)
    out = head + f9.MARKER + f9.HELPER % kmax + tail
    assert f9.NEW_SKIP in out and f9.NEW_END in out
    out = f9.full_lot(out) if full else out
    return out.replace(chr(10), chr(13) + chr(10)) if crlf else out


def with_lock(src):
    lock = Path('frontier5_lockstep.py').read_text(encoding='utf-8')
    return src.rstrip('\r\n') + '\n\n# Frontier10: Kaggriculture Lab lockstep sale ordering on top of the public stack\nagent = globals().pop("agent") if "agent" in globals() else kaggle_submission_agent\n' + lock


def bound_lock(src, entry):
    """Lockstep layer on a base whose Kaggle entry point (last callable) is not called `agent` (Ahmed Berat Ozer's V5x)."""
    assert ('def %s(' % entry) in src
    lock = Path('frontier5_lockstep.py').read_text(encoding='utf-8')
    bind = chr(10) + chr(10) + '# Frontier10: bind the public entry point (last callable, as the Kaggle loader does) before the Lab lockstep layer' + chr(10) + 'agent=' + entry + chr(10)
    return src.rstrip(chr(13) + chr(10)) + bind + lock


VARIANTS = {
    'f10_pipe16_pre': ('pipe16', 4, False, 'Pipe-16 + bounded full-lot pre-emption (KMAX 4)'),
    'f10_pipe16_prelock': ('pipe16', 4, True, 'Pipe-16 + pre-emption + Lab lockstep ordering'),
    'f10_v54_pre': ('degnon_best', 4, False, 'V54 (four public notebooks) + bounded full-lot pre-emption'),
    'f10_metav4_pre': ('metav4', 4, False, 'Metav4 v13 + bounded full-lot pre-emption'),
    'f10_omw_pre': ('gluzdov_omw', 4, False, 'One More Wheat + bounded full-lot pre-emption'),
    'f10_omw_prelock': ('gluzdov_omw', 4, True, 'One More Wheat + pre-emption + Lab lockstep ordering'),
    'f10_omw_lock': ('gluzdov_omw', 0, True, 'One More Wheat + Lab lockstep ordering only (no pre-emption); exported candidate'),
    'f10_v53_lock': ('v53', 0, '_e363_agent', 'Ahmed Berat Ozer V53 + Lab lockstep ordering (second lineage); exported candidate'),
    'f10_omwg_lock': ('prvsiyan_guard', 0, 'final_price_guard', 'One More Wheat + prvsiyan visible-price wheat guard (public, 21 Sep) + Lab lockstep ordering'),
}


def build(name):
    base, kmax, lock, _ = VARIANTS[name]
    src = preempt(load(base), kmax) if kmax else load(base)
    if isinstance(lock, str):
        return bound_lock(src, lock)
    return with_lock(src) if lock else src


def write(name, src):
    compile(src.replace('\r\n', '\n'), name, 'exec')
    Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
    print('wrote', name, len(src))


if __name__ == '__main__':
    manifest = {'pins': {k: hashlib.sha256(Path('candidates', k + '.py').read_bytes()).hexdigest() for k in PINS}, 'variants': {}}
    for name, (base, kmax, lock, note) in VARIANTS.items():
        write(name, build(name))
        manifest['variants'][name] = dict(base=base, kmax=kmax, lockstep=lock, note=note,
                                          sha256=hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest())
    Path('results/frontier10').mkdir(parents=True, exist_ok=True)
    Path('results/frontier10/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))
