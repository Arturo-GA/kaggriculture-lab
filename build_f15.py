"""Assemble Frontier15 candidates: Frontier14B (cha22 + lockstep + advance 4 + windows 16) plus ONE extra sale-timing
layer bound after the Lab lockstep layer.  Motivation (26 Sep audit of the 96 live games of the active pair against
rivals rated 2400+, vendor/live_f14 + outputs/session/gold/ledger_f14live.json): in the 2450-2600 band the rivals are
same-production clones (same hands, land, animals, opening money 1042) and the margins are decided by sale timing in
days 16-28 (-7 to -1500); the blowouts (-3000 to -35000) come only from private agents with different production
(geese, tomatoes, carrots).  Engine facts (kaggle_environments/envs/kaggriculture/kaggriculture.py): price is a pure
function of market inventory; the town removes a few units per product after every step = 0 mod 4; both players' i-th
orders settle unit by unit at the same quote; SELL orders with quantity 0 are parsed as empty slots.  Market regime in
the live clone games (48 replays): MILK, WOOL and MELON are in glut from day 12-15 on (price 0.3-0.6 of base),
STRAWBERRY from day 21, EGG and CARROT stay scarce (price above base).  In a glut the first seller after each
consumption tick takes the recovered slack; the others sell into the depressed price.

Layers (each one variant; all read the base's own helpers: projected_shed, _IMPL.chassis, _v9_town_draw,
_r37_market_price, _lk_reorder):
  wh   window head: at step % 4 == 1 sell this window's planned tape lots (E076 lead2 idea, mooman0222, MIT).
  e81  full projected shed of MILK/WOOL/STRAWBERRY at every window head (E081, mooman0222, MIT).
  e81g E081 restricted to items in glut (inventory >= I0), MELON included.
  slk  window head: this window's planned lots + the next tick's town draw, only for items in glut.
  ad   rival-adaptive: windows 16 -> 24 for the rest of the game once the rival's observed premium sales over the last
       48 turns exceed ours by >= 6 units (rival flow from the base's own _fx_update tracker).
"""
import hashlib
import json
from pathlib import Path

import build_f14

LAYER = r'''
# ==== Frontier15 (Arturo-GA, Apache-2.0): one extra sale-timing layer after the Lab lockstep layer ====
# Window-head selling in glut markets.  The town removes its draw after every step = 0 mod 4, so the quote is highest at
# step 4k+1; both players' i-th orders settle at the same quote, so the player that lists the units first takes the slack.
_F15_MODE = %(mode)r
_F15_TOM = %(tom)r
_F15_TOM_MONEY = 9000
_F15_PARENT = agent
# Optional production lever: the base's finite late tomato investment (V219) qualifies a world only with >= 3
# PIZZA_SHOP / FARMERS_MARKET shops and >= 12000 coins at step 432.  Live 2500+ rivals that planted tomatoes in 1-2
# pizza worlds beat our clone lineage by ~2700 (the tomato scarcity premium accumulates while nobody sells tomatoes).
# _F15_TOM = k relaxes the gate to >= k such shops and >= _F15_TOM_MONEY coins; every other check of the base stays.
_F15_Q_ORIG = _v219_qualifies


def _v219_qualifies(obs, native):
    if not _F15_TOM: return _F15_Q_ORIG(obs, native)
    try:
        shops = list(obs['town']['unlocked_shops']); cnt = sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET') for s in shops)
        player = int(obs['player']); farm = obs['farms'][player]
        if cnt < _F15_TOM or int(farm['money']) < _F15_TOM_MONEY: return _F15_Q_ORIG(obs, native)
        farms = list(obs['farms']); farms[player] = dict(farm, money=max(int(farm['money']), 12000))
        obs2 = dict(obs); obs2['farms'] = farms
        obs2['town'] = dict(obs['town'], unlocked_shops=shops + ['PIZZA_SHOP'] * max(0, 3 - cnt))
        return _F15_Q_ORIG(obs2, native)
    except Exception:
        return _F15_Q_ORIG(obs, native)
_F15_ITEMS = ('MILK', 'WOOL', 'STRAWBERRY', 'MELON')
_F15_E81_ITEMS = ('MILK', 'WOOL', 'STRAWBERRY')
_F15_FROM = 216
_F15_TO = 700
_F15_AD_WIN = 48
_F15_AD_MARGIN = 6
_F15_AD_H = 24
_F15_STATE = {}
_F15_REPORT = dict(f15_fires=0, f15_units=0, f15_errors=0, f15_escalated=0)


def _f15_glut(obs, item):
    inv = int(obs['market']['inventory'].get(item, 10000))
    return inv >= int(_R37_MARKET_PARAMS.get(item, {}).get('I0', 10000))


def _f15_planned(player, step, lo, hi):
    plan = {}
    for t in range(step + lo, step + hi + 1):
        for o in _adv_future(player, t):
            if o and len(o) >= 3 and o[0] == 'SELL':
                try: q = max(0, int(o[2]))
                except Exception: q = 0
                if q > 0: plan[o[1]] = plan.get(o[1], 0) + q
    return plan


def _f15_sell(obs, action, wanted):
    """Add SELL orders (or enlarge existing ones) for {item: units}, bounded by the projected shed."""
    market = [list(o) for o in (action.get('market') or []) if o]
    if any(len(o) > 1 and o[0] == 'BUY_PRODUCT' for o in market): return action
    stock = projected_shed(action, FarmView(obs))
    if not isinstance(stock, dict): return action
    selling = {}
    for o in market:
        if len(o) >= 3 and o[0] == 'SELL':
            try: selling[o[1]] = selling.get(o[1], 0) + max(0, int(o[2]))
            except Exception: return action
    changed = False
    for item, want in wanted.items():
        avail = int(stock.get(item, 0)) - selling.get(item, 0)
        n = min(int(want), avail)
        if n <= 0: continue
        same = next((o for o in market if len(o) >= 3 and o[0] == 'SELL' and o[1] == item), None)
        if same is not None: same[2] = int(same[2]) + n
        elif len(market) < 10: market.insert(0, ['SELL', item, n])
        else: continue
        changed = True; _F15_REPORT['f15_fires'] += 1; _F15_REPORT['f15_units'] += n
    if not changed: return action
    out = dict(action, market=market[:10])
    try: out = _lk_reorder(obs, out)
    except Exception: pass
    return out


def _f15_apply(obs, action):
    step = int(obs['step']); player = int(obs['player'])
    if not _F15_FROM <= step < _F15_TO: return action
    if _F15_MODE == 'ad':
        st = _F15_STATE.setdefault(player, {'step': -1, 'own': {}, 'esc': False})
        if step <= st['step']: st.update(step=-1, own={}, esc=False)
        st['step'] = step
        own = 0
        for o in (action.get('market') or []):
            if o and len(o) >= 3 and o[0] == 'SELL' and o[1] in _FX_ITEMS:
                try: own += max(0, int(o[2]))
                except Exception: pass
        st['own'][step] = own
        if not st['esc']:
            flow = _FX_STATE.get(player, {}).get('flow', {})
            rival = sum(q for (t, i), q in flow.items() if step - _F15_AD_WIN <= t < step)
            mine = sum(q for t, q in st['own'].items() if step - _F15_AD_WIN <= t < step)
            if rival >= mine + _F15_AD_MARGIN:
                st['esc'] = True; _F15_REPORT['f15_escalated'] += 1
                globals().update(_EV_H=_F15_AD_H, _DP_H=_F15_AD_H, _MP_H=_F15_AD_H)
        return action
    if step %% 4 != 1: return action
    wanted = {}
    if _F15_MODE == 'wh':
        plan = _f15_planned(player, step, 1, 3)
        wanted = {i: q for i, q in plan.items() if i in _F15_ITEMS}
    elif _F15_MODE == 'e81':
        wanted = {i: 999 for i in _F15_E81_ITEMS}
    elif _F15_MODE == 'e81g':
        wanted = {i: 999 for i in _F15_ITEMS if _f15_glut(obs, i)}
    elif _F15_MODE == 'slk':
        plan = _f15_planned(player, step, 1, 3)
        draw = _v9_town_draw(list(obs['town']['unlocked_shops']), step + 3)
        for i in _F15_ITEMS:
            if _f15_glut(obs, i):
                q = plan.get(i, 0) + int(draw.get(i, 0))
                if q > 0: wanted[i] = q
    if not wanted: return action
    return _f15_sell(obs, action, wanted)


def agent(observation, configuration=None):
    action = _F15_PARENT(observation, configuration)
    try:
        step = int(observation['step'])
        if step == 0:
            _F15_REPORT.update(f15_fires=0, f15_units=0, f15_errors=0, f15_escalated=0)
            if _F15_MODE == 'ad': globals().update(_EV_H=16, _DP_H=16, _MP_H=16)
        standard = configuration is None or all(configuration.get(k, v) == v for k, v in [('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100), ('maxMarketOrdersPerTurn', 10)])
        if standard: action = _f15_apply(observation, action)
    except Exception:
        _F15_REPORT['f15_errors'] += 1
    _F15_TELEMETRY.clear(); _F15_TELEMETRY.update(getattr(_F15_PARENT, 'telemetry', {})); _F15_TELEMETRY.update(_F15_REPORT)
    return action
_F15_TELEMETRY = {}
agent.telemetry = _F15_TELEMETRY
agent = globals().pop('agent')
'''

VARIANTS = {
    'f15_wh': ('wh', 0, 'Frontier14B + window-head sale of this window planned lots (MILK/WOOL/STRAWBERRY/MELON)'),
    'f15_e81': ('e81', 0, 'Frontier14B + E081 full projected shed of MILK/WOOL/STRAWBERRY at every window head'),
    'f15_e81g': ('e81g', 0, 'Frontier14B + E081 restricted to items in glut (inventory >= I0), MELON included'),
    'f15_slk': ('slk', 0, 'Frontier14B + window-head planned lots + next town draw, items in glut only'),
    'f15_ad': ('ad', 0, 'Frontier14B + rival-adaptive window escalation 16 -> 24'),
    'f15_tom2': ('none', 2, 'Frontier14B + tomato investment gate relaxed to >= 2 pizza/farmers shops and >= 9000 coins'),
    'f15_tom1': ('none', 1, 'Frontier14B + tomato investment gate relaxed to >= 1 pizza/farmers shop and >= 9000 coins'),
    'f15_e81_tom2': ('e81', 2, 'Frontier14B + E081 window-head liquidation + tomato gate >= 2 shops'),
    'f15_e81_tom1': ('e81', 1, 'Frontier14B + E081 window-head liquidation + tomato gate >= 1 shop'),
}


def build(name):
    mode, tom, note = VARIANTS[name]
    src = build_f14.build('f14_adv4_h16')
    nl = chr(10)
    return src + nl + ('# Frontier15 (%s): %s' % (name, note)) + nl + (LAYER % {'mode': mode, 'tom': tom}).replace('\n', nl)


if __name__ == '__main__':
    manifest = {'parent': 'f14_adv4_h16', 'variants': {}}
    for name, (mode, tom, note) in VARIANTS.items():
        src = build(name)
        compile(src.replace('\r\n', '\n'), name, 'exec')
        Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
        manifest['variants'][name] = dict(mode=mode, tom=tom, note=note, sha256=hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest())
        print('wrote', name, len(src))
    Path('results/frontier15').mkdir(parents=True, exist_ok=True)
    Path('results/frontier15/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
