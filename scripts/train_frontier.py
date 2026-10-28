"""Seed-group bootstrapping and independent selection for the joint planner."""
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import sklearn
from sklearn.tree import DecisionTreeRegressor

from build_frontier import build
from ml_features import _ML_FEATURE_NAMES, _ML_PRODUCTS
from ml_policy import _ml_tree_predict
from train_ml import utility, metrics

OUT=Path('results/gold')
FEATURES=_ML_FEATURE_NAMES+['plan_net','plan_hire_cost','plan_unassigned','plan_workers','plan_input_buy']+['plan_'+p for p in _ML_PRODUCTS]


def choose(features,model):
    values=sorted(_ml_tree_predict(t,features)[1] for t in model['trees'])
    return int(values[int(model['quantile']*(len(values)-1))]>model['threshold'])


def read_split(name):
    path=OUT/('frontier_'+name+'.jsonl')
    meta=json.loads(path.with_suffix('.meta.json').read_text());assert meta['complete']
    rows=sorted([json.loads(s) for s in path.read_text().splitlines()],key=lambda r:(r['seed'],r['opponent'],r['seat']))
    assert len(rows)==meta['contexts']
    assert len({(r['seed'],r['opponent'],r['seat']) for r in rows})==len(rows)
    for row in rows:
        assert len(row['features'])==109
        assert row['options'][0]['prefix_sha256']==row['options'][1]['prefix_sha256']
        for i,o in enumerate(row['options']):
            assert o['status']==['DONE','DONE'] and o['calls']==719
            assert o['telemetry']['frontier_decisions']==1 and o['telemetry']['frontier_choice']==i
    return rows


def rank(item):
    m=item['metrics'];t=m['total']
    return m['acceptable'],t['score_delta'],t['utility_delta'],-t['interventions']


def main():
    train,selection=read_split('train'),read_split('selection')
    seeds=sorted({r['seed'] for r in train});assert set(seeds).isdisjoint(r['seed'] for r in selection)
    x=np.asarray([r['features'] for r in train]);assert x.shape[1]==len(FEATURES)
    y=np.asarray([[utility(o)-utility(r['options'][0]) for o in r['options']] for r in train])
    checks=[r['features'] for r in train+selection]
    rng=np.random.default_rng(20260913);trees=[];importance=[]
    for index in range(64):
        sample=rng.choice(seeds,size=len(seeds),replace=True)
        ix=[i for s in sample for i,r in enumerate(train) if r['seed']==s]
        estimator=DecisionTreeRegressor(max_depth=4,min_samples_leaf=8,random_state=index).fit(x[ix],y[ix])
        t=estimator.tree_
        tree=dict(left=t.children_left.tolist(),right=t.children_right.tolist(),feature=t.feature.tolist(),
                  threshold=t.threshold.tolist(),value=t.value[:,:,0].tolist())
        np.testing.assert_array_equal(estimator.predict(checks),np.asarray([_ml_tree_predict(tree,f) for f in checks]))
        trees.append(tree);importance.append(estimator.feature_importances_)
    model=dict(schema_version=1,feature_names=FEATURES,options=['native','joint_planner'],trees=trees)
    grid=[]
    for q in (.1,.25,.5):
        for threshold in (0,.001,.005,.01,.025,.05,.1,.2):
            policy=dict(model,quantile=q,threshold=threshold)
            choices=[choose(r['features'],policy) for r in selection]
            grid.append(dict(quantile=q,threshold=threshold,choices=choices,metrics=metrics(selection,choices)))
    grid.append(dict(quantile=.1,threshold=2.,choices=[0]*len(selection),metrics=metrics(selection,[0]*len(selection))))
    best=max(grid,key=rank);model.update(quantile=best['quantile'],threshold=best['threshold'])
    path=OUT/'frontier_model.json';path.write_text(json.dumps(model,separators=(',',':'))+'\n')
    exported=build(path)
    report=dict(training_contexts=len(train),training_games=2*len(train),selection_contexts=len(selection),
                selection_games=2*len(selection),export_exact_parity_checks=64*len(checks),selected_gate=best,
                constants=[dict(option=i,metrics=metrics(selection,[i]*len(selection))) for i in (0,1)],grid=grid,
                exported=exported,sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                [path,OUT/'frontier_train.jsonl',OUT/'frontier_selection.jsonl']},
                versions=dict(python=platform.python_version(),numpy=np.__version__,sklearn=sklearn.__version__),
                feature_importance=sorted([dict(feature=n,importance=float(v)) for n,v in zip(FEATURES,np.mean(importance,axis=0))],key=lambda r:-r['importance']))
    (OUT/'frontier_training.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['selected_gate','constants','exported','export_exact_parity_checks']},indent=2))


if __name__=='__main__':main()
