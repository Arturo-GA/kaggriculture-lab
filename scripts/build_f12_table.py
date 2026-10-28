"""Build the Frontier12 routing table from closed-loop games of the two candidates against the public family.

Input: round-robin/evaluator JSON files whose rows carry candidate, opponent, seed, seat, margin and the final shop list.
World = the first two town shops (known at step 144).  For every world cell the base with the better win points (ties
broken by mean margin) over all seeds, rivals and seats in that cell is chosen; cells with fewer than MIN_GAMES games fall
back to the first-shop marginal, and that to the global default.  Written to results/frontier12/table.json.

usage: python build_f12_table.py results.json [more.json ...] [--min-games 4] [--opening pv]
"""
import argparse
import datetime
import json
from collections import defaultdict
from pathlib import Path

BASES = {'f11_pv_lock': 'pv', 'f11b_hs3_lock': 'hs'}


def points(margin):
    return 1.0 if margin > 0 else (0.5 if margin == 0 else 0.0)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('files', nargs='+')
    p.add_argument('--min-games', type=int, default=4)
    p.add_argument('--opening', default='pv')
    p.add_argument('--out', default='results/frontier12/table.json')
    a = p.parse_args()
    cell = defaultdict(lambda: defaultdict(list))      # (s1, s2) -> base -> margins
    first = defaultdict(lambda: defaultdict(list))     # s1 -> base -> margins
    total = defaultdict(list)
    seeds = set()
    for f in a.files:
        for r in json.loads(Path(f).read_text(encoding='utf-8'))['rows']:
            if r['candidate'] not in BASES or r['status'] != ['DONE', 'DONE']:
                continue
            b = BASES[r['candidate']]
            shops = r['shops']
            if len(shops) < 2:
                continue
            cell[(shops[0], shops[1])][b].append(r['margin'])
            first[shops[0]][b].append(r['margin'])
            total[b].append(r['margin'])
            seeds.add(r['seed'])

    def best(groups):
        scored = {}
        for b, ms in groups.items():
            scored[b] = (sum(points(m) for m in ms) / len(ms), sum(ms) / len(ms), len(ms))
        return max(scored, key=lambda b: (scored[b][0], scored[b][1])), scored

    default, tot = best(total)
    by_first, table, detail = {}, {}, {}
    for s1, groups in first.items():
        if all(len(ms) >= a.min_games for ms in groups.values()) and len(groups) == len(BASES):
            by_first[s1], sc = best(groups)
            detail[s1] = sc
    for (s1, s2), groups in cell.items():
        if all(len(ms) >= a.min_games for ms in groups.values()) and len(groups) == len(BASES):
            table[s1 + '|' + s2], sc = best(groups)
            detail[s1 + '|' + s2] = sc
    out = dict(built_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), files=a.files, seeds=len(seeds),
               min_games=a.min_games, default=default, opening=a.opening, table=table, by_first=by_first,
               totals={b: dict(points=round(v[0], 3), mean_margin=round(v[1]), games=v[2]) for b, v in tot.items()},
               detail={k: {b: dict(points=round(v[0], 3), mean_margin=round(v[1]), games=v[2]) for b, v in sc.items()} for k, sc in detail.items()},
               note='world = first two shops; cells with >= %d games per base, else first-shop marginal, else default' % a.min_games)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1) + '\n', encoding='utf-8')
    print('seeds', len(seeds), '| totals', out['totals'], '| default', default)
    print('cells decided:', len(table), 'of', len(cell), '| first-shop marginals:', len(by_first))
    disagree = sum(1 for k, v in table.items() if by_first.get(k.split('|')[0], default) != v)
    print('cells whose choice differs from their first-shop marginal:', disagree)
    for k in sorted(table):
        d = out['detail'][k]
        print(f"  {k:32s} -> {table[k]}   " + '  '.join(f"{b}: {v['points']:.2f} pts {v['mean_margin']:+6d} ({v['games']})" for b, v in d.items()))


if __name__ == '__main__':
    main()
