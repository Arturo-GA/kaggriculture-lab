"""Post-selection diagnostic; inspecting a failure never changes frozen results."""
import argparse, contextlib, io, json
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,required=True);p.add_argument('--opponent',default='f19_market2');args=p.parse_args()
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    fn=get_last_callable(Path('candidates/f20_delivery.py').read_text(encoding='utf-8'))
    opponent=get_last_callable(Path('candidates',args.opponent+'.py').read_text(encoding='utf-8'))
    ns=fn.__globals__;worker=ns['_v233_worker'];rows=[]
    def observed(obs,actor,targets):
        result=worker(obs,actor,targets)
        original=ns['_F20D_WORKER'](obs,actor,targets)
        if original!=result:
            farm=obs['farms'][obs['player']]
            rows.append(dict(step=int(obs['step']),actor=actor,original=original,proposal=result,
                prices=dict(obs['market']['prices']),inventory=dict(obs['private']['inventories'][actor]),
                standing_wool=sum(farm['tiles'][y][x].get('yield_units',0) for x,y in targets),
                shops=obs['town']['unlocked_shops']))
        return result
    ns['_v233_worker']=observed
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        env=make('kaggriculture',configuration={'episodeSteps':720,'seed':args.seed},debug=True)
        final=env.run([fn,opponent])[-1]
    report=dict(seed=args.seed,opponent=args.opponent,rewards=[r['reward'] for r in final],rows=rows,
        interpretation='Exploratory diagnosis after seeing a held-out failure. Any resulting new policy requires separate new seeds. Original selection criteria and results stay unchanged.')
    path=Path('results/frontier20',f'trace-{args.seed}-{args.opponent}.json')
    path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('rewards',report['rewards'],'changed worker actions',len(rows))
    for r in rows:print(r['step'],r['actor'],r['original'],r['proposal'],'quotes',r['prices']['WOOL'],r['prices']['FERTILIZER'],'cargo',r['inventory'])

if __name__=='__main__':main()
