# Frontier5: qué hace el resto y cómo respondemos — 17 de septiembre de 2026

## Dónde estamos y contra quién perdemos

Leaderboard del 17 de septiembre (02:03 UTC): 9282 equipos; cortes oro 2925 (29 equipos), plata 2662
(464), bronce 2429. Nuestra fila: puesto 437, 2674, con las dos Frontier4 activas. Ambas empezaron
50/60 y 54/60 y cayeron a 6/16 y 26/60 en sus últimas partidas; contra rivales de 2700-2900 pierden
(19/35 y 15/28 la primera; 19/18 y 4/13 la segunda).

Auditamos 38 replays recientes contra rivales de 2700 o más (`outputs/session/live/audit_f4_live.json`,
fuera de Git; el bot desplegado reproduce sus 719 acciones en todos). Tres causas, en este orden:

1. **Microestructura del turno 0-1 (la mayoría).** El rival abre con un viaje de ida y vuelta de trigo
   de 15, 20, 45 o 50 unidades, con `BUY 43 / SELL 4x`, con `BUY 7 / SELL 2` (V46) o con `BUY 13`.
   Por la liquidación por índice del motor, nuestro `BUY 70 / SELL 70` de V45 queda cotizado peor:
   perdemos 50-90 monedas en el turno 1 y una o dos semillas de melón. La brecha es de −1300 a −1600
   en el turno 288 y la partida, que es un espejo, termina en −1100 a −1900. Catorce de las derrotas
   auditadas siguen exactamente este patrón (viajes 15-50: 0 victorias, 9 derrotas).
2. **Espejos V45 (70/70)**: 3/5, decididos por la carrera de ventas del mismo turno.
3. **Economías distintas del top 10**: SpaTaro (#4) nos gana −4433 pese a que íbamos +7344 en el
   turno 288.

## Qué hace el top

**Las plazas 12-40 son clones de nuestra propia cinta.** Con el dataset comunitario de partidas
(georgymamarin, `vendor/episodes_ds`, fuera de Git) las huellas de sus últimas submissions coinciden
con la nuestra: 11-15 manos, tierra el día 6, 239 baldosas plantadas, 163 trigo / 33 fresa / 12 melón
/ 31 zanahoria. Driz Lo (#12), Thomas Tschinkel (#15), mikelou1 (#18), yfy (#25), Hamed Vakili (#28),
yjshyfy, Leifson1337: idénticos a `f4_probe` hasta la última baldosa. Su rating de 2900-2990 viene de
la ola pública del 15-16 de septiembre:

| Notebook público | Idea | Resultado declarado |
|---|---|---|
| Pipe-7 (Nathan Jacob, 60 votos) | viaje de trigo 70 → 5 | 197-3 vs V45 |
| Pipe-8 (Nathan Jacob) | sin viaje: `BUY 5` en el turno 0 y contratar/comprar animales en el 1 | 191-9 vs pipe-7 |
| Beyond 48-0 (sdy623, 35 votos) | ventas al frente de la lista de órdenes, adelanto de 2 turnos, horizonte 24, viaje de 50 | 128-0 vs V45 |
| V46 (Ahmed Berat Özer) | `BUY 7 / SELL 2` en el turno 0, ataque de 30 trigos en el índice 0 del turno 1, adelanto de 3 turnos, ventas primero, horizonte de un día contra clones | 58/6 vs V45, 52/12 vs Beyond-48, 53/11 vs pipe-7, 51/13 vs pipe-8 |
| "2820" (Seyit Kaan Güneş) | V44 + preguardia nocturna, orden lockstep contra copia, cadencia de ventas, rebaño de lana con tienda de hilo | 2801 en vivo |

Medido en nuestro simulador (12 partidas por par, semillas 5601-5606): **V46 gana 11/1 a cada uno**
(aurax v6 +921, Beyond-48 +393, pipe-7 +481, pipe-8 +684, tetsutani +846, V45 +921) y f4_probe
pierde 1/11 contra V46 y 0/12 contra Beyond-48. La base tiene que ser V46.

**El top 2-10 sí es distinto.** SpaTaro (#4) contrata 4-6 manos en el turno 1 y compra melones,
vacas y ovejas de inmediato; mantiene la caja cerca de cero hasta el día 10 reinvirtiendo, compra la
segunda tierra el día 10 y llega al día 12 con 9 vacas, 10 ovejas y 28 fresas (nosotros 6/11/33); entre
los días 12 y 21 gana 61k frente a nuestros 48k. Unknown Mother-Goose (#6): 10 vacas y 38 fresas.
DSM (#2), Sida Zuo (#3) y Planned Economy (#19) plantan muchas más zanahorias y tomates en la fase
tardía (120-139 zanahorias frente a nuestras 31; Sida Zuo comparte nuestra cinta hasta el día 20 y
diverge después). Son estrategias de cinta propia; replicarlas exige clonar sus replays (Sida Zuo tiene
373 partidas públicas), un proyecto aparte.

## Lo que la economía del espejo dice (56 replays)

| Producto | Tiendas al final | Precio medio días 14 / 20 / 26 / 29 |
|---|---:|---|
| Lana | 0 (18 partidas) | 99 / 1 / 1 / 1 |
| Lana | 1 | 153 / 84 / 67 / 58 |
| Lana | 2 | 193 / 155 / 126 / 152 |
| Leche | 1 | 55 / 7 / 6 / 3 |
| Leche | 2 | 104 / 32 / 20 / 12 |
| Leche | 3 | 158 / 59 / 48 / 46 |
| Huevo | cualquiera | 51-55 / 51-56 / 52-57 / 53-59 |
| Fresa | — | 191 / 119 / 66 / 61 |

En un espejo los dos granjeros saturan leche, lana y fresa; solo el huevo (curva logarítmica) y el
trigo aguantan. Sin tienda de hilo compramos 3,7 ovejas después del día 5 y vendemos 70 lanas por 600
monedas en total. Probamos la sustitución "gansos en vez de vacas y ovejas tardías" (`frontier5_geese.py`):
mecánicamente correcta (8 compras convertidas, 7 colocadas, 160 huevos vendidos) pero **negativa** en 6
de 8 mundos (hasta −33k cuando la tienda de hilo aparece en el cuarto sorteo): la cinta cosecha los
sitios convertidos cada 2-3 días y sin cuidado extra un ganso rinde un huevo al día, y ovejas y vacas
son opciones sobre tiendas futuras. Descartada y documentada.

## El candidato: f5_lock

`build_f5.py` fija el V46 público por hash. Se probaron dos capas propias:

- **Orden lockstep de ventas** (`frontier5_lockstep.py`). El motor liquida las órdenes por índice y
  cotiza cada unidad de ambos jugadores al mismo inventario. Cuando la granja rival es una copia
  (similitud pública ≥ 0,90 desde el turno 144), asumimos que su lista de mercado es la que produjo
  nuestro propio padre, reproducimos la liquidación unidad a unidad con la función de precio exacta
  del motor para cada permutación de nuestras órdenes SELL (mismas casillas, cantidades y productos) y
  conservamos la de mejor margen modelado, si mejora al menos 3 monedas. No añade, quita ni cambia
  cantidades. En los espejos contra V46 la ganancia modelada coincide con el margen real (717 → +700,
  980 → +964, 869 → +869). Máximo medido: 32 ms por llamada en local.
- **Capas terminales de Frontier4** (`frontier4_layers.py`): planificador del último día, entregas en
  ruta y asignación de capacidad.

Selección (semillas 5741-5748, 16 partidas por par, motor C++):

| Candidato | vs V46 | vs Beyond-48 | vs pipe-7 |
|---|---:|---:|---:|
| f5_term (V46 + capas terminales) | 13/3 (+380) | 15/1 (+616) | 15/1 (+917) |
| f5_lock (V46 + lockstep) | 15/1 (+659) | 15/1 (+978) | 15/1 (+779) |
| **f5_lockterm** | **15/1 (+1050)** | **15/1 (+1227)** | **15/1 (+1159)** |

La única derrota de cada uno es la semilla 5748 en el asiento 0, un mundo asimétrico (el asiento 1
gana +12k).

`f5_lockterm` se congeló primero y pasó el holdout C++ (semillas 5761-5768, 12 rivales: 16/0 contra
todos, V46 +1317) y el motor oficial (5821-5824: 8/0 contra cinco rivales, 6/2 contra V46). Pero
la reproducción de su derrota oficial en 5821 muestra que las capas terminales pierden el último día
por 4150 monedas (+1455 en el amanecer del día 29 → −2698 al final; `f5_term` −3770), mientras que
`f5_lock` gana +1076 en el mismo mundo: el planificador terminal propio, validado sobre V37, no es
fiable sobre el cierre de V46 en el motor oficial, y el simulador C++ no lo detecta. Además apareció
una excepción capturada en el turno 718 (almacén proyectado nulo), corregida con una guarda. **Se
exporta `f5_lock`: V46 + orden lockstep, sin capas terminales.** Hash congelado en
`results/frontier5/selection.json`.

## Aceptación de f5_lock

Holdout (motor C++, semillas nuevas 5771-5778, 12 rivales, 384 partidas con control V46 emparejado):
**16/0 contra todos**: V46 +1083, Beyond-48 +1202, pipe-7 +940, pipe-8 +1448, aurax v6 +1152,
tetsutani +1075, V45 +1152, f4_probe +1543, prvsiyan +6936, router +7288, kaito +34264, nagata
+103805. Diferencia de puntos emparejada +26, sin errores. `results/frontier5/holdout_summary.json`.

Confirmación oficial (`kaggle-environments` 1.32.7, semillas nuevas 5831-5834, 96 partidas): **8/0
contra los seis rivales**: V46 +965, Beyond-48 +968, pipe-7 +1708, f4_probe +1267, prvsiyan +11102,
kaito +33348. Diferencia emparejada +8, latencia máxima 216 ms, cero errores.
`results/frontier5/official_summary.json`. Las seis pruebas de `test_frontier5.py` pasan, incluida
la comprobación del modelo lockstep contra la función de precio del motor.

Verificación en Kaggle (kernel privado `jarturo/kaggriculture-frontier5-lockstep`, versión 1,
semillas 5921-5922, ambos asientos, control V46): 4/0 contra V46 (+1195), 4/0 contra Beyond-48
(+1020), 4/0 contra Frontier4 (+1208); latencia máxima 292 ms en la CPU de Kaggle, cero errores.
`main.py` y `submission.tar.gz` descargados coinciden byte a byte con el candidato congelado;
SHA-256 del archivo `3d80ca6e070fcdc2b12a8765457a4c0c5e04491bb6ffd60918ba19e5170b1398`
(`results/frontier5/kaggle_verified.json`). No se ha enviado al leaderboard: `python submit_frontier5.py --submit`
solo con petición explícita; sustituiría a la Frontier4 más antigua (56266564).

Qué esperar: paridad con el V46 público más un margen sistemático de ~+1000 en cada espejo contra
clones de V46 y de la ola anterior. Eso apunta al nivel del clúster de clones actualizado (2900-3000
en la tabla del 17 de septiembre, corte de oro 2925), no al top 10, y durará lo que tarde la siguiente
versión pública. El siguiente salto exige clonar una cinta propia del top 10 sobre este chasis.

## Límites

La ola pública se renueva a diario (V46 es del 16 de septiembre a las 22:04 UTC); la paridad con ella
dura lo que tarde el siguiente notebook. El orden lockstep gana solo contra copias; contra rivales con
otra cinta es neutro. El techo real sigue siendo la economía del top 10, que no comparte nuestra cinta.
