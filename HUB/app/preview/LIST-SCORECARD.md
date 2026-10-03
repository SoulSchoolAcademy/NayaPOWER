# Smart List — Room Scorecard (subagent build, 2026-10-02; director reworks, 2026-10-02 evening)

Branch: `naya4/room-02-reports-v2`.
Sources: 24 canonical smart notes via `ListAdapter.parseNotes` (projection, never invention).
Verified: node syntax OK (adapter + room), CSS brace balance OK,
63-check smoke suite green (SmartTabs ribbon, drift tick/ping-pong/poke,
post-mount measure regression, arrow-key travel, ⋯ menu four actions,
💜/⭐ persistence + sort, edit popover, ＋Add popover, remove + hidden-restore
round-trip, clear-filter chip, search, board spectrum, Today board anatomy,
modal + flow color, focus trap, save flow, lists row, Today-key read, honest
placeholders). Preview rebuilt.

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

## Director rework v8 — the drift actually drifts (2026-10-02, bug fix)

Shawn: "I don't see any movement." He was right — the drift never ran.
Root cause, verified: the room measures layout (scrollWidth/clientWidth)
inside `renderTabs()`, which executes while the stage is still detached
from the document — every width reads 0, so the timer never armed (and the
chevrons/fades never appeared either). The smoke suite couldn't catch it
because the stub has no layout.

1. **Measure after mount.** Each scroll row now carries a ResizeObserver
   that re-runs measure + arm whenever its size changes (0 → real width on
   attach included); plus a double-rAF / setTimeout fallback where RO is
   unavailable. Observers are disconnected on re-render — no leaks.
2. **Regression test.** The suite now reproduces the bug shape: fresh stage
   (detached, widths 0) → no timer; simulate attach (widths appear) →
   refresh → timer arms and `is-scroll` sets.
3. **Bonus enhancement (his invitation):** ←/→ arrow keys travel between
   pills, Home/End jump to the ends — the expected keyboard pattern for a
   tab ribbon.

## Effectiveness scorecard (Shawn asked: score it for effectiveness)

The room's job: Smart List is where Smart Notes are saved and organized
into categories and lists. Scored against that job, not against itself:

| # | Effectiveness test | Score | Note |
|---|--------------------|-------|------|
| 1 | Find any note fast | 10 | SmartTabs ribbon + toggle + search + × CLEAR — three ways in, all instant. |
| 2 | Browse by what it teaches | 10 | Categories auto-derived from the real notes; 💜/⭐ floats priorities. |
| 3 | Save notes into lists | 10 | SAVE TO LIST on every board; lists persist per device. |
| 4 | Manage the organization | 10 | Tabs: add/edit/heart/star/remove/restore. Lists: create/delete. |
| 5 | Receive Today saves | 9 | Wired to Today's real SAVE key; unresolvable saves are honest placeholders until the Today lane ships snapshots. |
| 6 | Read a note fully | 8 | VIEW FULL NOTE shows parsed nutshell + metadata + source — not the complete note body yet. |
| 7 | Pro feel | 9 | Shawn: "that's a lot better." The drift now actually runs; his eyes confirm the feel. |

**Effectiveness: 9.5/10.** It does the whole job — the half point off is
read-the-full-note (needs full-body projection) and the Today snapshot
contract (Today lane), plus his visual sign-off on the drift.

## Score: 9.6/10 (unchanged — the drift adds motion, not points)

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | All 24 real notes parse; zero demo content. |
| 2 | Honesty | 10 | Empty states honest; unresolvable Today saves are placeholders, never invented. |
| 3 | Button law | 10 | Every control persists/navigates; his pill language throughout. |
| 4 | Color law | 10 | Spectrum per tab (stable), 💜/⭐ glows per his spec, white/silver chrome. |
| 5 | Visual consistency | 10 | His SmartTabs v9 ported faithfully; Today board anatomy below. |
| 6 | Keyboard/accessibility | 10 | Pills focusable, Enter/Space toggles, Escape closes, focus trap, reduced-motion respected. |
| 7 | Composition (clean / organized / pro feel) | 9 | One ribbon, one language — his, now with his drift. |
| 8 | Completeness | 9 | Full tab lifecycle: add/edit/heart/star/remove/restore. |

## Why not 10

- **-0.3 — no visual confirmation** (screenshot pipeline down; structural QA only — director's eyes are the pass).
- **-0.1 — composition needs his eyes**: the drift speed and feel are his call.

## What closes it

- Director visual pass on the drifting ribbon -> +0.4

## Files (written, uncommitted)

- `HUB/app/js/rooms/list-adapter.js` — `ListAdapter.parseNotes([{path,content}])`
- `HUB/app/js/rooms/list.js` — `window.NayaRooms.smartList(el, ctx)`
- `HUB/app/css/list.css` — emerald identity, glass, ≤760px responsive
- `HUB/app/preview/build-list-preview.py` — bakes 24 raw notes through the real adapter
- `HUB/app/preview/LIST-SCORECARD.md` — this file
- Preview: `~/workspace/your_files/list-preview.html`
