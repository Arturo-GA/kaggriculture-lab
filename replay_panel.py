"""Frozen-rival replay panel: replay our live games in the official engine with the SAME seed, the rival's recorded
action stream and a candidate agent playing our seat live.  Measures how many recorded results a candidate would flip.

Caveat: a frozen rival cannot react. Rival bank retention is descriptive only;
even 100% retention does not make a counterfactual game a valid competitive test.

Usage: python replay_panel.py <agent.py> [<agent2.py> ...] --workers 6 [--limit N] [--out file.json]
"""
import argparse, contextlib, gzip, hashlib, io, json, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from evaluate import write_json_atomic

RAW = Path('vendor/live_f8')
OUT = Path('outputs/session/gold')


def game(job):
    agent_path, episode, seat = job[:3]
    raw_dir = Path(job[3]) if len(job) > 3 else RAW
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    with gzip.open(raw_dir / f'episode-{episode}-replay.json.gz', 'rt', encoding='utf-8') as f:
        data = json.load(f)
    steps = data['steps']
    seed = data['info']['seed']
    rival = 1 - seat
    recorded = [steps[-1][s]['reward'] for s in (0, 1)]
    tape = [steps[t + 1][rival]['action'] or {'farmer': ['PASS'], 'hands': [], 'market': []} for t in range(len(steps) - 1)]

    def frozen(observation, configuration=None):
        t = int(observation['step'])
        return tape[t] if t < len(tape) else {'farmer': ['PASS'], 'hands': [], 'market': []}

    fn = get_last_callable(Path(agent_path).read_text(encoding='utf-8'), path=str(agent_path))
    pol = [fn, frozen] if seat == 0 else [frozen, fn]
    t0 = time.time()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': seed}, debug=True)
        env.run(pol)
    final = env.steps[-1]
    rew = [final[s]['reward'] for s in (0, 1)]
    tel = getattr(fn, 'telemetry', None)
    errors = {k: v for k, v in dict(tel or {}).items() if v and ('error' in k or 'fallback' in k)} if tel is not None else {}
    return dict(agent=Path(agent_path).stem, episode=episode, seat=seat, seed=seed,
                recorded_margin=recorded[seat] - recorded[rival], margin=rew[seat] - rew[rival],
                own=rew[seat], rival=rew[rival], rival_recorded=recorded[rival],
                rival_kept=round(rew[rival] / recorded[rival], 4) if recorded[rival] else None,
                status=[s['status'] for s in final], errors=errors, seconds=round(time.time() - t0, 1),
                telemetry=dict(tel or {}), steps=len(env.steps),
                sha256=hashlib.sha256(Path(agent_path).read_bytes()).hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('agents', nargs='+')
    ap.add_argument('--workers', type=int, default=6)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--out', default='')
    ap.add_argument('--resume', action='store_true', help='Reuse verified completed rows from the same output and exact agent sources')
    ap.add_argument('--raw', default=str(RAW), help='folder with episode-<id>-replay.json.gz files')
    ap.add_argument('--episodes', default=str(OUT / 'episodes_f8.json'), help='JSON list with id, seat, op_name, op_score (and op_sub)')
    a = ap.parse_args()
    raw_dir = Path(a.raw)
    eps = json.load(open(a.episodes, encoding='utf-8'))
    eps = [e for e in eps if (raw_dir / f"episode-{e['id']}-replay.json.gz").exists()]
    eps.sort(key=lambda e: e['id'])
    if a.limit:
        eps = eps[:a.limit]
    meta = {e['id']: e for e in eps}
    jobs = [(p, e['id'], e['seat'], str(raw_dir)) for p in a.agents for e in eps]
    out = Path(a.out) if a.out else OUT / ('panel_' + '_'.join(Path(p).stem for p in a.agents)[:80] + '.json')
    rows = []
    if a.resume and out.exists():
        rows=json.loads(out.read_text(encoding='utf-8'))
        hashes={Path(p).stem:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in a.agents}
        expected={(Path(p).stem,e['id'],e['seat']) for p in a.agents for e in eps}
        done=set()
        for r in rows:
            key=(r['agent'],r['episode'],r['seat'])
            assert key in expected and key not in done and r['sha256']==hashes[r['agent']]
            assert r['steps']==720 and r['status']==['DONE','DONE']
            done.add(key)
        jobs=[j for j in jobs if (Path(j[0]).stem,j[1],j[2]) not in done]
        print('Resuming',len(rows),'verified rows;',len(jobs),'pending',flush=True)
    total=len(rows)+len(jobs);completed=len(rows)
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(game, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), completed+1):
            r = f.result()
            m = meta[r['episode']]
            r.update(opponent=m.get('op_name'), op_score=m.get('op_score'), op_sub=m.get('op_sub'))
            rows.append(r)
            write_json_atomic(out,json.dumps(rows, indent=1))
            print(f"{i}/{total} {r['agent']} ep {r['episode']} rec {r['recorded_margin']:+.0f} now {r['margin']:+.0f} rival_kept {r['rival_kept']} {r['seconds']}s", flush=True)
    for p in a.agents:
        name = Path(p).stem
        rs = [r for r in rows if r['agent'] == name]
        print(f"== {name}: games {len(rs)} | recorded wins {sum(r['recorded_margin'] > 0 for r in rs)} | replayed wins {sum(r['margin'] > 0 for r in rs)}"
              f" | L->W {sum(r['recorded_margin'] <= 0 < r['margin'] for r in rs)} W->L {sum(r['margin'] <= 0 < r['recorded_margin'] for r in rs)}"
              f" | mean margin change {sum(r['margin'] - r['recorded_margin'] for r in rs) / max(1, len(rs)):+.0f} | DIAGNOSTIC ONLY: rival cannot react")


if __name__ == '__main__':
    main()
