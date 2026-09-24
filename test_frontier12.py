"""Frontier12 router build, entry-point and behaviour checks (python -m unittest -v test_frontier12.py)."""
import contextlib
import hashlib
import io
import json
import time
import unittest
from pathlib import Path

import build_f12

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parent
SELECTION = json.loads((ROOT / 'results/frontier12/selection.json').read_text())
PLAN = json.loads((ROOT / 'results/frontier12/plan.json').read_text())
TABLE = json.loads((ROOT / 'results/frontier12/table.json').read_text())
NAME = SELECTION['candidate']


class BuildTests(unittest.TestCase):
    def test_embedded_candidates_are_pinned(self):
        for name, prefix in build_f12.PINS.items():
            digest = hashlib.sha256((ROOT / 'candidates' / (name + '.py')).read_bytes()).hexdigest()
            self.assertTrue(digest.startswith(prefix), name)

    def test_router_rebuilds_byte_for_byte_and_matches_selection(self):
        text = (ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8')
        self.assertEqual(text, build_f12.build(TABLE))
        digest = hashlib.sha256((ROOT / 'candidates' / (NAME + '.py')).read_bytes()).hexdigest()
        self.assertEqual(SELECTION['sha256'], digest)
        self.assertEqual(PLAN['candidate_sha256'], digest)
        self.assertEqual(json.loads((ROOT / 'results/frontier12/build.json').read_text())['sha256'], digest)

    def test_table_is_well_formed(self):
        keys = set(build_f12.BASES)
        self.assertIn(TABLE['default'].partition(':')[0], keys)
        self.assertIn(TABLE['opening'], keys)
        for v in TABLE['table'].values():
            base, _, profile = v.partition(':')
            self.assertIn(base, keys)
            self.assertTrue(not profile or profile in TABLE.get('profiles', {}))
        self.assertTrue(all(k.count('|') <= 2 for k in TABLE['table']))
        self.assertEqual(set(TABLE['branch_money'].values()) <= keys | {'unknown'}, True)


class EntryPointTests(unittest.TestCase):
    def test_last_callable_is_the_router_and_loads_quickly(self):
        src = (ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8')
        t = time.perf_counter()
        fn = get_last_callable(src)
        self.assertLess(time.perf_counter() - t, 20.0)
        self.assertEqual(fn.__name__, 'agent')
        g = fn.__globals__
        self.assertEqual(set(g['_F12_AGENTS']), set(build_f12.BASES))
        for base in g['_F12_AGENTS'].values():
            self.assertEqual(base.__name__, 'agent')
            self.assertIn('_LK_PARENT', base.__globals__)

    def test_official_game_against_the_control_switches_and_completes_without_errors(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        rival = get_last_callable((ROOT / 'candidates' / (PLAN['control'] + '.py')).read_text(encoding='utf-8'))
        lat = []

        def timed(obs, cfg=None):
            t = time.perf_counter()
            a = fn(obs, cfg)
            lat.append(time.perf_counter() - t)
            return a
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': PLAN['unit_test_seed']}, debug=True)
            final = env.run([timed, rival])[-1]
        self.assertEqual([row['status'] for row in final], ['DONE', 'DONE'])
        self.assertEqual(len(env.steps), 720)
        tel = dict(fn.telemetry)
        self.assertEqual(tel['f12_switch_step'], 144)
        self.assertIn(tel['f12_choice'], build_f12.BASES)
        self.assertEqual(tel['f12_branch'], 'hs')   # the control is the Herd-Safe candidate
        self.assertEqual(tel['f12_choice'], 'hs')
        errors = {k: v for k, v in tel.items() if v and ('error' in k or 'fallback' in k)}
        self.assertEqual(errors, {})
        self.assertLess(max(lat), 1.0)


if __name__ == '__main__':
    unittest.main()
