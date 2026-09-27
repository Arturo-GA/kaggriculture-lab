"""Reproducible experiments from the frozen deployed F16, never overwrite it."""
import hashlib,json
from pathlib import Path

PARENT='f16_repaired'
PIN='0c6ac464ec556dc96a045c6575e718bb3aa77a153a97f9bae506eec3a32807cd'

def main():
    parent=Path('candidates',PARENT+'.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()==PIN
    rows={}
    for mode in ('cancel','close'):
        name='f17_'+mode
        data=parent+b'\n# Original modifications by Arturo-GA, September 27, 2026. Apache-2.0.\n'
        data+=f'_F17_MODE={mode!r}\n'.encode()+Path('frontier17_roundtrip.py').read_bytes()
        compile(data,name,'exec');Path('candidates',name+'.py').write_bytes(data)
        rows[name]=dict(sha256=hashlib.sha256(data).hexdigest(),mode=mode)
    for mode in ('cycle','robust'):
        name='f17_'+mode
        data=parent+b'\n# Original modifications by Arturo-GA, September 27, 2026. Apache-2.0.\n'
        data+=f'_F17_INPUT_ROBUST={mode=="robust"!r}\n'.encode()+Path('frontier17_input_market.py').read_bytes()
        compile(data,name,'exec');Path('candidates',name+'.py').write_bytes(data)
        rows[name]=dict(sha256=hashlib.sha256(data).hexdigest(),mode=mode)
    data=Path('candidates/f17_cancel.py').read_bytes()+b'\n_F17_INPUT_ROBUST=False\n'+Path('frontier17_input_market.py').read_bytes()
    name='f17_combined';compile(data,name,'exec');Path('candidates',name+'.py').write_bytes(data)
    rows[name]=dict(sha256=hashlib.sha256(data).hexdigest(),mode='cancel+cycle')
    Path('results/frontier17/build.json').write_text(json.dumps(dict(parent=PARENT,parent_sha256=PIN,variants=rows),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(rows))

if __name__=='__main__':main()
