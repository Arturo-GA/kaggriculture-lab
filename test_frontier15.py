"""Frontier15 build, entry-point and behaviour checks (python -m unittest -v test_frontier15.py)."""
import contextlib
import hashlib
import io
import json
import unittest
from pathlib import Path

import build_f13
import build_f14
import build_f15

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parent
SELECTION = json.loads((ROOT / 'results/frontier15/selection.json').read_text())
PLAN = json.loads((ROOT / 'results/frontier15/plan.json').read_text())
NAME = SELECTION['candidate']


class BuildTests(unittest.TestCase):
    def test_public_base_is_pinned(self):
        for name, prefix in build_f13.PINS.items():
            digest = hashlib.sha256((ROOT / 'candidates' / (name + '.py')).read_bytes()).hexdigest()
            self.assertTrue(digest.startswith(prefix), name)

    def test_candidate_matches_selection_plan_and_build_manifest(self):
        manifest = json.loads((ROOT / 'results/frontier15/build.json').read_text())
        digest = hashlib.sha256((ROOT / 'candidates' / (NAME + '.py')).read_bytes()).hexdigest()
        self.assertEqual(SELECTION['sha256'], digest)
        self.assertEqual(PLAN['candidate_sha256'], digest)
        self.assertEqual(manifest['variants'][NAME]['sha256'], digest)

    def test_candidate_is_frontier14b_plus_the_lab_layer(self):
        text = (ROOT / 'candidates' / (NAME + '.py')).read_bytes().decode('utf-8')
        self.assertEqual(text, build_f15.build(NAME))
        parent = build_f14.build('f14_adv4_h16')
        self.assertTrue(text.startswith(parent))
        self.assertEqual(PLAN['control'], 'f14_adv4_h16')
        self.assertEqual(hashlib.sha256(parent.encode('utf-8')).hexdigest(), PLAN['control_sha256'])
        self.assertEqual((ROOT / 'candidates' / 'f14_adv4_h16.py').read_bytes().decode('utf-8'), parent)
        tail = text[len(parent):]
        mode, tom, _ = build_f15.VARIANTS[NAME]
        self.assertIn('_F15_MODE = %r' % mode, tail)
        self.assertIn('_F15_TOM = %r' % tom, tail)
        self.assertEqual(tail.count('Frontier15'), 2)  # one header comment, one layer banner


class EntryPointTests(unittest.TestCase):
    def test_last_callable_is_the_lab_layer_over_the_lockstep(self):
        src = (ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8')
        fn = get_last_callable(src)
        self.assertEqual(fn.__name__, 'agent')
        g = fn.__globals__
        self.assertEqual(g['_F15_PARENT'].__name__, 'agent')            # the Frontier5 lockstep layer
        self.assertEqual(g['_LK_PARENT'].__name__, 'ig_agent')          # bound to cha22's public entry point
        mode, tom, _ = build_f15.VARIANTS[NAME]
        self.assertEqual(g['_F15_MODE'], mode)
        self.assertEqual(g['_F15_TOM'], tom)
        self.assertEqual((g['_ADV_LOOK'], g['_EV_H'], g['_DP_H'], g['_MP_H']), (4, 16, 16, 16))
        self.assertIsInstance(fn.telemetry, dict)

    def test_official_game_against_the_control_completes_without_errors(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        rival = get_last_callable((ROOT / 'candidates' / (PLAN['control'] + '.py')).read_text(encoding='utf-8'))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': PLAN['unit_test_seed']}, debug=True)
            final = env.run([fn, rival])[-1]
        self.assertEqual([row['status'] for row in final], ['DONE', 'DONE'])
        self.assertEqual(len(env.steps), 720)
        errors = {k: v for k, v in dict(getattr(fn, 'telemetry', {}) or {}).items() if v and ('error' in k or 'fallback' in k)}
        self.assertEqual(errors, {})


if __name__ == '__main__':
    unittest.main()
