"""Static extraction and fingerprints of current public evaluation opponents."""
import ast,base64,hashlib,io,json,tarfile
from pathlib import Path
from extract_public_agents import auto_extract
from research_top100 import write

def main():
    report=[]
    for folder in Path('vendor/f20_public').iterdir():
        if not folder.is_dir():continue
        for path in folder.glob('*.ipynb'):
            nb=json.loads(path.read_text(encoding='utf-8'));cells=[''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code']
            cells=[('%%writefile main.py\n'+c.split('\n',1)[1]) if c.startswith('%%writefile /kaggle/working/main.py') else c for c in cells]
            parts=[];assignments={}
            for cell in cells:
                try:tree=ast.parse(cell)
                except SyntaxError:continue
                for n in tree.body:
                    if isinstance(n,ast.Assign):
                        for t in n.targets:
                            if isinstance(t,ast.Name):
                                try:assignments[t.id]=ast.literal_eval(n.value)
                                except (ValueError,TypeError):pass
                    if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call):
                        c=n.value
                        if isinstance(c.func,ast.Attribute) and isinstance(c.func.value,ast.Name) and c.func.value.id=='ARCHIVE_PARTS' and c.func.attr=='append':parts.append(ast.literal_eval(c.args[0]))
            files={};data=auto_extract(cells)
            blob=assignments.get('ARCHIVE_B85') or ''.join(parts)
            if blob:
                raw=base64.b85decode(''.join(blob.split()))
                if 'EXPECTED_ARCHIVE_SHA256' in assignments:assert hashlib.sha256(raw).hexdigest()==assignments['EXPECTED_ARCHIVE_SHA256']
                with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as tf:files={m.name:tf.extractfile(m).read() for m in tf.getmembers() if m.isfile()}
                data=files['main.py']
            if data is None:
                print('NO SOURCE',folder.name,flush=True);continue
            digest=hashlib.sha256(data).hexdigest()
            if assignments.get('EXPECTED_MAIN_SHA256'):assert assignments['EXPECTED_MAIN_SHA256']==digest
            name='n30b_'+folder.name.split('_')[0][:14]+'_'+digest[:6]
            compile(data,name,'exec');Path('candidates',name+'.py').write_bytes(data)
            licensefolder=folder/'extracted_licenses';licensefolder.mkdir(exist_ok=True)
            for n in ('LICENSE.txt','NOTICE.txt'):
                if n in files:(licensefolder/n).write_bytes(files[n])
            report.append(dict(notebook=path.as_posix(),candidate=name,sha256=digest,bytes=len(data),members=list(files),metadata=json.loads((folder/'kernel-metadata.json').read_text(encoding='utf-8'))))
            print(name,len(data),'members',list(files),flush=True)
    write(Path('results/frontier20/public_sources.json'),report)

if __name__=='__main__':main()
