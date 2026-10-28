"""Dated top-100 census: two latest complete public games per team's best active agent."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import threading
import time
from requests.exceptions import HTTPError

from kaggle.api.kaggle_api_extended import KaggleApi
from live_report import leaderboard
from research_f16 import plain

ROOT = Path('results/top100_0927')
RAW = Path('vendor/top100_0927')
_lock = threading.Lock()
_next_call = 0.


def limited(fn, *args, **kwargs):
    global _next_call
    for attempt in range(8):
        with _lock:
            time.sleep(max(0., _next_call-time.monotonic()))
            _next_call = time.monotonic()+1.6
        try:
            return fn(*args, **kwargs)
        except HTTPError as exc:
            if exc.response.status_code != 429 or attempt == 7:
                raise
            pause = max(float(exc.response.headers.get('Retry-After', 5)), min(60., 5.*2**attempt))
            with _lock:
                _next_call = max(_next_call, time.monotonic()+pause)
            print('Kaggle rate limit; backing off', pause, 'seconds', flush=True)


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def api():
    client = KaggleApi()
    client.authenticate()
    return client


def select(team):
    client = api()
    subs = limited(client.competition_team_submissions, team['team_id']) or []
    if not subs:
        return dict(team, submissions=[], episodes=[], unavailable='No active submission')
    best = max(subs, key=lambda s: float(s.public_score or '-inf'))
    episodes = [e for e in limited(client.competition_list_episodes, best.id)
                if str(e.state).endswith('COMPLETED') and str(e.type).endswith('PUBLIC')]
    episodes.sort(key=lambda e: (str(e.create_time), e.id), reverse=True)
    chosen = []
    for e in episodes[:2]:
        me = next(a for a in e.agents if a.submission_id == best.id)
        chosen.append(dict(id=e.id, created=str(e.create_time), seat=me.index,
                           agents=[dict(submission=a.submission_id, seat=a.index, team_id=a.team_id,
                                        team_name=a.team_name, reward=a.reward) for a in e.agents]))
    return dict(team, submissions=plain(subs), submission=best.id, submission_score=best.public_score,
                available_public=len(episodes), episodes=chosen)


def download(eid):
    path = RAW / f'episode-{eid}-replay.json'
    zipped = Path(str(path) + '.gz')
    if not zipped.exists():
        if not path.exists():
            limited(api().competition_episode_replay, eid, path=str(RAW), quiet=True)
        blob = path.read_bytes()
        data = json.loads(blob)
        assert data['info']['EpisodeId'] == eid
        zipped.write_bytes(gzip.compress(blob, mtime=0))
        path.unlink()
    blob = gzip.decompress(zipped.read_bytes())
    data = json.loads(blob)
    assert data['info']['EpisodeId'] == eid and len(data['steps']) == 720
    assert data['module_version'] == '1.32.7'
    assert [p['status'] for p in data['steps'][-1]] == ['DONE', 'DONE']
    return dict(id=eid, path=zipped.as_posix(), sha256=hashlib.sha256(blob).hexdigest(),
                compressed_bytes=zipped.stat().st_size, raw_bytes=len(blob), seed=data['info']['seed'],
                teams=data['info']['TeamNames'], rewards=data['rewards'], engine=data['module_version'])


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    snapshot = ROOT / 'selection.json'
    if snapshot.exists():
        report = json.loads(snapshot.read_text(encoding='utf-8'))
    else:
        client = api()
        teams, cuts = leaderboard(client)
        top = [dict(team_id=int(k), **v) for k, v in sorted(teams.items(), key=lambda t: t[1]['rank'])[:100]]
        report = dict(checked_utc=datetime.now(timezone.utc).isoformat(), selection_rule=
                      'Top 100 by current team rank; highest-rated active submission; latest two completed public games, no outcome selection.',
                      leaderboard=top, cuts=cuts, own=teams.get('16639155'), teams=[], episodes=[], errors=[], complete=False)
        write(snapshot, report)
        write(Path('results/frontier17/active_after_submission.json'),
              dict(checked_utc=report['checked_utc'], submissions=plain(client.competition_team_submissions(16639155))))
    found = {t['team_id'] for t in report['teams']}
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = {pool.submit(select, t): t for t in report['leaderboard'] if t['team_id'] not in found}
        for future in as_completed(jobs):
            team = jobs[future]
            try:
                row = future.result()
                report['teams'].append(row)
                print('selected', row['rank'], row['name'], len(row['episodes']), flush=True)
            except Exception as exc:
                report['errors'].append(dict(stage='selection', team_id=team['team_id'], error=type(exc).__name__))
                print('selection failed', team['team_id'], type(exc).__name__, flush=True)
            write(snapshot, report)
    ids = sorted({e['id'] for t in report['teams'] for e in t['episodes']})
    found = {e['id'] for e in report['episodes']}
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = {pool.submit(download, eid): eid for eid in ids if eid not in found}
        for future in as_completed(jobs):
            eid = jobs[future]
            try:
                report['episodes'].append(future.result())
                print('downloaded', len(report['episodes']), '/', len(ids), eid, flush=True)
            except Exception as exc:
                report['errors'].append(dict(stage='download', episode=eid, error=type(exc).__name__))
                print('download failed', eid, type(exc).__name__, flush=True)
            write(snapshot, report)
    report['complete'] = len(report['teams']) == 100 and len(report['episodes']) == len(ids)
    write(snapshot, report)
    print('complete', report['complete'], 'teams', len(report['teams']), 'unique games', len(ids), flush=True)


if __name__ == '__main__':
    main()
