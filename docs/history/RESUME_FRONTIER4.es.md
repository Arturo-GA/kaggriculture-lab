Frontier4 — 16 de septiembre de 2026
Base: V45 público de Ahmed Berat Özer (SHA-256 2536d41ed5a00c75204b6350f1c76c54259c774cb065ba2a3a0072eedf210d94), extraído como datos con extract_public_agents.py; no está en Git.
Candidato congelado: candidates/f4_probe.py (V45 + sonda de carrera de ventas; sin capas terminales); su hash vive en results/frontier4/selection.json y results/frontier4/build.json. Reconstruir con build_f4.py (exige el hash de V45).
Cambio en la base: sonda de carrera (_F4_PROBE_LEVEL=24 hasta el turno 336; confirmación por ventas netas del rival de productos que nuestra cinta vende >4 turnos después; si no hay evidencia vuelve al horizonte 8 de V45). Capas terminales propias (frontier4_layers.py + frontier4_ml_support.py) medidas y NO exportadas.
Diagnóstico que motivó la ronda: FRONTIER4_RESULTS.es.md (carrera de ventas contra clones; Frontier3 perdía 0/12 contra V43/V44/V45).
Semillas consumidas: 5601–5638 y 5741–5758 (selección), 5701–5708 y 5801–5804 (f4_full, descartado), 5721–5728 (holdout f4_probe), 5811–5814 (oficial f4_probe), 5901–5902 (nube). No reajustar sobre ellas.
Descartado y documentado: f4_runner.py (manos extra "corredoras"); f4_r24/f4_adapt (horizonte fijo 24: pierde contra clones que venden a 4 turnos); f4_term/f4_full (capas terminales: sin ganancia en 32 partidas por par); f4_r24b/f4_fullb (sin tope de bloque en la reserva).
Empaquetado: make_frontier4_notebook.py → kaggle_frontier4/ → kernel jarturo/kaggriculture-frontier4-sales-race → verify_frontier4_cloud.py → submit_frontier4.py (--submit solo con petición explícita).
Seguimiento en vivo (solo lectura): python live_report.py <submission_id> ...
No crear automatizaciones ni iniciar nuevas rondas sin petición.
Kaggle verificado: True (results/frontier4/kaggle_verified.json, archivo 172daa82…).
Envío al leaderboard con recibo: True. Arturo autorizó el 16 de septiembre ("si haz todo lo que dijiste"); submission 56266564, descripción "Frontier4 sales race f426240e on V45", recibo en results/frontier4/submission_receipt.json. Consultar ese ID antes de cualquier intento nuevo para evitar duplicados; refrescar estado con `python submit_frontier4.py` (sin --submit).
Segunda plaza: Arturo pidió enviar el mismo archivo otra vez ("haz el submission en kaggle de lo que dices"); submission 56266648, descripción "... - second slot", recibo en results/frontier4/submission_receipt_2.json. Las dos plazas activas son ahora Frontier4 (56266564 y 56266648); Frontier3 dejó de estar en seguimiento. No enviar más copias.
