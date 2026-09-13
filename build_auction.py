"""Original terminal workforce and harvest-route controller on the frozen prefix."""
import hashlib
import json
from pathlib import Path


def main():
    parent=Path('candidates/ml_critic.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='ff2b5c8c7ea5c1809648fb4e404c4937e8083b44eaf2d06e26f9b137bbbb3e95'
    helper=Path('terminal_auction.py').read_text()
    records={}
    variants={'auction_joint':(696,0.,1.),'auction_joint_risk':(696,.5,1.2),
              'auction_joint_late':(700,.5,1.2),'auction_joint_safe':(696,1.,2.)}
    for name,(start,risk,reserve) in variants.items():
        source=parent.decode()+'\n'+helper
        source+=f'\n_AU_START={start}\n_AU_RISK={risk!r}\n_AU_RESERVE={reserve!r}\n'
        source+='''
_AU_PARENT=agent
def agent(observation,configuration=None):
    if int(observation['step']) < _AU_START:
        action=_AU_PARENT(observation,configuration)
    else:
        action=_auction_controller(observation,configuration)
        if action is None:action=_AU_PARENT(observation,configuration)
    st=_AU_STATE.get(int(observation['player']),{})
    agent.telemetry=dict(getattr(_AU_PARENT,'telemetry',{}),
        **{'auction_'+k:v for k,v in st.items() if k in ('errors','turns','planned_workers',
            'hire_cost','harvest_requests','water_requests','fertilizer_requests','hire_requests','late_returns','unassigned',
            'input_purchase','input_applications')})
    return action
agent.telemetry={}
agent=globals().pop('agent')
'''
        compile(source,name,'exec')
        Path('candidates',name+'.py').write_bytes(source.encode())
        records[name]=dict(sha256=hashlib.sha256(source.encode()).hexdigest(),start=start,risk=risk,reserve=reserve)
    Path('results/gold/auction_joint_build.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))


if __name__=='__main__':main()
