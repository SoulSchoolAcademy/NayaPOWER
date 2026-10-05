# NayaPOWER SELF — Machine Contract V2


**ULTIMATE SEMANTIC LOCK:** `.naya/specifications/NAYAPOWER-NINE-MASTER-NODES-ULTIMATE-LOCK-V1.md` — SELF semantics and boundaries MUST conform to the Human-Director lock; this file is an implementation/cognitive projection, not a competing semantic authority.
**Role:** identity, mission, continuity.

## Inputs
`message_id`, `execution_id`, `contract_version`, identity evidence, requested scope, checkpoint reference.

## Outputs
Resolved identity, mission, scope, continuity state, known/unknown/blocked classification, receipt and provenance references.

## States
`UNINITIALIZED → VALIDATING → READY → EXECUTING → COMPLETE`; failure states `BLOCKED | FAILED | INCONCLUSIVE`.

## Invariants
Never infer ownership from names, similarity, browser state, object IDs, timing, or usefulness. Never grant authority. Never cross owner scope.

## Errors
`IDENTITY_MISSING`, `IDENTITY_CONFLICT`, `SCOPE_VIOLATION`, `CHECKPOINT_MISSING`, `PROVENANCE_MISSING`, `CONTRACT_UNSUPPORTED`, `SUBSTRATE_UNAVAILABLE`, `DUPLICATE_EXECUTION`.

## Receipt
Must bind execution ID, node/version, input/output hashes, state transition, evidence, provenance, gaps and timestamp.

## Security / replay
Fail closed on ambiguous identity. Use deterministic idempotency keys and version fencing. Successor context carries intelligence and authority context but never inherited permission.

## Acceptance
Schema, negative-path, replay, cold-boot and successor tests; live authenticated identity resolution where claimed. Documentation is not runtime proof.