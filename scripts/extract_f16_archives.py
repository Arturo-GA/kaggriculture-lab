"""Extract literal public notebook archives as data; never execute notebook cells."""
import ast,base64,hashlib,io,json,tarfile
from pathlib import Path


def main():
    report=[]
    for folder in Path('vendor/f16_public').iterdir():
        if not folder.is_dir():continue
        for path in folder.glob('*.ipynb'):
            assignments={};parts=[]
            for cell in json.loads(path.read_text(encoding='utf-8'))['cells']:
                if cell['cell_type']!='code':continue
                try:tree=ast.parse(''.join(cell['source']))
                except SyntaxError:continue
                for node in tree.body:
                    if isinstance(node,ast.Assign):
                        for t in node.targets:
                            if isinstance(t,ast.Name) and t.id in ('ARCHIVE_B85','EXPECTED_MAIN_SHA256','EXPECTED_ARCHIVE_SHA256'):
                                try:assignments[t.id]=ast.literal_eval(node.value)
                                except (ValueError,TypeError):pass
                    if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call):
                        call=node.value
                        if isinstance(call.func,ast.Attribute) and isinstance(call.func.value,ast.Name) and call.func.value.id=='ARCHIVE_PARTS' and call.func.attr=='append':
                            parts.append(ast.literal_eval(call.args[0]))
            blob=assignments.get('ARCHIVE_B85') or ''.join(parts)
            if not blob:continue
            raw=base64.b85decode(''.join(blob.split()).encode())
            assert hashlib.sha256(raw).hexdigest()==assignments['EXPECTED_ARCHIVE_SHA256']
            with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as tf:
                files={m.name:tf.extractfile(m).read() for m in tf.getmembers() if m.isfile()}
            main=files['main.py'];digest=hashlib.sha256(main).hexdigest()
            assert digest==assignments['EXPECTED_MAIN_SHA256']
            name='n27_'+folder.name.split('_')[0][:14]+'_'+digest[:6]
            Path('candidates',name+'.py').write_bytes(main)
            licenses=folder/'extracted_licenses';licenses.mkdir(exist_ok=True)
            for n in ('LICENSE.txt','NOTICE.txt'):
                if n in files:(licenses/n).write_bytes(files[n])
            entry=dict(notebook=str(path),candidate=name,sha256=digest,bytes=len(main),members=list(files),
                archive_sha256=hashlib.sha256(raw).hexdigest(),method='literal AST extraction only; no notebook cells executed')
            report.append(entry);print(json.dumps(entry))
    Path('results/frontier16/archive_sources.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
