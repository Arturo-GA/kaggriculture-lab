# Original Arturo-GA, Apache-2.0. Current opponent motifs supplement the frozen
# historical predictor only after matching a causal prefix of observed sales.
_F19_FORECAST_OLD=_v92_p_forecast
_F19_FORECAST_ROWS=None
_F19_FORECAST_REPORT=dict(f19_forecast_checked=0,f19_forecast_matched=0,f19_forecast_uncertain=0,f19_forecast_errors=0)

def _f19_recent_patterns():
    global _F19_FORECAST_ROWS
    if _F19_FORECAST_ROWS is None:
        raw=_v92_json.loads(_v92_zlib.decompress(_v92_b64.b85decode(_F19_FORECAST_BLOB)))
        _F19_FORECAST_ROWS=[(r['team_id'],tuple(r['shops']),{(t,i):q for t,i,q in r['events']}) for r in raw]
    return _F19_FORECAST_ROWS

def _v92_p_forecast(obs,st):
    _F19_FORECAST_REPORT['f19_forecast_checked']+=1
    step=int(obs['step']);shops=tuple(obs['town']['unlocked_shops']);seen=st['obs'];lo=max(144,step-240)
    recent={(t,i) for t,i in seen if lo<=t<step-1}
    if len(recent)<8:return _F19_FORECAST_OLD(obs,st)
    best=[]
    for team,prefix,events in _f19_recent_patterns():
        # Compare only shops already public, never later shop identities.
        if prefix[:2]!=shops[:2]:continue
        sample={(t,i) for t,i in events if lo<=t<step-1}
        if len(sample)<8:continue
        hit=sum(any((t+d,i) in recent for d in (-1,0,1)) for t,i in sample)
        missing=sum(not any((t+d,i) in sample for d in (-1,0,1)) for t,i in recent)
        precision=hit/len(sample)
        if precision<_F19_FORECAST_PRECISION or hit<6:continue
        score=hit-.5*(len(sample)-hit)-.5*missing
        score-=sum(a!=b for a,b in zip(prefix[2:len(shops)],shops[2:]))
        best.append((score,team,events))
    if not best:
        _F19_FORECAST_REPORT['f19_forecast_uncertain']+=1
        return _F19_FORECAST_OLD(obs,st)
    best.sort(key=lambda x:-x[0]);top=best[0][0]
    previous=_F19_FORECAST_OLD(obs,st)
    def score_old(events):
        sample={(t,i) for t,i in events if lo<=t<step-1}
        hit=sum(any((t+d,i) in recent for d in (-1,0,1)) for t,i in sample)
        missing=sum(not any((t+d,i) in sample for d in (-1,0,1)) for t,i in recent)
        return hit-.5*(len(sample)-hit)-.5*missing
    if previous and top<max(score_old(ev) for ev in previous)+_F19_FORECAST_ADVANTAGE:
        _F19_FORECAST_REPORT['f19_forecast_uncertain']+=1
        return previous
    pool=[];teams=set()
    for score,team,events in best:
        if score<top-2 or team in teams:continue
        pool.append(events);teams.add(team)
        if len(pool)==3:break
    # A consensus signal rather than selecting a favourable future single game.
    needed=2 if len(pool)>1 else 1
    future={}
    for t in range(step,min(719,step+49)):
        for i in range(len(_V92_P_ITEMS)):
            quantities=sorted((sum(ev.get((t+d,i),0) for d in (-1,0,1)) for ev in pool),reverse=True)
            q=quantities[needed-1]
            if q>=4:future[(t,i)]=q
    # Retain observed-era evidence for the inherited four-turn confidence gate.
    for key,q in pool[0].items():
        if key[0]<step:future[key]=q
    _F19_FORECAST_REPORT['f19_forecast_matched']+=1
    return [future]

_F19_FORECAST_PARENT=agent
_F19_FORECAST_TELEMETRY={}
def agent(observation,configuration=None):
    if int(observation['step'])==0:
        for k in _F19_FORECAST_REPORT:_F19_FORECAST_REPORT[k]=0
    action=_F19_FORECAST_PARENT(observation,configuration)
    _F19_FORECAST_TELEMETRY.clear();_F19_FORECAST_TELEMETRY.update(getattr(_F19_FORECAST_PARENT,'telemetry',{}));_F19_FORECAST_TELEMETRY.update(_F19_FORECAST_REPORT)
    return action
agent.telemetry=_F19_FORECAST_TELEMETRY
agent=globals().pop('agent')
