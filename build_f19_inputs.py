"""Input-sizing ablations, retaining the original cash/capacity guards."""
import hashlib,json
from pathlib import Path
from research_top100 import write
def main():
    parent=Path('candidates/f18_small.py').read_bytes();assert hashlib.sha256(parent).hexdigest()=='d9289a3e55624596ab5c2a8368359542e09249ae7fd64391d506bf82daeec135'
    report={}
    for name,qs,robust in [('f19_balanced',(1,2,4,8,16,32),True),('f19_pressure',(1,2,4,8,16,32,48,64),False)]:
        settings=f'\n_F18_QS={qs!r}\n_F17_INPUT_ROBUST={robust!r}\n_F19_MARKET_MODE="robust"\n_F19_MARKET_DEPTH=1\n'
        data=parent+b'\n'+Path('frontier18_feed.py').read_bytes()+settings.encode()+Path('frontier19_market.py').read_bytes()
        compile(data,name,'exec');p=Path('candidates',name+'.py');assert not p.exists() or p.read_bytes()==data
        p.write_bytes(data);report[name]=dict(sha256=hashlib.sha256(data).hexdigest(),quantities=qs,robust_input=robust)
    write(Path('results/frontier19/input_build.json'),report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
