"""Four latest public games per current top-100 agent, plus all current F17 games.

Read-only, resumable, paced API calls. Preserve the earlier two-game census.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path

from live_report import leaderboard
from research_f16 import plain
from research_top100 import api, limited, download, write, RAW

ROOT = Path('results/top100_four_0927')


def episode_row(e, sid, teams):
    me = next(a for a in e.agents if a.submission_id == sid)
    op = next(a for a in e.agents if a.index != me.index)
    rival = teams.get(str(op.team_id), {})
    return dict(id=e.id, created=str(e.create_time), seat=me.index,
                my=me.reward, op=op.reward, margin=me.reward-op.reward,
                op_rank=rival.get('rank'), op_score=rival.get('score'), op_name=op.team_name,
                agents=[dict(submission=a.submission_id, seat=a.index, team_id=a.team_id,
                             team_name=a.team_name, reward=a.reward) for a in e.agents])


def public_episodes(client, sid, teams):
    episodes = [e for e in limited(client.competition_list_episodes, sid)
                if str(e.state).endswith('COMPLETED') and str(e.type).endswith('PUBLIC')]
    episodes.sort(key=lambda e: (str(e.create_time), e.id), reverse=True)
    return [episode_row(e, sid, teams) for e in episodes]


def select(team, teams):
    client = api()
    subs = limited(client.competition_team_submissions, team['team_id']) or []
    if not subs:
        return dict(team, submissions=[], episodes=[], unavailable='No active submission')
    best = max(subs, key=lambda s: float(s.public_score or '-inf'))
    rows = public_episodes(client, best.id, teams)
    return dict(team, submissions=plain(subs), submission=best.id, submission_score=best.public_score,
                available_public=len(rows), selected_utc=datetime.now(timezone.utc).isoformat(), episodes=rows[:4])


def main():
    ROOT.mkdir(parents=True, exist_ok=True); RAW.mkdir(parents=True, exist_ok=True)
    path = ROOT/'selection.json'
    if path.exists():
        report = json.loads(path.read_text(encoding='utf-8'))
    else:
        client = api(); teams, cuts = leaderboard(client)
        top = [dict(team_id=int(k), **v) for k, v in sorted(teams.items(), key=lambda t:t[1]['rank'])[:100]]
        report = dict(checked_utc=datetime.now(timezone.utc).isoformat(), selection_rule=
                      'Current top100; highest-rated active submission; four latest completed public episodes without outcome selection. API selection times recorded per team.',
                      leaderboard=top, full_leaderboard=teams, cuts=cuts, own=teams.get('16639155'),
                      active_own=plain(limited(client.competition_team_submissions, 16639155)),
                      f17_public=public_episodes(client, 56615489, teams), teams=[], episodes=[], errors=[], complete=False)
        write(path, report)
        own = report['f17_public']
        print('F17 public games', len(own), 'wins', sum(r['margin']>0 for r in own),
              'losses', sum(r['margin']<0 for r in own), 'ties', sum(r['margin']==0 for r in own), flush=True)
    found = {t['team_id'] for t in report['teams']}
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = {pool.submit(select, t, report['full_leaderboard']):t for t in report['leaderboard'] if t['team_id'] not in found}
        for future in as_completed(jobs):
            team = jobs[future]
            try:
                row = future.result(); report['teams'].append(row)
                print('selected', row['rank'], len(row['episodes']), flush=True)
            except Exception as exc:
                report['errors'].append(dict(stage='selection', team_id=team['team_id'], error=repr(exc)))
            write(path, report)
    ids = sorted({e['id'] for t in report['teams'] for e in t['episodes']} | {e['id'] for e in report['f17_public']})
    found = {e['id'] for e in report['episodes']}
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = {pool.submit(download, eid):eid for eid in ids if eid not in found}
        for future in as_completed(jobs):
            eid = jobs[future]
            try:
                report['episodes'].append(future.result())
                print('downloaded', len(report['episodes']), '/', len(ids), eid, flush=True)
            except Exception as exc:
                report['errors'].append(dict(stage='download', episode=eid, error=repr(exc)))
            write(path, report)
    report['complete'] = len(report['teams']) == 100 and len(report['episodes']) == len(ids)
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    write(path, report)
    print('complete', report['complete'], 'teams', len(report['teams']), 'unique games', len(ids), flush=True)


if __name__ == '__main__':
    main()
