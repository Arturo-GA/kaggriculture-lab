"""Produce the V41 diagnosis from complete frozen receipts, with cross-checks."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from statistics import mean

OUT=Path('results/review_v41')
LABELS={'matched6':'Primera (matched6)','ml_critic':'ML critic','frontier':'Joint Planner v1','frontier2_early':'Joint Planner v2'}


def read(name):
    return json.loads((OUT/name).read_text(encoding='utf-8'))


def aggregate(rows):
    return dict(games=len(rows),wins=sum(r['win'] for r in rows),ties=sum(r['tie'] for r in rows),
        losses=sum(1-r['win']-r['tie'] for r in rows),mean_margin=mean(r['margin'] for r in rows),
        max_call_ms=max(r['max_call_ms'] for r in rows))


def main():
    plan=read('plan.json');fast=read('fast.json');official=read('official.json');ablation=read('ablation.json')
    physical=read('physical_audit.json');live=read('live_audit.json');submissions=read('submissions.json')
    assert physical['complete'] and live['complete'] and len(physical['rows'])==32
    assert all(r['exact_actions'] for r in physical['rows'])
    assert all(r['statuses']==['DONE','DONE'] for s in live['submissions'] for r in s['rows'])
    panels={}
    for name,report,seeds in [('fast',fast,plan['fast_seeds']),('official',official,plan['official_seeds'])]:
        expected={(c,o,s,p) for c in plan['candidates'] for o in plan['opponents'] for s in seeds for p in (0,1)}
        actual={(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in report['rows']}
        assert report['complete'] and len(report['rows'])==len(expected) and actual==expected
        for r in report['rows']:
            assert r['sha256']==hashlib.sha256(Path('candidates',r['candidate']+'.py').read_bytes()).hexdigest()
            assert r['opponent_sha256']==hashlib.sha256(Path('candidates',r['opponent']+'.py').read_bytes()).hexdigest()
            assert r['status']==['DONE','DONE'] and r['calls']==719 and r['steps']==720
        panels[name]={c:{o:aggregate([r for r in report['rows'] if r['candidate']==c and r['opponent']==o]) for o in plan['opponents']} for c in plan['candidates']}
    assert ablation['complete'] and len(ablation['rows'])==16
    assert {(r['candidate'],r['opponent'],r['seed'],r['seat']) for r in ablation['rows']}=={
        (c,'frontier2_early',s,p) for c in ('v41_review','v41_old_opening') for s in plan['official_seeds'] for p in (0,1)}
    for row in ablation['rows']:
        assert row['sha256']==hashlib.sha256(Path('candidates',row['candidate']+'.py').read_bytes()).hexdigest()
        assert row['status']==['DONE','DONE'] and row['calls']==719
    reference={(r['seed'],r['seat']):r for r in official['rows'] if r['candidate']=='frontier2_early' and r['opponent']=='v41_review'}
    for row in ablation['rows']:
        if row['candidate']=='v41_review':
            control=reference[row['seed'],1-row['seat']]
            assert row['rewards']==control['rewards'] and row['margin']==-control['margin']
    ab={c:aggregate([r for r in ablation['rows'] if r['candidate']==c]) for c in ('v41_review','v41_old_opening')}
    cases={c:read(c+'_economy.json') for c in ('matched6','frontier2_early')}
    for candidate,case in cases.items():
        ref=next(r for r in official['rows'] if r['candidate']==candidate and r['opponent']=='v41_review' and r['seed']==case['seed'] and r['seat']==case['seat'])
        assert case['rewards']==ref['rewards'], 'Instrumentation must not change actual rewards.'
    first=cases['matched6']
    assert [first['snapshots']['24'][str(s)]['farm']['money'] for s in (0,1)]==[1,56]
    assert [first['snapshots']['25'][str(s)]['farm']['hands'] for s in (0,1)]==[1,3]
    assert [r.get('atomic_plant_rejections',0) for r in first['field_counts']]==[10,0]
    assert [r['harvested_MILK'] for r in first['field_counts']]==[164,266]
    assert [r['harvested_STRAWBERRY'] for r in first['field_counts']]==[182,249]
    live_summary={}
    for submission in live['submissions']:
        rows=submission['rows'];counts=Counter();late=Counter()
        for r in physical['rows']:
            if r['candidate']==submission['candidate']:
                counts.update(r['field_counts']);late.update(r['last_day_counts'])
        live_summary[submission['candidate']]=dict(wins=sum(r['margin']>0 for r in rows),losses=sum(r['margin']<0 for r in rows),
            losses_with_cash_deficit_at_696=sum(r['margin']<0 and r['snapshots']['696']['gap']<0 for r in rows),
            field_counts=dict(counts),last_day_counts=dict(late))
    summary=dict(panels=panels,ablation=ab,live=live_summary,action_identity_games=32,
        validations='Exact source hashes, full official status, ordered replay identity, 2 unchanged instrumented rewards, 8 reversed-seat controls.',
        caveats='Descriptive small samples. No conversion of game currency to ladder rating. Ablation is post-hoc. No new submission produced.')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    lines=['# Revisión del V41 y de nuestras submissions — 14 de septiembre de 2026','',
        'La principal vulnerabilidad identificada es el arranque de nuestra base V37 frente a una apertura comercial distinta. '
        'Puede quedarse sin dinero para contratar y comprar los insumos de su calendario. Las mejoras de venta y cierre '
        'no reparan esa cadena temprana. El V41 no necesita una nueva red neuronal para explotar esta diferencia.','',
        '## Puntuaciones consultadas','',
        f"Consulta de Kaggle: `{submissions['retrieved_utc']}`. El 2797 de V41 es el valor comunicado por Arturo; "
        'el notebook adjunto no identifica una submission que permita vincular y verificar ese rating. Se compara su código exacto.'
    ]
    lines+=['','| Versión | Submission | Rating observado |','|---|---:|---:|']
    mapping={'56216380':'frontier2_early','56214804':'frontier','56213093':'ml_critic','56190498':'matched6'}
    for s in reversed(submissions['submissions'][:4]):
        lines.append(f"| {LABELS[mapping[s['ref']]]} | {s['ref']} | {s['public_score']} |")
    lines+=['','Estas lecturas pertenecen a partidas y momentos distintos. La primera submission tiene episodios más antiguos '
        'en esta consulta. La diferencia de rating no demuestra por sí sola que una versión pierda el duelo directo; '
        'por eso se añaden rivales, semillas y lados compartidos.','',
        '## Comparación nueva con agentes que reaccionan','',
        '128 partidas exploratorias C++ (ocho semillas) y 64 oficiales (otras cuatro semillas), sin ajustar candidatos '
        'después de ver resultados. Cada contexto se juega en ambos lados. Son 192 partidas, no 192 mundos independientes. '
        'El simulador C++ conserva sus limitaciones conocidas; las conclusiones centrales tienen confirmación oficial.','',
        '| Nuestra versión | Contra V41: V/E/D oficial | Margen medio oficial | Contra primera versión: V/E/D oficial |',
        '|---|---:|---:|---:|']
    for candidate in LABELS:
        a=panels['official'][candidate]['v41_review'];b=panels['official'][candidate]['matched6']
        lines.append(f"| {LABELS[candidate]} | {a['wins']}/{a['ties']}/{a['losses']} | {a['mean_margin']:,.1f} monedas | {b['wins']}/{b['ties']}/{b['losses']} |")
    lines+=['','En exploración las cuatro versiones pierden 0/0/16 contra V41. Las tres posteriores ganan 16/0/0 '
        'contra la primera. Por tanto, las mejoras locales existían frente a esa política, pero no demostraban una ventaja '
        'general en el torneo. El margen en monedas no es el rating de Kaggle.','',
        'El máximo de llamada de nuestras versiones en este panel oficial es 254,0 ms. El cronómetro exploratorio C++ '
        'registró picos superiores a un segundo, hasta 1379,7 ms, durante la ejecución concurrente; incluye creación '
        'de observaciones y tiempo de espera del proceso. Se conservan esos datos y no se declara superada una prueba '
        'universal de latencia. No hubo terminaciones por error en las 64 partidas oficiales ni en los 32 episodios auditados.','',
        '## Prueba causal de la apertura','',
        'Se hizo una ablación posterior de diagnóstico: conservar V41 íntegro y sustituir únicamente su secuencia inicial '
        '`BUY WHEAT 5 → BUY WHEAT 10 → SELL WHEAT 60` por nuestra secuencia '
        '`BUY WHEAT 13 → BUY WHEAT 30 → SELL WHEAT 30`. Las cantidades son órdenes solicitadas; el motor puede ejecutar solo una parte. '
        'Se conservaron todas sus reservas de caja, protecciones físicas y controladores posteriores.','',
        '| Rival de Joint Planner v2 | V/E/D del rival | Margen medio del rival |','|---|---:|---:|']
    for key,label in [('v41_review','V41 completo'),('v41_old_opening','V41 con nuestra apertura')]:
        a=ab[key];lines.append(f"| {label} | {a['wins']}/{a['ties']}/{a['losses']} | {a['mean_margin']:,.1f} monedas |")
    lines+=['','Son 16 partidas oficiales en cuatro semillas ya utilizadas, con ambos lados. El control completo reproduce '
        'exactamente las recompensas de los duelos anteriores al invertir los lados. La apertura cambia todos los ganadores '
        'en esta muestra. Esto no demuestra que copiar esa apertura gane a cualquier rival, ni que las restantes reglas de '
        'V41 sean inútiles. La combinación y el rival importan; una apertura fija nueva también puede recibir una respuesta.','',
        '## Cadena económica reproducida','',
        'Caso oficial, semilla 92001, primera versión en el lado 0:','',
        '| Momento o resultado | Primera versión | V41 |','|---|---:|---:|',
        '| Dinero después del turno inicial | 2609 | 3034 |',
        '| Dinero al iniciar el segundo día, turno 24 | 1 | 56 |',
        '| Trabajadores después de contratar, turno 25 | 1 | 3 |',
        '| Siembras rechazadas por el lote atómico, partida completa | 10 | 0 |',
        '| Vacas al turno 288 | 6 | 9 |',
        '| Plantas de fresa al turno 288 | 25 | 33 |',
        '| Leche cosechada durante la partida | 164 | 266 |',
        '| Fresa cosechada durante la partida | 182 | 249 |',
        '| Dinero final | 107554 | 142723 |','',
        'El motor rechaza **todas** las siembras de un cultivo en ese turno si el conjunto de órdenes pide más semillas '
        'de las disponibles. Contratar menos trabajadores también invalida supuestos de las rutas programadas. '
        'V41 reserva dinero para la siguiente contratación y limita las siembras a recursos observados.','',
        'La contabilidad de transacciones reales cierra exactamente: dinero inicial + ventas − compras − tierra − salarios '
        '= dinero final. La instrumentación reproduce las recompensas del panel oficial sin cambiar acciones. '
        'Los 35.169 de diferencia contra la primera versión se convierten en 34.701 contra v2: una recuperación de solo 468 '
        'monedas de margen en ese mundo. Antes del último día v2 ya va 34.192 por detrás.','',
        '## Partidas realmente jugadas en Kaggle','',
        'Se seleccionaron las ocho partidas públicas completadas más recientes de cada submission, sin escoger por resultado. '
        'Las 32 reproducen las 719 acciones de su candidato local. No aparece evidencia de haber enviado una política diferente '
        'en esas partidas. Los agentes del rival no se sustituyeron por replays para atribuir victorias contrafactuales.','',
        '| Versión | Victorias / derrotas observadas | Derrotas con desventaja de caja al turno 696 |','|---|---:|---:|']
    for candidate in LABELS:
        a=live_summary[candidate];lines.append(f"| {LABELS[candidate]} | {a['wins']} / {a['losses']} | {a['losses_with_cash_deficit_at_696']} / {a['losses']} |")
    lines+=['','Las muestras tienen rivales y fechas diferentes: estos cocientes no comparan fuerza de manera causal. '
        'En v1, la derrota contra Alan ya era de 36.743 monedas al turno 696 y termina en 36.840; se observaron nueve '
        'órdenes de siembra rechazadas, una fuga de animal y recogidas incompletas de insumos. Es coherente con el fallo temprano '
        'que aparece en las pruebas contra V41.','',
        'También hay un fallo pendiente en v2: **24 unidades descartadas en el último turno de dos partidas**, '
        '11 de leche, siete de fertilizante, cuatro de trigo y dos de huevo. El planificador calcula retornos por ruta, '
        'pero todavía no coordina completamente la capacidad compartida del almacén. Las entregas intermedias reducen '
        'algunos casos; no eliminaron el problema. No se afirma que recuperar esas unidades hubiese ganado esas dos partidas.','',
        'La auditoría inicial encontró tres discrepancias aparentes. El JSON del replay ordena las claves; el motor conserva '
        'el orden de inserción, que afecta a DROP con almacén lleno y al desempate de ventas. Se reconstruyó el orden de '
        'inventario desde las acciones efectivas, verificando en cada turno que las cantidades fueran idénticas. Así se '
        'reproducen las 32 partidas. Se guardan ambos informes. Las muertes de plantas por sed se reportan en bruto y '
        'pueden incluir reemplazos intencionales; no se suman automáticamente como errores.','',
        '## Qué falló en nuestro proceso y qué cambiar','',
        '1. **Panel de rivales insuficiente.** Los rivales externos anteriores ya estaban mayormente resueltos; las ganancias '
        'adicionales se concentraban contra nuestras propias versiones. Más semillas del mismo grupo no corrigieron esa falta de diversidad.',
        '2. **Momento de intervención tardío.** El critic cambia ventas desde el turno 336; Joint Planner actúa desde el 696. '
        'La fragilidad observada aparece antes del turno 25 y todas las versiones la heredan.',
        '3. **Medición de órdenes frente a efectos.** Los contadores de errores de los nuevos módulos podían ser cero '
        'mientras el calendario heredado perdía siembras, trabajadores o insumos. La validación debe medir recursos realmente obtenidos y usados.',
        '4. **Sobreinterpretación del progreso local.** V2 mejoró frente a v1, pero debió presentarse como una mejora de esa '
        'familia y esos rivales, con evidencia insuficiente de mejora del rating general.',
        '5. **Siguiente candidato.** Probar un arranque con reserva explícita de caja y semillas, reconciliar el calendario '
        'con contrataciones/compras confirmadas y coordinar depósitos para evitar desbordamiento. Compararlo con V41 exacto, '
        'nuestra primera submission y una colección actualizada de aperturas distintas, manteniendo las ablaciones. '
        'No sumar otra capa de último día antes de resolver ese cuello de botella.','',
        'El V41 adjunto también declara que no pasó una de sus pruebas de confianza frente a registros de élite. '
        'Sus resultados declarados no se presentan aquí como mediciones nuestras. No se ha demostrado nivel gold '
        'ni se ha creado o enviado una nueva submission.','',
        '## Evidencia y reproducción','',
        '- `results/review_v41/source.json`: hashes del notebook y del código, atribuciones y extracción sin ejecutar celdas.',
        '- `plan.json`, `fast.json`, `official.json`, `summary.json`: protocolo y partidas completas.',
        '- `ablation_plan.json`, `ablation.json`: intervención de una sola secuencia de apertura.',
        '- `live_audit.json`, `physical_audit.json`: episodios públicos, identidad y efectos físicos.',
        '- `matched6_economy.json`, `frontier2_early_economy.json`: trazas y contabilidad oficial.',
        '- `prepare_v41_review.py`, `prepare_v41_ablation.py`, `audit_v41_live.py`, `diagnose_v41_replays.py`, '
        '`trace_v41_economy.py`, `report_v41_review.py`: herramientas de reproducción.',
        '', 'El notebook de entrada, los replays completos y las dos copias de V41 para evaluación quedan fuera de Git. '
        'Las atribuciones Apache-2.0 se conservan en las copias locales. Se mantienen intactos nuestros cuatro candidatos y archivos de envío.', '']
    Path('V41_REVIEW.es.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
