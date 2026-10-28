# Frontier4: diagnóstico de las submissions y nuevo candidato — 16 de septiembre de 2026

## Qué pasó con las tres familias enviadas

Consulta autenticada a Kaggle el 16 de septiembre (00:24 UTC). Leaderboard: 9178 equipos; cortes
de medalla oro 2916,8 (28 equipos), plata 2637,3 (459), bronce 2433,2 (918). Nuestra fila:
puesto 710, 2552,2. Solo las dos últimas submissions cuentan para la evaluación final y ambas son
Frontier3 (`56222986` y `56223026`); matched6 (2650) ya no participa.

| Familia | Submission | Partidas públicas | V/D | Rating observado |
|---|---:|---:|---:|---:|
| matched6 (V37 + horizonte 6) | 56190498 | 207 | 137/70 | 2650,6 |
| ML critic | 56213093 | 85 | 68/17 | 2507,5 |
| Frontier (planificador terminal) | 56214804 | 100 | 78/22 | 2589,0 |
| Frontier2 (entregas en ruta) | 56216380 | 87 | 61/26 | 2603,5 |
| Frontier3 (apertura V41 + capacidad) | 56222986 / 56223026 | 281 / 279 | 140/141 / 142/136 | 2527,9 / 2547,6 |

Las dos Frontier3 empezaron ganando 42/50 y terminan perdiendo: 10/31 y 12/29 en sus últimas
partidas. Contra rivales de 2500-2600 pierden (22/35 y 30/39). Los 30 replays auditados
(`outputs/session/audit_f3.json`, fuera de Git) reproducen exactamente las 719 acciones de
`frontier3_capacity`: el bot desplegado es el congelado, sin errores ni timeouts. En los 30
replays la granja rival es idéntica a la nuestra en el día 12 (33 fresas, 20 trigos, 3 gansos,
8 vacas, 6 ovejas): el pool de 2500-2900 está formado por clones del mismo linaje público.
Apertura del rival: 18 de 30 usan 5/10/60 (V41-V44), 2 usan 13/30/30 (V35-V40), 2 usan la
apertura C9 (pipe-4/5), el resto variantes. En las derrotas, ya vamos 400-1000 monedas por
detrás en el turno 288 y 1500-5000 al final.

## La causa: la carrera de ventas del mismo turno

Los notebooks públicos V44 ("Winning the Same-Turn Sale Race", 15 de septiembre) y V45
("First-Turn Wheat Round Trip", 15 de septiembre) de Ahmed Berat Özer adelantan las ventas 8
turnos cuando detectan un clon por posiciones idénticas de los trabajadores, y 24 turnos tras
perder una carrera. Nuestra base (V37 con matched6) anticipa 2-6 turnos. En un espejo, el primero
en cotizar cobra el precio previo al desplome: las fresas caen 1,92 por unidad vendida y los
melones se hunden de 271 a 78 en el día 11.

Simulación local (C++ verificado, 12 partidas por par, semillas 5601-5606):

| Nuestro bot | vs V43 | vs V44 | vs V45 | vs V41 |
|---|---:|---:|---:|---:|
| frontier3_capacity | 0/12 (−2156) | 0/12 (−2037) | 0/12 (−4497) | 6/6 (+1162) |

Rastreo de un espejo Frontier3-V45: la brecha se abre de golpe entre los turnos 240 y 264
(−1857), justo en la primera venta de melones. Orden de fuerza entre agentes públicos:
V45 > V44 > pipe-4/pipe-5 (V43 + apertura C9 + cierre) > V43 > V41 > nuestras versiones.

## Qué se probó

Todo sobre el V45 público extraído como datos (`extract_public_agents.py`, hash fijado en
`build_f4.py`); V45 sin modificar es el control emparejado en cada prueba.

| Variante | Cambio | Resultado principal |
|---|---|---|
| f4_r24 | horizonte de carrera fijo 24 | 43/52 vs V45 en cuatro pantallas; motor oficial 8/0 vs V45 y 8/0 vs V44; pero 23/9 vs pipe-4/5 donde V45 hace 31/1 |
| f4_adapt | escala a 24 al detectar venta rival en el turno del depósito | 27/5 vs V45, 31/1 vs V43/V44, 23-25/32 vs pipe |
| f4_term | V45 + planificador terminal, entregas y capacidad de Frontier | 23/9 vs V45 (+338); 27/5 vs pipe, V44 |
| f4_full / f4_adapt_full | horizonte + capas terminales | 23/9 vs V45; 25/7 vs las demás familias; oficial 5801-5804: 8/0 contra seis rivales |
| f4_r24b / f4_fullb | reserva sin tope de bloque | peor: 14/2 vs V45 y 6/10 vs pipe-5 |
| f4_run (manos "corredoras") | contratar 1-2 manos que cosechan y venden antes del amanecer | negativo (−900 a −6700): las 9-13 manos de la cinta llegan antes a las baldosas maduras y la contratación Fibonacci cuesta 144-377/día |
| f4_full_ds | capas dead_stock/clamp_sells de tetsutani activas | 14/2 vs pipe-5 pero 8/8 vs V45 |

Cuadro combinado, 32 partidas por par (semillas 5741-5758, ambos asientos):

| Candidato | pipe-4 | pipe-5 | V43 | V44 | V45 | Puntos/160 |
|---|---:|---:|---:|---:|---:|---:|
| V45 (control) | 31/1 | 29/3 | 31/1 | 31/1 | 16 (empates) | 138 |
| f4_adapt | 25/7 | 23/9 | 31/1 | 31/1 | 27/5 | 137 |
| f4_r24 | 23/9 | 23/9 | 31/1 | 31/1 | 27/5 | 135 |
| f4_term | 27/5 | 27/5 | 29/3 | 27/5 | 23/9 | 133 |
| f4_adapt_full | 25/7 | 25/7 | 27/5 | 27/5 | 23/9 | 127 |
| f4_full | 25/7 | 25/7 | 27/5 | 25/7 | 23/9 | 125 |

Lectura: adelantar las ventas gana el espejo contra V45 pero pierde contra clones que cotizan a
4 turnos (V43, pipe), porque vender 24 turnos antes renuncia a la recuperación de precio que
las tiendas producen. El planificador terminal propio no mejora sobre el cierre de V45 en la
muestra grande. Las diferencias entre V45, f4_adapt y f4_r24 están dentro del ruido de 16
mundos salvo dos efectos con mecanismo claro: +11/32 en el espejo V45 y −8/32 contra pipe.

## Candidato final: f4_probe (sonda de carrera)

La lección de las variantes fijas es que el horizonte correcto depende del rival: 24 gana el
espejo contra V44/V45 (que escalan a 24 tras perder una carrera) y pierde contra clones que
cotizan a 4 turnos (V43, pipe). `f4_probe` conserva V45 íntegro y añade una sonda a su capa de
carrera: el horizonte empieza en 24 turnos hasta el turno 336 (día 14); cada turno reconstruye
las ventas netas del rival en nuestros turnos de depósito (descontando nuestras ventas
efectivas a partir del almacén y de los DROP/PLACE propios) y, si el rival vende un producto que
nuestra propia cinta solo vende más de cuatro turnos después, confirma un rival de horizonte
largo y mantiene 24; sin evidencia al llegar al día 14 vuelve a los 8 turnos de V45, con su
escalada original por carrera perdida intacta. En las pantallas, la confirmación ocurre en
32/32 partidas contra V44 y V45 y en 0/32 contra V43 antes del día 14.

Selección (semillas 5741-5758, 32 partidas por par): 31/1 pipe-4, 29/3 pipe-5, 31/1 V43,
31/1 V44 (+1548 de margen frente a +1316 de V45) y **27/5 contra V45** (+152). 149 puntos de
160 frente a 138 del control V45. Latencia máxima medida en C++ bajo concurrencia: 912 ms en
una partida de f4_r24; f4_probe no superó 635 ms.

Holdout (semillas nuevas 5721-5728, 13 rivales, 416 partidas con control V45 emparejado):
16/0 contra aurax_v5, frontier3_capacity, kaito, lynn_v5, matched6, nagata, pipe-4, prvsiyan,
router, V43 y V44; 14/2 contra pipe-5; 11/5 contra V45. Diferencia de puntos emparejada +3,
ninguna regresión por rival, sin errores ni fallbacks. `results/frontier4/holdout_summary.json`.

Confirmación oficial (`kaggle-environments` 1.32.7, semillas nuevas 5811-5814, 96 partidas):
8/0 contra frontier3_capacity, kaito, pipe-5 (+2911), prvsiyan y V44 (+1332); 6/2 contra V45
(+26). Diferencia emparejada +4, latencia máxima 157 ms, cero errores.
`results/frontier4/official_summary.json`. Las seis pruebas de `test_frontier4.py` pasan.

Hash congelado de `candidates/f4_probe.py`:
`f426240eb717948205e8f19e51bc6fc3084d441a721b4f6e4557828ca7c8e860`
(`results/frontier4/selection.json`, `results/frontier4/build.json`).

Qué esperar: la mejora principal es pasar de una base V37 que perdía 0/12 contra el meta a una
base V45 que le gana o empata, más un pequeño margen sistemático en el espejo V45. Esto debería
llevar el rating al nivel del clúster público (aproximadamente 2800-2900 en la tabla del 16 de
septiembre), no al podio: los ocho primeros son estrategias únicas. El siguiente salto exige
una economía distinta (más vacas con CARE, otra mezcla de cultivos por tiendas), no otra capa
sobre la cinta.

Verificación en Kaggle (kernel privado `jarturo/kaggriculture-frontier4-sales-race`, versión 2,
motor oficial 1.32.7, semillas 5901-5902, ambos asientos, control V45 emparejado): f4_probe
3/1 contra V45 (+180), 4/0 contra pipe-5 (+962) y 4/0 contra Frontier3 (+6869); diferencia
emparejada +1, latencia máxima 526 ms en la CPU de Kaggle, cero errores. El `main.py` y el
`submission.tar.gz` descargados coinciden byte a byte con el candidato congelado; SHA-256 del
archivo `172daa824d75fe64af6970ca9311326aff249435d9f86df40da2df810549ae71`
(`results/frontier4/kaggle_verified.json`).

Envío al leaderboard autorizado por Arturo el 16 de septiembre: **submission 56266564**
("Frontier4 sales race f426240e on V45"), recibo en `results/frontier4/submission_receipt.json`.
A petición de Arturo se envió el mismo archivo una segunda vez (**submission 56266648**,
recibo en `results/frontier4/submission_receipt_2.json`) para que las dos plazas activas, que son
las que cuentan en la evaluación final, sean Frontier4; ambas Frontier3 dejan de estar en
seguimiento. El rating inicial de las primeras horas no es el resultado final.
Seguimiento: `python live_report.py 56266564 56266648`.

## Límites

Los paneles locales están dominados por linajes públicos de cinta; los ocho primeros del
leaderboard son estrategias únicas que no tenemos. Los dos asientos de una semilla comparten
mundo y no son observaciones independientes. El simulador C++ es exploratorio; la aceptación
usa el motor oficial. No se garantiza rating ni medalla.
