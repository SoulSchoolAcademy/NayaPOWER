# Admission Contract — Edge-Function Handoff (lane owner)

**Date:** 2026-10-09 · **Branch:** `naya5/learn-admission-contract`
**Why:** 2026-10-09 independent analysis proved 0 of 13 analyzed learning
candidates verifiable as designed (1 tautology, 4 honest nulls,
5 non-experiments, 3 definitional token changes). Capture design was the
bottleneck. This change makes unverifiable candidates un-admittable in code.

## What changed

1. **Canonical gate (Python):** `kernel/protocol/learning_capture.py` —
   `check_admission(candidate) -> AdmissionResult(passed, failed_rules,
   reasons)` with seven individually testable predicates. This module is
   canonical; every other port follows it.
2. **TypeScript port:** `supabase/functions/nayanet-learning-verify/
   admission_contract.ts` — same seven rules, identical rule IDs.
3. **Wiring (the seam):** `supabase/functions/nayanet-learning-verify/
   index.ts`, `mode === "candidate"` branch, immediately before the
   `learning_evidence` insert. A failing design returns
   `409 ADMISSION_CONTRACT_REJECTED` with `failed_rules` + `reasons` and
   **nothing is inserted**. A passing design's verdict is persisted in
   `observed_value.admission_design` / `admission_verdict` for audit.

## The seven rules (stable IDs)

`falsifiable_claim` · `same_named_task` · `preregistered_criterion` ·
`machine_measurement` · `doer_scorer_separation` · `null_not_verified` ·
`replication_gate`

Fail-closed: no named task + no pre-registered criterion + no machine
check ⇒ do not admit. When in doubt, REJECT. A candidate failing ANY rule
is rejected, never admitted as CANDIDATE.

## Lane separation (do not "fix" this)

- **Gated:** `nayanet-learning-verify` `mode="candidate"` — the
  system-captured path (provenance `OBSERVATION`, github-actions-oidc).
- **NOT gated:** `v7-smart-note-canonical` (the Receiver, provenance `USER`)
  and the human-director-verified instant path. The director's word IS the
  verification (Verification Law); gating it would be a law violation.
  The Python gate bypasses explicitly (`bypassed=True`) for
  `capture_path="human_director"` so the boundary stays machine-visible.

## What the lane owner must do

1. **Supply the admission design.** The workflow step that POSTs
   `{"mode":"candidate", ...}` to `nayanet-learning-verify`
   (`.github/workflows/live-supabase-runtime-proof.yml`, "Bind the exact
   persisted fresh lesson into the existing LEARN candidate lane") must now
   include an `admission` object in the request body:

   ```json
   "admission": {
     "claim": "Applying the X lesson causes <metric>=<value> on <TASK-ID> (treatment) vs control",
     "named_task_id": "TASK-ID", "control_task_id": "TASK-ID", "treatment_task_id": "TASK-ID",
     "control_description": "acted without applying the retained lesson",
     "treatment_description": "applied the retained lesson before acting",
     "preregistered_criterion": "treatment shows <metric>=true while control shows false, per machine receipt check",
     "preregistered_at": "2026-10-08T10:00:00+00:00",
     "arms_ran_at": "2026-10-08T12:00:00+00:00",
     "measurement": "machine | different_seat | deterministic  (never self_report)",
     "doer_seat": "naya-2", "scorer_seat": "coda-1",
     "outcome": "positive", "measured_capability_delta": true,
     "replications_on_unseen_tasks": 3
   }
   ```

   Design the experiment for real — do NOT fabricate a design to satisfy
   the gate. A fabricated design that passes the gate is manufactured
   proof and violates the Truth/Proof law.
2. **Redeploy the edge function** through the normal deploy path
   (deployment is a protected gate — not done on this branch).
3. **Grandfathered rows:** candidates admitted before this change
   (including the 13 analyzed 2026-10-09) keep their rows; they are
   documented NOT VERIFIED and must not be promoted on old designs.
4. **Keep the ports in sync:** Python is canonical. Any rule change lands
   in `kernel/protocol/learning_capture.py` FIRST, then the TS port, then
   the conformance test below must stay green.

## Tests

- `tests/test_learning_admission_contract.py` — 28 tests: all 13
  ground-truth failure modes REJECTED, 2 positive fixtures PASS,
  per-rule edge cases, fail-closed default, human-director bypass.
- `tests/test_learning_admission_edge_wiring.py` — conformance: the TS
  port carries all 7 rule IDs and `index.ts` enforces the gate at the
  insert (`ADMISSION_CONTRACT_REJECTED`, no insert on failure).
- Existing suites untouched and green (see branch test log).

## Coordination note — sibling lane (Learning Lane Owner)

The sibling worktree `naya5/learning-admission-law` contains an
uncommitted parallel gate, `tools/learning_admission_gate.py`
(schema `NAYAPOWER_LEARNING_CANDIDATE_ADMISSION_V1`, 8-rule contract
(a)–(h), ternary verdict admitted_as CANDIDATE/NOT_VERIFIED/REJECTED).
That is a SECOND admission gate over the same decision this branch
gates in `kernel/protocol` + the edge function. Two canonical gates
is one too many: it invites rule drift and verdict confusion.

RECOMMENDATION for the Lane Owner: reconcile to ONE canonical gate.
This branch's position is that `kernel/protocol/learning_capture.py`
is the canonical Python law (it extends the repo's existing
learning-capture module, carries the constitutional lane separation,
and is ported 1:1 into the deployed edge function where the actual
CANDIDATE insert happens). The queue-side tool should CALL the
canonical gate rather than re-implementing the rules — or be retired.
Decision is the Lane Owner's; this branch was not changed to resolve it.

## Explicitly NOT done on this branch

- The workflow caller was NOT modified (the lane owner designs the real
  experiment; nothing fabricated).
- The edge function was NOT redeployed (protected gate).
- `v7-smart-note-canonical` was NOT gated (separate lane by law).
- No existing validation was weakened to get green.
