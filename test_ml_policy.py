"""Feature boundaries and proof that the learned option reaches the policy."""
import contextlib
import copy
import io
import hashlib
import json
from pathlib import Path
import unittest

import accelerator
import ml_features as features
from build_ml_policy import NAMES


class MLPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            from kaggle_environments.agent import get_last_callable
        cls.policies = {name: get_last_callable(Path('candidates', name + '.py').read_text(encoding='utf-8'))
                        for name in (*NAMES, 'ml_critic')}

    def test_official_export_is_option_wrapper(self):
        for fn in self.policies.values():
            self.assertIs(fn, fn.__globals__['agent'])
            self.assertIsNot(fn, fn.__globals__['_ML_PARENT'])

    def test_feature_schema_and_private_future_identity_invariance(self):
        obs = accelerator.load().Game(7).observe(0)
        before = features._ml_features(obs, obs['market']['inventory'])
        other = copy.deepcopy(obs)
        other.update(seed=123, opponent_name='never-a-feature', future_reward=999999,
                     opponent_private={'shed': {'MILK': 999}})
        self.assertEqual(before, features._ml_features(other, obs['market']['inventory']))
        self.assertEqual(len(before), len(features._ML_FEATURE_NAMES))

    def test_option_changes_horizon_only_when_selected(self):
        fn = self.policies['ml_h18']
        ns = fn.__globals__
        obs = accelerator.load().Game(7).observe(0)
        obs['step'] = 335
        ns['_ml_before'](obs, {})
        self.assertEqual(ns['_ml_horizon'](obs, 6), 6)
        obs['step'] = 336
        ns['_ml_before'](obs, {})
        self.assertEqual(ns['_ml_horizon'](obs, 6), 18)
        self.assertEqual(ns['_ML_REPORT']['ml_decisions'], 1)
        obs['step'] = 0
        ns['_ml_before'](obs, {})
        self.assertEqual(ns['_ml_horizon'](obs, 6), 6)

    def test_learned_export_matches_frozen_selection_and_hash(self):
        training = json.loads(Path('results/ml/training.json').read_text())
        model = Path('results/ml/model.json')
        self.assertEqual(hashlib.sha256(model.read_bytes()).hexdigest(), training['model_sha256'])
        source = Path('candidates/ml_critic.py')
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),
                         training['exported']['candidates']['ml_critic'])
        rows = [json.loads(line) for line in Path('results/ml/selection.jsonl').read_text().splitlines()]
        rows.sort(key=lambda r: (r['seed'], r['opponent'], r['seat']))
        ns = self.policies['ml_critic'].__globals__
        choices = [ns['_ml_choose'](r['features'], ns['_ML_MODEL']) for r in rows]
        self.assertEqual(choices, training['selected_gate']['choices'])
        plan = json.loads(Path('results/ml/plan.json').read_text())
        splits = [set(plan[k]) for k in ('training_seeds', 'selection_seeds', 'holdout_seeds',
                                        'official_confirmation_seeds')]
        self.assertEqual(len(set.union(*splits)), sum(map(len, splits)))


if __name__ == '__main__':
    unittest.main()
