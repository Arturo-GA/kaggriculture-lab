"""Write the final repository status from the actual Kaggle receipt and tests."""
from datetime import datetime,timezone
from pathlib import Path
from release_f21 import ROOT,read,write

def direct_record(path, candidate):
    rows=[r for r in read(path)['rows'] if r['candidate']==candidate and r['opponent']=='f20_value']
    wins=sum(r['win'] for r in rows);draws=sum(r['tie'] for r in rows)
    return dict(games=len(rows),wins=wins,draws=draws,losses=len(rows)-wins-draws,points=wins+.5*draws)

def main():
    choice=read(ROOT/'selection.json');receipt=read(ROOT/'submission_receipt.json')
    release=read(ROOT/'release.json');cloud=read(ROOT/'kaggle_verified.json');private=read(ROOT/'kaggle_private_verified.json')
    active=read(ROOT/'active_after_submission.json')
    assert receipt['leaderboard_submitted'] and not receipt.get('error') and private['is_private'] and cloud['verified']
    assert receipt['status'].split('.')[-1]=='COMPLETE'
    assert {s['id'] for s in active['active']}=={receipt['id'],release['preserve_submission']}
    assert release['candidates']==[choice['selected']] and len(list(ROOT.glob('submission_intent.json')))==1
    holdout=read(ROOT/'holdout_summary.json') if (ROOT/'holdout_summary.json').exists() else None
    losses={n:read(ROOT/f'{n}_findings.json') for n in ('latest_loss','we_are_farmers')}
    record=dict(checked_utc=datetime.now(timezone.utc).isoformat(),selection=choice,submission=receipt,active=active,
        development=read(ROOT/'development_summary.json'),holdout=holdout,cloud=cloud,private_notebook=private,
        direct_records=dict(local=direct_record(ROOT/'holdout.json',choice['selected']),cloud=direct_record(ROOT/'kaggle/results/frontier21/cloud_games.json',choice['selected'])),
        scoring='One point per win and half a point per draw. Points are not win counts.',
        requested_loss_analyses=losses,
        limitations='No rank or medal guarantee. The latest two requested losses remain losses in the frozen diagnostics; the bounded sale adjustment does not solve production-plan gaps. Frozen rivals cannot react.')
    write(ROOT/'final_report.json',record)
    name=choice['selected'];sid=receipt['id'];status=receipt['status'].split('.')[-1]
    if choice['mode']=='measured_improvement':
        assert holdout['pass_gate']
        result=f'La variante {name} pasó los criterios registrados en 192 partidas nuevas: {holdout["scores"][name]:g}/96 puntos frente a {holdout["scores"]["f20_value"]:g}/96 de f20_value. Parte de f20_fill y amplía el máximo de venta residual cubierta de 8 a 12 unidades. La muestra comprende ocho semillas; el intervalo bootstrap por semilla incluye cero, por lo que la ventaja observada sigue siendo incierta. '
    else:
        result='Se envió f20_fill como alternativa empatada, autorizada expresamente por Arturo: 149/160 puntos y los mismos resultados que f20_value en el panel anterior. No se afirma una mejora sobre f20_value. Los nuevos ajustes y cualquier criterio fallido quedan documentados. '
    note=(f'**Último envío, 30 de septiembre: {sid} — {name} — {status}.** '+result+
        f'Notebook privado verificado; 16 partidas técnicas sin errores. Par activo comprobado: {" + ".join(str(s["id"]) for s in active["active"])}. '
        'Se revisaron exactamente las derrotas frente a Tm-ACCS (−23432) y WeAreFarmers (−276): la primera muestra una brecha de capacidad lanera; la segunda, pequeñas diferencias de mercado y cosecha. '
        'El ajuste de 12 unidades no cambia la primera y reduce la segunda a −236 contra acciones grabadas; no la convierte en victoria. '
        '[Resultados y recibos](results/frontier21/final_report.json), '
        '[notebook privado](https://www.kaggle.com/code/jarturo/kaggriculture-frontier21-final-validation). '
        'No hay ningún nuevo envío programado. La evidencia local no garantiza puesto ni medalla.\n')
    start='<!-- frontier21-current -->';end='<!-- /frontier21-current -->'
    for path in (Path('README.md'),Path('GUIA_PARA_EL_PROXIMO_CHAT.es.md')):
        text=path.read_text(encoding='utf-8')
        if start in text:
            before,rest=text.split(start,1);_,after=rest.split(end,1);text=before+start+'\n'+note+end+after
        else:
            first,rest=text.split('\n',1);text=first+'\n\n'+start+'\n'+note+end+'\n'+rest
        path.write_text(text,encoding='utf-8')
    print('Recorded final release',sid,name,status)

if __name__=='__main__':main()
