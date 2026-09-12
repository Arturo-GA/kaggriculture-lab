"""Build two sale-timing experiments on the immutable matched6 source."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = '28f57454d8dab2618441d8ef2f1fe04924cf8291e069a5e2ed20daf28cded489'

WRAPPER = '''
_LAB_GATE_PARENT = agent
def agent(observation, configuration=None):
    _lab_gate_before(observation, configuration)
    action = _LAB_GATE_PARENT(observation, configuration)
    _lab_gate_after(observation, action)
    agent.telemetry = dict(getattr(_LAB_GATE_PARENT, 'telemetry', {}), **_LAB_GATE_REPORT)
    return action
agent.telemetry = {}
agent = globals().pop('agent')
'''


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--funded', action='store_true')
    group.add_argument('--lead', action='store_true')
    args = parser.parse_args()
    source = (ROOT / 'candidates/matched6.py').read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED
    parent = source.decode('utf-8')
    helper = (ROOT / 'market_gate.py').read_text(encoding='utf-8')
    if args.lead:
        helper += '\n' + (ROOT / 'market_lead.py').read_text(encoding='utf-8')
    if args.funded:
        old = """    if any(o and o[0] != 'SELL' for t in range(step, due + 1)
           for o in (action if t == step else tape[t]).get('market', [])):
        return True"""
        assert helper.count(old) == 1
        helper = helper.replace(old, "    if not _lab_gate_funded(obs, action, tape, due):\n        return True")
        helper = (ROOT / 'market_gate_budget.py').read_text(encoding='utf-8') + '\n' + helper
    anchor = "        if qty:\n            market.append(['SELL',item,qty])"
    assert parent.count(anchor) == 1
    records = {}
    for mode in (('lead',) if args.lead else ('demand', 'belief')):
        name = 'belief_lead12' if args.lead else mode + '_gate' + ('2' if args.funded else '')
        text = parent.replace('def _r36_reserve(obs,action):',
                              helper + '\n\n' + 'def _r36_reserve(obs,action):')
        if args.lead:
            old = 'if 288 <= step < 696:_R37_HORIZONS[player] = 6 if 336 <= step < 648 and state["streak"] >= 6 else 4'
            assert text.count(old) == 1
            text = text.replace(old, 'if 288 <= step < 696:_R37_HORIZONS[player] = 12')
            old = '            if amount:\n                reservations.append((due_step,amount));available-=amount'
            assert text.count(old) == 1
            text = text.replace(old, '            if amount and _lab_allow_long_lead(obs,item,due_step,amount):\n'
                                '                reservations.append((due_step,amount));available-=amount')
        else:
            text = text.replace(anchor,
                                "        if qty and _lab_allow_advance(obs,action,stock,item,reservations):\n"
                                "            market.append(['SELL',item,qty])")
        text += '\n_LAB_GATE_MODE = ' + repr(mode) + '\n' + WRAPPER
        text = '# Modified 2026-09-12 Arturo-GA: public market scenario gate; Apache-2.0.\n' + text
        compile(text, name + '.py', 'exec')
        data = text.encode('utf-8')
        (ROOT / 'candidates' / (name + '.py')).write_bytes(data)
        records[name] = hashlib.sha256(data).hexdigest()
    receipt = dict(parent_sha256=EXPECTED, candidates=records,
                   helper_sha256=hashlib.sha256(helper.encode()).hexdigest())
    name = 'market_lead_build.json' if args.lead else ('market_gate2_build.json' if args.funded else 'market_gate_build.json')
    (ROOT / 'results' / name).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
