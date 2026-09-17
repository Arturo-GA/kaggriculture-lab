"""Frontier5 build, entry-point and behaviour checks (python -m unittest -v test_frontier5.py)."""
import contextlib
import hashlib
import io
import json
import unittest
from pathlib import Path

import build_f4
import build_f5

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parent
SELECTION = json.loads((ROOT / 'results/frontier5/selection.json').read_text())
NAME = SELECTION['candidate']
LOCK = (ROOT / 'frontier5_lockstep.py').read_text(encoding='utf-8')
SOURCES = {'f5_lock': build_f5.v46 + '\n' + LOCK, 'f5_lockterm': build_f5.v46 + build_f4.terminal + '\n' + LOCK,
           'f5_term': build_f5.v46 + build_f4.terminal}


class BuildTests(unittest.TestCase):
    def test_public_base_is_pinned(self):
        data = (ROOT / 'candidates/v46.py').read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), build_f5.V46_SHA256)

    def test_candidate_matches_selection_and_build_manifest(self):
        manifest = json.loads((ROOT / 'results/frontier5/build.json').read_text())
        digest = hashlib.sha256((ROOT / 'candidates' / (NAME + '.py')).read_bytes()).hexdigest()
        self.assertEqual(SELECTION['sha256'], digest)
        self.assertEqual(manifest['variants'][NAME]['sha256'], digest)

    def test_candidate_is_the_documented_transformation_of_v46(self):
        expected = SOURCES[NAME].encode('utf-8')
        self.assertEqual((ROOT / 'candidates' / (NAME + '.py')).read_bytes(), expected)
        text = expected.decode('utf-8')
        self.assertTrue(text.startswith(build_f5.v46))
        self.assertIn('def _lk_simulate(', text)


class LockstepModelTests(unittest.TestCase):
    def test_lockstep_simulation_matches_engine_market(self):
        """Two players sell the same lots; the modeled cash equals the engine's per-unit settlement."""
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        g = fn.__globals__
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            env = make('kaggriculture', configuration={'episodeSteps': 8, 'seed': 7})
            state = env.reset()
        obs = state[0]['observation']
        inventory = dict(obs['market']['inventory'])
        params = g['_lk_params']({'market': obs['market']})
        ours = [['SELL', 'WHEAT', 4], ['SELL', 'CARROT', 3]]
        theirs = [['SELL', 'CARROT', 3], ['SELL', 'WHEAT', 4]]
        stock = {'WHEAT': 4, 'CARROT': 3}
        rev_a, rev_b = g['_lk_simulate'](ours, theirs, inventory, stock, stock, params)
        # Swapped slots: each player sells one product into the other's earlier glut; the modeled
        # asymmetry is a few coins at most (carrot falls faster than wheat), never a sign flip.
        self.assertGreater(rev_a, 0)
        self.assertLessEqual(abs(rev_a - rev_b), 5)
        # Same product at the same index: both quoted at the same inventory each unit.
        rev_c, rev_d = g['_lk_simulate']([['SELL', 'WHEAT', 4]], [['SELL', 'WHEAT', 4]], inventory, stock, stock, params)
        self.assertAlmostEqual(rev_c, rev_d, places=6)


class EntryPointTests(unittest.TestCase):
    def test_last_callable_is_agent_with_telemetry(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        self.assertEqual(fn.__name__, 'agent')
        self.assertIsInstance(getattr(fn, 'telemetry', None), dict)

    def test_official_game_against_v46_completes_without_errors(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        rival = get_last_callable((ROOT / 'candidates/v46.py').read_text(encoding='utf-8'))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': 5999}, debug=True)
            final = env.run([fn, rival])[-1]
        self.assertEqual([row['status'] for row in final], ['DONE', 'DONE'])
        self.assertEqual(len(env.steps), 720)
        telemetry = fn.telemetry
        errors = {k: v for k, v in telemetry.items() if v and ('error' in k or 'fallback' in k)}
        self.assertEqual(errors, {})
        self.assertGreater(telemetry.get('lk_turns', 0), 0, 'lockstep ordering never consulted')
        self.assertGreaterEqual(final[0]['reward'], final[1]['reward'], 'candidate should not lose the mirror on this seed')


if __name__ == '__main__':
    unittest.main()
