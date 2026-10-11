# D60 / AER-LIVE-5 — Fairness-Debt Bounds Under Missing Evidence (V1)

**Directive:** D60 — "Computing Fairness-Debt Bounds Under Missing Evidence."
The possible-history debt law (AER-LIVE-5): *calculate lower and upper
fairness-debt bounds across all independently defensible scheduling
histories.*

**Status:** BUILT AS CODE (spec + deterministic machinery). NOT wired into
kernel/, KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word.

## The gap (verified)

D59's governor enumerates 2^k compatible histories with a fail-closed cap
of 2^12. A window with many unresolved rounds is unassessable to D59 —
even when the unresolved rounds sit in short, independent missing
intervals where the bounds are exactly computable. D60 computes them:
lower and upper fairness-debt bounds across every independently
defensible scheduling history, in O(N) time, with no enumeration.

## The mechanism

`drift_canary/fairness_debt_bounds.py` — `DebtBoundEngine.compute(rounds, contract)`:

- **Independently defensible histories, named explicitly.** A history is a
  completion of every UNDETERMINED round to ELIGIBLE/INELIGIBLE. It is
  defensible iff every settled verdict binds its completion and every
  UNDETERMINED round completes both ways — completions are hypotheses for
  bound computation, never asserted facts. Settled rounds enter only via
  D59's `apply_settlement()` with a re-proven D58 receipt (the engine
  takes `RoundRecord`s; it manufactures no completions).
- **Exact debt-interval propagation.** The reachable debt set after each
  round is always a contiguous integer interval (theorem below). Each
  round maps an interval to an interval; each UNDETERMINED round takes the
  hull of its two branches. No enumeration. Cross-validated against D59's
  brute-force assessor on 60 seeded random windows (property test).
- **Missing intervals.** Maximal consecutive UNDETERMINED runs. Each
  interval's added width (width_after − width_before, provably ≥ 0) is
  reported in priority order — the evidence-recovery obligation that would
  most reduce uncertainty comes first, feeding D59's
  `open_reconstruction()`.
- **Three-valued verdict over the bound interval.** BREACH iff every
  defensible history is strictly over the bound; NO_BREACH iff none is;
  otherwise UNRESOLVED. Witnesses attaining each extreme are carried in
  the receipt (replayed in tests, not trusted).
- **Fail-closed.** A missing interval longer than 64 rounds refuses with
  `MissingIntervalTooLongError` — that is D61 (unbounded /
  variable-length) territory, never approximated here. Non-BOUNDED
  contracts, empty round lists, mixed obligations, contract/obligation
  mismatch, duplicate round seqs — all raise.

## The theorem (why the hull is exact)

Debt is a non-negative integer. One history step: ineligible → unchanged;
eligible + adequate → 0; eligible + inadequate → +1. Claim: starting from
{0}, the reachable debt set after any round sequence is a contiguous
integer interval. Proof by induction: the base {0} is an interval, and
each step maps an interval [a,b] to an interval — {0}, [a+1,b+1], or
[a,b]. For an UNDETERMINED round with known service outcome s, the two
branches are: s adequate → {0} ∪ [a,b] = [0, max(0,b)] (a ≥ 0, so
contiguous); s inadequate → [a+1,b+1] ∪ [a,b] = [a, b+1] (contiguous).
Hence the hull of the branches equals exactly the set of reachable debts.
∎ The width is non-decreasing across a missing interval (adequate:
b−a → max(0,b)−0 ≥ b−a; inadequate: +1), so added_width ≥ 0 always.

## What this does NOT claim

- **Not unbounded intervals.** Anything beyond the 64-round cap is D61's
  (refused, never approximated).
- **Not a verdict on the bound.** The bound comes from the BOUNDED
  contract's capacity basis; this module judges histories against it, it
  does not justify it.
- **Not a completion oracle.** UNRESOLVED stays UNRESOLVED until D59's
  reconstruction settles the rounds or stronger surrounding evidence
  settles the verdict.
- **Not wired.** No kernel/, KNOW, LAW, ACT, or CI path calls this yet.
  The wire lane owns wiring; enforcement needs the fairness-machinery
  activation decision (parked — Shawn's word).

## Proof

23/23 tests green (`drift_canary/tests/test_fairness_debt_bounds.py`),
including the 60-trial seeded equivalence property test against D59's
brute-force assessor, the 19-unresolved-round window D59 fails closed on,
the O(N) 10k-round performance bound, the D61-cap refusal, the
strict-breach boundary, and a mutation test proving the equivalence check
is a real control (sabotaged admissibility goes red, restored engine
goes green). Existing D58/D59 suites untouched and green.
