# Original Arturo-GA, Apache-2.0. Finance six new geese only when visible egg
# demand and a supply-aware projection cover land, workers and feeding.
_F19_GOOSE_PARENT=agent
_F19_GOOSE_STATE={}
_F19_GOOSE_REPORT=dict(f19_goose_checks=0,f19_goose_requests=0,f19_goose_committed=0,
 f19_goose_hired=0,f19_goose_harvested=0,f19_goose_sold=0,f19_goose_feed=0,
 f19_goose_rescue=0,f19_goose_errors=0,f19_goose_shortfalls=0)

def _f19_goose_request(obs,action,st):
    step=int(obs['step']);day,hour=divmod(step,24);seat=int(obs['player'])
    if st.get('requested_day')==day or hour>5:return action
    native=_IMPL.chassis.players[seat];farm=obs['farms'][seat]
    planned=_v219_native_day(native,day);market=action.get('market',[])
    if any(o and o[0]=='HIRE' for a in planned[hour+1:] for o in a.get('market',[])):return action
    expected=max(len(a.get('hands',[])) for a in planned)
    hires=sum(bool(o) and o[0]=='HIRE' for o in market)
    if len(farm['hands'])+hires!=expected:return action
    initial=not st.get('committed')
    if initial:
        if day not in (12,15) or set(farm['unlocked_quadrants'])!={'NW','NE','SW'}:return action
        if any(farm['tiles'][y][x]!='LOCKED' for y in (5,6) for x in range(5,8)):return action
        shops=obs['town']['unlocked_shops']
        if sum(s in ('BAKERY','BRUNCH_SPOT') for s in shops)<2:return action
        if any(o and o[0]=='BUY_LAND' for t in range(step,719) for o in _cs_tape(seat,t).get('market',[])):return action
        _F19_GOOSE_REPORT['f19_goose_checks']+=1
        value=_hd2_ev('GOOSE',6,obs,{})[0]
        # Fixed wage forecast uses the native daily peak; the actual request is
        # separately cash-checked. No future shops or rival private stock used.
        wages=0
        for d in range(day,29):
            crew=max(len(a.get('hands',[])) for a in _v219_native_day(native,d))
            wages+=_v219_fib(crew)+_v219_fib(crew+1)
        feed=6*(30-day)*max(20,int(obs['market']['prices']['WHEAT']))
        if value-4000-wages-feed<_F19_GOOSE_EDGE:return action
    stock=projected_shed(action,FarmView(obs))
    # Reserve only the new flock's daily food; the parent retains its own plans.
    food=6 if day<29 else 0
    extras=([['BUY_LAND'],['BUY_ANIMAL','GOOSE',6]] if initial else [])+([['BUY_PRODUCT','WHEAT',food]] if food else [])+[['HIRE'],['HIRE']]
    if len(market)+len(extras)>10 or any(o and o[0]=='BUY_LAND' for o in market):return action
    incoming=food+6*initial+sum(int(o[2]) for o in market if len(o)>=3 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL'))
    if sum(max(0,int(q)) for q in stock.values())+incoming>100:return action
    budget=5800*initial+food*(int(obs['market']['prices']['WHEAT'])+20)
    budget+=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+hires+2))
    for o in market:
        if len(o)>=3 and o[0]=='BUY_PRODUCT':budget+=int(o[2])*(int(obs['market']['prices'][o[1]])+20)
        elif len(o)>=3 and o[0]=='BUY_ANIMAL':budget+=int(o[2])*_Y_COST[o[1]]
        elif len(o)>=3 and o[0]=='BUY_SEED':budget+=int(o[2])*_Y_SEED[o[1]]
    if farm['money']<budget+1500:return action
    st['requested_day']=day;st['pending']=dict(first=expected+1,initial=initial)
    _F19_GOOSE_REPORT['f19_goose_requests']+=1;_F19_GOOSE_REPORT['f19_goose_feed']+=food
    return dict(action,market=[list(o) for o in market]+extras)

def _f19_goose_apply(obs,action):
    step=int(obs['step']);day,hour=divmod(step,24);seat=int(obs['player'])
    if step==0:_F19_GOOSE_STATE.clear()
    st=_F19_GOOSE_STATE.setdefault(seat,dict(day=-1,workers={},previous={},credit={'EGG':0,'FERTILIZER':0}))
    farm=obs['farms'][seat];private=obs['private']
    if day<12:return action
    if st['day']!=day:st['day']=day;st['workers']={};st['previous']={};st['rescued']=0
    for actor,before in st['previous'].items():
        if actor>=len(private['inventories']):continue
        product={'HARVEST':'EGG','COLLECT_FERTILIZER':'FERTILIZER'}.get(before['op'])
        if product:
            gain=max(0,private['inventories'][actor].get(product,0)-before['inventory'].get(product,0));st['credit'][product]+=gain
            if product=='EGG':_F19_GOOSE_REPORT['f19_goose_harvested']+=gain
    pending=st.pop('pending',None)
    if pending:
        ok='SE' in farm['unlocked_quadrants'] and (not pending['initial'] or private['shed'].get('GOOSE',0)>=6)
        if not ok or len(farm['hands'])<pending['first']+1:_F19_GOOSE_REPORT['f19_goose_shortfalls']+=1
        else:
            for i in (0,1):st['workers'][pending['first']+i]=[(x,5+i) for x in range(5,8)]
            _F19_GOOSE_REPORT['f19_goose_hired']+=2
            if pending['initial']:st['committed']=True;_F19_GOOSE_REPORT['f19_goose_committed']+=1
    action=_f19_goose_request(obs,action,st)
    if not st.get('committed'):return action
    commands=[list(action.get('farmer') or ['PASS'])]+[list(c) for c in action.get('hands',[])]
    commands += [['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
    st['previous']={}
    for actor,targets in st['workers'].items():
        cmd=_f19_goose_worker(obs,actor,targets);commands[actor]=cmd
        st['previous'][actor]=dict(op=cmd[0],inventory=dict(private['inventories'][actor]))
    market=[list(o) for o in action.get('market',[])];result=dict(action,farmer=commands[0],hands=commands[1:],market=market)
    stock=projected_shed(result,FarmView(obs))
    if day<29 and hour<=14 and st['workers'] and not st['rescued'] and len(market)<10:
        hungry=sum(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='GOOSE' and not farm['tiles'][y][x].get('fed_today') for ts in st['workers'].values() for x,y in ts)
        carried=sum(private['inventories'][i].get('WHEAT',0) for i in st['workers'])
        buying=sum(int(o[2]) for o in market if len(o)>=3 and o[:2]==['BUY_PRODUCT','WHEAT'])
        need=max(0,hungry-carried-stock.get('WHEAT',0)-buying)
        if need and need<=6 and sum(stock.values())+need<=100 and farm['money']>1500+need*(int(obs['market']['prices']['WHEAT'])+20):
            market.append(['BUY_PRODUCT','WHEAT',need]);st['rescued']=need;_F19_GOOSE_REPORT['f19_goose_rescue']+=need
    for item in ('EGG','FERTILIZER'):
        scheduled=sum(int(o[2]) for o in market if len(o)>=3 and o[:2]==['SELL',item])
        q=min(st['credit'][item],max(0,int(stock.get(item,0))-scheduled))
        if q and len(market)<10:
            market.append(['SELL',item,q]);st['credit'][item]-=q
            if item=='EGG':_F19_GOOSE_REPORT['f19_goose_sold']+=q
    return result

_F19_GOOSE_TELEMETRY={}
def agent(observation,configuration=None):
    if int(observation['step'])==0:
        for k in _F19_GOOSE_REPORT:_F19_GOOSE_REPORT[k]=0
    action=_F19_GOOSE_PARENT(observation,configuration)
    try:action=_f19_goose_apply(observation,action)
    except Exception:_F19_GOOSE_REPORT['f19_goose_errors']+=1
    _F19_GOOSE_TELEMETRY.clear();_F19_GOOSE_TELEMETRY.update(getattr(_F19_GOOSE_PARENT,'telemetry',{}));_F19_GOOSE_TELEMETRY.update(_F19_GOOSE_REPORT)
    return action
agent.telemetry=_F19_GOOSE_TELEMETRY
agent=globals().pop('agent')
