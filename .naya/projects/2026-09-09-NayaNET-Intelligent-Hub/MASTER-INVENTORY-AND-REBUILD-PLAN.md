# NayaNET Intelligent Hub — Master Inventory

> **CANONICAL BLUEPRINT:** [MASTER-BLUEPRINT.md](./MASTER-BLUEPRINT.md)

This file is retained as the original project inventory artifact, but the deeper forensic specification now lives in the numbered blueprint documents below. Future Naya rebuild work should use the Master Blueprint as the index and the seven maps as the detailed contract.

## Project

- Date: 2026-09-09
- Source snapshot audited: `2026 09 08 452 NayaNET Hub.html`
- Feed asset: `nayanet-intelligent-feed-v6.js`
- Repository: `SoulSchoolAcademy/NayaPOWER`
- Branch: `main`

## Read in this order

1. [MASTER-BLUEPRINT](./MASTER-BLUEPRINT.md)
2. [PAGE MAP](./01-PAGE-MAP.md)
3. [COMPONENT MAP](./02-COMPONENT-MAP.md)
4. [INTERACTION + LINK MAP](./03-INTERACTION-LINK-MAP.md)
5. [INTELLIGENCE MAP](./04-INTELLIGENCE-MAP.md)
6. [VISUAL + RESPONSIVE MAP](./05-VISUAL-RESPONSIVE-MAP.md)
7. [ENGINEERING + VERIFICATION MAP](./06-ENGINEERING-VERIFICATION-MAP.md)
8. [REBUILD + ACCEPTANCE CONTRACT](./07-REBUILD-ACCEPTANCE-CONTRACT.md)

## Important distinction

The original inventory was intentionally expanded rather than discarded. The new documents add the missing depth: exact destinations, click behavior, persistence, intelligence flow, renderer architecture, responsive behavior, and verification requirements.

## Release blocker

The repository currently contains an authority discrepancy: `.naya/INTELLIGENT-FEED.md` refers to `NAYANETHUBONE.html` as the authoritative Hub source, while the current deployment workflow packages `2026 09 08 452 NayaNET Hub.html`. Resolve this before declaring the rebuilt Hub production-ready.

## Definition of done

**SOURCE → BUILD → DEPLOY → RUNTIME → OBSERVATION → INTERACTION → PERSISTENCE → MOBILE → NO REGRESSION**

A commit or workflow success alone is not completion.
