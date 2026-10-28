"""Audit recorded field effects, reconstructing dictionary insertion order.

Kaggle replay JSON sorts object keys. DROP at a full shed and tied sale sorting
depend on insertion order. Recover carried-item order from actual unit actions;
never change amounts, use future information in a policy, or replace its actions.
"""
import contextlib
import copy
import importlib
import io
import json
from collections import Counter
from pathlib import Path

OUT = Path('results/review_v41')


def apply_fields(engine, obs, action):
    farm = copy.deepcopy(obs['farms'][obs['player']])
    private = copy.deepcopy(obs['private'])
    stats = Counter()
    events = []
    commands = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    demand = Counter(c[1] for c in commands if len(c)>1 and c[0]=='PLANT')
    blocked = {crop for crop,n in demand.items() if n>private['seeds'].get(crop,0)}
    for actor, command in enumerate(commands[:len(private['inventories'])]):
        op = command[0]
        x,y = farm['farmer'] if actor==0 else farm['hands'][actor-1]
        tile = farm['tiles'][y][x]
        old_inv = dict(private['inventories'][actor])
        old_shed = dict(private['shed'])
        if op=='PLANT' and command[1] in blocked:
            stats['atomic_plant_rejections'] += 1
            command = ['PASS']
        if op=='FEED' and isinstance(tile,dict) and tile.get('animal') and not tile.get('fed_today') and old_inv.get('WHEAT',0)<=0:
            stats['feed_without_food'] += 1
            events.append(dict(step=obs['step'], actor=actor, event='feed_without_food', xy=[x,y]))
        engine._apply_unit_action(farm,private,actor,command,10,obs['step']//24,24,100)
        inv = private['inventories'][actor]
        if op in ('HARVEST','COLLECT_FERTILIZER'):
            for item,q in inv.items():
                stats['harvested_'+item] += max(0,q-old_inv.get(item,0))
        if op=='PICKUP' and (x,y) in ((4,4),(5,4),(4,5),(5,5)) and len(command)>1:
            q=max(0,int(command[2]) if len(command)>2 else 1)
            missing=max(0,q-max(0,inv.get(command[1],0)-old_inv.get(command[1],0)))
            if missing:
                stats['pickup_shortfall_'+command[1]] += missing
                events.append(dict(step=obs['step'],actor=actor,event='pickup_shortfall',item=command[1],units=missing))
        if op=='DROP' and (x,y) in ((4,4),(5,4),(4,5),(5,5)):
            for item,q in old_inv.items():
                lost=max(0,q-(private['shed'].get(item,0)-old_shed.get(item,0)))
                if lost:
                    stats['discarded_'+item] += lost
                    events.append(dict(step=obs['step'],actor=actor,event='drop_overflow',item=item,units=lost))
    return farm, private, stats, events


def main():
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
        engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    audit=json.loads((OUT/'live_audit.json').read_text(encoding='utf-8'))
    assert audit['complete']
    report=dict(method=__doc__, complete=False, rows=[])
    for submission in audit['submissions']:
        for row in submission['rows']:
            data=json.loads(Path('vendor/review_v41',f"episode-{row['episode']}-replay.json").read_text(encoding='utf-8'))
            seat=row['seat'];tracked=[{}];mismatches=[];counts=Counter();late=Counter();events=[]
            fn=get_last_callable(Path('candidates',submission['candidate']+'.py').read_text(encoding='utf-8'))
            config=dict(data['configuration'],seed=data['info']['seed'])
            for step in range(719):
                obs=dict(data['steps'][step][0]['observation'])
                obs.update(data['steps'][step][seat]['observation']);obs.update(player=seat,step=step)
                private=copy.deepcopy(obs['private'])
                while len(tracked)<len(private['inventories']):tracked.append({})
                assert tracked==private['inventories'], (row['episode'],step,'carried amount mismatch')
                private['inventories']=copy.deepcopy(tracked)
                old=private['shed'];private['shed']={k:old[k] for k in [*engine.PRODUCTS,*engine.ANIMALS] if k in old}
                assert private['shed']==old
                obs['private']=private
                expected=data['steps'][step+1][seat]['action']
                got=fn(obs,config)
                if got!=expected:mismatches.append(dict(step=step,expected=expected,got=got))
                farm,after,stats,new_events=apply_fields(engine,obs,expected)
                counts.update(stats);events.extend(new_events)
                if step>=696:late.update(stats)
                tracked=after['inventories']
                if step%24==23:
                    nxt=data['steps'][step+1][0]['observation']['farms'][seat]
                    for y,tiles in enumerate(farm['tiles']):
                        for x,tile in enumerate(tiles):
                            if not isinstance(tile,dict):continue
                            actual=nxt['tiles'][y][x]
                            if tile.get('animal') and not tile.get('fed_today') and tile.get('consecutive_unfed',0)>=1:
                                assert isinstance(actual,dict) and not actual.get('animal')
                                counts['animal_escapes']+=1
                            if tile.get('kind')=='PLANT' and not tile.get('watered_today') and tile.get('consecutive_unwatered',0)>=1:
                                assert isinstance(actual,dict) and actual.get('kind')=='WEED'
                                counts['raw_thirst_deaths']+=1
                    tracked=[{}]
            result=dict(candidate=submission['candidate'],episode=row['episode'],opponent=row['opponent'],margin=row['margin'],
                original_sorted_json_mismatches=row['mismatch_count'], reconstructed_order_mismatches=mismatches,
                exact_actions=not mismatches, field_counts=dict(counts), last_day_counts=dict(late), events=events,
                note='Raw thirst deaths may include intentional replacements. Pickup shortfall counts units, not failed calls. Actual recorded actions drive all field accounting.')
            report['rows'].append(result)
            (OUT/'physical_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
            print(json.dumps({k:result[k] for k in ('candidate','episode','exact_actions','field_counts')},ensure_ascii=True),flush=True)
    report['complete']=True
    (OUT/'physical_audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
