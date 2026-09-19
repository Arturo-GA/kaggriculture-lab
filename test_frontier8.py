"""Frontier8 build, entry-point and behaviour checks (python -m unittest -v test_frontier8.py)."""
import contextlib
import hashlib
import io
import json
import unittest
from pathlib import Path

import build_f8

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parent
SELECTION = json.loads((ROOT / 'results/frontier8/selection.json').read_text())
PLAN = json.loads((ROOT / 'results/frontier8/plan.json').read_text())
NAME = SELECTION['candidate']


class BuildTests(unittest.TestCase):
    def test_public_bases_are_pinned(self):
        for name, prefix in build_f8.PINS.items():
            digest = hashlib.sha256((ROOT / 'candidates' / (name + '.py')).read_bytes()).hexdigest()
            self.assertTrue(digest.startswith(prefix), name)

    def test_candidate_matches_selection_and_build_manifest(self):
        manifest = json.loads((ROOT / 'results/frontier8/build.json').read_text())
        digest = hashlib.sha256((ROOT / 'candidates' / (NAME + '.py')).read_bytes()).hexdigest()
        self.assertEqual(SELECTION['sha256'], digest)
        self.assertEqual(manifest['variants'][NAME]['sha256'], digest)

    def test_candidate_is_the_documented_stack(self):
        expected = build_f8.VARIANTS[NAME][0].encode('utf-8')
        self.assertEqual((ROOT / 'candidates' / (NAME + '.py')).read_bytes(), expected)
        text = expected.decode('utf-8')
        self.assertTrue(text.startswith(build_f8.tsch.rstrip('\r\n')))
        for marker in ("_ALT_MODE = 'EarlyCycle'", 'def _eq_close(', 'def _lk_simulate('):
            self.assertIn(marker, text)
        # layer order: opening crop, queue closure, lockstep ordering last
        self.assertLess(text.index('_ALT_MODE'), text.index('def _eq_close('))
        self.assertLess(text.index('def _eq_close('), text.index('def _lk_simulate('))


class EntryPointTests(unittest.TestCase):
    def test_last_callable_is_agent_wrapping_the_queue_closure(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        self.assertEqual(fn.__name__, 'agent')
        self.assertIsInstance(getattr(fn, 'telemetry', None), dict)
        g = fn.__globals__
        self.assertIs(g['_LK_PARENT'].__globals__, g)
        self.assertIs(g['_LK_PARENT'].telemetry, g['_EQ_REPORT'])

    def test_official_game_against_the_control_completes_without_errors(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        rival = get_last_callable((ROOT / 'candidates' / (PLAN['control'] + '.py')).read_text(encoding='utf-8'))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': 5997}, debug=True)
            final = env.run([fn, rival])[-1]
        self.assertEqual([row['status'] for row in final], ['DONE', 'DONE'])
        self.assertEqual(len(env.steps), 720)
        telemetry = fn.telemetry
        errors = {k: v for k, v in telemetry.items() if v and ('error' in k or 'fallback' in k)}
        self.assertEqual(errors, {})
        self.assertGreater(telemetry.get('lk_turns', 0), 0, 'lockstep ordering never consulted')
        self.assertGreaterEqual(final[0]['reward'], final[1]['reward'], 'candidate should not lose to its control on this seed')


if __name__ == '__main__':
    unittest.main()
