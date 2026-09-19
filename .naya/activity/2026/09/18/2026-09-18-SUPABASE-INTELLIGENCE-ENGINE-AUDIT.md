# 2026-09-18 — SUPABASE INTELLIGENCE ENGINE AUDIT — ARCHITECTURE FREEZE + BUILD MATRIX

**Status:** AUDIT EXECUTED / ARCHITECTURE FREEZE PROPOSED / NO NEW MIGRATION CREATED

## Purpose

Establish the shared-machine architecture for NayaNET before implementing Smart Ledger, Reports, or Smart Spaces.

The governing principle is:

> **One authenticated, permissioned canonical intelligence/event substrate; multiple projections.**

The Hub sidebar is a set of experience surfaces over that machine, not seven independent systems.

## Live production audit

Project: `dahisasgpfvziswqvmvm`

Live public schema currently contains 32 tables, including:

- Identity/profile: `members`, `nayanet_profiles`, `v7_profiles`
- Cognition/intelligence: `nayanet_cognition_events`, `nayanet_project_cognition_state`, `nayanet_intelligence_index`, `nayanet_notes`
- Smart Notes: `smart_note_events`, `smart_note_artifacts`, `smart_note_receipts`, `v7_smart_note_transactions`
- Learning: `learner_states`, `learning_evidence`, `maxess_results`, assessment tables
- Governance/execution: `nayanet_authority_grants`, `nayanet_execution_receipts`, `nayanet_policy_versions`, `nayanet_policy_evaluations`
- Reports/intelligence projections: `v7_intelligence_reports`, `v7_daily_intelligence`, `v7_collective_wisdom`
- Spaces: `nayanet_spaces`
- Communication/connections: `v7_mail_threads`, `v7_mail_members`, `v7_mail_messages`, `v7_connection_requests`
- Dream: `nayanet_dream_replays`

Live public routines include the canonical cognition commit/record/initialize functions, Smart Note creation/list/verification functions, authority issuance/validation/revocation, execution/policy functions, intelligence indexing, and Smart Mail functions.

Live triggers already project source changes into `nayanet_intelligence_index`, including from `smart_note_events`, `smart_note_receipts`, `nayanet_notes`, `nayanet_project_cognition_state`, and `nayanet_execution_receipts`.

RLS is enabled on the production domain tables inspected. Ownership policies use authenticated identity boundaries such as `auth.uid() = user_id` / `member_id` / `owner_id`, with Smart Note artifact/receipt policies joining through the owning Smart Note event.

## Architecture decision

Do **not** create parallel databases for Smart Notes, Activity, Ledger, Reports, Learning, CCT, or Spaces.

The current production substrate already demonstrates the pattern:

`source object/event -> indexed intelligence -> derived projection`

Therefore the next implementation must prefer:

1. **REUSE** existing canonical tables/functions.
2. **EXTEND** existing contracts where their semantics match.
3. **CREATE** only genuinely missing domain primitives.
4. **CONNECT** projections through explicit provenance/relationships.
5. **VERIFY** behavior with real authenticated transactions before calling it proven.

## Build matrix

| Domain | Existing production substrate | Decision | Required next work |
|---|---|---|---|
| Identity & ownership | `auth.users`, `members`, `nayanet_profiles`, RLS | **REUSE** | Finish real two-identity behavioral proof; no second identity system |
| Canonical cognition events | `nayanet_cognition_events` + record/commit/init routines | **REUSE / EXTEND** | Establish whether this or Smart Note event registry is the generalized event spine; do not duplicate blindly |
| Smart Note event registry | `smart_note_events` + artifacts + receipts + canonical RPC | **REUSE** | Make it a primary intelligence-event producer; preserve four-artifact verification semantics |
| Intelligence index | `nayanet_intelligence_index` + triggers | **REUSE** | Treat as retrieval/index projection, not canonical event truth |
| PIS/current cognition | `nayanet_project_cognition_state` | **REUSE** | Connect canonical event outputs; preserve owner RLS |
| CIS/learning | `learner_states`, `learning_evidence` and existing learning infrastructure | **REUSE / EXTEND** | Connect verified learning lifecycle; never equate memory with learning |
| Execution evidence | `nayanet_execution_receipts` | **REUSE** | Make Ledger consume/relate to existing receipts rather than copy them |
| Authority/governance | `nayanet_authority_grants`, policy versions/evaluations | **REUSE** | Keep authority separate from cognition ownership; explicit permissioned bridge only |
| Activity | Existing projection/feed surfaces plus event sources | **EXTEND / CONNECT** | Make Activity a projection of canonical events, not another event truth |
| Smart Ledger | Canonically defined in repository; no dedicated live Ledger domain identified in audit | **CREATE / CONNECT** | Build evidence/verification/value/points projection over canonical events and existing receipts |
| Reports | `v7_intelligence_reports`, `v7_daily_intelligence` already exist | **REUSE / EXTEND** | Consolidate/clarify report contract and provenance; do not create a second report store |
| Smart Spaces | `nayanet_spaces` exists | **EXTEND** | Extend contract for memberships/interactions/events only where missing; emit canonical events |
| CCT / lineage | Existing repository contract + relationship concepts; no dedicated live relationship table identified in inspected schema | **CREATE / CONNECT** | Add the smallest verified relationship substrate after event spine decision |
| Collective intelligence | `v7_collective_wisdom` + consent/visibility infrastructure | **EXTEND / VERIFY** | Derive only from explicitly scoped/provenanced/verified inputs |
| Smart Mail | `v7_mail_*` + Smart Mail routines/Edge Function | **REUSE / CONNECT** | Emit communication events into common substrate |
| Connections | `v7_connection_requests` | **REUSE / CONNECT** | Treat relationship actions as canonical events; preserve consent/ownership |
| Dream | `nayanet_dream_replays` | **REUSE / CONNECT** | Keep replay simulation read-only and non-authoritative |
| YAML/Markdown artifacts | Repository Smart Notes / control-plane artifacts | **REUSE AS REPRESENTATION** | Human/machine-inspectable projection only; never substitute for runtime truth |

## Critical discovery

The audit found that **Reports and Spaces are not greenfield database domains**:

- `v7_intelligence_reports` already exists with owner, period, report, status, and timestamps.
- `v7_daily_intelligence` already exists with owner/date/report/wisdom/status/failure state.
- `nayanet_spaces` already exists with owner, name, purpose, visibility, timestamps.

Likewise, Smart Note already has an event/artifact/receipt transaction boundary, and execution receipts already carry evidence, learning, value, authority, policy, experiment, and decision-hash fields.

Therefore the immediate engineering problem is **integration and canonicalization**, not wholesale table creation.

## Smart Ledger boundary

Smart Ledger should be an evidence/integrity projection:

`canonical event -> evidence -> verification -> value -> points -> level -> relationship`

It must not become a second canonical event universe.

Existing `nayanet_execution_receipts` and `smart_note_receipts` are evidence sources to relate to Ledger. The Ledger must preserve the distinction:

- RECORDED
- EVIDENCE_AVAILABLE
- VERIFIED
- VALUED
- APPLIED
- OUTCOME_VERIFIED

No points, consensus, report, or AI assertion may itself be treated as proof.

## Verification boundary

The common governed lifecycle remains:

`PROPOSED -> PROCESSING -> READY -> AUTHORIZED -> EXECUTING -> EXECUTED -> OBSERVED -> VERIFIED`

Learning remains:

`OBSERVED -> CANDIDATE -> EVALUATED -> VERIFIED -> PROMOTED -> RETRIEVED -> APPLIED -> OBSERVED -> OUTCOME_VERIFIED`

These are state contracts, not labels to be inferred from mere existence.

## Identity/security boundary

The audit confirms the production RLS pattern is already owner-bound in the inspected tables.

The remaining behavioral proof for the Assistant lane is still separate:

**real authenticated User A -> own write/read**

**real authenticated User B -> own write/read**

**B cannot retrieve A**

**A cannot retrieve B**

That proof remains NOT PROVEN until the protected identity provisioning boundary exists and the real transaction is executed. No migration in this audit changes that status.

## Freeze

Before any new Smart Ledger / Reports / Smart Spaces migration:

1. Resolve the canonical event-spine decision from the existing `nayanet_cognition_events` and `smart_note_events` semantics.
2. Map existing functions and triggers to the chosen spine.
3. Define the minimum Ledger projection against existing receipts/events.
4. Reconcile the existing Reports tables against the canonical report contract.
5. Extend `nayanet_spaces` only for contract gaps and event emission.
6. Add CCT relationship storage only after source/target event identity is settled.
7. Prove each new boundary with authenticated transactions and machine receipts.

## NayaNET-wide notice

This activity record is the canonical project-level handoff for all Naya continuations:

> **The Hub is a projection layer. The machine underneath is shared. Do not build isolated feature databases. Reuse the existing authenticated event/intelligence substrate, extend only where necessary, and make evidence + verification first-class.**

This is now the architectural audit baseline for the next implementation phase.

**Audit result: COMPLETE. New schema creation: DEFERRED until canonical event-spine reconciliation is complete.**
