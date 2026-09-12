# Attribution and changes

The immutable `baseline/v37.py` is extracted from the user-provided notebook
“Kaggriculture V37 — More Yield, Smarter Labor”, Ahmed Berat Özer, September 12, 2026.
It includes the full Apache License 2.0 and upstream notices, retained verbatim.
See `baseline/notebook_notes.md` for the author's attribution and evaluation claims.

The baseline credits thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
prvsiyan, Dmitrii Gluzdov, lucifer19, leoprovorov and Kaggle contributors,
among others. These credits imply no endorsement of this project.

Modified September 12, 2026 by Arturo-GA / Kaggriculture Lab:

- `candidates/h2.py`, `h6.py`, `h8.py`: replace the four-turn sale-reservation horizon.
- `candidates/pressure.py`: choose 4/6/8 using visible rival yield and price sensitivity.
- `candidates/matched6.py`: use six turns only under persistent public layout similarity.
- `candidates/routes14.py`, `routes14m6.py`: experimental replacement of schedule
  data and first-two-shop routing with yhay81's Shop Router 0911 Simple, combined
  with the existing V37 controllers. These experiments are not the exported agent.
  Source: https://www.kaggle.com/code/yhay81/shop-router-0911-simple .
  Reproducible extraction and hashes: `extract_panel_v2.py`,
  `build_routes_experiment.py`, `results/panel_v2_sources.json`.
- `build.py`, `evaluate.py`, tests, research, notebook and packaging: new project tooling.

The project additions are provided under Apache-2.0. All inherited source and
license notices are retained. Public opponent source files are used only locally
for evaluation and are excluded from Git and the exported runtime. The routes14
experiments incorporate the explicitly attributed schedule library; original
baseline source notices remain intact. No endorsement by the upstream authors
is implied.
