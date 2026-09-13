# Kaggriculture Lab

Investigación y experimentos para Kaggriculture sobre el V37 compartido por Arturo.
Repositorio privado. Primer candidato: **matched6**, que anticipa ventas seis turnos
solo cuando la granja rival mantiene una semejanza alta con la propia.

- [Investigación: competencias similares y papers 2025–2026](RESEARCH.es.md)
- [Resultados y limitaciones](RESULTS.es.md)
- [Diagnóstico del rating y 192 partidas adicionales](LIVE_DIAGNOSIS.es.md)
- [Papers recientes, cinco prototipos y simulación 8,72× más rápida](RESEARCH_2026_09_12.es.md)
- [Modelo entrenado, validación reservada y nuevo candidato](ML_RESULTS.es.md)
- [Análisis de ocho equipos del top 27 y planificador propio](GOLD_RESEARCH.es.md)
- [Frontier: resultados, ablaciones y límites](FRONTIER_RESULTS.es.md)
- [Mejora de Frontier: entregas durante la ruta y validación nueva](FRONTIER2_RESULTS.es.md)
- [Kernel privado en Kaggle](https://www.kaggle.com/code/jarturo/kaggriculture-lab-cpu-search)
- [Atribuciones y cambios](NOTICE.md)

En la confirmación local, matched6 ganó 18/18 partidas contra tres rivales.
El panel es pequeño y parte de la mejora se concentra frente a V37; no demuestra
un rating superior a 3000. Frente a prvsiyan conserva victorias pero reduce margen.

Kaggle **v2 COMPLETE**: otras 8/8 victorias frente a V37 en semillas nuevas,
con margen medio +1249,50 monedas. Se verificó la identidad del agente exportado.
Esa primera ronda documentó 162 partidas, incluyendo controles y exploración repetida.

**Actualización del 12 de septiembre, 18:40 UTC:** la submission `56190498`
marca **1885,9**; las cinco primeras partidas públicas auditadas fueron victorias.
El 687 comunicado al inicio era una lectura temprana. La segunda ronda añade
192 partidas y descarta reemplazar todas las rutas por la biblioteca de 14 planes:
introduce derrotas frente a otro rival. Se conserva matched6; no se promete un
rating final ni se ha enviado automáticamente otro agente.

La ronda posterior al rating 2100 comunicado por Arturo añade **248 partidas
válidas**, cinco prototipos de decisión de venta y un evaluador C++ opcional.
En tres comparaciones completas, el evaluador fue **8,72× más rápido** y reprodujo
recompensas, tiendas y telemetría. Los prototipos no añadieron victorias; se mantiene
matched6. Hay 602 partidas de estrategia documentadas entre las rondas, con
controles y repeticiones; las pruebas de equivalencia se cuentan aparte.

**13 de septiembre:** la submission original marca **2656,3** en la API de Kaggle.
El nuevo modelo `ml_critic` obtiene 78/80 victorias en la prueba reservada frente
a 61/80 de matched6 (con 14 empates). La opción fija h8 también obtiene 78/80;
todavía no se demuestra una ventaja de victorias del aprendizaje sobre ella.
El [informe de esta ronda](ML_RESULTS.es.md) conserva los detalles y el diagnóstico
de latencia. El nuevo experimento utiliza `kaggle_ml/` y un kernel privado separado.
Confirmación oficial: 40/40 victorias frente a 33/40 del control. El
[nuevo kernel privado](https://www.kaggle.com/code/jarturo/kaggriculture-learned-option-critic)
está **COMPLETE** y ganó otros 8/8 duelos. Archivo nuevo verificado:
[`results/ml/kaggle/submission.tar.gz`](results/ml/kaggle/submission.tar.gz).
La raíz conserva los archivos del primer agente; no se envió otra submission
automáticamente al leaderboard.

## Reproducir

**Frontier, versión 2: entregas durante la ruta.** `frontier2_early` entrega y vende
productos valiosos al pasar por el almacén, conservando fertilizante para después.
El panel reservado obtiene 109 victorias, 8 empates y 3 derrotas frente a 87, 24 y 9
de Frontier. La confirmación oficial obtiene 36 victorias y 4 empates frente a
30 victorias y 10 empates. Las 24 pruebas pasan. Ver `FRONTIER2_RESULTS.es.md`.
El notebook actualizado se genera en `kaggle_frontier2/`; la carpeta anterior
`kaggle_frontier/` conserva el experimento de la versión 1. La versión 2 se subió al
mismo kernel privado y exige una nueva comparación en la nube antes de exportar.
No se envía una submission al leaderboard automáticamente.

**Nueva ronda del 13 de septiembre: Frontier.** Planificador propio del último día:
contratación, fertilizante, cosecha, rutas y ventas, con selector entrenado. Conserva
la producción anterior de V37 / ml_critic. Panel reservado: 76 victorias y 4 derrotas
frente a 64 victorias, 12 empates y 4 derrotas del control. Confirmación oficial:
38 victorias y 2 derrotas frente a 32 victorias y 8 empates. La mejora de resultados
se concentra contra nuestra versión anterior; la ablación constante obtiene las
mismas victorias reservadas que el selector. No se ha demostrado nivel gold.

El [nuevo notebook privado](https://www.kaggle.com/code/jarturo/kaggriculture-frontier-joint-planner)
usa `kaggle_frontier/` y comprueba 32 partidas adicionales antes de exportar. Los
replays del top se usan sólo como estrés; no equivalen a sus agentes privados.
Dos replays nuevos exponen pequeñas discrepancias del simulador C++; se exige motor
oficial. El informe conserva también el pico de latencia y su diagnóstico en serie.

**Kaggle COMPLETE, versión 1:** archivo
[`submission.tar.gz` verificado](results/gold/kaggle/submission.tar.gz).
En la nube ganó 8/8 contra matched6 y 4/8 contra ml_critic, con un máximo de 299,6 ms
por llamada. El resultado agregado de esas partidas es igual al del control; no
replica la ganancia local ni demuestra una ventaja general. Se conserva como
candidato experimental, sin envío automático al leaderboard. Las 19 pruebas pasan.

Para regenerar el candidato congelado, ejecutar `build_frontier.py --model
results/gold/frontier_model.json`. Las variantes exploratorias conservan sus fuentes
y recibos originales; los builders actuales regeneran la última familia del experimento.
Las pruebas de Frontier se ejecutan con `python -m unittest test_frontier.py`.

Python 3.12. El agente usa solo la biblioteca estándar; no necesita GPU.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe build.py
.\.venv\Scripts\python.exe -m unittest -v test_experiment.py
.\.venv\Scripts\python.exe evaluate.py --candidates matched6 --opponents v37 --seeds 93001 93002 --workers 2 --output results/new_check.json
```

El entorno de desarrollo inicial instaló el paquete del motor sin dependencias
adicionales sobre bibliotecas ya disponibles. En una instalación limpia, usar
`requirements.txt` para resolver sus dependencias completas.

Para repetir el panel externo, descargar los notebooks con `kaggle kernels pull`
según `results/opponents.json`, en `vendor/nagata`, `vendor/tetsutani` y
`vendor/prvsiyan`, y ejecutar `python extract_opponents.py`. Los exports públicos
pueden cambiar; verificar los hashes antes de comparar con estos resultados.

## Ejecutar en Kaggle

```powershell
python make_notebook.py
python -m kaggle kernels push -p kaggle
python -m kaggle kernels status jarturo/kaggriculture-lab-cpu-search
```

El notebook realiza búsqueda exploratoria y validación separada, registra ambas,
y empaqueta matched6 si pasa el control; en caso contrario exporta V37.
Produce `main.py`, `submission.tar.gz` y resultados JSON. No envía automáticamente
a la competencia. Los pesos de una red y el entrenamiento RL quedan como hipótesis
de investigación, no como capacidades implementadas.

`baseline/v37.py` conserva el hash y las atribuciones del notebook original.
`build.py` define exactamente las intervenciones; `evaluate.py` ejecuta rivales
que reaccionan, con instancias de política independientes y ambos asientos.
No se accede al almacén privado del rival ni a semillas ocultas desde el agente.

## Experimentos de mercado y evaluador opcional

El agente enviado sigue usando solo Python estándar. Para reconstruir los
prototipos y ejecutar sus pruebas:

```powershell
python build_market_gate.py
python build_market_gate.py --funded
python build_market_gate.py --lead
.\.venv\Scripts\python.exe -m unittest -v test_market_gate.py
```

El acelerador se compiló con MinGW g++ 14.2.0 en esta estación Windows. Requiere
los rivales del panel anterior para ejecutar la verificación.

```powershell
git clone https://github.com/destbreso/kaggriculture-cppsim.git vendor/cppsim
git -C vendor/cppsim checkout da15925dcf2357d750cbae4bf35712011b4733c8
.\.venv\Scripts\python.exe -m pip install -r requirements-accelerator.txt
.\.venv\Scripts\python.exe build_cppsim.py
.\.venv\Scripts\python.exe verify_accelerator.py
.\.venv\Scripts\python.exe benchmark_accelerator.py
.\.venv\Scripts\python.exe evaluate_fast.py --candidates belief_lead12 matched6 --opponents matched6 router prvsiyan kaito --seeds 64001 64002 64003 64004 64005 64006 64007 64008 --workers 4 --output results/market_lead_holdout.json
python summarize_market.py
```

La revisión del simulador está fijada. Cambiarla exige reconstruir y volver a
verificar; una compilación distinta puede producir un hash de binario distinto.
Para confirmar resultados competitivos se conserva `evaluate.py`, con el motor
oficial. El kernel anterior no incorpora automáticamente estos prototipos.
