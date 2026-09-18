Repository Relationship Index Contract

STATUS: CANONICAL RELATIONSHIP / INDEX LAYER V1
DATE: 2026-09-18
AUTHORITY: Derived navigation only. It never overrides STATE, BLOCKS, MAP, PROOF, governance, canonical events, or human authority.

Purpose

Create a repository-wide relationship layer over existing records so any Naya can move from a record to its project, event, activity, intelligence, state, evidence, successor, and related records without creating another database.

Design law

ONE RECORD → MANY EXPLICIT LINKS → ONE CANONICAL TRUTH.

This layer is a derived index/projection. Existing files remain the records of truth.

Relationship vocabulary

derived-from, supports, contradicts, supersedes, superseded-by, applies-to, produced-by, verified-by, recorded-in, continues, successor-of, depends-on, references.

Node classes

CONTROL_PLANE, GOVERNANCE, RUNTIME, EVENT, ACTIVITY, SMART_NOTE, PROJECT, SUBPROJECT, TEAM_NAYA, SOURCE, WORKFLOW, TEST, EVIDENCE, HANDOFF, ISSUE, OTHER.

Required navigation

time → project → subproject → record → related records → current state → evidence → successor

Sources

Relationships may be derived from canonical path conventions, NayaNET boundaries, dated Team Naya records, canonical event paths/IDs, Main Superbrain Activity, Smart Notes, control-plane references, explicit Markdown/JSON links, and detectable issue/workflow/test/source references.

The layer must not invent semantic relationships merely because names look similar.

Current versus historical

Preserve the record's current/historical classification when known. The index itself is never proof of verification.

Regeneration

Run: python scripts/build_repository_relationship_index.py

The builder is deterministic for the same repository tree, uses no network, writes only the two declared projections, and never mutates source records.

Non-goals

Do not create another event store, memory database, Smart Note system, Activity database, authority registry, queue, or handoff system.

Cold-Naya acceptance

A cold Naya should be able to use the index to answer: What record is this? What project/sub-project does it belong to? What event/activity produced or records it? What intelligence does it create or depend on? What state/evidence does it connect to? What supersedes or contradicts it? What is its successor? What other records are directly related?

If a relationship cannot be established from repository evidence, mark it UNKNOWN rather than guessing.
