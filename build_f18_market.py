"""Original F17 input-search ablations: smaller quantities and bounded rival scenarios."""
import ast,hashlib,json
from pathlib import Path


def main():
    parent=Path('candidates/f17_selected.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='62b766886208e572462c19f45706cf9d0eded7d048c39a55a6093212bd72426f'
    source=Path('frontier17_input_market.py').read_text(encoding='utf-8')
    fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='_f17_input_apply')
    layer='\n'.join(source.splitlines()[fn.lineno-1:fn.end_lineno])+'\n'
    layer=layer.replace('if room<8:','if room<min(_F18_QS):').replace('for q in (8,16,32,48):','for q in _F18_QS:')
    layer=layer.replace('best<2','best<_F18_MIN_GAIN')
    variants={
        'f18_micro':((1,2,4,8,16,32,48),.5,False),
        'f18_micro_robust':((1,2,4,8,16,32,48),.5,True),
        'f18_small':((1,2,4,8,16),.5,False),
    }
    rows={}
    for name,(qs,min_gain,robust) in variants.items():
        settings=f'\n_F18_QS={qs!r}\n_F18_MIN_GAIN={min_gain!r}\n_F17_INPUT_ROBUST={robust!r}\n'
        # Rebind the helper looked up by F17, then export a wrapper as the last callable.
        tail='\n_F18_MICRO_PARENT=agent\ndef agent(observation,configuration=None):\n    return _F18_MICRO_PARENT(observation,configuration)\nagent.telemetry=_F18_MICRO_PARENT.telemetry\nagent=globals().pop("agent")\n'
        data=parent+b'\n# Original Arturo-GA input-search ablation, Apache-2.0.\n'+(settings+layer+tail).encode()
        compile(data,name,'exec');Path('candidates',name+'.py').write_bytes(data)
        rows[name]=dict(sha256=hashlib.sha256(data).hexdigest(),quantities=qs,min_gain=min_gain,rival_scenarios=2 if robust else 1)
    Path('results/frontier18/market_build.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(rows,indent=2))


if __name__=='__main__':main()
