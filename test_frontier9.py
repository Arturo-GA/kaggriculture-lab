"""Frontier9 build, entry-point and behaviour checks (python -m unittest -v test_frontier9.py)."""
import contextlib
import hashlib
import io
import json
import unittest
from pathlib import Path

import build_f9

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parent
SELECTION = json.loads((ROOT / 'results/frontier9/selection.json').read_text())
PLAN = json.loads((ROOT / 'results/frontier9/plan.json').read_text())
NAME = SELECTION['candidate']


class BuildTests(unittest.TestCase):
    def test_frontier8_base_is_pinned(self):
        digest = hashlib.sha256((ROOT / 'candidates/f8_stack_lock.py').read_bytes()).hexdigest()
        self.assertEqual(digest, build_f9.F8_SHA256)

    def test_candidate_matches_selection_and_build_manifest(self):
        manifest = json.loads((ROOT / 'results/frontier9/build.json').read_text())
        digest = hashlib.sha256((ROOT / 'candidates' / (NAME + '.py')).read_bytes()).hexdigest()
        self.assertEqual(SELECTION['sha256'], digest)
        self.assertEqual(manifest['variants'][NAME]['sha256'], digest)

    def test_candidate_is_the_documented_patch_of_frontier8(self):
        kmax = build_f9.VARIANTS[NAME][0]
        expected = build_f9.patched(kmax)
        if NAME.endswith('f'):
            expected = build_f9.full_lot(expected)
        text = (ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8')
        self.assertEqual(text, expected)
        self.assertIn('_F9_PRE_KMAX = %d' % kmax, text)
        self.assertIn('_CA_FEED_DAYS = 2', text)  # the public carrot feed reserve is untouched in the exported candidate
        self.assertNotIn('_F9_TRACK_PARENT', text)
        # everything outside the two documented edits is Frontier8
        base_lines = set(build_f9.BASE.split('\n'))
        added = [line for line in text.split('\n') if line not in base_lines]
        self.assertLess(len(added), 40, added[:5])

    def test_window_is_bounded_by_lot_over_drain(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        window = fn.__globals__['_f9_pre_window']
        no_shops = {'town': {'unlocked_shops': []}}
        three = {'town': {'unlocked_shops': ['SMOOTHIE_SHOP', 'ICE_CREAM_SHOP', 'BRUNCH_SPOT']}}
        yarn = {'town': {'unlocked_shops': ['YARN_STORE', 'YARN_STORE']}}
        kmax = build_f9.VARIANTS[NAME][0]
        self.assertEqual(window(no_shops, 'STRAWBERRY', 18), kmax)  # capped by KMAX
        self.assertEqual(window(three, 'STRAWBERRY', 2), 2)         # 2 / (3/4 + 1/24) = 2.5
        self.assertEqual(window(yarn, 'WOOL', 2), 1)                # 2 / (1 + 1/24) = 1.9
        self.assertEqual(window(three, 'MILK', 0), 0)


class EntryPointTests(unittest.TestCase):
    def test_last_callable_is_agent_with_telemetry(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        self.assertEqual(fn.__name__, 'agent')
        self.assertIsInstance(getattr(fn, 'telemetry', None), dict)
        g = fn.__globals__
        self.assertIs(g['_LK_PARENT'].telemetry, g['_EQ_REPORT'])

    def test_official_game_against_frontier8_completes_without_errors(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        rival = get_last_callable((ROOT / 'candidates' / (PLAN['control'] + '.py')).read_text(encoding='utf-8'))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': PLAN['unit_test_seed']}, debug=True)
            final = env.run([fn, rival])[-1]
        self.assertEqual([row['status'] for row in final], ['DONE', 'DONE'])
        self.assertEqual(len(env.steps), 720)
        errors = {k: v for k, v in fn.telemetry.items() if v and ('error' in k or 'fallback' in k)}
        self.assertEqual(errors, {})
        self.assertGreater(final[0]['reward'], final[1]['reward'], 'candidate should beat Frontier8 on this seed')


if __name__ == '__main__':
    unittest.main()
