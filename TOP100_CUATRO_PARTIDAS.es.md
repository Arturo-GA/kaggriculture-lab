# Cuatro partidas por equipo del top 100 — 27 de septiembre de 2026

Corte de leaderboard: 2026-09-27T19:00:03.397799+00:00; puesto 100: **2613.9**. La muestra contiene **400 actuaciones, 336 partidas distintas y 336 semillas**. Se eligió el mejor agente activo de cada uno de los 100 equipos y sus cuatro partidas públicas completas más recientes, sin filtrar victorias. Cada equipo conserva su hora de consulta; no se pretende una fotografía simultánea de todas las APIs.

El análisis anterior de dos partidas permanece intacto. Las columnas siguientes comparan las dos más recientes y las dos anteriores de esta misma selección: mantienen equipo y submission, pero cambian rivales y mundos.

| Medida | Cuatro (400) | Dos recientes (200) | Dos anteriores (200) | F17 (16) |
|---|---:|---:|---:|---:|
| Mediana del máximo diario de trabajadores, días 10–26 | 11.0 | 11.0 | 11.0 | 11.0 |
| Mediana de animales al paso 288 | 19.0 | 19.0 | 19.0 | 17.0 |
| Mediana de fresas al paso 288 | 24.0 | 24.5 | 23.0 | 33.0 |
| Mediana del primer paso con SW abierto | 219.0 | 220.0 | 219.0 | 266.0 |
| Actuaciones con SE abierto alguna vez | 113 | 55 | 58 | 3 |
| Actuaciones con tomate plantado antes del paso 288 | 199 | 100 | 99 | 0 |
| Actuaciones con zanahoria antes del paso 288 | 151 | 74 | 77 | 3 |
| Actuaciones con ≥10 turnos de compra/venta del mismo insumo | 42 | 21 | 21 | 15 |

## Repetición dentro de cada equipo

Cada fila cuenta equipos según el número de sus cuatro partidas que muestran el patrón. Una conducta presente en 4/4 es más estable en esta muestra; no demuestra que sea óptima ni que todos los equipos sean independientes.

| Patrón | 0/4 | 1/4 | 2/4 | 3/4 | 4/4 |
|---|---:|---:|---:|---:|---:|
| Abrir cuarto cuadrante (SE) | 66 | 2 | 6 | 5 | 21 |
| Abrir tercero (SW) antes del día 10 | 6 | 2 | 3 | 7 | 82 |
| Tomate antes del paso 288 | 34 | 7 | 13 | 18 | 28 |
| Zanahoria antes del paso 288 | 32 | 21 | 25 | 8 | 14 |
| ≥10 turnos con compra/venta del mismo insumo | 85 | 4 | 2 | 2 | 7 |
| ≥20 animales al paso 288 | 18 | 27 | 19 | 24 | 12 |
| ≥12 trabajadores (mediana de picos diarios) | 45 | 14 | 13 | 11 | 17 |

La ampliación confirma las diferencias generales de la muestra anterior: 11 trabajadores, unos 19 animales y menos fresas que F17. La apertura temprana de SW se repite en las cuatro partidas de 82 equipos; 66 no abren SE en ninguna. La mediana de apertura de SW es el paso 219 frente al 266 de F17. Una hipótesis de producción para un siguiente experimento es adelantar ese tercer cuadrante con un presupuesto y una ruta de trabajo coordinados. Cambiar únicamente la fecha de compra no prueba esa hipótesis. El tomate temprano se mantiene en 4/4 en 28 equipos, pero otros 34 nunca lo usan temprano; su conveniencia debe condicionarse a la demanda y a la producción rival observable.

## El líder también pierde

Se reconstruyeron las cuatro partidas de DECEM en el motor oficial 1.32.7. Ambas cuentas cierran en las cuatro y pasan **320 comparaciones de campos de estado**.

| Episodio, de más reciente a anterior | Rival | Margen de DECEM | Venta de tomate | Venta de zanahoria |
|---|---|---:|---:|---:|
| 114304518 | M & M & P & Q | -8332 | 0 | 6400 |
| 114292697 | Boey | -1302 | 0 | 2290 |
| 114279609 | Boey | +5808 | 15990 | 898 |
| 114267880 | DSM | +812 | 0 | 1789 |

Las ventas son ingresos contables brutos, no rentabilidad incremental: faltan semillas, insumos y trabajo compartido. Estas cuatro partidas contienen victorias y derrotas; copiar únicamente el esquema de una victoria sería una selección sesgada.

## Fallo comprobado de F17

La partida **114306320** contra BlueSky_sora terminó 86421–87158 (−737). La reproducción del motor y la ejecución del código congelado de F17 con las acciones rivales registradas coinciden exactamente con ese resultado. En el día 25, el trabajador 12 necesitaba alimentar seis ovejas, llevaba una unidad de trigo y el almacén estaba vacío. La política repetía `PICKUP WHEAT 0`: exigía reunir comida para toda su ruta antes de continuar, y el rescate existente interpretaba esa recogida vacía como progreso. Seis ovejas quedaron sin alimento/cuidado.

La traza exacta atribuye 18 unidades de lana perdidas a esa producción y otras seis a la siguiente: **24 unidades menos** que el rival. F17 vendió lana por 1353 menos. Su balance ventas−compras−semillas de trigo fue 1326 peor, mientras las zanahorias compensaron 1438. Son componentes contables: no deben sumarse con estimaciones de precio fijo porque el mercado responde al volumen.

La corrección `frontier18_feed.py` permite evaluar el rescate cuando la recogida pide cero; conserva los comandos físicos y las restricciones heredadas de caja, capacidad, hora y último día. En el diagnóstico con rival registrado, `f18_small` pasó de −737 a −601 y `f18_feed` a +909; la victoria de control se conservó. El rival conserva el 98,47 % de su dinero original en la derrota corregida. Esto no es una partida contra un rival reactivo y no entra como victoria de validación competitiva. Los resultados de los paneles nuevos se registran por separado.

## Qué se prueba y qué se descarta

- Microoperaciones de mercado con volumen máximo 16: 94/96 victorias y +12 puntos frente al control; supera su puerta local.
- Escenario alternativo de compra rival temprana: +1 punto total y regresión frente a F16; no supera su puerta.
- Desbloqueo de alimentación: arregla el caso real, pero el panel nuevo iguala 48/48 al padre y nunca activa el rescate; no se selecciona para envío.
- Previsión finita de tomate: empató con F17 en la exploración; no se seleccionó como mejora.
- Rotaciones más agresivas de zanahoria: empeoraron la exploración; no se enviaron.

Cuatro partidas por equipo permiten comprobar repetición, pero no revelan código privado ni justifican prometer oro. Las cantidades de órdenes no equivalen a ganancias realizadas; las estrategias se validan jugando contra políticas que reaccionan.

Fuentes: [leaderboard y partidas públicas de Kaggle](https://www.kaggle.com/competitions/kaggriculture/leaderboard), `selection.json` con identidades y hashes de replays, `profiles.json`, `features.json.gz`, `leader_accounting.json`, `results/frontier18/live_accounting.json`, `animal_trace.json` y los paneles de validación.
