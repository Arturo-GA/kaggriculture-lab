"""Compare live policies on both engines, checking all 719 action transitions."""
import contextlib
import copy
import io
import json
from pathlib import Path
import time

import accelerator

ROOT = Path(__file__).resolve().parent
KEYS = ('player', 'day', 'hour', 'farms', 'market', 'town', 'private')


def verify(candidate, opponent, seed):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
        env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': seed}, debug=True)
        env.reset(2)
    fast = accelerator.load(allow_unverified=True).Game(seed)
    source = [(ROOT / 'candidates' / (n + '.py')).read_text(encoding='utf-8')
              for n in (candidate, opponent)]
    official_policies = [get_last_callable(s) for s in source]
    fast_policies = [get_last_callable(s) for s in source]
    transitions = comparisons = 0
    engine_seconds = {'official': 0.0, 'cpp': 0.0}
    begin = time.perf_counter()
    while not env.done:
        official_actions, fast_actions = [], []
        for seat in (0, 1):
            obs = copy.deepcopy(dict(env.state[seat].observation))
            shared = env.state[0].observation
            for key in ('step', 'day', 'hour', 'farms', 'market', 'town'):
                if key not in obs:
                    obs[key] = copy.deepcopy(shared[key])
            other = fast.observe(seat)
            assert obs['step'] == fast.step_count
            for key in KEYS:
                assert obs[key] == other[key], (candidate, opponent, seed, fast.step_count, seat, key)
                comparisons += 1
            # Inventory insertion order controls shed overflow. Check it as well
            # as equality of values, which normal dict equality alone would miss.
            for a, b in [(obs['private']['shed'], other['private']['shed']),
                         *zip(obs['private']['inventories'], other['private']['inventories'])]:
                assert list(a) == list(b), ('inventory key order', seed, fast.step_count, seat)
            config = dict(env.configuration)
            official_actions.append(official_policies[seat](obs, config))
            fast_actions.append(fast_policies[seat](other, config))
        assert official_actions == fast_actions, ('actions', seed, fast.step_count)
        t = time.perf_counter()
        env.step(official_actions)
        engine_seconds['official'] += time.perf_counter() - t
        t = time.perf_counter()
        fast.step(*fast_actions)
        engine_seconds['cpp'] += time.perf_counter() - t
        transitions += 1
    official_rewards = [row.reward for row in env.state]
    assert fast.done and transitions == 719
    assert [row.status for row in env.state] == ['DONE', 'DONE']
    assert official_rewards == [fast.reward(0), fast.reward(1)]
    return dict(candidate=candidate, opponent=opponent, seed=seed, rewards=official_rewards,
                compared_field_blocks=comparisons, compared_seat_actions=2 * transitions,
                inventory_order_checked=True, engine_step_seconds=engine_seconds,
                total_seconds=time.perf_counter() - begin)


def main():
    build = json.loads((ROOT / 'results/cppsim_build.json').read_text())
    result = dict(passed=False, binary_sha256=build['binary_sha256'],
                  revision=build['revision'], rows=[])
    out = ROOT / 'results/cppsim_verification.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    for candidate, opponent, seed in [('matched6', 'router', 61001),
                                       ('belief_gate', 'prvsiyan', 61002),
                                       ('demand_gate', 'matched6', 61003)]:
        row = verify(candidate, opponent, seed)
        result['rows'].append(row)
        out.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(row), flush=True)
    result['passed'] = True
    result['scope'] = 'Default 1.32.7 configuration, 3 live duels. Not a proof for every state or custom configuration.'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print('PASSED', flush=True)


if __name__ == '__main__':
    main()
