"""Two official-engine case studies with actual transactions and field effects."""
import contextlib
import copy
import importlib
import io
import json
from collections import Counter
from pathlib import Path

from audit_v41_live import farm_summary
from diagnose_v41_replays import apply_fields


def game(candidate, seed=92001):
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
        engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    names=[candidate,'v41_review']
    functions=[get_last_callable(Path('candidates',n+'.py').read_text(encoding='utf-8')) for n in names]
    physical=[Counter(),Counter()];money=[Counter(),Counter()];transactions=[Counter(),Counter()]
    snapshots={};opening=[];owners={};current_step=[0]
    original={k:getattr(engine,k) for k in ('_process_market','_commit_unit','_do_hire','_do_buy_land')}
    def market(state,env):
        owners.clear();owners.update({id(f):i for i,f in enumerate(state[0].observation.farms)})
        return original['_process_market'](state,env)
    def commit(op,item,price,farm,private,market,shed_capacity=100):
        result=original['_commit_unit'](op,item,price,farm,private,market,shed_capacity)
        if result:
            seat=owners[id(farm)];money[seat][op+'_'+item]+=price;transactions[seat][op+'_'+item]+=1
        return result
    def hire(farm,private,board_size,mult=1):
        before=farm['money'];result=original['_do_hire'](farm,private,board_size,mult)
        money[owners[id(farm)]]['HIRE']+=before-farm['money']
        return result
    def land(farm,board_size):
        before=farm['money'];result=original['_do_buy_land'](farm,board_size)
        money[owners[id(farm)]]['BUY_LAND']+=before-farm['money']
        return result
    engine._process_market=market;engine._commit_unit=commit;engine._do_hire=hire;engine._do_buy_land=land
    policies=[]
    for seat,fn in enumerate(functions):
        def measured(obs,config,seat=seat,fn=fn):
            step=int(obs['step']);current_step[0]=step
            if step in (0,1,2,3,12,24,25,144,288,336,432,576,648,696,718):
                snapshots.setdefault(str(step),{})[seat]=dict(farm=farm_summary(obs['farms'][seat]),shed=copy.deepcopy(obs['private']['shed']),seeds=copy.deepcopy(obs['private']['seeds']),prices=dict(obs['market']['prices']),ledger=dict(money[seat]))
            action=fn(obs,config)
            _,_,stats,_=apply_fields(engine,obs,action);physical[seat].update(stats)
            if step<25:opening.append(dict(step=step,seat=seat,action=copy.deepcopy(action)))
            return action
        policies.append(measured)
    try:
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            env=make('kaggriculture',configuration={'episodeSteps':720,'seed':seed},debug=True)
            final=env.run(policies)[-1]
        assert len(env.steps)==720 and all(r['status']=='DONE' for r in final)
        rewards=[r['reward'] for r in final]
        for seat in (0,1):
            income=sum(v for k,v in money[seat].items() if k.startswith('SELL_'))
            expense=sum(v for k,v in money[seat].items() if not k.startswith('SELL_'))
            assert 3000+income-expense==rewards[seat]
        return dict(engine='official 1.32.7',candidate=candidate,opponent='v41_review',seed=seed,seat=0,rewards=rewards,
            margin=rewards[0]-rewards[1],snapshots=snapshots,actual_money=list(map(dict,money)),actual_transaction_units=list(map(dict,transactions)),
            field_counts=list(map(dict,physical)),telemetry=[dict(getattr(f,'telemetry',{})) for f in functions],opening=opening,
            note='Two explanatory cases from the frozen official panel; not an independent statistical sample.')
    finally:
        for key,fn in original.items():setattr(engine,key,fn)


if __name__=='__main__':
    for candidate in ('matched6','frontier2_early'):
        result=game(candidate)
        Path('results/review_v41',candidate+'_economy.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:result[k] for k in ('candidate','rewards','actual_money','field_counts')},ensure_ascii=True),flush=True)
