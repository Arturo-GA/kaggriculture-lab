import hashlib,json
from pathlib import Path
from research_top100 import write

def main():
    parent=Path('candidates/f18_small.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='d9289a3e55624596ab5c2a8368359542e09249ae7fd64391d506bf82daeec135'
    report={}
    for name,gain,ratio in [('f19_herd400b',400,1.1),('f19_herd1000b',1000,1.2)]:
        data=parent+b'\n'+Path('frontier18_feed.py').read_bytes()+f'\n_F19_HERD_GAIN={gain}\n_F19_HERD_RATIO={ratio}\n'.encode()+Path('frontier19_herd.py').read_bytes()
        compile(data,name,'exec');p=Path('candidates',name+'.py');assert not p.exists() or p.read_bytes()==data
        p.write_bytes(data);report[name]=hashlib.sha256(data).hexdigest()
    write(Path('results/frontier19/herd_build.json'),report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
