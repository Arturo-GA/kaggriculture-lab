"""Assemble Frontier11 candidates: the last public wave before the 23 September 2026 notebook lock + the Lab layers.

The public field of 21-23 September converged on one family: Ahmed Berat Ozer's V55 (One More Wheat + prvsiyan's wheat
guard), shiiin9's "Your Market List Is an Order Book" (V55 + layer D, a best-response ordering of the market list
against a copy of the stack without D), and Dmitrii Gluzdov's "Herd-Safe Sale Window" and its forks on top of it.
Public bases (extracted as data, pinned by hash, excluded from Git) are listed in PINS; their Apache-2.0 notices are
kept byte for byte at the top of every derived file.

Selected (results/frontier11/): f11_pv_lock = prvsiyan's "The Soil Remembers Rain" agent of 22 September (sha 178ae0f7...,
itself haideptry's "2965 Master Hybrid Engine" + sale lookahead 4 + seed hedge 0 + queue compaction + late SELL-block
reorder, strongest in a 270-game round robin of the ten best new agents) with its entry point bound and the unchanged
Frontier5 lockstep appended.  The f11x_* variants were screened and are not exported.

Lab layers:
  f11  frontier11_order.py: scores D's orderings against three rival lists at once (a copy without D, an exact copy,
       a copy one level up) and plays the best weighted margin that loses ground against none of them.
  lock frontier5_lockstep.py: the Frontier5-10 lockstep, which against a copy of a D-stack is a level-2 response.
"""
import hashlib
import json
from pathlib import Path

PINS = {
    'n23_dmitriigluzdov_488913': '4889137f1adf',
    'n23_arsgorynich_4f8637': '4f8637a3e333',
    'n23_prvsiyan_178ae0': '178ae0f72764',
    'n23_wzhengbiao_f6175f': 'f6175fd1bc38',
    'n23_dmitriigluzdov_7ac1a2': '7ac1a2545ea2',
}


def load(name):
    data = Path('candidates', name + '.py').read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest.startswith(PINS[name]), (name, digest)
    return data.decode('utf-8')


def bind(src, entry, layer_file, tag):
    """Bind the base's real entry point (the Kaggle loader runs the last callable) and append a Lab layer."""
    assert ('def %s(' % entry) in src, entry
    layer = Path(layer_file).read_text(encoding='utf-8')
    parent = '_F11_PARENT' if 'frontier11' in layer_file else 'agent'
    nl = chr(10)
    head = src.rstrip(chr(13) + nl) + nl + nl + '# Frontier11 (%s): bind the public entry point before the Kaggriculture Lab layer' % tag + nl
    return head + parent + '=' + entry + nl + layer


VARIANTS = {
    'f11x_hs_rob': ('n23_dmitriigluzdov_488913', 'opening_liquidity_agent', 'f11', 'Herd-Safe + robust order response (exploratory)'),
    'f11x_hs_lock': ('n23_dmitriigluzdov_488913', 'opening_liquidity_agent', 'lock', 'Herd-Safe + Frontier5 lockstep (exploratory)'),
    'f11x_hs3_rob': ('n23_arsgorynich_4f8637', 'herdsafe_forecast_agent', 'f11', 'Herd-Safe v3 risk-aware feed + robust order response (exploratory)'),
    'f11x_hs3_lock': ('n23_arsgorynich_4f8637', 'herdsafe_forecast_agent', 'lock', 'Herd-Safe v3 risk-aware feed + Frontier5 lockstep (exploratory)'),
    'f11x_hs_br': ('n23_dmitriigluzdov_488913', 'opening_liquidity_agent', 'f11', 'Herd-Safe + level-2 best response to the exact copy (exploratory)', {'_F11_W': (0.0, 1.0, 0.0), '_F11_HARD': False}),
    'f11x_hs_mix': ('n23_dmitriigluzdov_488913', 'opening_liquidity_agent', 'f11', 'Herd-Safe + weighted three-model response, no hard floor (exploratory)', {'_F11_W': (1.0, 2.0, 1.0), '_F11_HARD': False}),
    'f11x_hs3_br': ('n23_arsgorynich_4f8637', 'herdsafe_forecast_agent', 'f11', 'Herd-Safe v3 forecast4 + level-2 best response to the exact copy (exploratory)', {'_F11_W': (0.0, 1.0, 0.0), '_F11_HARD': False}),
    'f11x_hs3_mix': ('n23_arsgorynich_4f8637', 'herdsafe_forecast_agent', 'f11', 'Herd-Safe v3 forecast4 + weighted three-model response, no hard floor (exploratory)', {'_F11_W': (1.0, 2.0, 1.0), '_F11_HARD': False}),
    'f11x_pv_lock': ('n23_prvsiyan_178ae0', '_final_sell_block_reorder_entrypoint', 'lock', 'prvsiyan Soil/Moon (22 Sep) + Frontier5 lockstep (exploratory)'),
    'f11x_pv_br': ('n23_prvsiyan_178ae0', '_final_sell_block_reorder_entrypoint', 'f11', 'prvsiyan Soil/Moon (22 Sep) + level-2 best response (exploratory)', {'_F11_W': (0.0, 1.0, 0.0), '_F11_HARD': False}),
    'f11x_wz_lock': ('n23_wzhengbiao_f6175f', 'v15_submission_entry', 'lock', 'wzhengbiao hybu (23 Sep) + Frontier5 lockstep (exploratory)'),
    'f11x_wz_br': ('n23_wzhengbiao_f6175f', 'v15_submission_entry', 'f11', 'wzhengbiao hybu (23 Sep) + level-2 best response (exploratory)', {'_F11_W': (0.0, 1.0, 0.0), '_F11_HARD': False}),
    'f11_pv_lock': ('n23_prvsiyan_178ae0', '_final_sell_block_reorder_entrypoint', 'lock', 'prvsiyan "The Soil Remembers Rain" (22 Sep) + Frontier5 lockstep; exported candidate'),
    'f11b_hs3_lock': ('n23_arsgorynich_4f8637', 'herdsafe_forecast_agent', 'lock', 'arsgorynich "Herd-Safe v3 forecast4" (23 Sep) + Frontier5 lockstep; exported second-slot candidate'),
    'f11x_gm_lock': ('n23_dmitriigluzdov_7ac1a2', 'rescue_agent', 'lock', 'Gluzdov "More Wheat, Smarter Sales" (22 Sep) + Frontier5 lockstep (exploratory third base)'),
}


def build(name):
    base, entry, layer, _ = VARIANTS[name][:4]
    out = bind(load(base), entry, {'f11': 'frontier11_order.py', 'lock': 'frontier5_lockstep.py'}[layer], name)
    for key, value in (VARIANTS[name][4] if len(VARIANTS[name]) > 4 else {}).items():
        out += '%s = %r' % (key, value) + chr(10)
    return out


def write(name, src):
    compile(src.replace('\r\n', '\n'), name, 'exec')
    Path('candidates', name + '.py').write_text(src, encoding='utf-8', newline='')
    print('wrote', name, len(src))


if __name__ == '__main__':
    manifest = {'pins': {k: hashlib.sha256(Path('candidates', k + '.py').read_bytes()).hexdigest() for k in PINS}, 'variants': {}}
    for name, (base, entry, layer, note, *extra) in VARIANTS.items():
        write(name, build(name))
        manifest['variants'][name] = dict(base=base, entry=entry, layer=layer, note=note, overrides=extra[0] if extra else {},
                                          sha256=hashlib.sha256(Path('candidates', name + '.py').read_bytes()).hexdigest())
    Path('results/frontier11').mkdir(parents=True, exist_ok=True)
    Path('results/frontier11/build.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2))
