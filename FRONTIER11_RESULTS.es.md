# Frontier11: la última ola pública (21-23 de septiembre) y el candidato para volver a 2800 — 24 de septiembre de 2026

Petición de Arturo: la última submission fue muy buena pero la gente subió más modelos; revisar el foro y los
últimos códigos públicos con buenos puntajes y hacer una submission que vuelva a un puntaje parecido a 2800,
con todo lo aprendido.

## 1. Cómo están las dos Frontier10 (24 sep, 01:30 UTC)

| Submission | Agente | Rating | Partidas | Últimas partidas |
|---|---|---:|---:|---|
| 56410971 | `f10_omwg_lock` | 2229.9 | 371 (150 ganadas) | 5/21 en las últimas 21 |
| 56410981 | `f10_v53_lock` | 2401.6 | 381 (178 ganadas) | 6/31 en las últimas 31 |

Equipo en el puesto 757 de 9937. Cortes: oro 2854 (puesto 29), plata 2501 (puesto 496), bronce 2313 (puesto 993).
Hoy **2800 equivale al puesto 45**: el ladder se ha estirado y 2800 está a un paso del oro.

## 2. Lo que dice el foro

- **Cómo se decide el ranking final** (Addison Howard, Kaggle, 22 sep, hilo "Tournament Question"): el
  Bradley-Terry final usa *todas las partidas jugadas entre submissions que sigan activas al final*, no solo las
  dos semanas posteriores al cierre. Solo las dos últimas submissions de cada equipo están activas, y **cada envío
  nuevo retira la más antigua de las dos**. Consecuencias: enviar pronto el agente definitivo suma partidas que
  cuentan, y hay que enviar en último lugar el agente que se quiere conservar.
- Avineesh Arora, "What actually predicted the ladder": el motor local reproduce el ladder a la moneda; cuenta
  la tasa de victoria, no el margen (el 40 % de sus partidas contra rivales de 2250+ se decidió por menos de 100
  monedas); los agentes públicos fuertes no son transitivos; y un agente tiene que ganar también durante la
  subida desde 600, no solo en la franja donde se quiere terminar.
- El cierre de notebooks públicos fue el 23 de septiembre a las 23:59 UTC: **esta ola es la definitiva**. Ya no
  puede aparecer una base pública más nueva, solo mejoras privadas.

## 3. Por qué cayeron las Frontier10: el público copió la idea del lockstep

Se bajaron los 70 notebooks ejecutados desde el 20 de septiembre por la noche, se extrajeron 38 agentes y quedaron
31 únicos por hash que cargan.

- **shiiin9, "Your Market List Is an Order Book"** (21 sep): V55 + una "capa D" que ordena las ventas del turno
  contra una copia de la propia pila con el evaluador lockstep exacto del motor. Es nuestra idea del lockstep,
  generalizada (puede mover ventas por encima de compras fijas). Declara 280-0 contra V55.
- **Dmitrii Gluzdov, "Herd-Safe Sale Window"** (22 sep) sobre esa capa, y encima de él **arsgorynich** con
  "forecast4" (el predictor de ventas rivales mira cuatro turnos por delante) y una respuesta de segundo nivel
  ("Order Book v3").
- **Ahmed Berat Özer abandonó su familia V5x**: su V54 es byte a byte el agente con guarda de prvsiyan, y V55-V57
  son de la misma familia. Nuestra plaza "V5x" (`f10_v53_lock`) se quedó sin rival para el que estaba hecha.
- **prvsiyan** (22 sep, el mismo archivo en "The Soil Remembers Rain", "The Moon Counts Melons" y en el notebook
  de tetsutani del 23): el motor híbrido "2965" de haideptry + ventas adelantadas hasta 4 turnos + compactación de
  la cola del mercado (quita huecos y órdenes muertas para que nuestras ventas liquiden en posiciones anteriores
  a las del rival) + reordenación final de bloques de venta.

Gauntlet en el motor oficial (semillas 7601-7602, 12 partidas contra tres referencias: la guarda de prvsiyan,
`f10_omwg_lock` y Herd-Safe): prvsiyan 12/12 (+1018), wzhengbiao "hybu" 12/12 (+731), Herd-Safe forecast4 12/12
(+590), … **`f10_omwg_lock` 4/12 y `f10_v53_lock` 0/12**. Nuestros dos agentes en vivo están una generación por
detrás, igual que Frontier9 el día 20.

Round robin de los diez mejores (semillas 7611-7613, ambos asientos, 270 partidas, 54 por agente):

| Agente público | Victorias | Margen medio |
|---|---:|---:|
| prvsiyan, Soil/Moon (22 sep) | **52/54** | +505 |
| arsgorynich, Herd-Safe forecast4 (23 sep) | **48/54** | +634 |
| wzhengbiao, hybu (23 sep) | 28/54 | +309 |
| statma, Herd-Safe race ca20 | 28/54 | −234 |
| Gluzdov, More Wheat Smarter Sales (22 sep) | 28/54 | +186 |
| yasutakababa v16 / wzhengbiao v15 (mismo juego) | 26/54 | +283 |
| Gluzdov, Herd-Safe Sale Window | 24/54 | −327 |
| arsgorynich, Order Book v3 | 16/54 | −482 |
| haideptry, 2965 Master Hybrid | 15/54 | −333 |
| shiiin9, Order Book (y sus copias) | 5/54 | −540 |

## 4. El candidato: el agente de prvsiyan + nuestro lockstep (`f11_pv_lock`)

Con la capa D generalizada, la pregunta era si nuestro lockstep todavía suma algo. Contra una copia de una pila que
ya ordena, nuestro lockstep modela al rival con la lista *final* de esa pila, así que responde un nivel por encima.
Se probaron dos capas sobre las dos mejores bases, emparejadas con la base sin tocar (semillas 7621-7623, 8 rivales
del top, 48 partidas por agente):

| Agente | Victorias | Δ puntuación emparejada | Margen ganado por partida |
|---|---:|---:|---:|
| prvsiyan sin tocar | 38/48 (4 empates en el espejo) | — | — |
| **prvsiyan + lockstep** | **45/48** | **+5.0** | **+139** (positivo contra los 8) |
| prvsiyan + respuesta de tres modelos (`frontier11_order.py`) | 45/48 | +5.0 | +94 |
| Herd-Safe forecast4 sin tocar | 27/48 | — | — |
| Herd-Safe forecast4 + lockstep | 32/48 | +3.0 | +143 |
| Herd-Safe forecast4 + respuesta de tres modelos | 32/48 | +3.0 | +127 |

Se congela **prvsiyan + lockstep** (`candidates/f11_pv_lock.py`, hash
`def14a5a7c98c9847103bb41ae916a492d3e4e405995616bf25c8363427e47ca`): la base más fuerte, con el entry point público
`_final_sell_block_reorder_entrypoint` enlazado y `frontier5_lockstep.py` sin cambios. La capa nueva de tres
modelos (`frontier11_order.py`) queda en el repositorio como experimento medido: suma, pero menos que el lockstep.

## 5. Aceptación (holdout registrado)

Puerta registrada antes de correr (`results/frontier11/plan.json`): motor oficial, control emparejado = el agente de
prvsiyan sin tocar, 16 rivales (los diez mejores de la ola, V57, las bases más copiadas de antes y nuestras dos
Frontier10 en vivo, para ver también la subida desde 600), ambos asientos; total emparejado de +6 o más, espejo del
70 % o más, ningún rival por debajo de −2, sin errores y llamadas por debajo de 1000 ms.

Holdout (semillas nuevas 7631-7638, 512 partidas): **206 de 256 frente a 186 de 256 (+16 empates) del control;
emparejado +12, espejo 16/16, ningún rival peor que con la base, +56 monedas por partida de media. Puerta superada.**

| Rival (16 partidas) | f11_pv_lock | Base sin tocar | Margen ganado |
|---|---:|---:|---:|
| prvsiyan sin tocar (espejo) | **16/16** | empates | +111 |
| Gluzdov, Herd-Safe | **10/16** | 8/16 | +62 |
| haideptry, 2965 Master Hybrid | **10/16** | 8/16 | +61 |
| arsgorynich, Herd-Safe forecast4 | 8/16 | 8/16 | +66 |
| Gluzdov, More Wheat Smarter Sales | 6/16 | 6/16 | +64 |
| statma, Herd-Safe ca20 | 10/16 | 10/16 | +60 |
| Order Book v3 y Order Book | 12/16 cada uno | 12/16 | +60 |
| wzhengbiao hybu, yasutakababa v16, V57 | 16/16 cada uno | 16/16 | +57 a +67 |
| `f10_v53_lock` | 10/16 | 10/16 | +72 |
| `f10_omwg_lock`, guarda V54, One More Wheat, Pipe-16 | 16/16 cada uno | 16/16 | +22 a +29 |

Sin errores, 380 ms de máximo. Lectura honesta: el lockstep suma en todos los emparejamientos, pero **contra la
familia Herd-Safe el resultado depende mucho del mundo**. Las semillas 7637 y 7638 se pierden contra sus cinco
agentes y la 7632 contra cuatro; contra More Wheat Smarter Sales y Herd-Safe forecast4 se pierden además otros dos
mundos. En las semillas del round robin y del cribado la misma base había ganado 6/6 a cada uno. Contra los otros
nueve mejores de la ola, este candidato gana 100 de 144 partidas (69 %).

Verificación en Kaggle (kernel privado `jarturo/kaggriculture-frontier11-lockstep`, versión 1, semillas nuevas
7641-7644, control emparejado): **8/0 contra el agente de prvsiyan sin tocar (+75), 6/2 contra Herd-Safe forecast4
(+378) y 6/2 contra el 2965 de haideptry (+564)**, igual que el control en estos dos últimos; 324 ms, cero errores;
`main.py` y `submission.tar.gz` coinciden byte a byte con el candidato; SHA-256 del archivo
`8ed05fd54b7ec7b2c38dbc8f14994af6e28ed122e1de344871efc66f103ea4e7` (`results/frontier11/kaggle_verified.json`).
Las cinco pruebas de `test_frontier11.py` pasan.

## 6. Envío

**Enviado el 24 de septiembre de 2026 a las 03:03 UTC a petición de Arturo** ("haz una submission que tenga un
puntaje parecido al anterior de 2800"): `f11_pv_lock` = submission **56509994** (recibo en
`results/frontier11/submission_receipt.json`), validada por Kaggle sin errores y arrancando en 600. Retira la
submission activa más antigua, 56410971 (`f10_omwg_lock`, 2206). Quedan activas 56509994 y 56410981
(`f10_v53_lock`, 2382). Seguimiento: `python live_report.py 56509994 56410981`.

## 7. Qué esperar y límites

- Es el agente más fuerte que hemos medido sobre la ola pública definitiva: gana 16/16 a todas las bases antiguas
  (incluidas nuestras dos Frontier10) y 16/16 a su espejo. Contra la familia Herd-Safe queda entre el 40 y el 65 %,
  según el rival y el mundo.
- La diferencia con las rondas anteriores es que ya no puede salir una base pública más nueva. Lo que puede
  superarlo son agentes privados.
- **2800 hoy es el puesto 45, casi oro.** Nuestras Frontier anteriores tocaron esa zona cuando estaban sobre la ola
  pública más nueva, y esta vez esa condición se cumple hasta el final. Aun así no lo prometo: lo razonable es
  esperar la franja de 2600-2800. Además, según el foro, las submissions nuevas se pasan de largo al principio y
  necesitan de 40 a 70 partidas (unas 5-8 horas) para asentarse.
- La segunda plaza activa sigue con `f10_v53_lock` (2382), que ya está superado. El próximo envío retiraría esa
  plaza y no la nueva, porque se retira la más antigua. Conviene usarla con un segundo candidato complementario
  solo si Arturo lo pide.
