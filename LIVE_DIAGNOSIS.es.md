# Diagnóstico de la submission y segunda ronda de estrategias

12 de septiembre de 2026. Submission `56190498`; agente `matched6`.

## El rating 687 era una lectura temprana

La consulta autenticada a Kaggle a las **18:40 UTC (13:40 Lima)** devuelve
**1885,9**, estado `COMPLETE`. Durante el diagnóstico se observaron también
1062,1 y 1595,4. Estas cifras corresponden al mismo envío, sin reemplazarlo.
687 es el valor informado por Arturo; no se conservó una captura API de ese punto.
1885,9 es una instantánea, no una predicción del rating final.

La evaluación oficial comienza con un rating inicial y organiza partidas con
agentes de rating parecido. Para actualizarlo cuenta ganar, empatar o perder;
ganar por más monedas no da por sí mismo más rating. Solo las dos submissions más
recientes permanecen activas. [Reglas de evaluación](https://www.kaggle.com/competitions/kaggriculture/overview/evaluation).
El texto consultado mediante la API está en `results/live/evaluation.txt`.

Se descargaron y auditaron las **cinco primeras partidas públicas** disponibles
al iniciar la revisión, además de la validación. Las cinco fueron victorias y
acabaron con ambos agentes en `DONE`. Reproducir `matched6` sobre las observaciones
propias de esos replays produjo exactamente las mismas **3595 acciones**, sin
diferencias. El autojuego de validación no se cuenta como victoria pública.
Evidencia: `results/live/audit.json`; replays originales en `vendor/live/`, fuera
de Git. No se afirma haber auditado todas las partidas posteriores a ese corte.

El primer panel local era pequeño para estimar fuerza general. Esa limitación
sigue vigente, aunque el dato 687 no demuestra una caída de rendimiento.

## Qué se probó ahora

Se añadieron dos rivales públicos distintos por hash:

- [Kaito: V43 Sparse Shop Hybrid](https://www.kaggle.com/code/kaitofukami/103-128-fresh-public-v43-sparse-shop-hybrid).
- [yhay81: Shop Router 0911 Simple](https://www.kaggle.com/code/yhay81/shop-router-0911-simple).

Se respeta el último callable que selecciona el cargador oficial de Kaggle.
Kaito exporta un wrapper con nombre distinto de `agent`: la antigua aserción del
evaluador rechazaba ese formato válido. Se corrigió el evaluador; esto no cambia
el agente ya enviado. Cada partida registra hashes de ambos participantes,
entrypoints, tiendas finales, estado, margen y tiempo por decisión.

El panel inicial de 32 partidas encontró una debilidad concreta: `matched6` ganó
7/8 contra Shop Router y 8/8 contra Kaito; V37 ganó respectivamente 5/8 y 8/8.
No son agentes certificados del top actual ni un panel élite independiente.

Se construyeron dos variantes que incorporan los **14 planes y 64 combinaciones
de primeras tiendas** de Shop Router al controlador reactivo de V37:

- `routes14`: reserva original de cuatro turnos.
- `routes14m6`: reserva de seis turnos bajo la condición de semejanza de matched6.

En 32 partidas exploratorias, ambas ganaron 7/8 contra matched6 y 7/8 contra
Shop Router. `routes14` pasó a la evaluación con semillas nuevas por su mayor
margen exploratorio. Esta elección usa la exploración, no el leaderboard.

La validación ejecutó 128 partidas: ocho semillas nuevas, dos asientos, dos
candidatos y cuatro rivales. Sus resultados completos están en
`results/routes14_holdout.json`; el resumen reproducible es
`results/routes14_summary.json`.

| Rival | routes14 | matched6 de control |
|---|---:|---:|
| matched6 | 8 victorias / 16 | 16 empates / 16 |
| Shop Router | 16 victorias / 16 | 14 victorias / 16 |
| prvsiyan | 12 victorias / 16 | 16 victorias / 16 |
| Kaito | 16 victorias / 16 | 16 victorias / 16 |

**Decisión: conservar matched6.** La sustitución completa de planes no demuestra
una mejora general: cambia dos derrotas por victorias frente a Shop Router,
pero introduce cuatro derrotas frente a prvsiyan y no supera a matched6 en
enfrentamientos directos. Es una decisión conservadora tras examinar los datos;
no un test estadístico prerregistrado. No se exportó routes14 como nueva submission.

Se añadieron **192 partidas locales** a esta ronda; el total documentado pasa
de 162 a 354. No son 354 observaciones independientes: hay controles, semillas
exploratorias repetidas y dos asientos relacionados por semilla.

El motor comparte un generador aleatorio para eventos diarios: una política
puede cambiar el número de casillas vacías y, con ello, el consumo de aleatoriedad
antes del sorteo de tiendas. Usar la misma semilla no garantiza idénticas tiendas
entre políticas. Por eso también se registra la secuencia efectivamente observada.

## Estrategias siguientes, concretas y todavía no demostradas

1. **Selector de proyectos compatible con el estado.** Evitar elegir un plan
   completo solo por el nombre de las tiendas. Puntuar proyectos cortos con la
   caja, edificios, cultivos, almacén y trabajadores propios disponibles; rechazar
   proyectos cuyas precondiciones no se cumplen. El experimento de 14 planes no
   identifica todavía si sus pérdidas proceden de la ruta o de su interacción con
   los controladores heredados. La primera ablación debe separar esas dos causas.
   Después, entrenar un árbol pequeño con resultados de simulaciones es una opción
   barata de inferencia; comprobarlo con semillas y familias de rivales reservadas.

2. **Ventas con varios escenarios de oferta rival.** Comparar mantener, vender
   parcialmente y vender todo el excedente, conservando inventario comprometido.
   Usar cosechas y animales visibles para construir escenarios de oferta baja,
   media y alta; no tratar el almacén privado rival como si fuera conocido.
   Antes de optimizar, contrastar precios y consumo proyectados con el motor.
   El objetivo debe ser evitar derrotas, con el margen como diagnóstico secundario.

3. **Búsqueda de políticas con liga diversa.** Conservar rivales de diferentes
   familias de código y excluir duplicados por hash. Usar optimización de pocos
   parámetros, demostraciones e intervenciones acotadas para reducir coste; reservar
   escenarios nuevos para una única evaluación final. La imitación y las ligas de
   Lux AI, y la evolución guiada por evaluadores de AlphaEvolve, aportan ideas útiles;
   sus resultados no garantizan un rating en Kaggriculture. Fuentes y límites en
   [la investigación previa](RESEARCH.es.md).

No se ha entrenado todavía ese selector ni una política RL, y no hay evidencia de
superar 3000. La mejora de esta ronda es el diagnóstico real, el panel ampliado y
el descarte medido de una modificación que parecía prometedora en exploración.

## Reproducir esta ronda

```powershell
python -X utf8 -m kaggle kernels pull kaitofukami/103-128-fresh-public-v43-sparse-shop-hybrid -p vendor/kaito -m
python -X utf8 -m kaggle kernels pull yhay81/shop-router-0911-simple -p vendor/router -m
python extract_panel_v2.py
python build_routes_experiment.py
.\.venv\Scripts\python.exe evaluate.py --candidates matched6 v37 --opponents kaito router --seeds 3101 3102 3103 3104 --workers 4 --output results/panel_v2.json
.\.venv\Scripts\python.exe evaluate.py --candidates routes14 routes14m6 --opponents router matched6 --seeds 3101 3102 3103 3104 --workers 4 --output results/routes14_screen.json
.\.venv\Scripts\python.exe evaluate.py --candidates routes14 matched6 --opponents matched6 router prvsiyan kaito --seeds 42001 42002 42003 42004 42005 42006 42007 42008 --workers 4 --output results/routes14_holdout.json
python summarize_routes.py
python audit_live.py
.\.venv\Scripts\python.exe analyze_live.py
```

El rival prvsiyan se obtiene con el procedimiento del README inicial. Verificar
los hashes de `results/panel_v2_sources.json`: los notebooks públicos pueden
cambiar. Los comandos de auditoría descargan partidas de la cuenta autenticada;
no realizan envíos a la competencia. El snapshot de cinco partidas queda fechado
por los episodios incluidos en `results/live/episodes.json`.
