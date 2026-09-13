# Pausa solicitada por Arturo — 12 de septiembre de 2026

**Retomado el 13 de septiembre por petición de Arturo.** Esta nota conserva el
punto de pausa histórico; consultar `ML_RESULTS.es.md` para los resultados nuevos.

Arturo pidió detener los experimentos y apagar la laptop para continuar mañana.
No reanudar automáticamente ni crear una tarea programada.

## Guardado

- Modelo de opciones económicas entrenado: `results/ml/model.json` y `candidates/ml_critic.py`.
- 480 partidas de entrenamiento, 180 de selección y 10 de piloto completas.
- `results/ml/training.json` registra datos, hashes, selección y versiones.
- Selección: 12 empates contra matched6 pasan a victorias; sin cambios de victorias contra router y nagata. La opción fija ml_h8 obtiene las mismas victorias; aún no se demuestra ventaja del aprendizaje sobre esa opción.
- 8448 predicciones exportadas iguales a sklearn tras corregir la conversión float32 en `ml_policy.py`.
- `results/ml/native_parity.json`: 719 acciones del wrapper nativo idénticas a matched6.
- Pruebas anteriores de `test_ml_policy.py`: 3 aprobadas. La última ejecución conjunta de tests fue interrumpida antes de confirmar su resultado.
- No se ha reemplazado el agente publicado, ni enviado una submission nueva.

## Pendiente al retomar

1. Revisar si existe `results/ml/holdout.json` y su campo `complete`. Al solicitarse la pausa no se encontró ese archivo. La llamada para iniciar la prueba final fue interrumpida.
2. Ejecutar `python -m unittest -v test_experiment.py test_market_gate.py test_ml_policy.py` desde la venv.
3. Prueba final predefinida, sin modificar el modelo según sus resultados:

```powershell
.\.venv\Scripts\python.exe evaluate_fast.py --candidates ml_critic matched6 ml_h8 --opponents matched6 router nagata kaito prvsiyan --seeds 73001 73002 73003 73004 73005 73006 73007 73008 --workers 4 --output results/ml/holdout.json
.\.venv\Scripts\python.exe summarize_ml.py results/ml/holdout.json --output results/ml/holdout_summary.json
```

4. Si pasa los criterios de `results/ml/plan.json`, confirmar con el motor oficial y las semillas 74001–74004 antes de preparar un kernel de Kaggle. Comparar también contra la opción fija y describir honestamente si el modelo aporta una ventaja adicional.
5. Escribir el informe con resultados y fuentes, completar commit/push y preparar candidato si corresponde.

## Fuentes aplicadas

- https://www.kaggle.com/competitions/kaggriculture/discussion/738079 — opciones de alto nivel, ejecutor y ablación con salida constante.
- https://www.kaggle.com/competitions/kaggriculture/discussion/737027 — inventario público e incertidumbre; esta versión usa cambios observables del mercado, sin atribuirse una reconstrucción exacta del inventario rival.
- https://arxiv.org/abs/2605.05172 — inspiración de selección por valor; no reproducción de Q2RL.

Los candidatos forzados conservan el código anterior a la corrección float32 del evaluador de árboles, que no utilizan. Su fuente exacta quedó preservada en `results/ml/training_policy.py`; el constructor la usa para reproducir los hashes originales del dataset.
