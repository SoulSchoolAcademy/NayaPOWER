# MACHINE-LEARN-CONTRACT-V2


**ULTIMATE SEMANTIC LOCK:** `.naya/specifications/NAYAPOWER-NINE-MASTER-NODES-ULTIMATE-LOCK-V1.md` — LEARN semantics and boundaries MUST conform to the Human-Director lock; this file is an implementation/cognitive projection, not a competing semantic authority.
**Status:** CANONICAL MACHINE CONTRACT — implementation qualification layer. Runtime proof is separate.

## Role
LEARN is the machine boundary for reconciliation, promotion, compounding.

## Required functions
- extract_candidate
- reconcile
- detect_conflict
- test_applicability
- design_holdout
- measure_behavior_change
- promote
- reject
- supersede
- rollback_learning

## Input contract
A call MUST carry execution_id, kernel_revision, node_id=LEARN, typed input, provenance references, owner/scope context where applicable, and the upstream receipt hash. Missing required identity, provenance, scope, or authority context MUST fail closed.

## Output contract
Return status, typed output, execution_id, node_id, input/output hashes, evidence references, state transition, failure code when applicable, and deterministic receipt metadata. Output MUST NOT upgrade epistemic state without evidence.

## State machine
UNINITIALIZED → VALIDATING → READY/EXECUTING → COMPLETE. Negative terminal states are BLOCKED | FAILED | INCONCLUSIVE | DEFERRED. A negative state cannot be coerced to PASS by a downstream node.

## Invariants
1. Capability never creates authority.
2. Context never creates ownership.
3. Retrieval never creates truth.
4. Sequence never proves causality.
5. Self-report never constitutes independent verification.
6. Cross-owner leakage is prohibited.
7. Superseded records remain traceable.
8. Every consequential transition is receipt-backed.

## Error semantics
- BLOCKED: prerequisite/authority/scope missing.
- FAILED: execution error after prerequisites were satisfied.
- INCONCLUSIVE: evidence cannot support the requested claim.
- DEFERRED: candidate retained but promotion conditions unmet.

## Security
Reject ambiguous owner scope; reject forged/missing provenance; never accept inherited successor authority; enforce least privilege and idempotency for mutations; preserve immutable receipt lineage.

## Performance
Prefer deterministic bounded work; expose latency, retrieval count, evidence count, and retry count. Retries MUST be idempotent and MUST NOT weaken proof requirements.

## Acceptance
Unit tests cover happy and negative paths. Integration tests prove node-to-node contracts. Runtime tests must use legitimate authenticated identity and real substrate. Independent verification is required for VERIFIED. Production proof is a separate gate.


## Ultimate-lock promotion boundary
- Candidate capture may precede verification.
- Promotion to VERIFIED/ACTIVE/LEARNED requires canonical qualifying VERIFY/CVO/outcome evidence.
- Caller-supplied evidence-reference strings are not evidence validation.
- Learning never creates authority and ACTIVE never implies universal applicability.
