# NayaPOWER Inter-Node Wire Contract V1
Every node communicates through a versioned envelope: message_id, execution_id, source_node, target_node, contract_version, identity_context, authority_context, truth_context, provenance, payload, idempotency_key.
### Required routing
SELF→LAW; LAW→ACT; SELF→KNOW; KNOW→PROVE; KNOW→CONNECT; ACT→VERIFY; PROVE→VERIFY; VERIFY→LEARN; LEARN→EVOLVE; EVOLVE→SELF.
### Rules
No node may skip LAW for consequential execution. No downstream node may silently reinterpret an upstream receipt. Each transition returns a receipt and explicit state. Cross-node payloads are immutable snapshots; corrections create new lineage.
### Acceptance
Test schema rejection, wrong-target rejection, scope mismatch, stale version, replay, missing provenance, missing authority, contradictory truth, and successful round-trip receipt reconstruction.
