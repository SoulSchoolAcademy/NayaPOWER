# NayaNET Intelligent Hub — Read First

**Status:** HUB PROJECT-INTELLIGENCE INDEX — proposed on PR #1271  
**Purpose:** Give every Naya, designer, engineer, and reviewer one reliable entrance into the Hub experience before touching implementation.

## The decisive rule

> **The current visual Hub is the minimum visual-quality baseline, not the production architecture.**

Do not replace the experience with a generic SaaS dashboard merely because a cleaner implementation is easier. The implementation underneath must become dramatically cleaner. The visible experience may change only when the result is demonstrably better.

The Hub is the **human cockpit / projection layer** over governed NayaPOWER intelligence. It is not a second brain, second database, second authority system, or shadow memory.

## Read in this order

1. [Official Hub Experience Contract](../NAYA-ACTIVATION/DESIGN/NAYANET-HUB-EXPERIENCE-CONTRACT-V1.md)
2. [00 — Hub Project Intelligence Start Here](./PROJECT-INTELLIGENCE/00-START-HERE.md)
3. [01 — Deep Audit & AAA Scorecard](./PROJECT-INTELLIGENCE/01-HUB-DEEP-AUDIT-AND-SCORECARD.md)
4. [02 — Room, Board & Feature Contract](./PROJECT-INTELLIGENCE/02-HUB-ROOM-BOARD-AND-FEATURE-CONTRACT.md)
5. [03 — Journey, Routing & State Contract](./PROJECT-INTELLIGENCE/03-HUB-JOURNEY-ROUTING-AND-STATE-CONTRACT.md)
6. [04 — Production App Conversion Blueprint](./PROJECT-INTELLIGENCE/04-PRODUCTION-APP-CONVERSION-BLUEPRINT.md)
7. [05 — Cold-Naya Build Prompt](./PROJECT-INTELLIGENCE/05-COLD-NAYA-BUILD-PROMPT.md)
8. [Machine Interface Manifest](./PROJECT-INTELLIGENCE/HUB-INTERFACE-MANIFEST-V1.json)
9. [Machine Design Tokens](./PROJECT-INTELLIGENCE/HUB-DESIGN-TOKENS-V1.json)
10. [AAA Acceptance Contract](./PROJECT-INTELLIGENCE/HUB-AAA-ACCEPTANCE-V1.json)

Smart Door authority remains in [BRAIN/10-INTERFACES](../BRAIN/10-INTERFACES/README.md).

## Current physical artifacts on main

| Artifact | Current role | Preserve? | Production truth |
|---|---|---:|---|
| `NAYANET WELCOME PAGE.html` | Premium entrance / visual concept | YES | Concept surface; routing needs reconciliation |
| `NAYANET INDENITY PAGE.html` | Identity activation concept | VISUAL IDEAS ONLY | Needs major production rebuild; filename is misspelled |
| `NAYANET INTERFACE CONCEPT.html` | 843 KB accumulated Hub visual laboratory | YES AS VISUAL FLOOR | Not maintainable production architecture |
| `hub.html` | Powercast player | YES, but classify correctly | **Not the Intelligent Hub** |
| icons / manifest | app assets | REVIEW | Asset/support layer |

## Canonical human journey

**WELCOME → IDENTITY → INTELLIGENT HUB**

Powercast, Academy, White Paper, About Us and other ecosystem destinations may remain available, but Academy/Powercast are not the default successful onboarding destination.

## Canonical human-facing Hub navigation

**Smart Feed · Your Intelligence Today · Your Reports · Intelligent Library · Smart Connect · Smart Ledger · Your Connections · Smart Lists · Smart Mail · Smart Spaces · Settings**

`Smart Share` is historical UI language. Production uses **Smart Connect**.

## Smart Connect / Smart Doors law

**Smart Connect** is the human participation / connection / consent surface.  
**Smart Doors** are governed capability channels.

A Door exposes what Naya **can** do. LAW decides what Naya **may** do. ACT executes. VERIFY checks what happened.

Connection or technical availability never creates authority.

## Evidence boundary

These files establish design/product/project intelligence. They do **not** claim that the current HTML is production-ready, that every control works, or that a backend/browser journey is production-proven.

**Visual quality + causal functionality + truth + speed + accessibility + governed data = shippable.**
