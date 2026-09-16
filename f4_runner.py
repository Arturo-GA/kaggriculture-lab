# ==== Frontier4 harvest runners: hired hands deliver race-sensitive products before the tape's dawn sale ====
# Arturo-GA / Kaggriculture Lab, Apache-2.0. Uses only own public/private state and the own route tape;
# no rival private data. Runners harvest tiles the tape would reach later and deposit+sell by fixed deadlines.
_HR_PARENT=agent
_HR_START_DAY=10
_HR_END_STEP=696
_HR_MAX=2
_HR_TWO_VALUE=6000
_HR_ONE_VALUE=2000
_HR_COST_SHARE=0.2
_HR_CASH_BUFFER=300
_HR_DEADLINES=(9,16,22)
_HR_BIG_CARGO=1500
_HR_RACE={'STRAWBERRY':('STRAWBERRY',40),'MELON':('MELON',100),'SHEEP':('WOOL',40),'TOMATO':('TOMATO',30),'COW':('MILK',0)}
_HR_MILK_MAX_PRICE=170
_HR_STATE={}
_HR_REPORT=dict(hr_days=0,hr_hires=0,hr_hire_cost=0,hr_harvest_cmds=0,hr_placed_units=0,hr_sale_orders=0,hr_released=0,hr_errors=0)


def _hr_fib(n):
    a,b=1,1
    for _ in range(n):a,b=b,a+b
    return a


def _hr_tile(tile,prices,day):
    """(value, product) of a race-sensitive harvestable tile; melons only at full yield."""
    if not isinstance(tile,dict):return 0,None
    key=tile.get('crop') or tile.get('animal')
    spec=_HR_RACE.get(key)
    if spec is None:return 0,None
    item,floor=spec
    units=int(tile.get('yield_units',0))
    if units<=0:return 0,None
    if key=='MELON' and units<6 and day-int(tile.get('planted_day',day))<10:return 0,None
    price=int(prices.get(item,0))
    if price<floor:return 0,None
    if item=='MILK' and price>_HR_MILK_MAX_PRICE:return 0,None
    return units*price,item


def _hr_tape_day(player,day):
    try:
        native=_IMPL.chassis.players[player];tape=_IMPL.chassis.routes[native['route']]
    except Exception:
        return None
    out=[]
    for s in range(day*24,day*24+24):
        t=tape[s] if s<len(tape) and isinstance(tape[s],dict) else {}
        out.append(t)
    return out


def _hr_tape_harvest_hours(obs,planned,hour):
    """Hour at which the tape will HARVEST each tile later today, simulated from current unit positions."""
    farm=obs['farms'][obs['player']];positions=[list(farm['farmer'])]+[list(p) for p in farm['hands']]
    schedule={}
    for h in range(hour,24):
        t=planned[h];units=[t.get('farmer') or ['PASS']]+list(t.get('hands') or [])
        for i,pos in enumerate(positions):
            c=units[i] if i<len(units) else ['PASS']
            op=c[0] if c else 'PASS'
            if op in ('NORTH','SOUTH','EAST','WEST'):
                dx,dy={'NORTH':(0,-1),'SOUTH':(0,1),'EAST':(1,0),'WEST':(-1,0)}[op]
                nx,ny=pos[0]+dx,pos[1]+dy
                if 0<=nx<10 and 0<=ny<10:pos[0],pos[1]=nx,ny
            elif op=='HARVEST':
                key=(pos[0],pos[1])
                if key not in schedule:schedule[key]=h
    return schedule


def _hr_hire(obs,action,state):
    step=int(obs['step']);day=step//24;hour=step%24;player=int(obs['player'])
    if state.get('hire_day')==day or hour>2:return action
    farm=obs['farms'][player];prices=obs['market']['prices']
    market=list(action.get('market',[]))
    if len(market)>=10:return action
    parent_hires=sum(1 for o in market if o and o[0]=='HIRE')
    planned=_hr_tape_day(player,day)
    if planned is None:return action
    if any(o and o[0]=='HIRE' for a in planned[hour+1:] for o in a.get('market',[])):return action
    value=sum(_hr_tile(t,prices,day)[0] for row in farm['tiles'] for t in row)
    want=2 if value>=_HR_TWO_VALUE else 1 if value>=_HR_ONE_VALUE else 0
    want=min(want,_HR_MAX)
    if not want:return action
    base=int(farm['hires_today'])+parent_hires
    spend=sum(int(o[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}.get(o[1],0) for o in market if o and o[0]=='BUY_SEED')
    spend+=sum(int(o[2])*{'SHEEP':500,'COW':400,'GOOSE':300}.get(o[1],0) for o in market if o and o[0]=='BUY_ANIMAL')
    spend+=sum(int(o[2])*(int(prices.get(o[1],0))+10) for o in market if o and o[0]=='BUY_PRODUCT')
    spend+=sum(_hr_fib(int(farm['hires_today'])+i) for i in range(parent_hires))
    spend+=4000*sum(1 for o in market if o and o[0]=='BUY_LAND')
    k=0
    for cand in range(want,0,-1):
        cost=sum(_hr_fib(base+i) for i in range(cand))
        if cost<=_HR_COST_SHARE*value and farm['money']>=spend+cost+_HR_CASH_BUFFER and len(market)+cand<=10:
            k=cand;break
    if not k:return action
    state['hire_day']=day;state['pending']=dict(base=len(farm['hands'])+parent_hires,k=k,step=step)
    state['runners']=[]
    result=copy.deepcopy(action);result['market']=market+[['HIRE'] for _ in range(k)]
    _HR_REPORT['hr_hires']+=k;_HR_REPORT['hr_hire_cost']+=sum(_hr_fib(base+i) for i in range(k));_HR_REPORT['hr_days']+=1
    return result


def _hr_worker(obs,actor,claimed,occupied,schedule):
    farm=obs['farms'][obs['player']];private=obs['private'];prices=obs['market']['prices']
    step=int(obs['step']);hour=step%24;day=step//24
    pos=tuple(farm['hands'][actor-1]);inv=private['inventories'][actor]
    home=_v219_home(pos);dist=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    cargo=sum(int(prices.get(k,0))*v for k,v in inv.items() if v>0)
    deadline=next((d for d in _HR_DEADLINES if d>hour),23)
    best=None
    for y,row in enumerate(farm['tiles']):
        for x,t in enumerate(row):
            if (x,y) in claimed or (x,y) in occupied:continue
            v,item=_hr_tile(t,prices,day)
            if v<=0:continue
            d=abs(pos[0]-x)+abs(pos[1]-y);arrive=hour+d
            if schedule.get((x,y),99)<=arrive:continue
            hx=4 if x<5 else 5;hy=4 if y<5 else 5;h=abs(x-hx)+abs(y-hy)
            if arrive+1+h+1>deadline and (arrive+1+h+1>22 or inv):continue
            score=v/(d+1.0)
            if best is None or score>best[0]:best=(score,(x,y),v)
    deliver=bool(inv) and (best is None or cargo>=_HR_BIG_CARGO or hour+dist+1>=deadline)
    if deliver:
        move=_v219_walk(pos,home)
        if move:return move,None
        item=max(inv,key=lambda k:int(prices.get(k,0))*inv[k])
        return ['PLACE',item,int(inv[item])],item
    if best is None:return ['PASS'],None
    claimed.add(best[1])
    move=_v219_walk(pos,best[1])
    if move:return move,None
    _HR_REPORT['hr_harvest_cmds']+=1
    return ['HARVEST'],None


def _race_positions_equal(farms,player):
    """Runners extend our hand list; compare the rival's hands with our tape prefix."""
    own,rival=farms[player],farms[1-player]
    n=len(rival['hands'])
    return n>0 and len(own['hands'])>=n and own['hands'][:n]==rival['hands'] and own['farmer']==rival['farmer']


def agent(observation,configuration=None):
    action=_HR_PARENT(observation,configuration)
    try:
        step=int(observation['step']);player=int(observation['player']);day=step//24;hour=step%24
        state=_HR_STATE.get(player)
        if state is None or step<=state['step']:
            state=_HR_STATE[player]={'step':-1,'runners':[],'pending':None,'pending_sales':{}}
            if step==0:_HR_REPORT.update(hr_days=0,hr_hires=0,hr_hire_cost=0,hr_harvest_cmds=0,hr_placed_units=0,hr_sale_orders=0,hr_released=0,hr_errors=0)
        state['step']=step
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('episodeSteps',720),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1),('startingMoney',3000)])
        if not standard or day<_HR_START_DAY or step>=_HR_END_STEP:return action
        farm=observation['farms'][player];private=observation['private']
        if hour==0:state['runners']=[];state['pending']=None;state['pending_sales']={}
        pending=state.get('pending')
        if pending and step==pending['step']+1:
            got=len(farm['hands'])-pending['base']
            state['runners']=[pending['base']+1+i for i in range(min(got,pending['k']))]
            state['pending']=None
        if not state['runners']:
            return _hr_hire(observation,action,state)
        if any(o and o[0]=='HIRE' for o in action.get('market',[])):
            state['runners']=[];_HR_REPORT['hr_released']+=1;return action
        planned=_hr_tape_day(player,day)
        schedule=_hr_tape_harvest_hours(observation,planned,hour) if planned else {}
        result=copy.deepcopy(action)
        commands=[result.get('farmer') or ['PASS']]+list(result.get('hands') or [])
        commands+=[['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
        occupied={tuple(p) for i,p in enumerate([farm['farmer'],*farm['hands']]) if i not in state['runners']}
        claimed=set();placed={}
        for actor in state['runners']:
            if actor>=len(private['inventories']) or actor-1>=len(farm['hands']):continue
            command,item=_hr_worker(observation,actor,claimed,occupied,schedule)
            commands[actor]=command
            if item:placed[item]=placed.get(item,0)+int(command[2])
        result['farmer'],result['hands']=commands[0],commands[1:]
        if placed:
            room=max(0,100-sum(private['shed'].values()))
            _HR_REPORT['hr_placed_units']+=min(room,sum(placed.values()))
            for item,q in placed.items():state['pending_sales'][item]=state['pending_sales'].get(item,0)+q
        if state['pending_sales']:
            prices=observation['market']['prices']
            market=[list(o) for o in result.get('market',[]) if o]
            front=[]
            for item in sorted(list(state['pending_sales']),key=lambda k:-int(prices.get(k,0))*state['pending_sales'][k]):
                stock=int(private['shed'].get(item,0))+placed.get(item,0)
                if stock<=0:state['pending_sales'].pop(item,None);continue
                idx=next((i for i,o in enumerate(market) if o[0]=='SELL' and len(o)>2 and o[1]==item),None)
                if idx is not None:
                    o=market.pop(idx);o[2]=max(int(o[2]),stock);front.append(o)
                elif len(market)+len(front)<10:
                    front.append(['SELL',item,stock])
                else:
                    sells=[i for i,o in enumerate(market) if o[0]=='SELL']
                    if not sells:continue
                    market.pop(sells[-1]);front.append(['SELL',item,stock])
                state['pending_sales'].pop(item,None);_HR_REPORT['hr_sale_orders']+=1
            result['market']=front+market
        action=result
    except Exception:
        _HR_REPORT['hr_errors']+=1
    agent.telemetry=dict(getattr(_HR_PARENT,'telemetry',{}),**_HR_REPORT)
    return action
agent.telemetry={}
agent=globals().pop('agent')
