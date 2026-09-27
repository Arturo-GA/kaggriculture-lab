"""Descriptive counterfactual replay results, explicitly separate from the gate."""
import json
from pathlib import Path
from evaluate import write_json_atomic

root=Path('results/frontier17')
rows=json.loads((root/'combined_diagnostic.json').read_text(encoding='utf-8'))
control={r['episode']:r for r in rows if r['agent']=='f16_repaired'}
candidate=[r for r in rows if r['agent']=='f17_combined']
assert len(control)==len(candidate)==21
assert all(r['margin']==r['recorded_margin'] and r['rival_kept']==1 for r in control.values())
out=[]
for r in candidate:
    c=control[r['episode']]
    out.append(dict(episode=r['episode'],opponent=r['opponent'],before=c['margin'],after=r['margin'],
        delta=r['margin']-c['margin'],own_cash_delta=r['own']-c['own'],rival_cash_delta=r['rival']-c['rival'],
        rival_kept=r['rival_kept'],errors=r['errors'],status=r['status']))
result=dict(games=21,original_losses=17,original_wins=4,losses_flipped=sum(r['before']<0<r['after'] for r in out),
    wins_lost=sum(r['after']<=0<r['before'] for r in out),improved=sum(r['delta']>0 for r in out),
    worsened=sum(r['delta']<0 for r in out),unchanged=sum(r['delta']==0 for r in out),
    mean_margin_gain=sum(r['delta'] for r in out)/len(out),
    warning='Opponents are recorded action streams and cannot react. Selected set is loss-heavy, not a random leaderboard sample. Rival cash preservation does not make it a competitive strength estimate.',rows=out)
write_json_atomic(root/'diagnostic_summary.json',json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
