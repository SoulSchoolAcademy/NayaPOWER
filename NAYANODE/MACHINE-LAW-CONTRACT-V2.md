# NayaPOWER LAW — Machine Contract V2


**ULTIMATE SEMANTIC LOCK:** `.naya/specifications/NAYAPOWER-NINE-MASTER-NODES-ULTIMATE-LOCK-V1.md` — LAW semantics and boundaries MUST conform to the Human-Director lock; this file is an implementation/cognitive projection, not a competing semantic authority.
**Role:** authority, consent, governance.

## Functions
- `resolve_authority`
- `validate_scope`
- `validate_consent`
- `check_expiry`
- `check_revocation`
- `evaluate_constraints`
- `deny_out_of_scope`
- `emit_authorization_receipt`
- `revoke`
- `recheck_before_execution`

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