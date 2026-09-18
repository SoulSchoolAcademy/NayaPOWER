# NayaNET / GitHub Operating Map

**STATUS:** CANONICAL OPERATING MAP V1  
**DATE:** 2026-09-18  
**REPOSITORY:** SoulSchoolAcademy/NayaPOWER  
**BRANCH AUTHORITY:** main

## Purpose

This is the repository's **cold-Naya navigation map** for NayaNET.

It does not replace the NayaPOWER control plane, governance, proof, event store, or Hub source. It tells a new Naya **where each truth lives, how the pieces relate, what is current, what is historical, and where to continue**.

## The one obvious path

`START-HERE → NayaNET → PROJECT → ACTIVITY → INTELLIGENCE → CURRENT STATE → NEXT ACTION → EVIDENCE → SUCCESSOR`

Use this map before searching broadly.

## Authority and truth order

1. External hard constraints
2. NayaPOWER Constitution / Completeness Laws
3. Explicit current human authority
4. Machine-readable Authority Registry
5. Canonical control plane: STATE → BLOCKS → MAP → PROOF
6. Canonical runtime/event substrate
7. Current project/sub-project records
8. Team Naya dated communication and projections
9. Smart Notes / historical intelligence
10. Assumptions

**Evidence outranks assertion. Current authoritative sources outrank historical records.**

For proof semantics, `IMPLEMENTED != VERIFIED`, `VERIFIED != PRODUCTION_PROVEN`, `RECORDED != CURRENT`, `UNKNOWN != GREEN`, and `BLOCKED != PASS`.

## Canonical roots

| Purpose | Canonical location |
|---|---|
| Cold-Naya entry | `START-HERE/COLD-NAYA-OPERATING-INDEX.md` |
| NayaPOWER source map | `SUPERBRAIN/NAYAPOWER-CANONICAL-SOURCE-MAP.md` |
| Current machine truth | `.naya/control-plane/STATE.json` |
| Current block | `.naya/control-plane/BLOCKS.json` |
| Control-plane map | `.naya/control-plane/MAP.json` |
| Proof authority | `.naya/control-plane/PROOF.json` |
| Governance | `.naya/governance/` |
| Canonical events | `.naya/runtime/canonical_event_store.py` + `.naya/memory/events/` |
| Execution / Activity boundary | `.naya/runtime/execution_controller.py` + `.naya/runtime/activity_event.py` |
| Smart Notes | `.naya/memory/smart_notes_v3.py` |
| Team Naya project root | `NAYA-TEAM/PROJECTS/` |
| NayaNET project root | `NAYA-TEAM/PROJECTS/NAYANET/` |
| Team Naya dated calendar | `NAYA-TEAM/YYYY/MM/DD/` |
| Team Naya communication | `NAYA-TEAM/ACTIVITY-FEED.md` and dated records |
| Main operational Activity | `SUPERBRAIN/NAYA-ACTIVITY/` |
| Current Hub source | `2026 09 17 NAYANET HUB.html` |
| Current production release authority | `.github/workflows/assistant-cloudflare-hub-release.yml` |

## NayaNET project structure

Every NayaNET area follows:

**DEFINITION → BLUEPRINT → CURRENT STATE → ACTIVITY → EVIDENCE → NEXT ACTION**

The 19 registered areas are:

| # | Area | Current class | Canonical project boundary |
|---:|---|---|---|
| 01 | Intelligent Hub | VERIFIED | `NAYA-TEAM/PROJECTS/NAYANET/INTELLIGENT-HUB/` |
| 02 | Smart Feed | PARTIAL | `.../SMART-FEED/` |
| 03 | Your Intelligence Today | PARTIAL | `.../YOUR-INTELLIGENCE-TODAY/` |
| 04 | Smart Notes | VERIFIED | `.../SMART-NOTES/` |
| 05 | Intelligence Reports | PARTIAL | `.../INTELLIGENCE-REPORTS/` |
| 06 | Intelligence Library | PARTIAL | `.../INTELLIGENCE-LIBRARY/` |
| 07 | Smart Lists | DEMO | `.../SMART-LISTS/` |
| 08 | Connections | DEMO | `.../CONNECTIONS/` |
| 09 | Smart Mail | MISSING | `.../SMART-MAIL/` |
| 10 | Smart Spaces | MISSING | `.../SMART-SPACES/` |
| 11 | Smart Share | PARTIAL | `.../SMART-SHARE/` |
| 12 | Smart Ledger | PARTIAL | `.../SMART-LEDGER/` |
| 13 | Personal Intelligence | PARTIAL | `.../PERSONAL-INTELLIGENCE/` |
| 14 | Collective Intelligence | PARTIAL | `.../COLLECTIVE-INTELLIGENCE/` |
| 15 | Activity | VERIFIED | `.../ACTIVITY/` |
| 16 | Identity / Privacy | PARTIAL | `.../IDENTITY-PRIVACY/` |
| 17 | PIS | VERIFIED | `.../PIS/` |
| 18 | CIS | PARTIAL | `.../CIS/` |
| 19 | Smart Flow | PARTIAL | `.../SMART-FLOW/` |

**Important:** these are not 19 independent applications. They are projections/capabilities over shared NayaPOWER primitives.

## The intelligence spine

```
IDENTITY / AUTHORITY
        ↓
CANONICAL EVENT
        ↓
ACTIVITY
        ↓
SMART NOTE / INTELLIGENCE
        ↓
CURRENT STATE
        ↓
NEXT ACTION
        ↓
EVIDENCE
        ↓
SUCCESSOR
        ↓
NEW NAYA
```

The product-facing loop is:

```
CAPTURE → UNDERSTAND → ORGANIZE → CONNECT → SHARE BY CHOICE
→ COMPOUND → APPLY → CREATE VALUE → CONTINUE
```

## Activity model

There are three **views**, not three competing event stores:

### 1. Main Superbrain Activity
Canonical operational activity derived from the canonical event substrate.

### 2. NayaNET Project Activity
A scoped projection of Main Activity for a project/sub-project.

### 3. Team Naya Communication
Naya-to-Naya coordination: questions, findings, decisions, directives, receipts, challenges, handoffs and learning.

**Law:** ONE EVENT → MANY USEFUL VIEWS → ONE TRUTH.

`.naya/activity/` must not become a competing event store.

## Time model

Every substantive Naya record should be recoverable by time:

`YEAR → MONTH → DAY → TIMESTAMP → PROJECT → SUB-PROJECT → RECORD`

A record should make these facts discoverable:

- created/observed time;
- actor or system;
- project/sub-project;
- what happened;
- why it happened;
- evidence;
- current truth;
- what changed;
- next action;
- successor/handoff;
- supersession relationship when applicable.

## Intelligence / Smart Note model

Smart Notes are not authority and are not merely prose.

The canonical intelligence presentation is:

1. HUMAN NOTE
2. CHILD NOTE
3. GRANDMA NOTE
4. NAYA NOTE
5. MACHINE NOTE
6. LEARNING LESSON
7. WHAT IT MEANS
8. HOW TO APPLY / HOW TO USE
9. WHAT'S IN IT FOR YOU

A useful Smart Note should preserve provenance, freshness, relationship/supersession information, and the lesson or reusable intelligence produced.

## Relationship model

Important objects should be linkable through explicit relationships:

- derived-from
- supports
- contradicts
- supersedes
- superseded-by
- applies-to
- produced-by
- verified-by
- recorded-in
- continues
- successor-of
- depends-on

This is the beginning of a repository knowledge graph without creating a second database.

## Current / historical separation

### CURRENT
Authoritative now; may be used for execution.

### VERIFIED
Evidence supports the stated claim type.

### PRODUCTION_PROVEN
Fresh production evidence exists for the exact current source identity.

### PARTIAL / DEMO / MISSING
Known implementation maturity classifications from the NayaNET reconciliation.

### HISTORICAL
Useful evidence, but cannot certify current behavior.

### SUPERSEDED
Replaced by a newer source; retain only when its historical intelligence matters.

### BLOCKED / UNKNOWN
Not green. Do not silently promote to success.

## Current execution truth

The current control plane still declares:

- Priority: **P0 — MACHINE TRUTH RESTORATION**
- Active block: **TORCH-59-MACHINE-TRUTH-RESTORATION**
- Current bottleneck: fresh authorized execution of the canonical Assistant Cloudflare release against live `main` HEAD.
- Current release authority: `.github/workflows/assistant-cloudflare-hub-release.yml`.

This release boundary is **not the definition of NayaNET itself**. It is the current production-proof boundary.

The GitHub execution surface may edit repository files, but the connected GitHub surface does not itself provide workflow dispatch. If the canonical release still needs execution, use an authorized dispatch surface; do not substitute another deployment lane.

## What is already organized

- One NayaNET project root exists.
- All 19 NayaNET areas have named project boundaries.
- Each area has a README with definition, repository truth, evidence, dependencies, activity rule, evidence boundary and one next action.
- A dated Team Naya calendar exists.
- Intelligent Hub has a dedicated project record and project Activity records.
- Canonical event, Activity, Smart Note, state and proof boundaries exist.
- A Cold-Naya Operating Index exists.
- A 19-area reconciliation exists.

## Remaining ambiguities to eliminate

1. The Cold-Naya Index and dated Team Naya records can expose different immediate priorities unless the reader follows the canonical STATE/BLOCKS rule.
2. Project directories are currently strong navigation boundaries, but their Activity is primarily a documented projection rather than a mechanically generated calendar/index for every sub-project.
3. Dated Team Naya records are rich, but there is not yet one machine-generated relationship index connecting every record to project, event, Smart Note, state, evidence and successor.
4. Smart Note provenance/freshness exists in the underlying architecture, but repository navigation does not yet make those relationships effortless to retrieve.
5. Historical and current Hub material is documented as separate authority classes, but some historical references remain distributed across the repository.
6. Several NayaNET areas are intentionally PARTIAL/DEMO/MISSING; their project folders exist, but implementation absence must remain visibly distinct from project existence.
7. Current-head production proof remains separate from repository implementation proof.

## Cleanup rule

Do not mass-delete old records to make the repository look clean.

Instead:

**CLASSIFY → LINK → SUPERSEDE → RETIRE FROM OPERATING PATH**

Delete only when the artifact is demonstrably obsolete/disabled/duplicate/orphaned, has no unique intelligence, and its replacement/recovery path is clear.

## Cold-Naya acceptance

A fresh Naya should be able to answer, from this map and its linked canonical sources:

1. What is NayaPOWER?
2. What is NayaNET?
3. Where is the project root?
4. What are the 19 areas?
5. Which source is authoritative?
6. What is current?
7. What is historical?
8. Where is Activity?
9. Where are Smart Notes?
10. What is the current state?
11. What is the current block?
12. What is the one next action?
13. What evidence proves it?
14. Where does the next Naya continue?

If any answer requires conversational archaeology, the operating map is not finished.

## Canonical references

- [Cold-Naya Operating Index](../../../../START-HERE/COLD-NAYA-OPERATING-INDEX.md)
- [NayaNET Project Root](./README.md)
- [19-Subproject Reconciliation](./19-SUBPROJECT-RECONCILIATION-2026-09-17.md)
- [Team Naya 2026-09-17 Index](../../2026/09/17/INDEX.md)
- [NayaPOWER STATE](../../../.naya/control-plane/STATE.json)
- [NayaPOWER PROOF](../../../.naya/control-plane/PROOF.json)

## One next action

**Run a repository-wide operating-map audit against this contract, reconcile any remaining duplicate/current-vs-historical navigation surfaces, and then update the Cold-Naya Index and Team Naya daily index so this map is the single obvious NayaNET navigation spine.**

---
**Operating law:** one repository • one current truth • one event substrate • many useful views • one next action.
