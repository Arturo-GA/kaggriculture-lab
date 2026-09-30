"""Dated rank200..300 census and outcome-labelled diagnostics of our live agents."""
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import json
from pathlib import Path
from research_four import select
from research_top100 import api,limited,download,write
from research_f16 import plain

ROOT=Path('results/frontier19')


def main():
    initial=json.loads((ROOT/'initial.json').read_text(encoding='utf-8'));path=ROOT/'selection.json'
    if path.exists():s=json.loads(path.read_text(encoding='utf-8'))
    else:
        teams=[dict(team_id=int(k),**v) for k,v in initial['leaderboard'].items() if 200<=v['rank']<=300 or v['rank'] in (1,10,50,100,150)]
        own=[]
        for sid,rs in initial['episodes'].items():
            selected={r['id']:dict(r,submission=int(sid),selection_reason='latest4') for r in rs[:4]}
            groups=[('recent_target_loss',[r for r in rs if r['margin']<0 and r['op_rank'] and 100<=r['op_rank']<=400][:4]),
                    ('recent_close_loss',[r for r in rs if -3000<r['margin']<0][:4]),
                    ('recent_win',[r for r in rs if r['margin']>0][:2])]
            for reason,part in groups:
                for r in part:selected.setdefault(r['id'],dict(r,submission=int(sid),selection_reason=reason))
            own+=list(selected.values())
        s=dict(snapshot_utc=initial['checked_utc'],selection_rule='All ranks200..300 plus ranks1,10,50,100,150; four latest public completed games of best active submission. Own losses deliberately selected for diagnosis, never treated as unbiased strength estimate.',
               target_teams=teams,own=own,teams=[],episodes=[],errors=[],complete=False)
        write(path,s)
    # Our diagnostic episodes are available first; the later census shares the cache.
    found={r['id'] for r in s['episodes']}
    for r in s['own']:
        if r['id'] not in found:
            s['episodes'].append(download(r['id']));found.add(r['id']);write(path,s)
            print('own replay',r['id'],r['margin'],flush=True)
    client=api()
    for tid in (744277,744380,743716,743829,744614):
        p=ROOT/f'topic-{tid}.json'
        if not p.exists():write(p,plain(limited(client.competition_list_topic_messages,'kaggriculture',tid,page_size=100)))
    found={t['team_id'] for t in s['teams']}
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs={pool.submit(select,t,initial['leaderboard']):t for t in s['target_teams'] if t['team_id'] not in found}
        for f in as_completed(jobs):
            t=jobs[f]
            try:s['teams'].append(f.result());print('team',t['rank'],flush=True)
            except Exception as exc:s['errors'].append(dict(stage='select',team=t['team_id'],error=repr(exc)))
            write(path,s)
    ids={r['id'] for t in s['teams'] for r in t['episodes']}|{r['id'] for r in s['own']}
    found={r['id'] for r in s['episodes']}
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs={pool.submit(download,i):i for i in ids-found}
        for f in as_completed(jobs):
            try:s['episodes'].append(f.result());print('replay',len(s['episodes']),'/',len(ids),flush=True)
            except Exception as exc:s['errors'].append(dict(stage='download',episode=jobs[f],error=repr(exc)))
            write(path,s)
    s['complete']=len(s['teams'])==len(s['target_teams']) and len({r['id'] for r in s['episodes']})==len(ids)
    s['finished_utc']=datetime.now(timezone.utc).isoformat();write(path,s)
    print('COMPLETE',s['complete'],len(s['teams']),len(ids),flush=True)


if __name__=='__main__':main()
