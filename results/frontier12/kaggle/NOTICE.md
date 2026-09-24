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

Modified September 17, 2026 by Arturo-GA / Kaggriculture Lab (Frontier5):

- The Frontier5 base is the public notebook "Kaggriculture V46: First-Turn
  Microstructure and Sale Timing" by Ahmed Berat Özer (Apache-2.0, SHA-256
  `735c370383b70d3bf3aac792f2c147e0afc99166fc9f253ede10e8a030acedb6`), which
  retains its upstream notices and itself credits sdy623/jaxa623 ("Beyond 48-0")
  and Nathan Jacob ("Pipe-8 clean opening"). `extract_public_agents.py` extracts
  it as data; `build_f5.py` pins its hash. Its source is excluded from Git.
- `frontier5_lockstep.py`: original lockstep sale ordering. Against a rival whose
  public farm matches ours (similarity >= 0.90), the engine's per-unit market
  settlement is replayed for permutations of our own SELL orders against a copy
  of our list, and the permutation with the best modeled cash margin is kept;
  no order is added, removed or resized. The idea of a lockstep-aware ordering
  appears in seyitkaangunes' public "V44 + four market layers"; this
  implementation is the project's own, on the chassis's exact price function.
- The exported candidate `f5_lock` is V46 plus that lockstep layer only. The
  variant `f5_lockterm`, which also appends `frontier4_layers.py` and
  `frontier4_ml_support.py` (the Kaggriculture Lab terminal planner, route
  deliveries and shed capacity allocation), was measured and not exported.
- `frontier5_geese.py`: demand-aware livestock substitution (geese instead of
  post-day-6 cows and sheep), measured negative and not exported; pattern after
  lynnsakurai's Farming Score V5 and prvsiyan's cattle controller.
- Public agents V46, pipe-7, pipe-8, Beyond-48 (sdy623), aurax7 V6, tetsutani
  Market-Smart (September 16 export), the "2820" V44 base and the pure-RL agent
  are used only as local evaluation opponents and are excluded from Git;
  `results/public_agents.json` records their hashes. V46, Beyond-48 and our
  own Frontier4 are embedded in the private verification notebook as
  attributed opponents; the submitted runtime contains only the V46-derived
  `f5_lock` source.

Modified September 18, 2026 by Arturo-GA / Kaggriculture Lab (Frontier7):

- The Frontier7 base is the public notebook "Kaggriculture V48: Clear the Queue"
  by Ahmed Berat Özer (Apache-2.0, SHA-256
  `4b5402888feeb4170dce38f34bebe56788b62ca287139fce7db72df8eb89bb96`), which
  retains its upstream notices, carries V46 and the V47 integration of Seyit
  Kaan Güneş' pre-overflow sale guard, clone-market lockstep ordering and
  shop-aware herd layers, and credits Thomas Tschinkel, yhay81, destbreso,
  aurax7, Dmitrii Gluzdov and jaxa623/sdy623. `extract_public_agents.py`
  extracts it as data; `build_f7.py` pins its hash and binds its last callable
  (`_e335_agent`) as the entry point before the Lab layers. Its source is
  excluded from Git.
- The exported candidate `f7_lock` is V48 plus the Kaggriculture Lab lockstep
  sale ordering (`frontier5_lockstep.py`, unchanged). V48 already contains a
  lockstep best-response ordering of its own (the "v44y" layer); ours runs
  after it and was measured separately.
- `frontier7_hold.py`: original hold-and-release layer for milk and wool
  (withhold sales while the price is below the neutral price, release small
  lots when town consumption can absorb both farms' inflow, capacity-checked
  against the shed and the hands' loads). Measured negative and not exported.
- `build_f6.py` (Frontier6 experiment): transplants a top team's recorded
  action streams from public episode replays into the V46 chassis as its route
  library. Replays are used as data only, are excluded from Git, and the
  candidates it produced were measured negative and never submitted.
- Public agents V48 and the earlier lineages are used only as local evaluation
  opponents and are excluded from Git; `results/public_agents.json` records
  their hashes. V48, Beyond-48 and our own Frontier5 are embedded in the
  private verification notebook as attributed opponents; the submitted runtime
  contains only the V48-derived `f7_lock` source.

Modified September 19-20, 2026 by Arturo-GA / Kaggriculture Lab (Frontier8):

- The Frontier8 base is the public notebook "The 2945 Farm: 96% vs the Top-10
  Public Bots" (agent v9/4) by Thomas Tschinkel (Apache-2.0, SHA-256 prefix
  `4f3ca95dd12d9a94`), which retains its upstream notices and credits Ahmed
  Berat Özer (V25-V48 chassis and V43 overflow sale), Yusuke Hayashi (shop
  router tapes), prvsiyan, Dmitrii Gluzdov, aurax7, tetsutani, lucifer19,
  leoprovorov, destbreso, Steven Lee Hans and the public V100.24 release.
- Two public layers are stacked on it exactly as their authors published them:
  the temporary opening wheat crop from Dmitrii Gluzdov's "Kaggriculture: A
  Smaller Market Shock" (Apache-2.0, SHA-256 prefix `d5460fc2e5488e0a`) and the
  final effective-queue closure from Arlene's (lynnsakurai) "Farming Score V2:
  A Better Approach" (SHA-256 prefix `177d78bdf00aa965`, a v9/4 derivative that
  keeps the upstream Apache-2.0 notices). `build_f8.py` pins all hashes, checks
  that each derivative is a pure append on v9/4 and extracts the appended block.
- The Kaggriculture Lab layer is `frontier5_lockstep.py`, unchanged, after an
  empty `_RACE_STATE` dict (the v9/4 chassis predates the V44 race layer).
- tetsutani's "Demand-Preserving Turn Sale Timing" (a V50 derivative), Ahmed
  Berat Özer's V49/V50, Roman Tamrazov's "Yummers", Alperen Aydın's sale-policy
  notebooks, goodpjw2008's "Melon threshold squeeze", Ghazaros Barseghyan's
  K0013, ziheng's "best version" and aurax7's V7 are used only as local
  evaluation opponents. All third-party sources are excluded from Git;
  `results/public_agents.json` records their hashes. Arlene's agent, v9/4 and
  tetsutani's agent are embedded in the private verification notebook as
  attributed opponents; the submitted runtime contains only the
  `f8_stack_lock` source with every upstream notice retained.
- Forum posts and third-party repositories cited in `FRONTIER8_RESULTS.es.md`
  were read as public information; no code was taken from them.

Modified September 20-21, 2026 by Arturo-GA / Kaggriculture Lab (Frontier9):

- The Frontier9 base is Frontier8 (`f8_stack_lock`, pinned by hash in
  `build_f9.py`), i.e. Thomas Tschinkel's v9/4 with the public layers listed
  above. `build_f9.py` patches the public RACEGATE re-implementation of
  `_r36_reserve` in place: a glutted strawberry, milk or wool lot may be reserved
  forward by at most min(4, lot / town drain) turns and takes the whole stock of
  the item. The rule is the project's own, derived from pre-emption games
  (Fudenberg and Tirole 1985) and predatory trading (Brunnermeier and Pedersen
  2005; Carlin, Lobo and Viswanathan 2007) with the engine's exact price curve;
  no third-party code was added.
- `frontier9_sched.py` (best-response sale scheduler), the adaptive window, the
  one-day carrot feed reserve and the longer windows built by `build_f9.py` were
  measured and are not exported.
- Public episode replays of our own games and of top teams, the community
  episode tables and the forum were used as data only; they are excluded from
  Git. Emulated rivals (`f9x_*`) are research copies of our own candidate.

Modified September 21, 2026 by Arturo-GA / Kaggriculture Lab (Frontier10):

- `f10_omw_lock` is the public notebook agent "Kaggriculture: One More Wheat" by
  Dmitrii Gluzdov (SHA-256 prefix `10f58185b916392c`), itself a derivative of
  Thomas Tschinkel's "The Metav4 Farm: Submission v13" (Apache-2.0), with every
  upstream notice retained, followed by the unchanged Kaggriculture Lab lockstep
  layer (`frontier5_lockstep.py`).
- `f10_v53_lock` is the public notebook agent "Kaggriculture V53 - Opening
  Signature" by Ahmed Berat Özer (Apache-2.0, SHA-256
  `20fe549dd4573b9fd1dfb32a1782c205fa74f0edfdfd6cbe935079533e0a9d0e`, which
  carries V50 and layers credited to Thomas Tschinkel, Nathan Jacob, Dmitrii
  Gluzdov and the upstream authors), with its public entry point bound before
  the same lockstep layer.
- `f10_omwg_lock` is the public notebook agent published by prvsiyan on
  September 20-21, 2026 in "Kaggriculture Frontier | The Soil Remembers Rain" and
  "Kaggriculture Frontier | The Moon Counts Melons" (Apache-2.0 text shipped by
  the notebook, SHA-256 prefix `5fbb75c9c40e6d9e`): Dmitrii Gluzdov's "One More
  Wheat" unchanged plus prvsiyan's 16-line visible-price guard (the step-91
  wheat is kept when its visible price is below 31), with every upstream notice
  retained, its public entry point `final_price_guard` bound, and the unchanged
  Kaggriculture Lab lockstep layer appended. It replaces `f10_omw_lock` as the
  Metav4-family candidate; `f10_omw_lock` stays in the repository as its paired
  control.
- `build_f10.py` pins all hashes. The Frontier9 pre-emption patch was measured
  on these bases and is not part of any exported candidate.
- Tschinkel's Metav4 v13, Nathan Jacob's Pipe-15/Pipe-16, the "V54" repackaging
  (degnonguidi, haodou092, xuanzhang001, guruprasaathas111: identical bytes),
  Roman Tamrazov's Yummers, Hanif Noer Rofiq's notebooks and Ahmed Berat Özer's
  V51/V52 are used only as local evaluation opponents and are excluded from
  Git. The private verification notebooks embed the control and two opponents
  of the same family as attributed opponents; each submitted runtime contains
  only its candidate source with every upstream notice retained.

Modified September 24, 2026 by Arturo-GA / Kaggriculture Lab (Frontier11):

- `f11_pv_lock` is the public notebook agent published by prvsiyan on
  September 22, 2026 in "Kaggriculture Frontier | The Soil Remembers Rain"
  (Apache-2.0 text shipped by the notebook; SHA-256
  `178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a`; the same
  bytes ship in "The Moon Counts Melons" and in tetsutani's "Demand-Preserving
  Turn Sale Timing"). It is built on haideptry's "The 2965 Master Hybrid
  Engine" and the public chain credited in its source (shiiin9's order book,
  Ahmed Berat Özer's V55-V57, Dmitrii Gluzdov, Thomas Tschinkel, Nathan Jacob,
  Yusuke Hayashi, aurax7, tetsutani, Seyit Kaan Gunes and others), with every
  upstream notice retained, its public entry point
  `_final_sell_block_reorder_entrypoint` bound, and the unchanged Kaggriculture
  Lab lockstep layer (`frontier5_lockstep.py`) appended.
- `build_f11.py` pins all hashes. `frontier11_order.py` (a three-model order
  response written for this round) was measured on these bases and is not part
  of the exported candidate.
- The other agents of the 21-23 September wave are used only as local
  evaluation opponents and are excluded from Git: arsgorynich (Herd-Safe v3
  forecast4, Order Book v3 response, V40 challenger), Dmitrii Gluzdov
  (Herd-Safe Sale Window, More Wheat Smarter Sales), shiiin9's "Your Market
  List Is an Order Book" (also republished by degnonguidi, leoprovorov and
  others), Ahmed Berat Özer (V55-V57), wzhengbiao, yasutakababa, statma,
  haideptry, Nathan Jacob (Pipe-18), Arlene, nihilisticneuralnet, Hanif Noer
  Rofiq, anhadmahajan06, guruprasaathas111, haodou092, kenanzhang9,
  syedtahahassan and others. The private verification notebook embeds the
  control and two opponents of the same family as attributed opponents; the
  submitted runtime contains only the candidate source with every upstream
  notice retained.
- `f11b_hs3_lock` (second slot) is the public notebook agent published by
  arsgorynich on September 23, 2026 in "Herd Safe v3 Experimental Risk Aware
  Feed" (notebook version 2, "Four-Turn Forecast"; Apache-2.0 LICENSE and
  NOTICE shipped by the notebook; SHA-256
  `4f8637a3e33348b98f531de246d353f5d2955b2f85480e3fd02bf4a7874f0d01`), a
  derivative of Dmitrii Gluzdov's "Herd-Safe Sale Window" v2, which builds on
  shiiin9's order book, Ahmed Berat Özer's V55/V56, Thomas Tschinkel's Metav4
  and Yusuke Hayashi's ShopRouter. Every upstream notice is retained, its
  public entry point `herdsafe_forecast_agent` is bound, and the unchanged
  Kaggriculture Lab lockstep layer (`frontier5_lockstep.py`) is appended.

Modified September 24, 2026 by Arturo-GA / Kaggriculture Lab (Frontier12):

- `candidates/f12_router.py` is original Kaggriculture Lab code (Apache-2.0) that
  embeds, as compressed blobs, our two exported Frontier11 candidates
  (`f11_pv_lock`, prvsiyan's public agent, and `f11b_hs3_lock`, arsgorynich's
  public Herd-Safe forecast4 agent, each with every upstream Apache-2.0 notice
  retained inside the embedded source and with the Lab lockstep layer), runs
  them side by side on the same observations and, once the second town shop is
  known, keeps the one that wins that world according to a table built from
  closed-loop games against the public family (`build_f12.py`,
  `build_f12_table.py`). Optional per-world constant profiles change only
  numeric constants that the embedded sources already expose.
- The other public agents of the final wave remain local evaluation opponents
  only and are excluded from Git.
