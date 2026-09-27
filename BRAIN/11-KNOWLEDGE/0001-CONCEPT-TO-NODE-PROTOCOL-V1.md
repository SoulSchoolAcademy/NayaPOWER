# Concept-to-Node Protocol V1

**Status:** CANONICAL BUILD CONTRACT

## Purpose
Map KNOWLEDGE concepts into the nine-node ontology with explicit reasoning and provenance.

## Mapping record
`concept_id, source_ref, source_revision, node_ids[], mapping_reason, relationship_ids[], confidence, truth_state, reviewer, timestamp`.

## Laws
- Mapping is an interpretation, not a rewrite of source knowledge.
- Every Node mapping has a reason and source evidence.
- One concept may map to multiple Nodes.
- Low-confidence or disputed mappings remain explicit and are not silently promoted.
- Mapping never grants authority.

## Acceptance
The same source revision produces deterministic concept IDs and stable Node mappings; every mapping is traceable to source and can be challenged or superseded.
