import argparse
import hashlib
import json
from pathlib import Path


def build(model=None):
    source=Path('candidates/auction_joint_risk.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()=='8906f6dbbf065b62e6d0af4a74f504f3828549c57f57c626e86552b0c7bc3178'
    helper=Path('frontier_gate.py').read_text()
    weights=json.loads(Path(model).read_text()) if model else None
    targets=[('frontier',None)] if weights else [('frontier_control',0),('frontier_force',1)]
    records={}
    for name,force in targets:
        text=source.decode()+f'\n_FRONTIER_FORCE={force!r}\n_FRONTIER_MODEL={weights!r}\n'+helper
        compile(text,name,'exec');Path('candidates',name+'.py').write_bytes(text.encode())
        records[name]=hashlib.sha256(text.encode()).hexdigest()
    Path('results/gold/frontier_'+('model' if weights else 'forced')+'_build.json').write_text(json.dumps(records,indent=2)+'\n')
    return records


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--model');args=parser.parse_args()
    print(build(args.model))
