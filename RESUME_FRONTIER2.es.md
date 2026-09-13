Estado de la mejora de Frontier — 13 de septiembre de 2026

Arturo pidió revisar qué mejorar a partir del rendimiento actual. Se auditó la
submission `56214804` y se reprodujeron sus 719 acciones en seis partidas públicas;
coinciden con el Frontier local. Ganó cinco y perdió una. Instantánea del rating:
2347,5 a las 22:50 UTC; no es una puntuación final.

Se seleccionó `candidates/frontier2_early.py`, SHA-256
`0bb0cddbb6e3883850138cbbd3dfc39e5fa285fd83c356a0e02391bebdbff33c`.
Entrega productos al pasar por el almacén mediante PLACE, conserva fertilizante
y vende en ese mismo turno. La producción anterior al turno 696 es idéntica.
El selector antiguo se omite para la opción modificada. No hay entrenamiento nuevo.

- Exploración: 120 partidas, tres variantes y control. Se elige la entrega con
  umbral 250; se descartan la de umbral 600 y el escalonamiento rígido.
- Ablación: 60 partidas. Desactivar las entregas reproduce el planificador constante
  anterior en 30 contextos; la entrega explica +10 puntos de resultado exploratorio.
- Reservada: 240 partidas. Nuevo 109/8/3 frente a 87/24/9; doce semillas, cinco rivales.
- Oficial: 80 partidas. Nuevo 36/4/0 frente a 30/10/0; otras cuatro semillas.
- 24 pruebas de código aprobadas. Latencia seleccionada bajo 1.000 ms en ambos paneles.
- `FRONTIER2_RESULTS.es.md` conserva hallazgos, cifras y limitaciones.
- El notebook inicial superó 1 MB y Kaggle lo rechazó. Se cambió sólo la compresión
  del paquete a LZMA; sus archivos son idénticos por bytes. Tamaño final 362.606 bytes.
- El kernel privado `jarturo/kaggriculture-frontier-joint-planner` recibió la versión 2.
  Directorio actual: `kaggle_frontier2/`; versiones anteriores archivadas por separado.
- **COMPLETE y verificada** la versión 2: `verify_frontier2_cloud.py` aprobado.
  Contra Frontier: 5 victorias, 2 empates y 1 derrota; contra ml_critic: 7 victorias
  y 1 derrota. Diferencia emparejada de resultado +2 por rival. Máximo 267,7 ms.
  Archivo `results/frontier2/kaggle/submission.tar.gz`, SHA-256
  `adcab448c1ed6db9b52c1af1f48f52d1ca13aaa2fff8abf5557da81e7ab9427d`.
  La política descargada es idéntica al candidato local congelado.

No se envió automáticamente al leaderboard. No crear automatizaciones ni continuar
experimentos nuevos sin petición. El control completo de la saturación del almacén
y los calendarios de producción anteriores al último día siguen pendientes como
líneas de investigación; no se ha demostrado nivel gold.
