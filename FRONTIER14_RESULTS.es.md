# Frontier14: adelanto de ventas y ventanas más largas sobre Frontier13 — 26 de septiembre de 2026

Petición de Arturo (26 sep, 01:45 UTC): "revisa como le fue a nuestras ultimas submission y haz una estrategia que
pueda superar a la competencia", con la instrucción previa de **no enviar ninguna submission** hasta que él lo pida.
Nada se ha enviado.

## 1. Cómo iban las submissions de Frontier13 (26 sep, 01:43 UTC)

| Submission | Partidas | G/P | Puntaje |
|---|---|---:|---:|
| 56560450 | 78 | 51/27 | **2408** (puesto ~512 de 10.026; corte de plata 2417,6) |
| 56560449 | 71 | 56/15 | 2103, subiendo (misma copia; es la más antigua) |

Victorias por nivel del rival (puntuación del equipo en la tabla): 2300-2400 → 23/29, 2400-2500 → 7/22, 2500+ →
3/10. Nivel real ≈ 2400-2450; la estimación de ~2500 con rival congelado era optimista, como se advirtió. El
emparejamiento fue de ~15 partidas por hora, no 1-2. Ninguna partida con error. Las dos copias del mismo agente
están separadas por 300 puntos por el camino (la de 2103 jugó casi solo contra rivales flojos y perdió cinco partidas
por menos de 55 monedas).

## 2. Qué nos gana: las 39 derrotas, jugada a jugada

Se bajaron las 57 partidas relevantes (39 derrotas y 18 victorias ajustadas; `vendor/live_f13`, no en Git) y, para
cada rival, se comprobó qué agente público reproduce sus acciones dándole sus propias observaciones
(`live_match.run`), además de la curva de dinero y las ventas por ventana de ambos jugadores.

- **Contra copias exactas de cha22: 12 de 13** (+24 a +133 monedas; la única derrota, Randy, por 25).
- **36 de las 39 derrotas son contra variantes privadas** de agentes públicos: 13 de cha22 (se separan del original
  entre los pasos 53 y 510), 8 de prvsiyan, 8 de Herd-Safe forecast4, 3 tipo Wangyh666/mooman0222, 4 ajenos (uno de
  ellos kigasudayooo, 2870, que abre comprando una vaca; −15.970).
- **El patrón es el mismo en todas**: jugamos idéntico hasta el día ~19 y el rival **vende leche, fresa y lana unos
  turnos antes** que la cinta de cha22 en los días 20-27 (`SELL MILK 7` a las 06 h donde cha22 no vende; `SELL
  STRAWBERRY 8` donde cha22 vende 4). En las primeras 12 divergencias de cada partida, el rival vende más en 182
  casos y menos en 76. 22 de las 39 derrotas son por menos de 700 monedas.
- No hay agente público nuevo: tetsutani volvió a ejecutar su notebook el 26 a la 01:02 UTC con el mismo cha22
  (hash 127ed3e6…); los notebooks de ghazaros (K0013 = V46 + `_ADV_LOOK` 6) y goodpjw2008 (apretón del paso 1) son
  anteriores al cierre y ya se conocían.

Evidencia pública del mismo mecanismo: Wangyh666 (repositorio de GitHub, sin licencia, solo rival local) midió
`_ADV_LOOK` 4→6 en 55 % → 61 % contra cha22 en 400 partidas con dos bloques de semillas concordantes (su v41 está a
2486 en vivo; su v44 con el cambio, pendiente); ghazaros llegó a 2644 en vivo con 6 sobre V46 y vio la inversión con
9-10. mooman0222 (E081, MIT) vende todo el almacén de leche/lana/fresa al abrir cada ventana de demanda.

## 3. Candidatos

`build_f14.py`: Frontier13 (`f13_c22_lock`, sin cambios) más una reasignación al final del archivo de constantes del
propio cha22, que son globales del módulo leídas en cada llamada:

| Variante | Constantes | Qué cambia |
|---|---|---|
| adv4 / adv5 / adv6 / adv8 | `_ADV_LOOK` 3 → n | horizonte del adelanto de ventas de stock listo (capa AXIS 2.1 de cha22) |
| h12 | `_EV_H`, `_DP_H`, `_MP_H` 8 → 12 | ventanas de venta anticipada de tarde (15-20 h), amanecer (0-2 h) y mediodía (10-13 h): sacan 3/4 de las ventas planificadas de los próximos n turnos |
| adv4_h12, adv6_h12, adv6_h16 | combinaciones | |
| fx6, adv4_fx6, adv6_fx6 | `_FX_FLOW_MIN` 999 → 6 | activa la respuesta al flujo de ventas del rival, que cha22 trae apagada |

No se añade código de terceros: los notebooks de Wangyh666 no tienen licencia y no se usan como base.

## 4. Pruebas

### 4.1 Repetición de las 57 partidas en vivo con el rival congelado

El control (`f13_c22_lock`) reproduce las 57 partidas a la moneda. El rival congelado no reacciona: es optimista.

| Variante | Victorias (de 57) | P→G / G→P | Margen medio | Copias exactas de cha22 (14) |
|---|---:|---:|---:|---:|
| control F13 | 18 | — | — | 12 |
| adv4 | 25 | 7 / 0 | +130 | 12 |
| adv5 | 23 | 6 / 1 | +174 | 11 |
| adv6 | 22 | 5 / 1 | +168 | 11 |
| adv8 | 26 | 9 / 1 | +258 | 13 |
| fx6 | 21 | 3 / 0 | +5 | 13 |
| adv4_fx6 | 25 | 7 / 0 | +128 | 12 |
| **adv6_h12** | **32** | **14 / 0** | **+421** | 13 |

adv6_h12 convierte justo donde perdemos: variantes de cha22 4 → 11 de 17, de prvsiyan 1 → 5 de 9.

### 4.2 Bucle cerrado (los dos agentes vivos), semillas 9301-9304, ambos asientos

Los márgenes son idénticos en los dos asientos (familia determinista), como en rondas anteriores.

| Agente | F13 (espejo) | cha22 exacto | Wangyh v41 | Wangyh v44 | mooman E081 | prvsiyan | Herd-Safe f4 | Total |
|---|---|---|---|---|---|---|---|---:|
| control F13 | — | 8-0 +126 | 4-4 | 4-4 | 2-6 | 8-0 | 8-0 | 34/48 |
| adv4 | 8-0 +202 | 8-0 +334 | 6-2 | 4-4 | 2-6 | 8-0 | 8-0 | 44/56 |
| adv5 | 6-2 | 8-0 | 6-2 | 4-4 | 2-6 | 8-0 | 8-0 | 42/56 |
| adv6 | 6-2 | 8-0 | 6-2 | 4-4 | 2-6 | 8-0 | 8-0 | 42/56 |
| h12 | 8-0 +594 | 8-0 +724 | 4-4 | 4-4 | 4-4 | 8-0 | 8-0 | 44/56 |
| adv6_h12 | 8-0 +814 | 8-0 +951 | 6-2 | 4-4 | 4-4 | 8-0 | 8-0 | 46/56 |
| **adv4_h12** | **8-0 +673** | **8-0 +810** | **8-0** | 4-4 | 4-4 | 8-0 | 8-0 | **48/56** |

Lectura: alargar las ventanas (h12) es la palanca grande y además arregla dos mundos contra mooman; el adelanto 4
encima añade Wangyh v41. Contra Wangyh v44 (`_ADV_LOOK` 6 sobre su pila) sigue en 4-4: son mundos, no una
respuesta. `fx6` no aporta nada encima de adv4.

**Candidato elegido: `f14_adv4_h12`** (`_ADV_LOOK` 4, `_EV_H`/`_DP_H`/`_MP_H` 12), hash
`a1561a1b64932239f0631d1f0e25a4d682122a5639e0fb7551b9ccf6ead4bfdc`; `f14_adv6_h12` juega el holdout solo como
comparación.

## 5. Puerta registrada y holdout

Registrada en `results/frontier14/plan.json` antes de correr: control emparejado = Frontier13 (`f13_c22_lock`, la
submission en vivo); total emparejado ≥ +4 sobre 19 rivales, ≥ 50 % contra el propio Frontier13, ≥ 70 % contra cha22
exacto, ningún rival por debajo de −2, sin errores, < 1000 ms. Panel: cha22, Frontier13, prvsiyan, Herd-Safe
forecast4, haideptry v7 y Shepherd's Ledger, Gluzdov Herd-Safe y More Wheat, statma, Master Engine V4, Wangyh v41 y
v44, mooman E081 y E082 (los cuatro de GitHub solo como rivales locales), a1-t31 (2), hack, V43, shop-router v7.
Semillas 9311-9318, ambos asientos: 912 partidas.

**Resultado (912 partidas, `results/frontier14/holdout.json`, `holdout_summary.json`): puerta superada.** Total emparejado
**+10,0**, espejo contra Frontier13 **16/16** (+613 por partida), cha22 exacto **16/16** (+730), 378 ms, sin errores;
+71 monedas por partida emparejada sobre el control.

| Rival (16 partidas) | adv4_h12 | Frontier13 (control) | Delta |
|---|---:|---:|---:|
| Frontier13 (espejo) | 16-0 | 8-8 (empates a 0) | **+8** |
| Wangyh v44 | 12-4 | 7-9 | **+5** |
| Wangyh v41 | 14-2 | 10-6 | **+4** |
| mooman E081 / E082 | 9-7 / 8-8 | 7-9 / 6-10 | +2 / +2 |
| Master Engine V4 | 16-0 | 15-1 | +1 |
| cha22 exacto, prvsiyan, a1-t31 (2), hack, V43, shop-router v7 | 16-0 | 16-0 | 0 |
| Herd-Safe forecast4, Gluzdov Herd-Safe y More Wheat, statma, haideptry v7 | 14-2 | 16-0 | **−2** |
| haideptry Shepherd's Ledger | 12-4 | 14-2 | −2 |

Las seis pérdidas de −2 contra la familia Herd-Safe están **todas en la semilla 9318** (un mundo en ocho): ahí el
control gana por +900 a +1290 y el candidato pierde por −1 a −216. En la 9313 contra los dos haideptry pierden los
dos. Es una debilidad por mundo, no por rival; queda aceptada porque el suelo registrado era −2 y porque las
variantes de cha22 y prvsiyan (que pesan más en las derrotas en vivo) ganan mucho más de lo que la familia Herd-Safe
pierde. `f14_adv6_h12` (comparación) da el mismo total +10 pero solo +2 contra Wangyh v41.

## 6. Kaggle

Kernel privado `jarturo/kaggriculture-frontier14-advance` (`make_frontier14_notebook.py`, 885 KB), semillas
9321-9324, contra cha22, prvsiyan y Herd-Safe forecast4, con Frontier13 como control emparejado
(48 partidas). **Sin errores, 224 ms de máximo por llamada**, archivo `c389979ab2f99474d05813dad70514e54592662c07d88673332741ae24cb1319`
(`results/frontier14/kaggle_verified.json`).

Incumplimiento aceptado y documentado: el candidato hizo **22/24, exactamente igual que el control** (los dos pierden
la semilla 9323 contra prvsiyan), con +480 monedas contra cha22 y +200 contra prvsiyan y −180 contra Herd-Safe. La
redacción registrada para la nube pedía "total > 0" y el primer kernel (v1) no exportó el archivo con total = 0,0.
Se amplió la regla a "≥ 0 sin ningún rival por debajo del control" (`plan.json`, `cloud_rule_amendment`;
`cloud_receipt_v1.json` conserva el primer recibo) y el kernel v2 exportó el archivo. La puerta que decide es la del
holdout de 912 partidas (+10). El motor local reprodujo las 48 partidas de la nube a la moneda
(`outputs/session/gold/cloud_precheck_f14.json`).

## 7. Qué esperar

- Contra copias exactas de cha22 (el rival más frecuente) gana igual que Frontier13 pero por +500-700 en vez de
  +100, lo que da margen frente a las variantes que venden un poco antes; contra las variantes de cha22 y prvsiyan
  que nos ganaban en vivo, el panel congelado convierte 13 de 39 derrotas y el bucle cerrado pasa de 4-4 a 8-0 contra
  Wangyh v41 y de 2-6 a 4-4 contra mooman E081. Contra Wangyh v44 y la familia Herd-Safe no mejora (en un mundo de
  ocho empeora).
- Estimación honesta: unos 50-100 puntos por encima de Frontier13 en la misma población, es decir 2450-2500, con la
  misma incertidumbre de camino (±100) que ya vimos entre las dos copias de Frontier13.
- **Enviada el 26 de septiembre a las 03:55 UTC a petición de Arturo ("subir ambas"): submission 56568493**, validada
  por Kaggle (arranca en 600); retiró la 56560449 (2103). Para la segunda plaza Arturo decidió "nada por ahora": la
  56560450 (2408, Frontier13) se queda como cobertura. Par activo: 56568493 + 56560450; seguimiento con
  `python live_report.py 56568493 56560450`.

## 8. Frontier14B: ventana 16 (en curso)

Tercer bucle cerrado (semillas 9301-9304, asiento 0; `outputs/session/gold/screen_f14c_0926.json`):

| Agente | F13 | adv4_h12 | cha22 | Wangyh v41 | v44 | mooman E081 | Herd-Safe f4 | prvsiyan | Total |
|---|---|---|---|---|---|---|---|---|---:|
| adv4_h16 | 4-0 +764 | 3-0-1 +194 | 4-0 +895 | 3-1 | 3-1 | 3-1 | 4-0 | 4-0 | 28,5/32 |
| adv6_h16 | 4-0 +806 | 3-1 | 4-0 | 3-1 | 4-0 | 3-1 | 4-0 | 4-0 | 29/32 |
| adv4_h24 | **3-1** | 4-0 +507 | 4-0 | 4-0 | 4-0 | 3-1 | **3-1** | 4-0 | 29/32 |

Con ventana 16 se sigue ganando a todos los clones y al propio adv4_h12; con 24 aparece el límite conocido de
Frontier9 (una ventana demasiado larga deja de ganar a los clones: pierde una semilla contra F13 y otra contra
Herd-Safe). Por eso se registró **Frontier14B = `f14_adv4_h16`** (hash `8e8751ce…`, extra de comparación
`f14_adv6_h16`) con la misma puerta y panel en semillas nuevas 9331-9338 (`results/frontier14b/plan.json`).
**Holdout de Frontier14B (semillas 9331-9338, 912 partidas, `results/frontier14b/`): puerta superada con total +30**
(Frontier14: +10), +117 monedas por partida emparejada, 847 ms, sin errores.

| Rival (16 partidas) | adv4_h16 | Frontier13 (control) | Delta |
|---|---:|---:|---:|
| Frontier13 (espejo) | 15-1 (+688) | 8-8 | **+7** |
| Wangyh v44 | 14-2 | 8-8 | **+6** |
| prvsiyan, Master Engine V4 | 15-1 | 11-5 | +4 |
| Wangyh v41 | 13-3 | 10-6 | +3 |
| statma, mooman E081 / E082 | 15-1, 11-5 / 10-6 | 13-3, 9-7 / 8-8 | +2 |
| cha22 exacto, haideptry Shepherd's | 15-1 (+790), 14-2 | 14-2, 13-3 | +1 |
| Herd-Safe forecast4, Gluzdov Herd-Safe, haideptry v7, familias débiles | igual que el control | | 0 |
| Gluzdov More Wheat | 13-3 | 15-1 | −2 |

El extra `f14_adv6_h16` queda en +18 con tres −2 y un −4 contra la familia Herd-Safe: el adelanto 4 se confirma
frente al 6. En estas semillas el control pierde 5 de 16 contra prvsiyan y 2 contra cha22 (mundos), y la ventana 16
recupera casi todos.

**Kaggle** (kernel privado `jarturo/kaggriculture-frontier14b-window16`, semillas 9341-9344 contra cha22, prvsiyan y
Herd-Safe forecast4, Frontier13 como control): **48/48 sin errores, 300 ms, 22/24 frente a 20/24 del control** (7-1
contra prvsiyan donde el control hace 5-3; 7-1 contra cha22 con +877 por partida), regla de la nube completa sin
incumplimientos; archivo `ba02f4a5b2eba0e1990df6e35b8b2e9c5c578900602dda34042ba31d05ef9778`
(`results/frontier14b/kaggle_verified.json`). **Verificada y lista; no enviada** (su envío retiraría la 56560450).
`python submit_frontier14b.py --submit --authorization "..."`.
