"""Preserve exact experimental sources compactly, including rejected prototypes."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path

ROOT = Path('results/frontier19')
ARCHIVE = ROOT / 'source_snapshot.json.xz'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--restore', nargs='+', metavar='CANDIDATE')
    args = p.parse_args()
    if args.restore:
        payload = json.loads(lzma.decompress(ARCHIVE.read_bytes()))
        for name in args.restore:
            assert name.startswith(('f19_', 'n30_')) and Path(name).name == name
            key = 'candidates/' + name + '.py'
            raw = payload[key].encode('utf-8')
            target = Path(key)
            if target.exists():
                assert target.read_bytes() == raw, 'Refusing to overwrite a different source'
            else:
                target.parent.mkdir(exist_ok=True)
                target.write_bytes(raw)
            print(key, hashlib.sha256(raw).hexdigest())
        return
    assert not ARCHIVE.exists(), 'The source snapshot is immutable'
    paths = sorted(Path('candidates').glob('f19_*.py'))
    paths.append(Path('candidates/n30_lynnsakurai_031656.py'))
    license_dir = Path('vendor/f19_public/lynnsakurai_farmer-john-and-the-wheat-seller/extracted_licenses')
    for name in ('LICENSE.txt', 'NOTICE.txt'):
        source = license_dir / name
        target = Path('attribution/frontier19/lynn_benchmark') / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        paths.append(target)
    paths.extend(Path('attribution').glob('frontier*/LAB_NOTICE.md'))
    paths.extend(Path('attribution/frontier16').glob('*.txt'))
    payload = {p.as_posix(): p.read_bytes().decode('utf-8') for p in paths}
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode('utf-8')
    ARCHIVE.write_bytes(lzma.compress(raw, preset=6))
    assert json.loads(lzma.decompress(ARCHIVE.read_bytes())) == payload
    manifest = dict(archive_sha256=hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
                    compressed_bytes=ARCHIVE.stat().st_size,
                    entries={p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                    purpose='Exact research sources, including rejected and superseded prototypes. Not a selection or release manifest.')
    (ROOT / 'source_snapshot_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print('Preserved', len(paths), 'files in', manifest['compressed_bytes'], 'bytes')


if __name__ == '__main__':
    main()
