# D59 — Governing Unresolved Eligibility Evidence (AER-LIVE-4)

**Directive:** D59, registered 2026-10-10 (comment 6102368579). Owner: Naya 2.
**Implementation:** `drift_canary/unresolved_evidence.py` + `drift_canary/tests/test_unresolved_evidence.py`.
**Status:** built as code, NOT wired into any live path. Wiring needs Shawn's word.
**Stacks on:** D58 (PR #2311, `naya2/d58-eligibility-proof`) — the UNDETERMINED
verdicts this module governs.

## The law in one paragraph

Missing, contradictory, stale, or unverifiable eligibility records are
unresolved evidence obligations — never proven ineligibility, never a
fairness violation. Preserve every compatible history, reconstruct the
missing evidence, and derive only conclusions supported across those
histories. A single debt number cannot hold uncertainty: track the debt
range, and conclude BREACH only if every history breaches, NO_BREACH only
if none does, UNRESOLVED otherwise. Stronger surrounding evidence can
settle a disputed conclusion without ever recovering the missing record.
Reconstruction is itself an independent obligation with its own fairness
contract, so "can't prove starvation because the logs are missing" can
never excuse not repairing the logs. Reconstruction deadlines may
escalate — never manufacture proof, authority, or completion.

## What the mechanism enforces

1. **Defect-carrying rounds.** Every UNDETERMINED round names its defect per
   component (`MISSING` / `CONTRADICTORY` / `STALE` / `UNVERIFIABLE`), and
   the defects must match the D58 receipt's unknown components exactly.
   Service history is a stated precondition: `adequate_service` must be a
   known bool — unknown service is a different unknown and is refused.
2. **Compatible-history assessment.** Each UNDETERMINED round completes both
   ways; debt evolves per history with the `FairnessLedger` rule
   (eligible+adequate → 0, eligible+inadequate → +1, ineligible →
   unchanged). The public verdict is three-valued over the range; breach is
   strict (`debt > bound`). Enumeration is capped at 2¹² histories —
   beyond that the module refuses rather than sampling.
3. **Reconstruction as an independent obligation.** `attempt()` merges fresh
   verifier evidence over the original receipt and re-runs the D58 prover.
   Tainted origins raise (`TaintedOriginError`) — the false-ineligibility
   mutation (settling via the scheduler's own flag) is caught. Unknown
   components in the fresh evidence raise before anything merges.
4. **The repair has its own fairness contract.** Failed attempts accrue
   repair debt against a repair bound; attempts consume a budget. Budget
   exhaustion → `ESCALATED/BUDGET_EXHAUSTED`; repair starvation →
   `ESCALATED/REPAIR_STARVED`. Both preserve the history: the assessment
   after escalation is byte-identical in verdict and range.
5. **Nothing manufactured, ever.** There is no method that asserts a single
   completion as fact; settled rounds enter only via `apply_settlement()`
   with a re-proven D58 receipt — never a bare boolean. Witness histories
   are labeled witnesses, not findings.

## What it does NOT claim

- The *truth* of any reconstructed evidence — only that the prover re-ran
  and tainted origins were refused. Reviewers judge substance.
- Wiring: nothing in `kernel/`, `KNOW`, `LAW`, `ACT`, or any live path
  consumes these assessments. The seam is documented in the module docstring.
- Deadline policy (how long a budget lasts in wall-clock time) — the
  mechanism counts attempts and repair rounds; wall-clock escalation policy
  is reviewer-owned.
- Histories beyond the 2¹² cap are not assessed — the module says so loudly
  instead of silently narrowing the window.

## The AER-LIVE-004 case (acceptance, from the registration)

Two proven rounds, one missing record, complete service history, bound 2:
verdict UNRESOLVED, debt range (2, 3). Continuation A — reconstruction
proves the missing authorization → round settles ELIGIBLE → BREACH.
Continuation B — reconstruction refutes it → round settles INELIGIBLE →
NO_BREACH. The false-ineligibility mutation (scheduler-flag "evidence")
is refused with `TaintedOriginError`. Budget exhausted → ESCALATED with
the UNRESOLVED assessment unchanged. All pinned as tests; sabotage-verified
(see PR body).
