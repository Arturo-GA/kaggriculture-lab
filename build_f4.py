"""Assemble Frontier4 candidates: public V45 base + clone race horizon + Kaggriculture Lab terminal layers.

Inputs: candidates/v45.py (from extract_public_agents.py, git-ignored) and frontier4_layers.py (our
terminal planner, route deliveries and capacity allocation lifted from the Frontier3 lineage).
"""
import hashlib
import json
import re
from pathlib import Path

V45_SHA256 = '2536d41ed5a00c75204b6350f1c76c54259c774cb065ba2a3a0072eedf210d94'
RACE_OLD = '_RACE_HORIZON_CLONE=8'
RACE_NEW = '_RACE_HORIZON_CLONE=24'

v45 = Path('candidates/v45.py').read_bytes()
assert hashlib.sha256(v45).hexdigest() == V45_SHA256, 'Public V45 source changed; re-extract and re-verify'
v45 = v45.decode('utf-8')
assert v45.count(RACE_OLD) == 1
base = v45.replace(RACE_OLD, RACE_NEW)
# Adaptive race: escalate to the 24-turn horizon as soon as the rival sells a race product at the very
# turn our shed received it (a same-turn seller), even when we also sold; V45 escalates only after
# holding while the rival quoted. Non-racing rivals (V43-style four-turn sellers) never trigger it.
ADAPT_OLD = "if held<=before or item in sold or prices.get(item,0)<=1:continue"
ADAPT_NEW = "if held<=before or prices.get(item,0)<=1:continue"
assert v45.count(ADAPT_OLD) == 1
adapt = v45.replace(ADAPT_OLD, ADAPT_NEW)
# Adaptive race, tape-aware: a rival sale at our drop turn counts as racing evidence only when our own
# route tape does not plan to sell that product within the next four turns (a V43-style four-turn seller
# would legitimately quote there). Otherwise identical to V45.
ADAPT2_HELPER = '''def _f4_tape_sells_soon(observation,item,within):
    try:
        player=int(observation['player']);step=int(observation['step'])
        native=_IMPL.chassis.players[player];tape=_IMPL.chassis.routes[native['route']]
        for s in range(max(0,step-1),min(len(tape),step+within)):
            t=tape[s] if isinstance(tape[s],dict) else {}
            if any(len(o)>=3 and o[0]=='SELL' and o[1]==item for o in t.get('market',[])):return True
        return False
    except Exception:
        return True

def _race_lost(observation,state):'''
ADAPT2_NEW = ("if held<=before or prices.get(item,0)<=1:continue\r\n"
              "        if item in sold and _f4_tape_sells_soon(observation,item,4):continue")
assert v45.count('def _race_lost(observation,state):') == 1
adapt2 = v45.replace(ADAPT_OLD, ADAPT2_NEW).replace('def _race_lost(observation,state):', ADAPT2_HELPER)
# Probe race: start the clone horizon at 24 turns, which wins the first long-horizon race against
# V44/V45-style rivals and makes them escalate. Then watch the rival: if within _F4_PROBE_TURNS it sells
# a race product at our drop turn that our own tape only sells more than four turns later (evidence of a
# long horizon), keep 24; otherwise (V43-style four-turn sellers) fall back to V45's 8-turn behaviour.
# V45's own lost-race escalation stays in force after the fallback. Rival sales are measured net of our
# own filled sales, reconstructed from our shed and drop accounting.
PROBE_HELPER = '''_F4_PROBE_LEVEL=24
_F4_PROBE_END=336

def _f4_tape_sells_soon(observation,item,within):
    try:
        player=int(observation['player']);step=int(observation['step'])
        native=_IMPL.chassis.players[player];tape=_IMPL.chassis.routes[native['route']]
        for s in range(max(0,step-1),min(len(tape),step+within)):
            t=tape[s] if isinstance(tape[s],dict) else {}
            if any(len(o)>=3 and o[0]=='SELL' and o[1]==item for o in t.get('market',[])):return True
        return False
    except Exception:
        return True

def _f4_rival_long(observation,state):
    """True when the rival sold, at our previous drop turn, a race product our tape sells >4 turns later."""
    prev=state.get('prev');prev_action=state.get('prev_action')
    if prev is None or prev_action is None:return False
    step=int(observation['step'])
    if step!=prev['step']+1 or step%24==0:return False
    shed=observation['private']['shed'];inv=observation['market']['inventory'];pinv=prev['inventory'];prices=prev['prices']
    town=_race_town(step-1,prev['shops']);view=prev['view']
    commands=[prev_action.get('farmer') or ['PASS'],*(prev_action.get('hands') or [])]
    for item in _RACE_ITEMS:
        held=int(shed.get(item,0));before=int(view.shed.get(item,0))
        if prices.get(item,0)<=1:continue
        dropped=0
        for i,c in enumerate(commands[:len(view.positions)]):
            if not c:continue
            if c[0]=='DROP':dropped+=int(view.inv(i).get(item,0))
            elif c[0]=='PLACE' and len(c)>1 and c[1]==item:dropped+=min(int(c[2]) if len(c)>2 else 1,int(view.inv(i).get(item,0)))
        if held<=before and dropped<=0:continue
        ours=max(0,before+dropped-held)
        rival=int(inv[item])-int(pinv[item])+town.get(item,0)-ours
        if rival>0 and not _f4_tape_sells_soon(observation,item,4):return True
    return False

def _race_lost(observation,state):'''
PROBE_STATE_OLD = "state=_RACE_STATE[player]={'step':-1,'hist':[],'horizon':0,'level':_RACE_HORIZON_CLONE,'prev':None,'prev_action':None}"
PROBE_STATE_NEW = "state=_RACE_STATE[player]={'step':-1,'hist':[],'horizon':0,'level':_F4_PROBE_LEVEL,'prev':None,'prev_action':None,'probe':None,'confirmed':False}"
PROBE_BLOCK_OLD = "            _RACE_REPORT['race_clone_turns']+=1\r\n            if state['level']<_RACE_HORIZON_ESCALATED and _race_lost(observation,state):"
PROBE_BLOCK_NEW = ("            _RACE_REPORT['race_clone_turns']+=1\r\n"
                   "            if not state['confirmed'] and _f4_rival_long(observation,state):state['confirmed']=True;_RACE_REPORT['f4_probe_confirmed']+=1\r\n"
                   "            if state['confirmed']:state['level']=_RACE_HORIZON_ESCALATED\r\n"
                   "            elif step<_F4_PROBE_END:state['level']=max(state['level'],_F4_PROBE_LEVEL)\r\n"
                   "            elif state['level']==_F4_PROBE_LEVEL and not state.get('reverted'):state['level']=_RACE_HORIZON_CLONE;state['reverted']=True;_RACE_REPORT['f4_probe_reverted']+=1\r\n"
                   "            if state['level']<_RACE_HORIZON_ESCALATED and _race_lost(observation,state):")
PROBE_REPORT_OLD = "_RACE_REPORT=dict(race_clone_turns=0,race_horizon_turns=0,race_lost_races=0,race_escalations=0,race_errors=0)"
PROBE_REPORT_NEW = "_RACE_REPORT=dict(race_clone_turns=0,race_horizon_turns=0,race_lost_races=0,race_escalations=0,race_errors=0,f4_probe_confirmed=0,f4_probe_reverted=0)"
PROBE_RESET_OLD = "if step==0:_RACE_REPORT.update(race_clone_turns=0,race_horizon_turns=0,race_lost_races=0,race_escalations=0,race_errors=0)"
PROBE_RESET_NEW = "if step==0:_RACE_REPORT.update(race_clone_turns=0,race_horizon_turns=0,race_lost_races=0,race_escalations=0,race_errors=0,f4_probe_confirmed=0,f4_probe_reverted=0)"
for old in (PROBE_STATE_OLD, PROBE_BLOCK_OLD, PROBE_REPORT_OLD, PROBE_RESET_OLD):
    assert v45.count(old) == 1, old[:60]
probe = (v45.replace('def _race_lost(observation,state):', PROBE_HELPER)
         .replace(PROBE_STATE_OLD, PROBE_STATE_NEW).replace(PROBE_BLOCK_OLD, PROBE_BLOCK_NEW)
         .replace(PROBE_REPORT_OLD, PROBE_REPORT_NEW).replace(PROBE_RESET_OLD, PROBE_RESET_NEW))
layers = Path('frontier4_layers.py').read_text(encoding='utf-8').splitlines()
au_defs = '\n'.join(layers[13:227])
au_wrap = '\n'.join(layers[227:278])
fr = '\n'.join(layers[278:387])
f2 = '\n'.join(layers[387:459])
f3c = '\n'.join(layers[459:526])
cap_wrapper = '''
_F4C_PARENT=agent
_F4C_REPORT=dict(f4_capacity_errors=0)
def agent(observation,configuration=None):
    action=_F4C_PARENT(observation,configuration)
    try:
        step=int(observation['step'])
        standard=all((configuration or {}).get(k,v)==v for k,v in [('boardSize',10),('episodeSteps',720),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard and step>=716:action=_f3_capacity(observation,action)
    except Exception:
        _F4C_REPORT['f4_capacity_errors']+=1
    _F4C_TELEMETRY.clear()
    _F4C_TELEMETRY.update(getattr(_F4C_PARENT,'telemetry',{}))
    _F4C_TELEMETRY.update(_F4C_REPORT)
    return action
_F4C_TELEMETRY={}
agent.telemetry=_F4C_TELEMETRY
agent=globals().pop('agent')
'''
products = Path('frontier4_ml_support.py').read_text(encoding='utf-8') + '\n'
terminal = ('\n# ==== Frontier4 terminal layers (Arturo-GA / Kaggriculture Lab, Apache-2.0) ====\n' + products
            + au_defs + '\n' + au_wrap + '\n' + fr + '\n' + f2 + '\n' + f3c
            + '\n_R124_REPORT=globals().get("_R124_REPORT",{})\n' + cap_wrapper)
runner = Path('f4_runner.py').read_text(encoding='utf-8')


def write(name, src, overrides=None):
    for k, v in (overrides or {}).items():
        pat = r'^%s=.*$' % re.escape(k)
        assert re.search(pat, src, flags=re.M), k
        src = re.sub(pat, '%s=%r' % (k, v), src, count=1, flags=re.M)
    compile(src.replace('\r\n', '\n'), name, 'exec')
    Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
    print('wrote', name, len(src))


NOCAP_OLD = "end=min(695,step+_R37_HORIZONS.get(int(obs['player']),2),(step//72+1)*72-1)"
NOCAP_NEW = "end=min(695,step+_R37_HORIZONS.get(int(obs['player']),2),647 if step<648 else 695)"


def nocap(src):
    assert src.count(NOCAP_OLD) == 1
    return src.replace(NOCAP_OLD, NOCAP_NEW)


if __name__ == '__main__':
    write('f4_r24', base)
    write('f4_full', base + terminal)
    write('f4_r24b', nocap(base))
    write('f4_fullb', nocap(base) + terminal)
    write('f4_run', base + '\n' + runner)
    write('f4_term', v45 + terminal)
    write('f4_adapt', adapt)
    write('f4_adapt_full', adapt + terminal)
    write('f4_adapt2', adapt2)
    write('f4_probe', probe)
    manifest = {n: hashlib.sha256(Path('candidates', n + '.py').read_bytes()).hexdigest()
                for n in ('f4_r24', 'f4_full', 'f4_r24b', 'f4_fullb', 'f4_run', 'f4_term', 'f4_adapt', 'f4_adapt_full', 'f4_adapt2', 'f4_probe')}
    manifest['v45_sha256'] = V45_SHA256
    Path('results/frontier4').mkdir(parents=True, exist_ok=True)
    Path('results/frontier4/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))
