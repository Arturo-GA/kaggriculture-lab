# Resultados del primer experimento

Motor: `kaggle-environments==1.32.7`. Fecha: 12 de septiembre de 2026.
La evidencia local inicial comprende **114 partidas completas**: 4 smoke, 24 exploratorias,
32 de validación inicial y 54 de confirmación. Todas terminaron `DONE/DONE`.
Las semillas y los dos asientos se conservan en los JSON de `results/`.

## Exploración

Tres semillas (101, 202, 303), ambos asientos, siempre contra V37:

| Variante | Victorias / partidas | Margen medio de caja |
|---|---:|---:|
| h2 | 0 / 6 | −2755,67 |
| h6 | 6 / 6 | +2214,67 |
| h8 | 6 / 6 | +2146,67 |
| pressure | 6 / 6 | +1868,00 |

Se seleccionó h6 para la primera validación. En cuatro semillas nuevas (91001–91004)
ganó las ocho partidas contra V37. Contra Nagata mantuvo las victorias pero perdió
algo de caja respecto a V37. Esa observación motivó `matched6`; por tanto, esta primera
validación dejó de ser una muestra ciega para diseñar la nueva variante.

## Confirmación nueva: semillas 92001–92003

Se compararon matched6, h6 y V37 contra V37, Nagata y prvsiyan, en ambos asientos.
Son 54 partidas y tres mundos por rival, no 54 mundos independientes.

| Política | Rival | Victorias / empates / derrotas | Margen medio |
|---|---|---:|---:|
| matched6 | V37 | 6 / 0 / 0 | +2100,00 |
| matched6 | Nagata | 6 / 0 / 0 | +111141,33 |
| matched6 | prvsiyan | 6 / 0 / 0 | +5393,67 |
| V37 | V37 | 0 / 6 / 0 | 0,00 |
| V37 | Nagata | 6 / 0 / 0 | +111141,33 |
| V37 | prvsiyan | 6 / 0 / 0 | +5903,33 |

**matched6 ganó 18/18**, pero V37 ya ganaba 12/12 contra los dos rivales externos.
La mejora de resultados observada corresponde a los enfrentamientos con V37.
Contra Nagata, matched6 conserva exactamente las recompensas del control;
contra prvsiyan, el margen cae 509,67 monedas y la caja propia cae 602 monedas en promedio.
Esto impide afirmar superioridad universal. Los dos rivales externos no constituyen
un panel representativo de los líderes actuales.

Se preselecciona matched6 como **candidato experimental** por conservar el control
contra la granja diferente de Nagata, mientras gana a V37. h6 obtiene algo más de
margen contra V37, pero reduce la caja contra Nagata. No se ha entrenado una red
neuronal ni se ha implementado un algoritmo completo de MPC o AlphaEvolve.

En las 54 partidas de confirmación, todos los contadores de error expuestos por
la telemetría terminaron en cero. El máximo medido fue 314,53 ms por decisión
entre las tres políticas, bajo concurrencia local. Estas medidas excluyen la carga
inicial del módulo; no son una garantía sobre todo el hardware o estados posibles.
El contador de proyección de almacén no resuelta puede ser positivo en V37;
no se confunde ese diagnóstico heredado con un error nuevo.

## Verificación y Kaggle

Cuatro pruebas cubren identidad de baseline, intervención aislada, elección correcta
del entrypoint oficial, escenarios de presión y empaquetado determinista. El notebook
se genera desde archivos explícitos sin incluir credenciales ni rivales descargados.

La versión 1 del kernel realizó la búsqueda inicial. La versión 2 incorpora matched6
y corrige el control de autojuego: los asientos de una semilla pueden tener malas
hierbas diferentes; se exige inversión del margen al cambiar etiquetas, no empate
obligatorio en todas las semillas. La publicación final y sus recibos se registran
en `results/kaggle_run.json` y `results/kaggle/` cuando están disponibles.

Un **push de kernel ejecuta el notebook**. No envía `submission.tar.gz` al leaderboard.
No hay nuevo rating medido para nuestras variantes y no se afirma superar 2700 o 3000.
