# NayaPOWER Canonical Object Types V1

**Status:** CANONICAL SPECIFICATION — minimum type contract defined  
**Purpose:** Prevent type proliferation while making every canonical object machine-validatable.

## Core object families

```
NODE EVENT PRINCIPLE RULE DECISION REQUIREMENT GOAL CONSTRAINT
INSIGHT CLAIM QUESTION UNKNOWN EVIDENCE VERIFICATION OUTCOME
LEARNING PROCEDURE CAPABILITY EXPERIMENT PREDICTION STATE
RELATIONSHIP SUCCESSOR
```

## Universal envelope

Every object has stable identity, type, provenance, status and relationships.

Minimum universal fields:

| Field | Requirement |
|---|---|
| `id` | unique, immutable |
| `type` | member of this registry |
| `status` | valid lifecycle state |
| `provenance` | one or more resolvable lineage references |
| `relationships` | typed relationship list; empty only when justified |
| `created_at` | canonical timestamp |
| `updated_at` | canonical timestamp |

## Minimum semantic fields by type

| Type | Required semantic fields |
|---|---|
| NODE | responsibility, purpose, applicability |
| EVENT | actor, action, occurred_at, source |
| PRINCIPLE | proposition, scope |
| RULE | condition, effect, enforcement_point |
| DECISION | decision, rationale, authority_scope |
| REQUIREMENT | condition, acceptance |
| GOAL | objective, success_measure |
| CONSTRAINT | constraint, scope |
| INSIGHT | proposition, evidence_basis |
| CLAIM | proposition, epistemic_state |
| QUESTION | question, context |
| UNKNOWN | unknown, blocked_reason_or_missing_evidence |
| EVIDENCE | evidence_ref, provenance, integrity |
| VERIFICATION | subject_ref, verifier, verdict, evidence |
| OUTCOME | action_ref, observed_result, observed_at |
| LEARNING | lesson, evidence_basis, future_behavior |
| PROCEDURE | steps, preconditions, verification |
| CAPABILITY | capability, boundary, authority_required |
| EXPERIMENT | hypothesis, control, treatment, metric |
| PREDICTION | forecast, basis, uncertainty |
| STATE | subject_ref, state, as_of |
| RELATIONSHIP | relationship_id, source_id, target_id, relationship_type |
| SUCCESSOR | predecessor_ref, successor_ref, inherited_intelligence, authority_inherited |

## Creation law

A new object type requires:

1. a demonstrated responsibility gap;
2. a stable schema;
3. lifecycle semantics;
4. provenance requirements;
5. authorization implications;
6. proof/acceptance requirements;
7. a machine validator.

It is not created merely for organizational convenience.

## Validation law

A canonicalizer MUST reject:

- unknown object types;
- missing universal fields;
- invalid type-specific fields;
- unresolved provenance;
- malformed relationships;
- identity collisions;
- status transitions unsupported by the object's contract.

Unknown fields may be preserved for forward compatibility only when the object's versioned contract explicitly permits them.
