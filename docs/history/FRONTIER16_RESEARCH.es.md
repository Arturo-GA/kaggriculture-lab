# Frontier16: revisión de GitHub, Kaggle y la franja objetivo

Revisión del 27 de septiembre de 2026. Petición: mejorar la estrategia actual con
la evidencia pública más reciente y buscar 2660–2700, sin dar por supuesto que un
resultado local equivale a ese rating.

## Estado que se comprobó

Se hizo fetch del repositorio privado `Arturo-GA/kaggriculture-lab`: `main` y
`origin/main` estaban en `36ee7d1`. La estrategia vigente era Frontier15 E081,
no el antiguo JointPlanner. Se leyeron los resultados de F13–F15 y los
experimentos descartados para no repetirlos.

Consulta de Kaggle a las 12:32 UTC, guardada en
`results/frontier16/live_snapshot.json`: equipo 599.º con 2308,7; Frontier14B
2308,7 y Frontier15 2097,3. F15 llevaba 86 victorias y 18 derrotas, pero casi
todas frente a rivales de menos de 2300; eso no demuestra fuerza de 2660.
Frontier14B llevaba 0/14 contra 2500–2600. Los tramos usan el rating actual del
equipo rival, no un rating reconstruido del instante de la partida.

La [clasificación consultada](https://www.kaggle.com/competitions/kaggriculture/leaderboard)
mostraba DECEM 3056,5, Boey 3022,8, M & M & P & Q 2983,3, Majkel1337 2974,8 y
Vadim Vasilenko 2947,4. Los ratings cambian y no identifican una versión pública
exacta del código de esos equipos.

## Código público actualizado

Se consultaron 50 notebooks recientes y se descargaron 14. Se extrajeron sus
agentes como datos, sin ejecutar las celdas de los notebooks. Los archivos TAR
se leyeron en memoria, verificando sus hashes y conservando las licencias.
Los recibos están en `public_scan.json` y `archive_sources.json` dentro de
`results/frontier16/`.

| Fuente | Actualización UTC | Hallazgo |
|---|---|---|
| [Farmer John and the Idle Seller](https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-idle-seller) | 27/09 09:29 | Base `03165654`, cierre de reordenaciones con parada temprana y detección de ciclos. Elegida por resultados y menor coste de ejecución. |
| [Demand-Preserving Turn Sale Timing](https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing) | 27/09 02:50 | Base `55be5d5f`, repite 41 pasadas; mismo resultado en las 12 partidas de exploración que la base elegida. |
| [Master Engine V4](https://www.kaggle.com/code/guruprasaathas111/kaggriculture-top-2-master-engine-v4) | 27/09 03:45 | Mismos bytes `55be5d5f`; su título «TOP 2» no verifica un rating. |
| [Harvest Ledger](https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger) | 27/09 08:38 | Base `63dde9`, mismos resultados de exploración, mayor latencia máxima. |
| [Multi-route Farming Agent](https://www.kaggle.com/code/flexonafft/kaggriculture-multi-route-farming-agent) | consulta del 27/09 | No superó F15: 0/4 en exploración. |
| [Farmer John and the Wheat Seller](https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-wheat-seller) | 26/09 06:49 | Tampoco superó F15: 0/4 en exploración. |

Las tres mejores bases públicas dieron exactamente los mismos resultados en
este cribado; no deben contarse como tres familias independientes. La base
seleccionada ganó 4/4 a F15, con margen medio de 537,75 monedas, antes de añadir
nuestros cambios. El avance de la base pública explica una parte importante
de la mejora; no se atribuye todo a código propio.

## Discusiones y elección del experimento

- [Six things I wish I'd known before trusting my local win rates](https://www.kaggle.com/competitions/kaggriculture/discussion/743231): advierte sobre dependencia entre asientos, ciclos de victorias entre linajes y sesgo de los rivales grabados. Se usan ocho semillas nuevas, diez rivales, ambos asientos y controles emparejados. Siguen siendo ocho mundos independientes, no 160.
- [My RL Won, But Also Failed](https://www.kaggle.com/competitions/kaggriculture/discussion/743716): su autor relata un entrenamiento grande con PPO que ganaba a públicos pero encontraba un techo frente a rivales fuertes. Es una experiencia publicada por un participante, no una prueba de que RL no pueda mejorar el juego. No justifica sustituir un agente validado por un entrenamiento sin evaluar.
- [Discusión del torneo final](https://www.kaggle.com/competitions/kaggriculture/discussion/731587): el resultado final se calcula después del cierre. Un rating temprano no es un puntaje definitivo.

## Qué se sabe de los mejores equipos

Se volvió a revisar la evidencia económica conservada en
`ANALISIS_2700.es.md` y `outputs/session/gold/top10_econ_0925.json`: son replays
públicos del **25 de septiembre**, no código privado ni partidas nuevas del 27.
Muestran con frecuencia más animales, 12–13 manos y expansión temprana al
cuadrante sudeste, con excepciones como Boey. La mezcla de producción cambia
con las tiendas. Ganar a clones del agente público no demuestra poder vencer
esas economías.

La mejora inmediata implementada en F16 actúa sobre la ejecución del mercado.
No se afirma haber reconstruido los planificadores de los líderes. Las pruebas
previas de expansión, trasplante de rutas y liquidación adicional de huevos o
melón se conservaron como resultados negativos; no se volvió a promocionarlas.

## Aporte propio y límites

Se implementó una programación dinámica sobre subconjuntos de ventas para
elegir posiciones en la lista del mercado. Conserva cantidades, comandos
físicos y el orden relativo de las compras; las compras fijas solo pueden
atrasarse. Excluye ventas duplicadas, sin stock o cuyo producto se compra en
el mismo turno. Evalúa precios frente a una copia de nuestras órdenes: esa
suposición es aproximada y no revela el inventario privado del rival.

La variante elegida combina esa capa con la venta de existencias al abrir la
ventana de demanda, idea pública E081 que ya usaba F15. La validación incluye
la base pública sin modificar para separar su avance del aporte de nuestras
capas. La procedencia y los avisos se conservan en `NOTICE.md` y
`attribution/frontier16/`.

El objetivo 2660–2700 queda como objetivo de competición. El panel local no
está calibrado para convertir victorias en ese rating, y las estrategias de
los rivales cambian con nuevas versiones.
