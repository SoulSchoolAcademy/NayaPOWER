# BRIEF — Membership page (2026-11-21)

**Seat:** maker (coordinator-built, single seat — coordinator at depth 2 cannot spawn).
**Report to:** the captain. NOT to Shawn.
**Shawn's order, today:** "get working on the membership page. It is simple — just another frame, with the COVER in the frame." The old membership fix-8 page goes away — do NOT deliver its link, do NOT build on it.

## LAWS (read first, named in this brief)
- `THE-NAYA-DESIGN-LAWS.md` FIRST — THE RULE BOOK. Then `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-ULTIMATE-ORIENTATION.md`, `THE-SET-ORIENTATION.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md`, `THE-HEART-OF-THE-MACHINE.md`, `THE-OFFICIAL-PARTS.md`, `THE-ARMY-TRAINING.md`.
- **One-Build Law:** frame code byte-identical to the frame source; no new layout, no additions beyond this brief, no redesign. Harvest first, compose never create.
- **Eleven Laws** (his eye is the verdict; one bar the same everywhere; never guess a destination).
- **Inventory Law** — every harvested piece named with its source.

All docs under `~/workspace/team-nitro/`.

## THE PAGE
A membership page in the current system (like the Personal page), built from the frame that works + the real frames under the One-Build Law.

**HARVEST FIRST (done — see HARVEST-MANIFEST.md):** no membership page home exists in the current system (main tree, 16,737 entries, zero `TEAM-NITRO/membership*` paths). Build from the frame source.

**Frame source:** `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html`, blob `1f0b0474` (142,532 B) — the frame that works.
**Cover model:** Personal page, `personal/complete-round4-20261120`, blob `65d2d314`, file `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html` — the `.sa-cover` board.
**Course data (DATA ONLY — no markup/layout/behaviour):** membership-complete blob `4e1e470a` — Academy (5 lessons, YouTube IDs on file), AI Masterclass (no lessons on file — honest empty room), Fast Action Club (9 lessons, full layers).
**Pull file bytes via the git blob API only** — repo `SoulSchoolAcademy/NayaPOWER`, helper `~/workspace/team-nitro/gh-direct.py` (mints the app JWT + installation token in memory; never write tokens to disk/logs). The local repo copy `~/workspace/nayapower-repo` is STALE — do not use it. Contents API returns EMPTY content for files over 1 MB — use the git blob API. Pipe base64 straight into the API call, never stage multi-MB payloads to disk.

**Branch:** `membership/page-20261121`. **Lane:** `~/workspace/team-nitro/membership/page-20261121/`.

## THE STRUCTURE (settled by Shawn 2026-11-21 ~10:00 MST — replaces the looser "cover → click in" flow)
The entrance is TWO frames, for EVERY course:
1. **FIRST:** the cover to the course, with a button. Click it, boom, they enter. The cover introduces the course.
2. **SECOND:** a frame holding the buttons for ALL the lessons — the table of contents. How many lessons there are is how many buttons are on that second frame. Click a lesson's button → that lesson's frame-by-frame starts.
3. **NO links below** — nothing below the table of contents.

The page cover (beat 0) shows the three courses like landing on a Personal page. Click a course → its cover → click in → the table of contents → click a lesson → the lesson unfolds frame by frame.

**Toggle:** MIXED (images + videos + text — the full deal, the DEFAULT), or ALL VIDEO, or ALL AUDIO. There is NO all-text view.

## OUT OF SCOPE
- Login/feature-page wiring (follows after Personal is unfrozen).
- Payments (ladder is context only: Power $25 = 10 sites · Pro $50 = 100 · Max $100 = unlimited; owner pastes their own PayPal link).
- No bottom bar added (the frame carries none; the Eleven Laws law-3 one-bar question is the captain's call).

## ACCEPTANCE (all proven before reporting)
1. **Byte diff** (`verify-byte-diff.js`): frame code identical to blob `1f0b0474` except the documented word adaptations (5 lines, listed in `frame-adaptations.json`).
2. **Static audit** (`audit-static.js`): 90 beats; TOC buttons 5 + 0 + 9; zero `<a>` tags; every `data-mem-go` in range; mode sets correct per lesson.
3. **Design-laws check** (`check-design-laws.py`): delta 0 vs the frame source (1 pre-existing comment false positive, identical in both).
4. **Render, phone 390 AND desktop 1440** (`render-probe.py`): load + full click-walk (cover → course cover → TOC → lesson cover → Begin → watch → toggle ALL VIDEO / ALL AUDIO → Lessons → TOC), zero JS errors, zero failed requests to the page's own host, no horizontal overflow.
5. **Staged link verified first-hand** (HTTP 200 + size/sha match) before reporting.
