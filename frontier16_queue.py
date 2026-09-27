# Frontier16: inventory-safe market queue assignment, Arturo-GA, Apache-2.0.
# Inspired by the public fixed-SELL closure in tetsutani / lynnsakurai (27 Sep).
# Original subset DP; uses the inherited attributed item-separable quote model.
# Fixed spending orders retain their order and may only move later. BUY_PRODUCT
# slots, unsafe sales, quantities and all physical commands remain unchanged.
_F16_PARENT=agent
_F16_FIXED=('HIRE','BUY_SEED','BUY_ANIMAL','BUY_LAND')
_F16_REPORT=dict(f16_turns=0,f16_passes=0,f16_reordered=0,f16_predicted_gain=0.0,
                 f16_cycles=0,f16_errors=0)


def _f16_queue(obs,action):
    orders=[list(o) for o in action.get('market',[])]
    if len(orders)<2:return action
    stock={k:max(0,int(v)) for k,v in projected_shed(action,FarmView(obs)).items()}
    counts={};bought=set()
    for o in orders:
        if len(o)>=3 and o[0]=='SELL' and int(o[2])>0:counts[o[1]]=counts.get(o[1],0)+1
        if len(o)>=3 and o[0]=='BUY_PRODUCT' and int(o[2])>0:bought.add(o[1])
    safe={i for i,o in enumerate(orders) if len(o)>=3 and o[0]=='SELL' and
          counts.get(o[1])==1 and o[1] not in bought and 0<int(o[2])<=stock.get(o[1],0)}
    fixed=[i for i,o in enumerate(orders) if o and o[0] in _F16_FIXED]
    if not safe or not fixed:return action
    sells=sorted(safe);slots=sorted(safe.union(fixed))
    if len(sells)>6:return action
    params=_v44y_params(obs);inventory=obs['market']['inventory'];weights=[]
    for i in sells:
        item=orders[i][1]
        if item not in params or item not in inventory:return action
        theirs=[o if len(o)>=3 and o[0] in ('SELL','BUY_PRODUCT') and o[1]==item else [] for o in orders]
        row=[]
        for slot in slots:
            mine=[[] for _ in orders];mine[slot]=orders[i]
            a,b=_v44y_lockstep(mine,theirs,{item:int(inventory[item])},
                {item:stock[item]},{item:stock[item]},{item:params[item]})
            row.append(a-b)
        weights.append(row)
    # A state needs only the subset of sales used; the number of fixed orders
    # consumed follows from the current slot and the subset's population count.
    dp={0:(0.0,())}
    for pos,slot in enumerate(slots):
        nxt={}
        for mask,(value,path) in dp.items():
            used_fixed=pos-mask.bit_count()
            if used_fixed<len(fixed) and slot>=fixed[used_fixed]:
                proposal=(value,path+(fixed[used_fixed],))
                if mask not in nxt or value>nxt[mask][0]+1e-9:nxt[mask]=proposal
            for j,index in enumerate(sells):
                if mask&(1<<j):continue
                key=mask|(1<<j);score=value+weights[j][pos]
                if key not in nxt or score>nxt[key][0]+1e-9:nxt[key]=(score,path+(index,))
        dp=nxt
    target=(1<<len(sells))-1
    if target not in dp:return action
    _,path=dp[target];trial=list(orders)
    for slot,index in zip(slots,path):trial[slot]=orders[index]
    if trial==orders:return action
    # Verify the DP proposal with the complete inherited factor model.
    margin=_v44y_factor_margin(orders,dict(inventory),stock,params)
    gain=margin(trial)-margin(orders)
    if gain<=0.5:return action
    _F16_REPORT['f16_reordered']+=1;_F16_REPORT['f16_predicted_gain']+=gain
    return dict(action,market=trial)


def agent(observation,configuration=None):
    action=_F16_PARENT(observation,configuration)
    step=int(observation['step'])
    if step==0:
        for k in _F16_REPORT:_F16_REPORT[k]=0
    standard=configuration is None or all(configuration.get(k,v)==v for k,v in
        [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)])
    try:
        if standard and step>=144 and _r37_similarity(observation)>=_F16_SIMILARITY:
            _F16_REPORT['f16_turns']+=1
            seen={tuple(tuple(o) for o in action.get('market',[]))}
            for _ in range(_F16_PASSES):
                _F16_REPORT['f16_passes']+=1
                proposal=_f16_queue(observation,action)
                key=tuple(tuple(o) for o in proposal.get('market',[]))
                if proposal==action:break
                if key in seen:
                    _F16_REPORT['f16_cycles']+=1;break
                seen.add(key);action=proposal
            state=_RACE_STATE.get(int(observation['player']))
            if state is not None and state.get('prev_action') is not None and state.get('step')==step:
                state['prev_action']=action
    except Exception:
        _F16_REPORT['f16_errors']+=1
    _F16_TELEMETRY.clear();_F16_TELEMETRY.update(getattr(_F16_PARENT,'telemetry',{}));_F16_TELEMETRY.update(_F16_REPORT)
    return action


_F16_TELEMETRY={}
agent.telemetry=_F16_TELEMETRY
agent=globals().pop('agent')
