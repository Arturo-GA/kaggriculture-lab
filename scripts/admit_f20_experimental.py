"""Record the user's later request without rewriting the frozen competitive gate."""
from datetime import datetime,timezone
from release_f20 import ROOT, read, write, digest, eligible

AUTHORIZATION='Veo prometedora a esta semilla envia 1 submission a kaggle ahora y despues de los controles si vemos mejoras mandamos otra plaza'

def main():
    assert not (ROOT/'release_selection.json').exists()
    plan=read(ROOT/'value_gate'/'plan.json')
    data=read(ROOT/'value_gate'/'holdout.json')
    rows=[r for r in data['rows'] if r['candidate']=='f20_value']
    assert len(rows)==160
    path=ROOT/'value_gate'/'experimental_f20_value_games.json'
    write(path,dict(engine=data['engine'],complete_candidate_slice=True,full_panel_complete_at_admission=data['complete'],rows=rows))
    admission=dict(candidate='f20_value',source_sha256=plan['hashes']['f20_value'],
        candidate_games_sha256=digest(path),created_utc=datetime.now(timezone.utc).isoformat(),
        user_authorization=AUTHORIZATION,user_requested_immediate_submission=True,
        controls_pending=True,competitive_gate_passed=None,original_candidate_gate_passed=False,
        wlt=[sum(r['win'] for r in rows),sum(r['margin']<0 for r in rows),sum(r['tie'] for r in rows)],
        max_call_ms=max(r['max_call_ms'] for r in rows),second_submission='Only if completed controls demonstrate improvement over this first release; not merely a tie.')
    write(ROOT/'experimental_admission.json',admission)
    write(ROOT/'release_selection.json',dict(selected=['f20_value'],
        source_plans={'f20_value':(ROOT/'value_gate'/'plan.json').as_posix()},
        validation_status='experimental_controls_pending_user_requested',authorization=AUTHORIZATION,
        caveat='Immediate experimental release explicitly requested by user; comparative gate not yet assessed. Original failed selection and all frozen thresholds are preserved.'))
    assert eligible('f20_value')
    print(admission)

if __name__=='__main__':main()
