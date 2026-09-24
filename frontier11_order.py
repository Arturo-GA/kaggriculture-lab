
# ==== Frontier11 robust order-book response (Arturo-GA / Kaggriculture Lab, Apache-2.0) ====
# The engine settles both market lists slot by slot, one unit at a time at the same quote, so the order of a list
# decides who sells into whose glut.  Layer D of this base (shiiin9, "Your Market List Is an Order Book") plays the
# best response to the list the stack produced BEFORE D, i.e. to a copy of the stack without D.  A copy of this very
# stack plays the FINAL list, and a response layer one level up (Order Book v3) plays the best response to that final
# list.  This layer scores the orderings D considers against those three rival lists at once, with D's own per-unit
# lockstep evaluator, and plays the ordering with the best weighted margin among those that lose ground against none
# of the three.  It adds, removes and resizes nothing; purchases, round trips and empty slots stay where D left them.
# Requires the base's _v44y_factor_margin, _v44y_params, projected_shed and FarmView (V48 lineage); uses layer D's
# pre-D list (_CXD_PARENT_ORDERS) when the base has D.  The builder binds _F11_PARENT to the base's real entry point.
import itertools as _f11_it
_F11_FIXED = ('HIRE', 'BUY_SEED', 'BUY_ANIMAL', 'BUY_LAND')
_F11_PRE = globals().get('_CXD_PARENT_ORDERS')
_F11_BUDGET = 700
_F11_W = (1.0, 2.0, 1.0)
_F11_TOL = 0.5
_F11_MIN_GAIN = 2.0
_F11_HARD = True
_F11_REPORT = dict(f11_turns=0, f11_changed=0, f11_gain=0.0, f11_evals=0, f11_budget_hits=0, f11_errors=0)


def _f11_split(orders):
    bought = {o[1] for o in orders if o and len(o) > 1 and o[0] == 'BUY_PRODUCT'}
    slots, sells, fixed = [], [], []
    for i, o in enumerate(orders):
        if not o:
            continue
        if o[0] in _F11_FIXED:
            slots.append(i); fixed.append(o)
        elif o[0] == 'SELL' and len(o) > 1 and o[1] not in bought:
            slots.append(i); sells.append(o)
    return slots, sells, fixed


def _f11_candidates(orders, slots, sells, fixed):
    """Orderings of `sells` over `slots`, fixed-price orders filling the rest in their own order (as layer D)."""
    for positions in _f11_it.permutations(slots, len(sells)):
        out = list(orders)
        rest = [i for i in slots if i not in positions]
        for i, order in zip(positions, sells):
            out[i] = order
        for i, order in zip(rest, fixed):
            out[i] = order
        yield out


def _f11_best_response(orders, slots, sells, fixed, margin):
    best, best_orders, evals = margin(orders), orders, 0
    for cand in _f11_candidates(orders, slots, sells, fixed):
        if cand == orders:
            continue
        evals += 1
        if evals > _F11_BUDGET:
            break
        value = margin(cand)
        if value > best + 0.5:
            best, best_orders = value, cand
    return best_orders, evals


def _f11_reorder(obs, action):
    market = action.get('market') or []
    if len(market) < 2:
        return action
    orders = [list(o) if isinstance(o, (list, tuple)) else o for o in market]
    slots, sells, fixed = _f11_split(orders)
    if not sells or len(slots) < 2:
        return action
    _F11_REPORT['f11_turns'] += 1
    params = _v44y_params(obs)
    stock = {k: max(0, int(v)) for k, v in projected_shed(action, FarmView(obs)).items()}
    inv0 = {k: int(v) for k, v in obs['market']['inventory'].items()}
    pre = [list(o) for o in (_F11_PRE or []) if o] or orders
    m_pre = _v44y_factor_margin(pre, inv0, stock, params)
    m_fin = _v44y_factor_margin(orders, inv0, stock, params)
    up, evals = _f11_best_response(orders, slots, sells, fixed, m_fin)
    m_up = _v44y_factor_margin(up, inv0, stock, params)
    models = (m_pre, m_fin, m_up)
    base = [f(orders) for f in models]

    def score(values):
        return sum(w * v for w, v in zip(_F11_W, values))
    base_score = best_score = score(base)
    best_orders = None
    for cand in _f11_candidates(orders, slots, sells, fixed):
        if cand == orders:
            continue
        evals += 1
        if evals > 2 * _F11_BUDGET:
            _F11_REPORT['f11_budget_hits'] += 1
            break
        values = [f(cand) for f in models]
        if _F11_HARD and any(v < b - _F11_TOL for v, b in zip(values, base)):
            continue
        s = score(values)
        if s > best_score + _F11_MIN_GAIN:
            best_score, best_orders = s, cand
    _F11_REPORT['f11_evals'] += evals
    if best_orders is None:
        return action
    _F11_REPORT['f11_changed'] += 1
    _F11_REPORT['f11_gain'] += best_score - base_score
    return dict(action, market=best_orders)


def agent(observation, configuration=None):
    # D refreshes _CXD_PARENT_ORDERS only on turns it scores; clear it so a stale list is never used as a rival model
    if _F11_PRE is not None:
        _F11_PRE[:] = []
    action = _F11_PARENT(observation, configuration)
    try:
        if int(observation.get('step', 0)) == 0:
            _F11_REPORT.update(f11_turns=0, f11_changed=0, f11_gain=0.0, f11_evals=0, f11_budget_hits=0, f11_errors=0)
        standard = configuration is None or all(configuration.get(k, v) == v for k, v in [('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100), ('maxMarketOrdersPerTurn', 10)])
        if standard:
            action = _f11_reorder(observation, action)
    except Exception:
        _F11_REPORT['f11_errors'] += 1
    _F11_TELEMETRY.clear()
    _F11_TELEMETRY.update(getattr(_F11_PARENT, 'telemetry', {}) or {})
    _F11_TELEMETRY.update(_F11_REPORT)
    return action


_F11_TELEMETRY = {}
agent.telemetry = _F11_TELEMETRY
agent = globals().pop('agent')
