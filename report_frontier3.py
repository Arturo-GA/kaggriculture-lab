"""Summarize measured outcomes without converting an export exception into success."""
import json
from pathlib import Path


def record(path):return json.loads(Path(path).read_text(encoding='utf-8'))


def table(summary):
    lines=['| Rival | Victorias | Empates | Derrotas | Cambio de resultado vs control | Margen medio |',
           '|---|---:|---:|---:|---:|---:|']
    for name,g in summary['per_opponent'].items():
        lines.append(f"| {name} | {g['wins']} | {g['ties']} | {g['losses']} | {g['score_delta']:+g} | {g['mean_margin']:+.1f} |")
    return '\n'.join(lines)


def main():
    root=Path('results/frontier3')
    held=record(root/'holdout_summary.json');official=record(root/'official_summary.json')
    rows=[r for r in record(root/'official.json')['rows'] if r['candidate']==official['candidate']]
    funding=sum(r['telemetry'].get('opening_seed_budget_units',0) for r in rows)
    atomic=sum(r['telemetry'].get('opening_atomic_rescued_confirmed',0) for r in rows)
    capacity=sum(r['telemetry'].get('f3_capacity_turns',0) for r in rows)
    lines=['# Frontier3: apertura financiada y depósitos con capacidad compartida',
        '', '**Estado: candidato experimental.** Mejora frente a nuestras versiones anteriores en estas pruebas, '
        'pero **no superó el criterio predefinido de 50 % frente a V41 en el bloque oficial local**. '
        'La decisión posterior de exportarlo queda explícita en `results/frontier3/release_decision.json`. '
        'El resultado original sigue marcado como fallido; no hay ajuste de código tras observar las semillas reservadas.',
        '', '## Qué cambia y de dónde procede', '',
        '- Apertura con órdenes solicitadas de trigo 5 / 10 / 60, tomada del V41 compartido por Arturo, que acredita a Rayk Kretzschmar. Las cantidades ejecutadas dependen del motor y la liquidez.',
        '- Reserva de dinero para la contratación del primer amanecer y comprobación de semillas: cuatro helpers de Ahmed Berat Ozer, Apache-2.0, integrados sobre Frontier2. La validación de PLANT se generaliza al día actual antes del turno 696.',
        '- Desde el turno 716, asignación conjunta de los 100 espacios del almacén: DROP completo, PLACE de un producto o conservación de carga. Se estima valor con precios visibles y se recalculan ventas a partir del estado propio proyectado.',
        '- Se conserva el critic anterior, sin reentrenamiento. No es un modelo nuevo de RL ni una estrategia enteramente original. Los créditos completos están en NOTICE.md.',
        '', '## Selección y validación', '',
        'Exploración C++: 96 partidas totales, cuatro semillas y tres variantes más Frontier2. '
        'Cada variante obtuvo 20 victorias y 4 derrotas: 4/8 contra V41, 8/8 contra matched6 y 8/8 contra Frontier2. '
        'Las protecciones de recursos y capacidad **no añadieron victorias** respecto a cambiar solo la apertura; '
        'la capacidad redujo ligeramente el margen medio contra V41. Se eligió por sus contratos físicos probados, '
        'sin atribuirle una ventaja competitiva separada.',
        '', '**Panel reservado C++:** 224 partidas totales, candidato y control, ocho semillas nuevas y siete rivales. '
        'Es exploratorio; no sustituye al motor oficial.', '', table(held),
        '', f"Máximo observado C++: {held['max_call_ms']:.1f} ms; incluye creación de observaciones y planificación del sistema. No cumple 1000 ms como medición bruta y no se oculta. El criterio temporal final usa el callback medido en el motor oficial.",
        '', '**Confirmación oficial 1.32.7:** 112 partidas totales, candidato y control, cuatro semillas distintas y ambos asientos.', '', table(official),
        '', f"Máximo de callback del candidato: {official['max_call_ms']:.1f} ms. Errores/fallbacks o contratación inicial insuficiente reportados: {len(official['errors'])}. Todas las partidas completaron 720 estados y 719 llamadas.",
        '', f"Telemetría del candidato en ese bloque: {funding} unidades de compra de semillas recortadas, {atomic} siembras rescatadas y confirmadas, {capacity} turnos con intervención de capacidad. La nueva apertura ya evita la escasez inicial en estas semillas; las protecciones de compra/siembra se comprobaron en casos dirigidos, sin atribuirles las victorias del panel. Se confirmaron las tres contrataciones previstas en cada partida.",
        '', 'La comparación de resultado asigna 1 a victoria, 0,5 a empate y 0 a derrota, y resta el control en el mismo rival, semilla y asiento. No equivale a rating de Kaggle. '
        'Los dos asientos de una semilla pueden producir partidas idénticas: no son muestras estadísticas independientes.',
        '', 'Las 31 pruebas de código pasaron: 30 en la ejecución conjunta y la de empaquetado al repetirla con acceso a su carpeta temporal, que el sandbox había bloqueado. '
        'Siete pruebas nuevas comprueban efectos del motor oficial: apertura, reserva de dinero, siembra factible, capacidad, retención de carga y descarga posterior. No se demuestra que toda la carga retenida llegue a venderse.',
        '', '## Publicación y límites', '',
        f"Agente congelado: `candidates/{official['candidate']}.py`, SHA-256 `{official['sha256']}`.",
        '', 'Notebook privado: https://www.kaggle.com/code/jarturo/kaggriculture-frontier-joint-planner . '
        'El paquete v3 conserva los archivos v1/v2 y el archivo raíz de la primera submission.',
        '', 'El notebook exige 24 partidas oficiales adicionales con hashes exactos, ejecución válida y mejora emparejada frente al control antes de exportar. '
        'El criterio original contra V41 se sigue calculando y comunicando, incluso cuando falla. '
        'Esta excepción de publicación es posterior a los resultados locales, no una validación predefinida aprobada.',
        '', 'El panel contiene V41 y otros rivales públicos almacenados anteriormente; no representa todos los agentes actuales del top. '
        'La capacidad usa precios visibles, no anticipa perfectamente al rival y no garantiza monetizar inventario antes del final. '
        'No se garantiza superar 2797, mejorar el rating anterior ni conseguir medalla.']
    verified=root/'kaggle_verified.json'
    if verified.exists():
        cloud=record(verified)
        lines+=['', '**Kaggle: ejecución y archivo verificados.**', '', table(cloud),
            '', f"Máximo de callback: {cloud['max_call_ms']:.1f} ms; criterio original de este bloque: `{cloud['passed']}`; comprobaciones para exportación experimental: `{cloud['export_checks_passed']}`.",
            '', f"Archivo: `results/frontier3/kaggle/submission.tar.gz`, SHA-256 `{cloud['archive_sha256']}`. El main.py descargado y el contenido del TAR coinciden por bytes con el candidato congelado."]
    else:lines+=['','**Kaggle pendiente:** todavía no se declara verificada una ejecución en la nube ni un envío al leaderboard.']
    submission=root/'submission_receipt.json'
    if submission.exists():
        s=record(submission)
        lines+=['',f"Envío al leaderboard solicitado por Arturo: submission `{s['id']}`, estado observado `{s['status']}` a {s['checked_utc']}. El rating inicial no se toma como resultado final."]
    Path('FRONTIER3_RESULTS.es.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    resume=['Frontier3 — 14 de septiembre de 2026',
        'El usuario pidió enviar la submission con el código actualizado.',
        f"Fuente congelada: {official['candidate']}, SHA-256 {official['sha256']}.",
        'No modificar ni borrar candidatos, archivos o recibos de rondas anteriores.',
        'Resultados y advertencia de criterio V41 fallido: FRONTIER3_RESULTS.es.md.',
        'No reajustar sobre las semillas 93001–96002 ni cambiar el criterio fallido a aprobado.',
        'Reproducir empaquetado: make_frontier3_notebook.py; carpeta kaggle_frontier3/.',
        'Kaggle verificado: '+str(verified.exists()),
        'Envío al leaderboard con recibo: '+str(submission.exists()),
        'Si ya existe submission_receipt.json, consultar su ID antes de cualquier intento nuevo para evitar duplicados.',
        'No crear automatizaciones ni iniciar nuevas rondas sin petición.']
    Path('RESUME_FRONTIER3.es.md').write_text('\n'.join(resume)+'\n',encoding='utf-8')


if __name__=='__main__':main()
