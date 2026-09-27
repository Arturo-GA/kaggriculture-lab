"""Reuse official-market contracts on both new input policies, including small spare capacity."""
import contextlib,copy,importlib,io,unittest
from pathlib import Path
from test_frontier17 import Frontier17Tests


class MarketContracts(unittest.TestCase):
    candidate='f18_micro'
    fixture=Frontier17Tests.fixture
    market=Frontier17Tests.market
    test_stock=Frontier17Tests.test_market_stock_and_fixed_purchases_preserved_officially
    test_abstain=Frontier17Tests.test_insufficient_cash_or_capacity_abstains

    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments import make
            from kaggle_environments.agent import get_last_callable
        cls.make=staticmethod(make);cls.load=staticmethod(get_last_callable)
        cls.engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
        cls.fn=cls.load(Path('candidates',cls.candidate+'.py').read_text(encoding='utf-8'));cls.ns=cls.fn.__globals__

    def test_small_room_stock_is_preserved(self):
        changed=0
        for item in ('WHEAT','FERTILIZER'):
            for inventory in (9700,9950,10000,10050,10200):
                env,obs,base=self.fixture(item,inventory)
                for i in (0,1):env.state[i].observation.private.shed['WHEAT']=78
                obs['private']['shed']['WHEAT']=78
                trial=self.ns['_f17_input_apply'](obs,base)
                changed+=trial!=base
                for rival in (base,dict(base,market=[]),dict(base,market=[['BUY_PRODUCT',item,30]])):
                    a=self.market(env,base,rival);b=self.market(env,trial,rival)
                    self.assertEqual(a[0].observation.private.shed,b[0].observation.private.shed)
                    self.assertEqual(a[0].observation.farms[0].hands,b[0].observation.farms[0].hands)
        self.assertGreater(changed,0)


class RobustContracts(MarketContracts):
    candidate='f18_micro_robust'


class SmallContracts(MarketContracts):
    candidate='f18_small'


if __name__=='__main__':unittest.main()
