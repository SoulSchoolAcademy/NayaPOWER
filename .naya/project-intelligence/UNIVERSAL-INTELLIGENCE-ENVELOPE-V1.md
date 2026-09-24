# UNIVERSAL INTELLIGENCE ENVELOPE V1

STATUS: CANONICAL BOUNDED CONTRACT
VERSION: V1
PURPOSE: normalize a meaningful output before it enters an existing governed intelligence receiver.

## Boundary

A sender produces a **Universal Intelligence Envelope**. The envelope is an input contract, not a second intelligence store and not a new authority model.

```
SENDER OUTPUT
→ ENVELOPE V1
→ EXISTING GOVERNED RECEIVER
→ INTELLIGENT EVENT / PROJECT INTELLIGENCE
→ EXISTING INDEX / PROJECTION / RECEIPT
```

The existing Project Intelligence Bridge V1 remains the receiver transport contract. The existing Intelligent Event V1 remains the canonical temporal intelligence object. `intelligence_commit` is unchanged.

## Required fields

- `schema` = `NAYANET_UNIVERSAL_INTELLIGENCE_ENVELOPE_V1`
- `envelope_id`
- `source`
- `identity`
- `owner_scope`
- `occurred_at`
- `received_at`
- `output`
- `meaningfulness`
- `provenance`
- `epistemic`
- `privacy`
- `authority`
- `context`
- `idempotency_key`

## Meaningfulness

The sender must explicitly classify the output:

- `MEANINGFUL`: eligible to enter the governed receiver path.
- `NOT_MEANINGFUL`: retained only by the caller's working context; it must not be promoted by this contract.

A meaningful classification does not mean VERIFIED truth. It only says the output is worth evaluating for durable intelligence.

## Epistemic truth

Allowed epistemic states:

- `UNKNOWN`
- `OBSERVED`
- `VERIFIED`

`UNKNOWN` is never silently promoted to `OBSERVED` or `VERIFIED`.

## Privacy

Default visibility is `PRIVATE`. Sharing requires an explicit policy decision/consent path already enforced by the receiver.

## Authority

The envelope may describe authority context, but it never creates authority. Consequential receiver actions continue through the existing `ExecutionAuthorization` / `UniversalExecutionGate` boundary.

## Provenance

Provenance must identify the originating sender and source reference. Derived content must retain its source identity.

## Receiver compatibility

The adapter MUST NOT create a new persistence path. It must hand the envelope to the existing canonical receiver contract.

The receiver remains responsible for authentication, authorization, validation, persistence, indexing, projection, retrieval, and receipt.

## Idempotency

`idempotency_key` identifies the logical delivery. Replaying the same envelope must not create a second canonical effect where the existing receiver defines idempotency.

## Failure contract

Malformed envelopes, missing provenance, missing identity, non-private default visibility, or missing idempotency are rejected before consequential receiver work.

No rejection may be represented as successful intelligence.

## Proof boundary

This contract is PROVEN only when an independent process demonstrates:

1. a valid envelope is accepted by the adapter;
2. the adapter reaches the existing receiver without a competing store;
3. malformed envelope cases fail before receiver mutation;
4. the receiver's existing persistence/index/receipt identity is preserved;
5. exact replay remains idempotent.

This proof does **not** by itself prove universal coverage of every future sender.
