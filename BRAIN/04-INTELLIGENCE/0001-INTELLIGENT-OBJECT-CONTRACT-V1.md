# Intelligent Object Contract V1

**Status:** CANONICAL BUILD CONTRACT

An Intelligent Object is durable, addressable intelligence that can be retrieved and safely interpreted.

## Required fields
`object_id, object_type, owner_scope, title, meaning, source_refs[], provenance, truth_state, authority_state, privacy_state, lifecycle_state, node_ids[], relationship_ids[], created_at, updated_at, version`.

## Laws
- Identity is stable and provenance is mandatory.
- Retrieval is read-only with respect to authority.
- Unknown truth/authority/lifecycle remains explicit.
- Supersession and revocation preserve lineage.
- Missing required fields invalidate the object.

## Acceptance
Schema validation rejects malformed objects and cold retrieval returns the same canonical identity, version, scope, and lineage.
