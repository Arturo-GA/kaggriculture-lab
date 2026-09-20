"""Assemble Frontier9 candidates: Frontier8 (f8_stack_lock, all public sources pinned in build_f8.py) + bounded pre-emption.

In the public v9/4 agent the RACEGATE layer never pulls a sale forward when the item's quote is at or below its base
price: the lot waits in the shed for the route's own sale turn T while the town drains the glut.  Every public clone does
the same, so both farms sit on identical lots, and private derivatives that sell a turn or two earlier took a third of our
live losses (outputs of the 20 September audit, FRONTIER9_RESULTS.es.md).  With lot n, local slope b and town drain r per
turn, selling k turns before a rival who sells at T is worth b*n*(n - r*k) relative coins: positive up to k = n/r and
largest for small k (Fudenberg-Tirole pre-emption; Brunnermeier-Pedersen and Carlin-Lobo-Viswanathan predatory trading).
The patch therefore lets a glutted STRAWBERRY / MILK / WOOL lot be reserved forward by at most
K = min(KMAX, floor(lot / drain)) turns, with the drain computed from the unlocked shops, using the public layer's own
debt ledger so later route sales stay consistent.  Nothing else changes.
"""
import hashlib
import json
from pathlib import Path

import build_f8

F8_SHA256 = 'e5529ee0b1a7f139497c885009b797edc8c5867e4ec0e97e67a55babcaa2a77e'
BASE = build_f8.VARIANTS['f8_stack_lock'][0]
assert hashlib.sha256(BASE.encode('utf-8')).hexdigest() == F8_SHA256, 'Frontier8 source changed'

MARKER = "_V9_RACEGATE_RESERVE = _r36_reserve\n"
OLD_SKIP = ("        if item in blocked or item in glutted or view.prices.get(item, 0) < 2:\n"
            "            continue\n")
NEW_SKIP = ("        if item in blocked or view.prices.get(item, 0) < 2:\n"
            "            continue\n"
            "        if item in glutted and item not in _F9_PRE_ITEMS:\n"
            "            continue\n")
OLD_END = "        item_end = min(end, step + _v9_hz[item]) if _v9_hz and item in _v9_hz else end\n"
NEW_END = (OLD_END +
           "        if item in glutted:\n"
           "            _f9_w = _f9_pre_window(obs, item, available)\n"
           "            if _f9_w <= 0:\n"
           "                continue\n"
           "            item_end = min(item_end, step + _f9_w)\n")
HELPER = '''
# ---- Frontier9 bounded pre-emption (Arturo-GA / Kaggriculture Lab, Apache-2.0); see build_f9.py ----
_F9_PRE_ITEMS = ("STRAWBERRY", "MILK", "WOOL")
_F9_PRE_KMAX = %d
_F9_PRE_SHOPS = {"BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"), "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
                 "YARN_STORE": ("WOOL",), "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT",),
                 "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"), "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY")}


def _f9_pre_window(obs, item, lot):
    """Turns a glutted lot may be sold ahead of the route: never beyond lot / town drain per turn."""
    drain = 1.0 / 24.0
    for shop in (obs.get("town") or {}).get("unlocked_shops", []):
        goods = _F9_PRE_SHOPS.get(shop, ())
        if item in goods:
            drain += (2.0 if len(goods) == 1 else 1.0) / 4.0
    return max(0, min(_F9_PRE_KMAX, int(lot / drain)))

'''


TRACKER = '''

# ==== Frontier9 rival-lead tracker (Arturo-GA / Kaggriculture Lab, Apache-2.0); see build_f9.py ====
# Recovers the rival's sales of the three glut products from the public book (book change + town drain - our own sale;
# exact above the 1-coin floor) and measures how many turns before the route's own sale turn the rival sold.  The bounded
# pre-emption window then answers the lead this rival has shown: K = max(KMAX, lead + 1), still capped by lot / drain.
_F9_TRACK_PARENT = agent
_F9_TRACK_STATE = {}
_F9_TRACK_REPORT = dict(f9_leads_seen=0, f9_max_lead=0, f9_track_errors=0)


def _f9_track(obs, action):
    step = int(obs["step"])
    seat = int(obs["player"])
    st = _F9_TRACK_STATE.get(seat)
    if st is None or step <= st["step"]:
        st = _F9_TRACK_STATE[seat] = {"step": -1, "inv": {}, "sold": {}, "price": {}, "held": {}}
        _F9_PRE_LEAD[seat] = {}
    inventory = obs["market"]["inventory"]
    prices = obs["market"]["prices"]
    shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
    if st["step"] == step - 1 and step >= 193:
        tape = _IMPL.chassis.routes[_IMPL.chassis.players[seat]["route"]]
        for item in _F9_PRE_ITEMS:
            prev = st["inv"].get(item)
            if prev is None:
                continue
            drain = 0
            if (step - 1) % 4 == 0:
                for shop in shops:
                    goods = _F9_PRE_SHOPS.get(shop, ())
                    if item in goods:
                        drain += 2 if len(goods) == 1 else 1
            if (step - 1) % 24 == 0:
                drain += 1
            rival_sold = int(inventory[item]) - prev + drain - st["sold"].get(item, 0)
            # a lead only counts when we were sitting on a lot of the same item in a glutted book and did not sell it
            if (rival_sold < 2 or st["price"].get(item, 10 ** 6) > _F9_PRE_BASE[item]
                    or st["held"].get(item, 0) < 2 or st["sold"].get(item, 0) > 0):
                continue
            for due in range(step - 1, min(len(tape), step + 40)):
                future = tape[due] if isinstance(tape[due], dict) else {}
                if any(len(o) >= 3 and o[0] == "SELL" and o[1] == item for o in (future.get("market") or [])):
                    lead = due - (step - 1)
                    if lead > 0:
                        leads = _F9_PRE_LEAD[seat].setdefault(item, [])
                        leads.append(lead)
                        del leads[:-3]
                        _F9_TRACK_REPORT["f9_leads_seen"] += 1
                        _F9_TRACK_REPORT["f9_max_lead"] = max(_F9_TRACK_REPORT["f9_max_lead"], lead)
                    break
    stock = projected_shed(action, FarmView(obs))
    left = {k: max(0, int(v)) for k, v in stock.items()}
    sold = {}
    for o in action.get("market") or []:
        if len(o) >= 3 and o[0] == "SELL" and int(prices.get(o[1], 0)) > 1:
            q = min(max(0, int(o[2])), left.get(o[1], 0))
            left[o[1]] = left.get(o[1], 0) - q
            sold[o[1]] = sold.get(o[1], 0) + q
    st["sold"] = sold
    st["held"] = {item: left.get(item, 0) for item in _F9_PRE_ITEMS}
    st["inv"] = {item: int(inventory[item]) for item in _F9_PRE_ITEMS}
    st["price"] = {item: int(prices.get(item, 0)) for item in _F9_PRE_ITEMS}
    st["step"] = step


def agent(observation, configuration=None):
    action = _F9_TRACK_PARENT(observation, configuration)
    try:
        if int(observation["step"]) == 0:
            _F9_TRACK_REPORT.update(f9_leads_seen=0, f9_max_lead=0, f9_track_errors=0)
        if isinstance(action, dict):
            _f9_track(observation, action)
    except Exception:
        _F9_TRACK_REPORT["f9_track_errors"] += 1
    _F9_TRACK_TELEMETRY.clear()
    _F9_TRACK_TELEMETRY.update(dict(getattr(_F9_TRACK_PARENT, "telemetry", {}) or {}))
    _F9_TRACK_TELEMETRY.update(_F9_TRACK_REPORT)
    return action


_F9_TRACK_TELEMETRY = {}
agent.telemetry = _F9_TRACK_TELEMETRY
agent = globals().pop("agent")
'''

ADAPT_WINDOW = '''
_F9_PRE_LEAD = {}
_F9_PRE_LEAD_CAP = 40
_F9_PRE_BASE = {"STRAWBERRY": 120, "MILK": 160, "WOOL": 200}


def _f9_pre_window(obs, item, lot):
    """Turns a glutted lot may be sold ahead of the route: the fixed window, or one turn more than the lead this rival
    has shown on the item, never beyond lot / town drain per turn."""
    drain = 1.0 / 24.0
    for shop in (obs.get("town") or {}).get("unlocked_shops", []):
        goods = _F9_PRE_SHOPS.get(shop, ())
        if item in goods:
            drain += (2.0 if len(goods) == 1 else 1.0) / 4.0
    leads = (_F9_PRE_LEAD.get(int(obs["player"])) or {}).get(item) or []
    window = max(_F9_PRE_KMAX, min(_F9_PRE_LEAD_CAP, max(leads) + 1)) if leads else _F9_PRE_KMAX
    return max(0, min(window, int(lot / drain)))

'''


def adaptive(kmax):
    src = patched(kmax)
    start = src.index("def _f9_pre_window(obs, item, lot):")
    end = src.index(chr(10) + chr(10), src.index("return max(0, min(_F9_PRE_KMAX", start)) + 2
    src = src[:start] + ADAPT_WINDOW.strip() + chr(10) + chr(10) + src[end:]
    return src.rstrip() + chr(10) + TRACKER


def patched(kmax):
    assert BASE.count(MARKER) == 1 and BASE.count(OLD_SKIP) == 1
    head, tail = BASE.split(MARKER, 1)
    assert tail.count(OLD_END) == 1, 'RACEGATE re-implementation not found after the marker'
    tail = tail.replace(OLD_SKIP, NEW_SKIP) if OLD_SKIP in tail else tail
    tail = tail.replace(OLD_END, NEW_END)
    src = head + MARKER + HELPER % kmax + tail
    if OLD_SKIP in src:
        src = src.replace(OLD_SKIP, NEW_SKIP)
    assert NEW_SKIP in src and NEW_END in src
    return src


FULL_A = "        reservations = []" + chr(10)
FULL_B = "        qty = sum(q for _, q in reservations)" + chr(10)


def full_lot(src):
    """When a glutted lot is pre-empted, sell the whole stock of the item: the public chain itself dumps the rest of the
    stock the turn after its route sale, so going first with the route's planned amount only leaves the rest behind."""
    head, tail = src.split(MARKER, 1)
    assert tail.count(FULL_A) == 1 and tail.count(FULL_B) == 1
    tail = tail.replace(FULL_A, FULL_A + "        _f9_all = available" + chr(10))
    tail = tail.replace(FULL_B, FULL_B + "        if qty and item in glutted:" + chr(10) + "            qty = max(qty, _f9_all)" + chr(10))
    return head + MARKER + tail


VARIANTS = {
    'f9_pre3': (3, 'f8_stack_lock + bounded pre-emption of glutted premium lots, KMAX 3'),
    'f9_pre4': (4, 'f8_stack_lock + bounded pre-emption of glutted premium lots, KMAX 4'),
    'f9_pre8': (8, 'KMAX 8'),
    'f9_pre12': (12, 'KMAX 12'),
    'f9_pre20': (20, 'KMAX 20'),
    'f9_pre40': (40, 'KMAX 40 (window = lot / drain, effectively uncapped)'),
    'f9_pre4a': (4, 'KMAX 4, widened to one turn more than the lead the rival has shown (tracker layer appended)'),
    'f9_pre4f': (4, 'KMAX 4, and a pre-empted glutted lot takes the whole stock of the item with it'),
    'f9_pre8c': (8, 'KMAX 8 + one-day wheat feed reserve in the public CARROT2 layer (_CA_FEED_DAYS 2 -> 1); exported candidate'),
}
CARROT_OLD = '_CA_FEED_DAYS = 2'
CARROT_NEW = '_CA_FEED_DAYS = 1'


def carrot_reserve(src):
    lines = src.split(chr(10))
    hits = [i for i, line in enumerate(lines) if line.rstrip(chr(13)) == CARROT_OLD]
    assert len(hits) == 1, hits
    lines[hits[0]] = lines[hits[0]].replace(CARROT_OLD, CARROT_NEW)
    return chr(10).join(lines)


def write(name, src):
    compile(src.replace('\r\n', '\n'), name, 'exec')
    Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
    print('wrote', name, len(src))


if __name__ == '__main__':
    manifest = {'f8_sha256': F8_SHA256, 'variants': {}}
    for name, (kmax, note) in VARIANTS.items():
        src = adaptive(kmax) if name.endswith('a') else patched(kmax)
        src = full_lot(src) if name.endswith('f') else src
        write(name, carrot_reserve(src) if name.endswith('c') else src)
        manifest['variants'][name] = dict(kmax=kmax, note=note,
                                          sha256=hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest())
    Path('results/frontier9').mkdir(parents=True, exist_ok=True)
    Path('results/frontier9/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))
