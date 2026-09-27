"""Trace swallowed upstream exceptions without changing the failed candidate's actions."""
import contextlib,io,json,traceback
from pathlib import Path


def main():
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    fn=get_last_callable(Path('candidates/f16_selected.py').read_text(encoding='utf-8'))
    ns=fn.__globals__;original=ns['_s839_apply'];errors=[]
    def traced(obs,action):
        try:return original(obs,action)
        except Exception as ex:
            errors.append(dict(step=obs['step'],market=action.get('market'),error=repr(ex),traceback=traceback.format_exc()))
            raise
    ns['_s839_apply']=traced
    rival=get_last_callable(Path('candidates/f15_e81.py').read_text(encoding='utf-8'))
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        env=make('kaggriculture',configuration={'seed':16102,'episodeSteps':720},debug=True)
        env.run([fn,rival])
    Path('results/frontier16/upstream_bug.json').write_text(json.dumps(errors,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(errors,indent=2))


if __name__=='__main__':main()
