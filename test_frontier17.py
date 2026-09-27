"""Check stock neutrality against the official simultaneous market, not mocks."""
import contextlib,copy,importlib,io,unittest
from pathlib import Path


class Frontier17Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments import make
            from kaggle_environments.agent import get_last_callable
        cls.make=staticmethod(make);cls.load=staticmethod(get_last_callable)
        cls.engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
        cls.fn=cls.load(Path('candidates/f17_cycle.py').read_text(encoding='utf-8'))
        cls.ns=cls.fn.__globals__

    def fixture(self,item,inventory):
        env=self.make('kaggriculture',configuration={'seed':17091},debug=True);env.reset()
        state=env.state
        for i in (0,1):
            state[0].observation.farms[i]['money']=20000
            state[i].observation.private.shed.update(WHEAT=10,FERTILIZER=4,MILK=8)
        state[0].observation.market.inventory[item]=inventory
        self.engine._refresh_prices(state[0].observation.market)
        obs=copy.deepcopy(state[0].observation);obs['player']=0;obs['step']=200
        action=dict(farmer=['PASS'],hands=[],market=[['HIRE'],['BUY_PRODUCT',item,5]])
        return env,obs,action

    def market(self,env,mine,rival):
        state=copy.deepcopy(env.state);state[0].action=mine;state[1].action=rival
        self.engine._process_market(state,env)
        return state

    def test_market_stock_and_fixed_purchases_preserved_officially(self):
        changed=0
        for item in ('WHEAT','FERTILIZER'):
            for inventory in (9700,9950,10000,10050,10200):
                env,obs,base=self.fixture(item,inventory);old=copy.deepcopy(base);before=copy.deepcopy(obs)
                trial=self.ns['_f17_input_apply'](obs,base)
                self.assertEqual(base,old);self.assertEqual(obs,before)
                self.assertEqual(trial['farmer'],base['farmer']);self.assertEqual(trial['hands'],base['hands'])
                self.assertLessEqual(len(trial['market']),10)
                for rival in (base,dict(base,market=[]),dict(base,market=[['SELL',item,7]])):
                    a=self.market(env,base,rival);b=self.market(env,trial,rival)
                    self.assertEqual(a[0].observation.private.shed,b[0].observation.private.shed)
                    self.assertEqual(a[0].observation.private.seeds,b[0].observation.private.seeds)
                    self.assertEqual(a[0].observation.farms[0].hands,b[0].observation.farms[0].hands)
                if trial!=base:
                    changed+=1
                    a=self.market(env,base,base);b=self.market(env,trial,base)
                    gain=(b[0].observation.farms[0]['money']-b[0].observation.farms[1]['money'])-(a[0].observation.farms[0]['money']-a[0].observation.farms[1]['money'])
                    self.assertGreater(gain,0)
        self.assertGreater(changed,0)

    def test_insufficient_cash_or_capacity_abstains(self):
        env,obs,base=self.fixture('WHEAT',9900)
        obs['farms'][0]['money']=100
        self.assertEqual(self.ns['_f17_input_apply'](obs,base),base)
        obs['farms'][0]['money']=20000;obs['private']['shed']['WHEAT']=90
        self.assertEqual(self.ns['_f17_input_apply'](obs,base),base)

    def test_roundtrip_edits_preserve_every_physical_command(self):
        original=self.load(Path('candidates/f16_repaired.py').read_text(encoding='utf-8')).__globals__['_IMPL'].chassis.routes
        patched=self.load(Path('candidates/f17_cancel.py').read_text(encoding='utf-8')).__globals__['_IMPL'].chassis.routes
        changed=0
        for rid,tape in original.items():
            for a,b in zip(tape,patched[rid]):
                self.assertEqual(a.get('farmer'),b.get('farmer'));self.assertEqual(a.get('hands'),b.get('hands'))
                changed+=a.get('market')!=b.get('market')
        self.assertGreater(changed,0)


if __name__=='__main__':unittest.main()
