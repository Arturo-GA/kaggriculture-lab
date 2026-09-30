import hashlib,json
from pathlib import Path
from research_top100 import write

def main():
    parent=Path('candidates/f19_market2.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='b264030ccb0bb26da379c25bbfda7b1b6f40c03840045f29dc22476a75a5a516'
    layer=Path('frontier20_delivery.py').read_bytes();rows={}
    for name,wool,fill in [('f20_woolfast',True,False),('f20_fill',False,True),('f20_delivery',True,True)]:
        data=parent+f'\n_F20D_WOOL={wool!r}\n_F20D_FILL={fill!r}\n'.encode()+layer
        compile(data,name,'exec');path=Path('candidates',name+'.py');assert not path.exists() or path.read_bytes()==data
        path.write_bytes(data);rows[name]=dict(wool=wool,fill=fill,sha256=hashlib.sha256(data).hexdigest())
    write(Path('results/frontier20/delivery_build.json'),rows);print(json.dumps(rows,indent=2))

if __name__=='__main__':main()
