"""Keep original receipts and verify a diagnostics-only rebuild on every context."""
import hashlib
import json
from pathlib import Path
from summarize_ml import summarize


def main():
    root=Path('results/gold')
    old=json.loads((root/'frontier_holdout.json').read_text())
    new=json.loads((root/'frontier_holdout_verified.json').read_text())
    assert old['complete'] and new['complete']
    controls={(r['opponent'],r['seed'],r['seat']):r for r in old['rows'] if r['candidate']=='frontier'}
    digest=hashlib.sha256(Path('candidates/frontier.py').read_bytes()).hexdigest()
    assert len(new['rows'])==80
    for r in new['rows']:
        prior=controls[r['opponent'],r['seed'],r['seat']]
        assert r['sha256']==digest and r['rewards']==prior['rewards']
        assert r['telemetry']['frontier_choice']==prior['telemetry']['frontier_choice']
        if r['telemetry']['frontier_choice']:
            assert r['telemetry']['auction_turns']==23
            assert r['telemetry']['auction_harvest_requests']>0
    merged=dict(new,expected_games=240,
                rows=new['rows']+[r for r in old['rows'] if r['candidate']!='frontier'],
                sources=['frontier_holdout_verified.json','frontier_holdout.json'],
                diagnostics_fix='All 80 frontier rewards/choices identical after telemetry fix. '
                                '160 unchanged baseline/constant rows reused with original hashes.')
    path=root/'frontier_holdout_merged.json';path.write_text(json.dumps(merged,indent=2)+'\n')
    summary=summarize(path,'ml_critic','frontier_choice')
    (root/'frontier_holdout_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary['candidates']['frontier'],indent=2))


if __name__=='__main__':main()
