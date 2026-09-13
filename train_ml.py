"""Train on whole seed groups; select a gate using separate counterfactual games."""
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import sklearn
from sklearn.tree import DecisionTreeRegressor

from build_ml_policy import build, NAMES
from ml_features import _ML_FEATURE_NAMES
from ml_policy import _ml_choose, _ml_tree_predict

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results/ml'


def read_split(name):
    meta = json.loads((OUT / (name + '.meta.json')).read_text())
    assert meta['complete']
    rows = [json.loads(line) for line in (OUT / (name + '.jsonl')).read_text().splitlines()]
    return sorted(rows, key=lambda r: (r['seed'], r['opponent'], r['seat']))


def utility(row):
    return row['win'] + 0.5 * row['tie'] + 0.05 * np.tanh(row['margin'] / 3000)


def metrics(rows, choices):
    per_opponent = {}
    for row, choice in zip(rows, choices):
        chosen, base = row['options'][int(choice)], row['options'][0]
        group = per_opponent.setdefault(row['opponent'], dict(games=0, win_delta=0, score_delta=0.0,
                                                               utility_delta=0.0, interventions=0))
        group['games'] += 1
        group['win_delta'] += chosen['win'] - base['win']
        group['score_delta'] += chosen['win'] - base['win'] + 0.5 * (chosen['tie'] - base['tie'])
        group['utility_delta'] += float(utility(chosen) - utility(base))
        group['interventions'] += int(choice != 0)
    total = {key: sum(v[key] for v in per_opponent.values()) for key in next(iter(per_opponent.values()))}
    return dict(total=total, per_opponent=per_opponent,
                acceptable=all(v['win_delta'] >= 0 and v['score_delta'] >= 0 for v in per_opponent.values()))


def rank(result):
    t = result['metrics']['total']
    return result['metrics']['acceptable'], t['win_delta'], t['utility_delta'], -t['interventions']


def main():
    train, selection = read_split('train'), read_split('selection')
    plan = json.loads((OUT / 'plan.json').read_text())
    train_seeds = sorted({r['seed'] for r in train})
    assert set(train_seeds).isdisjoint({r['seed'] for r in selection})
    x = np.asarray([r['features'] for r in train], dtype=np.float64)
    y = np.asarray([[utility(o) - utility(r['options'][0]) for o in r['options']] for r in train])
    check_x = [r['features'] for r in train + selection]
    assert x.shape[1] == len(_ML_FEATURE_NAMES)
    rng = np.random.default_rng(20260912)
    trees, importances = [], []
    parity_checks = 0
    for tree_index in range(64):
        sampled = rng.choice(train_seeds, size=len(train_seeds), replace=True)
        indices = [i for seed in sampled for i, row in enumerate(train) if row['seed'] == seed]
        estimator = DecisionTreeRegressor(max_depth=4, min_samples_leaf=6, random_state=tree_index)
        estimator.fit(x[indices], y[indices])
        t = estimator.tree_
        tree = dict(left=t.children_left.tolist(), right=t.children_right.tolist(),
                    feature=t.feature.tolist(), threshold=t.threshold.tolist(), value=t.value[:, :, 0].tolist())
        reference = estimator.predict(check_x)
        exported = np.asarray([_ml_tree_predict(tree, features) for features in check_x])
        np.testing.assert_array_equal(reference, exported)
        parity_checks += len(check_x)
        trees.append(tree)
        importances.append(estimator.feature_importances_)
    model = dict(schema_version=1, feature_names=_ML_FEATURE_NAMES, options=list(NAMES), trees=trees)
    grid = []
    for quantile in plan['quantile_grid']:
        for threshold in plan['threshold_grid']:
            policy = dict(model, quantile=quantile, threshold=threshold)
            choices = [_ml_choose(r['features'], policy) for r in selection]
            grid.append(dict(quantile=quantile, threshold=threshold, choices=choices,
                             metrics=metrics(selection, choices)))
    # Explicit no-intervention candidate, even when all nonzero gates regress.
    grid.append(dict(quantile=0.1, threshold=2.0, choices=[0]*len(selection),
                     metrics=metrics(selection, [0]*len(selection))))
    best = max(grid, key=rank)
    model.update(quantile=best['quantile'], threshold=best['threshold'])
    constants = [dict(option=i, candidate=name, metrics=metrics(selection, [i]*len(selection)))
                 for i, name in enumerate(NAMES)]
    constant = max(constants, key=rank)
    model_path = OUT / 'model.json'
    model_path.write_text(json.dumps(model, separators=(',', ':')) + '\n')
    exported = build(model_path)
    importance = np.mean(importances, axis=0)
    report = dict(training_contexts=len(train), training_games=len(train)*5,
                  selection_contexts=len(selection), selection_games=len(selection)*5,
                  model_sha256=hashlib.sha256(model_path.read_bytes()).hexdigest(),
                  training_data_sha256=hashlib.sha256((OUT/'train.jsonl').read_bytes()).hexdigest(),
                  selection_data_sha256=hashlib.sha256((OUT/'selection.jsonl').read_bytes()).hexdigest(),
                  versions=dict(python=platform.python_version(), numpy=np.__version__, sklearn=sklearn.__version__),
                  export_exact_parity_checks=parity_checks, selected_gate=best, best_constant=constant,
                  grid=grid, constants=constants, exported=exported,
                  feature_importance=sorted([dict(feature=n, importance=float(v)) for n,v in
                                            zip(_ML_FEATURE_NAMES, importance)], key=lambda r:-r['importance']))
    (OUT/'training.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:report[k] for k in ['selected_gate','best_constant','export_exact_parity_checks']}, indent=2))


if __name__ == '__main__':
    main()
