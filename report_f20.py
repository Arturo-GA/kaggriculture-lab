"""Publish a concise repository status only from verified release receipts."""
import json
from pathlib import Path
from release_f20 import read, write, ROOT

def main():
    selection=read(ROOT/'release_selection.json');name=selection['selected'][0]
    summary_path=Path(selection['source_plans'][name]).with_name('holdout_summary.json')
    holdout=read(summary_path) if summary_path.exists() else None
    admission=read(ROOT/'experimental_admission.json')
    release=read(ROOT/'release.json');cloud=read(ROOT/'kaggle_verified.json')
    private=read(ROOT/'kaggle_private_verified.json');receipt=read(ROOT/(name+'_submission_receipt.json'))
    active=read(ROOT/'active_after_submission.json');diag=read(ROOT/'diagnostic_summary.json')
    assert selection['selected']==release['candidates']==[name]
    assert cloud['verified'] and private['is_private']
    assert selection['validation_status']=='experimental_controls_pending_user_requested'
    assert receipt['status'] in ('SubmissionStatus.COMPLETE','SubmissionStatus.PENDING','SUBMITTED') and receipt['leaderboard_submitted']
    assert {r['id'] for r in active['active']} in ({receipt['id'],56714342},{56714336,56714342})
    record=dict(submission=receipt,active=active,holdout=holdout,cloud=cloud,private_notebook=private,
        changes=dict(candidate=name,residual_sales=True,wool_urgency_with_economic_guard=name=='f20_value'),
        diagnostic_gain=diag['variants'][name],selection=selection,
        grigor=read(ROOT/'grigor/status.json'),
        experimental_admission=admission,
        candidate_behavior=read(ROOT/'candidate_behavior_summary.json'),
        first_live_check=read(ROOT/'first_live_check.json'),
        second_submission_decision=read(ROOT/'second_submission_decision.json') if (ROOT/'second_submission_decision.json').exists() else None,
        limitation='First experimental submission explicitly requested before the full controls completed. Eight independent seeds and correlated public families. No demonstrated top300-400 rank, guaranteed rating, silver medal or victory against Grigor. One immediate submission authorized and sent; a second is authorized only if subsequent controls demonstrate improvement.',
        source_evidence=[selection['source_plans'][name],str(Path(selection['source_plans'][name]).with_name('holdout.json')),'results/frontier20/loss_audit.json','results/frontier20/diagnostic_summary.json','results/frontier20/kaggle_verified.json'])
    write(ROOT/'final_report.json',record)
    ev=holdout['candidates'][name] if holdout else admission;sid=receipt['id']
    deltas={n:d['score_delta'] for n,d in ev.get('comparisons',{}).items()}
    comparison=(f'Controles completos: {deltas["f19_market1"]:+g} puntos frente a Market1 y {deltas["f19_market2"]:+g} frente a Market2 en {holdout["games"]} juegos; paso del criterio registrado: {ev["pass_gate"]}. ' if holdout else 'Los controles comparativos siguen pendientes. ')
    second=record['second_submission_decision']
    second_note=('No se envió una segunda plaza: la alternativa no demostró mejora sobre la ya enviada. ' if second and not second['submit_second'] else 'Segunda plaza condicionada a demostrar una mejora después de los controles. ')
    status=receipt['status'].split('.')[-1]
    active_ids=' + '.join(str(r['id']) for r in active['active'])
    note=(f'**30 de septiembre, Frontier20: una submission privada, {sid}, {status}.** '
        'Se reconstruyeron las 23 derrotas públicas disponibles de las dos submissions anteriores. '+
        ('La nueva capa completa pequeñas ventas cubiertas y prioriza lana solo si el riesgo de precio supera el fertilizante. ' if name=='f20_value' else 'La nueva capa completa pequeñas ventas cubiertas conservando la producción y las rutas anteriores. ')+
        f'Se envió por petición explícita como experimento con controles pendientes, después de {admission["wlt"][0]}V/{admission["wlt"][1]}D/{admission["wlt"][2]}E en 160 juegos de la candidata. '+comparison+
        'La primera candidata falló y se conserva su resultado. '+
        f'Kaggle completó {cloud["games"]} juegos de verificación y confirmó el paquete idéntico. '
        f'Par activo confirmado a {active["checked_utc"]}: {active_ids}. '+second_note+
        '[Resultados y recibos](results/frontier20/final_report.json), '
        '[investigación](results/frontier20/research_summary.json), '
        f'[código](candidates/{name}.py), '
        '[notebook privado](https://www.kaggle.com/code/jarturo/kaggriculture-frontier20-policy-validation). '
        'La mejora local no garantiza puesto ni medalla; no se verificó una victoria contra Grigor.\n')
    start='<!-- frontier20-current -->';end='<!-- /frontier20-current -->'
    for p in (Path('README.md'),Path('GUIA_PARA_EL_PROXIMO_CHAT.es.md')):
        text=p.read_text(encoding='utf-8')
        if start in text:
            before,rest=text.split(start,1);_,after=rest.split(end,1)
            text=before+start+'\n'+note+end+after
        else:
            first,rest=text.split('\n',1)
            text=first+'\n\n'+start+'\n'+note+end+'\n'+rest
        p.write_text(text,encoding='utf-8')
    print(json.dumps(dict(submission=sid,status=receipt['status'],deltas=deltas,active=[r['id'] for r in active['active']]),indent=2))

if __name__=='__main__':main()
