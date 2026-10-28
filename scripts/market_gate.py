"""Experimental public-demand / observed-supply gate for V37 sale advances.

Original project code, Apache-2.0. Embedded by build_market_gate.py.
This is a short-horizon scenario heuristic, not a learned Q-function or a
guaranteed safe policy improvement algorithm. No opponent private state.
"""
import math as _lab_math

_LAB_SHOPS = {
    'BAKERY': ('EGG', 'WHEAT'),
    'PIZZA_SHOP': ('MILK', 'TOMATO', 'WHEAT'),
    'BRUNCH_SPOT': ('EGG', 'WHEAT', 'STRAWBERRY'),
    'YARN_STORE': ('WOOL',),
    'ICE_CREAM_SHOP': ('STRAWBERRY', 'MILK', 'WHEAT'),
    'PET_CAFE': ('CARROT',),
    'SMOOTHIE_SHOP': ('STRAWBERRY', 'MILK'),
    'FARMERS_MARKET': ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY'),
}
_LAB_ITEMS = ('CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL')
_LAB_GATE_STATES = {}
_LAB_GATE_REPORT = {}


def _lab_drain(shops, item, start, end):
    """Inventory removed AFTER actions at steps in [start, end), default config."""
    per_shop = sum((2 if len(_LAB_SHOPS[s]) == 1 else 1)
                   for s in shops if item in _LAB_SHOPS.get(s, ()))
    return sum((per_shop if t % 4 == 0 else 0) +
               (1 if t % 24 == 0 and item != 'FERTILIZER' else 0)
               for t in range(start, end))


def _lab_gate_before(obs, config):
    seat, step = int(obs['player']), int(obs['step'])
    old = _LAB_GATE_STATES.get(seat)
    if old is None or step <= old['step']:
        old = _LAB_GATE_STATES[seat] = dict(step=-1, samples={p: [] for p in _LAB_ITEMS})
        _LAB_GATE_REPORT.clear()
        _LAB_GATE_REPORT.update(gate_considered=0, gate_waits=0, gate_held_units=0,
                                gate_observed_trades=0, gate_errors=0)
    supported = all((config or {}).get(k, v) == v for k, v in
                    [('townShopSellInterval', 4), ('townCenterSellInterval', 24),
                     ('shedCapacity', 100), ('turnsPerDay', 24), ('episodeSteps', 720)])
    old['supported'] = supported
    if supported and old['step'] == step - 1 and 'previous' in old:
        previous = old['previous']
        for item in _LAB_ITEMS:
            # No own order for this product: market residual is observable rival
            # supply above the $1 floor. Other products cannot buy these goods.
            # Missing/ambiguous observations are omitted, never filled with zero.
            if item in previous['own_items']:
                continue
            if min(previous['prices'][item], obs['market']['prices'][item]) <= 1:
                continue
            delta = (obs['market']['inventory'][item] - previous['inventory'][item]
                     + _lab_drain(previous['shops'], item, step - 1, step))
            if delta < 0 or delta > 100:
                continue
            old['samples'][item].append((step, float(delta)))
            if delta:
                _LAB_GATE_REPORT['gate_observed_trades'] += 1
    for item in _LAB_ITEMS:
        old['samples'][item] = [(t, v) for t, v in old['samples'][item] if t > step - 48]
    old['step'] = step


def _lab_gate_after(obs, action):
    st = _LAB_GATE_STATES[int(obs['player'])]
    st['previous'] = dict(inventory=dict(obs['market']['inventory']),
                          prices=dict(obs['market']['prices']),
                          shops=list(obs['town']['unlocked_shops']),
                          own_items={o[1] for o in action.get('market', []) if len(o) > 1})


def _lab_allow_advance(obs, action, stock, item, reservations):
    """Keep the baseline unless a delayed sale wins every modeled scenario."""
    st = _LAB_GATE_STATES.get(int(obs['player']))
    if not st or not st['supported'] or not reservations:
        return True
    step = int(obs['step'])
    due = min(t for t, q in reservations)
    # Never defer across a day / route boundary, terminal window, or purchases.
    if due >= (step // 24 + 1) * 24 - 1 or step >= 648:
        return True
    if obs['farms'][int(obs['player'])]['money'] < 12000:
        return True
    carried = sum(sum(inv.values()) for inv in obs['private']['inventories'])
    if sum(stock.values()) + carried > 65:
        return True
    native = _IMPL.chassis.players[int(obs['player'])]
    tape = _IMPL.chassis.routes[native['route']]
    if any(o and o[0] != 'SELL' for t in range(step, due + 1)
           for o in (action if t == step else tape[t]).get('market', [])):
        return True
    drain = _lab_drain(obs['town']['unlocked_shops'], item, step, due)
    if not drain:
        return True
    quantity = sum(q for t, q in reservations)
    inventory = obs['market']['inventory'][item]
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for key, patch in obs['market'].get('params', {}).items():
        if key in params:
            params[key].update(patch)
    supply = 0
    if _LAB_GATE_MODE == 'belief':
        samples = [v for t, v in st['samples'][item]]
        if len(samples) < 12:
            return True
        avg = sum(samples) / len(samples)
        sd = _lab_math.sqrt(sum((v - avg) ** 2 for v in samples) / len(samples))
        animal = {'EGG': 'GOOSE', 'MILK': 'COW', 'WOOL': 'SHEEP'}.get(item)
        rival = obs['farms'][1 - int(obs['player'])]
        standing = sum(max(0, int(tile.get('yield_units', 0)))
                       for row in rival['tiles'] for tile in row if isinstance(tile, dict)
                       and (tile.get('crop') == item or
                            (animal is not None and tile.get('animal') == animal)))
        # Three deliberately simple stress scenarios. This is not a calibrated
        # confidence bound on hidden inventory, and quiet-turn sampling is selective.
        supply = max(2, int(_lab_math.ceil((avg + sd) * (due - step) + min(24, standing) / 4)))
    _LAB_GATE_REPORT['gate_considered'] += 1
    now = sum(_r37_market_price(item, inventory + j, params) for j in range(quantity))
    values = [sum(_r37_market_price(item, inventory - drain + extra + j, params)
                  for j in range(quantity)) for extra in (0, supply // 2, supply)]
    if min(values) >= now + max(6, 0.01 * now):
        _LAB_GATE_REPORT['gate_waits'] += 1
        _LAB_GATE_REPORT['gate_held_units'] += quantity
        return False
    return True
