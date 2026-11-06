# ACT ROLLOUT — every page, board, button, icon, tile, block

**DRAFT — the Clarity Confirmation Act is NOT stamped by Shawn; nothing here is law yet.**

Shawn’s order, 2026-11-06 00:31Z: the same treatment goes to ALL of our pages, all of our boards, all our buttons — everything, all of our parts. Every page, board, button, icon, tile, block gets updated to the Act’s language. **ORDER: Dashboard first, then Personal, then the rest (Business, Space, and the others) — finish the first thing before moving to the next.**

The craft rule: each piece is optimized for what IT is — the most extraordinary button, board, icon, tile, block — molded and crafted for what it is, with the SAME principles and concept language running through all of them. The universal language + the specific craft per piece. Per-piece craft lives in each inventory entry (`signature-pieces/*.html`, `INVENTORY.md`, `inventory.json`).

## States

- **TREATED** — piece harvested + crafted + inventoried (this pass). The piece is ready; the page edit is a separate step.

- **IN PROGRESS** — owned by another lane right now. Do not touch, do not collide.

- **NOT YET** — queued. Rollout edits deferred until its turn, in order.

## The six — in Shawn’s order

| # | Page | State | Pieces it takes | Template | Evidence |
|---|---|---|---|---|---|
| 1 | **Dashboard** (nayanet.live/dashboard) | TREATED — pieces inventoried · PAGE EDIT NOT YET | 01, 05, 06, 11, 12, 13, 16, 18, 19, 20, 21, 22, 07, 08, 09, 15 | `templates/dashboard.html` | templates/dashboard.html (verbatim whole, sha-verified) + signature-pieces/ (groups 1+3). |
| 2 | **Personal** (nayanet.live/personal) | TREATED — pieces inventoried · PAGE EDIT NOT YET | 02, 03, 04, 10, 14, 17, 07, 08, 09, 15, 01 | `templates/personal.html` | templates/personal.html (assembled 2026-11-03, verified present) + signature-pieces/ (groups 2+3, button 01 reused from Dashboard). |
| 3 | **Business** (nayanet.live/business) | NOT YET — queued | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 | `templates/business.html` | templates/business.html (assembled 2026-11-03, verified present); all 22 pieces compose from inventory. |
| 4 | **Space** (nayanet.live/space) | NOT YET — queued | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 | `templates/space.html` | templates/space.html (assembled 2026-11-03, verified present); all 22 pieces compose from inventory. |
| 5 | **Membership (Smart Access)** (membership pages) | NOT YET — queued | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 | `templates/membership.html` | templates/membership.html (assembled 2026-11-03, verified present); all 22 pieces compose from inventory. |
| 6 | **Hub** (nayanet.live (Hub)) | BOARD IN PROGRESS — other lane · DO NOT TOUCH | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 | `templates/hub.html` | templates/hub.html (verbatim whole harvest, sha-verified) — for reference/composition only, never an edit to the live Hub file. Branch remotes/origin/hub-board-black-live-20261105 exists; repo git status clean of this role’s work. |

## The six, in detail

### 1. Dashboard — TREATED — pieces inventoried · PAGE EDIT NOT YET
v7 Builder in flight on team-nitro/dashboard/index-reporting-pass1-20261105.html (mtime 2026-11-06 00:16Z). Coordinate, never collide: rollout edits to the Dashboard happen AFTER the v7 Builder lands.
Pieces: 01, 05, 06, 11, 12, 13, 16, 18, 19, 20, 21, 22, 07, 08, 09, 15. Template: `templates/dashboard.html`. Evidence: templates/dashboard.html (verbatim whole, sha-verified) + signature-pieces/ (groups 1+3).

### 2. Personal — TREATED — pieces inventoried · PAGE EDIT NOT YET
After Dashboard finishes — finish the first thing before moving to the next.
Pieces: 02, 03, 04, 10, 14, 17, 07, 08, 09, 15, 01. Template: `templates/personal.html`. Evidence: templates/personal.html (assembled 2026-11-03, verified present) + signature-pieces/ (groups 2+3, button 01 reused from Dashboard).

### 3. Business — NOT YET — queued
BUILD FRESH per PI §7: assemble from the flagship chassis — never a new design.
Pieces: 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22. Template: `templates/business.html`. Evidence: templates/business.html (assembled 2026-11-03, verified present); all 22 pieces compose from inventory.

### 4. Space — NOT YET — queued
EDIT per PI §7.
Pieces: 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22. Template: `templates/space.html`. Evidence: templates/space.html (assembled 2026-11-03, verified present); all 22 pieces compose from inventory.

### 5. Membership (Smart Access) — NOT YET — queued
Membership is an add-on to any page, never a separate app (Act §4.8).
Pieces: 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22. Template: `templates/membership.html`. Evidence: templates/membership.html (assembled 2026-11-03, verified present); all 22 pieces compose from inventory.

### 6. Hub — BOARD IN PROGRESS — other lane · DO NOT TOUCH
Hub board owned by the v5 team (agent 3cf0b8cc, branch hub-board-black-live-20261105 — remote branch verified present). HUB/app/index.html is THEIRS: this role harvests from it read-only (via harvested/hub.html) and never edits it. Other Hub surfaces: NOT YET.
Pieces: 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22. Template: `templates/hub.html`. Evidence: templates/hub.html (verbatim whole harvest, sha-verified) — for reference/composition only, never an edit to the live Hub file. Branch remotes/origin/hub-board-black-live-20261105 exists; repo git status clean of this role’s work.

## The others — queued after the six (PI §8 lane order)

| Page | URL | PI §7 work type | State |
|---|---|---|---|
| Home | nayanet.live/ | EDIT | NOT YET — queued after the six |
| Intel Today | nayanet.live/rooms/today | EDIT | NOT YET — queued after the six |
| Growth | nayanet.live/rooms/growth | EDIT | NOT YET — queued after the six |
| About | nayanet.live/about | EDIT | NOT YET — queued after the six |
| Connections | nayanet.live/rooms/connections | EDIT | NOT YET — queued after the six |
| Smart Mail | nayanet.live/rooms/mail | EDIT | NOT YET — queued after the six |
| Smart Lists | nayanet.live/lists | REPLACE — pilot built, scored 9.0 | NOT YET — queued after the six |
| Reports | nayanet.live/rooms/reports | EDIT | NOT YET — queued after the six |
| Settings | nayanet.live/settings | REDO — compose the one true page from harvested parts | NOT YET — queued after the six |
| Library | nayanet.live/rooms/library | EDIT | NOT YET — queued after the six |
| Project Intelligence | nayanet.live/pi | EDIT | NOT YET — queued after the six |
| Projects | nayanet.live/projects | REDO — compose the one true page from harvested parts | NOT YET — queued after the six |
| Welcome | nayanet.live/welcome (+ /world/*) | EDIT | NOT YET — queued after the six |
| Smart Notes | nayanet.live/s/<id> (+ Smart Feed) | EDIT | NOT YET — queued after the six |
| Smart Factory | nayanet.live/smartfactory | EDIT | NOT YET — queued after the six |
| Certificate / Identity | section inside Personal Settings | EDIT | NOT YET — queued after the six |
| Pricing | nayanet.live/pricing | EDIT | NOT YET — queued after the six |
| Ask Naya | Hub Ask surface (nayanet.live) | EDIT | NOT YET — queued after the six |
| Booking | nayanet.live/book | EDIT | NOT YET — queued after the six |
| Smart Meet | no surface yet — to build | BUILD FRESH — after settled C1 | NOT YET — queued after the six |

## Not pages (no page rollout)

- **Smart Match** — system, no page (engine) — not a page rollout item; the ONE auto-match algorithm.
- **Smart Search** — universal capability, NOT an app (Shawn 2026-10-30) — search-the-network rides on every page with the pieces.

## Collision rules (hard, verified this pass)

- **HUB/app/index.html — DO NOT EDIT.** Hub board owned by the v5 team (agent 3cf0b8cc, branch `hub-board-black-live-20261105`, remote branch verified present 2026-11-06). This role only read the harvested copy (`harvested/hub.html`). Local `HUB/app/index.html` mtime 2026-11-04 21:36, untouched; repo `git status` clean of this role’s work.
- **DASHBOARD/index-reporting-pass1-20261105.html — DO NOT TOUCH while its v7 Builder runs.** File at `~/workspace/team-nitro/dashboard/index-reporting-pass1-20261105.html`, mtime 2026-11-06 00:16Z. Rollout edits to the Dashboard happen AFTER the v7 Builder lands — coordinate, never collide, never touch the same file at the same time.
- **Inventory work is read-only on live files.** It harvests from the pages and places pieces in the Factory; it never edits a live page.

## Rollout groups (pieces)

- **Group 1 — prove on Dashboard (12):** 01, 05, 06, 11, 12, 13, 16, 18, 19, 20, 21, 22 — the instrument set (gauge family, orb, chart) + the Dashboard’s controls (button, tabs, Smart Link, controls).
- **Group 2 — prove on Personal (6):** 02, 03, 04, 10, 14, 17 — the world set (board, grand block, icon, jewel, header, well).
- **Group 3 — shared (4):** 07, 08, 09, 15 — architecture + shared chrome, proved on Dashboard + Personal, then everywhere.

## Sources

- Page list + work types: `~/workspace/project-intelligence/alignment-master-26-apps-20261030.md` §6 (25 pages), §7 (EDIT 20 / BUILD FRESH 2 / REDO 2 / REPLACE 1), §8 (lanes).
- Order: Shawn 2026-11-06 00:31Z (Dashboard, Personal, then the rest).
- Pieces + craft: `signature-pieces/*.html`, `INVENTORY.md`, `inventory.json` (this Factory).
- Canonical repo home: `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/` (live on GitHub main).
