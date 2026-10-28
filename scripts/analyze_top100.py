"""Observable economic signatures; submitted orders are not treated as realized revenue."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
from statistics import median

from audit_v41_live import farm_summary

ROOT = Path('results/top100_0927')
SNAPSHOTS = (144, 216, 240, 264, 288, 360, 432, 480, 576, 648, 672, 696, 719)
ANIMALS = ('GOOSE', 'COW', 'SHEEP')
CROPS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON')


def features(data, seat):
    snapshots = {}
    seen_plants, seen_animals, first_land = set(), set(), {}
    plantings, placements = [], []
    commands, orders, cycles = Counter(), Counter(), Counter()
    daily_hands = [0]*30
    last_ops = {}
    sell_phases = Counter()
    for t, frame in enumerate(data['steps']):
        obs = frame[0]['observation']
        farm = obs['farms'][seat]
        own = frame[seat]['observation']
        shops = list(obs['town']['unlocked_shops'])
        daily_hands[t//24] = max(daily_hands[t//24], len(farm['hands']))
        for land in farm['unlocked_quadrants']:
            first_land.setdefault(land, t)
        for y, row in enumerate(farm['tiles']):
            for x, tile in enumerate(row):
                if not isinstance(tile, dict):
                    continue
                if tile.get('crop'):
                    key = (x, y, tile['crop'], tile['planted_day'])
                    if key not in seen_plants:
                        seen_plants.add(key)
                        plantings.append(dict(step=t, xy=[x,y], crop=tile['crop'], planted_day=tile['planted_day'],
                                              shops=shops, price=obs['market']['prices'].get(tile['crop'])))
                if tile.get('animal'):
                    key = (x, y, tile['animal'], tile['placed_day'])
                    if key not in seen_animals:
                        seen_animals.add(key)
                        placements.append(dict(step=t, xy=[x,y], animal=tile['animal'], placed_day=tile['placed_day'], shops=shops))
        if t in SNAPSHOTS:
            snap = farm_summary(farm)
            snap.update(quadrants=farm['unlocked_quadrants'], shops=shops,
                        prices=obs['market']['prices'], shed=own['private']['shed'],
                        carried=dict(sum((Counter(inv) for inv in own['private']['inventories']), Counter())))
            snapshots[str(t)] = snap
        if t == 719:
            continue
        action = data['steps'][t+1][seat]['action'] or {}
        for command in [action.get('farmer', []), *action.get('hands', [])]:
            if command:
                commands[command[0]] += 1
                last_ops[command[0]] = t
        quantities = Counter()
        for order in action.get('market', []):
            if len(order) >= 3 and order[0] in ('BUY_PRODUCT', 'BUY_SEED', 'BUY_ANIMAL', 'SELL'):
                quantities[(order[0], order[1])] += int(order[2])
                orders[order[0]+'_'+order[1]] += int(order[2])
                if order[0] == 'SELL':
                    sell_phases[str(t % 4)] += 1
        for item in ('WHEAT', 'FERTILIZER', *CROPS[1:], 'MILK', 'WOOL', 'EGG'):
            if quantities[('BUY_PRODUCT', item)] and quantities[('SELL', item)]:
                cycles[item+'_turns'] += 1
                cycles[item+'_units'] += min(quantities[('BUY_PRODUCT', item)], quantities[('SELL', item)])
    return dict(rewards=data['rewards'], margin=data['rewards'][seat]-data['rewards'][1-seat],
                seed=data['info']['seed'], snapshots=snapshots, first_land_step=first_land,
                daily_peak_hands=daily_hands, peak_hands_midgame=median(daily_hands[10:27]),
                plantings=plantings, placements=placements, physical_commands=dict(commands),
                last_command_step=last_ops, requested_trade_units=dict(orders),
                same_turn_buy_sell=dict(cycles), sell_order_phases=dict(sell_phases))


def main():
    source = json.loads((ROOT/'selection.json').read_text(encoding='utf-8'))
    available = {e['id']:e for e in source['episodes']}
    rows = []
    for team in sorted(source['teams'], key=lambda t:t['rank']):
        for ep in team['episodes']:
            if ep['id'] not in available:
                continue
            meta = available[ep['id']]
            blob = gzip.decompress(Path(meta['path']).read_bytes())
            assert hashlib.sha256(blob).hexdigest() == meta['sha256']
            data = json.loads(blob)
            row = dict(team_id=team['team_id'], team=team['name'], rank=team['rank'],
                       rating_at_selection=team['score'], submission=team['submission'],
                       episode=ep['id'], seat=ep['seat'], created=ep['created'],
                       **features(data, ep['seat']))
            rows.append(row)
    summary = []
    for lo, hi in [(1,100),(1,10),(11,30),(31,60),(61,100)]:
        part = [r for r in rows if lo <= r['rank'] <= hi]
        if not part:
            continue
        at = lambda r:r['snapshots']['288']
        summary.append(dict(rank_band=[lo,hi],team_count=len({r['team_id'] for r in part}),player_games=len(part),
            wins=sum(r['margin']>0 for r in part),ties=sum(r['margin']==0 for r in part),
            midgame_peak_hands_median=median(r['peak_hands_midgame'] for r in part),
            se_by_step288=sum(r['first_land_step'].get('SE',9999)<=288 for r in part),
            any_se=sum('SE' in r['first_land_step'] for r in part),
            animals_step288_median=median(sum(at(r)['layout'].get(a,0) for a in ANIMALS) for r in part),
            crops_step288_median={c:median(at(r)['layout'].get(c,0) for r in part) for c in CROPS},
            tomato_by_step288=sum(any(p['crop']=='TOMATO' and p['step']<=288 for p in r['plantings']) for r in part),
            carrot_by_step288=sum(any(p['crop']=='CARROT' and p['step']<=288 for p in r['plantings']) for r in part),
            late_melon_planting=sum(any(p['crop']=='MELON' and 288<=p['step']<=480 for p in r['plantings']) for r in part),
            input_roundtrip_games=sum(bool(r['same_turn_buy_sell'].get('WHEAT_turns',0) or r['same_turn_buy_sell'].get('FERTILIZER_turns',0)) for r in part)))
    report = dict(complete=source['complete'], snapshot_utc=source['checked_utc'],
                  unique_games=len({r['episode'] for r in rows}), player_games=len(rows),
                  note='Descriptive census. Two recent games per best active submission; matched opponents and shops differ. No causal claim or inferred private code.',
                  bands=summary, rows=rows)
    (ROOT/'features.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2,ensure_ascii=False))


if __name__ == '__main__':
    main()
