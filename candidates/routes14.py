# Modified 2026-09-12 by Arturo-GA: experimental integration of yhay81
# Shop Router 0911 Simple 14-route data and shop mapping into V37.
# All original Apache-2.0 notices retained; see NOTICE.md.
# EXP-173 isolate opening market sequence inspired by yhay81/shop-router-0911-simple (Apache-2.0).
# Kaggriculture EXP-167 candidate. Not submitted automatically.
# Attribution: thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
# prvsiyan and Dmitrii Gluzdov. Apache-2.0 derivations; notices retained below.
# Kaggriculture v31 / EXP-157, Ahmed Berat Ozer, September 9 2026.
# Selected mechanism: crop_public_order. New independent confirmation is required.
# Public V221B/V224C production/timing lineage: prvsiyan, Apache-2.0.
# Original economics and integration; retained upstream licenses follow.
# Kaggriculture v28 / EXP-154, Ahmed Berat Ozer, September 9 2026.
# Changes: aurax7 day-end storage guard; Dmitrii Gluzdov physical terminal rescue
# adapted to v27, with 64 deterministic simulations. Apache-2.0.
# New action tapes and ordered shop-pair map: yhay81/shop-router-0909, Apache-2.0.
# Kaggriculture v25, EXP-149: Shop0908 production, sale lead, terminal cargo rescue.
# Runtime chassis: Apache-2.0; thomastschinkel, yhay81, tetsutani.
# Routing and public action data: yhay81/shop-router-0908, frozen September 8, 2026.
# 
#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/
# 
#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
# 
#    1. Definitions.
# 
#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.
# 
#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.
# 
#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.
# 
#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.
# 
#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.
# 
#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.
# 
#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).
# 
#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.
# 
#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."
# 
#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.
# 
#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.
# 
#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.
# 
#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:
# 
#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and
# 
#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and
# 
#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and
# 
#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.
# 
#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.
# 
#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.
# 
#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.
# 
#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.
# 
#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.
# 
#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.
# 
#    END OF TERMS AND CONDITIONS
# 
#    APPENDIX: How to apply the Apache License to your work.
# 
#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.
# 
#    Copyright [yyyy] [name of copyright owner]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Kaggriculture route-replay chassis (pure Python, stdlib only).

A *route* is a pre-computed tape of 719 Kaggle-format actions
``{"farmer": [op, ...], "hands": [[op, ...], ...], "market": [[order, item, qty], ...]}``.
The chassis replays the tape chosen by a caller-supplied ``router`` and wraps it
in small reactive layers (each independently switchable via ``settings``):

    hand_align            pad/truncate hands to the real hand count      (fieldbook_logic)
    weed_repair           DIG a weed that blocks PLANT/BUILD, replay      (tetsutani + task spec)
    sell_lead             sell next step's lots one step early            (fieldbook _lead_sale)
    front_run             sell before the opponent's scheduled SELL       (hook; opponent_plan)
    budget_guard          fund each 72-step block's purchases             (six_day_budget_guard.hpp)
    room_guard            keep shed <= 99 at hour 23                      (tetsutani)
    clamp_sells           trim SELL orders to the projected shed          (tetsutani)
    dead_stock            sell stock the route will never sell            (tetsutani)
    terminal_liquidation  step >= 718: sell the whole projected shed      (fieldbook _terminal_sale)

Engine facts (verified against kaggle_environments 1.32.7, env_1_32_7.py):
  observation["farms"][p] = {"money", "tiles"[y][x], "farmer"[x,y], "hands"[[x,y]..],
                             "unlocked_quadrants", "hires_today"}
  tiles: None (empty) | "LOCKED" | {"kind": WEED|COOP|PASTURE|PLANT, "crop"/"animal", ...}
  observation["private"] = {"shed": {item: n}, "seeds": {crop: n}, "inventories": [{}...]}
  observation["market"] = {"inventory": {...}, "prices": {...}}
  observation["town"] = {"unlocked_shops": [...]}
  Agents act on steps 0..718 (interpreter marks DONE once step >= episodeSteps-2).
"""
from __future__ import annotations

import copy

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
LAND_PRICES = (1000, 2000, 4000)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FRONT_RUN_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
LAST_ACT_STEP = 718
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

DEFAULT_SETTINGS = {
    "hand_align": True,
    "weed_repair": True,
    "sell_lead": True,
    "front_run": True,
    "budget_guard": True,
    "room_guard": True,
    "clamp_sells": True,
    "dead_stock": True,
    "terminal_liquidation": True,
    # tunables
    "block_turns": 72,
    "shed_capacity": 100,
    "board_size": 10,
    "max_orders": 10,
    "turns_per_day": 24,
    "min_sell_price": 2,
}


# --------------------------------------------------------------------------- helpers
def _get(value, key, default=None):
    """Field access that works for dicts and Kaggle Struct/attribute objects."""
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _step_of(observation):
    raw = _get(observation, "step")
    if raw is not None:
        return _int(raw)
    return _int(_get(observation, "day", 0)) * 24 + _int(_get(observation, "hour", 0))


def _shed_adjacent(pos, board):
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return False
    half = board // 2
    return pos[0] in (half - 1, half) and pos[1] in (half - 1, half)


def _tile_at(tiles, pos):
    try:
        x, y = int(pos[0]), int(pos[1])
        return tiles[y][x]
    except (TypeError, ValueError, IndexError):
        return "LOCKED"


def _is_noop(act, tile, inv, seeds, pos, board):
    """True when the engine will certainly ignore ``act`` (mirrors _apply_unit_action)."""
    if not act:
        return True
    op = act[0]
    x, y = pos[0], pos[1]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    adjacent = _shed_adjacent(pos, board)
    if op == "DROP":
        return (not adjacent) or (not inv)
    if op == "PICKUP":
        return not adjacent
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if item in ANIMAL_STRUCTURE and isinstance(tile, dict) \
                and _get(tile, "kind") == ANIMAL_STRUCTURE[item] and _get(tile, "animal") is None:
            return _int(_get(inv, item, 0)) <= 0
        return (not adjacent) or _int(_get(inv, item, 0)) <= 0
    if tile == "LOCKED":
        return True
    is_dict = isinstance(tile, dict)
    kind = _get(tile, "kind") if is_dict else None
    animal = is_dict and _get(tile, "animal") is not None
    if op == "PLANT":
        return tile is not None or _int(_get(seeds, act[1] if len(act) > 1 else None, 0)) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(_get(tile, "watered_today"))
    if op == "HARVEST":
        return (not is_dict) or _int(_get(tile, "yield_units", 0)) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or _int(_get(inv, "FERTILIZER", 0)) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(_get(tile, "fed_today")) or _int(_get(inv, "WHEAT", 0)) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not _get(tile, "fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(_get(tile, "cared_today"))
    return True


class _View:
    """Cheap per-step snapshot of everything the layers read from the observation."""

    def __init__(self, observation, player, cfg):
        farms = list(_get(observation, "farms", []) or [])
        self.farm = farms[player] if player < len(farms) else {}
        self.rival = farms[1 - player] if len(farms) >= 2 and 1 - player < len(farms) else {}
        private = _get(observation, "private", {}) or {}
        self.shed = {k: max(0, _int(v)) for k, v in dict(_get(private, "shed", {}) or {}).items()}
        self.seeds = dict(_get(private, "seeds", {}) or {})
        self.invs = [dict(i or {}) for i in (_get(private, "inventories", []) or [])]
        market = _get(observation, "market", {}) or {}
        self.prices = {k: _int(v) for k, v in dict(_get(market, "prices", {}) or {}).items()}
        self.money = float(_get(self.farm, "money", 0.0) or 0.0)
        self.tiles = _get(self.farm, "tiles", []) or []
        self.board = len(self.tiles) or cfg["board_size"]
        self.positions = [_get(self.farm, "farmer", None)] + [list(p) for p in (_get(self.farm, "hands", []) or [])]
        self.hires_today = _int(_get(self.farm, "hires_today", 0))
        self.quadrants = len(list(_get(self.farm, "unlocked_quadrants", []) or []))

    def inv(self, idx):
        return self.invs[idx] if idx < len(self.invs) else {}

    def in_hands(self, item):
        return sum(max(0, _int(_get(inv, item, 0))) for inv in self.invs)


# --------------------------------------------------------------------------- chassis
class Chassis:
    """Replays ``routes[router(...)]`` with reactive safety/market layers.

    routes         : {route_id: list of >= 719 Kaggle action dicts}
    router         : callable(observation, step, state_dict) -> route_id, called every
                     step; ``state_dict`` is per-player and persists across the game.
    settings       : overrides for DEFAULT_SETTINGS (layer switches + tunables)
    opponent_plan  : optional list of the opponent's expected actions (front_run hook)
    """

    def __init__(self, routes, router=None, settings=None, opponent_plan=None):
        self.routes = {rid: list(tape) for rid, tape in routes.items()}
        self.router = router or (lambda observation, step, state: next(iter(self.routes)))
        self.cfg = dict(DEFAULT_SETTINGS)
        self.cfg.update(settings or {})
        self.opponent_plan = opponent_plan
        self.players = {}
        self.diagnostics = {"layer_fallbacks": 0, "entry_fallbacks": 0}
        self._future_sells = {}   # route id -> {item: [remaining planned SELL qty from step t]}

    # ---- state -----------------------------------------------------------------
    def _state(self, player, step):
        st = self.players.get(player)
        if st is None or step == 0 or step <= st["last_step"]:
            st = {"last_step": -1, "route": None, "router_state": {},
                  "pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}
            self.players[player] = st
        st["last_step"] = step
        return st

    def _route_action(self, route, step):
        tape = self.routes[route]
        if 0 <= step < len(tape) and isinstance(tape[step], dict):
            return copy.deepcopy(tape[step])
        return copy.deepcopy(PASS_ACTION)

    def future_sells(self, route, item, step):
        """Planned SELL quantity of ``item`` in route steps >= ``step`` (suffix sums)."""
        table = self._future_sells.get(route)
        if table is None:
            tape = self.routes[route]
            n = len(tape)
            table = {p: [0] * (n + 1) for p in PRODUCTS}
            for t in range(n - 1, -1, -1):
                for p in PRODUCTS:
                    table[p][t] = table[p][t + 1]
                for o in (tape[t].get("market") or []) if isinstance(tape[t], dict) else []:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in table:
                        table[o[1]][t] += max(0, _int(o[2]))
            self._future_sells[route] = table
        col = table.get(item)
        return col[step] if col and 0 <= step < len(col) else 0

    # ---- main entry -----------------------------------------------------------
    def act(self, observation, configuration=None):
        if len(_get(observation, "farms", []) or []) < 2:
            raise ValueError("incomplete observation")  # factory falls back to tape
        step = _step_of(observation)
        player = _int(_get(observation, "player", 0))
        st = self._state(player, step)
        cfg = self.cfg
        view = _View(observation, player, cfg)

        route = self.router(observation, step, st["router_state"])
        if route not in self.routes:
            route = st["route"] if st["route"] in self.routes else next(iter(self.routes))
        st["route"] = route
        action = self._route_action(route, step)
        raw = copy.deepcopy(action)
        try:
            if cfg["hand_align"]:
                self._hand_align(action, view)
            if cfg["weed_repair"]:
                self._weed_repair(action, view, st, route, step)
            if cfg["sell_lead"] or cfg["front_run"]:
                self._apply_suppression(action, st["sell_state"], step)
            projected = self._projected_shed(action, view)
            lead_available = dict(projected)
            next_sup = {"due_step": -1, "suppress": {}, "r36_debts": st["sell_state"].get("r36_debts", {})}
            if cfg["sell_lead"]:
                self._sell_lead(action, view, lead_available, route, step, next_sup)
            if cfg["front_run"] and self.opponent_plan:
                self._front_run(action, view, lead_available, route, step, next_sup)
            st["sell_state"] = next_sup
            if cfg["budget_guard"]:
                self._budget_guard(action, view, route, step)
            if cfg["room_guard"]:
                self._room_guard(action, view, route, step)
            if cfg["clamp_sells"]:
                self._clamp_sells(action, projected)
            if cfg["dead_stock"]:
                self._dead_stock(action, view, projected, route, step)
            if cfg["terminal_liquidation"]:
                self._terminal_liquidation(action, projected, step)
            action["market"] = action["market"][: cfg["max_orders"]]
            return action
        except Exception:
            self.diagnostics["layer_fallbacks"] += 1
            return raw

    # ---- layer: hand_align ----------------------------------------------------
    def _hand_align(self, action, view):
        """Pad with PASS / truncate the tape's hand list to the real number of hands
        (fieldbook_logic.act). Extra hands would be ignored by the engine anyway;
        missing ones just idle, so alignment only tidies the action."""
        expected = max(0, len(view.positions) - 1)
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
        action["hands"] = hands[:expected]

    # ---- layer: weed_repair ---------------------------------------------------
    def _weed_repair(self, action, view, st, route, step):
        """If a PLANT/BUILD_* target tile is a WEED, DIG now and queue the intended
        action for that unit; the queue replays on a later step when the unit still
        stands there and its tape action would be a no-op (the displaced no-op is
        queued behind it, so PLANT -> WATER chains survive). A PLANT is only replayed
        when the unit's next tape action is not a move, so the mandatory same-day
        WATER can follow; otherwise the seed is kept. A no-op turn spent on a weed
        is also converted to DIG (tetsutani weed_dig)."""
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        pending = st["pending"]
        tape = self.routes[route]
        nxt = tape[step + 1] if step + 1 < len(tape) and isinstance(tape[step + 1], dict) else {}
        next_units = [nxt.get("farmer") or ["PASS"]] + list(nxt.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            pos = (int(pos[0]), int(pos[1]))
            tile = _tile_at(view.tiles, pos)
            act = list(units[i])
            queue = pending.get(i)
            if queue and queue[0][0] != pos:
                pending.pop(i, None)
                queue = None
            is_weed = isinstance(tile, dict) and _get(tile, "kind") == "WEED"
            noop = _is_noop(act, tile, view.inv(i), view.seeds, pos, view.board)
            next_op = next_units[i][0] if i < len(next_units) and next_units[i] else "PASS"
            if act and act[0] in ("PLANT", "BUILD_COOP", "BUILD_PASTURE") and is_weed:
                pending.setdefault(i, []).append((pos, act))
                act = ["DIG"]
            elif queue and noop:
                _, replay = queue[0]
                if replay[0] == "PLANT" and next_op in MOVES:
                    pending.pop(i, None)          # WATER could never follow: keep the seed
                else:
                    queue.pop(0)
                    if act and act[0] != "PASS" and act[0] not in MOVES:
                        queue.append((pos, act))
                    act = replay
                    if not queue:
                        pending.pop(i, None)
            elif is_weed and noop:
                act = ["DIG"]
            units[i] = act
        action["farmer"] = units[0]
        action["hands"] = units[1:]

    # ---- projected shed -------------------------------------------------------
    def _projected_shed(self, action, view):
        """Shed contents after this step's unit actions but before the market runs:
        PICKUP removes, DROP/PLACE(non-animal) near the shed adds up to capacity
        (fieldbook _projected_shed / tetsutani projected shed)."""
        cap = self.cfg["shed_capacity"]
        proj = {p: view.shed.get(p, 0) for p in PRODUCTS}
        for k, v in view.shed.items():
            proj.setdefault(k, v)
        total = sum(proj.values())
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            if not _shed_adjacent(view.positions[i], view.board):
                continue
            act = units[i]
            op = act[0] if act else "PASS"
            inv = view.inv(i)
            if op == "PICKUP" and len(act) >= 2 and act[1] in proj:
                qty = min(proj[act[1]], max(0, _int(act[2]) if len(act) >= 3 else 1))
                proj[act[1]] -= qty
                total -= qty
            elif op == "DROP":
                for item, held in inv.items():
                    take = min(max(0, _int(held)), max(0, cap - total))
                    if take > 0:
                        proj[item] = proj.get(item, 0) + take
                        total += take
            elif op == "PLACE" and len(act) >= 2 and act[1] not in ANIMAL_STRUCTURE:
                item = act[1]
                take = min(max(0, _int(act[2]) if len(act) >= 3 else 1),
                           max(0, _int(_get(inv, item, 0))), max(0, cap - total))
                if take > 0:
                    proj[item] = proj.get(item, 0) + take
                    total += take
        return proj

    # ---- layer: sell_lead / front_run suppression ------------------------------
    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold a step early."""
        if sell_state.get("due_step") != step:
            return
        remaining = dict(sell_state.get("suppress", {}))
        kept = []
        for order in action.get("market") or []:
            order = list(order)
            if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
                removed = min(max(0, _int(order[2])), remaining[order[1]])
                order[2] = _int(order[2]) - removed
                remaining[order[1]] -= removed
                # A zero-quantity order keeps later market race slots intact.
            kept.append(order)
        action["market"] = kept

    @staticmethod
    def _add_sell(action, item, qty, max_orders, merge=True):
        market = action.setdefault("market", [])
        if merge:
            for order in market:
                if order and order[0] == "SELL" and order[1] == item:
                    order[2] = _int(order[2]) + qty
                    return True
        if len(market) >= max_orders:
            return False
        market.append(["SELL", item, qty])
        return True

    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """fieldbook _lead_sale: when step % 4 != 0 (no town consumption between the
        two steps) sell the lots the tape plans to SELL next step now, for products
        other than WHEAT/FERTILIZER we already hold, and suppress them next step.
        Skipped at the last step, at shop-unlock boundaries and if a SELL for that
        product is already queued this step."""
        cfg = self.cfg
        nxt = step + 1
        unlock_period = 3 * cfg["turns_per_day"]
        if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
            return
        tape = self.routes[route]
        future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
        planned = {}
        for o in future.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for item in PRODUCTS:
            if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                continue
            qty = min(projected.get(item, 0), planned[item])
            if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    def _front_run(self, action, view, projected, route, step, next_sup):
        """Hook: if ``opponent_plan`` (their expected tape) schedules a SELL of
        MILK/WOOL/STRAWBERRY/MELON next step, sell what we hold of it now (before
        their supply depresses the price) and suppress our own SELL of that quantity
        next step. Bounded by our own remaining planned sales so it never dumps."""
        cfg = self.cfg
        nxt = step + 1
        plan = self.opponent_plan
        if nxt > LAST_ACT_STEP or nxt >= len(plan) or not isinstance(plan[nxt], dict):
            return
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for o in plan[nxt].get("market") or []:
            if not (o and o[0] == "SELL" and len(o) >= 3 and o[1] in FRONT_RUN_ITEMS):
                continue
            item = o[1]
            if item in already or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            own_next = sum(max(0, _int(x[2])) for x in self.routes[route][nxt].get("market", [])
                           if len(x) >= 3 and x[0] == "SELL" and x[1] == item)
            qty = min(projected.get(item, 0), max(0, _int(o[2])), own_next)
            if qty <= 0:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            already.add(item)
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    # ---- layer: budget_guard --------------------------------------------------
    def _block_requirements(self, view, route, start, end):
        """Planned purchase cost and item reserves for tape steps [start, end)
        (six_day_budget_guard.hpp calculate_six_day_requirements)."""
        tape = self.routes[route]
        budget = 0.0
        seed_bal, item_bal = {}, {}
        seed_need, item_need = {}, {}
        hires_by_day = {}
        quadrants = view.quadrants
        for t in range(start, min(end, len(tape))):
            a = tape[t] if isinstance(tape[t], dict) else {}
            for u in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                arg = u[1] if len(u) > 1 else None
                qty = max(1, _int(u[2]) if len(u) > 2 else 1)
                if op == "PLANT" and arg in SEED_PRICE:
                    seed_bal[arg] = seed_bal.get(arg, 0) - 1
                    seed_need[arg] = max(seed_need.get(arg, 0), -seed_bal[arg])
                elif op == "FEED":
                    item_bal["WHEAT"] = item_bal.get("WHEAT", 0) - 1
                    item_need["WHEAT"] = max(item_need.get("WHEAT", 0), -item_bal["WHEAT"])
                elif op == "FERTILIZE":
                    item_bal["FERTILIZER"] = item_bal.get("FERTILIZER", 0) - 1
                    item_need["FERTILIZER"] = max(item_need.get("FERTILIZER", 0), -item_bal["FERTILIZER"])
                elif op == "PLACE" and arg is not None:
                    item_bal[arg] = item_bal.get(arg, 0) - qty
                    item_need[arg] = max(item_need.get(arg, 0), -item_bal[arg])
            for o in a.get("market") or []:
                if not o:
                    continue
                op = o[0]
                item = o[1] if len(o) > 1 else None
                qty = max(1, _int(o[2]) if len(o) > 2 else 1)
                if op == "HIRE":
                    day = (t - start) // self.cfg["turns_per_day"]
                    hires_by_day[day] = hires_by_day.get(day, 0) + 1
                elif op == "BUY_LAND":
                    extra = quadrants - 1
                    if 0 <= extra < len(LAND_PRICES):
                        budget += LAND_PRICES[extra]
                        quadrants += 1
                elif op == "BUY_SEED" and item in SEED_PRICE:
                    budget += SEED_PRICE[item] * qty
                    seed_bal[item] = seed_bal.get(item, 0) + qty
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    budget += view.prices.get(item, 0) * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    budget += ANIMAL_COST[item] * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
        for day, n in hires_by_day.items():
            first = view.hires_today if day == 0 else 0
            for k in range(n):
                budget += _fib(first + k)
        return budget, item_need

    def _budget_guard(self, action, view, route, step):
        """At every block boundary (step % 72 == 0) make sure cash + the value of
        stock the block already plans to sell covers the block's purchases (hires,
        land, seeds, animals, products). A shortfall is covered by extra SELLs of
        unprotected shed stock, highest price first; SELLs are moved in front of
        the buys so the money is there when they execute."""
        cfg = self.cfg
        block = cfg["block_turns"]
        if block <= 0 or step % block != 0:
            return
        budget, item_need = self._block_requirements(view, route, step, step + block)
        market = action.setdefault("market", [])
        existing = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
        cash = view.money
        for item in PRODUCTS:
            planned = max(existing.get(item, 0), self.future_sells(route, item, step)
                          - self.future_sells(route, item, step + block))
            cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
        shortfall = budget - cash
        if shortfall <= 0:
            return
        candidates = []
        for item in PRODUCTS:
            price = view.prices.get(item, 0)
            if price < cfg["min_sell_price"]:
                continue
            protected = max(0, item_need.get(item, 0) - view.in_hands(item))
            avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
            if avail > 0:
                candidates.append((-price, item, avail, price))
        candidates.sort()
        added = False
        for _, item, avail, price in candidates:
            if shortfall <= 0:
                break
            qty = min(avail, -(-int(shortfall) // price))
            if self._add_sell(action, item, qty, cfg["max_orders"]):
                shortfall -= qty * price
                added = True
        if added:
            sells = [o for o in market if o and o[0] == "SELL"]
            others = [o for o in market if not (o and o[0] == "SELL")]
            action["market"] = sells + others

    # ---- layer: room_guard ----------------------------------------------------
    def _room_guard(self, action, view, route, step):
        """tetsutani room_guard: at hour 23 the end-of-day drop pushes every unit's
        inventory into the shed and overflow is destroyed. Estimate the shed after
        this step (stock + carried + harvest/collect - feed/fertilize/place + buys -
        sells) and, if it exceeds capacity-1, add SELLs preferring products with no
        future planned sale, then highest price."""
        cfg = self.cfg
        if step % cfg["turns_per_day"] != cfg["turns_per_day"] - 1:
            return
        cap = cfg["shed_capacity"]
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = sum(max(0, _int(n)) for inv in view.invs for n in inv.values())
        produced = consumed = 0
        for i in range(min(len(units), len(view.positions))):
            tile = _tile_at(view.tiles, view.positions[i])
            a = units[i]
            if not a:
                continue
            op = a[0]
            if op == "HARVEST" and isinstance(tile, dict):
                produced += max(0, _int(_get(tile, "yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and _get(tile, "fertilizer_available"):
                produced += 1
            elif op in ("FEED", "FERTILIZE"):
                consumed += 1
            elif op == "PLACE" and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
                consumed += 1
        market = action.setdefault("market", [])
        planned_sells, planned_buys = {}, 0
        for o in market:
            if not o:
                continue
            if o[0] == "SELL" and len(o) >= 3:
                planned_sells[o[1]] = planned_sells.get(o[1], 0) + max(0, _int(o[2]))
            elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                planned_buys += max(0, _int(o[2]))
        shed_total = sum(view.shed.values())
        fillable = sum(min(view.shed.get(it, 0), n) for it, n in planned_sells.items())
        needed = shed_total + carried + produced - consumed + planned_buys - fillable - (cap - 1)
        if needed <= 0:
            return
        priority = sorted(PRODUCTS, key=lambda it: (self.future_sells(route, it, step + 1) > 0,
                                                   -view.prices.get(it, 0), it))
        for item in priority:
            avail = max(0, view.shed.get(item, 0) - planned_sells.get(item, 0))
            qty = min(needed, avail)
            if qty <= 0 or view.prices.get(item, 0) < 1:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"]):
                continue
            planned_sells[item] = planned_sells.get(item, 0) + qty
            needed -= qty
            if needed <= 0:
                break

    # ---- layer: clamp_sells ---------------------------------------------------
    @staticmethod
    def _clamp_sells(action, projected):
        """Clamp against a sequential stock upper bound, retaining market slots.

        Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg. Their full
        quantity is an upper bound; the engine enforces actual cash/capacity.
        Removing empty orders would change the later lockstep market races.
        """
        avail = dict(projected)
        kept = []
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                have = avail.get(o[1], 0)
                n = min(_int(o[2]), have)
                n = max(0, n)
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    avail[o[1]] = avail.get(o[1], 0) + max(0, _int(o[2]))
        action["market"] = kept

    # ---- layer: dead_stock ----------------------------------------------------
    def _dead_stock(self, action, view, projected, route, step):
        """tetsutani dead_stock: stock beyond everything the rest of the route still
        plans to SELL is dead; sell it now when price > 1 (on day 29 everything not
        already in this step's orders is dead). Highest value lots first."""
        planned = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                planned[o[1]] = planned.get(o[1], 0) + _int(o[2])
        day = step // self.cfg["turns_per_day"]
        extra = []
        for item in PRODUCTS:
            have = projected.get(item, 0) - planned.get(item, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(route, item, step + 1)
            if surplus > 0 and view.prices.get(item, 0) > 1:
                extra.append(["SELL", item, surplus])
        extra.sort(key=lambda o: -view.prices.get(o[1], 0) * o[2])
        action["market"] = (action.get("market") or []) + extra

    # ---- layer: terminal_liquidation -----------------------------------------
    def _terminal_liquidation(self, action, projected, step):
        """fieldbook _terminal_sale: on the final acting step (>= 718) replace the
        market orders with a SELL of the whole projected shed."""
        if step < LAST_ACT_STEP:
            return
        action["market"] = [["SELL", item, qty] for item, qty in projected.items()
                            if qty > 0 and item in PRODUCTS][: self.cfg["max_orders"]]


# --------------------------------------------------------------------------- factory
def make_agent(routes, router=None, opponent_plan=None, **settings):
    """Build a Kaggle ``agent(observation, configuration)`` closure that never raises:
    a failure inside a layer falls back to the raw tape action, and a failure even
    before that falls back to PASS (with hands padded when possible)."""
    chassis = Chassis(routes, router, settings, opponent_plan)

    def agent(observation, configuration=None):
        try:
            return chassis.act(observation, configuration)
        except Exception:
            chassis.diagnostics["entry_fallbacks"] += 1
            try:
                step = _step_of(observation)
                player = _int(_get(observation, "player", 0))
                tape = chassis.routes.get(chassis.players.get(player, {}).get("route"),
                                          next(iter(chassis.routes.values())))
                if 0 <= step < len(tape):
                    return copy.deepcopy(tape[step])
            except Exception:
                pass
            try:
                farms = _get(observation, "farms", []) or []
                hands = _get(farms[_int(_get(observation, "player", 0))], "hands", []) or []
                return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
            except Exception:
                return copy.deepcopy(PASS_ACTION)

    agent.chassis = chassis
    return agent


import base64
import json
import zlib
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c%1CLU9Tipk|g$D_<SGoD<bpit(vUuCbr0GG)Xm9gF#~?jj({Qf-t*p1O0c^y%{Gm&T(@y^T^9?EwlguX622{JfHqyZtni?-~F%u@?Zb;yZ`B*{{6fE<6r*mzx?aJeS7)cpFjQb%Xk0$^4)*_m;dX3|F7TP`1bO@{L8=npa1&bzP<jZ@BZ-HfBM^>|MK;R-@gC#yO;0&`lrvIzWx7r{^ytEPv^tipMLrL<xBV8KmR{3+u!{8>tBBTQ~sm<$H}ivZ-4pIkAM06o%`bLYd-z_<4>R7e&GABfBo*|6yE;jPoF>k`RxzGsDJtTTR-Y=i}&OA|M9m!FJJZcMaybFrnr68KfRsv@Js81_n~w@x%oQwTYvcN$1gwp?b{>2{`NL?=g01g+Wpw@EpmciK7Ie$m|xic;iLF>{`&csU*BJR|4B?~dD30A^^3=Kk9Xmh&!2zz_V=GYfBE_|I3nYE@ezER^UuGo-<G^H?2a1JaU4=xSa6iUueG85_0zAP|1!RMUna8b|KV*U-7h>o{P^a!*w$IKrg%RO-S4hDny>ZanSO=Jn;uV_wXpG_`}*zK;qHsf^?&>=-ly(&n;Z`FUcO-Sdrd@wg>TYjJA!bayx$G$9k)9!^Z5H}na_n~X8RqNdwBXI)*b9KTlf3Z<sTkRh2Ll4!~KdsOV(RoG^PsU1i``r1@b#CDA~|u0P1H83;OtOXF-8VdTK$(pDKMZ`MTl7E?cNy<jlg<b`DT~U>miD83zjA+M%%@!&?4kd`r~7>t~lgIbZVi%a_mJ|N6K8@cA#l{`lp`|78?$>o>s%D+VvH<CE`fmcj5gymyP!vU&8|eNWw_@uYnIH16<2m5zq0<Dq3%V79t^rpZr(DLb;J-Nxu#q;k}lVE#K{CHKjd$JhKm!vy#DsqwCo=6<$5c(f1c@QkcZ?%fmTocz|O{FLp`E>G>v2Wz^x!~bI_b#4E0QHWF!?h<m6`j+A;`iw=@%N%W{xH4l=>1FnNQt2Zgh<%?t7i574xAW=cMF@!;pS_xkK~P#vU?x5{TI;wHcmB!MeAZ;7gO!s<a4#5c`@%nc`pf^k56>X0yq<zR&X={^>#(12W9@y|z(bBRD{bT_k2f%SI~|Z4Q~7=aO>t>%Kp%Kmy#oaj^f3l5+IAchDuV%jD3_IeAwa>GLt*R_S%5fBX^4>P@pnQb3Z}`q3`Iy=gat{gS0%-fTO&dvhj3s4{jdI3QLcT|?;w~cDwyoWzHI;^qoR4^n#Tb@)}m7~`;?^Gi{PCzX_)D{A#Ux!d03Ig#kI|YV1P%pw~bukY4wuURs}48_jpB?dY`xr2L7;|Ktp`2U4rIj9hrj3$PcJig5GyS)Nq#}boPIW2@Yrxt&EP*B6{AiM1Iqr`3rk|1e2gnPjCbOVyr*6!-8N|*yDRs{)+s5dvDs}f<PqswH<07SZ&4+?J?sru1eXgo1QZ3oYTc3JRb!)Q9I~&HnVnFSL^MyPz(u?#Wl`@H~XxsA&gcu*2MbeHmmdP%#Da%^B&9zfFL{Us<Luf*BqE4+^YIugEm?sS=eNcfr8XHjhMNi7~*`aJ4$0}d&L9*1IQ@>6M6aA^V97lin7w9<OunA2a^*5_*qW`GYN1Be#pRioZu__K6l`C6uvME0#nAXdt&v;@BHwWuYayuCcp)l@V7h0C<j8Hi<9sDd3kMY3(Wa)uswtEcj_hqB`pN*!1o~P%|MsVenQwbK(w^4gY!uQ&j&$<PlfK*562~X-bl?DPnK#Ui;S?5r!Br!4#kz&1@G6~Vohg#Oqw63<nC{j_b<Qx<<npP@cA!)`A^_%BhNtn-g6TJ=!6Ks6?kG1?%d4Yv*qK6S5=Y&#&yB#g;pPSKR58Vdt9+m+!?t)WyM>;#(xON0wQ7H5bQHs7__|;vCK}WFXNVj`DAn(f|ENqcFBC6Bk=7CYKz>uQns9B`8fG7$WmbHJ>@bdR?Ikr$G*d`i6l=CBV5&_LAx$pvGt2nm<ZT!iCV1P#O=*U?IHY@KGgAUMhgK<J^oG2^I^Vz{rc^HvtficG<x{}9>69y3L6BYb5919dp&FF={MnVpD#&IeSEs;c086onTj%b)-OoH28RBBb`Bv<0Rle2a3Ew5wk3`U18m30X9uH<K03&;1-|&{V-?o}AxI#pocLsB9UWbD0Y*8*S91E^_N};%g&gQG1|XgsmdDF5dgI8g!BEF#i30`NVdUl;hDuC5l|KwF9t~5-bW@!r0|!rUpb~y)PX~EtIs-2jnS=R++=fgRGX@9zQy=AQnv#=R)o64(asYs1OmDs5v?seXUNw>}MbBBXQ;d#7uHwd)thsD75tzE1FBms4NKvm^B1L-vMV5eWEZnz~yOT({czZ{~j(@Mc!<R015!t09u<=Lui2DLnnN#+19keQP(1a9dL&KK!)<C&i>PBE6>HE<(jqVh)opkKq*IX#%NY<@{NJq?gBSAiMEo=L88oa~i>LWQgSRm>X%z>kJYuqUbTkrM2qH&o!#LUmyeM{Y;ydY1<ia&8giG>K(!xi;Tu5IF)2`VC6lSf2sa9kc<R?4$O!?E@V=nruV!QC*@H+}pYxWs~(+QyNulQbo%9z{P2GEgE_I#c3R``=k3dZX_08l{1y+2X>Et6nr>b9bisC~pVny%tc+b3YTy_HhOMc%Yqt6>LZ}f;3@sSe(7*OAjhf0!yPTyAmT2v)FfCbAooJA)eeKI9u?ZMeWnTI*MPi^?s_50>i_=TU-+t9Ai)_&~u=I=E*Csm|IYGq^y&%Kfo4O@jU?WWZaFX^1*NyNFhWnNd)z`#Wh(Jz&2f8xCn+*LN_a<T6c#mTqr7=3k>I`(SG{z%YS?i86lWBJOnR00Beh5TbKC$Lq`xFGH~UXfRhzHCDbH^ttxxeN<?77N(06=F*e30;dXFah^euHI}wjGaCQK*fvSOBs~1IUbhc#WsI7N|j09>Bm<eSLBN|ZC0LwrHez_iDc@9skx;nJ%#E5j<N^vZbiTYRq5PU-MC}pGWskZf0RW&FCs2{>G1#L2eMFHng%2?)!4CRcszT}?O^b)C<#lUl53n;12+yti(uwNm{PQzRubhCl*W67qq(9uRZx9ZQvStSe-uK#vP%)y!{jVno8Ms5a7TMq6yh)KEdupxVBI1Ii=>IsAi)x1=2+~NyxKOR5Z#iPP0Lot4lX;3K3$#!)>f?kkgKU@+P3-I|DlwPRZT~;N4ez+ziK^hgvF~_Mu=wP6F-(E7#q#>M`#U%6Lw=ci~mh-beI!3yWPz%Cfnjaev;*y{f+_(G#=YeJWf}O@Hzb{74jIs2LToDfTYN;~E*{a;&<^%zoX#Lv*K?tW@ld?qJ3YfyIqC=|C^61%p<cgB8bM$ePR}>MUq5yS96I!)ocH=6|h{f~l^0E3oG7H(K%8>)Qx8%wCmFqIau-Jx9P5m-vd%S<e&7h@3AO%GVIB-=xZY;_TauEcvAxDMWBbUnhom3wZkl2G2?yMw6mzkk(ln_=_FZ)8p34Suz-jz8#eH@jxD3`r@0*yew5WRljUp?NEDi^E@miJ8OS6I>YQ{vH3rTB=8qqA}RG=N%H8yX}j;0_XGfRQwpgaG{Y{@!s@E{m+1;bTUUrddipRb2%g*2A-Eab^oiyTME6%A(Hv+`jY<FD^#>Vz`Xu_%riV$EWs(p+7d>ykF<%SAxYVtU^?>zvCaje*NXMOrbM^hItZX;T4Rpd+C+Dh$3i<`S+O-kUb<xw?JTY2S9RV)2K?vYcLFtaL93PF$=+R{UJk+BvrQt`ewlmq%pE*u|Us475l;r7-R+p33?R`zTMT*tRZp;A4C)w0O!<%D2@sTdn1q`T3{{B`Q~nknOU*@0KQltF`6U9VJJx!T^KN3AoKzHC6HKU<rB0Hhj~i)l&IRU7})L)g9cZW&)k#q+}UGuKRQ)-0H_w>pzWw>SRYVPQe<}DQ4YJ~5b_f1;BK_YN!euo$WUvuk#p^sX2DEi3_Xg(1G#t4JN^FaSZhey@Ua-#vVMkUpW1#37n>Io8HUc!Y0e0LEDtJ-k;rD+8#+0>B0-t$s;FL-lM*1mDjZN<VPNOQBWdB0DIoF;+}oxN;GQvhJV9AL@;2gu16eG{-jr29oFuLLP+!e^Ly9T{ZT*mX#4E=%9T1GBEkf@rR|eWx<UgW~q81e>=^JpjY>gO*V<))hnFKLy4;Dbr@3lw)9bSCEJ~+*b3-o~P)Q1-(VhH<z(u-Qws05CJgcs)83p7ZN??-KS#sWg`!@&on9t}ZPK&^ILaQ&qPK9cN){>t(4Ewpqih|=WLRA3WUtEScS2DWH^Viv|2G*8zsim{#1o2RWH%Ja^0!U(w{BtA_Ex6ws>=rt)JhmuQA?o_#tCzwPeqN?C5qv53|&`EcU2<D?OX_T|E81L2#;wOfWw>$f}L&)#YzIutBXF+L<z~M#5)-DC*A2QZ(%m+LvU#B}|l|brqn?!otb7DwN-qu2^6maFkcbgRyl805=S0UTuLqwjN&+QY9-OR7(#UK**;3d?sdrAQZ4v5OS%Bj=)DJ;?45p}c>UZgHZ6zRzQN+hJZPv*Q(iWa3^`FDl{vI>_(pC?${*+U!^^r%x0pDD&5j#R{|cgwLLw18P{^)dc^&Qv%lZkW-aeg%uf2u<ew028T&^yW@ZA7jtN@x@I8;yQ{Xgm##XMfcGXxu|#ln(qNal0uz7vvpK-BWR85d=7?Oey%(PI}ae9y-ynGjG{7ssKgg|RucSwfn{{9J52X<C0@`%Fmup@m83f!HDV>#Y3bog$24$dqkV`89W=4GvJ8=}pcum-%H%)EG)WSFS<?zC{(zU0Kx;xFJ;Boy0B8zM4at9rfAR^c@H_)|gQjgo?n|2ET07VFp_0Zc(3^t=QC%c?n3yoYy;ocdn-tPcOWJ_6DHiB5g1&pyq9wZw1!($ZX(EEM+Tw1zC(&-}$>qt%nVV|Bz~N>_a$5eY<ahvLUlbx>WZqI03f|cJ>J`D?o4iy$Zy@05)m%$$gWX5Ym5d;(TsfLF=Vj+o6M}M#^E0m??m)$g16m)b-S``EjDY^Ri>GZLITj8w{SoPx0$zqn_wa8-9+cM!Jz-oR#snIP`P79EV<YTgD(v?ek&E{pN&7u2BZ8iMG2Wcti<jt8yd?2yi2H4c1~GKFv(J!~LBp!ZjN`wcH)()erOD+{_xNTq+T0(mS&ftsEK&}#IPy-rl_e=4rk)V9l9LqMu%QNL!J0xj3(Dqk`?Mvb5pbi7(q1kFnuE{mcs*a!8`;Xy-&@HH@x<Aq8bwSkW14U$Sj>S&@X68SEFnO|v*Tv<q9s~o)aj0__Azj<cO_OAL;U;}(0D=C+`2qQFR%?{;f^!7_d0tuz0H+#i3O#r!s9(=%A}u32s){gaE~3l7{m)3fH>JI;8DwJq@t#TU9gxFSg(Chnl3q8cFV;UmSRgU4%o+NW6_}H<#+NWF1eNL(AQt(l@vef*yk_MB7yLZUvb}Sw(w*Svl66a*5mIPuau`4h}|@cbZGP<owidax1@{x-cBv4&j0qOoZudqD$x0Zhmp-6h>^$Rq(DgXpJ_znEcGS26(ZZ51&k}sP82N<E;CX{5hP-OjixOdeS(QNAw?ge4<Y>kX|yt?NGvx4AU2Z1GsIiNnF0<I(n62QepZ_15-pBfSjh7svk1Fu*Q;RZBdp>ph!X5HXJMvDbUwfsM(4WjJrRBH@Pi6e^<hFEdpi_&-n&pA;*c`Kl10mq3^X0?S{Mawj$cOJViE2DLeRzl`hv+fwyMe*y)C&8U02Jy3t*v&wK9FMLp7^5-I=`v0ck9;;$r|ZWVpUOY`ADhifyI)%g!EpwB&hFm{O$vxa1%Hk@9r`F;WKXQz9&ytHB~AvR1((u%{6IkRi?<yN^SkL}~*6w1j|2eTqW*AMB<U57%J2y(GSyaCo=mMfm-n|M<rb?nAees7nZd8HKPv88k~aP4LE^?PW8OO=$~mPJ^4q)C<pL4)y%J7^PMCh1NK93lwoWCm19Tk{iMIlC4CTt>mQ9aJd{sw2eSYTJW0~$CD(GK4AjcU7%yN3k->npe7k6DOV?DYOV4GkK9A$#tf53Yeiw=G2E|EI+3L~X7yq|#vDb&jl3*XZ{SrrOBC#gc*&^I1b)J2eE0XDbd>wGpglnM<S_Ui@JB(VH1wMJ0|_~kocp?kO%5$dIRn!Ho5YZw%}gt6?E9y{$Md@Ck#x_R3rLVQDWPrenw3|?sI<T>{Wdi*_CPS~J@I(IKFSY2{t?_CtGLe&yM$h5=J?A>YQ*h%!eZI%&vtn@nTn!H5m5g7g~$6z0PY{#i@oF(&Z{Z|572s|TfP%)r-C=x@7OcQPHX@M8Wc_23I(^f$3K*Z<-RgI2G{|7AX#(N;2vlGJ>%xQDB2SgV&|j7o3gwtWJg1v`xP!hJ49xyJjyL)Dvo)*a0wp1hJyl>^rMwSoCta_8j=XMgUbe&)1=keVZg!w3#1<q6aZ=l@_)1k?GG6mYOI0+FybOk5_7Fre?`h~&FFLpe^I5|trHcy#O~~f5_H$4#RM=AV=cibETw#hi%ctFF(2_InJKhM$_WUbF6TjGXYB>0K|m5Z@B>Du;yohQCEi?i&OX3GC1fLNlUhON_?<ib052piPJl0Jz%e5(^gUK_yzK5!D?|wetz#C;TD^Q@K3~KXDCLk;5z(2ycuM{0VV~)1eI$Jo5(*g@cm+~%Nihx;xQw~Qu_Ig3f)QwkwLEj0&H%V*+koCOD~Hs_DInu9*#6+0ev09Hw&;9;vkX&8g6{c%qm9Q%3JT-1S_h1SFcmP0*fZsTB9dS$eA{j>5QAa`NY=W1jD{RC;Y`{wxA3-KFpUUU&^)Tb*GSPlI}ig-#fR}T<cIbUJp`smx9sJ2hF?J55~_#B0EL*;5NH-Up&=pBzk^U&y8QP2O(`ymuHv-RqIQp{((NUl2SlVq@?y0W<1IB3^rub$JvTTO&44nFJr`*UA6tzJX@tl(rx?Z#XKu7s0)vX;e?Z0Ui8A{Ew0%%e^emk;%q)Du(&#-y*YWb9@5_=eErp(AVI@dqPp&}}3lLK=fI&ZEay+~}Z<M3swK7>hn9(;22WLl>HEF}t;20?CDz~rXR9Hs}3q~gHDEiH6w2e~aBM!PM2A1(u%tRL;S*vS_0C^yT`6idj`zE(?U%dm?RGwm0^q3G)`VoUpEd;D7GcP1YBCHzU#`uJJKud;zvmK)j6<Vf<iBKn-TE(?sL!}TN!J|^BgBGQa7BafG`*dH@Z?l3E#QsYuC=5*zl(Xq4`GXaG)8`N&FlzdBuL$GJD%#Ku%4uP$>ifl2j7it^V6Uu{2XG9N>k<DbNigjr50pL(Z_F1d5H<dx5JtR2z)SA~49R78vljdob!N!pZYw`a7a?SO8iyryC&1P4=3bKI6q-fcIT{#2dTCFl0!<VF)+7UGflsD~B<T8(`>5<k^l_O2sE7JgAe#C!W=Xdf1b~;QDm+}60#U_6QY0m|7z3p>w|r-Z#Xh-RSF<k#?W3^a;JD;(m3<4DvYjGhFVdxh+!ay@Z6`&U2E`ddRj}y2yqXf)$+*@OSO;)}6lt7~wUf(2ucTbkB+Z@y_&ds3ihIb*!23`$PRIM$G7orU?DVrR)@m82s=YfQZ*T8PU1Dqq=B6@O*G<_dMQ|wUBP_4z9VU5g3KmR!dx*BVsHr@~2n-z#+FtrbaH~+<QNmQn;DcPlG+qhUrZTBm$-M6k{CNM4&Kuo=d87@Ka<V+tNFa`}36!iO5r@NeW_AG`bPOHUl=Ey}5LRTvCWo*;<s`<f|G;A|Oyc?3b5W$oq&U0y8G2=K?aEXVY4>mM)BT3UoeCmk^bP)@XpHQ+U@#>h#=zqY#IIV*pKJ%eS=Fp4NKyiXCoDy?%_#R_)pvr01b2DnG1(`eW2_n=s>FvjESfM+W)j7<wbT5ekr0-DM*@+ugUz@f^J<>X8j2f1n|VRg-GDZBx=|zs!cwDUb&PaQJBw#9o{04AfEufXdfD37E|LDRf~8ClW01Jzq-(Jpz0Bm;Wj&D;H?K;fxOEv1fqJSrJdy5^RnEp~2O{JWc+c$_M=AoFNDHL6LlQJBt>ELzm=~2B7fJaF5ZhyHF_15rU#y*#f(w8$!5#{v=?q!#VHCY^!}Y;ijYT~rgAk8ia}TzcIJlRmej$`>Wi6r@ZM3gXPzxRb6N+P&(daAm@L&sw8A7PMv^<3p2HVe*Vi!6dDW@?cOZI!JnnMmCfzsLB2acVoT!bN<N0MwJ`B{;U0U7zB=)1vNkK0Ol7UsICs_y#61P9FV?%(mb-_^UPE%u;0Ij4VtjR%JW|IL!t%XzT+n2*GgC(4HMWR!RXV4V?@u7Qxvq;3iDIa3$h=>7<&Yg9&s3}GW_8`=9{N@?~>DafJN#4u(n*`t7+sfL!=xJgwk5q{x}QRcqCU?W|m)dDe^m5?5w;?zaN(%yHkcY68pgz)$hCB*CcpC4n(3-*nyMMeqhROf2^(Tb8+-FfI9v*>>ba1c~z;-f|I4*HW%H^xb^1sethzVn_oul7X?@Cl83mLj0!Ai$XD$Fw&Ah9fyMJah{%K~f>BZhND(#=;>UU|MXgk}&qdy@*|@{~3ivmTJf&$Qcw<_QA+$;Pt6#+KpG_uw(+E6DhZN3-jtmI0-sq`jU>h0h)k$WEw#_7-k^H`fg9}lOM3yT|EspEx$wRyIEI~rixK_7-hcZH_%&sqbLLq0~rx5h9Bo8U5SI9RuO&i1i7EwQs-n~T^ZNVqQ~v^4=9+j3x)nD1m>+c0>@yw+>F>=<l{=IN^q6;?MN8~Q}<?0S0G=IV=dRhjF`_rP*Ze9DPB<VW1^cNQoHjy8rw0`qLId^R2vYI7AxeV@(XeXPt{Z^C3?%zc#bQL{?^NK>`h9C3(guCXt_l$kNa!XM?nVG{<sRcRw()y7(hjh4$cHkM(<C;l&SB%x3Y5IGEdm!lZW>-N7UgA?7<m0yMR?6(D9r--FN^DmWUoAOg$1wsqw7Kvp@+VySPPKw%9!!*xkh#a45Eqbog2aPe~rXg1^_`Tm|#F%m+pR2@E>|sb?D$$}ltfBR@#Qhufo+B&9m<;8v0I+=1V9L*pUeSLBx=C#0k+R!~dC@niH8-W!+g#c;Y%$nrxg*NCK#3<P9A5xKCTK&MuzZe0+!kqZDQc;E!w;<hEv7UiinS0F?2vrnz+JRfo=pvG0P5mo~k84)=Ji-1b8LF^qcL3Kqk8%Xf25`mCaD<Ol8MQE#KMFt!7<#%ShP@=4nyOOh9DEr@}WW+2yzyxYSM-y6>o<F6!33iWLEMVOZKfrU7XaiLd)I1|xSn>@FO(bm>`Iyq;NNP~*GRERF=npluw2x%XaEMZ-Ffr5sd9@tlr|bHJE|K=)p6ac52@#jLNE?RB)|cT7u_iE;J>e(L-I9!m)FVjD6Njsw3q_h>rA~T|!^yiG)GKqm;vr`hJXyWG4?{mnH^VP&!$aJr$ym++;x5BJv{Jzj4&y1FTX01QGXhIdNZQR}(FM@eD5)VzeLg%mJQx(k&KLvIBn^e-DaD-SeF9SBQ^~8q8iELh)Go4t72uW;N<Lghw?`LUT~2o+i@GO#Y}LA^7Ad7W%e8LKb0%Y+OooW2F$i!H>A}jU?{wK^sV<ajoA(^V^h3rZ1?-OZl@2W_c>M;F8e<nQ_gI=x>Epucsd(1&q31{wdTTX=_Y~wPS#{cfdJhZ!U3;>qf}`NC@FNJE(5L+!CAjgKHSwKc4%#GP;jN(jIQ7Fp(CP3P^$q0Xu%a2*lw%*=k)2bjn9e(NC>tPM<;UMXhz~*{Lcml4giuPX*;%VXN9_SgNEuK(<%Hzt^k)ECP#(I6Pbo7^1qo`n2xVVORIFF(Pp!C^FIOzp^SurRnQZZtx2Fmms1Ii=$2)2?h*Nvv`^VPdr)BoQ4E7k*G*g4Q>t#{H5+E2eM6Eu}_aE)#nm74aiOAC+fVwDaB91d{=^U|xxT@qh@_6#l*=`GZq>OemUO5(T@op(rrg@k(dUD`!JVo~l>(5$FmP5VeG@8skt@*?`^M5-OuRR1Fr;9b+c~S_2dikd@LMSa6u7oN?Kk#aVHfS)jAPEhpu#lIV%f`_IHpLCCgH8jGj5*+RqLZ~TMM_4K5$*r@ikW*(W!%bK+8o-Yqq&jkU@VS}p^%)*<ger~FGu37;AROQQKSp!HTkyZp^vsVFTXSKg0NV435+3I1r)u>*a@jCpZVOPrtWp~P9LRvydMjZG}&T8CxD>B^M63u&airZ!IslqY;}}g{74TN5Yfcam9ttR5qyYMPI3L&G}C$K2=U@?92lI^3G6fjhS`-E$?C^v1N94UxQ2UocZ#;`2E50IK+v^y7f{)}%k?K!WS<6oNIQiObtnNrreE3dUt{bfz92Odml3*bWsad(*)q9@D_+#l9_HP!^r<Mkoa&UNFo}tHIu3K~hqFQx(J3o*qLySK%GyM!48SUv<B4)~mpEp8H}K^zNDe~j%cD43_4GVUOkt&d>mx0%cA}8cy_vwbZ~e<xBuCoqTpo~|0p4Ft9b4#5Yv3duz3|t14&E)>iIhdl^iN3*Iu$ST;#5g80zP0C*U4nxJcr)lHHKUlxYti8LKNOge8Kn@WwKWet2Y6nA2DC6zps0$=@0kyBVbl>6RCFL(FLpt^4y}x{!f4t=b9@0jWCfCHU;)`eCtCLCtdd9D}sP*oqL=&QLN#bAq3m^PkY|~doWT?<2K}2%FxXPf-&T{-*bMD6B#$en{&JO7;rK8r=S2dMPPui&3mb!;w@hAe_u)mWGpb!ABRn|C8?!yux^NjI!{>#VKx?3%K?kcq0e?MU->%vsET7lO2Xs_fF!!KNMqlRUFA0oGuhgp%cqoE=mj=d283)!=bz3}smiwPp6e!^FY)(gzZCFH0tqqdcY2&-IB4fwLX3H1qWGNf-|vbN3R`z<m@|?Wcc>4NhBe6zU@cJg+3aIQp1tcDp}$yk1n4xOapX})rn@;Ix(7vwE;zW`^H0rWWYY)eeB89-p_XAR@Njg7L{y)R5qJG_a{ZX6gS(u>=i*`0>v?_R%$TSsySZQ%eDpivE_u9B_e3TV;el3xpE?dI)8*n@qi{E34jk1)9VV-{K9c$bmv=9gDMF#ZG!>Uh*{H<Z+&b2q(h6XfhR6UzbIU6S0h|1-_V`D}D}Hy_C2mLpy9~q;=`3e0UC!+Nk7T-}I1#?DIkW;98vUEYL6e#=ln1%+DYn~@fhl-Nt@Z#Rj=)d}M3#<8HgK&z8e^esk-nMrR{9|>Ag8kUxxjRJ?HCuJ4ImxH$^+?g1&pIoDi;6-G^&ykCdHkYJdR5oBx4wMXOPG=Mj%DU@v-<1c$l8zN5_up1HZ(>o*1%FI1hIPYkY?+fnX=&)Z%O^LI-j#Jv3cWlRJWf0NaeTYc^Il76dDX>A^r?pxNfMi()4Gb{`4VAn144hjtQuZj6T`!B<)70uJdg8t7o@#Vm%ZBLOEOZXV+qsH2_83C9ojkVjS=S@=Muj;JND338`sMh<m2**xl(G8z=h9amY4%ub@%YN7NqU7$ksFA8-4bk#k;$_n9L3sCQjegft}4=YI0W(&emBNJ6X(#%~<o{Hsr+v@MMPt8BS<Y`Tg8OP+8ldr@+55&rz^rjC*DCF&v*#9<puVY4ReC;<Eb1$ppW0P}U66_+%SKwtsr%*cM$r*49hO$aiDTC()d-S*ddT4B88QYwFVWABM@6rQFBK!F$Jak17n|do6#zDmaoa~deV7=jUv8JMr$afm^SIp0yRW2f65Z_7M%;4JZuS|f9!T39F4Hu~9YtB3%NbY6RmRegPi)KS$X043_FNK`o`&UZFj&NM8dXC_uM(7FAd65-|NMVFg&1j~AAG<HH1zt6eT>+lTi0~z-sc;7Y^(Km3T;eG<G#)qMci@_p^5x<ME8R~k6DCyd3>PmH&X8@Wye2k#lo%<8!LHE8zV-;+)b;v+P(ICztH0W((m4O55LrNcL;hC{6cFl(nSVvS!2%-ZY%S%b@m@Y4F^r&XvRr^bqX4DFR9ZSp69=>MfuAg-;_R~#xzzi}7(bb`1F?j%kI^yuw?1;~AMzr->HCwh18df1w^Hsb20Lh_mJr=__&0L@USF?qVP3aOvkK$GA&~9BX8V}F0-mt?wi?8AC-iOHVgLF!*&IiIcUF9mKtTR`H<cj)<J60vy~idc-S2S7DX#b#EH{8TQrrYpi770_ScE7}73SzNK3!bGy0nDW0%51HG7AAr*hK=g$O+u`|HE%Te)-{V-+x`yR2(xJSR?>SMM&1k3(R(d^DVO{cz?_F&;^R9!UjfL<_V;7R9hYbLE@PN;Cx1kRr<I6q*<QBOSMqJoFeHbN#!{+>{;pq8BRTN3g}IMGe}ve(hnDC63tblv|__d?m)8JuG4{R&gfmXUwSOlFmri?W0bCv8Ap@?(-*b!Gc52)!N(V<FG@9v=%E}8w-xM)b{mg{QgS^8z6(W@xlrM-oo$%12Gw}C{BApfH&5hWeIAUxka0dX1xk*mWIrP@HWxr2G!=g47^RbD#SmYZ6tS)k9~jVVT?qy?Y+ZC-EnQll0R;%*Vd?<O`?2bO)tyHn)An~dUjP~C5QX>IA=enFz?_Hl{H1xkUFGfb=4){)@63ngH^GGhvsC5rLjJ->-nKN}wmq1aVPgXWeVeAU`CzgJ<@?veM_aV)eNkRtowCdDRy~l-kmw#?tPjJldh!wy0O@h2c9pzc=s8`P*53sfipV2^_;Z9vKEs`dE#4C`Q`YyVp7K-6PUVFhyvi!Mr=>9<10#kWOEtE@Ag(>6Hy$BkECLSu57M~m`%C^}nco2Ps2rLAORyCV?watjyt49@2)|jHP(`A7__}t`XkZF%6f<DbhxQ*dy|dPFN_Sc3={v@fZ5nc`3Vd{^NJJLW^C;|0cQ~aKU-|%i<740$Hn5;MLsfQe^ouhWN9E{#GR!X88DobX6&csR0BcVo4Dkgxn(KiCt=bq>ililrEZyuLE(7rSYuNKZ_-)R+TqjNs))ck|rA2+<T8L}}wiYxUIQjxZg6a;(w0C5F{rc0VU%!Tjw`c$L)>*ipzkL0fxC&vN2N?5?WC<Un<R8<>B`P1r)_3$apZENY6&@Gvzk?-4*+Ktfee?Ad#OWy3r4}BeGi^WwKOjqPL>>NnTXNtG!~&B5=d3UAfH3|4Zl(K><o&}aTb`*i@D(Xg&49rE1><Ep>;DgsIs0}X@B75$K_6Zk7rlS?xi!yDJ(_GE>iqU~|M$QAxBu-w|LeDT{rh*vw=X>uN*DDQTl?xW__?)&CVKpB9RGCXKTOvKf*0TZ@Opq(DN6{;48cw%lYJP$#J3U5lm$4YOKae?Z(o0NSyzN-<Id%HIuwv<I_~4?C~SP3R7tAiJbtMC#ECBbsr$K@OwWHS`Yi81Ic$eWK#WwT;n%}~KAw-tvMjI)YDf8az9`6T6@Gb|f1J|gC|qA~2?4kwr*T=PahX(6ylSa*BTYC?dp-$y2LLGq&*wQGQC2TWC#<&dnvgQ;k#@%C>vL)Cik?q)^FEM68_27w8k6kLJ<VF=Z;RFJ!c3oj{_&?z?~3^AUmw@y_4EPKvigEt-`BGpE}|4$C*5842v~-6Dap(3=&+=I@W(W}h~3fGNoXmaQ-wh}u(-Ur=Q5UAj0J#}AoZ#D1>WPwW}7o+?yo(&f_XQGOY+N~K7ao6rp*@)(ypiWDzrmPgh6b}w!rrv-!4ST)F!lzzV_xa&|AUWu#?ecHP$#WMutx|X`REXvM#{Ql9YFVLL&l~q?Uer>U21$5rSZ11o&Ba83o{zRigs;bm$Em(%6IrvjPq0vD4$zmcn00cM`4xt)CW$ms0iJl~m(BmvlwJ3?_9cxinBCz6gaYcw+$S1qNXClAjKfLh@Kj;AW!31C;jeUG7<27#yXfB>bFOURkoMxGP)K2QCw#<L0=()IFy*zM9_&f00}VLT;~J2xYNH07hhQ;y<G(CU<erq8<;*(IJ&ehy6!9OL0;%qx5t<s{5M)Wd4Os@Q2e;X${6Q2diMwY7)5RbUZ5%iJy~h+fv=i2|w@SxVYnRdXYvW&=|o~$57BKT3e<D7oCn*A<dttu141=boYyrV01>-77ElEIZYT(Ug8fkR_^gBlViXA0R0l!&v3NIu={rZx>Lr_nBux@YSX+e$$S(rRs>WDEgN+75XDc27h32q!&c}UDV@Nn^72!ls5wYlejnsnt!)(MI!b~ERjO~6iJ^H?-dW_2p(;_5bzj27-cG@{efeSi$9nt!`1R{ApN-r9lA1QL8%whpXCC=EiDilJu+p?e1bP_qA<n<xm|d@<P>gmBk4Pn^5Wpi-$1MMrQpdu<z_{&ll_KuIx`80$8iL@dFgp)^6N2PFk0WtR66ydjp#G7){x-a$R1ril)kK^mCLG$B&dQEW>$hU70}#5PTISJ&+?+a}3dk2SUSo`Lby}^qA3@B$up@a^#vix|sXa5K=0>&_ZT&0_)@!=*R4pt*;ym?7NtQQ=7mfn<C?meV%_LTKZezSiVAra9nY3rYu0(v4Id$7&QJp3|PgemODAGMp7P>-|T-zo}rdKI_sm~>C-TH@=u7{W4KAZVK&6Z0V!L;b!S7EAE(iGoEdlW|_I*QTH=Apz@5vd?pY@M2v?aD>ULQyzhYjII3?rAKS=4WdS-)`tt+WpZK@*63sDib7fb06Md#&J`;Sj}DPA^v6-0OS#2c)4Dyr>*Jg+iU5x!J@<n$DkF&jB2^Vl_jG1*e=dM_!CuBX&I;Ba)9Z8n%W?gV_cwDiRn6(oV+3uF9?EAqy?f4d&BxwVX|I#6Op$H`4no2s4jnD*6gc_|L|g|rE**hHm5Oa=zEO>QE|7SeZ=;Oa?=7AdJ7+1#5}T${qP<5LcNM(xGlt$8onT<F|lviXL`<eQs1%t5l?ivU6+HR%@TA4O^}s}rQcA=^^At+qtxYnRwo-agtqXw(4nC{x1f=aOiZ8f?Wx?j44j4Sk?CEpWY|#?Mwz0x13;xQ@4hlS#g4<$#C6MJjn%m0s7T)X&}5_;RiuqR0wTNs({0<Ow>yyGSEQ)R8uY}p+mLXKiox8M<E)f2h@M6Hi$YZh;xf7#qvy6Tj}9^(z+_(xYxgqHzauh5>qbZeHbF>O^-6|~Y^m3m%XPP*9vKQq9k2_qDsvF9$p|$gsy=G#=rT8zaFOJ0rU--?83T|Bu}JwHi`#KY;=+S06}(}7+$2f__;;h^lmb86Q!$^6o646-Ca7d46vWc)f-N8bHm;&+oMhoWZ~7-8UEH<`Tcajxs}dd2K1p&=mFr^5a{z2Lv=YmdRVW1==L~<vG7Gq=F_7gR@*_Ia%T#K(+ZO8Bo@BrRAl9|wdNa92wB<0fNdqG;Osy;1)FJJXU6hNaWwOd$_cDH%C3o)SR9<|924}FThbzf!?YUXmFgtt2*=6pN)bhTFwZ^?JLk?HsAVI@_d*MJLrJ55&kYqvjOi$dF`COHM&I&2*i34R((dZIgl@9>ekfSE_F?j$C^Int$^cbQcqI5sYF@bh`w3}Fyr^HNHMtZGC+5QXzax53aF??S_El`~Ja+5f;@D%6tFPBt|!qnt?C}q*D3grzRbEa%|1nw@kQ7}V!wh>nyhRD4ZdU!pWB#Xai&|?#Aw^39Zese!RZRf$z60rIFhFwjDjLENrB1KcH^EMvcTL>%BUPxQ&A?=h7mWNIpL^O9aK%~rD_2$LDD&_{S87Y$=!-#2FEw^Yu<_UFyuFI>WeZVYaEb<vmD-E8A-hsBy|305-2rYp5052@N(rV{`odyhr5^RzB<kJ8KL#=FBiG{`;3`a|!V#0Y#Q3Drk8tIH~=W`h5vye>|9pXC6-PLQGTMhN3ImVBm{@|~N8+OYsXiQP?wb2b9)QGJtnqV5r<U~(4&URmnnTb*y3s%@@3Y3ikwe9n15_5$PI@7{!t0ZVomO+!CI3hTm=G~xu++5jQjD%`A^5|fs%Y<Z+fD)3D`vp*V<XkJ0nwM0ly>o_bOMf~~ySG)|N=h#;(dB@vy$oMjX4nTw92Qol)Jt!^k7_6dr4}_F_M$x^j6}5j4!RYqSHCW&=E7?N!9zgoa=#N-YD5m-&Ww<pg|kdf6&L~u6aX<whl-L@GZaln0otHtijQbspgivaS<lJX47IzS3fD~+ojL?8bT)XJ;=~t21(45ScIP$?!^DS(uSNLuC@WE%#jtR9k*Oq89+b`O1o}VYzUes9G)XV95+|x<o$iS+flX0Ts>)T#%ooSd(He!dII_$YEVJAFpJpZgNTYdUD{1B<;3^{I_>6YZK-%phTVNpTL$s<IFOkNbAAnL$(@n)_+~tNys`MUcB*&~tGiFN*<Dq%FlOe&el?F5q#5WMY<f+~?L3kRnr37zZ32(JgV*XMlrryAiMg<pt9bEIO;TRsJ)|RIVs97+#J#^N=7@CPXEBl+!!tLGj-4bxiYBZf?R!XHw8<g%Tv;YOX{**Xuh|nwx4qJ40yO<)6w=(+lGTuVDfCwWJY5?}`q>Ek$tuiUSo;2w$kXyj%Y6FGZ;;ZW14d%}prH`#p&@?;7NDfcNs0cWbNHv24P~qV6$xUr?H`j@&gR3zaROB5IP$W6`%Oqs5E)PF#hbJSFeYS8SNl2B77=noJ^L|@B;52kq;Jvi$^0O|96#zc6LPrZ}UA3nvjA7BaP<8}#w=OpiuP3DtIL836s2px7(IiRbrs*pA5hyjM{U2Xn^JrN2A`*CdT;eKA@EPl7qcDWtk^HsLT5i3%ngwFhbZc~L@8B<^9I8L%ZCj+5zdf+1U}lmt&q@XM>s-W3LUMgZ9b1yn+rIS*6V+Ow#qvRRRahsVVRssIWBy1F)ab02=_&((U`{H6^spZ}M?0<Fp~Q!A2$~AI$&yRF^n<2)0;|vf)g%WqUelY@rV$iDB6>(~vojW0KEF$^oo=UsosB$dY?viUVsh;ZNf_9WYZBwO(|^a(o2nmCOMy!P-&a~^=6mpfhu!bo_%B=l^aXhpJ7%-I)!@mSkw2s0yR>2e@H5B@`Q<ilbenD04n+5246tI5*Frx5B;4=kE>o9XjA{c+5>tTZYIa-6q^`fY(hLD&TBJ&-p+_B3mi6oK3suz!K@Dpojyv=MF<E)R;^U_fdGPmXI|YmogA_)nVTzOzBnskC5t6kTWjgm|rbj4zmXAvc0(#}&Hd#N&*>^S5Mot(TfpOouuNHI5b{8D)=<S1(lE#2!doZU8OtOS852%2l6-ge5FZ-PQ_2#|2YSV;*ue)*SxP`i74mxq%etD1@1vRZXJFkX?qpE}<n*b~#II<NeyRZsF-uE(7+w8&Yv|diZ>t-?F!AEyksH>Eb7L5q*p;ss_h_C6uwbuMQ&@DTh&9qB%oAa$Kvy}aY0KF3C3JwT(s}Q9F^KTBZ&OuUatdDtR1~g(^9>vtyJMU60MS<r7End4>7|CKuifI;FaNgUGw}GiTwY-FNe;Roy0tl1l)UpilJc(Jdy4YYf_%S%OWm5Ev7}+Q{>&=T-sh*|zI^_t+97@2YO#opG3h?K6@F80mlS~6<SVT?dq3s=MEC>{5A;&N}n{n;}7M%~ZERIBZJnCGEb}D=mcYvkB8&SoLmPMGg<(G&e*2Auti?I*+$q0yur!gN?(o0I{y>zoJUrM&KruqjM$vm|E1L0){9EDBN_(kJ;C6DNO@SMb41y_i_H@mbDfw5s@1pu^tIw}&z&bb9<&Bnm=lP`)iveNuVLv3m+Vh~O_;hH9AFeHRC#P;lNf#gB1VVc38jGnuWy^pxIaWizqGAW~}2`WPp)ptz772MH}hT-BQo24@JZKOL_3<m@#XnQreF9rNZqX$I;2t=%LJ{mBO8!bc!R4}PFI+Q!Wu|!%XSvZaHwat5Wb$?`GGR$XyZpY{1=^ty3e#p6A%S0@by{dz4#(tPk0<#6PtiZP;A=eO7Hy;4eTt*6yXhJ8ypxmTeuV*O@23#<i5**(GO0}|UyfP!wm?xYU$wNP=Ay!q&g7%_j31fW}Pm*CH@Yha~M8`@98pFe)jbIlX24BE)o1?;Kz`)!hPDtN*SSowm&x>$CoprBuHL-s*?iwL=0HDvO-U1rgn{uHxl}UHM5RF&+c-As(+R!QC^&@M=Dn`=38O{mXg#Ey2#xc#-CHsPolR6JYXc&_*`c5o|H(knfA$Q=a@Z?_Y8O3Jvkq9DC;gsSc=kYA6+C1iyr1P+J8NX&cG7C^MR&*VV_7>~*scMpxg<7hn1LgtLtJ`;C8UOhpKyL2E=WHd-V&sGE>SE02T0tFPSw_$^A=cVV#T|(DG8x?_h-ym-r|oq1)9yS55V{fAs{_BxR@xW{b2e@U&WY!A;6W+q^sV`96m3Rwg&>*0W{$o(c*p?A8cHx!^{SH6z`!8G#ZI(Cw9?wC3ax^=0_^iyCiHT8T~MSuJb*mg)fWwZi(pv6SExsh#KKC&9=&53y+kn-(_ckq1jo+3G$n`l{Hj1GFKhwgyx3>9PhN#y*w5)A>wO3YHO+ITD2AA-iC;uUU^6g>+Iy^XO(|i9Z66KKWMvlSp@<%^y*ymVsNp6uhrmoeB4Tk`k6W#*FZXrx0B5GA(2T<|TSlt#Zz+=M^@J6u*WTFWG6B`hP*Wh$xln%xVN5T@d>yy+?3t8xa>v={fn-yu=JQ1oRX-Xg(?Pl%M+>R9W5fkt;q?Y{hN_JkJ@aB2i4j?VfDLn7#}CZun*?8C_IaSOXUW=kL-!iqnYsn>z&Fql17QG@qICdB3^9fX2$1Gcp|2`2qu_)>O3o$|<${St1)iS8Z-XkxqwBJnoy1l-<#}AHQ9R*p`QWfwX=#ypC}Rmw%Ub?0FIuLPq3OqSO}}>;){Rwm2ODB%C*p!slyC%3EbZz*CZbxpvFgX5Voa?6N@^$Z8@CK_7FM^Q?gGl4aV$l4QC@s^9-9E}qxSMt7<nyX6~v@--n2fg4$LY5RIN}1=7yaQGRv%Dn4{X7okT8yiV9HHpHp8fUil?ZcEtDK@e$jTm{n*XUQOCn%CB9|EOllhtSrH00<wj#pF~BAQE)GnZNM^6nOIASlh8=v=@@CUt$#WUVkL-5qEx#WabZL?;v%^^YN*Fa5+{MMw+q55ml;JUv#jQMF0@h$@nY=8^H{05%**Jc^9}@Fl6o6XGIbd&xsau09uLjEon;hWSOsy|wA2V$XRx}O9Owc%eoV7ebq$PJ*VKvvGAMCM@}ot3i4O0xcMqUP`1`x}dC0nxj>LDj9)Fa(TD95i?0NtxeJJV~{zg9e0n<5A-*Hw9ux;Y$?*UZ}#V9Sdk^`cou+_9VU~+j+Tc~JN@4P5$;BD{i;owoEa)CY6$z)4A7WrhAx~NRa>2@<-ZD;bL^4NTJ8r~CmsUoVek~dJiBYIFm=(<_8c>PuO>tJCv47~l}w;#X!@VD>3E=jC$pV5TA&s(K?+a$Kn>7*?oWiAB@%rW$6Y3>^@KNS*&*vM|ROa!GdOAy70OnDq3v`97xk-Zi>HUVqauTmYUtm)shc1;D+ePXwe+^~UpZix-#B={wkPoYFNxwGC3`JEkVjM5me@Mc&sQe?@}qhO!On~D<1lHrmKLD<zKdLR9Sp=2ntub(+v8(`u66h9I|;D*7K?mokg&qaWLl_CR?7|1j9eNn#*RyC`|Lqum6V3WX{%4)h35^xNU#s+$qw)hf>5Q&|Nj2g}Iv<D<u?duM25@R;V)Qjhx(d5AJ3R#GPed~9NEP^`ANF}_WPAf_rB^D<bc(%!}vf4KL)?~Ngx-;gfts|E~`#KNa1`xS(K?7>Xg5@n$p@cM`ZM<Z`7*KV8l4TL(1sJCRkkd}2y~WiAYI1<^uuV<ZFHLXNKhT#~o^zKSnRWe9MH+z{bstTpO%A>}uSv`cjxE+sA}`j5;aAzVpE)1JDMxwOIUFUQ;l|Teb+ewJ9>WP(zt^F79*w3kNlcf;(t|-LTn|RQ7)ifm1LS&QRBQ$W+ZI(8hsi8hY6A-6l2z*fi+fgMESFtY@iJh%<Ux_^L6+*JQBL8h0V^!Et-#nEoKd<f*k%U43tZt<ENTYEsh!Jx_I~*wfKPgak!||&^&rEH=~YEWN4Ctn_FuN_6`@6U!{N@;f`n9|tOr4skk#i@5x%JL$|9@eXtePkje_}Rbb?|{!g?nw&LQDzc!xv61N3`6DhI@z{2)W{!mJND5~tN)dW@YGoTZagz#N?<^OWgZJMjPaDW2P~d&Rme8jQ8YF5{YWB<4X3`X&Unn*&Ji#_3bO44W9Sh@-{7ryUEO`&^xS>m*H9LwP_7=2>SOmnL4l!E@`xk$qm*_%)~|HnnNZVp?`r)W>eJ(BfDjEv|=+GaDyZ^)Doc6MEed7Q;$$*z1z&=&hrn2pYMBsH<Wqjshn`j-M<Ea6F`S{1c+e=FRnhcJKcB^`}q2ejVQ(NHE)T@cGNvpT{@v71|H6O6hVszD?=$Hk$)o-bkK&xZiC?AaU%t7P~`_zi;gEq;xy1RWssO{Qw(Ku>8b`3J$gt{_L|aauDJuyU+mq*<qTT(l-eTvkYmdXD$*6I%tX|fPp_o7IK&y7@x{q<?$|T;)2EH-Bp*d%wjCS9spd89>Sf8#<ZNtMGURg?ZS<F`-S$$Pe1?o)2DZ7@~6+A|GcS*m(?g+W_}g6UM!V?;;e0r??1j>ixjvvsYOkw3_VkJC63wkOCBaboEYa4!F^iiAj4STa>)n)bGkX-B3y*iK?bv!LCmaXnRozJjmq59K~;WWA=_x=t+{mTPILHllWzbbY^Q^&_CTw&#Nh#JxwevOytSGQTCS0$2BHK>12y7{(76n)eSwy{>5j5Xej1Qf3QNZ%u+2n=2LKpVz1*|7FbM?$oKLV~JVll-*;U+?hxMK;QyeRe;+jdkr#8M@>27dxQoIg?jZ(W1ui`>*rwObb{xbp%dCxbrs7D#MBX!n>{YMU>I4PN3dK!>PRR4*w8@vmf6d5@kmDXUGG*|^70!cPTA8a`t6<JT5lbE!MbSoR#G7gn2A2yx!`iw@PF@i~0$#k<vEoYwzX8xRq-2q1>+LE-hIsl_#&o=I#Q=9EPU_Qj%0A2<QGbuyf(vas<!Td!hIP!m2&Gkfg_hoD{y&1?JmPzi#vJ%^D2$tN3cveS}-;VO#(Mh1^HnN#|kLTYVJ7OTxx_nn*pRte%1c_Lvf_84~7UAtLjGuEK{YBLeh@m=;KT~Em%iHL;ev+wUtisCnZo{&{_^8H5qp+D|4O8Z~g0p~zA}q>Y@wbCG75cOCSDF{R*PA)dv}tNr_bCr~encYxiVxqGC7o3#)u`p7eCD_;YvvLL%kMO&;3LI8*0hLZA`tR@=qqGrz*_C+Ze;*ql2*jmmerC}aK5VeMSs5m>MQeUsQH!T@>{p!>IWhse#dG>fmuekY#S1A>eHUqC7+a#j)U~;q9-kdvgCxgsyEuWV*sC>7*4<8Tq*N6Gl-jqJrX+vi8U@MKzO(9>8nC@ARV5QGW|T0l!qF2_o8tVly}d_EYT_p($&fCmpis)euUO5n`|meS1r7W%h}J-%e%`Uo+X#^dH)sk+}6I;F7x~$C;QeGNZ}Dc8PQ~;oOGX>_sN>L=)vV|<S{eqe{{<@fyB7PiJg48D3!+Scj`&Hl)26rbD3Mq;8lG@N&%O{N}LkrC9s5<t{vm$QY%H6V98{2m<R>rpW%c-A9XA`h(#T0HL=WD=>mAP!u?1}&4<coEa@~Jrl|k{^(O<Od~T)z5Ygd?nkd#~sA$V#P{PMt)n;BkaWe%_DD_^|ag*N(E!Jh&KC*>_jk-7}pswU_F}%Lr<YLE!xots>7_?3G9NeB^-QzpJB9ejQhXrde_4<g#Wh!O0@K=?>`7X=>4wf>KMPD}{;GwA?iU;I6VTDQld9a);cwiB$(?OBF9F7~9+tj_80|iwh`(aFLyr(k`r=zMj3?pCR=1^6x&YfEib{TO^%~wfANN@yMe9O*gEa>Cc$Gc@l!F}FCKqc<ft{f&yLy1}w8G!<-)aj&ZdhnVmq=dY06{l8Sg(c83i<W84yRFZ-akAPFi5zo_B;yfGC&|#4>6LbT-KxF7aJaVSlAu`9Jg_b88Ll7un#8T$AdxX`qK<QSUNUOPabKddk+^4i?Xt#_izKG$R4(K_4LvG*u=gxa0PxYg*i{fn@g5DKTe#pN-!XIq$!-+O@gkR~YhF5yZSnHsL8~N#Kg!+|*&1GCbOr+cS&t=^P78=XV}pv}+odk=B2v8`m-rAZ;U38Q;a6D)i}4G!U)Ba)tRu*HF){suqF&s9S_}RysW#IT3Ik@<(}5McgO&4wa1x-5L-lxcl-e9B=|ZVKc)CLHG)XA42z^T(Lo~5I3#?$v-azteTMEVAj&}^03IOWKD>nFQv5E3Ya=8)KL=?0rE6+Y^<S|XMxr&0ZVKuJ@#ILMqqyhx9e-P%gQ88y75A1Cd3=q4615H}1c$iJdOHxE8!weZ|HoU<mLsH9bnw5Oo*KWwF6shy7l0}wPcEC^6*PF&^iY$$3mINzMU=L{i!dO%H(e$k%S`*)IK9cOBz%Oi}G%%;UB?13wB+10(M}2ET{~G0$n<jcQQmzULX34EN^ocB{!~=DcW(iE{n*-bTqr2TuprJ&#PMI8#W57NLOO=x};CBybCVr&13T!|8COdYp64NOI)sDFUe=c61q24sq(a1U34hhJkBxdT39gNb~3m_cZk9Pdm=x@arH61pTF(y71Z8HRtU37q;R-uL+=w(s@cE1(K#RMJ4=a)BaO}w3atgoT7Y~QC04!T@y&e^0e9UcztcVKAdHq~nC_UPFy)pi*O`2t-y7S!FAiJ4yQyMaNSw6h!!i{zQi?xh|JvGP@>2?gA~#`gtu<pd_%DF$GghyJQ?OdIb3s*0K7#5f20Iljd%M)T`m_sSrXJ7B#EDr-K_l!g*urDE5-lhr|GEAZ?gYDx}t1ZayspRmy+pwTsb8@`_p%4Ls{0d9Z-X_zx&Rb?NRP(2SEi=7o5Vy!c2fgv^LT9k>NdV#{KRj)r7;JF&U`un3j*4Ff+?JtDQhi2CzmiKubWz}V%;-blu2Cw$1wXqfK(WrFKIFFIs0q%%k(LH^HhMaP`)WsT(f%>{pR$MWF4`{Y-Ykzz+xNoT)mg+gY4*+0FQs?J^59LHdnYM?+1<%E!rRyGqHs9goU)7-j=bq-apu#0_GS(zIt4>X%(D_B9anw3uf7DyDz(Dg!;v&M9uAFYL1Il40AnLuvCfJOuvD7+eWr`qiq3W3d`*|#$L2PUDphhWhl8Ea+#Na+%DCDZm?DxHWzH{t}<`+tSd~R$*6tjPGI4a~$I;7Zk)?K@MJ?yfuKgp5;L0A;?(V1qO%sg;dWHo=5<P{+*;Rd8tMZm};NKQv43}lBoPA^$+t;duPie#54w=9bwl}+bk$!|in4T)8rWN4Y*m2H#{1U{M?1ml)=GIh-w<^(A)q2|pFNtSjh2U1zYE{H}aJJ7&lTt+Kvd2j?c2!|cI-QuFHl|HadvK}YZM2f^V4UxkAQ5HSB5AUK%e=3HeB2_SXNja+lOMMBxetc({l*Efa)Ebg^9mJ^Ti<0HEL`g*#drDjtSI`#Rmdnsgl9%4(5v7znqh=YEXj(Q;HJuZAkSxf;8zOR!xY3ZU0S=QytBk-FFx>*Zi-cK4cz?|9N+W&qB%6t0MqD0v#3Cpf06g)R1eoSYV_5NL-OAW7^jg#XYwlKURtAnGseFo;-i8(u9kP$I>bA?cdlTUP3(5JRHY9=~C<&j%%fUE@yd)A&MI=I$uVd9u<2*$Gx7$}&f?4qDQnGv`7)J{;PZcYHjN|ctRhJsXAfkTYZBb}oK$RXIZN=Hhh%&r51^cY@yULC4cb=D|8u0Xii5%{88xPMC#Z7crek&<gG#HNSNTnhsH4@lW-8dg!<Q|->@@Xm{g`5mke?_k`&t2_fOfQLvKO0W1!e!8g@$3g){DalKnCD6Ofh?lrt~+ZVLt^0frEMPgEIn|VS{LnPXhj2ws}?dFuSyRV>`YReNvLa!gVmJ`nP<CI*OT0B^X#~Fzmf|YYon~YB8fpPbSLw;DO;|ht2Xv35<nS2{}v{G$-W|$VFS6JB(+3rjpf_Nn)R$tMhIZZ!|?hVdzQYwZULHA6+N1%UuE3Uhq}-!ovMSHAjq)kc2?bmNPEZgRXF?ch5W?`-OS!&)8>|#ccJO$tOdm}*7iH0B|y==WkqCB>2*G1`beBHqzOm)kb_`zO%$R4bXNyrzSg@-+BG+9k~$3Q)MD?kN8$;r!?B6Bn{53-b(RyVB8+IWs{x#Dn@YQ}PKrh*dw?ZJNsIuD3tQ(6`aB{N8*Jv57)PAD&ATRTvM=9%sk;~vG@z4MsKxWEY$3t2^SG%FZ3<L|Ns`8x%ufu0s5lyD_EojHhIT8g5F48Yu44k5N^4`e5dZ++YmN9SH6q%-#EE{Na_j1PNYp==t9e38TON9ycePFCp=qbU+DHTCSfwaF48Q6b4FDH{*hk%-fIG3C2F`J0yK*@L8{^3r%b-*U7kTWt^(LR;((y7bYjj19cuo~IQM#{7%jttrT|k-XsUMwwBJEowd7SIGOLZ+Z{%DOZH4B^$V)VjX50dR=s|+q@!AFNq;CrSqw`sf<6rWiAc)y%mNv>XZj-oq%YhBn?u0Eqe#1~-cV-NOnnX=Abi+htOt&7`e-cd%efxQ1h7>;yqo2h*Jn)BN?^u8w}i~ixaAHV$Yw{L^^^|yo$2W^q>zy1}W-?8KS9LIiKE{AOB(ft@6*$}>VMl^vDwK$2b57|)0j?m7a5H>OP<o)UMm#;ss9(b?2$8F?;ZV=i18<TfvZ=9!RvFNQE^ygX=ND!ae43IWdOb7*W%s_B7Z(p)f0R$Iy;jlIP$Hdn0s9LK%PG^1yLN&y~0WJ)AIlxDmLF#OId?>3X6~=svLmmqg42yhHZJ#jrjPQ#$wD|i^TvRx%oJ(r3=0a5OI0THNLgYE}j69%t%Ui2t6doX~+CaNy+)pwjRZNEQW*7fr8Hnr>k)hewLE~E0-3dkS)6YNt^y$l@M%SY}7I>fz>F?S8u8qg<N(N&3HTI`WqF#nn>w+Mv^igIji*KiQ^i@^N=aGJl60r(Wd0D~ZfN#XH0Lvak+d&ICnOiR7|3|>i-3FMtOLA9viqN~B+Fsm{X2q;V+h{Ou79tIJ5Ht^zsXPvqI(U0Jn*l0w3FE|ARi<Q<);Y-1<KSk=$PsWy&9(*M7Mu=+=Fsuiz!k|{erwgJz&#yQf<%nX1NVMwO{V?ZMfCsxXPpkJ%RNmLiNgb&>)J}H@t#Y%LJKvr)IgMo3aW6#s=BTSCwRVa^^%_svYsyEd~7B<JV2v--sPUfg;DKU>54J-xLPt*74iX0CCfxOC6G7iL2{=yzFX;TaHeLw4oH+MdM3OOvd3o#v<W^A{_}k|D$G%|sDr}~93A2;5BtA~u8!b9c2Y8<^mLR2iM0EOe_@kKBB!I$8jNNKRso1WCnT^8Mm0&bd$%y%%0{+~L-isJn~vDp!9TFpW*NaGtYi-5MHaAkCaC!{6l$^36y0P)x<;YaS(F5$GqU1n)EPO&HVk)P>W*Q}Sh>fiOajLC1N2K^b+^$T!|vOH7iKkqr?@VChQ?{g&>$?eXeok7PsqejNy5VmE%cXREA)+UW7!MiQ=t3+uAX}u(lA)}Dra!)=~_}@CWdAiaEgIdlu0G&B_&Mk?G$|5mmk)DthfJ<U%&qH*|_~Lsc92g?9FBzav?Y#K;q3Y?csR@8u4>>J7yzK71=dtsxgOYFoggfnL1|qx9G!^W;LE}yIiG+JFwa~$hd|ecq+`!2bp#gQz;#jggO8WsP7V2&PS;th+wLTIAWr7IVR_$>Lr|)Gr(2{V2wky%%cgpIdwi2kS}Ds#<Ci#(;D;UO{#x>B+ttDW3>}_uO*$W&=<m$2J1Cld8!r`A#t9JQk*=UoC5Z!#-Bqt-BL!+lT4NH^2d`xO4yZ%k20q&R%uxW@7KXmejaSC<hJL*ame#jsAJ7vxgD(KhfFSRe+llhnQ8g!H-Z<Z)CL+@ccY$e;kLe5MynVOq#kb!4#7}j&pV;&?j_tlI04q0<vy)zEiOvMJ&om3^1jya?S@{Z-5*UMzu1|oBSIoK_u<`WWyir3FBUhFdWgT71pv+7KV5ER^|UozJv0NUMB#y!0y#<O<QWwthAT@%@v&W;*Ggkxs=lJjfw~OF$~7RAV_cwDiRqR~Fv?m%q#k%VwWT+#Ulk_HYZjZiaJ(%`MJsM{7IJI$RmFdJYJDj=k-_GES(4^^z1AW_&^}`OM7e3(s2FbRYt|6Rasak=#&DrjR=_szFg1Ju*FUju*=PFRJxQK$`y-y{a=R`EMUN!t3Ys9R1>n_~F_IwCB(S;7O4m(gMtvmJc4;Enr>KuiOrP-Wsob~>oQ3U?0VMo5?5GK&Oi|ncpwgIkUzwd^$6;yWx@9p}Kkj(aL-nE~&8WZutJ4_4iQaI>H$VJ}6m?q(5F#-{I?7A$b)l-@_vJV%r3|8HQU0P(mC^UweQpc$=pf?(O!mdFb}s|{J0erG{EakV6NH3i@iS~>OTE4f#c3;sdSoadb-*sbs?1UQorF*`qUxizjxKXk2^UH3W{N<Vkud<75Q~)GvA7+VBrZJ2Qo$SM$4#O{fPXhiPATxCJr#?0a8vm*6xBt#JTamCvI{!s4_DDNPO|WxH~o{4E^ZO7tx=Pe4UCRxEEcg*mAsl&Z*B%#4Xwm7Wfe+6$2r4avCIN)Y7At#hx~}n^fHwi?v{0`b-F16%fjyvJkX~!NPTe%`noW+ZhKjWv`cnTE}E9fDtFz>_+ggZ&_EF)TuQBH{PAGeZTc<VCpaq`W@klayINEvH-XyC8uz-)V*)62kf7ney>Jm-mUANYz<210C6WJfRsK1vFt8^Mlto3OOLSE}0ANFon$XAO0WdtiWoV&g<VL|(mh~a*_-Hp--ADSxSw?!TNZI}j19B`E!!dkcLM>37_@axi2~TlO{{p*UowM_^Ba{NO=+nwH505!hHah}$m)j_qp*-7&s}4itUJE_E9!-+P-!tg3iME@{)d%;jpP#n#+@=&<#UL3nCchGj6iuy$jdo%j31KDL3u#NO3w*hu69*B^9SsmE^H#li@v{6CFC64HQlvpy>~pxHG8WuhPn4v6z$|1e@)=Dl4W5Wf)V9xmFBLPk8;|n=URZXe)y@Gs4Hya~*dq1GC#zGnwi4yJWJ#rze8F(0O~r!zqD>>6(QRc^X)u$aHO#jqNS55yYnxjQ^`tq*kD&hGuZJ6U%Pwe4QSi0VSo|c#Ru)Y#4dqaxC(9dO_%UWCN^vY$VWTNfHVV|X&qM#!I9KSPGc6qZPb&vE1;-usJeEE~Q`HJ+Z<ljsVO&Hb$Q>fh@R&}rNI(fm$^8N-JaVp;NzIEL03ZG3d`o{iPrJ8O-bzX@FVW?ItGx_gS!UP=NgS5=g5T8yqnIwWj(ohERizTR3ZesHNbUGhp1&@q=Azn(gF|4oA5$)4YD5m-&Ww<pg|kdf6&L~u6aX<whl-L@GZaln0otHtiVxJR@;*Lzu0C1M$=D3FyPgWyO&6Uy1T1tmc$(r=Xm$z)eGaobw`mwAK5oM15I#N1N)%@?ESz=ui+5akP&Ts@=>LrSrsGJ{B)!B+oT!#{x+lT}HbqIPDpw^lUmQb6Ym`TwZjs@dnJZXkxBEXd%tZZT^G-s>R?^Hzz*R)Z@fq!+fwbF2w!lEvhiFwbULwtJR=3`+n~Kr6%MFoK={?X$j#-mt%$63$L-TYeLxN)~4QL*SZy<olQ@v?|@HAvg3EsXE-fE-7{H07xy@A;%$samG!!bNctu0R#P_tled+4l#F*Fl(R`xfch1<L5yCvY3)o41)tdvTVHYnXwXaNd%{V8$S5TT({CyRqHIMObr$m6YyKD~^$P%a?Ch=dxT`|3g$y$)K5o)MF7@JVg~r>hMVYKyO`b2pejYm`2=LP68)7$Z468KWZLL?YD;4nT#2%O^Lr$%O*)nG;h7S7S1$$U7pSNOJC%NyuPb9)8*mPevp|m3kyeNR^7LQRw#lDeP6O*4+T7tLiMmwfK{rWC7qKD|EDwmhSqgjA7BfCR55(9iZXo=HXQ~1?L<Cz@l=vr9_h?m7Auk<VT>?oV6W1yuRkqu<k`9@btLERhHm0*3Cv?2)!fut8@O>LKw@GGz-M0>DK7h-oal+sk)ScI;V-3zdf+1U}lmt&q@XM>s-W3LUMgZ9b1yn+rIS*6V+Ow#qvRRRahsVVRssIWBy1F)ab02=_&((U`{H6^spZ}M?0<Fp~Q!A2$~AI$&yRF^n<2)0;|vf)g%WqUelY@rV$iDB6>(~vojW0KEF$^ot%cc2*$@JPH>s^+82^Aup!qZ#%-tnj-@wMKcbcbmjb@8w9d@;-~kW2-?{N$xB%!2@+x-BW_hc@lQ$!OM!|P!#Q@-EkQegHZQSTK+pZmm?!_2j#UQVRega6i-_Kp9F1r}j2ACwK0MFIzwvtI*e{-c70>rdPl~6;EI;1S?*Wnkcsu6-3)<zt6=mlc3@`A<3Pa*Q)@6&b)7$F8Jj8MZADJ4i0#GxW2YftNR?#oP%Q1~n#mlOovd{*5ySwG0xcQw;SP8b`3ao@VH7IVvX7aZ^C?Sqq&#(-pdFsBMkvV<=WsDPmrNgjwV`<(ps=DoaX(}aSryK(8bg}P%7I&s{7d5{_fHLW>2uZD%As)Qk%04yRnvK1)1unI%o_cBx4?7{4`UQWU5W-;KwM|W7LtCW!zjR@|cS12xsuj#<G*8IB|afm3kXeB=l)y*84rR+BZ=#?;6a6rIYg(w}Ee{+a+4w7PHeatH}pb_KpD5l2Vd6#M_3OpZZ@!HM8NES;{Ota8}^L?ntHZa+VmzJ>ZPa`iy0AbRcT9yHxCoxM_7aObwKL)3^Op2ZnBOB#ry?OB})w48TryK#9LkYOF2_TF?0sb5hK4c4Hl4-yUi>T>5w7nyZ1%cu$<QPV0GtOPWqVu7a#gQnFN1aR2PK9sc4zN^sBdWO3vIw)b{1Q>bde{|nG4>%p837UTH0Fa!dPxbrmu|M@OUZWDRQ~`YnTNK2AiV5=qp(RDzi51~<PlvDo|BlX;0p2gW|tNsFg9$g0D!hnM@7QeIk&*9*%+99@<owGR+|54s7-A}48kcVT+`$XhJ<j2*q+@jkUYpWOf&eC(R0_a_Yv1NZicQ{CS^1=L1jpy`i@Dsf;;-rFkGBuvs8w@jdbUV;eY@IZLcQxrGWov^q^<}frvHEM+4?@qlM^z3MSP?hjIrvmPpGa3#T!@wt3I4?vE@?hWQN8?f6_g{bSA14>{LsnTTbwS9P$>*bfs*V76eE75H`}<Qih?<^v#_%Sho7P3Ytol$&(x^(>{qfD0y5g5z62saAH4S7t;S^MvyvdFTf<#HvbJ&|cImVXTkhNiu8%{@O{B=vWCsV|ZA!5$uA);0t(eb5!^Y7?@kc3F$izOJ$Gyc@Yk%v+lL7CiaiUT_dCp0QC9PTR<awQ!dn|GU@IYqVZ}U&sv5}8#*Pteq^m!#Yp-$!#P2lupc<hIHuXUWM9y6Qs<!v4P!D!--+e$rc0SF<PKaFp4_WFqu6Xd5<vtioKjrmJf1~Wo5y^TbRL#2<JXKwW&vu(imrpv-eTQ8RZWtzP)pTxz&wC@b^A^%<3Aq+$j!a@oUNo;jC`<NU5xo$E2sl3%LsZV#9EuFxC7B%CZpQ~QEe&Vw4Kg=+MUM$LN@|?b>NrTN*e=V&c@BaIq{qhJSYX7zBQkXqRmLI5F``W%+Xf|4;cViLkWheUR6>W7#L)@*ok(CR$4n%p;b^<fPFs8gkDas3yO4y2aspG`l7*a5ezH%3iZg5SXimpqjxN$mneo}`m4x{;MlpBrsNQxUlj=Dg)Kmw7yHci$*a%{`#D`?y$`{lrg_d3#Sl|9@r%d^YzF2~dyjRlDJ9IX?W5tDtjxkZ6ww2=mxl`(HQYqz5SYnFL@ZA0ajTW}<-Tqn;LOw%nsGR0%ScuJEk#njp0EP-+8euECZL)bY6>Je7wYdIjOnGAuj7`UJ(IFd?l}8AkZdZ|e7;Dc>PN$5I!Kq}Xd(4>jJV({{C<PKec|QpyAB1Atw#ddW`kcouF(?o`1?{HPpTaa?x-<%#~9jLeqy*cCbN+d^iV4|!kM`bV<_wt)6h9d+hD7w7m`J=5N&(g((yPyc^P2PAUsHrf<qgKY`B;)F0cJ^dA+p~xb$u5KK=aTPoLff`2E+vu5#`;CeaMzv*Fi0R9*l89c8)<<ur=rsxniTA=SFqbw?-OIg0E?Fo^E(GCrkZISPqGVPJ828Hi;pvlt7l`xt5!Z_13D`JF6ivxeb<WM4Znub1SPKYjlE=S}2}HorX%Ng~T6Y5F`c8`lNC|M+$xQWZ-Y5cMi{8R$@TDqe^^g+660GEQu~#)h_D=OF82fSV<46#&_pE#$&2I2~kx3xEheN<79Zl2snER*eeW(?R*Cta@66v)2-I>rUI~E#PgO4$3E`SW+Awh|JVhQjNFRFh&YBveZD7AZegRd=Uy4Sa?2by;mpxB|jYsH6J4`v6<-b0P6v0Uha7pphE*^i13~vPx+Fm_N<S5ie#Ap8I5Hk*dga-e7DlwfWJtt0}|zm3kWZSve;wX8}Bnr0N9YG-giUe5m<b;MIAWsz|kSmpke<}aWHXGGNbf#lpQZ))R<EMEuPNu<4S9wZ;i3LxY6U)WwEbyhg5@DaZb8zOLZ$7*)k4U%5U6sR*`@uo24U|gq3V|Xr(y{Cg#*``#|Z9(%gVeUcys%zk#k%$Tp3VV01>-#C+<EoML;7yD#<m%h#XZT^*R26`q2{J-dRL;REzbV16wx5Z~Ol``4YaoZ2a_%bK8ZUy`8^dxWtfsVU}htuFxG)oK%~4YVGFK1uWqWYCAvf)~c8vPxO;Ru5Iu!P-V)PF}F5Yy6Q+3=QSP8RZMy0LpfG0xo+y1>g4NhxH%p?f>J~ufKdYZvRVa+QjH&vl)lN;~Wo&%M#yVF|Z;6jo9zI9ka2XDza<50{DX|1n|hzG0VS2AEvY#^69qARf@O+?J1M<JWOGBKIoQMfgk0VB-8<5Kz&E7Iv=HqAcCnT;v~KN(8hFDc5J*+v^XUQ2(#Ali8#y6sq?9Td?DjCvKm&W)hs_bh`ASbB+ttD12-YHXZqGvq<8`>MIsH>Yr67OEi6LfJQ<0nhzf%O7ht;()1bf2npJzAE)v)!1;8Lr;RPauTe%z`<%GsWlb$D^Drb`y-2OH?4tbsmC5@hp`tO0(NTyqV3GTC*X+felUMA1Ap(T2bS7EC8FP71&Dn%q&JqCwhDA7)ojP=#ecmlFj@A+Dbi&Ak<W4XNAfYk8qhF+!JA59^j+paprlE}?{csH7SHJIW~c-vI?d1O5643M44tXZ^C08FA9=b><IB?=F;6zBzlPF|%03M(RTPa10%$0<h3i1#3L%!mVhF#X*B(doO~F3_vQbV~_Did@aAU*K32(T2TY{i-lok2%Q-N)3O83}ss@Iz5NauPXk-+Y43Nk5bsYoYZoDtwn~QeZ=;Oa?`d^G2A`P%wfy>c)w&9>Qx-WhoqGq+3*q!RBQ5?zCQBI&f%O)bh%xZgQ7<gbOlY2b!npCkfZ~ehUdx+T4trw<d{((7CO{=;1+aVq6tnXe0wT4E}@j-<H+=`S2FCV30We7vXd<DzA`(-j>FQ#b<5UR01-b?EiFTnk><g^nt;K9RZrf?NCOi_x^b34zb(KYQ{*1W_sC7UoRv}r(X%LjQK-sjBkn%8g?V(4@c<_KVpzMEf&LwlDcYjINFIU+339X;g9lNsFGC(e#ZZq71*8tx1z43iszk_Bxj=7;%w=vW;UdZ1Oc4k(G6o<MVv+JY7PsS)#Dxc0DtN>ExJi@<@b5;+DFwdMjewiVm+2^Vd169AEFFRXI_M8q(KJr7@SZpQlaMZMBT|y^L>$pruU_Y4t1_6NSIidwyi6*Tf{t^oy(4f_V<5{t<j1rc`(>)(Zdu<ir}{pyEd1Vdl}2vM%#0$6E=*m?D|8|4l3kRGre(6qUH3A6m?bxqu!jhjQtKIiJQ#MHnpO7+&dP=<70%VW74&K(H$4!r0`7I0$D%sWL4t<=_QFMUS<VR}NMy^no>-dhU9QSMC;X0GaiA<J8eO8R@&N!Fa@2%ACJ%t&@hw9OEh9Gyv#_iWVaG?iX#|GlNSlE^P+^3W?aweE$8s?o!}lfB0>z0hH;F?FPjOEF0t?lhv-7hflwx+%b;{KtPx{3O++A*?V21Jxm0s9hVRgB{;q_>eEdHKBk4?1QRQ)q>-}?D!JC8MXeL*mhEknlSS3;4ZsnxI+PmCjx<_bi+w55L4ebmj+iGzsdjs}R7d8^*M__4!R5Qb<uWs#Fmh?NFqvCrX(O4QtGnVY12z$|1e@)=Dl4W5u#X<>$~yWrUHDb5FYVa1Lq%uWM_LJ77=ee%g_+EJ-IXO;=Xr!akr3FoY6M{9*R(iv59BrWP>A)72Z#C4XttJgNS8tO@Nj2}V$!CwzI?3P{7n4;ioqZ>Y`5nE|ZyoYiq(UXm{-4|nKqLef%-V;(E1!~*pp+s_=D|FDA7LKh9+_p3UMReHnSo#cwj4Pmh++5iafP`u}^5|fs%Y<Z+fD)3D`vp*V<XkJ0nitEAKN`>ami~0E^<gXBN=h#;(dE+K$+G;UtWy?+fzo%Q*omXM)QbPc!(OyUgpr7r-$A!x%i^V4>vU1=2*4pAcDZbwK_Q(B_;zN5<Sd+Ja;m@(NT2|SQ94wVoSLC%IttJREmM4;W;H4?HlC|b)^jp8L+!4o!gbR{rw#!NoeiF*IPt|$0pxR-U27$MF-&|>K9&$ZJ<3WHXE7|Cwe7aMKHK&22baA+vI+N1$C0K<dWn@dQ7!9qPlO3<ijq=Qu1aRUIEIeaDDTF}tusz)z$BL0?fy@*5`XbtR9p?3`3Sg*2su8ZT{Mt(yT}$R4oa)4@e*m=`2i^9G~HB;#$9fRq)P9BMsm!WG-I~3FdmwxJC)jqiF$ev-#`G9r+U)_;c1rDwV^+^(`FF!mohQ+24<tV={mUPRrB@$?WqE47R+rAopmsVW}?o@{wB0=d-r^|1l+P3O=p>vQfbl#rF#l3Kmo5mB@P=RG+*pE2!kW-Vv0Q8%IMR}cnjqMB8*6=0oc1MmJ)YBE73-7nx(ryZULvO4HRmNuc~u5m_KWjKDI(Z)9e@{IXoGoB6)w2?mch-DjZxsxv5R=<~lKTa5W}_io7ENiX`WLnS>11<>9C8@MJ`?&lXN338_*MLlE)(DeP6O*4+T7t7_!FtI3Z`Vg-PYtkBUyT37993S$_WUKlbHJ)rs4<>ukF&}bcjji}k5!7U}4B&pmqT_ryPrRKE%<Lhf44eMS+0#A=iTxAJ9W8G{NhR{2bzdGlCErhX5NwYv~nr@A5?H&AOltcBWSV%3_IZeF$?SVxFGn1ToRw}Sx=OSJblIt_-Sl799y2`$nyjVWSt_thqGwe=-Zp<I)ff}9lGF@dL5X?zMkRJ9U=V+(ZJCyh^4nb2vH(7FtmwwPxPhb@qpqk`h#%p?$+BAY9xJzJ{-ezYkuzY@(UOU}R1v@)w`UwoPQgbj+8OBJ$z=m9t7`L7NyXvt=3zk9Wl1l;KS6XN0d+>mV-S6D^FI)ih1$h-aX0yE2;K`ejKcnEgv|<48Gsp}1<u-0~n{C$)ME7D0uwszcLO%f{-0$ZuQ<q(gY6DCXQ-J4cc3a7$uD`j`3;|+Vq)MovM;%g@_3Q8pRn-VV4QnHgJ6O#&1&fcLLgc~Ur|lFlLJU$Ep@u0^N{}dsLq$kbtH_2c4JD7Njf>GM|F+5cLC(IbnKp95*a(dK)_t{@TeiF4ct>v^oRl;MB-?{IRbY}Oe0e|x46R7=Kz!Nf<gYjH<yD&|6nx!{OUEtL9dpo$<Mzvg)F`NF&DnW1EF4uO4A}%=5y6qIK-q;=81lZCnc8L#W~Yt4MZtBm81UeuJ1o>y%1Dbw1ozM@6c@zTbl_TR{#}eXL=-zKR=R4-TUll)`wanlCCn8Z5b#zZN(biO9Ace=q}W&=^U4fppw8>HciyF1iUQ9ETD*3%Fp|ZR6w@rU;Cvry>v=pTS4q;@Y230L<s3>8K$tYAmSuqFNz9Vf#RjXvkHM)elcHzD$VRzYZ(h7g^(@WTDMvu&Py#M(0tjPJfIr8B581+)WEwETB5FDhZSP29L7+GbIfl{MjB^*T=zOSUaU{y)QRh;$Q{kJq11uHZh$?QhEW)fUzeE(V9(KiCjD5&YMnFV7jrpLGUQ$BurJHT}QnH;j)jz;U=ArE$2roO}C~T6(FB;z~c|_NP=OpGTxI+BB*`<XDj13zr0HE#DQIRlq&Mh!&HU_4jd{Ly4mF7PhYExSggK)|T*EBhUAt9V0wr6(>BoA^8(+vJ(^xSpqeZ;kmo1rU~Nf}K|P#Kb_zGD)u;EsMY3>PQaER~^eBi*@TI3Pel+pEcaDd0aEJt!JLAYzU4(SUi}XdybFf=RW}q1*wECDJm<!fA}JZQir1`y&gJVLk(NJ3bdr|5$VML(cVDCSsZFRUK?I_QQk{m@SxP1-=~#xrUg!`2dLKGE#U%6FT_?<tE*FJxggY;DX7N;P@6$s+C>il^K!7JmI`Z9{NEIv8qxQv==o?80({Wk_;Pxzjl%&I#xo^7#<dF1iRoc_yV5W92GtT2IdxVLi*0bQrY8vUW5bctb47iiT$H-*9fTt0DV677SPDvlnb?~OuGApXuR6TvzB4ghE55uA6Y9_F_Qkxa8A%B><3OWj%l_o*%x%2)OjdE!<dZGcVaob=~AW(xdT^)C--X4C^nmqL=b@rrxX`Ck7rTU<}sfnork5%_%-8^S%8|cqU&I^w^+ANRg<JF)KWDaFb|+!-M$mc_|FFca&s>}XDewIBOh#67h^ux3hDsMGJ>87vDRiP?m)Dc$>=sgR9i|oZKt!JcIPpG(2c-e9r$Io(#AlTvvD(UPCTar4@yC&Z_Q_;Xfu*41jz(8bM)20Lk2+BP=cYVSCy0o1_l`}cA_1kmDWyGXcg2IV4u%2p_kL^f+F4F0p!`PzG(1U1j7oxLOpUM7FH_u=pD=GC5oY#{wgvfICk!(DLKUFR|P_OVG9uF#Xhrr@+$Pgeohxz??W)CX`VAhF~n3&{30>}n}Iph-ea9>N(nP;`)GJ3E3+^UMf8B}<>5j`4L6ZF1ZMIP5sTA$+-hZgxv!fCI5RbcW*m;$GE$X)OOaHsC#*od_Qo!k38-d<ngWT=h59=PV|pp(>$s(7&!nuAJI+22B%4Y#pD&WA`q40%4$|c~T1dSeBQE#~uQyovxwQFw1zkz@rP$6~JHU}azFmWrc7FfQM7ux>3gmR_DjqCemBpA*yA=|l)-2cU3bi04J|*$Vyk6h<WLuP>a)Sl!5ysqhEA(SiqNsznk!)<Fe4n;}8S#@5KlQ#KL%I!@<e)A{S8L-v6{j2W;cyskSb!Ii&UNn>gai&~QQqHPrYz3@Z?q9BGu_$C%MXJ<r)WQ{+s&{^4dUd|W+@9|z-zs-Gb7_IzE~fIUuAcdM<<5P|FPc7T$MwMg24Ipme0Uhtl_`&IMOJ%j^IA}@}Ks@TO{4}pnAGvWQ$kS_m_yTRVS>kVR@E3@~fl*GA}8<0QlW{f<fidN(oOOZnM0BF0t-9aQl{FpebVO9ZM82(}*~C2}$q2OE7X?MvEp#hy`l*W@;-klu*lS<Pd?>=Y=-$k-VFK-|&LodrNX{e)-#MzkT2I_Eke%nFMJ6@Y|1He)!wB(fs<`D4wAqyiEA}uYW~O(nHp?(avB7E$7j2ogP1iM>e3-&WI*3qK3lQQlAZFUG880^!anR1b9%uw>ge{te-xA`TFx3h3_@gxQ%?!&8NJ7WAYA7V0n5Li&hEM4ey01?+b_A=*<9WpT-1_i(>}D<hTq@21zppT6Zpnt=T^&wvI<TAW9Cw7IWC{!v_y}IlxDml;>=Dd<Yr8aLl(j<gr84u*fIXUlzOjgRH<@mE|V}Ak0ivWEpn`P!Uj~<4~zN>P((>&7$urw81E;C=dJYw=T;!KZ$NBWa9pcm^FtskXNyfsZ)O)G_KVwJK;aQE#0S|fBfmwmqm@PM|rG@F^tdVQ|-yk1>VI`*1w=hiZ#GZrkXB8s<or<jt+wrVPndX-9dMF8K1(;IjsmA`e1Q+UB_iCvlt6)<Pe$<ZTg0p1)CTPbLG_r6)=ZOa#wjT;3M$VUWKz2BlI8+G#ZSXg-9`T0`c^i`7+QO^9bIiyQg!9Bp1htjn~-F)9V~$!Ao$nWbgrawy1TbfS%q*csj_6l>j%2&;bLNGHMf8H7amV2NiH;<<KKPZ8Y8E)0V<tN2h|!lpGR=2dI{{l~m&`c7T;ajVv_~C7I33Mtl(pS76MZFI>Ikr$eEML-YbR6CEC4&Z2p_XK`VYmaU8li!#`4*L7X8tGFv$5DP9-94jp?U~|Zq@!d*y1O6hp4oH-%<UV*Il*JySFL<9}M*k)Y3LvB0#X*ZYIQ+oTA<pu!|ESuxI4PM?dK$cXL^}&uD9`D$5^t6tS6YJwo53mo5vU8uuRC;BU;#fT-L|E=m5po}hpf#%ZaOP5$g0PrBbbDh%%MES)+v)n+HD_lbS-9x%kQ9T6v{_MNiaGiD~?8;k<)ocVLhO-8DlW$tGL;*>*n2~yCZ2cHZkH;CO2UF0s1AdY}aTNVkdGzEwgCU6nAH(XWW-$7KIMj&mPlEtoIr0fnPcb`e~M7m>8o4^;>jozMPf#?fm|*{$srpfBgFOm(RwXcu5t06VO99E$$POKy{3WK99m82G0)XBsn_E0*uW=kj_U-(1in$nE<f5)M?4TMIWiO_0Q?H%Z-RWIc=btCpDP#(epv~e-2{VQP<QsW*~N#MRXpFxflfi_8KxfpNofgIRNLutO7P(%C5v38L*$BvfxO2e$CFO0xE=5ZB)psLud9{z_J7%$<d04OYu7g3C1OD*~{$!oR#GUu4-xq^o^u7<FYRdDy_|HdNio^TBO+dQXm#?dRwlHJB%{nyzqEi3u&0a3_MRp1uK+O!+F@K3Q5>A#(vzU=bopFT3%L3940)xKxA^O^Wvk-ncPyBJG<>X`8juX7KGa<SI0lkQ=vBUlj#F{Aibbm@I75BI-O@)+4$`Sabup-*{&ZZHJ8yUW(BEw7lTqTglSh?ijCS5zlAl0yHD#{i^oz`N@K{pY@xKC+6}!*&nlXkev*7rUn=5SG0t%x-i=mq8Qh;@9*b0={LL)zs5%US%av3TmuSj)=zvp+{sS!qnu?;6S81insuA8vq3z;0U2RwfKL}Yf!a^U!Klgv+wo`wBUL}@Xszjo)v{@O=a-K!+w7e=T*h|4=m8pk6LsGV_6*v7Ka!=t^#hrMcVmxen6TynP)iKVmwTKk7kJvs@PF$drhZZ_!F`TSST3T-6{Hjto9+FnJcE?LF<ZP4A^wjy8ox?eq=yJO*2Sv*y$Q7C(YxhjQp^~uz8YDGN(lRSuZ-*K6k<2?5jpP<I!XJp~6TUr_8<)_N;c;XD`9BUjYQiW}6lWpN#(#Qtij{|@iR+fFH8hF%iE3#Xnv8Ix{L<(nAfip$5!uONm7*?7P403zLam)g6+h%AUCv4=gQ#7UzbH6`;6tN8A9`+!Q0d_20ZjJAuy!v4?L2~NwAZ0gg#;ob$kAfVAw>DU3<V7;hI(X1Aa%elz^cqqOM`^SllQI6T;`?{E|OHv6oD`!V}5QzXi|R1;&xn;Nbn#_1z(vTH;EDf-rp!WrNDRE8gf(lG99HZPfREnr+^@UCL6$2G>wx!fLfjYNk|v&DPW^!xUa+!jg9X%s?x8t4Qw^E63diTm<k=|41dKk3%IE<Na!B&BRbQ|RBE_e)<E28;|DAYzsY^2Bm6QmqZ@+@Q&$QUxsZ0rF3LsIGFj!WdznVek{f#AL4-@G^^CV347*M7>-z*}Wy6#@@aWwNdNtCS9tc<g_qxnu;wf~Hpy9v0a1mXWbAkvG*)pytmZ}SvtMboTIfy-Rpe&#pU81Y<0RRhg)Pz1J4}jtEEkg?}BR49%vTPG!$49$q1cv2En}I&ijD(c!&oCh6axomK5hc_D#fdLBi9-udaZdjNE8d^8^RpwA0<-s{?G`-dOxf%R++A*?V21Jx)o|QiVRgB{;Z-#;b)BRPdTgTYrfLL$`_|7-+j%gw1Z+OPMp~00W6~|5pE+dUUR=jG66w-Nv`brRU4P0Aoj8bS?r4BWnYZfAi<iZvc(pLMqYDknVxPkmm8eVfGB-*4fZ5Mj<TDCf8ayGf(!vZE(KU^oqvL#l7glV&%Iq{?D3oA})F+>;?w^$s_GZ5Ud<xU2m~hUjf42HUBUMx-Wzy=<7P85rLtJOMyLxSNtD&AWxA_s&AN=)j!*1CHjjg?WZ8R2LNwJkh6HG%HmgvdG+3t%mGf|3T!3rBqfwEDcwtXIYEycM)2c2o**b~w1ZyQiV<rC)8XXuDj0qx`F%GQD;RLhY^2P0i3B#RT2kd)jnpt)NnK`O=>k_vo%nOAA)Pv=@g_tLGT)cq1&F3Vk;WFHGz@H`3wrSC?u6GwHabrFh(y=adJBM~jXgKovj)l1u#>7x1?f<r*;a@m8ELOK`l?aT<tSvbq&RAD2KoB|M|bf_pPHbc>L6rc@SrcXi5YP57{JXfEr=j3RHnqg0c>!yoN%K{cU8$3-P<BOpJ$mcM-bDM@?;)^~sgz)K6R-!nIVc{%IIo@&QLD|esp#L-On~oz*lk^fRaiUuLvpo?euqjGPRk<pe`QjKlTBAIwVDD=6nV0!rR%2G;FW!rat3k6$0ap<r$7i&Q2GVX9_W}c1AEMRVcxg87`~Z}4nr<pa<1RNuQl<AmBROU*oG~9=7!S?Uol5=4MIAqgZy<olQ@v^O^)$;iUC^J~X)}oVOPQE@149}WT>N!#&8y~p2HR5w)Qpzg$kAB`V`wJotn6<>3%7UAcT2!6tI>3pSt*q!ZBV+W&;k_j`cvYtAwokn5f%qwaHL(tk;hvZeR>&hp%g=e5eYQ_dw0d2WDaO0`q59bbQj1i;B>WtLT&L?b?yf9XN{7}Rw!ti9b+ViCu39uoJgda!2zgnaQWn>Hn~u^K67H~;A%_;6?sPl6iLqgG6@;1%fnCG;mL?(sE&^$38?^*HSOBI&-;n=fYVjAf!Wn9*d?(7z(-a;X(6qv_B4etEZT2nN|~wyuV-R253eVs5IDyGu&5kvDbXZJ;kxN6`4K2Jr~MyaU-M{K_aYK_dR*cvOaB?`W}`5K-jV#(Isa=RjAcri1!B{5YjkVx;4h;bDr@B}hoqOkJ+P=yXOc6|N)-0%T*OO4a(zY}TawV*zV!+d)mouN`ayP8SSO!hcN%nK{zwnh=&YCNDg%LFPAY=*upc=`JFVWK#D{SRnhLtfa#p<bgQj`{tIz<|BnLBI)0@<$5fnipdPr}xGZt7rze}&3Zl{8sjXY{>n3cMWgUT>Q5(YNpn#8#6^xv`crs_x3Qs7d+_m$R}`5rvrVfQ;X{%efV#1}l_Sv1?Zzt!N$n~^`G;JdV90Pr)&3;E?XZgjKD=%VOei~&{*@>=L8fQ0+~+-2&rds1zHNn#4{T+J>onbh?+SDGO}Op8<rHT0-M%CdePexa%wA*f+(#BqmSASNp>SbY2xA`kvPZKr?{VvxcJHB6CGf<!?aDnhdM^i1cz%=8F_&+>6eK|rtk+a~J=Is2|=+Q<oG12XPg_tj!<+3tel9ld>UQqmZZY)j@;fk~F|<pC8iv?9p^@nxTrzuvr;S8bY5@O3vX9k)<->Om)t+b<7NqoAfWXXn+ha8#8rWD|fz1V^?4WfxXq$opPqx}$qQ2y3iz3SKvh0S`X9!$Mu9jI?M(a1XsgaY1}d2d=f|-^GYSM6t7CrK`5Qm1UN)-w>cz!d$@t0dEzebYT9?A=WuaijDO#ugri(jLV~#8hhtms--CKe4xc^Hwz<KEJ-oVLNV|6p&r}7WCvhceY-!6yc7Y1Nposh26&#tELll!up0aroZ2!edPa<Fl$!+S#j8}W)O?+C1Y`~+;L_%UFa`zqb3FKvEsRN~0W&P3rt{Elk2Ev{inEYo2)g%#xeHiyKGd=}66Nuzb14eS^G)0VmI`k~6*pQIVb+#kB8ph=ykaiKKIA7OAR?Z|d{9X*DWUh$&9;0g+0L5kA7CW&&~6ZfmmP2vHfQ4(jqjB_qU*tP5_1(?A^zU%(n18rhK&^f(Dv!5NEkck7ML{~1Jh5wDALGE^B)bhsjY}XIOT+Enw-Iq5Y7<Wv%3Y72f2o627fYo?mG59;@Y^)&=t$1jHV{23`tbqF$q_2M?V^di<4}Y%29NyGcJ#0)}pJ)eJS8S8a*f)Kp<j`^U;8L+-M;>pn^%Y(V^S{jwRAE$--%juWjD5tNSAhlVLssbUQv5PybkR^h3_|S|(zd>{T6XGxo!T5|}NRWd*(+3Au)ty7>Tz<}y-vL=!ss1?48)dOb^NFyMm8l;HRlP^y((<CPha#ysJ?NFMq@4Y8_HHj?h$62|%{o+QIY;IEw|iH?;JG=_&oTfZ(i48DNpHb;fefPuM1oRGfruvGTApBLePI_qBRYGVIr+%-b#06?Ely#+L~H|0WYDwFPhAzIt^@vLRow4qbN>qpj#Rg9#6Gn^B&3HyQ5jANRuOZEjFCv_f*&@d)r^qp7^Z@QG}Lhis-;mN()Gm1^_BN0TP!YRc?&f{5BwRy}ZN#|kdGJef?WEP-Cx9B<;?Jd^rQ`ICX3$;{D2h0PgSGVuPGXC>HfZW`R&)G_v#mEQS)y0_4wSqdpvW%c-Laeo!iaQYPWiq-=5Y?6vPTT41r`>rBAao<JR|kHXt+X)^=4{*yoD<LKz=KlI>09&JDB6tV3PCb~%^ZDo@Q?wJHI!he>QyDBfq_AWi=AkPXr;AN6<P&#1=#1aOz7qGx}ZpRcmR2}t1lY-7QwKBuTYO1iG`JlJ$lD7dWm8vroW2J2#%e5X-W?9`Bi~XUf2S}d9lxIpS%jau%FXK*830)YMSRvQ4BFv6TgUzz-C|$wf9)(no`0H+ddke$;vFuLlHe-dwIB!QNvAS4uP3`M8x8>9=BRqU+(MX0nSWKp&5r`wv1He-%=#i>j^7Ruf4I$Wdf?1p{78hbD{nY!kAu)`8sat*)u8Y<c_n?1IeaR&F70Gs(v&~rh{}jjuujH$A}BQ!tXcu+ZWDn-*vIksz3bp<Ch=)_H8)7{x-5Rpkuz|3Vi?dujs@)5QTPV<~W06BY+#{=<#ECWP_>hjA#NQYAQ+CbexA2xM08h>GS75dxHWSeH?>RKYjl4_2(6m?9cSLjeOAUg5AF{d55z3o}R@bO+u-cdzGI1!XcTm86a(1lNcv)%pj<FTm~l*qbwZPor_^>_K%6J<IzTk$RXGY;O#zq@Q{}Se3T4jXUpS5sPPOO^DPc}ESEnl@<}z@!u^5<S%HE3<tGNKz~pT+`Y~!$Nf?3mVGL#KVv!A=f@0+2q~->T&!eQ2ZNu8*{G_UfA<^(4!9fpgAhMlo#wWiH8rSL^m;{5~mhRKfKmPRT%c4ftqdcYv4&$?fOM4O(0K9#a$$*rxEtadwyI+P>>&@96op|SH+$uudbcdJmDF=ebSa6^pEG{o{vy5dHW1&@TLnZc269qGSorR=Vl0i@bYrpyRlH66^3-|~;wY|7mCP|Bf0H=5~7&i-%IuNA2TJJzC1HCbi;BC5l${0(gMV#1pjSW4$&OuiH0XIu}Vjv)4HpmRO;B=7XdqBMFQNT7{k*uzowQ5x0o(>9qW3?e;ux>Qn3$ZD{N;@4C;zp73I6M${uC1gRZ?PSg6l!FtfhfsrUN+*3P`JRt^K){_Zuz+lt5DH4dI6h>4i7MA(Y)NVxG+ioDn<)H={&aUx-OY&KK;lROO^>xZCRd`O{iJMcPrfu_>1H^AW^QE&hSDgi#@V>@IJ%zrVS<ZeK$1Pip6(Z)WP8gjt+5_hy6#T55-BzjMCFl_VbOL7*24uScuDyE3JXPH8K<8MvqsQMfTSnQthwBIq9}7)vat~%Q$4A(s9#Sy%m;9n~q=-R<hZDnr2{`h<dy2L&8Fo<_2u?5}vyI4Rnn{E`5{)qcgJNXw(@w#pXYEU+Ruw%~-j|r(o&gt{iaq0R0kJJz%uQu=}>)g;~XbDXz<!es*7yq0K~uu_7!QvsBj?fXr_-!PW*^A7VR6^bOPp38Musj8A2C0OPG5dO(1+jl!I~U{BZBahVvJWxy#ikwMz7vKDuc(ZB7>59>eH+yBR}Uw`>*-2Ru;w29n{W-|_L6*wLcmnFW#BK$=J8s+xvcFe|V(a5gx+ItM95Wpi-$1MLAeVEc(@2A@?S1IBSv}0DzVl#!=`JfyA1@@<7l28YL0reei^n8>mf(WLXh?B`Phc>3OvSZ_oqNR5M-36*;9!<#2sq?9Td?DjCa<*2d)hw<%h`ASbB+ttD12-YHXZpr`q%;gHv?LAIYr67OEi6LfJQ->Ai0Fp`7ht;(kE*}TBvy8AW4uUUmy|bzEUXuZ5N_pie3UtL+iLusCOuC+5!j|?x!t>T9P&IB3bsATY1#v=kv!i165MAq({gKXtaF}8NDGi1ufkOGUo4|l3<pw*BL;_HDA7&>kKH5AcmlE!`T1Ili&Ak<W4XMRiq!D!hF+!JA59@Yb4T^TCXt)_@NP7<bTGx8@V2S&^T>GC_ar-$q3wxZ-cX_%=b<cjB?=F;6zFt>PF|(I6DyH&Pl;_8$0@bV(uzRnm=Op1VEVcLqtjKsU7%Nq>6X$XRq6<<?So@cL>u;o^{c{UJzh8~mpA+w=3m%a(dnpuepT@w-aM_+T$#e=<&?eiYb`Pa?IX5Nl$*AVis9anW`=H7yCKbiI}c0-P@XMs3X9SjkbT%Cl912z)!%1!4(DW|%k8=x6g`rlD`<kO2Oa%}xG+l8b%o;^H)xraP6B2|eI(V6m29{LjeKNc`h;&!<;EoxihUdzK*Ep1j+&6ASt&co^6o3MQ|ve_O<cEZjRg?#6V=i(G#P0g?5hbF99Z?_ZQ3+2VH8uy>VtGS6(IrmQCbAKNtd%y${>0c<u3|VA&ASU8iJnN!aO?2cmR`qF|6IoK>v=&6m7s_q((x71UXua!GoyRmm$llVyH)k0#XO;0<6j$)mcplHF-0g%w=vW;UdZ1Oc4k(G6o<MVv+JY7PsS)#Dxc0DtN>ExJi@<@b5;+DFwdMYlWN2m+2^Vd169AEFFRXI_M8q(KJr7@SZpQlaMZMn`M&DNgUDGjYC(PP(^-0C#)_0d6`rw1s&&F^IG7h#z2;P$d75SiOW>O-LkHRPHz!lS@@kdD{U&5nHeQwU6{I(HSI#$CA%mWP0M7JyY6NDFiUP|&;b!HrPee4crffX75VNHoRtkzDhsZ6E9lioZh9bK1>Ea0j|rgAL4t<=_QFMUS<VR}NMy^no>*FnUarbNC;X0GaiA<J8eO8R@&N!Fa@2%ACJ%t&@hw9OEh9I|PO+>HVaG?iX#|GlNSlE^P+^3W?aweE$8s?o!}lfB0>z0hH;F?FPjOEF0?Tlov-7hfl)`%A#MWc97$@?iUyQ)r<u(dtD9=z~ne7!;mkS(Tk0#0D?-}&iMB7c}>Vx~%&rjQVtZnrRf{APyGA6$giWE()hLy%*9Er4!A=;%a^^kT-2g^ez4kDU68X!{Ut$Op~$Nq&u7^3BrC7eQ;X&RKpK8GtRQR}*8Zj$x^vyidKXEd!ectT>Og&DTqsbf34I3M7J75hOkI}I2LCD<bM$tQ_ZJIU)n{Y<H@JG)<?oz+ogQ3lO2U#A6ArH-gs^cCN_^eLu{wv@b9^%|?E);9Af>5+JDn&k#Vq2K_I`j7Dy+Mrd2FwTP`gP{5e*%DlpZq`1(Un7@RW#-a)i59HRLX+HJvO%J*(9#x#pN=&Yp60wiNG1b*6eRvFQy4L2#<z~P^?5cPytDajHHLyc5o?L_-^YSr${w>76bKO^&9OMqaL|Vq1#zwrLSlAeY$fEjg$p>hnkbppygRHEH&=G#A!GuMjcfaPY7>%WEJ|2k?zut<ld}QI(6<Wj(dL~woP*LI3aJNNPD~zvA0Fwz6Rlk!ww=3ktx;=9Y|spi65|x0Rm<>|b0Z6xLL-q=s|LBKW0TXR)-E7k&!UYl951vV4r07cN3|;gXMlLNvb7ckMK9pnOF`B_nO;<hE|7u*FxPabD7`zwp$*q$8MI82gPPx{)ZCcjKHb&Hc@EX@gi#>0=f&{0L|t~mHTKw26jO>u&VAsKw9s7=Dif4{Z}X0U?$4N+hOC<;hEa)P)^eiv#6P1_nJPsCk#gPg#NG{w<HJ(e_hK2C5=~W#S7uW=)|Wo~6hm3fd}&*ytD#CeMX?GjMA~y4r3&Zs&Em&MU{6wDBZdjdFc-ie`=~OKjo8b%O>0)uigLE%lhP#aXgMUnAh_~I(9o_I2nMn~L<>ZYlQLqSR4q<70lI3$2XKOwO~83|)jn?m`j|?6T}25{h>9Uh+_QD^QO~m733Tvx8fjwwQc<Sf*KBl~UkBG<7T&L^Jyig{gW%plu@va)tQ;Pa$zt!G@AZM(RACmP=`ZtC28MJ4=q^KuT*L^KZLN0hBCS!NHp-hwc`jb|$1>hRwUdZC6J`^3t&4qLQkXjJpYFidvn-uL?g;1K4mlwf0beJhv8b61-mfRrF+FnBI)-!ewr|~gVC(DQr*#WMhl|XQtz+vkTU{hZ63j`R>^?L&R=1A_GY^<=$16D$p|1uK9;B{L8a2yOJleip55hv+)m_o$*8?O?77uD&b*>s_5XLPuu`m{iSsvyd<+tW~Qo^3opHP=&gZ56eL{e04x=QL6${K9{#~0T;8rB84pX%4PuCf-Wu}U`JMtEk)U!BvwR^(Zxr0HmOzCbPS!#n27D2Fn1v7%!vxNMMjQ03mFct;ABWT8JRk5k}Oun@?yA~FmLW~stc4|9m;P^8s$)Jhl=Z*ur1IX}EKi>6`&<HtaXBu6@)-kVe@5dpwGio5hvJEMrz+W@0I73{{Ow>YpjN<BzHi6)W_g>cZ@PLESH?xl4Cp;I(Miyow%+x0i!^91P+{XUKV!gY6FkgZHj`}>Fm<K||httkj9Ez|*wW%5FPx!klyPr1#u!@`(*Q8qiNPNkSu0J`=b%w~1oWb?4v0F!($;E$P2jxu5D3zeJFNkICF3?()6s2U6rUZ`3~=yh0|aJRXae3kq2GB{+AN<j~xQy>g6mSGqkrXVVbp&W7r=MPPer=fIM=<Ex36e%lO%D9q6Y3(nY(W&C__0^Sb*=~X3%3`!^JC;$(fVfdLDOswQhyTi4=p=8-zfoJ(VNQQp=BsTAiuvt^J>wSg4pWr8)3s^O?T%N&?m$tX#Ep$_Q37fW9xYGt1uL*ao4akEVCvb}Sll6vChv_OmEbqoQE7RIun~HNB2M^L4n%JPGH&Z2M}Q!Nr|C}K$|6eHSqNq-;eOzNfVY$o>x)w@v)yaa&@HaNBEZ^%*_~UE^MO`iu8_f!im)EzYaSB<CFAQfu51p74dpW+qL!~<PH-}($%?w;yLM`eqN4E;;4Zh5&daN*uDUWN3a2y{DIAl~AQOl6w&19AwlH<(*W6|>l<mn|Spr>D$ZCy#R-B6f`sPC|=^>HFkIJf|fe+u5GW;h95Q8N@4~<DAHyU7iDt!EVgBzQPLKVDBRON!CoYzY?+wx^%I|vS6ZxAr%CxP`~S3Q1D_!dada1~WfX0!6Y#owEyRtO1{3#&$&N^Zp8XMR+{@}08{+=q=32HciXU8x#;CgyL@{Wz_arc_Y6Hf7+jF&9GY<hrG$9g<O2oTf=FyV2VQRilYIHD<aB_T64gW5?aP`1@3Zrvt*Vy<Xgl0Dh9uiX>f$#T!1fIU4|n8@)ouQLt7v3h$Yny|vlQuKJBkHHKIWIOF(SJkw)AS$6lX>R4XYu{0wIOn`t{f!RFA@EwtvFwvXuxNFuIb?Y_9jbE>>df|L5B>;eHAhS>7TR@?Cl-Vt=)MLQ+$((RHAde%UE@f4j2YSAmb*0CHbdn?rf$??sJ$fKQ92l+$?ZpdgHMBXlGj~z|1Q?iGM+@m153gg7`vxIGCr-L>+dmrB>+%@pQ*TX-JhU9u%6v?kj%dD+W%1_|?U9ubkCEoLs%P|X1^`a7EkjCYxnkp~drqM1@L={f2P2<F?}FtL(ws}UkY+mDDnhRI$OmfGR%#*wFsB6WO20F<a!Pk_nXjZ|Fe1NSZXYRW)W;Sbd!sYRIvrJrlM)0=RaC${fLe50c5Jq(%XOH~2Z7&m&o`&0Xl@!D{xYgs;S^x#MOZK4LfUjQzUag>I_nloRQ*XDX{U#r78zom({XIVFye$~X*3{I)wmisIhS)f2kB2E`OEN)g4al}5C{(#yU`T}4;dKJYa8{n!-2pY=5ghAWdb2?pn)`xLaO;kXPGI;2~<IE?l9Ez^g3S<_|24IElHsbIW!4tI(zw^%jhLkpvc)OBq7*U#Vg_gAm>+w^mynzh)-hI);@U^5Vqf`i!3uBNUt>El0pk&swSuqyH!nXYN~3hf^}3jJ~KxNbt;-LL$NeqSb1QLQL9U&c7U1epoY$uTB%v?spbK^O!uIPh10Z*ROJCuRMKmbD=;WS$g-tYRkJne4Q;>rI|$QxiLL9nrC-j3sgtqFJ`V(#lW{pDQ7<!*l*Nw*xpWvSpF&8X9O;?gCiU%u*SF7HY^>=Izy0{-hrfOM*<XJf*$2?wUdZ6zfBh>uF%SHp9hy0g^w`o1jdS$)F+8%t{&q$*fe|&$BTP3=p9xf@U;gy@^Pjyzfek&5R?SbJzkL09bz=InJ8mN%bh}{pZ%p2y<guq`u}G6pTH;>i<Gyf6rfddCyZ9tFNE|Z?;x2=eI8YYa>dwWmHT%cJ*70Z~Jme5;1@LwsK6uE>0X|CltFz_tA=HTnj`<dcJZ4J{i+obu$8ZCsK~`WI=JFGRRbY~W8QYar2h0rH<4_bUCj0ZG10x?JH8(=}Se|0hAv?$UNtF%*l;J@FF&)}KWPja^zI+`tuGLDBP<uc9{NqobzAS2VJ<4Ma*f752`<{G}gYHL}?L`U2V!5g`?`24}W~HJcCyhEq{F?6YGCt)%@W=@cyMx8$#Wt3)%wjCGHfAWSy(w*E<`uKRF(~!FOl1z2<gW5mcYyWO_TpxlBrVbaoZ``7+$==uD3E@0AS8JlGL^uE*i#Hu@*d*E#%pZo>2(gW+zPl^(&GYA2D4*mxCN(!td|0USda3U@rq>CoUB!&0{3)KARDVW7b9?^>8=7!iNaq;r+_sIh{xf9XmV{O)p(07nxs%8OASOxX7jQUs|wq|!t+x}%5M3&4XaQiGkO7=i4G4iXVJXev$!xxyCfFuM_DMg>$)zP>c;&@W=fU`&{kP`kV!8&wej6bcLV++xeiE_s~QjRLMV$pa&_=N!}OgE9rJxRG}?;AcU#oK;RlWmah8YuM<v+ANy&`T(@{1!j!YL$7Ph#8%a1Fqfxb1;4dO<RSC@tB*Bw&*z{NS~wk_4IY-GzgWWmI7(^)|cmg$*}U=mic*^rxN7@5d<yX^z{KT2~0HhBq8-Tel-Mj=r<N`lcDS#dP#jGSV>nY%A_$FOFs+~ZTQU}{%{G<<-52~15N?J?}WEqGy8pJ9sYvZh_#mt-hnA7QKri^eR>^#vf(TV27mf!2rEP7-|s6(PcC!3*P4S%tQEtA~2>U~Qu?CokC3HOgBihGrRXiacVFma4499nA4>`|`v3kM;Kd@$1)LJ{!0HB{gj##iH4aLs@o?2gGHG@307e5rH0te2DWeIA&wjT4dLF4Fd*K2;h;aW0rr5K1^w;wbN~vs}yku+IJ@>tC_;=e2~08Q2W*}NvH$Bfcmc1`1vSR1QAR%5hqhz4sA?lWyi)FMT?>Wx(igxJerW3Q|D6w`9j8Pq-L#7Ypv`lCIk*g@~n(Ma1&B{rf<1MDwn`2KGI;lrYld?!XhNjlaXMK_<SgE0k#YAsQTMXVrAzx#)|}YN&Py=!g_%S;Z`okN10Q%P44V8>3Q<`zBV<>?G2>kkmspTwChRk(jI6H>3Vnx?z5R`>8`hAEh7&wE%$a6rdqMU*LhY92U3C}28UoM(N3w3Z9>j?0<0YVeOlLAT$GA?8q4LiLZpUoH}op){%8vM={TybF^SyVhj*iip@S*zgttwFpGU^C{tMZe%-Sy)rSc@IaUSX@SEBGhOM(6>=;T$p%8;wKWZ|`o<J3lGxk4ax%!mV_MLi7V7#HYOV!EZIN0lMMs@&jM6w!vgVg3IW_jS9G97nS+#EY5fpBY}t*1{GbX${DNuMYeq-@6|zr>dvBGBP5vNx*;sQ{<3azgd})k&*8Tll6GvOwDchF)XvNU&a2GzcFw2UFCmx%ce?;RtlRtb$G|v>%Ep4g8mWPC(2FRXT@-DIkWCI(;G!XEp6WK;uyXxt?XBamtd$DA-{8!_g>jKT$72m+cjSlJ(8d+Xo9Ts75xiwVU(%cJDwXisLe`O_A;kFl4^G=x2C^EV`Sp`gukBJjXCI&zK#qa;m2XemylIcDL<*K@uy~|*m2mJxMA6r3n1nvK1*$AGSfWxR|{}B@Y4ge4~9mWnL}tuB<w9frVwE@-P(mo^Q0bSkUfj`7p1BY#ARrHpwI1L9-U;ofXTiY-tIimzauh5J7yRakPsn3ffi%%AnNrzR8v(P^~g{_&jGst+hdM&L=!^Ih^mjTbqtyNlQ2tiH+u+#8yORj39(4U9WCsblf3X?O9gM3A2*2-0sh@+Ii<mm{?sMx5O<a5<tpFu#D#)bIs^f9(jTs(>6~QgJ#YFqVO`wjuB4ok1foL^h2vA{3m^ht4Xs3*vPz|(<6LW^3BuHv$Z`+)6`koel^X7r^_z3LNdV8nZ*}Oj3mj%<h^4wPb){<Bg|th4QEr;rWL3ECRs1kdZs`615ia$tXZ-Qt*zM%=o)cV^4^tAk*1Hwn)kto7Az%gEYhK3!P#7RV$A5p}BDyT+1Q8^%W&E9JD!%hw#pi_IaVig#Wkq91bXPF|U_*{Cp^wP}V0iqN@d~w(8(LDV>O=VP(Qg`oVL8(7pbu0SVP%hJ7?5MR8II}u5^90+#PdVq&>~V?)1N>Q%_%!SCsHY}iaz>oA!5!Rn-ht<`7s)1XwQ&-%>D|i%LNXvN0Vgv_Y8XMrtP6>^}&5R&QJS!tfBB5f{AP!G8VrQiWDuahJs=-k3>42kk_Rz^}Fs?Z>CNhL^KaHK&H%F^&Z8K9qWQIM9V3anu6#vP0He!!!?zAlW|CN&AL|`tU|^npV73^<O#`@7G~H?*E04>i}L|dSh0-}^V5K%P=YP;zKK@Lor+kdscec*VfrbGGhy2dBtaUFXSqtcAfB6MeZkZq*wFDk(1Cd$dJX2JMa8cy{t%#tEA_~3WUNW>pPz#O3hd-^WE?Mp{z(j7<803*m6`1%&9cesg?gLNdpYz0@L5irO)2_NfVBvjCMSdy?RN(;`nZu0ZeTt|Y}Mj6#0r=wnbz1&X`I%2It39=uIz+D63-k*)xOqt;iTk22^Y$v90=;?%rP?bJzx3Nj+F%`ZwL5j8I-gGh9f2q0%b2j9S*uq^YwE#)p|~rY$9dzm)MDEr*$b=EJZJ)DOT>qXy|kvYnf|$@!a-0d%&G^v>%>nZqreXX22OBQIKqPL;<uJ{Pj{oZtxUlCFcanRRBJh4i%LGXPBk!+Rd_{3c59hcyDJF`_xFQKK2D`M=uV{Q*>~jb)goBhuGk$gToi2?%Pa#8b&}R6vqj@)*}c}7-ih92COVGPk*@U)U>IP)~4D57bYVk8YX*@VS6QUS1SWPlk$si<5JPdLq5Wu8a3w2&VA7arYvlg)s(r0juWX5|Hss~kW0FP*{oNiP3?9adrZQ+Tl7yA5EPf9cz7URSV?YzSGB3~1)+0>_M3P)#>>g4Q>ajmKnBT1Vi!lW=qB%`f!B4<W|gmGsQFG<%h<C)VoZb-SBs)KoeBVU!etm$PUB+a!0F-nQCND=SN1p>k;pd)!AIBWIkCHbxWuaj!3FH3i(bBPg82cx%VZMbG57z+Z9!<N*Q>gJuJ3yvq!cAGSW31VL=s-fPj!#1Z6-P$X7iP5yfb=2+TaHDizp-$b>3ipd^%h{Bp8;|3^J*t<MLXG>^JCS?W?mx>ip0OZ@J4}g<LEcu*<_b`3!^G(=Z;;fBcbSy4i5O?-Du$b5fAb>uKX0wX}L!@gIys(7Q)GWDbd!zG|wAXkaYe#Ds$qujxa+HZk#v8@nCo{WfEh)ib*EqUCYZt~m;<@re^$F1_{z5^CZd^m(21$yK8?D%iq19zrX?H6-E8X5Yz)JhbD^jsJxO(Dq;Of-fQZ|NK@*P96q-Sb=b9#U$`n$rtjEyQHAyvAS>&!rLM$S8-TtNQ(%Jd94kcy6oam8(>1r1)-*?HlJBte{-c90?f3aimIW<H>7Oqx8WC5Wk|jrzedqQWWI2^^8Cn&Q@BU$jwu^QzyUF6AZ83H;>wVyKv@YNznaixb8j=fLgVB1nnhpvw@vCNIQy<<+S3JNBNQGkAFJgb+3tel9YHK`QqmNyY>(np!6!@j_KN;lcfN!N>)Sr3ey>L_@7gs%jD^oZW_SyA#{hKVxc~AZMu^-{4|d)S4@aq_AfEs%A~>=VSUtB2L)}}OsqOaQeDT;h(qVce-y47RgonCW8R^joz#i6E0IVNh(}A6(as9|Fjs&_)tZjQOA7z`R{5J&OIk;dTQ0xu}_?EJ2T&%7K#F~SxlAmAmmD?7TnrG)bA66|bd|WS7yswf}O~k|sEyzBG+B@2g<Z_uxy^ULzqntx2CWJ}zglPtN-oz}KE+|+HehhAXnG|6Obn>k>E6l|^RL{12opJ<Z4H7tM6C{|U0aZXe)sQVrt<+;b!y;<B4sCx(V<qr#7HTX&uk|o@0gJAe8m%&UJYG6qLQbA<;t8-+L?cSvp)JCyJwLxMlT15(De?oIgSY@~qKbu@(p2WdY|EFD?X3Cy1B_%H+8zP&g9DDjCNcb?@x78qbUS!XVUmI?#Lv55TFAiIu(1LF`aTV{NI;D5+}uK;18Qe4iD{C0{fYUHj#}@6el<u|D4If0Ba5uLzAt#;&+P6^-9ivX#%q{XFeantq2n<|9E)1mThS(Eh`OUP?D%}gvK_&C|7sX6PO^I{L*FX8bH#K(fP(f{lgCmZel#?=J3t_EjqBBbdE9IvI-r7Sw0lE&030P^GRwltmEZfkSNH9YT}c_{gKF`1pNpq|)Li?LbA2p+U55%%Dq}&BAZC=nY{4um@a;$iG|be)2S6lq%M)46@eh7Mxl6ZQPs1gm`5#%N6Tbx>)yl4MWh(Sy-f$TLPyL{VAXO_1+N+roj`}FxB*RAFuLnyK11n)@j0j5?`i#Zdeb!T-qrzvvz+4dv^xk<`D*L$M&=x?QZLhVO%KsX7jgUG3(AV410~*<za-lw5Y4Ro;&mHqwZP>J-MZyk8-ilSeeEeoOCukGS1E(3sG+USK4;(nD>rl4Nn2a%YV%^))rA!y{1g;8C?%keIY_=PTAOaOmDK2szpG8%B#C(%<9^j$a#d%!G5jCSj*TInY-nLJvX;Btxsk|M`13a&;?sgmhbP*sokK%K-l4ddT!5;MN)~Qy|4m`^UdM3nLo2hsL(QcE`Z4&5f>33W@NsSsWo&kjJ4E7elx7kV`17Xg_&A^4_oDMuZ3bYcc4c`#0B>m$Nk_mj~7^{O1830*F2?m*sDk%*N3^H6I=vSbX)=pK>&pHUuu9K`a<n+4mke-MD!2R)&_cjf`MIux%6wf0^Vxdx_NAGB(mneo}`m4;0;MlpBrW6oQ?+S$S(iR}ki(_W{<W=Z}$2rXxA2EguYFPWo(m3u^P5dG<0=t7bXx}j9{!+mV+di6}0VlAH^rn0-4;M02RYc_wn8{aUEN<Izn@a8*k9G3|XZB2`nsH!HRJAQdQoWvd0`)qZyKECs&73N#|NhTG8WZ6OX?^@U%gCNtS;oe8lFPud4Uq#lDw3%B)i9Y((&ac>D7_ssF8B(6+~B|d;N!>Nnr*b|Z-4&s>(BrFYdHV@b7W`0z`WH8{QdiX(202=3jNTmaR%2;05{Ij>mS1-8(ei~L<<;Ef0Bex$9YJB3--r9zkU0cHz=^t*D*Qu+qYl8|Gq(z$1^={BOi3XV9&ppe2236K0S+OO&(+P^Ar$yE*!Ecy8%+s{=_+nV+Kjhu7M~KqbwbFI2Xg#oF5Zg$E%GFkwdUI!25mp;vu&Ke3cAkXUpS<knlbn^CJ#<)XyCj`KFqU;C=~%t-!#2`zHpkz~pT+`Y~$MMHqq4VXT8-X%N}qB`8KMPU>!0>V9tn-q6p~`pKsrrbNRB2@ZPc1Cj0YGCuizcyX=HNl7y3$I|`u`!B!!^lN)Yx1&6k2oB@3lS^j`6#%?_mBoORu`QOX%DZnvs`Vy29G!UQXx@soJWucFy9yw9js++B!Qyg}n>LnJjAdi2Qx?ck82Q6@G^^KHN*bs&?_01OF3I!BQv%Q1sXdyTHc2WD0)pbvVcac58bFZtGRFX-4fMexf*;c@kb@P597*l3iH+CTc&E2HNcA6Zvt%R&5)x*Euy6}*7b)KZ@?9^{#&|_Cxj<{xsKLEm6#5o39RPgVdy@y(y^xy%thC!jA#M~YkHZ6b=h{lD@z!uNZPdt815=Xuyllj?cyNJ-=hx(v!}6&Qt01o#qk!E+hYzq|(Y)NNxG+gO4@L_><ve!ix-FS%zWJ&aOO^>xZCRa_O{i((dz9`5{1?e}K&D(Vo#BO$9qa?E2k$d1Z`x5pKXyZ-t=N3`MI8cu5a^I#dDwp>eJD;!=9J#9vY%n(#BhSM#X@ZVxOz3vUyaO!xY6U)WtshLhgADdaZV1~mcFfQWNjQ$mUP^7rnkaMY10ub!b>*$Z_)}Z6H)KCeJEIn*4%(i-omGzaRXhWP)i>z!5EBeI2sK`Zc%Ih8B0AetQ9}*@l#OR_s}6I`~v+WP(5Ju$8h-8@WM<nV2SIpm7hJAWRO;mFjj;`W0mUm1t9ZVO+dASc1*F|B>D#QLBeRk7shX8I)L$354!GPZKE+KU$9Tt*m0Q|T4lm1GLb>quJRU7kkS9zm!G%)*lzznzJLGYn{oT!Qr9MOFS^e-D86$%ATCS%4$JTt5olD~b2=~^)uNGKgQgm_cm`Jp;E`!ymj4xfm{L*n+v8NI6mbW}wkIq$)0j;c-GV2uKOL8Z1^^7GKhQ>}t9&AeVXB!pSv+&;W15s78*dbq-UW0Q))+i7XSq8y-3rJTa$X~6D>hr_DhY#`dt*m(QqCW^38_DGY&S!sVW7~GbXf1{%F}0|8Hs5z%IbM{PYT#09@X(SlU&)<$2d!1m&hAJ7S<a?2={h5ev}1udo}*UOFAt+5!j|?={^Z^ZM!L13W9B)<TRau)<_-i@e({|bFZc3sHLH4L@whYAD4bO?$YIqudrV<qM9Q5H5C1{Jk(?8xB5k-SE~<;>sLHzN#@|fI%#3^q0BSNS-+5&=u6s#*s_4!_9HG%TQo=QnN_xc>?O-xheo$Bn_yg|ch*2Rfi?uOSe7c<+T+85Inz<tpvO;UvTbikUSHK~kvHX<s2%5b^j)PUcvI<5c3cOGXmrkKBd;Yb;M2{vj?$*~2^-u|&D6HfwKhLyIbRf^jl{#q7h{dY>0e07Q)&G62B&<G0P8G|Hd{rQ!Mo^sYN4q;*mmN#9W2CrRl*k(a6y>`@VV%7jCUuXX!BLFFyP`8I#Ke1CXbc(9P6N(!IDv)6c1-qQHiFMMhz|Je3MFH>7MOJl0`gFH)(*X!Uc~DJV^<f)7iew22zywEoh;_yA_0oH+_gU4@F-Cmxl_fG8>R**}($ewZDd7o<hwj`gN($nGSfC`CsA36vhi&v7BS!Uc8}LsKWY;iFWixMyTjD=<O`0M~b*E5$*r+M*jF_iXqQ)UC-W#G?Tk+zXhqinI)^5S#RMt$IM^C=usQd{f(hhIF*mc%(D_B(J5y5kXGm?O4IobyU_EZvY6cY2OAg<BZ)a<?+2}I;Q5pN@+=CbNB&E#A1b0_XD_Op$~Em{FfTP=E$f))^sNB?lHb+QZ-LmK_QjANbs^A7MXn2%N(6|j9S+;5;%%>*<Z$PB^9S_11P0k0v5$q@p;?*KTPn^v#CGcu*orBgNXm&1u@vlNu~t$>G7n@9iCG8B4${iloWQ`#CP^@-XjOO>k;NhPr#qTH@4}GLh?CJS>MT@r$@P^E{zYV0z3@*5_3RJKI#!^*Y%O=Fk5-wTq)NLwa<BK#%)YMj&}(qMt78N>kE5&Mr$0cFa{QL@`nQoA;!>=(gJT+?I$^}#<w*OPxf>B<=5~SrkUxkqNzaDc75U%b1iB@E$Osa+y5Yg}`;|}G`8kpJVV!SY0-MEjP6pz}hVbBh?0DkP$r`7sP!<Jc#A0zkmil7C?v@m)ks{lss47}89toW7ys0F3%pzkl^8_ABP(Z?VI$#i*&e26M%=vTlV}&l^anbs3y7DNM5Zo`@Y7Z5%bjTc)LeJ5f{2r0Galjm86USDI;b@~pl`u<C#HM+0?3rmUL}u@|O_B^1STK#>EygHIlWDkvgfl~MPnL^RY%?EMlzz|8Se|1HhG-d^1I8s6{<slfFsBnZWDck1t<rq8_g=MHK2>x}O_5oAb<$5U@>wSN)OD0bx~M8XrILV_G9An1a-yeuo9=yXH8`HuaK9KU17;P>!XvXPu>_>@kir8T0n~0u2DzDt=ET{aBT6v)j|mM50#A7%Z^Nzb`#cEj$GJj~irLE82*+(|MiZYU0?abV;8(IqadRa+MTiv~Yj>(J+Jt2Kzl0{{5g9ZdIVaC#io_-rueRleHhypAKGnK-mTo1b@0U2C8HZz$;>A+sG8zN*-i>A_j%uz+$H&87^iYIni<aL3?_$IIruDtdiqiuQ0SP8#<0T5F&ET&yCnW1o)33y=1e^prWl#VLLq)~ES=L!+!up_P2^D-<4IST3tg_!=t0FdNqshDweVt}qngx7zHh9Vj_p|+I&{LS*)Td#%_(FV~u$evnUo>a29Q$yQsU=e}m2BTixM8ncs&o1G>BVJ{abqP{TH{@x$+Ch?QC152BE00w`W58p=ojU~Ie8qMlS+T5J#vi9-?A$67w<(S)S#86@xg+a{e*VW$Z^;rW?&%Ohp1}ZIH?M!1|b#8k&8vh*lM|9Qn-@bj)u<E{28m!h4auO-KEroQs@;zd;>vF-qV|s=ay9>eK4Lo=`)D=OPiQR1FO**dmCJjs(Evn{;2|L7Tj%*ndM*%-9=q(PCbM0#qRlG3Akl7Vp^M(deWp1O7|3cfFdXGDRbBnp>?*CHw=!n#VSoOJ_Xg+f*eDH5s9=0j_!($C>+pAG$CD987`1pzzLf3Vd@@{TIWDmJX=mDj8<h^6~`IL;mMdM$-7e>z9;DTwGAF8xAe&cf&MIrse`Mr`pB)=M1KpO`!)%gVayX!`{Btns#Q!x%2YBI)&BcS*sG|9-T|lkMR=5_TEw}uZ2<U41(crBy6Z?&IK$BO!jKux|C(EuyNCCidJs500=0@Y_|@bkNtCgcyQFrYI>-M1URi(UN;vmo2WCNB;w~i)jdin87{W|Re(Ie6O=zS|NmEyBs(P*Dz&rSDl!Llf6sq&6VlCwpgS8iBI3bv&WiKHoRK!by2t%Op9c$zJzR9l1ycq##3mw+U=QiGkw=w_75vb9170X>F0>PYA2I=KL@;Ze~QA3&!;}G;G=piMoxI~C1*#fW70M#V>HD1$)d`%-Lf_uy!RFmwg9i~&^5}TKS!OH#Yq-8X4%u1~#0sYfZl)#Q$w-}F;@jJHO^!X8`>f8$WvC=j(KY|Ag_~Xuv|Ahrs-%wO>Vm9qt9iDs`HDn6D8xA6a7}yu`kK4G>W3@v&kll+pz=}hDR&wXlac-Ns>=IQQU{ZGjB3HAUO=fld&6RElFw>$)#nwXtxSVP0x8WC5>j*&&zeXH)NVxx%BPUKFir}BqcGS5LgA`_{VFj2nBnskC84}fKxZ_IiS7?0xZnnMWLKo_`NnI>w-_=YzIbm$H#$)S_jdmhvvb*4T$7mm%lr#q<+pjsAO?lZ&hYA>40WWmL_9g0MFnW2{t_cNSPvg>Y3w1{#bmF-G@**_~YFZC=-VF~2<?0d$A%2UpLMu>qVHF1LgEmv!?ZND{u`@NeZWaR`{OSo0b+a<kqY=qH^cBhr;%ho^tu_BHW*j1lor%G2uVr1kM)_|D&?{lC;DCT{6|!`>c;BK6rxY9OYrZlQ8eCGw`Ob$`OHtr;D7?zMo=X-B7G15hIQ<yvwGT{oI;Ilg$J5B=I3P@#Q_FIFNIpxZI}TQZAA?(8CPmMPnT>KYWUx~3S53N8=HhQVe{`!zlSP<=0{l6ie8?8YB-4Ny7E#l6Xe&q>H-d+=P<0rC%{X@fi>{Yi6-V-T4ElrlE5kSO1XwDf5vAMJ7Gc$%Ut)?_kHBIr#yR9CBOoH4#(GgjFG83g=w!N=lI^Vd`~!?+9oi~_^s)nvN~K3Ym!x|okLY&roWfiMSBRf?zqF8nv0-Bc0Q7yjDiX%Yxdmp;&cXDHFN!p>()>q9ZRsmw5KcManigj;B!n}>&g^c1<Uy`sDm##jo`;Ud7;$TpXS@|{QbyAlVBf&=9gA=Ucl4`axH!q~sa&PPvb;Q!S&ObFkEKBTm<!B}JAD<o#`S8zJZ`oS9Z<of+P$GX0FH7-nPuTL#`iw&)qVRT3zK0!19UrnE}s5TTJ}rM^(GV1CVN*0+syqiqXcFPW?6x6M?$V)rXD^3qPdI|9?^tOenGiQw_VRt84S2!vLrZu3p}coUE}Jc=*7I@x=5b-K@G>MRu;5xWpYfVqj-}H8-c$H-7aBhj0lT1+HE)tzJODoqrzvvz+B}i^xk<`D*L!!7vX?9+g@uSwEs2k8X<K6psz!ZiIKf27wRdVbqXdm5G9b$YQv_DzY<<Q@>VP{lH)hSIYFCn9yrZ7rrEk=f8fALT?Y{w#$+Vw!}JvamCbM=PvENX<lgNW4Me@Y^+g1G&O5D^!+sW3?Gf`$(s@|9i~<<Anm1~8i>|}sfOBm+N(hs(P)lk$U>@LkCG;dT{^=q>ZXU(wY$eTN<byrvVysh5PzQLH5%f%mwKh}n1ftz0bCXwqzLpYBI~nW)FWj6Npp12v!a7MG17Xg_&A>JBoDMuZ3c7r2oea5bWLF5134CTEIv?(xQFF5ns$Nx68W<R4xY&huh*nxVRgLrXHf+;oAY?%=r`Lst^h5-ZSG)SA!EeD_=!=z~CA`=5BJ4JLiDD?Gzsk%Aj-7jHN&)fou0SX+Z2|JUIA*p_UWHzGoYO4zJ_LiB);UuYLrm4gFCrtbJD7v^Ui8QmvZQ1&n14$6axrN?i0A>|%fp2X4L4Ca1ZMIT8H?L?+-kDEJl4$<oY^ylW*m-L8>y<lrAVsR>sX*(XLFZr0;)5tra+=|p?(h1n5Div>ntOCW@Vk)arXPbvZ+$@b(TccuZGEVk}k*5Lh0?8alu#k;|Blr2j74Et=UGa{`TiDzyAE+zlQVgKSy>349r`tz~8_B2c4J~qR<b`8fS3r1aRXVz5X#gvcXk%Mznwt^(RUAbexA2xL|+$^V_$7d4mEQeI1iizkU1l`|lehc|6nOHu6FD3-<hr$#*E5@6)qr)+9*1JXLz03x{mVZh*9-LE@amF@vP$wGB=pMp-)Ua4v?eIX@=0j#nEUB8OmafcN|G#Y1if_$nF7&X&gyp?2qR%#S$aQ7(U2<eO?;k2^KduE1MArsqGgss^UK_QNQGAt2tEjbo|uqgQYp^^RgZobjjc!wX||izJgc;M{%CKmGp8Z$JIo-jZ$5L&;}cY~~z-Z)qN1IE3Sp56e1M@(s&s=YY=C695$YDr@#Av0ChMl^)-QRBI!9h-za7iKdq#B25ow8=vy?c`5|w<H6!`Et)nK)pMST&j!KtU9SVP$ed-4x2q5?$-bxfc9Wlv(;N6LcyN#YQky50@c`lL=-TbpB6aoAdjwtmHqZz2-G5B?jNq{3M8t`WH`y>|+Z?1$54c=1W&)`L)Nu#=nQ#$q7b&y@GE*<9*?3Db1vG2bsLj1y6i&ue9AjE-bg~OsB)}iLT@*G(G3_`!kRh(Eq#AFrah0@dWT}BE$-GlGV%1|3xP*T7OgVs_`mhSxv(aDQO?3DG3+v3wy^0Hybedubd{lU22btTFsaEN)x~^oI04bJLMA_7rHoiycZoq$$TnA*z6(<>92o-BY{tez|SctSEZ+`5C#znFD?u$Bv<^X*pVePR0NTg7ll*})^U1iVX$X?-8WQ#A@{&DqcpuZY91aYIstIKlm+YYG~;o_Vewk>^I*~r>Bq@-xx%pOQ$k)qdh1dH&J%{HR6R?5V_`)wae3!*g#zNBUgKH~<uMxp9GT7oec*$^)pjND?Io@Y4qM4MLpxW`XHk>P`IZ}<iJM_`@*=#SwDt|5C_ZT}M2Wh)eWF3Hdkf<Q6RQ;c>B(C$U9c=*ChhTSAw2b4U*Xu%i8Z)J*o@m3Gr8o=5{V@|$cpRV!PGBdQw)KKIMg92OSEuNr_|FthaZ~w8~{(pS`{>L}t_P?dBO=L-QpK)k_!0~{%Eb%)m7jKwS%2~;7xf7U;y3WY2@fvXqt`LAE)4(kMEBY{{s_eJNsZc564z#yb&NnlS*>usZ`2tVVaY<+Z0LO?3p3_x65yUXnOq?upx%4qj%8!jVii+d{VhVhgX)cMlQ`4=0d?DvGva7bB)s(><%-kD0l9O`&z)eW~nPUq*BH{uik)*?VPgkBk3(ZJOi%|fND0wJ%0k#V<o{qPf<kY4<##sWpM2HabrQRSyxVOvkqb#V~>*gO`(rNK2yEci+?XyMmm2G$hX|+$XkIq1Aq~i8?37)fAsW93PemJlBqf%klyKvR~FWP7o7lDXo#N-gnCfWttvCqSVCm>sfPxo4Cl$v{*&gH5n@`dj=^e+AW=nDBYHmYMa$=p1L_n<|fgDdW2xXlMYPmX6DO0qMVHLW*<2qmg94Qz@^A|AX_peGSJd6iB~Ow8n2yxK30BZ|!mfI#Y)aR-k1^y&CRr~iAuK<^UMEfq4VA`hm*gL6^jH9R`j?+TOk7~D+QZul{*l(1h#r}z2vuJS*;%~_=lGKI~{#dXtrEi(lDBeqYJ%(l;p;VzD5Ep4W<kXEZr1Cs#=spaik5oZkfhli36@;gVJ_LZH(HJNC;UGqf|840?ACdj(Q(Z3KEMwz;U#9OBawOQ$MUFOtB`s=7U!#!veBNNvr{Poms%t6xibz}ftJ`Ov+gsdP+`AJrEUzwdE$YE>ZhGknWfS8~7EVZG@O!MGhEx_TxPfy-ZO#>5#>_MjFaj1R>rMfQ>5ELfOlX{dv_AJ_8l&V4ym!a>0KDUQ?bdvD`Ci`Z1yYo=K6_F|0D#a*bga`==v>1bDpm(>S-%mU0k)eQ|19kzn#~dl5CWM;2?M)Uk_a|YNv~>0m2sbh&AQNJdiaT1^F(-N9!Ilc@Fh6b*B?A1r(Q-<I?{r1suJXKG<y)S(P!LOpAb?K#!&Nk$lPtaGP5&mWi`x*H6kd`*H1^HVx)4f^7xb*!<Dc`QQYq*-*V@d2Ff}H!+(Uj%yF$!M4R_1>4?0~yfM?<N$gDJ!Y%?>&TwR#DQs3-C+9kgzH%)D_DqQz!m6#_tw9<eGmwMJS{&;ZgcG`K*39ibADG7M%-3sq&BsaYfumbKiuVbku43MDXzrS!1U6yl#2ol*c{!X;!pYvVC=Y-#JDi4%pMPo>GS1|x!Lyj+@kI4gIc>I>}3bm0N0#U5$L-_I0ZyJGNInwT+4^$XoWsheVkYl+Sj_LanYJu{^^F!j$B2rw_pFqLPDLX$WQYox^O>7cIWiwGE{bnTY=ErE5p*=$qF#9X4E*Chw9!-+v-!tg3o3@9lst5P&I6v*@u?Ev`2qv;^$XNeMC{nZ*8)|~ZJQ8X0LSC1?)I;Sd9V}0sIEZK-Xn;(ax9UBLA3F^OV~CbhiY)~}XquG8F^6j^QIokgH%a?|g~-_CGn!VKJR!N#!VG(t)3NbfoDYb?ik+L7p9UO-5^Ryi<crljsG@*r%9Y|%n0|^G=S)1PEAotVMpYb1#pNtylVykao8|86z0a+NdeR!>S5kk7*TW5aWEV7+DEP0@C{vPREA1s%2H}zz$;R29%P})kN}8shNvV$pweRyF)gI>x19bKZ$CfH?d#r#WI_!CDeFj1G3TPiUS9T^LsalRaIv8o2kQ50hAt`xW0F6h^wKA!BvE9L|0k-eyFH@}_Wa(B?dU=U1m-cX%GPqJNF&YE)-i>A_j%u!nkjKMb^hbn~h?d_$w_@w`rW(D>sx1mQ1jH|wEqo}XGlRd*oRFM_(<Y}hhCl%YK#bC%qT<vHMblY;K4@9u17B7{5w`POeX^cYu^FVjK9#OpW?ec2JajgATH?ePLnV->FuUH;el}cuA!AJlpB`l;nzNV|K3rsK$y5YoGdscipK;%G9%)%*lvv3V)v8X<WSGFFC@WRvs$}kq<LKxY<-<979GsIHFo|t;zyHgs%wN10l~99LJ_4>HLXIc2iw4qei)?{`Y#*Y+YFs6a2R{I%T$YE*(YVVEkyIHy&`gf0Ni$YU3+JInx=X2@p^(&r_yz))yr(xU5MEZP@(<&=lRkr(zqE;IG_V>?mbbz6sG7Ga>7Oc~X2IR|&{+p#=q~E2{BJ@Fw|CDEOTaCw(RA9Z)RQKCP`ank0~GN3r_5nTgx1;4gD^PK7E|Q;Rz{z0<1NSqL>Q4!18{U#Y-!+tR-&EdvdVCQ+yYKl8z|HkUscy`uy{5tVb9iJv?|-GIL=58PsXfB-skA>J#YXj99%xRrB5zMy=Os89bApYprY=GfFjAcZ<CP8x;*`~AD+xe20eLXNr*~COhLr&FJZ3^BJKyk>3$I&<*8<4E{PQYK2o8hr?l=m(iF}xbiFWSCVJ8Ht;^lR`%OIvoMV8RjvCxj@{%OVP0L;KBT#8h|9^aa&7)!6i%8%(;u3c$!Dp<SjlvLmNAgqW{BJ@SZAzL2V$*bMbZhV6w^0u2Pf<uM>YOG~{{Fxs!OWy)o=F8B*SUz7gyQ;)I(F!wyxe8~U9Oi8s;j~}`3$?;@HXZjIRZ7h>SejhL?D=x${@Y`N6yhs)jO2=Fb+X~f*w+GiAz6dsweOY4Ny&TFyl3S$k#N2BDh=Wp}ftmSYY-1F1>bn+zNhn(tH>=W~C;DKpDm;!oZGPw-}F;@w@8vNd?PbaLKKJA1iG$^CNh`!#?iZ_+MB6^bJK7CuY;W)#1s9Q9q;LyHqg%#2MrZ`NwVC=&{<N9mwv*9AL#EucdwhNO(TZZBv)61#1IL3R6JjYBpTStggSg(hUJ-T9ittp~p9*Z0on-7gW^<K@Gn~9Cxsq{t6Z!KZPiQe@@#GFhUGcn4yLxQp%7hh(l#aRLk0qD-DuI)duS5EC04h{UB%G)l54%VeAFQW9y?@%p==faJ*x*4^B#&1CkxW92J;k3Ey5&0YfX2IuPIXIrZy3dU@Bb2?bwI<I-^pb;lfZ;<*3vA~gzXS`T*K4G%}Dgdv{*EFw6v6)3x~3Pas@o2l*gV0PNr;}~2wivbUQ^@NAISsCfkh~ysn3grdyH66ItntvBF4iUx9#7ei<@=>-~%6~(EUI}vr2Lybpkfj6j?*Xx{K~ik2uldSMXvDlc%BivMd|0&<1zs;yymq%RlEspUX%@P0ehjtuULT9AB<bunZds0U4pIaVCe5j38Q^&nvt+v1U^VzLxb<aH^o*F<;8-enX>#!@)wVQWryK!Ug9KdK1Q6z+0Dq1rAF_op$uwYwMbva1+TM}Ig5cpS)ELHKGtOPWqU)tr#gRN7FP%%#PK9sc39wW|BTC$;EyAijzr+-=9(KiAjC06OMnFV7jrF36UQ$Bue3)(dQnH;jpMQXntV7#BkY0AcQP?DnUo^f~@`!E+&ne7RaE17J_e%>I7#lWL06^cTt0G~XoLgYl>>NzL_@YQ7E6sm&)Rw*?2H}(wu4!=wLqa%1?9A>KNFL-GrWO3j=y~XPj1jjsZpK^DCS^1=K{6!q`Hn@nf;;-vFkGBu_f&?yjdbUV>3{$Q?XM<}r9k{>^q}YffygzkR|Dp8vxVq@3MSR=4dnrFlt{}g3#T!@_j#}G+aFn&4D%VF+wpVp^pBdOUvjQDnTR&oyE@or?uQvAFk3Lo3Vb^fat$-}@Bt9bWu)+kCUo)(%3ZqcdX~yyzy*^f!SP$*QLXG6S7t;n<_*_H^3)G%h*h<+puMOmVXTkhO)_i*{(7(^F|ZPb#)z<JBiM$+;0rkQIVyYx49pdALhqf2rLvFvbrBAzv+cE36Z>D|t`SlP0Q!16dO#z4Q!dm_ne_A*qVei6pVfv<8#*Pte&nrKVkF0JhI4{8;XH7faZIyy$^O8Ble!KfG>pj@V<%R_n=WO#kSB0ecyjOdjAFC-NCXk6a7uBJ^Y|>P+9T$hr1P+H8DBFVxdo^hE4mIwdy8%Rl$s=Ep_bHiz&yb7>h_&z<DV`9<mOR)&Q{VaMn2esF2*|51a*LC89~p4SZgyCPaxWDGP+F=eJv%Nb~4ycyYm=8=+0no0eqXS^f3_TY}^c76VK_u!=s?fx7NuJZANy5Aeq2tj<GuUkO7c&lweTxs*=*cz#zlLF0@0m(%PvCt%42$?CT^8dO5u=JftTgfV|q(Hw}J^V5s0Lo=1+vLZxDl-qA)cQ4GcOSD6{Xv2!m?DIlKS6$s^}EkK?Z$ISN0tI!LNbDE{zhhR|CI%kSvh^d<RMPvka2XoNgW1VYC1v6~>XnH1-Sy%@VJ>YwJxR9aYCMt)(OuiyxaodhtP1cvkx_N>#d#2Eg!!c_kRrR+NN%eZd3e@Xt?y^llH8a!{NOUgL&p{f~D>2{3EhBqoWu4k__WQuHsZ#TGmPFOBhRJl2F2~VA>Ft<t!B_a>2LJU3ua_TxY_{R5zy0~kuRs6yukrl*&yk)1BlA`)@b~ZkK}Y5VDfCmb#wlDo1Kc=BuYU}WZ1B~c5iMXu{Y?^19Va3MGT0yg{Pyi%-k`uvU&rj!Z{L3X{`-bW9uM`njeOAkhCTmc@*PU&`}8cDISE=XPnn+Q!Xcxw8zAjklXxd_%pj|IZG)4LQI?N8oQq*=&X0+$<JE?T$RXHU;Qc;)@sQgAzDkO+v*qzasPhaQ^CJ#<)XN_h`KG#U;f6tjt-#2A`zHpsz$9)n{xRxQNhpEOVGO!;QDuYIpcutCslUMz^r$Lj-?8?(e)6q{InnSz0)$@rKx9AJj8J|bUR<knV3G~`v2;KE{>yJa{o0<<?I@2mg2VXi?9!P^1%Pi~Wi=qBY>VZp67SoPYRx$hM<?Dnnz)KsH{IbjJ{3XmBn!^;gT>`4H*GAd7z>rP4N~m8E(&J(I?G9KEQ9a_Yz^nPOY(g3-oUTGQ+qTwZIV<S1VqK7!?;_BG=d=g)s7KF8|Z^Y1V5&GM#orEE#kz+YizvJ+Z?3)54c$}6ayIvvqNUM1-FaT?*R#~mx67)BAKw7wQAJh-YyD$W8#o8TQ|Dyh2#{VrQI$Ha-&dr93DtK*H%)Ex7ZI$8a1-iz?5V@FB|bJ9$etz`9(S9uzc#nDoEPKC}20y;R7sKG%xomE=<zEitz$aJ&zr_ZcC=RPru5=l4Sy1TUKagGiuuS9;Leh|3z{gkSSMGXLuo$#~x`tc%NZ?(~cARu^Sq0#pb&&>JadQK!*g&!~P@fLvd0vr}TD}4SgdihBKTk8e;p$)vJO2YNRH_jUKNqOYLtvr21crb8^_W^lfD$YvYhgrQ@bE!4+0Zn~q=+Ub5MMnwDUhkb1xEL&ZY0<_2u?7C!Zi8|WH^V)|$a#$aT_(P%Joi`{>ovD6d8TJhr^KLxdm4|>4i7w8{>@&ThihQqgp7iN+HOI(+&{_MFVL!XHVV?|grmZ@%E05-qX1zS64#~j;DqHjPTB#ah(Vf<Dm1Q>7i&;$akZ8YZO3-;+6JuWjtt4ugWDl(|sRo>zWHu_)t^7Hl|+wK3y_wRpvGj9J|>e@u|MfVwpz6u-<h|3bc!&3Z31R53hoDR%JxoG6qc>O&FR|w#dX<(NB6@8devG?2KRHzhj2ih_#r?HvFY`W-<e}Vq#xFj?HU_kwWH#%MA6G049&BV#-nM)tjr2N=;qp0>S;Jd(QnP(GncWSy7kT2xCM$*<6w3_O=gPD6{M{-imAGisrKXdHNN3>y}(voyo@9E0ZXQ3I1X))^R5z`MPF2HsnBGvIWlU&)<$2d!1m*^Wp8rB;`2={h5ev}1udpZ8YOFAt+6WHcvx$V1j9&%a=ifx}HHJyRhNFnd>5<F+KQoXewv~ylcNEOJgcj2n}U$oIGh6B;!h{++CO0?_1WBZ5+Pe67epYFB1C^h#qm&?Ue<O|<#=w15#(G~JbcT^*6lDT;f??G!z2UpxlZ<`N(o*B;?pJZn;^gZ$Q4JE2E4Z7TwEIfFnK&vBk@+u9Um`2L8CbnN3M{Aqa6@k<-BMuys>C^FtPFwkYf!-yiTdI##wIfX22j`;5Yj||5-xVh75yP2Y-tc2sfMLIiPD}OaUFCmx_q0lPWeS^@Yxbu1T4o6PM{J)cH*KF4!_6Vh65UL^AuWQN1||d0XUn_7qPhm;A08@6$nPBG-&b}H*JPsYcFh+>k0j^{njmXJNB=@x7-i}X%5j|=)MlltfSFStNwuSt4fmi?j7(gg@YhqjF$bmC*O37v{5b6R60$lg<tJIuePwov9fz%n8<uUk0AhaPv($zrGtGm4wE%|$KRtP$HVsS|Y6_V^$f2epQ~<xUMNpVDPwG(y*|TVWQK||-T!w52`rIDo(MiS&nCzS3?al-JJ0erG1B+1`2@w($XfXy4qF&EKnN`J6j|>I$9Iy+pJ?2PgH6hgG-E^{$xjzZBBzLoiK)8`H0hthsRNT?LjXB8+54KeBhWT-mC=uY_jh0gye5ct8ca`VmD&O+Ng@RZ*1Oar?AFiV5oMh=eZ~8Z3UEDs)q@I%mqOl!^mYYy2zn~S?9{-#dl}bU!xz@cFgsCx+<sR~D+H7K8YPeh0*3fA#0z3=9^`_saayyrXMyv}{SIVYcNW0`0<)*1kR)y<c#Sio3h7KJN;Zo0f#vc!k-A<D4Il)!=FeP1Zy<6d3jpU{m0#?Ai=5;Ipg#i+D{P!0wqRVnl5J4ha#@~t7Q*^$o_?+-NPUV5JtY{30?kWZVY{>B?^f7q=43FP3UZFN}LwAZ*eF#53`b{G+EJxZM^nnT^tnBd&19B`k!!dndLM@;p`;a)ah!ofKCs2oT%FfS;R0?Z~6MK(QHBJ;szZr?U`7s)1XwQ(c%>D|i%LNXvN0Vgv_Y8XMrtP6>^}&5R&QJS!tZ(%jf{AP!G8VrQiWDuahEiiOk3@RMkk_Rz^-y+72g_3@4kDTd8X!~Vt$L5*#|DPM7^3Br8csoHnkHp&%;B0!)Vr?DP0~JK6*4yYjHZ<)Pe`t`FvH$Fb?j#s=L4d!VnZnArvXQy1Y4vr`C|1Xst9YEDyaArrk`TQInyNSIzJ<wQ58p0%{mL&WZ5D9X1Tk1?{ll6p0vjJmDC^N^>D);*#(Uy3jS*}il3y|N_z>GK@KHGvT?TOa?H$>l3wg*QtG2Y?fX0^z{k150G++Uu~UoNbt|BV4tpM3pFyX+0@}yTl?_iws+J><4o2E0Bt-&BNJ<_TK;w~ftxRfO?4t1MtL=OG%T#MKS-O>!US6WhrLEzmx~`OAjK)B{cca;fqnc~l=JBu>{So0LqUCqct=N&hiBT`J>b3$70rAUaXCMmc%;2vxCnRU#w8<%fAy7a85TkUcs5mu4(R3D|4_cP^z?an!n(aJSpRDIpYzFPFPo?XYS(gq051kF3mN@anPzmHI%x>z_FkF10j!g)k9%Ut(vzQh>Tx4p=R0L%+JHh*(ao=>Y!?MUIv63gMRh^#6Fo8``R;tQX$=nym(a|r;hja2cI43n=65H&4|Cd#nzj!Yyp$4sd1YAXg98YK$4W!)`*#ZOEK15a3xI`KcegI0jEDx2VahDq+sWN(?nH*D-W~`PL&O?uMmr|ERp{ED&4FoWGPj6ZvysWZ$0F38O`V3<J(k7<Sz-shv-UipBYTo^%f2x3*1$Wy+XB~{8yQr)3zX>he-aS7o0k^D1(`mC(Pnz^W>7GIlP{8Y^Ic(#f?R*D=9c|G>o>yfw={DYiEI@<{2?YR0am9`Z4mg!r<84P|SU^rYr=<;4X^WStYcyEgYDgUK2e@ZiACa%saXNAsGG;&WHc5x?fdf$C+ValnOP^d2iqC?TI*1yJK1F>I0Y8#+-zFiGa(S9*KRlUv3~Kbqk`OhDm}+niVpQesz|#F9JjYYL%3QK40CuDjM^9bdbwnwgUg%<BXiT)S=UbP%f%ltw5IC0r^(-|wq~s+@6q=U1<Uybkoc{m#`kF_>x)+hCbHpF+QfkjwHydpsG>+t_&iUU2FWQte+ry^g)@aq<!Ed7+RGy+>TGTU5qWS%SMZ%a#Z9J0%Jg##Q7YRl58Aa?ssb21~eJ>Zq2US#IoqQ(UZFn2=j~oFRatnLVbe9P~FejBMdijr>i=C=;DDz<)g8l?Oq_h&3c+iwi;1wF+ndDl=Yx<C{X#_uTv(rNvn_Zc}>h@h4?ee%4{OqK6F>uUEJr02aj4Zau*x}t`JWj^xs#PczCWFBxw*r2ww9U+q-~r$IxO3xwVWH1A6jhv<P5V}dAs<GajDqP>WdIOokT2vPxACFJYKL|pix+c!6^Fc*;t62j**JHby6jd|8(>m^0wPzlt4d~d{mqqb2r$#4Bti{6z9D5>zYV{jo<@jh_%-6VgVi%wu=V&UL=pUR+Kx~WVv52{G%STuhD1ReDifkQ-gaDRkT$CJUq@g0w@vB<Is2|=+DQmw!!I6NA5~!<+3tel9ix44Qqo+HYy;+~y(CNc_JRr+T9MRy__oifQ}5BsyLL?|_<9<bj$5cZ<De7A{g)ScQBcr&u=8$sI7$r+`2=7Q!I7;%*@aaY>bu)aZMO%r(8d<Y;JR5%ckrtxJk-s~NRLJ&@z7T&|A(*Xz^T?eyI4UJQS3~VbbBoyWt*k^Hw5UFFjsIuz_$unIxznp5bIha#k%^Mugru-OfsP|D)yZZtCpg`>xGKc?iNO}RT9z6LaWV>q4w78V-b}km)*uK%Tdljasa}lIfX0(Ja1x_O#d3J20sS3zD$aS5i=X*ro6dGmFi8JuTzeItU>B6ZT1IqP=F`LlMmU#n4}pn!y;<B4(;to13~a`7HSD&uo>qrVA1tbtJX*!kC&dMXq&<}@dQ{Zq7fxx)D~gYo?l{$Sg*Qb&BZz7CnFjnp2m7n#VsjucRtLvd@0$^n$JJLNY<gfA4o4d;3#Z{#xEM*D|tk>gXa|BD!4-Yy!)kv42%sMD*&MH(^Zi$PR=bbYjzH%Uu03Fk(K5@I%-Q_5rbIDiPf|SgCQZDA$DeW3nUM64bw{fWb{0AJjRGyyEfykXp=IUmms;3_<YA=Tfq_iY8Wm~vU@5+e@41<#dJV`g7#OF$5J4EG<r>RfI#FL*Q){ZxY<H<Kn0U(_lEKSI7*>qmW9i5y!Uyp?%N+(m<;n7pxg0t@$`?{qF-{ZH#vwl*}FQ}X6}a>B`{ks%L;ru5^@bQ_3!}@&1IzUh$eLM3(8%(?Ru8VUBCsCrN8l8;8CsY8dqRMFXj!`Kl0QMYJ63-vY?HqDOIeG;!QGa1pa!kBr&iOhQ^4nXv5cr!{7@z^*Jhh1`Ny<YeMgxho!QQ`*jfxsI%?0Rt@`K<E{}>2LSqdJ9<DPds8mdPJ#6F7ox%HF`w0jO&d2Qynf`ZSfV4xZ-#S%HsL&QnsH3Cb;<s~fs?upVl#}%7-J_^tD7!mx{xPuRd{mm_Kadv`A7s2sBlVgk@NU0s@fywo22uwav5J69=Qdm=_<MoMjMN5`;=-VWucZ-bHF^n^Xm4OXyczQ0_5gVe9l(VEJi-qgZ{-j)r50^XBk1ygjj1c6;B}AZ8EwY5PdBroOUwUPrL9KK<Lh3ZvlLpt@JSv=4{*yT>H-Hz{8`U%eU6a5NAeqg&>*0XO6Kt_>cjRb(COG@2Zm0z`!8G#V)i%w9?wC3N3*SLhI`!3wk-dE<B_sB7nTw)i(`(D`2S9E1pM=#6m@4kKWNnFHsD|^jDb~!Lf5MO(`Ir-W3Str7b|77st%@$*a%{k8_%(u7_Yy(>iC0Vu-1l_(fy{b_a9N*kc`PN(D1)`)GP5lUY~?u{_{=dAN|F)g~&3z)Zd(V{zM#TTQ-~$GUlfGkd1cjKeW&BUSac6iM}ZzY5grZ0@p6Ks7DY6i9R~)Xza0(<?FG#w{azW@Vk)arXPbvZ+$@b(TccuZGEVk}k*5Lh0?8alu#k;|Blr2d~#3f9z5~*^W>^-|a0m5`HwTaa2?D!ml^gcLul47{X(WZMA=5xHu-Ykumg8&o)Auc@ASxaEf*4oTY8h)zcfvQdo$$z3<(4T|apnVAddfkU#~OJ`mYiF{51GkIUsX(Ms^rA4~Vs@4x)^(~klE{ri75Lw6mkXom6G`0E)iFF=5<vR;Og8pU!|si|#9wKjE!qZ98Og?1wvM0dE2Prb1mhQzrru((_YqK#!0W1#|%L6mr>CvFyavaHRPhYQwzYrVW(l0W|W?c2Y0sXN-`_BvFFv`NzXdEhs03;g`Y_Y0A}v82<`@r`W*9b~8Cg*c<=DU*?LV&gS7Uh8cRQXm7|Ea|KO%+Bl;7jD7rA{8zGB>d8Hj8`O+9<o-A8r<7O1*l9uE#ldm2Hm#PHhc?+8@G!JN-3BWhX+zKwUt!kEp~>HMvW{rFeS(us1eWN!37?kPg_4eC;lbBT?(R)5t!Ibboc;k_Ge!1^%SB*GiQkLo<UFflBqtduY!tXnE)G&l_J<V=Qh4a>2AP(kz5C4$`u(9UI^u}$HX_@XIKHSV@-YRh6W_C`R<E4kl;a}L()OR{v&lTaZ)m;^mdi4Eo0i4a{w)(PW#8ztAYM%Oy0$f9<MG-er-FXI>Cx_a@e-?ZDk{C<B(c@<EAr70#<F7j$jd9ve}B27AcsZQ@`y4r#D)212%aJpL)g(bd5r}X|x1mFtSzV(_rKl`(Qj{sc*l2|NSG>fu&jDQ&8RWpqLqcf&LL#V9S-@d-(SJbGNLhc8Tk<RcJhyWKdj>FjizW#X_#_3&3}^`oU@k?TA9(B>DzQ=)-8i7shX8Qd#j<4|3>WZKE+KU$9Tt2qc*q8uY{&=L_5bN_Y7LT=wG>{IxGXZ~w8~{(pS`{>L}t_P?dBO-xUApK(wg=XgL|miQf(1S=xYi2i;$FdGF`kzeB};18}4z$4SZEdML|Fr{+Hx5ueaDdG;ac}!09Fpb%C(Y>z%LCSGSXaK-~`UA6Sy2>Yl7^a$ull<~aAJe4#*m$F;Iwi;mvmWt@Im_Lt=~h6#kn<X84O`G^>Q4@4?u{MENjZPuCZzt%u}2kAPk>q^(qX-)D^H(=W+bM?s60hn7?ijG+l8nG$J?xFwbL?7V3#O>L88JNL<skGIewHg8k3iFT70gY&0cUD+2}mvv=lUrKAHAE1Fex#x8o&v&Ss^GL_dg`yx4|n^jz=4Rr9}Sqg66Rq*^^DhhQqvu9S=d>l2=U?8!UbYk5&>?rAQU%MHjEzTeQh^!uYL<dfS~OIVV*c@FPEtFH!E+(~bn4}P8*&sqayXEN&wZ76_ARAU;HYb#lJ@JfMZAn4>(TA(l$foIiNzc`K>Eo0t;)G;Ft9FytO@rO=><$i(QC8k@dAX4mVCVzo*QRFo|I@a$Bll7>ROi^n1F{CKlucFgjczRd)AKqW6(r1*y=H;rE>AjX2g8mWPC(2FRXT@;)G_!~;Z`l2oU8r|)3}2R3wq(OgFmSEO?;Hh^S9T89WTNeM%@;+FB<Kp7AZyb^|3Xp^XgZ!7H>k}@*U2%bJ}h()d*B{)uF(Xi6aIQ?H|C(F_&PGj&?^~sd<j`4g7TBB=)N*L#g4<)#0|@~TmUgY@mXp^lbPnhzgmF9fuEkdlaU4{jC$j&gnqBUA8X`Z)%Pe&nkV%rgX~$fzbI8@^b2=Cw}*LjlJNp2`(}8%^FaTO$Q12SU{nu5gaidzjKPDb*Yi+_P;t~FLjgSp>;i0$Ig%pewOpXNL>4mlCt;T4ZuSreH!>z56Jn8yJ6hN=Cwbw)mI~f5KW-8w0{pwta!P~mv?JiI^1NK-Tb{U35KD(3fKK|uRWzNGEWPJV|0b-9+liD^Jdr>&3fAj_Y^8$<n#Jt#&v{X)6m*<x{T)G=8WUOWA-|?_?DJB?-Ll4Cj{H9GEd1tll}>JLW`>HQ3sYAL3tdRN<QL_psZCae>t4kV^W+8%dx&tUXFcPO2ghzFTJ@aZs(hG|a<1O3@UBL3(+dGB;9m1Os_MW12|E7!3m4I4IVXr9kuBrzMC-aY-&K50_#LP6Kv`BahD3K20{}MU_!9b<JOGBrZyB#p8@Zv(!m2)mA0Pdu5g3*u?GE}tg%MWvc!mKvmYd<2zAvE`C{H{;Bn~Yi#Wnp2RH~b@^K&AVVz$$D^y*L~{bnTY=ErE5p*=&|3;QdqE*Chw9!-+v-!tg3o3@7%Km+&fI6v*@vCgh<2qv;^$XNVJC{nbv8jA76JQC@yKwg)=)bF~Hx|uq05Yar)0GTpx)q4~_w)hIh5G|)vISERvG%1T?4%bwo?oMrPlJ)_skg>^UG_5pwLUN^r8TR&qW5=gB9}tBVTc$8S4LAxV*dmR|7prSWMS9NE3B;!`{S-6KnQBMxg*eg~RdFO$b+V96mL1}6mb<I>KDQd`No$N>N&O*S4>#<QUC>yf;J-!>d{85{(z|#Mawsv9jk7(MV`iq5bSplSQXdU!-{(OiInEUZ=<F4ay$syGGyz3)*z?%>3`)io&^~UiYzaV8wH$eLFw!<5DH2dZQu4R}8jqZ7Wm5B^&iJeItncYBQ>_tO=~hyDd5JEUHcyuNlTxTG8Uyv-jb<l~YObmO#=~CpM}(7zmfu0QV$b3x*SgHA9|1T7#4ne<Gbp4pgTKz4ker3nCZ`03Kmi3njMAZ^;?xX9(^-H%Xj$R|UsgkkvGZJgvYu118MM1Tm9AT6T{;9jbT)We;=~t2C6K2uyWUHBHe7t6A4>?I9%Ut(vzQjn`gYrGpKXEsA!I)u*@XM1^GM4gqr^&{s8)4)Cc^|aMOmpTS0!^_97jjLC?C$r<KUdsfJtn#`~6>5W&Yy5sDv7{@)2+q5pq1CT{Mt(TV#u=gHlyBE|JEAAAnLW%R}X8+~tNys*E0JCdbsI8LOp*^Ux#RrPN1E=;=Xx0|89l)0-9uFRPT-hVk4<pFzxD+Qc*(SdH$c+u(Xs&HDrNPZdzJ;BI^9tb;Lh7j;$sH=%{wyXS``;Fi^BI&D_!Ns~S(-BaiR3V8if=CC6|>ul#i7#wMfDe`<PqffW-7UTjVj7X>fIJzrpi94W`=p(nRGF%|HfYa3m3bn;o)wLTeo;9S8tyIvmI?hNAPsXfB-eBbLJ#YXj99%xRrBCkR1~GMTH5P-4x+4OLB<H?OLMH3-^wWNLG9!7c7EUY)QK^V2i1_^_>{V3j?ts%>b#gz|<;Nwl0>DQqbo7+gT}PV28HTPGhRj40Xufs1dw4H&T1Q|b>h@=FOUX-;C^s#4$&Wy#IsO0f^)-)%buS`;=ZH((r39a`ZZ---=pD&Vo%6p5VYDe}7KlyLt<kN$gWpCus6Ry^wWxENMEUyziv%;1nt3J_cwFZqUJ{DyGwRr(b?I`KjW4-aKB%q=>*O=+Zo}J{f8+?%=&G0HE)#)ZPAY@+@*g=zJ5}#c=EFDy{Rw(V$t5oRpsAj~D>Ohg$-#`*^dVo<2#Vk~frs)oyJCUW^Skug<#8+c*-6(=;Fy)Vg8^k2qX+{#a@}G)PR8%5$sQFfgTW=Y0)DKt&CHMB0T27QbK`$u0nj%TRh*bj`&Nf1A4dI*g6~qr01#)8FXSJ$aihm-hjt*l7ju9WhrE{h2_WJ5IJZq*b}_0AFeyv{k*nElC9}Hz=1MmNm}yZep@tsckg~1chF?%sBLp@48gbmg>b5CZeEbxm2>v;3N5BX%NMVK=mPjc>q96{HAyK^|JFYZH9#uORqp$qiCiR1yeOEK><b<&i7>})wYB7&&cfs+F(LOjSX%0xX2Xj<lk|lh5K?Mx0Na{d*+vn7;_vqzayCxKTJ&jApEz})z(23*z%Zt<~sA)aec{e;9r4ojG0<ehS$X1~2!YT}P-)*M0+k@F@V{=h(-7E$?_|+30>Skr6M<bGZ=qr>L#MgA-T5JAY%s508I}<D2Udu<>W-0#-0eU6O6&w)otwNR#%)bZ3x&}$HvA*UjGogW6uh+iwVbxL;c)d{Z+TFrP7E2<gS!lueG1T7lcr31xq_f+&WjV?@ND)AoG^dtjfagujlIdcD)!@hA)|W}qGh$|=+^jbjuTnir^L5G*kTpoarA+`~4hrz+c=91z7?Vr`W>`c`*P-nlX)FjH&O(i03^wE31uVK=YE>M`<MGnD6zx>_CY}IGMKq$sjoKot+Ve|H5$j=Bti?Eo{A2_~#M4+Ws^}#p^v;LbmM<mSS@Zb^7|A-c{R8P`2ONb>()dN=dnJ$PcJQ3STm@H%pLf5skb$vbV+8>8eYz?V#>u$_X3fsQ^ouWwG_unCM@MbxD`F5%IpLZXXD}p$GsMp9Zh_=Mu3=iipNyV|j>i~rYvX3T6>U;RQxhaZ5})r_ge$nCUk$^>Np??V=-Wtlu9yx8P|*Hr@>mMQk46uQ4iJc3<9an<9yeQv4ya&K?cPux07r?m%(8GA<9na?>c0Jvg~>3V0lFPO7f=7FIr=5%dXtH0lfA2hZRUQMQ3A6Cv#h|kBO%u?Qx6{i(OgCfk7z<Czo6Wu+pcG+3<g{<SrQz-1s>JPu5o2X^kUv{T_jKapoUmgD+}6-ni9tPDBdK)M&PdpOA-SsVQ7p9i#CF7I1IjkQ=g;4XTZQ*5hwKCc~~m@xL+6HfI8b=Yc;X|HSQWAbpW8Rx1$F%vNz>I?UYGRe<2#L9`jjk*tDTj!s|!giX}#J{AM^OXcNu@ry0jITbJw)95|`#AVR~Kj4^g%HN5FkrVDujSA{3{ZqFz-n~y{gfeNP-7dem5qN+V&zDYU{E0^&#<B?l{nz5qmV6?Z`woj=^QWk1SO$W>aJg;uwi8lV}B0z2)#pi4#&0^$(J?LVrQ%z6@c$N|LOo+8MQ}G0%-6o^k1ku-0!f7Xi{j@ue0fg=h_7=dm*-9S+Va~?Qz%}ul4m>;xx_oP$4AEv}R|t{`eC8OdgAW-1Sw{&5Rj(>34Gau2T<k(SL@TYGs?aLvAi%y(vY?mK>%v2NA_B;(U47Hww+My`zT$c0NGwz;_UIjL^b*BTOn;S`5ga@B(v$+?>0N<PUfKfWd2!5apS%ja@HnSg>U{_XHLY`|D2AA-iC;uUV0SPF?LF4Hrc^M)wvVP~GMR;S5YYp^mxl`(8g8O;2+ZUwG8VV(xYcBRd90f!IJ0L8%{UyhHd0l8OOaHsC#*od&gL%L1XMFaO@Tz`Lj4@1F})J=ZQL@lXI9p!9cRA}ESoAdUuQ{F{c4y@C+Tt=EtKAl85ewoKW^|}fAD(y@yBKxuKL@bzx?|1fBzcKzyBQR889+$#R7l-{vUK?UXVgRHEW#0wKKqtgY^2x@W=*V-5JpWM%3RV;nZ;=QXqr<@y~DH{^bn{?DTcaPW|@n*YCe?nB?(LkK4!x-EY|QFDBoibiPl|qM4JR_41VIc`h6>D!T#Ft~H5w62}a(n%6cs2^nSixWl;^w&whp*g9Tqc!(T=y#?Oy!xs;^9pI~^C_7soKZH8Zz%f7KkVn1zVUcgD+ZJvZG}sD^+_!&X5R8lR7QFbwsDdFV-k6SKx$>i1a2*AYVnCb`sPDrIW3|d7lQ;m~eb7Js{>yJa{o3A=ZO}u_XIyON9fEIZB40R!<B|`{I+pSc%W5Zq&J+{?82T!U_9(Mj>~fVK--cA{p?L^vV+x7pmm(xh4`v&ma`bsF1SjOd;&L&XHkMV4g{sd6#q?dX1GCDUrH;3&5H87zZu0YSdIP@&5AM-lYV)Kz9w2@lUAx^{q`p4sgm(1x+dv=8cmFZnGm68K6cHyj-ekj=ZF7)9J>YW5pb6v-%wCq^BHS)gX$PdHURty9mShrW)~ZpPd%Gy0jLA60yxQnw7t%<8Kz6$*aEyZ5ad;p_Tw6&s-eTt}Y1hb715=WDr)<QtcyobE=$Frw1L&y_s~|ob{q@~MhYzr@&b-{KxG+hpDVD)Ul{a>fxh<LM6a6aeN|p(*Vp&O)&3$R(dz9`5{1?e}K&D)glHr9=u|_1|;C+UbNIUlC$8Km~6r1n9s6%KD;71bH4*QQ(3dKpu{L<T1w%(2O70yMr2!rh(SFZ;8tC2(yH+sCfED68ukm^(|&dFih(zlh3tc^ozijJGkq)}MaYdV5Oc*$m~Xj&{~g5UkNJDoQoiXHv2&9;h+sc@++-O2;!;kICu^A+|0%=>kMwwXL9`S<T*?JrjWu_<|aKI`CK9kGhrqR<pr=<+e!e|-P`$B=zsk~WYsB(tmg^`pB+XE`X+^Y|=sTjO_FaukF~%&?=fh_jCJbkUu<!X7vVin;^sdz$Yx4bK<A?&1rD9@_A;><i7-n8vQS@l}iaNi{P;o|<*EPvF4ZxK6i19E_}GBwK7|)>OqT+`VaFT}8(pT%okY{@78AXgWZJ6#0DJ)0GdG5_pZ%V${PTh7Lk9!FC}6#PK$3vhTFa66PUB9MUJ=AYQO{EaFEw&+-jF%G2UA_-syv+jfU$FWT@5N=u(4Bb*7eNdeyR5<F+KQk|q9bWvUcM3sZCA6M;5k{@lfDl<uH=u?^SHwY_8R6NSQPj~{dgYa~(B}%Bdr^y{If*@b`enan)AQCHve9FCQU`ue^=kOl1CTws7oqU)1;OD8btYJZRCbJ&ahAx>*xJ*NCwUU+tuM}uef=*tgF$>c+c-FG@i{ohIvU&iJNMf19V|+Lrf5;t>;{|$`2v4c5NpZfJC<jKS$!mCYtlt$v;}JTU&eiZ^NSwA`MW+?=^sdlg-u0-`6_tW$<yxERy@nG*|A_4qrMB!ba@^F-EUnAii@#+T>RlYem!*}B;_wm-3~=&0N7?3;ox?SmXuDnWMbVm2^(~noYaT`aLR=VS>JExeoh;C1rK|UtQy<B2qXY%_pizuWT%YjQQ@b$-g~!*CK|o>{c6<q0eT4FptmwWnJ4Khl*2E3VHbo9%e&Vy#h9>h)gMYOEhXX%7d4DAhOc+(rSz-Ty3mq!=UYY<XOqwV4C<AU%w7<Z`bGn<mpWDMcI^}QylYKM1-Fc|yh{zP}oM6;6L4*VaS}dPGkUiVb@24I0n6E_70lNU(V~zw8d4(Bhd69+8{YjW5NtHbW!i|jjmI=*3#T_l|n3tehgbcbM67u6FQ6j*`87-$Y_)e1q?kdmARlenk3k9)s2m+uqDM-JJt7tkWM;+Yi^l!qtxcyN{9To{hql~^T6Ibe-poPsI|C|?<N<qiD)^!qusWFk|9`b7{5<f3B+%0QI<}?KWo`v5suhL(x&CJktbYbdBxuXkdm;9pKG_}d9aNVn1V4mEdtPc?`^{i)X(%{(bq_mzBT$K+~((~2372efA3)mrG1>9?1$HFZbAVJ4}f8ip!EawCfB(i1vooKxP=evr}3A^A_9w^I-#*pZ)VgSI68ec*mlLx@?_$}iVY9lxFVi*Tp`0>$i8i8Rs((a(&4FXi={s5{RH^VV~UqUTVo_Kyp99l$*Yx)zYpEqUa=R_)nHM594gQ$ugilpC+#NGTD4KuW7ND*Rxh1KN(hgT_Vux$3La)+6=hpMp!_w6`8?dP$6vu_9{vTev%4M!+av@#P)1jRfO>G?ojm%h~Ry1l!ZI&l!uJkS7{GH=y;6hAf|3&s#Fr(_2PeOQ{5#W9C#DpAj=HaAK8fMto;<TIL9nmi%7(!vaT)5Eb3Rh$oq!itStn4bn5g%WI$#^j6DOQa%*XQ~(CQ<#2=8Rtw(r0a8xbVgMwMYX0ZWRqow_?zYK>b=jchI-P9!&g#&h}Xjndt?_h3WfWx(I{GwVk^D3_#k5tBiT6Hb2(;aN=XmpGb#1ap!R(pl$+yRIeQ+w!m-1G+bt)chz@rfTc1H+xdPh9&6SM`NUD}2j}AuKCL~LSOGru{7eM2YbFEBjUQ|DS^~3c&{bj1Phb!GmN-r<b<<geUQWaCmr$u9+-n-H4#8J&PP2zaii~fjk64CNI=vM5c+(cxTS#?POhk*FyvZDuubY}3^nG=$;aN6XQ;s_|90EkgKR8*>#p=de_&<8DRqv6YH2t;<Ct54P&kSIBaJ%D^JUAN4-bO?CpZ1BKVyU3<WAWva-y~FivxcEZVmJmKY%1Sh6F)f^R6StdD+ckni$bLMs3HMFsk(Nb9iIqH2O-%hvh6!wnvQky9O6I;ej*fm&KAe-s!8xe`lh|hW`@gKp{Kb1w2{l-Q5X4nP$nk`B(Lma5$sI6|?L$;%iEAeD;0K_T%TRty=$&f0A(ASi2b#$-6)Hw4LE${~NOvi9HxmL|5Z^!mllSzZ**r(RO3`l^&z<xc#QddAOrwF-=()NLu1D3pYeD~10W}NmwujC-7(;haSLJ^bTDZM?epmu-S&gRCW~H7q>4VZeg&v@Q*FR+rJ0i5sb{>Smk+!rN&$lxAbQ^C$XDPyngc^XOyQ0Fm16qmhcFQWm1#$~GU2ULHTYObryTRhww1hodgVCyNtKv8#IXoG&B6-`B!}q`esBm!k<d#0UAc>L%F?Db?7K4hqBLa#f=e|usChPL_(|&j|BN^1CktHE26)^=7zrTdNI!HPn0H?d^FMq1{kV|3(fR9w@=qatcjx>cc3|%h_nTgiaeCu-e@LuTuj=)CLgV5lXl9wcrlUnYQAAw49`v2qWYaR{jUPJ=V5tq12K`vw6Y!rsjJCdI|=YJEzXj9TG5Syl3qg#6izm4+v_C;|YAbyoZ`TGNl<nxl6`LqZi<b;ZNNhq$*sAGqQs>@xr<K*hupt>rolh3fb4R2%q5koBPQ1!ChWg-yFNo9~;{v+pTr|KQbd>DtIKS2*Exx}R(G}Tk|`j#Pc!oiH!^dVo<2#Vn5g@^JsyJCUW^Skug<#8+c*-0-_;Fy(qmH}lLqX+{#a@}G)PR8%5^&b^1gTW=Y0)DKt&CHMB0T27QbK`%FSsL9Qw=$ddtqxB<jQSY`-=&HHAkH9P$Uko5Mvv7F?Lc-f<^U@Wc`fx5K*IBJZkxL7G*%m6QkViFSF`;>W_A6|m2L<y)1p*D4L!agWm~@uzo4o{2x|B>;<$s=15~j1_$fpY{BzolfDvMl!VEPmky3_4K^!VWqB>Z1TxpOzs`gVxU-`F9>IXUdu4dZF31ep<9$O#PVjkJ<g5w>deQ;9J9FXi6<fy<TOZfJJ3K&|E)PeZ6&#7PU(aXDbO(^(!8kde+sQYK26UY6R7pYND(|WM;Zg@CKB@FolU=hKQtw7m@RT%2N+e~e@2eZ@0mZ!YW8$Cqhub%KwH!CAO8j;*XU!lApzNQ1$TJ!H>#v!8EnON!eT0Y7)OZjgI&?{lC;DCT{6|!_-{yiYpHAsq$^)+9a2@TW`zV@9DtCpg`>xGKf?iNO}SQ0VKLQlSrq4rkHV{w%vo!!PQ%TdljiU7i-IkhYUJa1x_Ocxuh20sS3zD$aq5i=VcO9d}YE?%XY80PDgBOq&#fJ<9~!5kFe&++6#wlF4{2F$RCnyy0=EYfBSJe-9Z!x(JFxeHiyz0|5WlE>qvbGfxfQ;{;-#1mkth(?sSQCoyndwz*2VjZoDwHW7+pNxQrcpB?P6}_Z{-uW=w@}*=uYd-$~BUy(gU?9EhfTOTw62EACujCQk4xUq(tKbUp^X``xGB7r5tN?(%Pgh04I61e#tl2r3e(^<-Mpl~t=%_7yMGV3zCtTCw42FbohS-_iEs#9OHB2k`lhO0g@fag6{pB{^iZ&^usR@!HiO+W|!WG=nuZH2`B)g|FbaA6QS4;;4C}@8*c`OCuN23Qt2M9#2alINakDDz-2UIYrc5f&TfTKiOW?49m@x9M`b>Dv2`z*zL2IzMDTs-}w=IEE4>rE!2P4=!1wwe23MhVOo%(4RCj)YvpOg(%6L~|J_JfaDm{DN|qZo8hPG8k~dWJz%R7I;)EyT+9n(TjP*b&)*vgBoI0t!yOSyAsCwDBdK)M&PdpOA-SsVQ7p9i&fQh90p&&sn1d2Ghkq@h!cA6JS>%c+^>spK%H%`wVK%f8h4G5Isnku+tC9W*_(2qcFLruzhIK>uhF-BRvR{L=#=pKk+))rksQAn&I#It^T27wG0oN``vV6~>N<$fFeYP+omdTTx|Hccp1@V%$-Ub%imj(35k#QEDaA$3<Flx0kC<<g&cn)Oe9d^|7NBOV=sFnfEw=4bYLb+NT2j*i^8nAQ+jpXkf4T^en@90ETS>DR`Ct#a80%CM)B&Dl1U(aCt<6+CfoQkM=r%$0wUlt$$zVV2&SL<fJA=Ii@NKrz$3U2~aWimDJf{N>kAg1WS|>xa8QB$rWCEW##_Hfh20+$Pf<e`*N=gF*gA5nD&<@c`Yo{u-3OWd|uahk3<@CDnke-MD@@iM#H25uop@Oe?9yt;Vm5M!jM;pCFF%;8ZWo87&&b>6HfOvXWAe5K30C`><GutPxLN7edX_k5)f<aB|oGFSSrfT9BkrCJ(%t3pPb*?ED%&_gF>6uJsVI4&DfbZquLWYK$s2l<_`HGCiZ98r?SzjLO<_XU1nL;xT$E=N1)!$Mi)$0i>P_MJO%QgYk%urJx(Ya7R2Wd>N#C#jKjO>|}b!x}i?*q%GO3l|<5>>w%Ceul}97hYKw`0ZyU*V4%{MR46PCx$GrGT;>p@6>I;Ge#3=@RtukF~zuR6iQrQey~@F}BtIi9u2+7Jzelw80Z6aqb9Mvux7w;#@~bkmxdI6vO**lwLC_GKm8e)Cc|3@4x)^(~r;m{ri7jgC44);$k!V3BIMNF5zsAOFk^?SnM(^s|}N$q1*zX<|@ltDECn8a+N{ahE(e^cX0e7$Vw4d*1SIRudeUvDdcD&PFaD)<#G*eEUOp`)n^Qv!aF%|vksFbSGKDVF3E~+@*n^F_U&K03q<?WUWa;)HcwjV4m`YVji3Mcel611kn{>VzJ_g}gFsZg6K6CzW!f-KY`n>aG27-Kr7XbZl5Pb+*UWBj;Ue5FQi}qBw=XrucuO*oAZyjA&AnYzD9MD*BJ#Yc#cexn1Fe8!al5GSk-|Q4cp!;VTS+zEVs95|*T_->Q-Z948u2XNT;LM=1oPvI;$QOHr6A83A%xvThYzrJedgs}Phl@K$A!4*8Ay~bnd+qaDt$<n3Gl{P(SV&DZsU8D?gso9$#p=cT+#O6g;23ZOi|-~hFtv}zv*K)G<1N?cVE<jt_}iplDHZ6AL)3Blal$Rx2tSU856vmt!Ghc+CQ#d4fIz*%~{y!@#?ZP)wV;bm#a7@hiyyWRyMLW4yn2~ZaNbWV0B^X2o~Wbo6S^dIe`fe_1iwMZ=*Fw&FUqg<{3B8H425H(GrZo$W}v7gOOY8Wbq8AzWw_B_m5}?7Ey&yK^@M6wq^JQ`bS_X?C6i-2=4jkZdv*364zy`rFbsMpqWmfnCK}+I|Z1jR!3LupdIm<n}q8?v3nRT_`>+DOw=mg>Os&PtZg*r<O}xc8r35+Lxb`+V`qUIK#3`zK+Jxeg1`3V=j}hX+y9U6-~ae#-2S)JwTX$u?lTS=;T#W$%M!oC(p82jrD@&lmOFvjD1D0j8c(Z!aD@OQnFeP0U(tst6)wI#PK8PlccATGa!Q72%%+R(UKOZJj!QxV060d(fts%Ji6DllX5u6h{L;rXDL*#eD5@g~a<{C@dt%OVcWSy7kT2xCMgqbXw3<qhgPD6{M{-imAGisrKXdFdMRX3JYKU}L@9E0ZXQ3I1X)$U<5o-nIF2HsnQo!*xYXa=F%o5loT3wJ*@CFgWy<LtU<=n&MC7l+Z)n@Yy+*UL+U)hFNP#^kag8mG&MvBsom*6>@m1+n5piuI%7^<doy$e^(|Dugn2?~+A@|YZg*+jdhF-oCNcmlGk?sTuEMya`{>0B-hAYb@?L+{e>kFJnULsv~*N#^D`ya%n58eDNF!)-qJd2&1x@z2g=*4Nq4>XN9&G_WZuiFoizfwmp!<W-uLuzLSzeOJFYj&3aD$b-}|;|?72>C^FtPK)Gzf!-yiTdMU@JZL6VfpbyhH9R`j?+TOkNRCYVY4|ZD6Wgz%(;j$wSNR{_38>O3l)~oa`jhFsmKlQn5!)w9X4_}QaHBJ`+$?Xo{gz#*cX13~mR2@T!%Hx*qRH<ZrHog04%cL&?RL!<MPwxC3Ys8ms6_ulQn_b3o*O-=%}Q6aF{eH(bdY7>9(1mz1g8`JdTKZ3pnCW^GRM#>8FqXLS<Qg*ldR~zGCM_(!`8$N%eGtqF+cHHYD1Hm=E1*OfWv{Gp1kLf1}2Qk;H=nvuazIG*<N+>C`_6s^(cevS+u_>Rb_Pic0ad=d32KT0w()rc)RmZ;SiB2+D*Wy^MMEn3bYu5XP|etq2EtC>XD&<o&$CPw#OWa2J)&a&;}w4nfsG4OIkX62!tCM6Oak9NW~p3?3k0h@L)>?b(kMFi4p<+-Do+b!FL)5a94R=uJSEUTqua8Ll8hG{oyK_&PkTu^QM0j*2V1^N@|lxAR49Rb?LNHtORXc_W0+#s8k9%&b3aAAWV&kEccLKQ{nV^so`!}i!MhfA9xmi8@Wo)wKg+D@6d&*D<yy~q+Rlha?{i%tHO1!R*89XgW5bqxYV<r@yCN>x09E8PH<H|OiANb?^bwMBf05?fE94Bc^&m{V1NW2|NVuF=(3y>M3Bgq@pq#2$D8jeJ}3N+Q+c2)D;h(hyNUq-8*+RJeM}wz!{fJ%SE!BL&`@DjAHt81e$xmH%aL{meW1b!D|<Y{fE>%sa7^EqPz#hNo*xp27Lnqb{sd~uP1*T5kxDTe-#W^2D3X3N5_j`sG|bSRA(e#v6;_uE9A1wm$@1?R^w>??LrIl^`*xh4_VZW|);9zb**0XXe<c(tT8j;3b7CHe^g$r6OJC}D-SXT_oj8bS9%z6}nYZdaiXWSC1!IVoQ|gff%~YC{#W9C#Dp4P%HaAK8fQ87|<TIL9nmi%7(!vaTBfzmYQ=AWo!ivpJn4bn5g%WI$#^j6DU!x)tXDa&PQ<#2=8Rtx2qjxPF>5Qs4lIky6$R^7U@i)ue)q9^?4fUio#;>IQ5U+<D_Q)=1EK%@ZqX#~y5nJi~wg=&o7|F)jp35;aQ%d>@pGm2Y2DR_=pk^HB3IlZZ3dgPkZU>owB0B7OY<&jJ;R<LUH&=@HlT<B79vzIdO-PCal#rA>E`Y`(=USQ6yr>BN>JjUE`pZ;nnO3@$lwMw<%cX6OrBbAn6pO|{y?3M8iKCipI=%6*7yS|8B%<Ya(5={AxCyH+v+5iG4gvAYWtR&I>CE7-Gbbcx;k3yqjUiA#0T82fsHiwKL(y~=pbuJ>_`sLd5KZhnSD&osRBQ%muTQ1xmRXk$0S}!Go|ZWA#ZU?4Da@{SeVz>$Unsp2!ly@BiRLV(g|iOZc7tYH%6<shk4HA)zUe&DvdAd0k|(NFou0`sflX0Xs>)T#+!x2u(J#t}bMiPiCpBOa+w6Y-msOd+crPlU2CaMqTt$Q&PiPknq}>+TVmh8wSdFWs@!$ubl*{r^IU0AlA(ASi2b#$-HEG6bY2iHdNOvi9{1TFS5Z^!mllSzd1;WcJg|J~fchYAN^OrU;jRsbu59v0z9#wNC|Nf~0Y8KpW51n-|hVG)S%Ks*`aC`Usums$)8cnCoN<C@P2c>%oJwO4kf65$oL};DuJP3m$Z81fjZ)No9Hr|3<K!gzqH2_C<Mb&Qyv=SZPmQ{ue<Q8zc+CZVU_^P^ggT=FH3468%qgB~f#c@V*crs>1@>U>+?|}nQ;o$PgEq!tiH;Ac&tFahV)EyB}BsuqO5;9qrr=Rx2lNrflwQyodh)P9FLB#JbVXqE7a1VgfUG-c))sM#|u>!zHDs=Re)?G)M!Wo9H7lzD4yJo(1xqEmo^h8HsBkId%a7)Qck|;MVcgc@Hr8)io@%1&2hIKC@f#--z+@%Dcv2HdBL+BmJPo49>31PG;X%>i0)2-31y@TIIIjBEHA+@M;nnd~g1B(PRlbU%Z6?k0dB3=@T>oe-up~>iSmn|x}UOuR<3hU%E>~6!`n1AF5)aa_0<t`I}U`{H7^zt7$M>|#TQ0Bup1pNtmNXaEG{h+Cyz$-LBHOaw@*YqJ@(+G;-hJJ_gHoIbh)$_ab+U0R8_}NK+PT-i8`gj3l7^4USJ96D(JWj^%svRB`EQ7%%w*r2ww9U+q-~kW&xO3xwVFA!L6jhv<P5V}dCm%-rjDqh{#Q+dzkT2vPw{fG#YKL|pyBBkS6^Fc*`UxQ6`8c;tU3TB94KOK80g<cOa3!<4{^m+I1ej@2DxroR-;lDc--cgMRU-s7{2FoG!Rm`CSbY2xq6q#uZAZWeF-T#C8kR^YL!uxKl_61G9XqZxNFG&t45P37+a~pcoPAd_?c{{97Z{JNk7_ZGY<I!&j?q3iDQON!b_jD+V3H+#dqD*Ztw`!XeB0;LulMNXUAra}d_9dz$1T(ybI^(7{>zKhD5z;Y*m*ZR9HkP5d;+kD;K){>?7}Jxb>D5Kw%dc*X=58uaNR5hJowcU9_nUgq(>u?d*~~a7sS_e;96_`UCcN{6gv|u-CoN_*=8yK4FP&3%oQ9E@U23Y4$Qv?#JUDav9Z49D>I>inxxmh^I_Fe6nMQ*@!H+ONES;XrdjC1`7zYqo_H*-lBBcSxMexYIY<#em^7!BWq{{R%#!J1gVo^2;MSK((KBLZgJY@SrOCysRNK;gopJ<Z4H9r^6F``Q0{l6ie8?8YB-4Ny7E#l6XnRK*3xbEUP-7T_%{X@fi>{Yi6-V-TymT%_I~Bf(C%{q>jVN)Wwg{{C{1Q{dde{|fG0q`B837UTG}enMdPxbr^I^8-OUZWDeEtDOvJP$kKzi8$M`4pRe$n_|$s@WQJf|>M!4=}?-7hU<U~Je}0RVlUu8M?la&CcHvvV;0;)^1UtTg}8QCs?o7=%+!xTeJ!3<=>3u`|0{AbF5$m{#y7qvxUHF-F|lxEXIno0QSi1j&%Z=Q|eR3hwAv!*Fqu-BTI*HqxCdrUL>Lw7;4>mICpk(SxD`1R~eCUJaPX%@(2qDwtHeH<Sm!Q6ep~ES$#p-sio#Z+~QAGR$XyZpY8X(?4pCe#yDsWFp#R@9JQixgTbfz-+-REAZ_|$TiH=!v{b#myyCFn$XEFD0k_$>scy;0T)b`1jlcIN42tRT$vHQm^WM($x}b5Ay(DOg7%`Ogt0z~H_5OO`0K%v#K1}z8Y9A@jbIxNgD>FJ=cw=*Ffdod3B7k7mdZZv*F`v>&bHTDP3(V-yGBSI0O;%O=mCxFO}S7zWzy4Mh{mhOd{!GaZRnKn`jNL{iIE(?8O{mXg!8~@#xc#-CHn&hPU<>{&@d)rjGb5wZ@QG}LY}}?;mN(*Gm6dTBN0TP!YRc?&f~MFYLA$2lFq}*Wqi$e<QAZ2tmrxz?Jc(LQ)-fwg<4Y60rLRQtJ`;?jeoibkef&GIa^7y82Mlix)|$J6Vw5oWduDFVy(?oJb`Gp$>=sg^tF_5+R0!)?apHWp*w@U1@LXQ(#JrUvvD(UO+2Rq508Q_-&!X_v>DkIf@A`pImYVXLk2+BQG!9$t4c}(1A`0~yU-5NN^7Sov<f;1u&<LW=;idf@Q|K}0P<>A-!%9wf}w)1cpf<t3zdpJdPf_*L@^Z8Uu9+l$IiVprGR*PS0I#^wg7ov95dS|uR<?8&S{o<AA&(m>zpZyA*O2L7m*Rz9n3*{k9Dpo70j^hqv@GUW?>yf^nmZ>;X;Ono2VQDGx>^)#cexoHCbOC>*fj0?3qF{4#%vGRMp>7B-QH)D^Rbqxyv>I)yz;+Akn!{KL=?{uf%*Cw~XwWm33;z+3y3(rb^A%SrS#h8Ya_8x*SIfrMF|o1z+Lq2CF!iHlMGcE6KhT+nMVCI5NohYp~JIpZ_z_F3^Gk1>IW3gXOET95ZUSLNe5v<+@*?o`l4wBz`j2>l;7W7iCaxu%JD{nA>lK{@9W{)FIkPHa1eeZ+pOu#L0-C`dpBq+=g3npbK))+W08NISl!7xePZfz>Db3b?+C11TJV%KEB<iEYARMv=Nn=p6uoJ4}(OfXg{pm&9F%g=49@(l!6%WT5s&k$asriY#)Yy%I+$UP7Iy@YrWfCRX~f9!1?u-pMkU3(tp!9(rCD@;6D2HpZ3FRmhOI0J>4;~#TE7aCE{y!FxL05JgtuWE~$VlN{U|q{BAqJK)JLc;R(!bRyS}cth*1~zBUXrMeMy}ivngE5$8ie(#O9`Fmf)VMT;ZE0`+^d^c5K-)N+j+Vvvq?q1}8W-_8Ht@CCj1mgU<0%YV)G|NY<p{eR<`_y_')))
_ROUTES={0:_PAYLOAD['base']}
for _rid,_patch in _PAYLOAD['patches'].items():
    _tape=list(_ROUTES[0])
    for _t,_a in _patch: _tape[_t]=_a
    _ROUTES[int(_rid)]=_tape
del _PAYLOAD
_SETTINGS={'hand_align': True, 'weed_repair': True, 'sell_lead': True, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': False, 'front_run': False}

def _router(observation,step,state):
    if step>=144 and not state.get('day6'):
        shops=_get(_get(observation,'town',{}),'unlocked_shops',[]) or []
        state['route']={('BAKERY', 'BAKERY'): 3, ('BAKERY', 'BRUNCH_SPOT'): 3, ('BAKERY', 'FARMERS_MARKET'): 3, ('BAKERY', 'ICE_CREAM_SHOP'): 3, ('BAKERY', 'PET_CAFE'): 3, ('BAKERY', 'PIZZA_SHOP'): 3, ('BAKERY', 'SMOOTHIE_SHOP'): 3, ('BAKERY', 'YARN_STORE'): 4, ('BRUNCH_SPOT', 'BAKERY'): 3, ('BRUNCH_SPOT', 'BRUNCH_SPOT'): 5, ('BRUNCH_SPOT', 'FARMERS_MARKET'): 3, ('BRUNCH_SPOT', 'ICE_CREAM_SHOP'): 3, ('BRUNCH_SPOT', 'PET_CAFE'): 6, ('BRUNCH_SPOT', 'PIZZA_SHOP'): 3, ('BRUNCH_SPOT', 'SMOOTHIE_SHOP'): 7, ('BRUNCH_SPOT', 'YARN_STORE'): 4, ('FARMERS_MARKET', 'BAKERY'): 8, ('FARMERS_MARKET', 'BRUNCH_SPOT'): 3, ('FARMERS_MARKET', 'FARMERS_MARKET'): 3, ('FARMERS_MARKET', 'ICE_CREAM_SHOP'): 8, ('FARMERS_MARKET', 'PET_CAFE'): 3, ('FARMERS_MARKET', 'PIZZA_SHOP'): 3, ('FARMERS_MARKET', 'SMOOTHIE_SHOP'): 3, ('FARMERS_MARKET', 'YARN_STORE'): 4, ('ICE_CREAM_SHOP', 'BAKERY'): 3, ('ICE_CREAM_SHOP', 'BRUNCH_SPOT'): 3, ('ICE_CREAM_SHOP', 'FARMERS_MARKET'): 3, ('ICE_CREAM_SHOP', 'ICE_CREAM_SHOP'): 3, ('ICE_CREAM_SHOP', 'PET_CAFE'): 9, ('ICE_CREAM_SHOP', 'PIZZA_SHOP'): 3, ('ICE_CREAM_SHOP', 'SMOOTHIE_SHOP'): 9, ('ICE_CREAM_SHOP', 'YARN_STORE'): 4, ('PET_CAFE', 'BAKERY'): 3, ('PET_CAFE', 'BRUNCH_SPOT'): 10, ('PET_CAFE', 'FARMERS_MARKET'): 11, ('PET_CAFE', 'ICE_CREAM_SHOP'): 3, ('PET_CAFE', 'PET_CAFE'): 3, ('PET_CAFE', 'PIZZA_SHOP'): 3, ('PET_CAFE', 'SMOOTHIE_SHOP'): 12, ('PET_CAFE', 'YARN_STORE'): 4, ('PIZZA_SHOP', 'BAKERY'): 3, ('PIZZA_SHOP', 'BRUNCH_SPOT'): 3, ('PIZZA_SHOP', 'FARMERS_MARKET'): 3, ('PIZZA_SHOP', 'ICE_CREAM_SHOP'): 3, ('PIZZA_SHOP', 'PET_CAFE'): 3, ('PIZZA_SHOP', 'PIZZA_SHOP'): 3, ('PIZZA_SHOP', 'SMOOTHIE_SHOP'): 3, ('PIZZA_SHOP', 'YARN_STORE'): 4, ('SMOOTHIE_SHOP', 'BAKERY'): 3, ('SMOOTHIE_SHOP', 'BRUNCH_SPOT'): 3, ('SMOOTHIE_SHOP', 'FARMERS_MARKET'): 3, ('SMOOTHIE_SHOP', 'ICE_CREAM_SHOP'): 3, ('SMOOTHIE_SHOP', 'PET_CAFE'): 3, ('SMOOTHIE_SHOP', 'PIZZA_SHOP'): 3, ('SMOOTHIE_SHOP', 'SMOOTHIE_SHOP'): 3, ('SMOOTHIE_SHOP', 'YARN_STORE'): 13, ('YARN_STORE', 'BAKERY'): 4, ('YARN_STORE', 'BRUNCH_SPOT'): 4, ('YARN_STORE', 'FARMERS_MARKET'): 1, ('YARN_STORE', 'ICE_CREAM_SHOP'): 4, ('YARN_STORE', 'PET_CAFE'): 4, ('YARN_STORE', 'PIZZA_SHOP'): 4, ('YARN_STORE', 'SMOOTHIE_SHOP'): 4, ('YARN_STORE', 'YARN_STORE'): 4}.get(tuple(shops[:2]),0)
        state['day6']=True
    if step>=648 and not state.get('day27'):
        state['route']=2
        state['day27']=True
    return state.get('route',0)


_R42_OPENING=[['BUY_PRODUCT', 'WHEAT', 13], ['BUY_PRODUCT', 'WHEAT', 30], ['SELL', 'WHEAT', 30]]
for _r42_tape in _ROUTES.values():
    _r42_tape[0]=dict(_r42_tape[0],market=[list(o) for o in _R42_OPENING])
del _r42_tape
_IMPL=make_agent(_ROUTES,router=_router,**_SETTINGS)
_IMPL.chassis.diagnostics['terminal_rescue_errors']=0

def agent(observation,configuration=None):
    try:
        action=_IMPL(observation,configuration)
        pass
        return action
    except Exception:
        return {'farmer':['PASS'],'hands':[],'market':[]}

_SHOP_PARENT=agent
del agent

def agent(observation,configuration=None):
    action=_SHOP_PARENT(observation,configuration)
    try:
        if _step_of(observation)>=718:
            view=_View(observation,_int(_get(observation,'player',0)),_IMPL.chassis.cfg)
            units=[]
            for i,pos in enumerate(view.positions):
                units.append(['DROP'] if _shed_adjacent(pos,view.board) and view.inv(i) else ['PASS'])
            action={'farmer':units[0],'hands':units[1:],'market':[]}
            projected=_IMPL.chassis._projected_shed(action,view)
            action['market']=[['SELL',item,projected.get(item,0)] for item in PRODUCTS if projected.get(item,0)>0]
            action['market'].sort(key=lambda o:-view.prices.get(o[1],0)*o[2])
    except Exception:
        _IMPL.chassis.diagnostics['terminal_rescue_errors'] += 1
    return action

# EXP-154 modifications: Ahmed Berat Ozer; public capabilities credited below.
# Dmitrii Gluzdov Seven Turn Rescue and Kaggle engine contributors, Apache-2.0.

_UNIT_NS={"__name__":"v28_own_unit_model"}
exec('# SPDX-License-Identifier: Apache-2.0\n# Extracted Kaggle / kaggle-environments contributor code; see NOTICE.txt.\n"""Exact deterministic unit/decay semantics extracted from kaggle-environments 1.32.7.\nSource kaggriculture.py SHA256 bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e.\nNo interpreter, market RNG, policy controls, or replay content is included.\n"""\n\nENGINE_VERSION = "1.32.7"\nSOURCE_SHA256 = "bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e"\n\nCROPS = {\n    "WHEAT":      {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},\n    "CARROT":     {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False},\n    "TOMATO":     {"seed": 50, "first_yield_day": 8, "max_yield_day": 8, "interval": 1, "max_yield": 4, "ongoing": True},\n    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},\n    "MELON":      {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},\n}\n\nANIMALS = {\n    "GOOSE": {"cost": 300, "structure": "COOP",    "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},\n    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},\n    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},\n}\n\nPRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]\n\nFARMER_MOVES = {\n    "NORTH": (0, -1),\n    "SOUTH": (0, 1),\n    "EAST":  (1, 0),\n    "WEST":  (-1, 0),\n}\n\ndef _shed_access_tiles(board_size):\n    """Four inner-corner tiles around the shed, in NWSE order."""\n    half = board_size // 2\n    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]\n\ndef _is_shed_adjacent(pos, board_size):\n    return tuple(pos) in {(x, y) for (x, y) in _shed_access_tiles(board_size)}\n\ndef _new_plant(crop, day, turns_per_day):\n    cd = CROPS[crop]\n    return {\n        "kind": "PLANT",\n        "crop": crop,\n        "planted_day": day,\n        "watered_today": False,\n        "consecutive_unwatered": 1,  # planting day counts as unwatered\n        "yield_units": 0 if cd["ongoing"] else 1,\n        "max_lifespan_step": (-1 if cd["ongoing"] else (day + cd["max_yield_day"] + 1) * turns_per_day),\n        "fertilized_until_day": -1,\n    }\n\ndef _new_animal(animal, day):\n    a = ANIMALS[animal]\n    return {\n        "kind": a["structure"],\n        "animal": animal,\n        "placed_day": day,\n        "yield_units": 0,\n        "consecutive_unfed": 0,\n        "fed_today": False,\n        "cared_today": False,\n        "fertilizer_available": False,\n        "pending_care_bonus": 0,\n    }\n\ndef _farmer_position(farm, idx):\n    """idx 0 = main farmer, 1+ = hand index."""\n    if idx == 0:\n        return farm["farmer"]\n    return farm["hands"][idx - 1] if idx - 1 < len(farm["hands"]) else None\n\ndef _set_farmer_position(farm, idx, pos):\n    if idx == 0:\n        farm["farmer"] = list(pos)\n    else:\n        farm["hands"][idx - 1] = list(pos)\n\ndef _farmer_inventory(private, idx):\n    """Inventories list is [main_farmer, *hands]; grow it if idx is past the end."""\n    while len(private["inventories"]) <= idx:\n        private["inventories"].append({})\n    return private["inventories"][idx]\n\ndef _inv_add(inv, item, n=1):\n    inv[item] = inv.get(item, 0) + n\n\ndef _inv_take(inv, item, n=1):\n    if inv.get(item, 0) < n:\n        return False\n    inv[item] -= n\n    if inv[item] == 0:\n        del inv[item]\n    return True\n\ndef _apply_unit_action(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):\n    """Process one farmer/hand\'s action. Invalid / illegal actions are silent no-ops."""\n    if not isinstance(action, list) or not action:\n        return\n    op = action[0]\n    pos = _farmer_position(farm, idx)\n    if pos is None:\n        return\n    fx, fy = pos[0], pos[1]\n    inv = _farmer_inventory(private, idx)\n\n    if op in FARMER_MOVES:\n        dx, dy = FARMER_MOVES[op]\n        nx, ny = fx + dx, fy + dy\n        if not (0 <= nx < board_size and 0 <= ny < board_size):\n            return\n        # Movement onto LOCKED tiles is allowed: a hand can spawn on a locked\n        # shed-access tile, and blocking movement would strand it there forever.\n        # Tile operations (PLANT, WATER, etc.) still no-op on LOCKED tiles.\n        _set_farmer_position(farm, idx, (nx, ny))\n        return\n\n    if op == "PASS":\n        return\n\n    tile = farm["tiles"][fy][fx]\n\n    # Shed operations resolve before the LOCKED guard. They use the tile only as\n    # a standing position -- the shed itself is always owned -- and three of the\n    # four shed-access tiles start LOCKED, so guarding them first would make the\n    # shed unreachable from those tiles.\n    if op == "DROP":\n        if not _is_shed_adjacent((fx, fy), board_size):\n            return\n        shed = private["shed"]\n        for item, n in list(inv.items()):\n            if n <= 0:\n                del inv[item]\n                continue\n            room = max(0, shed_capacity - sum(shed.values()))\n            take = min(n, room)\n            if take > 0:\n                shed[item] = shed.get(item, 0) + take\n            del inv[item]\n        return\n\n    if op == "PICKUP":\n        if not _is_shed_adjacent((fx, fy), board_size):\n            return\n        if len(action) < 2:\n            return\n        item = action[1]\n        n = int(action[2]) if len(action) >= 3 else 1\n        if n <= 0:\n            return\n        # Seeds live in private["seeds"] and are consumed directly by PLANT;\n        # they never pass through farmer inventory or the shed.\n        available = private["shed"].get(item, 0)\n        n = min(n, available)\n        if n <= 0:\n            return\n        private["shed"][item] -= n\n        _inv_add(inv, item, n)\n        return\n\n    if op == "PLACE":\n        if len(action) < 2:\n            return\n        item = action[1]\n        # Animal placement: standing on a matching unoccupied structure. A LOCKED\n        # tile is the string "LOCKED", never a dict, so this branch cannot match\n        # there and PLACE falls through to the shed path below.\n        if (\n            item in ANIMALS\n            and isinstance(tile, dict)\n            and tile.get("kind") == ANIMALS[item]["structure"]\n            and "animal" not in tile\n        ):\n            if _inv_take(inv, item, 1):\n                farm["tiles"][fy][fx] = _new_animal(item, day)\n            return\n        # Shed drop: orthogonally adjacent to the shed; obeys shedCapacity.\n        if _is_shed_adjacent((fx, fy), board_size):\n            n = int(action[2]) if len(action) >= 3 else 1\n            if n <= 0:\n                return\n            n = min(n, inv.get(item, 0))\n            if n <= 0:\n                return\n            current = sum(private["shed"].values())\n            room = max(0, shed_capacity - current)\n            n = min(n, room)\n            if n <= 0:\n                return\n            inv[item] -= n\n            if inv[item] == 0:\n                del inv[item]\n            private["shed"][item] = private["shed"].get(item, 0) + n\n        return\n\n    # Everything below mutates the tile the unit stands on, so it requires that\n    # tile to be owned.\n    if tile == "LOCKED":\n        return\n\n    if op == "PLANT":\n        if len(action) < 2:\n            return\n        crop = action[1]\n        if crop not in CROPS:\n            return\n        if tile is not None:\n            return\n        if private["seeds"].get(crop, 0) <= 0:\n            return\n        private["seeds"][crop] -= 1\n        farm["tiles"][fy][fx] = _new_plant(crop, day, turns_per_day)\n        return\n\n    if op == "WATER":\n        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):\n            return\n        if tile["watered_today"]:\n            return\n        tile["watered_today"] = True\n        crop_data = CROPS[tile["crop"]]\n        if not crop_data["ongoing"]:\n            age_days = day - tile["planted_day"]\n            window_start = (crop_data["max_yield_day"] + 1) // 2\n            if window_start <= age_days <= crop_data["max_yield_day"]:\n                bonus = 2 if tile["fertilized_until_day"] >= day else 1\n                tile["yield_units"] = min(crop_data["max_yield"], tile["yield_units"] + bonus)\n        return\n\n    if op == "HARVEST":\n        if not isinstance(tile, dict):\n            return\n        if tile.get("yield_units", 0) <= 0:\n            return\n        if tile.get("kind") == "PLANT":\n            crop_data = CROPS[tile["crop"]]\n            if day - tile["planted_day"] < crop_data["first_yield_day"]:\n                # Ongoing crops only accumulate yield_units after first_yield_day,\n                # so reaching here with yield_units > 0 indicates a bug.\n                if crop_data["ongoing"]:\n                    print(\n                        f"WARNING: HARVEST on immature ongoing {tile[\'crop\']} "\n                        f"(planted day {tile[\'planted_day\']}, current day {day}, "\n                        f"first_yield_day {crop_data[\'first_yield_day\']}, "\n                        f"yield_units {tile[\'yield_units\']}); should never happen"\n                    )\n                return\n            units = tile["yield_units"]\n            tile["yield_units"] = 0\n            _inv_add(inv, tile["crop"], units)\n            if not crop_data["ongoing"]:\n                farm["tiles"][fy][fx] = None\n        elif "animal" in tile:\n            units = tile["yield_units"]\n            tile["yield_units"] = 0\n            _inv_add(inv, ANIMALS[tile["animal"]]["product"], units)\n        return\n\n    if op == "FERTILIZE":\n        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):\n            return\n        if not _inv_take(inv, "FERTILIZER", 1):\n            return\n        # Active for `day`, `day+1`, `day+2` (3 days inclusive).\n        tile["fertilized_until_day"] = max(tile.get("fertilized_until_day", -1), day + 2)\n        return\n\n    if op == "DIG":\n        if tile is None:\n            return\n        # Removes plants, weeds, empty coop/pasture. Does NOT remove a placed animal.\n        if isinstance(tile, dict) and "animal" in tile:\n            return\n        farm["tiles"][fy][fx] = None\n        return\n\n    if op == "BUILD_COOP":\n        if tile is not None:\n            return\n        farm["tiles"][fy][fx] = {"kind": "COOP"}\n        return\n\n    if op == "BUILD_PASTURE":\n        if tile is not None:\n            return\n        farm["tiles"][fy][fx] = {"kind": "PASTURE"}\n        return\n\n    if op == "FEED":\n        if not (isinstance(tile, dict) and "animal" in tile):\n            return\n        if tile["fed_today"]:\n            return\n        if not _inv_take(inv, "WHEAT", 1):\n            return\n        tile["fed_today"] = True\n        return\n\n    if op == "COLLECT_FERTILIZER":\n        if not (isinstance(tile, dict) and "animal" in tile):\n            return\n        if not tile["fertilizer_available"]:\n            return\n        tile["fertilizer_available"] = False\n        _inv_add(inv, "FERTILIZER", 1)\n        return\n\n    if op == "CARE":\n        if not (isinstance(tile, dict) and "animal" in tile):\n            return\n        if tile["cared_today"]:\n            return\n        tile["cared_today"] = True\n        return\n\ndef _decay_plants(farm, step):\n    board_size = len(farm["tiles"])\n    for y in range(board_size):\n        for x in range(board_size):\n            tile = farm["tiles"][y][x]\n            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":\n                continue\n            mls = tile["max_lifespan_step"]\n            if mls < 0 or step < mls:\n                continue\n            if (step - mls) % 2 != 0:\n                continue\n            tile["yield_units"] -= 1\n            if tile["yield_units"] <= 0:\n                farm["tiles"][y][x] = {"kind": "WEED"}\n\n',_UNIT_NS)
_PLANNER_NS=dict(_UNIT_NS)
exec('"""E182 modification: Shop0909 last-seven-turn physical closure planner.\n\nNo engine imports, policy tapes, replay fixtures, RNG or remote calls.\nThe only supported market continuation is SELL; unknown execution abstains.\n"""\nfrom copy import deepcopy\nfrom time import perf_counter\nSTART, FINAL = (712, 718)\nOPS = set(FARMER_MOVES) | {\'PASS\', \'DROP\', \'PICKUP\', \'PLACE\', \'PLANT\', \'WATER\', \'HARVEST\', \'FERTILIZE\', \'DIG\', \'BUILD_COOP\', \'BUILD_PASTURE\', \'FEED\', \'CARE\', \'COLLECT_FERTILIZER\'}\nITEMS = tuple(PRODUCTS) + tuple(ANIMALS)\n\nclass Unsupported(ValueError):\n    pass\n\ndef _get(obj, key, default=None):\n    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)\n\ndef _settings(config):\n    size, turns, last = (_get(config, k, d) for k, d in [(\'boardSize\', 10), (\'turnsPerDay\', 24), (\'episodeSteps\', 720)])\n    if (size, turns, last) != (10, 24, 720):\n        raise Unsupported(\'requires pinned 10x10/24/720 terminal window\')\n    cap = int(_get(config, \'shedCapacity\', 100))\n    orders = min(10, int(_get(config, \'maxMarketOrdersPerTurn\', 10)))\n    if cap < 1 or orders < 1:\n        raise Unsupported(\'invalid capacity/order limit\')\n    return (size, turns, cap, orders)\n\ndef physical_state(obs):\n    """Comparable own physical state; market prices and bank are intentionally excluded."""\n    seat = int(_get(obs, \'player\', 0))\n    farm = _get(obs, \'farms\')[seat]\n    return ({k: v for k, v in farm.items() if k != \'money\'}, _get(obs, \'private\'))\n\ndef _commands(action, n):\n    return [action.get(\'farmer\', [\'PASS\']), *action.get(\'hands\', [])][:n] + [[\'PASS\'] for _ in range(max(0, n - 1 - len(action.get(\'hands\', []))))]\n\ndef _clone_state(farm, private):\n    f = dict(farm)\n    f[\'tiles\'] = [[dict(tile) if isinstance(tile, dict) else tile for tile in row] for row in farm[\'tiles\']]\n    f[\'farmer\'] = list(farm[\'farmer\'])\n    f[\'hands\'] = [list(pos) for pos in farm[\'hands\']]\n    f[\'unlocked_quadrants\'] = list(farm[\'unlocked_quadrants\'])\n    pr = dict(private)\n    pr[\'shed\'], pr[\'seeds\'] = (dict(private[\'shed\']), dict(private[\'seeds\']))\n    pr[\'inventories\'] = [dict(inv) for inv in private[\'inventories\']]\n    return (f, pr)\n\ndef _clone_schedule(schedule):\n    result = []\n    for action in schedule:\n        value = dict(action)\n        if \'farmer\' in action:\n            value[\'farmer\'] = list(action[\'farmer\'])\n        for key in [\'hands\', \'market\']:\n            if key in action:\n                value[key] = [list(command) for command in action[key]]\n        result.append(value)\n    return result\n\ndef _validate(schedule, n, orders):\n    for action in schedule:\n        if not isinstance(action, dict) or set(action) - {\'farmer\', \'hands\', \'market\'}:\n            raise Unsupported(\'unknown action shape\')\n        if not isinstance(action.get(\'hands\', []), list):\n            raise Unsupported(\'hands must be a list\')\n        for command in [action.get(\'farmer\', [\'PASS\']), *action.get(\'hands\', [])]:\n            if not isinstance(command, list) or not command or command[0] not in OPS:\n                raise Unsupported(\'unknown/malformed unit operation\')\n            if command[0] in {\'PICKUP\', \'PLACE\', \'PLANT\'}:\n                if len(command) < 2 or command[1] not in ITEMS:\n                    raise Unsupported(\'unknown unit item\')\n                if len(command) > 2 and (not isinstance(command[2], int)):\n                    raise Unsupported(\'noninteger unit quantity\')\n        market = action.get(\'market\', [])\n        if not isinstance(market, list) or len(market) > orders:\n            raise Unsupported(\'market order shape/cap\')\n        for order in market:\n            if not isinstance(order, list) or len(order) != 3 or order[0] != \'SELL\' or (order[1] not in PRODUCTS) or (not isinstance(order[2], int)) or (order[2] <= 0):\n                raise Unsupported(\'baseline market must contain positive integer SELL only\')\n\ndef liquidation(shed, inherited_market, max_orders=10):\n    """Use actual post-unit stock; retain first parent item ordering, then stable product order."""\n    items = []\n    for order in inherited_market:\n        if order[1] not in items:\n            items.append(order[1])\n    items += [item for item in PRODUCTS if item not in items]\n    orders = [[\'SELL\', item, int(shed.get(item, 0))] for item in items if shed.get(item, 0) > 0]\n    if len(orders) > min(10, max_orders):\n        raise Unsupported(\'actual final stock exceeds order slots\')\n    return orders\n\ndef shop_liquidation(farm, private, prices):\n    """Exact original final worker/drop and market rule, with current stock/prices."""\n    return liquidate(FarmView({\'player\': 0, \'farms\': [farm], \'private\': private, \'market\': {\'prices\': prices}}))\n\ndef simulate(obs, config, schedule, *, final_liquidate=False, detailed=False, preserve_final_commands=False):\n    """Exact own unit/decay and SELL-stock transitions. No claim to simulate shared prices."""\n    size, turns, cap, order_cap = _settings(config)\n    step = int(_get(obs, \'step\', -1))\n    if step < START or step + len(schedule) - 1 > FINAL or (not schedule):\n        raise Unsupported(\'outside 712..718; no day boundary or terminal auto-drop\')\n    if any(((t + 1) % turns == 0 for t in range(step, step + len(schedule)))):\n        raise Unsupported(\'day boundary\')\n    farm0, private0 = physical_state(obs)\n    farm, private = _clone_state(farm0, private0)\n    n = 1 + len(farm[\'hands\'])\n    if len(private[\'inventories\']) != n or n > 32:\n        raise Unsupported(\'invalid/unbounded worker inventory shape\')\n    _validate(schedule, n, order_cap)\n    deposited = [dict() for _ in range(n)]\n    sold = {}\n    snapshots, rows, events = ([], [], [])\n    executed = _clone_schedule(schedule)\n    overflow = 0\n    for offset, action in enumerate(executed):\n        t = step + offset\n        if detailed:\n            snapshots.append(_clone_state(farm, private))\n        if t == FINAL and (not preserve_final_commands):\n            action = shop_liquidation(farm, private, _get(obs, \'market\')[\'prices\'])\n            executed[offset] = action\n        all_commands = [action.get(\'farmer\', [\'PASS\']), *action.get(\'hands\', [])]\n        demand = {}\n        for command in all_commands:\n            if command[0] == \'PLANT\':\n                demand[command[1]] = demand.get(command[1], 0) + 1\n        blocked = {item for item, count in demand.items() if count > private[\'seeds\'].get(item, 0)}\n        for actor, command in enumerate(_commands(action, n)):\n            if command[0] == \'PLANT\' and command[1] in blocked:\n                command = [\'PASS\']\n            pos = farm[\'farmer\'] if actor == 0 else farm[\'hands\'][actor - 1]\n            xy = tuple(pos)\n            inv = private[\'inventories\'][actor]\n            before_inv = dict(inv) if command[0] in {\'DROP\', \'HARVEST\', \'COLLECT_FERTILIZER\'} else None\n            before_shed = dict(private[\'shed\']) if command[0] in {\'DROP\', \'PLACE\'} else None\n            _apply_unit_action(farm, private, actor, command, size, t // turns, turns, cap)\n            if before_shed is not None:\n                delta = {item: amount - before_shed.get(item, 0) for item, amount in private[\'shed\'].items() if amount > before_shed.get(item, 0)}\n                for item, amount in delta.items():\n                    deposited[actor][item] = deposited[actor].get(item, 0) + amount\n                if delta:\n                    events.append({\'offset\': offset, \'actor\': actor, \'op\': command[0], \'xy\': xy, \'deposited\': delta})\n                if command[0] == \'DROP\':\n                    overflow += sum((max(0, amount - inv.get(item, 0) - delta.get(item, 0)) for item, amount in before_inv.items()))\n            if command[0] in {\'HARVEST\', \'COLLECT_FERTILIZER\'}:\n                delta = {item: amount - before_inv.get(item, 0) for item, amount in inv.items() if amount > before_inv.get(item, 0)}\n                if delta:\n                    events.append({\'offset\': offset, \'actor\': actor, \'op\': command[0], \'xy\': xy, \'acquired\': delta})\n        pre_market = dict(private[\'shed\'])\n        if t == FINAL and preserve_final_commands and final_liquidate:\n            action[\'market\'] = liquidation(pre_market, [], order_cap)\n            prices = _get(obs, \'market\')[\'prices\']\n            action[\'market\'].sort(key=lambda order: -int(prices.get(order[1], 0)) * order[2])\n        for _, item, requested in action.get(\'market\', []):\n            quantity = min(requested, private[\'shed\'].get(item, 0), 99999)\n            if quantity > 0:\n                private[\'shed\'][item] -= quantity\n                sold[item] = sold.get(item, 0) + quantity\n        _decay_plants(farm, t)\n        rows.append({\'pre_market_shed\': pre_market, \'post_market_shed\': dict(private[\'shed\']), \'deposited_by_actor\': [dict(v) for v in deposited], \'sold\': dict(sold)})\n    if detailed:\n        snapshots.append(_clone_state(farm, private))\n    return {\'rows\': rows, \'states\': snapshots, \'events\': events, \'actions\': executed, \'overflow_units\': overflow, \'farm\': farm, \'private\': private, \'sold\': sold}\n\ndef _ge(left, right):\n    return all((left.get(item, 0) >= value for item, value in right.items()))\n\ndef dominates(candidate, baseline):\n    """Preserve every baseline worker\'s actual deposit prefixes and shed availability."""\n    if candidate[\'overflow_units\']:\n        return False\n    for new, old in zip(candidate[\'rows\'], baseline[\'rows\']):\n        if not _ge(new[\'pre_market_shed\'], old[\'pre_market_shed\']):\n            return False\n        if not _ge(new[\'sold\'], old[\'sold\']):\n            return False\n        if any((not _ge(a, b) for a, b in zip(new[\'deposited_by_actor\'], old[\'deposited_by_actor\']))):\n            return False\n    return True\n\ndef _value(run, prices):\n    shed = run[\'private\'][\'shed\']\n    return sum(((run[\'sold\'].get(item, 0) + shed.get(item, 0)) * prices[item] for item in PRODUCTS))\n\ndef _walk(start, end):\n    x, y = start\n    tx, ty = end\n    return [[\'EAST\']] * max(0, tx - x) + [[\'WEST\']] * max(0, x - tx) + [[\'SOUTH\']] * max(0, ty - y) + [[\'NORTH\']] * max(0, y - ty)\n\ndef _return(pos):\n    targets = _shed_access_tiles(10)\n    target = min(targets, key=lambda xy: (abs(pos[0] - xy[0]) + abs(pos[1] - xy[1]), targets.index(xy)))\n    return _walk(pos, target) + [[\'DROP\']]\n\ndef _proposals(run, actor, prices, max_per_actor):\n    """One/two resource bundles plus direct carry closure, replacing a baseline suffix."""\n    owners = {}\n    for event in run[\'events\']:\n        if \'acquired\' in event:\n            owners.setdefault((tuple(event[\'xy\']), event[\'op\']), set()).add(event[\'actor\'])\n    proposals = []\n    seen = set()\n    horizon = len(run[\'rows\'])\n    for offset in range(horizon):\n        farm, private = run[\'states\'][offset]\n        pos = tuple(farm[\'farmer\'] if actor == 0 else farm[\'hands\'][actor - 1])\n        inventory = private[\'inventories\'][actor]\n        carried = sum((prices.get(item, 0) * count for item, count in inventory.items()))\n        prefix_deposits = run[\'rows\'][offset - 1][\'deposited_by_actor\'][actor] if offset else {}\n        future_deposits = run[\'rows\'][-1][\'deposited_by_actor\'][actor]\n        obligation = sum((prices.get(item, 0) * (count - prefix_deposits.get(item, 0)) for item, count in future_deposits.items()))\n        bundles = []\n        for y, row in enumerate(farm[\'tiles\']):\n            for x, tile in enumerate(row):\n                if not isinstance(tile, dict):\n                    continue\n                xy, operations, value = ((x, y), [], 0)\n                if tile.get(\'yield_units\', 0) > 0:\n                    item = tile.get(\'crop\') if tile.get(\'kind\') == \'PLANT\' else ANIMALS.get(tile.get(\'animal\'), {}).get(\'product\')\n                    mature = item and (\'animal\' in tile or (START + offset) // 24 - tile[\'planted_day\'] >= CROPS[item][\'first_yield_day\'])\n                    if mature and (not owners.get((xy, \'HARVEST\'), set()) - {actor}):\n                        operations.append([\'HARVEST\'])\n                        value += prices[item] * tile[\'yield_units\']\n                if tile.get(\'fertilizer_available\') and \'animal\' in tile and (not owners.get((xy, \'COLLECT_FERTILIZER\'), set()) - {actor}):\n                    operations.append([\'COLLECT_FERTILIZER\'])\n                    value += prices[\'FERTILIZER\']\n                if operations:\n                    distance = len(_walk(pos, xy)) + len(operations) + len(_return(xy))\n                    if distance <= horizon - offset:\n                        bundles.append((xy, operations, value, distance))\n        bundles.sort(key=lambda b: (-b[2] / b[3], -b[2], b[0]))\n        variants = [([], carried)] if carried else []\n        for xy, ops, value, _ in bundles[:6]:\n            variants.append(([(xy, ops)], carried + value))\n        for first in bundles[:3]:\n            for second in bundles[:3]:\n                if first[0] != second[0]:\n                    variants.append(([(first[0], first[1]), (second[0], second[1])], carried + first[2] + second[2]))\n        for stops, value in variants:\n            route, cursor = ([], pos)\n            for xy, ops in stops:\n                route += _walk(cursor, xy) + ops\n                cursor = xy\n            route += _return(cursor)\n            if len(route) > horizon - offset:\n                continue\n            route += [[\'PASS\']] * (horizon - offset - len(route))\n            key = (offset, tuple((tuple(c) for c in route)))\n            if key not in seen:\n                seen.add(key)\n                proposals.append((value - obligation, offset, route, len(stops)))\n    proposals.sort(key=lambda p: (-p[0], p[1], p[2]))\n    direct = [p for p in proposals if p[3] == 0 and p[0] > 0][:2]\n    chosen = direct + [p for p in proposals if p not in direct]\n    return chosen[:max_per_actor]\n\ndef plan_terminal(obs, config, baseline_remaining, *, max_simulations=64, passes=1, proposals_per_actor=4):\n    """At 712 accept seven actions; positive physical delivery is mandatory."""\n    begun = perf_counter()\n    fallback = {\'accepted\': False, \'reason\': \'\', \'actions\': None, \'simulations\': 0}\n    try:\n        if int(_get(obs, \'step\', -1)) != START or len(baseline_remaining) != FINAL - START + 1:\n            raise Unsupported(\'planning requires step 712 and exactly seven actions through 718\')\n        max_simulations = min(256, max(1, int(max_simulations)))\n        passes = min(2, max(1, int(passes)))\n        proposals_per_actor = min(16, max(1, int(proposals_per_actor)))\n        baseline = simulate(obs, config, baseline_remaining, detailed=True)\n        prices = {item: max(1, float(_get(obs, \'market\', {}).get(\'prices\', {}).get(item, 1))) for item in PRODUCTS}\n        current, best = (_clone_schedule(baseline_remaining), baseline)\n        baseline_value = best_value = _value(baseline, prices)\n        changes, simulations = ([], 0)\n        n = len(baseline[\'private\'][\'inventories\'])\n        for sweep in range(passes):\n            improved = False\n            for actor in range(n):\n                winner = None\n                for _, offset, route, bundle_count in _proposals(best, actor, prices, proposals_per_actor):\n                    if simulations >= max_simulations:\n                        break\n                    trial = _clone_schedule(current)\n                    for i, command in enumerate(route, offset):\n                        if actor == 0:\n                            trial[i][\'farmer\'] = command\n                        else:\n                            trial[i].setdefault(\'hands\', [])\n                            while len(trial[i][\'hands\']) < n - 1:\n                                trial[i][\'hands\'].append([\'PASS\'])\n                            trial[i][\'hands\'][actor - 1] = command\n                    evaluated = simulate(obs, config, trial)\n                    simulations += 1\n                    score = _value(evaluated, prices)\n                    if score > best_value and dominates(evaluated, baseline):\n                        required = {(tuple(e[\'xy\']), e[\'op\'], e[\'actor\']): e[\'acquired\'] for e in best[\'events\'] if \'acquired\' in e and e[\'actor\'] != actor}\n                        acquired = {}\n                        for e in evaluated[\'events\']:\n                            if \'acquired\' in e:\n                                key = (tuple(e[\'xy\']), e[\'op\'], e[\'actor\'])\n                                dst = acquired.setdefault(key, {})\n                                for item, amount in e[\'acquired\'].items():\n                                    dst[item] = dst.get(item, 0) + amount\n                        if all((_ge(acquired.get(k, {}), v) for k, v in required.items())):\n                            winner, best_value = ((trial, offset, bundle_count), score)\n                if winner:\n                    current, offset, bundle_count = winner\n                    best = simulate(obs, config, current, detailed=True)\n                    changes.append({\'pass\': sweep, \'actor\': actor, \'from_step\': START + offset, \'resource_bundles\': bundle_count, \'estimated_stock_value\': best_value})\n                    improved = True\n                if simulations >= max_simulations:\n                    break\n            if not improved or simulations >= max_simulations:\n                break\n        if not changes or best_value <= baseline_value:\n            return {**fallback, \'reason\': \'no positive physical delivery gain\', \'simulations\': simulations, \'changed_workers\': [], \'changes\': [], \'certificate\': {\'stock_value_gain_at_initial_prices\': 0, \'sold_unit_delta\': dict.fromkeys(PRODUCTS, 0)}, \'planning_ms\': (perf_counter() - begun) * 1000}\n        final = simulate(obs, config, current, final_liquidate=True, detailed=True)\n        physical = simulate(obs, config, current)\n        if not dominates(physical, baseline):\n            raise Unsupported(\'no zero-overflow dominating continuation\')\n        delta = {item: final[\'sold\'].get(item, 0) - baseline[\'sold\'].get(item, 0) for item in PRODUCTS}\n        deposited_gain = any((final[\'rows\'][-1][\'deposited_by_actor\'][actor].get(item, 0) > baseline[\'rows\'][-1][\'deposited_by_actor\'][actor].get(item, 0) for actor in range(n) for item in PRODUCTS))\n        worker_change = any((_commands(new, n) != _commands(old, n) for new, old in zip(final[\'actions\'], baseline[\'actions\'])))\n        accepted = worker_change and deposited_gain and any((v > 0 for v in delta.values())) and all((v >= 0 for v in delta.values()))\n        plan = {\'accepted\': accepted, \'reason\': \'joint physical dominance\' if accepted else \'no improvement\', \'baseline\': _clone_schedule(baseline_remaining), \'actions\': final[\'actions\'], \'expected_states\': final[\'states\'][:-1], \'simulations\': simulations, \'changes\': changes, \'abandoned\': False, \'changed_workers\': sorted({c[\'actor\'] for c in changes}), \'certificate\': {\'baseline_rows\': baseline[\'rows\'], \'physical_rows\': physical[\'rows\'], \'baseline_overflow\': baseline[\'overflow_units\'], \'candidate_overflow\': final[\'overflow_units\'], \'sold_unit_delta\': delta, \'stock_value_gain_at_initial_prices\': best_value - baseline_value, \'baseline_final_shed\': baseline[\'private\'][\'shed\'], \'final_shed\': final[\'private\'][\'shed\'], \'positive_physical_deposit_gain\': deposited_gain, \'markets_712_717_unchanged\': all((final[\'actions\'][i].get(\'market\', []) == baseline_remaining[i].get(\'market\', []) for i in range(FINAL - START)))}}\n    except (Unsupported, KeyError, TypeError, ValueError, IndexError) as exc:\n        plan = {**fallback, \'reason\': str(exc)}\n    plan[\'planning_ms\'] = (perf_counter() - begun) * 1000\n    return plan\n\ndef _effective_action(action, n):\n    return (_commands(action, n), action.get(\'market\', []))\n\ndef _recover_observed(obs, config, parent_action, plan):\n    """Bounded cargo salvage after deviation; never resume old positional commands."""\n    farm, private = physical_state(obs)\n    positions = [farm[\'farmer\'], *farm[\'hands\']]\n    remaining = FINAL - int(_get(obs, \'step\')) + 1\n    room = max(0, int(_get(config, \'shedCapacity\', 100)) - sum(private[\'shed\'].values()))\n    commands = []\n    problems = []\n    prices = _get(obs, \'market\', {}).get(\'prices\', {})\n    for actor, (pos, inv) in enumerate(zip(positions, private[\'inventories\'])):\n        command = [\'PASS\']\n        if any((v > 0 for v in inv.values())):\n            route = _return(pos)\n            if len(route) > remaining:\n                problems.append({\'actor\': actor, \'reason\': \'unreachable cargo\'})\n            elif len(route) > 1:\n                command = route[0]\n            elif sum((max(0, q) for q in inv.values())) <= room:\n                command = [\'DROP\']\n                room -= sum((max(0, q) for q in inv.values()))\n            else:\n                items = [item for item in PRODUCTS if inv.get(item, 0) > 0]\n                if room and items:\n                    item = max(items, key=lambda i: (prices.get(i, 1) * min(inv[i], room), -PRODUCTS.index(i)))\n                    quantity = min(inv[item], room)\n                    command = [\'PLACE\', item, quantity]\n                    room -= quantity\n                else:\n                    problems.append({\'actor\': actor, \'reason\': \'no shed capacity\'})\n        commands.append(command)\n    action = {\'farmer\': commands[0], \'hands\': commands[1:], \'market\': deepcopy(parent_action.get(\'market\', []))}\n    if int(_get(obs, \'step\')) == FINAL:\n        action[\'market\'] = []\n        action = simulate(obs, config, [action], final_liquidate=True, preserve_final_commands=True)[\'actions\'][0]\n    plan[\'recovery_steps\'] = plan.get(\'recovery_steps\', 0) + 1\n    if problems:\n        plan.setdefault(\'recovery_failures\', []).append({\'step\': int(_get(obs, \'step\')), \'problems\': problems})\n    return action\n\ndef terminal_action(obs, config, parent_action, plan):\n    """Canonical guard, pre-deviation abstention, observed recovery after deviation."""\n    step = int(_get(obs, \'step\', -1))\n    if not plan or not plan.get(\'accepted\') or (not START <= step <= FINAL):\n        return parent_action\n    if plan.get(\'abandoned\'):\n        return _recover_observed(obs, config, parent_action, plan) if plan.get(\'deviated\') else parent_action\n    index = step - START\n    n = 1 + len(physical_state(obs)[0][\'hands\'])\n    mismatch = physical_state(obs) != plan[\'expected_states\'][index] or _effective_action(parent_action, n) != _effective_action(plan[\'baseline\'][index], n)\n    if mismatch:\n        plan[\'abandoned\'] = True\n        plan[\'abandon_step\'] = step\n        plan[\'reason\'] = \'physical observation or effective baseline action diverged\'\n        plan[\'safety_failure\'] = True\n        return _recover_observed(obs, config, parent_action, plan) if plan.get(\'deviated\') else parent_action\n    result = deepcopy(plan[\'actions\'][index])\n    if step == FINAL:\n        farm, private = physical_state(obs)\n        result = shop_liquidation(farm, private, _get(obs, \'market\')[\'prices\'])\n    if _commands(result, n) != _commands(parent_action, n):\n        plan[\'deviated\'] = True\n    return result',_PLANNER_NS)
# EXP-154 integration by Ahmed Berat Ozer, derived from Dmitrii Gluzdov E182.
# The preserved v27 parent is simulated on a private shadow only at step 712.
_PRE_TERMINAL_AGENT=agent
del agent
_TERMINAL_PLANS={}
_TERMINAL_PREVIOUS={}
_UPGRADE_STATS={'planning_calls':0,'accepted':0,'changed_steps':0,'aborted':0,'shadow_declines':0,'errors':0,'max_planning_ms':0.0}

def _parent_liquidate(farm, private, prices):
    # Exactly v27's final projected DROP ordering, in the planner's private state.
    view=_View({'player':0,'farms':[farm],'private':private,'market':{'prices':prices}},0,_IMPL.chassis.cfg)
    commands=[['DROP'] if _shed_adjacent(pos,view.board) and view.inv(i) else ['PASS'] for i,pos in enumerate(view.positions)]
    action={'farmer':commands[0],'hands':commands[1:],'market':[]}
    stock=_IMPL.chassis._projected_shed(action,view)
    action['market']=[['SELL',item,stock.get(item,0)] for item in PRODUCTS if stock.get(item,0)>0]
    action['market'].sort(key=lambda o:-view.prices.get(o[1],0)*o[2])
    return action

_PLANNER_NS['shop_liquidation']=_parent_liquidate

def _shadow_terminal(obs,config):
    seat=int(obs['player']);chassis=_IMPL.chassis
    state=chassis.players.get(seat)
    if not state or state.get('last_step')!=711 or state.get('route')!=2:
        return None
    # No delayed weed/structure intervention may depend on an unmodeled future.
    if state.get('pending'):
        return None
    shadow=copy.copy(chassis);shadow.players=copy.deepcopy(chassis.players)
    shadow.diagnostics={k:0 for k in chassis.diagnostics}
    projected=copy.deepcopy(obs);baseline=[];states=[]
    for step in range(712,719):
        projected['step']=step;projected['day']=step//24;projected['hour']=step%24
        states.append(copy.deepcopy(shadow.players[seat]))
        action=shadow.act(projected,config)
        if step==718:
            action=_parent_liquidate(projected['farms'][seat],projected['private'],projected['market']['prices'])
        else:
            market=action.get('market',[])
            if len(market)!=9 or {o[1] for o in market}!=set(PRODUCTS) or any(o[0]!='SELL' or len(o)!=3 or type(o[2]) is not int or o[2]<100 for o in market):
                return None
        if any(shadow.diagnostics.values()):return None
        run=_PLANNER_NS['simulate'](projected,config,[action])
        if run['actions'][0]!=action:return None
        baseline.append(action)
        run['farm']['money']=projected['farms'][seat]['money']
        projected['farms'][seat]=run['farm'];projected['private']=run['private']
    return baseline,states

def agent(observation,configuration=None):
    try:
        step=int(observation['step']);seat=int(observation['player'])
    except Exception:
        return _PRE_TERMINAL_AGENT(observation,configuration)
    previous=_TERMINAL_PREVIOUS.get(seat)
    if step==0 or (previous is not None and step<=previous):_TERMINAL_PLANS.pop(seat,None)
    _TERMINAL_PREVIOUS[seat]=step
    plan=_TERMINAL_PLANS.get(seat)
    if plan and plan.get('accepted') and 712<=step<=718:
        if previous!=step-1:plan.update(abandoned=True,reason='nonconsecutive callback')
        try:
            result=_PLANNER_NS['terminal_action'](observation,configuration,plan['baseline'][step-712],plan)
            if plan.get('abandoned'):
                if not plan.get('abort_counted'):
                    plan['abort_counted']=True;_UPGRADE_STATS['aborted']+=1
                if not plan.get('deviated'):
                    _IMPL.chassis.players[seat]=copy.deepcopy(plan['parent_states_before'][step-712])
                    _TERMINAL_PLANS.pop(seat,None)
                    return _PRE_TERMINAL_AGENT(observation,configuration)
            _UPGRADE_STATS['changed_steps']+=int(result!=plan['baseline'][step-712])
            return result
        except Exception:
            _UPGRADE_STATS['errors']+=1
            if plan.get('deviated'):
                try:return _PLANNER_NS['_recover_observed'](observation,configuration,plan['baseline'][step-712],plan)
                except Exception:return _parent_liquidate(observation['farms'][seat],observation['private'],observation['market']['prices'])
    if step!=712:return _PRE_TERMINAL_AGENT(observation,configuration)
    _UPGRADE_STATS['planning_calls']+=1
    try:shadow=_shadow_terminal(observation,configuration)
    except (ValueError,KeyError,TypeError,IndexError):shadow=None
    if shadow is None:
        _UPGRADE_STATS['shadow_declines']+=1
        return _PRE_TERMINAL_AGENT(observation,configuration)
    baseline,states=shadow
    actual=_PRE_TERMINAL_AGENT(observation,configuration)
    if actual!=baseline[0]:
        _UPGRADE_STATS['shadow_declines']+=1;return actual
    try:
        plan=_PLANNER_NS['plan_terminal'](observation,configuration,baseline,max_simulations=64,passes=1,proposals_per_actor=4)
        _UPGRADE_STATS['max_planning_ms']=max(_UPGRADE_STATS['max_planning_ms'],plan.get('planning_ms',0.0))
        if not plan.get('accepted'):return actual
        plan['parent_states_before']=states;_TERMINAL_PLANS[seat]=plan
        _UPGRADE_STATS['accepted']+=1
        result=_PLANNER_NS['terminal_action'](observation,configuration,actual,plan)
        _UPGRADE_STATS['changed_steps']+=int(result!=actual)
        return result
    except Exception:
        _UPGRADE_STATS['errors']+=1;return actual

agent.telemetry=_UPGRADE_STATS

# EXP-154: aurax7 Reactive v2 day-end storage guard, adapted to our v27 view.
_PRE_ROOM_AGENT=agent
del agent
_ROOM_STATS={'changed_turns':0,'added_units':0,'errors':0}
def agent(observation,configuration=None):
    action=_PRE_ROOM_AGENT(observation,configuration)
    try:
        step=_step_of(observation)
        if step%24!=23:return action
        view=_View(observation,_int(_get(observation,'player',0)),_IMPL.chassis.cfg)
        carried=sum(max(0,int(n)) for inv in view.invs for n in inv.values())
        needed=sum(view.shed.values())+carried-99
        if needed<=0:return action
        planned={}
        for o in action.get('market',[]):
            if o and o[0]=='SELL' and len(o)>=3:planned[o[1]]=planned.get(o[1],0)+max(0,int(o[2]))
        result=copy.deepcopy(action);added=0
        for item in sorted(PRODUCTS,key=lambda it:-int(view.prices.get(it,0))):
            qty=min(needed,max(0,view.shed.get(item,0)-planned.get(item,0)))
            if qty<=0:continue
            if len(result['market'])>=10:break
            result['market'].append(['SELL',item,qty]);needed-=qty;added+=qty
            if needed<=0:break
        if added:_ROOM_STATS['changed_turns']+=1;_ROOM_STATS['added_units']+=added
        return result
    except Exception:
        _ROOM_STATS['errors']+=1;return action

agent.telemetry=_ROOM_STATS

# Incorporated upstream attribution and change notice:
# E182 Shop0909 + terminal physical closure (modified 2026-09-09)
# 
# The active public parent is Yusuke Hayashi's yhay81/shop-router-0909 v3.
# router_parent.py and actions.json are exact original bytes, not newly authored
# routes. The parent credits aurax7's Reactive Router for sale timing and shed
# projection; that attribution remains in router_parent.py. Original payload
# LICENSE.txt is preserved unchanged (Apache License 2.0 text); it contains no
# named copyright grantor and no separate NOTICE was supplied. No additional
# ownership, endorsement, or upstream replay-data rights claim is made.
# 
# Local changes: separate main.py/policy.py adapter; bounded start712 planner
# copied from frozen E180/S78 and modified for seven callbacks, exact Shop final
# liquidation, strict positive physical delivery/sale gain, and observation guards.
# unit_model.py is an unchanged frozen E180 copy of Kaggle's extracted semantics.
# The following original E180 notice is retained verbatim for attribution history.
# Its references to Thomas files describe E180, not files supplied in this Shop
# package: no Thomas tapes, trees or policy are included here.
# 
# ----- Original E180 notice -----
# Kaggriculture: Last-Mile Harvest Planner
# Attribution and change notice
# 
# Thomas Tschinkel is the author of the parent public state-router policy and its
# published decision trees and action-route data. Source: Kaggriculture: 93.8% Win
# Rate Public State Router, notebook version 3, scriptVersionId 347936183:
# https://www.kaggle.com/code/thomastschinkel/kaggriculture-93-8-win-rate-public-state-router?scriptVersionId=347936183
# The public notebook identifies its license as Apache License, Version 2.0.
# Original published main.py SHA-256:
# b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522
# 
# Changes to that source for this distribution: compressed route/tree literals
# were decoded into readable tapes.json and trees.json; a read-only planned_action
# helper was added; descriptive headers and local data loading were adapted.
# The original parent feature extraction, tree traversal and agent behavior are
# retained. These public routes are not claimed as newly authored or trained by
# the notebook distributor.
# 
# unit_model.py contains deterministic unit-action and crop-decay definitions
# extracted from Kaggle's kaggle-environments 1.32.7 Kaggriculture engine, licensed
# under Apache License, Version 2.0. Credit: Kaggle and the kaggle-environments
# contributors. Project: https://github.com/Kaggle/kaggle-environments
# Source file: kaggle_environments/envs/kaggriculture/kaggriculture.py
# Source SHA-256:
# bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e
# The extracted unit/decay definitions are not a newly authored game engine;
# market price dynamics and the full interpreter are not part of this module.
# 
# Additional work in this distribution: a bounded last-nine-action collection
# and delivery planner, observation guards and recovery, a settings-consuming
# factory and entry point, standalone examples, and deterministic packaging.
# The full Apache License, Version 2.0 is included as LICENSE.txt.
# No endorsement by Thomas Tschinkel or Kaggle is implied.
# 
# Data provenance limitation: Thomas's source refers to public replay data and
# an upstream provenance.json. That original episode-level manifest, replay IDs
# and individual replay-author identities were not supplied with the public
# notebook/output used here. No names or episode lineage have been invented.
# Notebook-level licensing does not independently establish the missing underlying
# replay-data rights chain. The package supplies usable readable routes, not a
# reproducible reconstruction of their original collection or training process.
# 
# Packaging note: source inputs described as byte-exact above are
# normalized to UTF-8/LF text with a final newline in this standalone
# notebook package. Route JSON values and parent policy behavior are unchanged.

# Final public-entry guard; measured separately and compared on captured observations.
_V28_CORE=agent
del agent
_IMPL.chassis.diagnostics['v28_entry_errors']=0
def agent(observation,configuration=None):
    try:
        return _V28_CORE(observation,configuration)
    except Exception:
        _IMPL.chassis.diagnostics['v28_entry_errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_ROOM_STATS

# EXP-155: prvsiyan V221B finite tomato investment, adapted by Ahmed Berat Ozer.
# Original public source is retained under research24/public; Apache-2.0.
MAX_ORDERS=10
class FarmView(_View):
    def __init__(self,obs):super().__init__(obs,int(obs['player']),_IMPL.chassis.cfg)
    def inventory(self,actor):return self.inv(actor)
def projected_shed(action,view):return _IMPL.chassis._projected_shed(action,view)

CROP_MIN_PRICE=70

# V219: a finite late tomato investment with dedicated, observed workers.
_V219_PARENT = agent
del agent
_V219_FERTILIZE = True  # Builder changes only this flag for the ablation.
_V219_STATES = {}
_V219_REPORT = {'commitments': 0, 'hire_requests': 0, 'confirmed_workers': 0,
                'hire_shortfalls': 0, 'plant_requests': 0, 'confirmed_plants': 0,
                'water_requests': 0, 'fertilize_requests': 0, 'harvest_requests': 0,
                'confirmed_harvest_units': 0, 'drop_requests': 0,
                'tomato_sale_requests': 0, 'budget_declines': 0, 'lost_plants': 0}


def _v219_fib(n):
    a, b = 1, 1
    for _ in range(n): a, b = b, a+b
    return a


def _v219_native_day(native, day):
    tape = _IMPL.chassis.routes[native['route']]
    return tape[day*24:min((day+1)*24,719)]


def _v219_qualifies(obs, native):
    farm=obs['farms'][obs['player']]
    if len(farm['tiles']) != 10 or set(farm['unlocked_quadrants']) != {'NW','NE','SW'}:
        return False
    if farm['money'] < 12000 or obs['market']['prices']['TOMATO'] < CROP_MIN_PRICE:
        return False
    if sum(s in ('PIZZA_SHOP','FARMERS_MARKET') for s in obs['town']['unlocked_shops']) < 3:
        return False
    if any(farm['tiles'][y][x] != 'LOCKED' for y in (5,6) for x in range(5,10)):
        return False
    if obs['private']['seeds'].get('TOMATO',0) or obs['private']['shed'].get('TOMATO',0):
        return False
    if any(isinstance(t,dict) and t.get('crop')=='TOMATO' for row in farm['tiles'] for t in row):
        return False
    # The investment uses spare land and new worker indices. Avoid taking over
    # any native tomato or land purchase obligation on the known own schedule.
    for tape in _IMPL.chassis.routes.values():
        for a in tape[432:719]:
            if any(o and o[0]=='BUY_LAND' for o in a.get('market',[])):return False
            if any(c==['PLANT','TOMATO'] for c in [a.get('farmer')]+a.get('hands',[])):return False
    return True


def _v219_walk(pos, target):
    x,y=pos;tx,ty=target
    if x != tx:return ['EAST' if x < tx else 'WEST']
    if y != ty:return ['SOUTH' if y < ty else 'NORTH']
    return None


def _v219_home(pos):
    return min(((4,4),(5,4),(4,5),(5,5)),key=lambda p:abs(pos[0]-p[0])+abs(pos[1]-p[1]))


def _v219_request(obs, action, state, native):
    step=int(obs['step']);day=step//24;offset=step%24
    farm=obs['farms'][obs['player']];private=obs['private']
    # If the planting-day transaction could not complete, abandon investment.
    # Later purchases would miss the finite day26..29 production window.
    if not state.get('committed') and day!=18:return action
    if state.get('requested_day')==day or offset>3:return action
    planned=_v219_native_day(native,day)
    remaining=planned[offset+1:]
    if any(o and o[0]=='HIRE' for a in remaining for o in a.get('market',[])):
        return action
    parent_hires=sum(bool(o) and o[0]=='HIRE' for o in action['market'])
    expected=max(len(a.get('hands',[])) for a in planned)
    if len(farm['hands'])+parent_hires != expected:return action
    fertilizer=bool(_V219_FERTILIZE and day in (24,27) and obs['market']['prices']['FERTILIZER']<=30)
    # One watering tour: at most 2 entry moves + 9 between tiles + 10 waters.
    # A hire request by hour2 leaves at least21 callbacks after confirmation.
    crop_workers=1 if day in (19,20,21,22,23,25) and offset<=2 else (3 if 26<=day<=28 else 2)
    labor=_r53_labor_assignment(obs,action,fertilizer)
    if labor is not None:crop_workers=labor['workers']
    count=crop_workers+int(fertilizer and day==27 and labor is None)
    extra=[]
    if not state.get('committed'):
        extra += [['BUY_LAND'],['BUY_SEED','TOMATO',10]]
    if fertilizer:extra.append(['BUY_PRODUCT','FERTILIZER',10])
    extra += [['HIRE'] for _ in range(count)]
    if len(action['market'])+len(extra)>MAX_ORDERS:return action
    # No assumed sale proceeds. Reserve 3,000 for parent obligations and price
    # movement; the qualification separately requires 12,000 initial liquidity.
    budget=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+parent_hires+count))
    if not state.get('committed'):budget+=4500
    if fertilizer:budget+=10*(obs['market']['prices']['FERTILIZER']+5)
    for order in action['market']:
        if not order:continue
        if order[0]=='BUY_PRODUCT':budget+=int(order[2])*(int(obs['market']['prices'][order[1]])+10)
        elif order[0]=='BUY_ANIMAL':budget+=int(order[2])*{'COW':400,'SHEEP':500,'GOOSE':300}[order[1]]
        elif order[0]=='BUY_SEED':budget+=int(order[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[order[1]]
    if farm['money']<budget+3000:
        _V219_REPORT['budget_declines']+=1;return action
    state['pending']={'step':step,'first_actor':expected+1,'count':count,'crop_workers':crop_workers,'fertilizer':fertilizer,'labor':labor}
    if labor is not None:
        _R53_LABOR_REPORT['labor_requests']+=1;_R53_LABOR_REPORT['labor_hires_avoided']+=1;_R53_LABOR_REPORT['labor_day'+str(day)]+=1
    state['requested_day']=day
    _V219_REPORT['hire_requests']+=count
    if not state.get('committed'):
        state['committed']=True;_V219_REPORT['commitments']+=1
    changed=copy.deepcopy(action);changed['market']+=extra
    return changed


def _v219_worker(obs, state, actor, role):
    day=int(obs['step'])//24;step=int(obs['step']);view=FarmView(obs)
    pos=tuple(view.positions[actor]);inv=view.inventory(actor)
    targets=role['targets']
    # Actual cargo differences, observed on the next callback, verify harvests.
    previous=state['last_work'].get(actor)
    if previous and previous['step']==step-1 and previous['command']==['HARVEST']:
        _V219_REPORT['confirmed_harvest_units']+=max(0,int(inv.get('TOMATO',0))-previous['tomatoes'])
    if role.get('needs_fertilizer') and not role.get('loaded'):
        home=_v219_home(pos)
        walk=_v219_walk(pos,home)
        if walk:return walk
        desired=role.get('fertilizer_quantity',10 if role['kind']=='fertilizer' else 5)
        if inv.get('FERTILIZER',0)>=desired:role['loaded']=True
        elif role.get('pickup_requested'):
            # Never spend repeated turns waiting for stock that was not bought.
            role['loaded']=True;role['fertilizer_available']=int(inv.get('FERTILIZER',0))
        elif view.shed.get('FERTILIZER',0)>=desired:
            role['pickup_requested']=True;return ['PICKUP','FERTILIZER',desired]
        else:role['loaded']=True
    todo=[]
    for target in targets:
        x,y=target;tile=view.tiles[y][x]
        tomato=isinstance(tile,dict) and tile.get('crop')=='TOMATO'
        if tomato and target not in state['seen_plants']:
            state['seen_plants'].add(target);_V219_REPORT['confirmed_plants']+=1
        if target in state['seen_plants'] and not tomato and target not in state['lost']:
            state['lost'].add(target);_V219_REPORT['lost_plants']+=1
        command=None
        if role['kind']=='fertilizer':
            if tomato and tile.get('fertilized_until_day',-1)<day+2 and inv.get('FERTILIZER',0)>0:
                command=['FERTILIZE']
        elif day==18 and not tomato:
            if tile is None and obs['private']['seeds'].get('TOMATO',0)>0:command=['PLANT','TOMATO']
            elif isinstance(tile,dict) and tile.get('kind')=='WEED':command=['DIG']
        elif tomato:
            # No later production follows the final day, so watering then would
            # consume time needed to harvest and deliver the final cargo.
            if day<29 and not tile.get('watered_today'):command=['WATER']
            elif role.get('needs_fertilizer') and tile.get('fertilized_until_day',-1)<day+2 and inv.get('FERTILIZER',0)>0:
                command=['FERTILIZE']
            elif tile.get('yield_units',0)>0:command=['HARVEST']
        if command:todo.append((target,command))
    # Final return has priority once only the exact distance plus DROP remains.
    home=_v219_home(pos);distance=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    if step>=718-distance and inv.get('TOMATO',0):
        return _v219_walk(pos,home) or ['PLACE','TOMATO',int(inv.get('TOMATO',0))]
    if todo:
        target,command=min(todo,key=lambda v:(abs(pos[0]-v[0][0])+abs(pos[1]-v[0][1]),targets.index(v[0])))
        return _v219_walk(pos,target) or command
    if inv.get('TOMATO',0):return _v219_walk(pos,home) or ['PLACE','TOMATO',int(inv['TOMATO'])]
    if any(inv.values()):return _v219_walk(pos,home) or ['DROP']
    return ['PASS']


def agent(observation, configuration=None):
    action=_V219_PARENT(observation,configuration)
    step=int(observation['step']);player=int(observation['player']);day=step//24
    state=_V219_STATES.get(player)
    if state is None or step<=state['last_step']:
        state={'last_step':step,'day':-1,'workers':{},'last_work':{},'seen_plants':set(),'lost':set(),
               'targets':[(x,y) for y in (5,6) for x in range(5,10)]}
        _V219_STATES[player]=state
    state['last_step']=step
    native=_IMPL.chassis.players[player]
    if step==432:state['eligible']=_v219_qualifies(observation,native)
    if not state.get('eligible') or day<18:return action
    if state['day']!=day:
        state['day']=day;state['workers']={};state['last_work']={}
    farm=observation['farms'][player]
    pending=state.pop('pending',None)
    if pending:
        if len(farm['hands'])+1 >= pending['first_actor']+pending['count'] and 'SE' in farm['unlocked_quadrants']:
            for index in range(pending['count']):
                fertilizer_worker=index==pending['crop_workers']
                if fertilizer_worker:targets=state['targets']
                elif pending['crop_workers']==1:targets=state['targets']
                elif pending['crop_workers']==2:targets=state['targets'][index*5:index*5+5]
                else:targets=[[(5,5),(6,5),(7,5)],[(8,5),(9,5),(9,6),(8,6)],[(5,6),(6,6),(7,6)]][index]
                state['workers'][pending['first_actor']+index]={'kind':'fertilizer' if fertilizer_worker else 'crop','targets':targets,
                    'needs_fertilizer':pending['fertilizer'] and (day==24 or fertilizer_worker)}
                if pending.get('labor') is not None:
                    role=state['workers'][pending['first_actor']+index]
                    role['targets']=[tuple(p) for p in pending['labor']['paths'][index]]
                    role['needs_fertilizer']=pending['labor']['fertilizer'];role['fertilizer_quantity']=len(role['targets'])
                    if tuple(farm['hands'][pending['first_actor']+index-1])!=tuple(pending['labor']['spawns'][index]):_R53_LABOR_REPORT['labor_spawn_errors']+=1
                    if index==0:_R53_LABOR_REPORT['labor_confirmed']+=1
            _V219_REPORT['confirmed_workers']+=pending['count']
        else:_V219_REPORT['hire_shortfalls']+=pending['count']
    action=_v219_request(observation,action,state,native)
    if state['workers']:
        commands=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
        commands += [['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
        for actor,role in state['workers'].items():
            if actor>=len(commands):continue
            command=_v219_worker(observation,state,actor,role)
            commands[actor]=command
            name={'PLANT':'plant_requests','WATER':'water_requests','FERTILIZE':'fertilize_requests',
                  'HARVEST':'harvest_requests','DROP':'drop_requests'}.get(command[0])
            if name:_V219_REPORT[name]+=1
            state['last_work'][actor]={'step':step,'command':command,'tomatoes':observation['private']['inventories'][actor].get('TOMATO',0)}
        action=copy.deepcopy(action);action['farmer'],action['hands']=commands[0],commands[1:]
    if state.get('committed') and len(action['market'])<MAX_ORDERS and not any(o[:2]==['SELL','TOMATO'] for o in action['market']):
        quantity=projected_shed(action,FarmView(observation)).get('TOMATO',0)
        if quantity>0:
            action=copy.deepcopy(action);action['market'].append(['SELL','TOMATO',quantity])
            _V219_REPORT['tomato_sale_requests']+=quantity
    return action


agent.telemetry=_V219_REPORT

# V221B: labor-only ablation of frozen V219G; not yet publicly scored.


# Crop workers own their final routes after commitment. A private parent shadow
# does not contain these obligations, so terminal rescue must abstain there.
_ORIGINAL_SHADOW_TERMINAL=_shadow_terminal
def _shadow_terminal(obs,config):
    if _V219_STATES.get(int(obs['player']),{}).get('committed'):return None
    return _ORIGINAL_SHADOW_TERMINAL(obs,config)

APPLY_TIMING=False

_EXPERIMENT_PARENT=agent
del agent
_V219_REPORT['extra_fertilizer_days']=0
_V219_REPORT['reordered_market_turns']=0
_V219_REPORT['errors']=0
def agent(observation,configuration=None):
    try:
        action=_EXPERIMENT_PARENT(observation,configuration)
        if APPLY_TIMING and int(observation['step'])>=144:action=_v224_sales_first(action)
        return action
    except Exception:
        _V219_REPORT['errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_V219_REPORT

def _v224_sales_first(action):
    original=action.get('market',[])[:MAX_ORDERS]
    orders=[list(o) for o in original if o and (o[0] in ('HIRE','BUY_LAND') or (len(o)>=3 and int(o[2])>0))]
    for index in range(len(orders)):
        order=orders[index]
        if order[0]!='SELL':continue
        cursor=index
        while cursor>0:
            previous=orders[cursor-1]
            if previous[0]=='SELL':break
            if previous[0] in ('BUY_PRODUCT','BUY_ANIMAL') and previous[1]==order[1]:break
            orders[cursor-1],orders[cursor]=orders[cursor],orders[cursor-1]
            cursor-=1
    if orders==original:return action
    _V219_REPORT['reordered_market_turns']+=1
    changed=copy.deepcopy(action);changed['market']=orders
    return changed
_ORDER_PARENT=agent
del agent

def agent(observation,configuration=None):
    try:
        action=_ORDER_PARENT(observation,configuration)
        if int(observation["step"])>=144:action=_v224_sales_first(action)
        return action
    except Exception:
        _V219_REPORT["errors"]+=1
        return {"farmer":["PASS"],"hands":[],"market":[]}
agent.telemetry=_V219_REPORT

_V31_CORE=agent
del agent
_IMPL.chassis.diagnostics['production_errors']=0
_IMPL.chassis.diagnostics['v31_entry_errors']=0
def agent(observation,configuration=None):
    before=_V219_REPORT['errors']
    try:
        action=_V31_CORE(observation,configuration)
        _IMPL.chassis.diagnostics['production_errors']+=_V219_REPORT['errors']-before
        return action
    except Exception:
        _IMPL.chassis.diagnostics['v31_entry_errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_V219_REPORT

# Apache-2.0; later cattle transfer from prvsiyan, Moon (2026-09-10).
# Bounded livestock substitution; confirm owned animals before redirecting workers.
_V231_PARENT=agent
_V231_CAP=4
_V231_STATES={}
_V231_REPORT={}

def _v231_new_state():
    return {'last':-1,'confirmed':0,'reserved':0,'pending_buy':None,
            'carrying':{},'pending_places':[],'sites':{},'milk_credit':0,
            'requested':0,'failed_purchase_units':0,'picked':0,'placed':0,
            'failed_placements':0,'extra_milk_harvested':0,'extra_milk_sale_requests':0}

def _v231_controller(obs,action,state,cap):
    step=int(obs['step']);seat=int(obs['player']);farm=obs['farms'][seat]
    private=obs['private'];shed=private['shed'];inventories=private['inventories']
    positions=[farm['farmer'],*farm['hands']]
    pending=state['pending_buy']
    if pending is not None:
        gained=max(0,int(shed.get('COW',0))-pending['before'])
        confirmed=min(pending['quantity'],gained)
        state['confirmed']+=confirmed;state['reserved']+=confirmed
        state['failed_purchase_units']+=pending['quantity']-confirmed
        state['pending_buy']=None
    for pending in state['pending_places']:
        x,y=pending['site'];tile=farm['tiles'][y][x]
        if (isinstance(tile,dict) and tile.get('animal')=='COW'
                and tile.get('placed_day')==pending['day']):
            state['sites'][(x,y)]=pending['day'];state['placed']+=1
            actor=pending['actor'];state['carrying'][actor]=max(0,state['carrying'].get(actor,0)-1)
        else:state['failed_placements']+=1
    state['pending_places']=[]
    state['last']=step
    result=copy.deepcopy(action)
    workers=[result.get('farmer') or ['PASS'],*(result.get('hands') or [])]
    seen_harvest=set();cow_available=int(shed.get('COW',0));occupied=set()
    for actor,work in enumerate(workers[:len(positions)]):
        inventory=inventories[actor] if actor<len(inventories) else {}
        x,y=positions[actor];tile=farm['tiles'][y][x];site=(x,y)
        if (work==['HARVEST'] and site in state['sites'] and site not in seen_harvest
                and isinstance(tile,dict) and tile.get('animal')=='COW'
                and tile.get('placed_day')==state['sites'][site]):
            units=max(0,int(tile.get('yield_units',0)))
            state['milk_credit']+=units;state['extra_milk_harvested']+=units
            seen_harvest.add(site)
        if len(work)>=2 and work[:2]==['PICKUP','SHEEP']:
            quantity=max(0,int(work[2]) if len(work)>2 else 1)
            center=len(farm['tiles'])//2
            if (quantity and state['reserved']>=quantity and cow_available>=quantity
                    and x in (center-1,center) and y in (center-1,center)
                    and not any(inventory.get(a,0) for a in ('COW','SHEEP','GOOSE'))):
                work[1]='COW';state['reserved']-=quantity;cow_available-=quantity
                state['carrying'][actor]=state['carrying'].get(actor,0)+quantity
                state['picked']+=quantity
        if (len(work)>=2 and work[:2]==['PLACE','SHEEP']
                and state['carrying'].get(actor,0)>0 and inventory.get('COW',0)>0
                and isinstance(tile,dict) and tile.get('kind')=='PASTURE'
                and 'animal' not in tile and site not in occupied):
            work[1]='COW'
            state['pending_places'].append({'actor':actor,'site':site,'day':step//24})
        if (len(work)>=2 and work[0]=='PLACE' and work[1] in ('COW','SHEEP','GOOSE')
                and inventory.get(work[1],0)>0):occupied.add(site)
    result['farmer'],result['hands']=workers[0],workers[1:]
    market=result.get('market',[])
    animal_orders=[o for o in market if len(o)>=3 and o[0]=='BUY_ANIMAL']
    shops=obs['town']['unlocked_shops'];prices=obs['market']['prices']
    counts={'COW':0,'SHEEP':0}
    for line in farm['tiles']:
        for tile in line:
            if isinstance(tile,dict) and tile.get('animal') in counts:counts[tile['animal']]+=1
    cargo=sum(int(inv.get(a,0)) for inv in inventories for a in ('COW','SHEEP','GOOSE'))
    stock_animals=sum(int(shed.get(a,0)) for a in ('COW','SHEEP','GOOSE'))
    milk_shops=sum(shop in ('PIZZA_SHOP','ICE_CREAM_SHOP','SMOOTHIE_SHOP') for shop in shops)
    if (216<=step<=227 and len(shops)>=3 and state['confirmed']<cap and not state['reserved']
            and not any(state['carrying'].values()) and not state['pending_places']
            and not cargo and not stock_animals and len(animal_orders)==1
            and animal_orders[0][1]=='SHEEP' and milk_shops>=2 and 'YARN_STORE' not in shops
            and int(prices.get('MILK',0))>=int(prices.get('WOOL',0))
            and counts['COW']>=4 and counts['SHEEP']>=2):
        order=animal_orders[0];quantity=int(order[2])
        if 1<=quantity<=2 and quantity<=cap-state['confirmed']:
            order[1]='COW';state['requested']+=quantity
            state['pending_buy']={'before':int(shed.get('COW',0)),'quantity':quantity}
    # Sell only additional physically harvested production at an existing sale slot.
    if state['milk_credit']>0:
        stock=projected_shed(result,FarmView(obs))
        total_planned=sum(max(0,int(o[2])) for o in market if len(o)>=3 and o[:2]==['SELL','MILK'])
        extra=min(state['milk_credit'],max(0,int(stock.get('MILK',0))-total_planned))
        if extra:
            for order in market:
                if len(order)>=3 and order[:2]==['SELL','MILK'] and int(order[2])>0:
                    order[2]=int(order[2])+extra
                    state['milk_credit']-=extra;state['extra_milk_sale_requests']+=extra
                    break
    result['market']=market
    return result

def agent(observation,configuration=None):
    step=int(observation['step']);seat=int(observation['player'])
    state=_V231_STATES.get(seat)
    if state is None or step<=state['last']:
        state=_V231_STATES[seat]=_v231_new_state()
    action=_V231_PARENT(observation,configuration)
    action=_v231_controller(observation,action,state,_V231_CAP)
    _V231_REPORT.clear();_V231_REPORT.update(_V231_PARENT.telemetry)
    for name in ('confirmed','reserved','requested','failed_purchase_units','picked','placed',
                 'failed_placements','extra_milk_harvested','extra_milk_sale_requests','milk_credit'):
        _V231_REPORT['cattle_'+name]=state[name]
    _V231_REPORT['cattle_carried_pending']=sum(state['carrying'].values())
    return action

agent.telemetry=_V231_REPORT


# EXP-167, adapted from Dmitrii Gluzdov's Two Coins, One Sheep (Apache-2.0).
# Reserve only physically available stock after the final parent worker actions.
_R36_SALE_PARENT=agent
_R36_NATIVE_LEAD=Chassis._sell_lead
_R36_NATIVE_SUPPRESS=Chassis._apply_suppression
_R36_SALE_REPORT={}

def _r36_native_lead(self,action,view,projected,route,step,next_sup):
    if step<288 or step>=696:
        return _R36_NATIVE_LEAD(self,action,view,projected,route,step,next_sup)

def _r36_suppress(action,state,step):
    _R36_NATIVE_SUPPRESS(action,state,step)
    due=state.get('r36_debts',{}).pop(step,{})
    for order in action.get('market',[]):
        if len(order)>=3 and order[0]=='SELL':
            removed=min(max(0,int(order[2])),due.get(order[1],0))
            order[2]-=removed
            due[order[1]]=due.get(order[1],0)-removed

Chassis._sell_lead=_r36_native_lead
Chassis._apply_suppression=staticmethod(_r36_suppress)

def _r36_reserve(obs,action):
    step=int(obs['step'])
    # The final planner forecasts its own parent, so keep its full window native.
    if not 288<=step<696:return action
    native=_IMPL.chassis.players[int(obs['player'])]
    tape=_IMPL.chassis.routes[native['route']]
    end=min(695,step+_R37_HORIZONS.get(int(obs['player']),2),(step//72+1)*72-1)
    if end<=step:return action
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    view=FarmView(obs)
    # This projection intentionally abstains on ambiguous animal depot returns.
    if any(len(c)>1 and c[0]=='PLACE' and c[1] in ANIMAL_STRUCTURE
           and view.inv(i).get(c[1],0)>0 for i,c in enumerate(commands[:len(view.positions)])):
        return action
    stock=projected_shed(action,view)
    market=action.get('market',[])
    blocked={o[1] for o in market if len(o)>1 and o[0] in ('SELL','BUY_PRODUCT')}
    blocked.update(c[1] for c in commands if len(c)>1 and c[0]=='PICKUP')
    blocked.update(c[1] for queue in native['pending'].values() for pos,c in queue
                   if len(c)>1 and c[0]=='PICKUP')
    debts=native['sell_state'].setdefault('r36_debts',{})
    for item in PRODUCTS:
        if item in ('WHEAT','FERTILIZER') or item in blocked or view.prices.get(item,0)<2:continue
        available=max(0,int(stock.get(item,0)))
        if not available or len(market)>=10:continue
        reservations=[]
        for due_step in range(step+1,end+1):
            future=tape[due_step]
            work=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
            if any(len(c)>1 and c[:2]==['PICKUP',item] for c in work):break
            if any(len(o)>1 and o[:2]==['BUY_PRODUCT',item] for o in future.get('market',[])):break
            planned=sum(max(0,int(o[2])) for o in future.get('market',[]) if len(o)>=3 and o[:2]==['SELL',item])
            amount=min(available,max(0,planned-debts.get(due_step,{}).get(item,0)))
            if amount:
                reservations.append((due_step,amount));available-=amount
            if not available:break
        qty=sum(q for _,q in reservations)
        if qty:
            market.append(['SELL',item,qty])
            for due,q in reservations:
                debt=debts.setdefault(due,{})
                debt[item]=debt.get(item,0)+q
            _R36_SALE_REPORT['sale_reserved_units']+=qty
            _R36_SALE_REPORT['sale_reservations']+=1
    return action

def agent(observation,configuration=None):
    if int(observation.get('step',0))==0:
        _R36_SALE_REPORT.update(sale_reserved_units=0,sale_reservations=0,sale_errors=0)
    action=_R36_SALE_PARENT(observation,configuration)
    try:
        if configuration is None or all(configuration.get(k,v)==v for k,v in
            [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):
            action=_r36_reserve(observation,action)
            if int(observation['step'])>=288:action=_v224_sales_first(action)
    except Exception:
        _R36_SALE_REPORT['sale_errors']=_R36_SALE_REPORT.get('sale_errors',0)+1
    _R36_SALE_REPORT.update(_R36_SALE_PARENT.telemetry)
    return action

agent.telemetry=_R36_SALE_REPORT

# Ensure the Kaggle-selected final callable is the exported policy.
agent = globals().pop("agent")


# Public capability transfer: lucifer19; Flexon is the same Two Coins asset set.
# Apache-2.0; exact functions from Kaggle kaggle-environments 1.32.7.
# https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture
import math
_R37_MARKET_PARAMS = {'WHEAT': {'base': 25, 'I0': 10000, 'T': 400, 'below_func': 'sqrt', 'below_target': 0.8, 'above_func': 'log', 'above_target': 0.2}, 'CARROT': {'base': 35, 'I0': 10000, 'T': 450, 'below_func': 'hinge', 'below_target': 1.0, 'above_func': 'sqrt', 'above_target': 0.7}, 'TOMATO': {'base': 60, 'I0': 10000, 'T': 200, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'sqrt', 'above_target': 0.6}, 'STRAWBERRY': {'base': 120, 'I0': 10000, 'T': 100, 'below_func': 'sqrt', 'below_target': 0.7, 'above_func': 'linear', 'above_target': 1.6}, 'MELON': {'base': 250, 'I0': 10000, 'T': 300, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.6}, 'EGG': {'base': 50, 'I0': 10000, 'T': 332, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'log', 'above_target': 0.2}, 'MILK': {'base': 160, 'I0': 10000, 'T': 122, 'below_func': 'sqrt', 'below_target': 0.6, 'above_func': 'linear', 'above_target': 1.6}, 'WOOL': {'base': 200, 'I0': 10000, 'T': 105, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.2}, 'FERTILIZER': {'base': 100, 'I0': 10000, 'T': 200, 'below_func': 'linear', 'below_target': 0.4, 'above_func': 'linear', 'above_target': 0.4}}
_R37_PRICE_FLOOR = 1
_R37_HINGE_GAIN = 8.0
def _r37_shape(func, x, T=None):
    x = max(0.0, x)
    if func == "linear": return x
    if func == "sq":     return x * x
    if func == "sqrt":   return math.sqrt(x)
    if func == "log":    return math.log(1.0 + x)
    if func == "log10":  return math.log10(1.0 + x)
    if func == "hinge":
        # Degenerates to linear if T is missing or non-positive.
        if not T or T <= 0:
            return x
        u = x / T
        return u + _R37_HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x

def _r37_market_price(item, inventory, params=None):
    """Floor at _R37_PRICE_FLOOR."""
    p = (params or _R37_MARKET_PARAMS)[item]
    base = p["base"]
    I0 = p["I0"]
    T = p["T"]
    if inventory < I0:
        f = p["below_func"]
        amp = p["below_target"] * base / _r37_shape(f, T, T)
        price = base + amp * _r37_shape(f, I0 - inventory, T)
    else:
        f = p["above_func"]
        amp = p["above_target"] * base / _r37_shape(f, T, T)
        price = base - amp * _r37_shape(f, inventory - I0, T)
    return max(_R37_PRICE_FLOOR, int(round(price)))

def _r37_similarity(observation):
    """Empty tiles cannot make two unrelated production layouts look alike."""
    farms = observation['farms']
    own, rival = farms[observation['player']], farms[1-observation['player']]
    if own['unlocked_quadrants'] != rival['unlocked_quadrants']:
        return 0.0
    matches = total = 0
    for a, b in zip([t for row in own['tiles'] for t in row],
                    [t for row in rival['tiles'] for t in row]):
        sa = (a.get('crop'), a.get('animal')) if isinstance(a, dict) else (None, None)
        sb = (b.get('crop'), b.get('animal')) if isinstance(b, dict) else (None, None)
        if sa != (None, None) or sb != (None, None):
            total += 1
            matches += sa == sb
    return matches / total if total >= 8 else 0.0


def _r37_quote_priority(observation, order, stock):
    """Revenue exposed to a small rival batch, not nominal headline revenue."""
    item = order[1]
    quantity = min(max(0, int(order[2])), stock.get(item, 0))
    if not quantity or item not in _R37_MARKET_PARAMS:
        return 0.0
    inventory = observation['market']['inventory'][item]
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for k, patch in observation['market'].get('params', {}).items():
        if k in params:
            params[k].update(patch)
    rival = observation['farms'][1-observation['player']]
    crop_item = item if item in ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON') else None
    animal = {'EGG':'GOOSE','MILK':'COW','WOOL':'SHEEP'}.get(item)
    standing = sum(max(0, int(t.get('yield_units', 0))) for row in rival['tiles'] for t in row
                   if isinstance(t, dict) and
                   ((crop_item is not None and t.get('crop') == crop_item) or
                    (animal is not None and t.get('animal') == animal)))
    # Public fields do not reveal the rival shed. Eight units are a scenario,
    # not a recovered hidden quantity; visible ripe yield increases the stress.
    batch = min(24, max(8, standing))
    now = sum(_r37_market_price(item, inventory+j, params) for j in range(quantity))
    later = sum(_r37_market_price(item, inventory+batch+j, params) for j in range(quantity))
    return now-later


def _r37_reorder_sales(observation, action):
    """Keep quantities and purchase barriers; rank distinct contiguous sales."""
    stock = projected_shed(action, FarmView(observation))
    orders = [list(o) for o in action['market']]
    start = 0
    while start < len(orders):
        if orders[start][0] != 'SELL':
            start += 1
            continue
        end = start
        while end < len(orders) and orders[end][0] == 'SELL':
            end += 1
        block = orders[start:end]
        if len({o[1] for o in block}) == len(block):
            orders[start:end] = sorted(block, key=lambda o: _r37_quote_priority(observation, o, stock), reverse=True)
        start = end
    if orders != action['market']:
        _R37_STATS['quote_reordered_turns'] += 1
        action = dict(action, market=orders)
    return action



# EXP175: bounded public cash-response probe inspired by leoprovorov,
# Two Coins Mirror Counter v1 (Apache-2.0). No hidden rival inventory.
_R44_PROBES={}
_R44_REPORT=dict(probe_matches=0,probe_four_turn_calls=0,probe_errors=0)

def _r44_before(obs):
    player=int(obs['player']);step=int(obs['step'])
    st=_R44_PROBES.get(player)
    if st is None or step<=st['step']:
        st=_R44_PROBES[player]={'step':-1,'money':None,'probe':0,'matched':False}
    if step==0:_R44_REPORT.update(probe_matches=0,probe_four_turn_calls=0,probe_errors=0)
    money=tuple(float(obs['farms'][i]['money']) for i in (player,1-player))
    if st['money'] is not None and st['probe']>=100 and _r37_similarity(obs)>=.90:
        own=money[0]-st['money'][0];rival=money[1]-st['money'][1]
        if own>0 and rival>0 and abs(own-rival)<=max(5.0,.05*st['probe']):
            if not st['matched']:_R44_REPORT['probe_matches']+=1
            st['matched']=True
    st.update(step=step,money=money,probe=0)
    return st

def _r44_after(obs,action,st):
    step=int(obs['step']);player=int(obs['player'])
    if not 336<=step<648 or st['matched']:return
    # Positive all-sale probes avoid mistaking equal spending for preemption.
    if not action['market'] or any(o and o[0]!='SELL' for o in action['market']):return
    debts=_IMPL.chassis.players[player]['sell_state'].get('r36_debts',{})
    own=debts.get(step+3,{})
    if own:st['probe']=sum(max(0,int(n))*int(obs['market']['prices'].get(item,0)) for item,n in own.items())

_R37_ADAPTIVE = True
_R37_QUOTE = True
# EXP-168: adapted from lucifer19 / Harvest Nocturne, Apache-2.0.
# All rivalry features use public occupied tiles; no private rival inventory.
_R37_PARENT = agent
_R37_PLAYERS = {}
_R37_HORIZONS = {}
_R37_REPORT = {}
_R37_STATS = dict(quote_reordered_turns=0, three_turn_calls=0, nocturne_errors=0)
del agent

def agent(observation, configuration=None):
    player, step = int(observation['player']), int(observation['step'])
    state = _R37_PLAYERS.get(player)
    if state is None or step <= state['step']:
        state = _R37_PLAYERS[player] = {'step': -1, 'streak': 0}
    if step == 0:
        _R37_STATS.update(quote_reordered_turns=0, three_turn_calls=0, nocturne_errors=0)
    state['step'] = step
    _R37_HORIZONS[player] = 2
    probe_state=_r44_before(observation)
    try:
        if _R37_ADAPTIVE and step < 648:
            state['streak'] = state['streak'] + 1 if _r37_similarity(observation) >= .90 else 0
            if 336 <= step < 648 and state['streak'] >= 6:
                _R37_HORIZONS[player] = 3
                _R37_STATS['three_turn_calls'] += 1
    except Exception:
        _R37_STATS['nocturne_errors'] += 1
    if _R37_HORIZONS[player]==3 and probe_state['matched']:
        _R37_HORIZONS[player]=4
        _R44_REPORT['probe_four_turn_calls']+=1
    # EXP179: four-turn reservation; retain stock, debt and purchase barriers.
    if 288 <= step < 696:_R37_HORIZONS[player] = 4
    action = _R37_PARENT(observation, configuration)
    _r44_after(observation,action,probe_state)
    if _R37_QUOTE and step >= 288:
        try:
            action = _r37_reorder_sales(observation, action)
        except Exception:
            _R37_STATS['nocturne_errors'] += 1
    _R37_REPORT.update(getattr(_R37_PARENT, 'telemetry', {}))
    _R37_REPORT.update(_R37_STATS)
    _R37_REPORT.update(_R44_REPORT)
    return action

agent.telemetry = _R37_REPORT

# Export guard: normal decisions stay identical to the frozen screened policy.
_RELEASE_PARENT=agent
_RELEASE_REPORT={}
_RELEASE_ERRORS=0
del agent

def agent(observation,configuration=None):
    global _RELEASE_ERRORS
    try:
        result=_RELEASE_PARENT(observation,configuration)
    except Exception:
        _RELEASE_ERRORS+=1
        count=0
        try:
            count=min(64,len(observation['farms'][int(observation['player'])]['hands']))
        except Exception:
            pass
        result={'farmer':['PASS'],'hands':[['PASS'] for _ in range(count)],'market':[]}
    _RELEASE_REPORT.update(getattr(_RELEASE_PARENT,'telemetry',{}))
    _RELEASE_REPORT['release_errors']=_RELEASE_ERRORS
    return result

agent.telemetry=_RELEASE_REPORT
agent=globals().pop('agent')

# Adapted from prvsiyan / The Soil Remembers Rain, Apache-2.0.
# V233: bounded, financed six-sheep SE discovery investment.
_V233_PARENT=agent
del agent
_V233_STATES={}
_V233_REPORT=dict(sheep_commit_requests=0,sheep_committed=0,sheep_hire_requests=0,
    sheep_workers_confirmed=0,sheep_hire_shortfalls=0,sheep_budget_declines=0,
    sheep_capacity_declines=0,sheep_purchase_shortfalls=0,sheep_feed_buy_requests=0,
    sheep_wool_harvested=0,sheep_fert_collected=0,sheep_extra_wool_sales=0,
    sheep_extra_fert_sales=0,sheep_rescue_feed_requests=0)

def _v233_eligible(obs,native):
    farm=obs['farms'][obs['player']];prices=obs['market']['prices']
    if len(farm['tiles'])!=10 or set(farm['unlocked_quadrants'])!={'NW','NE','SW'}:return False
    if obs['town']['unlocked_shops'].count('YARN_STORE')<2 or prices['WOOL']<220 or prices['WHEAT']>45:return False
    if any(farm['tiles'][y][x]!='LOCKED' for y in (5,6) for x in range(5,8)):return False
    if obs['private']['shed'].get('SHEEP',0) or any(i.get('SHEEP',0) for i in obs['private']['inventories']):return False
    for day in range(12,30):
        for a in _v219_native_day(native,day):
            if any(o and (o[0]=='BUY_LAND' or o[:2]==['BUY_ANIMAL','SHEEP']) for o in a.get('market',[])):return False
            if any(c and c[0] in ('PICKUP','PLACE') and len(c)>1 and c[1]=='SHEEP' for c in [a.get('farmer')]+a.get('hands',[])):return False
    return True

def _v233_request(obs,action,state,native):
    step=int(obs['step']);day=step//24;hour=step%24
    if hour>(2 if state.get('committed') else 1) or state.get('requested_day')==day:return action
    if not state.get('committed') and (day!=12 or not _v233_eligible(obs,native)):return action
    planned=_v219_native_day(native,day)
    if any(o and o[0]=='HIRE' for a in planned[hour+1:] for o in a.get('market',[])):return action
    farm=obs['farms'][obs['player']];market=action.get('market',[])
    parent_hires=sum(bool(o) and o[0]=='HIRE' for o in market)
    expected=max(len(a.get('hands',[])) for a in planned)
    if len(farm['hands'])+parent_hires!=expected:return action
    initial=not state.get('committed')
    extra=([['BUY_LAND'],['BUY_ANIMAL','SHEEP',6]] if initial else [])+[['BUY_PRODUCT','WHEAT',6],['HIRE'],['HIRE']]
    if len(market)+len(extra)>MAX_ORDERS:return action
    stock=projected_shed(action,FarmView(obs))
    incoming=6+6*initial
    budget=7000*initial+6*(int(obs['market']['prices']['WHEAT'])+10)
    budget+=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+parent_hires+2))
    for o in market:
        if not o:continue
        if o[0]=='BUY_LAND':return action
        if o[0]=='BUY_PRODUCT':
            incoming+=int(o[2]);budget+=int(o[2])*(int(obs['market']['prices'][o[1]])+10)
        elif o[0]=='BUY_ANIMAL':
            incoming+=int(o[2]);budget+=int(o[2])*{'SHEEP':500,'COW':400,'GOOSE':300}[o[1]]
        elif o[0]=='BUY_SEED':budget+=int(o[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[o[1]]
    if sum(stock.values())+incoming>100:
        _V233_REPORT['sheep_capacity_declines']+=1;return action
    if farm['money']<budget+(3000 if initial else 1000):
        _V233_REPORT['sheep_budget_declines']+=1;return action
    state['requested_day']=day
    state['pending']={'first':expected+1,'initial':initial}
    _V233_REPORT['sheep_hire_requests']+=2;_V233_REPORT['sheep_feed_buy_requests']+=6
    if initial:_V233_REPORT['sheep_commit_requests']+=1
    result=copy.deepcopy(action);result['market']=market+extra
    return result

def _v233_worker(obs,actor,targets):
    farm=obs['farms'][obs['player']];private=obs['private'];step=int(obs['step'])
    pos=tuple(farm['hands'][actor-1]);inv=private['inventories'][actor]
    access=((4,4),(5,4),(4,5),(5,5))
    home=min(access,key=lambda p:(abs(pos[0]-p[0])+abs(pos[1]-p[1]),p))
    distance=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    cargo=[item for item in ('WOOL','FERTILIZER') if inv.get(item,0)]
    if cargo and step%24 >= (22 if step//24==29 else 23)-distance:
        return _v219_walk(pos,home) or ['PLACE',cargo[0],inv[cargo[0]]]
    missing=sum(not(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='SHEEP') for x,y in targets)
    if missing and not inv.get('SHEEP',0) and private['shed'].get('SHEEP',0):
        return _v219_walk(pos,home) or ['PICKUP','SHEEP',min(missing,private['shed']['SHEEP'])]
    hungry=sum(not(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('fed_today')) for x,y in targets)
    if hungry and not inv.get('WHEAT',0) and private['shed'].get('WHEAT',0):
        return _v219_walk(pos,home) or ['PICKUP','WHEAT',min(hungry,private['shed']['WHEAT'])]
    tasks=[]
    for target in targets:
        x,y=target;tile=farm['tiles'][y][x];command=None
        if tile is None:command=['BUILD_PASTURE']
        elif isinstance(tile,dict) and tile.get('kind')=='WEED':command=['DIG']
        elif isinstance(tile,dict) and tile.get('kind')=='PASTURE' and not tile.get('animal'):
            if inv.get('SHEEP',0):command=['PLACE','SHEEP']
        elif isinstance(tile,dict) and tile.get('animal')=='SHEEP':
            if not tile['fed_today'] and inv.get('WHEAT',0):command=['FEED']
            elif not tile['cared_today']:command=['CARE']
            elif tile['yield_units']:command=['HARVEST']
            elif tile['fertilizer_available']:command=['COLLECT_FERTILIZER']
        if command:tasks.append((abs(pos[0]-x)+abs(pos[1]-y),targets.index(target),target,command))
    if tasks:
        _,_,target,command=min(tasks);return _v219_walk(pos,target) or command
    if cargo:return _v219_walk(pos,home) or ['PLACE',cargo[0],inv[cargo[0]]]
    return ['PASS']

def _v234_rescue(obs,action,state):
    if not state['workers'] or int(obs['step'])%24>14:return action
    orders=action.get('market',[])
    if len(orders)>=MAX_ORDERS:return action
    if any(o and (o[0] in ('HIRE','BUY_LAND','BUY_ANIMAL','BUY_PRODUCT','BUY_SEED') or (len(o)>1 and o[1]=='WHEAT')) for o in orders):return action
    farm=obs['farms'][obs['player']];private=obs['private'];hungry=carried=0
    commands=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
    for actor,targets in state['workers'].items():
        command=commands[actor]
        if command==['FEED'] or command[:2]==['PICKUP','WHEAT']:return action
        carried+=private['inventories'][actor].get('WHEAT',0)
        hungry+=sum(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='SHEEP' and not farm['tiles'][y][x].get('fed_today') for x,y in targets)
    stock=projected_shed(action,FarmView(obs))
    shortage=hungry-carried-stock.get('WHEAT',0)
    if not 0<shortage<=6 or state.get('rescue_today',0)+shortage>6:return action
    quote=int(obs['market']['prices']['WHEAT'])
    if quote<1 or farm['money']<1000+shortage*(quote+10) or sum(stock.values())+shortage>100:return action
    result=copy.deepcopy(action);result['market'].append(['BUY_PRODUCT','WHEAT',shortage])
    state['rescue_today']=state.get('rescue_today',0)+shortage
    _V233_REPORT['sheep_rescue_feed_requests']+=shortage
    return result

def agent(observation,configuration=None):
    action=_V233_PARENT(observation,configuration)
    step=int(observation['step']);player=int(observation['player']);day=step//24
    state=_V233_STATES.get(player)
    if state is None or step<=state['last_step']:
        state={'last_step':step,'day':-1,'workers':{},'work':{},'credit':{'WOOL':0,'FERTILIZER':0}}
        _V233_STATES[player]=state
    state['last_step']=step
    if configuration is not None and any(configuration.get(k,v)!=v for k,v in
        (('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10))):return action
    if day<12:return action
    farm=observation['farms'][player];private=observation['private']
    if state['day']!=day:state['day']=day;state['workers']={};state['work']={};state['rescue_today']=0
    for actor,previous in state['work'].items():
        if previous['step']!=step-1 or actor>=len(private['inventories']):continue
        item={'HARVEST':'WOOL','COLLECT_FERTILIZER':'FERTILIZER'}.get(previous['command'][0])
        if item:
            gained=max(0,private['inventories'][actor].get(item,0)-previous['inventory'].get(item,0))
            state['credit'][item]+=gained
            _V233_REPORT['sheep_wool_harvested' if item=='WOOL' else 'sheep_fert_collected']+=gained
    pending=state.pop('pending',None)
    if pending:
        funded='SE' in farm['unlocked_quadrants'] and (not pending['initial'] or private['shed'].get('SHEEP',0)>=6)
        if not funded:_V233_REPORT['sheep_purchase_shortfalls']+=1
        elif len(farm['hands'])<pending['first']+1:_V233_REPORT['sheep_hire_shortfalls']+=1
        else:
            for i in range(2):state['workers'][pending['first']+i]=[(x,5+i) for x in range(5,8)]
            _V233_REPORT['sheep_workers_confirmed']+=2
            if pending['initial']:state['committed']=True;_V233_REPORT['sheep_committed']+=1
    action=_v233_request(observation,action,state,_IMPL.chassis.players[player])
    if not state.get('committed'):return action
    result=copy.deepcopy(action)
    commands=[result.get('farmer') or ['PASS']]+list(result.get('hands') or [])
    commands += [['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
    state['work']={}
    for actor,targets in state['workers'].items():
        command=_v233_worker(observation,actor,targets);commands[actor]=command
        state['work'][actor]={'step':step,'command':command,'inventory':dict(private['inventories'][actor])}
    result['farmer'],result['hands']=commands[0],commands[1:]
    result=_v234_rescue(observation,result,state)
    stock=projected_shed(result,FarmView(observation))
    for item in ('WOOL','FERTILIZER'):
        scheduled=sum(int(o[2]) for o in result['market'] if o[:2]==['SELL',item])
        count=min(state['credit'][item],max(0,stock.get(item,0)-scheduled))
        if count and len(result['market'])<MAX_ORDERS:
            result['market'].append(['SELL',item,count]);state['credit'][item]-=count
            _V233_REPORT['sheep_extra_wool_sales' if item=='WOOL' else 'sheep_extra_fert_sales']+=count
    return result

_R46_SHEEP_AGENT=agent
_R46_SHADOW_PARENT=_shadow_terminal
_R46_REPORT={}
def _shadow_terminal(obs,config):
    if _V233_STATES.get(int(obs['player']),{}).get('committed'):return None
    return _R46_SHADOW_PARENT(obs,config)
del agent
def agent(observation,configuration=None):
    try:
        if int(observation.get('step',-1))==0:
            for k in _V233_REPORT:_V233_REPORT[k]=0
        result=_R46_SHEEP_AGENT(observation,configuration)
    except Exception:
        _R46_REPORT['sheep_overlay_errors']=_R46_REPORT.get('sheep_overlay_errors',0)+1
        result={'farmer':['PASS'],'hands':[],'market':[]}
    _R46_REPORT.update(getattr(_V233_PARENT,'telemetry',{}))
    _R46_REPORT.update(_V233_REPORT)
    return result
agent.telemetry=_R46_REPORT
agent=globals().pop('agent')

# EXP182: finite-harvest wheat/carrot input planner; original adaptation.
_R51_INPUT_PARENT=agent
_R51_INPUT_STATES={}
_R51_INPUT_REPORT={}
_R51_INPUT_MAX_WORKERS=2
_R51_INPUT_CROPS={'WHEAT':(2,4,6),'CARROT':(2,3,4)}

def _r51_input_forecast(obs,route,expected):
    step=int(obs['step']);day=step//24;farm=obs['farms'][obs['player']]
    pos=[list(farm['farmer'])]+[list(p) for p in farm['hands'][:expected]];targets={}
    for y,line in enumerate(farm['tiles']):
        for x,tile in enumerate(line):
            if not isinstance(tile,dict) or tile.get('crop') not in _R51_INPUT_CROPS:continue
            item=tile['crop'];first,last,cap=_R51_INPUT_CROPS[item]
            if 1<=day-tile['planted_day']<last:
                targets[(x,y)]={'crop':item,'birth':tile['planted_day'],'yield':tile['yield_units'],
                    'until':tile.get('fertilized_until_day',-1),'watered':tile.get('watered_today',False),'water':[],'harvest':None,'first':first,'last':last,'cap':cap}
    access=((4,4),(5,4),(4,5),(5,5));seen=set()
    # Native continuation ends before the reactive terminal closure planner.
    for t in range(step,min(712,(day+4)*24)):
        tape=_IMPL.chassis.routes[2 if t>=648 else route];a=tape[t]
        for actor,c in enumerate([a.get('farmer') or ['PASS'],*(a.get('hands') or [])][:len(pos)]):
            if not c:continue
            xy=tuple(pos[actor]);target=targets.get(xy)
            if target is not None and target['harvest'] is None:
                if c[0]=='WATER' and (t//24,xy) not in seen:
                    seen.add((t//24,xy))
                    if not(t//24==day and target['watered']) and target['first']<=t//24-target['birth']<=target['last']:target['water'].append(t)
                if c[0]=='HARVEST':target['harvest']=t
            if c[0] in MOVES:
                dx,dy=MOVES[c[0]];pos[actor]=[max(0,min(9,pos[actor][0]+dx)),max(0,min(9,pos[actor][1]+dy))]
        for o in a.get('market',[]):
            if o and o[0]=='HIRE':
                counts={p:sum(tuple(q)==p for q in pos) for p in access}
                pos.append(list(min(access,key=lambda p:(counts[p],access.index(p)))))
        if (t+1)%24==0:pos=[[4,4]]
    return targets

def _r51_input_gain(target,arrival,day):
    if target['harvest'] is None or target['harvest']<=arrival:return 0
    extra=sum(arrival<t<=target['harvest'] and day<=t//24<=day+2 and t//24>target['until'] for t in target['water'])
    baseline=target['yield']+sum(2 if t//24<=target['until'] else 1 for t in target['water'])
    return max(0,min(extra,target['cap']-baseline))

def _r51_input_path(obs,targets):
    step=int(obs['step']);day=step//24;now=step+4;pos=(4,4);remaining=dict(targets);path=[];quantities={'WHEAT':0,'CARROT':0}
    while remaining and len(path)<8:
        options=[]
        for xy,target in remaining.items():
            arrival=now+abs(pos[0]-xy[0])+abs(pos[1]-xy[1]);gain=_r51_input_gain(target,arrival,day)
            price=max(1,int(obs['market']['prices'][target['crop']])-2)
            if gain and arrival<day*24+23:options.append((gain*price/(arrival-now+1),gain*price,-arrival,xy,arrival,gain))
        if not options:break
        _,_,_,xy,arrival,gain=max(options);target=remaining.pop(xy)
        path.append((xy[0],xy[1],target['crop'],target['birth']));quantities[target['crop']]+=gain;now=arrival+1;pos=xy
    return path,quantities

def _r51_input_control(obs,action,state):
    step=int(obs['step']);day=step//24;hour=step%24;player=int(obs['player']);farm=obs['farms'][player];private=obs['private']
    native=_IMPL.chassis.players[player]
    if state.get('day')!=day:state.update(day=day,workers={},pending=None,placed=[])
    for x,y in state['placed']:
        tile=farm['tiles'][y][x]
        if isinstance(tile,dict) and tile.get('fertilized_until_day',-1)>=day+2:_R51_INPUT_REPORT['input_confirmed_applications']+=1
        else:_R51_INPUT_REPORT['input_application_errors']+=1
    state['placed']=[]
    if state.get('pending'):
        pending=state.pop('pending')
        for actor,plan in pending.items():
            if len(farm['hands'])>=actor:state['workers'][actor]=plan;_R51_INPUT_REPORT['input_confirmed_hires']+=1
            else:_R51_INPUT_REPORT['input_hire_errors']+=1
    if state['workers']:
        changed=copy.deepcopy(action)
        for actor,plan in state['workers'].items():
            inv=private['inventories'][actor];pos=tuple(farm['hands'][actor-1]);cmd=['PASS']
            if not plan['loaded']:
                stock=projected_shed(changed,FarmView(obs));q=min(plan['quantity'],max(0,stock.get('FERTILIZER',0)))
                if q and _shed_adjacent(pos,10):
                    cmd=['PICKUP','FERTILIZER',q];plan['loaded']=True;_R51_INPUT_REPORT['input_loaded_units']+=q
                    if q<plan['quantity']:_R51_INPUT_REPORT['input_stock_shortfalls']+=plan['quantity']-q
            elif inv.get('FERTILIZER',0):
                while plan['path']:
                    x,y,crop,birth=plan['path'][0];tile=farm['tiles'][y][x]
                    if not isinstance(tile,dict) or tile.get('crop')!=crop or tile.get('planted_day')!=birth or tile.get('fertilized_until_day',-1)>=day+2:
                        plan['path'].pop(0);continue
                    cmd=_v219_walk(pos,(x,y)) or ['FERTILIZE']
                    if cmd==['FERTILIZE']:state['placed'].append((x,y));plan['path'].pop(0);_R51_INPUT_REPORT['input_application_requests']+=1
                    break
            changed['hands'][actor-1]=cmd
        return changed
    if hour not in (1,2,3) or not 12<=day<=28:return action
    planned=_v219_native_day(native,day);expected=max(len(a.get('hands',[])) for a in planned)
    if any(o and o[0]=='HIRE' for a in planned[hour:] for o in a.get('market',[])) or native['pending']:return action
    parents=[_V219_STATES.get(player,{}),_V233_STATES.get(player,{})]
    # A parent may retry after a full market queue; its headcount must remain native.
    if day in (12,18) or any(p.get('committed') and p.get('requested_day')!=day for p in parents):return action
    if any(p.get('pending') for p in parents) or any(o and o[0]=='HIRE' for o in action.get('market',[])):return action
    owned=set(range(1,expected+1))
    for p in parents:
        actors=set(p.get('workers',{}))
        if owned&actors:return action
        owned|=actors
    if owned!=set(range(1,len(farm['hands'])+1)):return action
    targets=_r51_input_forecast(obs,native['route'],expected);plans=[];total_q=0;total_cost=0;all_units={'WHEAT':0,'CARROT':0}
    stock=projected_shed(action,FarmView(obs));purchases=sum(max(0,int(o[2])) for o in action.get('market',[]) if len(o)>2 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL'))
    # Units act before market orders. Preserve the native next-turn pickup,
    # after the current parent's actual sales/purchases, before buying tour inputs.
    available=max(0,stock.get('FERTILIZER',0))
    for o in action.get('market',[]):
        if len(o)>=3 and o[:2]==['SELL','FERTILIZER']:available=max(0,available-max(0,int(o[2])))
        elif len(o)>=3 and o[:2]==['BUY_PRODUCT','FERTILIZER']:available+=max(0,int(o[2]))
    next_native=planned[hour+1];native_pickups=sum(max(0,int(c[2]) if len(c)>2 else 1) for c in [next_native.get('farmer') or ['PASS'],*(next_native.get('hands') or [])] if len(c)>1 and c[:2]==['PICKUP','FERTILIZER'])
    topup=max(0,native_pickups-available)
    for i in range(_R51_INPUT_MAX_WORKERS):
        path,units=_r51_input_path(obs,targets);q=len(path)
        if q<3 or len(action.get('market',[]))+2+i>10 or sum(stock.values())+purchases+total_q+q+topup>95:break
        quote=_r37_market_price('FERTILIZER',obs['market']['inventory']['FERTILIZER']-total_q-q-topup)
        cost=(q+(topup if i==0 else 0))*(quote+2)+_v219_fib(int(farm['hires_today'])+i)
        value=sum(n*max(1,_r37_market_price(item,obs['market']['inventory'][item]+all_units[item]+n)-2) for item,n in units.items())
        if value<1.5*cost+50 or farm['money']<total_cost+cost+3000:break
        plans.append({'path':path,'quantity':q,'loaded':False});total_q+=q;total_cost+=cost
        for item,n in units.items():all_units[item]+=n
        for x,y,_,_ in path:targets.pop((x,y),None)
    if not plans:return action
    state['pending']={len(farm['hands'])+1+i:plan for i,plan in enumerate(plans)}
    _R51_INPUT_REPORT['input_hire_requests']+=len(plans);_R51_INPUT_REPORT['input_purchase_requests']+=total_q+topup
    _R51_INPUT_REPORT['input_forecast_wheat']+=all_units['WHEAT'];_R51_INPUT_REPORT['input_forecast_carrot']+=all_units['CARROT']
    changed=copy.deepcopy(action);changed['market'] += [['BUY_PRODUCT','FERTILIZER',total_q+topup]]+[['HIRE'] for _ in plans];return changed

def agent(observation,configuration=None):
    try:
        step=int(observation['step']);player=int(observation['player']);state=_R51_INPUT_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R51_INPUT_STATES[player]={'step':-1}
            _R51_INPUT_REPORT.update(input_hire_requests=0,input_confirmed_hires=0,input_hire_errors=0,input_purchase_requests=0,
                input_loaded_units=0,input_stock_shortfalls=0,input_application_requests=0,input_confirmed_applications=0,
                input_application_errors=0,input_errors=0,input_forecast_wheat=0,input_forecast_carrot=0)
        state['step']=step;action=_R51_INPUT_PARENT(observation,configuration)
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):
            action=_r51_input_control(observation,action,state)
        _R51_INPUT_REPORT.update(getattr(_R51_INPUT_PARENT,'telemetry',{}));return action
    except Exception:
        _R51_INPUT_REPORT['input_errors']=_R51_INPUT_REPORT.get('input_errors',0)+1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_R51_INPUT_REPORT
agent=globals().pop('agent')

# EXP182: project the final hour's actual worker actions before automatic deposit.
_R51_WAREHOUSE_PARENT=agent
_R51_WAREHOUSE_REPORT={}

def _r51_close_warehouse(obs,action):
    step=int(obs['step']);day=step//24
    if step%24!=23 or not 12<=day<=28:return action
    # No speculative product purchase/worker count model: these hours abstain.
    if any(o and o[0] not in ('SELL',) for o in action.get('market',[])):return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    blocked={k for k,q in demand.items() if q>private['seeds'].get(k,0)}
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        if len(c)>1 and c[0]=='PLANT' and c[1] in blocked:c=['PASS']
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,day,24,100)
    post=dict(private['shed'])
    for o in action.get('market',[]):
        if len(o)>=3 and o[0]=='SELL':post[o[1]]=max(0,post.get(o[1],0)-max(0,int(o[2])))
    needed=sum(post.values())+sum(max(0,q) for inv in private['inventories'] for q in inv.values())-100
    if needed<=0:return action
    result=copy.deepcopy(action);orders=result['market']
    # Grain and fertilizer have native input obligations; other products do not.
    # Additional commodity sales are bounded by actual post-action physical stock.
    for item in sorted((p for p in PRODUCTS if p not in ('WHEAT','FERTILIZER')),key=lambda p:-obs['market']['prices'].get(p,0)):
        qty=min(needed,post.get(item,0))
        if not qty:continue
        existing=next((o for o in orders if len(o)>=3 and o[:2]==['SELL',item]),None)
        if existing is not None:existing[2]=max(0,int(existing[2]))+qty
        elif len(orders)<10:orders.append(['SELL',item,qty])
        else:continue
        needed-=qty;post[item]-=qty;_R51_WAREHOUSE_REPORT['warehouse_extra_sales']+=qty
        if needed<=0:break
    if needed>0:
        native=_IMPL.chassis.players[int(obs['player'])];reserve=0
        for t in range(step+1,719):
            future=_IMPL.chassis.routes[2 if t>=648 else native['route']][t]
            for c in [future.get('farmer') or ['PASS'],*(future.get('hands') or [])]:
                if len(c)>1 and c[:2]==['PICKUP','WHEAT']:reserve+=max(0,int(c[2]) if len(c)>2 else 1)
            if any(len(o)>1 and o[:2]==['BUY_PRODUCT','WHEAT'] for o in future.get('market',[])):break
        incoming=sum(max(0,inv.get('WHEAT',0)) for inv in private['inventories'])
        others=sum(q for p,q in post.items() if p!='WHEAT')+sum(max(0,q) for inv in private['inventories'] for p,q in inv.items() if p!='WHEAT')
        # Even if every other carried item deposits first, this grain reserve fits.
        qty=min(needed,post.get('WHEAT',0),max(0,post.get('WHEAT',0)+incoming-reserve)) if 100-others>=reserve else 0
        existing=next((o for o in orders if len(o)>=3 and o[:2]==['SELL','WHEAT']),None)
        if qty and (existing is not None or len(orders)<10):
            if existing is not None:existing[2]=max(0,int(existing[2]))+qty
            else:orders.append(['SELL','WHEAT',qty])
            needed-=qty;_R51_WAREHOUSE_REPORT['warehouse_extra_sales']+=qty
    _R51_WAREHOUSE_REPORT['warehouse_projected_unresolved']+=max(0,needed)
    if result!=action:_R51_WAREHOUSE_REPORT['warehouse_changed_turns']+=1
    return result

def agent(observation,configuration=None):
    result=_R51_WAREHOUSE_PARENT(observation,configuration)
    try:
        if int(observation['step'])==0:_R51_WAREHOUSE_REPORT.update(warehouse_changed_turns=0,warehouse_extra_sales=0,warehouse_projected_unresolved=0,warehouse_errors=0)
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):result=_r51_close_warehouse(observation,result)
    except Exception:_R51_WAREHOUSE_REPORT['warehouse_errors']=_R51_WAREHOUSE_REPORT.get('warehouse_errors',0)+1
    _R51_WAREHOUSE_REPORT.update(getattr(_R51_WAREHOUSE_PARENT,'telemetry',{}));return result
agent.telemetry=_R51_WAREHOUSE_REPORT
agent=globals().pop('agent')

from itertools import permutations as _r53_permutations
_R53_LABOR_REPORT=dict(labor_requests=0,labor_hires_avoided=0,labor_spawn_errors=0,labor_confirmed=0,labor_day26=0,labor_day27=0,labor_day28=0)

def _r53_labor_assignment(obs,action,fertilizer):
    step=int(obs['step']);day=step//24;farm=obs['farms'][obs['player']]
    if day not in (26,27,28) or step%24>2:return None
    # Do not preempt a later price-gated fertilizer request with a smaller unfertilized team.
    if day==27 and not fertilizer:return None
    count=3 if fertilizer else 2
    positions=[list(farm['farmer'])]+[list(p) for p in farm['hands']]
    for i,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])][:len(positions)]):
        if c and c[0] in MOVES:
            dx,dy=MOVES[c[0]];positions[i]=[max(0,min(9,positions[i][0]+dx)),max(0,min(9,positions[i][1]+dy))]
    access=((4,4),(5,4),(4,5),(5,5));spawns=[]
    native_hires=sum(bool(o) and o[0]=='HIRE' for o in action.get('market',[]))
    for i in range(native_hires+count):
        chosen=min(access,key=lambda p:(sum(tuple(q)==p for q in positions),access.index(p)));positions.append(list(chosen))
        if i>=native_hires:spawns.append(chosen)
    groups=(((5,5),(6,5),(7,5),(8,5)),((9,5),(9,6),(8,6)),((5,6),(6,6),(7,6))) if fertilizer else (tuple((x,5) for x in range(5,10)),tuple((x,6) for x in range(5,10)))
    choices=[];remaining=23-step%24
    for assignment in _r53_permutations(groups):
        costs=[]
        for start,path in zip(spawns,assignment):
            distance=abs(start[0]-path[0][0])+abs(start[1]-path[0][1])
            distance+=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(path,path[1:]))
            distance+=min(abs(path[-1][0]-x)+abs(path[-1][1]-y) for x,y in access)
            costs.append(distance+(3 if fertilizer else 2)*len(path)+1+int(fertilizer))
        if max(costs)<=remaining:choices.append((max(costs),sum(costs),assignment))
    if not choices:return None
    _,_,assignment=min(choices)
    return dict(paths=assignment,spawns=spawns,remaining=remaining,workers=count,fertilizer=fertilizer)

_R53_LABOR_PARENT=agent
def agent(observation,configuration=None):
    if isinstance(observation,dict) and observation.get('step')==0:
        for k in _R53_LABOR_REPORT:_R53_LABOR_REPORT[k]=0
    result=_R53_LABOR_PARENT(observation,configuration)
    _R53_LABOR_COMBINED.update(getattr(_R53_LABOR_PARENT,'telemetry',{}));_R53_LABOR_COMBINED.update(_R53_LABOR_REPORT)
    return result
_R53_LABOR_COMBINED={}
agent.telemetry=_R53_LABOR_COMBINED
agent=globals().pop('agent')
