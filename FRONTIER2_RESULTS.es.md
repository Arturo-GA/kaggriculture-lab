Frontier: diagnóstico y mejora de entregas — 13 de septiembre de 2026

Se seleccionó `frontier2_early`, que entrega productos valiosos cuando su recorrido
pasa por el almacén y los vende en ese mismo turno. Conserva los insumos necesarios
para las tareas posteriores. La producción anterior al turno 696 sigue siendo la
de Frontier / ml_critic / V37; la modificación afecta al último día.

La consulta de Kaggle a las 2026-09-13T22:50:41.742023+00:00 registró 2347,5 para la última
submission `56214804`, 2501,9 para la anterior y 2650,6 para la primera. Son lecturas
del torneo en ese momento, no puntuaciones finales ni pruebas causales entre versiones.
Se reconstruyeron las observaciones públicas/propias de seis replays de la última
submission: las 719 acciones de cada uno coinciden exactamente con el Frontier local.
Ganó cinco de esas seis partidas. Es una muestra pequeña, no una estimación precisa
de su probabilidad de victoria en el torneo.

El diagnóstico encontró tres oportunidades concretas:

1. Los recorridos podían pasar por el almacén con mercancía y aun así guardarla hasta
   el final. En un caso reproducido, 18 unidades de leche esperaban hasta el turno 718;
   la versión nueva vende 12 en el 704, tres en el 708 y tres en el 718. Esa entrega
   modifica tanto lo que cobramos como el precio al que vende el rival.
2. Varios trabajadores entregaban juntos y saturaban el almacén de 100 unidades.
   La contabilidad de acciones detectó cuatro unidades descartadas en un caso.
   El prototipo que escalonaba rígidamente los finales de ruta introducía derrotas;
   se descartó. La congestión completa del almacén sigue siendo un tema pendiente,
   no se presenta como solucionada universalmente.
3. Un cultivo finito maduro con rendimiento cero todavía puede generar producto si
   admite riego. Se añadió esa tarea y se verificó con el motor oficial. La ablación
   indica que no explica la ganancia de resultados en la muestra exploratoria.

La entrega anticipada usa `PLACE` por producto, en lugar de `DROP`: así no deja también
el fertilizante que necesita el trabajador. La proyección de existencias permite
vender lo colocado en ese mismo turno. El umbral seleccionado es de 250 unidades
monetarias de valor estimado del cargamento por producto, no 250 unidades físicas.
El selector antiguo se entrenó para otra opción y se omite para este controlador
modificado; no se atribuye la ganancia a un entrenamiento nuevo.

En el ejemplo conocido de la semilla 87001 frente a ml_critic, el margen pasó de
−387 a +553. Nuestro dinero final sube 201 y el del rival baja 739. Es un ejemplo
explicativo de la interacción del mercado, usado para diagnóstico, no una partida
reservada ni una garantía de obtener ese beneficio en otros contextos.

| Prueba | Entregas anticipadas: victorias / empates / derrotas | Frontier anterior |
| --- | --- | --- |
| Reservada: 120 casos por candidato, doce semillas y cinco rivales | 109 / 8 / 3 | 87 / 24 / 9 |
| Confirmación oficial: 40 casos por candidato, otras cuatro semillas y cinco rivales | 36 / 4 / 0 | 30 / 10 / 0 |

En el panel reservado la diferencia de resultado es +14,
valorando la victoria en 1 y el empate en 0,5. La media por caso es
0.1167; el intervalo bootstrap por semilla es
[0.03333333333333333, 0.19999999999999998]. En el motor oficial, la diferencia
es +3. Ninguna familia pierde resultado agregado
en esos paneles, aunque sí existen casos particulares en que el cambio empeora.
Las victorias adicionales se concentran frente a nuestras versiones; los resultados
contra router, prvsiyan y kaito se conservan. No se demuestra nivel gold.

Se compararon tres variantes en 120 partidas exploratorias y se congeló la elegida
antes de las semillas reservadas. Otras 60 partidas de ablación comparan el control
constante anterior con una variante nueva que desactiva las entregas intermedias.
Ambos controles dieron recompensas idénticas en 30 contextos.
Activar las entregas aporta +10 puntos de
resultado exploratorio sobre ese control. La ablación explica el efecto observado;
no se utilizó para retocar el candidato después de ver el panel reservado.

El código pasó 24 pruebas, incluyendo conservación de fertilizante después de PLACE,
venta en el mismo turno, recuperación de un cultivo con rendimiento cero, identidad
del prefijo anterior al cambio y del archivo congelado. El máximo del candidato en
la prueba reservada fue 501.2 ms y en la confirmación oficial
348.4 ms, ambos por debajo de 1.000 ms. Los errores de
telemetría reportados son cero; eso no equivale por sí solo a probar que cada orden
ha tenido efecto. El diagnóstico incluye contabilidad de efectos de las acciones.

Los resultados C++ siguen tratándose como exploratorios por las discrepancias
documentadas en la ronda anterior. Las comprobaciones finales usan el motor oficial.
Doce semillas no equivalen a 120 observaciones independientes, y varios rivales
comparten partes de la base pública. Hace falta rendimiento sostenido en el torneo
antes de afirmar una ventaja frente al conjunto real de participantes.

La derrota pública auditada ya tenía una desventaja de 829 monedas al comenzar el
último día y terminó con una desventaja de 624. En ese caso Frontier recuperaba parte
de una desventaja previa. Optimizar producción y calendarios antes del último día
sigue siendo necesario para un salto mayor; esta mejora terminal no sustituye ese trabajo.

El notebook actualizado usa `kaggle_frontier2/` y el mismo kernel privado de Frontier,
conservando su historial. Antes de exportar ejecuta otras 32 partidas oficiales,
con semillas 90001–90004, comparando las dos versiones frente a Frontier y ml_critic.
Exige mejora total positiva y ninguna regresión agregada por rival, ausencia de errores
reportados y llamadas por debajo de 1.000 ms. No envía al leaderboard automáticamente.
