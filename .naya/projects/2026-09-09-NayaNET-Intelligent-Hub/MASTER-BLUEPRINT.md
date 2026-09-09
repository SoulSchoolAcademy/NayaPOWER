# NayaNET Intelligent Hub — MASTER BLUEPRINT

**Project date:** 2026-09-09
**Project:** NayaNET Intelligent Hub — Fresh Rebuild
**Repository:** `SoulSchoolAcademy/NayaPOWER`
**Branch:** `main`

## 0. NEW AUTHORITY MODEL

**There is no legacy authoritative Hub source anymore.**

The new Hub is a fresh build.

The file `2026 09 08 452 NayaNET Hub.html` is a **FROZEN REFERENCE SNAPSHOT ONLY**. It is used to learn what existed, what worked, what failed, what links existed, and what product intent must be preserved. It is not edited as part of the new Hub.

Historical NAYANETHUBONE material is also historical reference only and must never silently become the new source.

The future build will create a new canonical Hub source under an explicitly chosen new path/name. Until that source is created, the project documents are the product/design authority—not an old HTML file.

## 1. NORTH STAR

**INTELLIGENCE MADE VISIBLE.**

Product mission:

**CAPTURE → DISTILL → ORGANIZE → REMEMBER → FIND → COMPOUND**

The Hub is the user's living intelligence environment, not a generic dashboard.

## 2. HOUSE MODEL

The Hub is designed as a connected house of rooms:

1. Home / Intelligence Today
2. Smart Feed / Intelligent Feed
3. Smart Notes
4. Daily Intelligence / Reports
5. Intelligence Library
6. Collective Intelligence
7. Evidence
8. Connections
9. Smart Mail
10. Smart Space
11. Settings
12. Search / Retrieval (cross-room intelligence service)
13. Naya access (cross-room intelligence service)

And the shared structural areas:

- Top Bar
- Left Sidebar
- Lower Feature Reports Bar
- Ecosystem Link Bar
- Mobile Navigation

The detailed room contract is in `09-HUB-ROOM-BY-ROOM-SPEC.md`.

## 3. SMART FEED AUTHORITY

The Smart Feed / Intelligent Feed is the primary intelligence surface.

It has three conceptual layers:

- Personal Intelligence
- Collective Intelligence
- Activity Feed

One event remains one canonical intelligence object.

The Intelligent Block sequence is:

**WISDOM → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → WEAVER → LESSON / MEANING / ACTION**

The detailed Smart Feed specification is in `08-SMART-FEED-INTELLIGENCE-SPEC.md`.

## 4. CURRENT-STATE DOCTRINE

The feed follows:

**CURRENT STATE FIRST → RELEVANT HISTORY SECOND**

It must answer:

- Where are we?
- What matters now?
- What changed?
- What did we learn?
- What is verified?
- What is not verified?
- What is protected?
- What remains unresolved?
- What happens next?

## 5. PRIVACY LAW

**PRIVATE BY DEFAULT · SHARED BY CHOICE · COLLECTIVE BY CONSENT · PUBLIC BY DECISION**

This is both product language and architecture law.

## 6. PRESERVED HOME ORIENTATION

The new Home must intentionally retain the orientation elements that were lost during prior iterations:

- personalized greeting (`Good morning, Shawn` or time-appropriate equivalent)
- current time
- current date
- country/locale
- intelligence philosophy statement
- privacy statement

Working philosophy language to preserve:

**MORE INTELLIGENCE. LESS WASTE.**

If the exact earlier canonical wording is recovered from a frozen reference, it may be used instead of this working wording. It must never disappear accidentally.

## 7. SOURCE REFERENCE — WHAT WE LEARNED

The frozen 2026-09-08 4:52 source contains substantial proven/product-relevant material:

- desktop left navigation
- mobile navigation
- topbar
- ecosystem links
- feature report links
- Home orientation
- Smart Notes
- Daily Intelligence
- Intelligence Library
- Collective
- Evidence
- Connections
- Smart Mail
- Settings
- local state/persistence examples
- search/index examples
- intelligence perspective examples
- multiple failed/competing feed renderer layers

The source is evidence. The new architecture is the clean implementation.

## 8. EXTERNAL DESTINATIONS TO PRESERVE

Frozen-reference mappings:

- HOME → `https://hmclibrary.groovemember.net/home`
- NAYA POWER → `https://academy.nayanet.app/`
- 5 DAY CHALLENGE → `https://academy.nayanet.app/`
- ENTER FREE → `https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab`
- POWERCASTS → `https://nayanet.groovepages.com/powerplayer`
- WHITE PAPER → `https://nayanet.groovepages.com/whitepaper`
- ABOUT US → `https://nayanet.groovepages.com/aboutus`
- HMC LOGIN → `https://hmclibrary.groovemember.net/login`

Five feature reports:

- SMART NOTES → Google Drive file `19sRtp22aAn35wNoqqpNiZHkaFGmUOxoP`
- NO DEAD ENDS → Google Drive file `1LgRmYAQ85AB6mmu6Qp2ovghyd1lP-FNh`
- CONTEXT LAW → Google Drive file `1N-XzV3_RCTHuLdp4leZNlOo7ITFwrICR`
- 10-STAR SERVICE → Google Drive file `1F9M66i5Av_oJcIa5dve-U0mMeAgYKczT`
- ADAPTIVE LEARNING → Google Drive file `1dcViGUqV7GKnNBCYybbAEEKuOoZw3-XC`

Exact URLs are maintained in the Page and Interaction maps.

## 9. ENGINEERING LAW

The new Hub must not repeat the layered-renderer failure pattern.

Forbidden:

```text
renderer A + renderer B + overlay C + MutationObserver + interval + animation-frame repair
```

Required:

```text
Canonical State
      ↓
Selectors / Queries
      ↓
One Router / Page State
      ↓
One Renderer per surface
      ↓
DOM
```

External services are adapters.

Persistence is behind an explicit persistence adapter.

Naya is behind an explicit Naya adapter.

Search is behind an explicit retrieval/index adapter.

## 10. DATA LAW

One canonical event identity must flow through:

```text
Human Input
 → Smart Note / Note Event
 → Persistence
 → Naya enrichment (when available)
 → Machine evidence / receipt
 → Intelligent Feed projection
 → Search / Retrieval
 → Daily Intelligence
 → Learning
 → Lesson / Meaning / Action
 → Compounding Intelligence
```

No duplicate intelligence databases merely for presentation.

## 11. VISUAL LAW

The Hub must feel like one extraordinary instrument:

- premium
- cinematic
- editorial
- architectural
- dimensional
- tactile
- black/obsidian foundation
- white typography
- purple/magenta intelligence light
- sapphire/blue machine/source accent
- green verified/success
- restrained gold significance/evidence/caution
- beautiful, instantly readable icons
- strong hierarchy
- generous spacing
- no generic SaaS card wall
- no excessive glassmorphism
- no rainbow decoration

Intelligent Blocks should appear elevated from their parent surface, with depth that makes them feel almost touchable, while remaining extremely easy to scan and read.

## 12. RESPONSIVE LAW

### Desktop
- left sidebar
- no right Hub sidebar
- full intelligent workspace
- persistent top context
- lower feature report bar

### Mobile
- no persistent left sidebar
- intentional mobile navigation
- one-column intelligence object
- accessible controls
- lower report bar positioned above mobile navigation
- no content obscured by fixed UI

Desktop and mobile are separate designed experiences, not merely resized versions.

## 13. VERIFICATION LAW

Completion requires:

**SOURCE → BUILD → DEPLOY → RUNTIME → OBSERVATION → INTERACTION → PERSISTENCE → MOBILE → NO REGRESSION**

A commit is not proof.
A green workflow is not proof.
A source marker is not proof.
The visible runtime is the final acceptance surface.

## 14. PROJECT DOCUMENT INDEX

### Core architecture
- `00-README-CANONICAL-BLUEPRINT.md`
- `MASTER-BLUEPRINT.md`

### Forensic maps
- `01-PAGE-MAP.md`
- `02-COMPONENT-MAP.md`
- `03-INTERACTION-LINK-MAP.md`
- `04-INTELLIGENCE-MAP.md`
- `05-VISUAL-RESPONSIVE-MAP.md`
- `06-ENGINEERING-VERIFICATION-MAP.md`
- `07-REBUILD-ACCEPTANCE-CONTRACT.md`

### Fresh-build specifications
- `08-SMART-FEED-INTELLIGENCE-SPEC.md`
- `09-HUB-ROOM-BY-ROOM-SPEC.md`
- `10-OPEN-DECISIONS-BEFORE-CODING.md`

## 15. EXECUTION METHOD

Build one room at a time, in dependency order.

### Stage A — Foundation
- source boundary
- data model
- persistence adapter
- routing/state model
- verification harness

### Stage B — House shell
- top bar
- left sidebar
- lower bar
- ecosystem bar
- mobile navigation
- Home orientation

### Stage C — Intelligence core
- Smart Note event model
- Smart Feed
- Intelligent Block renderer
- Personal/Collective/Activity modes
- Search

### Stage D — Intelligence rooms
- Daily Intelligence
- Intelligence Library
- Evidence
- Connections
- Collective

### Stage E — Communication/system
- Smart Mail
- Smart Space
- Settings
- Naya adapter

### Stage F — Production proof
- runtime verification
- interaction verification
- persistence verification
- responsive verification
- accessibility verification
- no-regression verification

## 16. RULE FOR EVERY NAYA

Before building any room, answer:

**WHAT IS IT? WHY DOES IT EXIST? WHAT DOES THE USER SEE? WHAT CAN THEY DO? WHERE DOES EVERY ACTION GO? WHAT DATA MOVES? WHAT PERSISTS? WHAT DOES NOT? WHAT ARE THE STATES? HOW DOES IT CONNECT? WHAT DOES DESKTOP LOOK LIKE? WHAT DOES MOBILE LOOK LIKE? HOW DO WE VERIFY IT?**

If something is unknown, record the unknown. Never silently invent it.

## 17. FINAL BUILD PRINCIPLE

**We are not repairing the old Hub. We are learning from it and building the right Hub.**

Preserve proven value. Remove accumulated ambiguity. Make every room intentional. Make every connection explicit. Make every state truthful. Make the intelligence beautiful. Verify the exact runtime.
