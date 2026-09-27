# Original Frontier17: inventory-neutral input-market search, Arturo-GA,
# Apache-2.0. Candidate quantities are bounded by observed capacity and cash.
# The rival queue is a scenario inferred from similar public farm layouts,
# never an observation of its hidden orders or private shed.
_F17_INPUT_PARENT=agent
_F17_INPUT_REPORT=dict(f17_input_turns=0,f17_input_units=0,f17_input_gain=0.,f17_input_errors=0)


def _f17_input_apply(obs,action):
    orders=[list(o) for o in action.get('market',[])]
    if len(orders)>8 or not orders:return action
    targets=[]
    for item in ('WHEAT','FERTILIZER'):
        buys=[i for i,o in enumerate(orders) if len(o)>=3 and o[:2]==['BUY_PRODUCT',item] and int(o[2])>0]
        if len(buys)==1 and not any(len(o)>=2 and o[:2]==['SELL',item] for o in orders):targets.append((item,buys[0]))
    if not targets:return action
    stock={k:max(0,int(v)) for k,v in projected_shed(action,FarmView(obs)).items()}
    purchases=sum(max(0,int(o[2])) for o in orders if len(o)>=3 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL'))
    room=100-sum(stock.values())-purchases
    if room<8:return action
    params=_v44y_params(obs);inventory=dict(obs['market']['inventory'])
    farm=obs['farms'][int(obs['player'])]
    cost=0;hires=int(farm.get('hires_today',0));land=len(farm['unlocked_quadrants'])-1
    for o in orders:
        if not o:continue
        if o[0]=='HIRE':cost+=_fib(hires+1);hires+=1
        elif o[0]=='BUY_LAND':cost+=(1000,2000,4000)[min(land,2)];land+=1
        elif len(o)>=3 and o[0]=='BUY_SEED':cost+=int(o[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[o[1]]
        elif len(o)>=3 and o[0]=='BUY_ANIMAL':cost+=int(o[2])*{'GOOSE':300,'COW':400,'SHEEP':500}[o[1]]
        elif len(o)>=3 and o[0]=='BUY_PRODUCT':cost+=int(o[2])*_r37_market_price(o[1],inventory[o[1]]-400,params)
    # Ignore sale income for funding; leave enough slack for a rival's larger buy.
    budget=float(farm['money'])-cost-1000
    if budget<=0:return action
    scenarios=[orders]
    if _F17_INPUT_ROBUST:
        # An aggressive sibling can put its input purchase at the first slot.
        front=sorted(enumerate(orders),key=lambda p:(0 if p[1] and p[1][0]=='BUY_PRODUCT' else 1,p[0]))
        early=[o for _,o in front]
        if early!=orders:scenarios.append(early)
    margins=[_v44y_factor_margin(op,inventory,stock,params) for op in scenarios]
    base=[f(orders) for f in margins];best=0.;chosen=None;chosen_q=0
    for item,index in targets:
        for q in (8,16,32,48):
            if q>room or q*_r37_market_price(item,inventory[item]-400,params)>budget:continue
            for before in range(index+1):
                for after in range(max(before+1,index+1),len(orders)+2):
                    trial=[list(o) for o in orders];trial.insert(before,['BUY_PRODUCT',item,q]);trial.insert(after,['SELL',item,q])
                    gains=[f(trial)-v for f,v in zip(margins,base)]
                    value=min(gains) if _F17_INPUT_ROBUST else gains[0]
                    if value>best+1e-9:
                        best=value;chosen=trial;chosen_q=q
    if chosen is None or best<2:return action
    _F17_INPUT_REPORT['f17_input_turns']+=1;_F17_INPUT_REPORT['f17_input_units']+=chosen_q;_F17_INPUT_REPORT['f17_input_gain']+=best
    result=dict(action,market=chosen)
    state=_RACE_STATE.get(int(obs['player']))
    if state is not None and state.get('step')==int(obs['step']):state['prev_action']=result
    return result


_F17_INPUT_TELEMETRY={}


def agent(observation,configuration=None):
    step=int(observation['step'])
    if step==0:
        for k in _F17_INPUT_REPORT:_F17_INPUT_REPORT[k]=0
    action=_F17_INPUT_PARENT(observation,configuration)
    try:
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in
            [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard and 144<=step<700 and _r37_similarity(observation)>=.95:action=_f17_input_apply(observation,action)
    except Exception:
        _F17_INPUT_REPORT['f17_input_errors']+=1
    _F17_INPUT_TELEMETRY.clear();_F17_INPUT_TELEMETRY.update(getattr(_F17_INPUT_PARENT,'telemetry',{}));_F17_INPUT_TELEMETRY.update(_F17_INPUT_REPORT)
    return action


agent.telemetry=_F17_INPUT_TELEMETRY
agent=globals().pop('agent')
