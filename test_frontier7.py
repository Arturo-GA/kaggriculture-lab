"""Frontier7 build, entry-point and behaviour checks (python -m unittest -v test_frontier7.py)."""
import contextlib
import hashlib
import io
import json
import unittest
from pathlib import Path

import build_f7

with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

ROOT = Path(__file__).resolve().parent
SELECTION = json.loads((ROOT / 'results/frontier7/selection.json').read_text())
NAME = SELECTION['candidate']


class BuildTests(unittest.TestCase):
    def test_public_base_is_pinned(self):
        data = (ROOT / 'candidates/v48.py').read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), build_f7.V48_SHA256)

    def test_candidate_matches_selection_and_build_manifest(self):
        manifest = json.loads((ROOT / 'results/frontier7/build.json').read_text())
        digest = hashlib.sha256((ROOT / 'candidates' / (NAME + '.py')).read_bytes()).hexdigest()
        self.assertEqual(SELECTION['sha256'], digest)
        self.assertEqual(manifest['variants'][NAME]['sha256'], digest)

    def test_candidate_is_the_documented_transformation_of_v48(self):
        expected = build_f7.VARIANTS[NAME][0].encode('utf-8')
        self.assertEqual((ROOT / 'candidates' / (NAME + '.py')).read_bytes(), expected)
        text = expected.decode('utf-8')
        self.assertTrue(text.startswith(build_f7.v48))
        self.assertIn('agent=_e335_agent', text)
        self.assertIn('def _lk_simulate(', text)
        self.assertNotIn('def _hd_apply(', text)


class EntryPointTests(unittest.TestCase):
    def test_last_callable_is_agent_wrapping_the_v48_entry_point(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        self.assertEqual(fn.__name__, 'agent')
        self.assertIsInstance(getattr(fn, 'telemetry', None), dict)
        g = fn.__globals__
        # The lockstep layer must wrap V48's last layer (queue cleanup), not the V46-era `agent` it popped earlier.
        self.assertIs(g['_LK_PARENT'], g['_e335_agent'])

    def test_official_game_against_v48_completes_without_errors(self):
        fn = get_last_callable((ROOT / 'candidates' / (NAME + '.py')).read_text(encoding='utf-8'))
        rival = get_last_callable((ROOT / 'candidates/v48.py').read_text(encoding='utf-8'))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': 5998}, debug=True)
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
