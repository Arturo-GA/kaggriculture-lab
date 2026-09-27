"""Exact official-engine accounts for a preregistered rank-spaced replay sample."""
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
from audit_f17_replays import audit
from evaluate import write_json_atomic

ROOT=Path('results/top100_0927')
RANKS=(1,3,5,8,10,20,25,29,40,60,80,100)


def main():
    source=json.loads((ROOT/'selection.json').read_text(encoding='utf-8'))
    downloaded={e['id']:e for e in source['episodes']}
    path=ROOT/'accounting.json'
    report=json.loads(path.read_text(encoding='utf-8')) if path.exists() else dict(
        complete=False,selection_ranks=RANKS,selection_rule='Most recent of the two selected games, fixed ranks, no outcome selection.',rows=[])
    done={r['rank'] for r in report['rows']}
    jobs=[]
    for t in source['teams']:
        if t['rank'] not in RANKS or t['rank'] in done or not t['episodes']:
            continue
        e=t['episodes'][0]
        if e['id'] not in downloaded:
            continue
        jobs.append(dict(id=e['id'],rank=t['rank'],team=t['name'],team_id=t['team_id'],seat=e['seat'],
                         agents=e['agents'],raw_path=downloaded[e['id']]['path']))
    with ProcessPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(audit,j) for j in jobs]):
            r=future.result();report['rows'].append(r)
            report['complete']=len(report['rows'])==len(RANKS)
            write_json_atomic(path,json.dumps(report,indent=2,ensure_ascii=False)+'\n')
            print('accounted rank',r['rank'],r['team'],'rewards',r['recorded_rewards'],'exact',r['reproduced_exactly'],flush=True)


if __name__=='__main__':main()
