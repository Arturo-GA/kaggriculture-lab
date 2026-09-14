"""Observed-resource contracts around Frontier, Apache-2.0.

Funding and atomic planting helpers adapted from Ahmed Berat Ozer's V41;
opening credited there to Rayk Kretzschmar. General-day seed validation,
integration and confirmed-effect telemetry: Arturo-GA / Kaggriculture Lab.
"""
_F3_PARENT=agent
_F3_STATES={}
_R124_REPORT={}


def agent(observation,configuration=None):
    action=_F3_PARENT(observation,configuration)
    player=int(observation['player']);step=int(observation['step'])
    state=_F3_STATES.get(player)
    if state is None or step<=state['step']:
        state=_F3_STATES[player]={'step':-1,'pending_plants':[]}
        _R124_REPORT.clear()
        _R124_REPORT.update(opening_seed_budget_units=0,opening_seed_budget_cost=0,
            opening_atomic_dropped=0,opening_atomic_rescued_requests=0,
            opening_atomic_rescued_confirmed=0,opening_atomic_plant_errors=0,
            opening_day1_cash=0,opening_day1_hires_requested=0,
            opening_day1_hires_confirmed=0,opening_day1_hire_shortfalls=0,
            f3_resource_errors=0,f3_capacity_turns=0,f3_deposit_units_deferred=0)
    state['step']=step
    farm=observation['farms'][player]
    for p in state.pop('pending_plants',[]):
        x,y=p['xy'];tile=farm['tiles'][y][x]
        if isinstance(tile,dict) and tile.get('crop')==p['crop'] and tile.get('planted_day')==p['birth']:
            _R124_REPORT['opening_atomic_rescued_confirmed']+=1
        else:_R124_REPORT['opening_atomic_plant_errors']+=1
    standard=all((configuration or {}).get(k,v)==v for k,v in
        [('boardSize',10),('episodeSteps',720),('turnsPerDay',24),('shedCapacity',100),
         ('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
    if standard:
        original=action
        try:
            if step<24:
                native=_ROUTES[_IMPL.chassis.players[player]['route']]
                reserve,_=_r124_labor_reserve(native)
                action=_r124_seed_budget(observation,action,reserve)
            if step<696:action=_r124_atomic(observation,action,state)
            if _F3_CAPACITY and step>=716:action=_f3_capacity(observation,action)
        except Exception:
            _R124_REPORT['f3_resource_errors']+=1
            action=original
    if step==24:
        _R124_REPORT['opening_day1_cash']=farm['money']
        state['hires']=sum(bool(o) and o[0]=='HIRE' for o in action.get('market',[]))
        _R124_REPORT['opening_day1_hires_requested']=state['hires']
    if step==25:
        _R124_REPORT['opening_day1_hires_confirmed']=len(farm['hands'])
        _R124_REPORT['opening_day1_hire_shortfalls']=max(0,state.get('hires',0)-len(farm['hands']))
    agent.telemetry=dict(getattr(_F3_PARENT,'telemetry',{}),**_R124_REPORT)
    return action


agent.telemetry={}
agent=globals().pop('agent')
