Análisis del top 27 y nuevo agente Frontier — 13 de septiembre de 2026

Frontier incorpora un planificador propio del último día sobre nuestra segunda
versión, `ml_critic`. La producción de los días anteriores sigue procediendo de
V37 y sus autores; no es un agente completamente nuevo desde cero. La nueva parte
decide conjuntamente contratación, compra y distribución de fertilizante, tareas
de cosecha, rutas de regreso y orden de ventas. Es una intervención considerablemente
mayor que cambiar el horizonte de ventas de nuestro primer envío, aunque su alcance
sigue limitado a los últimos 23 turnos.

Consulté el leaderboard y descargué partidas públicas de ocho equipos en posiciones
1, 2, 3, 5, 8, 13, 21 y 27. La instantánea es de las 20:00 UTC del 13 de septiembre;
las posiciones pueden cambiar. Son 24 observaciones de equipo-partida, correspondientes
a 22 partidas distintas. Los duelos compartidos no son observaciones independientes.
El registro, identificadores y hashes están en `results/gold/audit.json` y el análisis
reproducible en `analyze_gold.py` / `results/gold/behavior.json`.

Lo observado no revela el código privado, su algoritmo de entrenamiento ni todo su
comportamiento frente a otro rival. En esa muestra:

| Equipo y posición de la instantánea | Observación concreta |
| --- | --- |
| Majkel1337, 1 | En el día 18: 24–35 fresas, 8 vacas, 17–25 trigos y 3–10 ovejas, además de otros activos. Once trabajadores en el día 24 de las tres partidas. |
| Artem The Farmer, 2 | Mezclas distintas entre partidas: 14–38 fresas, 9–10 vacas y 2–16 ovejas. Once o doce trabajadores en el día 24. |
| Otter Vibe, 8 | Mayor diversidad, incluyendo tomates, melones y gansos; entre once y catorce trabajadores en el día 24. |
| QQ Farming, 27 | En el día 18: 11–12 melones y 11–20 tomates; composición muy distinta de nuestra base. |

La lectura útil es que no existe una única combinación de cultivos en esta muestra.
También hay actividad muy distinta al final: el primero registra 13 órdenes PASS
en los últimos seis días de sus tres partidas, frente a cientos en otros equipos.
Son órdenes solicitadas, no una medición de productividad exitosa; contratar más
trabajadores cambia el denominador. No atribuyo causalmente el ranking a ese dato.
Motiva estudiar el coste de mano de obra, el trabajo pendiente y la entrega antes
del cierre, que sí podemos optimizar y contrastar.

En el foro [Any High-Ranking Entries Using RL?](https://www.kaggle.com/competitions/kaggriculture/discussion/736369)
se discuten enfoques heurísticos y aprendizaje por refuerzo. Son declaraciones de
participantes, no auditorías de sus agentes. La discusión sobre
[el cuarto cuadrante](https://www.kaggle.com/competitions/kaggriculture/discussion/734308)
señala el compromiso entre expansión, rentabilidad, trabajo y desplazamientos.
El notebook público [Island GA](https://www.kaggle.com/code/destbreso/island-ga-an-owned-schedule-is-a-moat)
propone desarrollar calendarios propios mediante búsqueda; revisamos su método,
pero no ejecutamos su búsqueda genética ni atribuimos sus resultados a Frontier.

El paper de 2026 [Q2RL](https://arxiv.org/abs/2605.05172) utiliza estimaciones de
valor para alternar entre una política aprendida por imitación y otra de RL. Nos
inspira a permitir que un controlador nuevo se abstenga. Nuestro selector es un
conjunto de 64 árboles entrenado con partidas contrafactuales; no reproduce Q2RL,
no usa sus pesos y no hereda sus resultados en robótica. Que un paper sea reciente
no garantiza una mejora en esta competencia.

La implementación propia evalúa ocho construcciones de rutas y plantilla laboral
desde los activos observables. Valora tareas con escenarios de precios que incluyen
la cosecha madura visible del rival; eso no revela su inventario privado. Compara el
valor marginal de un trabajador con su coste Fibonacci, prevé dónde aparecerá cada
contratado y reserva turnos para llevar la mercancía al almacén. También considera
fertilizar y regar antes de cosechar cuando compensa, y vende los productos expuestos
antes de ocupar turnos de mercado con contrataciones. No es un optimizador exacto
ni una garantía de máximo global.

El selector usa 109 variables observables y del plan, sin identidad del rival,
semilla del mundo, datos futuros ni replays en el nuevo controlador. Se entrenó con
288 partidas de 24 semillas; la selección usa otras 96 partidas de ocho semillas.
Las dos opciones parten exactamente de las mismas acciones hasta el turno 695.
El panel reservado y la confirmación oficial usan semillas diferentes. Los resultados
y las limitaciones finales se detallan en `FRONTIER_RESULTS.es.md`.

Los prototipos de reemplazo tardío de trigo por zanahoria quedaron inactivos en las
pruebas: no los incluimos ni presentamos como una mejora. El primer planificador
sin insumos también perdió casos y se conserva como experimento descartado.

Hay dos límites importantes. El simulador C++ discrepa ligeramente del motor oficial
en dos de los 22 replays nuevos; por eso sus resultados son exploratorios y exigimos
confirmación oficial. Además, enfrentar nuestro agente a una secuencia grabada del
líder puede hacer que esa secuencia colapse, porque ya no corresponde al estado
que esperaba. Esas victorias grandes no son victorias contra el agente privado del
líder. Las pruebas de replays se etiquetan únicamente como estrés.

Mantener el repositorio y el notebook privados reduce la copia directa. No hace
incopiable una estrategia, ni prueba una ventaja sostenible. La ventaja que importa
debe medirse contra rivales diversos y en el leaderboard; todavía no hemos demostrado
fuerza de gold. Un siguiente salto mayor requerirá optimizar producción y calendarios
de más días, además de esta mejora terminal.
