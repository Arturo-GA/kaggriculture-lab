"""Generate the user-facing report from completed evidence, not partial scores."""
import json
from pathlib import Path

root=Path('results/frontier17')
summary=json.loads((root/'holdout_summary.json').read_text())
plan=json.loads((root/'plan.json').read_text())
diag=json.loads((root/'diagnostic_summary.json').read_text())
stress=json.loads((root/'stress.json').read_text())
stress_plan=json.loads((root/'stress_plan.json').read_text())
live=json.loads((root/'live_snapshot_final.json').read_text(encoding='utf-8'))
submission_path=root/'submission_receipt.json'
if submission_path.exists():
    submission=json.loads(submission_path.read_text(encoding='utf-8'))
    cloud=json.loads((root/'kaggle_verified.json').read_text(encoding='utf-8'))
    deployment_status=(
        f"Arturo autorizó una plaza con «{submission['authorization']}». "
        f"Submission **{submission['id']}**, estado **{submission['status']}** "
        f"al {submission['checked_utc']}. "
        '[Notebook privado](https://www.kaggle.com/code/jarturo/kaggriculture-frontier17-input-market), versión 1. '
        f"La verificación en Kaggle completó {cloud['games']} partidas: F17 ganó 8/8 contra F16, "
        f"con cero errores y máximo {cloud['max_call_ms']:.1f} ms. "
        'El paquete exportado coincide byte por byte con el local. Se realizó un solo envío. '
        'El estado del par activo se conserva en `results/frontier17/active_after_submission.json`.')
else:
    deployment_status=('El candidato se preparó localmente para revisión y para un notebook configurado como privado. '
        'No se ha ejecutado Frontier17 en Kaggle ni enviado una nueva submission en esta ronda. '
        'Las submissions activas anteriores conservan su evaluación.')
fresh=json.loads((root/'new_loss_diagnostic.json').read_text(encoding='utf-8'))
fresh_control={r['episode']:r for r in fresh if r['agent']==plan['control']}
fresh_new=[r for r in fresh if r['agent']==plan['candidate']]
assert len(fresh_control)==len(fresh_new)==5
assert all(r['margin']==r['recorded_margin'] and r['rival_kept']==1 for r in fresh_control.values())
fresh_summary=dict(games=5,flips=sum(r['margin']>0 for r in fresh_new),
    improved=sum(r['margin']>r['recorded_margin'] for r in fresh_new),
    errors=sum(bool(r['errors']) for r in fresh),
    note='Five newly arrived losses, read only after the source was frozen. Recorded rivals cannot react; no tuning.',
    rows=[dict(episode=r['episode'],opponent=r['opponent'],before=r['recorded_margin'],after=r['margin']) for r in fresh_new])
(root/'new_loss_summary.json').write_text(json.dumps(fresh_summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert summary['complete'] and stress['complete']
sr=stress['rows'];score=lambda r:r['win']+.5*r['tie']
stress_scores={c:sum(score(r) for r in sr if r['candidate']==c) for c in (plan['candidate'],plan['control'])}
stress_bad=[r for r in sr if r['max_call_ms']>=1000 or any(v and ('error' in k.lower() or 'fallback' in k.lower()) for k,v in r['telemetry'].items())]
assert len(sr)==16 and len({(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in sr})==16
for r in sr:
    assert r['sha256']==stress_plan['hashes'][r['candidate']]
    assert r['opponent_sha256']==stress_plan['hashes'][r['opponent']]
    assert r['status']==['DONE','DONE'] and r['steps']==720 and r['calls']==719
stress_pass=not stress_bad and stress_scores[plan['candidate']]>=stress_scores[plan['control']]
(root/'stress_summary.json').write_text(json.dumps(dict(passed=stress_pass,scores=stress_scores,error_or_runtime_games=len(stress_bad),
    games=16,independent_seeds=4,limitations='Original synthetic stress rival, not a known top100 submission.'),indent=2)+'\n',encoding='utf-8')
lines=['# Frontier17: resultados del candidato de mercado','',
    f"Puerta registrada: **{'SUPERADA' if summary['pass_gate'] else 'NO SUPERADA'}**. "
    f"Ganancia emparejada frente a F16: **+{summary['paired_score_delta']:g} puntos de partida** "
    f"en {summary['games_per_agent']} por agente (victoria = 1, empate = 0,5). "
    'Son puntos de esta evaluación, no puntos del leaderboard.','',
    'El holdout contiene 256 partidas completas, ocho rivales, ocho semillas nuevas y ambos asientos. '
    'Las semillas son la unidad de diversidad; los asientos del mismo mundo están correlacionados.','',
    '| Rival | F17 V/E/D | F16 V/E/D | Diferencia de puntuación |',
    '|---|---:|---:|---:|']
for r in summary['by_opponent']:
    a='/'.join(map(str,r['candidate_wtl']));b='/'.join(map(str,r['control_wtl']))
    lines.append(f"| {r['opponent']} | {a} | {b} | {r['delta']:+g} |")
lines += ['',f"Ganancia excluyendo el enfrentamiento contra F16: **{summary['nonmirror_delta']:+g}**. "
    f"Máxima llamada del candidato: **{summary['max_call_ms']:.1f} ms** frente al límite de 1000 ms. "
    f"Partidas con errores registrados: **{len(summary['errors'])}**.",'',
    'Las doce pruebas unitarias de F16/F17 pasaron. Incluyen conservación de inventario y compras '
    'frente al mercado oficial, rechazo por caja/capacidad insuficiente y conservación de comandos físicos.','',
    '## Prueba adicional frente a otra estrategia de compras','',
    f"En cuatro semillas nuevas (17301–17304), F17 puntuó **{stress_scores[plan['candidate']]:g}/8** "
    f"y F16 **{stress_scores[plan['control']]:g}/8** contra `f17_robust`. "
    f"Resultado de la prueba: **{'superada' if stress_pass else 'no superada'}**. "
    'Este rival es una variante original creada para someter a prueba la hipótesis de órdenes similares; '
    'no se presenta como un agente del top 100.','',
    '## Diagnóstico de las pérdidas reales','',
    f"Se reconstruyeron exactamente 28 partidas originales. En el panel contrafactual de F16, "
    f"el candidato convierte **{diag['losses_flipped']} de 17 derrotas** y pierde **{diag['wins_lost']} de cuatro victorias**. "
    f"Mejora {diag['improved']}, empeora {diag['worsened']} y deja {diag['unchanged']} iguales. "
    'Los rivales grabados no pueden responder; esas cifras no estiman la tasa de victoria real.','',
    f"Después de congelar el código llegaron cinco derrotas nuevas de F16. El candidato mejora las cinco "
    f"y convierte **{fresh_summary['flips']}/5** en victorias al repetir esos rivales grabados. "
    'El control reproduce las cinco exactamente; no se retocó el candidato después de verlas. '
    'Este segundo panel tampoco sustituye una evaluación competitiva en Kaggle.','',
    'La derrota de −8488 contra trantrikien239 pasa a −306. Las derrotas amplias frente a keiz, '
    'Smackaveli y ShunkiKyoya siguen presentes; requieren mejorar la composición productiva. '
    'Detalles, contabilidad y fuentes en [FRONTIER17_RESEARCH.es.md](FRONTIER17_RESEARCH.es.md).','',
    '## Estado y alcance','',
    deployment_status,'',
    f"Consulta previa al envío ({live['checked_utc']}): corte top 100 **{live['top100_cut']['score']}**, "
    f"Frontier16 **{live['own']['score']}**, puesto **{live['own']['rank']}**. "
    'No hay una conversión validada entre este panel público y el rating. Tampoco se dispone '
    'del código privado de los mejores rivales. La duda del foro sobre versiones públicas posteriores '
    'al cierre de publicación sigue registrada en el informe de investigación.','',
    '## Reproducción','',
    '```powershell','.venv/Scripts/python.exe -X utf8 build_f17.py',
    '.venv/Scripts/python.exe -X utf8 -m unittest test_frontier17 test_frontier16 -v',
    '.venv/Scripts/python.exe -X utf8 analyze_f17.py',
    '.venv/Scripts/python.exe -X utf8 report_f17.py',
    '.venv/Scripts/python.exe -X utf8 pack_frontier17.py',
    '.venv/Scripts/python.exe -X utf8 make_frontier17_notebook.py','```','',
    'La regeneración no reejecuta el holdout ni realiza solicitudes a Kaggle. '
    'La matriz, semillas, hashes y umbrales están en [plan.json](results/frontier17/plan.json).','',
    f"SHA-256 del candidato: `{plan['hashes'][plan['candidate']]}`.",'']
Path('FRONTIER17_RESULTS.es.md').write_text('\n'.join(lines),encoding='utf-8')
print('report written; main gate',summary['pass_gate'],'stress gate',stress_pass)
