"""Exact accounting of every available defeat of the latest two submissions."""
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
from audit_f17_replays import audit
from research_top100 import write

ROOT=Path('results/frontier20')

def main():
    s=json.loads((ROOT/'selection.json').read_text(encoding='utf-8'));assert s['complete']
    paths={r['id']:r['path'] for r in s['episodes']};out=ROOT/'loss_audit.json'
    rows=json.loads(out.read_text(encoding='utf-8'))['rows'] if out.exists() else []
    found={(r['id'],r['submission']) for r in rows}
    metas=[dict(r,raw_path=paths[r['id']]) for r in s['own'] if (r['id'],r['submission']) not in found]
    if metas:
        with ProcessPoolExecutor(max_workers=4) as pool:
            for f in as_completed([pool.submit(audit,m) for m in metas]):
                r=f.result();rows.append(r);write(out,dict(expected=len(s['own']),complete=len(rows)==len(s['own']),rows=rows))
                print('Audit',len(rows),'/',len(s['own']),r['id'],r['margin'],flush=True)
    summary=[]
    for r in rows:
        a,b=r['seat'],1-r['seat'];own=r['money'][a];opp=r['money'][b]
        gaps={k:(own.get(k,0)-opp.get(k,0))*(1 if k.startswith('SELL_') else -1) for k in own.keys()|opp.keys()}
        products={k[5:] for k in own.keys()|opp.keys() if k.startswith('SELL_')}
        net_products={item:((own.get('SELL_'+item,0)-own.get('BUY_PRODUCT_'+item,0))-
            (opp.get('SELL_'+item,0)-opp.get('BUY_PRODUCT_'+item,0))) for item in products}
        summary.append(dict(id=r['id'],submission=r['submission'],seed=r['seed'],seat=a,margin=r['margin'],op_rank=r['op_rank'],op_name=r['op_name'],
            revenue_gaps=sorted(gaps.items(),key=lambda kv:kv[1]),
            net_product_cashflow_gaps=sorted(net_products.items(),key=lambda kv:kv[1]),
            accounting_note='Net product cashflow deducts product purchases from sales. It excludes seed, animal, land and labor costs; it is not total economic profit.',
            physical=r['physical'][a],rival_physical=r['physical'][b],
            layout_288=r['snapshots']['288'],layout_648=r['snapshots']['648']))
    write(ROOT/'loss_summary.json',summary)
    for r in summary:
        print(r['submission'],r['id'],r['margin'],'rank',r['op_rank'],'GAPS',r['revenue_gaps'][:4],
              'FAILURES',{k:v for k,v in r['physical'].items() if any(s in k for s in ('overflow','without_food','market_failed','noop_'))})

if __name__=='__main__':main()
