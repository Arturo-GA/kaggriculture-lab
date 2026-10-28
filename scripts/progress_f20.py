"""Read-only compact progress of the frozen final panel."""
import json
from pathlib import Path

def main():
    root=Path('results/frontier20/value_gate')
    plan=json.loads((root/'plan.json').read_text(encoding='utf-8'))
    data=json.loads((root/'holdout.json').read_text(encoding='utf-8'));rows=data['rows']
    print('Progress',len(rows),'/',data['expected_games'],'complete',data['complete'])
    for name in plan['candidates']+plan['controls']:
        part=[r for r in rows if r['candidate']==name]
        if not part:continue
        errors=sum(any(v and ('error' in k.lower() or 'fallback' in k.lower()) for k,v in r['telemetry'].items()) for r in part)
        print(name,'games',len(part),'points',sum(r['win']+.5*r['tie'] for r in part),
            'WLT',[sum(r['margin']>0 for r in part),sum(r['margin']<0 for r in part),sum(r['margin']==0 for r in part)],
            'max_ms',round(max(r['max_call_ms'] for r in part),1),'error_games',errors)
    decision=root/'selection_decision.json'
    if decision.exists():print('Selected',json.loads(decision.read_text(encoding='utf-8'))['selected'])

if __name__=='__main__':main()
