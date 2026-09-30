"""Reuse the inherited generic six-animal worker, preserve its Apache notices."""
import ast,hashlib,json
from pathlib import Path
from research_top100 import write

def main():
    parent=Path('candidates/f18_small.py').read_bytes();s=parent.decode('utf-8')
    assert hashlib.sha256(parent).hexdigest()=='d9289a3e55624596ab5c2a8368359542e09249ae7fd64391d506bf82daeec135'
    fn=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name=='_v233_worker')
    worker=ast.get_source_segment(s,fn).replace('_v233_worker','_f19_goose_worker').replace('SHEEP','GOOSE').replace('WOOL','EGG').replace('PASTURE','COOP')
    worker=worker.replace("if hungry and not inv.get('WHEAT',0)","if step//24<29 and hungry and not inv.get('WHEAT',0)")
    worker=worker.replace("if not tile['fed_today'] and", "if step//24<29 and not tile['fed_today'] and").replace("elif not tile['cared_today']:","elif step//24<29 and not tile['cared_today']:")
    report={}
    for name,edge in [('f19_goose0c',0),('f19_goose5c',5000)]:
        data=parent+b'\n'+Path('frontier18_feed.py').read_bytes()+f'\n_F19_GOOSE_EDGE={edge}\n'.encode()+worker.encode()+b'\n'+Path('frontier19_goose.py').read_bytes()
        compile(data,name,'exec');p=Path('candidates',name+'.py');assert not p.exists() or p.read_bytes()==data
        p.write_bytes(data);report[name]=hashlib.sha256(data).hexdigest()
    write(Path('results/frontier19/goose_build.json'),report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
