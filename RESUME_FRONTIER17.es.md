# Retomar Frontier17

Petición de Arturo: analizar las pérdidas del modelo actual y desarrollar
estrategias para acercarse al top 100. Después autorizó «Y lanza una plaza a kaggle».
**F17 se envió una sola vez: submission 56615489**. El notebook y el repositorio siguen privados.

## Estado comprobado

- Consulta del 27/09/2026, 17:33 UTC: F16 `56609913`, COMPLETE, **2449,8**, puesto
  **273**, 67 partidas, 45V/22D. F15 `56592376`, COMPLETE, 2105,0, 118 partidas.
  Corte del top 100: **2621,9**. Snapshot: `results/frontier17/live_snapshot_final.json`.
- Candidato local: `candidates/f17_selected.py`, SHA-256
  `62b766886208e572462c19f45706cf9d0eded7d048c39a55a6093212bd72426f`.
- Paquete: `results/frontier17/local/submission.tar.gz`, SHA-256
  `0660e5c4f80c0cb0bbfd67a542d444ee1527a4ed3d409e4c5b30090cdecc4cb3`.
- Notebook subido y completado, versión 1: `jarturo/kaggriculture-frontier17-input-market`.
  Privacidad y coincidencia de todas las celdas verificadas mediante descarga desde Kaggle.
  `notebook_prepared.json` conserva el estado histórico de preparación; los recibos actuales son
  `kaggle_upload.json`, `kaggle_private_verified.json`, `kaggle_run_status.json` y `kaggle_verified.json`.
- Kaggle completó 16 partidas, semillas 17201–17204: F17 8 victorias de 8 contra F16,
  control F16 8 empates contra sí mismo, cero errores, máximo 248,4 ms. Paquete idéntico al local.
- Submission `56615489`, enviada el 27/09 a las 17:49 UTC. Consultar `submission_receipt.json`
  para el estado verificado más reciente y `active_after_submission.json` para los agentes activos.

## Qué cambió y qué demostró

1. `frontier17_roundtrip.py`: elimina parejas especulativas de compra y venta
   al turno siguiente dentro de nuestras rutas. No modifica los comandos físicos
   de esas rutas. Esas parejas eran explotables, sobre todo en la ruta 103.
2. `frontier17_input_market.py`: busca compras/reventas en un mismo turno alrededor
   de compras de insumos, con caja y espacio observables. Usa un escenario de
   rival similar; no conoce sus órdenes simultáneas. Puede perder contra otra
   política de mercado, como demuestra la prueba adicional.
3. `build_f17.py`: conserva F16 completo como prefijo y crea variantes propias.
   `f17_combined` y `f17_selected` tienen los mismos bytes. No modificar este
   último después del holdout. No se agregó código público nuevo en esta ronda.

Holdout preregistrado, motor oficial 1.32.7, 256 partidas:

- F17 **128V/0E/0D**; F16 **111V/14E/3D**. Puntuación 128 frente a 118.
- F17 vence a F16 **16/16**. Ganancia fuera de ese duelo: **+2**, frente a
  `n25_abhinav0370_127ed3`. Ninguna regresión de puntuación por rival.
- Cero errores/fallbacks registrados; máximo del candidato **458 ms**.
- Ocho semillas nuevas, no 256 mundos independientes.
- Prueba adicional contra `f17_robust`: F17 **4/8**, F16 **0/8**, cuatro semillas
  nuevas. Cero errores y tiempo dentro del límite. Es un rival sintético propio.
- Doce pruebas unitarias pasaron. Los tests nuevos contrastan el mercado oficial
  para comprobar inventario y compras; no son solo comparaciones con nuestro código.

Replays: 28 reconstrucciones exactas con contabilidad (17 derrotas y cuatro
victorias F16, siete derrotas F15). Diagnóstico contrafactual de F16: 4/17
derrotas convertidas, ninguna de las cuatro victorias perdida, dos regresiones.
Después llegaron cinco derrotas F16 nuevas: sin retocar el código se mejoran
cinco y se convierten dos. **Los rivales grabados no reaccionan** y esta selección
por derrotas no permite estimar una tasa de victoria ni rating.

La gran pérdida contra trantrikien239 pasa de −8488 a −306; las de keiz,
Smackaveli y ShunkiKyoya siguen sin resolver. La siguiente mejora productiva
debe considerar tiendas, ciclos, alimentación y trabajo; revisar composiciones
y ledger en `FRONTIER17_RESEARCH.es.md`, no trasplantar cintas rivales.

## Envío realizado y continuación

El notebook ejecutó su verificación y exportó el paquete tras superar los controles.
`verify_frontier17_cloud.py` recomputó la matriz, puntuación, tiempos, hashes y contenido
del archive. `submit_frontier17.py` registró intención antes de llamar a Kaggle y guardó
el id devuelto. Conservar privado el notebook y el repo.

La autorización de una plaza está ejecutada. No volver a subir otra copia de F17.
`python submit_frontier17.py` sin argumentos solo refresca el recibo existente.
La nueva submission está destinada a acompañar F16 y retirar F15 al activarse;
usar la lista oficial de agentes activos para comprobar que ya ocurrió.

Semillas consumidas: exploración 17001–17004; pruebas de contratos 17091;
holdout 17101–17108; estrés 17301–17304; Kaggle 17201–17204.
Resultados y hashes en `results/frontier17/`; datos brutos en `vendor/live_f16`
y `vendor/research_f17`, excluidos de Git. `resume_eval.py` sirve si una futura
evaluación se interrumpe; esta ronda quedó completa.

## Restricción pendiente de procedencia

El hilo 741281 anuncia cierre de publicación el 23/09, 23:59 UTC. La consulta
743890 sobre versiones posteriores seguía sin respuesta. F16 hereda una base
pública del 27; las capas propias de F17 no despejan esa duda. Está documentada
sin afirmar una interpretación definitiva ni elegibilidad para premios.

Archivos de informe: `FRONTIER17_RESULTS.es.md`, `FRONTIER17_RESEARCH.es.md`.
Scripts: `research_f17.py`, `audit_f17_replays.py`, `analyze_f17.py`,
`summarize_f17_diagnostics.py`, `fetch_f17_new_losses.py`, `report_f17.py`,
`pack_frontier17.py`, `make_frontier17_notebook.py`, `cloud_frontier17.py`,
`verify_frontier17_cloud.py`, `submit_frontier17.py`.
