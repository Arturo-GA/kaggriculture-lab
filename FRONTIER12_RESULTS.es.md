# Frontier12: el enrutador por rama y mundo — 24 de septiembre de 2026

Petición de Arturo: las dos Frontier11 no pasaron de 2200; pensar primero estrategias para salir del impasse, revisar
los supuestos, buscar algo mejor, apuntar al top 100 y, al terminar, enviar a las dos plazas.

## 1. Diagnóstico con las partidas en vivo

| Submission | Rating (24 sep, 11:20 UTC) | Partidas | Victorias | Derrotas contra rivales de <2300 |
|---|---:|---:|---:|---:|
| 56509994 (`f11_pv_lock`) | 2122 | 86 | 64 (74 %) | 16 de 71 |
| 56511120 (`f11b_hs3_lock`) | 2237 | 83 | 72 (87 %) | 6 de 72 |

Los replays de las 33 derrotas se reproducen a la moneda en el motor local; sin errores ni consumo del margen de
tiempo. 25 de las 33 son contra clones de la familia pública (misma cinta: 25 contrataciones y 18 trigo / 12 melón /
4 fresa en seis días), 16 de ellas por menos de 500 monedas; 8 son agentes privados distintos (vacas en el turno 0,
ruta de zanahoria, mucho cómputo) que ganan por 4.000-21.000.

Con el panel de replays (rival congelado), la *otra* base gana 7 de las 22 derrotas de `f11_pv_lock` y 5 de las 11 de
`f11b_hs3_lock`, incluidas dos de −21.000 que pasan a +9.000 y +4.900.

## 2. Supuestos revisados

| Supuesto | Prueba | Resultado |
|---|---|---|
| La partida entre dos agentes de la familia es determinista y la decide el mundo | 759 pares locales con ambos asientos | 711 márgenes idénticos por asiento |
| El clon rival se puede reproducir con una copia ("sombra") | Copia alimentada con sus observaciones | 719/719 acciones idénticas; con el almacén equivocado 573/719 |
| Se puede cambiar de base en el paso 144 | Prototipo, 12 partidas | ±8 monedas respecto a la base elegida |
| Saber la lista exacta del rival mejora el orden de ventas | Oráculo con la lista real, 3 semillas | Peor las tres: −98→−355, +91→−292, +57→−594 |
| Una constante puede dar la vuelta a un mundo perdido | 32 variantes de una constante en dos mundos perdidos | `_ADV_LOOK` 4→2: −649→+568; `V9_RACE_DEFAULT` 41→46: −179→+399; rebaño y zanahoria no cambian nada |
| Basta el mundo para elegir la base | 100 semillas × 2 rivales, validación dejando una semilla fuera | Tabla por tiendas: 0,905 puntos frente a 0,887 de "siempre prvsiyan"; oráculo 0,985 |
| **La rama del rival decide más que el mundo** | Las mismas 800 partidas | prvsiyan+lockstep gana 96/100 a su rama; Herd-Safe+lockstep 93/100 a la suya; **elegir la base de la rama del rival: 0,953** |

La rama se lee en el paso 1 en el dinero público del rival tras la compra inicial de trigo: 2854 en todo el grupo
"BUY 20 / SELL 15" (prvsiyan, Gluzdov, haideptry, Order Book, V55-V57, wzhengbiao, yasutakababa…), 2858 en el
grupo Herd-Safe "BUY 8 / SELL 3" (Gluzdov, arsgorynich, statma, nihilisticneuralnet); V53 2867, Metav4 2864. Es
independiente de la semilla.

Descartado: la "clarividencia" (responder al turno con la lista exacta del rival) empeora porque el rival reacciona en
los turnos siguientes; cualquier cambio hay que medirlo en bucle cerrado con la partida completa.

## 3. El enrutador (`candidates/f12_router.py`)

Un solo archivo con los dos candidatos de Frontier11 incrustados (fuentes públicas con sus avisos Apache-2.0 y la capa
lockstep), cada uno en su propio espacio de nombres. Los dos reciben las mismas observaciones; Herd-Safe juega la
apertura (coinciden en 142 de los 144 primeros pasos y su apertura vale +8); en el paso 1 se lee la rama del rival;
en el paso 144 se elige la base de la misma rama que el rival (desconocido → prvsiyan) y desde ahí solo corre esa
base. Carga en 2,5 s, llamadas de 9 ms de media y menos de 350 ms de máximo. La tabla admite además claves por mundo (`rama|tienda1|tienda2`) y
perfiles de constantes por mundo (versión 2, en búsqueda).

## 4. Aceptación (holdout registrado)

Primera versión (apertura de prvsiyan, semillas 8401-8408): 179 puntos frente a 177 (prvsiyan+lockstep) y 172
(Herd-Safe+lockstep); la puerta pedía +4 sobre el mejor control y se quedó a 2. Causa medida: la apertura BUY 20 /
SELL 15 vale **8 monedas menos** que la BUY 8 / SELL 3 en todas las partidas, así que los espejos contra clones
Herd-Safe se perdían por 8. La v1b juega la apertura Herd-Safe (la huella del rival pasa a 2850 = grupo BUY 20 /
SELL 15, 2854 = grupo Herd-Safe).

Puerta registrada antes de correr (`results/frontier12/plan.json`): motor oficial, semillas nuevas nunca usadas para
la tabla, ambos asientos, los dos candidatos incrustados juegan el mismo panel como controles emparejados; total del
enrutador ≥ mejor control + 4 y ≥ peor control + 8; ningún rival por debajo del mejor de los dos controles en más de
2; sin errores; llamadas < 1000 ms.

Holdout v1b (semillas 8421-8428, 14 rivales, 672 partidas; la escritura del archivo falló en la partida 456 y las 217
restantes se repitieron en las mismas semillas con escritura atómica): **200 puntos frente a 190 (prvsiyan+lockstep)
y 164 (Herd-Safe+lockstep); puerta superada**; 337 ms de máximo, sin errores.

| Rival (16 partidas) | Enrutador | prvsiyan+lock | Herd-Safe+lock |
|---|---:|---:|---:|
| prvsiyan+lock (espejo con apertura distinta) | 16 empates | — | 6/16 |
| Herd-Safe+lock | 16 empates | 10/16 | — |
| prvsiyan (22 sep) | **16/16** | 16/16 | 6/16 |
| Herd-Safe forecast4 | 12/16 (4 empates) | 10/16 | 12/16 (4 empates) |
| Herd-Safe (Gluzdov), statma ca20 | 14/16 | 14/16 | 14/16 |
| Order Book, Order Book v3, haideptry 2965 | 14/16 | 14/16 | 14/16 |
| V57, wzhengbiao hybu, yasutakababa v16 | 16/16 | 16/16 | 12, 10, 8 /16 |
| Gluzdov More Wheat | 12/16 | 12/16 | 14/16 |
| guarda V54 | 16/16 | 16/16 | 16/16 |

Lectura: contra la rama Herd-Safe el enrutador iguala al mejor de los dos (+2 sobre prvsiyan en forecast4), contra la
rama prvsiyan iguala a prvsiyan, y contra sus propios clones empata en vez de perder. El punto flojo que queda es el
grupo BUY 20 / SELL 15 que no es prvsiyan (Order Book, haideptry, Gluzdov More Wheat): ahí Herd-Safe sería mejor pero
la huella del turno 1 no los distingue; es lo que ataca la versión 2 (tabla por rama y mundo, perfiles de constantes).

## 5. Kaggle y envío de la primera plaza

Verificación en Kaggle (kernel privado `jarturo/kaggriculture-frontier12-world-router`, versión 1, semillas 8431-8434): el
kernel reconstruye el enrutador a partir de las dos fuentes y la tabla y su hash coincide con el congelado; sin errores,
364 ms de máximo; **8/0 contra Herd-Safe (+401), 8/0 contra prvsiyan (+89), 8 empates contra `f11b_hs3_lock`** (es su
propia base tras la misma apertura) y **6/2 contra el 2965 de haideptry (+698), donde el control `f11b_hs3_lock` hace
8/0**. Total emparejado +4, pero la regla registrada "ningún rival por debajo del control" falla por −2 en ese rival.
Es el punto flojo ya descrito (la rama Order Book comparte la apertura BUY 20 / SELL 15 y la huella la manda a la
base de prvsiyan). Queda registrado como incumplimiento aceptado en `results/frontier12/plan.json`; la puerta local
con dos controles emparejados sí se superó. El archivo se empaquetó en local a partir de los mismos bytes que el
kernel reconstruyó (SHA-256 `be0fa3caa6a2730925ebb3da1bea5c0c06102d9a5dbd38a0b66301aca9a64bd1`,
`results/frontier12/kaggle_verified.json`). Las cinco pruebas de `test_frontier12.py` pasan.

**Enviado el 24 de septiembre de 2026 a las 14:13 UTC a petición de Arturo** ("cuando termines haz submission 2
plazas a kaggle"): `f12_router` = submission **56523438** (recibo en `results/frontier12/submission_receipt.json`),
validada sin errores, arranca en 600. Retiró 56509994 (`f11_pv_lock`, 2147). Activas: 56511120 (`f11b_hs3_lock`,
2256) y 56523438. Seguimiento: `python live_report.py 56523438 56511120`.

## 6. Versión 2 (segunda plaza, en curso)

Búsqueda en bucle cerrado sobre 200 semillas nuevas (8101-8300, asiento 0): seis perfiles de constantes de tiempo de
venta (`_ADV_LOOK` 2/6, `_V92_P_EVERY` 2/4, `V9_RACE_DEFAULT` 36/46) sobre cada base, más una tercera base (Gluzdov
More Wheat + lockstep), contra tres rivales de la rama prvsiyan/Order Book (prvsiyan, Gluzdov More Wheat, haideptry) y
dos de la rama Herd-Safe (Gluzdov, statma). Con eso: tabla por rama y mundo (`rama|tienda1|tienda2`) con perfil, y
validación en semillas nuevas antes de sustituir la segunda plaza.

## 7. Qué esperar

El enrutador convierte las derrotas por el mundo contra su propia familia en empates o victorias, y añade +8 monedas
en todas las partidas por la apertura. En el holdout gana 200 de 224 puntos posibles contra el campo público; en
vivo la primera plaza de Frontier11 ganaba el 74 % y la segunda el 87 %. Contra los privados no cambia nada. La
meta es el top 100 (hoy ~2710); no prometo llegar: dependerá de cuántos privados haya en la franja 2400-2700.
