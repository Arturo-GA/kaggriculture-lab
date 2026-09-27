# Frontier18 — operaciones pequeñas y diagnóstico de alimentación

Arturo pidió comparar dos enfoques **si mejoran**, y amplió la investigación a las cuatro partidas
públicas más recientes de cada equipo del top 100. La autorización no justifica enviar variantes
que fallen la validación. Los recibos de Kaggle bajo `results/frontier18/` son la fuente de estado.

## Candidato que pasa la validación principal

`candidates/f18_small.py`, SHA-256
`d9289a3e55624596ab5c2a8368359542e09249ae7fd64391d506bf82daeec135`.

Conserva íntegramente el prefijo F17. Busca operaciones de insumos de 1, 2, 4, 8 o 16 unidades,
con umbral de ganancia modelada 0,5, en lugar de 8, 16, 32 o 48 y umbral 2. Conserva las
restricciones de caja/capacidad, la semejanza pública entre granjas y el inventario neutral al
terminar las compras/reventas dentro del turno. Es una mejora acotada sobre una base heredada,
con todos sus avisos de licencia; no incorpora código privado de jugadores.

Panel registrado antes de ejecutarse: semillas 18101–18108, seis rivales, ambos asientos,
tres políticas evaluadas, 288 partidas en el motor oficial 1.32.7.

| Política | Victorias | Derrotas | Empates | Puntos (V + 0,5 E) | Puerta de validación |
|---|---:|---:|---:|---:|---|
| F18 volumen pequeño | 94 | 2 | 0 | 94 | Pasa |
| F18 dos escenarios de rival | 82 | 12 | 2 | 83 | No pasa |
| F17 control | 74 | 6 | 16 | 82 | Referencia |

F18 pequeño gana **16/16** contra F17. De sus +12 puntos, ocho vienen de ese duelo y
cuatro del rival sintético `f17_robust`. No pierde puntuación agregada frente a ninguno de los
seis rivales. Mejora en siete de las ocho semillas, pero empeora un punto en la semilla 18103;
no es una mejora universal. Cero errores/fallbacks registrados y máximo 615,6 ms por llamada.
Los 288 juegos contienen ocho semillas, no 288 mundos independientes, y varios rivales
pertenecen a familias públicas similares. No permiten traducir estos números a un rating futuro.

La variante de dos escenarios falla tres requisitos fijados de antemano: +1 frente al mínimo
de +4 puntos, 8/16 contra F17 frente al mínimo de 9 y −2 frente a F16, por debajo del límite
de −1. No se envía aunque el nombre del experimento incluya «robust».

## Experimentos que no se seleccionaron

- Calendario finito de tomate: igualó al control en cuatro semillas de exploración.
- Rotación de zanahoria y combinación con calendario: empeoraron algunos resultados.
- Microcantidades manteniendo el máximo 48: no mejoraron la puntuación de exploración.
- `f18_feed`: evita que `PICKUP WHEAT 0` bloquee la compra de rescate. Corrige una pérdida
  real de producción, pero necesita cobertura competitiva adicional antes de seleccionarse.

El diagnóstico exacto de alimentación está en [el análisis de cuatro partidas](TOP100_CUATRO_PARTIDAS.es.md).
En el episodio 114306320, seis ovejas perdieron 24 unidades de lana por el bloqueo del día 25.
Contra las acciones registradas del rival, el arreglo sobre F18 pequeño cambia −737 a +909.
Ese rival no reacciona, por lo que el resultado queda fuera de la puerta competitiva.
Las cuatro semillas nuevas del panel adicional no activaron el rescate en ninguno de sus
48 juegos del candidato: no proporcionan evidencia de mejora del arreglo en ese escenario.
El panel adicional terminó 48V/48 para ambos candidatos, delta cero, y no pasó los requisitos
de mejora mínima y semillas positivas. Su máximo fue 799,8 ms, sin errores registrados.
El código queda separado; **el paquete seleccionado F18 pequeño no incorpora el arreglo de alimentación**.

## Evidencia reproducible

- `build_f18.py`, `build_f18_market.py`, `build_f18_feed.py`: fuentes y hashes de experimentos.
- `results/frontier18/plan.json`, `holdout.json`, `holdout_summary.json`: panel y decisiones.
- `results/frontier18/feed/`: panel adicional congelado antes de semillas 18301–18304.
- `live_accounting.json` y `animal_trace.json`: reconstrucción exacta de ambas contabilidades
  y de cada ciclo de alimentación, cuidado y producción animal.
- `recorded_rival_diagnostics.json`, `feed_recorded_diagnostics.json`: diagnóstico separado.
- Doce contratos de mercado y cuatro pruebas de regresión de alimentación. El escenario real
  tiene una unidad de trigo en la mano y requiere comprar cinco, no seis.
- `release_f18.py`: genera el notebook privado, verifica juegos/bytes/licencias y envía una vez.
  La intención se guarda antes de llamar a Kaggle; invocaciones posteriores reconcilian el recibo.

Consulta en vivo del 27/09 a las 19:17 UTC (14:17 Lima): F17 **2315,4**, con 21V/1D públicas;
F16 **2407,0**. El rating de F17 había sido 1992,6 diecisiete minutos antes. Estas cifras son
fotografías fechadas, no estimaciones de convergencia.

Notebook: [Frontier18 privado](https://www.kaggle.com/code/jarturo/kaggriculture-frontier18-policy-validation).
Consultar `kaggle_private_verified.json`, `kaggle_verified.json` y
`f18_small_submission_receipt.json` para comprobar subida, verificación y envío por separado.

## Publicación privada y envío

Notebook versión 1, kernel 136157944: privacidad y todas las celdas verificadas por descarga.
Kaggle completó 16 juegos: F18 **8/8** contra F17; control F17 puntuación 4/8 contra sí mismo.
Cero errores y máximo del candidato **150,7 ms**. El archivo de Kaggle es idéntico al local,
incluidos `main.py`, `LICENSE.txt` y `NOTICE.txt`.

SHA-256 del paquete: `28d30e598de4ac49ac6330484a29a2ebcb6d01a9ec17b5fc18a2679f2756d491`.
Enviado una sola vez el 27/09 a las 19:31 UTC: **submission 56617687**.
Se usó **una de las dos plazas autorizadas condicionalmente**. Las otras variantes no pasaron;
no se efectuó un segundo envío. No duplicar: consultar primero el recibo y la lista remota.

Confirmación a las **19:36 UTC (14:36 Lima)**: submission **COMPLETE**, sin error, rating inicial
600. Los dos agentes activos son F18 `56617687` y F17 `56615489` (2366,0 en esa consulta).
F16 dejó de figurar entre los activos. El 600 inicial no es una predicción de convergencia.
