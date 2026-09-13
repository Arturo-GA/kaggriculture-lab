Frontier: resultados medidos — 13 de septiembre de 2026

El agente incorpora el planificador terminal propio descrito en
[GOLD_RESEARCH.es.md](GOLD_RESEARCH.es.md). Es un candidato experimental que supera
a nuestra segunda versión en el panel reservado y la confirmación oficial. No hemos
demostrado nivel gold ni superioridad sobre los agentes privados del top.

| Prueba | Frontier: victorias / empates / derrotas | ml_critic, control emparejado |
| --- | --- | --- |
| Panel reservado, 80 partidas por candidato, ocho semillas y cinco rivales | 76 / 0 / 4 | 64 / 12 / 4 |
| Motor oficial, 40 partidas por candidato, otras cuatro semillas y cinco rivales | 38 / 0 / 2 | 32 / 8 / 0 |

En el panel reservado mejora 6 puntos de
resultado, donde ganar vale 1 y empatar 0,5. En la confirmación oficial mejora
2. Ninguna familia del panel pierde
puntos agregados de resultado. La ganancia de victorias se concentra en los duelos
contra nuestra propia versión anterior; frente a router, prvsiyan, kaito y nagata
se conservan los resultados agregados. No es evidencia de victorias adicionales
frente a rivales gold. Varias familias comparten código público y ocho semillas
son una muestra pequeña: las 80 partidas no son 80 observaciones independientes.

La mejora media reservada es 0.075 por partida.
El intervalo bootstrap por grupos de semilla es
[0.037500000000000006, 0.1]; describe este panel,
no el rating esperado en Kaggle.

La ablación `auction_joint_risk`, que usa siempre el planificador, obtuvo
76 / 0 / 4 en el mismo panel. Frontier se abstuvo en
7 de 80 casos. Todavía no hay evidencia de
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

El simulador acelerado registró un máximo de 1088.6 ms,
por encima del límite objetivo de 1.000 ms. Esa medición incluía generar la observación
y se ejecutó con otros procesos activos. No se oculta el fallo: se repitieron sus
tres contextos más lentos, en serie y con motor oficial, con máximo de
64.3 ms. El máximo del panel oficial fue
234.8 ms. La exportación en Kaggle exige de nuevo
menos de 1.000 ms y ausencia de errores reportados. Un contador `auction_errors`
en cero por sí solo no demuestra que todas las órdenes hayan tenido efecto.

Las pruebas de código verifican la carga del entrypoint oficial, los límites de
información, la equivalencia con el controlador nativo, el prefijo causal compartido,
los pesos exportados y una ruta con fertilizante, cosecha y entrega ejecutada por
el motor oficial. Los resultados de las partidas exigen 719 llamadas y estado DONE.

En 12 pruebas reservadas contra secuencias públicas de equipos en posiciones
3, 8, 21 y 27, ambos candidatos ganaron 10.
Frontier mejoró el margen en 8, lo empeoró en
3 y empató en 1.
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

Kaggle completó y verificó el notebook. El archivo descargado contiene exactamente la política local congelada. Ganó 8/8 frente a matched6 y 4/8 frente a ml_critic (con cuatro derrotas). El control ml_critic obtuvo 8/8 frente a matched6 y ocho empates consigo mismo. El resultado agregado de la nube es igual al del control para ambos rivales: este pequeño panel no replica la ganancia local. Máximo por llamada: 299.6 ms. No demuestra superioridad general.

Archivo verificado: [submission.tar.gz](results/gold/kaggle/submission.tar.gz). Notebook [COMPLETE, versión 1](https://www.kaggle.com/code/jarturo/kaggriculture-frontier-joint-planner). No se envió una submission al leaderboard.
