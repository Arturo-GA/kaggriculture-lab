"""Realized sale motifs from four public games per team, with diagnostic games excluded."""
import contextlib,copy,gzip,hashlib,importlib,io,json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from research_top100 import write

ROOT=Path('results/frontier19')
ITEMS=('MILK','WOOL','STRAWBERRY','EGG','MELON')

def extract(job):
    team,ep,meta=job
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    raw=gzip.decompress(Path(meta['path']).read_bytes());assert hashlib.sha256(raw).hexdigest()==meta['sha256']
    data=json.loads(raw);seat=ep['seat'];events=[]
    for step in range(719):
        a=data['steps'][step+1][seat]['action'] or {};orders=a.get('market',[])
        selling=[o for o in orders if len(o)>=3 and o[0]=='SELL' and o[1] in ITEMS and int(o[2])>=2]
        if not selling:continue
        obs=data['steps'][step][seat]['observation']
        farm=copy.deepcopy(obs['farms'][seat]);private=copy.deepcopy(obs['private'])
        commands=[a.get('farmer') or ['PASS']]+list(a.get('hands') or [])
        for i,cmd in enumerate(commands):
            engine._apply_unit_action(farm,private,i,cmd,10,step//24,24,100)
        held=dict(private['shed']);volume={}
        for o in selling:
            item=o[1];q=min(max(0,int(held.get(item,0))),int(o[2]));held[item]=held.get(item,0)-q
            volume[item]=volume.get(item,0)+q
        for item,q in volume.items():
            # With these five goods BUY_PRODUCT is invalid. SELL is therefore
            # exactly bounded by stock after physical actions, without knowing
            # the rival's hidden queue. Low-price disposal is not a race signal.
            if q>=2 and obs['market']['prices'][item]>3:events.append([step,ITEMS.index(item),min(255,q)])
    return dict(episode=ep['id'],team_id=team['team_id'],rank=team['rank'],seat=seat,
                shops=data['steps'][719][0]['observation']['town']['unlocked_shops'],events=events)

def main():
    selection=json.loads((ROOT/'selection.json').read_text(encoding='utf-8'));assert selection['complete']
    excluded={r['id'] for r in selection['own']};available={r['id']:r for r in selection['episodes']}
    jobs=[(team,ep,available[ep['id']]) for team in selection['teams'] if 200<=team['rank']<=300 for ep in team['episodes'] if ep['id'] not in excluded]
    rows=[]
    with ProcessPoolExecutor(max_workers=2) as pool:
        for f in as_completed([pool.submit(extract,j) for j in jobs]):
            rows.append(f.result())
            if len(rows)%20==0:print('patterns',len(rows),'/',len(jobs),flush=True)
    rows.sort(key=lambda r:(r['team_id'],r['episode'],r['seat']))
    payload=json.dumps(rows,separators=(',',':'),ensure_ascii=False).encode()
    with (ROOT/'sale_motifs.json.gz').open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as z:z.write(payload)
    write(ROOT/'motif_manifest.json',dict(snapshot_utc=selection['snapshot_utc'],rows=len(rows),teams=len({r['team_id'] for r in rows}),
        excluded_episodes=sorted(excluded),source_sha256={str(k):v['sha256'] for k,v in available.items() if k not in excluded},
        data_sha256=hashlib.sha256(payload).hexdigest(),method='Physical actions simulated on the official engine; SELL quantities clipped by post-physical stock. Only observed history is matched online.'))
    print('COMPLETE',len(rows),flush=True)
if __name__=='__main__':main()
