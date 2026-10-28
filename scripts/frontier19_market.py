# Original Arturo-GA, Apache-2.0. Bounded responses to alternative observable-
# clone queue policies. All permutations retain physical actions and quantities.
_F19_MARKET_PARENT=agent
_F19_MARKET_REPORT=dict(f19_market_calls=0,f19_market_changed=0,f19_market_evals=0,f19_market_errors=0)

def _f19_key(orders):return tuple(tuple(o) for o in orders)

def _f19_permutations(orders,stock):
    bought={o[1] for o in orders if len(o)>=3 and o[0]=='BUY_PRODUCT' and int(o[2])>0}
    totals={}
    for o in orders:
        if len(o)>=3 and o[0]=='SELL':totals[o[1]]=totals.get(o[1],0)+max(0,int(o[2]))
    safe={p for p,q in totals.items() if p not in bought and q<=stock.get(p,0)}
    slots=[];sells=[];fixed=[];fixed_at=[]
    for i,o in enumerate(orders):
        if o and o[0] in ('BUY_SEED','BUY_ANIMAL','HIRE','BUY_LAND'):
            slots.append(i);fixed.append(o);fixed_at.append(i)
        elif len(o)>=3 and o[0]=='SELL' and o[1] in safe:
            slots.append(i);sells.append(o)
    yield orders
    if not sells or len(slots)<2:return
    seen={_f19_key(orders)};count=0
    # One permutation of positions already assigns every labelled SELL; do not
    # multiply by permutations of the same sells a second time.
    for places in _cxd_it.permutations(slots,len(sells)):
        rest=[i for i in slots if i not in places]
        if any(new<old for new,old in zip(rest,fixed_at)):continue
        trial=list(orders)
        for i,o in zip(places,sells):trial[i]=o
        for i,o in zip(rest,fixed):trial[i]=o
        key=_f19_key(trial)
        if key in seen:continue
        seen.add(key);yield trial;count+=1
        if count>=160:return

def _f19_response(orders,stock,inventory,params):
    f=_v44y_factor_margin(orders,inventory,stock,params)
    best=orders;value=f(orders)
    for trial in _f19_permutations(orders,stock):
        v=f(trial);_F19_MARKET_REPORT['f19_market_evals']+=1
        if v>value+.5:best=trial;value=v
    return best

def _f19_market(obs,action):
    if int(obs['step'])<144 or _r37_similarity(obs)<.95:return action
    orders=[list(o) for o in action.get('market',[])];n=len(orders)
    if not 2<=n<=10:return action
    stock={p:max(0,int(q)) for p,q in projected_shed(action,FarmView(obs)).items()}
    inventory=dict(obs['market']['inventory']);params=_v44y_params(obs)
    current=orders;orbit=[orders];seen={_f19_key(orders)}
    for _ in range(_F19_MARKET_DEPTH):
        nxt=_f19_response(current,stock,inventory,params);key=_f19_key(nxt)
        if key in seen:break
        seen.add(key);orbit.append(nxt);current=nxt
    if len(orbit)<2:return action
    if _F19_MARKET_MODE=='last':best=current
    else:
        # Maximize the minimum *improvement from this same base* across an
        # unmodified queue and its best response. Never compare raw worst-case
        # margins from different opponents as if they were policy gains.
        models=[orders,orbit[1]]
        scores=[_v44y_factor_margin(m,inventory,stock,params) for m in models]
        base=[f(orders) for f in scores];gain=.5;best=orders
        for trial in _f19_permutations(orders,stock):
            delta=min(f(trial)-b for f,b in zip(scores,base))
            _F19_MARKET_REPORT['f19_market_evals']+=len(scores)
            if delta>gain:gain=delta;best=trial
    if best==orders:return action
    _F19_MARKET_REPORT['f19_market_changed']+=1
    result=dict(action,market=best)
    st=_RACE_STATE.get(int(obs['player']))
    if st is not None and st.get('step')==int(obs['step']):st['prev_action']=result
    return result

_F19_MARKET_TELEMETRY={}
def agent(observation,configuration=None):
    if int(observation['step'])==0:
        for k in _F19_MARKET_REPORT:_F19_MARKET_REPORT[k]=0
    action=_F19_MARKET_PARENT(observation,configuration)
    try:
        _F19_MARKET_REPORT['f19_market_calls']+=1
        action=_f19_market(observation,action)
    except Exception:_F19_MARKET_REPORT['f19_market_errors']+=1
    _F19_MARKET_TELEMETRY.clear();_F19_MARKET_TELEMETRY.update(getattr(_F19_MARKET_PARENT,'telemetry',{}));_F19_MARKET_TELEMETRY.update(_F19_MARKET_REPORT)
    return action
agent.telemetry=_F19_MARKET_TELEMETRY
agent=globals().pop('agent')
