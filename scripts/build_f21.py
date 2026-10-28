"""Final bounded sale-size experiment; keep F20 source and evidence immutable."""
from pathlib import Path
from datetime import datetime,timezone
from release_f20 import read,write,digest

ROOT=Path('results/frontier21')

def main():
    ROOT.mkdir(exist_ok=True)
    source=Path('candidates/f20_fill.py').read_bytes()
    assert digest('candidates/f20_fill.py')=='9924b8f2dec2930a046e0edee28463f6cda2e64453252e04bfeba2d50d5a2a8a'
    old=b'if not 0<extra<=8:continue'
    assert source.count(old)==1
    candidates={}
    for cap in (12,16):
        name=f'f21_cap{cap}'
        data=source.replace(old,f'if not 0<extra<={cap}:continue'.encode())
        compile(data,name,'exec')
        path=Path('candidates',name+'.py')
        assert not path.exists() or path.read_bytes()==data
        path.write_bytes(data)
        candidates[name]=dict(cap=cap,sha256=digest(path),parent='f20_fill')
    write(ROOT/'development_plan.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),
        candidates=candidates,control='f20_value',control_sha256=digest('candidates/f20_value.py'),
        opponents=['f20_value','f19_market2','n30b_haodou092_531a42','n30b_evgendvorkin_8ddb01','n23_arsgorynich_4f8637'],
        seeds=[20201,20206],seats=[0,1],games=60,
        rationale='Test selling slightly larger covered residual lots (12 or16 versus8 units). Preserve production, feed controls, similarity threshold, sale window, order count, and existing product exclusions.',
        selection='Development only: require strictly more win/tie points than f20_value, then choose highest points, then smaller cap. Freeze the selected source before new holdout seeds. If neither improves, use already-validated f20_fill as explicitly authorized by user.',
        authorization='User: osea puede ser un poquito mejor vasta y si no puedes envia la que empata nomas',
        deadline_utc='2026-09-30T23:59:00Z',target_submit_by_utc='2026-09-30T23:45:00Z'))
    print(candidates)

if __name__=='__main__':main()
