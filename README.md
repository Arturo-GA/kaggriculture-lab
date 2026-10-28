# Kaggriculture Lab

🥉 **Bronze medal — 951st of 10,148 teams** in [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture) (Kaggle Featured Simulation Competition, September 2026).

A research lab for building, evaluating and shipping agents for a two-player farming simulation. Over 19 days and 21 agent generations ("Frontiers"), the project went from a public baseline rated ~1,900 to a final agent that competed in the top 10 % of the leaderboard.

## The problem

Two agents run rival farms on a 10×10 grid for 720 turns (30 days × 24 hours) and share one market. Each turn an agent hires workers, plants, waters, harvests, raises animals, routes deliveries and places buy/sell orders; the market settles both players' orders unit by unit at a price that depends on current inventory. Only the final cash balance matters: win or lose, no margin. Ratings come from a Bradley-Terry fit over thousands of live games, so the opponent pool changes daily as other teams publish new agents.

## What is in this repo

The agents build on public Apache-2.0 baselines shared during the competition (see [NOTICE.md](NOTICE.md) and `attribution/`). The original contribution is the **layers added on top of those baselines and the evaluation machinery used to decide what to ship**:

| Component | What it does | Where |
|---|---|---|
| **Lockstep sale ordering** | Re-plays the engine's per-unit settlement to choose the permutation of our own sell orders with the best modelled margin when the rival runs a clone of our tape | `scripts/frontier5_lockstep.py` |
| **Sale-timing gates** | Demand/belief/lead gates that decide *when* to sell saturated goods (milk, wool, strawberries) using public demand accounting | `candidates/demand_gate*.py`, `belief_*.py` |
| **Branch router** | Reads the rival's lineage from its public cash at step 1 and switches to the base that wins that match-up | `candidates/f12_router.py` |
| **Market/input layers** | In-turn search for input purchases under cash and capacity limits; covered residual sales; delivery-on-route | `scripts/frontier17_input_market.py`, `frontier20_*.py`, `build_f21.py` |
| **Learned option critic** | Small model trained on logged games to pick the sale-reservation horizon (78/80 held-out wins vs 61/80 for the hand-tuned rule) | `scripts/train_ml.py`, `build_ml_policy.py`, `results/ml/` |
| **Evaluation harness** | Registered acceptance gates (fresh seeds, both seats, mirror match, opponent floor, zero errors, latency < 1 s) that a candidate must pass locally *and* in a private Kaggle kernel before submission | `scripts/evaluate.py`, `frontier5_validation.py`, `assess_f*.py`, `verify_*_cloud.py` |
| **C++ accelerator** | Integration of a community C++ port of the engine, verified against the official engine: 8.7× faster holdouts | `scripts/accelerator.py`, `build_cppsim.py`, `verify_accelerator.py` |
| **Opponent research** | Reconstruction of top-100 replays (exact per-turn accounting), census of their strategies, loss audits game by game | `scripts/research_top100.py`, `analyze_*.py`, `docs/history/TOP100_*.md` |

Every submission has a receipt (`results/frontier*/submission_receipt.json`) with the SHA-256 of the exported agent, the holdout summary that justified it and the Kaggle verification run.

## How a Frontier was shipped

1. **Diagnose** – pull the live games of the active submissions, identify the opponents behind each loss, and reproduce the losses locally with the rival's recorded actions.
2. **Build** – `scripts/build_fN.py` composes a candidate from a hash-pinned base plus the new layer and writes it to `candidates/`.
3. **Gate** – `scripts/assess_fN.py` runs the registered holdout (`results/frontierN/plan.json`): new seeds, both seats, the previous Frontier as control. A candidate that fails the gate is kept in the log but never submitted.
4. **Verify in the cloud** – `scripts/make_frontierN_notebook.py` bundles the exact files into a private Kaggle kernel that replays the gate on the official engine and checks the archive byte for byte.
5. **Submit** – `scripts/submit_frontierN.py` (later `release_fN.py` / `finish_fN_submission.py`) sends one slot and stores the receipt.

The full log, Frontier by Frontier, with every number and every discarded idea, is in [`docs/history/`](docs/history/README.md) (Spanish).

## Results timeline

| Date | Frontier | Live rating / rank | Note |
|---|---|---|---|
| 12 Sep | matched6 (V37 + 6-turn sale reservation) | 1,886 → 2,656 | first submission |
| 13–14 Sep | Frontier / Frontier2 (own last-day planner, deliveries on route) | 2,613 | |
| 16–17 Sep | Frontier4 / Frontier5 (sales-race probe, **lockstep layer**) | 2,674 → 2,751 (#238) | silver zone at the time |
| 19–21 Sep | Frontier8 / Frontier9 (stacked public layers + lockstep, bounded sale advance) | 2,825 peak | |
| 24–27 Sep | Frontier11–18 (branch router, input market, feed fix) | 2,450 (#273) | public wave of new baselines reset the pool |
| 30 Sep | Frontier20 / Frontier21 (covered residual sales) | final pair | |
| **Final** | **Bradley-Terry ranking after two weeks of play** | **951 / 10,148 — bronze** | |

Live ratings are noisy and shifted every time a stronger public baseline appeared; the table is there to show the iteration, not a monotone climb.

## Repository layout

```
candidates/        exported agents, one file each (the submitted ones are tracked; public rivals are git-ignored)
baseline/          the pinned public V37 baseline with its upstream notices
scripts/           build_*, assess_*, evaluate, research, notebook builders, submit/verify tooling
tests/             unit tests per Frontier (python -m unittest discover -s tests)
notebooks/         generated Kaggle kernels (one folder per Frontier)
results/           holdouts, plans, receipts and Kaggle verification runs, per Frontier
attribution/       licenses and notices of the public code each Frontier builds on
docs/history/      day-by-day research log and results reports (Spanish)
```

## Reproduce

Python 3.12; the agents use only the standard library. Run everything from the repository root.

```bash
python -m venv .venv && source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt                          # kaggle-environments 1.32.7

# unit tests (some require public rival agents that are not redistributed; see .gitignore)
python -m unittest discover -s tests

# evaluate a candidate against a rival on fresh seeds, both seats, official engine
python scripts/evaluate.py --candidates f21_cap12 --opponents f20_value --seeds 93001 93002 --workers 2 --output results/new_check.json

# rebuild the final candidate from its pinned base and layer
python scripts/build_f21.py && python -m unittest tests/test_frontier21.py
```

Optional C++ accelerator: `pip install -r requirements-accelerator.txt`, then `python scripts/build_cppsim.py && python scripts/verify_accelerator.py` (see `results/cppsim_build.json` for the pinned upstream revision).

## Honest limitations

- Local panels are small (8–16 seeds × a handful of rivals) and dominated by public tape lineages; several Frontiers passed their gate and still lost rating when a new public wave arrived.
- The strongest agents (top 30) used private economies or RL; this project stayed within heuristic layers on public bases, which is what the final rank reflects.
- `results/` keeps raw receipts as they were written during the competition, including informal notes.

## License

Project additions: Apache-2.0 (see [LICENSE](LICENSE)). Inherited public code keeps its original notices; see [NOTICE.md](NOTICE.md) and `attribution/`.
