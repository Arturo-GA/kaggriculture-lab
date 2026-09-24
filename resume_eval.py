"""Run the jobs of an interrupted evaluate.py run that are missing from its output, then merge into a complete file.
usage: resume_eval.py <partial.json> <candidates,...> <opponents,...> <seeds,...> <workers>"""
import importlib.metadata, json, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from evaluate import game, write_json_atomic
out = Path(sys.argv[1]); cands = sys.argv[2].split(','); opps = sys.argv[3].split(','); seeds = [int(s) for s in sys.argv[4].split(',')]; workers = int(sys.argv[5])
data = json.loads(out.read_text(encoding='utf-8'))
have = {(r['candidate'], r['opponent'], r['seed'], r['seat']) for r in data['rows']}
jobs = [(c, o, s, p) for c in cands for o in opps for s in seeds for p in (0, 1) if (c, o, s, p) not in have]
print('saved', len(have), 'missing', len(jobs), flush=True)
rows = list(data['rows'])
if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for fut in as_completed([pool.submit(game, j) for j in jobs]):
            rows.append(fut.result())
            write_json_atomic(out, json.dumps({'engine': importlib.metadata.version('kaggle-environments'), 'expected_games': len(have) + len(jobs),
                                               'complete': len(rows) == len(have) + len(jobs), 'rows': rows,
                                               'note': 'resumed after a failed write at %d rows; %d games rerun on the same seeds' % (len(have), len(jobs))}, indent=2) + '\n')
            print(f"{len(rows)}/{len(have) + len(jobs)}", flush=True)
    print('DONE', flush=True)
