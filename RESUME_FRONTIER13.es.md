Frontier13 — 25 de septiembre de 2026
Motivo: Arturo pidió una nueva tanda de dos envíos con objetivo de plata al cierre, revisando repositorios públicos (GitHub, foro, código abierto). Las dos copias del enrutador F12 estaban en 2246/2199 (corte de plata 2427).
Estudio (workflow de 5 investigadores + crítico; outputs/session/gold/research_0925/): notebooks actualizados tras el cierre (vendor/pub0925, candidates/n25_*), 14 datasets (vendor/ds25, candidates/d25_*), ~120 repos de GitHub (vendor/gh25, candidates/g25_*), foro, y 172 replays de partidas en vivo contra rivales de 2300+ (vendor/live_f12). Hallazgo: cha22 (route-replay, abhinav0370/cha22-agent = tetsutani demand-preserving = guruprasaathas master engine v3 = evgendvorkin; Apache-2.0; sha 127ed3e6…) domina: 33 equipos lo juegan; el grupo "BUY 5 trigo / 1 semilla" nos ganó 61 de 67 en vivo; ALLAI 0,998 de coincidencia.
cha22 contra el campo (9111-9114): 56/56; cha22 + lockstep 60/60 (4/4 contra cha22); enrutador F12 36,5/56 y 0/4 contra cha22.
Candidato: candidates/f13_c22_lock.py = cha22 + frontier5_lockstep.py enlazado a ig_agent (build_f13.py), sha 831952068d102bfefe413091b6cc2aa0b6fbe7cc0b870ab2dfe139be2b861d8a.
Holdout registrado (results/frontier13/plan.json, 9141-9148, 16 rivales incl. familias débiles): 251/256 frente a 234/256 de cha22; emparejado +11, espejo 15/16, 507 ms. La variante f13x_c22_br (nivel 2 sobre la capa D) 245/256, no se exporta.
Repetición de 166 partidas en vivo con rival congelado: 29 → 99 victorias (2300-2400 9→42/57, 2400-2500 10→36/60, 2500-2600 6→17/32, 2600+ 4→4/17).
Kaggle (jarturo/kaggriculture-frontier13-cha22, 9151-9154): 8/0 cha22, 6/2 prvsiyan, 6/2 haideptry v7, 176 ms; archivo 475e4163….
ENVIADO a las dos plazas el 25 sep a las 21:26 UTC por petición de Arturo ("puedes tener una nueva tanda de 2 envios para la competencia? el objetivo es plata al cierre revisa repositorios publicos"): submissions 56560449 y 56560450 (mismo archivo), validadas; retiraron 56523438 y 56524328. Seguimiento: python live_report.py 56560449 56560450.
Prueba complementaria (9161-9164, 16 rivales vivos que faltaban): 60/64 (cha22 58/64); flojos: mooman0222 E081 3/4, E082 2/4, Wangyh666 v44 3/4.
Herramientas nuevas: pull_public_notebooks.py, scan_public_agents.py, replay_panel.py --raw/--episodes, evaluate.py respeta agentes de un argumento y escribe de forma atómica.
Semillas consumidas: 9001-9003 (smoke), 9101-9103, 9111-9114, 9121, 9131-9136 (parcial), 9141-9148, 9151-9154, 9161-9164, 9211 (crítico).
Guía completa para un chat nuevo: GUIA_PARA_EL_PROXIMO_CHAT.es.md.
No enviar más sin petición explícita. No crear automatizaciones sin petición.
