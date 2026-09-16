"""Frontier4 build, entry-point and behaviour checks (python -m unittest -v test_frontier4.py)."""
import contextlib
import hashlib
import io
import json
import unittest
from pathlib import Path

import build_f4

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parent
SELECTION = json.loads((ROOT / 'results/frontier4/selection.json').read_text())
NAME = SELECTION['candidate']
SOURCES = {'f4_full': build_f4.base + build_f4.terminal, 'f4_r24': build_f4.base, 'f4_probe': build_f4.probe,
           'f4_adapt2': build_f4.adapt2, 'f4_adapt': build_f4.adapt, 'f4_term': build_f4.v45 + build_f4.terminal}


class BuildTests(unittest.TestCase):
    def test_public_base_is_pinned(self):
        data = (ROOT / 'candidates/v45.py').read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), build_f4.V45_SHA256)

    def test_candidate_matches_selection_and_build_manifest(self):
        manifest = json.loads((ROOT / 'results/frontier4/build.json').read_text())
        digest = hashlib.sha256((ROOT / 'candidates' / (NAME + '.py')).read_bytes()).hexdigest()
        self.assertEqual(SELECTION['sha256'], digest)
        self.assertEqual(manifest[NAME], digest)

    def test_candidate_is_the_documented_transformation_of_v45(self):
        expected = SOURCES[NAME].encode('utf-8')
        self.assertEqual((ROOT / 'candidates' / (NAME + '.py')).read_bytes(), expected)
        text = expected.decode('utf-8')
        self.assertIn('_RACE_HORIZON_ESCALATED=24', text)
        if NAME == 'f4_probe':
            self.assertIn('_F4_PROBE_LEVEL=24', text)
            self.assertIn('def _f4_rival_long(observation,state):', text)
            self.assertEqual(text.count('_RACE_HORIZON_CLONE=8'), 1)

    def test_rebuild_is_deterministic(self):
        before = (ROOT / 'candidates' / (NAME + '.py')).read_bytes()
        build_f4.write(NAME, SOURCES[NAME])
        self.assertEqual((ROOT / 'candidates' / (NAME + '.py')).read_bytes(), before)


class EntryPointTests(unittest.TestCase):
    def test_last_callable_is_agent_with_telemetry(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        self.assertEqual(fn.__name__, 'agent')
        self.assertIsInstance(getattr(fn, 'telemetry', None), dict)

    def test_official_game_against_v45_completes_without_errors(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        rival = get_last_callable((ROOT / 'candidates/v45.py').read_text(encoding='utf-8'))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': 5999}, debug=True)
            final = env.run([fn, rival])[-1]
        self.assertEqual([row['status'] for row in final], ['DONE', 'DONE'])
        self.assertEqual(len(env.steps), 720)
        telemetry = fn.telemetry
        errors = {k: v for k, v in telemetry.items() if v and ('error' in k or 'fallback' in k)}
        self.assertEqual(errors, {})
        self.assertGreater(telemetry.get('race_horizon_turns', 0), 0, 'clone race horizon never engaged')
        if NAME == 'f4_probe':
            self.assertIn('f4_probe_confirmed', telemetry)
        self.assertGreaterEqual(final[0]['reward'], final[1]['reward'], 'candidate should not lose the mirror on this seed')


if __name__ == '__main__':
    unittest.main()
