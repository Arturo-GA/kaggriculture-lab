"""Check every native-wrapper action against the unchanged deployed policy."""
import contextlib
import hashlib
import io
import json
from pathlib import Path

import accelerator


def main():
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
    source = Path('candidates/matched6.py').read_text(encoding='utf-8')
    base = get_last_callable(source)
    rival = get_last_callable(source)
    wrapper = get_last_callable(Path('candidates/ml_native.py').read_text(encoding='utf-8'))
    env = accelerator.load().Game(70001)
    count = 0
    digest = hashlib.sha256()
    while not env.done:
        obs = env.observe(0)
        expected, actual = base(obs, {}), wrapper(obs, {})
        assert expected == actual, (env.step_count, expected, actual)
        digest.update(json.dumps(actual, sort_keys=True).encode())
        env.step(actual, rival(env.observe(1), {}))
        count += 1
    report = dict(passed=True, seed=70001, exact_action_checks=count,
                  actions_sha256=digest.hexdigest(), rewards=[env.reward(i) for i in (0,1)],
                  telemetry=wrapper.telemetry)
    Path('results/ml/native_parity.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
