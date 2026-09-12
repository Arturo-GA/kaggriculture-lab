"""Economic identities and information boundaries for the experimental gate."""
import contextlib
import copy
import io
import unittest
from types import SimpleNamespace
from pathlib import Path

import market_gate as gate
import market_gate_budget as funding


class MarketGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments.agent import get_last_callable
            from kaggle_environments.envs.kaggriculture import kaggriculture as engine
        cls.engine = engine
        cls.policies = {n: get_last_callable(Path('candidates', n + '.py').read_text(encoding='utf-8'))
                        for n in ('belief_gate', 'demand_gate', 'belief_gate2', 'demand_gate2', 'belief_lead12')}
        cls.policy = staticmethod(cls.policies['belief_gate'])

    def test_official_loader_selects_wrapper_not_parent_alias(self):
        for policy in self.policies.values():
            self.assertIs(policy, policy.__globals__['agent'])
            self.assertIsNot(policy, policy.__globals__['_LAB_GATE_PARENT'])

    def test_prices_match_official_curves_and_override(self):
        price = self.policy.__globals__['_r37_market_price']
        params = self.engine._resolve_market_params({'MILK': {'base': 173}})
        for item in self.engine.PRODUCTS:
            for inventory in (8800, 9549, 9799, 9999, 10000, 10122, 10500, 15000):
                self.assertEqual(price(item, inventory, params),
                                 self.engine.market_price(item, inventory, params))

    def test_drain_matches_official_with_repeated_shops_and_boundaries(self):
        shops = ['YARN_STORE', 'YARN_STORE', 'PIZZA_SHOP', 'PET_CAFE']
        for start, end in ((0, 1), (3, 4), (3, 5), (23, 25), (287, 293)):
            inventory = {p: 10000 for p in self.engine.PRODUCTS}
            market = {'inventory': inventory, 'prices': {}, 'params': self.engine.MARKET_PARAMS}
            state = [SimpleNamespace(observation=SimpleNamespace(
                market=market, town={'unlocked_shops': shops}))]
            for step in range(start, end):
                self.engine._town_consume(SimpleNamespace(configuration={}), state, step)
            for item in self.engine.PRODUCTS:
                self.assertEqual(10000 - inventory[item], gate._lab_drain(shops, item, start, end))

    def test_residual_excludes_own_orders_and_price_floor(self):
        items = gate._LAB_ITEMS
        obs = dict(player=0, step=48, town={'unlocked_shops': ['YARN_STORE']},
                   market={'inventory': {p: 10000 for p in items}, 'prices': {p: 100 for p in items}})
        gate._lab_gate_before(obs, {})
        gate._lab_gate_after(obs, {'market': [['SELL', 'MILK', 6]]})
        nxt = copy.deepcopy(obs)
        nxt['step'] += 1
        for p in items:
            nxt['market']['inventory'][p] -= gate._lab_drain(['YARN_STORE'], p, 48, 49)
        nxt['market']['inventory']['WOOL'] += 7
        nxt['market']['inventory']['MILK'] += 12  # mixed own/rival: must be omitted
        nxt['market']['prices']['MELON'] = 1
        gate._lab_gate_before(nxt, {})
        samples = gate._LAB_GATE_STATES[0]['samples']
        self.assertEqual(samples['WOOL'], [(49, 7.0)])
        self.assertEqual(samples['MILK'], [])
        self.assertEqual(samples['MELON'], [])
        self.assertEqual(samples['TOMATO'], [(49, 0.0)])
        gate._lab_gate_before(obs, {})
        self.assertTrue(all(not values for values in gate._LAB_GATE_STATES[0]['samples'].values()))

    def test_unsupported_config_abstains_before_accessing_farm(self):
        obs = {'player': 0, 'step': 0}
        gate._lab_gate_before(obs, {'townShopSellInterval': 5})
        self.assertTrue(gate._lab_allow_advance(obs, {}, {}, 'MILK', [(2, 4)]))

    def test_funding_reserves_spending_without_assuming_sale_revenue(self):
        orders = [['HIRE'], ['HIRE'], ['BUY_SEED', 'TOMATO', 3], ['SELL', 'MILK', 100]]
        required = 12000 + self.engine._hire_cost(8) + self.engine._hire_cost(9) + 3 * 50
        obs = dict(player=0, step=0, farms=[dict(money=required, hires_today=8,
                                               unlocked_quadrants=['NW'])], market={'prices': {}})
        action = {'market': orders}
        self.assertTrue(funding._lab_gate_funded(obs, action, [action], 0))
        obs['farms'][0]['money'] -= 1
        self.assertFalse(funding._lab_gate_funded(obs, action, [action], 0))

    def test_long_lead_preserves_native_window_and_requires_observed_pressure(self):
        ns = self.policies['belief_lead12'].__globals__
        fn = ns['_lab_allow_long_lead']
        ns['_R37_PLAYERS'][0] = {'streak': 6}
        ns['_LAB_GATE_STATES'][0] = {'supported': True, 'samples': {'MILK': [(330, 0)] * 24}}
        obs = dict(player=0, step=336, town={'unlocked_shops': []},
                   market={'inventory': {'MILK': 10000}})
        self.assertTrue(fn(obs, 'MILK', 342, 12))
        self.assertFalse(fn(obs, 'MILK', 344, 12))
        ns['_LAB_GATE_STATES'][0]['samples']['MILK'] = [(330, 3)] * 24
        self.assertTrue(fn(obs, 'MILK', 344, 12))


if __name__ == '__main__':
    unittest.main()
