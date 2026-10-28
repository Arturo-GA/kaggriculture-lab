"""Test the newer public 14-route library within our existing reactive controller.

Public schedules: yhay81, Shop Router 0911 Simple. Retain V37's Apache notices.
This is an experiment; changing route libraries can invalidate controller assumptions.
"""
import ast
import base64
import hashlib
import json
from pathlib import Path
import zlib


def main():
    baseline=Path('baseline/v37.py').read_text(encoding='utf-8')
    donor=Path('candidates/router.py').read_text(encoding='utf-8')
    tree=ast.parse(donor)
    assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and
                    any(isinstance(t,ast.Name) and t.id=='_DATA' for t in n.targets))
    encoded=ast.literal_eval(assignment.value.args[0].args[0].args[0])
    data=json.loads(zlib.decompress(base64.b85decode(encoded)))
    tapes=data['tapes']
    assert len(tapes)==14 and all(len(t)==719 for t in tapes)
    payload={'base':tapes[0], 'patches':{str(i):[[t,a] for t,a in enumerate(tape) if a!=tapes[0][t]]
                                       for i,tape in enumerate(tapes) if i}}
    encoded=base64.b85encode(zlib.compress(json.dumps(payload,separators=(',',':')).encode())).decode()
    original_tree=ast.parse(baseline)
    node=next(n for n in original_tree.body if isinstance(n,ast.Assign) and
              any(isinstance(t,ast.Name) and t.id=='_PAYLOAD' for t in n.targets))
    source=baseline.replace(ast.get_source_segment(baseline,node),
        '_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('+repr(encoded)+')))')
    route_map={tuple(row['shops']):row['plan'] for row in data['routes']}
    router=next(n for n in original_tree.body if isinstance(n,ast.FunctionDef) and n.name=='_router')
    replacement='''def _router(observation,step,state):
    if step>=144 and not state.get('day6'):
        shops=_get(_get(observation,'town',{}),'unlocked_shops',[]) or []
        state['route']=ROUTE_MAP.get(tuple(shops[:2]),0)
        state['day6']=True
    if step>=648 and not state.get('day27'):
        state['route']=2
        state['day27']=True
    return state.get('route',0)
'''.replace('ROUTE_MAP',repr(route_map))
    source=source.replace(ast.get_source_segment(baseline,router),replacement)
    variants={'routes14':source,'routes14m6':source.replace(
        'if 288 <= step < 696:_R37_HORIZONS[player] = 4',
        'if 288 <= step < 696:_R37_HORIZONS[player] = 6 if 336 <= step < 648 and state["streak"] >= 6 else 4')}
    records={}
    for name,text in variants.items():
        text=('# Modified 2026-09-12 by Arturo-GA: experimental integration of yhay81\n'
              '# Shop Router 0911 Simple 14-route data and shop mapping into V37.\n'
              '# All original Apache-2.0 notices retained; see NOTICE.md.\n'+text)
        compile(text,name+'.py','exec')
        Path('candidates',name+'.py').write_bytes(text.encode('utf-8'))
        records[name]=hashlib.sha256(text.encode()).hexdigest()
    Path('results/routes14_build.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records))


if __name__=='__main__':
    main()
