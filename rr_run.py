"""Round robin on the official engine without mirrored duplicates: each unordered pair once, every seed, both seats.
usage: python rr_run.py --agents A B C ... [--extra X Y --vs A B] --seeds ... --workers N --output file.json
  --agents  : all unordered pairs among these
  --extra/--vs : additionally every extra agent against every --vs agent"""
import argparse, importlib.metadata, json
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from evaluate import game

p = argparse.ArgumentParser()
p.add_argument('--agents', nargs='*', default=[])
p.add_argument('--extra', nargs='*', default=[])
p.add_argument('--vs', nargs='*', default=[])
p.add_argument('--seeds', nargs='+', type=int, required=True)
p.add_argument('--workers', type=int, default=7)
p.add_argument('--output', required=True)
a = p.parse_args()
pairs = [(x, y) for i, x in enumerate(a.agents) for y in a.agents[i + 1:]] + [(x, y) for x in a.extra for y in a.vs if x != y]
jobs = [(x, y, s, seat) for x, y in pairs for s in a.seeds for seat in (0, 1)]
rows, out = [], Path(a.output)
out.parent.mkdir(parents=True, exist_ok=True)
if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for fut in as_completed([pool.submit(game, j) for j in jobs]):
            row = fut.result(); rows.append(row)
            out.write_text(json.dumps({'engine': importlib.metadata.version('kaggle-environments'), 'expected_games': len(jobs),
                                       'complete': len(rows) == len(jobs), 'rows': rows}, indent=1) + '\n')
            print(f"{len(rows)}/{len(jobs)} {row['candidate']} vs {row['opponent']} seed={row['seed']} seat={row['seat']} margin={row['margin']:.0f} max_ms={row['max_call_ms']:.1f}", flush=True)
