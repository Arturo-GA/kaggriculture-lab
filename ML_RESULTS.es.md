# Modelo de opciones económicas: resultados del 13 de septiembre

El nuevo candidato **ml_critic** mejora las victorias en el panel local reservado:
78/80 frente a 61/80 de matched6. La opción fija de ocho turnos también logra
78/80: el aprendizaje todavía no demuestra más victorias que esa alternativa.
El modelo y todas las semillas se congelaron antes de la prueba final.

La API autenticada de Kaggle confirmó **2656,3** para la submission original
`56190498` el 13 de septiembre. El puesto aproximado 400 y los 3200 del líder
proceden del reporte de Arturo. Estas cifras no son resultados del candidato nuevo.

## Qué se implementó a partir de la investigación

- La [discusión 738079](https://www.kaggle.com/competitions/kaggriculture/discussion/738079)
  propone que el modelo seleccione opciones de alto nivel mientras un ejecutor
  conserva la factibilidad. También propone sustituirlo por una salida constante
  para comprobar su aportación real. Implementamos ambas cosas: selección aprendida
  de una opción de venta y comparación con la mejor opción fija.
- La [discusión 737027](https://www.kaggle.com/competitions/kaggriculture/discussion/737027)
  describe información y ambigüedades del inventario público. El modelo utiliza
  precios, inventario y cambios observados durante 48 turnos, junto con producción
  pública y existencias propias. No reconstruye exactamente el inventario privado
  rival ni utiliza sus valores ocultos.
- [Q2RL, RSS 2026](https://arxiv.org/abs/2605.05172) inspira la comparación del valor
  de intervenir frente a conservar una política base. Aquí esos valores se aprenden
  con continuaciones del simulador; no se implementó el algoritmo Q2RL ni se usaron
  sus pesos. El ejecutor V37 es determinista y no proporciona probabilidades BC.

En el turno 336, el modelo recibe **95 variables observables** y selecciona entre
mantener matched6 o anticipar ventas 2, 8, 12 o 18 turnos durante la ventana
336–647. El ejecutor mantiene las restricciones de existencias, recogidas,
compras futuras y límites del calendario. Fuera de esa ventana conserva matched6.
El bot final utiliza únicamente la biblioteca estándar de Python; no necesita GPU,
scikit-learn ni acceso a internet durante una partida.

El crítico contiene 64 árboles de profundidad máxima 4 y un mínimo de 6 muestras
por hoja. El remuestreo se realiza por semillas completas. Aprende la ventaja
respecto a la política nativa con una utilidad que prioriza victoria/empate/derrota
y añade un término acotado de margen. El umbral y el cuantil se eligieron en
selección; resultaron 0 y 0,1. Este cuantil del conjunto es una heurística de
prudencia, no una garantía probabilística calibrada de seguridad.

## Datos y comparación reservada

| Fase | Semillas | Partidas | Uso |
|---|---|---:|---|
| Piloto | 70001 | 10 | Verificar intervenciones y prefijos |
| Entrenamiento | 71001–71016 | 480 | Ajustar árboles |
| Selección | 72001–72006 | 180 | Elegir umbral y opción fija |
| Prueba final | 73001–73008 | 240 | Comparar modelo, matched6 y opción fija |
| Confirmación oficial | 74001–74004 | 80 | Comparar modelo y matched6 en el motor oficial |

Cada ejemplo compara cinco partidas completas con políticas reactivas y memoria
independiente. Verificamos que las cinco opciones tienen exactamente el mismo
prefijo de acciones y los mismos datos antes de la decisión. El rival continúa
reaccionando a las acciones; no es una reproducción fija de un replay.
Las 480 partidas de entrenamiento corresponden a **96 contextos de decisión**;
las 180 de selección, a 36. No son 660 estados iniciales independientes.

Entrenamiento y selección usan matched6, Shop Router y Nagata. Kaito y Prvsiyan
quedan fuera del entrenamiento de este modelo, aunque ya se habían utilizado en
rondas anteriores del proyecto. Se prueban ambos asientos. Las semillas son grupos
de escenarios y no deben contarse como si ambos asientos fueran independientes.

| Rival, 16 partidas por candidato | matched6: V/E/D | Modelo: V/E/D | Opción fija h8: V/E/D |
|---|---:|---:|---:|
| matched6 | 1/14/1 | 16/0/0 | 16/0/0 |
| Shop Router | 12/0/4 | 14/0/2 | 14/0/2 |
| Nagata | 16/0/0 | 16/0/0 | 16/0/0 |
| Kaito | 16/0/0 | 16/0/0 | 16/0/0 |
| Prvsiyan | 16/0/0 | 16/0/0 | 16/0/0 |
| **Total** | **61/14/5** | **78/0/2** | **78/0/2** |

La diferencia es **17 victorias adicionales** y una mejora de 12,5 puntos
porcentuales al contar cada empate como media victoria. El intervalo percentil
del remuestreo por las ocho semillas es [10; 17,5] puntos. Es una descripción de
este pequeño panel, no una predicción del rating ni una garantía contra otros bots.

El modelo conserva la opción nativa en 20/80 casos y elige h8 en 60/80. Obtiene
las mismas victorias que h8 fija, con un margen medio aproximadamente 47 monedas
mayor. Frente a Prvsiyan ambas variantes reducen el margen en 175 monedas por
partida, aunque mantienen las victorias. La mayor parte de la mejora sigue
concentrada frente a variantes cercanas a nuestro propio agente.

## Verificación y demora detectada

La confirmación con `kaggle-environments==1.32.7` terminó: **40/40 victorias del
modelo frente a 33/40 del control**, que tuvo seis empates y una derrota. Son
cuatro semillas nuevas y los mismos cinco rivales, en ambos asientos. Esta vez
las siete victorias adicionales se concentran frente a matched6. Ningún rival
presenta una caída neta de victorias; no hubo errores ni fallbacks registrados.
La llamada más lenta del modelo fue de **239,5 ms**.

El wrapper nativo reprodujo las 719 acciones del agente original. La exportación
del modelo pasó 8448 comparaciones exactas con scikit-learn; fue necesario reproducir
su conversión de entradas a float32. Las 15 pruebas unitarias distintas del proyecto
pasaron, incluyendo selección del callable correcto y comprobación del modelo congelado.

El resumen original de la prueba acelerada **no pasa el criterio completo**:
una llamada del modelo midió 1003,7 ms frente al límite predefinido de 1000 ms.
El control también registró 1295,2 ms. Esos registros se conservan.

Se diagnosticaron, sin modificar el modelo, los tres contextos más lentos de cada
política en ejecuciones secuenciales. Los seis reprodujeron exactamente sus
recompensas. El máximo del modelo, incluyendo generación de observación, fue
185,4 ms. La demora original no se reprodujo; no se ha probado su causa exacta.
Para preparar la publicación exigimos además que el panel oficial y la ejecución
en Kaggle cumplan por separado el mismo límite de 1000 ms. Esta comprobación
adicional resuelve el hallazgo operativo; no borra el fallo del registro inicial.

## Reproducir y revisar

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-ml.txt
.\.venv\Scripts\python.exe build_ml_policy.py
.\.venv\Scripts\python.exe collect_ml.py --split train --workers 4
.\.venv\Scripts\python.exe collect_ml.py --split selection --workers 4
.\.venv\Scripts\python.exe train_ml.py
.\.venv\Scripts\python.exe -m unittest -v test_experiment.py test_market_gate.py test_ml_policy.py
```

El evaluador acelerado requiere la compilación y verificación descritas en
`RESEARCH_2026_09_12.es.md`. Los rivales descargados se identifican mediante hashes
en los recibos; sus fuentes no se incluyen en el bot ni en el nuevo notebook.
`results/ml/training_policy.py` conserva la fuente exacta de los candidatos
forzados que generaron los datos. La selección del modelo nunca recibe semillas,
identificadores de rival, observaciones futuras ni inventarios privados ajenos.

Recibos principales: `results/ml/training.json`, `holdout_summary.json`,
`latency_diagnosis.json`, `official_summary.json` y `release_plan.json`.
Las predicciones y semillas del modelo no se reajustan con la prueba final.

El nuevo kernel se prepara por separado para conservar el primer experimento:
[Kaggriculture Learned Option Critic](https://www.kaggle.com/code/jarturo/kaggriculture-learned-option-critic).
Su ejecución valida antes de producir `submission.tar.gz`; no realiza una
submission al leaderboard automáticamente.
