# Object Types V1

**Status:** CANONICAL BUILD CONTRACT

## Canonical classes
- **NODE** — one of the nine Master Nodes.
- **INTELLIGENT_OBJECT** — durable addressable intelligence.
- **RELATIONSHIP** — typed directed connection.
- **EVENT** — immutable temporal fact.
- **EVIDENCE** — material supporting or constraining a claim.
- **VERIFICATION** — determination about a claim, action, or outcome.
- **LEARNING** — verified durable lesson eligible for controlled promotion.
- **SUCCESSOR_HANDOFF** — bounded continuity package for a cold successor.

## Universal envelope
Every object has `id, type, owner_scope, lifecycle_state, version, provenance, created_at, updated_at`; truth/authority/privacy fields are mandatory where applicable.

## Laws
Existence never grants authority. Retrieval never grants authority. Historical objects never silently become current truth. Unknown object types and malformed envelopes fail closed.

## Acceptance
Runtime rejects unknown types and missing required envelope fields and preserves identity/lineage across serialization and cold restore.
