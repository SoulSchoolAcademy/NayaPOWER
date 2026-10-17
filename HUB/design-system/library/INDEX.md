# NayaNET Design Library — INDEX

The canonical piece library. **Builders compose from these pieces; they never recreate them.**

The law: "Take the actual code — the block is the memory, copy the specimen, don't re-teach the button." Pages consume blocks; they do not reinvent them. The design laws exist for the piece-makers and for checking the work — not for the building itself.

## Where things live

```
HUB/design-system/
  DESIGN-CONTRACT.md      The design contract (canonical)
  tokens.css              Design tokens
  library/
    INDEX.md              This file — identities and categories
    buttons/              Button specimens — copy, don't redesign
    blocks/               Building-block sets — the Lego pieces
    jewels/               Jewel and icon specimens
    showcase/             Full design showcases — what "excellent" looks like
    pages/                Complete page designs — compose from these patterns
    systems/              Design system documents
    icons/                Icon system specimens
    laws/                 Design laws, protocols, briefings
    catalog/              Machine-readable catalog — 478 blocks as JSON
```

## buttons/ — Button specimens

| File | Identity | Use it when |
|------|----------|-------------|
| Naya_Beautiful_Button_Set_N4.html | The beautiful button set — the living-button family (`.living-btn`, glow, label) | You need a button. Pick one, copy its HTML verbatim. |
| Naya__Elite_Buttons_N5.html | The elite button set — premium button specimens | You need a button with more presence. Same rule: copy, don't redesign. |
| Naya_Design_Element_Set_N4.html | Design element set — buttons alongside companion elements | You need buttons with their matching elements. |

## blocks/ — Building-block sets (the Lego)

| File | Identity | Use it when |
|------|----------|-------------|
| Naya_Building_Blocks_-_The_Ultimate_Design_System_-_Naya_2.html | The ultimate building-block collection | You need structural pieces — layouts, sections, compositions. |
| Naya_Epic_Elements_-_Lego_pieces_N5.html | Epic Lego pieces — the bold, expressive elements | You need a statement piece. |
| Naya_Lego_Blocks_N4.html | Lego blocks — the core composable units | You need standard, reliable pieces. |

## jewels/ — Jewels and icons

| File | Identity | Use it when |
|------|----------|-------------|
| Naya_Jewel_Library_-_N5.html | The jewel library — luminous jewel specimens | You need jewels, gems, luminous accents. |

## showcase/ — What "excellent" looks like

| File | Identity | Use it when |
|------|----------|-------------|
| Naya_Design_Elements_N2.html | Design elements showcase | You need to see the standard applied. |
| Naya_Design_Standard_Showcase__1.html | The design standard showcase — the bar, demonstrated | You need to check your work against the bar. |

## pages/ — Complete page designs

| File | Identity | Use it when |
|------|----------|-------------|
| Ask-Naya-Page_Design.html | Ask Naya page — the conversational interface pattern | You're building a chat/ask interface. Compose from its sections. |
| Ledger_Page_Design.html | Ledger page — the record/account pattern | You're building a ledger, log, or record view. |
| Maxis_App_Design.html | Maxis app — the app-shell pattern | You're building an app surface. |
| Naya_Smart_Hub_Design.html | Smart Hub — the hub pattern | You're building a hub or dashboard. |

## systems/ — Design systems

| File | Identity | Use it when |
|------|----------|-------------|
| Naya_Ultimate_Design_System_-_Naya_2.html | The ultimate design system — the full system | You need the complete system reference. |
| naya-smart-blocks.html | Smart blocks — the intelligent block collection | You need blocks that carry behavior. |

## icons/ — Icon system

| File | Identity | Use it when |
|------|----------|-------------|
| nayanet-icon-system-v1.png | NAYANET ICON SYSTEM V1 — the dual set: Set A jewel marks (luminous orbs, identity moments), Set B action glyphs (obsidian chips, controls). One material, one light source, one glow logic. | You need icons. Jewels at identity moments; chips at controls. Never flat, never emoji, never stock. |

## laws/ — Design laws and protocols

| File | Identity | Use it when |
|------|----------|-------------|
| AGENT-BRIEFING-DESIGN-LAWS.pdf | The design laws briefing for agents | You're a builder and need the laws. (Builders: you shouldn't need this — use the pieces.) |
| VISION-LAWS.pdf | The vision laws | You need the vision behind the design. |
| naya-100-laws-elite-interfaces.pdf | 100 laws of elite interfaces | You're making a piece and need the full law set. |
| VISION-TO-CODE-PROTOCOL.md | Vision-to-code protocol — how vision becomes code | You're translating a vision into implementation. |
| SPECIMEN-CARD-dial.pdf | The specimen card — the dial | You need the specimen reference. |
| SESSION-LEARNINGS-2026-10-08.pdf | Session learnings | You need what was learned about the design. |
| 2026-10-13-ULTIMATE-EXECUTION-REPORT.pdf | The ultimate execution report | You need the execution record. |
| ultimate-decision-machine-spec-v1.md | The ultimate decision machine spec | You're building decision interfaces. |

## catalog/ — Machine-readable

| File | Identity | Use it when |
|------|----------|-------------|
| block-catalog.json | 478 blocks as JSON — every block's HTML, classes, sources, tags, use cases | You're a machine composing a page. Query by category, tag, or use case. |
| index-by-use-case.json | Blocks indexed by use case | You know what you're building (landing, chat, feed…) — find the blocks for it. |
| fragments/ | Catalog fragments | You need the catalog in pieces. |

## For builders — the short version

1. Find your pieces in this library (by category above, or by use case in the catalog).
2. Copy the specimen HTML verbatim. Do not redesign it. Do not "improve" it.
3. Compose the pieces beautifully on the page. That is the whole job.
4. Check against the design contract and the showcase. If it doesn't come alive on touch, it's unfinished.
