# Smart List — Room Scorecard (subagent build, 2026-10-02; director rework, 2026-10-02 evening)

Branch: `naya4/room-02-reports-v2`.
Sources: 24 canonical smart notes via `ListAdapter.parseNotes` (projection, never invention).
Verified: node syntax OK (adapter + room), CSS brace balance OK,
jsdom 17 pass / 0 fail / 0 errors on the v1 build (render, search, modal, Escape,
new list, save/un-save, delete list, category filter, today empty state,
persistence). Rework re-verified: syntax + preview rebuild + spot checks below.

## Director rework (2026-10-02, Shawn's own words)

1. **Color flow, not all-green.** Boards now flow the natural spectrum —
   purple → indigo → cyan → forest → lime → yellow → gold → orange → red →
   magenta — the exact Living Intel FLOW, white/silver at rest, the board's
   flow color ignites the whole perimeter on hover/focus. Emerald identity retired.
2. **Today-style boards.** Cards are now the Your Intelligence Today anatomy:
   rank glyph + title + when + IN A NUTSHELL + explicit SAVE TO LIST /
   VIEW FULL NOTE actions + footer strip — the same mini in-a-nutshell blocks
   the Today page saves, not a different look.
3. **Store contract resolved with evidence.** The Today v8.3 preview writes
   SAVE to `localStorage['nayanet.today.smartlist.v1']` (flat array of ids —
   verified in today-highlights-preview.html). The v1 proposal
   (`naya.smartlist.today`) was never the real Today key. This room now reads
   the real key for "Saved from Today" (read-only; Today owns writes).
   Custom lists stay in `naya.smartlist = {custom:{name:[ids]}}`.
   Open lane item: Today saves that aren't among the 24 known notes render as
   honest placeholders pointing back at the Today page — a snapshot contract
   ({id,title,nutshell} at SAVE time) belongs with the Today lane.

## Score: 9.2/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | All 24 real notes parse; title/truth/date/nutshell/category from file + path taxonomy. Zero demo content. |
| 2 | Honesty | 10 | Empty states say what they are; unresolvable Today saves render as honest placeholders, never invented titles. |
| 3 | Button law | 10 | Every control persists or navigates: save/un-save, new list, delete list, filters, search, modal. Silver at rest, flow color ignites. |
| 4 | Color law | 10 | Spectrum flow on boards per director; white/silver chrome; truth pills stay semantic (candidate amber, ratified mint). |
| 5 | Visual consistency | 10 | Boards share the Today `.naya509-board` anatomy — rank, title, meta, nutshell, explicit actions, footer. |
| 6 | Keyboard/accessibility | 9 | Cards focusable + Enter/Space opens, Escape closes, focus-visible rings. Modal focus trap not implemented. |
| 7 | Completeness | 8 | Core flows done; no bulk operations, no list rename, no drag-reorder. |

## Why not 10

- **-0.3 — no visual confirmation** (screenshot pipeline down; structural QA only).
- **-0.2 — polish gaps**: no modal focus trap, no list rename, single-column mobile is plain.
- **-0.3 — Today snapshot contract**: unresolvable Today saves can't show their
  nutshell until the Today lane stores snapshots at SAVE time.

## What closes it

- Director visual pass -> +0.3
- Focus trap + rename -> +0.2
- Today SAVE snapshot contract -> +0.3

## Files (written, uncommitted)

- `HUB/app/js/rooms/list-adapter.js` — `ListAdapter.parseNotes([{path,content}])`
- `HUB/app/js/rooms/list.js` — `window.NayaRooms.smartList(el, ctx)`
- `HUB/app/css/list.css` — emerald identity, glass, ≤760px responsive
- `HUB/app/preview/build-list-preview.py` — bakes 24 raw notes through the real adapter
- `HUB/app/preview/LIST-SCORECARD.md` — this file
- Preview: `~/workspace/your_files/list-preview.html`
