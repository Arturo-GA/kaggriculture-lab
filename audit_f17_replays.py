"""Re-run recorded actions exactly and account actual money/physical effects on both farms.

This is descriptive replay reconstruction, not a counterfactual strength estimate.
Every final reward must match Kaggle exactly before accounting is accepted.
"""
import argparse,contextlib,copy,gzip,importlib,io,json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
from evaluate import write_json_atomic
from audit_v41_live import farm_summary


def audit(meta):
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    with gzip.open(Path('vendor/live_f16',f"episode-{meta['id']}-replay.json.gz"),'rt',encoding='utf-8') as f:data=json.load(f)
    assert data['module_version']=='1.32.7'
    money=[Counter(),Counter()];units=[Counter(),Counter()];physical=[Counter(),Counter()]
    daily=[[Counter() for _ in range(30)] for _ in range(2)];events=[];owners={};tick=[-1];snapshots={}
    original={n:getattr(engine,n) for n in ['_process_market','_commit_unit','_do_hire','_do_buy_land','_apply_unit_action']}
    def market(state,env):
        expected={id(f):i for i,f in enumerate(state[0].observation.farms)}
        assert all(expected[k]==v for k,v in owners.items())
        owners.clear();owners.update(expected)
        return original['_process_market'](state,env)
    def commit(op,item,price,farm,private,market,shed_capacity=100):
        ok=original['_commit_unit'](op,item,price,farm,private,market,shed_capacity)
        seat=owners[id(farm)]
        if ok:
            key=op+'_'+item;money[seat][key]+=price;units[seat][key]+=1;daily[seat][tick[0]//24][key]+=price
        else:physical[seat]['market_failed_'+op+'_'+item]+=1
        return ok
    def hire(farm,private,board_size,mult=1):
        old=farm['money'];out=original['_do_hire'](farm,private,board_size,mult);seat=owners[id(farm)]
        money[seat]['HIRE']+=old-farm['money'];daily[seat][tick[0]//24]['HIRE']+=old-farm['money'];return out
    def land(farm,board_size):
        old=farm['money'];out=original['_do_buy_land'](farm,board_size);seat=owners[id(farm)]
        money[seat]['BUY_LAND']+=old-farm['money'];daily[seat][tick[0]//24]['BUY_LAND']+=old-farm['money'];return out
    def apply(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity=100):
        if id(farm) not in owners:owners[id(farm)]=len(owners)
        seat=owners[id(farm)];assert seat in (0,1)
        op=action[0] if action else 'EMPTY';physical[seat]['command_'+op]+=1
        pos=engine._farmer_position(farm,idx)
        if pos is None:
            physical[seat]['absent_actor_'+op]+=1
            return original['_apply_unit_action'](farm,private,idx,action,board_size,day,turns_per_day,shed_capacity)
        pos=list(pos);x,y=pos
        before_inv=dict(engine._farmer_inventory(private,idx));before_shed=dict(private['shed']);tile=copy.deepcopy(farm['tiles'][y][x])
        result=original['_apply_unit_action'](farm,private,idx,action,board_size,day,turns_per_day,shed_capacity)
        inv=private['inventories'][idx];after_tile=farm['tiles'][y][x]
        if op in ('HARVEST','COLLECT_FERTILIZER'):
            gain=sum(max(0,v-before_inv.get(k,0)) for k,v in inv.items())
            if not gain:physical[seat]['empty_'+op]+=1
            for item,v in inv.items():physical[seat]['harvested_'+item]+=max(0,v-before_inv.get(item,0))
        if op in ('CARE','FEED','WATER','FERTILIZE','PLANT','DIG') and tile==after_tile:
            physical[seat]['noop_'+op]+=1
        if op=='FEED' and isinstance(tile,dict) and tile.get('animal') and not tile.get('fed_today') and before_inv.get('WHEAT',0)==0:
            physical[seat]['feed_without_food']+=1
            if len(events)<400:events.append(dict(step=tick[0],seat=seat,actor=idx,event='feed_without_food',xy=pos))
        if op=='DROP' and tuple(pos) in ((4,4),(5,4),(4,5),(5,5)):
            for item,q in before_inv.items():
                lost=max(0,q-(private['shed'].get(item,0)-before_shed.get(item,0)))
                if lost:
                    physical[seat]['drop_overflow_'+item]+=lost
                    if len(events)<400:events.append(dict(step=tick[0],seat=seat,actor=idx,event='drop_overflow',item=item,units=lost))
        return result
    engine._process_market=market;engine._commit_unit=commit;engine._do_hire=hire;engine._do_buy_land=land;engine._apply_unit_action=apply
    policies=[]
    for seat in (0,1):
        def recorded(obs,config,seat=seat):
            t=int(obs['step'])
            if t!=tick[0]:owners.clear();tick[0]=t
            if t in (0,144,216,264,288,360,432,504,576,648,672,696,718):
                summary=farm_summary(obs['farms'][seat]);summary['quadrants']=obs['farms'][seat]['unlocked_quadrants']
                summary['shed']=dict(obs['private']['shed']);summary['carried']=dict(sum((Counter(v) for v in obs['private']['inventories']),Counter()))
                summary['ledger']=dict(money[seat]);summary['shops']=list(obs['town']['unlocked_shops'])
                snapshots.setdefault(str(t),{})[seat]=summary
            return data['steps'][t+1][seat]['action'] or {'farmer':['PASS'],'hands':[],'market':[]}
        policies.append(recorded)
    try:
        config=dict(data['configuration'],seed=data['info']['seed'])
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            env=make('kaggriculture',configuration=config,debug=True);last=env.run(policies)[-1]
        rewards=[s['reward'] for s in last]
        assert rewards==data['rewards'],(meta['id'],rewards,data['rewards'])
        assert [s['status'] for s in last]==['DONE','DONE']
        for seat in (0,1):
            net=sum(v if k.startswith('SELL_') else -v for k,v in money[seat].items())
            assert 3000+net==rewards[seat],(meta['id'],seat,net,rewards[seat])
        return dict(meta,seed=data['info']['seed'],recorded_rewards=rewards,reproduced_exactly=True,
            money=list(map(dict,money)),units=list(map(dict,units)),physical=list(map(dict,physical)),
            daily=[[dict(d) for d in days] for days in daily],snapshots=snapshots,events=events)
    finally:
        for n,f in original.items():setattr(engine,n,f)


def main():
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=4);p.add_argument('--limit',type=int,default=0);args=p.parse_args()
    metas=json.loads(Path('results/frontier17/episodes.json').read_text(encoding='utf-8'))
    if args.limit:metas=metas[:args.limit]
    rows=[];out=Path('results/frontier17/replay_audit.json')
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(audit,m) for m in metas]):
            r=future.result();rows.append(r)
            write_json_atomic(out,json.dumps(dict(complete=len(rows)==len(metas),expected=len(metas),rows=rows),indent=2,ensure_ascii=False)+'\n')
            print(len(rows),len(metas),r['id'],r['margin'],'exact',r['reproduced_exactly'],flush=True)


if __name__=='__main__':main()
