Frontier17 changes by Arturo-GA / Kaggriculture Lab, September 27, 2026.
License for these original additions: Apache-2.0.

The complete Frontier16 deployed source is retained byte-for-byte as a prefix:
0c6ac464ec556dc96a045c6575e718bb3aa77a153a97f9bae506eec3a32807cd.
All original source notices, Frontier16 LICENSE.txt, NOTICE.txt and LAB_NOTICE.md
remain applicable and are included in the local archive.

Original additions in this round:
- Inspect the agent's own route plans and remove one-turn speculative buy/sell
  pairs with preserved physical commands and market slots.
- Search bounded inventory-neutral input purchases and sales within a turn,
  using the inherited attributed per-unit price model and a similar-rival
  scenario. Cash and capacity bounds are conservative. No hidden opponent
  state or recorded opponent action streams are used by the runtime.
- Official-engine replay accounting, paired evaluation, unit tests and reports.

The observed input-trading patterns are documented in publicly visible episodes
114243937, 114227694 and 114258667. The Lab implementation is independently
written; it does not contain the opponents' source code or action tapes.
No third-party notebook update was incorporated after the frozen F16 baseline
in this round. No endorsement, guaranteed rating, or eligibility ruling is made.
