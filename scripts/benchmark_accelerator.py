"""Paired end-to-end checks on official and accelerated live-policy runners."""
import json
from pathlib import Path
import evaluate
import evaluate_fast


def main():
    pairs = [('matched6', 'router', 61001, 0),
             ('belief_gate2', 'matched6', 53003, 0),
             ('belief_lead12', 'router', 53005, 1)]
    rows = []
    for job in pairs:
        official = evaluate.game(job)
        fast = evaluate_fast.game(job)
        assert official['rewards'] == fast['rewards'], (job, official['rewards'], fast['rewards'])
        assert official['shops'] == fast['shops'], job
        assert official['telemetry'] == fast['telemetry'], ('telemetry', job)
        row = dict(job=job, official=official, cpp=fast,
                   speedup=official['seconds'] / fast['seconds'])
        rows.append(row)
        print(json.dumps(dict(job=job, rewards=official['rewards'], speedup=row['speedup'])), flush=True)
    result = dict(passed=True, rows=rows,
                  aggregate_speedup=sum(r['official']['seconds'] for r in rows) /
                                    sum(r['cpp']['seconds'] for r in rows),
                  note='Three sequential pairs on this workstation, including live Python policies. Not a universal speedup or leaderboard benchmark.')
    Path('results/cppsim_benchmark.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
