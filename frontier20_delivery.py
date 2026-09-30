# Original Arturo-GA, Apache-2.0. Extra-sheep delivery priority learned from
# exact live defeat 115933722: fertilizer collection delayed two wool couriers
# by three ticks, while an otherwise comparable farm sold before the crash.
_F20D_WORKER=_v233_worker
_F20D_PARENT=agent
_F20D_REPORT=dict(f20d_prioritized=0,f20d_filled_turns=0,f20d_filled_units=0,f20d_errors=0)

def _v233_worker(obs,actor,targets):
    if not _F20D_WOOL:return _F20D_WORKER(obs,actor,targets)
    try:
        # Only the dynamic three-sheep couriers; retain construction, the
        # six-sheep feeding-only routine, native workers and final-day logic.
        day=int(obs['step'])//24
        if len(targets)!=3 or day>=28:return _F20D_WORKER(obs,actor,targets)
        player=int(obs['player']);farm=obs['farms'][player]
        if not all(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='SHEEP' for x,y in targets):
            return _F20D_WORKER(obs,actor,targets)
        wool=int(obs['private']['inventories'][actor].get('WOOL',0))
        wool+=sum(int(farm['tiles'][y][x].get('yield_units',0)) for x,y in targets)
        if wool<=0:return _F20D_WORKER(obs,actor,targets)
        # A local scheduling view hides optional fertilizer tasks only while
        # wool remains to be harvested/delivered. Real observations stay intact;
        # FEED, CARE, HARVEST, cargo and return routing use the actual state.
        tiles=list(farm['tiles'])
        for y in {xy[1] for xy in targets}:tiles[y]=list(tiles[y])
        for x,y in targets:tiles[y][x]=dict(tiles[y][x],fertilizer_available=False)
        farms=list(obs['farms']);farms[player]=dict(farm,tiles=tiles)
        original=_F20D_WORKER(obs,actor,targets)
        proposal=_F20D_WORKER(dict(obs,farms=farms),actor,targets)
        if original!=proposal:_F20D_REPORT['f20d_prioritized']+=1
        return proposal
    except Exception:
        _F20D_REPORT['f20d_errors']+=1
        return _F20D_WORKER(obs,actor,targets)

def _f20d_fill(obs,action):
    if not _F20D_FILL or not 216<=int(obs['step'])<696 or _r37_similarity(obs)<.95:return action
    orders=[list(o) for o in action.get('market',[])]
    stock=projected_shed(action,FarmView(obs));added=0
    for item in ('EGG','MILK','WOOL','STRAWBERRY','CARROT','TOMATO','MELON'):
        if obs['market']['prices'].get(item,0)<=3:continue
        hits=[o for o in orders if len(o)>=3 and o[:2]==['SELL',item] and int(o[2])>0]
        if not hits:continue
        qty=sum(int(o[2]) for o in hits);extra=max(0,int(stock.get(item,0))-qty)
        # Bound the correction to small residual batches already being sold.
        if not 0<extra<=8:continue
        hits[0][2]=int(hits[0][2])+extra;added+=extra
    if not added:return action
    _F20D_REPORT['f20d_filled_turns']+=1;_F20D_REPORT['f20d_filled_units']+=added
    return dict(action,market=orders)

_F20D_TELEMETRY={}
def agent(observation,configuration=None):
    if int(observation['step'])==0:
        for k in _F20D_REPORT:_F20D_REPORT[k]=0
    action=_F20D_PARENT(observation,configuration)
    try:
        action=_f20d_fill(observation,action)
        st=_RACE_STATE.get(int(observation['player']))
        if st is not None and st.get('step')==int(observation['step']):st['prev_action']=action
    except Exception:_F20D_REPORT['f20d_errors']+=1
    _F20D_TELEMETRY.clear();_F20D_TELEMETRY.update(getattr(_F20D_PARENT,'telemetry',{}));_F20D_TELEMETRY.update(_F20D_REPORT)
    return action
agent.telemetry=_F20D_TELEMETRY
agent=globals().pop('agent')
