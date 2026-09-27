"""Recent own-agent reference, without selecting by result; not a matched win-rate benchmark."""
from datetime import datetime,timezone
import gzip,hashlib,json
from pathlib import Path
from analyze_top100 import features
from research_top100 import ROOT,api,limited,download,write


def main():
    target=ROOT/'baseline.json'
    if target.exists():
        print('Baseline snapshot already exists; preserved.');return
    client=api();available={}
    for sid in (56615489,56609913):
        episodes=[e for e in limited(client.competition_list_episodes,sid)
                  if str(e.state).endswith('COMPLETED') and str(e.type).endswith('PUBLIC')]
        episodes.sort(key=lambda e:(str(e.create_time),e.id),reverse=True);available[sid]=episodes
    sid=56615489 if len(available[56615489])>=4 else 56609913
    report=dict(checked_utc=datetime.now(timezone.utc).isoformat(),submission=sid,
                candidate='f17_selected' if sid==56615489 else 'f16_repaired',
                available_public={str(k):len(v) for k,v in available.items()},
                rule='Latest up to 12 complete public games. F17 if at least four exist; otherwise F16 production-line reference. No outcome selection.',
                complete=False,rows=[])
    for e in available[sid][:12]:
        cached=Path('vendor/live_f16',f'episode-{e.id}-replay.json.gz')
        if cached.exists():
            path=cached
        else:
            path=Path(download(e.id)['path'])
        blob=gzip.decompress(path.read_bytes());data=json.loads(blob)
        assert data['module_version']=='1.32.7' and data['info']['EpisodeId']==e.id
        seat=next(a.index for a in e.agents if a.submission_id==sid)
        report['rows'].append(dict(episode=e.id,seat=seat,created=str(e.create_time),
            raw_path=path.as_posix(),sha256=hashlib.sha256(blob).hexdigest(),**features(data,seat)))
        write(target,report);print('own reference',sid,len(report['rows']),e.id,flush=True)
    report['complete']=True;write(target,report)


if __name__=='__main__':main()
