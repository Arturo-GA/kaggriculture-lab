"""Original joint terminal harvest-routing and variable-workforce optimizer.

No opponent tapes, team IDs or world seeds. All plans are built from current
observable assets. Inherited production is used only before the handover.
"""
_AU_HOME=((4,4),(5,4),(4,5),(5,5))
_AU_PRODUCT={'GOOSE':'EGG','COW':'MILK','SHEEP':'WOOL'}
_AU_CROPS={'WHEAT':(2,4,6),'CARROT':(2,3,4),'TOMATO':(8,8,4),
           'STRAWBERRY':(10,10,4),'MELON':(10,12,6)}
_AU_STATE={}


def _au_dist(a,b):return abs(a[0]-b[0])+abs(a[1]-b[1])


def _au_home(pos):return min(_AU_HOME,key=lambda h:_au_dist(pos,h))


def _au_walk(pos,target):
    x,y=pos;tx,ty=target;commands=[]
    while x!=tx:
        commands.append(['EAST' if tx>x else 'WEST']);x+=1 if tx>x else -1
    while y!=ty:
        commands.append(['SOUTH' if ty>y else 'NORTH']);y+=1 if ty>y else -1
    return commands


def _au_fib(n):
    a,b=1,1
    for _ in range(n):a,b=b,a+b
    return a


def _au_jobs(obs):
    farm=obs['farms'][obs['player']];jobs={}
    for y,row in enumerate(farm['tiles']):
        for x,t in enumerate(row):
            if not isinstance(t,dict):continue
            variants=[];q=t.get('yield_units',0)
            animal=t.get('animal');crop=t.get('crop')
            if animal:
                item=_AU_PRODUCT[animal]
                if q>0:variants.append(( [['HARVEST']], {item:q}))
                if t.get('fertilizer_available'):
                    variants.append(([['COLLECT_FERTILIZER']],{'FERTILIZER':1}))
                    if q>0:variants.append(([['HARVEST'],['COLLECT_FERTILIZER']],{item:q,'FERTILIZER':1}))
            elif crop:
                first,last,cap=_AU_CROPS[crop];age=obs['day']-t['planted_day']
                if age>=first and q>0:
                    variants.append(([['HARVEST']],{crop:q}))
                    if crop in ('WHEAT','CARROT','MELON') and not t['watered_today'] and (last+1)//2<=age<=last:
                        extra=min(cap-q,2 if t.get('fertilized_until_day',-1)>=obs['day'] else 1)
                        if extra>0:variants.append(([['WATER'],['HARVEST']],{crop:q+extra}))
                        if t.get('fertilized_until_day',-1)<obs['day'] and q+1<cap:
                            variants.append(([['FERTILIZE'],['WATER'],['HARVEST']],
                                             {crop:min(cap,q+2),'FERTILIZER':-1}))
            if variants:jobs[(x,y)]=variants
    return jobs


def _au_prices(obs,risk):
    prices=dict(obs['market']['prices'])
    if not risk:return prices
    rival=obs['farms'][1-obs['player']]
    supply={item:0 for item in prices}
    for row in rival['tiles']:
        for tile in row:
            if not isinstance(tile,dict):continue
            item=tile.get('crop') or _AU_PRODUCT.get(tile.get('animal'))
            if item:supply[item]+=tile.get('yield_units',0)
            if tile.get('fertilizer_available'):supply['FERTILIZER']+=1
    # A conservative visible-stock scenario, not claimed to reveal private stock.
    for item in prices:
        inventory=obs['market']['inventory'][item]+int(risk*supply[item])
        prices[item]=min(prices[item],_r37_market_price(item,inventory))
    return prices


def _au_route(pos,start,jobs,prices,power,bias,end=719,input_cap=100):
    left=dict(jobs);chosen=[];commands=[];value=0.;products={};cursor=tuple(pos);inputs=0
    while left:
        best=None
        for target,variants in left.items():
            distance=_au_dist(cursor,target)
            home_distance=_au_dist(target,_au_home(target))
            for ops,goods in variants:
                need=int(goods.get('FERTILIZER',0)<0)
                if need and (tuple(pos) not in _AU_HOME or inputs+need>input_cap):continue
                setup=int(need>0 and inputs==0)
                duration=distance+len(ops)+setup
                if start+len(commands)+duration+home_distance+1>end:continue
                gain=sum(prices[k]*v for k,v in goods.items())
                # A terminal orienteering insertion score; power/bias are searched
                # jointly, and the entire resulting workforce is priced below.
                cost=max(.5,duration+bias*(home_distance-_au_dist(cursor,_au_home(cursor))))
                score=gain/(cost**power)
                rank=(score,gain,-duration,-target[1],-target[0])
                if best is None or rank>best[0]:best=(rank,target,ops,goods,gain,need)
        if best is None:break
        _,target,ops,goods,gain,need=best
        if need and inputs==0:commands.insert(0,['PICKUP','FERTILIZER',0])
        inputs+=need
        commands+=_au_walk(cursor,target)+ops;cursor=target
        value+=gain;chosen.append(target);left.pop(target)
        for item,q in goods.items():products[item]=products.get(item,0)+q
    if chosen:
        commands+=_au_walk(cursor,_au_home(cursor))+[['DROP']]
    if inputs:commands[0][2]=inputs
    return dict(start=start,origin=list(pos),commands=commands,jobs=chosen,value=value,products=products,inputs=inputs)


def _au_spawn(plans,step):
    occupancy={h:0 for h in _AU_HOME}
    for plan in plans:
        x,y=plan['origin']
        for cmd in plan['commands'][:max(0,step-plan['start']+1)]:
            op=cmd[0]
            x+=int(op=='EAST')-int(op=='WEST');y+=int(op=='SOUTH')-int(op=='NORTH')
        if (x,y) in occupancy:occupancy[x,y]+=1
    return min(_AU_HOME,key=lambda h:occupancy[h])


def _au_construct(obs,prices,power,bias,reserve):
    farm=obs['farms'][obs['player']];jobs=_au_jobs(obs);plans=[]
    original_positions=[farm['farmer'],*farm['hands']]
    score=0.;spent=0.;hire_steps=[]
    for actor in range(1+len(farm['hands'])+19):
        existing=actor<len(original_positions)
        if existing:
            start=obs['step'];pos=original_positions[actor];cost=0
        else:
            hire_index=actor-len(original_positions)
            hire_step=obs['step']+hire_index//7
            start=hire_step+1;pos=_au_spawn(plans,hire_step)
            cost=_au_fib(farm['hires_today']+hire_index)
        if start>=717:break
        cap=obs['private']['shed'].get('FERTILIZER',0) if existing else 100
        plan=_au_route(pos,start,jobs,prices,power,bias,input_cap=cap)
        if not existing and (plan['value']<=cost*reserve or spent+cost>farm['money']*.15):break
        plans.append(plan);score+=plan['value']-cost;spent+=cost
        for job in plan['jobs']:jobs.pop(job)
        if not existing:hire_steps.append(hire_step)
    return dict(plans=plans,hire_steps=hire_steps,predicted_net=score,hire_cost=spent,
                unassigned=len(jobs),power=power,bias=bias)


def _au_plan(obs,config):
    prices=_au_prices(obs,_AU_RISK)
    candidates=[_au_construct(obs,prices,power,bias,_AU_RESERVE)
                for power in (.6,.85,1.1,1.4) for bias in (0.,.6)]
    best=max(candidates,key=lambda p:p['predicted_net'])
    best.update(step=obs['step'],last_step=obs['step']-1,errors=0,turns=0,
                planned_workers=len(best['plans'])-1,harvest_requests=0,water_requests=0,
                fertilizer_requests=0,hire_requests=0,late_returns=0,
                input_purchase=max(0,sum(p['inputs'] for p in best['plans'])-obs['private']['shed'].get('FERTILIZER',0)),
                input_applications=0)
    return best


def _au_action(obs,config,state):
    step=obs['step'];farm=obs['farms'][obs['player']]
    positions=[farm['farmer'],*farm['hands']];inventories=obs['private']['inventories']
    commands=[];projected=dict(obs['private']['shed'])
    for actor,pos in enumerate(positions):
        plan=state['plans'][actor] if actor<len(state['plans']) else None
        index=step-plan['start'] if plan else -1
        cmd=plan['commands'][index] if plan and 0<=index<len(plan['commands']) else ['PASS']
        inv=inventories[actor] if actor<len(inventories) else {}
        # Deadline repair uses observed position and cargo, never a future trace.
        distance=_au_dist(pos,_au_home(pos))
        if inv and step+distance+1>=719:
            cmd=_au_walk(pos,_au_home(pos))[0] if distance else ['DROP']
            state['late_returns']+=1
        if cmd[0]=='DROP' and tuple(pos) in _AU_HOME:
            room=max(0,100-sum(projected.values()))
            for item,q in inv.items():
                take=min(q,room);projected[item]=projected.get(item,0)+take;room-=take
        if cmd[0]=='PICKUP' and tuple(pos) in _AU_HOME:
            projected[cmd[1]]=max(0,projected.get(cmd[1],0)-cmd[2])
        commands.append(cmd)
        state['harvest_requests']+=cmd[0]=='HARVEST'
        state['water_requests']+=cmd[0]=='WATER'
        state['fertilizer_requests']+=cmd[0]=='COLLECT_FERTILIZER'
        state['input_applications']+=cmd[0]=='FERTILIZE'
    hires=state['hire_steps'].count(step)
    orders=[['HIRE'] for _ in range(hires)]
    if step==state['step'] and state['input_purchase']:
        orders.append(['BUY_PRODUCT','FERTILIZER',state['input_purchase']])
    reserve=sum(p['inputs'] for p in state['plans'] if p['inputs'] and step<p['start'])
    projected['FERTILIZER']=max(0,projected.get('FERTILIZER',0)-reserve)
    sales=[['SELL',item,q] for item,q in projected.items() if q>0 and item in obs['market']['prices']]
    sales.sort(key=lambda o:(-_r37_quote_priority(obs,o,projected),
                             -o[2]*obs['market']['prices'][o[1]]))
    # Market slots resolve across both players in order. Hire completion still
    # occurs this turn when sales precede it, but exposed inventory sells sooner.
    orders=sales[:max(0,10-len(orders))]+orders
    state['hire_requests']+=hires;state['turns']+=1;state['last_step']=step
    return dict(farmer=commands[0],hands=commands[1:],market=orders)


def _auction_controller(obs,config):
    seat=int(obs['player']);step=int(obs['step'])
    if step<_AU_START:return None
    if any((config or {}).get(k,v)!=v for k,v in [('boardSize',10),('episodeSteps',720),
            ('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):return None
    state=_AU_STATE.get(seat)
    if state is None or step<=state['last_step']:
        state=_AU_STATE[seat]=_au_plan(obs,config)
    return _au_action(obs,config,state)
