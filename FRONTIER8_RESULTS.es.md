# Frontier8: qué dice el foro, qué cambió el 19 de septiembre y cómo volver a plata — 19-20 de septiembre de 2026

Pregunta de Arturo: investigar el foro de la competencia y fuentes externas sobre lo que usa el top, y
encontrar una estrategia que pueda estar en medalla de plata. Este documento recoge lo leído, lo medido
y el candidato que sale de ahí.

## 1. Dónde estamos y por qué bajamos

Tabla del 19 de septiembre (9587 equipos): oro 2917,8 (puesto 29), **plata 2665,0 (puesto 479)**, bronce
2450,1. Nuestra fila: **puesto 628, 2600,7** (Frontier7, 273 partidas: 155 ganadas; 25/40 contra rivales de
2600-2700, 7/16 contra 2800-2900; últimos 23 juegos 6/17). La segunda plaza (Frontier5) cayó a 2326: pierde
45/61 incluso contra rivales de 2300-2500.

La causa es una nueva ola pública del 19 de septiembre, mucho mayor que las anteriores:

| Notebook (19 sep) | Qué es | Lo declarado |
|---|---|---|
| **The 2945 Farm** v9/4 (Thomas Tschinkel) | su agente de escalera completo, **2944,7 en vivo** | 519-21 contra los 10 mejores notebooks públicos; 0-36 contra siete equipos del top 10 |
| Demystifying 2900, Top 10 Public Bots, auto top1 | **el mismo archivo byte a byte** (SHA `4f3ca95d…`) | cuatro notebooks de un clic lo distribuyen |
| V49 / V50 (Ahmed Berat Özer) | V48 + capas económicas de Tschinkel; V50 adelanta la expansión de ovejas al día 11 | 96/0 contra V48; 80/0 en mundos con hilo |
| Demand-Preserving (tetsutani) | V50 + ataque de apertura de 22 trigos | 2750 en vivo, el mejor público antes de Tschinkel |
| Farming Score V2 (Arlene), Master Engine V4 | Tschinkel + cierre efectivo de la cola de órdenes | — |
| A Smaller Market Shock (Dmitrii Gluzdov) | Tschinkel + un trigo extra en la apertura | 10/0 contra Tschinkel por +50 |

Medido en nuestro simulador (semillas 5941-5944, 8 partidas por par): **Frontier7 pierde 0/8 contra cada
uno de ellos por −2700 a −3400**. Entre ellos, Arlene > Gluzdov > Tschinkel > Yummers por márgenes
pequeños y constantes (+464, +50); tetsutani > V50 = V49; y entre los dos linajes el resultado se reparte
por mundos (4/4).

## 2. Lo que dice el foro de Kaggle

- **Los notebooks públicos se cierran el 23 de septiembre a las 23:59 UTC** (Addison Howard, Kaggle, hilo
  741281). Después no puede publicarse código nuevo: la parte pública de la población queda congelada una
  semana antes del cierre.
- **El ranking final no es la escalera en vivo**: tras el 30 de septiembre las dos últimas submissions
  siguen jugando dos semanas y se ajusta un único torneo Bradley-Terry sobre esas partidas (María Cruz,
  Kaggle). El historial, la edad y la suerte inicial de una submission no cuentan.
- Una submission nueva empieza en 600 y converge al ~90 % en unas 60 partidas (~5 horas); después el
  ruido es de ±25-50 puntos y dos copias idénticas han acabado a 300-1400 puntos de distancia. Solo cuenta
  ganar o perder, no el margen (Ryo Hasegawa, ex número 1; Rayk Kretzschmar).
- "Clonar una estrategia pública suficientemente reciente basta para estar en el 10 % superior"; en un
  todos-contra-todos de 14 implementaciones públicas la más nueva ganó a la más vieja en 86 de 91 pares
  y no hay ciclos piedra-papel-tijera; cada ola alcanza su pico un día después de publicarse (sobameshi).
- Los que suben fuera de la cinta usan **aprendizaje por refuerzo**: Snorlax (puesto 24) con PPO a nivel
  macro, clonación de comportamiento previa y unas 300 000 partidas; Sayaka Miki (121) también. No es
  replicable en diez días.
- Tschinkel documenta el mismo muro que medimos en Frontier7: su agente pierde 0-36 contra el top 10
  porque ellos plantan ~9 tomates desde el día 12 (71 tomates a 114) y la cinta no tiene mano de obra
  para hacerlo; sus intentos de tomates (0/85, 0/56), de retener producto (−7,5k a −34k), de planificador
  adaptativo (6-24) y de planificador desde cero (990-1578 en vivo) fallaron todos.
- Un hallazgo curioso (leoprovorov, "Hacked stores"): las granjas consumen el mismo flujo aleatorio que
  sortea las tiendas, así que cavar una casilla antes de un sorteo cambia la tienda siguiente en el 77 %
  de los casos; dirigirlo exige conocer la semilla oculta y hoy solo alcanzaría al 10-18 % de las partidas.
  Lo vemos en nuestros datos: la misma semilla da tiendas distintas según el rival.

Fuera de Kaggle solo hay repositorios de participantes. Coinciden en lo mismo: cinta grabada más capas
reactivas que se adelantan a la venta del rival; "las cintas fijas se deprecian 30-40 puntos al día"
(zansued); retener, topes y puertas de venta perdieron en todos los casos.

## 3. La estrategia para plata

La plata es el 5 % superior. Con un agente de 2945 repartido por cuatro notebooks de un clic, la frontera
de plata va a caer dentro del clúster de clones. Dentro de un clúster de copias exactas las partidas son
casi deterministas: gana quien tenga una ventaja constante, aunque sea de 50 monedas. Por eso:

1. **Base**: el agente público más fuerte (linaje Tschinkel v9/4).
2. **Apilar las mejoras públicas compatibles** que ya le ganan por separado (apertura de Gluzdov, cierre de
   cola de Arlene).
3. **Añadir nuestra capa lockstep**, que ordena nuestras ventas contra una copia con el modelo exacto del
   mercado.
4. **Repetir el proceso tras el cierre del 23 de septiembre** sobre la última ola y dejar ese par final en
   las dos plazas antes del 30; desde el 24 nadie puede publicar una base más nueva.

## 4. El candidato

Ver la sección 5 para la versión final y sus números.

`build_f8.py` fija por hash las cuatro fuentes públicas y construye:

| Variante | Contenido |
|---|---|
| f8_stack | v9/4 + apertura de Gluzdov + cierre de cola de Arlene (solo capas públicas) |
| **f8_stack_lock** | f8_stack + orden lockstep de Kaggriculture Lab |
| f8_lynn_lock | Arlene + lockstep |
| f8_tetsu_lock | tetsutani (linaje V50) + lockstep |

Pantalla (semillas 5951-5956, 12 partidas por par, motor C++): f8_stack_lock **72/72** contra Tschinkel
(+452), Arlene (+438), Gluzdov (+404), tetsutani (+701), V50 (+701) y Yummers (+397); f8_stack sin nuestra
capa gana también 72/72 pero por +50 a +107 contra su propio linaje: la capa lockstep aporta unos +350.
f8_tetsu_lock pierde 4/8 contra el linaje Tschinkel.

## 5. Aceptación de f8_stack_lock

Holdout (motor C++, semillas nuevas 5961-5972, 14 rivales, 1008 partidas con control emparejado Arlene,
el mejor agente público sin modificar): **301 victorias de 336 (89,6 %)**; el control gana 256.

| Rival | f8_stack_lock | Margen medio |
|---|---:|---:|
| Tschinkel v9/4, Arlene, Gluzdov, Yummers | 23/1 cada uno | +527 a +772 |
| tetsutani y V50 (linaje V50) | 17/7 | +940 |
| V49 | 19/5 | +1016 |
| Alperen ×2, Melon squeeze, K0013, ziheng, aurax v7, Frontier7 | 20-24 de 24 | +3200 a +4800 |

Diferencia de puntos emparejada +45, cero errores, latencia máxima 418 ms. `f8_lynn_lock` (sin la apertura
de Gluzdov) queda en 297/336.

Confirmación oficial (`kaggle-environments` 1.32.7, semillas nuevas 5981-5986, 144 partidas): **12/0 contra
Tschinkel (+623), 12/0 contra Arlene (+503), 12/0 contra Gluzdov (+574), 10/2 contra tetsutani (+1495),
10/2 contra Alperen y 10/2 contra Frontier7**; diferencia emparejada +16, latencia máxima 153 ms, cero
errores. Las cinco pruebas de `test_frontier8.py` pasan.

Aviso de medición: el simulador C++ no es exacto al bit con este linaje (mundo 5970 contra tetsutani:
−1805 en C++, −1835 en el oficial; mundo 5961: −862 frente a −1414). Los signos coinciden, pero con
márgenes de cientos de monedas la decisión se apoya en el motor oficial.

Dónde perdemos: los mundos con hilo tardío o mucha demanda de zanahoria contra el linaje V50 (en 5970
ellos tenían 27 zanahorias el día 24 y nosotros 6: −7,5k en zanahoria). Una reserva de pienso de un día
en la capa de zanahorias (`f8x_feed1`) dio la vuelta a ese mundo, pero en doce semillas nuevas
(6001-6012) dejó exactamente el mismo balance de victorias (154/168 en ambos casos, ninguna partida
cambiada), así que el candidato congelado no se toca. Queda como primera prueba de la ronda posterior
al cierre.

Verificación en Kaggle (kernel privado `jarturo/kaggriculture-frontier8-stack-lockstep`, versión 1, semillas
6021-6022, ambos asientos, control Arlene emparejado): **4/0 contra Arlene (+477), 4/0 contra Tschinkel
(+477) y 2/2 contra tetsutani (+555 de media; el control también 2/2)**; latencia máxima 167 ms en la CPU de
Kaggle, cero errores. `main.py` y `submission.tar.gz` descargados coinciden byte a byte con el candidato
congelado; SHA-256 del archivo `c87445d0a0f21d588457c2c2da86b01a8ccb28ba999dbea3d52ef86ad4db5881`
(`results/frontier8/kaggle_verified.json`). **No se ha enviado nada al leaderboard.**

## 6. Qué esperar y qué sigue

Tschinkel subió a 2945 con este agente cuando casi nadie lo tenía; una copia nueva iba por 2908 un día
después. Con las copias multiplicándose, su rating se repartirá entre ellas. Nuestro candidato gana 23 de
24 a cada copia exacta y 17 de 24 al linaje V50, así que debería situarse por encima de ambos clústeres;
el corte de plata está hoy en 2665. No es una garantía: una submission nueva tarda ~5 horas en converger y
se mueve ±50-100 puntos por emparejamientos.

Plan hasta el cierre:

1. Enviar Frontier8 ahora (si Arturo lo autoriza) para recuperar la zona de plata.
2. **El 24 de septiembre**, con los notebooks públicos ya cerrados, repetir este mismo proceso sobre la
   última ola (extraer, todos-contra-todos, apilar, lockstep, holdout, oficial, Kaggle) y dejar ese par en
   las dos plazas antes del 30. A partir de ahí ninguna base pública más nueva puede superarnos.
3. Revisar antes del 30 que las dos plazas finales corren sin errores en la escalera.

## 7. Límites

Seguimos por debajo del top 10 adaptativo (RL o planificadores con tomates desde el día 12), igual que
el propio Tschinkel (0-36 contra ellos). El objetivo de esta ronda es plata, no oro. El linaje V50 nos
gana 3 de cada 10 mundos. Las ventajas de cientos de monedas en espejos son reales pero pequeñas: por eso
se confirman en el motor oficial y en Kaggle antes de enviar.
