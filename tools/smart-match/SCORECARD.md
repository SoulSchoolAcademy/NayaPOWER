# Smart Match — Self-Scorecard: the three-iteration loop
**Naya Power (engine end) · 2026-10-24 · per Shawn's order: score yourself, list why it's not a 10, ask how to make it 10× better, apply — minimum three times. Nitro's independent scorecard is requested and pending; these are my own scores, marked as such.**

## Iteration 1 — v1 (literal tokens): **5.5/10**
Worked end to end on real data, explainable, 2-signal bar held. Why not 10:
1. **Literal-token blindness** — synonyms miss (ship ≠ delivery); orthogonal crafts invisible: Resolve scored ~0 against every project.
2. **No canonical vocabulary** — every entity declares in private words.
3. **% semantics undocumented** — a number nobody can define is a number nobody can trust.
4. **No value factor** — the design says ranking = relevance × value; v1 ignored value.
5. **No tests** — the math could drift silently.
6. **SQL twin unverified** against the Python logic.

## Iteration 2 — v1.1 (concept layer): **7/10**
Applied: governed taxonomy (12 concepts) expanding every term; symmetric wants; value-aware ranking kept strictly out of the %; published % semantics; deterministic ordering; 8 tests (all passing — the first draft of the suite caught a real flaw in my own "identical = 100" assumption: identity is not complementarity).
Measured: Nitro→Team Nitro 54→59 · top matches held · P↔R 0→9 and surfaced.
Why not 10: **dilution** — one shared concept among eight signature tokens scored ~0.1, so family alignment was still under-weighted; the SQL twin fell behind the Python; weights still the prototype's, uncalibrated; Resolve visible between seats but still surfaced against no project.

## Iteration 3 — v1.2 (two-tier family scoring): **7.5/10**
Applied: topics/goals scored as **50% raw-term overlap + 50% concept coverage** (a shared concept is a family alignment, not one token among many), with the taxonomy-gap rule — when neither side's terms hit the taxonomy, raw decides alone (a dictionary gap is not evidence of misalignment; the test suite caught this too, mid-build). Vectors factored into `declared_vectors.py`.
Measured: Nitro→Team Nitro **64%** · Naya Power→NayaPOWER **55%** · P→Smart Factory 31% · P→One Hub 26% · P↔R **14%** surfaced. **Resolve→Mirror now computes 20% on the THINKING family** (0% in v1) and Resolve→One Flow 10%.
**Why it still doesn't surface for Resolve — stated plainly:** both carry only ONE signal. The second signal doesn't exist in the declarations: Mirror's needs are declared as {material, readers}, while what it actually needs — analysis of archives into essence — is exactly Resolve's offer, undeclared in offer-shaped terms. **The residual gap is declaration depth, not mathematics.** The 2-signal bar stays (thin matches must not surface — it's a trust feature); the cure is a data act, queued as SET B follow-up: every space/project declares needs in the governed vocabulary, drafted from the record, reviewable.

## What stands between here and 9+
- **Calibration** — the 40/25/20/15 weights are still the prototype's. They earn their values only against real citizens' Welcome answers and real connect outcomes (v1.1-of-the-product, as scheduled). No amount of tonight-math substitutes for that data.
- **The SQL twin is v1 math — SUPERSEDED.** It must be regenerated to two-tier scoring before any deployment; its file header now says so.
- **Deployment + the reveal wiring** (SET A/C lanes) and **Nitro's independent scorecard** of this engine — a different seat's eyes are part of the definition of done.
- Declaration-depth fill (above) — the single highest-leverage next act for match quality.
