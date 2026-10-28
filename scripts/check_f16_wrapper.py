"""Assert behavior-neutral telemetry instrumentation for every turn of a complete official game."""
import contextlib,copy,io,json
from pathlib import Path


def main():
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments import make
        from kaggle_environments.agent import get_last_callable
    raw=get_last_callable(Path('candidates/f16_new_both.py').read_text(encoding='utf-8'))
    release=get_last_callable(Path('candidates/f16_selected.py').read_text(encoding='utf-8'))
    rival=get_last_callable(Path('candidates/f15_e81.py').read_text(encoding='utf-8'))
    calls=0
    def shadow(obs,config):
        nonlocal calls
        a=raw(copy.deepcopy(obs),config);b=release(copy.deepcopy(obs),config)
        assert a==b,(obs['step'],a,b)
        calls+=1
        return b
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
        env=make('kaggriculture',configuration={'seed':16902,'episodeSteps':720},debug=True)
        last=env.run([shadow,rival])[-1]
    assert calls==719 and [s['status'] for s in last]==['DONE','DONE']
    result=dict(seed=16902,calls=calls,actions_identical=True,telemetry=release.telemetry)
    errors={k:v for k,v in release.telemetry.items() if ('error' in k or 'fallback' in k) and v}
    result['nonzero_errors']=errors
    Path('results/frontier16/wrapper_check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2));assert not errors


if __name__=='__main__':main()
