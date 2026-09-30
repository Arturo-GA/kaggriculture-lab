import contextlib,copy,io,unittest
from pathlib import Path
from test_frontier20 import DeliveryContracts

class ValueContracts(DeliveryContracts):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments.agent import get_last_callable
            cls.ns=get_last_callable(Path('candidates/f20_value.py').read_text(encoding='utf-8')).__globals__

    def test_flat_market_preserves_optional_fertilizer(self):
        obs=copy.deepcopy(self.fixture['wool_obs']);obs['market']['inventory']['WOOL']=9000
        obs['market']['prices']['WOOL']=self.ns['_r37_market_price']('WOOL',9000)
        targets=((5,5),(6,5),(7,5))
        self.assertEqual(self.ns['_F20D_WORKER'](obs,13,targets),['COLLECT_FERTILIZER'])
        self.assertEqual(self.ns['_v233_worker'](obs,13,targets),['COLLECT_FERTILIZER'])

if __name__=='__main__':unittest.main()
