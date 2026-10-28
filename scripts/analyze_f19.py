"""Dated public replay evidence; exact own-game ledgers before policy changes."""
import argparse,gzip,hashlib,json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from collections import Counter
from statistics import median
from analyze_top100 import features
from audit_f17_replays import audit
from research_top100 import write

ROOT=Path('results/frontier19')

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['own','census']);args=p.parse_args()
    selection=json.loads((ROOT/'selection.json').read_text(encoding='utf-8'))
    available={r['id']:r for r in selection['episodes']}
    if args.mode=='own':
        out=ROOT/'own_audit.json';rows=json.loads(out.read_text(encoding='utf-8'))['rows'] if out.exists() else []
        found={r['id'] for r in rows}
        metas=[dict(r,raw_path=available[r['id']]['path']) for r in selection['own'] if r['id'] not in found]
        with ProcessPoolExecutor(max_workers=3) as pool:
            for f in as_completed([pool.submit(audit,m) for m in metas]):
                row=f.result();rows.append(row)
                write(out,dict(expected=len(selection['own']),complete=len(rows)==len(selection['own']),rows=rows))
                print('audit',len(rows),row['id'],row['margin'],flush=True)
    else:
        assert selection['complete']
        rows=[]
        for t in selection['teams']:
            for ep in t['episodes']:
                meta=available[ep['id']];raw=gzip.decompress(Path(meta['path']).read_bytes())
                assert hashlib.sha256(raw).hexdigest()==meta['sha256']
                rows.append(dict(team=t['name'],rank=t['rank'],team_id=t['team_id'],episode=ep['id'],seat=ep['seat'],**features(json.loads(raw),ep['seat'])))
        with gzip.GzipFile(filename=str(ROOT/'features.json.gz'),mode='wb',mtime=0) as f:f.write(json.dumps(rows,ensure_ascii=False).encode())
        part=[r for r in rows if 200<=r['rank']<=300]
        summary=dict(snapshot_utc=selection['snapshot_utc'],team_count=len({r['team_id'] for r in part}),appearances=len(part),unique_games=len({r['episode'] for r in part}),
            mean_margin=sum(r['margin'] for r in part)/len(part),median_hands=median(r['peak_hands_midgame'] for r in part),
            median_layout={c:median(r['snapshots']['288']['layout'].get(c,0) for r in part) for c in ('WHEAT','CARROT','STRAWBERRY','TOMATO','GOOSE','COW','SHEEP')},
            sw_step_median=median(r['first_land_step'].get('SW',720) for r in part),
            se_games=sum('SE' in r['first_land_step'] for r in part),input_roundtrip_games=sum(bool(r['same_turn_buy_sell'].get('WHEAT_turns',0) or r['same_turn_buy_sell'].get('FERTILIZER_turns',0)) for r in part))
        write(ROOT/'census_summary.json',summary);print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
