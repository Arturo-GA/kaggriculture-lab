"""Decode public notebook source without running notebook installation cells."""
import base64
import hashlib
import json
import zlib
from pathlib import Path
from extract_opponents import literal


def main():
    records=[]
    for name in ('kaito','router'):
        notebook=next(Path('vendor',name).glob('*.ipynb'))
        cells=json.loads(notebook.read_text(encoding='utf-8'))['cells']
        codes=[''.join(c['source']) for c in cells if c['cell_type']=='code']
        if name=='kaito':
            data=zlib.decompress(base64.b85decode(literal(codes[0],'payload')))
            assert hashlib.sha256(data).hexdigest()=='69f06a802b62aa08f28705dab5728eb924bb6a7c23ffe0164f65b104cc3dadf3'
        else:
            data=next(c.split('\n',1)[1] for c in codes if c.startswith('%%writefile main.py')).encode('utf-8')
        compile(data,name+'.py','exec')
        Path('candidates',name+'.py').write_bytes(data)
        metadata=json.loads(Path('vendor',name,'kernel-metadata.json').read_text())
        records.append(dict(name=name,url='https://www.kaggle.com/code/'+metadata['id'],
                            agent_sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),
                            notebook_sha256=hashlib.sha256(notebook.read_bytes()).hexdigest()))
    Path('results/panel_v2_sources.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))


if __name__=='__main__':
    main()
