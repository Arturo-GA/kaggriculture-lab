"""Create local experimental artifacts and a reproducible summary."""
import hashlib
import json
from pathlib import Path
import shutil
import build


def main():
    source = Path('baseline/v37.py').read_text(encoding='utf-8')
    lines = source.splitlines()
    start = next(i for i,l in enumerate(lines) if 'Apache License' in l)
    end = next(i for i,l in enumerate(lines) if l.startswith('"""Kaggriculture'))
    license_text = '\n'.join(l[2:] if l.startswith('# ') else l[1:] if l.startswith('#') else l
                             for l in lines[start:end])+'\n'
    Path('LICENSE').write_bytes(license_text.encode('utf-8'))
    build.package('matched6','submission.tar.gz')
    shutil.copyfile('candidates/matched6.py','main.py')
    receipt = dict(candidate='matched6', status='experimental',
                   source_sha256=hashlib.sha256(Path('main.py').read_bytes()).hexdigest(),
                   archive_sha256=hashlib.sha256(Path('submission.tar.gz').read_bytes()).hexdigest(),
                   confirmation='results/confirmation.json', leaderboard_submitted=False)
    Path('results/release.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
