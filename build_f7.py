"""Assemble Frontier7 candidates: public V48 base (pinned) + Kaggriculture Lab layers.

Inputs: candidates/v48.py (from extract_public_agents.py, git-ignored), frontier5_lockstep.py and frontier7_hold.py.
V48 ends with `_e335_agent`; the Kaggle loader takes the last callable, so the base entry point is bound to `agent`
explicitly before the Lab layers wrap it (an earlier build that wrapped the module-level `agent` bypassed V47/V48's
own layers and behaved exactly like Frontier5).
"""
import hashlib
import json
from pathlib import Path

V48_SHA256 = '4b5402888feeb4170dce38f34bebe56788b62ca287139fce7db72df8eb89bb96'

v48 = Path('candidates/v48.py').read_bytes()
assert hashlib.sha256(v48).hexdigest() == V48_SHA256, 'Public V48 source changed; re-extract and re-verify'
v48 = v48.decode('utf-8')
assert v48.rstrip().endswith('return _e334_agent(observation,configuration)')
bind = ('\n# Frontier7: bind the public V48 entry point (last callable, as the Kaggle loader does) '
        'before the lockstep layer\nagent=_e335_agent\n')
lock = Path('frontier5_lockstep.py').read_text(encoding='utf-8')
hold = Path('frontier7_hold.py').read_text(encoding='utf-8')

VARIANTS = {
    'f7_lock': (v48 + bind + lock, 'V48 + lockstep sale ordering against a copy (exported candidate)'),
    'f7_hold': (v48 + bind + lock + '\n' + hold, 'f7_lock + milk/wool hold-and-release layer (measured negative, not exported)'),
    'f7_holdonly': (v48 + bind + hold, 'V48 + hold layer alone (measured negative, not exported)'),
}


def write(name, src):
    compile(src.replace('\r\n', '\n'), name, 'exec')
    Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
    print('wrote', name, len(src))


if __name__ == '__main__':
    manifest = {'v48_sha256': V48_SHA256, 'variants': {}}
    for name, (src, note) in VARIANTS.items():
        write(name, src)
        manifest['variants'][name] = dict(sha256=hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest(), note=note)
    Path('results/frontier7').mkdir(parents=True, exist_ok=True)
    Path('results/frontier7/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))
