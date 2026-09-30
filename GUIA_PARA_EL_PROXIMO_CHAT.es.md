# Guía de traspaso para el próximo chat — Kaggriculture (estado al 25 de septiembre de 2026, ~21:40 UTC)

<!-- frontier20-current -->
**30 de septiembre, Frontier20: una submission privada, 56719762, PENDING.** Se reconstruyeron las 23 derrotas públicas disponibles de las dos submissions anteriores. La nueva capa completa pequeñas ventas cubiertas y prioriza lana solo si el riesgo de precio supera el fertilizante. Se envió por petición explícita como experimento con controles pendientes, después de 149V/11D/0E en 160 juegos de la candidata. Los controles comparativos siguen pendientes. La primera candidata falló y se conserva su resultado. Kaggle completó 16 juegos de verificación y confirmó el paquete idéntico. Par activo confirmado a 2026-09-30T22:03:25.886816+00:00: 56714342 + 56714336. Segunda plaza condicionada a demostrar una mejora después de los controles. [Resultados y recibos](results/frontier20/final_report.json), [investigación](results/frontier20/research_summary.json), [código](candidates/f20_value.py), [notebook privado](https://www.kaggle.com/code/jarturo/kaggriculture-frontier20-policy-validation). La mejora local no garantiza puesto ni medalla; no se verificó una victoria contra Grigor.
<!-- /frontier20-current -->

**30 de septiembre: Frontier19, submissions 56714342 y 56714336.** Cuatro partidas por cada equipo del puesto 200–300, veinte contabilidades propias exactas, 544 juegos de comparación y dos estrategias verificadas funcionalmente en un notebook privado. Market2 pasa su puerta; Market1 es una segunda plaza experimental con un retroceso documentado. [Resultados](FRONTIER19_RESULTS.es.md) y [estado para continuar](RESUME_FRONTIER19.es.md). La mejora local no garantiza top 300.

Los estados anteriores que siguen son históricos.

> **Actualización más reciente: Frontier18, 27/09, submission 56617687.** Leer
> [RESUME_FRONTIER18.es.md](RESUME_FRONTIER18.es.md). Censo de cuatro partidas por equipo:
> 400 actuaciones en 336 partidas, cuatro reconstrucciones exactas del líder y un fallo
> de alimentación demostrado en F17. Solo `f18_small` superó su puerta principal: 94/96,
> 16/16 contra F17 y +4 fuera de ese duelo. Kaggle confirmó 8/8 y paquete idéntico, privado.
> Se realizó un solo envío de las dos plazas autorizadas **si mejoran**; las otras variantes
> no pasaron. Consultar recibos antes de actuar. Los apartados siguientes son históricos.

> **Investigación más reciente: top 100 completo (27/09).** Leer [TOP100_ESTRATEGIAS.es.md](TOP100_ESTRATEGIAS.es.md).
> 184 partidas, 200 actuaciones de los 100 equipos, 11 reconstrucciones exactas y cuatro partidas de F17.
> La mediana actual es 11 trabajadores; SE aparece en 52/200 actuaciones. Corrige las generalizaciones del
> informe anterior sobre expandir siempre a cuatro cuadrantes con 12–13 trabajadores. Se proponen previsión
> por ciclo y escenarios de resiembra, rotación en casillas existentes y tercer cuadrante más temprano.
> Los componentes heredados `_cxtb_their_supply`, `_cxtb_expected_revenue` y `_v9_carrot` ya cubren parte de ello;
> distinguir mejoras nuevas de funciones existentes. Esta ronda investigó, no construyó ni envió F18.
> F17 `56615489` está COMPLETE y acompaña a F16 `56609913`; F15 ya no figura en la lista activa.

> **Última actualización: Frontier17 enviado (27/09), submission 56615489.** Leer primero
> [RESUME_FRONTIER17.es.md](RESUME_FRONTIER17.es.md). Se analizaron 22 derrotas de F16;
> el nuevo candidato ganó 128/128 en la validación principal y pasó la prueba adicional.
> Arturo autorizó «Y lanza una plaza a kaggle» y se realizó exactamente un envío.
> Notebook privado, versión 1; Kaggle validó 16 partidas, F17 8/8 contra F16, cero errores y máximo 248 ms.
> El paquete coincide byte por byte con el local. Revisar `results/frontier17/submission_receipt.json`
> y `active_after_submission.json` antes de cualquier acción; no duplicar el envío.
> El objetivo solicitado es mejorar hacia el top 100. Persisten derrotas contra economías privadas distintas
> y una duda sin aclarar en el foro sobre actualizaciones públicas posteriores al cierre de publicación.

> **Actualización posterior: Frontier16 (27 de septiembre).** Leer primero
> [RESUME_FRONTIER16.es.md](RESUME_FRONTIER16.es.md). El nuevo candidato local es
> `f16_repaired`, SHA `0c6ac464ec556dc96a045c6575e718bb3aa77a153a97f9bae506eec3a32807cd`.
> Antes de F17, F16 (`56609913`) y F15 (`56592376`) eran los envíos activos. F16 está COMPLETE;
> F14B está retirada. Al 27/09, 17:33 UTC: F16 2449,8, puesto 273, 45V/22D.
> Arturo autorizó explícitamente la subida privada y la submission el 27/09.
> Kaggle completó 32 partidas de verificación (F16 14/16, delta +9, sin errores)
> y se verificó el hash del paquete. El bloqueo anterior de aprobación quedó
> resuelto. Consultar el recibo antes de cualquier reintento para no duplicar.
> Los apartados siguientes conservan la historia anterior.

Este documento existe para que un chat nuevo, sin memoria de la conversación anterior, pueda retomar el proyecto en
minutos. Léelo entero antes de tocar nada. El dueño es **Arturo** (GitHub `Arturo-GA`, Kaggle `jarturo`, equipo
"Arturo Gutiérrez Aguilar", team id 16639155). Escribe en español; aprueba acciones externas con frases cortas
("envía una plaza", "envía las dos", "haz submission 2 plazas").

## 1. La competición en una página

- **Kaggriculture** (Kaggle, simulación). Dos jugadores, granja 10×10, 720 turnos (30 días × 24), mercado compartido;
  gana quien acaba con más dinero. **Solo cuenta ganar o perder**, no el margen. `kaggle-environments` 1.32.7.
- **Cierre de envíos: 30 de septiembre de 2026.** Después las submissions siguen jugando dos semanas y el ranking final
  es **un único ajuste Bradley-Terry sobre todas las partidas jugadas entre submissions que sigan activas al final**
  (confirmado por el staff el 22 de septiembre). Las partidas de ahora cuentan, pero solo contra rivales que no se
  retiren.
- **Solo las dos últimas submissions de cada equipo están activas; cada envío nuevo retira la más antigua de las dos.**
  Envía en último lugar la que quieras conservar.
- Cada submission nueva empieza en 600 y sube; desde el 23 de septiembre el emparejamiento va lento (1-2 partidas por
  hora), así que el rating tarda más de un día en asentarse. El número en vivo es ruidoso (el mismo agente puede quedar
  a 300 puntos de su copia) y tiene un fallo de actualización concurrente que el staff no arreglará.
- Medallas (~10.000 equipos): oro ≈ top 30, **plata ≈ top 5 % (≈ puesto 500, corte ≈ 2427 el 25 de septiembre)**,
  bronce ≈ top 10 %. **Objetivo actual de Arturo (27/09): acercarse al top 100 mediante análisis de derrotas y nuevas mejoras.**
- Compartir código público cerró el 23 de septiembre 23:59 UTC, pero los notebooks ya públicos se siguen pudiendo
  **actualizar** (hueco denunciado en el foro; el staff dice que lo revisa). Así apareció cha22 el 24. Compartir código
  en privado fuera del equipo está prohibido.

## 2. Estado actual (lo primero que tienes que comprobar)

**Submissions activas: 56570873 (Frontier14B, `candidates/f14_adv4_h16.py`, enviada el 26 de septiembre a las ~05:55 UTC)
y 56592376 (Frontier15, `candidates/f15_e81.py`, enviada el 27 a las 00:06 UTC)**. Retiradas: las dos Frontier13
(56560449, 56560450) y Frontier14 56568493. Recibos: `results/frontier14b/submission_receipt.json`,
`results/frontier15/submission_receipt.json`.

```bash
python live_report.py 56570873 56592376      # rating, victorias por tramo de rival, peores rivales
python submit_frontier13.py; python submit_frontier13.py --slot 2    # solo lectura: refresca los recibos
```

Evidencia de Frontier13 (detalle en `FRONTIER13_RESULTS.es.md`): holdout oficial 251/256 (15/16 contra cha22 sin
tocar); repetición de 166 partidas en vivo con rival congelado: 29 → 99 victorias; verificado en Kaggle. **Nivel real
medido el 26 de septiembre: 2400-2450** (2408 / 2103 tras ~75 partidas; 79 % contra 2300-2400, 32 % contra 2400-2500);
la estimación con rival congelado (~2500) era optimista.

**Frontier14 (26 de septiembre, ENVIADA como 56568493; `FRONTIER14_RESULTS.es.md`, `RESUME_FRONTIER14.es.md`)**:
las 39 derrotas en vivo son casi todas contra variantes privadas de cha22/prvsiyan/Herd-Safe que venden leche, fresa y
lana unos turnos antes en los días 20-27. `candidates/f14_adv4_h12.py` = Frontier13 + reasignación de constantes del
propio cha22 (`_ADV_LOOK` 4, ventanas EV/DP/MP 12): holdout registrado +10 (espejo 16/16, cha22 16/16, −2 en un mundo
contra Herd-Safe), Kaggle limpio (224 ms). **Frontier14B** (`f14_adv4_h16`, ventanas 16): puerta registrada superada
con +30 (`results/frontier14b/`), Kaggle limpio (300 ms), ENVIADA como 56570873 (retiró la 56560450); con ventanas 24 aparece el límite de Frontier9. Para enviar (solo si Arturo lo
pide): `python submit_frontier14.py --submit --authorization "..."` (una plaza; retira 56560449 y conserva 56560450).

**Frontier15 (27 de septiembre, ENVIADA como 56592376; `FRONTIER15_RESULTS.es.md`, `RESUME_FRONTIER15.es.md`)**: revisión de
las 96 partidas en vivo del par activo contra 2400+ (`vendor/live_f14`, `outputs/session/gold/ledger_f14live.json`):
los de 2450-2600 son clones de nuestra línea decididos por tiempos de venta (−7…−1500); las palizas son privados de
otra producción. Hechos del motor: precio = f(inventario); retirada del pueblo tras cada paso múltiplo de 4; ambas
listas se liquidan unidad a unidad al mismo precio; leche/lana/melón saturados desde el día 12-15 → el primero en
vender tras cada retirada cobra la holgura. `candidates/f15_e81.py` = Frontier14B + capa propia que vende todo el
almacén proyectado de leche/lana/fresa en el paso % 4 == 1 (idea E081 de mooman0222, MIT): bucle cerrado 34/36 y 34/36
(+870 por partida, 8/8 contra `f14_adv4_h16`), panel congelado 29 → 52 de 96. `f15_e81_tom2` además permite la
inversión en tomates con 2 pizzerías-mercados (+730 en el único mundo en que actúa). Puerta registrada con control =
Frontier14B (`results/frontier15/plan.json`): holdout +33 (espejo 14/16, cha22 16/16, suelo −2 respetado, 289 ms),
Kaggle 48/48 limpio a 258 ms (cha22/F13/prvsiyan 8/0). Enviada a petición de Arturo el 27 a las 00:06 UTC como
56592376 (retiró 56568493). Un envío nuevo retiraría 56570873 (Frontier14B). Las variantes `f15_ad` (ventanas 16→24 si el rival vende antes), `f15_e81g`, `f15_slk` y
`f15_wh` quedaron por debajo; `f15_e81` gana 4/4 a `f15_ad`.

Historial de rondas (cada una tiene `FRONTIERn_RESULTS.es.md` y `RESUME_FRONTIERn.es.md`):

| Ronda | Idea | Resultado en vivo |
|---|---|---|
| F5-F7 | V45/V46/V48 + lockstep | ~2600-2750, luego cayeron con cada ola pública |
| F8 | v9/4 de Tschinkel + capas públicas + lockstep | 2825 el primer día, luego 2650 |
| F9 | adelanto de ventas acotado | ~2720 |
| F10 | lockstep sobre One More Wheat y V53 | 2400 / 2200 (el público copió el lockstep) |
| F11 | prvsiyan + lockstep / Herd-Safe forecast4 + lockstep | 2150 / 2265 |
| F12 | enrutador por rama del rival (dos bases F11) | 2246 / 2199 (cha22 lo aplasta) |
| F13 | cha22 + lockstep, dos copias | 2380 / 2137 (retiradas) |
| F14 / F14B | + adelanto 4 y ventanas 12 / 16 del propio cha22 | 2341 (retirada) / 2396 (activa) |
| **F15** | **+ venta de todo el almacén al abrir cada ventana de demanda** | **en curso desde el 27 sep (56592376)** |

## 3. Lo que hemos aprendido (lecciones con evidencia)

1. **El meta lo marcan las olas públicas.** Cada ola nueva gana a la anterior casi siempre; un agente construido sobre
   la base vieja cae 200-600 puntos en un día. Antes de cada envío hay que revisar notebooks nuevos (incluidos los
   *actualizados* después del cierre).
2. **Nuestra ventaja estable es el lockstep** (`frontier5_lockstep.py`): el motor liquida las listas de mercado de los
   dos jugadores posición a posición y unidad a unidad al mismo precio, así que el orden de tu lista decide quién vende
   en el exceso de quién. La capa reordena nuestras ventas contra una copia de nuestra propia lista. Gana el espejo
   contra clones de la base por +80 a +300 monedas casi siempre. El público copió la idea (shiiin9 "Order Book",
   capa D), pero sobre una base que ya tiene capa D nuestro lockstep responde un nivel por encima y sigue sumando.
3. **Solo cuenta W/L**; el 40 % de las partidas de la franja alta se deciden por menos de 100 monedas. Cambios de
   margen grandes en partidas que ya ganas no valen nada.
4. **Las partidas entre agentes de la misma familia son deterministas y simétricas por asiento** (711 de 759 pares con
   el mismo margen en ambos asientos): la unidad de evidencia es la **semilla**, no el asiento. Usa ≥ 6-8 semillas.
5. **El motor local reproduce el ladder a la moneda.** Se pueden bajar replays propios y repetir la partida con otro
   agente contra el rival congelado (`replay_panel.py`), pero el rival congelado no reacciona: es optimista.
6. **Una copia "sombra" de un rival público reproduce sus acciones** (719/719) si le das sus observaciones; aun así,
   responder al turno con su lista exacta **empeora** (el rival reacciona en los turnos siguientes). Todo cambio se
   mide en bucle cerrado, partida completa.
7. **No es transitivo**: un agente puede ganar a A y perder contra B que pierde contra A. Mide contra el panel real y
   por rival, no solo el total. Incluye siempre las familias débiles de la subida (a1-t31 `n23_kenanzhang9_b52378`,
   hack `n23_syedtahahassan_a2047e`, utils-v1 = `v43`, shop-router `aurax_v7`): una submission empieza en 600.
8. **Rechazado con datos (no repetir):** vender con paciencia o partir ventas, mantener stock, adelantos fijos de venta
   (escalan y se vuelven caóticos), trasplantar grabaciones del top, la "clarividencia" miope, la tabla por mundo con
   pocas semillas, constantes de rebaño/zanahoria, RL/PPO en pocos días (los repos públicos de RL pierden por miles).
9. **La rama del rival se reconoce en el paso 1** por su dinero público tras la compra inicial de trigo (útil para
   enrutadores), pero hoy cha22 gana a todas las ramas, así que no hace falta enrutar.
10. **Donde pierde cha22 en su espejo**: juega igual hasta el paso ~432 y la diferencia aparece en los días 18-29
    (conversión final y carrera de ventas del mismo turno). Si quieres mejorar, ése es el sitio.

## 4. Cómo trabajar en este repo

Ruta: `C:\Users\Arturo\Documents\RSNA - ChatGPT\kaggriculture-lab`. Python:
`.venv/Scripts/python.exe -X utf8`. Kaggle CLI (`python -m kaggle`) y `gh` autenticados. Windows con Git Bash.

Herramientas clave:

| Archivo | Para qué |
|---|---|
| `evaluate.py` | partidas oficiales `--candidates A B --opponents X Y --seeds ... --workers 7 --output f.json` (candidatos × rivales × semillas × 2 asientos) |
| `rr_run.py` | round robin sin duplicados espejo; `--extra A B --vs X Y` y `--seat0` para la mitad de coste |
| `resume_eval.py` | reanuda una evaluación cortada, repitiendo solo las partidas que faltan |
| `frontier5_validation.py` | `assess()` de un holdout emparejado contra un control |
| `replay_panel.py` | repite partidas en vivo con un agente propio contra el rival congelado (`--raw`, `--episodes`) |
| `live_report.py` | estado en vivo de submissions |
| `pull_public_notebooks.py` / `scan_public_agents.py` | baja notebooks y extrae los agentes incrustados (todos los formatos conocidos), deduplica por hash |
| `build_f13.py` (y anteriores) | construye candidatos = base pública fijada por hash + capa del Lab |
| `cloud_/make_/verify_/submit_frontier13.py` | notebook privado de verificación en Kaggle → verificación local → envío con autorización |
| `test_frontier13.py` | pruebas de construcción, punto de entrada y una partida |

Proceso estándar para un candidato nuevo (lo que hicimos en cada ronda):
1. Revisar lo público: `python -m kaggle kernels list --search kaggriculture --sort-by dateRun` (**usa `--search`**:
   `--competition` omite notebooks), bajar con `pull_public_notebooks.py <carpeta>` y extraer con
   `scan_public_agents.py <carpeta> <prefijo> <informe.json>`.
2. Medir los agentes nuevos contra nuestra submission y las mejores referencias (`rr_run.py`, pocas semillas).
3. Construir la variante (base + `frontier5_lockstep.py`, enlazando el **último callable** de la base — Kaggle ejecuta
   el último callable de `main.py`).
4. Registrar la puerta en `results/frontierN/plan.json` **antes** de correr; holdout en semillas nuevas con la base
   sin tocar como control emparejado; `assess`.
5. Notebook privado de verificación en Kaggle (debe pesar < 1 MB: los agentes incrustados deben compartir código), bajar
   la salida, `verify_*`.
6. Enviar **solo si Arturo lo pide explícitamente**, con `submit_frontierN.py --submit --authorization "<sus palabras>"`
   (`--slot 2` para la segunda plaza). Esperar a que Kaggle la valide (COMPLETE) y refrescar el recibo.
7. Documentar (`FRONTIERn_RESULTS.es.md`, `RESUME_FRONTIERn.es.md`, README, NOTICE), commit y push.

Semillas ya usadas (no reajustar sobre ellas): 5601-6022, 7101-7704, 8001-8434, 9001-9164 (detalle en cada RESUME).

## 5. Reglas del proyecto (no negociables)

- **Nunca enviar a Kaggle sin petición explícita de Arturo**, y registrar su frase en el recibo. No crear
  automatizaciones ni rondas nuevas sin que lo pida.
- **El código de terceros no va a Git**: los agentes públicos viven en `candidates/` pero están en `.gitignore`
  (prefijos `n23_`, `n25_`, `d25_`, `g25_`…); solo se suben nuestros candidatos derivados, con los avisos originales
  intactos y crédito en `NOTICE.md`. Antes de cada commit, comprueba que ningún archivo preparado coincide por hash
  con una fuente de terceros.
- **Licencias**: solo se usa como base código con licencia abierta (Apache-2.0/MIT/CC0). Repositorios de GitHub sin
  licencia (la mayoría, incluido el de Gluzdov) solo como rivales de evaluación local.
- Nada de credenciales en Git (hay un dataset público con un `kg_token.py` que no se debe abrir ni usar).

## 6. Trampas técnicas que ya nos mordieron

- **Windows `OSError [Errno 22]`** al reescribir el JSON de resultados: pasó con lecturas concurrentes y sin ellas.
  Los evaluadores ya escriben de forma atómica con reintentos; aun así **vigila el log, no el JSON**, y si se corta usa
  `resume_eval.py`.
- Lanza las tandas largas con `run_in_background` (se pueden detener con TaskStop); no con `&`. El clasificador de
  permisos no deja matar procesos por PID.
- **Último callable**: muchos notebooks dejan un `agent` intermedio; enlaza siempre el que ejecuta Kaggle. Algunos
  agentes aceptan un solo argumento (`evaluate.py` ya lo respeta). Algunos notebooks publicados están rotos (último
  callable que no es el agente) y juegan con 3.000 de dinero final.
- Archivos con CRLF: la herramienta Edit falla; parchea con Python leyendo bytes. Los heredocs de bash con comillas
  anidadas fallan: escribe el script con Write y ejecútalo.
- El acelerador C++ (`evaluate_fast.py`) **no** es exacto para estos linajes; usa siempre el motor oficial.
- Disco C: casi lleno (≈18 GB libres). No bajes los datasets diarios de replays (≈700 MB/día, solo top) ni los archivos
  de varios GB.

## 7. Consejos para lo que queda hasta el 30 de septiembre

1. **Mira el estado en vivo** (`live_report.py 56560449 56560450`) y el tramo donde se gana ~50 %: ése es el nivel real.
   **No reemplaces una submission que aún sube por una diferencia de 100-200 puntos.**
2. **Revisa si hay agentes nuevos por actualización de notebooks** (paso 1 del proceso). Si aparece uno que gana a cha22,
   repite el proceso: base nueva + lockstep, holdout, Kaggle, y pide permiso a Arturo para enviar.
3. Lo que sabemos ahora del espejo (Frontier15): en mercados saturados gana el primero que vende tras cada retirada del
   pueblo; la liquidación al abrir la ventana (`f15_e81`) domina a las ventanas fijas y a la escalada adaptativa. Lo que
   queda por explorar: cultivo ligado a las tiendas (zanahorias con PET_CAFE, tomates con PIZZA_SHOP: los clones que
   lo hacen nos ganan por 2700-3300), y nada de tiempos sirve contra los privados de 2600+.
   Antes (Frontier13): el hueco estaba en los días 18-29 del espejo contra cha22 (conversión final).
   **Para ganar a los de 2700 hace falta otra economía** (`ANALISIS_2700.es.md`, 27 sep): 4 cuadrantes hacia el día 10,
   12-13 manos, 20-25 animales el día 12 elegidos por las tiendas, tomates/zanahorias tempranos, trigo de caja; los
   top-100 lo hacen con planificadores propios o PPO + clonación de comportamiento sobre los replays oficiales del top.
   Probado y descartado antes del cierre: bloques de expansión en el SE con manos 12-13 (no rentan), trasplante de
   cintas grabadas del top-10 (Boey gana 4/12 y se derrumba en 8/12), dirigir el sorteo de tiendas (God's mode).
   **Puntos flojos medidos** (prueba complementaria, `FRONTIER13_RESULTS.es.md` §5): `g25_mooman0222_a62376` (E081,
   3/4) y `g25_mooman0222_baf0d3` (E082, 2/4) — Herd-Safe que vende todo el almacén de leche/lana/fresa al abrir cada
   ventana de demanda — y `g25_wangyh_v44` (3/4, cha22-like con `_ADV_LOOK` 6). Ideas sin probar: "reparar la acción
   bloqueada" (Avineesh, +4.373 de margen en su arnés), `_ADV_LOOK` 6 sobre cha22, y una respuesta específica a la venta
   en bloque al abrir ventana. Cualquier cambio: holdout emparejado contra `f13_c22_lock` en semillas nuevas.
4. **El último envío antes del 30 debe ser el que quieras conservar**, y conviene enviar pronto: las partidas previas
   al cierre cuentan en el ajuste final.
5. Mantén siempre dos submissions activas y fuertes; dos copias del mejor agente es una opción válida (dos trayectorias
   independientes frente al ruido).

## 8. Dónde está cada cosa

- Resultados y decisiones por ronda: `FRONTIER*_RESULTS.es.md`, `RESUME_FRONTIER*.es.md`, `README.md`.
- Evidencia de cada holdout y verificación: `results/frontierN/` (plan, holdout, holdout_summary, kaggle_verified,
  recibos).
- Material de investigación (no está en Git): `outputs/session/gold/` (incluye `research_0925/`: notebooks, datasets,
  GitHub, foro, derrotas en vivo y crítico), `vendor/` (notebooks, datasets, repos y replays bajados).
- Memoria persistente del asistente para este proyecto: `C:\Users\Arturo\.claude\projects\C--Users-Arturo-Documents-RSNA---ChatGPT-kaggriculture-lab\memory\`.
