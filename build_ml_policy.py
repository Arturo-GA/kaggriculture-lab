"""Build forced options for causal training and export a learned option policy."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = '28f57454d8dab2618441d8ef2f1fe04924cf8291e069a5e2ed20daf28cded489'
NAMES = ('ml_native', 'ml_h2', 'ml_h8', 'ml_h12', 'ml_h18')
WRAPPER = '''
_ML_PARENT = agent
def agent(observation, configuration=None):
    _ml_before(observation, configuration)
    action = _ML_PARENT(observation, configuration)
    agent.telemetry = dict(getattr(_ML_PARENT, 'telemetry', {}), **_ML_REPORT)
    return action
agent.telemetry = {}
agent = globals().pop('agent')
'''


def build(model_path=None, name='ml_critic'):
    data = (ROOT / 'candidates/matched6.py').read_bytes()
    assert hashlib.sha256(data).hexdigest() == EXPECTED
    source = data.decode()
    features = (ROOT / 'ml_features.py').read_text(encoding='utf-8')
    # Preserve exact counterfactual-data hashes. The old tree evaluator is unused
    # by forced options; the learned export uses the corrected float32 evaluator.
    policy_path = ROOT / ('ml_policy.py' if model_path else 'results/ml/training_policy.py')
    policy = policy_path.read_text(encoding='utf-8')
    source = source.replace('def _r36_reserve(obs,action):', features + '\n' + policy + '\n\ndef _r36_reserve(obs,action):')
    anchor = '    if 288 <= step < 696:_R37_HORIZONS[player] = 6 if 336 <= step < 648 and state["streak"] >= 6 else 4'
    assert source.count(anchor) == 1
    source = source.replace(anchor, anchor + '\n    if 336 <= step < 648:_R37_HORIZONS[player] = _ml_horizon(observation,_R37_HORIZONS[player])')
    model = json.loads(Path(model_path).read_text()) if model_path else None
    targets = [(name, None)] if model else [(n, i) for i, n in enumerate(NAMES)]
    records = {}
    for candidate, force in targets:
        text = '# Modified 2026-09-12 Arturo-GA: trained economic option policy; Apache-2.0.\n' + source
        text += '\n_ML_FORCE_OPTION = ' + repr(force) + '\n_ML_MODEL = ' + repr(model) + '\n' + WRAPPER
        compile(text, candidate + '.py', 'exec')
        (ROOT / 'candidates' / (candidate + '.py')).write_bytes(text.encode())
        records[candidate] = hashlib.sha256(text.encode()).hexdigest()
    receipt = dict(parent_sha256=EXPECTED, candidates=records,
                   features_sha256=hashlib.sha256(features.encode()).hexdigest(),
                   policy_sha256=hashlib.sha256(policy.encode()).hexdigest(),
                   model_sha256=hashlib.sha256(Path(model_path).read_bytes()).hexdigest() if model else None)
    out = ROOT / 'results/ml'
    out.mkdir(parents=True, exist_ok=True)
    (out / ('build_' + name + '.json' if model else 'build_forced.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model')
    parser.add_argument('--name', default='ml_critic')
    args = parser.parse_args()
    print(json.dumps(build(args.model, args.name), indent=2))
