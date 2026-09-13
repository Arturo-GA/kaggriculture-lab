"""Sell valuable cargo when a route crosses the shed, retaining future inputs."""
_F2_OLD_JOBS=_au_jobs


def _au_jobs(obs):
    jobs=_F2_OLD_JOBS(obs)
    for y,row in enumerate(obs['farms'][obs['player']]['tiles']):
        for x,t in enumerate(row):
            if not isinstance(t,dict) or t.get('crop') not in ('WHEAT','CARROT','MELON'):continue
            if t.get('yield_units',0)!=0 or t.get('watered_today'):continue
            crop=t['crop'];first,last,cap=_AU_CROPS[crop];age=obs['day']-t['planted_day']
            if max(first,(last+1)//2)<=age<=last:
                active=t.get('fertilized_until_day',-1)>=obs['day']
                jobs[x,y]=[([['WATER'],['HARVEST']],{crop:2 if active else 1})]
                if not active:jobs[x,y].append(([['FERTILIZE'],['WATER'],['HARVEST']],{crop:2,'FERTILIZER':-1}))
    return jobs


def _f2_walk(pos,target,cargo,prices):
    cursor=tuple(pos);commands=[];remaining=dict(cargo)
    for move in _au_walk(pos,target):
        if cursor in _AU_HOME:
            # PLACE transfers one selected product and keeps fertilizer for tasks
            # later in this trip. DROP would silently offload those inputs too.
            for item,q in sorted(remaining.items(),key=lambda kv:-prices[kv[0]]*kv[1]):
                if item!='FERTILIZER' and q*prices[item]>=_F2_THRESHOLD:
                    commands.append(['PLACE',item,q]);remaining[item]=0
        commands.append(move)
        x,y=cursor;op=move[0]
        cursor=(x+int(op=='EAST')-int(op=='WEST'),y+int(op=='SOUTH')-int(op=='NORTH'))
    return commands,remaining


def _au_route(pos,start,jobs,prices,power,bias,end=719,input_cap=100):
    left=dict(jobs);chosen=[];commands=[];value=0.;products={};cargo={};cursor=tuple(pos);inputs=0
    while left:
        best=None
        for target,variants in left.items():
            walk,delivered_cargo=_f2_walk(cursor,target,cargo,prices)
            home_distance=_au_dist(target,_au_home(target))
            for ops,goods in variants:
                need=int(goods.get('FERTILIZER',0)<0)
                if need and (tuple(pos) not in _AU_HOME or inputs+need>input_cap):continue
                setup=int(need>0 and inputs==0)
                duration=len(walk)+len(ops)+setup
                if start+len(commands)+duration+home_distance+1>end:continue
                gain=sum(prices[k]*v for k,v in goods.items())
                cost=max(.5,duration+bias*(home_distance-_au_dist(cursor,_au_home(cursor))))
                rank=(gain/(cost**power),gain,-duration,-target[1],-target[0])
                if best is None or rank>best[0]:best=(rank,target,ops,goods,gain,need,walk,delivered_cargo)
        if best is None:break
        _,target,ops,goods,gain,need,walk,cargo=best
        if need and inputs==0:commands.insert(0,['PICKUP','FERTILIZER',0])
        inputs+=need;commands+=walk+ops;cursor=target
        value+=gain;chosen.append(target);left.pop(target)
        for item,q in goods.items():
            products[item]=products.get(item,0)+q
            if q>0:cargo[item]=cargo.get(item,0)+q
    if chosen:commands+=_au_walk(cursor,_au_home(cursor))+[['DROP']]
    if inputs:commands[0][2]=inputs
    return dict(start=start,origin=list(pos),commands=commands,jobs=chosen,value=value,products=products,inputs=inputs)


_F2_OLD_ACTION=_au_action
def _au_action(obs,config,state):
    action=_F2_OLD_ACTION(obs,config,state)
    farm=obs['farms'][obs['player']];positions=[farm['farmer'],*farm['hands']]
    commands=[action['farmer'],*action['hands']]
    projected=dict(obs['private']['shed'])
    for i,(cmd,pos) in enumerate(zip(commands,positions)):
        if tuple(pos) not in _AU_HOME:continue
        inv=obs['private']['inventories'][i]
        if cmd[0]=='DROP':
            for item,q in inv.items():
                take=min(q,max(0,100-sum(projected.values())))
                projected[item]=projected.get(item,0)+take
        elif cmd[0]=='PLACE' and len(cmd)>2:
            item=cmd[1];take=min(cmd[2],inv.get(item,0),max(0,100-sum(projected.values())))
            projected[item]=projected.get(item,0)+take
        elif cmd[0]=='PICKUP':projected[cmd[1]]=max(0,projected.get(cmd[1],0)-cmd[2])
    reserve=sum(p['inputs'] for p in state['plans'] if p['inputs'] and obs['step']<p['start'])
    projected['FERTILIZER']=max(0,projected.get('FERTILIZER',0)-reserve)
    other=[o for o in action['market'] if o[0]!='SELL']
    sales=[['SELL',k,v] for k,v in projected.items() if v>0 and k in obs['market']['prices']]
    sales.sort(key=lambda o:(-_r37_quote_priority(obs,o,projected),-o[2]*obs['market']['prices'][o[1]]))
    action['market']=sales[:10-len(other)]+other
    state['early_deliveries']=state.get('early_deliveries',0)+sum(c[0]=='PLACE' for c in commands)
    return action


_F2_PARENT=agent
def agent(observation,configuration=None):
    action=_F2_PARENT(observation,configuration)
    state=_AU_STATE.get(observation['player'],{})
    agent.telemetry=dict(getattr(agent,'telemetry',{}),early_deliveries=state.get('early_deliveries',0))
    return action
agent.telemetry={}
agent=globals().pop('agent')
