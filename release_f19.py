"""Private two-policy release, with independent cloud checks and idempotent submissions."""
import argparse,base64,gzip,hashlib,io,json,lzma,tarfile
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path('results/frontier19')
KERNEL='jarturo/kaggriculture-frontier19-policy-validation'


def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def eligible(name):
    decision=read(ROOT/'release_selection.json')
    if name not in decision['selected']:return False
    plan=Path(decision['source_plans'][name])
    evidence=read(plan.with_name('holdout_summary.json'))['candidates'][name]
    if decision['validation_status'][name]=='passed_all_frozen_criteria':return evidence['pass_gate']
    # Explicitly experimental admission under the user's two-slot request.
    # Keep the failed frozen gate intact; never label it a pass.
    return (name=='f19_market1' and bool(decision['authorization']) and not evidence['pass_gate']
            and [k for k,v in evidence['checks'].items() if not v]==['nonmirror']
            and evidence['score_delta']==6 and evidence['head_to_head_score']==16
            and evidence['nonmirror_delta']==-2 and evidence['error_games']==0
            and evidence['max_call_ms']<1000)


def package(name,path):
    release=read(ROOT/'release.json');source=Path('candidates',name+'.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()==release['source_sha256'][name]
    files={'main.py':source,'LICENSE.txt':Path('attribution/frontier16/LICENSE.txt').read_bytes(),
           'NOTICE.txt':b'\n\n'.join(Path(p).read_bytes() for p in (
               'attribution/frontier16/NOTICE.txt','attribution/frontier16/LAB_NOTICE.md',
               'attribution/frontier17/LAB_NOTICE.md','attribution/frontier18/LAB_NOTICE.md','attribution/frontier19/LAB_NOTICE.md'))}
    raw=io.BytesIO()
    with tarfile.open(fileobj=raw,mode='w') as tf:
        for n,b in files.items():
            info=tarfile.TarInfo(n);info.size=len(b);info.mode=0o644;info.mtime=0
            tf.addfile(info,io.BytesIO(b))
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as gz:gz.write(raw.getvalue())
    with tarfile.open(path,'r:gz') as tf:
        assert tf.getnames()==list(files)
        assert all(m.isfile() for m in tf.getmembers())
        for n,b in files.items():assert tf.extractfile(n).read()==b
    return dict(archive_sha256=digest(path),candidate_sha256=release['source_sha256'][name],
                members_sha256={n:hashlib.sha256(b).hexdigest() for n,b in files.items()})


def prepare(names):
    from make_notebook import cell
    assert 1<=len(names)<=2 and len(names)==len(set(names)) and all(eligible(n) for n in names)
    assert not (ROOT/'release.json').exists(),'Frozen release already exists.'
    decision=read(ROOT/'release_selection.json')
    assert names==decision['selected'] and len(names)==2
    evidence=[ROOT/'plan.json',ROOT/'holdout_summary.json',ROOT/'selection_decision.json',ROOT/'release_selection.json']
    for n in names:
        plan_path=Path(decision['source_plans'][n])
        for p in (plan_path,plan_path.with_name('holdout_summary.json')):
            if p not in evidence:evidence.append(p)
        plan=read(plan_path)
        assert digest(Path('candidates',n+'.py'))==plan['hashes'][n]
    control='f18_small'
    release=dict(kernel=KERNEL,candidates=names,control=control,cloud_seeds=list(range(19201,19205)),
                 source_sha256={n:digest(Path('candidates',n+'.py')) for n in names+[control]},
                 evidence_sha256={p.as_posix():digest(p) for p in evidence},
                 cloud_rule=f'{(len(names)+1)*8} complete official-engine games; zero errors and under 1000ms per call. Functional, runtime and archive check only; competitive selection uses the frozen local holdout. Cloud scores are reported without an additional promotion threshold.',
                 created_utc=datetime.now(timezone.utc).isoformat())
    write(ROOT/'release.json',release)
    for n in names:write(ROOT/'local'/f'{n}.json',package(n,ROOT/'local'/f'{n}.tar.gz'))
    paths=[Path('candidates',n+'.py') for n in names+[control]]+evidence+[
        ROOT/'release.json',Path('release_f19.py'),Path('evaluate.py'),
        Path('attribution/frontier16/LICENSE.txt'),Path('attribution/frontier16/NOTICE.txt'),
        Path('attribution/frontier16/LAB_NOTICE.md'),Path('attribution/frontier17/LAB_NOTICE.md'),Path('attribution/frontier18/LAB_NOTICE.md'),Path('attribution/frontier19/LAB_NOTICE.md')]
    payload={p.as_posix():p.read_bytes().decode('utf-8') for p in paths}
    blob=base64.b64encode(lzma.compress(json.dumps(payload,ensure_ascii=False).encode(),preset=9)).decode()
    restored=json.loads(lzma.decompress(base64.b64decode(blob)))
    for p in paths:assert restored[p.as_posix()].encode()==p.read_bytes()
    cells=[cell('markdown','# Frontier19 — private policy validation\n\nTwo user-authorized experiments with inherited Apache-2.0 notices. Market2 passed every frozen local criterion. Market1 is an explicitly exploratory second slot: 44/48 versus 38/48 for F18 and 16/16 head-to-head, but a two-point regression against Lynn fails the frozen nonmirror criterion. That failure remains recorded. Cloud games validate runtime and packaging, without a score threshold; exports require those functional checks. Recorded-rival diagnostics cannot predict competitive performance. No leaderboard score is promised. This notebook never submits automatically.\n'),
        cell('code','from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
             f'payload=json.loads(lzma.decompress(base64.b64decode({blob!r})))\n'
             'for name,data in payload.items():\n    p=Path(name)\n    p.parent.mkdir(parents=True,exist_ok=True)\n    p.write_bytes(data.encode("utf-8"))\n'),
        cell('code','import importlib.metadata,subprocess,sys\n'
             'if importlib.metadata.version("kaggle-environments")!="1.32.7":\n'
             '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
             'subprocess.run([sys.executable,"release_f19.py","cloud"],check=True)\n'),
        cell('code','from IPython.display import display,FileLink\nprint(Path("results/frontier19/cloud_receipt.json").read_text())\n'
             'for p in Path(".").glob("f19_*.tar.gz"):display(FileLink(str(p)))\n')]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),'cell','exec')
    nb=dict(nbformat=4,nbformat_minor=5,cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}})
    data=(json.dumps(nb,indent=1,ensure_ascii=False)+'\n').encode();assert len(data)<2000000
    folder=Path('kaggle_frontier19');folder.mkdir(exist_ok=True);(folder/'experiment.ipynb').write_bytes(data)
    metadata=dict(id=KERNEL,title='Kaggriculture Frontier19 policy validation',code_file='experiment.ipynb',language='python',
                  kernel_type='notebook',is_private=True,enable_gpu=False,enable_internet=True,dataset_sources=[],competition_sources=['kaggriculture'],kernel_sources=[])
    write(folder/'kernel-metadata.json',metadata)
    write(ROOT/'notebook_prepared.json',dict(kernel=KERNEL,is_private=True,notebook_bytes=len(data),notebook_sha256=hashlib.sha256(data).hexdigest(),payload_verified=True))
    print('Prepared private notebook:',names,len(data),'bytes')


def check_games(report,release):
    names=release['candidates']+[release['control']];control=release['control']
    expected={(n,control,s,p) for n in names for s in release['cloud_seeds'] for p in (0,1)}
    rows=report['rows'];assert report['complete'] and report['engine']=='1.32.7'
    assert len(rows)==len(expected)==len(names)*8
    assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in rows}==expected
    for r in rows:
        assert r['status']==['DONE','DONE'] and r['steps']==720 and r['calls']==719
        assert r['sha256']==release['source_sha256'][r['candidate']]
        assert r['opponent_sha256']==release['source_sha256'][r['opponent']]
        assert not any(v and ('error' in k.lower() or 'fallback' in k.lower()) for k,v in r['telemetry'].items())
        assert r['margin']==r['rewards'][r['seat']]-r['rewards'][1-r['seat']]
        assert r['win']==int(r['margin']>0) and r['tie']==int(r['margin']==0)
    scores={n:sum(r['win']+.5*r['tie'] for r in rows if r['candidate']==n) for n in names}
    times={n:max(r['max_call_ms'] for r in rows if r['candidate']==n) for n in names}
    assert all(times[n]<1000 for n in release['candidates'])
    return dict(scores=scores,max_call_ms=times,games=len(rows),error_games=0)


def cloud():
    from evaluate import run
    release=read(ROOT/'release.json')
    for p,h in release['evidence_sha256'].items():assert digest(p)==h
    for n,h in release['source_sha256'].items():assert digest(Path('candidates',n+'.py'))==h
    assert all(eligible(n) for n in release['candidates'])
    run(release['candidates']+[release['control']],[release['control']],release['cloud_seeds'],2,ROOT/'cloud_games.json')
    checked=check_games(read(ROOT/'cloud_games.json'),release)
    checked.update(cloud_gate_passed=True,cloud_games_sha256=digest(ROOT/'cloud_games.json'),
                   exports={n:package(n,n+'.tar.gz') for n in release['candidates']})
    write(ROOT/'cloud_receipt.json',checked);print(json.dumps(checked,indent=2))


def verify():
    release=read(ROOT/'release.json');folder=ROOT/'kaggle'
    assert all(eligible(n) for n in release['candidates'])
    receipt=read(folder/ROOT/'cloud_receipt.json');games=folder/ROOT/'cloud_games.json'
    checked=check_games(read(games),release)
    for k,v in checked.items():assert receipt[k]==v
    assert receipt['cloud_gate_passed'] and receipt['cloud_games_sha256']==digest(games)
    for p,h in release['evidence_sha256'].items():assert digest(p)==h and digest(folder/p)==h
    for n,h in release['source_sha256'].items():assert digest(Path('candidates',n+'.py'))==h
    for n in release['candidates']:
        archive=folder/(n+'.tar.gz');assert archive.read_bytes()==(ROOT/'local'/(n+'.tar.gz')).read_bytes()
        expected=package(n,ROOT/'local'/(n+'.tar.gz'))
        assert receipt['exports'][n]==expected and digest(archive)==expected['archive_sha256']
    write(ROOT/'kaggle_verified.json',dict(receipt,verified=True,export_checks_passed=True,checked_utc=datetime.now(timezone.utc).isoformat()))
    print(json.dumps(checked,indent=2))


def submit(name,authorization):
    from kaggle.api.kaggle_api_extended import KaggleApi
    release=read(ROOT/'release.json');verified=read(ROOT/'kaggle_verified.json');private=read(ROOT/'kaggle_private_verified.json')
    assert name in release['candidates'] and eligible(name)
    assert verified['verified'] and verified['export_checks_passed']
    assert private['id']==KERNEL and private['is_private'] is True and private['notebook_cells_match']
    proof=verified['exports'][name];archive=ROOT/'kaggle'/(name+'.tar.gz')
    assert digest(archive)==proof['archive_sha256'] and digest(Path('candidates',name+'.py'))==proof['candidate_sha256']
    desc=f'Frontier19 {name} ({proof["candidate_sha256"][:8]})'
    rp=ROOT/(name+'_submission_receipt.json');ip=ROOT/(name+'_submission_intent.json')
    receipt=read(rp) if rp.exists() else None
    client=KaggleApi();client.authenticate();submissions=client.competition_submissions('kaggriculture') or []
    matches=[s for s in submissions if s and ((s.ref==receipt['id']) if receipt else (s.description==desc))]
    if matches:
        s=matches[0];receipt=dict(receipt or {},id=s.ref,status=str(s.status),description=s.description,
            public_score=s.public_score,error=s.error_description,date=str(s.date),checked_utc=datetime.now(timezone.utc).isoformat(),
            **proof,leaderboard_submitted=True)
        write(rp,receipt);print(json.dumps(receipt,indent=2));return
    if receipt:print(json.dumps(receipt,indent=2));return
    assert authorization,'No upload: use --authorization to record the existing user authorization.'
    assert not ip.exists(),'Uncertain earlier attempt: reconcile remotely; never duplicate.'
    other=[p for p in ROOT.glob('*_submission_intent.json') if p!=ip]
    assert len(other)<2,'The two-submission authorization is exhausted.'
    write(ip,dict(created_utc=datetime.now(timezone.utc).isoformat(),description=desc,authorization=authorization,**proof))
    response=client.competition_submit(str(archive),desc,'kaggriculture',quiet=True)
    assert response.ref>0,response.message
    receipt=dict(id=response.ref,status='SUBMITTED',message=response.message,description=desc,**proof,
                 checked_utc=datetime.now(timezone.utc).isoformat(),leaderboard_submitted=True,authorization=authorization)
    write(rp,receipt);print(json.dumps(receipt,indent=2))


def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','cloud','verify','submit'])
    p.add_argument('--candidates',nargs='+');p.add_argument('--candidate');p.add_argument('--authorization',default='');args=p.parse_args()
    if args.mode=='prepare':prepare(args.candidates)
    elif args.mode=='cloud':cloud()
    elif args.mode=='verify':verify()
    else:submit(args.candidate,args.authorization)


if __name__=='__main__':main()
