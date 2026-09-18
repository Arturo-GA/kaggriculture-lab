# Kaggriculture Lab

Investigación y experimentos para Kaggriculture sobre el V37 compartido por Arturo.
Repositorio privado. Primer candidato: **matched6**, que anticipa ventas seis turnos
solo cuando la granja rival mantiene una semejanza alta con la propia.

**18 de septiembre: Frontier7 (lockstep sobre V48) y el análisis del top 2.** Frontier5 subió a
2751 (puesto 238) y empezó a caer: 8/24 en sus partidas contra rivales de 2800 o más, casi todas
contra clones de V47/V48 (17 de septiembre), que integran el pre-guardia nocturno, un orden lockstep
propio y el rebaño según tiendas de Seyit Kaan Güneş; V48 gana 10/2 a f5_lock y 12/0 a V46 en nuestro
simulador. El análisis de Unknown Mother-Goose (#1, 106 replays) está en
[FRONTIER7_RESULTS.es.md](FRONTIER7_RESULTS.es.md): contra 79 clones gana 75 con +13255 de media con
la misma mano de obra y las mismas cosechas, pero vende fresa, leche y lana un 30-40 % más caras
(producción más temprana y lotes constantes) y añade tomates, zanahorias y huevos. Con el modelo exacto
del mercado del motor se midió la palanca de "retener y dosificar" leche y lana
(`frontier7_hold.py`): el almacén de la cinta no deja sitio (80 de 100 al amanecer, 66 unidades en manos
por la noche) y la capa pierde 1/11 contra V48; descartada. Superar al top 2 exige una economía propia
(planificador), no un envoltorio. Candidato inmediato `candidates/f7_lock.py` = V48 público (hash
fijado en `build_f7.py`, punto de entrada `_e335_agent`) + `frontier5_lockstep.py`: 11/1 contra V48
(+1124) en pantalla, holdout C++ 16/0 contra los 12 rivales (V48 +922, f5_lock +1283), motor oficial
8/0 contra V48 (+861) y Kaggle 4/0 contra V48, Beyond-48 y f5_lock (archivo verificado,
`results/frontier7/kaggle_verified.json`). Arturo pidió una plaza: **submission 56318681** (recibo en
`results/frontier7/submission_receipt.json`); la otra plaza sigue con Frontier5. Notas:
[RESUME_FRONTIER7.es.md](RESUME_FRONTIER7.es.md).

```powershell
python extract_public_agents.py        # V48 y rivales públicos desde vendor/pub/ (kaggle kernels pull)
python build_f7.py                     # f7_lock (exportable), f7_hold y f7_holdonly (descartados) desde el V48 fijado
python -m unittest -v test_frontier7.py
python make_frontier7_notebook.py; python -m kaggle kernels push -p kaggle_frontier7
python verify_frontier7_cloud.py       # tras `kaggle kernels output ... -p results/frontier7/kaggle`
python submit_frontier7.py             # estado; --submit --authorization "..." solo con petición explícita
```

**17 de septiembre: Frontier5 (orden lockstep sobre V46).** Las Frontier4 llegaron a plata (2674,
puesto 437) y empezaron a caer: la ola pública del 16 de septiembre (pipe-7/8, Beyond-48, V46) gana
el turno 0-1 por microestructura de órdenes y nos cuesta ~1300 monedas antes del día 12; V46 gana 11/1
a todos los demás públicos y f4_probe pierde 1/11 contra ella. El análisis del top (dataset comunitario
de partidas y 56 replays propios) está en [FRONTIER5_RESULTS.es.md](FRONTIER5_RESULTS.es.md): las plazas
12-40 son clones de nuestra cinta con esos ajustes; el top 2-10 usa cintas propias (reinversión temprana,
9-10 vacas, zanahorias y tomates tardíos); en los espejos leche, lana y fresa se saturan y solo el huevo
aguanta. El candidato `candidates/f5_lock.py` = V46 público (hash fijado) + orden lockstep de ventas
propio (`frontier5_lockstep.py`): contra una copia reproduce la liquidación unidad a unidad del motor y
elige la permutación de ventas con mejor margen. Holdout C++ (semillas nuevas, 12 rivales): 16/0 contra
todos, V46 +1083, Beyond-48 +1202, pipe-7 +940, pipe-8 +1448; motor oficial 8/0 contra seis rivales
incluida V46 (+965). Descartados con medición: gansos por vacas/ovejas (`frontier5_geese.py`) y las
capas terminales sobre V46 (pierden el último día en el motor oficial). Arturo pidió el envío: **submission
56292870** y una segunda copia en la otra plaza (recibos en `results/frontier5/submission_receipt*.json`).
Notas: [RESUME_FRONTIER5.es.md](RESUME_FRONTIER5.es.md).

```powershell
python extract_public_agents.py        # V46 y rivales públicos desde vendor/pub/ (kaggle kernels pull)
python build_f5.py                     # variantes Frontier5 desde el V46 fijado
python -m unittest -v test_frontier5.py
python make_frontier5_notebook.py; python -m kaggle kernels push -p kaggle_frontier5
python verify_frontier5_cloud.py       # tras `kaggle kernels output ... -p results/frontier5/kaggle`
```

**16 de septiembre: Frontier4 (sonda de carrera de ventas).** Las dos Frontier3 activas
(`56222986`, `56223026`) cayeron a 50 % de victorias y ~2540 de rating (puesto 710) porque el
pool de 2500-2900 son clones del linaje público V41-V45 y nuestra base V37 pierde la carrera de
ventas del mismo turno: 0/12 contra V43, V44 y V45 en simulación. El nuevo candidato
`candidates/f4_probe.py` se construye sobre el V45 público (extraído como datos, hash fijado) y
añade una sonda al horizonte de carrera que gana el espejo contra V44/V45 sin perder contra
clones de 4 turnos: 149/160 puntos frente a 138 de V45 en selección, holdout 416 partidas sin
regresión (11/5 contra V45, 16/0 contra otros 11 rivales) y motor oficial 8/0 contra cinco
rivales y 6/2 contra V45, latencia máxima 157 ms. Diagnóstico, variantes descartadas (manos
corredoras, horizonte fijo, capas terminales) y límites: [FRONTIER4_RESULTS.es.md](FRONTIER4_RESULTS.es.md);
notas de continuidad: [RESUME_FRONTIER4.es.md](RESUME_FRONTIER4.es.md). Verificación en la nube:
kernel privado `jarturo/kaggriculture-frontier4-sales-race`. Arturo pidió el envío: **submissions 56266564 y 56266648**
(mismo archivo, recibos en `results/frontier4/submission_receipt*.json`); ninguna submission se envía automáticamente.

```powershell
python extract_public_agents.py        # tras `kaggle kernels pull` de los notebooks públicos a vendor/pub/
python build_f4.py                     # candidatos Frontier4 desde el V45 fijado
python -m unittest -v test_frontier4.py
python make_frontier4_notebook.py; python -m kaggle kernels push -p kaggle_frontier4
python verify_frontier4_cloud.py       # tras `kaggle kernels output ... -p results/frontier4/kaggle`
python live_report.py 56222986 56223026
```

**14 de septiembre: Frontier3 experimental.** Actualiza la apertura comercial,
reserva dinero y semillas, y distribuye la capacidad compartida del almacén.
Ganó 8/8 contra nuestra primera submission y 8/8 contra Frontier2 en el bloque
oficial local; contra V41 obtuvo 3/8 y **no alcanzó el criterio original de 50 %**.
La publicación experimental conserva ese fallo y no garantiza una mejora de rating.
Estado de Kaggle, archivo y resultados completos: [FRONTIER3_RESULTS.es.md](FRONTIER3_RESULTS.es.md).
La versión 3 del notebook está COMPLETE y su archivo fue verificado por bytes.
En la nube ganó 4/4 contra matched6, 4/4 contra Frontier2 y 2/4 contra V41.
Arturo pidió el envío: submission **56222986**; el último estado consultado está en
`results/frontier3/submission_receipt.json`. Archivo:
[`results/frontier3/kaggle/submission.tar.gz`](results/frontier3/kaggle/submission.tar.gz).

- [Investigación: competencias similares y papers 2025–2026](RESEARCH.es.md)
- [Resultados y limitaciones](RESULTS.es.md)
- [Diagnóstico del rating y 192 partidas adicionales](LIVE_DIAGNOSIS.es.md)
- [Papers recientes, cinco prototipos y simulación 8,72× más rápida](RESEARCH_2026_09_12.es.md)
- [Modelo entrenado, validación reservada y nuevo candidato](ML_RESULTS.es.md)
- [Análisis de ocho equipos del top 27 y planificador propio](GOLD_RESEARCH.es.md)
- [Frontier: resultados, ablaciones y límites](FRONTIER_RESULTS.es.md)
- [Mejora de Frontier: entregas durante la ruta y validación nueva](FRONTIER2_RESULTS.es.md)
- [Revisión del V41: apertura vulnerable, fallos reales y comparación oficial](V41_REVIEW.es.md)
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

**Versión 2 COMPLETE y verificada en Kaggle:** 5 victorias, 2 empates y 1 derrota
frente a Frontier; 7 victorias y 1 derrota frente a ml_critic. Mejora de resultado
emparejado +2 para cada rival, con máximo de 267,7 ms por llamada. Archivo nuevo:
[`results/frontier2/kaggle/submission.tar.gz`](results/frontier2/kaggle/submission.tar.gz).
Arturo la envió al leaderboard como `56216380`. La consulta del 14 de septiembre
a las 05:01 UTC registra 2613,3; ver `V41_REVIEW.es.md` para el diagnóstico posterior.
Los archivos de la versión 1 se conservan.

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
