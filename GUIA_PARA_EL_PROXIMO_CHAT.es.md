# Guía de traspaso para el próximo chat — Kaggriculture (estado al 25 de septiembre de 2026, ~21:40 UTC)

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
  bronce ≈ top 10 %. **Objetivo actual de Arturo: plata al cierre.**
- Compartir código público cerró el 23 de septiembre 23:59 UTC, pero los notebooks ya públicos se siguen pudiendo
  **actualizar** (hueco denunciado en el foro; el staff dice que lo revisa). Así apareció cha22 el 24. Compartir código
  en privado fuera del equipo está prohibido.

## 2. Estado actual (lo primero que tienes que comprobar)

**Submissions activas: 56560449 y 56560450**, las dos con el mismo archivo `candidates/f13_c22_lock.py`
(cha22 + nuestra capa lockstep), enviadas el 25 de septiembre a las 21:26 UTC y validadas (arrancan en 600).
Recibos: `results/frontier13/submission_receipt.json` y `submission_receipt_2.json`.

```bash
python live_report.py 56560449 56560450      # rating, victorias por tramo de rival, peores rivales
python submit_frontier13.py; python submit_frontier13.py --slot 2    # solo lectura: refresca los recibos
```

Evidencia de Frontier13 (detalle en `FRONTIER13_RESULTS.es.md`): holdout oficial 251/256 (15/16 contra cha22 sin
tocar); repetición de 166 partidas en vivo con rival congelado: 29 → 99 victorias; verificado en Kaggle. Estimación
honesta: nivel alrededor de 2500 (≈50 % en la franja 2500-2600), por encima del corte de plata; contra los privados de
2600+ no mejora.

Historial de rondas (cada una tiene `FRONTIERn_RESULTS.es.md` y `RESUME_FRONTIERn.es.md`):

| Ronda | Idea | Resultado en vivo |
|---|---|---|
| F5-F7 | V45/V46/V48 + lockstep | ~2600-2750, luego cayeron con cada ola pública |
| F8 | v9/4 de Tschinkel + capas públicas + lockstep | 2825 el primer día, luego 2650 |
| F9 | adelanto de ventas acotado | ~2720 |
| F10 | lockstep sobre One More Wheat y V53 | 2400 / 2200 (el público copió el lockstep) |
| F11 | prvsiyan + lockstep / Herd-Safe forecast4 + lockstep | 2150 / 2265 |
| F12 | enrutador por rama del rival (dos bases F11) | 2246 / 2199 (cha22 lo aplasta) |
| **F13** | **cha22 + lockstep, dos copias** | **en curso (desde 600)** |

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
3. Si hay tiempo para mejorar el agente: el hueco está en los días 18-29 del espejo contra cha22 (conversión final).
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
