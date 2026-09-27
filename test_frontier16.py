"""Queue contracts and exhaustive small-instance optimality against the price model."""
import contextlib,copy,io,itertools,unittest
from collections import Counter
from pathlib import Path


class Frontier16Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments import make
            from kaggle_environments.agent import get_last_callable
        cls.make=staticmethod(make);cls.loader=staticmethod(get_last_callable)

    def setUp(self):
        self.fn=self.loader(Path('candidates/f16_repaired.py').read_text(encoding='utf-8'))
        self.ns=self.fn.__globals__
        env=self.make('kaggriculture',configuration={'seed':16901},debug=True);env.reset()
        self.obs=copy.deepcopy(env.state[0]['observation']);self.obs['player']=0;self.obs['step']=200
        self.obs['private']['shed'].update(MILK=8,WOOL=7,WHEAT=6)
        self.action={'farmer':['PASS'],'hands':[],'market':[['HIRE'],['SELL','MILK',8],['BUY_SEED','WHEAT',1],['SELL','WOOL',7]]}

    def test_exact_order_multiset_and_physical_commands(self):
        old=copy.deepcopy(self.action);obs=copy.deepcopy(self.obs)
        out=self.ns['_f16_queue'](self.obs,self.action)
        self.assertEqual(self.action,old);self.assertEqual(self.obs,obs)
        self.assertEqual(out['farmer'],old['farmer']);self.assertEqual(out['hands'],old['hands'])
        self.assertEqual(Counter(map(tuple,out['market'])),Counter(map(tuple,old['market'])))
        for order in (['HIRE'],['BUY_SEED','WHEAT',1]):self.assertGreaterEqual(out['market'].index(order),old['market'].index(order))
        self.assertLess(out['market'].index(['HIRE']),out['market'].index(['BUY_SEED','WHEAT',1]))

    def test_dp_matches_exhaustive_feasible_optimum(self):
        orders=self.action['market'];stock=self.ns['projected_shed'](self.action,self.ns['FarmView'](self.obs))
        score=self.ns['_v44y_factor_margin'](orders,self.obs['market']['inventory'],stock,self.ns['_v44y_params'](self.obs))
        legal=[list(p) for p in itertools.permutations(orders) if p.index(orders[2])>=2 and p.index(orders[0])<p.index(orders[2])]
        best=max(map(score,legal));out=self.ns['_f16_queue'](self.obs,self.action)
        self.assertGreater(best,score(orders)+.5)
        self.assertAlmostEqual(score(out['market']),best)

    def test_same_item_purchase_and_sale_stay_fixed(self):
        self.action['market']=[['BUY_PRODUCT','MILK',1],['HIRE'],['SELL','MILK',8]]
        self.assertEqual(self.ns['_f16_queue'](self.obs,self.action),self.action)

    def test_insufficient_stock_is_not_moved(self):
        self.action['market']=[['HIRE'],['SELL','MILK',999]]
        self.assertEqual(self.ns['_f16_queue'](self.obs,self.action),self.action)

    def test_duplicate_item_orders_are_not_moved(self):
        self.action['market']=[['HIRE'],['SELL','MILK',3],['SELL','MILK',3]]
        self.assertEqual(self.ns['_f16_queue'](self.obs,self.action),self.action)

    def test_opening_exactly_matches_public_parent(self):
        parent=self.loader(Path('candidates/n27_lynnsakurai_031656.py').read_text(encoding='utf-8'))
        self.obs['step']=0
        self.assertEqual(self.fn(copy.deepcopy(self.obs),{}),parent(copy.deepcopy(self.obs),{}))
        self.assertEqual(self.fn.telemetry['f16_errors'],0)

    def test_window_uses_projected_stock_and_preserves_commands(self):
        old=copy.deepcopy(self.action);self.obs['step']=217
        self.ns['_F16_WINDOW_PARENT']=lambda *a:copy.deepcopy(old)
        self.ns['projected_shed']=lambda *a:dict(MILK=12,WOOL=7,STRAWBERRY=5)
        out=self.ns['_F16_PARENT'](self.obs,{})
        self.assertEqual(out['farmer'],old['farmer']);self.assertEqual(out['hands'],old['hands'])
        amounts={o[1]:o[2] for o in out['market'] if o[0]=='SELL'}
        self.assertEqual(amounts,dict(MILK=12,WOOL=7,STRAWBERRY=5))
        self.assertEqual(self.action,old)

    def test_window_does_not_modify_product_purchase_turns(self):
        self.action['market'].append(['BUY_PRODUCT','MILK',2]);self.obs['step']=217
        self.ns['_F16_WINDOW_PARENT']=lambda *a:copy.deepcopy(self.action)
        self.assertEqual(self.ns['_F16_PARENT'](self.obs,{}),self.action)

    def test_legal_empty_slots_preserve_action_and_report_skip(self):
        self.action['market'].insert(1,[])
        self.assertIs(self.ns['_s839_apply'](self.obs,self.action),self.action)
        self.assertEqual(self.ns['_F16_HOLE_REPORT']['f16_preemption_hole_skips'],1)
        self.assertEqual(self.ns['_S839_REPORT']['errors'],0)


if __name__=='__main__':unittest.main()
