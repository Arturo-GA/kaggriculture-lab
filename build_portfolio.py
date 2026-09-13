import hashlib
import json
from pathlib import Path


def main():
    source=Path('candidates/auction_joint_risk.py').read_text(encoding='utf-8')
    assert hashlib.sha256(source.encode()).hexdigest()=='8906f6dbbf065b62e6d0af4a74f504f3828549c57f57c626e86552b0c7bc3178'
    helper=Path('crop_portfolio.py').read_text()
    records={}
    for name,threshold in [('portfolio_v2',1.05),('portfolio_v2safe',1.3)]:
        text=source+'\n'+helper+f'\n_PF_THRESHOLD={threshold!r}\n'+'''
_PF_PARENT=agent
def agent(observation,configuration=None):
    _pf_before(observation,configuration)
    action=_PF_PARENT(observation,configuration)
    action=_pf_after(observation,action)
    st=_PF_STATE[observation['player']]
    agent.telemetry=dict(getattr(_PF_PARENT,'telemetry',{}),**{'portfolio_'+k:st[k] for k in
        ('replacements','seed_requests','decisions','errors','confirmed','missed')})
    return action
agent.telemetry={}
agent=globals().pop('agent')
'''
        compile(text,name,'exec');Path('candidates',name+'.py').write_bytes(text.encode())
        records[name]=dict(sha256=hashlib.sha256(text.encode()).hexdigest(),threshold=threshold)
    Path('results/gold/portfolio_v2_build.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))


if __name__=='__main__':main()
