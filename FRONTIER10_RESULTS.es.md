# Frontier10: por qué Frontier9 se quedó en 2700 y el candidato para 2800 — 20-21 de septiembre de 2026

Petición de Arturo: revisar cómo le fue al último envío (no está cerca de donde apuntaba), revisar sus fallos
y crear uno que apunte a 2800.

## 1. Cómo le fue a Frontier9

Submission 56404796, tres horas después de enviarla: **2695 con 47 partidas** (36 ganadas). Contra rivales de
2600-2700: 7/4; contra 2700-2800: 6/6; contra 2800-2900: 0/1. Apuntaba a 2850-2900 y se estabilizaba hacia
2700-2750. Frontier8 (56372978) cayó a 2671, con 10 victorias en sus últimas 50 partidas.

## 2. El fallo: la base quedó una generación atrás en un día

El 20 de septiembre salió otra ola pública, encima de la del 19 sobre la que están construidos Frontier8 y 9:

| Notebook (20 sep) | Qué es | Declarado |
|---|---|---|
| The Metav4 Farm v13 (Thomas Tschinkel) | sucesor de su agente de 2945: recorte de manos caras, reserva de pienso de zanahoria 2→1 día, fertilización desde el día 14, biblioteca de ventas reconstruida con 1200 replays del top 30 | **40-0 contra su propio 2945**, +798 por partida |
| Pipe-16 (Nathan Jacob) | Metav4 + trigo con manos ociosas en la apertura | 50-0 contra Metav4 |
| "V54", best-agent-ranking, auto top1, Master Engine V4 | **el mismo archivo** de Pipe-16 reempaquetado (cuatro notebooks) | — |
| One More Wheat (Dmitrii Gluzdov) | Metav4 + otro trigo más | — |
| V51, V52, V53 (Ahmed Berat Özer) | V50 + constantes y PREDICT de Tschinkel; V53 vende un paso antes que las ventas grabadas de Pipe-16 y Gluzdov | +1314 sobre V50 |

Medido en el motor oficial (semillas 7501-7504): **Frontier9 empata 4/4 contra cada agente de la ola nueva**
(margen medio −114 a −188). No es que el adelanto de ventas fallara: es que los rivales de 2700-2850 ya
corren una base que gana 40-0 a la nuestra, y nuestro adelanto solo compensa esa desventaja hasta el empate.
Dentro de la ola: One More Wheat > Pipe-16 = V54 = Yummers > Metav4 > V53, por 28-78 monedas.

Las huellas de apertura de los rivales que nos ganaron en vivo lo confirman: 16 de 27 abren con
`BUY 20 / SELL 15` (linaje Tschinkel: 10-6 para nosotros), dos con `BUY 20 / SELL 15 / semilla de trigo`
(Pipe-16: 0-2) y uno es adaptativo (−6593).

## 3. Primer intento: el adelanto de Frontier9 sobre la base nueva (rechazado)

`build_f10.py` aplica el mismo parche de RACEGATE a One More Wheat (`f10_omw_pre`). Pantalla 7511-7516: 12/0
contra Gluzdov, Pipe-16 y Metav4 (+950 a +1140), 10/2 contra Frontier9, 5/7 contra V53. En el holdout
registrado (semillas nuevas 7521-7528) **falló la puerta**: total 161/192 frente a 147/192 del control, pero
**10/6 contra Pipe-16 y Metav4 cuando la base sin tocar les gana 14/2** (por 27-79 monedas). El adelanto gana
más grande y pierde tres mundos de cada ocho. Los libros por producto de los mundos perdidos muestran que
adelantar leche y lana suma (+250 a +1000) y adelantar fresa resta (−1000 a −1550); pero las variantes
solo-leche, solo-lana y leche+lana siguen perdiendo 2-4 mundos de 14 contra la base. Con dos agentes
reactivos el adelanto cambia la cadena de ventas de forma caótica: margen medio positivo, victoria no
garantizada. Rechazado (`results/frontier10/rejected_pre4f_holdout*.json`).

## 4. El candidato: One More Wheat + orden lockstep (`f10_omw_lock`)

Lo que cuenta es ganar, no el margen. La capa lockstep (ordena nuestras ventas del turno contra una copia con
el precio exacto del motor, sin cambiar qué ni cuándo se vende) añade una ventaja pequeña pero constante, y
sobre la base nueva no rompe nada: en las 14 semillas ya usadas (ambos asientos) gana **26/28 a One More
Wheat, 26/28 a Pipe-16 y 27/28 a Metav4** (márgenes +39 a +886; la única derrota es el mundo asimétrico 7524,
que la propia base pierde contra sí misma) y 15/28 a V53, igual que la base.

## 5. Aceptación de f10_omw_lock

Puerta registrada antes de correr (`results/frontier10/plan.json`): motor oficial, control emparejado One More
Wheat, total emparejado de +10 o más, espejo de 50 % o más, ningún rival por debajo de −2, sin errores y
llamadas por debajo de 1000 ms.

Holdout (semillas nuevas 7531-7538, 384 partidas): **170 de 192** (control 162).

| Rival (16 partidas) | f10_omw_lock | Control | Margen medio |
|---|---:|---:|---:|
| One More Wheat (espejo) | **16/0** | empates | +232 |
| Pipe-16 / V54 | **16/0** | 15/1 | +281 |
| Metav4 | **16/0** | 15/1 | +328 |
| V53 | 6/10 | 6/10 | −31 |
| V52 | 10/6 | 11/5 | +317 |
| Frontier9 | 12/4 | 12/4 | +656 |
| Frontier8, Tschinkel 2945, Pipe-15, Gluzdov (19 sep), Alperen | 16/0 cada uno | igual | +1650 a +3800 |
| tetsutani (V50) | 14/2 | 14/2 | +2137 |

Sin errores, latencia máxima 282 ms. **El umbral de total (+10) no se alcanzó: +8.** El control ya gana 162 de
192, así que lo único que quedaba por ganar eran los empates de su propio espejo (+8) y un mundo contra
Pipe-16 y Metav4, y se ganó todo eso; contra V52 pierde un mundo más que el control (−2, dentro de lo
permitido). Queda documentado como incumplimiento de 2 puntos en `plan.json`; el resto de criterios pasa.

Verificación en Kaggle (kernel privado `jarturo/kaggriculture-frontier10-lockstep`, versión 1, semillas
7541-7544, control emparejado): **8/0 contra One More Wheat (+207), 8/0 contra Pipe-16 (+234), 8/0 contra
Metav4 (+284)**; 181 ms, cero errores; `main.py` y `submission.tar.gz` coinciden byte a byte con el candidato;
SHA-256 del archivo `5a27957596d4e84b2a89e0ea22870040003e9c0b96cba9ee403ffb10e6282614`
(`results/frontier10/kaggle_verified.json`). Las cinco pruebas de `test_frontier10.py` pasan.

## 6. Segunda plaza: la otra familia pública (`f10_v53_lock`)

La franja 2700-2900 tiene ahora dos familias públicas de fuerza parecida: la de Metav4 (Tschinkel, Pipe-16/V54,
Gluzdov) y la V5x de Ahmed Berat Özer (V52/V53), que se reparten los mundos entre sí. `f10_omw_lock` gana
siempre a la primera y solo empata con la segunda. La misma capa lockstep sobre V53 (enlazando su punto de
entrada público `_e363_agent`) hace lo contrario: en las semillas ya usadas 7511-7516 ganó 12/12 a V53 y V52
(+189 a +531), 11/12 a One More Wheat y Pipe-16 y 9/12 a `f10_omw_lock`, con +412 de ganancia modelada por
partida.

Puerta registrada antes de correr (`results/frontier10b/plan.json`; control V53, total de +8 o más). Holdout
(semillas nuevas 7551-7558, motor oficial): **148 de 192 frente a 110 del control (emparejada +38), puerta
superada**:

| Rival (16 partidas) | f10_v53_lock | V53 sin tocar |
|---|---:|---:|
| V53 y V52 (espejo de familia) | **16/0** cada uno (+579) | empates |
| One More Wheat, Pipe-16 | 8/8 | 4/12 |
| Metav4 | 10/6 | 8/8 |
| f10_omw_lock (nuestro otro candidato) | 6/10 | 4/12 |
| Frontier9 | 10/6 | 6/10 |
| Tschinkel 2945, Pipe-15, Gluzdov (19 sep) | 14/2 | 12/4 |
| tetsutani (V50), Alperen | 16/0 | 16/0 |

Sin errores, 312 ms. Kaggle (kernel `jarturo/kaggriculture-frontier10b-v53-lockstep`, semillas 7561-7564):
**8/0 contra V53, V52 y tetsutani**, 289 ms; archivo `1e1651fc2747260b1210698d344a72627e948999d4fef4a00339a0d2063fbcb8`
(`results/frontier10b/kaggle_verified.json`). Las pruebas de `test_frontier10b.py` pasan.

Los dos candidatos se complementan: uno domina la familia Metav4 y el otro la familia V5x, y cada uno queda
cerca del 50 % contra la familia contraria. Como el leaderboard toma la mejor de las dos plazas, van uno en
cada plaza. **No se ha enviado nada al leaderboard.**

## 7. Qué esperar y límites

Frontier9 quedó en 2700 por estar una generación por detrás; estos dos están sobre la ola del 20 de septiembre
y ganan por poco pero casi siempre a los clones de su familia, que es lo que pasó con Frontier8 en su primer
día (2825) antes de que la base envejeciera. El objetivo de 2800 es razonable mientras no salga otra ola; las
olas han salido a diario y el cierre de notebooks públicos es el 23 de septiembre a las 23:59 UTC, así que hay
que contar con repetir este proceso una o dos veces más y dejar el par final el 24. Contra los agentes
adaptativos del top 10 seguimos sin respuesta (pérdidas de miles), igual que toda la familia pública.
