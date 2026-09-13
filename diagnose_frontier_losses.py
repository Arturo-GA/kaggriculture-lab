"""Explain terminal losses using unit-effect accounting, not request counts."""
import contextlib
import copy
import importlib
import io
import json
from pathlib import Path
from collections import Counter

import accelerator


def game(seed,candidate='frontier',opponent='ml_critic'):
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
        engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    policies=[get_last_callable(Path('candidates',n+'.py').read_text(encoding='utf-8')) for n in (candidate,opponent)]
    env=accelerator.load().Game(seed);trace=[];units=[Counter(),Counter()];requests=[Counter(),Counter()]
    noops=[Counter(),Counter()];initial=None
    while not env.done:
        obs=[env.observe(s) for s in (0,1)]
        actions=[f(o,{}) for f,o in zip(policies,obs)]
        if env.step_count>=696:
            if initial is None:initial=copy.deepcopy(obs)
            events=[]
            for s in (0,1):
                farm=copy.deepcopy(obs[s]['farms'][s]);private=copy.deepcopy(obs[s]['private'])
                commands=[actions[s].get('farmer',['PASS']),*actions[s].get('hands',[])]
                for i,cmd in enumerate(commands):
                    if i>=len(private['inventories']):break
                    before=copy.deepcopy((farm,private));inv=dict(private['inventories'][i])
                    requests[s][cmd[0]]+=1
                    engine._apply_unit_action(farm,private,i,cmd,10,29,24,100)
                    changed=before!=(farm,private)
                    if not changed and cmd[0] not in ('PASS',):noops[s][cmd[0]]+=1
                    if cmd[0] in ('HARVEST','COLLECT_FERTILIZER'):
                        for item,q in private['inventories'][i].items():units[s][item]+=max(0,q-inv.get(item,0))
                    if cmd[0]=='DROP':
                        lost=sum(inv.values())-sum(private['shed'].values())+sum(before[1]['shed'].values())
                        if lost:units[s]['discarded_overflow']+=lost
                    events.append(dict(seat=s,actor=i,command=cmd,changed=changed))
            trace.append(dict(step=env.step_count,actions=actions,events=events,
                              money=[o['farms'][s]['money'] for s,o in enumerate(obs)],
                              shed=[o['private']['shed'] for o in obs]))
        env.step(*actions)
    final=[env.observe(s) for s in (0,1)]
    plans=policies[0].__globals__.get('_AU_STATE',{}).get(0,{})
    remaining=[]
    for s in (0,1):
        ripe=Counter()
        for row in final[s]['farms'][s]['tiles']:
            for t in row:
                if not isinstance(t,dict):continue
                item=t.get('crop') or {'COW':'MILK','SHEEP':'WOOL','GOOSE':'EGG'}.get(t.get('animal'))
                if item:ripe[item]+=t.get('yield_units',0)
                if t.get('fertilizer_available'):ripe['FERTILIZER']+=1
        remaining.append(dict(ripe))
    return dict(seed=seed,candidate=candidate,opponent=opponent,rewards=[env.reward(s) for s in (0,1)],
                initial=initial,final=final,units=list(map(dict,units)),requests=list(map(dict,requests)),
                noops=list(map(dict,noops)),remaining=remaining,plans=plans,trace=trace)


def main():
    out=Path('results/frontier2');out.mkdir(exist_ok=True)
    for seed in (87001,87002,87003,87004,85003):
        result=game(seed);(out/f'diagnosis_{seed}.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ['seed','rewards','units','requests','noops','remaining']},indent=1),flush=True)


if __name__=='__main__':main()
