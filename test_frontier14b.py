"""Frontier14B build, entry-point and behaviour checks (python -m unittest -v test_frontier14.py)."""
import contextlib
import hashlib
import io
import json
import unittest
from pathlib import Path

import build_f13
import build_f14

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parent
SELECTION = json.loads((ROOT / 'results/frontier14b/selection.json').read_text())
PLAN = json.loads((ROOT / 'results/frontier14b/plan.json').read_text())
NAME = SELECTION['candidate']


class BuildTests(unittest.TestCase):
    def test_public_base_is_pinned(self):
        for name, prefix in build_f13.PINS.items():
            digest = hashlib.sha256((ROOT / 'candidates' / (name + '.py')).read_bytes()).hexdigest()
            self.assertTrue(digest.startswith(prefix), name)

    def test_candidate_matches_selection_plan_and_build_manifest(self):
        manifest = json.loads((ROOT / 'results/frontier14b/build.json').read_text())
        digest = hashlib.sha256((ROOT / 'candidates' / (NAME + '.py')).read_bytes()).hexdigest()
        self.assertEqual(SELECTION['sha256'], digest)
        self.assertEqual(PLAN['candidate_sha256'], digest)
        self.assertEqual(manifest['variants'][NAME]['sha256'], digest)

    def test_candidate_is_frontier13_plus_the_knob_rebinds(self):
        text = (ROOT / 'candidates' / (NAME + '.py')).read_bytes().decode('utf-8')
        self.assertEqual(text, build_f14.build(NAME))
        parent = build_f13.build('f13_c22_lock')
        self.assertTrue(text.startswith(parent))
        self.assertEqual(PLAN['control'], 'f13_c22_lock')
        self.assertEqual(hashlib.sha256(parent.encode('utf-8')).hexdigest(), PLAN['control_sha256'])
        tail = text[len(parent):]
        knobs = build_f14.VARIANTS[NAME][0]
        self.assertEqual([l for l in tail.splitlines() if l and not l.startswith('#')], ['%s = %r' % kv for kv in knobs.items()])
        for key in knobs:
            self.assertIn(chr(10) + key + ' = ', parent)  # every knob is a base global read at call time


class EntryPointTests(unittest.TestCase):
    def test_last_callable_is_the_lockstep_with_the_knobs_rebound(self):
        src = (ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8')
        fn = get_last_callable(src)
        self.assertEqual(fn.__name__, 'agent')
        self.assertEqual(fn.__globals__['_LK_PARENT'].__name__, 'ig_agent')
        for key, value in build_f14.VARIANTS[NAME][0].items():
            self.assertEqual(fn.__globals__[key], value, key)
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
