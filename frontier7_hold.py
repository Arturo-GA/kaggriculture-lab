# ---- Frontier7 hold layer (Kaggriculture Lab, 18 September 2026) ----
# Milk and wool have linear/quadratic glut curves above the market's neutral inventory and recover only
# through town consumption (6 units a day per shop instance listing them, 12 for a yarn store, plus one
# a day from the town centre). The public tape sells them in bursts right after each harvest, so both
# clones push the inventory far above neutral and split the crash. This layer withholds those two
# products while the observed price is below the neutral price and releases them in small lots when the
# inventory is back at neutral, but only when the town's daily consumption can absorb both farms'
# inflow (estimated from our own recent inflow, doubled). Shed headroom, cash, and the last day stay
# with the public tape: held stock never exceeds what the shed can take if every hand dropped its load
# (limit 95 with the carried units counted), is drained from day 27.5 and
# is released entirely before day 29. Nothing else in the action changes.
_HD_PARENT=agent
_HD_SHOPS={"BAKERY":("EGG","WHEAT"),"PIZZA_SHOP":("MILK","TOMATO","WHEAT"),"BRUNCH_SPOT":("EGG","WHEAT","STRAWBERRY"),"YARN_STORE":("WOOL",),"ICE_CREAM_SHOP":("STRAWBERRY","MILK","WHEAT"),"PET_CAFE":("CARROT",),"SMOOTHIE_SHOP":("STRAWBERRY","MILK"),"FARMERS_MARKET":("WHEAT","CARROT","TOMATO","STRAWBERRY")}
_HD_ITEMS=('MILK','WOOL')
_HD_SLACK=0
_HD_RATIO=1.0
_HD_LOT=3
_HD_MAX_HOLD=40
_HD_LIMIT=95
_HD_FROM=192
_HD_RELEASE_FROM=660
_HD_OFF=696
_HD_MIN_MONEY=1500
_HD_WINDOW=72
_HD_STATE={}
_HD_REPORT=dict(hd_turns=0,hd_held=0,hd_released=0,hd_forced=0,hd_errors=0)

def _hd_params(obs):
    params={k:dict(v) for k,v in _R37_MARKET_PARAMS.items()}
    for k,patch in (obs['market'].get('params') or {}).items():
        if k in params and isinstance(patch,dict):params[k].update(patch)
    return params

def _hd_consumption(shops,item):
    return 6*sum((2 if len(_HD_SHOPS[s])==1 else 1) for s in shops if s in _HD_SHOPS and item in _HD_SHOPS[s])+1

def _hd_effective(orders,shed):
    stock=dict(shed);sold={}
    for o in orders:
        if o and len(o)>=3 and o[0]=='SELL':
            q=min(max(0,int(o[2])),max(0,int(stock.get(o[1],0))));stock[o[1]]=stock.get(o[1],0)-q;sold[o[1]]=sold.get(o[1],0)+q
    return sold

def _hd_free(orders,private):
    """Units the shed could still take if every hand dropped its load now (or at the night drop)."""
    stock,_,_=_r97_market_stock(private['shed'],orders)
    carried=sum(max(0,int(n)) for bag in private['inventories'] for n in bag.values())
    return _HD_LIMIT-sum(max(0,int(v)) for v in stock.values())-carried

def _hd_set(orders,item,q):
    """Give the item exactly one SELL slot of q units (q=0 blanks the tape's slots); every other index is kept."""
    idx=[i for i,o in enumerate(orders) if o and len(o)>=3 and o[0]=='SELL' and o[1]==item]
    for i in idx[1:]:orders[i]=[]
    if q<=0:
        if idx:orders[idx[0]]=[]
        return True
    if idx:
        orders[idx[0]]=['SELL',item,int(q)];return True
    holes=[i for i,o in enumerate(orders) if not o]
    if holes:orders[holes[0]]=['SELL',item,int(q)];return True
    if len(orders)<10:orders.append(['SELL',item,int(q)]);return True
    return False

def _hd_apply(obs,action):
    step=int(obs['step']);player=int(obs['player']);hour=step%24
    st=_HD_STATE.get(player)
    if st is None or step<=st['step']:st=_HD_STATE[player]={'step':-1,'last':{},'sold':{},'inflow':{it:[] for it in _HD_ITEMS}}
    shed=obs['private']['shed']
    for it in _HD_ITEMS:
        cur=max(0,int(shed.get(it,0)));prev=st['last'].get(it)
        if prev is not None:st['inflow'][it].append((step,max(0,cur-prev+int(st['sold'].get(it,0)))))
        st['inflow'][it]=[e for e in st['inflow'][it] if e[0]>step-_HD_WINDOW]
        st['last'][it]=cur
    st['step']=step
    orders=[list(o) if isinstance(o,(list,tuple)) else [] for o in (action.get('market') or [])]
    farm=obs['farms'][player]
    def done(final):
        st['sold']=_hd_effective(orders if final is None else final,shed)
        return action if final is None else dict(action,market=final)
    if step<_HD_FROM or step>=_HD_OFF or float(farm['money'])<_HD_MIN_MONEY or len(st['inflow'][_HD_ITEMS[0]])<24:
        return done(None)
    params=_hd_params(obs);prices=obs['market']['prices'];shops=list((obs.get('town') or {}).get('unlocked_shops') or [])
    _,private=_r127_fields(obs,action)
    planned=_hd_effective(orders,private['shed']);changed=False;forced=0
    for it in _HD_ITEMS:
        avail=max(0,int(private['shed'].get(it,0)))
        if avail<=0:continue
        rate=sum(q for _,q in st['inflow'][it])*24.0/_HD_WINDOW
        if rate<=0 or _hd_consumption(shops,it)<_HD_RATIO*2.0*rate:continue
        threshold=_r37_market_price(it,int(params[it]['I0'])+_HD_SLACK,params)
        if step>=_HD_RELEASE_FROM:q=min(avail,max(_HD_LOT,-(-avail//max(1,(_HD_OFF-step)//2))))
        elif int(prices.get(it,0))>=threshold:q=min(avail,_HD_LOT)
        else:q=0
        if avail-q>_HD_MAX_HOLD:forced+=avail-_HD_MAX_HOLD-q;q=avail-_HD_MAX_HOLD
        trial=[list(o) for o in orders]
        if not _hd_set(trial,it,q):continue
        free=_hd_free(trial,private)
        if free<0:
            extra=min(avail-q,-free)
            if extra>0:
                q+=extra;forced+=extra
                if not _hd_set(trial,it,q):continue
        if trial!=orders:
            orders=trial;changed=True
            before=int(planned.get(it,0))
            if q<before:_HD_REPORT['hd_held']+=before-q
            elif q>before:_HD_REPORT['hd_released']+=q-before
    if not changed:return done(None)
    _HD_REPORT['hd_turns']+=1;_HD_REPORT['hd_forced']+=forced
    return done(orders)

def agent(observation,configuration=None):
    action=_HD_PARENT(observation,configuration)
    try:
        step=int(observation['step'])
        if step==0:_HD_REPORT.update(hd_turns=0,hd_held=0,hd_released=0,hd_forced=0,hd_errors=0)
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('townShopSellInterval',4),('townCenterSellInterval',24)])
        if standard:
            action=_hd_apply(observation,action)
            st=_RACE_STATE.get(int(observation['player']))
            if st is not None and st.get('prev_action') is not None and st.get('step')==step:st['prev_action']=action
    except Exception:
        _HD_REPORT['hd_errors']+=1
    _HD_TELEMETRY.clear();_HD_TELEMETRY.update(getattr(_HD_PARENT,'telemetry',{}));_HD_TELEMETRY.update(_HD_REPORT)
    return action
_HD_TELEMETRY={}
agent.telemetry=_HD_TELEMETRY
agent=globals().pop('agent')
