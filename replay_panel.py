"""Frozen-rival replay panel: replay our live games in the official engine with the SAME seed, the rival's recorded
action stream and a candidate agent playing our seat live.  Measures how many recorded results a candidate would flip.

Caveat (Tschinkel, lesson 2): a frozen rival cannot react.  Each row therefore records how much of its recorded bank the
frozen rival keeps; judge only games where it keeps >= 95 %.

Usage: python replay_panel.py <agent.py> [<agent2.py> ...] --workers 6 [--limit N] [--out file.json]
"""
import argparse, contextlib, gzip, io, json, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

RAW = Path('vendor/live_f8')
OUT = Path('outputs/session/gold')


def game(job):
    agent_path, episode, seat = job
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    with gzip.open(RAW / f'episode-{episode}-replay.json.gz', 'rt', encoding='utf-8') as f:
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
                telemetry={k: v for k, v in dict(tel or {}).items() if k.startswith(('f9_', 'br_'))})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('agents', nargs='+')
    ap.add_argument('--workers', type=int, default=6)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    eps = json.load(open(OUT / 'episodes_f8.json', encoding='utf-8'))
    eps = [e for e in eps if (RAW / f"episode-{e['id']}-replay.json.gz").exists()]
    eps.sort(key=lambda e: e['id'])
    if a.limit:
        eps = eps[:a.limit]
    meta = {e['id']: e for e in eps}
    jobs = [(p, e['id'], e['seat']) for p in a.agents for e in eps]
    out = Path(a.out) if a.out else OUT / ('panel_' + '_'.join(Path(p).stem for p in a.agents)[:80] + '.json')
    rows = []
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        futs = [ex.submit(game, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            r = f.result()
            m = meta[r['episode']]
            r.update(opponent=m.get('op_name'), op_score=m.get('op_score'), op_sub=m.get('op_sub'))
            rows.append(r)
            out.write_text(json.dumps(rows, indent=1), encoding='utf-8')
            print(f"{i}/{len(jobs)} {r['agent']} ep {r['episode']} rec {r['recorded_margin']:+.0f} now {r['margin']:+.0f} rival_kept {r['rival_kept']} {r['seconds']}s", flush=True)
    for p in a.agents:
        name = Path(p).stem
        rs = [r for r in rows if r['agent'] == name]
        ok = [r for r in rs if r['rival_kept'] is not None and r['rival_kept'] >= 0.95]
        print(f"== {name}: games {len(rs)} | recorded wins {sum(r['recorded_margin'] > 0 for r in rs)} | replayed wins {sum(r['margin'] > 0 for r in rs)}"
              f" | valid (rival keeps >=95%) {len(ok)}: recorded wins {sum(r['recorded_margin'] > 0 for r in ok)} -> {sum(r['margin'] > 0 for r in ok)}"
              f" | L->W {sum(r['recorded_margin'] <= 0 < r['margin'] for r in ok)} W->L {sum(r['margin'] <= 0 < r['recorded_margin'] for r in ok)}"
              f" | mean margin change {sum(r['margin'] - r['recorded_margin'] for r in ok) / max(1, len(ok)):+.0f}")


if __name__ == '__main__':
    main()
