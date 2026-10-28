import contextlib
import io
import json
import sys
from pathlib import Path

import accelerator


def main():
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
    names=[sys.argv[1] if len(sys.argv)>1 else 'auction_risk','ml_critic']
    agents=[get_last_callable(Path('candidates',n+'.py').read_text(encoding='utf-8')) for n in names]
    env=accelerator.load().Game(81001);rows=[]
    while not env.done:
        obs=[env.observe(i) for i in range(2)]
        actions=[f(o,{}) for f,o in zip(agents,obs)]
        if env.step_count>=696:
            rows.append(dict(step=env.step_count,actions=actions,
                             money=[o['farms'][i]['money'] for i,o in enumerate(obs)],
                             workers=[len(o['farms'][i]['hands']) for i,o in enumerate(obs)],
                             private=[o['private'] for o in obs]))
        env.step(*actions)
    result=dict(names=names,rows=rows,final=[env.observe(i) for i in range(2)],
                plans=agents[0].__globals__['_AU_STATE'],rewards=[env.reward(i) for i in range(2)])
    Path('results/gold/auction_diagnosis.json').write_text(json.dumps(result,indent=2)+'\n')
    print('rewards',result['rewards'],'start',rows[0]['money'])
    for i,n in enumerate(names):
        o=result['final'][i]
        print(n,'shed',o['private']['shed'],'carried',o['private']['inventories'])
    st=result['plans'][0]
    print('plan',{k:v for k,v in st.items() if k not in ('plans','hire_steps')})
    print('portfolio',agents[0].__globals__.get('_PF_STATE'))


if __name__=='__main__':main()
