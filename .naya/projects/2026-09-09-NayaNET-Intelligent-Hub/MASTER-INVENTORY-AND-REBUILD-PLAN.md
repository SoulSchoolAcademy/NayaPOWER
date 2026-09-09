# NayaNET Intelligent Hub — Master Inventory, System Map & Rebuild Plan

**Project date:** 2026-09-09  
**Project name:** NayaNET Intelligent Hub 2026-09-09  
**Repository:** `SoulSchoolAcademy/NayaPOWER`  
**Branch:** `main`  
**Authoritative current Hub source:** `2026 09 08 452 NayaNET Hub.html`  
**Feed runtime asset:** `nayanet-intelligent-feed-v6.js`  
**Canonical production runtime:** `https://nayanet-v7-intelligent-hub.nayanet.workers.dev/`  
**Smart Link:** `https://nayanet-v7-intelligent-hub.nayanet.workers.dev/intelligence/nayanet-intelligent-feeds`

---

# 0. PURPOSE OF THIS PROJECT

This document is the **master reconstruction inventory** for the NayaNET Intelligent Hub.

The purpose is not to preserve accidental historical implementation. The purpose is to establish a complete, understandable source of truth for the Hub so that a new Naya can reconstruct the product without guessing, losing functionality, inventing replacements, or repeatedly damaging working areas while repairing another area.

The Hub is treated as a complete connected product consisting of:

- shell
- brand/header
- desktop navigation
- mobile navigation
- main feed
- intelligent boards
- search
- categories/filters
- compose/capture
- Smart Notes
- messaging/mail
- account/profile state
- page routing
- actions/buttons
- external links
- persistence and intelligence connections
- runtime scripts
- deployment path
- responsive behavior
- accessibility
- verification

**North Star:** INTELLIGENCE MADE VISIBLE.

**Product mission:** CAPTURE → DISTILL → ORGANIZE → REMEMBER → FIND → COMPOUND.

---

# 1. CRITICAL OPERATING LAW

## 1.1 The screen is the acceptance test

A successful GitHub commit or successful Cloudflare deployment does **not** prove the Hub is correct.

The verification ladder is:

`SOURCE → BUILD ARTIFACT → DEPLOYMENT → PUBLIC RUNTIME → RENDER PATH → VISIBLE UI → USER ACCEPTANCE`

A task is not complete merely because source and deployment are green.

## 1.2 One source of truth

The rebuilt Hub must have one authoritative renderer for each visible function.

Do not stack competing renderers such as:

- legacy renderer
- V11 renderer
- V12 renderer
- V12.1 override
- temporary wrapper
- duplicate feed
- hidden alternate feed

If an implementation is rejected, remove it rather than hiding it under another implementation.

## 1.3 Adaptive Reconstruction + Surgical Evolution

**NEVER DESTROY THE HOUSE TO RENOVATE ONE ROOM.**

Preserve proven functionality and design intent while reconstructing damaged areas deliberately.

## 1.4 No invented functionality

If behavior cannot be verified from source/runtime evidence, mark it **UNKNOWN / REQUIRES VERIFICATION** rather than inventing a contract.

---

# 2. CURRENT AUTHORITATIVE SOURCE INVENTORY

## 2.1 Primary HTML

`2026 09 08 452 NayaNET Hub.html`

This is the current main Hub document on `main`.

The source contains the overall application shell and extensive CSS for the following observed component families:

- `.app`
- `.sidebar`
- `.brand`
- `.brandLogo`
- `.navlabel`
- `.nav`
- `.nav button`
- `.sidefoot`
- `.main`
- `.topbar`
- `.crumb`
- `.topright`
- `.connectionPill`
- `.avatar`
- `.page`
- `.heroIntro`
- `.hero`
- `.heroCopy`
- `.naya`
- `.nayaPhoto`
- `.nayaLabel`
- `.actions`
- `.btn`
- `.surface`
- `.feature`
- `.mailSurface`
- `.pageHead`
- `.compose`
- `.search`
- `.filters`
- `.filter`
- `.noteList`
- `.note`
- `.noteTop`
- `.noteBody`
- `.noteTabs`
- `.noteTab`
- `.noteView`
- `.grid2`
- `.metricGrid`
- `.metric`
- `.chain`
- `.chainRow`
- `.colorCard`
- `.state`
- `.flow`
- `.toggleList`
- `.toggle`
- `.switch`
- `.mailLayout`
- `.mailCol`
- `.mailPad`
- `.mailTitle`
- `.mailNav`
- `.mailKinds`
- `.mailTab`
- `.alias`
- `.mailCenter`
- `.mailCenterHead`
- `.thread`
- `.mailCompose`
- `.mailKind`

These are **source-observed component families**, not a claim that every family is currently visually correct.

## 2.2 Feed JavaScript

`nayanet-intelligent-feed-v6.js`

Current file contains a V12.1 implementation labeled:

`NayaNET Intelligent Feed V12.1 — TRUE LEGACY BOARD RECONSTRUCTION`

It currently targets `#homeIntelligentBlocks` and attempts to normalize descendant grids/columns into a vertical layout, remove selected rejected renderer artifacts, and apply premium styling.

**Important architectural finding:** this file is currently an override layer. It must not automatically be treated as the authoritative definition of what the user sees. The actual render path must be established before further visual work.

## 2.3 Existing continuity documentation

`.naya/INTELLIGENT-FEED.md`

This establishes the broader meaning of the Intelligent Feed as the current-state continuity surface and states:

`CURRENT STATE FEED = INTELLIGENT FEED = SMART NOTE FEED`

It also establishes:

`CURRENT STATE FIRST → RELEVANT HISTORY SECOND`

and the current-state pattern:

`WHAT CHANGED → WHAT MATTERS → WHAT WAS LEARNED → WHAT IS VERIFIED → WHAT REMAINS → WHAT HAPPENS NEXT.`

The Hub project must respect this intelligence architecture rather than creating a competing memory/feed authority.

---

# 3. PAGE/SHELL INVENTORY

## 3.1 Global application shell

Observed structure:

`body → .app → .sidebar + .main`

Desktop shell is currently a two-region layout with a left sidebar and main content.

**Required future contract:**

- left navigation remains available on desktop
- no right sidebar in the primary Hub feed
- main content receives the full available working width
- mobile removes the persistent left sidebar and exposes navigation through the mobile control
- no accidental third column

## 3.2 Brand area

Observed:

- `.brand`
- `.brandLogo`
- brand name text
- supporting brand text

Branding direction is already substantially established.

**Preserve:** recognizable NayaNET identity, existing logo treatment, premium dark/purple visual language.

**Do not redesign merely for novelty.**

## 3.3 Desktop left navigation

Observed component family:

`.sidebar → .navlabel → .nav → .nav button`

Navigation buttons support an active state with:

- dark/purple active surface
- border highlight
- right-side active indicator
- icon region
- optional badge

**Inventory requirement for next implementation:** every navigation item must be documented with:

1. label
2. icon
3. destination/page
4. active-state rule
5. badge behavior
6. click action
7. whether navigation changes route or local page state
8. persistence requirements
9. mobile equivalent

The exact current labels/destinations must be extracted from the complete DOM/script render path before rebuilding. Do not guess them.

## 3.4 Sidebar footer

Observed `.sidefoot`.

Purpose appears to be a fixed/anchored lower sidebar information area.

Exact text, actions, and data source require DOM-level inventory before reconstruction.

## 3.5 Top bar

Observed `.topbar` containing:

- breadcrumb/current-page indicator (`.crumb`)
- right controls (`.topright`)
- connection state (`.connectionPill`)
- user avatar (`.avatar`)

**Required contract:** top bar should identify where the user is and expose only high-value global status/account controls.

## 3.6 Connection status

Observed `.connectionPill` with LED state.

States include visual good/connected behavior through `.led.good` and a non-good/gold state.

**Required inventory:** identify the actual connection source, status calculation, click behavior, and failure behavior before rebuilding.

## 3.7 User/avatar control

Observed `.avatar` and `.avatar img`.

Exact click destination/action must be extracted from the actual DOM event wiring.

---

# 4. MAIN PAGE / FEED INVENTORY

## 4.1 Home/primary feed

The Hub's primary content area is the most important product surface.

It must not become a generic dashboard.

The desired product definition is:

> A living, searchable intelligence library/feed whose job is CAPTURE → DISTILL → ORGANIZE → REMEMBER → FIND → COMPOUND.

## 4.2 Hero/intro region

Observed component families:

- `.heroIntro`
- `.hero`
- `.heroCopy`
- `.naya`
- `.nayaPhoto`
- `.nayaLabel`
- `.actions`

The hero combines:

- large headline
- supporting explanation
- action controls
- Naya visual/presence

**Required future contract:** hero should orient the user immediately to what the Hub is doing now and provide the highest-value action without competing with the intelligence feed.

## 4.3 Main feed container

Current feed script targets:

`#homeIntelligentBlocks`

This must be verified against the actual rendered DOM before further reconstruction.

The key question is:

> Is `#homeIntelligentBlocks` actually the visible source of the boards the user sees?

If no, identify the real renderer and replace this assumption.

## 4.4 Intelligent Boards

This is the primary redesign target.

The board is **one intelligence object**, not a collection of generic cards.

Canonical intelligence sequence:

`WISDOM → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → WEAVER → LESSON / MEANING / ACTION`

### WISDOM

Purpose: establish the distilled truth/central intelligence of the event.

Visual role: strongest conceptual anchor.

### HUMAN

Purpose: preserve the originating human experience, observation, intention, decision, question, or input.

### CHILD

Purpose: represent curiosity, first-principles perception, simplicity, play, or the question that exposes what matters.

### GRANDMA

Purpose: practical lived wisdom, common sense, experience, human meaning, and long-range perspective.

### NAYA

Purpose: AI interpretation, synthesis, guidance, questioning, and intelligent response.

### MACHINE

Purpose: evidence, system state, data, tools, code, runtime, measurable facts, and machine-derived intelligence.

### WEAVER

Purpose: synthesis across Human + Naya + Machine and transformation into coherent intelligence.

This is the climax of the object, not another ordinary card.

### LESSON

Purpose: what should be retained.

### MEANING

Purpose: why it matters.

### ACTION

Purpose: what happens next.

### Board laws

- One coherent vertical intelligence narrative.
- No competing two-column board architecture.
- No random card wall.
- No generic SaaS dashboard styling.
- No unnecessary horizontal fragmentation.
- No fake intelligence.
- No invented fields just to fill visual space.
- Strong hierarchy.
- Premium black/obsidian foundation.
- Purple as intelligence accent.
- White typography.
- Restrained gold for significance/culmination.
- Dimensional depth through controlled light, layering, borders, shadows, and spacing.
- Clear beginning, synthesis climax, and compounding endpoint.
- Responsive and readable on mobile.

---

# 5. SEARCH INVENTORY

Observed source family:

`.search`

The search control is one of the areas that appears conceptually correct and should be preserved as a high-value function unless the actual implementation proves otherwise.

Required contract:

- search input
- query state
- filtering/search execution
- result projection
- empty state
- clear/reset behavior
- keyboard behavior
- connection to intelligence store/feed
- whether search is local, remote, or hybrid
- pagination/limit if applicable
- mobile behavior

**Do not change search merely because other parts of the Hub are being rebuilt.**

---

# 6. CATEGORIES / FILTER INVENTORY

Observed:

- `.filters`
- `.filter`
- active filter styling

Categories are intended to narrow/organize the intelligence feed.

Required contract for every category:

- category name
- category meaning
- event types included
- visual label
- active state
- filtering logic
- URL/state persistence if applicable
- empty result behavior
- relationship to Smart Notes

The actual category labels and filtering code must be inventoried from the complete runtime before reconstruction.

**Do not invent category taxonomy.**

---

# 7. CAPTURE / COMPOSE INVENTORY

Observed:

`.compose`

with textarea and `.composeRow` / `.hint` patterns.

Purpose: capture a new intelligence event/Smart Note.

Required contract:

`USER INPUT → VALIDATION → NAYA/INTELLIGENCE PROCESSING → SMART NOTE → PERSISTENCE → FEED PROJECTION → SEARCHABILITY → COMPOUNDING`

The capture surface must document:

- input field
- placeholder/instructions
- submit button
- disabled/enabled state
- validation
- save operation
- success state
- failure state
- duplicate/idempotency behavior
- generated metadata
- feed insertion behavior
- Smart Note connection
- Naya connection

---

# 8. SMART NOTE INVENTORY

Observed source families:

- `.noteList`
- `.note`
- `.noteTop`
- `.noteBody`
- `.noteTabs`
- `.noteTab`
- `.noteView`
- `.type`

A Smart Note is one intelligence event, not merely a note-card UI.

Known conceptual event dimensions include:

- Human
- Naya
- Machine
- insight
- mistake
- breakthrough
- decision
- idea
- lesson
- question
- goal
- win
- opportunity

The exact UI fields currently displayed must be extracted from the DOM before rebuild.

### Smart Note contract

A note must have:

1. event identity
2. timestamp/provenance
3. source/context
4. human contribution
5. Naya contribution where applicable
6. machine/evidence contribution where applicable
7. distilled intelligence
8. lesson/meaning/action when applicable
9. category/type
10. retrieval/search metadata
11. persistence status
12. verification state

### Feed relationship

The feed is a prioritized projection of intelligence, not a second memory authority.

Canonical durable intelligence remains in the Note Event architecture.

---

# 9. METRICS / INTELLIGENCE STATUS INVENTORY

Observed:

- `.metricGrid`
- `.metric`
- `.state`
- `.flow`
- `.chain`
- `.chainRow`
- `.colorCard`

These appear to represent metrics, state, process/chain, and status information in parts of the Hub.

Before reconstruction, determine which are actually visible on which page and whether they are:

- user-facing intelligence
- system status
- diagnostic information
- historical artifact
- implementation residue

Anything that exists only for developers must never leak into the user-facing Hub.

---

# 10. TOGGLES / SETTINGS INVENTORY

Observed:

- `.toggleList`
- `.toggle`
- `.switch`

Required contract:

- setting name
- meaning
- current value
- persistence
- interaction
- optimistic vs confirmed state
- failure rollback
- accessibility label
- mobile behavior

The exact settings represented must be extracted from the runtime before rebuilding.

---

# 11. MESSAGE / MAIL INVENTORY

This area is explicitly identified as currently **not right** and must be treated as a full subsystem reconstruction rather than a cosmetic repair.

Observed source families:

- `.mailSurface`
- `.mailLayout`
- `.mailCol`
- `.mailPad`
- `.mailTitle`
- `.mailNav`
- `.mailKinds`
- `.mailTab`
- `.alias`
- `.mailCenter`
- `.mailCenterHead`
- `.thread`
- `.mailCompose`
- `.mailKind`

The source defines a three-column mail layout internally:

`220px | flexible center | 260px`

This must not be confused with the **Hub shell requirement** of having no right sidebar. The message page can have an internal mail workspace only if that is the intended product design and it is verified against the desired UX.

### Message subsystem inventory requirements

Document separately:

1. mailbox/navigation
2. message categories
3. thread list
4. selected thread
5. compose/reply
6. recipient fields
7. subject
8. message body
9. send
10. reply
11. archive/delete if present
12. unread state
13. timestamps
14. sender identity
15. alias/contact identity
16. attachments if present
17. external email integration
18. loading/error/empty states
19. mobile behavior
20. persistence

### Known external architecture

The broader Naya Communication Hub architecture has been defined as:

`Groove/UI → HTTPS/API → Cloud Backend → Database → SendGrid outbound + Namecheap Private Email IMAP inbound`

Known inbound Namecheap IMAP host:

`mail.privateemail.com`

Known secure IMAP port:

`993`

Known outbound provider:

`SendGrid`

The Hub UI must not claim a backend capability unless the connection is actually implemented and verified.

---

# 12. BUTTON / INTERACTION INVENTORY

Every visible button must become an explicit inventory item.

For every button, record:

- visible label
- icon
- location
- purpose
- target
- event handler
- state rules
- success behavior
- error behavior
- analytics/receipt if applicable
- keyboard behavior
- mobile behavior
- whether destructive

Current global button styling is represented by `.btn` and variants such as:

- `.green`
- `.blue`
- `.purple`
- `.gold`
- `.small`

These variants should become semantic design tokens rather than arbitrary decoration.

---

# 13. LINKS / ROUTES INVENTORY

The Hub must maintain a route map that distinguishes:

### Internal page state

Example pattern:

`Hub shell → selected page → content renderer`

### Internal application route

Example pattern:

`/intelligence/nayanet-intelligent-feeds`

### External destination

Any destination outside the Hub must be recorded with:

- label
- URL
- purpose
- open behavior
- authentication requirements
- fallback behavior

### Canonical production links

Production runtime:

`https://nayanet-v7-intelligent-hub.nayanet.workers.dev/`

Intelligent Feed Smart Link:

`https://nayanet-v7-intelligent-hub.nayanet.workers.dev/intelligence/nayanet-intelligent-feeds`

Canonical public/social brand URL:

`NayaNET.xyz`

Do not introduce alternate brand spellings.

---

# 14. RESPONSIVE ARCHITECTURE

## Desktop

- persistent left navigation
- no right Hub sidebar
- main feed receives maximum useful width
- premium large-format intelligence objects
- top bar remains usable

## Mobile

- no persistent left sidebar
- navigation exposed by compact control
- full-width feed
- intelligence board becomes a single vertical narrative
- controls remain touch-friendly
- text remains readable
- no horizontal overflow
- no clipped actions
- no hidden essential functionality

## Accessibility

Required:

- semantic landmarks
- keyboard navigation
- visible focus
- accessible button names
- accessible form labels
- sufficient contrast
- reduced-motion support
- logical reading order
- screen-reader meaningful headings

---

# 15. VISUAL DESIGN SYSTEM

## Foundation

- black / obsidian background
- white primary typography
- purple intelligence accent
- restrained gold for high-value/cumulative states

## Depth

Use:

- layered surfaces
- controlled radial light
- fine borders
- restrained shadows
- luminous intelligence spine where appropriate
- meaningful hierarchy

Avoid:

- generic SaaS cards
- excessive glassmorphism
- rainbow styling
- random angled cards
- decorative effects without semantic purpose
- excessive borders
- visual noise

## Typography

Hierarchy should be editorial/cinematic rather than cramped dashboard typography.

The current source already establishes large responsive heading families. Rebuild should preserve the sense of scale while making the content hierarchy coherent.

---

# 16. RUNTIME / SCRIPT ARCHITECTURE

Current feed script V12.1 attempts to:

- remove selected rejected renderer artifacts
- target `#homeIntelligentBlocks`
- normalize grids/columns
- force vertical layout
- hide code/debug artifacts
- style the feed
- repeatedly restore the structure

### Critical finding

The repeated DOM repair loop is a warning sign.

A production-quality Hub should not need an endless `requestAnimationFrame` repair cycle to fight competing markup/renderers.

The rebuild should identify and remove the root cause so the correct structure is produced once by the authoritative renderer.

### Rule

**Render correctly at the source. Do not continuously repair incorrect output after rendering.**

---

# 17. DATA / INTELLIGENCE CONNECTION ARCHITECTURE

The Hub belongs to the broader Naya Power intelligence architecture.

Conceptual flow:

`HUMAN EXPERIENCE`
→ `CAPTURE`
→ `NAYA PROCESSING`
→ `MACHINE / EVIDENCE`
→ `INTELLIGENCE DISTILLATION`
→ `SMART NOTE / NOTE EVENT`
→ `CURRENT STATE / INTELLIGENT FEED`
→ `SEARCH / RETRIEVAL`
→ `WEAVER / SYNTHESIS`
→ `LESSON / MEANING / ACTION`
→ `COMPOUNDING INTELLIGENCE`

The durable memory authority remains the Note Event architecture.

The Hub is the human-facing visualization, interaction, capture, retrieval, and action surface.

---

# 18. DEPLOYMENT ARCHITECTURE

Canonical deployment target:

**Cloudflare Worker**

Not Vercel for this current Hub runtime.

Known workflow:

`.github/workflows/deploy-current-nayanet-hub.yml`

Dedicated deployment workflow:

`.github/workflows/deploy-supreme-intelligent-block-v11.yml`

The dedicated workflow currently carries the V12.1 display naming/checks.

### Deployment verification law

A deployment must prove:

1. authoritative source selected
2. correct source marker present
3. production artifact packaged
4. artifact deployed
5. public runtime serves expected artifact
6. Smart Link serves expected application
7. visible runtime matches intended source

The final step cannot be inferred from the first six.

---

# 19. CURRENT PROBLEM INVENTORY

Based on the current project direction, the following are **known redesign/reconstruction areas**:

### HIGH PRIORITY

1. Intelligent Boards — structurally and visually wrong.
2. Main Smart Feed — requires reconstruction.
3. Left/sidebar navigation — currently not meeting desired product standard.
4. Message/Mail experience — not right and requires subsystem-level redesign.
5. Main page composition/hierarchy — has accumulated conflicting implementations.

### POTENTIALLY GOOD / PROTECT UNTIL PROVEN OTHERWISE

6. Logo/brand identity.
7. Search concept/function.
8. Some category/filter concepts.
9. Proven underlying intelligence/feed concepts.

These must be verified before being changed.

### TECHNICAL RISK

10. Multiple historical Hub artifacts exist in the repository.
11. Multiple historical renderer scripts exist.
12. Current V12.1 is an override rather than a clean single-source renderer.
13. Visual source-of-truth versus runtime render path has not been independently proven.

---

# 20. HISTORICAL ARTIFACT INVENTORY RELEVANT TO RECONSTRUCTION

Repository contains multiple Hub-era artifacts, including:

- `2026 09 07  1:14 NAYANETHUBONE.html`
- `2026 09 07 2:05 NAYANET HUB.HTML`
- `2026 09 08 452 NayaNET Hub.html`
- `2026 09 07 NAYANET INTELLIGENT HUB V13 SURGICAL SIDEBAR RESTORATION.js`
- `2026 09 07 11:45 PM NAYANET TEN-STAR DELIVERY RECEIPT FEED.js`
- `nayanet-intelligent-feed-v6.js`

These historical artifacts are evidence, not automatically current authority.

A future Naya must explicitly distinguish:

`CURRENT AUTHORITY` vs `HISTORICAL REFERENCE`.

---

# 21. MASTER COMPONENT INVENTORY TEMPLATE

For every Hub component, future documentation must use this exact model:

## [COMPONENT NAME]

**Purpose:**  
What this component exists to accomplish.

**User sees:**  
Exact visible object/content.

**Location:**  
Where it appears on desktop and mobile.

**Inputs:**  
What data enters it.

**Outputs:**  
What it produces.

**State:**  
Loading / empty / active / disabled / error / success.

**Actions:**  
Every button/click/keyboard interaction.

**Data connection:**  
Source of truth and persistence path.

**Navigation:**  
Where it routes or changes application state.

**Dependencies:**  
Scripts, APIs, data, components.

**Visual contract:**  
Size, hierarchy, typography, surface, spacing, interaction states.

**Responsive contract:**  
Desktop/tablet/mobile behavior.

**Accessibility contract:**  
Keyboard, focus, labels, semantics.

**Verification:**  
What evidence proves it works.

**Protected behavior:**  
What must not be broken during future edits.

**Known problems:**  
Current defects.

**Rebuild decision:**  
PRESERVE / REPAIR / RECONSTRUCT / REMOVE.

---

# 22. REBUILD PROJECT PLAN

## Phase 0 — Freeze and inventory

**Goal:** establish truth before touching design.

Actions:

1. Freeze the current Hub as evidence.
2. Identify the exact authoritative HTML.
3. Identify every script loaded by the Hub.
4. Identify every page/section in the DOM.
5. Identify every visible renderer.
6. Identify every navigation destination.
7. Identify every button and handler.
8. Identify every external link.
9. Identify every data connection.
10. Identify every duplicate/legacy renderer.
11. Identify the actual visible DOM tree for the Intelligent Boards.
12. Identify the actual source of the bottom code/debug artifact.

**Exit condition:** no uncertainty remains about what produces each major visible area, or every remaining unknown is explicitly documented.

## Phase 1 — Define the canonical Hub architecture

Create a clean component map:

`APP SHELL`
→ `BRAND`
→ `NAVIGATION`
→ `TOP BAR`
→ `MAIN PAGE`
→ `CAPTURE`
→ `SEARCH`
→ `CATEGORIES`
→ `INTELLIGENT FEED`
→ `SMART NOTE`
→ `MESSAGE`
→ `PROFILE/ACCOUNT`
→ `RUNTIME/CONNECTION`

## Phase 2 — Reconstruct shell/navigation

Repair the entire sidebar/navigation as one system.

Do not patch individual buttons without understanding the whole navigation contract.

## Phase 3 — Reconstruct main feed

Build one authoritative feed renderer.

Remove competing renderers at their source.

## Phase 4 — Reconstruct Intelligent Boards

Build the actual intelligence object around:

`WISDOM → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → WEAVER → LESSON / MEANING / ACTION`

## Phase 5 — Reconstruct messaging

Treat message functionality as its own complete product surface.

## Phase 6 — Preserve and validate search/categories

Do not change working functionality unnecessarily.

## Phase 7 — Connect persistence and intelligence

Verify Smart Note → Note Event → Feed → Search → Retrieval.

## Phase 8 — Production verification

Perform:

`SOURCE → BUILD → DEPLOY → PUBLIC RUNTIME → VISUAL INSPECTION → ACCEPTANCE`

Only then lock the release.

---

# 23. ACCEPTANCE STANDARD

The rebuilt Hub is not accepted because it is deployed.

It is accepted only when all are true:

### Shell

- [ ] Desktop left sidebar is coherent.
- [ ] No unwanted right Hub sidebar exists.
- [ ] Mobile navigation is coherent.
- [ ] Logo/brand remains correct.
- [ ] Top bar is correct.

### Feed

- [ ] One feed renderer only.
- [ ] No two-column Intelligent Board architecture.
- [ ] No duplicate/legacy renderer visible.
- [ ] No code/debug/implementation artifact visible.
- [ ] Feed reads as intelligence, not dashboard cards.

### Intelligent Board

- [ ] Wisdom is the conceptual anchor.
- [ ] Human/Child/Grandma/Naya/Machine are distinct intelligence perspectives.
- [ ] Weaver is the synthesis climax.
- [ ] Lesson/Meaning/Action produce compounding output.
- [ ] Visual hierarchy is premium and intentional.
- [ ] No fake data.

### Search/categories

- [ ] Search works.
- [ ] Categories work.
- [ ] Empty states work.
- [ ] Results remain connected to intelligence.

### Capture/Smart Notes

- [ ] Capture works.
- [ ] Smart Note persists.
- [ ] Feed projection is correct.
- [ ] Search/retrieval is correct.

### Messaging

- [ ] Navigation works.
- [ ] Threads work.
- [ ] Compose/reply works if enabled.
- [ ] States/errors work.
- [ ] Mobile works.

### Engineering

- [ ] One source of truth.
- [ ] No repair-loop dependency.
- [ ] No hidden duplicate renderer.
- [ ] Responsive.
- [ ] Accessible.
- [ ] Runtime independently verified.

### Final acceptance

**THE SCREEN MUST MATCH THE INTENDED PRODUCT.**

---

# 24. NAYA RECONSTRUCTION INSTRUCTION

A new Naya receiving this project must not begin by editing code.

The required order is:

`READ THIS MASTER INVENTORY`
→ `READ CURRENT-STATE FEED`
→ `IDENTIFY CURRENT AUTHORITY`
→ `INSPECT ACTUAL RENDER PATH`
→ `INVENTORY COMPONENT`
→ `PRESERVE WORKING FUNCTION`
→ `REMOVE CONFLICTING IMPLEMENTATION`
→ `RECONSTRUCT ONE AREA`
→ `TEST INTERACTIONS`
→ `DEPLOY`
→ `VERIFY PUBLIC RUNTIME`
→ `VERIFY VISIBLE UI`
→ `RECORD SMART NOTE`
→ `CONTINUE`

Never assume that a file named “current,” “V13,” “V12,” “final,” or “supreme” is authoritative merely because of its name.

**Runtime truth beats filename intent.**

---

# 25. CURRENT STATE / TRUTH BOUNDARY

## Verified from repository

- Current Hub source file exists on `main`.
- Current feed JS exists on `main`.
- Current source contains the observed shell/component CSS families listed above.
- Current feed JS contains the V12.1 legacy-board reconstruction layer.
- The repository contains multiple historical Hub artifacts.
- The broader Naya Power architecture defines the Intelligent Feed as a current-state continuity projection over durable intelligence.

## Not yet independently proven by this inventory

- Exact visible DOM renderer for every page.
- Exact click handler for every button.
- Exact destination for every navigation item.
- Exact runtime data source for every metric/status object.
- Exact visual appearance of the public runtime.
- Exact origin of every currently visible unwanted artifact.
- Complete visual parity between the source and the user's current screen.

These are **not failures of the project plan**. They are explicit verification boundaries that prevent future false claims.

---

# 26. FIRST EXECUTION TARGET

The first implementation cycle after this inventory must **not** redesign anything yet.

It must produce the missing forensic map:

`VISIBLE AREA → DOM NODE → SOURCE FILE → SCRIPT → HANDLER → DATA → DESTINATION → STATE → DEPLOYED RUNTIME`

Once that map is complete, reconstruction can proceed deliberately.

This is the point at which the project stops going in circles.

---

# 27. MASTER PRINCIPLE

> **We are not rebuilding the Hub from memory. We are rebuilding it from evidence.**

> **We are not patching symptoms. We are identifying the actual source of every visible behavior.**

> **We are not measuring success by commits. We are measuring success by the working product.**

> **We preserve what works, remove what conflicts, and reconstruct what has been damaged.**

> **The user's visible screen is the final truth.**

---

**Status:** INVENTORY / RECONSTRUCTION FOUNDATION CREATED  
**Date:** 2026-09-09  
**Next required artifact:** component-level forensic map of the actual current runtime and complete page/interaction inventory.  
**Do not declare the Hub rebuilt until runtime and visible UI verification are complete.**
