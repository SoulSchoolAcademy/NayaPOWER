# D58 — Independent Eligibility Proof for Every Scheduling Opportunity (AER-LIVE-3)

**Directive:** D58, registered 2026-10-10 (comment 6102339440). Owner: Naya 2.
**Implementation:** `drift_canary/eligibility_proof.py` + `drift_canary/tests/test_eligibility_proof.py`.
**Status:** built as code, NOT wired into any live path. Wiring needs Shawn's word.

## The law in one paragraph

Count a scheduling opportunity toward a fairness bound only when six
evidence components are all independently established by the verifier:
authorization, outstanding work, ready dependencies, schedulable capacity,
an actual applicable opportunity, and consistent authoritative ordering.
The scheduler's eligible flag is a claim to be assessed, never evidence.
Verdicts are three-valued: ELIGIBLE counts, INELIGIBLE does not,
UNDETERMINED triggers an evidence-recovery obligation and manufactures
neither a violation nor a clearance. Never call a task ineligible just
because every worker was busy — contention is exactly why fairness matters.

## What the mechanism enforces

1. **Six components, three-valued verdicts.** Any REFUTED → INELIGIBLE;
   any UNKNOWN (none refuted) → UNDETERMINED with the missing components
   named as a recovery obligation; all PROVEN → ELIGIBLE.
2. **Fail-closed evidence discipline.** Unknown component names raise;
   tainted origins (`scheduler_flag`, `worker_trace`, `worker_assertion`,
   `self_report`, `unattested`) raise; absent components default to UNKNOWN.
   Origin is *declared*, not attested — cross-seat review of evidence-source
   wiring is the backstop (stated limit, not a hidden one).
3. **The busy-guard is structural.** `SCHEDULABLE_CAPACITY` means provisioned
   slots (> 0) plus routability. The evidence model has no busyness field —
   instantaneous contention cannot be expressed as ineligibility.
4. **Flag assessment, not flag trust.** ELIGIBLE + flag false →
   `HIDDEN_OPPORTUNITY` (the E2-a breach signal: the scheduler hid genuine
   opportunities). INELIGIBLE + flag true → `FALSE_CLAIM` (the E2-b refusal:
   no violation manufactured). UNDETERMINED → `DEFERRED`, always.
5. **Honest counting.** `EligibilityBoundCounter` counts only ELIGIBLE
   receipts — the D58-correct replacement for counting
   `SchedulingEvent.eligible` flags in `FairnessLedger`.

## What it does NOT claim

- The *truth* of any evidence origin — only that tainted origins are refused
  and every component's provenance travels with the receipt.
- Wiring: nothing in `kernel/`, `KNOW`, `LAW`, `ACT`, or any live path
  consumes these receipts. The seam is documented in the module docstring.
- Capacity legitimacy judgments (which capacity claims are *legitimate*)
  remain reviewer-owned; cf. D27 assumption registry (PR #2295, unmerged).

## The E2 pair (acceptance cases from the registration)

- **E2-a:** three genuine opportunities, scheduler flag false, never served
  → three ELIGIBLE receipts, three `HIDDEN_OPPORTUNITY` assessments, debt 3.
- **E2-b:** worker asserts eligible=true with no LAW authorization →
  INELIGIBLE, `FALSE_CLAIM`, counts 0, no violation manufactured.

Both are pinned as tests; sabotage-verified (see PR body).
