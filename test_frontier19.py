"""Stock, cash-timing and physical-action contracts for the F19 market overlay."""
import contextlib
import copy
import io
import itertools
import unittest
from collections import Counter
from pathlib import Path

import test_frontier18_feed as feed_tests


class MarketContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The overlay alone needs only these inherited symbols for pure helpers.
        cls.ns = {'agent': lambda *_: None, '_cxd_it': itertools}
        exec(compile(Path('frontier19_market.py').read_text(encoding='utf-8'),
                     'frontier19_market.py', 'exec'), cls.ns)

    def variants(self, orders, stock):
        return list(self.ns['_f19_permutations'](orders, stock))

    def test_sales_never_advance_fixed_spending_or_change_its_order(self):
        orders = [['HIRE', 1], ['SELL', 'MILK', 7], ['BUY_LAND', 'SW'],
                  ['SELL', 'WOOL', 4], ['BUY_SEED', 'STRAWBERRY', 5]]
        before = copy.deepcopy(orders)
        trials = self.variants(orders, {'MILK': 7, 'WOOL': 4})
        self.assertGreater(len(trials), 1)
        fixed = [orders[i] for i in (0, 2, 4)]
        for trial in trials:
            self.assertEqual(Counter(map(tuple, trial)), Counter(map(tuple, orders)))
            self.assertEqual([o for o in trial if o in fixed], fixed)
            self.assertTrue(all(trial.index(o) >= orders.index(o) for o in fixed))
        self.assertEqual(orders, before)

    def test_traded_inputs_and_uncovered_sales_keep_their_positions(self):
        orders = [['BUY_PRODUCT', 'WHEAT', 8], ['SELL', 'WHEAT', 8],
                  ['SELL', 'EGG', 8], ['HIRE', 1], ['SELL', 'MILK', 3]]
        for trial in self.variants(orders, {'WHEAT': 8, 'EGG': 7, 'MILK': 3}):
            self.assertEqual(trial[:3], orders[:3])

    def test_duplicate_sales_use_total_stock_and_search_is_bounded(self):
        orders = [['SELL', 'MILK', 3], ['HIRE', 1], ['SELL', 'MILK', 4]]
        self.assertEqual(self.variants(orders, {'MILK': 6}), [orders])
        many = [['SELL', p, 1] for p in ('MILK', 'WOOL', 'EGG', 'TOMATO', 'MELON')]
        many += [['HIRE', i] for i in range(1, 6)]
        trials = self.variants(many, {o[1]: 1 for o in many[:5]})
        self.assertLessEqual(len(trials), 161)
        keys = [tuple(map(tuple, t)) for t in trials]
        self.assertEqual(len(keys), len(set(keys)))

    def test_early_game_and_dissimilar_farms_are_identity(self):
        action = {'market': [['HIRE', 1], ['SELL', 'MILK', 7]],
                  'farmer': ['MOVE', 'N'], 'hands': [['PASS']]}
        self.assertIs(self.ns['_f19_market']({'step': 100}, action), action)
        self.ns['_r37_similarity'] = lambda _: .94
        self.assertIs(self.ns['_f19_market']({'step': 500}, action), action)


def load_tests(loader, standard_tests, pattern):
    # Apply the real replay regression to every frozen candidate, not merely the
    # standalone rescue prototype. The source is loaded once per test class.
    suite = unittest.TestSuite([loader.loadTestsFromTestCase(MarketContracts)])
    for name in ('f19_market2', 'f19_robust', 'f19_balanced', 'f19_pressure'):
        def setup(cls, name=name):
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                from kaggle_environments.agent import get_last_callable
                cls.ns = get_last_callable(Path('candidates', name + '.py').read_text(encoding='utf-8')).__globals__
        cls = type(name + 'FeedContracts', (feed_tests.FeedContracts,), {'setUpClass': classmethod(setup)})
        suite.addTests(loader.loadTestsFromTestCase(cls))
    return suite


if __name__ == '__main__':
    unittest.main()
