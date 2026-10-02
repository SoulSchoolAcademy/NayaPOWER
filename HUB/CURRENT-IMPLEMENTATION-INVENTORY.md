# 🔱 NayaNET Hub — Current Implementation Inventory

**Evidence snapshot:** 2026-10-01  
**Status:** OBSERVED IMPLEMENTATION EVIDENCE — not canonical target law  
**Canonical target:** `HUB/PROJECT-INTELLIGENCE.md` + `HUB/DESIGN-CONTRACT.md` + `HUB/ROOMS/`  
**Execution owner:** #1270

## 1. Source truth inspected

### Canonical repository
Live `main` observed at:

`5885459af85bcbaede4480557413ae9c681028a1`

### Public deployed worker
Observed:

`https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/`

The deployed page presents **NayaNET — Intelligent Hub V7 · 509 AAA** and visibly exposes:
- Smart Feed
- Your Intelligence Today
- Your Reports
- Intelligent Library
- **Smart Share**
- Smart Ledger
- Your Connections
- Smart Lists
- Smart Mail
- Smart Spaces
- Settings
- Collective / Personal / Activity
- Naya companion
- Smart Notes / Intelligent Blocks

### Human Director supplied implementation snapshots

`index.HTML`
- 27,206 bytes
- 1,579 lines
- git-blob hash: `b434cdf6016a546a43cb4f0d4d5da6c18542c6f5`

`smart-feed.html`
- 864,094 bytes
- 1,306 lines
- git-blob hash: `ed6b1a81f50ba752e8d081b63987c6963cd85755`

These snapshots are **not byte-identical** to current main reference files:
- main Welcome blob: `3b04e5f0bd3f6c5e9a630b77b87981769eb644e5`
- main Hub concept blob: `7b1126a014b3b27026a0360dbc1b8226a9be9f50`

Therefore exact deployed-source parity is **UNKNOWN** until the worker source is reconciled to repository truth.

## 2. What is already winning

The current implementation is not empty. It contains important working/prototype intelligence:

- protected obsidian + spectral visual DNA;
- left-rail Hub model;
- Collective / Personal / Activity separation;
- prominent search;
- Naya companion;
- explicit provenance/truth language;
- real runtime hooks through `window.NayaAssistantRuntime`;
- Smart Note capture call through `captureSmartNote(...)`;
- canonical/deep-link retrieval through `retrieveIntelligentBlock(...)`;
- authenticated personal runtime feed projection through `smartFeed(...)`;
- honest RUNTIME UNAVAILABLE / NOT VERIFIED fallbacks in several newer surfaces;
- keyboard handling for some tab/action controls;
- reduced-motion handling in several CSS layers.

These are assets to preserve, not excuses to preserve the monolith.

## 3. Architecture inventory of supplied `smart-feed.html`

Observed:
- 31 script blocks;
- 176 named function declarations;
- 119 unique function names;
- repeated patch families such as `run`, `boot`, `css`, `actions`, `feed`, `toast`;
- 14 `localStorage` references across at least 7 local keys;
- one source `fetch(...)` path;
- 8 `new MutationObserver(...)` sites;
- **the first script replaces `window.MutationObserver` with a no-op class**, and no later replacement was found.

This is strong evidence that the file is a layered laboratory/reference artifact rather than the final maintainable production architecture.

## 4. Current global journey

### Welcome
The supplied Welcome page is visually strong and contains the 108-jewel orbital system.

Observed route behavior:
- normal entry → `identity.html?name=...`
- auto-login → `identity.html`
- Powercasts link → `hub.html`

Current repository build law says:
`WELCOME → IDENTITY → INTELLIGENT HUB`

The `hub.html` Powercast path is stale relative to the current repository rename to `powercast-player.html` unless deployment intentionally maps it.

### Identity
Current main Identity remains a prototype/local identity bridge and must not be treated as governed identity proof.

The production app needs one non-duplicative identity/session boundary.

### Hub
The deployed/supplied Hub is a visual and functional laboratory. It is not yet a coherent production shell with independently proven room contracts.

## 5. Room/function inventory

| Surface | Current observed behavior | Target gap |
|---|---|---|
| Smart Feed | Real/static intelligence boards + local interaction state; authenticated runtime can prepend personal feed items | one canonical feed architecture; real PERSONAL/COLLECTIVE/ACTIVITY retrieval; no patch-stack ownership |
| Your Intelligence Today | A newer center-workspace implementation honestly exposes missing daily comparison/learning/priority boundaries | real daily retrieval + synthesis + What Changed + evidence-grounded Naya Reflection |
| Your Reports | current workspace mainly reports rendered block counts / truth metadata | real DAY/WEEK/MONTH/YEAR semantics, evidence-backed synthesis |
| Intelligent Library | searches currently visible DOM intelligence in one path | canonical semantic retrieval, domains, gaps, source/provenance |
| Smart Connect | deployed/supplied UI still says **Smart Share**; share action uses browser share/clipboard | canonical Smart Connect + Smart Door registry/status; connection/auth/authority/health separation |
| Smart Ledger | probes runtime methods if exposed, otherwise honest unavailable | canonical receipt/outcome/verification projection and causal timeline |
| Your Connections | governed runtime methods attempted if exposed | complete relationship + consent/share intelligence |
| Smart Lists | current path derives from saved/favorited visible blocks/local state | canonical list definitions referencing canonical intelligence |
| Smart Mail | governed runtime methods attempted if exposed | real messaging + context + explicit send authority |
| Smart Spaces | runtime path when available; otherwise visible intelligence fallback | real context scope changing retrieval/people/activity/goals/rules |
| Settings | runtime snapshot/verify surfaced | full human control deck; local vs account vs governed enforcement explicit |

## 6. Cross-function gaps that block a true smart app

### G1 · No single production architecture yet
The monolithic worker/snapshot and open `HUB/app/` foundation are separate implementation shapes.

### G2 · Exact deployed-source parity is unknown
The Human Director supplied snapshots differ from current main reference blobs. The worker cannot be treated as repository-canonical source.

### G3 · IA naming conflict remains
Live/supplied Hub still exposes **Smart Share** while canonical project intelligence requires **Smart Connect**.

### G4 · 11-room vs 13-room implementation conflict
PR #1278 implements Smart Notes + System as primary rooms. Current canonical proposal keeps 11 primary rooms, with Smart Note as universal capability/focused surface and System Health under Settings.

### G5 · runtime contract is not complete enough for the room promises
Today explicitly lacks daily comparison/learning/priority retrieval. Reports/Library/Lists/Spaces still use partial/local projections in places.

### G6 · local state is still carrying product behavior
Several actions use localStorage/DOM-derived state. Local interaction state is allowed for UI preference, but it is not canonical intelligence/persistence proof.

### G7 · maintainability/performance debt
864 KB single HTML + 31 scripts + repeated repair layers + observer shim conflicts with the production performance/maintainability target.

### G8 · Welcome/Identity/Hub are not yet one governed journey
Welcome routes to a local Identity filename; current main Identity still redirects into the worker and creates local key state. Production should have one coherent journey.

### G9 · proof is uneven
Some code is honest about unavailable runtime state, which is good. But end-to-end browser/runtime/persistence/independent proof does not yet cover the complete app.

### G10 · open branches must converge before implementation continues
- #1278 = app foundation, currently stale/diverged from current main and implements 13 rooms.
- #1281 = art-direction layer.
- #1290 = room contracts + review system.
- #1270 = production conversion owner.

## 7. Naya working score — implementation snapshot

This is a **builder self-score**, not independent closure.

| Dimension | Working score | Evidence summary |
|---|---:|---|
| D1 Visual Excellence | 8.3 | distinctive baseline survives; room-specific production design still incomplete |
| D2 Functional Completeness | 4.8 | many controls/surfaces exist, but several are local/thin/not end-to-end |
| D3 Intelligence | 4.2 | real runtime hooks exist; major room promises still lack canonical retrieval/synthesis |
| D4 Honesty | 8.3 | many newer paths explicitly refuse to fabricate data |
| D5 Performance | 3.8 | 864 KB monolith, 31 script blocks, patch layering, unmeasured production performance |
| D6 Reliability & Continuity | 4.8 | some persistence/runtime paths; local state + parity uncertainty remain |
| D7 Accessibility | 5.5 | partial keyboard/reduced-motion; no complete audit/proof |
| D8 Craft | 5.8 | strong DNA but mixed architecture, duplicated repair layers and unfinished room presentation |

**Working composite: ~5.7 / 10.**

This is consistent with the canonical project's ~5.6 baseline: the design DNA is ahead of the application integration.

## 8. Highest-value convergence path

Do not add another concept layer.

1. ratify/reconcile the 11-room IA and room contracts;
2. reconcile #1281 art direction into the canonical design intelligence;
3. move the best parts of #1278 onto current main / accepted specs instead of literal monolith migration;
4. establish one production App Shell + Router + runtime adapter;
5. fix Welcome → governed Identity → Hub;
6. implement Your Intelligence Today as the first complete vertical slice;
7. prove capture → persistence → retrieval → Today/Feed/Library → Ledger;
8. then activate rooms in dependency order;
9. harden accessibility/performance/reliability;
10. independently score D1–D8 and continue until target.

## 9. Definition of the next true milestone

The next meaningful milestone is **not another design document** and not another patch to the 864 KB file.

It is:

**CURRENT-MAIN APP SHELL + GOVERNED JOURNEY + CANONICAL RUNTIME ADAPTER + YOUR INTELLIGENCE TODAY WORKING END-TO-END + EVIDENCE.**

That slice must preserve the visual baseline while proving the architecture the rest of the app will inherit.


## 10. Human Director presentation finding — mobile navigation

**Source:** direct Human Director QA feedback, 2026-10-01.  
**Independent reproduction:** NOT YET VERIFIED.

Reported behavior:
- opening the mobile "+" / navigation affordance reveals the sidebar;
- a duplicate/double-sidebar condition remains visible during scroll;
- scrolling can expose a large unused black gutter/empty side region;
- the result reads as unfinished even when individual controls look good.

Classification:
**P1 PRESENTATION / RESPONSIVE SHELL DEFECT** because the global shell is inherited by every room.

Required closure:
- exactly one primary navigation surface per viewport;
- no permanent desktop rail underneath an open mobile drawer;
- drawer overlays instead of reserving a second content column;
- no horizontal overflow;
- no dead black gutter;
- open/close preserves scroll;
- long-page testing at phone/tablet widths;
- screenshot/video evidence before closure.

Do not mark this defect PASS from code inspection alone.
