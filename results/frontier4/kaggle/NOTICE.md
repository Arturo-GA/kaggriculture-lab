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

Modified September 13, 2026 by Arturo-GA / Kaggriculture Lab:

- `terminal_auction.py`, `frontier_gate.py`, `build_frontier.py`: original joint
  final-day workforce, material, route and sales planner with a learned gate.
  The preceding production policy remains the attributed V37 / ml_critic lineage.
- `audit_gold.py`, `analyze_gold.py`, `evaluate_gold.py`: public-replay behavioral
  analysis and explicitly limited fixed-stream stress tests. No private elite
  source code was accessed, reconstructed or embedded in the runtime.
- `crop_portfolio.py`: inactive late-crop experiment, excluded from Frontier.
- Frontier data collection, training, tests, receipts and private Kaggle tooling
  are new project code. Algorithmic inspiration is distinguished from reproduced
  methods in `GOLD_RESEARCH.es.md`; no third-party trained weights are used.

Further modified September 13, 2026 by Arturo-GA / Kaggriculture Lab:

- `frontier_deliveries.py`: original route-aware intermediate product transfers,
  same-turn sale projection and finite-crop zero-yield recovery. This changes the
  terminal option, so Frontier's old learned gate is explicitly bypassed.
- `diagnose_frontier_losses.py`, `audit_frontier_live.py`, Frontier2 builders,
  tests and cloud checks: actual unit-effect accounting, replay identity checks,
  paired ablations and independent-seed validation. Prior production and all
  inherited attributions remain unchanged.

Modified September 14, 2026 by Arturo-GA / Kaggriculture Lab:

- Frontier3 opening orders (5 / 10 / 60 wheat) follow the user-supplied V41,
  which credits Rayk Kretzschmar. `_r97_budget`, `_r124_labor_reserve`,
  `_r124_seed_budget` and `_r124_atomic` are adapted from Ahmed Berat Ozer's
  Apache-2.0 V41. `results/frontier3/build.json` records the exact donor hash;
  `results/frontier3/v41_funding_helpers.py` preserves the extracted helpers.
- `frontier3_resources.py`: integrates those helpers with the existing Frontier2
  policy, generalizes seed checks to the actual planting day, and records
  confirmed planting and first-dawn hiring effects.
- `frontier3_capacity.py`: original shared-capacity allocation across terminal
  deposits, using visible inventory and price estimates. The existing option
  critic is retained without retraining; its optimality is not claimed.
- Frontier3 builders, tests and local/cloud verification are new project tooling.
  V41 is also embedded as an explicitly attributed evaluation opponent in the
  private notebook; its full source is excluded from the submitted runtime.

Modified September 16, 2026 by Arturo-GA / Kaggriculture Lab (Frontier4):

- The Frontier4 base is the public notebook "Kaggriculture V45: First-Turn Wheat
  Round Trip" by Ahmed Berat Özer (Apache-2.0, SHA-256
  `2536d41ed5a00c75204b6350f1c76c54259c774cb065ba2a3a0072eedf210d94`), which retains
  its own upstream notices (thomastschinkel, yhay81, aurax7, tetsutani, prvsiyan,
  Dmitrii Gluzdov, lucifer19, leoprovorov, Rayk Kretzschmar, Kaggle contributors).
  `extract_public_agents.py` extracts it as data; `build_f4.py` pins its hash.
- `build_f4.py` derives every Frontier4 candidate from that pinned V45 source.
  The exported candidate `f4_probe` adds an original probe to V45's clone
  sales-race layer: the reservation horizon starts at 24 turns until day 14,
  the rival's net sales at our drop turns are reconstructed from our own shed
  and drop accounting, and the 24-turn horizon is kept only when the rival
  demonstrably sells products our route tape sells more than four turns later;
  otherwise the agent returns to V45's 8-turn behaviour and V45's own lost-race
  escalation. Other variants (`f4_r24`, `f4_adapt*`, `f4_term`, `f4_full*`)
  append `frontier4_layers.py` (the Kaggriculture Lab terminal planner, route
  deliveries and shed capacity allocation) and `frontier4_ml_support.py`; they
  were measured and not exported. The old learned option critic is not included.
- `f4_runner.py`: experimental hired "harvest runner" hands; measured negative
  and excluded from the exported agent.
- Public agents V43, V44, pipe-4/pipe-5 (Nathan Jacob), Lynn V5, aurax7 V5 and
  HarvestForge are used only as local evaluation opponents and are excluded from
  Git; `results/public_agents.json` records their hashes. V45 and pipe-5 are
  embedded in the private verification notebook as attributed opponents; the
  submitted runtime contains only the V45-derived `f4_probe` source.
