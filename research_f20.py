"""Read-only, dated audit of all available PUBLIC losses of the two F19 releases."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import argparse, json
from pathlib import Path
from live_report import leaderboard
from research_top100 import api, limited, download, write
from research_four import public_episodes
from research_f16 import plain

ROOT = Path('results/frontier20')
IDS = (56714342, 56714336)

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['snapshot','download']);args=p.parse_args()
    ROOT.mkdir(parents=True,exist_ok=True)
    if args.mode=='snapshot':
        assert not (ROOT/'initial.json').exists(), 'Preserve the dated initial snapshot'
        client=api();teams,cuts=leaderboard(client)
        ranked=sorted(teams.values(),key=lambda t:t['rank'])
        n=len(ranked); silver=n//20 if n>=1000 else 50
        report=dict(checked_utc=datetime.now(timezone.utc).isoformat(),leaderboard=teams,
                    own=teams.get('16639155'),cuts={str(r):next((v for v in ranked if v['rank']==r),None) for r in (100,200,300,350,400,silver)},
                    medal_rule='Kaggle official progression: >=1000 teams silver top5%, rounded down; final eligibility/ranks govern.',silver_rank=silver,
                    active=plain(limited(client.competition_team_submissions,16639155)),
                    limits=plain(limited(client.competition_get_submission_limits,'kaggriculture')),episodes={})
        for sid in IDS:report['episodes'][str(sid)]=public_episodes(client,sid,teams)
        write(ROOT/'initial.json',report)
        print(json.dumps({k:v for k,v in report.items() if k not in ('leaderboard','episodes')},indent=2))
        for sid,rs in report['episodes'].items():
            print(sid,'public',len(rs),'WLT',[sum((r['margin']>0 if o=='W' else r['margin']<0 if o=='L' else r['margin']==0) for r in rs) for o in 'WLT'])
            print('Latest four:',[(r['id'],r['margin'],r['op_rank']) for r in rs[:4]])
        for page in (1,2):
            topics=plain(limited(client.competition_list_topics,'kaggriculture',sort_by='recent',page=page))
            write(ROOT/f'topics-{page}.json',topics);print('TOPICS',json.dumps(topics,ensure_ascii=False))
        timeline=plain(limited(client.competition_list_pages,'kaggriculture',page_name='timeline'))
        write(ROOT/'timeline.json',timeline)
    else:
        initial=json.loads((ROOT/'initial.json').read_text(encoding='utf-8'))
        own=[dict(r,submission=int(sid)) for sid,rs in initial['episodes'].items() for r in rs if r['margin']<0]
        path=ROOT/'selection.json'
        s=json.loads(path.read_text(encoding='utf-8')) if path.exists() else dict(snapshot_utc=initial['checked_utc'],selection_rule='Every completed public defeat exposed by the API at snapshot time for exactly the latest two F19 submissions. Outcome-selected diagnostics, not a strength estimate.',own=own,episodes=[],errors=[],complete=False)
        ids={r['id'] for r in own};found={r['id'] for r in s['episodes']}
        with ThreadPoolExecutor(max_workers=3) as pool:
            jobs={pool.submit(download,eid):eid for eid in ids-found}
            for future in as_completed(jobs):
                try:s['episodes'].append(future.result());print('Downloaded',len(s['episodes']),'/',len(ids),flush=True)
                except Exception as exc:s['errors'].append(dict(id=jobs[future],error=repr(exc)))
                write(path,s)
        s['complete']={r['id'] for r in s['episodes']}==ids;s['finished_utc']=datetime.now(timezone.utc).isoformat();write(path,s)
        print('COMPLETE',s['complete'],'appearances',len(own),'unique losses',len(ids))

if __name__=='__main__':main()
