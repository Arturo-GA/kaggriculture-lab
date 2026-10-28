"""Behavioral fingerprints from public elite replays, without inferring private code."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import statistics


def snapshot(obs,seat):
    farm=obs['farms'][seat]
    tiles=[t for row in farm['tiles'] for t in row if isinstance(t,dict)]
    return dict(cash=farm['money'],workers=len(farm['hands']),land=len(farm['unlocked_quadrants']),
                assets=dict(Counter(t.get('crop') or t.get('animal') or t['kind'] for t in tiles)),
                ripe=sum(t.get('yield_units',0) for t in tiles),
                prices=obs['market']['prices'])


def analyze(data,seat):
    daily=[];fingerprints=[]
    for day in range(30):
        ops=Counter();market=Counter();sell=Counter();buy=Counter();plant=Counter();idle=total=0
        day_actions=[];max_workers=0
        for step in range(day*24,min(719,(day+1)*24)):
            action=data['steps'][step+1][seat]['action'] or {}
            obs=data['steps'][step][seat]['observation']
            cmds=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
            n=1+len(obs['farms'][seat]['hands'])
            max_workers=max(max_workers,n-1)
            cmds=cmds[:n]+[['PASS']] * max(0,n-len(cmds))
            for cmd in cmds:
                op=cmd[0] if cmd else 'PASS';ops[op]+=1;total+=1;idle+=op=='PASS'
                if op=='PLANT' and len(cmd)>1:plant[cmd[1]]+=1
            for order in action.get('market',[]):
                if not order:continue
                market[order[0]]+=1
                if order[0]=='SELL' and len(order)>2:sell[order[1]]+=order[2]
                if order[0].startswith('BUY') and len(order)>2:buy[order[1]]+=order[2]
            day_actions.append(action)
        daily.append(dict(day=day,ops=dict(ops),market=dict(market),sell_requests=dict(sell),
                          buy_requests=dict(buy),plant_requests=dict(plant),idle=idle,total=total,max_workers=max_workers))
        fingerprints.append(hashlib.sha256(json.dumps(day_actions,sort_keys=True).encode()).hexdigest())
    return dict(reward=data['rewards'][seat],
                snapshots={str(s):snapshot(data['steps'][s][seat]['observation'],seat)
                           for s in (144,288,432,576,648,696,719)},
                daily=daily,day_action_hashes=fingerprints)


def main():
    audit=json.loads(Path('results/gold/audit.json').read_text())
    assert audit['complete']
    rows=[]
    for team in audit['selected']:
        for ep in team['episodes']:
            seat=next(a['seat'] for a in ep['agents'] if a['submission_id']==team['submission_id'])
            data=json.loads(Path('vendor/gold',f"episode-{ep['id']}-replay.json").read_text())
            assert data['module_version']=='1.32.7' and len(data['steps'])==720
            rows.append(dict(team_id=team['team_id'],team=team['team_name'],rank=team['rank'],
                             submission_id=team['submission_id'],episode=ep['id'],seat=seat,
                             seed=data['info']['seed'],**analyze(data,seat)))
    report=dict(scope='24 team-episode observations; overlapping duels are not independent. '
                      'Sell/buy/plant counts are requests, not verified completions.',rows=rows)
    Path('results/gold/behavior.json').write_text(json.dumps(report,indent=2)+'\n')
    for team in audit['selected']:
        subset=[r for r in rows if r['team_id']==team['team_id']]
        print(json.dumps(dict(rank=team['rank'],team=team['team_name'],
            mean_cash=statistics.mean(r['reward'] for r in subset),
            assets_day18=[r['snapshots']['432']['assets'] for r in subset],
            workers_day24=[r['daily'][24]['max_workers'] for r in subset],
            late_operations=dict(sum((Counter(d['ops']) for r in subset for d in r['daily'][24:]),Counter())))),flush=True)


if __name__=='__main__':main()
