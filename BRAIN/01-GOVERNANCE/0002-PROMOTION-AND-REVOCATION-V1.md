# Promotion, Revocation & Supersession V1

**Status:** CANONICAL SPECIFICATION — explicit state-transition invariants defined

Promotion must be evidence-bound.

```
RAW → CAPTURED → DISTILLED → STRUCTURED → CANDIDATE → SUPPORTED → VERIFIED → CANONICAL
```

The exact ladder may vary by object type, but no transition may weaken epistemic truth.

## State-transition invariants

1. Every transition has a source state, target state, actor, timestamp and reason.
2. Every transition is append-only in lineage; history is never rewritten.
3. A transition MUST satisfy the target state's proof requirements.
4. `CANDIDATE → VERIFIED` requires evidence appropriate to the object type.
5. `VERIFIED → CANONICAL` requires successful canonicalization/index validation.
6. A failed promotion produces a rejection receipt; it does not silently downgrade or disappear.
7. Revocation changes current applicability but preserves provenance and history.
8. Supersession creates explicit old→new lineage and never mutates the historical object into the new meaning.
9. Contradictory evidence remains explicit until reconciled.
10. Promotion, revocation and supersession are distinct operations and MUST NOT be represented by one overloaded status value.

## Revocation

Revocation removes current applicability without destroying provenance.

A revocation record MUST identify:

- subject object;
- authority/source of revocation;
- reason;
- effective time;
- scope;
- replacement/superseding object when known.

## Supersession

Supersession establishes lineage from old understanding to new understanding.

A superseding object MUST identify:

- superseded object;
- reason for change;
- effective applicability;
- supporting evidence;
- whether the old object remains historically retrievable.

## Fail-closed rule

If the system cannot prove a requested transition is authorized and evidence-complete, the transition remains unpromoted and the failure is recorded.
