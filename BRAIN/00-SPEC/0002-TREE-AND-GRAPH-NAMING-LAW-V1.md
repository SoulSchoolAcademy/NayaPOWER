# Tree & Graph Naming Law V1

**Status:** CANONICAL BUILD CONTRACT

## Purpose
One deterministic naming law for Brain objects, Nodes, relationships, files, and machine references.

## Laws
1. **PATH IS NAVIGATION. ID IS IDENTITY.** Paths may change; canonical IDs do not.
2. Canonical objects have one stable ID; display labels are mutable.
3. Nine Master Node IDs are exactly SELF, LAW, ACT, KNOW, PROVE, CONNECT, VERIFY, LEARN, EVOLVE.
4. Relationship IDs are deterministic from source ID + relation type + target ID; duplicate canonical edges are forbidden.
5. IDs never encode mutable state and are never reused.
6. Runtime MUST NOT invent IDs by guesswork; allocation is explicit and attributable.
7. Unknown IDs, ambiguous aliases, and collisions fail closed.
8. Archived, revoked, or superseded objects remain addressable for lineage but are not current truth.
9. Machine indexes reference canonical IDs, not filenames or free-form labels.

## Acceptance
The implementation passes when repeated allocation is deterministic, collisions are rejected, unknown IDs fail closed, and renaming a display label does not change identity.

## Evidence
Every canonical relationship/object receipt records ID, type, source/target where applicable, version, lifecycle, scope, provenance, and allocation evidence.
