# Graph Contract V1

**Status:** CANONICAL BUILD CONTRACT

The Brain graph represents typed relationships that can influence contextual retrieval.

## Edge envelope
`edge_id, source_id, target_id, relation_type, direction, priority, provenance, truth_state, owner_scope, lifecycle_state`.

## Laws
- Edges are directed and typed.
- Relationship existence is not proof of truth.
- Scope and provenance travel with the edge.
- Graph context may influence retrieval only when applicable to the current task.
- Unknown, revoked, or out-of-scope edges cannot silently drive decisions.

## Acceptance
A live comparison must show baseline retrieval versus relationship-aware retrieval, identify the edge that changed context, and preserve evidence for that routing decision.
