"""Frozen F20 sale-race experiments based on all 23 current public defeats."""
import hashlib,json
from pathlib import Path
from research_top100 import write

def main():
    parent=Path('candidates/f19_market2.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='b264030ccb0bb26da379c25bbfda7b1b6f40c03840045f29dc22476a75a5a516'
    layer=Path('frontier20_race.py').read_bytes();rows={}
    for name,reactive,look in [('f20_react6',True,6),('f20_ready3',False,3),('f20_ready6',False,6)]:
        data=parent+f'\n_F20_REACTIVE={reactive!r}\n_F20_LOOK={look}\n'.encode()+layer
        compile(data,name,'exec');path=Path('candidates',name+'.py')
        assert not path.exists() or path.read_bytes()==data
        path.write_bytes(data);rows[name]=dict(reactive=reactive,look=look,sha256=hashlib.sha256(data).hexdigest())
    write(Path('results/frontier20/build.json'),rows);print(json.dumps(rows,indent=2))

if __name__=='__main__':main()
