"""Preserve the frozen small-market variant, add the observed zero-pickup fix."""
import hashlib,json
from pathlib import Path


def main():
    parent=Path('candidates/f18_small.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest()=='d9289a3e55624596ab5c2a8368359542e09249ae7fd64391d506bf82daeec135'
    data=parent+b'\n'+Path('frontier18_feed.py').read_bytes()
    compile(data,'f18_feed','exec');Path('candidates/f18_feed.py').write_bytes(data)
    out=dict(candidate='f18_feed',parent='f18_small',sha256=hashlib.sha256(data).hexdigest(),
             rationale='F17 loss 114306320: day25 zero wheat pickup blocks inherited rescue, six sheep miss feeding.')
    Path('results/frontier18/feed_build.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
