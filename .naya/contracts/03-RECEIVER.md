# Contract 03 — Receiver V1

**Owns:** canonical intake and creation boundary for durable intelligence.  
**Does not own:** human intent interpretation, UI rendering, or independent learning claims.

## Purpose

The Receiver is where an authorized intelligence request becomes canonical NayaPOWER state.

## Required semantic sequence

As applicable, the receiver MUST establish:

**request identity → actor/principal → authority/scope → source/context → canonicalization → immutable IB identity → intelligence event → persistence → indexing → projection state → receipt → learning eligibility/state**

Internal batching is allowed; semantic boundaries are not.

## Receiver authority

The Receiver is authoritative for:

- canonical IB identity;
- canonical event;
- canonical persistence;
- provenance/lineage attachment;
- lifecycle state;
- transaction identity;
- projection eligibility.

## Sender boundary

The Sender MUST NOT allocate IB IDs, persist canonical state, claim receiver success without receiver evidence, assign verified learning, or manufacture Smart Links.

## Idempotency

Replay MUST NOT create an unintended duplicate consequence.

The receiver MUST reconcile an equivalent request to an existing result or create a new result only where the contract explicitly permits repetition.

## Failure

On a failed boundary:

- do not claim completion;
- preserve the failure receipt;
- identify the first failed boundary;
- expose partial persistence;
- define safe recovery/retry conditions.

## Acceptance tests

- Unauthorized request denied before canonical persistence.
- Authorized request receives one receiver-allocated immutable IB identity.
- Event → IB → persistence is traceable.
- Replay is idempotent or explicitly repeatable.
- Partial failure cannot produce false PASS.