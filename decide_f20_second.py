"""Apply the later user condition to a completed, unchanged comparative panel."""
from datetime import datetime,timezone
from release_f20 import ROOT,read,write,digest

def main():
    folder=ROOT/'value_gate'
    data=read(folder/'holdout.json');summary=read(folder/'holdout_summary.json')
    assert data['complete'] and summary['complete'] and len(data['rows'])==640
    assert summary['holdout_sha256']==digest(folder/'holdout.json')
    first='f20_value';second='f20_fill'
    rows={n:{(r['opponent'],r['seed'],r['seat']):r for r in data['rows'] if r['candidate']==n} for n in (first,second)}
    assert len(rows[first])==len(rows[second])==160 and rows[first].keys()==rows[second].keys()
    points=lambda r:r['win']+.5*r['tie']
    delta={k:points(rows[second][k])-points(rows[first][k]) for k in rows[first]}
    controls=read(folder/'plan.json')['controls']
    total=sum(delta.values());outside=sum(d for k,d in delta.items() if k[0] not in controls)
    by_seed={s:sum(d for k,d in delta.items() if k[1]==s) for s in sorted({k[1] for k in delta})}
    per_opponent={o:sum(d for k,d in delta.items() if k[0]==o) for o in sorted({k[0] for k in delta})}
    # No tie-break can spend a second slot under the user's newer instruction.
    # A positive result still needs review; this tool never submits.
    improved=total>0 and outside>=0 and summary['candidates'][second]['pass_gate']
    result=dict(checked_utc=datetime.now(timezone.utc).isoformat(),first=first,alternative=second,
        first_submission=read(ROOT/'f20_value_submission_receipt.json')['id'],
        user_condition=read(ROOT/'experimental_admission.json')['second_submission'],
        complete_games=640,paired_games_per_candidate=160,
        scores={n:summary['scores'][n] for n in (first,second)},
        alternative_minus_first=total,nonmirror_delta=outside,per_seed_delta=by_seed,
        per_opponent_delta=per_opponent,changed_point_outcomes=sum(d!=0 for d in delta.values()),
        original_frozen_gate={n:summary['candidates'][n]['pass_gate'] for n in (first,second)},
        submit_second=False,improvement_requires_review=improved,
        reason=('Positive paired difference requires review before a second release.' if improved else
            'No demonstrated improvement over the first release. Equal outcomes do not justify another submission; the original simplicity tie-break is not evidence of improvement.'),
        holdout_sha256=digest(folder/'holdout.json'))
    write(ROOT/'second_submission_decision.json',result)
    print(__import__('json').dumps(result,indent=2))

if __name__=='__main__':main()
