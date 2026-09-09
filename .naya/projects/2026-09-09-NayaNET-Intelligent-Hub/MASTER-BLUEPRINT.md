# NayaNET Intelligent Hub — MASTER BLUEPRINT

**Project date:** 2026-09-09  
**Source snapshot audited:** `2026 09 08 452 NayaNET Hub.html`  
**Repository:** `SoulSchoolAcademy/NayaPOWER`  
**Branch:** `main`

## THIS IS THE LOCKED BLUEPRINT INDEX

This project is now the reconstruction authority for the NayaNET Intelligent Hub. The older `MASTER-INVENTORY-AND-REBUILD-PLAN.md` remains historical project material; the documents below are the deeper forensic specification and should be read as one system.

### 01 — PAGE MAP
Exact internal page states, entry/exit paths, external links, Smart Link, feature-report destinations, and page-by-page behavior.

[Open Page Map](./01-PAGE-MAP.md)

### 02 — COMPONENT MAP
Every major shell, page, feed, note, mail, intelligence, settings and utility component: purpose, behavior, data, persistence and dependencies.

[Open Component Map](./02-COMPONENT-MAP.md)

### 03 — INTERACTION + LINK MAP
Buttons, controls, clicks, functions, state changes, destinations, persistence and feedback behavior.

[Open Interaction + Link Map](./03-INTERACTION-LINK-MAP.md)

### 04 — INTELLIGENCE MAP
Human → Naya → Machine → Smart Note → Intelligent Feed → Search → Daily Intelligence → Learning → Compounding, plus the target board sequence.

[Open Intelligence Map](./04-INTELLIGENCE-MAP.md)

### 05 — VISUAL + RESPONSIVE MAP
Layout, typography, dimensions, surfaces, borders, glow, hierarchy, desktop/mobile behavior, accessibility and visual prohibitions.

[Open Visual + Responsive Map](./05-VISUAL-RESPONSIVE-MAP.md)

### 06 — ENGINEERING + VERIFICATION MAP
HTML/JS architecture, local stores, APIs, renderer model, deployment path, runtime verification and the architecture that should replace the current layered override model.

[Open Engineering + Verification Map](./06-ENGINEERING-VERIFICATION-MAP.md)

### 07 — REBUILD + ACCEPTANCE CONTRACT
The AAA execution sequence and the exact definition of done.

[Open Rebuild + Acceptance Contract](./07-REBUILD-ACCEPTANCE-CONTRACT.md)

## Critical source facts captured from the actual Hub

### External ecosystem destinations
- HOME → `https://hmclibrary.groovemember.net/home`
- NAYA POWER → `https://academy.nayanet.app/`
- “5” DAY CHALLENGE → `https://academy.nayanet.app/`
- ENTER FREE → `https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab`
- POWERCASTS → `https://nayanet.groovepages.com/powerplayer`
- WHITE PAPER → `https://nayanet.groovepages.com/whitepaper`
- ABOUT US → `https://nayanet.groovepages.com/aboutus`
- HMC LOGIN → `https://hmclibrary.groovemember.net/login`

### Feature report destinations
- SMART NOTES → Google Drive ID `19sRtp22aAn35wNoqqpNiZHkaFGmUOxoP`
- NO DEAD ENDS → Google Drive ID `1LgRmYAQ85AB6mmu6Qp2ovghyd1lP-FNh`
- CONTEXT LAW → Google Drive ID `1N-XzV3_RCTHuLdp4leZNlOo7ITFwrICR`
- “10” STAR SERVICE → Google Drive ID `1F9M66i5Av_oJcIa5dve-U0mMeAgYKczT`
- ADAPTIVE LEARNING → Google Drive ID `1dcViGUqV7GKnNBCYybbAEEKuOoZw3-XC`

### Primary intelligence mount
`#homeIntelligentBlocks`

### Primary feed renderer asset
`nayanet-intelligent-feed-v6.js` — currently labeled V12.1 TRUE LEGACY BOARD RECONSTRUCTION.

### Current production runtime configured by deployment workflow
`https://nayanet-v7-intelligent-hub.nayanet.workers.dev/`

### Current Smart Link configured by deployment workflow
`https://nayanet-v7-intelligent-hub.nayanet.workers.dev/intelligence/nayanet-intelligent-feeds`

## What this blueprint learned from the failed implementation cycle

1. A deployment receipt is not a visual result.
2. Multiple renderers fighting over the same DOM make the product impossible to reason about reliably.
3. A historical source name must never silently become current authority.
4. A right-rail removal must be structural, not endlessly re-hidden by overlays.
5. Smart Notes, Intelligent Feed and current-state continuity must be one intelligence architecture.
6. Local persistence must be labeled local; server persistence must be proven separately.
7. Naya interpretation must never be fabricated when the production service is absent.
8. Every external link must be preserved exactly unless intentionally changed.
9. Every button must have a documented click contract.
10. The screen is the final acceptance test.

## Canonical product architecture to build from here

```text
USER / HUMAN EXPERIENCE
        ↓
CAPTURE
        ↓
CANONICAL SMART NOTE / NOTE EVENT
        ↓
VALIDATE + PERSIST
        ↓
NAYA PROCESSING (when connected)
        ↓
MACHINE RECEIPT / EVIDENCE
        ↓
INTELLIGENT FEED PROJECTION
        ↓
SEARCH / RETRIEVAL
        ↓
WEAVER / SYNTHESIS
        ↓
LESSON → MEANING → ACTION
        ↓
DAILY INTELLIGENCE
        ↓
ADAPTIVE LEARNING / PREFLIGHT
        ↓
COMPOUNDING INTELLIGENCE
```

## Current unresolved release blocker

The repository's continuity document says `NAYANETHUBONE.html` is the authoritative Hub source, while the current deployment workflow explicitly packages `2026 09 08 452 NayaNET Hub.html`. This must be reconciled before the rebuild is called production-ready.

## Rule for every future Naya

**Read this blueprint first. Inspect the actual source next. Reconstruct from verified facts. Make one surgical change at a time. Verify the exact public runtime. Then lock the result into this project.**
