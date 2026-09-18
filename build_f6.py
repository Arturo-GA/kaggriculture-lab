"""Frontier6 experiment: transplant a top team's recorded action streams into the V46 chassis as its route library.

Inputs (all outside Git): vendor/top_replays/<team>/episode-*-replay.json and outputs/session/live/top_replays_index.json
(from outputs/session/fetch_top_replays.py). One recording per ordered first-two-shop pair, chosen by the recorded
team's own final bank; unseen pairs fall back to the swapped pair, then the same first shop, then the best bank overall.
The V46 reactive layers, opening and race logic stay; the day-27 switch to the public route 2 is removed because the
recorded streams carry their own last days. The public V46 source is pinned by hash.
"""
import argparse
import base64
import hashlib
import json
import re
import zlib
from pathlib import Path

import build_f5

SHOPS = ('BAKERY', 'PIZZA_SHOP', 'BRUNCH_SPOT', 'YARN_STORE', 'ICE_CREAM_SHOP', 'PET_CAFE', 'SMOOTHIE_SHOP', 'FARMERS_MARKET')
PASS = {'farmer': ['PASS'], 'hands': [], 'market': []}


def load_recordings(team, index_path='outputs/session/live/top_replays_index.json'):
    rows = [r for r in json.loads(Path(index_path).read_text(encoding='utf-8')) if r['team'] == team]
    out = []
    for r in rows:
        path = Path('vendor/top_replays', team, f"episode-{r['episode']}-replay.json")
        if not path.exists():
            continue
        d = json.loads(path.read_text(encoding='utf-8'))
        if len(d['steps']) < 720:
            continue
        seat = r['seat']
        tape = []
        for t in range(719):
            a = d['steps'][t + 1][seat].get('action') or {}
            tape.append({'farmer': list(a.get('farmer') or ['PASS']), 'hands': [list(h) for h in (a.get('hands') or [])],
                         'market': [list(o) for o in (a.get('market') or []) if o]})
        tape.append(dict(PASS))
        out.append(dict(episode=r['episode'], pair=tuple(r['shops'][:2]), shops=tuple(r['shops']), bank=float(r['my'] or 0),
                        margin=float(r['my'] or 0) - float(r['op'] or 0), tape=tape))
    return out


def normalize_opening(tape):
    """Bring the recording's first two market turns to the lineage convention the V46 opening layer rewrites."""
    tape[0] = dict(tape[0], market=[['BUY_PRODUCT', 'WHEAT', 5], ['BUY_PRODUCT', 'WHEAT', 10], ['SELL', 'WHEAT', 60]])
    m1 = [list(o) for o in tape[1].get('market') or []]
    head = [o for o in m1[:2] if o and o[0] in ('SELL', 'BUY_PRODUCT') and o[1] == 'WHEAT']
    rest = m1[len(head):]
    tape[1] = dict(tape[1], market=[['SELL', 'WHEAT', 13], ['BUY_PRODUCT', 'WHEAT', 5]] + rest)
    return tape


def choose_routes(recordings):
    by_pair = {}
    for rec in recordings:
        cur = by_pair.get(rec['pair'])
        if cur is None or rec['bank'] > cur['bank']:
            by_pair[rec['pair']] = rec
    routes, shops, route_of = {}, [], {}
    for rid, (pair, rec) in enumerate(sorted(by_pair.items()), start=100):
        routes[rid] = normalize_opening([dict(a) for a in rec['tape']])
        route_of[pair] = rid
        shops.append({'shops': list(pair), 'route': rid, 'episode': rec['episode'], 'bank': rec['bank']})
    best = max(by_pair.values(), key=lambda r: r['bank'])
    fallback = {'default': route_of[best['pair']], 'first_shop': {}}
    for s in SHOPS:
        cands = [rec for pair, rec in by_pair.items() if pair[0] == s]
        if cands:
            fallback['first_shop'][s] = route_of[max(cands, key=lambda r: r['bank'])['pair']]
    return routes, shops, fallback


ROUTER = '''def _router(observation,step,state):
    if step>=144 and not state.get('day6'):
        shops=tuple((_get(_get(observation,'town',{}),'unlocked_shops',[]) or [])[:2])
        route=_MG_SHOP_ROUTES.get(shops)
        if route is None and len(shops)==2:route=_MG_SHOP_ROUTES.get((shops[1],shops[0]))
        if route is None and shops:route=_MG_FALLBACK['first_shop'].get(shops[0])
        if route is None:route=_MG_FALLBACK['default']
        state['expert']='MG';state['route']=route;state['day6']=True
    return state.get('route',_MG_FALLBACK['default'])
'''


def build(team, name):
    recordings = load_recordings(team)
    assert recordings, 'no recordings'
    routes, shops, fallback = choose_routes(recordings)
    data = {'routes': {str(k): v for k, v in routes.items()}, 'shops': shops, 'fallback': fallback}
    blob = base64.b85encode(zlib.compress(json.dumps(data, separators=(',', ':')).encode('utf-8'), 9)).decode()
    src = build_f5.v46
    nl = '\r\n' if '\r\n' in src else '\n'
    anchor = "_R108_SHOP_ROUTES={tuple(r['shops']):r['route'] for r in _R108_DATA['shops']}" + nl + "del _R108_DATA" + nl
    assert src.count(anchor) == 1
    inject = (anchor + "_MG_DATA=json.loads(zlib.decompress(base64.b85decode(" + repr(blob) + ")))" + nl
              + "_ROUTES={int(k):v for k,v in _MG_DATA['routes'].items()}" + nl
              + "_MG_SHOP_ROUTES={tuple(r['shops']):r['route'] for r in _MG_DATA['shops']}" + nl
              + "_MG_FALLBACK=_MG_DATA['fallback']" + nl
              + "del _MG_DATA" + nl)
    src = src.replace(anchor, inject)
    # the public router (day-6 pair lookup + day-27 switch to route 2) becomes the recording router
    start = src.index('def _router(observation,step,state):')
    end = src.index('_R42_OPENING=', start)
    src = src[:start] + ROUTER.replace('\n', nl) + nl + src[end:]
    # every "route 2 after step 648" tape lookup follows the selected route instead
    src, n = re.subn(r"routes\[2 if [^\]]*? else ([^\]]+)\]", r"routes[\1]", src)
    assert n >= 10, n
    compile(src.replace('\r\n', '\n'), name, 'exec')
    Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
    manifest = dict(team=team, recordings=len(recordings), routes=len(routes), pairs=[s['shops'] for s in shops],
                    fallback=fallback, sha256=hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest(),
                    v46_sha256=build_f5.V46_SHA256, route_lookups_rewritten=n)
    Path('results/frontier6').mkdir(parents=True, exist_ok=True)
    Path('results/frontier6', name + '_build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in manifest.items() if k != 'pairs'}, indent=2))
    return src


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--team', default='mother_goose')
    p.add_argument('--name', default='f6_mg')
    a = p.parse_args()
    src = build(a.team, a.name)
    lock = Path('frontier5_lockstep.py').read_text(encoding='utf-8')
    locked = src + '\n' + lock
    compile(locked.replace('\r\n', '\n'), a.name + 'lock', 'exec')
    Path('candidates', a.name + 'lock.py').write_text(locked, encoding='utf-8', newline='')
    print('wrote', a.name, 'and', a.name + 'lock')
