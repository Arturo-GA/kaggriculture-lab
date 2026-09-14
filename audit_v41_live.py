"""Read current public episodes and identify our exact four frozen policies."""
import contextlib
import hashlib
import io
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

OUT = Path('results/review_v41')
RAW = Path('vendor/review_v41')
SOURCES = {56216380:'frontier2_early', 56214804:'frontier', 56213093:'ml_critic', 56190498:'matched6'}


def farm_summary(farm):
    layout, ripe = Counter(), Counter()
    for row in farm['tiles']:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            item = tile.get('crop') or tile.get('animal')
            if item:
                layout[item] += 1
                ripe[item] += tile.get('yield_units', 0)
    return dict(money=farm['money'], hands=len(farm['hands']), layout=dict(layout), ripe=dict(ripe))


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    api = KaggleApi(); api.authenticate()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
    report = dict(retrieved_utc=datetime.now(timezone.utc).isoformat(), selection='Latest 8 completed public episodes per submission; no outcome selection.',
        scope='Actual played actions; not fixed-replay counterfactual wins.', complete=False, submissions=[])
    for sid, candidate in SOURCES.items():
        episodes = api.competition_list_episodes(sid)
        public = [e for e in episodes if str(e.state).endswith('COMPLETED') and str(e.type).endswith('EPISODE_TYPE_PUBLIC')]
        public.sort(key=lambda e: e.create_time, reverse=True)
        metadata = [dict(id=e.id, created=str(e.create_time), agents=[dict(submission_id=a.submission_id,
            seat=a.index, team_id=a.team_id, team_name=a.team_name, reward=a.reward) for a in e.agents]) for e in public]
        entry = dict(submission=sid, candidate=candidate, returned_episodes=len(episodes), available_public=metadata, rows=[])
        report['submissions'].append(entry)
        source = Path('candidates', candidate+'.py').read_bytes()
        entry['source_sha256'] = hashlib.sha256(source).hexdigest()
        for ep in public[:8]:
            path = RAW/f'episode-{ep.id}-replay.json'
            if not path.exists():
                api.competition_episode_replay(ep.id, path=str(RAW), quiet=True)
            data = json.loads(path.read_text(encoding='utf-8'))
            seat = next(a.index for a in ep.agents if a.submission_id == sid)
            fn = get_last_callable(source.decode('utf-8'))
            config = dict(data['configuration'], seed=data['info']['seed'])
            mismatches = []
            for step in range(len(data['steps'])-1):
                obs = dict(data['steps'][step][0]['observation'])
                obs.update(data['steps'][step][seat]['observation'])
                obs.update(player=seat, step=step)
                got = fn(obs, config)
                if got != data['steps'][step+1][seat]['action']:
                    mismatches.append(step)
            row = dict(episode=ep.id, created=str(ep.create_time), seat=seat, rewards=data['rewards'],
                margin=data['rewards'][seat]-data['rewards'][1-seat],
                exact_actions=not mismatches, mismatch_count=len(mismatches), first_mismatches=mismatches[:10],
                opponent=next(a.team_name for a in ep.agents if a.index != seat),
                statuses=[s['status'] for s in data['steps'][-1]],
                engine=data['module_version'], seed=data['info']['seed'], snapshots={})
            for step in (24,144,288,432,576,648,696,719):
                farms = data['steps'][step][0]['observation']['farms']
                row['snapshots'][str(step)] = dict(own=farm_summary(farms[seat]), rival=farm_summary(farms[1-seat]), gap=farms[seat]['money']-farms[1-seat]['money'])
            row['telemetry'] = dict(getattr(fn, 'telemetry', {}))
            entry['rows'].append(row)
            (OUT/'live_audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
            print(json.dumps(dict(candidate=candidate, episode=ep.id, margin=row['margin'], gap_at_696=row['snapshots']['696']['gap'], exact=row['exact_actions']), ensure_ascii=True), flush=True)
    report['complete'] = True
    (OUT/'live_audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
