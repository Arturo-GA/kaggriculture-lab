"""One final private submission, preserving the already-active F20 value agent."""
import argparse,base64,gzip,hashlib,io,json,lzma,tarfile
from datetime import datetime,timezone
from pathlib import Path
from release_f20 import read,write,digest,check_games

ROOT=Path('results/frontier21')
KERNEL='jarturo/kaggriculture-frontier21-final-validation'

def eligible(name):
    choice=read(ROOT/'selection.json')
    assert choice['selected']==name and choice['source_sha256']==digest(Path('candidates',name+'.py'))
    contracts=read(ROOT/'contracts.json')['candidates'][name]
    assert contracts['success'] and contracts['source_sha256']==choice['source_sha256']
    if choice['mode']=='measured_improvement':
        proof=read(choice['proof']);plan=read(ROOT/'holdout_plan.json')
        return proof['pass_gate'] and all(proof['checks'].values()) and plan['hashes'][name]==choice['source_sha256']
    assert choice['mode']=='authorized_tied_fallback' and name=='f20_fill' and choice['authorization']
    proof=read(choice['proof'])
    assert read('results/frontier20/value_gate/plan.json')['hashes'][name]==choice['source_sha256']
    return proof['candidates'][name]['pass_gate'] and proof['scores'][name]==proof['scores']['f20_value']

def package(name,path):
    release=read(ROOT/'release.json');source=Path('candidates',name+'.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()==release['source_sha256'][name]
    notices=['attribution/frontier16/NOTICE.txt']+[f'attribution/frontier{k}/LAB_NOTICE.md' for k in range(16,22)]
    files={'main.py':source,'LICENSE.txt':Path('attribution/frontier16/LICENSE.txt').read_bytes(),
        'NOTICE.txt':b'\n\n'.join(Path(p).read_bytes() for p in notices)}
    raw=io.BytesIO()
    with tarfile.open(fileobj=raw,mode='w') as tf:
        for n,b in files.items():
            info=tarfile.TarInfo(n);info.size=len(b);info.mode=0o644;info.mtime=0
            tf.addfile(info,io.BytesIO(b))
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as gz:gz.write(raw.getvalue())
    with tarfile.open(path,'r:gz') as tf:
        assert tf.getnames()==list(files) and all(m.isfile() for m in tf.getmembers())
        for n,b in files.items():assert tf.extractfile(n).read()==b
    return dict(archive_sha256=digest(path),candidate_sha256=release['source_sha256'][name],
        members_sha256={n:hashlib.sha256(b).hexdigest() for n,b in files.items()})

def prepare():
    from make_notebook import cell
    choice=read(ROOT/'selection.json');name=choice['selected'];assert eligible(name)
    assert not (ROOT/'release.json').exists()
    evidence=[ROOT/'selection.json',ROOT/'contracts.json',ROOT/'development_plan.json',ROOT/'development_summary.json',
        Path('results/frontier20/value_gate/plan.json'),Path('results/frontier20/value_gate/holdout_summary.json')]
    if (ROOT/'holdout_summary.json').exists():evidence += [ROOT/'holdout_plan.json',ROOT/'holdout_summary.json']
    release=dict(kernel=KERNEL,candidates=[name],control='f20_value',cloud_seeds=list(range(21201,21205)),
        source_sha256={n:digest(Path('candidates',n+'.py')) for n in (name,'f20_value')},
        evidence_sha256={p.as_posix():digest(p) for p in evidence},validation_mode=choice['mode'],
        created_utc=datetime.now(timezone.utc).isoformat(),
        cloud_rule='16 official-engine games; zero errors and candidate calls below1000ms. Runtime/archive check only, not a new competitive selection sample.',
        expected_active_before=[56719762,56714342],preserve_submission=56719762,
        authorization=choice['authorization'])
    write(ROOT/'release.json',release)
    write(ROOT/'local'/f'{name}.json',package(name,ROOT/'local'/f'{name}.tar.gz'))
    paths=[Path('candidates',n+'.py') for n in (name,'f20_value')]+evidence+[
        ROOT/'release.json',Path('release_f21.py'),Path('release_f20.py'),Path('evaluate.py'),
        Path('attribution/frontier16/LICENSE.txt'),Path('attribution/frontier16/NOTICE.txt')]+[
        Path(f'attribution/frontier{k}/LAB_NOTICE.md') for k in range(16,22)]
    payload={p.as_posix():p.read_bytes().decode('utf-8') for p in paths}
    blob=base64.b64encode(lzma.compress(json.dumps(payload,ensure_ascii=False).encode(),preset=6)).decode()
    restored=json.loads(lzma.decompress(base64.b64decode(blob)))
    for p in paths:assert restored[p.as_posix()].encode()==p.read_bytes()
    status=('Passed a separately frozen fresh-seed comparison against the active F20 value agent.' if choice['mode']=='measured_improvement'
        else 'User-authorized fallback: this fill-only agent tied F20 value in all160 earlier point outcomes. No improvement over that agent is claimed.')
    cells=[cell('markdown',f'# Frontier21 — final private validation\n\nCandidate: {name}. {status}\n\nOnly the covered residual-sale cap was investigated. Failed candidates and frozen criteria are preserved. Cloud games check runtime and archive integrity. No leaderboard position or medal is guaranteed. This notebook never submits automatically.\n'),
        cell('code','from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
            f'payload=json.loads(lzma.decompress(base64.b64decode({blob!r})))\n'
            'for name,data in payload.items():\n    p=Path(name)\n    p.parent.mkdir(parents=True,exist_ok=True)\n    p.write_bytes(data.encode("utf-8"))\n'),
        cell('code','import importlib.metadata,subprocess,sys\n'
            'if importlib.metadata.version("kaggle-environments")!="1.32.7":\n'
            '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
            'subprocess.run([sys.executable,"release_f21.py","cloud"],check=True)\n'),
        cell('code','from IPython.display import display,FileLink\nprint(Path("results/frontier21/cloud_receipt.json").read_text())\n'
            'for p in Path(".").glob("*.tar.gz"):display(FileLink(str(p)))\n')]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),'cell','exec')
    nb=dict(nbformat=4,nbformat_minor=5,cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}})
    data=(json.dumps(nb,indent=1,ensure_ascii=False)+'\n').encode();assert len(data)<2000000
    folder=Path('kaggle_frontier21');folder.mkdir(exist_ok=True);(folder/'experiment.ipynb').write_bytes(data)
    write(folder/'kernel-metadata.json',dict(id=KERNEL,title='Kaggriculture Frontier21 final validation',code_file='experiment.ipynb',language='python',
        kernel_type='notebook',is_private=True,enable_gpu=False,enable_internet=True,dataset_sources=[],competition_sources=['kaggriculture'],kernel_sources=[]))
    write(ROOT/'notebook_prepared.json',dict(kernel=KERNEL,is_private=True,notebook_sha256=hashlib.sha256(data).hexdigest(),payload_verified=True))
    print('Prepared',name,choice['mode'],len(data),'bytes')

def cloud():
    from evaluate import run
    release=read(ROOT/'release.json')
    assert eligible(release['candidates'][0])
    for p,h in release['evidence_sha256'].items():assert digest(p)==h
    for n,h in release['source_sha256'].items():assert digest(Path('candidates',n+'.py'))==h
    run(release['candidates']+[release['control']],[release['control']],release['cloud_seeds'],2,ROOT/'cloud_games.json')
    checked=check_games(read(ROOT/'cloud_games.json'),release)
    checked.update(cloud_gate_passed=True,cloud_games_sha256=digest(ROOT/'cloud_games.json'),
        exports={n:package(n,n+'.tar.gz') for n in release['candidates']})
    write(ROOT/'cloud_receipt.json',checked);print(json.dumps(checked,indent=2))

def verify():
    release=read(ROOT/'release.json');folder=ROOT/'kaggle'
    assert eligible(release['candidates'][0])
    receipt=read(folder/ROOT/'cloud_receipt.json');games=folder/ROOT/'cloud_games.json'
    checked=check_games(read(games),release)
    for k,v in checked.items():assert receipt[k]==v
    assert receipt['cloud_gate_passed'] and receipt['cloud_games_sha256']==digest(games)
    for p,h in release['evidence_sha256'].items():assert digest(p)==h and digest(folder/p)==h
    for n in release['candidates']:
        archive=folder/(n+'.tar.gz');assert archive.read_bytes()==(ROOT/'local'/(n+'.tar.gz')).read_bytes()
        expected=package(n,ROOT/'local'/(n+'.tar.gz'))
        assert receipt['exports'][n]==expected and digest(archive)==expected['archive_sha256']
    write(ROOT/'kaggle_verified.json',dict(receipt,verified=True,export_checks_passed=True,checked_utc=datetime.now(timezone.utc).isoformat()))
    print('Cloud/archive verified',checked)

def submit():
    from research_top100 import api,limited
    from research_f16 import plain
    release=read(ROOT/'release.json');name=release['candidates'][0];verified=read(ROOT/'kaggle_verified.json');private=read(ROOT/'kaggle_private_verified.json')
    assert eligible(name) and verified['verified'] and verified['export_checks_passed']
    assert private['id']==KERNEL and private['is_private'] is True and private['notebook_cells_match']
    proof=verified['exports'][name];archive=ROOT/'kaggle'/(name+'.tar.gz')
    assert digest(archive)==proof['archive_sha256'] and digest(Path('candidates',name+'.py'))==proof['candidate_sha256']
    desc=f'Final Frontier21 {name} ({proof["candidate_sha256"][:8]})'
    rp=ROOT/'submission_receipt.json';ip=ROOT/'submission_intent.json';receipt=read(rp) if rp.exists() else None
    client=api();subs=limited(client.competition_submissions,'kaggriculture') or []
    matches=[s for s in subs if s and ((s.ref==receipt['id']) if receipt else (s.description==desc))]
    if matches:
        s=matches[0];receipt=dict(receipt or {},id=s.ref,status=str(s.status),description=s.description,public_score=s.public_score,
            error=s.error_description,date=str(s.date),checked_utc=datetime.now(timezone.utc).isoformat(),**proof,leaderboard_submitted=True)
        write(rp,receipt);print(json.dumps(receipt,indent=2));return
    if receipt:print(json.dumps(receipt,indent=2));return
    assert release['authorization'] and not ip.exists(),'Reconcile any uncertain earlier submission; do not duplicate.'
    assert datetime.now(timezone.utc)<datetime(2026,9,30,23,59,tzinfo=timezone.utc)
    limits=limited(client.competition_get_submission_limits,'kaggriculture');assert limits.num_allowed_now>0
    active=limited(client.competition_team_submissions,16639155) or []
    assert {s.id for s in active}==set(release['expected_active_before']),'Inspect changed active pair before submitting.'
    write(ROOT/'preflight.json',dict(active=plain(active),limits=plain(limits),checked_utc=datetime.now(timezone.utc).isoformat()))
    write(ip,dict(created_utc=datetime.now(timezone.utc).isoformat(),description=desc,authorization=release['authorization'],**proof))
    response=client.competition_submit(str(archive),desc,'kaggriculture',quiet=True)
    assert response.ref>0,response.message
    write(rp,dict(id=response.ref,status='SUBMITTED',message=response.message,description=desc,**proof,
        checked_utc=datetime.now(timezone.utc).isoformat(),leaderboard_submitted=True,authorization=release['authorization']))
    print('Submitted',response.ref)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','cloud','verify','submit']);a=p.parse_args()
    {'prepare':prepare,'cloud':cloud,'verify':verify,'submit':submit}[a.mode]()
