"""Pair replay changes against the unchanged parent; never infer ladder strength."""
import json
from pathlib import Path
from statistics import mean
from research_top100 import write

ROOT=Path('results/frontier20')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def score(rows):return dict(games=len(rows),wins=sum(r['margin']>0 for r in rows),ties=sum(r['margin']==0 for r in rows),
    mean_margin=mean(r['margin'] for r in rows),errors=sum(bool(r['errors']) for r in rows),
    rival_retention_range=[min(r['rival_kept'] for r in rows),max(r['rival_kept'] for r in rows)])

def main():
    base=read(ROOT/'diagnostic_controls.json');changed=read(ROOT/'diagnostic_delivery.json')
    assert len(base)==46 and len(changed)==69
    if (ROOT/'diagnostic_value.json').exists():
        extra=read(ROOT/'diagnostic_value.json');assert len(extra)==23
        changed+=extra
    expected={(r['id'],r['seat']) for r in read(ROOT/'episodes.json')}
    for name in {r['agent'] for r in base+changed}:
        assert {(r['episode'],r['seat']) for r in base+changed if r['agent']==name}==expected
    for r in base+changed:assert r['steps']==720 and r['status']==['DONE','DONE'] and not r['errors']
    parent={r['episode']:r for r in base if r['agent']=='f19_market2'}
    # The appropriate original agent must reproduce its own historical loss.
    ids={r['id']:r['submission'] for r in read(ROOT/'selection.json')['own']}
    originals=[r for r in base if r['agent']==('f19_market2' if ids[r['episode']]==56714342 else 'f19_market1')]
    reproduction=[dict(episode=r['episode'],agent=r['agent'],margin=r['margin'],recorded_margin=r['recorded_margin'],exact=r['margin']==r['recorded_margin'] and r['rival']==r['rival_recorded']) for r in originals]
    names=sorted({r['agent'] for r in changed})
    loss=dict(interpretation='Outcome-selected frozen rival diagnostics. Comparison to F19 Market2 isolates each overlay; recorded margins mix two original agents.',
        original_agent_reproduction=reproduction,parent=score(list(parent.values())),variants={})
    for name in names:
        rows=[r for r in changed if r['agent']==name]
        loss['variants'][name]=dict(**score(rows),mean_paired_margin_gain=mean(r['margin']-parent[r['episode']]['margin'] for r in rows),
            parent_losses_flipped=sum(parent[r['episode']]['margin']<=0<r['margin'] for r in rows),
            parent_wins_lost=sum(r['margin']<=0<parent[r['episode']]['margin'] for r in rows),
            per_episode=[dict(episode=r['episode'],parent_margin=parent[r['episode']]['margin'],margin=r['margin'],gain=r['margin']-parent[r['episode']]['margin']) for r in rows])
    write(ROOT/'diagnostic_summary.json',loss)
    basic=dict(original_losses_reproduced=sum(r['exact'] for r in reproduction),loss_variants={n:{k:v for k,v in d.items() if k!='per_episode'} for n,d in loss['variants'].items()})
    gr=ROOT/'grigor'
    if not (gr/'stress.json').exists():
        print(json.dumps(basic,indent=2));return
    rows=read(gr/'stress.json');fixtures=read(gr/'episodes.json')
    expected={(r['id'],r['seat']) for r in fixtures};assert len(rows)==len(expected)*3
    for name in ('f20_delivery','f19_market1','f19_market2'):
        assert {(r['episode'],r['seat']) for r in rows if r['agent']==name}==expected
    for r in rows:assert r['steps']==720 and r['status']==['DONE','DONE'] and not r['errors']
    summary=dict(interpretation='Eight public games: four latest of each Grigor agent, chosen before results. Original recorded margins belong to his actual opponents. Rival actions are frozen and cannot respond: these outcomes do not verify beating his private reactive agent.',
        samples=fixtures,policies={name:score([r for r in rows if r['agent']==name]) for name in ('f20_delivery','f19_market1','f19_market2')},paired={})
    candidate={r['episode']:r for r in rows if r['agent']=='f20_delivery'}
    for name in ('f19_market1','f19_market2'):
        control={r['episode']:r for r in rows if r['agent']==name}
        summary['paired'][name]=dict(mean_margin_gain=mean(candidate[e]['margin']-control[e]['margin'] for e in candidate),
            per_episode=[dict(episode=e,candidate_margin=candidate[e]['margin'],control_margin=control[e]['margin'],gain=candidate[e]['margin']-control[e]['margin']) for e in sorted(candidate)])
    write(gr/'stress_summary.json',summary)
    print(json.dumps(dict(basic,grigor=summary['policies']),indent=2))

if __name__=='__main__':main()
