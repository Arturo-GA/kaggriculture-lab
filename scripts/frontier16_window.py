# Frontier16 window-head liquidation on the new public production base.
# Original integration of the attributed E081 idea (mooman0222, MIT), as in F15.
_F16_WINDOW_PARENT=agent
_F16_WINDOW_REPORT=dict(f16_window_turns=0,f16_window_units=0,f16_window_errors=0)


def agent(observation,configuration=None):
    action=_F16_WINDOW_PARENT(observation,configuration)
    step=int(observation['step'])
    if step==0:
        for k in _F16_WINDOW_REPORT:_F16_WINDOW_REPORT[k]=0
    try:
        if 216<=step<700 and step%4==1:
            orders=[list(o) for o in action.get('market',[])]
            if not any(o and o[0]=='BUY_PRODUCT' for o in orders):
                stock=projected_shed(action,FarmView(observation));changed=0
                for item in ('MILK','WOOL','STRAWBERRY'):
                    selling=sum(int(o[2]) for o in orders if len(o)>=3 and o[:2]==['SELL',item])
                    extra=max(0,int(stock.get(item,0))-selling)
                    if not extra:continue
                    same=next((o for o in orders if len(o)>=3 and o[:2]==['SELL',item]),None)
                    if same is not None:same[2]=int(same[2])+extra
                    elif len(orders)<10:orders.insert(0,['SELL',item,extra])
                    else:continue
                    changed+=extra
                if changed:
                    action=dict(action,market=orders)
                    _F16_WINDOW_REPORT['f16_window_turns']+=1
                    _F16_WINDOW_REPORT['f16_window_units']+=changed
                    state=_RACE_STATE.get(int(observation['player']))
                    if state is not None and state.get('step')==step:state['prev_action']=action
    except Exception:
        _F16_WINDOW_REPORT['f16_window_errors']+=1
    _F16_WINDOW_TELEMETRY.clear();_F16_WINDOW_TELEMETRY.update(getattr(_F16_WINDOW_PARENT,'telemetry',{}));_F16_WINDOW_TELEMETRY.update(_F16_WINDOW_REPORT)
    return action


_F16_WINDOW_TELEMETRY={}
agent.telemetry=_F16_WINDOW_TELEMETRY
agent=globals().pop('agent')
