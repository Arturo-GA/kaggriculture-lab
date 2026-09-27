# Retomar Frontier18 — 27 de septiembre de 2026

Leer primero [resultados](FRONTIER18_RESULTS.es.md) y
[cuatro partidas por equipo](TOP100_CUATRO_PARTIDAS.es.md).

Arturo autorizó dos submissions **si mejoran** y pidió ampliar el análisis de dos a cuatro
partidas públicas por agente del top 100. Se completó el censo (400 actuaciones, 336 juegos)
y se hicieron **una subida privada y una submission**, F18 pequeño `56617687`.
La segunda plaza no se usó: el escenario rival alternativo falla su puerta y el arreglo de
alimentación no muestra mejora en el panel adicional, donde el fallo nunca aparece.
No convertir la autorización condicional en permiso para gastar la segunda plaza sin evidencia.

## Fuente y recibos

- Candidato congelado: `candidates/f18_small.py`.
- SHA: `d9289a3e55624596ab5c2a8368359542e09249ae7fd64391d506bf82daeec135`.
- Paquete: `results/frontier18/kaggle/f18_small.tar.gz`.
- SHA del paquete: `28d30e598de4ac49ac6330484a29a2ebcb6d01a9ec17b5fc18a2679f2756d491`.
- Notebook privado, versión 1: `jarturo/kaggriculture-frontier18-policy-validation`.
- `results/frontier18/kaggle_verified.json`: 16 juegos oficiales, 8/8 frente a F17, cero
  errores, máximo 150,7 ms, bytes y licencias idénticos al paquete local.
- `f18_small_submission_intent.json` y `f18_small_submission_receipt.json` evitan duplicados.
  Consultar el recibo y `active_after_submission.json` antes de cualquier envío nuevo.
- `release_f18.py submit --candidate f18_small` **sin autorización** solo reconcilia un
  envío existente; no repetir la subida con otro nombre o descripción.

## Qué se aprendió

F18 limita el tamaño especulativo a 16 y permite cantidades pequeñas. No cambia las rutas
físicas. En el panel congelado de ocho semillas y seis rivales ganó 94/96, +12 puntos sobre F17,
16/16 directamente; cuatro puntos de mejora vienen del rival sintético de mercado.
No extrapolar esos números a rating ni a políticas privadas que no están en el panel.

F17 no estaba estancado bajo 2000: al 27/09 19:17 UTC tenía 2315,4 y 21V/1D públicas.
El censo de cuatro partidas encontró SW temprano en 4/4 de 82 equipos; 66/100 nunca abren SE.
La mediana de SW es el paso 219 frente al 266 de F17. No afirmar que oro exige cuatro
cuadrantes, 12–13 trabajadores o PPO. El líder perdió sus dos partidas más recientes.

El episodio 114306320 identificó un bloqueo real: el trabajador 12 recoge cero trigo,
el rescate lo interpreta como progreso y seis ovejas quedan sin comida el día 25. La traza
exacta demuestra 24 unidades de lana perdidas. `frontier18_feed.py` corrige el bloqueo y
el replay cambia −737 a +909, pero el rival registrado no reacciona. La fuente **no** se
incluyó en F18 pequeño. Su panel de cuatro semillas nuevas empata 48/48 con el padre y
no ejecuta la rama de rescate ni una vez: hace falta otra validación con cobertura del
problema, declarada antes de ver sus resultados. Conservar el resultado negativo original.

Las rotaciones de zanahoria empeoraron la exploración y el calendario finito de tomate
igualó el control; no venderlas como mejoras demostradas. La apertura más temprana de SW
es una hipótesis pendiente que requiere planificar caja, siembra y trabajadores juntos.

## Evidencia y reproducción

`research_four.py` congela el leaderboard y selecciona cuatro episodios por mejor agente activo.
Usa el caché ignorado `vendor/top100_0927/`, limita llamadas y respeta HTTP 429.
`analyze_four.py`, `audit_four_leader.py` y `report_four.py` producen el informe; cuatro
partidas del líder cuadran exactamente y pasan 320 comparaciones de campos de estado.
Las muestras anteriores de dos partidas se conservan intactas.

`validate_f18.py` y `validate_f18_feed.py` se niegan a sobrescribir un plan existente.
Los paneles están completos; no volver a ejecutarlos para buscar una muestra favorable.
`assess_f18.py` aplica las puertas registradas. No modificar candidatos congelados tras ver
los resultados. `build_f18_market.py` y `build_f18_feed.py` regeneran variantes ignoradas
manteniendo prefijos y hashes. Las licencias heredadas se preservan en todos los paquetes.
