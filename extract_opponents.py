"""Extract source as data, without executing notebook cells or archive paths."""
import ast
import base64
import hashlib
import io
import json
import tarfile
from pathlib import Path


def literal(source, name):
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(name)


def main():
    records = []
    for name in ('nagata','tetsutani','prvsiyan'):
        p = next(Path('vendor',name).glob('*.ipynb'))
        notebook = json.loads(p.read_text(encoding='utf-8'))
        codes = [''.join(c['source']) for c in notebook['cells'] if c['cell_type']=='code']
        if name == 'nagata':
            source = next(c.split('\n',1)[1] for c in codes if c.startswith('%%writefile main.py'))
            data = source.encode('utf-8')
        elif name == 'tetsutani':
            cell = next(c for c in codes if 'ARCHIVE_B64 =' in c)
            archive = base64.b64decode(literal(cell,'ARCHIVE_B64'))
            assert hashlib.sha256(archive).hexdigest() == literal(cell,'EXPECTED_ARCHIVE_SHA256')
            with tarfile.open(fileobj=io.BytesIO(archive),mode='r:gz') as tf:
                data = tf.extractfile('main.py').read()
            assert hashlib.sha256(data).hexdigest() == literal(cell,'EXPECTED_MAIN_SHA256')
        else:
            data = literal(next(c for c in codes if c.startswith('AGENT_SOURCE=')),'AGENT_SOURCE').encode('utf-8')
        compile(data, name+'.py', 'exec')
        Path('candidates',name+'.py').write_bytes(data)
        metadata = json.loads(Path('vendor',name,'kernel-metadata.json').read_text())
        record = dict(name=name, url='https://www.kaggle.com/code/'+metadata['id'],
                      retrieved='2026-09-12', notebook_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                      agent_sha256=hashlib.sha256(data).hexdigest(),
                      same_as_v37=data == Path('baseline/v37.py').read_bytes(),
                      use='evaluation only; excluded from Git and Kaggle runtime')
        records.append(record)
        print(json.dumps(record))
    Path('results/opponents.json').write_text(json.dumps(records,indent=2)+'\n')


if __name__ == '__main__':
    main()
