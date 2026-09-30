"""Newest public loss: exact accounting and explicitly frozen-rival diagnostics."""
from pathlib import Path
from release_f20 import read,write
from audit_f17_replays import audit
from replay_panel import game

ROOT=Path('results/frontier21')

def main(prefix='latest_loss'):
    live=read(ROOT/f'{prefix}.json');raw=read(ROOT/f'{prefix}_download.json')
    if not live['losses']:return
    loss=live['losses'][0];me=next(a for a in loss['agents'] if a['submission_id']==live['submission'])
    opponent=next(a for a in loss['agents'] if a['submission_id']!=live['submission'])
    meta=dict(id=loss['id'],seat=me['index'],submission=live['submission'],margin=me['reward']-opponent['reward'],
        op_name=opponent['team_name'],op_sub=opponent['submission_id'],op_rank=None,raw_path=raw['path'],raw_sha256=raw['sha256'])
    row=audit(meta);write(ROOT/f'{prefix}_audit.json',row)
    a=me['index'];b=1-a;money=row['money'];units=row['units']
    products={k[5:] for bank in money for k in bank if k.startswith('SELL_')}
    product_rows=[]
    for item in products:
        net=lambda seat:money[seat].get('SELL_'+item,0)-money[seat].get('BUY_PRODUCT_'+item,0)
        product_rows.append(dict(item=item,net_cashflow_gap=net(a)-net(b),
            sold_units=[u.get('SELL_'+item,0) for u in units],
            average_sale_price=[round(m.get('SELL_'+item,0)/max(1,u.get('SELL_'+item,0)),3) for m,u in zip(money,units)]))
    product_rows.sort(key=lambda r:r['net_cashflow_gap'])
    summary=dict(episode=loss['id'],opponent=opponent['team_name'],margin=meta['margin'],reproduced_exactly=row['reproduced_exactly'],
        product_cashflows=product_rows,physical=row['physical'],snapshots=row['snapshots'],
        caveat='Product net cashflow excludes seed/animal/labor/land costs; it is not total profit. Counterfactual replay opponents cannot react.')
    write(ROOT/f'{prefix}_summary.json',summary)
    print('Exact loss accounting',meta,flush=True);print('Product gaps',product_rows,flush=True)
    diagnostics=[]
    for name in ('f20_value','f20_fill','f21_cap12'):
        result=game((f'candidates/{name}.py',loss['id'],a,str(Path(raw['path']).parent)))
        diagnostics.append(result);write(ROOT/f'{prefix}_diagnostics.json',diagnostics)
        print('Frozen-rival diagnosis',name,result['margin'],'own',result['own'],'rival',result['rival'],flush=True)
    original=diagnostics[0]
    assert original['own']==me['reward'] and original['rival']==opponent['reward'],'Do not treat a non-reproducing replay as controlled evidence.'
    assert all(r['status']==['DONE','DONE'] and r['steps']==720 and not r['errors'] for r in diagnostics)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--prefix',default='latest_loss');a=ap.parse_args()
    main(a.prefix)
