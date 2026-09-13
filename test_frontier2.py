"""Official unit effects for early delivery, material retention and new tasks."""
import contextlib
import copy
import importlib
import io
import json
from pathlib import Path
import unittest

import accelerator


class DeliveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments.agent import get_last_callable
            cls.engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
        cls.fn=staticmethod(get_last_callable(Path('candidates/frontier2_early.py').read_text(encoding='utf-8')))
        cls.ns=cls.fn.__globals__

    def observation(self):
        obs=accelerator.load().Game(123).observe(0);obs['step']=696;obs['day']=29
        obs['farms'][0]['farmer']=[4,4]
        return obs

    def test_export_and_frozen_source(self):
        import hashlib
        selection=json.loads(Path('results/frontier2/selection.json').read_text())
        self.assertEqual(hashlib.sha256(Path('candidates/frontier2_early.py').read_bytes()).hexdigest(),selection['sha256'])
        self.assertIs(self.fn,self.ns['agent'])
        self.assertEqual(self.ns['_FRONTIER_FORCE'],1)

    def test_delivery_preserves_fertilizer_for_later_task(self):
        obs=self.observation();farm=obs['farms'][0];private=obs['private']
        private['shed']={'FERTILIZER':1};private['inventories']=[{}]
        farm['tiles'][4][5]={'kind':'PASTURE','animal':'COW','yield_units':6}
        farm['tiles'][4][6]=dict(kind='PLANT',crop='WHEAT',planted_day=27,yield_units=0,
                                watered_today=False,fertilized_until_day=-1)
        jobs={(5,4):[([['HARVEST']],{'MILK':6})],
              (6,4):[([['FERTILIZE'],['WATER'],['HARVEST']],{'WHEAT':2,'FERTILIZER':-1})]}
        route=self.ns['_au_route']((4,4),696,jobs,dict(MILK=200,WHEAT=50,FERTILIZER=1),1.,0.,input_cap=1)
        self.assertLessEqual(696+len(route['commands']),719)
        saw_delivery=False
        for cmd in route['commands']:
            self.engine._apply_unit_action(farm,private,0,cmd,10,29,24,100)
            if cmd[0]=='PLACE':
                saw_delivery=True;self.assertEqual(private['inventories'][0]['FERTILIZER'],1)
                self.assertEqual(private['shed']['MILK'],6)
        self.assertTrue(saw_delivery)
        self.assertEqual(private['shed']['WHEAT'],2)
        self.assertFalse(private['inventories'][0])

    def test_zero_yield_can_be_watered_and_harvested(self):
        obs=self.observation()
        obs['farms'][0]['tiles'][4][3]=dict(kind='PLANT',crop='WHEAT',planted_day=27,
            yield_units=0,watered_today=False,fertilized_until_day=-1)
        jobs=self.ns['_au_jobs'](obs)
        self.assertIn((3,4),jobs)
        ops,goods=jobs[(3,4)][0]
        obs['farms'][0]['farmer']=[3,4]
        for cmd in ops:self.engine._apply_unit_action(obs['farms'][0],obs['private'],0,cmd,10,29,24,100)
        self.assertEqual(obs['private']['inventories'][0]['WHEAT'],goods['WHEAT'])

    def test_same_turn_sale_includes_placed_product(self):
        obs=self.observation();obs['step']=700
        obs['private']['shed']={};obs['private']['inventories']=[{'MILK':6,'FERTILIZER':2}]
        state=self.ns['_au_plan'](obs,{})
        state['plans']=[dict(start=700,commands=[['PLACE','MILK',6]],inputs=2)]
        state['hire_steps']=[];state['input_purchase']=0
        action=self.ns['_au_action'](obs,{},state)
        self.assertIn(['SELL','MILK',6],action['market'])
        self.assertNotIn(['SELL','FERTILIZER',2],action['market'])

    def test_same_production_prefix_as_frontier(self):
        from evaluate_fast import game
        old=game(('frontier','router',87001,0),capture_frontier=True)
        new=game(('frontier2_early','router',87001,0),capture_frontier=True)
        self.assertEqual(old['prefix_sha256'],new['prefix_sha256'])
        self.assertGreater(new['telemetry']['early_deliveries'],0)
        self.assertNotEqual(old['rewards'],new['rewards'])


if __name__=='__main__':unittest.main()
