# Frontier20 modifications — Arturo-GA / Kaggriculture Lab

Copyright 2026 Arturo-GA. Licensed under the Apache License, Version 2.0.

The inherited Frontier16–19 source and notices are preserved. Original changes
prioritize wool delivery by the dynamic three-sheep couriers while retaining
feeding, care, harvesting, construction and final-day behavior. Optional
fertilizer collection resumes after the wool has been delivered. A separate
change fills small, covered residual quantities at an existing cash-product
sale, only against very similar public farm layouts. Both mechanisms were
tested separately before selecting their combination.

All 23 public defeats exposed at 20:11 UTC on 30 September 2026 for submissions
56714342 and 56714336 were reconstructed exactly with the official engine.
Public replays supplied diagnostic examples; no private competitor code was
accessed. Inference uses only the agent's own private state and public fields.

Public discussion topics 743231 and 742856 informed the evaluation design:
paired seeds, per-opponent comparisons, two active controls, and separation of
frozen replay diagnostics from games against reactive policies. Topic 731587
explains the final Bradley–Terry evaluation. Forum claims are not treated as
proof of performance. No RL training, leaderboard rating, rank, or medal is
claimed from these local changes. Earlier sale-reservation prototypes and an
unpromoted queue-mixture prototype are research artifacts, not release gains.

The initial delivery policy failed its registered nonmirror criterion. A later
economic guard compares the wool price exposure from currently observable
ready stock against optional fertilizer value. It retains normal fertilizer
collection when rushing offers little economic benefit. This revision uses
only public standing yields and its own inventories, never rival private
cargo or future shops. Its validation uses a separately registered fresh-seed
panel; the initial failure remains recorded and is not converted to a pass.
