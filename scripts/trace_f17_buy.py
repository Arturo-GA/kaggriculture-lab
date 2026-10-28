"""Locate the policy layer introducing a disputed purchase on an exact replay."""
import contextlib,gzip,io,json,sys
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make
    from kaggle_environments.agent import get_last_callable

data=json.load(gzip.open('vendor/live_f16/episode-114243937-replay.json.gz','rt',encoding='utf-8'))
fn=get_last_callable(Path('candidates/f16_repaired.py').read_text(encoding='utf-8'))
rows=[];trace=[]
def profile(frame,event,arg):
    if event=='return' and isinstance(arg,dict) and 'market' in arg:
        market=json.loads(json.dumps(arg['market']))
        if not trace or trace[-1]['market']!=market:
            trace.append(dict(function=frame.f_code.co_name,line=frame.f_code.co_firstlineno,market=market))
def p0(obs,cfg):return data['steps'][int(obs['step'])+1][0]['action']
def p1(obs,cfg):
    t=int(obs['step'])
    if t<=296:
        if t==296:sys.setprofile(profile)
        a=fn(obs,cfg)
        sys.setprofile(None)
        if t==296:
            g=fn.__globals__;rows.append(dict(trace=trace,action=a,native=g['_IMPL'].chassis.players[1]))
    return data['steps'][t+1][1]['action']
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    env=make('kaggriculture',configuration=dict(data['configuration'],seed=data['info']['seed']),debug=True)
    env.run([p0,p1])
Path('results/frontier17/buy_trace.json').write_text(json.dumps(rows,indent=2,default=str)+'\n',encoding='utf-8')
print(json.dumps(trace,indent=2))
