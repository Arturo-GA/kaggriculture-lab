"""Descriptive four-versus-two stability, with teams as the unit of comparison."""
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import median

ROOT = Path('results/frontier19')


def main():
    selection = json.loads((ROOT / 'selection.json').read_text(encoding='utf-8'))
    features = json.loads(gzip.decompress((ROOT / 'features.json.gz').read_bytes()))
    by_key = {(r['team_id'], r['episode'], r['seat']): r for r in features}
    teams = [t for t in selection['teams'] if 200 <= t['rank'] <= 300]
    rows = []
    for team in teams:
        rs = [by_key[team['team_id'], e['id'], e['seat']] for e in team['episodes']]
        assert len(rs) == 4
        sw = [r['first_land_step'].get('SW', 720) for r in rs]
        strawberries = [r['snapshots']['288']['layout'].get('STRAWBERRY', 0) for r in rs]
        herd = [tuple(r['snapshots']['288']['layout'].get(a, 0) for a in ('GOOSE', 'COW', 'SHEEP')) for r in rs]
        trades = [sum(r['same_turn_buy_sell'].get(a + '_turns', 0) for a in ('WHEAT', 'FERTILIZER')) for r in rs]
        rows.append(dict(team_id=team['team_id'], rank=team['rank'],
                         episodes=[e['id'] for e in team['episodes']],
                         sw=sw, strawberries=strawberries, herds=herd, input_trade_turns=trades,
                         four_vs_two_sw_median_change=median(sw) - median(sw[:2]),
                         stable_herd_count=Counter(herd).most_common(1)[0][1],
                         all_four_sw_before_240=all(s < 240 for s in sw),
                         first_two_sw_before_240=all(s < 240 for s in sw[:2]),
                         later_two_contradict_early_sw=all(s < 240 for s in sw[:2]) and any(s >= 240 for s in sw[2:])))
    summary = dict(teams=len(rows),
                   all_four_sw_before_240=sum(r['all_four_sw_before_240'] for r in rows),
                   first_two_sw_before_240=sum(r['first_two_sw_before_240'] for r in rows),
                   later_two_contradict_early_sw=sum(r['later_two_contradict_early_sw'] for r in rows),
                   identical_herd_all_four=sum(r['stable_herd_count'] == 4 for r in rows),
                   absolute_sw_median_shift=median(abs(r['four_vs_two_sw_median_change']) for r in rows),
                   note='Descriptive snapshots conditioned on shops and game state. Four games cannot establish causality or reveal private policy. Input-trade counts add per-item turns, so two items in one turn count twice.',
                   features_sha256=hashlib.sha256((ROOT / 'features.json.gz').read_bytes()).hexdigest())
    (ROOT / 'four_game_stability.json').write_text(json.dumps(dict(summary=summary, teams=rows), indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
