"""Preserve exact research inputs; a snapshot does not promote any prototype."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path

ROOT=Path('results/frontier20')
ARCHIVE=ROOT/'source_snapshot.json.xz'

def main():
    p=argparse.ArgumentParser();p.add_argument('--restore',nargs='+');args=p.parse_args()
    if args.restore:
        payload=json.loads(lzma.decompress(ARCHIVE.read_bytes()))
        manifest=json.loads((ROOT/'source_snapshot_manifest.json').read_text(encoding='utf-8'))
        assert hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()==manifest['archive_sha256']
        for name in args.restore:
            assert Path(name).name==name and name.replace('_','').isalnum()
            key='candidates/'+name+'.py';raw=payload[key].encode('utf-8');target=Path(key)
            assert hashlib.sha256(raw).hexdigest()==manifest['entries'][key]
            if target.exists():assert target.read_bytes()==raw,'Refusing to overwrite a different source'
            else:target.write_bytes(raw)
            print(key,manifest['entries'][key])
        return
    assert not ARCHIVE.exists(),'Research snapshot is immutable'
    plan=json.loads((ROOT/'plan.json').read_text(encoding='utf-8'))
    paths=set(Path('candidates').glob('f20_*.py'))
    paths.update(Path('candidates',n+'.py') for n in plan['hashes'])
    paths.update(p for p in Path('attribution').rglob('*') if p.is_file() and p.suffix in ('.md','.txt'))
    paths.update(p for p in Path('vendor/f20_public').rglob('*') if p.is_file() and (p.name=='kernel-metadata.json' or p.parent.name=='extracted_licenses'))
    paths=sorted(paths);payload={p.as_posix():p.read_bytes().decode('utf-8') for p in paths}
    ARCHIVE.write_bytes(lzma.compress(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode('utf-8'),preset=6))
    assert json.loads(lzma.decompress(ARCHIVE.read_bytes()))==payload
    manifest=dict(archive_sha256=hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),compressed_bytes=ARCHIVE.stat().st_size,
        entries={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        purpose='Private research reproducibility, including rejected and untested prototypes. Does not mark them as validated or deployed. Public-source metadata and available license notices preserved.')
    (ROOT/'source_snapshot_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Preserved',len(paths),'files in',manifest['compressed_bytes'],'bytes')

if __name__=='__main__':main()
