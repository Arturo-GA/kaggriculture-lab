from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse
import json
from pathlib import Path

from evaluate_fast import game


def collect(job):
    seed,opponent,seat=job
    rows=[game((c,opponent,seed,seat),capture_frontier=True) for c in ('frontier_control','frontier_force')]
    assert rows[0]['prefix_sha256']==rows[1]['prefix_sha256']
    assert rows[0]['decision_features']==rows[1]['decision_features']
    assert all(r['telemetry']['frontier_decisions']==1 for r in rows)
    return dict(seed=seed,opponent=opponent,seat=seat,features=rows[0]['decision_features'],
                prefix_sha256=rows[0]['prefix_sha256'],options=rows)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--split',choices=['train','selection'],required=True)
    parser.add_argument('--workers',type=int,default=4);args=parser.parse_args()
    plan=json.loads(Path('results/gold/frontier_plan.json').read_text())
    jobs=[(s,o,p) for s in plan[args.split+'_seeds'] for o in plan['opponents'] for p in (0,1)]
    out=Path('results/gold/frontier_'+args.split+'.jsonl');assert not out.exists()
    with out.open('w',encoding='utf-8') as stream,ProcessPoolExecutor(max_workers=args.workers) as pool:
        count=0
        for f in as_completed([pool.submit(collect,j) for j in jobs]):
            row=f.result();stream.write(json.dumps(row,separators=(',',':'))+'\n');stream.flush();count+=1
            print(f"{args.split} {count}/{len(jobs)} {row['seed']} {row['opponent']} margin_delta={row['options'][1]['margin']-row['options'][0]['margin']}",flush=True)
    out.with_suffix('.meta.json').write_text(json.dumps(dict(complete=True,contexts=len(jobs),games=len(jobs)*2)))


if __name__=='__main__':main()
