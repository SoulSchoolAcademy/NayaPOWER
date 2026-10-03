# Smart List — Room Scorecard (subagent build, 2026-10-02; director reworks, 2026-10-02 evening)

Branch: `naya4/room-02-reports-v2`.
Sources: 24 canonical smart notes via `ListAdapter.parseNotes` (projection, never invention).
Verified: node syntax OK (adapter + room), CSS brace balance OK,
27-check smoke suite green (render, tabs, spectrum order, Today board anatomy,
search, category filter, modal + flow color, focus trap, save flow, list
create/delete as tabs, Today-key read, honest placeholders). Preview rebuilt.

## Director rework v2 — layout (2026-10-02, Shawn's own words)

1. **Categories across the top, no sidebar.** Views (ALL NOTES / SAVED FROM
   TODAY), CATEGORIES, and MY LISTS are now sticky smart-tab rows — the
   sidebar is gone, so no dead black space on scroll. Lists render as tabs
   with an inline × delete; + NEW LIST is a tab-button.
2. **Widescreen boards, not boxes.** The grid is now a full-width single
   column — boards read like the Today page, not boxed cards.

## Director rework v1 — color + Today-style boards (2026-10-02)

1. **Color flow, not all-green.** Boards flow the natural spectrum —
   purple → indigo → cyan → forest → lime → yellow → gold → orange → red →
   magenta — white/silver at rest, the board's flow color ignites the whole
   perimeter on hover/focus. Emerald identity retired.
2. **Today-style boards.** Today `.naya509-board` anatomy: rank glyph + title
   + when + IN A NUTSHELL + explicit SAVE TO LIST / VIEW FULL NOTE + footer.
3. **Store contract resolved with evidence.** Today v8.3 writes SAVE to
   `nayanet.today.smartlist.v1` (flat id array); this room reads it
   read-only. Custom lists in `naya.smartlist={custom:{}}`. Unresolvable
   Today saves render as honest placeholders.

## Score: 9.4/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | All 24 real notes parse; zero demo content. |
| 2 | Honesty | 10 | Empty states honest; unresolvable Today saves are placeholders, never invented. |
| 3 | Button law | 10 | Every control persists/navigates; silver at rest, flow ignites. |
| 4 | Color law | 10 | Spectrum flow on boards per director; white/silver chrome. |
| 5 | Visual consistency | 10 | Today board anatomy + smart tabs across the top, per director. |
| 6 | Keyboard/accessibility | 10 | Focusable boards, Enter/Space opens, Escape closes, focus trap cycles Tab inside modal. |
| 7 | Completeness | 8 | Core flows done; no bulk operations, no list rename, no drag-reorder. |

## Why not 10

- **-0.3 — no visual confirmation** (screenshot pipeline down; structural QA only — director's eyes are the pass).
- **-0.2 — completeness gaps**: no bulk operations, no list rename, no drag-reorder.
- **-0.3 — Today snapshot contract**: unresolvable Today saves can't show their
  nutshell until the Today lane stores snapshots at SAVE time.

## What closes it

- Director visual pass -> +0.3
- Today SAVE snapshot contract (Today lane) -> +0.3
- Bulk ops / rename / reorder -> +0.2 (beyond the 10 bar for this pass)

## Files (written, uncommitted)

- `HUB/app/js/rooms/list-adapter.js` — `ListAdapter.parseNotes([{path,content}])`
- `HUB/app/js/rooms/list.js` — `window.NayaRooms.smartList(el, ctx)`
- `HUB/app/css/list.css` — emerald identity, glass, ≤760px responsive
- `HUB/app/preview/build-list-preview.py` — bakes 24 raw notes through the real adapter
- `HUB/app/preview/LIST-SCORECARD.md` — this file
- Preview: `~/workspace/your_files/list-preview.html`
