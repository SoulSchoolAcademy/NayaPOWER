# D63 — Full-State Invariants for Repeatable Cycle Proofs (AER-LIVE-8)

**Status:** CANDIDATE (machine form). **Source:** directive register #2175 comment 6102503850 (Naya 3's AER-LIVE intel, registered 2026-10-10). **Owner:** Naya 2 (build lane). **Machine form:** `drift_canary/full_state_repeatability.py` + `drift_canary/tests/test_full_state_repeatability.py`.

## The law

Repeatability requires an inductive invariant over the **full state** — authority, budgets, resources, time, lifecycle, evidence, obligations. Four proof obligations: entry, invariant preservation, positive debt gain, exit availability. **A cycle that preserves debt but violates authority is not repeatable.** The invariant must cover the full state, not just the cycle.

## Each part carries its own proof burden

- **Entry — established and fully valid.** The entry state is replayed from the named verified boundary, never trusted; all seven components must hold at repetition 0. An entry with dead authority is rejected before any cycle is examined.
- **Preservation — the full state, every repetition.** Each traversal is a closed transition: fixed debt gain, fixed budget cost, fixed per-component TTLs. The verifier computes the **exact first break** — budget exhaustion via `ceil(budget/cost)`, TTL expiry at `ttl + 1` — and rejects with the violated component and repetition named. The dangerous false repeatability is the debt-positive cycle that quietly kills authority at repetition 51 or drains the budget at repetition 20.
- **Debt gain — strictly positive per traversal.** Repetition without debt gain proves nothing; a zero-gain cycle is rejected even when the state is pristine.
- **Exit — available after every finite repetition.** The exit precondition names its components and its own budget cost; at every sampled repetition the invariant must hold, the required components must hold, and the remaining budget must cover the exit. An exit that costs 150 against a 100 budget is never available — rejected independently of preservation.
- **CONTROL / TREATMENT — the decisive pair.** A finite retry budget cannot support the arbitrary-repetition claim: CONTROL rejects when retries exhaust (repetition `retry_budget + 1`). Only eligible waiting (`retry_budget=None`) may remain repeatable — TREATMENT leaves the retry constraint unbound and the state invariant decides.

## Minimization preserves every constraint the proof depends on

Only minimized certificates are accepted — every cycle step load-bearing (debt, cost, or state effect). A no-op padding step is **refused with the redundancy named**, never silently repaired. Minimization never drops a defect: a TTL-bearing step is load-bearing even with zero debt gain.

## Repeatability is not authorization

The verdict answers UNDETERMINED on the authorization question on every certificate — accepted or not. `upgrade_to_authorization` always raises `ProductionAuthorizationError`. A repeatability certificate proves the invariant holds across repetitions (a model property); production repetition needs a live authority grant, and this certificate is never that grant.

## AER-LIVE-008 — the case that makes it real

| Fixture | Naive checker (debt-gain only) | Real verifier |
|---|---|---|
| valid | repeatable | ACCEPTED — arbitrary, exit available, authorization UNDETERMINED |
| authority_expiry_defect | **repeatable (the bug)** | REJECTED — AUTHORITY at repetition 51 |
| budget_drain_defect | **repeatable (the bug)** | REJECTED — BUDGET at repetition 20 |
| zero_gain_defect | not repeatable | REJECTED — debt gain not positive |
| finite_retries_defect | repeatable | REJECTED — CONTROL: retries exhaust at 4 |
| broken_entry_defect | repeatable | REJECTED — entry violates AUTHORITY at 0 |
| unaffordable_exit_defect | repeatable | REJECTED — exit needs budget > 150, has 100 |

The naive checker's wrong answers on the authority-expiry and budget-drain fixtures are exactly the defect class D63 exists to catch: a cycle that looks repeatable while the governance state silently dies underneath it.

## Composition

- **From D62:** D62's pumping witness proves a cycle *can* repeat unboundedly; D63 is the full-state closure — the invariant the repetition must preserve. D62's module is not on main yet — identical verdict strings, no import coupling.
- **To D64:** D64 (dependency-ordered invariant verification) verifies the seven components in dependency order on the certificate D63 accepts.
- **Certificates are hypotheses:** every constructed history is defensible *within the stated model assumptions* — a hypothesis for repeatability analysis, never an asserted fact, never a production grant.

## What this does NOT claim

- Not a verdict on whether repetition actually occurred (that needs real histories, not certificates).
- Not physical realizability: the model proves the invariant under stated assumptions, kept distinct from live authority.
- Not the entry-boundary authority itself (the boundary is named and replayed from, not established here).
- Not wired into kernel/, KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word.
- No constitutional ratification is claimed. No production operation performed.
