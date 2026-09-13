"""Generate the measured release report without changing the frozen agent."""
import json
from pathlib import Path


def main():
    root=Path('results/gold')
    hold=json.loads((root/'frontier_holdout_summary.json').read_text())['candidates']
    official=json.loads((root/'frontier_official_summary.json').read_text())['candidates']
    latency=json.loads((root/'frontier_latency.json').read_text())
    gold=json.loads((root/'frontier_gold_holdout.json').read_text())['rows']
    controls={r['episode']:r for r in gold if r['candidate']=='ml_critic'}
    new=[r for r in gold if r['candidate']=='frontier']
    for r in new:assert r['prefix_sha256']==controls[r['episode']]['prefix_sha256']
    deltas=[r['margin']-controls[r['episode']]['margin'] for r in new]
    def record(r):
        t=r['total'];return f"{t['wins']} / {t['ties']} / {t['losses']}"
    text=f'''Frontier: resultados medidos — 13 de septiembre de 2026

El agente incorpora el planificador terminal propio descrito en
[GOLD_RESEARCH.es.md](GOLD_RESEARCH.es.md). Es un candidato experimental que supera
a nuestra segunda versión en el panel reservado y la confirmación oficial. No hemos
demostrado nivel gold ni superioridad sobre los agentes privados del top.

| Prueba | Frontier: victorias / empates / derrotas | ml_critic, control emparejado |
| --- | --- | --- |
| Panel reservado, 80 partidas por candidato, ocho semillas y cinco rivales | {record(hold['frontier'])} | {record(hold['ml_critic'])} |
| Motor oficial, 40 partidas por candidato, otras cuatro semillas y cinco rivales | {record(official['frontier'])} | {record(official['ml_critic'])} |

En el panel reservado mejora {hold['frontier']['total']['score_delta']:.0f} puntos de
resultado, donde ganar vale 1 y empatar 0,5. En la confirmación oficial mejora
{official['frontier']['total']['score_delta']:.0f}. Ninguna familia del panel pierde
puntos agregados de resultado. La ganancia de victorias se concentra en los duelos
contra nuestra propia versión anterior; frente a router, prvsiyan, kaito y nagata
se conservan los resultados agregados. No es evidencia de victorias adicionales
frente a rivales gold. Varias familias comparten código público y ocho semillas
son una muestra pequeña: las 80 partidas no son 80 observaciones independientes.

La mejora media reservada es {hold['frontier']['paired_score_delta_mean']:.3f} por partida.
El intervalo bootstrap por grupos de semilla es
{hold['frontier']['seed_bootstrap_95_percentile_interval']}; describe este panel,
no el rating esperado en Kaggle.

La ablación `auction_joint_risk`, que usa siempre el planificador, obtuvo
{record(hold['auction_joint_risk'])} en el mismo panel. Frontier se abstuvo en
{hold['frontier']['choices'].get('0',0)} de 80 casos. Todavía no hay evidencia de
que el selector aprendido añada victorias sobre el planificador constante; no
atribuimos la mejora a sus árboles. Se conserva como experimento de selección,
con el control constante y todas sus mediciones disponibles.

El aprendizaje utilizó 288 partidas y la selección otras 96, con semillas separadas.
Se verificaron 12.288 predicciones exportadas contra scikit-learn. La representación
y el runtime del selector no dependen de scikit-learn. La política final y los pesos
están congelados y sus hashes constan en `frontier_training.json` y
`frontier_model_build.json`.

Se corrigió únicamente el registro de diagnósticos después de la primera ejecución
reservada. Se repitieron los 80 casos del candidato y todos conservaron exactamente
recompensas y decisiones. Los 160 controles de código intacto se reutilizan con sus
hashes originales. Los archivos iniciales se mantienen; `verify_frontier_holdout.py`
comprueba la equivalencia y crea el resumen combinado.

El simulador acelerado registró un máximo de {latency['original_max_ms']:.1f} ms,
por encima del límite objetivo de 1.000 ms. Esa medición incluía generar la observación
y se ejecutó con otros procesos activos. No se oculta el fallo: se repitieron sus
tres contextos más lentos, en serie y con motor oficial, con máximo de
{max(r['max_call_ms'] for r in latency['rows']):.1f} ms. El máximo del panel oficial fue
{official['frontier']['max_call_ms']:.1f} ms. La exportación en Kaggle exige de nuevo
menos de 1.000 ms y ausencia de errores reportados. Un contador `auction_errors`
en cero por sí solo no demuestra que todas las órdenes hayan tenido efecto.

Las pruebas de código verifican la carga del entrypoint oficial, los límites de
información, la equivalencia con el controlador nativo, el prefijo causal compartido,
los pesos exportados y una ruta con fertilizante, cosecha y entrega ejecutada por
el motor oficial. Los resultados de las partidas exigen 719 llamadas y estado DONE.

En 12 pruebas reservadas contra secuencias públicas de equipos en posiciones
3, 8, 21 y 27, ambos candidatos ganaron {sum(r['win'] for r in new)}.
Frontier mejoró el margen en {sum(d>0 for d in deltas)}, lo empeoró en
{sum(d<0 for d in deltas)} y empató en {sum(d==0 for d in deltas)}.
Las secuencias grabadas no reaccionan al nuevo estado. No contamos esos resultados
como victorias frente a los agentes privados, ni los usamos para entrenar el selector.
Dos de los 22 replays iniciales mostraron discrepancias pequeñas del C++ y fueron
confirmados exactamente con el motor oficial. Todos los duelos de estrés publicados
se ejecutaron con el motor oficial.

Los experimentos anteriores, incluidos los que perdieron y los cambios de cultivo
que no llegaron a activarse, permanecen en `results/gold`. El nuevo controlador no
usa esas mutaciones de cultivo. La producción anterior al turno 696 conserva la
base pública atribuida; la implementación propia afecta al cierre.

El notebook privado independiente está preparado en `kaggle_frontier`. Su verificación
en la nube compara Frontier y ml_critic frente a ml_critic y matched6 en otras
32 partidas. Sólo exporta si no hay regresión agregada por rival, errores reportados
ni llamadas de 1.000 ms o más. No envía automáticamente una submission al leaderboard.
El repositorio y el notebook privados reducen la copia directa; no prueban una
ventaja imposible de reproducir ni garantizan una medalla.
'''
    cloud=root/'frontier_kaggle_verified.json'
    if cloud.exists():
        c=json.loads(cloud.read_text());assert c['verified']
        text+='\nKaggle completó y verificó el notebook. El archivo descargado contiene exactamente '
        text+='la política local congelada. Resultado de la nube: '+json.dumps(c['per_opponent'])+'. '
        text+=f"Máximo por llamada: {c['max_call_ms']:.1f} ms.\n"
    Path('FRONTIER_RESULTS.es.md').write_text(text,encoding='utf-8')
    print('FRONTIER_RESULTS.es.md written')


if __name__=='__main__':main()
