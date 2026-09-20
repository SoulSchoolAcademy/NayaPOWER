# 01 — Engine and Data Flow

## Canonical execution model
```text
COLD NAYA
 → RESTORE
 → UNDERSTAND
 → PREFLIGHT
 → GOVERN
 → SELECT
 → EXECUTE
 → OBSERVE
 → VERIFY
 → RECORD
 → ACTIVITY
 → INTELLIGENCE
 → STATE
 → HANDOFF
 → CONTINUE
```

## Intelligence lifecycle
```text
EXPERIENCE / INPUT
 → CAPTURE
 → SMART NOTE / EVENT
 → PIS
 → CIS
 → CLASSIFY
 → CONNECT / DEDUPLICATE / CORRECT / INVESTIGATE
 → RETAIN OR REJECT
 → SUPERBRAIN CONTEXT
 → RETRIEVE
 → APPLY
 → OBSERVE OUTCOME
 → VERIFY
 → LEDGER / EVIDENCE
 → LEARNING
 → CONTINUITY
```

## Product projection lifecycle
Canonical backend state is projected into product surfaces:
```text
CANONICAL OBJECTS + EVENTS
        ↓
AUTHORIZED RETRIEVAL / ADAPTERS
        ↓
HUB PROJECTION
        ↓
USER INTERACTION
        ↓
AUTHORIZED COMMAND
        ↓
DOMAIN ACTION
        ↓
EVENT / RECEIPT / LEDGER RECORD
        ↓
UPDATED PROJECTION
```

## Event rule
Every cross-system action must identify: actor, authority scope, event type, target object, source/context, time, resulting state, provenance, and correlation/lineage where applicable. Do not invent a new event if an existing canonical event contract already covers the behavior.

## Front-end requirements
- Route and navigation must map to a defined product surface.
- UI state must represent loading, empty, error, unauthorized and stale states.
- Actions must show the correct authority/confirmation boundary.
- Displayed data must be traceable to an API/adapter contract.
- Optimistic UI is allowed only when reconciliation is deterministic and failure is visible.
- UI must never imply VERIFIED solely because an object is displayed.

## Back-end requirements
- Authenticated identity resolution.
- Authorization before protected reads/writes.
- Canonical data owner for every mutation.
- Idempotency for retryable consequential operations.
- Stable IDs and timestamps.
- Explicit event/receipt generation for meaningful state changes.
- Observability sufficient to reconstruct the transaction.
- No duplicate intelligence stores merely for presentation.

## Failure rule
When an operation fails: observe concrete failure → classify → identify root cause → make a changed repair → rerun → verify. Do not repeat an equivalent attempt without new information.

## NIS build sequence
1. Discover current source/runtime.
2. Map existing primitives to this flow.
3. Identify the smallest missing boundary.
4. Implement.
5. Test unit + integration + authenticated end-to-end behavior.
6. Compare source/build/deployed runtime where applicable.
7. Record evidence and state.
8. Continue from the highest-value unresolved action.
