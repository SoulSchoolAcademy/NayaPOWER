# NayaPOWER ACT — Machine Contract V2

**Role:** execution, agency, prioritization.

## Functions
- `plan_action`
- `validate_action`
- `bind_authority`
- `define_expected_outcome`
- `define_proof_requirements`
- `execute`
- `timeout`
- `retry`
- `rollback`
- `observe`
- `emit_receipt`
- `idempotency_check`

## Envelope
`message_id`, `execution_id`, `source_node`, `target_node`, `contract_version`, `identity_context`, `authority_context`, `truth_context`, `provenance`, `payload`, `idempotency_key`.

## State
`UNINITIALIZED → READY → VALIDATING → EXECUTING → OBSERVING → COMMITTING → COMPLETE`; terminal `BLOCKED | FAILED | DEFERRED | INCONCLUSIVE`.

## Invariants
No implicit scope widening; retrieval never authorizes; execution never verifies itself; similarity never becomes truth; missing evidence never becomes evidence; successor context never becomes inherited authority.

## Preconditions / postconditions
Validate schema, identity, target, version, substrate, authority where consequential, provenance, and idempotency before execution. After execution emit typed output, legal state transition, receipt, provenance and explicit gaps.

## Errors
Identity missing/conflict, authority missing/expired, scope violation, schema invalid, unsupported contract, substrate unavailable, provenance missing, stale/superseded data, contradiction, duplicate execution, timeout, retry exhausted, verification inconclusive.

## Persistence / replay
Durable writes bind owner scope, lineage, schema version, content hash and receipt. Replays use deterministic idempotency; stale version fences fail closed.

## Security
Resist confused-deputy, prompt-injection, replay, forged provenance, stale authority and cross-owner leakage. Capability never creates authority.

## Acceptance
Contract/schema tests, negative paths, state transitions, authority/provenance boundaries, replay, live invocation and inspectable receipts. Runtime proof is separate from documentation.