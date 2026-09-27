# Original Frontier17: close or remove one-turn inventory-neutral speculative
# route pairs. Arturo-GA, Apache-2.0, September 27, 2026.
# Only own planned orders are read. No replay, seed or hidden rival information.
_F17_PARENT=agent
_F17_REPORT=dict(f17_pairs=0,f17_pair_units=0,f17_errors=0)


def _f17_prepare_routes():
    # Some routes share action dictionaries. Clone all routes together so the
    # parent data stays frozen, but keep deliberate shared references consistent.
    routes=copy.deepcopy(_IMPL.chassis.routes)
    seen=set()
    for route,tape in routes.items():
        for t in range(216,min(648,len(tape)-1)):
            if t%24==23:continue
            a,b=tape[t],tape[t+1]
            if not isinstance(a,dict) or not isinstance(b,dict):continue
            key=(id(a),id(b))
            if key in seen:continue
            seen.add(key)
            orders=a.get('market',[]);future=b.get('market',[])
            for item in ('WHEAT','FERTILIZER'):
                buys=[i for i,o in enumerate(orders) if len(o)>=3 and o[:2]==['BUY_PRODUCT',item] and int(o[2])>=12]
                sells=[i for i,o in enumerate(future) if len(o)>=3 and o[:2]==['SELL',item] and int(o[2])>=12]
                if len(buys)!=1 or len(sells)!=1:continue
                i,j=buys[0],sells[0];q=int(orders[i][2])
                if int(future[j][2])!=q:continue
                if any(len(o)>=2 and o[:2]==['SELL',item] for o in orders):continue
                if any(len(o)>=2 and o[:2]==['BUY_PRODUCT',item] for o in future):continue
                commands=[b.get('farmer',[]),*b.get('hands',[])]
                if any(c[:2]==['PICKUP',item] for c in commands):continue
                if _F17_MODE=='close' and len(orders)>=10:continue
                # Empty slots retain the simultaneous ordering of other trades.
                if _F17_MODE=='cancel':orders[i]=[]
                else:orders.append(['SELL',item,q])
                future[j]=[]
                _F17_REPORT['f17_pairs']+=1;_F17_REPORT['f17_pair_units']+=q
    _IMPL.chassis.routes=routes
    _IMPL.chassis._future_sells.clear()


_f17_prepare_routes()
_F17_TELEMETRY={}


def agent(observation,configuration=None):
    action=_F17_PARENT(observation,configuration)
    _F17_TELEMETRY.clear();_F17_TELEMETRY.update(getattr(_F17_PARENT,'telemetry',{}));_F17_TELEMETRY.update(_F17_REPORT)
    return action


agent.telemetry=_F17_TELEMETRY
agent=globals().pop('agent')
