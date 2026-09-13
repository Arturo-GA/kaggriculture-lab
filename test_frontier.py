"""Runtime export, information boundaries and route feasibility."""
import contextlib
import copy
import hashlib
import io
import importlib
import json
from pathlib import Path
import unittest

import accelerator


class FrontierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments.agent import get_last_callable
        cls.policy=staticmethod(get_last_callable(Path('candidates/frontier.py').read_text(encoding='utf-8')))
        cls.ns=cls.policy.__globals__

    def test_export_and_selection_parity(self):
        self.assertIs(self.policy,self.ns['agent'])
        report=json.loads(Path('results/gold/frontier_training.json').read_text())
        self.assertEqual(hashlib.sha256(Path('candidates/frontier.py').read_bytes()).hexdigest(),report['exported']['frontier'])
        rows=sorted([json.loads(r) for r in Path('results/gold/frontier_selection.jsonl').read_text().splitlines()],key=lambda r:(r['seed'],r['opponent'],r['seat']))
        choices=[self.ns['_frontier_choose'](r['features'],self.ns['_FRONTIER_MODEL']) for r in rows]
        self.assertEqual(choices,report['selected_gate']['choices'])

    def test_features_exclude_identity_future_and_rival_private(self):
        obs=accelerator.load().Game(123).observe(0)
        plan=self.ns['_au_plan'](obs,{})
        features=self.ns['_frontier_features'](obs,plan)
        other=copy.deepcopy(obs)
        other.update(seed=999,opponent_name='private-policy',future_reward=123456,
                     opponent_private={'shed':{'MILK':10000}})
        self.assertEqual(features,self.ns['_frontier_features'](other,self.ns['_au_plan'](other,{})))
        self.assertEqual(len(features),109)

    def test_terminal_route_executes_with_materials_before_deadline(self):
        # Feasibility checks material balance, distinct harvest tasks,
        # return position and a strict terminal deadline on a small route.
        jobs={(3,4):[([['HARVEST']],{'WHEAT':2}),
                       ([['FERTILIZE'],['WATER'],['HARVEST']],{'WHEAT':4,'FERTILIZER':-1})],
              (2,4):[([['HARVEST']],{'CARROT':3})]}
        route=self.ns['_au_route']((4,4),696,jobs,dict(WHEAT=50,CARROT=50,FERTILIZER=1),.6,0.,input_cap=3)
        self.assertLessEqual(route['start']+len(route['commands']),719)
        x,y=route['origin'];carried=route['inputs'];visited=set()
        for cmd in route['commands']:
            x+=int(cmd[0]=='EAST')-int(cmd[0]=='WEST');y+=int(cmd[0]=='SOUTH')-int(cmd[0]=='NORTH')
            if cmd[0]=='FERTILIZE':
                self.assertGreater(carried,0);carried-=1
            if cmd[0]=='HARVEST':
                self.assertIn((x,y),jobs);self.assertNotIn((x,y),visited);visited.add((x,y))
        self.assertEqual(set(route['jobs']),visited)
        self.assertIn((x,y),self.ns['_AU_HOME']);self.assertEqual(route['commands'][-1],['DROP'])
        # A distant task cannot be admitted with only one turn left.
        impossible=self.ns['_au_route']((4,4),718,{(0,0):jobs[(2,4)]},dict(CARROT=100),1.,0.)
        self.assertEqual(impossible['commands'],[])
        # Resolve those exact commands using the official unit-action engine.
        engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
        obs=accelerator.load().Game(123).observe(0)
        farm,private=copy.deepcopy(obs['farms'][0]),copy.deepcopy(obs['private'])
        farm['farmer']=[4,4];private['shed']={'FERTILIZER':3};private['inventories']=[{}]
        for (x,y),crop,day,q in [((3,4),'WHEAT',26,2),((2,4),'CARROT',27,3)]:
            farm['tiles'][y][x]=dict(kind='PLANT',crop=crop,planted_day=day,yield_units=q,
                                    watered_today=False,fertilized_until_day=-1)
        for cmd in route['commands']:engine._apply_unit_action(farm,private,0,cmd,10,29,24,100)
        self.assertEqual(private['shed']['WHEAT'],4)
        self.assertEqual(private['shed']['CARROT'],3)
        self.assertEqual(private['shed']['FERTILIZER'],2)
        self.assertFalse(private['inventories'][0])

    def test_forced_native_matches_original_whole_game(self):
        from evaluate_fast import game
        control=game(('frontier_control','router',86001,0),capture_frontier=True)
        original=game(('ml_critic','router',86001,0))
        self.assertEqual(control['rewards'],original['rewards'])
        forced=game(('frontier_force','router',86001,0),capture_frontier=True)
        self.assertEqual(control['prefix_sha256'],forced['prefix_sha256'])
        self.assertNotEqual(control['rewards'],forced['rewards'])
        self.assertEqual(forced['telemetry']['frontier_choice'],1)


if __name__=='__main__':unittest.main()
