"""All-turn differential test of the compatibility fix on a previously failing world."""
import argparse,contextlib,copy,io,json
from pathlib import Path


def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=16102);a=p.parse_args()
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    def load(n):return get_last_callable(Path('candidates',n+'.py').read_text(encoding='utf-8'))
    old,new,rival=load('f16_selected'),load('f16_repaired'),load('f15_e81');calls=0
    def shadow(obs,config):
        nonlocal calls
        x=old(copy.deepcopy(obs),config);y=new(copy.deepcopy(obs),config)
        assert x==y,(obs['step'],x,y);calls+=1;return y
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        env=make('kaggriculture',configuration={'seed':a.seed,'episodeSteps':720},debug=True)
        last=env.run([shadow,rival])[-1]
    assert calls==719 and [s['status'] for s in last]==['DONE','DONE']
    errors={k:v for k,v in new.telemetry.items() if ('error' in k or 'fallback' in k) and v}
    result=dict(seed=a.seed,calls=calls,actions_identical=True,old_s839_errors=old.telemetry['upstream_S839_REPORT_errors'],
        explicit_hole_skips=new.telemetry['f16_preemption_hole_skips'],nonzero_errors=errors)
    assert result['old_s839_errors']==result['explicit_hole_skips']>0 and not errors
    Path(f'results/frontier16/repaired/repair_check_{a.seed}.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
