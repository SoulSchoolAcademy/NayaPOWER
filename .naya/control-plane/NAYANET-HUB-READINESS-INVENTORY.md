# 🔱 NayaNET Intelligent Hub — Readiness Inventory

**Status:** CANONICAL READINESS WORKING INVENTORY  
**Date:** 2026-09-22  
**Repository:** SoulSchoolAcademy/NayaPOWER

## Purpose

This is the single canonical inventory for the NayaNET Intelligent Hub readiness program. It maps each human-facing capability across:

**VISUAL / FUNCTIONAL / SENDER / RECEIVER / BRIDGE / PERSISTENCE / RETRIEVAL / EVIDENCE**

The Hub is the human door to NayaPOWER. It is not a second brain, second authority, or second persistence system.

Causal target:

HUMAN → HUB → GOVERNED CAPABILITY → NAYAPOWER → PERSISTENCE → RETRIEVAL → HUB → EVIDENCE → CONTINUATION

A selector or route passing is not proof of this complete causal chain.


## 0A. Canonical 2026-09-24 room/process/block distinction

The 2026-09-24 system-wide alignment supersedes older Hub taxonomy where it conflicts.

**Human-facing Hub rooms/destinations:**
1. Intelligence Today
2. Feed
3. Reports
4. Intelligent Library
5. Smart Connect
6. Smart Mail
7. Smart Lists
8. Contacts
9. Smart Spaces
10. Smart Ledger
11. Settings

**Superbrain processes — not rooms:** Dream, learning, categorization, recall, replay/review, analysis, comprehension, pattern recognition, intelligence compounding, RSI/modular RSI, and application of learned intelligence.

**Intelligent Block capabilities — not rooms:** Naya Play and other object-level actions.

**Retired:** Smart Share as a Hub room. Any remaining `share` route/UI is legacy product surface and must not be treated as canonical Smart Connect.

**Completion contract for every room:** UI → authenticated identity → governed runtime → real data → correct privacy → real action → persistence → verification → receipt. UI presence alone is not completion; unknown backend state must render as NOT VERIFIED.

**Smart Connect doors:** GitHub App, MCP, REST/OpenAPI, Webhooks, SDK, A2A, MCP Apps. Participation through a door does not grant public identity, publication, private-data access, or unrestricted execution authority.

**Canonical participation law:** LEARN BY DEFAULT. SHARE WISDOM BY CONSENT. PROTECT IDENTITY BY DEFAULT. PUBLISH BY DECISION.

## 1. Canonical surfaces inspected

### Protected visual reference

2026 09 17 NAYANET HUB.html

Observed GitHub blob SHA: 4b5873cbf1442d4b6fcd1eb1ad1fdf1b2d5f4c51

The reference establishes the visual language: black/dark foundation, deep purple glow, jewel-like glyphs, dimensional physical buttons, intelligence blocks, lenses, search, Naya context, and dense human-facing intelligence presentation.

The reference also contains an original three-column shell followed by injected CSS that hides the right rail and establishes a single left rail. Shell ownership therefore has to be reconciled explicitly.

### Current React Hub

NAYANET/HUB/src/main.tsx
NAYANET/HUB/src/app/App.tsx
NAYANET/HUB/src/app/AppShellV3.tsx
NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx

Observed:

- App renders IdentityProvider → AppShellV3 → HubRouter.
- AppShellV3 owns a complete sidebar, topbar, and mobile navigation.
- SmartFeedBoard is a real intelligence rendering/action component with lenses, search, durable actions, apply/use, sharing, connections, spaces, and evidence-oriented Intelligent Block fields.
- HubBaselineApp.tsx contains a separate iframe-based legacy baseline shell, but App.tsx does not import it. It is therefore historical/competing-surface risk, not a second authority to activate.

### Current human-surface acceptance

Workflow: .github/workflows/human-surface-completeness-acceptance.yml

Run 35771409482: SUCCESS.

It currently proves presence/navigation for:

- name-first identity;
- Smart Feed surface;
- search;
- Reports;
- Settings;
- Dream;
- Naya Play;
- Smart Lists;
- Smart Spaces;
- Contacts;
- Smart Share;
- Smart Mail.

It does not prove visual fidelity, singular shell ownership, full create/save/reload/retrieve/evidence journey, or every sender/receiver/bridge/persistence boundary.

## 2. Readiness matrix

| Surface | VISUAL | FUNCTIONAL | SENDER | RECEIVER | BRIDGE | PERSISTENCE | RETRIEVAL | EVIDENCE | State |
|---|---|---|---|---|---|---|---|---|---|
| Hub shell / single owner | PARTIAL | PARTIAL | N/A | N/A | N/A | N/A | N/A | PARTIAL | FIRST REPAIR BOUNDARY |
| Smart Feed | PARTIAL | PARTIAL | PARTIAL | VERIFIED in prior Smart Note proof | PARTIAL | VERIFIED in prior proofs | VERIFIED in prior proofs | PARTIAL | Current-head full journey open |
| Universal search | VERIFIED presence | VERIFIED surface behavior | PARTIAL | PARTIAL | PARTIAL | N/A | PARTIAL | PARTIAL | Semantic retrieval proof open |
| Smart Note capture | VERIFIED | VERIFIED prior workflow | VERIFIED | VERIFIED | VERIFIED | VERIFIED | VERIFIED | VERIFIED for dedicated proof scope | Fresh consolidated journey open |
| Intelligent Block display | PARTIAL | PARTIAL | PARTIAL | VERIFIED block fields in component | PARTIAL | VERIFIED prior receiver proof | PARTIAL | PARTIAL | Current canonical display/retrieval proof open |
| Personal Intelligence | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | Lens exists; full current proof open |
| Collective Intelligence | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | Consent/privacy/current rendering proof open |
| Activity Feed | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | Automatic current-head synchronization open |
| Reports | VERIFIED presence | VERIFIED route | N/A | N/A | N/A | UNKNOWN | UNKNOWN | PARTIAL | Content durability not in current acceptance |
| Smart Connect | NOT PRESENT in current canonical Hub | NOT IMPLEMENTED as canonical Hub room | RUNTIME SEAM EXISTS | PARTICIPATION PROOF EXISTS | PARTIAL | PARTIAL | PARTIAL | PARTIAL | Canonical room/door integration missing |
| Smart Lists | VERIFIED surface | VERIFIED surface | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | Current acceptance is surface-only |
| Smart Spaces | VERIFIED surface | VERIFIED surface | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | Current acceptance is surface-only |
| Contacts | VERIFIED surface | VERIFIED surface | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | Current surface is labeled `connections`; canonical Contacts contract requires reconciliation |
| Smart Mail | VERIFIED surface | VERIFIED prior production proofs | VERIFIED | VERIFIED | VERIFIED | VERIFIED | VERIFIED | VERIFIED | Re-consolidate in current journey |
| Smart Ledger | PARTIAL | PARTIAL | PARTIAL | VERIFIED backend history | VERIFIED | VERIFIED | PARTIAL | VERIFIED backend history | Human evidence projection open |
| Dream / Learning | PROCESS, not room | VERIFIED prior runtime proofs | VERIFIED prior | VERIFIED | VERIFIED | VERIFIED | VERIFIED | VERIFIED | Preserve Dream as Superbrain process; do not promote to sidebar room |
| Naya Play | BLOCK/OBJECT CAPABILITY, not room | VERIFIED surface | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | PARTIAL | Keep as Intelligent Block capability; do not add Hub room |
| Settings / identity | VERIFIED surface | VERIFIED surface | PARTIAL | PARTIAL | VERIFIED adapter history | VERIFIED | VERIFIED | PARTIAL | Consolidated evidence open |
| Mobile/responsive | PARTIAL | PARTIAL | N/A | N/A | N/A | N/A | N/A | PARTIAL | Current visual geometry gate open |
| Activity → Control Plane → Baton → successor | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | Baton exists; universal automatic sync remains unknown |

## 3. First deterministic gap

### GAP-001 — Singular Hub shell and source/build/runtime ownership

Evidence:

1. App.tsx selects AppShellV3 as the React shell.
2. AppShellV3 independently renders a complete sidebar/topbar/mobile navigation.
3. HubBaselineApp.tsx contains a separate full iframe-based baseline shell.
4. The protected reference is itself a complete visual shell.
5. Run 35771409482 passes because it checks selectors/text/routes, not shell singularity or visual geometry.

Therefore the first repair boundary is:

**HUB SOURCE → SINGLE SHELL OWNER → BUILD ARTIFACT → LIVE RUNTIME → VISUAL/DOM OBSERVATION**

This is the first gate because downstream visual polish or feature repair is unsafe while the exact shell being served is not unambiguous.

## 4. Ten-gate execution program

1. **Shell authority** — establish one production Hub shell owner; preserve historical evidence without activating a competing shell.
2. **Visual parity** — reconcile the single shell against the protected reference: hierarchy, rails, spacing, typography, jewel glyphs, glow/depth, buttons, and responsive behavior.
3. **Smart Feed** — make Smart Feed unmistakably central and prove its visible intelligence states.
4. **Human golden path** — OPEN → UNDERSTAND → NAVIGATE → SEARCH → CREATE → SAVE → SEE RESULT → RELOAD → FIND IT → UNDERSTAND EVIDENCE → CONTINUE.
5. **Causal transport** — prove HUB → GOVERNED CAPABILITY → NAYAPOWER → PERSISTENCE → RETRIEVAL → HUB.
6. **Smart Door contract** — apply the same sender/receiver/bridge/persistence/retrieval/evidence contract to each Smart Door.
7. **Intelligence lifecycle** — prove SMART NOTE → INTELLIGENT BLOCK → INDEX → FEED → ACTIVITY → LEARNING → PLAYBACK.
8. **Continuity automation** — update ACTIVITY → CURRENT STATE → BATON → notification/successor after meaningful state-changing work.
9. **Human + cold-Naya acceptance** — run visual/functionality acceptance and cold-successor reconstruction.
10. **Readiness** — declare broad-use readiness only at the scope whose complete causal chain is independently verified.

## 5. Tag — You're It policy

Every substantive Naya execution ends with:

DONE / PROVEN / CHANGED / LEARNED / UNKNOWN / BLOCKED / DO-NOT / EVIDENCE / CURRENT STATE / ONE NEXT ACTION / SUCCESSOR PROMPT

The next Naya does not ask Shawn to reconstruct the mission.

The single canonical continuation source is:

.naya/control-plane/BATON.json

BATON.json is the continuation object, not a second state machine. It resolves STATE, BLOCKS, MAP, PROOF, evidence, and playback.

## 6. Read-me-first policy

The boot rule is:

**READ README-FIRST.md → READ .naya/control-plane/BATON.json → RECONCILE LIVE STATE → EXECUTE ONLY THE ONE AUTHORIZED NEXT ACTION → VERIFY → RECORD → UPDATE BATON → PASS THE BATON**

README-FIRST.md is a pointer/instruction file, not a duplicate current-state database.

## 7. No conversational archaeology

A cold Naya must be able to recover:

- what we are building;
- why;
- current state;
- proven and unknown;
- active block;
- exact one next action;
- evidence;
- successor instructions.

If that requires searching old conversation, the continuity gate has failed.

## 8. Current boundary

**ACTIVE BLOCK:** HUMAN-JOURNEY-P2

**FIRST REPAIR:** GAP-001 — singular Hub shell/source/build/runtime ownership.

**2026-09-24 taxonomy finding:** current canonical `NAYANET/HUB/index.html` exposes a `Smart Share` page and `Your Connections` page, but no `Smart Connect` or canonical `Contacts` page. It also contains no `Dream` or `Naya Play` Hub destination. This is correctly classified as a product-taxonomy mismatch, not evidence that Dream/Naya Play should become rooms.

**DO NOT:** begin broad visual redesign or mass Smart Door work before this boundary is reconciled.

**SUCCESS:** one active human-facing shell, observable source/build/runtime identity, and the next visual/functionality acceptance exercises that exact shell.

## Final law

**ONE BRAIN. ONE HUB. ONE CURRENT STATE. ONE NEXT ACTION. ONE CONTINUOUS HANDOFF.**

**TAG → YOU'RE IT → EXECUTE → VERIFY → RECORD → UPDATE → PASS THE BATON.**
