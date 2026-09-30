"""Final-sale coverage and unchanged food protections on real loss fixtures."""
import contextlib,copy,gzip,io,json,unittest
from pathlib import Path
from test_frontier18_feed import FeedContracts
from release_f20 import write,digest

def load(name):
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
        return get_last_callable(Path('candidates',name+'.py').read_text(encoding='utf-8')).__globals__

def suite_for(name,cap):
    ns=load(name)
    class Food(FeedContracts):
        @classmethod
        def setUpClass(cls):cls.ns=ns
    class Sales(unittest.TestCase):
        def setUp(self):
            f=json.loads(gzip.decompress(Path('results/frontier20/delivery_fixture.json.gz').read_bytes()))
            self.obs=f['egg_obs'];self.action=f['egg_action']
        def test_size_boundary_and_coverage(self):
            for residual in (1,8,cap,cap+1):
                obs=copy.deepcopy(self.obs);action=copy.deepcopy(self.action)
                sold=sum(o[2] for o in action['market'] if o[:2]==['SELL','EGG'])
                current=ns['projected_shed'](action,ns['FarmView'](obs))['EGG']
                obs['private']['shed']['EGG']+=sold+residual-current
                before=copy.deepcopy((obs,action))
                out=ns['_f20d_fill'](obs,action)
                total=sum(o[2] for o in out['market'] if o[:2]==['SELL','EGG'])
                self.assertEqual(total,sold+(residual if residual<=cap else 0))
                self.assertLessEqual(total,ns['projected_shed'](action,ns['FarmView'](obs))['EGG'])
                self.assertEqual((obs,action),before)
                self.assertEqual(out['hands'],action['hands']);self.assertEqual(out['farmer'],action['farmer'])
                self.assertEqual(len(out['market']),len(action['market']))
        def test_final_day_and_dissimilar_farms(self):
            self.obs['step']=700
            self.assertEqual(ns['_f20d_fill'](self.obs,self.action),self.action)
            self.obs['step']=400;self.obs['farms'][1-self.obs['player']]['unlocked_quadrants']=['NW']
            self.assertEqual(ns['_f20d_fill'](self.obs,self.action),self.action)
    return unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(c) for c in (Food,Sales)])

def main():
    reports={}
    for name,cap in (('f21_cap12',12),('f21_cap16',16),('f20_fill',8)):
        log=io.StringIO();result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite_for(name,cap))
        reports[name]=dict(tests=result.testsRun,passed=result.testsRun-len(result.failures)-len(result.errors),
            success=result.wasSuccessful(),source_sha256=digest(Path('candidates',name+'.py')),log=log.getvalue())
        print(name,result.wasSuccessful(),result.testsRun)
        if not result.wasSuccessful():print(log.getvalue())
    write('results/frontier21/contracts.json',dict(candidates=reports))
    assert all(r['success'] for r in reports.values())

if __name__=='__main__':main()
