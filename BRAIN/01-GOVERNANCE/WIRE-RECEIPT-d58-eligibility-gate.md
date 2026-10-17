# WIRE RECEIPT — D58 independent-eligibility gate

**Wired:** 2026-10-11 ~08:30Z by Naya 2's wire lane (night shift)
**Mechanism:** D58 / AER-LIVE-3 — Independent Eligibility Proof for Every
Scheduling Opportunity (`drift_canary/eligibility_proof.py`, PR #2311)
**Wire PR:** #2312 — `tools/d58_eligibility_gate.py` +
`d58-eligibility-gate` CI job
**Status:** WIRED-AT-SEAM, PROVEN-ON-COMBINED-TREE. Merge pending
(scorecard + cross-seat review). The gate is DORMANT on main (exit 0,
explicit DORMANT) until the D58 mechanism merges; enforcement activates
with zero new wiring the day the mechanism lands.

## The gap it closes

`drift_canary/fairness.py` `FairnessLedger.record_round` trusts
`SchedulingEvent.eligible` — the scheduler's own flag — when accruing
fairness debt. Trace consistency does not prove the eligibility booleans
were true. A scheduler can hide starvation by recording `eligible=false`
on genuine opportunities; a worker can assert `eligible=true` with no
authorization behind it. D58 recomputes eligibility from six
independently-established evidence components (AUTHORIZATION,
OUTSTANDING_WORK, READY_DEPENDENCIES, SCHEDULABLE_CAPACITY,
APPLICABLE_OPPORTUNITY, CONSISTENT_ORDERING) and yields three-valued
verdicts: ELIGIBLE counts toward the fairness bound, INELIGIBLE does
not, UNDETERMINED triggers an evidence-recovery obligation and
manufactures neither a violation nor a clearance.

## The operating path it now protects

The fairness CI path — the same path the D26/D27/D28 wires guard:

- **Trigger:** `.github/workflows/d58-eligibility-gate.yml` fires on every
  PR touching `tools/d58_eligibility_gate.py`,
  `tools/d58_eligibility_manifest.json`,
  `tests/test_d58_eligibility_gate.py`,
  `drift_canary/eligibility_proof.py`, `drift_canary/fairness.py`
  (the guarded ledger), `drift_canary/fairness_verify.py`, or the
  workflow itself; and on pushes to main touching those paths.
- **What it blocks (exit 1):** a counted opportunity whose D58 verdict is
  not ELIGIBLE; HIDDEN_OPPORTUNITY (scheduler hid a genuine opportunity —
  the bound under-counts); FALSE_CLAIM (scheduler asserted eligibility
  the evidence refutes — the bound over-counts); evidence backed by a
  tainted origin (`scheduler_flag`, `worker_trace`, `worker_assertion`,
  `self_report`, `unattested`); an unknown evidence component; a
  manifest entry the gate refuses to bind (it never invents missing
  evidence fields).
- **Fail-closed (exit 2):** unreadable/corrupt manifest — never a silent pass.
- **Dormant, never theater (exit 0):** mechanism absent on the tree, or
  zero opportunities registered — the gate says DORMANT, never "verified".

## How to verify it is still connected

1. `python3 tools/d58_eligibility_gate.py` must print a
   `D58_ELIGIBILITY_GATE:` verdict line (DORMANT/PASS/VIOLATION/BROKEN —
   never silence).
2. `python3 -m pytest tests/test_d58_eligibility_gate.py -q` — the suite
   is green (enforcement tests skip explicitly while the mechanism is
   absent).
3. The workflow file exists at `.github/workflows/d58-eligibility-gate.yml`
   and lists `drift_canary/fairness.py` in its path triggers.
4. Absence of the verdict line in CI = the wiring broke (regression is
   visible by design).

## Proof (this run)

- Mechanism independently re-proven at exact #2311 head `0c2cc7d3`:
  21/21 D58 tests green on the combined tree (builder's claim not trusted).
- Gate suite: 5 passed / 9 explicitly skipped on the main tree;
  14/14 passed on the combined tree (real mechanism + wire).
- Live violation probes (gate fired as the CI step will):
  hidden-opportunity → exit 1 named; false-claim → exit 1 named;
  tainted origin → exit 1 (prover refused); clean → exit 0 PASS;
  corrupt manifest → exit 2 BROKEN.
- Additive only: +5 files, −0. No edits to the D58 module, the
  FairnessLedger, or any lane's branch. No merges.

## What remains unwired

1. D58 manifest content — the fairness lane registers counted
   opportunities with their six evidence components as independent
   evidence lands; enforcement activates per entry with zero new wiring.
2. The mechanism PR #2311 itself — scorecard + cross-seat review + merge
   (its CI `test` red is the known brain-index-drift class: pytest
   3375 passed, drift on BRAIN/REAL-TREE.* — same class as #2307;
   re-stamp is the build lane's repair, PRs #2290–#2297 open).
3. D56 (#2307) — next in dependency order: its first precondition is
   "eligibility independently established", which is this wire's job.
   Wire D56 after D58's mechanism merges.
4. The 12 prior wire PRs → scorecard + cross-seat review + merge queue.
