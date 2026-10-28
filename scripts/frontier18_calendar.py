# Original finite crop calendar and observed-store demand forecast.
# Arturo-GA, Apache-2.0, 27 September 2026. No hidden observations or replay data.
_F18_REPORT=dict(f18_calendar_calls=0,f18_rotation_checks=0,f18_rotation_changed=0,
                 f18_rotation_on=0,f18_calendar_errors=0,f18_rotation_errors=0)


def _f18_shop_demand(obs,item,future_day):
    shops=obs['town']['unlocked_shops'];now=int(obs['step'])//24
    demand=1.0
    for shop in shops:
        products=_RACE_SHOPS.get(shop,())
        if item in products:demand+=12.0 if len(products)==1 else 6.0
    future=min(max(0,8-len(shops)),sum(d%3==0 for d in range(now+1,future_day+1)))
    expected=sum((12.0 if len(products)==1 else 6.0) for products in _RACE_SHOPS.values() if item in products)/8.
    return demand+future*expected


def _f18_finite_tomatoes(obs,upto,replant=True):
    now=int(obs['step'])//24;supply={}
    for row in obs['farms'][1-int(obs['player'])]['tiles']:
        for tile in row:
            if not isinstance(tile,dict) or tile.get('crop')!='TOMATO':continue
            planted=int(tile['planted_day'])
            # Conservatively allow two units per production and an immediate
            # replacement after the final production day, with a fresh age-8 wait.
            while planted+8<=upto:
                for d in range(planted+8,planted+12):
                    if now<d<=upto:supply[d]=supply.get(d,0.)+2.
                if not replant:break
                planted+=12
    return supply


_F18_CALENDAR_ORIGINAL=_cxtb_expected_revenue


def _cxtb_expected_revenue(obs):
    if not _F18_CALENDAR:return _F18_CALENDAR_ORIGINAL(obs)
    _F18_REPORT['f18_calendar_calls']+=1
    inventory=float(obs['market']['inventory']['TOMATO']);day=int(obs['step'])//24
    supply=_f18_finite_tomatoes(obs,max(_CXTB_HARVEST_DAYS));revenue=0.
    for d in range(day,max(_CXTB_HARVEST_DAYS)+1):
        inventory-=_f18_shop_demand(obs,'TOMATO',d)
        inventory+=supply.get(d,0.)
        if d in _CXTB_HARVEST_DAYS:
            for _ in range(_CXTB_OUR_UNITS):
                revenue+=_r37_market_price('TOMATO',int(round(inventory)))
                inventory+=1
    return revenue


def _f18_forward_quote(obs,item,days):
    now=int(obs['step'])//24;end=now+days;inventory=float(obs['market']['inventory'][item])
    inventory-=sum(_f18_shop_demand(obs,item,d) for d in range(now,end+1))
    # Visible crops only. This is a conservative supply scenario, not knowledge
    # of rival orders, inventories, future planting or future shop identities.
    for farm in obs['farms']:
        for row in farm['tiles']:
            for tile in row:
                if isinstance(tile,dict) and tile.get('crop')==item:
                    age=end-int(tile['planted_day'])
                    if age>=2:inventory+=max(int(tile.get('yield_units',0)),4 if item=='CARROT' else 6)
    # Account for a small batch of the contemplated additional production.
    inventory+=12 if item=='CARROT' else 16
    return _r37_market_price(item,int(round(inventory)))


_F18_CARROT_ORIGINAL=_v9_carrot


def _v9_carrot(obs,action,state):
    global V9_CARROT_RATIO,V9_CARROT_WHEAT_RESERVE
    if not _F18_ROTATION:return _F18_CARROT_ORIGINAL(obs,action,state)
    day=int(obs['step'])//24
    if not 10<=day<=23:return _F18_CARROT_ORIGINAL(obs,action,state)
    old_ratio=V9_CARROT_RATIO;old_reserve=V9_CARROT_WHEAT_RESERVE
    try:
        _F18_REPORT['f18_rotation_checks']+=1
        pc=_f18_forward_quote(obs,'CARROT',3);pw=_f18_forward_quote(obs,'WHEAT',4)
        # Keep the existing sowing/harvest-route repair and cash guards. Only
        # change the economic decision at a compatible wheat planting slot.
        gain=(3*pc-20)-(4*pw-10)
        choose=gain>=_F18_ROTATION_PREMIUM
        instant=obs['market']['prices']['CARROT']/max(1,obs['market']['prices']['WHEAT'])>=old_ratio
        if choose!=instant:_F18_REPORT['f18_rotation_changed']+=1
        if choose:_F18_REPORT['f18_rotation_on']+=1
        V9_CARROT_RATIO=0. if choose else 1e9
        farm=obs['farms'][int(obs['player'])]
        animals=sum(isinstance(t,dict) and bool(t.get('animal')) for row in farm['tiles'] for t in row)
        V9_CARROT_WHEAT_RESERVE=max(24,2*animals)
        return _F18_CARROT_ORIGINAL(obs,action,state)
    finally:
        V9_CARROT_RATIO=old_ratio;V9_CARROT_WHEAT_RESERVE=old_reserve


_F18_PARENT=agent
_F18_TELEMETRY={}


def agent(observation,configuration=None):
    if int(observation['step'])==0:
        for k in _F18_REPORT:_F18_REPORT[k]=0
    action=_F18_PARENT(observation,configuration)
    _F18_TELEMETRY.clear();_F18_TELEMETRY.update(getattr(_F18_PARENT,'telemetry',{}))
    _F18_TELEMETRY.update(_F18_REPORT)
    for prefix,report in [('tomato',_CXTB_REPORT),('crop',_V219_REPORT),('carrot',_V9_CARROT_REPORT)]:
        for k,v in report.items():
            if isinstance(v,(int,float)):_F18_TELEMETRY['f18_'+prefix+'_'+k]=v
    return action


agent.telemetry=_F18_TELEMETRY
agent=globals().pop('agent')
