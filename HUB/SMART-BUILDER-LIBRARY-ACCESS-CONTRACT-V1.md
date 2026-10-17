# Smart Builder Library Access Contract — v1

**Status:** implementation proposal committed on a working branch; not yet merged or production-proven.  
**Purpose:** remove the requirement for Shawn or another human to re-send library parts that already exist in GitHub.

## What the investigation found

There are multiple real registries, but they are not yet one automatically refreshed discovery surface:

- Main branch: `BRAIN/10-INTERFACES/DESIGN-BLOCKS/naya-design-catalog.json` (declares 91 entries; 91 records observed).
- Canonical Smart Blocks branch: `naya5/smart-blocks-library`, `smart-blocks/manifest.json` (58 records observed) and `smart-blocks/REGISTRY.md`.
- The human field manual explicitly says the unified Smart Blocks library is canonical but not merged to main. The older `naya-library/` shelf on main is superseded and must not be extended.
- The design catalog and Smart Blocks manifest use different IDs and scopes. They must remain separate source registries; their counts must not be presented as unique parts or blindly summed.

## The contract

1. **Discover first.** Search the generated inventory and source registries before inventing, extracting, or asking for an asset.
2. **Resolve by identity.** Each chosen part must resolve to a stable source ID, repository path, and pinned Git ref/SHA.
3. **Read the part's own contract.** Use recorded purpose, use/avoid guidance, dependencies, CSS classes, states, and source provenance.
4. **Resolve dependencies.** CSS, JavaScript, tokens, icons, fonts, and sibling blocks must be explicit. A missing dependency is a named build failure.
5. **Do not silently substitute.** If no matching part exists, report the gap with search evidence; only create a new part through the governed add-and-register process.
6. **Keep the source of truth singular.** The inventory is a generated discovery index, not another component registry. Do not hand-edit its derived records.
7. **Prove availability.** “Indexed” is not “standalone-tested,” “build-compatible,” or “production-proven.” The build verifier must check paths and dependencies at the exact pinned revision.
8. **Reproduce.** A build receipt records contract hash, source registry refs and blob SHAs, selected IDs, dependency closure, assembler version, output hash, and verifier results.
9. **Fail closed.** Missing, ambiguous, stale, or mismatched entries block the build rather than being treated as success.
10. **Improve once for everyone.** Repair the canonical source or resolver and add a regression test; do not make customer-specific copies of the same fix.

## What this branch adds

- A machine-readable cross-registry discovery index derived from the two existing source registries.
- A searchable HTML gallery with filters and direct links to the actual part/specimen files.
- A source-of-truth/access contract that documents how Naya and the assembler must use the library.

## Explicit limitations

- This is an inventory/discovery layer, not yet the full production Smart Builder or a verified deterministic assembler.
- Catalog entries do not prove that all dependencies exist or that every block works standalone.
- The unified Smart Blocks library still lives on its own branch; it is linked, not silently copied or claimed merged.
- The 478-piece count mentioned in earlier conversation is not asserted here because the current source registries inspected in this pass do not independently establish that as a count of unique, available, buildable parts.

## Acceptance tests for this layer

- Both source registries parse and their observed record counts are recorded separately.
- Every record has a stable composite key `source_registry:source_id`.
- Search covers name, category, description, use guidance, tags, classes, states, and dependencies.
- Every displayed source link points to a real repository path or source registry.
- The UI labels records as catalogued and does not imply runtime verification.
- The index can be regenerated from the source registries; derived data is never edited by hand.

## Next implementation stage

Connect this inventory to the assembler and template contract: template modules reference composite IDs, the resolver pins source revisions, assembles only resolved dependencies, and produces a deterministic self-contained mobile-first HTML/PWA candidate. Then verify output behavior and consumer-visible rendering before any claim of completion.
