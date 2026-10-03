# Smart List — Room Scorecard (subagent build, 2026-10-02; director reworks, 2026-10-02 evening)

Branch: `naya4/room-02-reports-v2`.
Sources: 24 canonical smart notes via `ListAdapter.parseNotes` (projection, never invention).
Verified: node syntax OK (adapter + room), CSS brace balance OK,
36-check smoke suite green (header layout, conditional lists row, category
toggle, clear-filter chip, per-category tab colors, spectrum order, Today
board anatomy, search, modal + flow color, picker input focus, focus trap,
save flow, list create/delete, Today-key read, honest placeholders).
Preview rebuilt.

## Director rework v4 — composition, pro level (2026-10-02, Shawn's verdict)

His verdict on v3's top, from his screenshot: the ALL NOTES / SAVED FROM
TODAY tabs "look out of place... not clean and nice and pro level," ALL
NOTES "lit all the time" against unlit siblings "looks weird," and
+ NEW LIST floated mid-row instead of owning the corner. Composition was a
6/10 — the call was fair.

1. **+ NEW LIST in the true top-right corner.** The header is now a flex
   row: title block left, + NEW LIST top-right. It no longer lives in the
   tab area at all.
2. **View tabs deleted.** No ALL NOTES, no permanent SAVED FROM TODAY.
   The default view IS all notes; category tabs toggle on/off, so nothing
   sits lit by default and a lit tab always means something.
3. **Lists row earns its space.** It renders only when something exists:
   SAVED FROM TODAY appears as a system tab only when Today saves are
   non-empty (it "didn't make sense" as a permanent empty tab); custom
   lists appear once created. No placeholder noise, ever.
4. **Clear-filter chip.** When a category, list, or search is active, the
   toolbar shows × CLEAR next to the count — the toggle is discoverable.
5. **Categories stay one level**, white at rest, each igniting in its own
   spectrum color on hover/select.

## Score: 9.4/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | All 24 real notes parse; zero demo content. |
| 2 | Honesty | 10 | Empty states honest; unresolvable Today saves are placeholders, never invented. |
| 3 | Button law | 10 | Every control persists/navigates; silver at rest, own color ignites. |
| 4 | Color law | 10 | Spectrum flow on boards AND category tabs per director; white/silver chrome. |
| 5 | Visual consistency | 9 | Today board anatomy; two-row tabs max, header action top-right, per director. |
| 6 | Keyboard/accessibility | 10 | Focusable boards, Enter/Space opens, Escape closes, focus trap, picker focuses its input. |
| 7 | Composition (clean / organized / pro feel) | 9 | The dimension Shawn is judging: nothing lit without meaning, no dead tabs, action in the corner. |
| 8 | Completeness | 8 | Core flows done; no bulk operations, no list rename, no drag-reorder. |

## Why not 10

- **-0.3 — no visual confirmation** (screenshot pipeline down; structural QA only — director's eyes are the pass).
- **-0.2 — completeness gaps**: no bulk operations, no list rename, no drag-reorder.
- **-0.1 — composition needs his eyes**: the top now follows every rule he gave; the last point is whether it *feels* pro to him.

## What closes it

- Director visual pass on the new top -> +0.3
- Today SAVE snapshot contract (Today lane) -> +0.3
- Bulk ops / rename / reorder -> +0.2 (beyond the 10 bar for this pass)

## Files (written, uncommitted)

- `HUB/app/js/rooms/list-adapter.js` — `ListAdapter.parseNotes([{path,content}])`
- `HUB/app/js/rooms/list.js` — `window.NayaRooms.smartList(el, ctx)`
- `HUB/app/css/list.css` — emerald identity, glass, ≤760px responsive
- `HUB/app/preview/build-list-preview.py` — bakes 24 raw notes through the real adapter
- `HUB/app/preview/LIST-SCORECARD.md` — this file
- Preview: `~/workspace/your_files/list-preview.html`
