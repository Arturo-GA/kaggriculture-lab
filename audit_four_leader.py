"""Reconstruct all four selected leader games, including losses, without outcome filtering."""
import json
from pathlib import Path
from audit_f17_replays import audit
from research_top100 import write

ROOT=Path('results/top100_four_0927')


def main():
    s=json.loads((ROOT/'selection.json').read_text(encoding='utf-8'));assert len(s['teams'])==100
    leader=next(t for t in s['teams'] if t['rank']==1);metas={r['id']:r for r in s['episodes']}
    assert all(e['id'] in metas for e in leader['episodes'])
    path=ROOT/'leader_accounting.json'
    out=json.loads(path.read_text(encoding='utf-8')) if path.exists() else dict(complete=False,rows=[])
    for e in leader['episodes']:
        if any(r['id']==e['id'] for r in out['rows']):continue
        meta=metas[e['id']]
        r=audit(dict(e,raw_path=meta['path'],raw_sha256=meta['sha256'],rank=1,team=leader['name'],submission=leader['submission']))
        out['rows'].append(r);write(path,out)
        print('exact leader replay',r['id'],r['margin'],flush=True)
    out['complete']=True;write(path,out)


if __name__=='__main__':main()
