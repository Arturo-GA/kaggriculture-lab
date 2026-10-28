"""Exact accounting of F17's first observed loss and the latest public win."""
from pathlib import Path
import json
from research_top100 import download, write
from audit_f17_replays import audit


def main():
    source=json.loads(Path('results/top100_four_0927/selection.json').read_text(encoding='utf-8'))
    rows=source['f17_public'];chosen=[r for r in rows if r['margin']<0]+[next(r for r in rows if r['margin']>0)]
    path=Path('results/frontier18/live_accounting.json')
    out=json.loads(path.read_text(encoding='utf-8')) if path.exists() else dict(complete=False,rows=[])
    for row in chosen:
        if any(r['id']==row['id'] for r in out['rows']):continue
        meta=download(row['id'])
        result=audit(dict(row,raw_path=meta['path'],raw_sha256=meta['sha256']))
        out['rows'].append(result);write(path,out)
        print('reconstructed',row['id'],row['margin'],flush=True)
    out['complete']=True;write(path,out)


if __name__=='__main__':main()
