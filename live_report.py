"""Read-only live report: public episodes of our submissions joined with the current leaderboard.

Usage: python live_report.py 56223026 56222986 [--chunk 50] [--out results/live/report.json]
Prints win rate per time chunk, per rival rating bucket and per seat, and the rivals with most net losses.
No uploads, no replays downloaded.
"""
import argparse
import collections
import csv
import glob
import json
import os
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi


def leaderboard(api):
    folder = tempfile.mkdtemp(prefix='kaggriculture_lb_')
    api.competition_leaderboard_download('kaggriculture', path=folder)
    for z in glob.glob(os.path.join(folder, '*.zip')):
        zipfile.ZipFile(z).extractall(folder)
    rows = list(csv.DictReader(open(glob.glob(os.path.join(folder, '*.csv'))[0], encoding='utf-8-sig')))
    teams = {r['TeamId']: dict(name=r['TeamName'], score=float(r['Score']), rank=int(r['Rank'])) for r in rows}
    scores = sorted((float(r['Score']) for r in rows), reverse=True)
    n = len(scores)
    cuts = dict(teams=n, gold=scores[10 + round(0.002 * n) - 1], silver=scores[round(0.05 * n) - 1],
                bronze=scores[round(0.10 * n) - 1])
    return teams, cuts


def bucket(score):
    if score is None:
        return 'unknown'
    for edge in (2300, 2500, 2600, 2700, 2800, 2900):
        if score < edge:
            return '<%d' % edge
    return '>=2900'


def outcome(r):
    return 'W' if r['my'] > r['op'] else ('L' if r['my'] < r['op'] else 'T')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('submissions', nargs='+', type=int)
    p.add_argument('--chunk', type=int, default=50)
    p.add_argument('--out', default=None)
    a = p.parse_args()
    api = KaggleApi()
    api.authenticate()
    teams, cuts = leaderboard(api)
    print('leaderboard teams %d | gold cut %.1f | silver cut %.1f | bronze cut %.1f' % (cuts['teams'], cuts['gold'], cuts['silver'], cuts['bronze']))
    report = dict(checked_utc=datetime.now(timezone.utc).isoformat(), cuts=cuts, submissions={})
    for sid in a.submissions:
        rows = []
        for e in api.competition_list_episodes(sid):
            if not str(e.type).endswith('PUBLIC') or not str(e.state).endswith('COMPLETED'):
                continue
            me = next(x for x in e.agents if x.submission_id == sid)
            op = next(x for x in e.agents if x.submission_id != sid)
            t = teams.get(str(op.team_id))
            rows.append(dict(id=e.id, created=str(e.create_time), seat=me.index, my=me.reward or 0, op=op.reward or 0,
                             op_team=op.team_id, op_name=op.team_name, op_score=t['score'] if t else None))
        rows.sort(key=lambda r: r['created'])
        wins = sum(outcome(r) == 'W' for r in rows)
        print('\n== submission %d: %d public games, W/L/T %d/%d/%d' % (
            sid, len(rows), wins, sum(outcome(r) == 'L' for r in rows), sum(outcome(r) == 'T' for r in rows)))
        chunks = []
        for i in range(0, len(rows), a.chunk):
            ch = rows[i:i + a.chunk]
            w = sum(outcome(r) == 'W' for r in ch)
            chunks.append(dict(start=i, games=len(ch), wins=w, from_=ch[0]['created'][:16], to=ch[-1]['created'][:16]))
            print('  games %3d-%3d: %2d/%2d wins  (%s .. %s)' % (i, i + len(ch), w, len(ch), ch[0]['created'][:16], ch[-1]['created'][:16]))
        by = collections.defaultdict(lambda: [0, 0, 0])
        for r in rows:
            by[bucket(r['op_score'])]['WLT'.index(outcome(r))] += 1
        for k in sorted(by):
            print('  rival %-8s W/L/T %s' % (k, by[k]))
        for seat in (0, 1):
            ch = [r for r in rows if r['seat'] == seat]
            print('  seat %d: %d/%d wins' % (seat, sum(outcome(r) == 'W' for r in ch), len(ch)))
        net = collections.defaultdict(lambda: [0, 0])
        for r in rows:
            net[(r['op_name'], r['op_score'])][0 if outcome(r) == 'W' else 1] += 1
        worst = sorted(net.items(), key=lambda kv: -(kv[1][1] - kv[1][0]))[:8]
        print('  most net losses:', ', '.join('%s(%s) %d-%d' % (k[0][:20], k[1], v[0], v[1]) for k, v in worst))
        report['submissions'][sid] = dict(games=len(rows), wins=wins, chunks=chunks, by_bucket=dict(by), rows=rows)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
