# ==== Frontier9 best-response sale scheduler for glutted premium books (Arturo-GA / Kaggriculture Lab, Apache-2.0) ====
# Glut books (strawberry, milk, wool above the neutral inventory) only recover through the town's drain, and the impact
# of a sale is permanent.  The relative value of selling our lot now instead of at a later turn tau is therefore
# slope * lot * (2 * rival units sold in between - town drain in between): pre-empt a rival lot that is about to land,
# wait when the town will drain more than twice what the rival still sells.  Public clones either dump on the tape's
# turn (70 strawberries a game at ~13 coins in top-team replays) or sit on the lot behind RACEGATE and get pre-empted by
# one turn (a third of our live losses).  This layer decides both cases with one rule: in the glut regime it replays
# the book forward with the exact engine price function, the known drain of the unlocked shops and the rival's
# predicted sales (our own route's future SELL orders, shifted by the lead this rival has shown), and sells the whole
# lot now only if no later candidate turn gives a better modeled margin (our revenue minus the rival's).  Outside the
# glut regime, without stock, with a rival that is not clone-like, near the shed limit or in the last turns the public
# route decides.  Nothing else in the action changes.
_BR_PARENT = agent
_BR_ITEMS = ("STRAWBERRY", "MILK", "WOOL")
_BR_BASE = {"STRAWBERRY": 120, "MILK": 160, "WOOL": 200}
_BR_SHOPS = {"BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"), "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
             "YARN_STORE": ("WOOL",), "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
             "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"), "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY")}
_BR_FROM = 288
_BR_LAST = 712
_BR_MIN_SIMILARITY = 0.80
_BR_MIN_GAIN = 25.0
_BR_HOLD_MAX_RATIO = 1.0
_BR_SHED_LIMIT = 93
_BR_MAX_LEAD = 12
_BR_STATE = {}
_BR_REPORT = dict(br_decisions=0, br_held_turns=0, br_held_units=0, br_sold_now=0, br_released_units=0,
                  br_forced=0, br_errors=0)


def _br_params(obs):
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for k, patch in (obs["market"].get("params") or {}).items():
        if k in params and isinstance(patch, dict):
            params[k].update(patch)
    return params


def _br_drain(shops, item, turn):
    """Units the town removes after the market of `turn` (engine: shops every 4 turns, centre every 24)."""
    n = 0
    if turn % 4 == 0:
        for shop in shops:
            goods = _BR_SHOPS.get(shop, ())
            if item in goods:
                n += 2 if len(goods) == 1 else 1
    if turn % 24 == 0:
        n += 1
    return n


def _br_rival_schedule(tape, item, step, lead):
    """Rival sales per future turn: our route's own SELL orders for the item, moved `lead` turns earlier."""
    plan = {}
    for due in range(step + 1, min(len(tape), 719)):
        future = tape[due]
        if not isinstance(future, dict):
            continue
        q = sum(max(0, int(o[2])) for o in (future.get("market") or []) if len(o) >= 3 and o[0] == "SELL" and o[1] == item)
        if q:
            at = max(step + 1, due - lead)
            plan[at] = plan.get(at, 0) + q
    return plan


_BR_PRICE_CACHE = {}


def _br_price(item, inv, params):
    key = (item, inv)
    p = _BR_PRICE_CACHE.get(key)
    if p is None:
        if len(_BR_PRICE_CACHE) > 20000:
            _BR_PRICE_CACHE.clear()
        p = _BR_PRICE_CACHE[key] = _r37_market_price(item, inv, params)
    return p


def _br_events(shops, item, step, rival_now, plan):
    """(turn, rival units, drain) for every turn from `step` on where the book moves."""
    events = []
    for turn in range(step, 718):
        theirs = rival_now if turn == step else plan.get(turn, 0)
        drain = _br_drain(shops, item, turn)
        if theirs or drain:
            events.append((turn, theirs, drain))
    return events


def _br_margin(item, params, inv, events, lot, sell_at):
    """Modeled (our revenue - rival revenue) on this book if we sell `lot` units at `sell_at` (exact engine quotes)."""
    own = rival = 0.0
    sold = False
    for turn, theirs, drain in events:
        if not sold and turn >= sell_at:
            mine = lot
            sold = True
            if turn > sell_at:  # our sale falls on a quiet turn before this event
                while mine > 0:
                    p = _br_price(item, inv, params)
                    own += p
                    mine -= 1
                    if p > 1:
                        inv += 1
        else:
            mine = 0
        # same-index lockstep: alternate units while both still sell
        while mine > 0 or theirs > 0:
            if mine > 0:
                p = _br_price(item, inv, params)
                own += p
                mine -= 1
                if p > 1:
                    inv += 1
            if theirs > 0:
                p = _br_price(item, inv, params)
                rival += p
                theirs -= 1
                if p > 1:
                    inv += 1
        inv -= drain
    if not sold:
        mine = lot
        while mine > 0:
            p = _br_price(item, inv, params)
            own += p
            mine -= 1
            if p > 1:
                inv += 1
    return own - rival


def _br_apply(obs, action):
    step = int(obs["step"])
    seat = int(obs["player"])
    st = _BR_STATE.get(seat)
    if st is None or step <= st["step"]:
        st = _BR_STATE[seat] = {"step": -1, "inv": {}, "sold": {}, "lead": {i: 0 for i in _BR_ITEMS}}
    market = [list(o) if isinstance(o, (list, tuple)) else [] for o in (action.get("market") or [])]
    shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
    inventory = obs["market"]["inventory"]
    native = _IMPL.chassis.players[seat]
    tape = _IMPL.chassis.routes[native["route"]]
    # lead the rival has shown: units it sold last turn (book delta + drain - our sale) against the route's next sale turn
    for item in _BR_ITEMS:
        prev = st["inv"].get(item)
        if prev is not None and st["step"] == step - 1:
            rival_sold = int(inventory[item]) - prev + _br_drain(shops, item, step - 1) - st["sold"].get(item, 0)
            if rival_sold >= 3:
                for due in range(step - 1, min(len(tape), step + _BR_MAX_LEAD)):
                    future = tape[due] if isinstance(tape[due], dict) else {}
                    if any(len(o) >= 3 and o[0] == "SELL" and o[1] == item for o in (future.get("market") or [])):
                        st["lead"][item] = max(st["lead"][item], min(_BR_MAX_LEAD, due - (step - 1)))
                        break
        st["inv"][item] = int(inventory[item])
    st["step"] = step

    def finish(final):
        stock = projected_shed(action, FarmView(obs))
        sold = {}
        left = {k: max(0, int(v)) for k, v in stock.items()}
        for o in final:
            if len(o) >= 3 and o[0] == "SELL":
                q = min(max(0, int(o[2])), left.get(o[1], 0))
                left[o[1]] = left.get(o[1], 0) - q
                sold[o[1]] = sold.get(o[1], 0) + q
        st["sold"] = sold
        return action if final is market and final == (action.get("market") or []) else dict(action, market=final)

    if not _BR_FROM <= step <= _BR_LAST or _r37_similarity(obs) < _BR_MIN_SIMILARITY:
        return finish(market)
    view = FarmView(obs)
    stock = projected_shed(action, view)
    carried = sum(max(0, int(n)) for i in range(len(view.positions)) for n in view.inv(i).values())
    total = sum(max(0, int(v)) for v in stock.values())
    hour = step % 24
    prices = obs["market"]["prices"]
    params = _br_params(obs)
    for item in _BR_ITEMS:
        have = max(0, int(stock.get(item, 0)))
        if have <= 0 or int(prices.get(item, 0)) > _BR_BASE[item]:
            continue
        idx = [i for i, o in enumerate(market) if len(o) >= 3 and o[0] == "SELL" and o[1] == item]
        if any(len(o) >= 2 and o[0] == "BUY_PRODUCT" and o[1] == item for o in market):
            continue
        planned = min(have, sum(max(0, int(market[i][2])) for i in idx))
        inv = int(inventory[item])
        plan = _br_rival_schedule(tape, item, step, st["lead"][item])
        rival_now = planned  # a clone on the same turn sells what our route sells now
        dumps = sorted(plan)
        candidates = [step] + [t - 1 for t in dumps if t - 1 > step] + [t + 1 for t in dumps[-2:]] + [716]
        candidates = sorted({min(716, c) for c in candidates if c >= step})[:14]
        best_t, best_v, now_v = step, None, None
        events = _br_events(shops, item, step, rival_now, plan)
        for cand in candidates:
            v = _br_margin(item, params, inv, events, have, cand)
            if cand == step:
                now_v = v
            if best_v is None or v > best_v + 1e-9:
                best_t, best_v = cand, v
        _BR_REPORT["br_decisions"] += 1
        hold = (best_t != step and best_v - now_v >= _BR_MIN_GAIN
                and int(prices.get(item, 0)) <= _BR_HOLD_MAX_RATIO * _BR_BASE[item])
        room = _BR_SHED_LIMIT - (total - planned) - carried  # shed room if this item's planned sale still happens
        if hold and (room - planned < 0 or (hour >= 21 and total + carried > _BR_SHED_LIMIT)):
            hold = False
            _BR_REPORT["br_forced"] += 1
        if hold:
            for i in idx:
                market[i] = []
            _BR_REPORT["br_held_turns"] += 1
            _BR_REPORT["br_held_units"] += planned
        elif have > planned:
            # now is the best modeled turn for the whole lot: sell the stock the route did not plan to sell too
            if idx:
                market[idx[0]] = ["SELL", item, have]
                for i in idx[1:]:
                    market[i] = []
            else:
                holes = [i for i, o in enumerate(market) if not o]
                if holes:
                    market[holes[0]] = ["SELL", item, have]
                elif len(market) < 10:
                    market.append(["SELL", item, have])
                else:
                    continue
            _BR_REPORT["br_sold_now"] += 1
            _BR_REPORT["br_released_units"] += have - planned
    return finish(market)


def agent(observation, configuration=None):
    action = _BR_PARENT(observation, configuration)
    try:
        if int(observation["step"]) == 0:
            for key in _BR_REPORT:
                _BR_REPORT[key] = 0
        standard = configuration is None or all(configuration.get(k, v) == v for k, v in [
            ("boardSize", 10), ("turnsPerDay", 24), ("shedCapacity", 100), ("maxMarketOrdersPerTurn", 10),
            ("townShopSellInterval", 4), ("townCenterSellInterval", 24)])
        if standard and isinstance(action, dict):
            action = _br_apply(observation, action)
    except Exception:
        _BR_REPORT["br_errors"] += 1
    _BR_TELEMETRY.clear()
    _BR_TELEMETRY.update(dict(getattr(_BR_PARENT, "telemetry", {}) or {}))
    _BR_TELEMETRY.update(_BR_REPORT)
    return action


_BR_TELEMETRY = {}
agent.telemetry = _BR_TELEMETRY
agent = globals().pop("agent")
