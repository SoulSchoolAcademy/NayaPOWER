# Smart List — Room Scorecard (subagent build, 2026-10-02; director reworks, 2026-10-02 evening)

Branch: `naya4/room-02-reports-v2`.
Sources: 24 canonical smart notes via `ListAdapter.parseNotes` (projection, never invention).
Verified: node syntax OK (adapter + room), CSS brace balance OK,
53-check smoke suite green (header layout, scrolling bar structure, chevrons,
category toggle, clear-filter chip, manage tabs rename/add/delete/hide/restore,
per-category tab colors, spectrum order, Today board anatomy, search, modal +
flow color, picker input focus, focus trap, save flow, list create/delete,
Today-key read, honest placeholders). Preview rebuilt.

## Director rework v5 — the scrolling tab bar (2026-10-02, Shawn's words)

His verdict on v4: "definitely better, but some of those buttons go right
off the page, it doesn't look right." His prescription: a proper scrolling
presentation — tabs scroll across deliberately — plus the ability to edit
each tab, add new ones, delete them. He'll upload his own smart-tabs list
to become the canonical tabs.

1. **A real scrolling bar.** The category row is now a scroll container with
   edge fade masks and ‹ › chevron buttons that appear only when content
   actually overflows — buttons glide under a fade instead of clipping
   mid-button at the page edge. Same treatment for the lists row.
2. **Manage tabs.** A ⚙ TABS button at the bar's end opens a manager:
   rename any tab inline, hide a derived tab (its notes stay under All;
   restorable from a Hidden section), delete a custom tab, add new tabs.
   All persisted in `naya.smartlist.cats` — notes themselves are never
   touched. Ready for his uploaded tab list to become canonical.
3. Everything else from v4 stands: + NEW LIST top-right, no view tabs,
   toggle categories, conditional lists row, × CLEAR chip.

## Score: 9.5/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | All 24 real notes parse; zero demo content. |
| 2 | Honesty | 10 | Empty states honest; unresolvable Today saves are placeholders, never invented. |
| 3 | Button law | 10 | Every control persists/navigates; silver at rest, own color ignites. |
| 4 | Color law | 10 | Spectrum flow on boards AND category tabs per director; white/silver chrome. |
| 5 | Visual consistency | 10 | Today board anatomy; scrolling tab bar with fades + chevrons, per director. |
| 6 | Keyboard/accessibility | 10 | Focusable boards, Enter/Space opens, Escape closes, focus trap, picker focuses its input. |
| 7 | Composition (clean / organized / pro feel) | 9 | Scrolling bar reads intentional; manage-tabs is one quiet gear button. |
| 8 | Completeness | 9 | Tabs fully manageable (add/rename/hide/restore); no bulk ops on notes, no drag-reorder. |

## Why not 10

- **-0.3 — no visual confirmation** (screenshot pipeline down; structural QA only — director's eyes are the pass).
- **-0.1 — composition needs his eyes**: the scroll behavior (fades, chevrons) can only be truly judged in a live browser.
- **-0.1 — his tab list not yet wired**: the canonical tabs await his upload.

## What closes it

- Director visual pass on the scrolling bar -> +0.3
- His smart-tabs upload wired in -> +0.1
- Today SAVE snapshot contract (Today lane) -> +0.1

## Files (written, uncommitted)

- `HUB/app/js/rooms/list-adapter.js` — `ListAdapter.parseNotes([{path,content}])`
- `HUB/app/js/rooms/list.js` — `window.NayaRooms.smartList(el, ctx)`
- `HUB/app/css/list.css` — emerald identity, glass, ≤760px responsive
- `HUB/app/preview/build-list-preview.py` — bakes 24 raw notes through the real adapter
- `HUB/app/preview/LIST-SCORECARD.md` — this file
- Preview: `~/workspace/your_files/list-preview.html`
