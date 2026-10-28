# Frontier15: venta al inicio de cada ventana de demanda — 26/27 de septiembre de 2026

Petición de Arturo (26 sep, 22:30 UTC): "Revisa nuestras partidas y analizar una estrategia que pueda llevarnos a 2600
de raiting ya puede ser una tercera idea combinada con las 2 que usamos sino busca cómo se podría ganar a los de
2500-2600" y "revisa que ese chat no sea antiguo y avanza". Enviada solo tras su autorización posterior (§8).

## 1. Situación (26 sep, 22:27 UTC)

10.057 equipos. Par activo: 56568493 (Frontier14, `f14_adv4_h12`) en 2334 y 56570873 (Frontier14B, `f14_adv4_h16`) en
2398; equipo en el puesto 433. Cortes: oro 2796,9 (puesto ~30), **plata 2367,6 (puesto 502)**, bronce 2158,3; 2500 =
puesto 228, 2600 = puesto 115. Emparejamiento ~15 partidas por hora y plaza. Por franja de rival (las dos plazas):
< 2300 101-15, 2300-2500 63-57, **2500-2600 4-19**, 2600+ 3-9.

## 2. Qué se revisó

Las 96 partidas en vivo del par activo contra rivales de 2400+ (replays en `vendor/live_f14`, lista
`outputs/session/gold/episodes_f14live.json`, libros de cuentas `ledger_f14live.json`: trayectoria de la diferencia de
dinero, ventas por producto y día, censo de producción final, apertura y dinero del rival en el paso 1, pasos en los
que divergen las acciones).

### 2.1 Los de 2450-2600 son clones de nuestra propia línea

En 45 de las 48 partidas contra rivales de 2440-2600 el rival termina con **exactamente la misma granja** que
nosotros (mismas manos, cuadrantes, vacas, ovejas y gansos) y el mismo dinero en el paso 1 (1042). Las acciones de
las unidades coinciden casi siempre; las ventas por producto y día son idénticas salvo en unos pocos pasos, y la
diferencia final va de −7 a −1500. Es una **carrera de tiempos de venta en los días 16-28**: quien lista antes el mismo
producto cobra el precio recuperado y el otro vende en el bache.

Dos clones ganaron por mucho más con una decisión de **cultivo ligada a las tiendas**: taiseiu (+3290) plantó
zanahorias el día 6 con un PET_CAFE (las zanahorias cotizan 1,3-1,4 veces su base al final) y Rômulo Drumond (+2693)
plantó tomates el día 11 con una PIZZA_SHOP (+3900 solo en el día 21). Kudo plantó zanahorias sin pet café y perdió
por 6005. Varios rivales de 2500+ hacen "lavados" (BUY_PRODUCT trigo o fertilizante n y SELL n) y rellenan la lista
con `SELL WHEAT 0`: el motor descarta las órdenes de cantidad 0 (huecos de posición) y las idas y vueltas cuestan
cero por su regla de cotización; no dan ventaja medible.

### 2.2 Las palizas son agentes privados de otra producción

Todas las derrotas de −3000 a −35486 (arutyunoff, by, kuengo, feel the agi, tine.sh, Capitaalgain, boominginging,
keiz, Crop Dustas, lumen, ymg_aq) son agentes con otra granja: gansos, 10-16 tomates, zanahorias, huevos. kuengo iba
−21647 en el paso 432 y terminó +35486. Contra ellos no hay ajuste de tiempos que sirva; son la mayoría de los 2600+.

### 2.3 Hechos del motor (kaggle_environments 1.32.7, `kaggriculture.py`)

- El precio es una función pura del inventario del mercado. Por encima del nivel base: leche y fresa bajan
  linealmente (−2,1 y −1,9 por unidad; cero a +76 y +62), lana y melón cuadráticamente (lana 200 → 107 a +40, 1 a +58),
  huevo y trigo logarítmicamente, zanahoria y tomate con raíz (suaves).
- El pueblo retira su demanda **después de cada paso múltiplo de 4**: una unidad por producto y tienda (dos en las
  tiendas de un solo producto: YARN_STORE, PET_CAFE) y una de cada producto del centro cada 24 pasos.
- Las órdenes i-ésimas de ambos jugadores se liquidan **unidad a unidad con la misma cotización**; vender a 1 no
  añade inventario.
- Régimen en vivo en las partidas contra clones (48 replays): leche, lana y melón están saturados desde el día 12-15
  (precio 0,3-0,6 de la base), la fresa solo en los días 21-27; huevo y zanahoria escasean (precio por encima de la
  base, la zanahoria hasta 1,4 con pet cafés). Con 3 pizzerías/mercados el tomate llega a 109-177 en los días 21-29
  (base 60); con 2, a 83-96; con 1, a 71-74.

Conclusión: en un mercado saturado, el primer vendedor tras cada retirada del pueblo se lleva la holgura recuperada;
el que espera vende en el bache y el bache no se recupera (la producción de los dos supera el consumo).

## 3. Candidatos (`build_f15.py`)

Cada candidato = Frontier14B (`f14_adv4_h16`, sin tocar) + **una** capa propia al final del archivo, después del
lockstep, que solo usa funciones del propio cha22 (`projected_shed`, `_adv_future`, `_v9_town_draw`, `_lk_reorder`):

| Variante | Capa |
|---|---|
| `f15_e81` | vende todo el almacén proyectado de leche, lana y fresa en el primer paso de cada ventana (paso % 4 == 1); idea E081 de mooman0222 (MIT) |
| `f15_e81g` | lo mismo solo para productos saturados (inventario ≥ base), melón incluido |
| `f15_slk` | al abrir la ventana vende los lotes planificados de la ventana más la retirada del pueblo siguiente (solo saturados) |
| `f15_wh` | al abrir la ventana adelanta los lotes planificados de esa ventana (casi no actúa: el adelanto de cha22 ya los toma) |
| `f15_ad` | ventanas 16 → 24 para el resto de la partida cuando el rival lleva ≥ 6 unidades más vendidas que nosotros en 48 turnos (flujo del rival reconstruido por el propio cha22) |
| `f15_tom2` / `f15_tom1` | la inversión tardía en tomates del propio cha22 se permite con ≥ 2 / ≥ 1 pizzerías o mercados y ≥ 9000 monedas (base: ≥ 3 y ≥ 12000) |
| `f15_e81_tom2` / `_tom1` | las dos cosas |

## 4. Bucle cerrado 1 (semillas 9401-9404, asiento 0; `outputs/session/gold/screen_f15_0926.json`)

Rivales: nuestro `f14_adv4_h16`, `f14_adv4_h12`, `f14_adv4_h24`, Frontier13, cha22 (haideptry v7), prvsiyan,
Herd-Safe forecast4, Wangyh v44 y mooman E081.

| Candidato | Total | Media | vs adv4_h16 | vs adv4_h12 | vs adv4_h24 | vs F13 | vs mooman | vs Wangyh v44 |
|---|---:|---:|---|---|---|---|---|---|
| **f15_e81** | **34/36** | +875 | 4/4 +766 | 4/4 +841 | 3/4 +280 | 4/4 +892 | 4/4 +1901 | 4/4 +1108 |
| f15_ad | 32/36 | +761 | 4/4 +505 | 4/4 +543 | 1/4 +176 | 4/4 +732 | 3/4 +1554 | 4/4 +714 |
| f15_e81g | 30/36 | +821 | 3/4 | 3/4 | 2/4 | 3/4 | 3/4 | 4/4 |
| f15_slk | 28/36 | +697 | 3/4 | 3/4 | 2/4 | 3/4 | 2/4 | 4/4 |
| f15_wh | 23/36 | +403 | 1/4 | 3/4 | 1/4 | 3/4 | 2/4 | 3/4 |
| control f14_adv4_h16 | 12/16 | +469 | — | — | — | 3/4 | 3/4 | 3/4 |

La liquidación al abrir la ventana gana a nuestro propio agente activo en los cuatro mundos y al agente del autor de
la idea (mooman E081, que la aplica sobre otra base) por +1900. Latencia máxima 252 ms.

## 5. Bucle cerrado 2 (semillas 9405-9408, asiento 0; `screen_f15b_0927.json`)

| Candidato | Panel (9 rivales × 4) | Media | Cara a cara |
|---|---:|---:|---|
| **f15_e81** | **34/36** | +861 | 4/4 contra f15_ad (+484) |
| f15_e81_tom2 (= tom1) | 34/36 | +936 | gana a f15_e81 por 730 en el único mundo con 2 pizzerías-mercados (9405); empate en los otros |
| f15_e81g | 34/36 | +835 | |
| f15_ad | 30/36 | +705 | |
| f15_tom2 (sin E081) | 26/36 | +667 | |
| control f14_adv4_h16 | 23/32 | +513 | |

Las dos pérdidas de `f15_e81` en cada cribado son contra mooman E081 (2/4), que ya vende al abrir la ventana: ahí la
carrera se reparte. El mundo 9406 tiene asimetría de asiento (+508 incluso en espejo puro), así que las diferencias
de 508 en ese mundo no son de los candidatos. El tomate con 2 pizzerías-mercados aporta +730 en el único mundo en
que actúa; con 1 no cambia nada en estos mundos.

## 6. Panel congelado (96 partidas reales, `outputs/session/gold/panel_f15_live.json`)

Se reproducen las 96 partidas en vivo con la misma semilla, el rival congelado en sus acciones grabadas y
`f15_e81` jugando nuestro asiento: **victorias 29 → 52** (26 derrotas pasan a victoria, 3 al revés; +365 de media;
el rival conserva el 99,7 % de su banco; sin errores). Por franja del rival: 2400-2500 **21 → 42 de 62**, 2500-2600
**5 → 7 de 22**, 2600+ 3 → 3 de 12. Por plaza: 56568493 (adv4_h12) 6 → 18 de 30; 56570873 (adv4_h16) 23 → 34 de 66.

Lectura honesta: el rival congelado no reacciona. Contra los clones de 2500-2600, cuyas ventas grabadas ya iban
adelantadas, la liquidación al abrir la ventana recupera solo dos partidas; en bucle cerrado, donde esos mismos
linajes reaccionan (sus capas condicionadas al precio esperan tras nuestra venta), gana 34/36. La verdad estará
entre ambas cifras: esperamos dominar la franja 2400-2500, disputar la 2500-2600 y no mejorar contra los privados de
2600+.

## 7. Holdout registrado (semillas 9411-9418, ambos asientos, 1056 partidas; `results/frontier15/`)

Puerta registrada antes de correr (`plan.json`): control emparejado = Frontier14B (`f14_adv4_h16`, nuestra plaza
56570873); total emparejado ≥ +4 sobre 22 rivales (los 19 de Frontier14B más nuestros `f14_adv4_h16/h12/h24`), espejo
≥ 50 %, cha22 ≥ 70 %, ningún rival por debajo de −2, sin errores, < 1000 ms.

**Resultado: PUERTA SUPERADA con total +33** (`holdout_summary.json`): espejo contra Frontier14B **14/16 (+6)**, contra
`f14_adv4_h12` 14/16 (+5), contra `f14_adv4_h24` 8/16 (+8; el control pierde 12), cha22 exacto **16/16 (+666)**,
Frontier13 14/16, prvsiyan 14/16, haideptry v7 16/16 (+2), Wangyh v44 14/16 (+2), mooman E081/E082 12/16 (+4/+4),
Herd-Safe forecast4, Gluzdov ×2 y statma 12/16 (+2 cada uno), las cuatro familias de la subida 16/16; únicos −2:
Frontier13, haideptry 8378f7 (8/16) y Master Engine V3 (14/16). 289 ms máximo, 0 errores.

Matiz honesto: la media de margen emparejada es −54 monedas por partida. Casi todo viene del mundo 9416
(FARMERS_MARKET ×2 + ICE_CREAM + BRUNCH), donde toda la línea cha22 —candidato y control por igual— pierde por
7600-8400 contra la familia Herd-Safe; en el resto, la liquidación gana más partidas pero a veces por menos margen
(vende antes y más barato que el control cuando el rival no compite). Solo cuenta ganar o perder.

**Extra `f15_e81_tom2` (inversión en tomates con 2 pizzerías-mercados): total −1, con −4 contra cha22, Frontier13 y
prvsiyan y −6 contra Master Engine V3 → rechazada.** El tomate con menos de 3 tiendas pierde más mundos de los que gana.

## 8. Kaggle

Kernel privado `jarturo/kaggriculture-frontier15-windowhead` (`make_frontier15_notebook.py`, 880 KB; semillas
9421-9424 contra cha22, Frontier13 y prvsiyan, control Frontier14B): **48/48 limpias, 258 ms; cha22 8/0 (+936),
Frontier13 8/0 (+851), prvsiyan 8/0 (+1727; el control 6/2); total +2 sobre el control, regla completa sin
incumplimiento**; archivo `9b4f993b8b4186477279b7ff5b902766b5324763ac43ed1b99fdaa517e779eba`
(`results/frontier15/kaggle_verified.json`).

**Enviada el 27 de septiembre de 2026 a las 00:06 UTC a petición de Arturo** ("Cuando termine y tengas un nuevo su
misión que cumpla los requerimientos dale submit en kaggle"): **submission 56592376** (recibo
`results/frontier15/submission_receipt.json`); retira la 56568493 (Frontier14 adv4_h12, 2341). Par activo:
56570873 (Frontier14B, 2396) + 56592376 (Frontier15). Seguimiento: `python live_report.py 56570873 56592376`.

## 9. Qué esperar y qué haría falta para 2600

- Contra la franja de clones 2400-2500 el candidato debería dominar (panel congelado 21 → 42 de 62; bucle cerrado
  8/8 contra nuestro agente activo). Contra 2500-2600 mejora, pero no está garantizado; contra los privados de 2600+
  no hay mejora. Estimación honesta: nivel 2450-2600, no 2600 asegurado.
- Para pasar de ahí haría falta producción distinta, no tiempos: cultivo ligado a las tiendas (zanahorias con
  PET_CAFE, tomates con PIZZA_SHOP desde el día ~11 como Rômulo Drumond, no la inversión tardía de cha22 que pierde
  con < 3 tiendas), que es lo que hacen los 2600+.
- Cualquier envío retira la plaza más antigua (56568493, adv4_h12 en 2334). Un envío nuevo necesita 1-2 días para
  asentarse; el cierre es el 30 de septiembre.
