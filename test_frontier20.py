"""Real-loss regressions: delivery priority, food/care and covered sale sizes."""
import contextlib,copy,gzip,io,json,unittest
from pathlib import Path

class DeliveryContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments.agent import get_last_callable
            cls.ns=get_last_callable(Path('candidates/f20_delivery.py').read_text(encoding='utf-8')).__globals__
        cls.fixture=json.loads(gzip.decompress(Path('results/frontier20/delivery_fixture.json.gz').read_bytes()))

    def test_actual_wool_courier_leaves_instead_of_collecting_fertilizer(self):
        obs=copy.deepcopy(self.fixture['wool_obs']);before=copy.deepcopy(obs)
        targets=((5,5),(6,5),(7,5));actor=13
        self.assertEqual(self.ns['_F20D_WORKER'](obs,actor,targets),['COLLECT_FERTILIZER'])
        self.assertEqual(self.ns['_v233_worker'](obs,actor,targets),['WEST'])
        self.assertEqual(obs,before)

    def test_feed_and_care_still_precede_departure(self):
        obs=copy.deepcopy(self.fixture['wool_obs']);farm=obs['farms'][obs['player']]
        x,y=farm['hands'][12];tile=farm['tiles'][y][x]
        tile['fed_today']=False;tile['cared_today']=False;obs['private']['inventories'][13]['WHEAT']=1
        targets=((5,5),(6,5),(7,5))
        self.assertEqual(self.ns['_v233_worker'](obs,13,targets),['FEED'])
        tile['fed_today']=True
        self.assertEqual(self.ns['_v233_worker'](obs,13,targets),['CARE'])

    def test_optional_fertilizer_returns_after_wool_delivery(self):
        obs=copy.deepcopy(self.fixture['wool_obs']);targets=((5,5),(6,5),(7,5))
        obs['private']['inventories'][13]['WOOL']=0
        for x,y in targets:obs['farms'][obs['player']]['tiles'][y][x]['yield_units']=0
        self.assertEqual(self.ns['_v233_worker'](obs,13,targets),self.ns['_F20D_WORKER'](obs,13,targets))

    def test_real_egg_residual_is_covered_and_commands_are_preserved(self):
        obs=copy.deepcopy(self.fixture['egg_obs']);action=copy.deepcopy(self.fixture['egg_action']);before=copy.deepcopy(action)
        result=self.ns['_f20d_fill'](obs,action)
        self.assertEqual(next(o[2] for o in result['market'] if o[:2]==['SELL','EGG']),8)
        self.assertEqual(result['farmer'],action['farmer']);self.assertEqual(result['hands'],action['hands'])
        self.assertEqual(len(result['market']),len(action['market']));self.assertEqual(action,before)
        stock=self.ns['projected_shed'](action,self.ns['FarmView'](obs))
        for item in ('EGG','MILK'):
            q=sum(o[2] for o in result['market'] if len(o)>2 and o[:2]==['SELL',item])
            self.assertLessEqual(q,stock[item])

    def test_final_day_and_unrelated_farms_keep_parent_policy(self):
        obs=copy.deepcopy(self.fixture['wool_obs']);obs['step']=29*24
        self.assertEqual(self.ns['_v233_worker'](obs,13,((5,5),(6,5),(7,5))),self.ns['_F20D_WORKER'](obs,13,((5,5),(6,5),(7,5))))
        obs=copy.deepcopy(self.fixture['egg_obs']);action=self.fixture['egg_action']
        obs['farms'][1-obs['player']]['unlocked_quadrants']=['NW']
        self.assertIs(self.ns['_f20d_fill'](obs,action),action)

if __name__=='__main__':unittest.main()
