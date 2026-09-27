"""Read current public Kaggle metadata and save a bounded research snapshot."""
from datetime import datetime,timezone
from pathlib import Path
import json
from kaggle.api.kaggle_api_extended import KaggleApi
from live_report import leaderboard


def plain(x):
    if x is None or isinstance(x,(str,int,float,bool)):return x
    if isinstance(x,(list,tuple)):return [plain(v) for v in x]
    if isinstance(x,dict):return {k:plain(v) for k,v in x.items()}
    if isinstance(x,datetime):return x.isoformat()
    if hasattr(x,'__dict__'):return {k.lstrip('_'):plain(v) for k,v in vars(x).items() if not k.startswith('__')}
    return str(x)


def main():
    api=KaggleApi();api.authenticate()
    folder=Path('vendor/research_f16');folder.mkdir(parents=True,exist_ok=True)
    kernels=plain(api.kernels_list(search='kaggriculture',sort_by='dateRun',page_size=50))
    (folder/'kernels.json').write_text(json.dumps(kernels,indent=2,ensure_ascii=False),encoding='utf-8')
    print('NOTEBOOKS',json.dumps(kernels,ensure_ascii=False),flush=True)
    topics=plain(api.competition_list_topics('kaggriculture',sort_by='recent',page=1))
    (folder/'topics.json').write_text(json.dumps(topics,indent=2,ensure_ascii=False),encoding='utf-8')
    print('TOPICS',json.dumps(topics,ensure_ascii=False),flush=True)
    teams,cuts=leaderboard(api)
    report=dict(checked_utc=datetime.now(timezone.utc).isoformat(),cuts=cuts,
        top40=[dict(id=k,**v) for k,v in sorted(teams.items(),key=lambda pair:pair[1]['rank'])[:40]],
        own=teams.get('16639155'),submissions=[dict(id=s.ref,status=str(s.status),score=s.public_score,description=s.description,date=str(s.date)) for s in api.competition_submissions('kaggriculture')[:5]])
    root=Path('results/frontier16');root.mkdir(parents=True,exist_ok=True)
    (root/'live_snapshot.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('LIVE',json.dumps(report,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
