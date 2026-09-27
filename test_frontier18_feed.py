"""Regression contracts for the observed zero-pickup deadlock, with real replay state."""
import contextlib,copy,gzip,io,json,unittest
from pathlib import Path


class FeedContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments.agent import get_last_callable
        cls.ns=get_last_callable(Path('candidates/f18_feed.py').read_text(encoding='utf-8')).__globals__

    def setUp(self):
        f=json.loads(gzip.decompress(Path('results/frontier18/feed_fixture.json.gz').read_bytes()))
        self.obs=f['obs'];self.action=f['action'];self.state=f['state']
        self.state['workers']={int(k):v for k,v in self.state['workers'].items()}

    def test_real_zero_pickup_buys_missing_feed_without_changing_commands(self):
        before=copy.deepcopy(self.obs);act=copy.deepcopy(self.action)
        old=self.ns['_F18_FEED_RESCUE_PARENT'](self.obs,self.action,copy.deepcopy(self.state))
        self.assertEqual(old,self.action)
        out=self.ns['_v234_rescue'](self.obs,self.action,self.state)
        # Six hungry sheep; the blocked worker already carries one unit.
        self.assertEqual(out['market'],self.action['market']+[['BUY_PRODUCT','WHEAT',5]])
        self.assertEqual(out['farmer'],act['farmer']);self.assertEqual(out['hands'],act['hands'])
        self.assertEqual(self.obs,before);self.assertEqual(self.action,act)

    def test_positive_pickup_is_not_reinterpreted_as_deadlock(self):
        self.action['hands'][11]=['PICKUP','WHEAT',2]
        self.assertEqual(self.ns['_v234_rescue'](self.obs,self.action,self.state),self.action)

    def test_no_rescue_on_final_day_or_without_cash(self):
        self.obs['step']=699
        self.assertEqual(self.ns['_v234_rescue'](self.obs,self.action,self.state),self.action)
        self.obs['step']=603;self.obs['farms'][0]['money']=50
        self.assertEqual(self.ns['_v234_rescue'](self.obs,self.action,self.state),self.action)

    def test_rescue_preserves_capacity_guard(self):
        self.obs['private']['shed']['TOMATO']=100
        self.assertEqual(self.ns['_v234_rescue'](self.obs,self.action,self.state),self.action)


if __name__=='__main__':unittest.main()
