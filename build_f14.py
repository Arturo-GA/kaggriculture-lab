"""Assemble Frontier14 candidates: Frontier13 (cha22 + Frontier5 lockstep) with the base's own sale-advance knobs re-bound
after the lockstep layer.  Motivation (26 Sep live audit of the 39 Frontier13 losses, vendor/live_f13): the rivals that
beat us are private variants of cha22 / prvsiyan / Herd-Safe that sell milk, strawberry and wool a few turns EARLIER
than cha22's tape during days 20-27; against exact cha22 copies Frontier13 is 12/13.  Two independent public sources
measured a longer ready-stock sale advance on this lineage: Wangyh666 (_ADV_LOOK 4->6, +6pp vs cha22 in two seed
blocks of 200 games) and ghazaros (live 2644 at 6, inverted at 9/10).  Every knob is a module global read at call
time, so a rebind at the end of the file changes the base's behaviour without touching third-party code.
"""
import hashlib
import json
from pathlib import Path

import build_f13

VARIANTS = {
    'f14_adv4': ({'_ADV_LOOK': 4}, 'Frontier13 + ready-stock sale advance 4 turns'),
    'f14_adv5': ({'_ADV_LOOK': 5}, 'Frontier13 + ready-stock sale advance 5 turns'),
    'f14_adv6': ({'_ADV_LOOK': 6}, 'Frontier13 + ready-stock sale advance 6 turns'),
    'f14_adv8': ({'_ADV_LOOK': 8}, 'Frontier13 + ready-stock sale advance 8 turns'),
    'f14_adv6_h12': ({'_ADV_LOOK': 6, '_EV_H': 12, '_DP_H': 12, '_MP_H': 12},
                     'Frontier13 + advance 6 + evening/dawn/midday chunked lead-sell windows 8->12 turns'),
    'f14_h12': ({'_EV_H': 12, '_DP_H': 12, '_MP_H': 12}, 'Frontier13 + evening/dawn/midday chunked lead-sell windows 8->12 turns'),
    'f14_adv4_h12': ({'_ADV_LOOK': 4, '_EV_H': 12, '_DP_H': 12, '_MP_H': 12}, 'Frontier13 + advance 4 + lead-sell windows 12'),
    'f14_adv6_h16': ({'_ADV_LOOK': 6, '_EV_H': 16, '_DP_H': 16, '_MP_H': 16}, 'Frontier13 + advance 6 + lead-sell windows 16'),
    'f14_adv4_h16': ({'_ADV_LOOK': 4, '_EV_H': 16, '_DP_H': 16, '_MP_H': 16}, 'Frontier13 + advance 4 + lead-sell windows 16'),
    'f14_adv4_h24': ({'_ADV_LOOK': 4, '_EV_H': 24, '_DP_H': 24, '_MP_H': 24}, 'Frontier13 + advance 4 + lead-sell windows 24'),
    'f14_fx6': ({'_FX_FLOW_MIN': 6}, 'Frontier13 + rival-flow lead-sell enabled (rival >= 6 units in 8 turns)'),
    'f14_adv6_fx6': ({'_ADV_LOOK': 6, '_FX_FLOW_MIN': 6}, 'Frontier13 + advance 6 + rival-flow lead-sell'),
    'f14_adv4_fx6': ({'_ADV_LOOK': 4, '_FX_FLOW_MIN': 6}, 'Frontier13 + advance 4 + rival-flow lead-sell'),
}


def build(name):
    knobs, note = VARIANTS[name]
    src = build_f13.build('f13_c22_lock')
    nl = chr(10)
    src += nl + '# Frontier14 (%s): re-bind the base sale-advance knobs after the Lab layer (%s)' % (name, note) + nl
    for key, value in knobs.items():
        assert (nl + key + ' = ') in src or (nl + key + '=') in src, key
        src += '%s = %r' % (key, value) + nl
    return src


if __name__ == '__main__':
    manifest = {'parent': 'f13_c22_lock', 'variants': {}}
    for name, (knobs, note) in VARIANTS.items():
        src = build(name)
        compile(src.replace('\r\n', '\n'), name, 'exec')
        Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
        manifest['variants'][name] = dict(knobs=knobs, note=note, sha256=hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest())
        print('wrote', name, len(src))
    Path('results/frontier14').mkdir(parents=True, exist_ok=True)
    Path('results/frontier14/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
