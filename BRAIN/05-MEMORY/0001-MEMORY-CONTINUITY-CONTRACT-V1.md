# Memory & Continuity Contract V1

**Status:** CANONICAL BUILD CONTRACT

## Purpose
Durably retain intelligence so a cold Naya can reconstruct the correct current context without human re-explanation.

## Canonical loop
`PERSIST → DESTROY WORKING CONTEXT → COLD RESTORE → RETRIEVE → UNDERSTAND → APPLY`

## Required retained state
Identity, owner/scope, version, relationships, provenance, evidence, verification, learning, supersession, revocation, and current lifecycle state.

## Laws
- Persistence is the canonical durable boundary.
- Memory must never silently convert history into current truth.
- Retrieval must preserve owner/scope and lineage.
- Missing or ambiguous identity fails closed.
- Cache/session/UI state is not canonical memory.

## Acceptance
A cold-round-trip receipt must show the same canonical object was persisted, working context was discarded, the object was retrieved from canonical persistence, and the retrieved intelligence changed a subsequent decision or action.
