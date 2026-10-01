# NayaPOWER Inter-Node Wire Contract V1

Every node communicates through a versioned envelope: message_id, execution_id, source_node, target_node, contract_version, identity_context, authority_context, truth_context, provenance, payload, idempotency_key.

## Semantic order vs runtime routing

The nine-organ semantic/display order is:

`SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE → SELF`

That order describes the organism. It is **not** a rule that every runtime message must traverse one linear call stack. Runtime communication is a governed graph with explicit fan-out/fan-in.

## Required routing

- SELF → LAW
- SELF → KNOW
- LAW → ACT
- ACT → VERIFY
- KNOW → PROVE
- KNOW → CONNECT
- PROVE → VERIFY
- CONNECT → VERIFY
- VERIFY → LEARN
- LEARN → EVOLVE
- EVOLVE → SELF

Additional typed routes may exist when justified by a canonical contract, but they do not replace these minimum routes and may not create authority.

## Rules

No node may skip LAW for consequential execution. No downstream node may silently reinterpret an upstream receipt. Each transition returns a receipt and explicit state. Cross-node payloads are immutable snapshots; corrections create new lineage.

A semantic neighbor is not automatically a runtime handoff. Node objects and graph edges MUST distinguish presentation/organism order from executable routing.

## Acceptance

Test schema rejection, wrong-target rejection, scope mismatch, stale version, replay, missing provenance, missing authority, contradictory truth, successful round-trip receipt reconstruction, required-route presence, and graph source/target direction consistency.
