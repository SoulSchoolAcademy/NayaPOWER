# NayaNET / GitHub Operating Map

**STATUS:** CANONICAL OPERATING MAP V2
**DATE:** 2026-09-18
**REPOSITORY:** SoulSchoolAcademy/NayaPOWER
**BRANCH AUTHORITY:** main

## Purpose

This is the repository's cold-Naya navigation map for NayaNET. It tells a new Naya where each truth lives, how the pieces relate, what is current, what is historical, and where to continue.

## The one obvious path

START-HERE → NayaNET → PROJECT AREA → CURRENT STATE → ACTIVITY → SMART NOTES → EVIDENCE → NEXT ACTION → SUCCESSOR

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

Evidence outranks assertion. Current authoritative sources outrank historical records.

## Canonical roots

| Purpose | Canonical location |
|---|---|
| Cold-Naya entry | START-HERE/COLD-NAYA-OPERATING-INDEX.md |
| NayaPOWER source map | SUPERBRAIN/NAYAPOWER-CANONICAL-SOURCE-MAP.md |
| Current machine truth | .naya/control-plane/STATE.json |
| Current block | .naya/control-plane/BLOCKS.json |
| Control-plane map | .naya/control-plane/MAP.json |
| Proof authority | .naya/control-plane/PROOF.json |
| Governance | .naya/governance/ |
| Canonical events | .naya/runtime/canonical_event_store.py + .naya/memory/events/ |
| Execution / Activity boundary | .naya/runtime/execution_controller.py + .naya/runtime/activity_event.py |
| Smart Notes engine | .naya/memory/smart_notes_v3.py |
| Team Naya project root | NAYA-TEAM/PROJECTS/ |
| NayaNET project root | NAYA-TEAM/PROJECTS/NAYANET/ |
| Team Naya dated calendar | NAYA-TEAM/YYYY/MM/DD/ |
| Team Naya communication | NAYA-TEAM/ACTIVITY-FEED.md and dated records |
| Main operational Activity | SUPERBRAIN/NAYA-ACTIVITY/ |

## NayaNET project structure

NayaNET has 19 registered areas. Every area now physically conforms to the same operating workspace:

AREA/
├── README.md
├── CURRENT-STATE.md
├── ACTIVITY/
├── SMART-NOTES/
├── EVIDENCE.md
└── NEXT-ACTION.md

Existing area-specific artifacts remain in place; this structure is additive and does not erase historical or engineering records.

The 19 areas are:

1. Intelligent Hub
2. Smart Feed
3. Your Intelligence Today
4. Smart Notes
5. Intelligence Reports
6. Intelligence Library
7. Smart Lists
8. Connections
9. Smart Mail
10. Smart Spaces
11. Smart Share
12. Smart Ledger
13. Personal Intelligence
14. Collective Intelligence
15. Activity
16. Identity / Privacy
17. PIS
18. CIS
19. Smart Flow

These are connected capabilities/views, not 19 independent applications.

## What each area means

- README.md: what the area is, why it exists, boundary, connections and engineering contract.
- CURRENT-STATE.md: what is true about the project now; never a substitute for runtime proof.
- ACTIVITY/: what happened in this area and what the next Naya needs for handoff.
- SMART-NOTES/: what this area learned that should be durable and reusable.
- EVIDENCE.md: direct receipts and evidence index; no invented proof.
- NEXT-ACTION.md: exactly one continuation action.

## Activity model

There are three scopes of operational/coordination view, not three competing event stores:

### 1. NayaPOWER Main Activity
Canonical operational activity derived from the canonical event substrate.

### 2. NayaNET Project / Area Activity
Scoped projections and working views of Main Activity for NayaNET and an individual area.

### 3. Team Naya Communication
Naya-to-Naya coordination: sign-in, findings, questions, decisions, directives, challenges, handoffs and sign-out.

Law: ONE EVENT → MANY USEFUL VIEWS → ONE TRUTH.

Team Naya communication is separate from operational Activity. Area Activity must never become a competing event store.

## Intelligence model

Smart Notes are durable intelligence, not authority and not merely prose. Live conversation may produce an event and/or Smart Note; ingestion, PIS, relationships and CIS determine how intelligence compounds. Area Smart Notes are organized views of that shared intelligence system.

## Time model

Every substantive record should be recoverable by:

YEAR → MONTH → DAY → TIMESTAMP → PROJECT → AREA → RECORD

Use YYYY/MM/DD/YYYY-MM-DDTHH-MM-SSZ__TOPIC.md for dated Activity and Smart Note records.

## Relationship model

Important objects should be linkable through explicit relationships such as derived-from, supports, contradicts, supersedes, applies-to, produced-by, verified-by, recorded-in, continues, successor-of and depends-on.

The repository relationship index is a navigation projection, never a second database, event store, memory system or authority source.

## Current / historical separation

CURRENT = authoritative now.
VERIFIED = evidence supports the stated claim type.
PRODUCTION_PROVEN = fresh production evidence exists for the exact current source identity.
PARTIAL / DEMO / MISSING = implementation maturity classification.
HISTORICAL = useful evidence that cannot certify newer current state.
SUPERSEDED = replaced by a newer source.
BLOCKED / UNKNOWN = not green; do not silently promote.

## What is now organized

- One NayaNET project root.
- All 19 named NayaNET areas.
- All 19 area operating workspaces with Current State, Activity, Smart Notes, Evidence and Next Action surfaces.
- Team Naya communication feed and dated calendar remain separate.
- NayaPOWER Main Activity remains the canonical operational event substrate.
- Area Activity remains scoped projection/working view.
- Area Smart Notes remain scoped intelligence organization.
- Existing engineering and historical artifacts remain preserved.

## Remaining engineering work

The physical information architecture is now reconciled. This does NOT mean all 19 features are implemented or runtime-verified. The next engineering work is to connect these human-readable workspaces to the actual canonical event, intelligence, ingestion, retrieval and verification machinery, starting with the smallest real vertical slice.

## Cold-Naya acceptance

A fresh Naya should be able to enter any area and answer:

What is it? → What are we doing? → What happened? → What did we learn? → What proves it? → What's next? → How does it connect?

If answering those questions requires conversational archaeology, improve the operating map or area workspace.

## Canonical references

- Cold-Naya Operating Index
- NayaNET Project Root README
- 19-Area Engineering Blueprint Master
- 19-Subproject Reconciliation
- Team Naya dated calendar and Activity Feed
- NayaPOWER STATE / BLOCKS / MAP / PROOF

---
**Operating law:** one company • one system • one event truth • many clear working views • one next action.
