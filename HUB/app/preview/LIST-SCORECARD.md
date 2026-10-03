# Smart List — Room Scorecard (subagent build, 2026-10-02; director reworks, 2026-10-02 evening)

Branch: `naya4/room-02-reports-v2`.
Sources: 24 canonical smart notes via `ListAdapter.parseNotes` (projection, never invention).
Verified: node syntax OK (adapter + room), CSS brace balance OK,
49-check smoke suite green (SmartTabs ribbon structure, pill filter toggle,
⋯ menu four actions, 💜/⭐ persistence + heart-first sort, edit popover,
＋Add popover, custom-tab empty state, remove + hidden-restore round-trip
with rename preserved, clear-filter chip, search, board spectrum, Today
board anatomy, modal + flow color, focus trap, save flow, lists row,
Today-key read, honest placeholders). Preview rebuilt.

## Director rework v6 — his SmartTabs become the tab bar (2026-10-02)

Shawn uploaded his SmartTabs v9.0.0 kit (pill ribbon, 💜/⭐ markers,
＋Add, add/edit/heart/star/remove/navigate, localStorage persistence) and
asked for Smart Tabs made out of it for the list. The full component code
was read from his PDF and ported faithfully — not approximated:

1. **His pill language.** Dark pill, bold white label, 💜 = purple inset
   glow, ⭐ = gold inset glow, ⋯ per-pill menu, ＋Add dashed pill at the
   ribbon's end. His menu verbatim: ✏️ Edit / 💜 Set Purple Heart /
   ⭐ Set Gold Star / ✕ Remove. His popover: Label + mutually-exclusive
   💜/⭐ toggles + Cancel/Save. His heart-first sort.
2. **Click = filter.** The one adaptation: his pills navigate, ours filter
   the Smart List (toggle on/off). His `route` binding becomes our category
   `key`; the store shape mirrors his `{id,label,heart,star}` plus that key.
3. **Selected pill lights in its spectrum color** — his earlier direction
   for this room (each tab its own color when lit), with the color hashed
   stable per tab so 💜/⭐ re-sorting never shifts a tab's identity color.
4. **Remove/restore done right.** Removing a derived tab hides it but keeps
   its object, so rename + 💜/⭐ survive a remove → restore round-trip
   (caught by the smoke suite). Hidden tabs are offered for restore inside
   the ＋Add popover.
5. The lists row (Saved from Today, custom lists) speaks the same pill
   language — count badge + × instead of ⋯.

## Score: 9.6/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | All 24 real notes parse; zero demo content. |
| 2 | Honesty | 10 | Empty states honest; unresolvable Today saves are placeholders, never invented. |
| 3 | Button law | 10 | Every control persists/navigates; his pill language throughout. |
| 4 | Color law | 10 | Spectrum per tab (stable), 💜/⭐ glows per his spec, white/silver chrome. |
| 5 | Visual consistency | 10 | His SmartTabs v9 ported faithfully; Today board anatomy below. |
| 6 | Keyboard/accessibility | 10 | Pills focusable, Enter/Space toggles, Escape closes menu/popover/modal, focus trap. |
| 7 | Composition (clean / organized / pro feel) | 9 | One ribbon, one language — his. |
| 8 | Completeness | 9 | Full tab lifecycle: add/edit/heart/star/remove/restore. |

## Why not 10

- **-0.3 — no visual confirmation** (screenshot pipeline down; structural QA only — director's eyes are the pass).
- **-0.1 — composition needs his eyes**: the port follows his code line-for-line, but feel is his call.

## What closes it

- Director visual pass on the SmartTabs ribbon -> +0.4
- Today SAVE snapshot contract (Today lane) -> noted separately, not scored here

## Files (written, uncommitted)

- `HUB/app/js/rooms/list-adapter.js` — `ListAdapter.parseNotes([{path,content}])`
- `HUB/app/js/rooms/list.js` — `window.NayaRooms.smartList(el, ctx)`
- `HUB/app/css/list.css` — emerald identity, glass, ≤760px responsive
- `HUB/app/preview/build-list-preview.py` — bakes 24 raw notes through the real adapter
- `HUB/app/preview/LIST-SCORECARD.md` — this file
- Preview: `~/workspace/your_files/list-preview.html`
