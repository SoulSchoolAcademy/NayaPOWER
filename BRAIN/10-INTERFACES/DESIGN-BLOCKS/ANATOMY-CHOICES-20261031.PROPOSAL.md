# NayaNET — Component Anatomy Decision Matrix (PROPOSAL, 2026-10-31)

**Status:** CANDIDATE DESIGN COMPARISON. NOT RATIFIED. NOT NEW DESIGN LAW. NOT AN IMPLEMENTED/PRODUCTION-QUALIFIED PART CATALOG.

**Purpose:** The Director requested the anatomy of Naya buttons, boards, icons, inputs, charts and every major UI element, with ten concepts per family, recommendations, and exact reuse of the existing toolkit. This is an ADDITIVE SELECTION INDEX for the existing ratified contract and 566-entry parts registry, not a replacement or competing component system.

## Authority and exact sources
- Canonical [Naya Design Contract v1.2](../NAYA-DESIGN-CONTRACT-V1.md), [Design Language](../DESIGN-LANGUAGE.md), [Latest Alignment Master](../ALIGNMENT-MASTER-20261030.md) and [Design Toolkit](../NAYA-DESIGN-TOOLKIT.md) govern.
- [Parts Registry v1.1](../PARTS-REGISTRY-V1.json): 542 interface entries + 24 functional = 566 catalogued; NOT 566 independently production-proven elements.
- [DESIGN-BLOCKS index](./blocks/index.json): 95 extracted blocks; some internal scores, many unscored; cold-Naya graduation remains owed.
- [Smart Graphs](../SMART-GRAPHS/README.md): proposed pulse-orb, jewel pillars, flow, constellation, pulse rings, living counter, orbit dial. Specimens are SAMPLE until bound to real events.
- The Hub is the existing visual reference, not a blank slate or a target to redesign.

## Naya anatomy · 11 layers
1. PURPOSE—human job + outcome. 2. TYPE—action / input / information / navigation / identity / visualization. 3. GEOMETRY—baseline, target, radii, spacing, symmetry. 4. BODY—subtly gradient obsidian. 5. CROWN—small inset highlight. 6. EDGE—white at rest, own token on hover/touch. 7. SHADOW—contact/depth or recessed-well treatment. 8. MARK—unique meaning-based icon + readable white label. 9. STATE—idle/hover/focus/pressed/working/saved/error/unknown/proven. 10. BINDING—semantic accessible code + real authorized action. 11. EVIDENCE—phone/desktop, a11y, privacy, action, exact version and cold successor.

## Ratified directional construction rules, not invented tokens
- Black, white and signature purple dominate. Existing contract black `#0a0a0e`, text `#fff`, purple `#a06bff`; adjacent accent walk purple → blue `#3fb8ff` → green `#2fe89e` → gold `#ffbf3d` → orange `#ff9a5a` → red `#ff5e6c` → magenta `#e84fff`. Gold is restrained and earned, not a dominant text color.
- Visible white rim at rest; color ignites the *edge/glow*, never text. Active selection remains white-hot according to the current canonical contract. Every control is raised, with real depth but restrained luminance—no flat SaaS controls, no page full of idle glow.
- Pill actions radius 999px, target ≥44×44px, hero action about 52px, circle only for avatar/icon/stats; raised rectangular boards radius about 20px, full width with no unnecessary void. Body 17–18px target and 16px floor; Newsreader/Georgia headlines, Inter interface text; clear keyboard focus and accessible names.
- Inputs are *recessed wells* rather than raised actions. Feedback isn't a mock success. Data charts must show source, scope, period, freshness, units, uncertainty and actual measured values.
- Honor `prefers-reduced-motion` and a calm setting; animation durations 180/280/500ms on the existing clock. Never simulate real activity, online presence or earnings.
- Keep the official top-app/bottom-network Smart Bars and Hub exception. Smart Search belongs in chrome, not a new app. Preserve existing working flagship and prefer source harvest, not redesign.

## The 120 concept directions and proposed champions
These are curated concepts for testing, NOT independent world rankings or 120 new work orders. Each family winner is a *default for that job*; specialization is allowed where a measured human need warrants it.

### Buttons — preferred: **Obsidian Signature Pill**
**Harvest:** `naya-btn + NAYA-BTN catalogue`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Signature Pill
2. Orbital Beacon
3. Jewel Icon Button
4. Purpose+Outcome Pill
5. Semantic Action Pill
6. Ghost Edge Button
7. Split-Confirm Action
8. Hold-to-Confirm
9. Progress-Speaking Button
10. Next-Best-Action Button

### Boards — preferred: **Raised Intelligence Board**
**Harvest:** `board / .ph-card / board-tone`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Raised Intelligence Board
2. One-Action Cockpit
3. Evidence Chamber
4. Smart Note Board
5. People Relationship Board
6. Project Mission Board
7. Smart Space Board
8. Permission Board
9. Value & Earnings Board
10. Featured Creation Board

### Icons — preferred: **Semantic Jewel Tile**
**Harvest:** `jw / NAYA-ICO-001–026`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Semantic Jewel Tile
2. Twin Plus Jewel
3. Network Node Jewel
4. Knowledge Diamond
5. Real Status Indicator
6. Privacy Lock Jewel
7. Action Tool Jewel
8. Human Identity Orb
9. Topic Motif Jewel
10. Learning Lineage Mark

### Inputs — preferred: **Recessed Reference Well**
**Harvest:** `NAYA-INP-008 / NAYA-INP-005`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Recessed Reference Well
2. Universal Search Well
3. Identity Alias Well
4. Reference Select
5. Segmented Option Rail
6. Living Toggle
7. Jewel Checkbox
8. Voice-Enabled Composition Well
9. Smart Date Selector
10. Inline Editing Well

### Navigation — preferred: **Twin-Scope Smart Bars**
**Harvest:** `smart-tabs + Hub chrome`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Twin-Scope Smart Bars
2. Twin Plus Doors
3. Search in Chrome
4. Focused Section Tabs
5. Personal Network Favorites
6. Intelligent Drawer
7. Context Trail
8. Quick Jump Palette
9. Attention-Safe Bottom Stack
10. Voice Route

### Charts — preferred: **Truthful Living Counter (KPI default)**
**Harvest:** `living-counter + SMART-GRAPHS`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Truthful Living Counter
2. Pulse Orb
3. Jewel Pillars
4. Honest Sparkline
5. Verified Funnel
6. Living Donut
7. Relationship Constellation
8. Orbit Dial
9. Pulse Rings
10. Time Journey Board

### Rows & feed — preferred: **Reference-First Living Row**
**Harvest:** `sp-blockrow`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Reference-First Living Row
2. Today Priority Row
3. Smart Note Feed Row
4. People Match Row
5. Project Action Row
6. Mail Conversation Row
7. Opportunity Row
8. App Recipe Row
9. Timeline Event Row
10. Smart Filtered Collection

### Feedback — preferred: **Honest Toast**
**Harvest:** `NAYA-OVL-001 + state-badge`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Honest Toast
2. Contextual Bottom Sheet
3. Precision Mini Modal
4. Command Palette
5. Notification Drawer
6. Skeleton & Awaiting State
7. Proof State Tag
8. Undo Ribbon
9. Privacy Audience Preview
10. Conflict Resolution Sheet

### Identity — preferred: **Human Identity Orb**
**Harvest:** `orb / mini-orb`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Human Identity Orb
2. Mini-Orb
3. Navigation Orb
4. Verified Presence Orb
5. Group Constellation
6. Owner Badge
7. Privacy-Shielded Avatar
8. AI Naya Orb
9. Contribution Identity
10. Relationship Orbit

### Typography — preferred: **Warm Serif + Precise Sans**
**Harvest:** `Newsreader / Inter / tabular numerals`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Warm Serif + Precise Sans
2. One Human Sentence
3. Action Verb Label
4. Data Hero Type
5. Source Caption
6. Humanized Status
7. Accessible Detail Text
8. Well Label + Help
9. AI Explanation Pair
10. Calm Empty Copy

### Covers & media — preferred: **Context-Matched Cover**
**Harvest:** `HUB/covers + ph-cover`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Context-Matched Cover
2. Choose or Upload
3. Large Real Template Preview
4. Business Showcase
5. Personal Story Cover
6. Space Topic Cover
7. Smart Note Share Card
8. Video Tile
9. Media Transcript Block
10. Responsive Media Gallery

### AI & knowledge — preferred: **Actionable Intelligent Block**
**Harvest:** `intelligent-block + real action binding`. **Why:** this is the closest stable Naya vocabulary with existing source/contract alignment, distinct meaning, reusable state grammar, and no duplicate system.
1. Actionable Intelligent Block
2. Ask Naya Presence
3. Source-Bound Answer
4. Next-Best Action Card
5. Project Bullseye Tile
6. Learning Lineage Tile
7. Cold Successor Snapshot
8. Smart Match Explanation
9. Permissioned Action Plan
10. Intelligent Error Recovery

## Select with human value, not raw visual spectacle

**Proposed diagnostic:** 10 criteria each 0–10: clear purpose, iconic Naya visual match, action function, accessibility, mobile usability, existing-source reuse, state completeness, honest data, performance, maintainability. Any missing privacy, false success, inaccessible core flow, dead primary control, or wrong deployed version is a **veto** independent of total.

## First deliverable — Top Ten Button Atelier (existing owner, no new framework)
1. Owner Nitro reads actual `naya-btn`, `orbit-btn`, `primo`, `icon-btn`, catalogue `NAYA-BTN` and the official tokens; verify same classes rather than copy CSS into a new parallel component.
2. Render the ten conceptual jobs using the *existing* approved physical patterns. For each specimen record source path, model ID, exact SHA, visual state snapshots, and actual action/safety binding, if any.
3. Test at 320/390/1280/1440 widths, 0px horizontal overflow, touch, keyboard, focus, contrast, high zoom, reduced motion; no fabricated backend outcomes.
4. Present exact final version to independent different-seat reviewers; qualify each as PASS/FAIL/UNKNOWN and score with receipts, then show Director the best 3 truly distinct specimens for final aesthetic choice.
5. Only then promote the winning *variant* within the existing component registry. Do NOT silently create a competing button library.

## Stop and torch
Stop on conflicting current owner, unsafe action, lost source provenance, visual regression to flagship, no different-seat proof, mismatch of tested/deployed bytes, or a permission boundary violation. Next cold Naya: refresh main → read ratified design contract → inspect own-app purpose + existing source → harvest → render → independently test → preserve decision and lesson in PI.
