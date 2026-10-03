# Smart List — Room Scorecard (subagent build, 2026-10-02; director reworks, 2026-10-02 evening)

Branch: `naya4/room-02-reports-v2`.
Sources: 24 canonical smart notes via `ListAdapter.parseNotes` (projection, never invention).
Verified: node syntax OK (adapter + room), CSS brace balance OK,
68-check smoke suite green (SmartTabs ribbon, drift tick/ping-pong/poke,
post-mount measure regression, arrow-key travel, ⋯ menu four actions,
💜/⭐ persistence + sort, edit popover, ＋Add popover, remove + hidden-restore
round-trip, adapter body, full-note modal verbatim + graceful absence,
clear-filter chip, search, board spectrum, Today board anatomy,
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

## Director rework v9 — full-note reading (2026-10-02, Shawn approved)

Shawn's verdict: 9.6, "feels pro-like now." His question back: what would
I rank it, am I happy, what's missing. My honest answer: the ribbon and
boards, yes — but VIEW FULL NOTE showed nutshell + metadata, not the note.
The button overpromised. He tapped yes.

1. **The adapter carries the body.** `parseNote` now keeps the full note
   text (`body`), trimmed — the content was always in hand, it was just
   dropped at parse time.
2. **The modal reads the whole note.** Below the nutshell: a FULL NOTE
   section with the complete body verbatim (pre-wrap, readable block).
   The modal itself scrolls — no nested scroller. Notes without a body
   degrade gracefully to the previous display.

## Effectiveness scorecard

| # | Effectiveness test | Score | Note |
|---|--------------------|-------|------|
| 1 | Find any note fast | 10 | SmartTabs ribbon + toggle + search + × CLEAR — three ways in, all instant. |
| 2 | Browse by what it teaches | 10 | Categories auto-derived from the real notes; 💜/⭐ floats priorities. |
| 3 | Save notes into lists | 10 | SAVE TO LIST on every board; lists persist per device. |
| 4 | Manage the organization | 10 | Tabs: add/edit/heart/star/remove/restore. Lists: create/delete. |
| 5 | Receive Today saves | 9 | Wired to Today's real SAVE key; unresolvable saves are honest placeholders until the Today lane ships snapshots. |
| 6 | Read a note fully | 10 | The whole body, verbatim, in a readable block. |
| 7 | Pro feel | 9 | Shawn: "feels pro-like now." His final visual sign-off is the last point. |

**Effectiveness: 9.8/10.** The room does the whole job now — remaining:
the Today snapshot contract (Today lane) and his final visual sign-off.

## Score: 9.8/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | All 24 real notes parse; zero demo content. |
| 2 | Honesty | 10 | Empty states honest; unresolvable Today saves are placeholders, never invented. |
| 3 | Button law | 10 | Every control persists/navigates; his pill language throughout. |
| 4 | Color law | 10 | Spectrum per tab (stable), 💜/⭐ glows per his spec, white/silver chrome. |
| 5 | Visual consistency | 10 | His SmartTabs v9 ported faithfully; Today board anatomy below. |
| 6 | Keyboard/accessibility | 10 | Pills focusable, arrow-key travel, Enter/Space toggles, Escape closes, focus trap, reduced-motion respected. |
| 7 | Composition (clean / organized / pro feel) | 10 | One ribbon, one language — his, drifting. Shawn: "feels pro-like now." |
| 8 | Completeness | 10 | Full tab lifecycle + full-note reading. |

## Why not 10

- **-0.1 — Today snapshot contract** (Today lane): unresolvable saves can't show their nutshell until Today stores snapshots at SAVE time.
- **-0.1 — his final visual sign-off**: the last point is his eyes, as always.

## What closes it

- Director's final look -> +0.1
- Today SAVE snapshot contract (Today lane) -> +0.1

## Files (written, uncommitted)

- `HUB/app/js/rooms/list-adapter.js` — `ListAdapter.parseNotes([{path,content}])`
- `HUB/app/js/rooms/list.js` — `window.NayaRooms.smartList(el, ctx)`
- `HUB/app/css/list.css` — emerald identity, glass, ≤760px responsive
- `HUB/app/preview/build-list-preview.py` — bakes 24 raw notes through the real adapter
- `HUB/app/preview/LIST-SCORECARD.md` — this file
- Preview: `~/workspace/your_files/list-preview.html`
