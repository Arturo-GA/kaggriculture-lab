# Retomar Frontier16

**Estado posterior: enviada como `56609913` el 27/09/2026 a las 13:31 UTC.**
Notebook privado confirmado por los metadatos remotos:
https://www.kaggle.com/code/jarturo/kaggriculture-frontier16-queue .
El recibo de submission y la comprobación de la nube están en
`results/frontier16/repaired/`. Última consulta: `PENDING`, sin error ni puntaje
todavía. El nuevo par previsto es F15 + F16 al activarse el agente.

Solicitud del 27/09: revisar el GitHub actualizado, discusiones, notebooks y
líderes de Kaggle, y mejorar la estrategia con objetivo 2660–2700 o el mejor
resultado posible. Se trabajó desde `36ee7d1` en el repositorio privado
`Arturo-GA/kaggriculture-lab`.

## Archivos principales

- `FRONTIER16_RESEARCH.es.md`: fuentes actuales, deduplicación de notebooks,
  lectura del leaderboard y límites del análisis de replays del top.
- `FRONTIER16_RESULTS.es.md`: resultados generados de la evidencia completa.
- `candidates/f16_repaired.py`: candidato final,
  SHA-256 `0c6ac464ec556dc96a045c6575e718bb3aa77a153a97f9bae506eec3a32807cd`.
- `results/frontier16/repaired/plan.json`: puertas y semillas registradas antes
  de correr las pruebas; `holdout.json` y `holdout_summary.json`: resultados.
- `kaggle_frontier16/experiment.ipynb`: notebook privado autónomo preparado.
- `results/frontier16/repaired/local/submission.tar.gz`: paquete local con
  código y avisos de licencia; `local_package.json` verifica su identidad.

## Qué cambió

Base nueva `n27_lynnsakurai_031656`: Farmer John and the Idle Seller,
Apache-2.0, todos los avisos conservados. Se añaden `frontier16_window.py`
(integración propia de E081) y `frontier16_queue.py` (programación dinámica
original sobre posiciones de ventas cubiertas por existencias). La búsqueda
conserva las cantidades, no cambia acciones físicas, mantiene las compras en
orden relativo y no las adelanta. Su rival de precios es una copia de nuestras
órdenes, no una observación del inventario privado del oponente.

Se preservó el candidato fallido `f16_selected` y su primera validación
incompleta. La telemetría nueva descubrió un `IndexError` en `_s839_apply`:
`_r37_reorder_sales` no toleraba huecos `[]`. `frontier16_hole_guard.py`
preserva explícitamente la misma respuesta anterior, sin borrar huecos.
Dos pruebas diferenciales, semillas 16102 y 16107, compararon las 1438 acciones
y fueron idénticas. No se ocultaron excepciones inesperadas ni se relajaron
umbrales: el candidato corregido usa ocho semillas nuevas, 16301–16308.

## Validación y reproducción

Nueve pruebas unitarias; panel oficial de 480 partidas (candidato, F15 y base
pública, cada uno contra diez rivales, ocho semillas, ambos asientos).
F16: 156 victorias y cuatro derrotas; F15: 116 victorias, 16 empates y 28
derrotas. Delta emparejado +32. El aporte sobre la base pública está en el
informe y el JSON final. No confundir los ocho mundos con 160 muestras
independientes, ni este panel con un rating calibrado de Kaggle.

```powershell
.venv\Scripts\python.exe -X utf8 build_f16.py
.venv\Scripts\python.exe -X utf8 -m unittest test_frontier16 -v
.venv\Scripts\python.exe -X utf8 assess_f16.py
.venv\Scripts\python.exe -X utf8 make_frontier16_notebook.py
.venv\Scripts\python.exe -X utf8 pack_frontier16_local.py
```

`build_f16.py` puede recuperar el código público original de los primeros
1.148.715 bytes de la fuente final, verificando su SHA, si falta la copia local
excluida de Git. Los rivales de otras familias continúan siendo entradas
locales; no se redistribuyen sueltos. Las licencias originales y el aviso de
modificaciones congelado están en `attribution/frontier16/`.

## Subida privada, verificación y submission

La revisión automática rechazó inicialmente dos veces `kaggle kernels push -p kaggle_frontier16`.
Después de la primera se comprobó, en lectura, la cuenta con `mine=True` y se
enumeró el contenido exacto del notebook. La segunda revisión exige que Arturo
autorice explícitamente este notebook privado y
`jarturo/kaggriculture-frontier16-queue`. Arturo resolvió ese bloqueo con
**«Dale submissions y súbelo como privado»**. El ejecutable CLI no estaba
instalado; una vez autorizada la acción, la API oficial subió la versión 1
(kernel id `136116215`). Se descargaron sus metadatos y se confirmó
`is_private=true`.

La nube completó las 32 partidas oficiales nuevas (semillas 16401–16404):
F16 ganó 7/8 a F15 y 7/8 a la base pública. Delta emparejado +9 frente a F15,
sin errores y máximo 364,5 ms por callback. `verify_frontier16_cloud.py`
recalculó la comparación y verificó fuente, licencias y archivo completo.
SHA-256 del TAR de Kaggle, idéntico al paquete local:
`13de630eb92cf78d3c74d47073867e6f70899d2441531a98a9ec3cef19e86067`.

`submit_frontier16.py` envió una sola submission, `56609913`, conservando F15
(`56592376`) y reemplazando F14B (`56570873`) cuando se active. Para consultar su estado sin enviar
de nuevo:

```powershell
.venv\Scripts\python.exe -X utf8 submit_frontier16.py
```

El script comprueba hashes y privacidad, guarda intención antes de subir y
no repite una subida incierta. Los recibos del intento anterior bloqueado y
del empaquetado local conservan el estado histórico de ese momento; el estado
actual está en `kaggle_verified.json` y `submission_receipt.json`.
