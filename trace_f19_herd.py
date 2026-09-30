import contextlib,io,json
from pathlib import Path

def main():
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    def load(n):return get_last_callable(Path('candidates',n+'.py').read_text(encoding='utf-8'),path=str(Path('candidates',n+'.py')))
    fn=load('f19_herd400b');ns=fn.__globals__;old=ns['_f19_herd'];events=[]
    def traced(obs,action):
        step=int(obs['step']);seat=int(obs['player']);st=ns['_F19_HERD_STATE'].get(seat,{})
        farm=obs['farms'][seat];cmds=[action['farmer']]+action['hands'];pos=[farm['farmer']]+farm['hands']
        for (t,i),(xy,before,after) in st.get('plan',{}).items():
            if t==step:events.append(dict(step=step,actor=i,expected_xy=xy,actual_xy=pos[i],before=before,after=after,actual=cmds[i],inventory=obs['private']['inventories'][i],tile=farm['tiles'][pos[i][1]][pos[i][0]]))
        return old(obs,action)
    ns['_f19_herd']=traced
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        env=make('kaggriculture',configuration={'seed':19002,'episodeSteps':720});last=env.run([fn,load('f18_small')])[-1]
    report=dict(events=events,telemetry=dict(fn.telemetry),rewards=[s['reward'] for s in last])
    Path('results/frontier19/herd_trace.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(events,indent=2))
if __name__=='__main__':main()
