# Naya Intelligence Object (NIO) Model V1

**Status:** CANONICAL MACHINE/INTELLIGENCE INTERFACE MODEL

## 1. Purpose

A NIO is the machine-addressable envelope through which a meaningful intelligence object can move through NayaPOWER without losing identity, provenance, state, governance, or intended use.

NIO is an object contract, not a new database and not a new intelligence layer.

## 2. Required envelope

Every NIO should be able to expose:

- `nio_id`
- `nio_type`
- `version`
- `status`
- `owner_scope`
- `source`
- `meaning`
- `intent`
- `truth_state`
- `authority_context`
- `applicability`
- `freshness`
- `relationships`
- `evidence`
- `event_lineage`
- `application_history`
- `outcome`
- `verification`
- `learning_state`
- `successor_context`

Fields may be absent when genuinely unknown; they must never be fabricated.

## 3. NIO types

Initial canonical types:

- `EXPERIENCE`
- `EVENT`
- `INTELLIGENCE`
- `RULE`
- `DECISION`
- `ACTION`
- `OUTCOME`
- `EVIDENCE`
- `LEARNING`
- `SUCCESSOR`
- `SYSTEM_STATE`

These types describe semantic role. They do not require separate storage systems.

## 4. State separation

NIO must keep separate:

**meaning** from **evidence**  
**evidence** from **authority**  
**authority** from **value**  
**observation** from **outcome**  
**outcome** from **verification**  
**learning candidate** from **verified learning**  
**current state** from **history**

## 5. Machine behavior

A machine may:

1. parse;
2. validate;
3. route;
4. retrieve;
5. compare;
6. apply;
7. record;
8. verify;
9. learn;
10. hand off.

A machine may not infer authority from the NIO itself.

## 6. NIO lifecycle

```
CREATE → VALIDATE → GOVERN → INDEX → RETRIEVE → APPLY
→ OBSERVE → VERIFY → LEARN → COMPOUND → SUCCESSOR
```

Invalid objects stop at validation/governance boundaries.

## 7. Canonical storage rule

NIO is an interface contract. Intelligent Blocks and Events remain canonical persistence concepts.

Do not create:

- NIO database;
- NIO ledger;
- NIO memory;
- NIO retrieval engine

unless a proven responsibility cannot be served by the existing canonical substrate.

## 8. Identity rule

Every NIO references one stable canonical object identity and explicit versioning.

Aliases are routing conveniences. They are not new identities.
