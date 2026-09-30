"""Frozen exploratory F19 variants; revisions use new names and fingerprints."""
import hashlib,json
from pathlib import Path
from research_top100 import write

def main():
    parent=Path('candidates/f18_small.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='d9289a3e55624596ab5c2a8368359542e09249ae7fd64391d506bf82daeec135'
    feed=Path('frontier18_feed.py').read_bytes();market=Path('frontier19_market.py').read_bytes()
    variants={
        'f19_market2':b"_F19_MARKET_MODE='last'\n_F19_MARKET_DEPTH=2\n"+market,
        'f19_market8':b"_F19_MARKET_MODE='last'\n_F19_MARKET_DEPTH=8\n"+market,
        'f19_robust':b"_F19_MARKET_MODE='robust'\n_F19_MARKET_DEPTH=1\n"+market,
        'f19_noextras':b'def _f17_input_apply(obs,action):return action\n_F19_MARKET_MODE="last"\n_F19_MARKET_DEPTH=8\n'+market,
    }
    report={}
    for name,layer in variants.items():
        data=parent+b'\n'+feed+b'\n'+layer;compile(data,name,'exec')
        p=Path('candidates',name+'.py')
        assert not p.exists() or p.read_bytes()==data,'Never mutate a tested policy.'
        p.write_bytes(data);report[name]=hashlib.sha256(data).hexdigest()
    write(Path('results/frontier19/market_build.json'),report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
