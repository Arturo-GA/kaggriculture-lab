# Frontier16 — resultados del 27 de septiembre de 2026

**Candidato recomendado para la siguiente verificación en Kaggle:** `f16_repaired`. Validado localmente; todavía no enviado al leaderboard ni verificado en la nube.

## Comparación congelada

Motor oficial `kaggle-environments==1.32.7`. Ocho semillas nuevas (`16301..16308`), diez rivales, ambos asientos y tres políticas: 480 partidas completas. Cada política juega 160. Los asientos comparten mundo: hay ocho semillas independientes, no 160.

| Política | Victorias | Empates | Derrotas | Puntos (V + ½E) |
|---|---:|---:|---:|---:|
| F15 desplegado | 116 | 16 | 28 | 124 |
| Base pública sin modificar | 140 | 16 | 4 | 148 |
| F16 corregido | 156 | 0 | 4 | 156 |

F16 mejora **+32 puntos frente a F15** y **+8 frente a la base pública** en el mismo panel. El cambio completo mezcla avance público y capas propias; el segundo número mide el aporte de las capas sobre esa base.

| Rival | F16 V/E/D | Delta de puntos frente a F15 | Delta frente a base pública |
|---|---:|---:|---:|
| `f15_e81` | 16/0/0 | +8 | +0 |
| `n27_lynnsakurai_031656` | 16/0/0 | +16 | +8 |
| `g25_mooman0222_a62376` | 16/0/0 | +0 | +0 |
| `g25_mooman0222_baf0d3` | 16/0/0 | +0 | +0 |
| `n23_arsgorynich_4f8637` | 14/0/2 | +6 | +0 |
| `n23_prvsiyan_178ae0` | 16/0/0 | +2 | +0 |
| `g25_wangyh_v44` | 16/0/0 | +2 | +0 |
| `n25_abhinav0370_127ed3` | 14/0/2 | -2 | +0 |
| `n23_kenanzhang9_b52378` | 16/0/0 | +0 | +0 |
| `v43` | 16/0/0 | +0 | +0 |

Se respetaron todas las puertas registradas antes de la prueba: +6 puntos o más frente a F15, al menos 65 % en el enfrentamiento directo, al menos 50 % contra la base pública, ningún rival por debajo de −2 puntos, aporte propio total no negativo y ejecución sin errores registrados. No se cambiaron los umbrales después de ver resultados.

Máximo observado por callback: **531.6 ms** en este equipo con seis procesos. Cada partida terminó con 719 decisiones y 720 estados. Nueve pruebas unitarias pasaron; dos pruebas diferenciales confirmaron 1438 decisiones idénticas tras la reparación descrita abajo.

## Cambios y experimento descartado

La base pública elegida es Farmer John and the Idle Seller (`03165654`), Apache-2.0. Se añadieron una asignación de posiciones de venta mediante programación dinámica sobre subconjuntos y la integración de venta de existencias al inicio de la demanda (idea E081 de mooman0222). Se conservan comandos físicos, cantidades en la capa de ordenación y barreras para compras del mismo producto.

Se probaron seis variantes en 108 partidas de exploración, después de 72 partidas de selección de bases públicas. La combinación elegida ganó 15/16. La variante de tres pasadas sobre F15 y la liquidación sin el optimizador no fueron elegidas.

La primera versión congelada `f16_selected` fue rechazada: una función pública heredada indexaba órdenes vacías y ocultaba un `IndexError`. Se conservaron su plan, partidas parciales y diagnóstico en `results/frontier16/`. La versión corregida conserva explícitamente la misma decisión ante esos huecos, sin borrar posiciones; los errores inesperados siguen siendo visibles. El nuevo holdout usa otras ocho semillas.

## Archivos y reproducción

- Fuente: `candidates/f16_repaired.py`, SHA-256 `0c6ac464ec556dc96a045c6575e718bb3aa77a153a97f9bae506eec3a32807cd`.
- Notebook autónomo: `kaggle_frontier16/experiment.ipynb`; se comprobaron los bytes de cada archivo que contiene.
- Paquete local: `results/frontier16/repaired/local/submission.tar.gz`, con `main.py`, `LICENSE.txt` y `NOTICE.txt`.
- Evidencia: `plan.json`, `holdout.json`, `holdout_summary.json`, `unit_tests.json` y `local_package.json` en `results/frontier16/repaired/`.
- Reconstrucción: `python build_f16.py`; pruebas: `python -m unittest test_frontier16 -v`; aceptación: `python assess_f16.py`; notebook: `python make_frontier16_notebook.py`; paquete: `python pack_frontier16_local.py`.
- Investigación y fuentes: [FRONTIER16_RESEARCH.es.md](FRONTIER16_RESEARCH.es.md).

El control automático de aprobación bloqueó el push a Kaggle y exige autorización explícita para este notebook y `jarturo/kaggriculture-frontier16-queue`. No se sorteó ese bloqueo. El notebook privado está preparado para 32 partidas oficiales adicionales con semillas `16401..16404`; esas partidas todavía no se han ejecutado. Solo exporta un archivo en Kaggle si pasan sus comprobaciones.

## Qué implica para 2660–2700

Es una mejora medida sobre F15 y sobre la base pública, dentro de este panel. No hay una conversión validada de estos resultados al rating objetivo. Los agentes privados de los primeros puestos tienen diferencias económicas que el panel público no reproduce. Las dos submissions activas siguen siendo F14B y F15; no se sustituyeron.
