# Frontier7: qué hace el top 2 y qué podemos hacer — 18 de septiembre de 2026

Pregunta de Arturo: buscar una estrategia que supere a los dos primeros (Unknown Mother-Goose 3200,
Majkel1337 3176 en la tabla del 18 de septiembre) usando lo que ya hay en GitHub y Kaggle. Este
documento recoge las mediciones, lo que se descartó con números y el candidato que sí sale de aquí.

## 1. Dónde estamos: Frontier5 en vivo

Las dos Frontier5 (56292870 y 56292879, V46 + orden lockstep) llegaron a 2751 (puesto 238) y bajan
(2736 y 2738 el 18 de septiembre). Auditoría de sus últimas 32 partidas contra rivales de 2800 o más
(`outputs/session/live/audit_f5_live.json`, fuera de Git; el bot desplegado reproduce sus acciones en
26 de 32): **8 victorias y 24 derrotas**, 30 submissions rivales distintas.

| Apertura del rival en el turno 0 | Partidas | Victorias | Margen medio |
|---|---:|---:|---:|
| `BUY 7 / SELL 2` (linaje V46-V47-V48) | 12 | 1 | −805 |
| `BUY 3 / SELL 3` | 2 | 0 | −6120 |
| `BUY 50 / SELL 50` | 2 | 0 | −2578 |
| `BUY 5 / BUY 10 / SELL 60` | 2 | 0 | −982 |
| `BUY 5 / SELL 5` | 2 | 2 | +2773 |
| `BUY 30 / SELL 30` | 2 | 1 | +894 |
| otras (una partida cada una) | 10 | 4 | — |

Las derrotas grandes no son de microestructura sino de rebaño: Bryan Pauze (2878, −11412) lleva dos
vacas más y una oveja menos que nosotros desde el día 12; 한밭대학교 (2852, −5115) una vaca más; Tim
Zagrebelny (2801, −4751) y Riva Kajangu (2851, −4573) tres ovejas más y tres gansos menos cuando hay
tienda de hilo. Eso es exactamente el "rebaño según tiendas" de Seyit Kaan Güneş que el V47 público
(17 de septiembre, 15:44 UTC) integró sobre V46 junto con su pre-guardia nocturno (vende a las 21-22 lo
que la guardia de las 23 tiraría) y su propio orden lockstep contra copia (la misma idea que nuestra
Frontier5, con caché por producto). V48 "Clear the Queue" (22:09 UTC, SHA-256 `4b540288…`) añade la
limpieza de la cola de órdenes (quita huecos y ventas repetidas de productos de caja sin mover índices)
y declara 36/0 en tres mundos contra seis fuentes públicas. En nuestro simulador C++ (semillas 5601-5606,
12 partidas por par): **V48 gana 10/2 a f5_lock (−718 para nosotros), 12/0 a V46 (−1909) y 11/1 a
Beyond-48 (+1861)**. La ola pública nos volvió a pasar en un día.

## 2. Qué hace el número 1 (Unknown Mother-Goose)

106 replays públicos de su submission 56221997 (`vendor/top_replays`, fuera de Git). Es determinista
hasta el día 6 y reactivo después (sesión anterior). Contra 79 rivales del linaje de la cinta pública
gana 75 con **+13255 de media** (mediana +11338; caja 112273 frente a 99017). Contra los 27 rivales
restantes gana 27 con +44985. SpaTaro (#4, 193 replays) es distinto desde el turno 0 en todas sus
partidas: totalmente adaptativo.

**No es mano de obra ni volumen.** En esas 79 partidas, líder frente a clon (medias por partida):

| | Líder | Clon |
|---|---:|---:|
| Contrataciones totales | 278 | 271 |
| Contrataciones por día (0-5 / 6-11 / 12+) | 5,4,4,5,4,5 / 8-11 / 10-11 | 5,5,… / 7-9 / 9-11 |
| Cosechas / plantaciones | 483 / 233 | 479 / 239 |
| Riegos / fertilizaciones | 1013 / 180 | 1115 / 91 |
| Ventas totales (monedas) | 89131 | 75202 |

**Es precio y mezcla.** Ventas por producto (unidades por partida, precio medio cobrado):

| Producto | Líder | Clon |
|---|---|---|
| Fresa | 140 u a 138 | 135 u a 100 |
| Leche | 125 u a 120 | 133 u a 93 |
| Lana | 86 u a 169 | 100 u a 132 |
| Huevo | 122 u a 51 | 54 u a 50 |
| Zanahoria | 90 u a 62 | 49 u a 54 |
| Tomate | 64 u a 80 | 2 u |
| Trigo / fertilizante | 314 u / 179 u | 404 u / 284 u |

La diferencia de precio no viene de la carrera del mismo turno (solo 2-4 solapes por partida). Viene del
calendario: el líder vende fresas desde el día 16 (8-15 al día, lotes de 5,9) y el clon desde el día
18-19 con picos de 16-21 al día en los días 22-24 (lotes de hasta 30); leche desde el día 13 frente al
15-18. Su economía: día 6 con 4 vacas, 2 ovejas, 12 melones, 4 fresas y 68 monedas en caja (todo
reinvertido); día 12 con 7,4 vacas, 5,9 ovejas, 3,8 gansos, 22 fresas y 15,5k; día 20 con 29 fresas,
8,8 tomates y 53k; día 27 con 15,5 zanahorias y 95k. Tierra los días 6 y 11 en las 106 partidas.

## 3. El mercado, con el modelo exacto del motor

`price = base ± amp·f(|inv − 10000|)`. Por encima del inventario neutro la fresa cae 1,92 por unidad
(precio 1 a +75), la leche 2,1 por unidad (+76), la lana en cuadrática (cero a +59) y el melón en
cuadrática (+158); por debajo suben en raíz o logaritmo. El pueblo consume cada 4 turnos una unidad de
cada producto por tienda que lo lista (dos si la tienda lista un solo producto, como la de hilo) y una
unidad diaria de cada producto desde el centro: **6 al día por tienda, 12 por tienda de hilo, +1**.

Espejo V48 contra V48 en el motor oficial (semilla 5611, tiendas Pet, Brunch, Smoothie, Pet, Farmers,
Pizza, Smoothie, Pizza): los dos venden 8-22 fresas al día desde el día 19 con un consumo de 19-25; el
precio pasa de 193 a 37-78. La leche cotiza 13-63 hasta que la cuarta tienda de leche la sube a 179 al
final. Sin tienda de hilo la lana vale 1-11 toda la partida (70 unidades por 592 monedas). Eso es lo que
el líder evita: vende antes de que la cinta pública inunde el mercado.

## 4. Palanca medida: retener y dosificar leche y lana (`frontier7_hold.py`)

Estudio fuera de línea sobre nueve espejos oficiales de V48 (semillas 5611-5619, ventas rivales y
consumo grabados, precio exacto): una política "no vender por debajo del precio neutro, soltar lotes de
3 cuando el inventario vuelve al neutro, solo si el consumo diario absorbe el doble de nuestra entrada"
sumaría **+9824 de margen en leche y +3394 en lana en los nueve mundos (unos +1500 por mundo)** si
pudiéramos retener 40 unidades; en fresa es negativa (−1581). Pero el almacén de la cinta no lo permite:
amanece con 80 de 100 (máximo 100), las manos llevan 66 unidades encima por la noche (32 trigo, 13
fertilizante, 6 fresas, 5 huevos, 4-5 leche) y el motor descarta lo que no cabe en el volcado nocturno y
en cada `DROP` sobre un almacén lleno. Con la ocupación real (límite 95 contando lo que llevan las
manos) el potencial baja a **+537 en leche y +1787 en lana en nueve mundos (≈ +260 por mundo)**. Vender
el trigo del almacén para hacer sitio subiría la leche a +3551, pero ese trigo es el pienso: la cinta
alimenta con él a los animales (328-342 órdenes `FEED` por partida) y dos días sin comer el animal escapa.

Se implementó igualmente (puerta por consumo, lote 3, tope 40, límite 95, drenaje desde el día 27,5,
cinta al mando el último día; 0 errores en telemetría) y se midió en el simulador (semillas 5621-5626,
12 partidas por par):

| Candidato | vs V48 | vs f7_lock |
|---|---:|---:|
| f7_hold (V48 + lockstep + retención) | 1/11 (−337) | 1/11 (−697) |
| f7_holdonly (V48 + retención) | 1/11 (−610) | 1/11 (−1229) |

Retuvo 112-225 unidades por partida y tuvo que forzar 10-63 por capacidad. **Descartada.** La lección:
el precio del líder sale de producir antes, no de retener; la cinta pública no deja capacidad para
hacer mercado.

## 5. Transplante de las grabaciones del líder (Frontier6, sesión anterior)

`build_f6.py` monta las 106 grabaciones de Mother-Goose como biblioteca de rutas del chasis V46 (una por
par de tiendas iniciales, apertura normalizada). Resultado: 6/10 contra V46, f5_lock y pipe-7 (−1948 de
media), 12/4 contra Beyond-48, varianza enorme y una llamada de 2649 ms. Reproduce su economía pero no
su reacción: una cinta abierta de un jugador reactivo no se transfiere. Descartado.

## 6. Conclusión sobre el top 2

Para llegar a 3200 hay que ganar al clúster de clones como lo hace el líder (95 %, +13k), y eso viene de
la economía: fresas y vacas antes (caja a cero hasta el día 10 reinvirtiendo), tomates y zanahorias
tardíos, huevos, doble fertilización, ventas tempranas y constantes. Nada de eso se consigue con una
capa sobre la cinta pública: la cinta fija el calendario de siembra, la mano de obra y el uso del
almacén. Hace falta un planificador propio:

1. Apertura: los seis primeros días del líder son deterministas (contrata 5,4,4,5,4,5; 4 vacas, 2 ovejas,
   12 melones, 4 fresas; tierra el día 6) y pueden reproducirse como cinta de apertura.
2. Días 6-29: planificador diario (siembra, animales, manos, entregas al almacén y ventas) evaluado con
   el simulador C++ (2,5 s por partida) contra clones de V48 y contra las grabaciones del líder.
3. Parte reactiva: imitación a partir de las 299 grabaciones disponibles (Mother-Goose 106, SpaTaro 193).

Es un proyecto de días, no de horas, y el techo que promete es el del líder (3200), no más.

## 7. El candidato que sí sale: Frontier7 = V48 + lockstep (`f7_lock`)

`build_f7.py` fija V48 por hash, enlaza su última función (`_e335_agent`) como punto de entrada y añade
`frontier5_lockstep.py` sin cambios. La primera construcción envolvió el `agent` de V46 que V48 deja
en el módulo y se comportó exactamente como f5_lock (empató 10 de 12 partidas con ella); corregida.
V48 ya trae su propio orden lockstep; el nuestro corre después y aporta aparte.

Pantalla (semillas 5611-5616, motor C++): **11/1 contra V48 (+1124), 11/1 contra f5_lock (+1451),
12/0 contra Beyond-48 (+3288)**.

Holdout (semillas nuevas 5871-5878, 12 rivales, 384 partidas con control V48 emparejado): **16/0 contra
todos**: V48 +922, V46 +1880, f5_lock +1283, Beyond-48 +2614, pipe-7 +2608, pipe-8 +2546, aurax v6
+2978, tetsutani +2976, "2820" +2610, xman +1880, f4_probe +2854, prvsiyan +7679. Diferencia de puntos
emparejada +10 (V48 +8, f5_lock +2), cero errores, latencia máxima 769 ms medida con otra pantalla
corriendo a la vez (68-434 ms en las pantallas aisladas). El evaluador perdió su última escritura
(`OSError` al guardar tras 346 filas); las 38 partidas de control que faltaban se repitieron con el mismo
binario y se fusionaron (nota en `results/frontier7/holdout.json`).

Confirmación oficial (`kaggle-environments` 1.32.7, semillas nuevas 5881-5884, 96 partidas con control
V48 emparejado): **8/0 contra V48 (+861), 8/0 contra Beyond-48 (+1247), 8/0 contra f5_lock (+1054),
6/2 contra pipe-7 (+1600 de media; el control V48 pierde las mismas dos), 8/0 contra prvsiyan y kaito**.
Diferencia emparejada +4, latencia máxima 160 ms, cero errores (`results/frontier7/official_summary.json`).
Las cinco pruebas de `test_frontier7.py` pasan, incluida la comprobación de que la capa envuelve
`_e335_agent` de V48 y no el `agent` de V46.

Verificación en Kaggle (kernel privado `jarturo/kaggriculture-frontier7-v48-lockstep`, versión 1,
semillas 5931-5932, ambos asientos, control V48 emparejado): **4/0 contra V48 (+616), 4/0 contra
Beyond-48 (+752), 4/0 contra f5_lock (+805)**; latencia máxima 236 ms en la CPU de Kaggle, cero errores.
`main.py` y `submission.tar.gz` descargados coinciden byte a byte con el candidato congelado; SHA-256 del
archivo `ec4b691030f4a7227cf4d82b97ee7e544f9dd5675d9ab63e1a80dea21c292c54`
(`results/frontier7/kaggle_verified.json`). Envío autorizado por Arturo el 18 de septiembre ("envia una
plaza"): **submission 56318681** (recibo en `results/frontier7/submission_receipt.json`), una sola plaza;
la otra plaza en seguimiento sigue con Frontier5. El rating de las primeras horas no es el resultado
final. Seguimiento: `python live_report.py 56318681`.

Qué esperar: paridad con la ola pública del 17 de septiembre más ~+1000 en cada espejo contra clones de
V48; es el nivel del clúster de clones actualizado, no el top 10. Se envía solo a petición
(`python submit_frontier7.py --submit --authorization "..."`).

## 8. Límites

El linaje público se renueva a diario (V48 es del 17 a las 22:09 UTC). El orden lockstep gana solo
contra copias. La palanca de mercado está medida y cerrada mientras la cinta ocupe el almacén como lo
hace. El techo real sigue siendo la economía del top 10.
