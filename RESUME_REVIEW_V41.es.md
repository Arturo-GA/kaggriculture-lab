# Estado después de revisar V41 — 14 de septiembre de 2026

Revisión terminada. No quedan experimentos en ejecución. No se modificaron ni
enviaron nuevas políticas a Kaggle. Informe principal: `V41_REVIEW.es.md`.

- V41 adjunto: `kaggriculture-v41-review-candidate.ipynb`, SHA del agente
  `8951ff93742015cba535b125223cf2e541bb7b602080fc4584f30c2613d210f3`.
  Código extraído como datos, sin ejecutar las celdas; solo se evaluó el agente.
- Ratings consultados 2026-09-14 05:01 UTC: matched6 2650,6; critic 2507,5;
  Frontier v1 2581,4; Frontier v2 2613,3 (submission 56216380).
- 128 duelos exploratorios + 64 oficiales. Las cuatro versiones pierden todos
  sus duelos contra V41 (16 y 8 por versión). Las tres posteriores ganan todos
  contra matched6 (16 y 8 por versión). No equivale a una mejora general del rating.
- Ablación oficial de 16 partidas: V41 intacto gana 8/8 contra v2; cambiando
  únicamente su apertura a la antigua pierde 8/8. Margen medio pasa de +23685,1
  a −2049. Son cuatro semillas ya consumidas, dos lados; diagnóstico posterior.
- Dos trazas instrumentadas repiten exactamente recompensas oficiales. Semilla
  92001: al turno 24 matched6 tiene 1 moneda y V41 56; confirma 1 trabajador frente
  a 3. Diez siembras rechazadas en nuestra partida. V2 pierde finalmente 34701.
- 32 partidas reales (ocho por submission) reproducen las 719 acciones de cada
  versión tras reconstruir el orden de los diccionarios. Los replays JSON ordenan
  claves; no comparar DROP/ventas empatadas sin recuperar el orden de inventario.
  `live_audit.json` conserva tres falsas discrepancias; `physical_audit.json`
  reconstruye el orden y confirma todas. Las cantidades se comprueban en cada turno.
- En dos finales reales v2 descarta 24 unidades: leche 11, fertilizante 7,
  trigo 4, huevo 2. No se atribuye automáticamente la derrota a ese desperdicio.
- Próxima prioridad si Arturo pide implementar: apertura y reservas para mano
  de obra/semillas, reconciliar acciones con recursos confirmados, capacidad
  compartida del almacén. Actualizar rivales, incluyendo V41, antes de promover.

V41 y la ablación local permanecen ignorados en `candidates/`; los replays en
`vendor/review_v41/`. Scripts y recibos en el repositorio. No reutilizar estas
semillas como un holdout nuevo. El notebook V41 declara un gate de élite fallido:
no afirmar gold ni un rating garantizado a partir de esta revisión.
