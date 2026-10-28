"""Assemble Frontier13 candidates on the post-lock public wave (agents re-published in existing public notebooks after the
23 September lock).

Base: "cha22" (Kaggriculture cha22 - route-replay agent; notebook abhinav0370/cha22-agent, the same bytes ship in
tetsutani's "Demand-Preserving Turn Sale Timing" and guruprasaathas111's "Master Engine V3", updated 24 Sep 2026;
Apache-2.0, v9/3 lineage with public route tapes and queue closure; every upstream notice retained).  Extracted as
data, pinned by hash, excluded from Git.  Lab layer: the unchanged Frontier5 lockstep, bound to the base's entry point.
"""
import hashlib
import json
from pathlib import Path

import build_f11

PINS = {'n25_abhinav0370_127ed3': '127ed3e62988', 'n25_haideptry_cda529': 'cda529cb6b35'}
VARIANTS = {
    'f13_c22_lock': ('n25_abhinav0370_127ed3', 'ig_agent', 'lock', 'cha22 route-replay agent + Frontier5 lockstep'),
    'f13x_hd_lock': ('n25_haideptry_cda529', 'agent', 'lock', 'haideptry 2965 hybrid (25 Sep) + Frontier5 lockstep (exploratory)'),
    'f13x_c22_br': ('n25_abhinav0370_127ed3', 'ig_agent', 'f11', 'cha22 + frontier11 level-2 best response over layer D orderings (exploratory)', {'_F11_W': (0.0, 1.0, 0.0), '_F11_HARD': False}),
    'f13x_c22_mix': ('n25_abhinav0370_127ed3', 'ig_agent', 'f11', 'cha22 + frontier11 weighted three-model response (exploratory)', {'_F11_W': (1.0, 2.0, 1.0), '_F11_HARD': False}),
}


def load(name):
    data = Path('candidates', name + '.py').read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest.startswith(PINS[name]), (name, digest)
    return data.decode('utf-8')


def build(name):
    base, entry, layer, _ = VARIANTS[name][:4]
    out = build_f11.bind(load(base), entry, {'lock': 'frontier5_lockstep.py', 'f11': 'frontier11_order.py'}[layer], name)
    for key, value in (VARIANTS[name][4] if len(VARIANTS[name]) > 4 else {}).items():
        out += '%s = %r' % (key, value) + chr(10)
    return out


if __name__ == '__main__':
    manifest = {'pins': {k: hashlib.sha256(Path('candidates', k + '.py').read_bytes()).hexdigest() for k in PINS}, 'variants': {}}
    for name, (base, entry, layer, note, *extra) in VARIANTS.items():
        src = build(name)
        compile(src.replace('\r\n', '\n'), name, 'exec')
        Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
        manifest['variants'][name] = dict(base=base, entry=entry, layer=layer, note=note,
                                          sha256=hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest())
        print('wrote', name, len(src))
    Path('results/frontier13').mkdir(parents=True, exist_ok=True)
    Path('results/frontier13/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))
