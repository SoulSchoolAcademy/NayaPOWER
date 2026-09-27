# Knowledge Population Specification V1

**Status:** CANONICAL BUILD CONTRACT

## Purpose
Convert the external KNOWLEDGE corpus into governed Brain intelligence without creating a competing source of truth.

## Pipeline
`KNOWLEDGE source → concept → provenance → Node mapping → relationships → Intelligent Object → verification state → retrieval index`

## Laws
- KNOWLEDGE is the source corpus; BRAIN is its governed representation.
- Every populated item retains source path, source revision/hash, concept ID, mapped Node(s), and population status.
- Unmapped material remains explicitly `UNMAPPED`; it is never silently promoted.
- Duplicate concepts are linked or superseded, not copied as competing truth.
- A concept may map to multiple Nodes only with an explicit mapping reason.
- Population is reproducible from the declared source revision.

## Minimum record
`concept_id, source_ref, source_revision, distilled_claim, node_ids[], relationship_ids[], provenance, truth_state, authority_state, privacy_state, lifecycle_state`.

## Acceptance
A population run passes when every emitted record traces to source, every source item is accounted for, duplicate handling is deterministic, and repeating the run against the same revision yields the same canonical IDs.
