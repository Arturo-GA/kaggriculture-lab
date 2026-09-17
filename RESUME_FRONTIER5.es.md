Frontier5 — 17 de septiembre de 2026
Base: V46 público de Ahmed Berat Özer (SHA-256 735c370383b70d3bf3aac792f2c147e0afc99166fc9f253ede10e8a030acedb6), extraído como datos con extract_public_agents.py (modo auto); no está en Git.
Candidato congelado: candidates/f5_lock.py = V46 + frontier5_lockstep.py (orden lockstep de ventas contra copia). Hash en results/frontier5/selection.json y results/frontier5/build.json. Reconstruir: v46 + frontier5_lockstep.py (ver test_frontier5.py). f5_lockterm (con capas terminales) se congeló primero y se descartó: en la semilla oficial 5821 el planificador terminal perdió el último día por 4150.
Diagnóstico de la ronda y análisis del top: FRONTIER5_RESULTS.es.md.
Semillas consumidas: 5601-5612 (pantallas y gansos), 5741-5748 (selección f5), 5761-5768 y 5821-5824 (f5_lockterm, descartado), 5771-5778 (holdout f5_lock), 5831-5834 (oficial f5_lock), 5921-5922 (nube). No reajustar sobre ellas.
Descartado: frontier5_geese.py (gansos por vacas/ovejas tardías: negativo, −700 a −33k en 6 de 8 mundos). f4_probe queda obsoleto: pierde 1/11 contra V46 y 0/12 contra Beyond-48.
Empaquetado: make_frontier5_notebook.py → kaggle_frontier5/ → kernel jarturo/kaggriculture-frontier5-lockstep → verify_frontier5_cloud.py → submit_frontier5.py (--submit solo con petición explícita).
Seguimiento en vivo: python live_report.py <submission_id> ...
Datos comunitarios: vendor/episodes_ds (dataset georgymamarin/kaggriculture-episodes, tablas csv) y replays propios en vendor/live_f4, vendor/live_top; todo fuera de Git.
Siguiente salto real: clonar la cinta de un top-10 con cinta propia (Sida Zuo: 373 replays públicos de la submission 56177113) y montarla en el chasis V46; o economía propia (reinversión temprana tipo SpaTaro).
No crear automatizaciones ni iniciar nuevas rondas sin petición.
Kaggle verificado: True (results/frontier5/kaggle_verified.json, archivo 3d80ca6e…).
Envío al leaderboard con recibo: True. Arturo autorizó el 17 de septiembre ("prosigue porfavor"): submission 56292870 ("Frontier5 lockstep 150e8e17 on V46", results/frontier5/submission_receipt.json) y segunda plaza con el mismo archivo ("... - second slot", results/frontier5/submission_receipt_2.json). Ambas Frontier4 dejan de estar en seguimiento. No enviar más copias; refrescar estado con `python submit_frontier5.py` (sin --submit).
