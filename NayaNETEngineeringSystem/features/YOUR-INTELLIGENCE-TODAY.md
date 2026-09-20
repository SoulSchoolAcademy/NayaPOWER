# Your Intelligence Today — Engineering Specification

## What / why
Your Intelligence Today is a derived daily intelligence synthesis surface. It answers: **What happened? What mattered? What did I learn? What changed? What should I carry forward?** It is not a duplicate Feed or canonical storage layer.

## Human interface
Daily briefing with only sections earned by the day's evidence. Possible blocks: Top Highlights, Biggest Aha, Top Lessons, Problems Solved, Key Decisions, Carry Forward. Each highlight drills down to Smart Note/Intelligent Block → related intelligence → source/evidence.

Never fabricate a section to fill a template.

## Front end requirements
- Daily route/date selector.
- Briefing/highlight cards with source links.
- Clear distinction between synthesis and source.
- Drill-down and carry-forward actions.
- Empty/low-intelligence day state that is truthful, not artificially filled.
- Loading/error/unauthorized states.
- Optional save/list/share actions where authorized.

## Back end requirements
- Retrieve day's authorized meaningful events, Smart Notes, verified outcomes, decisions, project/state changes and relevant Ledger evidence.
- Classify/cluster/rank/synthesize without changing source truth.
- Store/cache derived briefing with source references if useful.
- Preserve provenance, confidence/verification state and generation time.
- Rebuild/invalidate when canonical sources materially change.
- Respect source visibility and item-level authorization.

## Data / API contract
Conceptual briefing: `date/window, scope, highlight_ids, source_refs, categories, importance/novelty/relevance/learning signals, confidence, verification_state, carry_forward_refs, generated_at, provenance`. Exact API/storage is implementation-specific.

## Intelligence rules
Surface responsible value, not verbosity or engagement. Do not manufacture intelligence. A summary is navigation/understanding, not replacement for source.

## Connections
`Feed → daily source activity`; `Smart Notes → durable inputs`; `Ledger → evidence`; `Reports → longer horizon`; `Lists → organization`; `Continuity/MVPA → carry-forward`; `Superbrain/CIS → context and compounding`.

## Verification
Create meaningful events/notes; generate Today; verify each highlight traces to source; change source and verify derived behavior; test private source leakage; test empty day; refresh and compare retrieval; verify carry-forward state.

## Current state
**DEFINED** by `.naya/04`; architecture explicitly treats it as a derived daily view.

## Gap / next action
Inspect current Today/Hub implementation and map the daily synthesis pipeline to actual canonical sources and runtime endpoints.

## Source authority
`.naya/2026-09-11-NAYAPOWER-04-YOUR-INTELLIGENCE-TODAY-SMART-NOTE.md`; `.naya/2026-09-11-18-35-NAYAPOWER-32-MASTER-SYSTEM-ARCHITECTURE.md`; `.naya/2026-09-12-NAYAPOWER-49-REALTIME-LIVING-HUB-CONTRACT.md`.


## COMPLETION CHECKLIST — 2026-09-19

- [x] Source contract identified
- [x] .naya authority identified
- [x] Derived-view architecture identified
- [ ] Deployed Today surface mapped
- [ ] Canonical daily source query proven
- [ ] Synthesis pipeline proven
- [ ] Source traceability proven
- [ ] Private-source isolation proven
- [ ] Empty-day behavior proven
- [ ] Carry-forward behavior proven
- [ ] Refresh/rebuild behavior proven
- [x] Dated activity record exists
- [x] One next action recorded

**Current state:** DEFINED. See [2026-09-19 activity](../ACTIVITY/2026/09/19/YOUR-INTELLIGENCE-TODAY.md).
