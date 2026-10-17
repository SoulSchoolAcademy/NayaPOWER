# UD-09 — Trace Every Failure to Its True Cause

When something fails, blame belongs to whoever controlled the failing
condition — proven by evidence, never by labels.

## What it does

- **Four ownership domains** — ENVIRONMENT, SCHEDULER, WORKER,
  ORCHESTRATOR (the authorizing layer). A versioned
  `ResponsibilityRecord` names the controller of each liveness
  condition; the controller field is decisive and no narrative
  overrides it.
- **Canonical evidence events** — every event carries a producer AND
  an observer that must differ (self-certification is a construction
  error), a Lamport clock, a sha256 artifact hash over the canonical
  claim bytes, and an observer attestation. Corrupted logs are
  rejected at construction.
- **The four-rung observation ladder** — REPORTED →
  AUTHENTICATED → INDEPENDENTLY_CORROBORATED → CAUSALLY_QUALIFIED.
  Promotions are one rung at a time; corroboration requires lineage-
  independent events (no shared producer/observer); a CORRELATES_WITH
  edge can never be promoted to CAUSED_BY.
- **The three causal checks** — mechanism, counterfactual, independent
  reproduction. A CAUSED_BY edge exists only after all three pass on
  evidence. Ordering is not causation; a bare "A then B" is refused.
- **The verifier is pure** — `TrueCauseVerifier.verify()` reads
  symptoms, events, and responsibility records only. Narrative labels
  (`ComponentReport`) are never an input, so label swaps leave
  verdicts byte-identical, and a fresh verifier reproduces conclusions
  without trusting the original agents.
- **Honest uncertainty** — negative claims need coverage evidence.
  Without it the verdict is BOUNDARY_UNDETERMINED ("we can't observe
  enough to say"), never an invented explanation.

## Acceptance gate (encoded in test_true_cause.py, 28 tests)

1. Same symptoms ("workflow did not complete") produce different
   verdicts from different evidence: ENVIRONMENT_BLOCKER /
   SCHEDULER_STARVATION / WORKER_NONPROGRESS.
2. Swapped narrative labels leave the verdict digest byte-identical;
   false blame cannot move the verdict.
3. Corrupted logs (hash mismatch, missing attestation,
   self-certification) are rejected at construction; insufficient
   evidence downgrades to BOUNDARY_UNDETERMINED.
4. A fresh verifier instance reproduces byte-identical digests.

## Relationship to the D29 fixture

`drift_canary/d29_boundary.py` (branch `naya4/d29-boundary-fixture`)
built the boundary-classification experiment: controller-decisive
records and the evidence-based classifier. This module keeps that
vocabulary and adds the canonical evidence events, the observation
ladder, and the three causal checks the fixture did not have. It is
stdlib-only and self-contained under `tools/`.

## What this does NOT claim

- It judges the evidence it is given; it does not discover
  real-world hazards or collect the evidence itself.
- Attestation is a structured observer statement, not cryptography.
- A PASS certifies the tested scenarios only.
