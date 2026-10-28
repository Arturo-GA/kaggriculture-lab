"""Allocate the shared shed capacity across terminal deposit commands.

Original multiple-choice knapsack on physical inventories. Each unit may DROP
all its cargo, PLACE one product, or retain its cargo. No destructive partial
DROP is permitted. Quote values are estimates; future/rival private stock is
not observed. Orders are recomputed from exact resulting own field state.
"""


def _f3_capacity(obs,action):
    farm=obs['farms'][obs['player']];private=obs['private']
    positions=[farm['farmer'],*farm['hands']]
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    eligible=[i for i,(pos,c) in enumerate(zip(positions,commands))
              if tuple(pos) in _AU_HOME and c[0] in ('DROP','PASS') and private['inventories'][i]]
    if not eligible:return action
    # Fixed commands reserve capacity before distributing the remaining room.
    projected_farm,projected_private=_PLANNER_NS['_clone_state'](farm,private)
    fixed=list(commands)
    for i in eligible:fixed[i]=['PASS']
    for i,c in enumerate(fixed[:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](projected_farm,projected_private,i,c,10,29,24,100)
    room=max(0,100-sum(projected_private['shed'].values()))
    total=sum(sum(private['inventories'][i].values()) for i in eligible)
    if total<=room:return action
    prices=obs['market']['prices']
    # dp[used] = estimated value, path. Equal-value choices use less capacity.
    dp={0:(0.,())}
    for i in eligible:
        inv=private['inventories'][i]
        options=[(0,0.,['PASS'])]
        n=sum(inv.values())
        if n<=room:
            options.append((n,sum(prices.get(p,0)*q for p,q in inv.items()),['DROP']))
        for item,q in sorted(inv.items()):
            if item not in prices or q<=0:continue
            for take in range(1,min(int(q),room)+1):
                options.append((take,prices[item]*take,['PLACE',item,take]))
        updated={}
        for used,(value,path) in dp.items():
            for count,gain,cmd in options:
                key=used+count
                if key>room:continue
                proposal=(value+gain,path+(cmd,))
                if key not in updated or proposal[0]>updated[key][0]:updated[key]=proposal
        dp=updated
    used,(_,chosen)=max(dp.items(),key=lambda pair:(pair[1][0],-pair[0]))
    result=copy.deepcopy(action)
    result_commands=[result.get('farmer') or ['PASS'],*(result.get('hands') or [])]
    for i,c in zip(eligible,chosen):result_commands[i]=c
    result['farmer'],result['hands']=result_commands[0],result_commands[1:]
    pf,pp=_PLANNER_NS['_clone_state'](farm,private)
    for i,c in enumerate(result_commands[:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](pf,pp,i,c,10,29,24,100)
    projected=dict(pp['shed'])
    state=_AU_STATE.get(obs['player'],{})
    reserve=sum(p['inputs'] for p in state.get('plans',[]) if p['inputs'] and obs['step']<p['start'])
    projected['FERTILIZER']=max(0,projected.get('FERTILIZER',0)-reserve)
    other=[o for o in result.get('market',[]) if o and o[0]!='SELL']
    sales=[['SELL',p,q] for p,q in projected.items() if q>0 and p in prices]
    sales.sort(key=lambda o:(-_r37_quote_priority(obs,o,projected),-o[2]*prices[o[1]],o[1]))
    result['market']=sales[:max(0,10-len(other))]+other
    _R124_REPORT['f3_capacity_turns']+=1
    _R124_REPORT['f3_deposit_units_deferred']+=total-used
    return result
