Estado de Frontier — 13 de septiembre de 2026

Arturo pidió un agente con más desarrollo propio y análisis de equipos del rango
gold. La implementación y la validación local están terminadas. Ver
`GOLD_RESEARCH.es.md` y `FRONTIER_RESULTS.es.md`.

- Candidato: `candidates/frontier.py`; SHA-256
  `a485d1c0a44ae989417b39178defa5096837b03b850a7bc8db8b6458599dad1c`.
- Planificador terminal propio sobre la política de producción de ml_critic/V37.
  No incorpora los prototipos de cambio de cultivo, que no se activaron.
- Entrenamiento 288 partidas; selección 96. Panel reservado 240 partidas de tres
  candidatos, más 80 repeticiones tras corregir sólo la telemetría. Resultados iguales
  en las 80 repeticiones. Confirmación oficial 80 partidas y estrés reservado 24.
- `frontier_holdout_summary.json` conserva el fallo original de latencia C++.
  La repetición oficial en serie y el panel oficial pasan; recibo `frontier_latency.json`.
- El selector no supera en victorias reservadas a la ablación constante.
  Las victorias adicionales frente a ml_critic no prueban fuerza de gold.
- GitHub privado: `Arturo-GA/kaggriculture-lab`.
- Notebook privado nuevo, versión 1, enviado:
  https://www.kaggle.com/code/jarturo/kaggriculture-frontier-joint-planner .
  Debe completar 32 partidas en la nube y pasar `verify_frontier_cloud.py`.
- Los dos kernels anteriores y los archivos de la raíz se conservan. No enviar al
  leaderboard automáticamente: Arturo ha hecho las submissions manualmente.
- No crear automatizaciones ni reanudar experimentos posteriores sin petición.

Para avanzar estratégicamente, optimizar calendarios y producción de más días con
rivales reactivos diversos. Los replays gold son secuencias fijas y nunca deben
interpretarse como haber derrotado al agente privado original.
