import contextlib
import hashlib
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path
import build


class ExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = build.build()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments.agent import get_last_callable
        cls.policies = {name:get_last_callable((build.ROOT/'candidates'/(name+'.py')).read_text(encoding='utf-8'))
                        for name in cls.manifest['candidates']}

    def test_original_hash_and_exact_intervention(self):
        self.assertEqual(self.manifest['baseline_sha256'],build.EXPECTED)
        original = (build.ROOT/'baseline/v37.py').read_text(encoding='utf-8')
        modified = (build.ROOT/'candidates/h6.py').read_text(encoding='utf-8')
        self.assertEqual(modified.replace(build.ANCHOR[:-1]+'6',build.ANCHOR),original)

    def test_official_loader_selects_agent(self):
        for policy in self.policies.values():
            self.assertIs(policy,policy.__globals__['agent'])

    def test_pressure_scenarios_and_bounds(self):
        fn = self.policies['pressure'].__globals__['_lab_pressure_horizon']
        obs = {'player':0,'farms':[{}, {'tiles':[[None]]}],
               'private':{'shed':{'MILK':12}},
               'market':{'inventory':{p:10000 for p in ('MILK','WOOL','STRAWBERRY','MELON')}}}
        self.assertEqual(fn(obs),4)
        obs['farms'][1]['tiles'] = [[{'animal':'COW','yield_units':24}]]
        self.assertEqual(fn(obs),8)
        obs['private']['shed']={}
        self.assertEqual(fn(obs),4)

    def test_archive_reproducible_and_exact(self):
        parent = build.ROOT/'outputs'
        parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as folder:
            self.assertTrue(Path(folder).resolve().is_relative_to(parent.resolve()))
            a,b = Path(folder)/'a.tar.gz',Path(folder)/'b.tar.gz'
            build.package('matched6',a)
            build.package('matched6',b)
            self.assertEqual(a.read_bytes(),b.read_bytes())
            with tarfile.open(a,'r:gz') as tf:
                self.assertEqual(tf.getnames(),['main.py'])
                self.assertEqual(hashlib.sha256(tf.extractfile('main.py').read()).hexdigest(),
                                 self.manifest['candidates']['matched6'])


if __name__ == '__main__':
    unittest.main()
