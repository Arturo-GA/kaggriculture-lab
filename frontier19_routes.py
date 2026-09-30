# Original Arturo-GA, Apache-2.0. A public-replay production family with one
# coherent opening, causal routing at the second shop, and execution guards.
import base64 as _f19_b64,json as _f19_json,zlib as _f19_zlib
_F19_ROUTE_DATA=_f19_json.loads(_f19_zlib.decompress(_f19_b64.b85decode(_F19_ROUTE_BLOB)))
_F19_ROUTES={i:r['actions'] for i,r in enumerate(_F19_ROUTE_DATA)}
_F19_ROUTE_REPORT=dict(f19_route_selected=-1,f19_route_pair_exact=0,f19_route_rescue_feed=0,f19_route_terminal_recovered=0,f19_route_errors=0)

def _f19_router(obs,step,state):
    if step>=144 and 'selected' not in state:
        shops=tuple(obs['town']['unlocked_shops'][:2])
        def fit(i):
            row=_F19_ROUTE_DATA[i];known=tuple(row['shops'])
            ordered=sum(a==b for a,b in zip(shops,known))
            overlap=sum(min(shops.count(s),known.count(s)) for s in set(shops))
            return (known==shops,overlap,ordered,-row['rank'],row['episode'])
        state['selected']=max(_F19_ROUTES,key=fit)
        _F19_ROUTE_REPORT['f19_route_selected']=state['selected']
        _F19_ROUTE_REPORT['f19_route_pair_exact']=int(tuple(_F19_ROUTE_DATA[state['selected']]['shops'])==shops)
    return state.get('selected',0)

_F19_ROUTE_IMPL=make_agent(_F19_ROUTES,router=_f19_router,hand_align=True,weed_repair=True,
 sell_lead=_F19_ROUTE_SELL_LEAD,front_run=False,budget_guard=False,room_guard=True,
 clamp_sells=True,dead_stock=False,terminal_liquidation=True)

def _f19_route_act(obs,config=None):
    step=int(obs['step']);seat=int(obs['player']);farm=obs['farms'][seat];private=obs['private']
    action=_F19_ROUTE_IMPL(obs,config)
    if step>=696:
        cmds=[list(action.get('farmer') or ['PASS'])]+[list(c) for c in action.get('hands',[])]
        positions=[farm['farmer']]+farm['hands'];touched=set()
        for i,p in enumerate(positions[:len(cmds)]):
            x,y=p;tile=farm['tiles'][y][x];inv=private['inventories'][i]
            if cmds[i][0] in ('FEED','CARE') and isinstance(tile,dict) and tile.get('animal') and (x,y) not in touched:
                if tile.get('yield_units',0):cmds[i]=['HARVEST'];touched.add((x,y));_F19_ROUTE_REPORT['f19_route_terminal_recovered']+=1
                elif tile.get('fertilizer_available'):cmds[i]=['COLLECT_FERTILIZER'];touched.add((x,y))
                else:cmds[i]=['PASS']
            if sum(inv.get(p,0) for p in PRODUCTS)>0:
                home=min(((4,4),(5,4),(4,5),(5,5)),key=lambda h:abs(x-h[0])+abs(y-h[1]))
                dist=abs(x-home[0])+abs(y-home[1])
                if 718-step<=dist+1:
                    if dist==0:cmds[i]=['DROP']
                    elif home[0]>x:cmds[i]=['EAST']
                    elif home[0]<x:cmds[i]=['WEST']
                    elif home[1]>y:cmds[i]=['SOUTH']
                    else:cmds[i]=['NORTH']
        action=dict(action,farmer=cmds[0],hands=cmds[1:])
        if step>=718:
            stock=_F19_ROUTE_IMPL.chassis._projected_shed(action,_View(obs,seat,_F19_ROUTE_IMPL.chassis.cfg))
            action['market']=[['SELL',p,q] for p,q in stock.items() if p in PRODUCTS and q>0][:10]
    return action

_F19_ROUTE_TELEMETRY={}
def agent(observation,configuration=None):
    if int(observation['step'])==0:
        for k in _F19_ROUTE_REPORT:_F19_ROUTE_REPORT[k]=0
        _F19_ROUTE_REPORT['f19_route_selected']=-1
    try:result=_f19_route_act(observation,configuration)
    except Exception:
        _F19_ROUTE_REPORT['f19_route_errors']+=1
        raise
    _F19_ROUTE_TELEMETRY.clear();_F19_ROUTE_TELEMETRY.update(_F19_ROUTE_REPORT)
    _F19_ROUTE_TELEMETRY.update({'chassis_'+k:v for k,v in _F19_ROUTE_IMPL.chassis.diagnostics.items()})
    return result
agent.telemetry=_F19_ROUTE_TELEMETRY
agent=globals().pop('agent')
