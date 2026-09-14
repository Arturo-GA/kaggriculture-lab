# Apache-2.0: funding/seed guards adapted from Ahmed Berat Ozer V41.
# Opening lineage: Rayk Kretzschmar; integration/capacity solver: Arturo-GA.
def _r97_budget(obs,orders):
    farm=obs['farms'][obs['player']];cost=0;hires=int(farm['hires_today'])
    # At most ten 100-unit purchases per opponent turn. The additional 1000
    # own units give an intentionally conservative upper bound on buy quotes.
    prices={p:_r37_market_price(p,obs['market']['inventory'][p]-2000) for p in ('WHEAT','FERTILIZER')}
    for order in orders:
        if not order:continue
        op=order[0]
        if op=='HIRE':cost+=_v219_fib(hires);hires+=1
        elif op=='BUY_LAND':cost+=4000
        elif len(order)>2:
            item=order[1];q=max(0,int(order[2]))
            if op=='BUY_PRODUCT':cost+=q*prices[item]
            elif op=='BUY_ANIMAL':cost+=q*{'GOOSE':300,'COW':400,'SHEEP':500}[item]
            elif op=='BUY_SEED':cost+=q*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[item]
    return cost<=farm['money']

def _r124_labor_reserve(native):
    n=sum(bool(o) and o[0]=='HIRE' for o in native[24].get('market',[]))
    return sum(_v219_fib(i) for i in range(n)),n

def _r124_seed_budget(obs,action,reserve):
    if not any(o and o[0]=='BUY_SEED' for o in action.get('market',[])):return action
    player=int(obs['player']);budget=dict(obs,farms=[dict(f) for f in obs['farms']]);budget['farms'][player]['money']-=reserve
    if _r97_budget(budget,action.get('market',[])):return action
    result=copy.deepcopy(action)
    for i in range(len(result['market'])-1,-1,-1):
        order=result['market'][i]
        if len(order)<3 or order[0]!='BUY_SEED':continue
        before=max(0,int(order[2]));order[2]=before
        while order[2]>0 and not _r97_budget(budget,result['market']):order[2]-=1
        n=before-order[2]
        if n:
            _R124_REPORT['opening_seed_budget_units']+=n
            _R124_REPORT['opening_seed_budget_cost']+=n*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[order[1]]
        if _r97_budget(budget,result['market']):break
    return result

def _r124_atomic(obs,action,state):
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    if not demand:return action
    available=obs['private']['seeds'];blocked={p for p,n in demand.items() if n>available.get(p,0)}
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    changed=False;kept=[]
    for actor,c in enumerate(commands):
        if len(c)>1 and c[0]=='PLANT':
            pos=None if actor>=len(private['inventories']) else farm['farmer'] if actor==0 else farm['hands'][actor-1]
            valid=pos is not None and farm['tiles'][pos[1]][pos[0]] is None and private['seeds'].get(c[1],0)>0
            if not valid:
                commands[actor]=['PASS'];changed=True;_R124_REPORT['opening_atomic_dropped']+=1
            elif c[1] in blocked:
                kept.append(dict(xy=list(pos),crop=c[1],birth=int(obs["step"])//24));_R124_REPORT['opening_atomic_rescued_requests']+=1
        if actor<len(private['inventories']):_PLANNER_NS['_apply_unit_action'](farm,private,actor,commands[actor],10,int(obs["step"])//24,24,100)
    if kept:state['pending_plants']=kept
    if changed:
        action=dict(action,farmer=commands[0],hands=commands[1:])
    return action
