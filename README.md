# Kaggriculture Lab

Investigación y experimentos para Kaggriculture sobre el V37 compartido por Arturo.
Repositorio privado. Primer candidato: **matched6**, que anticipa ventas seis turnos
solo cuando la granja rival mantiene una semejanza alta con la propia.

- [Investigación: competencias similares y papers 2025–2026](RESEARCH.es.md)
- [Resultados y limitaciones](RESULTS.es.md)
- [Diagnóstico del rating y 192 partidas adicionales](LIVE_DIAGNOSIS.es.md)
- [Papers recientes, cinco prototipos y simulación 8,72× más rápida](RESEARCH_2026_09_12.es.md)
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

## Reproducir

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
