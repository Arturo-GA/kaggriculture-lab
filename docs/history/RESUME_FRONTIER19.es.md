# Retomar Frontier19 — 30 de septiembre de 2026

Leer [el informe](FRONTIER19_RESULTS.es.md). Arturo autorizó explícitamente:
«haz el mismo analisis para tener una estrategia que apunte al top 200-300 de la
copetencia manda 2 plazas». Esta autorización nueva es para dos envíos, con
notebook y GitHub privados, y reemplaza el alcance condicional de la ronda F18.

## Estado verificable

La fuente de verdad es `results/frontier19/`: `selection_decision.json`, `release_selection.json`,
`release.json`, `kaggle_private_verified.json`, `kaggle_verified.json` y los dos
`*_submission_receipt.json`. Un archivo ausente significa que esa fase no está
confirmada. El notebook no realiza submissions automáticamente. Cada envío
guarda intención antes del POST y recibo con ID inmediatamente después. Si queda
una intención sin recibo, reconciliar primero con Kaggle; nunca duplicar.

Al inicio, F18 `56617687` y F17 `56615489` eran los agentes activos, con ratings
1963 y 2018; el equipo estaba 657. Los cortes 200–300 eran 2396,5–2275,9. Son
valores de las 15:35 UTC, no el estado después de los envíos ni una predicción.

## Evidencia y selección

- Cuatro partidas públicas por cada equipo del puesto 200–300: 404 apariciones,
  360 episodios distintos. Con referencias superiores y pérdidas propias hay
  400 episodios descargados. Veinte contabilidades propias reproducidas exactas.
- Apertura SW mediana en 218 frente a 266 de F18. Adelantarla requiere cambiar
  financiación y rutas: nuestra caja no alcanza en 218. Copiar rutas completas,
  sustituir animales y añadir gansos no produjo una mejora validada.
- Modelos de ventas recientes: sin mejora de acciones/resultados en las pruebas.
- La corrección de `PICKUP WHEAT 0` pasa una regresión de una pérdida real, pero
  eso no la convierte por sí sola en evidencia de mayor rating.
- Cuatro finalistas congeladas antes de la prueba: `f19_market2`, `f19_robust`,
  `f19_balanced`, `f19_pressure`. No modificar sus archivos ni retocar parámetros
  con las semillas del holdout.
- `plan.json`: 400 juegos, cinco políticas incluido F18, cinco rivales reactivos,
  ocho semillas 19101–19108 y ambos asientos. `select_f19.py` aplica la puerta y
  el desempate fijados; una vez creada, la decisión no se sobrescribe.
- La primera puerta la supera solo `f19_market2`. `f19_robust` termina 76/80
  pero retrocede tres puntos contra Lynn, frente al máximo permitido. Ese fallo
  permanece. `supplement/plan.json` registra otras ocho semillas nuevas, tres
  rivales y 144 juegos para elegir la segunda plaza entre Market1 y Market8,
  con los mismos umbrales. `selection_decision.json` indica el plan de origen
  del candidato que pasa. Market1 terminó 44/48 contra 38/48 del control y
  16/16 contra F18, pero retrocede dos puntos contra Lynn y falla el límite de −1
  fuera del duelo directo. `release_selection.json` lo admite explícitamente
  como segunda plaza experimental bajo la autorización actual de Arturo para
  dos envíos. No se modificaron umbrales ni resultados. `release_f19.py`
  distingue el candidato que pasa de esta admisión experimental documentada.
- Los benchmarks públicos tienen familias correlacionadas. F18 ganó 38/40 en
  exploración y aun así estaba en 1963 en Kaggle. No convertir victorias locales
  ni rivales grabados en un pronóstico de top 200.

## Herramientas

Usar Python de `.venv/Scripts/python.exe`. El motor es `kaggle-environments==1.32.7`.
El repositorio es `Arturo-GA/kaggriculture-lab`, privado. El notebook de esta ronda
es `jarturo/kaggriculture-frontier19-policy-validation`, privado.

`release_f19.py prepare --candidates NOMBRE1 NOMBRE2` congela exactamente dos
fuentes elegidas y las pruebas previas, incluida la regresión de Market1. La nube juega semillas 19201–19204 para
comprobar ejecución, latencia y empaquetado; sus resultados no tienen un umbral
competitivo adicional. `verify` comprueba hashes y contenidos byte por byte.
`submit --candidate NOMBRE --authorization "..."` envía una vez; con un recibo
existente, una llamada posterior solamente reconcilia ese envío.

`snapshot_f19_sources.py --restore NOMBRE` recupera fuentes experimentales
idénticas desde el archivo comprimido, incluidas las rechazadas. Se niega a
sobrescribir una fuente distinta. Avisos y licencia del rival público de Lynn
están conservados; no se redistribuye código privado de competidores.

El límite oficial de envío es **30/09 a las 23:59 UTC, 18:59 Lima**. La ejecución
de partidas continúa después. No asumir que queda abierta la recepción de
submissions en una sesión futura.

## Resultado verificado y envíos

- f19_market2: **56714342**, `SubmissionStatus.COMPLETE`, 2026-09-30T17:25:14.769991+00:00.

- f19_market1: **56714336**, `SubmissionStatus.COMPLETE`, 2026-09-30T17:25:14.772267+00:00.

Dos envíos efectuados; consultar los recibos antes de cualquier acción. No queda una plaza pendiente de esta autorización.
