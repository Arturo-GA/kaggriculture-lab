"""Assemble the Frontier12 world router: two Frontier11 candidates in one file, chosen per world.

Why: games between agents of the final public family are deterministic and decided by the world (the first town shops):
each public branch wins some worlds and loses others, and our two Frontier11 candidates lose different worlds.  The
router runs both candidates side by side on the same observations (their actions agree on 142 of the first 144 steps),
lets one play until the second shop is known, then switches to the one that wins against the rival's branch in that world
according to a table built from closed-loop games against the public family (build_f12_table.py).  The rival's branch is
read at step 1 from its public money after the opening trade (2854 = the BUY 20 / SELL 15 group, 2858 = the Herd-Safe
BUY 8 / SELL 3 group; anything else = unknown).  Only the chosen base runs after the switch.

The two embedded candidates are our exported Frontier11 files (public bases with every upstream notice retained plus the
Lab lockstep layer); their hashes are pinned here.  The router itself is original Kaggriculture Lab code (Apache-2.0).
"""
import base64
import hashlib
import json
import zlib
from pathlib import Path

BASES = {'pv': 'f11_pv_lock', 'hs': 'f11b_hs3_lock'}
PINS = {'f11_pv_lock': 'def14a5a7c98c984', 'f11b_hs3_lock': '4aac62c84ba5be94'}
TABLE = Path('results/frontier12/table.json')

RUNTIME = r'''
# ==== Frontier12 world router (Arturo-GA / Kaggriculture Lab, Apache-2.0) ====
# Two agents of the final public wave, each with the Lab lockstep layer, run side by side on the same observations.
# One plays until the second town shop is known; then the one that wins that world (table from closed-loop games
# against the public family) plays on alone.  Nothing else changes: the chosen base's actions are returned verbatim.
import base64 as _f12_b64, zlib as _f12_zlib, json as _f12_json
_F12_SWITCH = 144
_F12_REPORT = dict(f12_choice='', f12_switch_step=-1, f12_key='', f12_profile='', f12_branch='', f12_errors=0, f12_shadow_errors=0)
_F12_STATE = {}
_F12_ORIGINAL = {}


def _f12_load(key):
    src = _f12_zlib.decompress(_f12_b64.b85decode(_F12_BLOBS[key])).decode('utf-8')
    ns = {'__name__': 'f12_' + key}
    exec(compile(src, key + '.py', 'exec'), ns)
    return [v for v in ns.values() if callable(v)][-1]   # the same rule as the Kaggle loader


_F12_AGENTS = {k: _f12_load(k) for k in _F12_ORDER}


def _f12_branch(observation):
    """The rival's public money after the opening trade tells its branch (deterministic, seed-independent)."""
    money = float(observation['farms'][1 - int(observation['player'])]['money'])
    return _F12_BRANCH_MONEY.get(str(int(round(money))), 'unknown')


def _f12_pick(observation, branch):
    shops = [str(s) for s in (observation.get('town', {}).get('unlocked_shops') or [])]
    keys = []
    for b in (branch, '*'):
        if len(shops) >= 2:
            keys.append(b + '|' + shops[0] + '|' + shops[1])
        if shops:
            keys.append(b + '|' + shops[0])
        keys.append(b)
    for k in keys:
        if k in _F12_TABLE:
            return _F12_TABLE[k], k
    return _F12_DEFAULT, 'default'


def _f12_apply(choice):
    """'base' or 'base:profile': set the profile's constants in that base's namespace (read at call time), remembering
    the originals so a new game starts clean."""
    base, _, profile = choice.partition(':')
    if profile:
        g = _F12_AGENTS[base].__globals__
        for k, v in _F12_PROFILES.get(profile, {}).items():
            _F12_ORIGINAL.setdefault((base, k), g.get(k))
            g[k] = v
    return base, profile


def _f12_restore():
    for (base, k), v in _F12_ORIGINAL.items():
        _F12_AGENTS[base].__globals__[k] = v
    _F12_ORIGINAL.clear()


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    if step == 0:
        _F12_STATE.clear()
        _f12_restore()
        _F12_REPORT.update(f12_choice='', f12_switch_step=-1, f12_key='', f12_profile='', f12_branch='', f12_errors=0, f12_shadow_errors=0)
    if step == 1 and 'branch' not in _F12_STATE:
        try:
            _F12_STATE['branch'] = _f12_branch(observation)
        except Exception:
            _F12_STATE['branch'] = 'unknown'
            _F12_REPORT['f12_errors'] += 1
        _F12_REPORT['f12_branch'] = _F12_STATE['branch']
    chosen = _F12_STATE.get('chosen')
    if chosen is None and step >= _F12_SWITCH:
        try:
            choice, key = _f12_pick(observation, _F12_STATE.get('branch', 'unknown'))
            chosen, profile = _f12_apply(choice)
        except Exception:
            chosen, profile, key = _F12_DEFAULT.partition(':')[0], '', 'error'
            _F12_REPORT['f12_errors'] += 1
        _F12_STATE['chosen'] = chosen
        _F12_REPORT.update(f12_choice=chosen, f12_switch_step=step, f12_key=key, f12_profile=profile)
    active = chosen or _F12_OPENING
    actions = {}
    for key, fn in _F12_AGENTS.items():
        if chosen is not None and key != chosen:
            continue
        obs = observation if key == active else _f12_json.loads(_f12_json.dumps(observation))
        try:
            actions[key] = fn(obs, configuration)
        except Exception:
            _F12_REPORT['f12_errors' if key == active else 'f12_shadow_errors'] += 1
    action = actions.get(active)
    if action is None:
        action = next(iter(actions.values()), None) or {'farmer': ['PASS'], 'hands': [], 'market': []}
    _F12_TELEMETRY.clear()
    _F12_TELEMETRY.update(getattr(_F12_AGENTS[active], 'telemetry', {}) or {})
    _F12_TELEMETRY.update(_F12_REPORT)
    return action


_F12_TELEMETRY = {}
agent.telemetry = _F12_TELEMETRY
'''


def load(name):
    data = Path('candidates', name + '.py').read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest.startswith(PINS[name]), (name, digest)
    return data


def build(table):
    nl = chr(10)
    blobs = {k: base64.b85encode(zlib.compress(load(n), 9)).decode('ascii') for k, n in BASES.items()}
    head = ('# Frontier12 world router: two public agents of the final Kaggriculture wave (with every upstream Apache-2.0' + nl +
            '# notice retained inside each embedded source) and the Kaggriculture Lab lockstep layer, chosen per world.' + nl +
            '# Embedded sources (SHA-256 of each candidate file): ' +
            ', '.join('%s=%s' % (k, hashlib.sha256(load(n)).hexdigest()) for k, n in BASES.items()) + nl +
            '# Table: %s (%s)' % (table.get('note', ''), table.get('built_utc', '')) + nl)
    consts = ('_F12_ORDER = %r' % (list(BASES),) + nl +
              '_F12_BLOBS = %r' % (blobs,) + nl +
              '_F12_TABLE = %r' % (table['table'],) + nl +
              '_F12_BRANCH_MONEY = %r' % (table.get('branch_money', {'2854': 'pv', '2858': 'hs'}),) + nl +
              '_F12_DEFAULT = %r' % (table['default'],) + nl +
              '_F12_OPENING = %r' % (table.get('opening', table['default']),) + nl +
              '_F12_PROFILES = %r' % (table.get('profiles', {}),) + nl)
    return head + consts + RUNTIME


if __name__ == '__main__':
    table = json.loads(TABLE.read_text(encoding='utf-8')) if TABLE.exists() else dict(table={'pv': 'pv', 'hs': 'hs'}, default='pv', opening='pv', profiles={}, note='branch mirror only')
    src = build(table)
    compile(src, 'f12_router', 'exec')
    out = Path('candidates/f12_router.py')
    out.write_text(src, encoding='utf-8', newline='')
    manifest = dict(bases={k: hashlib.sha256(load(n)).hexdigest() for k, n in BASES.items()}, table_keys=sorted(table['table']), profiles=sorted(table.get('profiles', {})),
                    branch_money=table.get('branch_money', {'2854': 'pv', '2858': 'hs'}), default=table['default'], opening=table.get('opening', table['default']),
                    sha256=hashlib.sha256(out.read_bytes()).hexdigest(), bytes=out.stat().st_size)
    Path('results/frontier12').mkdir(parents=True, exist_ok=True)
    Path('results/frontier12/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))
