"""Learn when to deploy the original joint workforce/input/route planner."""
_FRONTIER_HISTORY={}
_FRONTIER_STATE={}


def _frontier_features(obs,plan):
    features=_ml_features(obs,_FRONTIER_HISTORY.get(obs['player'],{}))
    features += [plan['predicted_net']/10000,plan['hire_cost']/1000,
                 plan['unassigned']/100,plan['planned_workers']/20,plan['input_purchase']/50]
    totals={item:0 for item in _ML_PRODUCTS}
    for route in plan['plans']:
        for item,q in route['products'].items():totals[item]+=q
    features += [totals[item]/100 for item in _ML_PRODUCTS]
    return features


def _frontier_choose(features,model):
    values=sorted(_ml_tree_predict(t,features)[1] for t in model['trees'])
    return int(values[int(model['quantile']*(len(values)-1))]>model['threshold'])


def _frontier_before(obs,configuration):
    step=obs['step'];seat=obs['player']
    if step==0:_FRONTIER_HISTORY.pop(seat,None);_FRONTIER_STATE.pop(seat,None)
    if step==648:_FRONTIER_HISTORY[seat]=dict(obs['market']['inventory'])
    if step!=696:return
    plan=_au_plan(obs,configuration)
    features=_frontier_features(obs,plan)
    choice=_FRONTIER_FORCE if _FRONTIER_FORCE is not None else _frontier_choose(features,_FRONTIER_MODEL)
    _FRONTIER_STATE[seat]=dict(features=features,choice=choice)
    if choice:_AU_STATE[seat]=plan


_FRONTIER_PARENT=agent
def agent(observation,configuration=None):
    _frontier_before(observation,configuration)
    st=_FRONTIER_STATE.get(observation['player'],{})
    # The inherited auction wrapper is bypassed when the learned selector abstains.
    if observation['step']>=696 and not st.get('choice',0):
        action=_AU_PARENT(observation,configuration)
        telemetry=getattr(agent,'telemetry',{})
    else:
        action=_FRONTIER_PARENT(observation,configuration)
        telemetry=getattr(agent,'telemetry',{})
    agent.telemetry=dict(telemetry,frontier_choice=st.get('choice',0),frontier_decisions=int(bool(st)))
    return action
agent.telemetry={}
agent=globals().pop('agent')
