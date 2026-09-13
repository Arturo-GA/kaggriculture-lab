"""Original late-season crop portfolio coordinated with terminal routing.

Only switches a finite crop when its terminal harvest remains inside the carrot
life window. Decisions use public prices and a joint own/rival supply scenario.
"""
_PF_STATE={}


def _pf_before(obs,config):
    seat=obs['player'];step=obs['step']
    st=_PF_STATE.get(seat)
    if st is None or step<=st['step']:
        st=_PF_STATE[seat]=dict(step=-1,enabled=False,buy=0,budget=0,
            replacements=0,seed_requests=0,decisions=0,errors=0,choice_days=[],pending=[],confirmed=0,missed=0)
    for x,y,day in st['pending']:
        tile=obs['farms'][seat]['tiles'][y][x]
        ok=isinstance(tile,dict) and tile.get('crop')=='CARROT' and tile.get('planted_day')==day
        st['confirmed']+=ok;st['missed']+=not ok
    st['pending']=[];st['step']=step
    if step not in (624,648):return
    farm=obs['farms'][seat];rival=obs['farms'][1-seat]
    inventory=obs['market']['inventory']
    # Optimize a small coupled portfolio, charging its own projected price impact.
    wheat=[];carrot=[]
    for other in (farm,rival):
        for row in other['tiles']:
            for tile in row:
                if not isinstance(tile,dict):continue
                if tile.get('crop')=='WHEAT':wheat.append(tile)
                if tile.get('crop')=='CARROT':carrot.append(tile)
    projected_wheat=inventory['WHEAT']+sum(t.get('yield_units',0) for t in wheat)
    projected_carrot=inventory['CARROT']+sum(t.get('yield_units',0) for t in carrot)
    wheat_price=_r37_market_price('WHEAT',projected_wheat)
    native=_IMPL.chassis.players.get(seat,{})
    route=native.get('route',0)
    planned=sum(c==['PLANT','WHEAT'] for t in range(step,step+24)
                for c in [_IMPL.chassis.routes[2 if t>=648 else route][t].get('farmer'),
                          *_IMPL.chassis.routes[2 if t>=648 else route][t].get('hands',[])])
    quota=0
    for count in range(1,min(24,planned)+1):
        # Native wheat seed purchases are retained and therefore are sunk costs.
        carrot_price=_r37_market_price('CARROT',projected_carrot+4*count)
        if 4*carrot_price-20 < _PF_THRESHOLD*5*wheat_price:break
        quota=count
    st['enabled']=quota>0;st['budget']=quota;st['decisions']+=1
    st['choice_days'].append(dict(day=obs['day'],quota=quota,wheat_price=wheat_price))
    st['buy']=max(0,quota-obs['private']['seeds'].get('CARROT',0))


def _pf_after(obs,action):
    st=_PF_STATE[obs['player']]
    if not (624<=obs['step']<672):return action
    import copy
    action=copy.deepcopy(action)
    if st['buy'] and len(action['market'])<10 and obs['farms'][obs['player']]['money']>20*st['buy']+1000:
        action['market'].append(['BUY_SEED','CARROT',st['buy']]);st['seed_requests']+=st['buy']
        st['buy']=0
    if not st['enabled']:return action
    seeds=obs['private']['seeds'].get('CARROT',0)
    positions=[obs['farms'][obs['player']]['farmer'],*obs['farms'][obs['player']]['hands']]
    commands=[action.get('farmer') or ['PASS'],*action.get('hands',[])]
    seeds=max(0,seeds-sum(c==['PLANT','CARROT'] for c in commands));claimed=set()
    for actor,command in enumerate(commands):
        if actor>=len(positions) or not seeds or not st['budget']:break
        x,y=positions[actor]
        if command==['PLANT','WHEAT'] and (x,y) not in claimed and obs['farms'][obs['player']]['tiles'][y][x] is None:
            commands[actor]=['PLANT','CARROT'];seeds-=1;st['budget']-=1;st['replacements']+=1
            st['pending'].append((x,y,obs['day']));claimed.add((x,y))
    action['farmer'],action['hands']=commands[0],commands[1:]
    return action
