"""Private single-policy release, with independent cloud checks and idempotent submissions."""
import argparse,base64,gzip,hashlib,io,json,lzma,tarfile
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path('results/frontier20')
KERNEL='jarturo/kaggriculture-frontier20-policy-validation'


def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def eligible(name):
    decision=read(ROOT/'release_selection.json')
    if decision['selected']!=[name]:return False
    plan=Path(decision['source_plans'][name])
    if decision.get('validation_status')=='experimental_controls_pending_user_requested':
        admission=read(ROOT/'experimental_admission.json')
        games=read(ROOT/'value_gate'/'experimental_f20_value_games.json')
        frozen=read(plan)
        rows=games['rows']
        expected={(name,o,s,p) for o in frozen['opponents'] for s in frozen['seeds'] for p in frozen['seats']}
        assert name==admission['candidate']=='f20_value' and admission['user_requested_immediate_submission']
        assert digest(Path('candidates',name+'.py'))==admission['source_sha256']==frozen['hashes'][name]
        assert digest(ROOT/'value_gate'/'experimental_f20_value_games.json')==admission['candidate_games_sha256']
        assert games['complete_candidate_slice'] and games['engine']==frozen['engine']
        assert len(rows)==len(expected)==160
        assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in rows}==expected
        for r in rows:
            assert r['sha256']==frozen['hashes'][name] and r['opponent_sha256']==frozen['hashes'][r['opponent']]
            assert r['status']==['DONE','DONE'] and r['steps']==720 and r['calls']==719
            assert r['max_call_ms']<1000
            assert not any(v and ('error' in k.lower() or 'fallback' in k.lower()) for k,v in r['telemetry'].items())
        return True
    evidence=read(plan.with_name('holdout_summary.json'))['candidates'][name]
    return evidence['pass_gate'] and all(evidence['checks'].values())


def package(name,path):
    release=read(ROOT/'release.json');source=Path('candidates',name+'.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()==release['source_sha256'][name]
    files={'main.py':source,'LICENSE.txt':Path('attribution/frontier16/LICENSE.txt').read_bytes(),
           'NOTICE.txt':b'\n\n'.join(Path(p).read_bytes() for p in (
               'attribution/frontier16/NOTICE.txt','attribution/frontier16/LAB_NOTICE.md',
               'attribution/frontier17/LAB_NOTICE.md','attribution/frontier18/LAB_NOTICE.md','attribution/frontier19/LAB_NOTICE.md','attribution/frontier20/LAB_NOTICE.md'))}
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
    assert len(names)==1 and len(names)==len(set(names)) and all(eligible(n) for n in names)
    assert not (ROOT/'release.json').exists(),'Frozen release already exists.'
    decision=read(ROOT/'release_selection.json')
    assert names==decision['selected'] and len(names)==1
    evidence=[ROOT/'plan.json',ROOT/'holdout_summary.json',ROOT/'selection_decision.json',ROOT/'release_selection.json',ROOT/'contracts.json']
    for n in names:
        plan_path=Path(decision['source_plans'][n])
        extra=([ROOT/'experimental_admission.json',ROOT/'value_gate'/'experimental_f20_value_games.json']
               if decision.get('validation_status')=='experimental_controls_pending_user_requested'
               else [plan_path.with_name('holdout_summary.json')])
        for p in [plan_path]+extra:
            if p not in evidence:evidence.append(p)
        contracts=plan_path.with_name('contracts.json')
        if contracts.exists():
            checks=read(contracts);proof=checks['candidates'][n] if 'candidates' in checks else checks
            assert proof['source_sha256']==digest(Path('candidates',n+'.py'))
            if contracts not in evidence:evidence.append(contracts)
        plan=read(plan_path)
        assert digest(Path('candidates',n+'.py'))==plan['hashes'][n]
    control='f19_market2'
    release=dict(kernel=KERNEL,candidates=names,control=control,cloud_seeds=list(range(20301,20305)),
                 source_sha256={n:digest(Path('candidates',n+'.py')) for n in names+[control]},
                 evidence_sha256={p.as_posix():digest(p) for p in evidence},
                 validation_status=decision.get('validation_status','competitive_gate_passed'),
                 cloud_rule=f'{(len(names)+1)*8} complete official-engine games; zero errors and under 1000ms per call. Functional, runtime and archive check only. This first experimental release was explicitly requested by the user with full comparative controls still pending; it does not claim the competitive gate passed. Cloud scores are reported without an additional promotion threshold.',
                 created_utc=datetime.now(timezone.utc).isoformat())
    write(ROOT/'release.json',release)
    for n in names:write(ROOT/'local'/f'{n}.json',package(n,ROOT/'local'/f'{n}.tar.gz'))
    paths=[Path('candidates',n+'.py') for n in names+[control]]+evidence+[
        ROOT/'release.json',Path('release_f20.py'),Path('evaluate.py'),
        Path('attribution/frontier16/LICENSE.txt'),Path('attribution/frontier16/NOTICE.txt'),
        Path('attribution/frontier16/LAB_NOTICE.md'),Path('attribution/frontier17/LAB_NOTICE.md'),Path('attribution/frontier18/LAB_NOTICE.md'),Path('attribution/frontier19/LAB_NOTICE.md'),Path('attribution/frontier20/LAB_NOTICE.md')]
    payload={p.as_posix():p.read_bytes().decode('utf-8') for p in paths}
    blob=base64.b64encode(lzma.compress(json.dumps(payload,ensure_ascii=False).encode(),preset=9)).decode()
    restored=json.loads(lzma.decompress(base64.b64decode(blob)))
    for p in paths:assert restored[p.as_posix()].encode()==p.read_bytes()
    cells=[cell('markdown','# Frontier20 — private experimental release\n\nThe user explicitly requested one immediate experimental submission, with full comparative controls still pending. The candidate completed 149 wins and 11 losses in 160 local games with no errors; this alone does not establish improvement over the controls. The original candidate failed its gate and that evidence is preserved. All 23 public defeats available at the dated snapshot of the two F19 submissions were reconstructed with exact rewards and accounting. Cloud games check runtime and packaging. Replay opponents cannot react and are diagnostics only. A second submission requires demonstrated improvement after controls. No rank or medal is guaranteed. This notebook never submits automatically.\n'),
        cell('code','from pathlib import Path\nimport os,json,base64,lzma\nos.chdir("/kaggle/working")\n'
             f'payload=json.loads(lzma.decompress(base64.b64decode({blob!r})))\n'
             'for name,data in payload.items():\n    p=Path(name)\n    p.parent.mkdir(parents=True,exist_ok=True)\n    p.write_bytes(data.encode("utf-8"))\n'),
        cell('code','import importlib.metadata,subprocess,sys\n'
             'if importlib.metadata.version("kaggle-environments")!="1.32.7":\n'
             '    subprocess.run([sys.executable,"-m","pip","install","--no-deps","kaggle-environments==1.32.7"],check=True)\n'
             'subprocess.run([sys.executable,"release_f20.py","cloud"],check=True)\n'),
        cell('code','from IPython.display import display,FileLink\nprint(Path("results/frontier20/cloud_receipt.json").read_text())\n'
             'for p in Path(".").glob("f20_*.tar.gz"):display(FileLink(str(p)))\n')]
    for c in cells:
        if c['cell_type']=='code':compile(''.join(c['source']),'cell','exec')
    nb=dict(nbformat=4,nbformat_minor=5,cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}})
    data=(json.dumps(nb,indent=1,ensure_ascii=False)+'\n').encode();assert len(data)<2000000
    folder=Path('kaggle_frontier20');folder.mkdir(exist_ok=True);(folder/'experiment.ipynb').write_bytes(data)
    metadata=dict(id=KERNEL,title='Kaggriculture Frontier20 policy validation',code_file='experiment.ipynb',language='python',
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
    desc=f'Frontier20 {name} ({proof["candidate_sha256"][:8]})'
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
    assert len(other)<1,'The one-submission authorization is exhausted.'
    assert datetime.now(timezone.utc)<datetime(2026,9,30,23,59,tzinfo=timezone.utc),'Final submission deadline passed.'
    limits=client.competition_get_submission_limits('kaggriculture')
    assert limits.num_allowed_now>0,'No submission quota remains.'
    active=client.competition_team_submissions(16639155) or []
    assert {s.id for s in active}=={56714342,56714336},'Active pair changed: inspect before retiring a submission.'
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
