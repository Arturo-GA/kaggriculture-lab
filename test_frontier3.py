"""Verify resource contracts and terminal deposit effects using the official engine."""
import contextlib
import copy
import importlib
import io
from pathlib import Path
import unittest


class Frontier3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments import make
            from kaggle_environments.agent import get_last_callable
            cls.engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
        cls.make=staticmethod(make);cls.loader=staticmethod(get_last_callable)

    def setUp(self):
        self.fn=self.loader(Path('candidates/frontier3_capacity.py').read_text(encoding='utf-8'))
        self.ns=self.fn.__globals__
        env=self.make('kaggriculture',configuration={'seed':93001},debug=True);env.reset()
        self.obs=copy.deepcopy(env.state[0]['observation']);self.obs['player']=0;self.obs['step']=0
        self.fn(self.obs,{})

    def test_export_and_opening_preserve_observation(self):
        self.assertIs(self.fn,self.ns['agent'])
        obs=copy.deepcopy(self.obs);before=copy.deepcopy(obs)
        action=self.fn(obs,{})
        self.assertEqual(obs,before)
        self.assertEqual(action['market'],[['BUY_PRODUCT','WHEAT',5],['BUY_PRODUCT','WHEAT',10],['SELL','WHEAT',60]])

    def test_seed_purchase_preserves_worker_cash(self):
        self.obs['farms'][0]['money']=24
        action={'farmer':['PASS'],'hands':[],'market':[['BUY_SEED','WHEAT',3]]}
        got=self.ns['_r124_seed_budget'](self.obs,action,4)
        self.assertEqual(got['market'],[['BUY_SEED','WHEAT',2]])
        self.assertEqual(action['market'][0][2],3)

    def test_seed_shortfall_keeps_feasible_plant_in_general_day(self):
        obs=self.obs;obs['step']=120;obs['day']=5
        farm=obs['farms'][0];farm['farmer']=[3,3];farm['hands']=[[3,4]]
        farm['tiles'][3][3]=None;farm['tiles'][4][3]=None
        obs['private']['inventories']=[{},{}];obs['private']['seeds']['WHEAT']=1
        action={'farmer':['PLANT','WHEAT'],'hands':[['PLANT','WHEAT']],'market':[]}
        state={};got=self.ns['_r124_atomic'](obs,action,state)
        self.assertEqual(got['hands'],[['PASS']])
        self.assertEqual(state['pending_plants'][0]['birth'],5)
        self.engine._apply_unit_action(farm,obs['private'],0,got['farmer'],10,5,24,100)
        self.engine._apply_unit_action(farm,obs['private'],1,got['hands'][0],10,5,24,100)
        self.assertEqual(farm['tiles'][3][3]['planted_day'],5)
        self.assertIsNone(farm['tiles'][4][3])

    def terminal(self,inventories,shed=None,step=718):
        obs=self.obs;obs['step']=step;obs['day']=29;obs['hour']=step%24
        obs['farms'][0]['farmer']=[4,4]
        obs['farms'][0]['hands']=[[4,5] for _ in inventories[1:]]
        obs['private']['inventories']=copy.deepcopy(inventories)
        obs['private']['shed']=dict(shed or {})
        obs['market']['prices'].update(WHEAT=10,MILK=200)
        return obs,{'farmer':['DROP'],'hands':[['DROP'] for _ in inventories[1:]],'market':[]}

    def apply(self,obs,action):
        farm=copy.deepcopy(obs['farms'][0]);private=copy.deepcopy(obs['private'])
        for i,cmd in enumerate([action['farmer'],*action['hands']]):
            self.engine._apply_unit_action(farm,private,i,cmd,10,29,24,100)
        return farm,private

    def test_shared_capacity_preserves_cargo_and_prioritizes_value(self):
        obs,action=self.terminal([{'WHEAT':90},{'MILK':20}])
        got=self.ns['_f3_capacity'](obs,action);_,private=self.apply(obs,got)
        self.assertEqual(private['shed'],{'WHEAT':80,'MILK':20})
        self.assertEqual(private['inventories'][0],{'WHEAT':10})
        self.assertEqual(sum(private['shed'].values())+sum(sum(i.values()) for i in private['inventories']),110)
        self.assertIn(['SELL','WHEAT',80],got['market'])
        self.assertIn(['SELL','MILK',20],got['market'])

    def test_partial_delivery_can_finish_next_turn(self):
        obs,action=self.terminal([{'WHEAT':9,'MILK':9}],{'CARROT':90},717)
        got=self.ns['_f3_capacity'](obs,action);farm,private=self.apply(obs,got)
        self.assertEqual(got['farmer'],['PLACE','MILK',9])
        self.assertEqual(private['inventories'][0],{'WHEAT':9})
        private['shed']={};obs['farms'][0]=farm;obs['private']=private;obs['step']=718
        got=self.ns['_f3_capacity'](obs,action);_,private=self.apply(obs,got)
        self.assertEqual(private['shed'],{'WHEAT':9})
        self.assertEqual(private['inventories'],[{}])

    def test_uncongested_deposit_is_unchanged(self):
        obs,action=self.terminal([{'MILK':12}])
        self.assertEqual(self.ns['_f3_capacity'](obs,action),action)

    def test_full_shed_retains_cargo(self):
        obs,action=self.terminal([{'MILK':12}],{'CARROT':100})
        got=self.ns['_f3_capacity'](obs,action);_,private=self.apply(obs,got)
        self.assertEqual(got['farmer'],['PASS'])
        self.assertEqual(private['inventories'],[{'MILK':12}])


if __name__=='__main__':unittest.main()
