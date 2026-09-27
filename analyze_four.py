"""Check whether top100 patterns recur across four games, not just the latest two."""
from collections import Counter
import gzip, hashlib, json
from pathlib import Path
from statistics import median
from analyze_top100 import features, ANIMALS, CROPS
from research_top100 import write

ROOT=Path('results/top100_four_0927')


def summary(rows):
    return dict(player_games=len(rows),teams=len({r['team_id'] for r in rows}),wins=sum(r['margin']>0 for r in rows),
        hands=median(r['peak_hands_midgame'] for r in rows),
        animals=median(sum(r['snapshots']['288']['layout'].get(a,0) for a in ANIMALS) for r in rows),
        strawberries=median(r['snapshots']['288']['layout'].get('STRAWBERRY',0) for r in rows),
        sw=median(r['first_land_step']['SW'] for r in rows if 'SW' in r['first_land_step']),
        se=sum('SE' in r['first_land_step'] for r in rows),
        tomato_by288=sum(any(p['crop']=='TOMATO' and p['step']<=288 for p in r['plantings']) for r in rows),
        carrot_by288=sum(any(p['crop']=='CARROT' and p['step']<=288 for p in r['plantings']) for r in rows),
        heavy_input=sum(heavy(r) for r in rows),
        final_leftovers=sum(sum(r['snapshots']['719']['shed'].values())+sum(r['snapshots']['719']['carried'].values())>0 for r in rows))


def heavy(r):
    return sum(r['same_turn_buy_sell'].get(i+'_turns',0) for i in ('WHEAT','FERTILIZER'))>=10


def main():
    s=json.loads((ROOT/'selection.json').read_text(encoding='utf-8'));assert s['complete']
    metas={e['id']:e for e in s['episodes']};rows=[];own=[]
    jobs=[(t,e,i) for t in sorted(s['teams'],key=lambda t:t['rank']) for i,e in enumerate(t['episodes'])]
    jobs += [(dict(team_id=16639155,name='F17',rank=s['own']['rank'],submission=56615489,score=None),e,i)
             for i,e in enumerate(s['f17_public'])]
    for t,e,i in jobs:
        m=metas[e['id']];blob=gzip.decompress(Path(m['path']).read_bytes())
        assert hashlib.sha256(blob).hexdigest()==m['sha256'];data=json.loads(blob)
        assert data['rewards'][e['seat']]==e['my']
        row=dict(team_id=t['team_id'],team=t['name'],rank=t['rank'],submission=t['submission'],
                 rating=t['score'],episode=e['id'],seat=e['seat'],recency_index=i,created=e['created'],
                 opponent_rank=e['op_rank'],opponent_score=e['op_score'],**features(data,e['seat']))
        (own if t['team_id']==16639155 else rows).append(row)
        if len(rows)%40==0:print('features',len(rows),len(own),flush=True)
    assert len(rows)==400 and all(n==4 for n in Counter(r['team_id'] for r in rows).values())
    features_blob=json.dumps(dict(rows=rows,own=own),ensure_ascii=False,separators=(',',':')).encode()
    (ROOT/'features.json.gz').write_bytes(gzip.compress(features_blob,mtime=0))
    patterns={
        'SE':lambda r:'SE' in r['first_land_step'],
        'SW_before_day10':lambda r:r['first_land_step'].get('SW',9999)<240,
        'early_tomato':lambda r:any(p['crop']=='TOMATO' and p['step']<=288 for p in r['plantings']),
        'early_carrot':lambda r:any(p['crop']=='CARROT' and p['step']<=288 for p in r['plantings']),
        'heavy_input':heavy,
        'at_least_20_animals':lambda r:sum(r['snapshots']['288']['layout'].get(a,0) for a in ANIMALS)>=20,
        'at_least_12_hands':lambda r:r['peak_hands_midgame']>=12,
    }
    stability={k:dict(Counter(sum(fn(r) for r in rows if r['team_id']==tid) for tid in {r['team_id'] for r in rows}))
               for k,fn in patterns.items()}
    team_profiles=[]
    for t in sorted(s['teams'],key=lambda t:t['rank']):
        rs=[r for r in rows if r['team_id']==t['team_id']]
        team_profiles.append(dict(team=t['name'],rank=t['rank'],submission=t['submission'],
            pattern_counts={k:sum(fn(r) for r in rs) for k,fn in patterns.items()},
            games=[dict(episode=r['episode'],margin=r['margin'],shops=r['snapshots']['288']['shops'],
                        hands=r['peak_hands_midgame'],layout288=r['snapshots']['288']['layout'],
                        first_land=r['first_land_step'],input_cycles=r['same_turn_buy_sell'],
                        plantings=dict(Counter(p['crop'] for p in r['plantings']))) for r in rs]))
    old=json.loads(Path('results/top100_0927/selection.json').read_text(encoding='utf-8'))
    old_ids={e['id'] for e in old['episodes']}
    info=dict(snapshot_utc=s['checked_utc'],complete=True,player_games=len(rows),unique_top100_games=len({r['episode'] for r in rows}),
        independent_seeds=len({r['seed'] for r in rows}),top100_cut=s['leaderboard'][-1],
        prior_two_census_overlap_games=len(old_ids & {r['episode'] for r in rows}),
        all_four=summary(rows),latest_two=summary([r for r in rows if r['recency_index']<2]),
        preceding_two=summary([r for r in rows if r['recency_index']>=2]),
        top10=summary([r for r in rows if r['rank']<=10]),own=summary(own),stability_team_counts=stability,
        own_public_wlt=[sum(r['margin']>0 for r in own),sum(r['margin']<0 for r in own),sum(r['margin']==0 for r in own)],
        caveats=['Four games do not identify a private algorithm or establish causality.',
                 'Selection uses one best active agent per team, current ranks, and no outcome filter.',
                 'Latest-two versus preceding-two comparisons hold team and submission fixed, not world or rival.',
                 'Same-turn orders are requested quantities, not measured profit.',
                 'Team rating belongs to its best active submission, which may differ from the observed rival.'])
    write(ROOT/'summary.json',info);write(ROOT/'profiles.json',team_profiles)
    write(ROOT/'verification.json',dict(verified=True,engine='1.32.7',four_per_team=True,
        feature_uncompressed_sha256=hashlib.sha256(features_blob).hexdigest(),
        files={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('selection.json','features.json.gz','profiles.json','summary.json')}))
    print(json.dumps(info,indent=2,ensure_ascii=False))


if __name__=='__main__':main()
