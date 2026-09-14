"""Build isolated opening/resource/capacity variants, preserving old artifacts."""
import ast
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path


def main():
    root=Path('results/frontier3');root.mkdir(exist_ok=True)
    parent=Path('candidates/frontier2_early.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='0bb0cddbb6e3883850138cbbd3dfc39e5fa285fd83c356a0e02391bebdbff33c'
    donor=Path('candidates/v41_review.py').read_bytes()
    assert hashlib.sha256(donor).hexdigest()=='8951ff93742015cba535b125223cf2e541bb7b602080fc4584f30c2613d210f3'
    wanted={'_r97_budget','_r124_labor_reserve','_r124_seed_budget','_r124_atomic'}
    text=donor.decode();tree=ast.parse(text)
    chunks=[ast.get_source_segment(text,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
    assert len(chunks)==len(wanted)
    helpers='\n\n'.join(chunks)
    helpers=helpers.replace('crop=c[1],birth=0','crop=c[1],birth=int(obs["step"])//24')
    helpers=helpers.replace('commands[actor],10,0,24,100','commands[actor],10,int(obs["step"])//24,24,100')
    credit='# Apache-2.0: funding/seed guards adapted from Ahmed Berat Ozer V41.\n# Opening lineage: Rayk Kretzschmar; integration/capacity solver: Arturo-GA.\n'
    helpers=credit+helpers+'\n'
    (root/'v41_funding_helpers.py').write_bytes(helpers.encode())
    old="_R42_OPENING=[['BUY_PRODUCT', 'WHEAT', 13], ['BUY_PRODUCT', 'WHEAT', 30], ['SELL', 'WHEAT', 30]]"
    new="_R42_OPENING=[['BUY_PRODUCT', 'WHEAT', 5], ['BUY_PRODUCT', 'WHEAT', 10], ['SELL', 'WHEAT', 60]]"
    source=parent.decode();assert source.count(old)==1
    source=credit+source.replace(old,new)
    variants={'frontier3_opening':source}
    for name,capacity in [('frontier3_funded',False),('frontier3_capacity',True)]:
        variants[name]=source+'\n'+helpers+'\n'+Path('frontier3_capacity.py').read_text(encoding='utf-8')+f'\n_F3_CAPACITY={capacity!r}\n'+Path('frontier3_resources.py').read_text(encoding='utf-8')
    receipt=dict(parent_sha256=hashlib.sha256(parent).hexdigest(),donor_sha256=hashlib.sha256(donor).hexdigest(),variants={})
    for name,source in variants.items():
        compile(source,name+'.py','exec');data=source.encode()
        Path('candidates',name+'.py').write_bytes(data)
        receipt['variants'][name]=hashlib.sha256(data).hexdigest()
    (root/'build.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    plan=dict(created_utc=datetime.now(timezone.utc).isoformat(),screen_candidates=[*variants,'frontier2_early'],
        screen_seeds=list(range(93001,93005)),screen_opponents=['v41_review','matched6','frontier2_early'],
        holdout_seeds=list(range(94001,94009)),holdout_opponents=['v41_review','matched6','frontier2_early','router','kaito','nagata','prvsiyan'],
        official_seeds=list(range(95001,95005)),cloud_seeds=[96001,96002],
        rule='Select on screen, freeze hash before holdout. Require positive paired score versus Frontier2, no net per-opponent score regression, >=50% direct score versus V41. Official and cloud callbacks below 1000ms; no reported errors/fallbacks or first-dawn hire shortfalls. C++ latency is diagnostic, not final runtime gate. No holdout retuning.',
        attribution='New opening and funding guards adapted from credited V41, general-day seed validation and terminal capacity allocation added here. Inherited ML critic unchanged and not retrained; no claim it remains optimal.',
        scope='Build, test and package the updated submission. Do not overwrite previous deployed source or archives.')
    path=root/'plan.json'
    if not path.exists():path.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
