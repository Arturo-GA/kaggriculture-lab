"""Write a human-readable report from complete frozen evidence, never from projected results."""
import json
from pathlib import Path


def main():
    root=Path('results/frontier16/repaired');plan=json.loads((root/'plan.json').read_text());gate=json.loads((root/'holdout_summary.json').read_text())
    raw=json.loads((root/'holdout.json').read_text());package=json.loads((root/'local_package.json').read_text())
    assert raw['complete'] and gate['registered_gate_passed'] and package['notebook_payload_verified']
    cloud=json.loads((root/'kaggle_verified.json').read_text()) if (root/'kaggle_verified.json').exists() else None
    submission=json.loads((root/'submission_receipt.json').read_text()) if (root/'submission_receipt.json').exists() else None
    def summary(name):
        rs=[r for r in raw['rows'] if r['candidate']==name];w=sum(r['win'] for r in rs);t=sum(r['tie'] for r in rs)
        return w,t,len(rs)-w-t,w+.5*t
    names=[('F15 desplegado',plan['control']),('Base pública sin modificar',plan['public_base']),('F16 corregido',plan['candidate'])]
    lines=['# Frontier16 — resultados del 27 de septiembre de 2026','',
        ('**Frontier16 enviada:** `f16_repaired`, submission `%s`, estado `%s`. Notebook privado y verificación en Kaggle completados.' % (submission['id'],submission['status']) if submission and cloud else
         '**Candidato recomendado para la siguiente verificación en Kaggle:** `f16_repaired`. Validado localmente; todavía no enviado al leaderboard ni verificado en la nube.'),'',
        '## Comparación congelada','',
        'Motor oficial `kaggle-environments==1.32.7`. Ocho semillas nuevas (`16301..16308`), diez rivales, ambos asientos y tres políticas: 480 partidas completas. Cada política juega 160. Los asientos comparten mundo: hay ocho semillas independientes, no 160.','',
        '| Política | Victorias | Empates | Derrotas | Puntos (V + ½E) |','|---|---:|---:|---:|---:|']
    for label,name in names:lines.append('| '+label+' | '+' | '.join(f'{v:g}' for v in summary(name))+' |')
    lines+=['',f"F16 mejora **{gate['total_score_delta']:+g} puntos frente a F15** y **{gate['ablation_score_delta']:+g} frente a la base pública** en el mismo panel. El cambio completo mezcla avance público y capas propias; el segundo número mide el aporte de las capas sobre esa base.",'',
        '| Rival | F16 V/E/D | Delta de puntos frente a F15 | Delta frente a base pública |','|---|---:|---:|---:|']
    for opponent in plan['opponents']:
        g=gate['per_opponent'][opponent]
        lines.append(f"| `{opponent}` | {g['wins']}/{g['ties']}/{g['losses']} | {g['score_delta']:+g} | {gate['ablation_per_opponent'][opponent]:+g} |")
    lines+=['','Se respetaron todas las puertas registradas antes de la prueba: +6 puntos o más frente a F15, al menos 65 % en el enfrentamiento directo, al menos 50 % contra la base pública, ningún rival por debajo de −2 puntos, aporte propio total no negativo y ejecución sin errores registrados. No se cambiaron los umbrales después de ver resultados.','',
        f"Máximo observado por callback: **{gate['max_call_ms']:.1f} ms** en este equipo con seis procesos. Cada partida terminó con 719 decisiones y 720 estados. Nueve pruebas unitarias pasaron; dos pruebas diferenciales confirmaron 1438 decisiones idénticas tras la reparación descrita abajo.",'',
        '## Cambios y experimento descartado','',
        'La base pública elegida es Farmer John and the Idle Seller (`03165654`), Apache-2.0. Se añadieron una asignación de posiciones de venta mediante programación dinámica sobre subconjuntos y la integración de venta de existencias al inicio de la demanda (idea E081 de mooman0222). Se conservan comandos físicos, cantidades en la capa de ordenación y barreras para compras del mismo producto.','',
        'Se probaron seis variantes en 108 partidas de exploración, después de 72 partidas de selección de bases públicas. La combinación elegida ganó 15/16. La variante de tres pasadas sobre F15 y la liquidación sin el optimizador no fueron elegidas.','',
        'La primera versión congelada `f16_selected` fue rechazada: una función pública heredada indexaba órdenes vacías y ocultaba un `IndexError`. Se conservaron su plan, partidas parciales y diagnóstico en `results/frontier16/`. La versión corregida conserva explícitamente la misma decisión ante esos huecos, sin borrar posiciones; los errores inesperados siguen siendo visibles. El nuevo holdout usa otras ocho semillas.','',
        '## Archivos y reproducción','',
        f"- Fuente: `candidates/f16_repaired.py`, SHA-256 `{package['source_sha256']}`.",
        '- Notebook autónomo: `kaggle_frontier16/experiment.ipynb`; se comprobaron los bytes de cada archivo que contiene.',
        '- Paquete local: `results/frontier16/repaired/local/submission.tar.gz`, con `main.py`, `LICENSE.txt` y `NOTICE.txt`.',
        '- Evidencia: `plan.json`, `holdout.json`, `holdout_summary.json`, `unit_tests.json` y `local_package.json` en `results/frontier16/repaired/`.',
        '- Reconstrucción: `python build_f16.py`; pruebas: `python -m unittest test_frontier16 -v`; aceptación: `python assess_f16.py`; notebook: `python make_frontier16_notebook.py`; paquete: `python pack_frontier16_local.py`.',
        '- Investigación y fuentes: [FRONTIER16_RESEARCH.es.md](FRONTIER16_RESEARCH.es.md).','',
        (f"Kaggle: **{cloud['total_games']} partidas oficiales completas**, delta emparejado **{cloud['total_score_delta']:+g}** frente a F15, máximo **{cloud['max_call_ms']:.1f} ms** y ningún error registrado. Se verificaron fuente, resultados, licencias y hash del archivo descargado. Notebook privado: https://www.kaggle.com/code/jarturo/kaggriculture-frontier16-queue . La autorización explícita de Arturo («Dale submissions y súbelo como privado») resolvió el bloqueo anterior de subida." if cloud else
         'El control automático de aprobación bloqueó el push a Kaggle y exige autorización explícita para este notebook y `jarturo/kaggriculture-frontier16-queue`. No se sorteó ese bloqueo. El notebook privado está preparado para 32 partidas oficiales adicionales con semillas `16401..16404`; esas partidas todavía no se han ejecutado. Solo exporta un archivo en Kaggle si pasan sus comprobaciones.'),'',
        '## Qué implica para 2660–2700','',
        'Es una mejora medida sobre F15 y sobre la base pública, dentro de este panel. No hay una conversión validada de estos resultados al rating objetivo. Los agentes privados de los primeros puestos tienen diferencias económicas que el panel público no reproduce. '+
        ('La nueva submission conserva F15 y reemplaza F14B al activarse; su último estado está en el recibo.' if submission else 'Las dos submissions activas siguen siendo F14B y F15; no se sustituyeron.'),'']
    Path('FRONTIER16_RESULTS.es.md').write_text('\n'.join(lines),encoding='utf-8')
    print('FRONTIER16_RESULTS.es.md written from complete evidence')


if __name__=='__main__':main()
