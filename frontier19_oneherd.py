# F19 follow-up: at most ONE single-unit sheep purchase changes species.
# Feasibility precedes selection; a rejected coop plan does not hide a valid cow route.
# Original Arturo-GA, Apache-2.0. Buy-time diversification with a verified
# same-day construction/carrier plan; no new workers or speculative orders.
_F19_HERD_PARENT=agent
_F19_HERD_STATE={}
_F19_HERD_REPORT=dict(f19_herd_checks=0,f19_herd_selected=0,f19_herd_units=0,
 f19_herd_rewrites=0,f19_herd_sold=0,f19_herd_no_plan=0,f19_herd_already_rewritten=0,f19_herd_errors=0,f19_herd_plan_mismatch=0)

def _f19_herd_plan(obs,action,source,target,quantity):
    step=int(obs['step']);seat=int(obs['player']);farm=obs['farms'][seat]
    positions=[list(farm['farmer'])]+[list(p) for p in farm['hands']]
    builds=[];pickups=[];places=[];plan={}
    for t in range(step,(step//24+1)*24):
        a=action if t==step else _cs_tape(seat,t)
        cmds=[a.get('farmer') or ['PASS']]+list(a.get('hands') or [])
        for i,pos in enumerate(positions):
            c=cmds[i] if i<len(cmds) else ['PASS'];xy=tuple(pos)
            if c[0] in _CS_MOVES:
                dx,dy=_CS_MOVES[c[0]];positions[i]=[max(0,min(9,pos[0]+dx)),max(0,min(9,pos[1]+dy))]
            elif c==['BUILD_PASTURE']:builds.append((t,i,xy))
            elif len(c)>1 and c[:2]==['PICKUP',source]:pickups.append((t,i,int(c[2]) if len(c)>2 else 1,xy))
            elif len(c)>1 and c[:2]==['PLACE',source]:places.append((t,i,xy))
        for _ in range(sum(o==['HIRE'] for o in a.get('market',[]))):positions.append(_cs_spawn(positions,10))
    chosen=[];seen=set()
    for t,i,xy in places:
        if xy not in seen:chosen.append((t,i,xy));seen.add(xy)
        if len(chosen)==quantity:break
    if len(chosen)!=quantity:return None
    carriers={}
    for t,i,xy in chosen:
        # Goose requires a COOP, so changing a previously built pasture is not
        # allowed. Require a future construction step already on this route.
        tile=farm['tiles'][xy[1]][xy[0]]
        if target=='GOOSE':
            quadrant=('N' if xy[1]<5 else 'S')+('W' if xy[0]<5 else 'E')
            next_land=next((q for q in ('NE','SW','SE') if q not in farm['unlocked_quadrants']),None)
            unlocked_now=tile=='LOCKED' and quadrant==next_land and any(o==['BUY_LAND'] for o in action.get('market',[]))
            if tile is not None and not unlocked_now:return None
            b=[(tb,ib,pb) for tb,ib,pb in builds if pb==xy and tb<t]
            if not b:return None
            tb,ib,pb=b[-1];plan[(tb,ib)]=(pb,('BUILD_PASTURE',),('BUILD_COOP',))
        ps=[p for p in pickups if p[1]==i and p[0]<t]
        if not ps:return None
        pickup=ps[-1];carriers[pickup]=carriers.get(pickup,0)+1
        plan[(t,i)]=(xy,('PLACE',source),('PLACE',target))
    for (t,i,q,xy),count in carriers.items():
        if q!=count:return None
        plan[(t,i)]=(xy,('PICKUP',source),('PICKUP',target,q))
    return plan

def _f19_herd(obs,action):
    step=int(obs['step']);day=step//24;seat=int(obs['player'])
    if step==0:_F19_HERD_STATE.clear()
    state=_F19_HERD_STATE.setdefault(seat,dict(plan={},changed=False))
    farm=obs['farms'][seat];private=obs['private']
    market=[list(o) for o in action.get('market',[])];result=action
    if 6<=day<=11 and not state['plan'] and not state['changed']:
        buys=[o for o in market if len(o)>=3 and o[0]=='BUY_ANIMAL' and o[1]=='SHEEP' and int(o[2])==1]
        for order in buys:
            source=order[1];q=int(order[2])
            if private['shed'].get(source,0) or any(b.get(source,0) for b in private['inventories']):continue
            # Protect existing animal transport; all replacements are cheaper.
            _F19_HERD_REPORT['f19_herd_checks']+=1
            options=('GOOSE',) if source=='COW' else ('GOOSE','COW')
            values={opt:_hd2_ev(opt,q,obs,{})[0] for opt in (source,)+options}
            plan=None
            for target in sorted(options,key=lambda p:-values[p]):
                if values[target]<max(values[source]+_F19_HERD_GAIN,values[source]*_F19_HERD_RATIO):continue
                plan=_f19_herd_plan(obs,action,source,target,q)
                if plan is not None:break
            if plan is None:_F19_HERD_REPORT['f19_herd_no_plan']+=1;continue
            state['plan']=plan;state['changed']=True;order[1]=target
            _F19_HERD_REPORT['f19_herd_selected']+=1;_F19_HERD_REPORT['f19_herd_units']+=q
            break
    commands=[list(action.get('farmer') or ['PASS'])]+[list(c) for c in action.get('hands',[])]
    positions=[farm['farmer']]+list(farm['hands'])
    for (t,i),(xy,old,new) in list(state['plan'].items()):
        if t!=step:continue
        del state['plan'][(t,i)]
        if i<len(positions) and i<len(commands) and tuple(positions[i])==xy and tuple(commands[i][:len(old)])==old:
            commands[i]=list(new);_F19_HERD_REPORT['f19_herd_rewrites']+=1
        elif i<len(positions) and i<len(commands) and tuple(positions[i])==xy and tuple(commands[i])==new:
            _F19_HERD_REPORT['f19_herd_already_rewritten']+=1
        else:_F19_HERD_REPORT['f19_herd_plan_mismatch']+=1
    if state['changed']:
        # Sell visible extra animal products after physical delivery. This also
        # accounts for reduced sheep output without fabricating sale credits.
        probe=dict(action,farmer=commands[0],hands=commands[1:],market=[])
        stock=projected_shed(probe,FarmView(obs))
        for item in ('EGG','MILK','WOOL'):
            held=max(0,int(stock.get(item,0)))
            planned=sum(int(o[2]) for o in market if len(o)>=3 and o[:2]==['SELL',item])
            if held>planned and (step%24 in (19,21,22) or step>=696) and len(market)<10:
                market.append(['SELL',item,held-planned]);_F19_HERD_REPORT['f19_herd_sold']+=held-planned
    return dict(action,market=market,farmer=commands[0],hands=commands[1:])

_F19_HERD_TELEMETRY={}
def agent(observation,configuration=None):
    if int(observation['step'])==0:
        for k in _F19_HERD_REPORT:_F19_HERD_REPORT[k]=0
    action=_F19_HERD_PARENT(observation,configuration)
    try:action=_f19_herd(observation,action)
    except Exception:_F19_HERD_REPORT['f19_herd_errors']+=1
    _F19_HERD_TELEMETRY.clear();_F19_HERD_TELEMETRY.update(getattr(_F19_HERD_PARENT,'telemetry',{}));_F19_HERD_TELEMETRY.update(_F19_HERD_REPORT)
    return action
agent.telemetry=_F19_HERD_TELEMETRY
agent=globals().pop('agent')
