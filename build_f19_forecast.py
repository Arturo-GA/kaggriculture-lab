import base64,gzip,hashlib,json,zlib
from pathlib import Path
from research_top100 import write

def main():
    root=Path('results/frontier19');data=gzip.decompress((root/'sale_motifs.json.gz').read_bytes())
    manifest=json.loads((root/'motif_manifest.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(data).hexdigest()==manifest['data_sha256']
    excluded=set(manifest['excluded_episodes']);assert not any(r['episode'] in excluded for r in json.loads(data))
    parent=Path('candidates/f19_robust.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='416a46b1648dd3647a26417bbac411a08697f5ce9cf02555830dc5e11b118791'
    blob=base64.b85encode(zlib.compress(data,9)).decode();report={}
    for name,precision,advantage in [('f19_recent65',.65,0),('f19_recent80',.8,2)]:
        settings=f'\n_F19_FORECAST_BLOB={blob!r}\n_F19_FORECAST_PRECISION={precision!r}\n_F19_FORECAST_ADVANTAGE={advantage!r}\n'
        source=parent+settings.encode()+Path('frontier19_forecast.py').read_bytes();compile(source,name,'exec')
        p=Path('candidates',name+'.py');assert not p.exists() or p.read_bytes()==source
        p.write_bytes(source);report[name]=dict(sha256=hashlib.sha256(source).hexdigest(),precision=precision,advantage=advantage,data_sha256=manifest['data_sha256'])
    write(root/'forecast_build.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
