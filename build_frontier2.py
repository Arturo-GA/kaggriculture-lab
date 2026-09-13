"""Independent delivery interventions on frozen Frontier; no retraining on holdout."""
import hashlib
import json
import argparse
from pathlib import Path


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--ablations',action='store_true');args=parser.parse_args()
    parent=Path('candidates/frontier.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='a485d1c0a44ae989417b39178defa5096837b03b850a7bc8db8b6458599dad1c'
    helper=Path('frontier_deliveries.py').read_text()
    receipt={}
    variants=[('frontier2_no_delivery',10000000,1)] if args.ablations else [('frontier2_early',250,1),('frontier2_selective',600,1),('frontier2_stagger',250,2)]
    for name,threshold,stagger in variants:
        source=parent.decode()
        anchor='plan=_au_route(pos,start,jobs,prices,power,bias,input_cap=cap)'
        assert source.count(anchor)==1
        source=source.replace(anchor,'plan=_au_route(pos,start,jobs,prices,power,bias,end=719-(actor%_F2_STAGGER),input_cap=cap)')
        source+=f'\n_F2_THRESHOLD={threshold}\n_F2_STAGGER={stagger}\n_FRONTIER_FORCE=1\n'+helper
        compile(source,name,'exec');data=source.encode();Path('candidates',name+'.py').write_bytes(data)
        receipt[name]=dict(sha256=hashlib.sha256(data).hexdigest(),threshold=threshold,stagger=stagger,
                           selector='forced planner; old learned gate not reused for changed option')
    out=Path('results/frontier2');out.mkdir(exist_ok=True)
    (out/('ablation_build.json' if args.ablations else 'build.json')).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
