"""A separate production hypothesis; never retune the four frozen finalists."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def main():
    parent = Path('candidates/f19_robust.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == '416a46b1648dd3647a26417bbac411a08697f5ce9cf02555830dc5e11b118791'
    raw = parent + b'\n_F19_HERD_GAIN=400\n_F19_HERD_RATIO=1.1\n' + Path('frontier19_oneherd.py').read_bytes()
    target = Path('candidates/f19_oneherd.py')
    assert not target.exists() or target.read_bytes() == raw
    compile(raw, str(target), 'exec')
    target.write_bytes(raw)
    report = dict(candidate=target.stem, sha256=hashlib.sha256(raw).hexdigest(),
                  parent_sha256=hashlib.sha256(parent).hexdigest(),
                  created_utc=datetime.now(timezone.utc).isoformat(),
                  hypothesis='At most one future single-unit sheep purchase changes species, only with predicted gain >=400 and >=10%, and a feasible same-day transport/build plan. Cow is considered if a goose coop cannot be built on that route.',
                  validation='Separate exploration only. Not part of frozen 19101..19108 selection. Needs fresh independent confirmation before submission.')
    Path('results/frontier19/oneherd_build.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
