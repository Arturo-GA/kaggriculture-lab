# Frontier17: de las derrotas al siguiente candidato

Consulta inicial: 27 de septiembre de 2026, 16:58 UTC. Frontier16 (`56609913`)
tenía **2457,1 puntos, puesto 258**, con 40 victorias y 17 derrotas. El puesto 100
estaba en **2619,6**. Es una fotografía del leaderboard, no una predicción del
puntaje final. El rating de cada rival en los registros es el de su equipo al
consultarlo, no necesariamente el de la submission exacta cuando se jugó.

## Qué se examinó

Se descargaron todas las 17 derrotas disponibles de F16, cuatro victorias
estrechas y siete derrotas de F15 ante equipos fuertes. `audit_f17_replays.py`
reconstruye las **28 partidas** usando las dos secuencias de acciones originales,
la semilla original y el motor oficial `kaggle-environments==1.32.7`.

Los 56 resultados finales coinciden exactamente y cada contabilidad cumple
`3000 + ventas − compras − contratación − terrenos = dinero final`.
No se ejecutaron celdas de notebooks públicos para esta investigación.

Evidencia: [snapshot](results/frontier17/live_snapshot.json),
[episodios](results/frontier17/episodes.json),
[contabilidad completa](results/frontier17/replay_audit.json),
[resumen por producto](results/frontier17/loss_summary.json).

## Dónde se pierde

**1. Operaciones especulativas expuestas entre dos turnos.** En la derrota contra
trantrikien239, la secuencia heredada compraba trigo y lo revendía en el turno
siguiente. Por ejemplo, en el paso 296 compró 48 unidades; el rival compró y
vendió 48 en el mismo turno. Nuestro siguiente turno vendió las 48 a un mercado
distinto. La desventaja final fue de 8488 monedas; el componente neto de trigo
(`ventas − compras de trigo`) explicó una diferencia contable de **7558**.

Se trazó el origen de la compra: estaba en la ruta propia 103, no en una compra
nueva requerida para alimentar animales. Se ensayaron cancelación y cierre en
el mismo turno, conservando las órdenes físicas. Contra el rival grabado:

| Variante | Margen final |
|---|---:|
| F16 original | −8488 |
| Cerrar la pareja en el mismo turno | −3338 |
| Cancelar la pareja especulativa | −576 |
| Cancelar + búsqueda de compras intraturno | −306 |

Es una prueba contrafactual de diagnóstico: el rival grabado no puede reaccionar.
La última mejora de margen incluye +3849 monedas propias y −4333 del rival;
no son 8182 monedas nuevas de producción. Los importes exactos quedan en
`diagnostic_summary.json`.

**2. Competencia por el orden de las compras.** Rivales como ALLAI insertan
parejas de compra/venta de trigo o fertilizante alrededor de nuestras compras.
Eso puede encarecer los insumos. Grandes cifras de ventas de estos productos
no equivalen a gran producción: ShunkiKyoya intercambió miles de unidades que
tienen compras compensatorias. El análisis usa ingresos netos, no ventas brutas.

En ocho de las 17 derrotas, los conteos de cultivos y animales eran iguales en
los días 15 y 27. Esto no demuestra igualdad de coordenadas, rendimientos,
trabajadores o decisiones; sí justifica investigar diferencias de mercado.

**3. Producción insuficiente contra composiciones distintas.** El mercado no
resuelve todas las derrotas:

| Rival | Margen F16 | Evidencia de composición |
|---|---:|---|
| keiz | −17320 | Día 12: rival 15 vacas y 4 ovejas, 3 melones y 3 tomates; nosotros 12 vacas, 5 ovejas, sin esos melones ni tomates. |
| Smackaveli | −20845 | Día 18: 58 zanahorias frente a nuestras 7; diferencia bruta de ventas de zanahoria de 35646, parcialmente compensada por otros productos y costes. |
| ShunkiKyoya | −11583 | Día 12 ya tenía 14 ovejas, 4 vacas y cultivos distintos; en día 24 mantuvo 15 melones y 9 tomates. |

Frontier17 conserva esas tres derrotas. No se presenta una modificación de
mercado como solución demostrada frente a planificadores productivos privados.

La instrumentación también cuenta acciones sin efecto, alimento ausente y
desbordes en `DROP`. No atribuye valor económico a cada acción sin efecto:
algunas forman parte de esperas previstas. El contador de desbordes no incluye
por sí solo el depósito automático nocturno.

## Cambio implementado

`frontier17_roundtrip.py` inspecciona exclusivamente las rutas propias y elimina
parejas `BUY_PRODUCT`/`SELL` del mismo producto y cantidad en turnos consecutivos.
Se limita a los pasos 216–647, sin cruce de día ni recogida prevista del producto
en el turno siguiente. Conserva los huecos de órdenes y todos los comandos de
campo; recalcula las ventas futuras del planificador. Las pruebas competitivas
comprueban el efecto conjunto de las capas que consumen esas rutas.

`frontier17_input_market.py` busca operaciones de compra y venta que dejan el
mismo inventario final alrededor de compras necesarias. Solo actúa con granjas
públicamente similares, un máximo de diez órdenes y margen de caja/capacidad.
Prueba tamaños 8, 16, 32 y 48 y distintas posiciones usando el modelo de precios
heredado. No accede a órdenes simultáneas ni inventario privado del rival: usa
un escenario de rival parecido al propio. Esa hipótesis puede fallar y debe
medirse en partidas completas. Se probó además una variante conservadora con
dos escenarios; quedó detrás de la versión elegida en exploración.

No hay entrenamiento de RL, red nueva ni acceso al código privado del top.
La contribución de esta ronda es original y parte de fallos observados; conserva
las atribuciones completas de F16 y de su base pública.

## Validación que evita confundir diagnóstico con fuerza

- Exploración: cuatro semillas 17001–17004; ambas mejoras por separado y juntas.
- Diagnóstico: 21 replays de F16, con control que reproduce exactamente las 21
  partidas originales. El combinado mejora 15, empeora 2 y deja 4 iguales;
  convierte 4 derrotas y pierde 0 de las cuatro victorias originales. Las dos
  regresiones son Matin Urdu (−95 adicionales) y Ezzzzzekki (−170).
- Holdout registrado antes de correr: 256 partidas oficiales, candidato y F16,
  ocho rivales, ocho semillas nuevas 17101–17108 y ambos asientos. Ocho semillas
  no son 256 escenarios independientes. Reglas en
  [plan.json](results/frontier17/plan.json); resultados finales en
  [FRONTIER17_RESULTS.es.md](FRONTIER17_RESULTS.es.md).
- Las pruebas unitarias comparan el inventario y las compras del candidato con
  el mercado simultáneo oficial bajo varios rivales; verifican además falta de
  caja/capacidad y conservación de las órdenes físicas de las rutas.

Una revisión posterior, después de congelar el código, encontró cinco derrotas
nuevas. Sin reajustar el candidato, se reprodujeron con F16 como control y se
contrastaron con F17: Agent 0 −258 → +486; Justin Yang −1056 → −774;
哈基米南北路多 −511 → −269; JezzLynn −227 → +360; Rishant Sharma −206 → −139.
Mejoraron las cinco y se convirtieron dos. Se conserva la misma limitación:
los rivales grabados no pueden responder. Estos episodios amplían las 22
derrotas de F16 examinadas; no se utilizaron para elegir o cambiar el código.

## Foros revisados y límites de las fuentes

[Six things I wish I'd known before trusting my local win rates](https://www.kaggle.com/competitions/kaggriculture/discussion/743231)
advierte sobre semillas correlacionadas, relaciones no transitivas y rivales
distintos según la banda de rating. Se aplica mediante control emparejado,
varias familias y semillas reservadas. No se toma su simulador rápido como
sustituto del motor oficial.

[My RL Won, But Also Failed](https://www.kaggle.com/competitions/kaggriculture/discussion/743716)
describe una experiencia de RL que dominaba agentes públicos pero se estancó
ante rivales fuertes. Es un relato de un participante, no una demostración de
que RL no sirva. Refuerza la necesidad de medir en la población objetivo.

El [hilo sobre cierre de publicaciones](https://www.kaggle.com/competitions/kaggriculture/discussion/741281)
anuncia el 23 de septiembre a las 23:59 UTC. Una
[consulta del 27 sobre versiones posteriores](https://www.kaggle.com/competitions/kaggriculture/discussion/743890)
seguía sin respuesta al revisarla. F16 contiene una base pública descargada el
27; añadir código propio no resuelve por sí solo esa duda de elegibilidad.
Esta ronda no incorpora código de notebooks nuevos posteriores a F16. Se deja
registrada la incertidumbre y no se afirma elegibilidad para premios.

## Lo que falta para sostener un top 100

La mejora de mercado puede ayudar en los enfrentamientos cercanos. La siguiente
línea productiva debe comparar el rendimiento marginal de cultivos y animales
según tiendas, ciclos restantes, alimentación y trabajo disponible, especialmente
la transición de fresas hacia zanahoria/tomate y una segunda cosecha de melón.
Las tres derrotas anteriores proporcionan casos concretos para evaluar ese
planificador. Copiar sus acciones grabadas no permite validar una política que
reaccione a cambios de mercado.

Ni ganar a F16 ni dominar el panel público convierte automáticamente el
candidato en top 100. La confirmación requiere partidas nuevas en Kaggle contra
esa banda. Los replays seleccionados por derrota tampoco permiten estimar un
porcentaje de victorias general ni una franja calibrada de rating.
