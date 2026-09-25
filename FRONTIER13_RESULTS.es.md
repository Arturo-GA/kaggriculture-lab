# Frontier13: cha22 + lockstep en las dos plazas — 25 de septiembre de 2026

Petición de Arturo: una nueva tanda de dos envíos con el objetivo de plata al cierre, revisando repositorios públicos
(GitHub, el foro de discusión y el código abierto), con todo lo aprendido.

## 1. Situación

Las dos copias del enrutador Frontier12 (56523438 y 56524328) estaban en 2246 y 2199 tras ~188 partidas; el equipo en
el puesto 995 de 10.017. Cortes: oro 2795, **plata 2427**, bronce 2243.

## 2. Qué se revisó (estudio en paralelo con cinco investigadores y un crítico)

- **Notebooks públicos ejecutados después del cierre** (`vendor/pub0925`, 20 notebooks): los notebooks que ya eran
  públicos se pueden seguir actualizando, y así se publicaron agentes nuevos después del 23 de septiembre. El más
  importante es **cha22** ("route-replay agent"), que aparece idéntico en los notebooks de abhinav0370 (cha22-agent),
  tetsutani (Demand-Preserving, actualizado el 24), guruprasaathas111 (Master Engine V3) y evgendvorkin. Otros:
  haideptry "2965 v7" y Shepherd's Ledger (ya con capas de cha22), Master Engine V4 (= prvsiyan con capas apagadas),
  Harvest Ledger V72, Pioneers candidate 2.
- **Datasets de Kaggle** (`vendor/ds25`, 14 datasets): la arena de agentes comunitarios de destbreso (anterior a
  cha22, con Herd-Safe primero), rivales de kksky9k, bundles y copias de seguridad; 156 agentes, casi todos de linajes
  conocidos o más antiguos.
- **GitHub** (`vendor/gh25`, ~120 repositorios): equipos que documentan su trabajo, como Wangyh666 (v41 = su v37 +
  capas de cha22, 2486 en vivo; mide que el 71 % de sus partidas son contra cha22 y gana ~30 %), mooman0222 (E081,
  Herd-Safe que vende todo al abrir ventana), doanthuan (su round robin pone a cha22 primero con 89 %), Gluzdov
  (repositorio del 16 de septiembre, sin licencia), y agentes RL/PPO/planificadores que no se acercan a la familia
  pública (pierden por 3.000-67.000). El repositorio de Gluzdov y la mayoría de repos no tienen licencia: solo se
  usan como rivales locales.
- **Foro**: el ranking final usa todas las partidas entre submissions activas al final; cada envío nuevo retira la
  más antigua; el emparejamiento se ha ralentizado a 1-2 partidas por hora desde el 23 (la convergencia tarda más de
  un día); hay que ganar también durante la subida (familias a1-t31, hack, utils-v1, shop-router v7); vender pronto
  gana a vender con paciencia; y la publicación tras el cierre por actualización de notebooks está denunciada y el
  staff la está revisando.
- **Derrotas en vivo** (172 replays de partidas contra rivales de 2300+, `vendor/live_f12`): el grupo mayor abre
  con BUY 5 trigo / 1 semilla y nos ganó **61 de 67**; ALLAI (2583) reproduce cha22 en el 99,8 % de 432 pasos; 33
  equipos juegan copias exactas de cha22 (mediana 2413 entre los de 2300+). Contra envíos rivales posteriores al 24
  el enrutador iba 19-123. Jugamos igual que ellos hasta el paso ~432 y perdemos en el final (+1.096 de diferencia al
  cierre): cha22 convierte mejor el final de temporada.

## 3. cha22 contra todo lo que teníamos

Semillas 9111-9114 (asiento 0), 15 rivales fuertes: **cha22 sin tocar 56/56** (+200 a +4.500 por partida), **cha22 +
nuestro lockstep 60/60** (4/4 contra cha22, +82 a +144), nuestro enrutador 36,5/56 (0/4 contra cha22, −1.791 a
−4.024).

## 4. Candidato y aceptación

`candidates/f13_c22_lock.py` = cha22 (hash `127ed3e6…`, Apache-2.0, avisos íntegros) + `frontier5_lockstep.py` sin
cambios, enlazado al punto de entrada público `ig_agent` (`build_f13.py`). Hash `831952068d102bfefe413091b6cc2aa0b6fbe7cc0b870ab2dfe139be2b861d8a` (ver
`results/frontier13/build.json`).

Puerta registrada antes de correr (`results/frontier13/plan.json`): control emparejado = cha22 sin tocar; total
emparejado ≥ +6, espejo ≥ 70 %, ningún rival por debajo de −2, sin errores, < 1000 ms. Panel de 16 rivales: la cima
posterior al cierre, las diez mejores de antes y las cuatro familias débiles de la subida.

Holdout (semillas nuevas 9141-9148, 768 partidas): **251/256 frente a 234/256 (+14 empates) de cha22; emparejado +11,
espejo 15/16, +54 monedas por partida, 507 ms, sin errores. Puerta superada.**

| Rival (16 partidas) | cha22 + lockstep | cha22 sin tocar |
|---|---:|---:|
| cha22 (espejo) | **15/16** | 1 victoria, 14 empates |
| Nuestro enrutador y Herd-Safe+lockstep | **16/16** | 14/16 |
| prvsiyan y Master Engine V4 | 14/16 | 14/16 |
| Herd-Safe (4), haideptry v7, Shepherd's Ledger, statma | 16/16 | 16/16 |
| a1-t31 (2 versiones), hack, V43, shop-router v7 | 16/16 (+1.700 a +5.400) | 16/16 |

La variante de nivel 2 sobre la capa D (`f13x_c22_br`) hizo 245/256 (+5) y no se exporta.

**Repetición de las 172 partidas en vivo con rival congelado** (`outputs/session/gold/panel_f13_live.json`): de 166
válidas, 29 victorias registradas → **99** con cha22 + lockstep (74 derrotas pasan a victoria, 4 al revés). Por franja
de rival: 2300-2400 9→42 de 57; 2400-2500 10→36 de 60; 2500-2600 6→17 de 32; 2600+ 4→4 de 17. Contra copias de cha22
4→36 de 56. El rival congelado no reacciona: es una estimación optimista.

Kaggle (kernel privado `jarturo/kaggriculture-frontier13-cha22`, semillas 9151-9154): **8/0 contra cha22 (+192), 6/2
contra prvsiyan y 6/2 contra haideptry v7**, 176 ms, sin errores; archivo
`475e416302c39880d41abc3005b318551df44672cd75888340e8e18aaf213a72` (`results/frontier13/kaggle_verified.json`).

## 5. Envío

**Enviado el 25 de septiembre de 2026 a las 21:26 UTC a petición de Arturo** ("puedes tener una nueva tanda de 2
envios para la competencia? el objetivo es plata al cierre revisa repositorios publicos"): el mismo archivo a las
dos plazas, **submissions 56560449 y 56560450** (recibos en `results/frontier13/submission_receipt.json` y
`submission_receipt_2.json`), validadas por Kaggle y arrancando en 600. Retiraron las dos copias del enrutador. Dos
copias del mismo agente: es el más fuerte que hemos validado con diferencia, y dos trayectorias de rating
independientes protegen contra la dependencia del camino que describe el foro (el mismo agente puede quedar a 300
puntos de su copia por una derrota temprana).

**Prueba complementaria tras el envío** (semillas 9161-9164, asiento 0, 16 rivales que el crítico señaló como relevantes
en vivo y que no estaban en el holdout; `outputs/session/gold/supp_f13_0925.json`): **cha22 + lockstep 60/64, cha22 sin
tocar 58/64.** 4/4 contra los agentes de equipos de GitHub de Wangyh666 v37/v41 (v41 en vivo ~2486), Harvest Ledger
V68 de doanthuan, Gluzdov mwss/shock, Pioneers, koshinm, wzhengbiao, Tschinkel, Metav4 y las familias viejas.
**Puntos flojos**: mooman0222 E081 (3/4; Herd-Safe que vende todo el almacén de leche/lana/fresa al abrir cada ventana
de demanda) y E082 (2/4), y Wangyh666 v44 (3/4; v41 con `_ADV_LOOK` 6). En los tres el lockstep iguala o mejora a cha22.

## 6. Qué esperar

- La estimación con rival congelado da ~50 % en la franja 2500-2600, es decir un nivel alrededor de 2500, por encima
  del corte de plata (2427). Contra los agentes privados de 2600+ no hay mejora.
- El emparejamiento va lento (1-2 partidas por hora): el rating tardará más de un día en asentarse.
- Riesgo: si Kaggle revierte las actualizaciones de notebooks posteriores al cierre, la población de cha22 no
  desaparece del ladder (ya está enviada); si aparecen más actualizaciones, habrá que revisarlas antes del 30.
