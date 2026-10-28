"""Coherent production-prefix families from the dated four-game census."""
import gzip,hashlib,json
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor,as_completed
from statistics import median
from research_top100 import write

ROOT=Path('results/frontier19')
def record(job):
    team,ep,path=job;data=json.loads(gzip.decompress(Path(path).read_bytes()));seat=ep['seat']
    actions=[data['steps'][t+1][seat]['action'] or {'farmer':['PASS'],'hands':[],'market':[]} for t in range(719)]
    prefix=[]
    for t,a in enumerate(actions[:144]):
        hires=len(data['steps'][t+1][0]['observation']['farms'][seat]['hands'])-len(data['steps'][t][0]['observation']['farms'][seat]['hands']) if t%24!=23 else 0
        prefix.append([a.get('farmer'),a.get('hands'),hires])
    farm=data['steps'][144][0]['observation']['farms'][seat]
    signature=[[(tile.get('kind'),tile.get('animal'),tile.get('crop'),tile.get('placed_day'),tile.get('planted_day')) if isinstance(tile,dict) else tile for tile in row] for row in farm['tiles']]
    key=hashlib.sha256(json.dumps([prefix,signature],sort_keys=True).encode()).hexdigest()
    sw=next((t for t,f in enumerate(data['steps']) if 'SW' in f[0]['observation']['farms'][seat]['unlocked_quadrants']),720)
    strawberry=sum(isinstance(t,dict) and t.get('crop')=='STRAWBERRY' for row in data['steps'][288][0]['observation']['farms'][seat]['tiles'] for t in row)
    return dict(key=key,episode=ep['id'],seat=seat,team=team['team_id'],rank=team['rank'],shops=data['steps'][144][0]['observation']['town']['unlocked_shops'][:2],sw=sw,strawberry=strawberry,actions=actions)

def main():
    selection=json.loads((ROOT/'selection.json').read_text(encoding='utf-8'));excluded={r['id'] for r in selection['own']};available={r['id']:r['path'] for r in selection['episodes']}
    jobs=[(team,ep,available[ep['id']]) for team in selection['teams'] for ep in team['episodes'] if ep['id'] not in excluded]
    groups=defaultdict(list);count=0
    with ProcessPoolExecutor(max_workers=2) as pool:
        for f in as_completed([pool.submit(record,j) for j in jobs]):
            row=f.result();groups[row['key']].append(row);count+=1
            if count%40==0:print('routes',count,flush=True)
    stats=[]
    for key,rows in groups.items():
        stats.append(dict(key=key,count=len(rows),teams=len({r['team'] for r in rows}),sw=median(r['sw'] for r in rows),strawberry=median(r['strawberry'] for r in rows),ranks=sorted({r['rank'] for r in rows})))
    stats.sort(key=lambda r:-r['count']);write(ROOT/'production_families.json',stats)
    viable=[r for r in stats if r['count']>=4 and r['sw']<=240 and r['strawberry']<30]
    assert viable,'No coherent early-production family; do not splice incompatible routes.'
    selected=viable[0];rows=sorted(groups[selected['key']],key=lambda r:(r['rank'],r['episode'],r['seat']))
    raw=json.dumps(rows,separators=(',',':')).encode()
    with (ROOT/'portfolio_records.json.gz').open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as z:z.write(raw)
    write(ROOT/'portfolio_manifest.json',dict(family=selected,excluded_episodes=sorted(excluded),data_sha256=hashlib.sha256(raw).hexdigest(),
          sources=[{k:r[k] for k in ('episode','seat','team','rank','shops','sw','strawberry')} for r in rows],rule='Largest coherent first-six-day physical-action and realized-hire family with median SW <=240 and <30 strawberries. No outcomes used in family selection.'))
    print(json.dumps(stats[:12],indent=2));print('SELECTED',selected)
if __name__=='__main__':main()
