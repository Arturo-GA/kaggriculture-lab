"""Audit outcomes and reproduce our actions on our own recorded observations."""
import contextlib
import copy
import io
import json
from pathlib import Path


def main():
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        from kaggle_environments.agent import get_last_callable
    summaries = []
    for path in sorted(Path('vendor/live').glob('*replay.json')):
        replay = json.loads(path.read_text())
        names = replay['info']['TeamNames']
        if names[0] == names[1]:
            continue
        seat = next(i for i,n in enumerate(names) if n.startswith('Arturo '))
        policy = get_last_callable(Path('candidates/matched6.py').read_text(encoding='utf-8'))
        differences = []
        for t in range(len(replay['steps'])-1):
            obs = copy.deepcopy(replay['steps'][t][seat]['observation'])
            shared = replay['steps'][t][0]['observation']
            for key in ('step','day','hour','farms','market','town'):
                if key not in obs:
                    obs[key] = copy.deepcopy(shared[key])
            obs['player']=seat
            action=policy(obs,copy.deepcopy(replay['configuration']))
            expected=replay['steps'][t+1][seat]['action']
            if action!=expected:
                differences.append(t)
        margin=replay['rewards'][seat]-replay['rewards'][1-seat]
        record=dict(episode_id=replay['info']['EpisodeId'],opponent=names[1-seat],
                    seat=seat,rewards=replay['rewards'],margin=margin,win=margin>0,
                    statuses=replay['statuses'],engine=replay['module_version'],
                    actions_checked=len(replay['steps'])-1,
                    action_mismatches=len(differences),first_mismatches=differences[:10])
        summaries.append(record)
        print(json.dumps(record,ensure_ascii=False),flush=True)
    Path('results/live/audit.json').write_text(json.dumps(summaries,indent=2,ensure_ascii=False),encoding='utf-8')


if __name__=='__main__':
    main()
