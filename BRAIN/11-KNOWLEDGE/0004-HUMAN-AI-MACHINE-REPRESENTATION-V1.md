# NayaPOWER Human / AI / Machine Representation Contract V1

**Purpose:** Make one canonical intelligence object simultaneously understandable by a human, usable by an AI reasoner, and deterministic for machines.

## One identity, many views

Every canonical object has one immutable `object_id`. Its representations are projections of that identity.

### HUMAN VIEW
Must answer in plain language:
- What is this?
- Why does it matter?
- What should I remember?
- When does it apply?
- What is uncertain?
- What should happen next?

### AI VIEW
Must expose:
- semantic type and purpose;
- context and applicability;
- dependencies and relationships;
- authority implications;
- conflicts and supersession;
- epistemic state;
- evidence requirements;
- safe-use and failure conditions;
- successor relevance.

### MACHINE VIEW
Must expose typed deterministic fields:
- `object_id`
- `object_type`
- `version`
- `status`
- `owner_id`
- `scope`
- `source_refs[]`
- `relationship_refs[]`
- `epistemic_state`
- `authority_state`
- `evidence_refs[]`
- `verification_refs[]`
- `applicability`
- `created_at`
- `updated_at`

### PROOF VIEW
Must expose:
- claim;
- evidence;
- method;
- verifier;
- scope;
- timestamp;
- result;
- limitations;
- unresolved gaps.

## Non-negotiable invariants

1. A representation never upgrades truth status.
2. A retrieved object never grants authority.
3. A human-friendly simplification must not delete meaning required for safe use.
4. A machine view must resolve to the same canonical identity as every other view.
5. AI reasoning may propose relationships; governed promotion establishes canonical relationships.
6. Historical views remain traceable to their source and supersession lineage.

## Acceptance test

Given any canonical object, a cold human, AI, and machine consumer must be able to independently identify the same `object_id`, purpose, current status, applicable scope, provenance, and unresolved uncertainty.
