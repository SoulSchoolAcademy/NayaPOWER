# NayaPOWER Persistence Contract V1
## Boundary
Durable intelligence is canonical only when stored in the governed persistence substrate with owner scope, provenance, schema version, lineage, state, and retrieval path.
## Required fields
object_id, owner_id, owner_scope, created_at, updated_at, schema_version, provenance, truth_state, status, superseded_by, lineage, content_hash.
## Read law
Every retrieval must enforce owner scope and current authorization context. Retrieval does not grant authority.
## Write law
Writes are append-safe and idempotent. Intelligence, proof, authority, and learning records are never silently overwritten.
## Supersession
Newer records point backward/forward through explicit lineage. Stale records remain inspectable but are not silently preferred.
## Acceptance
Live authenticated owner retrieval of canonical Intelligent Block; cross-owner denial; provenance preservation; supersession detection; duplicate-write idempotency; receipt reconstruction.
