# Kaggriculture Lab

Investigación y experimentos para Kaggriculture sobre el V37 compartido por Arturo.
Repositorio privado. Primer candidato: **matched6**, que anticipa ventas seis turnos
solo cuando la granja rival mantiene una semejanza alta con la propia.

- [Investigación: competencias similares y papers 2025–2026](RESEARCH.es.md)
- [Resultados y limitaciones](RESULTS.es.md)
- [Kernel privado en Kaggle](https://www.kaggle.com/code/jarturo/kaggriculture-lab-cpu-search)
- [Atribuciones y cambios](NOTICE.md)

En la confirmación local, matched6 ganó 18/18 partidas contra tres rivales.
El panel es pequeño y parte de la mejora se concentra frente a V37; no demuestra
un rating superior a 3000. Frente a prvsiyan conserva victorias pero reduce margen.

Kaggle **v2 COMPLETE**: otras 8/8 victorias frente a V37 en semillas nuevas,
con margen medio +1249,50 monedas. Se verificó la identidad del agente exportado.
Hay 162 partidas documentadas, incluyendo controles y exploración repetida.

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
