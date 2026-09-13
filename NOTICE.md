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
- `candidates/demand_gate.py`, `belief_gate.py`, `demand_gate2.py`, `belief_gate2.py`,
  `belief_lead12.py`: new project sale-timing experiments built on matched6;
  public demand accounting, observed supply scenarios, spending reserves and
  selective extension of planned sale reservations. Original source notices retained.
- `build_cppsim.py`, `accelerator.py`, `verify_accelerator.py`, `evaluate_fast.py`,
  `benchmark_accelerator.py`: project integration of destbreso's public C++ simulator,
  based on nikital7's engine port, Apache-2.0. Upstream revision and binary hash
  are in `results/cppsim_build.json`. Upstream source/binaries are not committed
  or included in the submitted runtime.

The research cites RP1, Q2RL and Deep SPI as methodological inspiration. The
heuristic market prototypes do not implement those algorithms, use their weights,
or inherit their performance claims. Downloaded notebooks used for method review
are attributed in `results/research_sources_20260912.json`.

The project additions are provided under Apache-2.0. All inherited source and
license notices are retained. Public opponent source files are used only locally
for evaluation and are excluded from Git and the exported runtime. The routes14
experiments incorporate the explicitly attributed schedule library; original
baseline source notices remain intact. No endorsement by the upstream authors
is implied.

Modified September 12–13, 2026 by Arturo-GA / Kaggriculture Lab:

- `ml_features.py`, `ml_policy.py`, `candidates/ml_*.py`: a learned macro-option
  selector and forced-option controls on the unchanged matched6 executor.
- `collect_ml.py`, `train_ml.py`: paired simulator-generated counterfactual data
  and a 64-tree grouped-bootstrap critic. No third-party trained weights used.
- `summarize_ml.py`, `profile_ml_latency.py`, tests and ML receipts: held-out
  comparisons, uncertainty estimates and runtime diagnosis.
- `make_ml_notebook.py`, `cloud_ml.py`: separate private Kaggle verification and
  export, retaining the original kernel and its artifacts.

Methodological sources: Kaggriculture discussions 738079 (high-level Options
and constant-policy ablations) and 737027 (public inventory and uncertainty),
and Q2RL (arXiv:2605.05172, value-based gating). This is an independently trained
option critic, not a reproduction of Q2RL, RP1 or Deep SPI.
