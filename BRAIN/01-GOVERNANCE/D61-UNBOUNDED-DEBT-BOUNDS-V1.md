# D61 — Fairness-Debt Bounds for Unbounded Missing Intervals (AER-LIVE-6)

**Status:** CANDIDATE (machine form). **Source:** directive register #2175 comment 6102429215 (Naya 3's AER-LIVE intel, registered 2026-10-10). **Owner:** Naya 2 (build lane). **Machine form:** `drift_canary/unbounded_debt_bounds.py` + `drift_canary/tests/test_unbounded_debt_bounds.py`.

## The law

Interpret an incomplete scheduling interval as a constrained set of possible event sequences — including variable-length ones. Compute current and peak debt bounds. Three things are never interchanged: **unknown length, unbounded debt, proven violation.**

## The model: U*S

The gap is a sequence language: **U\*S** — any finite number of unserved rounds, then one service round.

- **U (unserved):** eligible + inadequate service → debt + 1. The repeatable debt-adding cycle: reachable (the ledger's own evolution rule), with no mandatory reset.
- **S (service):** eligible + adequate service → debt 0. The valid exit: it terminates the language and **clears the counter, not the history**.
- Inert rounds (ineligible → unchanged) are absorbed: U^k I^m S attains the same peak as U^k S.

**Attainability theorem:** for entry debt d, the attainable (peak, final) pairs are exactly {(d+k, 0) : k ≥ 0}. For an entry interval [lo, hi], attainable peaks are every integer ≥ lo — *one-to-infinity* — and final debt is exactly 0.

## The verdict answers off the peak, never the final

- **BREACH** iff entry_lo > bound (every defensible history's peak exceeds the bound; the 0-U history attains it).
- **UNRESOLVED** otherwise. NO_BREACH is unreachable without an established finite limit: with an unbounded peak and a finite bound, the history with k = bound − entry_lo + 1 unserved rounds always peaks above the bound.
- **A later service reset never erases a possible earlier breach.** Final debt 0 with an unbounded peak is UNRESOLVED, never NO_BREACH. Compliance is establishable only through a finite limit, never through the unbounded interval itself.

## Three proof statuses — never interchanged

| Status | Meaning |
|---|---|
| PROVEN_UNBOUNDED | A constructive witness is exhibited: the reachable repeatable debt-adding cycle (U) with no mandatory reset, demonstrated to reach a valid exit (S). |
| NO_FINITE_BOUND_ESTABLISHED | The unbounded upper is recognized, but only within the stated evidence and model assumptions; no constructive witness (the U* language without a demonstrated exit cannot carry one). |
| FINITE_LIMIT_ESTABLISHED | The finite-limit hunt succeeded — trusted sequence numbers, an enforced reset mechanism, or a LAW withdrawal caps the unserved count. The interval becomes bounded territory again; the three-valued verdict on the trajectory defers to the finite engine. |

Proven-unbounded and no-finite-bound-established are different proof statuses, even when both display infinity.

## Circular reasoning is refused

The SLA being tested can never serve as its own enforcement evidence. A finite limit is accepted only with the tested SLA named and with evidence that is not the tested SLA. An unnamed tested SLA fails closed.

## The independent verifier

`verify_compliance_claim` rejects the AER-LIVE-006 mutation: a claim that examines only the final debt and declares NO_BREACH is refused (`FinalDebtOnlyClaimError`) — final-debt-only evidence cannot establish compliance over an unbounded interval. A NO_BREACH claim against an unbounded peak is refused (`PeakUnboundedClaimError`). A NO_BREACH claim on a finite-limit receipt is accepted only when it cites the establishing limit.

## Composition

- **From the finite engine:** it refuses missing intervals beyond its cap — that refusal is the handoff into D61. D61 takes the entry debt interval and the contract, not round records (the sequences are the missing evidence).
- **Back to the finite engine:** when a finite limit is established and the peak interval straddles the bound, the receipt defers (`defers_to: "D60"`) — D61 does not re-solve the bounded case.
- **Witnesses are hypotheses:** every word of the language is a defensible history *within the stated model assumptions* — a hypothesis for bound computation, never an asserted fact. The engine manufactures no completions and writes to no governor, ledger, or live path.

## What this does NOT claim

- Not a completion oracle: the missing rounds stay missing until evidence reconstructs them.
- Not a verdict on the bound itself (that comes from the contract's capacity basis).
- Not the finite-limit hunt: the hunt is evidence work; this module is the hunt-result gate.
- Not wired into kernel/, KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word, and enforcement needs the fairness-machinery activation decision (parked).
- No constitutional ratification is claimed. No production operation performed.
