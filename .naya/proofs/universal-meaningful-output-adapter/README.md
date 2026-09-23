# Universal Meaningful-Output Adapter — Bounded Validation Harness

**Proof ID:** UMOA-TOOLRESULT-001  
**Boundary:** one private `tool_result` → `UNIVERSAL_MEANINGFUL_OUTPUT_V1` → existing `intelligence_commit`  
**Scope:** capture/integration/checkpoint + identity/provenance/idempotency/fresh retrieval  
**Forbidden:** Smart Note capture, publication, consequential execution, second store.

## Canonical input

```json
{
  "output_id": "tool-result:adapter-proof-001",
  "output_version": 1,
  "event_at": "2026-09-23T20:00:00Z",
  "source_ref": "tool-result:adapter-proof-001",
  "source_type": "tool_result",
  "title": "Canonical resolver lesson",
  "content": "Use the existing canonical resolver instead of creating a parallel intelligence destination.",
  "meaning": "Prevents duplicate memory paths and preserves one authoritative intelligence system.",
  "materiality": "REUSABLE",
  "proposed_use": "Apply the canonical resolver rule when routing future meaningful outputs.",
  "applicable_scope": "NayaNET intelligence routing only.",
  "uncertainties": [],
  "provenance_refs": ["tool-result:adapter-proof-001"],
  "evidence_state": "OBSERVED",
  "privacy": "PRIVATE",
  "requested_action": "ROUTE_IF_AUTHORIZED",
  "destination_class": "existing_intelligence"
}
```

## Required execution assertions

1. Authenticate an authorized test member.
2. Submit exactly the canonical input above through the universal adapter.
3. Assert destination is `existing_intelligence`.
4. Assert Smart Note ingress was not called.
5. Assert returned status is `CAPTURED_INTEGRATED_CHECKPOINTED`.
6. Assert canonical cognition event identity is stable and equals `intelligence:<idempotency_key>`.
7. Assert source provenance remains bound to the test input.
8. Assert a receipt exists.
9. Assert intelligence-index projection exists for the same source event.
10. Assert checkpoint identity is `checkpoint:<idempotency_key>`.
11. Assert learning evidence is linked to the canonical source event.
12. Submit the exact same idempotency key/content again and assert replay/idempotent behavior with no uncontrolled duplicate event/block.
13. Retrieve the resulting intelligence in a fresh authenticated read context and assert the same canonical identity is returned.
14. Assert no public/share/consequential destination was created.

## Proof boundary

PASS requires all assertions above.

A successful database insert, operation log, or receipt alone is insufficient.

Applicability, behavior change, outcome verification, and improvement remain outside this proof.

## Execution requirement

The harness must run against the authenticated deployed NayaNET runtime, not by duplicating the `intelligence_commit` implementation in a local test.

The current ChatGPT connector surface can inspect and mutate repository source and execute Supabase SQL, but it does not expose an authenticated HTTP invocation primitive for this Edge Function. Therefore this artifact is implemented and ready, but **runtime execution must not be falsely simulated through direct SQL**.

Status: HARNESS_IMPLEMENTED / EXECUTION_NOT_YET_PERFORMED
