# ==== Frontier5 demand-aware livestock: geese instead of glut-bound cows and sheep (Arturo-GA, Apache-2.0) ====
# Measured on 56 live replays (September 16-17, 2026): without a yarn store wool sells at $1 from day 20 and even with
# three milk shops milk falls to ~$50 by day 20 in mirror games, while eggs hold $50-59 in every world (log glut curve,
# bakery/brunch demand).  When the route is chosen (step 144) and the two known shops contain no yarn store and at most
# one milk shop, every animal the tape buys from then on (day 6-7 cows, day 8-11 sheep) becomes a goose: the purchase
# order, the structure build, the pickup and the placement are rewritten transactionally; the tape's feed, care and
# harvest commands are species-agnostic.  Extra eggs are sold through an egg credit on the tape's own EGG sales.
# Pattern after lynnsakurai's Farming Score V5 egg substitution and prvsiyan's cattle controller (both Apache-2.0).
_GZ_PARENT=agent
_GZ_ENABLED=True
_GZ_DECIDE_STEP=144
_GZ_TO_STEP=696
_GZ_MILK_SHOPS=('PIZZA_SHOP','ICE_CREAM_SHOP','SMOOTHIE_SHOP')
_GZ_MAX_MILK_KNOWN=1
_GZ_MAX_YARN_KNOWN=0
_GZ_SPECIES=('COW','SHEEP')
_GZ_STATE={}
_GZ_REPORT=dict(gz_active=0,gz_buy_requests=0,gz_buy_confirmed=0,gz_buy_shortfalls=0,gz_coops=0,gz_pickups=0,
                gz_placements=0,gz_blocked_pastures=0,gz_egg_credit=0,gz_egg_sold=0,gz_errors=0)


def _gz_new_state():
    return {'step':-1,'decided':False,'active':False,'pending':None,'quota':0,'placed':0,'egg_credit':0,'sites':{},
            'last_harvest':{}}


def _gz_decide(obs,state):
    shops=list(obs['town'].get('unlocked_shops') or [])
    yarn=sum(s=='YARN_STORE' for s in shops);milk=sum(s in _GZ_MILK_SHOPS for s in shops)
    state['active']=bool(_GZ_ENABLED and yarn<=_GZ_MAX_YARN_KNOWN and milk<=_GZ_MAX_MILK_KNOWN)
    state['decided']=True
    _GZ_REPORT['gz_active']=int(state['active'])


def _gz_apply(obs,action,state):
    step=int(obs['step']);player=int(obs['player'])
    farm=obs['farms'][player];private=obs['private'];shed=private['shed'];inventories=private['inventories']
    positions=[farm['farmer'],*farm['hands']]
    pending=state['pending']
    if pending is not None:
        if step==pending['step']:
            gained=max(0,int(shed.get('GOOSE',0))-pending['before'])
            confirmed=min(pending['quantity'],gained)
            state['quota']+=confirmed
            _GZ_REPORT['gz_buy_confirmed']+=confirmed;_GZ_REPORT['gz_buy_shortfalls']+=pending['quantity']-confirmed
        state['pending']=None
    result=copy.deepcopy(action)
    market=[list(o) for o in (result.get('market') or []) if o]
    requested=0
    for o in market:
        if len(o)>=3 and o[0]=='BUY_ANIMAL' and o[1] in _GZ_SPECIES:
            try:n=max(0,int(o[2]))
            except Exception:n=0
            if n:
                o[1]='GOOSE';requested+=n
    if requested:
        state['pending']={'step':step+1,'before':int(shed.get('GOOSE',0)),'quantity':requested}
        _GZ_REPORT['gz_buy_requests']+=requested
    commands=[list(result.get('farmer') or ['PASS']),*[list(c) for c in (result.get('hands') or [])]]
    depot=int(shed.get('GOOSE',0))
    for actor,cmd in enumerate(commands[:len(positions)]):
        if not cmd:continue
        inventory=inventories[actor] if actor<len(inventories) else {}
        x,y=positions[actor];tile=farm['tiles'][y][x]
        if cmd[0]=='BUILD_PASTURE' and tile is None:
            commands[actor]=['BUILD_COOP'];_GZ_REPORT['gz_coops']+=1
        elif cmd[0]=='PICKUP' and len(cmd)>1 and cmd[1] in _GZ_SPECIES:
            try:n=max(0,int(cmd[2]) if len(cmd)>2 else 1)
            except Exception:n=1
            if depot>0 and int(shed.get(cmd[1],0))<n:
                take=min(n,depot);depot-=take
                commands[actor]=['PICKUP','GOOSE',take];_GZ_REPORT['gz_pickups']+=take
        elif cmd[0]=='PLACE' and len(cmd)>1 and cmd[1] in _GZ_SPECIES and int(inventory.get('GOOSE',0))>0:
            if isinstance(tile,dict) and tile.get('kind')=='COOP' and tile.get('animal') is None:
                commands[actor]=['PLACE','GOOSE'];state['placed']+=1;state['sites'][(x,y)]=step//24
                _GZ_REPORT['gz_placements']+=1
            elif isinstance(tile,dict) and tile.get('kind')=='PASTURE' and tile.get('animal') is None:
                _GZ_REPORT['gz_blocked_pastures']+=1
        elif cmd[0]=='HARVEST' and (x,y) in state['sites'] and isinstance(tile,dict) and tile.get('animal')=='GOOSE':
            units=max(0,int(tile.get('yield_units',0)))
            if units and state['last_harvest'].get((x,y))!=step:
                state['egg_credit']+=units;state['last_harvest'][(x,y)]=step;_GZ_REPORT['gz_egg_credit']+=units
    result['farmer'],result['hands']=commands[0],commands[1:]
    if state['egg_credit']>0 and int(obs['market']['prices'].get('EGG',0))>1:
        stock=int(shed.get('EGG',0))
        planned=sum(max(0,int(o[2])) for o in market if len(o)>=3 and o[0]=='SELL' and o[1]=='EGG')
        extra=min(state['egg_credit'],max(0,stock-planned))
        if extra>0:
            hit=next((o for o in market if len(o)>=3 and o[0]=='SELL' and o[1]=='EGG'),None)
            if hit is not None:
                hit[2]=int(hit[2])+extra;state['egg_credit']-=extra;_GZ_REPORT['gz_egg_sold']+=extra
            elif len(market)<10 and step%24 in (0,1,12,13):
                market.append(['SELL','EGG',extra]);state['egg_credit']-=extra;_GZ_REPORT['gz_egg_sold']+=extra
    result['market']=market
    return result


def agent(observation,configuration=None):
    action=_GZ_PARENT(observation,configuration)
    try:
        step=int(observation['step']);player=int(observation['player'])
        state=_GZ_STATE.get(player)
        if state is None or step<=state['step']:
            state=_GZ_STATE[player]=_gz_new_state()
            if step==0:_GZ_REPORT.update(gz_active=0,gz_buy_requests=0,gz_buy_confirmed=0,gz_buy_shortfalls=0,gz_coops=0,gz_pickups=0,gz_placements=0,gz_blocked_pastures=0,gz_egg_credit=0,gz_egg_sold=0,gz_errors=0)
        state['step']=step
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('episodeSteps',720),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('startingMoney',3000)])
        if standard and step>=_GZ_DECIDE_STEP and not state['decided']:_gz_decide(observation,state)
        if standard and state['active'] and _GZ_DECIDE_STEP<=step<_GZ_TO_STEP:
            action=_gz_apply(observation,action,state)
    except Exception:
        _GZ_REPORT['gz_errors']+=1
    _GZ_TELEMETRY.clear();_GZ_TELEMETRY.update(getattr(_GZ_PARENT,'telemetry',{}));_GZ_TELEMETRY.update(_GZ_REPORT)
    return action
_GZ_TELEMETRY={}
agent.telemetry=_GZ_TELEMETRY
agent=globals().pop('agent')
