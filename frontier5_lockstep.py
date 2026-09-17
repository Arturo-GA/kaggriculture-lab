# ==== Frontier5 lockstep sale ordering against a copy of ourselves (Arturo-GA, Apache-2.0) ====
# The engine settles market orders index by index and quotes both players' current units at the same inventory.
# Against a rival that executes our own tape (public farm similarity >= 0.90 after step 144), the rival's market list
# is assumed to be the list our parent produced; we replay the engine's per-unit lockstep for permutations of our own
# SELL orders (same slots, same quantities, same items) and keep the permutation with the best modeled cash margin.
# Nothing is added, removed or resized; non-SELL orders keep their positions.  Idea after seyitkaangunes' "V44 + four
# market layers" (lockstep layer); own implementation on this chassis's exact price function.
_LK_PARENT=agent
_LK_FROM=144
_LK_TO=719
_LK_MIN_SIMILARITY=0.90
_LK_MIN_GAIN=3.0
_LK_MAX_PERM=5
_LK_STATE={}
_LK_REPORT=dict(lk_turns=0,lk_reordered=0,lk_gain=0.0,lk_errors=0)


def _lk_params(obs):
    params={k:dict(v) for k,v in _R37_MARKET_PARAMS.items()}
    for k,patch in obs['market'].get('params',{}).items():
        if k in params:params[k].update(patch)
    return params


def _lk_simulate(ours,theirs,inventory,stock_a,stock_b,params):
    inv=dict(inventory);sa=dict(stock_a);sb=dict(stock_b);rev_a=rev_b=0.0
    n=max(len(ours),len(theirs))
    for i in range(n):
        oa=ours[i] if i<len(ours) else None;ob=theirs[i] if i<len(theirs) else None
        ra=[oa[1],int(oa[2])] if oa and oa[0]=='SELL' and len(oa)>=3 and oa[1] in params else None
        rb=[ob[1],int(ob[2])] if ob and ob[0]=='SELL' and len(ob)>=3 and ob[1] in params else None
        guard=0
        while ((ra and ra[1]>0) or (rb and rb[1]>0)) and guard<400:
            guard+=1;qa=qb=None
            if ra and ra[1]>0:
                if sa.get(ra[0],0)<=0:ra[1]=0
                else:qa=_r37_market_price(ra[0],inv.get(ra[0],10000),params)
            if rb and rb[1]>0:
                if sb.get(rb[0],0)<=0:rb[1]=0
                else:qb=_r37_market_price(rb[0],inv.get(rb[0],10000),params)
            if qa is None and qb is None:break
            if qa is not None:
                sa[ra[0]]-=1;rev_a+=qa;ra[1]-=1
                if qa>1:inv[ra[0]]=inv.get(ra[0],10000)+1
            if qb is not None:
                sb[rb[0]]-=1;rev_b+=qb;rb[1]-=1
                if qb>1:inv[rb[0]]=inv.get(rb[0],10000)+1
    return rev_a,rev_b


def _lk_permutations(items):
    if len(items)<=1:
        yield list(items);return
    for i,head in enumerate(items):
        for rest in _lk_permutations(items[:i]+items[i+1:]):
            yield [head]+rest


def _lk_reorder(obs,action):
    step=int(obs['step'])
    if not _LK_FROM<=step<=_LK_TO or _r37_similarity(obs)<_LK_MIN_SIMILARITY:return action
    market=[list(o) for o in (action.get('market') or []) if o]
    slots=[i for i,o in enumerate(market) if o[0]=='SELL' and len(o)>=3 and o[1] in _R37_MARKET_PARAMS]
    if len(slots)<2:return action
    for i in slots:
        try:market[i][2]=int(market[i][2])
        except Exception:return action
        if market[i][2]<=0:return action
    if len({market[i][1] for i in slots})<2:return action
    _LK_REPORT['lk_turns']+=1
    params=_lk_params(obs)
    stock=projected_shed(action,FarmView(obs))
    if not isinstance(stock,dict):
        stock=obs['private'].get('shed') or {}
    stock={k:max(0,int(v)) for k,v in stock.items() if isinstance(v,(int,float))}
    inventory=dict(obs['market']['inventory'])
    theirs=[list(o) for o in market]
    base_a,base_b=_lk_simulate(market,theirs,inventory,stock,stock,params)
    best=(base_a-base_b,None)
    sells=[market[i] for i in slots]
    if len(slots)<=_LK_MAX_PERM:
        candidates=_lk_permutations(sells)
    else:
        def swaps():
            for x in range(len(sells)):
                for y in range(x+1,len(sells)):
                    c=list(sells);c[x],c[y]=c[y],c[x];yield c
        candidates=swaps()
    for perm in candidates:
        trial=list(market)
        for i,o in zip(slots,perm):trial[i]=o
        a,b=_lk_simulate(trial,theirs,inventory,stock,stock,params)
        if a-b>best[0]+1e-9:best=(a-b,trial)
    if best[1] is None or best[0]-(base_a-base_b)<_LK_MIN_GAIN:return action
    _LK_REPORT['lk_reordered']+=1;_LK_REPORT['lk_gain']+=best[0]-(base_a-base_b)
    return dict(action,market=best[1])


def agent(observation,configuration=None):
    action=_LK_PARENT(observation,configuration)
    try:
        step=int(observation['step'])
        if step==0:_LK_REPORT.update(lk_turns=0,lk_reordered=0,lk_gain=0.0,lk_errors=0)
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)])
        if standard:
            action=_lk_reorder(observation,action)
            st=_RACE_STATE.get(int(observation['player']))
            if st is not None and st.get('prev_action') is not None and st.get('step')==step:st['prev_action']=action
    except Exception:
        _LK_REPORT['lk_errors']+=1
    _LK_TELEMETRY.clear();_LK_TELEMETRY.update(getattr(_LK_PARENT,'telemetry',{}));_LK_TELEMETRY.update(_LK_REPORT)
    return action
_LK_TELEMETRY={}
agent.telemetry=_LK_TELEMETRY
agent=globals().pop('agent')
