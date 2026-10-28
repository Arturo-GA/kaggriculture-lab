"""Read newly completed F16 losses after the candidate was frozen; no tuning."""
import gzip,json
from datetime import datetime,timezone
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
from live_report import leaderboard

root=Path('results/frontier17');old={r['id'] for r in json.loads((root/'f16_episodes.json').read_text(encoding='utf-8'))}
api=KaggleApi();api.authenticate();teams,_=leaderboard(api);rows=[]
for e in api.competition_list_episodes(56609913):
    if e.id in old or not str(e.state).endswith('COMPLETED') or not str(e.type).endswith('PUBLIC'):continue
    me=next(a for a in e.agents if a.submission_id==56609913);op=next(a for a in e.agents if a.submission_id!=56609913)
    if me.reward>=op.reward:continue
    team=teams.get(str(op.team_id),{})
    rows.append(dict(id=e.id,created=str(e.create_time),seat=me.index,my=me.reward,op=op.reward,margin=me.reward-op.reward,
        op_name=op.team_name,op_sub=op.submission_id,op_score=team.get('score'),op_rank=team.get('rank')))
rows.sort(key=lambda r:r['id'])
folder=Path('vendor/live_f16')
for r in rows:
    raw=folder/f"episode-{r['id']}-replay.json";zipped=Path(str(raw)+'.gz')
    if not zipped.exists():
        if not raw.exists():api.competition_episode_replay(r['id'],path=str(folder),quiet=True)
        data=raw.read_bytes();assert json.loads(data)['info']['EpisodeId']==r['id']
        with gzip.open(zipped,'wb') as f:f.write(data)
        raw.unlink()
(root/'new_loss_episodes.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(root/'new_loss_plan.json').write_text(json.dumps(dict(registered_at=datetime.now(timezone.utc).isoformat(),candidate='f17_selected',control='f16_repaired',
    frozen_source_sha256=json.loads((root/'plan.json').read_text())['hashes']['f17_selected'],episode_ids=[r['id'] for r in rows],
    rule='Out-of-sample recorded-rival diagnostic; no tuning after these results. Not a rating estimator.'),indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows,indent=2,ensure_ascii=False))
