"""Replace the old production tapes with a verified coherent public family."""
import ast,base64,gzip,hashlib,json,zlib
from pathlib import Path
from research_top100 import write

def main():
    root=Path('results/frontier19');raw=gzip.decompress((root/'portfolio_records.json.gz').read_bytes())
    meta=json.loads((root/'portfolio_manifest.json').read_text(encoding='utf-8'));assert hashlib.sha256(raw).hexdigest()==meta['data_sha256']
    rows=json.loads(raw);assert len({r['key'] for r in rows})==1
    excluded=set(meta['excluded_episodes']);assert not any(r['episode'] in excluded for r in rows)
    # One most recent route for each first-two-shop combination; tie by team
    # strength at the frozen snapshot, never by an individual game outcome.
    groups={}
    for r in rows:
        k=tuple(r['shops'])
        if k not in groups or (r['rank'],-r['episode'])<(groups[k]['rank'],-groups[k]['episode']):groups[k]=r
    rows=sorted(groups.values(),key=lambda r:(r['rank'],-r['episode']))
    blob=base64.b85encode(zlib.compress(json.dumps(rows,separators=(',',':')).encode(),9)).decode()
    parent=Path('candidates/f18_small.py').read_text(encoding='utf-8');tree=ast.parse(parent)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='make_agent')
    chassis='\n'.join(parent.splitlines()[:fn.end_lineno])+'\n'
    report={}
    for name,lead in [('f19_routes_plain',False),('f19_routes_lead',True)]:
        data=chassis.encode()+f'\n_F19_ROUTE_BLOB={blob!r}\n_F19_ROUTE_SELL_LEAD={lead!r}\n'.encode()+Path('frontier19_routes.py').read_bytes()
        compile(data,name,'exec');p=Path('candidates',name+'.py');assert not p.exists() or p.read_bytes()==data
        p.write_bytes(data);report[name]=dict(sha256=hashlib.sha256(data).hexdigest(),routes=len(rows),sell_lead=lead,bytes=len(data),data_sha256=meta['data_sha256'])
    write(root/'route_build.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
