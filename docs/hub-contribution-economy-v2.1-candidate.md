# Hub Contribution Economy V2.1 — Candidate Specification

**Status:** CANDIDATE, NOT RATIFIED. The decision calculus (Issue #1182) is the
root-core foundation; this economy is the *separate future model* it calls for.
**Never score human worth.** Contribution ≠ Reliability ≠ Conduct ≠ Trust.
**Authority ≠ Reputation — always.** No star count grants deploy, merge,
governance, or any other authority. Ever.

Reference implementation (candidate formulas): `kernel/decision-calculus/value-calculus-v2.1.ts`
(`contributionCredit`, `contributionPoints`, `attributionCredit`).
Receipts: SmartLedger contribution stream (§10B).

## 1. The load-bearing invariant

**Points are a consequence of verified value, never a target.**

- A like, comment, or share earns **exactly zero** by itself. `Activity ≠ Value.`
- It earns only when it leads to **verified downstream value**, via an attribution
  receipt: `attribution = 10% × (reuse's CVS)` (hypothesis), with a provenance
  link back to the reuse. No verified reuse → zero points, no matter how many likes.
- 10,000 low-value actions cannot outrank one major verified contribution: credit
  is bounded per contribution (±900 pts) and gated by the novelty factor.
- Farming activity without value yields exactly zero. This is not a tuning choice;
  it is the anti-Goodhart core. If points ever become the objective, the economy
  has failed and the weights must be recalibrated (§12).

## 2. Contribution credit (candidate formula)

For a verified contribution `j`:

`CVS_j = sign(ΔV_verified_j) × 9 × (Quality × Relevance × Verification × Impact × Novelty)^(1/5)`

Each factor ∈ [0,1]. `points_j = 100 × CVS_j` (hypothesis) → ±900 per contribution.

- `ΔV_verified_j` is baseline-relative verified value, from the VERIFY node —
  never self-reported.
- Negative verified value subtracts. No single negative contribution auto-bans or
  auto-punishes; conduct is a separate dimension (K).
- The geometric mean means one near-zero factor (e.g., zero novelty for the
  thousandth duplicate) collapses the credit toward zero. Diminishing returns are
  structural, not a policy patch.

## 3. Star tiers (candidate names + thresholds)

Unbounded points; tiers are display thresholds on the C dimension. No prior tier
name set was found in the repo — these are fresh candidates.

| Stars | Name | C (points) | R floor | K floor |
|---|---|---|---|---|
| ★1 | Seed | 0 | — | — |
| ★2 | Emerging | 500 | — | — |
| ★3 | Developing | 2,000 | 40 | 70 |
| ★4 | Advancing | 6,000 | 50 | 75 |
| ★5 | Mastering | 12,000 | 60 | 80 |
| ★6 | Guide | 20,000 | 65 | 85 |
| ★7 | Mentor | 30,000 | 70 | 88 |
| ★8 | Steward | 42,000 | 75 | 90 |
| ★9 | Luminary | 57,000 | 80 | 92 |
| ★10 | Primal Master | 75,000 | 85 | 95 |

- A tier is awarded only when **all three** hold: C ≥ threshold, R ≥ floor,
  K ≥ floor. High value with poor reliability or conduct does not display high stars.
- Negative C displays as ★1 Seed (no negative stars — display rule, not math).
- Tiers are re-evaluated on every new verified receipt; they can fall as well as rise.
- Pacing: a perfect contribution = 900 pts → ★10 ≈ 84 perfect contributions.
  Thresholds are hypotheses, versioned per §12.

## 4. Multidimensional profile

`Profile = (C, R, K, T)` — the star tier is the **C display**, never the whole person.

- **C — Contribution:** Σ verified contribution points. What value did you create?
- **R — Reliability:** accuracy/usefulness over time. Candidate: recency-weighted
  mean of verification strengths, 0–100. Did your contributions hold up?
- **K — Conduct:** rule/boundary compliance, 0–100 from a separate governance
  process (not the calculus). Did you respect the boundaries?
- **T — Trust:** contextual, derived: `T = f(C, R, K, provenance, recency, domain)`.
  Never a single global scalar, never usable as authority.

## 5. Transparency (the unseen-action defense)

Every action — human or AI agent — is recorded on the SmartLedger with its
predicted value, observed outcome, and verified ΔV. **You cannot act in the
system unseen.** Positive and negative value are both visible. This is what makes
the economy auditable and what makes gaming detectable: the ledger shows the
value, not the story about the value.

## 6. Anti-gaming controls

| Attack | Control |
|---|---|
| Like/comment rings | Zero points without verified downstream reuse |
| Sybil / duplicate identity | Contribution receipts bind contributor identity + provenance; novelty collapses duplicates |
| Self-reported impact inflation | ΔV comes from VERIFY, never the contributor |
| Volume farming | Bounded per-contribution credit + novelty decay + R/K floors on tiers |
| Collusion (A boosts B) | Attribution requires genuine reuse; reuse verification is independent |
| Reward-hacking the rubric | Weights/thresholds versioned; config hash bound into receipts; manipulation detectable |

## 7. What this does NOT do

- Does not grant authority of any kind.
- Does not score human worth, character, or dignity.
- Does not punish: negative value subtracts from C; sanctions live in governance (K), with due process.
- Does not go to production: no Supabase migration, no edge function, no UI
  change is authorized by this candidate. Production wiring needs explicit
  director authorization and a consent/privacy review.
