# Original Arturo-GA, Apache-2.0. Causal per-product sale-race observation.
# Opponent orders/private inventory are never read. Public market changes,
# known town consumption and our covered sales identify past rival pressure.
_F20_PARENT=agent
_F20_ITEMS=('STRAWBERRY','MILK','WOOL','EGG','CARROT','TOMATO','MELON')
_F20_STATE={}
_F20_REPORT=dict(f20_observed_sales=0,f20_preemptions=0,f20_turns=0,f20_units=0,f20_errors=0)

def _f20_update(obs,st):
    step=int(obs['step']);prev=st.get('prev')
    if not prev or prev['step']+1!=step:return
    draw=_race_town(prev['step'],prev['shops'])
    inventory=obs['market']['inventory'];prices=obs['market']['prices']
    for item in _F20_ITEMS:
        # Floor-price sales do not increase market inventory: abstain there.
        if min(prev['prices'].get(item,0),prices.get(item,0))<=3:continue
        q=int(inventory[item])-prev['inventory'][item]+draw.get(item,0)-prev['sold'].get(item,0)
        if q<2:continue
        _F20_REPORT['f20_observed_sales']+=1
        if prev['left'].get(item,0)>0 and prev['similar']:
            st['threats'][item]=st['threats'].get(item,0)+1
            st['last'][item]=step
            _F20_REPORT['f20_preemptions']+=1

def _f20_apply(obs,action,st):
    step=int(obs['step']);player=int(obs['player'])
    if not 216<=step<696 or _r37_similarity(obs)<.9:return action
    native=_IMPL.chassis.players.get(player)
    if not native:return action
    orders=[list(o) for o in action.get('market',[])]
    view=FarmView(obs);stock=projected_shed(action,view)
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    blocked={o[1] for o in orders if len(o)>1 and o[0]=='BUY_PRODUCT'}
    blocked.update(c[1] for c in commands if len(c)>1 and c[0]=='PICKUP')
    blocked.update(c[1] for queue in native['pending'].values() for pos,c in queue if len(c)>1 and c[0]=='PICKUP')
    debts=native['sell_state'].setdefault('r36_debts',{})
    added=0
    for item in _F20_ITEMS:
        if item in blocked or obs['market']['prices'].get(item,0)<3:continue
        if _F20_REACTIVE and (st['threats'].get(item,0)<2 or step-st['last'].get(item,-999)>120):continue
        current=sum(max(0,int(o[2])) for o in orders if len(o)>=3 and o[:2]==['SELL',item])
        avail=max(0,int(stock.get(item,0))-current)
        if not avail:continue
        hit=next((o for o in orders if len(o)>=3 and o[:2]==['SELL',item]),None)
        if hit is None and len(orders)>=10:continue
        reservations=[]
        for due in range(step+1,min(695,step+_F20_LOOK)+1):
            # Never cross the crew reset or pre-spend next day's inputs.
            if due//24!=step//24:break
            tape=_IMPL.chassis.routes[2 if due>=648 else native['route']][due]
            work=[tape.get('farmer') or ['PASS'],*(tape.get('hands') or [])]
            if any(c[:2]==['PICKUP',item] for c in work):break
            if any(o[:2]==['BUY_PRODUCT',item] for o in tape.get('market',[])):break
            planned=sum(max(0,int(o[2])) for o in tape.get('market',[]) if len(o)>=3 and o[:2]==['SELL',item])
            take=min(avail,max(0,planned-debts.get(due,{}).get(item,0)))
            if take:reservations.append((due,take));avail-=take
            if not avail:break
        qty=sum(q for _,q in reservations)
        if not qty:continue
        if hit is None:orders.insert(0,['SELL',item,qty])
        else:hit[2]=int(hit[2])+qty
        for due,q in reservations:
            debt=debts.setdefault(due,{})
            debt[item]=debt.get(item,0)+q
        added+=qty
    if not added:return action
    _F20_REPORT['f20_turns']+=1;_F20_REPORT['f20_units']+=added
    return dict(action,market=orders)

_F20_TELEMETRY={}
def agent(observation,configuration=None):
    step=int(observation['step']);player=int(observation['player'])
    if step==0 or player not in _F20_STATE:
        _F20_STATE[player]=dict(prev=None,threats={},last={})
        for k in _F20_REPORT:_F20_REPORT[k]=0
    st=_F20_STATE[player]
    try:_f20_update(observation,st)
    except Exception:_F20_REPORT['f20_errors']+=1
    action=_F20_PARENT(observation,configuration)
    try:
        action=_f20_apply(observation,action,st)
        stock=projected_shed(action,FarmView(observation));sold={}
        for o in action.get('market',[]):
            if len(o)>=3 and o[0]=='SELL' and o[1] in _F20_ITEMS:sold[o[1]]=sold.get(o[1],0)+max(0,int(o[2]))
        sold={p:min(q,max(0,int(stock.get(p,0)))) for p,q in sold.items()}
        st['prev']=dict(step=step,inventory=dict(observation['market']['inventory']),prices=dict(observation['market']['prices']),
                       shops=list(observation['town'].get('unlocked_shops',[])),sold=sold,
                       left={p:max(0,int(stock.get(p,0))-sold.get(p,0)) for p in _F20_ITEMS},similar=_r37_similarity(observation)>=.9)
        state=_RACE_STATE.get(player)
        if state is not None and state.get('step')==step:state['prev_action']=action
    except Exception:_F20_REPORT['f20_errors']+=1
    _F20_TELEMETRY.clear();_F20_TELEMETRY.update(getattr(_F20_PARENT,'telemetry',{}));_F20_TELEMETRY.update(_F20_REPORT)
    return action
agent.telemetry=_F20_TELEMETRY
agent=globals().pop('agent')
