# Frontier19 — cuatro partidas por equipo y dos plazas

Fecha de investigación: **30 de septiembre de 2026**. Arturo autorizó dos envíos
nuevos para intentar alcanzar los puestos 200–300. Los recibos JSON son la fuente
del estado real de las submissions; preparar o ejecutar el notebook no equivale
a enviar al leaderboard.

## Situación de partida

Consulta de las 15:35 UTC: equipo **657**, mejor rating **2018,0**. F18
`56617687` estaba en **1963,0** y F17 `56615489` en **2018,0**. Los cortes eran
2275,9 para el puesto 300, 2339,6 para el 250 y 2396,5 para el 200. Estas cifras
son una fotografía; no permiten predecir la puntuación de un agente nuevo.

La [fecha límite oficial](https://www.kaggle.com/competitions/kaggriculture/overview/timeline)
es el 30 de septiembre a las 23:59 UTC, 18:59 de Lima. Kaggle anuncia partidas
posteriores hasta aproximadamente el 15 de octubre o la convergencia.

## Muestra y diagnóstico

Se seleccionaron las cuatro partidas públicas completas más recientes de la
mejor submission activa de **cada uno de los 101 equipos en los puestos
200–300**, sin filtrar por victoria: **404 apariciones de jugadores en 360
partidas distintas**. Se añadieron cinco referencias de posiciones superiores
y veinte partidas propias para diagnóstico. El conjunto descargado contiene
400 episodios distintos; `selection.json` registra selección, fechas y hashes.
Las pérdidas propias se seleccionaron deliberadamente y no estiman una tasa de
victorias imparcial.

Al comparar dos partidas con cuatro, **seis equipos** que parecían abrir siempre
SW antes del turno 240 dejan de cumplirlo. En cambio, **65/101** lo hacen en las
cuatro partidas. Solo **2/101** conservan exactamente la misma combinación de
animales al turno 288 en los cuatro casos. Son señales descriptivas de variación
con el contexto, no prueba de una regla interna concreta. El detalle está en
`four_game_stability.json`.

Se reprodujeron exactamente las recompensas finales y la contabilidad de las
**20 partidas propias** con el motor oficial 1.32.7. Hallazgos principales:

- En la muestra objetivo, la mediana de apertura de SW es el turno **218**;
  nuestra apertura habitual lo tiene disponible en **266**, dos días después.
  La mediana de fresas al turno 288 es **25**, frente a nuestras 33.
- No basta con adelantar `BUY_LAND`: en la pérdida `115841455`, la caja propia
  era 992 en el turno 218 y 1821 en 240. El salto de caja llega con los melones
  cerca de 263. Cambiar la expansión exige rehacer también la financiación y
  las rutas de los trabajadores.
- En ese episodio perdimos **7043** frente al rival que ocupaba el puesto 268.
  La diferencia de ingresos de huevos fue **−12785**, de zanahorias **−7757**.
  Es una diferencia de producción y asignación de recursos, además del mercado.
- Otras derrotas, −341, −165 y −682, sucedieron con granjas prácticamente
  iguales. Ahí la secuencia de órdenes y las operaciones de insumos sí son
  hipótesis concretas y comprobables.
- 304/404 apariciones compran y revenden algún insumo en el mismo turno. Esto
  no significa que todas operen intensamente: contando cada producto por turno,
  la mediana es dos y solo 100/404 tienen al menos diez registros. El recuento
  suma trigo y fertilizante aunque coincidan en un turno. Se distingue el
  ingreso bruto de ventas del ingreso neto después de compras.

Una corrección de alimentación heredada de la investigación F18 evita que
`PICKUP WHEAT 0` bloquee una compra de rescate para animales hambrientos.
Conserva caja mínima, capacidad y comandos físicos. La regresión procede de un
estado real: seis ovejas, un trigo en la mano y cinco unidades faltantes. Su
corrección está probada; no se le atribuye por sí sola una mejora de rating.

## Discusiones y código público reciente

Se descargó y examinó estáticamente el notebook
[Farmer John and the Wheat Seller](https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-wheat-seller),
actualizado el mismo día, además de otras seis publicaciones. No se ejecutaron
celdas arbitrarias de notebooks descargados. Los hashes y metadatos están en
`public_sources.json`. El agente de Lynn se usa como rival reactivo, no como
fuente de una supuesta estrategia privada de un jugador top.

La [discusión sobre RL y ejecución](https://www.kaggle.com/competitions/kaggriculture/discussion/744380)
señala un problema relevante: maleza, acciones y futuras tiendas comparten
aleatoriedad. Una política puede cambiar la secuencia futura aun usando la misma
semilla. Otra [experiencia de RL](https://www.kaggle.com/competitions/kaggriculture/discussion/743716)
describe buen rendimiento contra scripts públicos sin trasladarlo a los rivales
más fuertes. Son observaciones del foro, no resultados propios de RL.

Los avisos sobre [colas de evaluación](https://www.kaggle.com/competitions/kaggriculture/discussion/744277)
y [reactivación de agentes](https://www.kaggle.com/competitions/kaggriculture/discussion/744614)
se archivaron para interpretar el estado del envío. No se confunde un rating
inicial con convergencia.

Como contraste metodológico se revisaron dos trabajos recientes:

- [Code-Space Response Oracles, Hennes et al., marzo de 2026](https://arxiv.org/abs/2603.10098):
  propone generar políticas interpretables como código mediante modelos de
  lenguaje dentro de un proceso de mejores respuestas. Incluye refinamiento
  iterativo y búsqueda evolutiva. La idea relevante para este proyecto es evaluar
  programas candidatos contra una población, en vez de valorar su complejidad o
  novedad por sí sola. Es una conexión metodológica; este experimento no reproduce
  CSRO completo ni sus resultados.
- [An Open-Ended Learning Framework for Opponent Modeling, AAAI 2025](https://ojs.aaai.org/index.php/AAAI/article/view/34488):
  estudia el problema de generalizar desde oponentes fijos a conductas nuevas y
  genera rivales de distintos estilos y niveles. Mi interpretación para nuestra
  evaluación es que ganar a varias copias de una familia pública aporta menos
  evidencia de la que parece. Nuestro panel sigue siendo limitado y así se
  informa; la búsqueda de mercado compara escenarios acotados y no entrena el
  Transformer descrito en ese artículo.

## Hipótesis implementadas y descartadas

1. **Sustituir vacas/ovejas por gansos según demanda prevista.** La sustitución
   coherente de compra, construcción y manejo perdió alrededor de 3658–5051
   en algunas semillas frente a F18. Se descartó.
2. **Ampliar a seis gansos en SE.** Tras corregir una excepción en un prototipo,
   la variante final no encontró oportunidades que activasen la ampliación en
   las semillas de exploración. No se presenta como mejora.
3. **Pronóstico de ventas aprendido de partidas recientes.** Se extrajeron
   patrones de 404 apariciones, excluyendo los episodios propios de diagnóstico,
   y se condicionaron solo a tiendas e historia ya observables. Hubo coincidencias
   en una traza real, pero no cambios de ventas que mejorasen esa pérdida. En el
   panel exploratorio las salidas fueron idénticas al control del experimento.
4. **Cartera de rutas de producción con expansión temprana.** Se agruparon
   aperturas físicamente compatibles y se conservaron rutas completas en vez de
   mezclar comandos inconexos. Ambas variantes terminaron 2V/22D, con margen
   medio cercano a −9684. Las repeticiones no recuperan la adaptación del agente
   original. Se descartaron.
5. **Compras/reventas de insumos más grandes.** La variante más agresiva ganó
   contra algunos notebooks y perdió sus ocho enfrentamientos preliminares
   contra F18. Esa no transitividad exige evaluar varios rivales.
6. **Sustituir como máximo una oveja y considerar primero rutas factibles.**
   Después de los fallos de sustitución masiva se ensayó esta hipótesis por
   separado, conservando un mínimo de ganancia prevista de 400 y del 10 %.
   En 16 duelos exploratorios no activó ninguna sustitución y dio resultados
   idénticos a los 16 duelos de su control. No se seleccionó.

No se incorporó una red neuronal ni se presenta una copia de acciones públicas
como recuperación del código privado de sus autores. Los diagnósticos con rival
grabado no son validación competitiva: el rival no reacciona y puede cambiar el
estado aleatorio. Se eliminó del evaluador antiguo la interpretación incorrecta
de que conservar cierto porcentaje de caja del rival haría válido ese resultado.

## Finalistas y prueba independiente

Las variantes conservan la producción base F18 e incorporan el arreglo de
alimentación y una búsqueda acotada de secuencias de venta. Solo se mueven
ventas cubiertas por existencias proyectadas, sin alterar cantidades o comandos
físicos; las compras de precio fijo mantienen su orden relativo y nunca se
adelantan. El modelo de rival se usa únicamente cuando las granjas públicas son
muy similares. Pasan veinte pruebas iniciales de regresión y contratos, más cuatro regresiones
de alimentación aplicadas a Market1.

- `f19_market2`: dos respuestas sucesivas a la secuencia modelada del rival.
- `f19_robust`: maximiza la peor **mejora sobre la misma base** frente a dos
  secuencias modeladas; esto no equivale a garantizar robustez frente a cualquier
  oponente.
- `f19_balanced`: añade tamaños de operación hasta 32 y compara dos escenarios
  de compras del rival.
- `f19_pressure`: permite hasta 64 y usa un solo escenario para insumos.

El plan se congeló a las **16:25:32 UTC**, antes de ejecutar sus partidas:
cuatro finalistas y F18 de control, cinco rivales reactivos, ocho semillas nuevas
19101–19108 y ambos asientos: **400 juegos**. Los rivales son F18, F17, el
notebook actualizado de Lynn y dos enfoques públicos de producción distintos.
`plan.json` fija hashes, requisitos y desempate antes de ver los resultados.

La puerta pide al menos +2 puntos respecto al control (victoria = 1, empate =
0,5), al menos 9/16 contra F18, mejora en tres semillas, sin deterioro mayor de
dos puntos ante un rival, cero errores y menos de un segundo por llamada.
Se conservan los fallos de la puerta y no se relajan sus umbrales después de ver
el resultado. La comprobación posterior en Kaggle tiene semillas distintas y
valida ejecución, latencia y bytes exportados; no añade un umbral competitivo
basado en una muestra de apenas ocho duelos por política.

Solo `f19_market2` superó todos los criterios del primer panel. `f19_robust`
ganó un duelo más en total, pero perdió tres contra Lynn que el control ganó;
incumple los límites de retroceso. Para la segunda plaza se registró un panel
adicional a las **17:01:52 UTC**, con ocho semillas nuevas y los tres rivales más
relevantes. Compara la respuesta directa `f19_market1` con ocho iteraciones
`f19_market8`. La primera usa una búsqueda de respuesta, la segunda la repite
hasta ocho veces o hasta detectar un ciclo. Ambas mantienen cantidades y rutas
físicas. La evaluación adicional usa los mismos umbrales y conserva el fallo
original de Robust. Market1 obtiene 44/48 frente a 38/48 del control, pero su
retroceso de dos puntos contra Lynn también incumple el límite fuera del duelo
directo. Se elige como segunda plaza experimental, con ese fallo explícito, bajo
la autorización actual para dos envíos; el criterio original no se modifica. Los dos rivales de producción más débiles, donde todas las
políticas empataron en puntos, no se repiten en este bloque.

**Limitación central:** F18 ganó 38/40 en el primer panel público de esta
investigación pese a estar en 1963 en Kaggle. Muchos scripts públicos están
correlacionados, y los rivales de producción más diferentes son relativamente
débiles. Ocho semillas y dos asientos no son 400 mundos independientes.
Una mejora local pequeña no demuestra que alcancemos 2276–2397 ni el top 300.

Los resultados y recibos verificados figuran a continuación. El repositorio y
el notebook se mantienen privados.

## Resultado verificado y envíos

| Política | V/D/E | Puntos | Delta frente a F18 | Pasa |
|---|---:|---:|---:|---|
| f19_market2 | 75/5/0 | 75 | +3 | Sí |
| f19_robust | 76/4/0 | 76 | +4 | No |
| f19_balanced | 61/19/0 | 61 | -11 | No |
| f19_pressure | 48/32/0 | 48 | -24 | No |
| F18 control | 65/1/14 | 72 | — | Referencia |

Se evaluaron todos los requisitos del plan, incluyendo deterioro máximo por rival,
semillas con mejora, errores y latencia. Los resultados completos de los cuatro
candidatos permanecen guardados, incluidos los rechazados.

Kaggle completó **24 juegos nuevos**, con cero errores, y confirmó
que ambos archivos exportados coinciden byte por byte con los archivos locales.
Los resultados de nube son comprobaciones adicionales, no pronósticos del rating.

La segunda plaza se estudió en **144 juegos adicionales**, con ocho semillas
nuevas 19301–19308 y tres rivales: F18, F17 y Lynn. Se conservaron los mismos
umbrales. El fallo original de Robust no fue borrado ni reinterpretado.

| Política, panel adicional | V/D/E | Puntos | Delta frente a F18 | Pasa |
|---|---:|---:|---:|---|
| f19_market1 | 44/4/0 | 44 | +6 | No |
| f19_market8 | 34/14/0 | 34 | -4 | No |
| F18 control | — | 38 | — | Referencia |

Los porcentajes brutos de los dos paneles no son comparables: cambian semillas
y rivales. Es una campaña adaptativa de investigación, no una única prueba
confirmatoria sin selección de candidatos.

**Decisión explícita para la segunda plaza:** Market1 se envía como experimento,
con la autorización actual de Arturo para dos plazas. Gana 44/48 frente a 38/48
del control y 16/16 contra F18, pero pierde dos puntos adicionales contra Lynn;
el límite fuera del duelo directo era −1. Su puerta sigue marcada **No**.
Se conserva la selección estricta original en `selection_decision.json` y la
decisión de envío con este riesgo en `release_selection.json`. No se cambia
el umbral ni se sigue buscando una muestra favorable para ocultar el fallo.

- **f19_market2**, submission **56714342**, estado `SubmissionStatus.COMPLETE`
  comprobado en 2026-09-30T17:22:21.562555+00:00. Contra F18: 11/16 puntos locales;
  8/8 puntos en nube. Máximo de llamada en nube: 313.1 ms.
  SHA de fuente: `b264030ccb0bb26da379c25bbfda7b1b6f40c03840045f29dc22476a75a5a516`.
  SHA de paquete: `f9fc3c1708025c84aa895e3576b6bae2885ed81ffed0494293ea0afaa76db109`.
- **f19_market1**, submission **56714336**, estado `SubmissionStatus.PENDING`
  comprobado en 2026-09-30T17:22:21.562555+00:00. Contra F18: 16/16 puntos locales;
  8/8 puntos en nube. Máximo de llamada en nube: 342.6 ms.
  SHA de fuente: `ed66b321ec70c1aebbbd135ba644d719bd536282d54a97c1a8270b1f9fedad56`.
  SHA de paquete: `fc9b6f213b3eb1cae5b31fa8a810db05b99864688286a90b56093e04a16243ff`.

[Notebook privado](https://www.kaggle.com/code/jarturo/kaggriculture-frontier19-policy-validation).
Se verificó la privacidad descargando metadatos y comparando las celdas del notebook.
Se realizaron exactamente dos envíos. Las intenciones previas al POST y los recibos
están separados para evitar duplicados tras una desconexión.

La mejora demostrada corresponde a este panel. El objetivo top 200–300 sigue
pendiente de confirmación por las partidas del leaderboard.
