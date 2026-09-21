"""Frontier10C build, entry-point and behaviour checks (python -m unittest -v test_frontier10c.py)."""
import contextlib
import hashlib
import io
import json
import unittest
from pathlib import Path

import build_f10

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parent
SELECTION = json.loads((ROOT / 'results/frontier10c/selection.json').read_text())
PLAN = json.loads((ROOT / 'results/frontier10c/plan.json').read_text())
NAME = SELECTION['candidate']


class BuildTests(unittest.TestCase):
    def test_public_bases_are_pinned(self):
        for name, prefix in build_f10.PINS.items():
            digest = hashlib.sha256((ROOT / 'candidates' / (name + '.py')).read_bytes()).hexdigest()
            self.assertTrue(digest.startswith(prefix), name)

    def test_candidate_matches_selection_and_build_manifest(self):
        manifest = json.loads((ROOT / 'results/frontier10/build.json').read_text())
        digest = hashlib.sha256((ROOT / 'candidates' / (NAME + '.py')).read_bytes()).hexdigest()
        self.assertEqual(SELECTION['sha256'], digest)
        self.assertEqual(manifest['variants'][NAME]['sha256'], digest)

    def test_candidate_is_the_public_base_plus_the_documented_layers(self):
        text = (ROOT / 'candidates' / (NAME + '.py')).read_bytes().decode('utf-8')
        self.assertEqual(text, build_f10.build(NAME))
        base_name, kmax, lock, _ = build_f10.VARIANTS[NAME]
        base = build_f10.load(base_name)
        if lock and not kmax:
            self.assertTrue(text.startswith(base.rstrip(chr(13) + chr(10))))
            self.assertIn('def _lk_simulate(', text)
            self.assertNotIn('_F9_PRE_KMAX', text)
        if kmax:
            self.assertIn('_F9_PRE_KMAX = %d' % kmax, text)


class EntryPointTests(unittest.TestCase):
    def test_last_callable_wraps_the_public_entry_point(self):
        src = (ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8')
        fn = get_last_callable(src)
        self.assertEqual(fn.__name__, 'agent')
        if build_f10.VARIANTS[NAME][2]:
            g = fn.__globals__
            base_src = (ROOT / 'candidates' / (build_f10.VARIANTS[NAME][0] + '.py')).read_text(encoding='utf-8')
            self.assertEqual(g['_LK_PARENT'].__name__, get_last_callable(base_src).__name__)
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
        self.assertGreater(final[0]['reward'], final[1]['reward'], 'candidate should beat the unguarded f10_omw_lock on this seed')


if __name__ == '__main__':
    unittest.main()
