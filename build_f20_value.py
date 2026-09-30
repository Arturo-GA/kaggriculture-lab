import hashlib,json
from pathlib import Path

def main():
    base=Path('candidates/f20_delivery.py').read_bytes()
    assert hashlib.sha256(base).hexdigest()=='f6af68946f9e4e1bb80a9365e75f0efc4a536776ec0a56c2d422ed469af25ae0'
    data=base+b'\n'+Path('frontier20_value.py').read_bytes();compile(data,'f20_value','exec')
    p=Path('candidates/f20_value.py');assert not p.exists() or p.read_bytes()==data;p.write_bytes(data)
    report=dict(candidate='f20_value',sha256=hashlib.sha256(data).hexdigest(),parent_sha256=hashlib.sha256(base).hexdigest(),
        rationale='Earlier urgent wool delivery lost fertilizer value in a market whose wool price stayed flat. Compare the observable wool batch price exposure with optional fertilizer value.',
        adaptive_scope='Original Frontier20 holdout results remain intact. This new policy was designed after inspecting seed20104 and must be evaluated on a separately frozen fresh-seed panel.')
    Path('results/frontier20/value_build.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
