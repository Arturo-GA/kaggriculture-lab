"""Preserve the original gate result and record the experimental release decision.

This is a post-result decision, not a replacement preregistered criterion.
No candidate source or original plan is modified here.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from frontier3_validation import assess


def main():
    root=Path('results/frontier3')
    plan=json.loads((root/'plan.json').read_text())
    selection=json.loads((root/'selection.json').read_text())
    candidate=selection['candidate']
    summaries={}
    for split in ('holdout','official'):
        path=root/(split+'.json');raw=json.loads(path.read_text())
        expected={(c,o,s,p) for c in (candidate,'frontier2_early')
            for o in plan['holdout_opponents'] for s in plan[split+'_seeds'] for p in (0,1)}
        assert raw['complete'] and len(raw['rows'])==len(expected)
        assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in raw['rows']}==expected
        for row in raw['rows']:
            for key,column in (('candidate','sha256'),('opponent','opponent_sha256')):
                assert hashlib.sha256(Path('candidates',row[key]+'.py').read_bytes()).hexdigest()==row[column]
        if split=='official':assert raw['engine']=='1.32.7'
        result=assess(path,candidate,latency=split=='official')
        assert result['sha256']==selection['sha256']
        (root/(split+'_summary.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        summaries[split]=result
        assert result['runtime_passed'] and result['baseline_comparison_passed'],result
    decision=dict(created_utc=datetime.now(timezone.utc).isoformat(),candidate_sha256=selection['sha256'],
        release_type='experimental',original_gate_passed=all(r['passed'] for r in summaries.values()),
        failed_original_checks=[s+': V41 score below 50%' for s,r in summaries.items() if not r['v41_gate_passed']],
        decision_timing='After local results, before cloud seeds; not a preregistered success.',
        rationale='The user requests the updated submission. Ship a clearly experimental candidate because it improves paired results against our deployed baseline without per-opponent score regression and passes runtime checks. The failed V41 criterion remains failed. No code retuning on holdout/official seeds.',
        cloud_export_checks='Complete paired games with exact source hashes, positive baseline score difference, no per-opponent score regression, no reported errors/fallbacks/hire shortfalls, every callback below 1000 ms. Report V41 outcome even if its original criterion fails.',
        no_guarantee='Neither rating improvement nor consistent superiority to V41 or gold strength is established.')
    (root/'release_decision.json').write_text(json.dumps(decision,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(decision=decision,summaries=summaries),indent=2))


if __name__=='__main__':main()
