"""Read-only stress fixtures for the explicitly requested opponent."""
import json
from datetime import datetime, timezone
from pathlib import Path
from research_top100 import api, limited, download, write
from research_four import public_episodes
from research_f16 import plain

ROOT = Path('results/frontier20/grigor')
TEAM = 16945978

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    initial = json.loads(Path('results/frontier20/initial.json').read_text(encoding='utf-8'))
    path = ROOT/'selection.json'
    client = api()
    if path.exists():
        report = json.loads(path.read_text(encoding='utf-8'))
    else:
        subs = limited(client.competition_team_submissions, TEAM)
        report = dict(checked_utc=datetime.now(timezone.utc).isoformat(), team_id=TEAM,
            team=initial['leaderboard'][str(TEAM)], submissions=plain(subs), selected=[], downloaded=[],
            selection_rule='Four latest completed public games of EACH active submission, independent of outcome.',
            interpretation='Counterfactual replay diagnostics only. Test policy occupies the opposite seat from Grigor. Original recorded margin belongs to the real opponent, not our historical agent. No claim of defeating a reactive private agent.', complete=False)
        for sub in subs:
            rows = public_episodes(client, sub.id, initial['leaderboard'])
            report['selected'].extend(dict(r, grigor_submission=sub.id) for r in rows[:4])
        write(path, report)
    done = {r['id'] for r in report['downloaded']}
    for eid in sorted({r['id'] for r in report['selected']}-done):
        report['downloaded'].append(download(eid))
        write(path, report)
        print('downloaded', eid, flush=True)
    fixtures=[]
    for r in report['selected']:
        fixtures.append(dict(id=r['id'], seat=1-r['seat'], grigor_seat=r['seat'],
            op_name=report['team']['name'], op_score=report['team']['score'],
            grigor_submission=r['grigor_submission'], original_other_team=r['op_name'],
            original_other_margin=-r['margin']))
    # A meeting between both active agents would otherwise duplicate an episode.
    fixtures=list({(r['id'],r['seat']):r for r in fixtures}.values())
    write(ROOT/'episodes.json',fixtures)
    report['complete']=len(report['downloaded'])==len({r['id'] for r in report['selected']})
    write(path,report)
    print(json.dumps({k:v for k,v in report.items() if k!='downloaded'},indent=2))

if __name__=='__main__':main()
