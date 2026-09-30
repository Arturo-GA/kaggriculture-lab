# Original Arturo-GA, Apache-2.0. Economic guard for optional wool urgency.
# A high, flat price does not justify abandoning useful fertilizer collection.
_F20V_WORKER=_v233_worker
_F20V_PARENT=agent
_F20V_REPORT=dict(f20v_calm_market=0,f20v_urgent_market=0,f20v_errors=0)

def _v233_worker(obs,actor,targets):
    try:
        if len(targets)==3 and int(obs['step'])//24<28:
            player=int(obs['player']);farm=obs['farms'][player]
            tiles=[farm['tiles'][y][x] for x,y in targets]
            if all(isinstance(t,dict) and t.get('animal')=='SHEEP' for t in tiles):
                cargo=int(obs['private']['inventories'][actor].get('WOOL',0))
                wool=cargo+sum(int(t.get('yield_units',0)) for t in tiles)
                if wool>0:
                    # Stress the current price with wool already observable:
                    # both farms' standing yields and our own carried/shed wool.
                    # Rival carried inventories and future shops are not known.
                    batch=sum(int(inv.get('WOOL',0)) for inv in obs['private']['inventories'])
                    batch+=int(obs['private']['shed'].get('WOOL',0))
                    batch+=sum(int(t.get('yield_units',0)) for f in obs['farms'] for row in f['tiles'] for t in row
                        if isinstance(t,dict) and t.get('animal')=='SHEEP')
                    params={'WOOL':dict(_R37_MARKET_PARAMS['WOOL'])}
                    params['WOOL'].update(obs['market'].get('params',{}).get('WOOL',{}))
                    quote=int(obs['market']['prices']['WOOL'])
                    stressed=_r37_market_price('WOOL',int(obs['market']['inventory']['WOOL'])+batch,params)
                    exposure=wool*max(0,quote-stressed)
                    fertilizer=sum(bool(t.get('fertilizer_available')) for t in tiles)*int(obs['market']['prices']['FERTILIZER'])
                    if exposure<=fertilizer:
                        _F20V_REPORT['f20v_calm_market']+=1
                        return _F20D_WORKER(obs,actor,targets)
                    _F20V_REPORT['f20v_urgent_market']+=1
    except Exception:
        _F20V_REPORT['f20v_errors']+=1
        return _F20D_WORKER(obs,actor,targets)
    return _F20V_WORKER(obs,actor,targets)

_F20V_TELEMETRY={}
def agent(observation,configuration=None):
    if int(observation['step'])==0:
        for k in _F20V_REPORT:_F20V_REPORT[k]=0
    action=_F20V_PARENT(observation,configuration)
    _F20V_TELEMETRY.clear();_F20V_TELEMETRY.update(getattr(_F20V_PARENT,'telemetry',{}));_F20V_TELEMETRY.update(_F20V_REPORT)
    return action
agent.telemetry=_F20V_TELEMETRY
agent=globals().pop('agent')
