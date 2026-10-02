# Smart List — Room Scorecard (subagent build, 2026-10-02)

Branch: `naya4/room-02-reports-v2` (files written, NOT committed — parent reviews/pushes).
Sources: 24 canonical smart notes via `ListAdapter.parseNotes` (projection, never invention).
Verified: node syntax OK (adapter + room), CSS brace balance OK,
jsdom 17 pass / 0 fail / 0 errors (render, search, modal, Escape, new list,
save/un-save, delete list, category filter, today empty state, persistence).

## Score: 8.8/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | All 24 real notes parse; title/truth/date/nutshell/category from file + path taxonomy. Zero demo content. |
| 2 | Honesty | 10 | Empty states say what they are; "Saved from Today" is empty until Today writes. |
| 3 | Button law | 10 | Every control persists or navigates: save/un-save, new list, delete list, filters, search, modal. Silver at rest, emerald ignite. |
| 4 | Color law | 10 | Emerald is the room's stable identity; truth pills use semantic color (candidate amber, ratified emerald). |
| 5 | Keyboard/accessibility | 9 | Cards focusable + Enter opens, Escape closes, focus-visible rings. Modal focus trap not implemented. |
| 6 | Completeness | 8 | Core flows done; no bulk operations, no list rename, no drag-reorder. |

## Why not 10

- **-0.7 — Today SAVE contract unverified.** The Today room lives on branch
  `naya4/room-01-main-stage-v2`; its SAVE localStorage key could not be found
  in this branch. This room proposes the shared contract
  `localStorage['naya.smartlist'] = {custom:{name:[ids]}, today:[...]}` and
  reads `today` defensively (note ids OR {title,nutshell} objects). Until the
  Today room adopts the same key, "Saved from Today" stays empty in production.
- **-0.3 — no visual confirmation** (screenshot pipeline down; structural QA only).
- **-0.2 — polish gaps**: no modal focus trap, no list rename, single-column mobile is plain.

## What closes it

- Today room writes to `naya.smartlist.today` (same key/shape) -> +0.7
- Director visual pass -> +0.3
- Focus trap + rename -> +0.2

## Files (written, uncommitted)

- `HUB/app/js/rooms/list-adapter.js` — `ListAdapter.parseNotes([{path,content}])`
- `HUB/app/js/rooms/list.js` — `window.NayaRooms.smartList(el, ctx)`
- `HUB/app/css/list.css` — emerald identity, glass, ≤760px responsive
- `HUB/app/preview/build-list-preview.py` — bakes 24 raw notes through the real adapter
- `HUB/app/preview/LIST-SCORECARD.md` — this file
- Preview: `~/workspace/your_files/list-preview.html`
