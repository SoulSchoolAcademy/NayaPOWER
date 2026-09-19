# Intelligent Reports — Engineering Specification

## What / why
Intelligence Reports synthesize intelligence across a defined period longer than the daily Today surface. They turn accumulated activity/intelligence into patterns, lessons, changes, decisions, outcomes and useful next actions.

## Human interface
Report index with period/type filters; report detail with executive synthesis, key patterns, important changes, lessons, unresolved items, decisions/outcomes and source drill-down. Every derived claim should provide a path to its supporting canonical intelligence/evidence when appropriate.

## Front end requirements
- Report list/search/filter.
- Period selector and report type/context.
- Structured synthesis blocks.
- Source/evidence drill-down.
- Clear generated/derived status.
- Save/list/share where authorized.
- Loading/error/empty/unauthorized states.

## Back end requirements
- Query authorized Smart Notes, events, Today outputs where appropriate, Ledger evidence, project/Space state, communications and outcomes over a defined period.
- Cluster and synthesize patterns without replacing source truth.
- Preserve source references, time window, provenance and generation/version metadata.
- Support regeneration when sources materially change.
- Respect privacy across personal/Space/collective scopes.
- Avoid double-counting derived reports as independent evidence.

## Data / API contract
Conceptual report: `report_id, scope, period_start, period_end, report_type, sections, source_refs, evidence_refs, generated_at, version, status, verification_state`. Exact persistence/API follows current report architecture.

## Connections
`Today → report inputs`; `Feed/events → activity`; `Smart Notes → intelligence`; `Ledger → evidence`; `Lists/Spaces/Projects → context`; `CIS/Adaptive Learning → patterns`; `Continuity → carry-forward`; `Library → durable knowledge`.

## Verification
Generate a report from known source events; verify each material conclusion traces to source; verify time-window boundaries; modify/delete a source and verify defined regeneration behavior; test private/collective isolation; verify report retrieval after refresh.

## Current state
**DEFINED** by `.naya/05` and master architecture. Runtime completeness must be established from current implementation rather than the concept document.

## Gap / next action
Inspect existing report generation/storage/runtime and establish the canonical report pipeline and evidence-trace contract.

## Source authority
`.naya/2026-09-11-NAYAPOWER-05-INTELLIGENCE-REPORTS-SMART-NOTE.md`; `.naya/2026-09-11-18-35-NAYAPOWER-32-MASTER-SYSTEM-ARCHITECTURE.md`; `.naya/2026-09-12-NAYAPOWER-50-INTELLIGENT-SEARCH-RETRIEVAL-CONTRACT.md`.


## COMPLETION CHECKLIST — 2026-09-19

- [x] Source contract identified
- [x] .naya authority identified
- [x] Report architecture identified
- [x] Ledger report hook identified
- [ ] Report UI mapped
- [ ] Generation/storage pipeline mapped
- [ ] Source/evidence traceability proven
- [ ] Period boundaries proven
- [ ] Regeneration proven
- [ ] Privacy isolation proven
- [ ] Fresh retrieval proven
- [x] Dated activity record exists
- [x] One next action recorded

**Current state:** DEFINED. See [2026-09-19 activity](../ACTIVITY/2026/09/19/INTELLIGENT-REPORTS.md).
