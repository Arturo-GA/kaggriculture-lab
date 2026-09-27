"""Check calendar mechanics against the official engine, plus safe global restoration."""
import contextlib,copy,importlib,io,unittest
from pathlib import Path


class Frontier18Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments.agent import get_last_callable
            cls.engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
        cls.ns=get_last_callable(Path('candidates/f18_combined.py').read_text(encoding='utf-8')).__globals__

    def test_finite_tomatoes_match_official_fertilized_production_dates(self):
        for planted in (8,12,16,18,22):
            farm={'tiles':[[None]*10 for _ in range(10)]}
            farm['tiles'][0][0]=self.engine._new_plant('TOMATO',planted,24)
            produced={}
            snapshot=None
            for day in range(planted,29):
                if day==18:snapshot=copy.deepcopy(farm)
                tile=farm['tiles'][0][0]
                tile['watered_today']=True;tile['fertilized_until_day']=day+2
                before=tile['yield_units']
                self.engine._daily_refresh_plants(farm,day,24)
                gain=farm['tiles'][0][0]['yield_units']-before
                if day+1>18 and gain:produced[day+1]=gain
                farm['tiles'][0][0]['yield_units']=0
            if snapshot is None:continue
            obs=dict(step=432,player=0,farms=[{},snapshot])
            got=self.ns['_f18_finite_tomatoes'](obs,29,replant=False)
            self.assertEqual(got,produced)

    def test_store_expectations_follow_three_day_unlocks_and_cap(self):
        obs=dict(step=432,town={'unlocked_shops':['PIZZA_SHOP']*6})
        f=self.ns['_f18_shop_demand']
        self.assertEqual(f(obs,'TOMATO',20),37)
        self.assertEqual(f(obs,'TOMATO',21),38.5)
        self.assertEqual(f(obs,'TOMATO',24),40)
        self.assertEqual(f(obs,'TOMATO',29),40)
        obs['town']['unlocked_shops']=['PET_CAFE']*6
        self.assertEqual(f(obs,'CARROT',18),73)
        self.assertEqual(f(obs,'CARROT',21),75.25)

    def test_future_quote_does_not_mutate_observations(self):
        obs=dict(step=432,farms=[{'tiles':[[None]]},{'tiles':[[None]]}],
                 town={'unlocked_shops':['PET_CAFE']*6},market={'inventory':{'WHEAT':10000,'CARROT':10000}})
        original=copy.deepcopy(obs)
        self.assertGreater(self.ns['_f18_forward_quote'](obs,'CARROT',3),0)
        self.assertEqual(obs,original)

    def test_rotation_restores_parent_configuration_after_failure(self):
        names=['V9_CARROT_RATIO','V9_CARROT_WHEAT_RESERVE','_F18_CARROT_ORIGINAL']
        saved={k:self.ns[k] for k in names}
        def fail(*args):raise ValueError('route error')
        self.ns['_F18_CARROT_ORIGINAL']=fail
        obs=dict(step=432,player=0,farms=[{'tiles':[[None]]},{'tiles':[[None]]}],
                 town={'unlocked_shops':['PET_CAFE']*6},
                 market={'inventory':{'WHEAT':10000,'CARROT':10000},'prices':{'WHEAT':25,'CARROT':80}})
        try:
            with self.assertRaisesRegex(ValueError,'route error'):self.ns['_v9_carrot'](obs,{}, {})
            for k in names[:2]:self.assertEqual(self.ns[k],saved[k])
        finally:
            for k,v in saved.items():self.ns[k]=v


if __name__=='__main__':unittest.main()
