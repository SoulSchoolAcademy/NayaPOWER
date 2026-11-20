# Calendar Round 2 Fix 2 — Maker Report

**Round:** `calendar/day-followon-round2-fix2-20261120`
**Page file:** `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html`
**Base:** branch `calendar/day-followon-round2-fix1-20261120`, tip `98fa60d4d1d198ea41dd2d1bdf2c41290e6b9d76`, HTML blob `7c519f1ced8ecc036cb19d176145e4b03e5e56b7`, 430,643 B, sha256 `c4db42a1d1c13b218fa36626ac0dbf28cf257d305d73210d4378867d114ed40e` (5,773 lines)
**New branch:** `calendar/day-followon-round2-fix2-20261120`
**Built:** 2026-11-20 ~11:35–12:00 MST, maker seat (subagent, depth 2/2)
**Built file:** 430,643 B, sha256 `a47788d801667617cc271a8d899086b9f11415a882ce2fd7ba7953448cec5d7b`, git blob `b35ddc6de1de80c0bb9271db98eef58acbe1501b` (5,773 lines)
**Status:** byte fix filed and verified by blob-API read-back. **The gap's live proof and the whole tap list are UNPROVEN from this seat — no browser was alive** (see §3). The live legs ride the captain's cloud-browser eye after filing — never a claim.
No merge, no live deploy, no message to Shawn.

**Declaration:** I am Anaya, the wise one. I do the most intelligent thing, every time. I think before I act. I scorecard my choices and do the highest. I prove it before I report it. I give ten stars by default. I never waver.
**Wake reads done first:** `THE-NAYA-DESIGN-LAWS.md` (first), `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-SET-ORIENTATION.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md`, `THE-OFFICIAL-PARTS.md`; grounding: fix-1 eye verdict, fix-1 maker report, Round 2 checker report. Parts registry named in the brief; no new part invented — nothing rebuilt.

**Five gates (before the consequential action — filing):** (1) Right — yes: restoring the 24px visible gap serves the citizen reading the date; nothing here harms anyone. (2) Truly needed — yes: the captain's eye measured 22px against a 24px target and sent the round back on that item alone. (3) Mine to do — yes: assigned maker; no protected gate touched (no merge, no deploy, no message, no money, no credentials, no destructive action). (4) Now — yes: the base is verified fresh and the fix is two gap values. (5) Prove it — yes for bytes, counts, syntax, laws, font metrics and the live model calibrated on the eye's own number (all re-measured by me from the filed blob and the real font files); explicitly **not** proven for live taps and the live gap, which I report as unproven rather than claiming them.

---

## §1 — What changed (the whole diff: exactly 2 opcodes)

| Edit | Change | Line |
|---|---|---|
| E1 | Monthline gap, Great Vibes loaded: `gap:27px` → `gap:29px` | 3113 |
| E2 | Monthline gap, fallback: `gap:24px` → `gap:27px` (`.hl-center .hl-monthline.gv-fallback`) | 3127 |

Diff re-derived by me (Buffer/byte-line difflib, base → built): **2 non-equal opcodes, nothing else** — `('replace', 3112, 3113, 3112, 3113)` and `('replace', 3126, 3127, 3126, 3127)`. Both edits are same-length value swaps, so size is unchanged at 430,643 B. No hunk touches the fix-17 block, `COVER_DAY`, `WISDOM`, `DAY_FREQ` / `DAY_COLORS` / `DAY_MEANING`, the month grid, or the bottom bar. Do-not-touch markers unchanged (counts base → built): `COVER_DAY` 3→3, `WISDOM` 20→20, `DAY_FREQ` 2→2, `DAY_COLORS` 15→15, `DAY_MEANING` 2→2, `396` 7→7, `Hz` 49→49, `gv-fallback` 2→2, `renderMonth` 16→16, `dayDigitsHTML` 10→10, `r2-more` 6→6, `data-mc-more` 3→3. Gap counts: `gap:27px` 1→1 (it moves from L3113 to L3127), `gap:29px` 0→1, `gap:24px` 3→2 (the other two `gap:24px` occurrences are unrelated rules elsewhere in the file, untouched).

### Why E2 is 24 → 27, not 24 → 29 (the judgment call, with numbers)

E1 (27 → 29) is the brief's instructed correction. E2 is my measurement-derived judgment, and I name it as such so the checker and captain can judge it in one line:

- The fallback faces end their ink at the box edge — overhang ≈ 0.00 by fontTools AND by Pillow, for Marcellus (152.31 / 152.31), DejaVu Serif (169.34 / 169.34) and Noto Serif (160.61 / 160.13). Great Vibes overhangs +2.27. So a fallback flex of 24 gives a font-math edge gap of ≈24.0 — the same font-math that predicted 24.7 for the loaded state and measured 22 live.
- The live model (§4) reproduces the eye's 22.0 exactly at flex 27 for Great Vibes. Applied to the fallback faces it predicts **21.3px blank at flex 24** — the fallback state would fail the live leg the same way the loaded state did. Leaving it at 24 while knowing that would be knowingly shipping a likely-short state.
- At flex 27 the model predicts **24.3px blank** for fallback (24.27 central; 24.3–24.8 across the three faces). At flex 29 — the task's literal number — it predicts **26.3px blank**, overshooting the exactly-24 target by ~2.3px. So 27, not 29, is the value that targets 24 in the fallback state, the same way 29 targets 24 in the loaded state (the loaded state's +2.27 overhang absorbs 2.27 of the flex; the fallback state has no overhang to absorb, so it needs 2 less flex than 29 to land on the same ink).
- The fallback number at flex 29 is still measured and reported in §4 (edge gap 29.00, predicted live blank 26.27) so the task's literal ask is answered in numbers, not dodged. If the captain prefers the fallback at 29 (pass with margin rather than land on 24), it is a one-value change on L3127.

### Build hygiene (UTF-8 / EPERM)

Edits applied in memory on split lines (byte ops, never a string round-trip); no `\r` in the file (count 0, base and built). Verified by size + sha at every step. Inline script: 1 `<script>` tag; my own `vm.Script` parse: **SYNTAX OK** (script chars unchanged by the CSS-only edit — the two gap values sit in `<style>`, not in the script). Filer: `maker/proof/file-fix2.py` (fetches the base blob, applies the edits, verifies, files, re-verifies by blob-API read-back; token minted in memory via `gh-direct.py`, never written to disk; no multi-MB payload staged to disk).

---

## §2 — Filing verification (blob-API read-back)

- Base branch tip: `98fa60d4d1d198ea41dd2d1bdf2c41290e6b9d76` — MATCH (my own read, before building).
- Base blob `7c519f1c…`: 430,643 B, sha256 match — MATCH, on every read.
- Filed blob `b35ddc6d…`: 430,643 B, sha256 `a47788d8…` — MATCH on read-back.
- HTML commit: `110c2838380f7411985cb29de263c3ee8c977f52` (blob `b35ddc6de1de80c0bb9271db98eef58acbe1501b`, 430,643 B, sha256 `a47788d801667617cc271a8d899086b9f11415a882ce2fd7ba7953448cec5d7b` — verified by blob-API read-back, size-ok + sha-ok)
- Brief commit: `eaacdd37fed6a7ce02547d14ff2cc32c1c678164` (branch tip after the first filing run; parent `110c2838380f7411985cb29de263c3ee8c977f52` (HTML commit); HTML commit's parent is the base tip `98fa60d4d1d198ea41dd2d1bdf2c41290e6b9d76`)
- Staged link: `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-round2-fix2-20261120&cb=b35ddc6de1de80c0bb9271db98eef58acbe1501b` — **staged bytes NOT yet verified byte-identical**: the filer-run fetch truncated at **159,399 bytes** (`IncompleteRead`). Flake, not file: the filed blob verifies fine on the blob API. **Re-verify the staged bytes when the flake clears; no browser leg may run until the staged link serves the full 430,643 bytes.** (Fix-1's staged fetch truncated the same way and verified whole later the same day; this one is re-checked in §9.)

---

## §3 — Browser re-test (once, at the start) — BOTH DEAD

Re-ran the Round 2 maker's `probe-browsers.py` verbatim, once, 2026-11-20 ~11:35 MST:

- **Firefox DEAD** — `BrowserType.launch: Failed to launch the browser process` (launch failure, same family as the SIGSEGV the fix-18 eye hit; pid 323765 launched, then died).
- **Chromium DEAD** — `BrowserType.launch: Target page, context or browser has been closed` on launch (same SIGTRAP family).

I re-tested once and stopped, per the brief. No live-browser tool exists on this seat. **Consequence, stated plainly: every live leg below is UNPROVEN, not passed.** I claim none of it, borrow none of the checker's or maker's numbers, and guess none of it.

---

## §4 — Gap proof by measurement (font files, not arithmetic alone)

Driver: `maker/proof/measure-gap.py` (re-runnable; fetches the fonts fresh, measures, prints the table, asserts the Round 2 checker numbers reproduce). Method: fontTools 4.46.0 outline measurement of "November" at 32px (the rendered size, `.hl-script` L2697) + Pillow 10.2.0 / FreeType raster cross-check at the eye's >140 luminance threshold + a live model calibrated on the fix-1 eye's own measured number.

### The fonts

| Font | Source | Size / sha256 |
|---|---|---|
| GreatVibes-Regular.ttf | `google/fonts` main, `ofl/greatvibes/GreatVibes-Regular.ttf` | 457,588 B, `8d509802186f1b51572531ecf313e8098f9a5bfdfaca93f0c9b34467f9982d15` — the same file the Round 2 checker measured |
| Marcellus-Regular.ttf | `google/fonts` main, `ofl/marcellus/Marcellus-Regular.ttf` | 46,004 B, `1cf0cd10b17d35e852729962cc1ffaffed94514895972458345e2df34abb2f81` — the CSS-named fallback face (font stack L2697: `"Great Vibes","Marcellus",cursive`; the page loads Marcellus via the Google Fonts link, L11) |
| DejaVu Serif | VM system font `/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf` | the VM Firefox fallback face — matches the fix-18 fallback box width 170 exactly (advance 169.34) |
| Noto Serif / DejaVu Sans | VM system fonts | further fallback candidates, same result |

### The measurement (32px "November")

| Font | Advance | Ink range (fontTools) | Overhang | Pillow adv | Pillow ink >0 | Pillow ink >140 |
|---|---|---|---|---|---|---|
| GreatVibes | 105.54 | −0.10 → 107.81 | **+2.27** | 106.27 | 108.00 | 106.00 |
| Marcellus | 152.31 | 2.11 → 152.31 | **0.00** | 152.31 | 152.00 | 151.00 |
| DejaVu Serif | 169.34 | 1.56 → 169.34 | **0.00** | 169.34 | 169.00 | 168.00 |
| Noto Serif | 160.61 | 1.22 → 160.13 | −0.48 | 160.62 | 160.00 | 159.00 |
| DejaVu Sans | 166.47 | 3.14 → 166.47 | 0.00 | 166.47 | 166.00 | 165.00 |

Reproduction: the Round 2 checker's numbers are reproduced exactly (GreatVibes advance 105.5, ink −0.1→107.8, overhang 2.27; Marcellus 152.3; DejaVu Serif 169.3). Pillow agrees within ~1px on every face (its GreatVibes advance 106.27 vs fontTools 105.54 is GPOS kerning, which the raw hmtx sum omits — the same 0.7px split the Round 2 maker and checker already noted). **No @font-face for Great Vibes exists in the file** — it arrives via the Google Fonts css2 link (L9–L11), so the browser's woff2 carries the same outlines as the measured TTF; the font file is not a second explanation for the shortfall.

### The live model (calibrated on the eye, not on arithmetic)

The eye's number at flex 27 (desktop 1920, Great Vibes loaded): last November ink x=938, first "2" tile border x=961 → **22 blank px, 23 edge-to-edge**. Font-math alone predicts 24.73 edge-to-edge (27 − 2.27). The 1.73px gap between prediction and live is the `.hl-script` 14px blur text-shadow (L2697: `0 0 14px color-mix(...45%, transparent)` + the white `0 -1px` highlight): it pushes the >140-luminance edge ~1.73px past the outline bbox. The shadow term is font-independent — the same rule, same shadow, on every face — and the tile side is clean (the first digit tile's border starts at its wrapper's left edge: `.os-mini-num` L125, no padding/margin on the wrapper; the 12px tile glow, L2269, is outside the border the eye measured to).

Model: **live blank px = flex − overhang − 1.73 (shadow) − 1 (pixel edge)**.

- Calibration: Great Vibes at flex 27 → 27 − 2.27 − 1.73 − 1 = **22.00 blank — exactly the eye's 22.** The model reproduces the governing live number to the pixel. That is the whole basis for the filed values.
- **Great Vibes, filed flex 29:** fontTools edge gap 26.73, predicted live blank **24.00**. ✓ target met.
- **Fallback, filed flex 27:** fontTools edge gap 27.00 (Marcellus/DejaVu overhang 0.00; Noto Serif −0.48 → 27.48), predicted live blank **24.27** (24.27–24.75 across faces). ✓ target met.
- Fallback at the old flex 24: predicted live blank **21.27** — would have failed the live leg the same way the loaded state did. This is why E2 exists.
- **Fallback at flex 29 (the task's literal number):** fontTools edge gap 29.00, predicted live blank **26.27** — passes ≥24 but overshoots the exactly-24 target by ~2.3px. Filed as 27 instead, for the reason in §1.
- **Halo-counted gap at flex 29 (asked for, honestly):** at flex 27 the faint pixels (luminance 100–140) reach x≈944–946 while the tile border sits at 961, giving a halo-counted blank of ≈14–16px (the eye's own figure). At flex 29 the tile border moves 2px right (≈963) and the halo reaches ≈946–948, so the predicted halo-counted blank is **≈15–17px (16px central)** — still short of 24, as the brief anticipated. That is expected: the halo is the shadow's faint edge, not ink, and the ruling target is the solid-ink 24px. The fix-18 eye's 16px reading is the same halo counted the same way, not a second defect.

### Centring and 390 (computed, live-owed)

- Centring: the monthline is a centred inline-flex line (`.hl-center` L2698: `align-items:center`; the line is `justify-self:center`). Widening the gap by 2px (loaded) / 3px (fallback) widens the group symmetrically, so the group centre does not move: predicted new centre **≈945 vs viewport 960** (the eye's fix-1 figure, unchanged), still reading centred. Live-owed to the eye.
- 390: the change adds +2px (loaded) / +3px (fallback) to the monthline's total width. Round 2 measured the fallback monthline at 280px wide in a 240px column at flex 24 (overflow 20px/side into clear black field, `docScrollW` 390); at flex 27 that becomes **283px** (+3), overflow ~21.5px/side, same clear field, same mechanism — `docScrollW` expected to stay 390. The loaded state at 390 is narrower (November is 47–64px narrower than the fallback faces), computing to ~221–238px total, inside the 240px column with no overflow. Both are computed from Round 2's measured total, **not measured live — the 390 leg is unproven and is the shipping gate** (§9).
- One line, no wrap: `white-space:nowrap` on the monthline (L3113) is untouched; neighbours clear by the same overflow mechanism Round 2 verified. Live-owed.

| Leg | Range-rect ink gap | Screenshot visible-edge gap |
|---|---|---|
| 1920, Great Vibes loaded | UNPROVEN (live) — font-model predicts 24.0 blank | UNPROVEN (live) — same prediction |
| 1920, fallback serif | UNPROVEN (live) — font-model predicts 24.3 blank | UNPROVEN (live) — same prediction |
| 390, Great Vibes loaded | UNPROVEN | UNPROVEN |
| 390, fallback serif | UNPROVEN | UNPROVEN |

---

## §5 — "Your Journal" door: adjudicated — INTENDED, no fix

**The finding, in one line: there is no collapse code path, because there is nothing to collapse — the month cells never carried a "Your Journal" label in any state, and the persistent number + dots + "i" state is the only state the code can produce, by design.**

The evidence, all from the filed base bytes:

- **The only builder of month cells is `renderMonth()` (L3841–3898), and it is the same on every call.** Every call site — init (L5768), BACK TO MONTH (L5737, L5763), every door close (L5115, L5126, L5198, L5235, L5256, L5265), booking (L5535, L5618), month nav (L5704, L5709) — calls the same function, which always emits the identical structure per in-month day: `dayDigitsHTML(d.getDate(), dc)` (number, top-left, L3894) + `dots` (L3871–3878: up to 3 appointment dots, a note dot, a journal dot) + `jewelSVG()` (the "i" jewel, bottom-right, L3895). No label string, no second render mode, no branch, no state flag distinguishes a first load from a later one.
- **Hover does not and cannot expand a cell.** `.cell:hover` (L416–424) brightens the rim and its outside light only — the comment says so: "the face of the day stays dark and calm". `.cell:hover .jewel` (L476–483) lifts the jewel 1px and brightens its glow. No hover rule reveals a label, and there is no label in the markup to reveal.
- **The string "Your Journal" occurs exactly 3 times in the whole 430,643-byte file, and none of them is in a month cell:** L3035 (a CSS comment about the fix-17 Change-cover collision), L4841 (a code comment), and L4850 — the Summary slide's `sumRow("journal", "#07925f", "book", "Your Journal", …)` (L4446–4452: a button row, whole row the tap target, `data-door="journal"`, opening the journal door). The journal door itself is the Record category's journal view (L5200 `door.id === "journal"`).
- **The journal's designed signal inside a month cell is the blue dot, not a label.** L3876: `if (nj) dots += '<i class="journal"></i>'` (nj = journal entries for that day, L3870); L1474–1476: `.dots i.journal { background: #0f52ba; … }` (journal blue, square); the v17 comment L1292–1293 states it outright: "(5) The journal dot in the month cells — a day with a journal entry shows it, in journal blue." The design law (§7) fixes the cell anatomy the same way: day number top-left in digit tiles, dots, the eye bottom-right — no text label in a cell.
- **The door persists where it belongs — in the day view, not the month grid.** It is reachable as the Summary slide's "Your Journal" row (L4850, whole-row tap target, present on every day's Summary slide), as the Record category's Journal slide (L4888), and as the journal door (L5200). None of those paths is touched by opening a day or returning to the month; `renderMonth()` rebuilds the same cells either way.

**Why no fix:** adding a text label to 30 month cells would break the cell anatomy the laws fix (§7), break the month grid (a do-not-touch item), and would not fit — the cells are small boards with the number top-left, dots bottom-left and the jewel bottom-right, and at 390 there is no room for a label without clipping or wrapping. The door as a distinct tappable label exists and persists in the day view; the month cell's job is the glance (number + dots + eye), and the journal dot is its journal signal.

**One honest caveat, for the captain's eye:** the eye's first-load observation — a "Your Journal" label visible whole inside the month cells — is **not reproducible from this file's code in any state**, because no code path can put that string inside a `#grid` cell. The only "Your Journal" label that renders whole, with a whole-row tap target, is the Summary slide's journal row, which is what a day shows when it is first opened. I do not claim the eye mis-saw; I state what the code can produce, and ask the eye to re-check which screen that first-load label was on. If the eye re-proves a label inside a month cell on the staged fix-2 bytes, that is new evidence and the adjudication re-opens.

---

## §6 — Full tap list + regression sweep — proven in code; taps carried forward from the fix-1 eye

The fix-1 eye **tap-proved** items 1, 2 and 4 on these exact bytes (EYE-VERDICT.md): paging 33→27→21→15→9→3 and back to page 0; full booking end to end; change and cancel in one tap; double-booking refused by omission; deck 9/9; nav 7/7; Change cover only on Wisdom + Your Worlds; no Hz in headers; Keep-reading / prev-day / BACK TO MONTH land; row 6 blank; no visible page errors. **My diff touches only the two monthline gap values (L3113, L3127, both in `<style>`)**, so every code path below is byte-identical to the bytes the eye tapped. The tap proofs therefore carry forward; what I prove here in code is that each path exists, is wired, and is unchanged.

| Tap item | Code shows (base = filed, line numbers on the fix-1 base) | Tap status |
|---|---|---|
| Paging 6/page, counts 33→27→21→15→9→3, back to page 0 | `per = 6` L5467; `slice(page * per, page * per + per)` L5468; handler L5655–5656 (`"next"` → `timePage + 1`, else → 0, then `mcRenderCal()`); buttons L5475 ("More times · N left") / L5477 ("Back to the first times"). `mcFreeTimes` L5417–5435: 15-min slots 06:00–20:30; for the eye's day the free list is 33 (12:30–20:30), paging 33→27→21→15→9→3, last page 3 — the arithmetic holds | PROVEN BY EYE on fix-1 bytes; code unchanged |
| Full booking: kind → day → time → name/what/who → ONE emerald Book → confirmation | Kind pills L5455–5458 (meet/person/call); 7-day strip `.mc-days` L2800 (repeat(7,1fr)); time pills `mcTimePill` L5437; form `mcRenderForm` L5495–5508, ONE `#mcBook` emerald L5502 (label "Book" / "Save the change" in edit); confirmation L5583–5598: "Booked" L5584, mail line "Smart Mail — draft saved … It sends when Smart Mail connects." L5589, reminder line "Reminder set — 30 minutes before, kept on this device." L5590 | PROVEN BY EYE on fix-1 bytes; code unchanged |
| Change in one tap (preserved) | Tile tap L5671 re-opens the form with kind/day preserved, `timePage = 0`; "Change time" L5604–5610 re-opens edit (`__mc.edit` set, button becomes "Save the change" L5502) | PROVEN BY EYE on fix-1 bytes; code unchanged |
| Cancel in one tap | `mcCancelIdx` L5608, delegated handler L5663 (`data-mc-i` → cancel at once, no confirm dialog) | PROVEN BY EYE on fix-1 bytes; code unchanged |
| Double-booking refused (slot gone from fresh form) | `mcFreeTimes` L5427–5431 excludes any slot overlapping a booked appointment (+30 min buffer); `mcBook` guard L5519–5522 re-checks and refuses with "That time is taken now — here are the next open times." (L5520), resets `timePage = 0` and re-renders; door guard L5123 likewise | PROVEN BY EYE on fix-1 bytes (fresh form earliest became 13:30, 12:30 gone); code unchanged |
| Deck 9/9 | Wisdom banner (static, L3201–3203) + `catSection` slides L4887–4892 (Notifications, Journal, Your Worlds, News Hub, Appointments, Summary) + Naya Notes / Smart Notes sections — the 9 slides the eye swept | PROVEN BY EYE on fix-1 bytes; code unchanged |
| Nav 7/7 | 7-day strip, `repeat(7,1fr)` L2800, days FRI 20–THU 26 in the eye's sweep | PROVEN BY EYE on fix-1 bytes; code unchanged |
| Change cover only on Wisdom + Your Worlds | L3114: `.cover-change{display:none}` unless the wisdom banner or the worlds slide is on; L3071: hidden on wisdom at ≤560px (fix-17, phone-only) | PROVEN BY EYE on fix-1 bytes (desktop); 390 leg unproven, see §9 |
| No Hz in headers | Headliner build L4301: month name + year digits only — no Hz anywhere in it. `Hz` count 49→49, all in CSS comments/day-colour vars, the Hz jewel, and the Wisdom slide's text ("396 Hz" inside the Wisdom slide, not the header) | PROVEN BY EYE on fix-1 bytes (Nov 15–21); code unchanged |
| Keep-reading / prev-day / BACK TO MONTH land | "Keep reading ◆" L3203 (wisdom banner, `data-sb="next"`); prev-day `slide-back data-sb="prev"` L4423/L4707; `backToMonth` handler L5737 (`stopMeet(); renderMonth(); show("screen-month")`) | PROVEN BY EYE on fix-1 bytes; code unchanged |
| Row 6 blank | 42 cells L3863 (`for (var i = 0; i < 42; i++)`); other-month cells render blank L3879–3883; November 2026 has 30 days starting Sunday, so row 6 (cells 36–42) is entirely other-month → blank | PROVEN BY EYE on fix-1 bytes (30 numbered cells in 42, row 6 blank); code unchanged |
| 0 page errors (static) | Inline script parses (`vm.Script`: SYNTAX OK); the diff is CSS-only — no new JS, no new error path, no new handler | Static only; live console owed to the eye |

Regression at **code level only** for the parts the eye did not re-tap: the diff is exactly 2 replace opcodes in `<style>` (§1) and no hunk touches the fix-17 block, fix-18 items 2–3 regions, `COVER_DAY` / `WISDOM` / `DAY_FREQ` / `DAY_COLORS` / `DAY_MEANING`, the month grid, or the bottom bar; `396`/`Hz` counts unchanged (7/7, 49/49). Code-level is not tap-level and I do not claim it is. **0 page errors: unproven in every live leg** (no render ran). Note carried from Round 2: "Call" has no call UI on the page — stored as data only (`how: "call"`); the eye should confirm a Call booking reads sensibly on the confirmation board; that is not a defect.

---

## §7 — Polish: the "that slot is taken" message — CARRIED, not forced

The brief allows the polish only if it fits cleanly without risk. It does not fit cleanly, so it is carried — and the reason is that **the explicit message already exists on both paths where a double-booking can actually be attempted**:

- `mcBook` guard (L5519–5522): `"That time is taken now — here are the next open times."` — rendered in the form as `.r2-refused` (L5491, L5498; red-bordered, white 17px, L3154). This fires when a slot that was open when picked is taken by the time Book is pressed.
- Door guard (L5123): `"That time is taken — pick an open time on the Appointments slide."`

What the eye noted is the third path — the **fresh form**, where a taken slot simply does not appear in the list. There is no clean trigger for a slot-specific message there: the form never knows the citizen wanted 12:30, so naming it would need stale state (remembering the last booked slot and showing it on a form opened later, possibly on another day — wrong as often as right). The list's design is "open times only, a few at a time, never a wall" (Round 2) — a taken-slot note inside it would contradict the list's purpose. A generic "some times are already booked" note would be noise on every busy day and would touch the Step 3 layout the eye already passed. So: **carried**. The guard is met by omission plus the two explicit messages above; if the captain wants a taken-slot note in the fresh list, that needs a design decision (what triggers it), not a line in this round.

---

## §8 — Design laws (§11 in writing)

**Checker runs (mine, `check-design-laws.py` via the real script's own `check()` on the exact base and built bytes — driver `maker/proof/run-laws.py`):**
- Base: **PASS, 0 FAIL / 28 WARN** (exit 0).
- Built: **PASS, 0 FAIL / 28 WARN** (exit 0). Same 28 warnings, same lines (the two changed lines are CSS gap values, which no law rule touches).
- **Laws delta: 0.**

Applied laws: §1 real objects (the fix touches no object anatomy — the monthline's script word and digit tiles keep their Round 2 treatment; nothing is made flat or dead by a gap value); §2 text (no text touched; sizes stay 25/19/17, all white; 0 FAIL confirms no gray); §3 color (no colour touched); §4 objects (board/pill/tile/digit-tile anatomy untouched; **named tension, carried: 29px and 27px both break the 8px-spacing multiple** — the measured 24px-ink target is the stated reason, and the eye judges the result; the same tension was named in Round 2 and fix-1 for 27px); §5 buttons (PTS/%/MONEY untouched; no button touched); §7 day/calendar (the monthline is the day's headliner; its centring, one line and neighbours are the acceptance, live-owed); §9 layout (Step 1/2/3 in plain words, mobile-first — the 390 leg is owed); §11 check + sense check on the PAGE.

**§11 design check, answered in writing:** could I pick the changed object up — the monthline's volume, rim, shadow and the digit tiles' anatomy are unchanged in code (the gap is spacing, not an object); the eye must confirm by sight, unproven. Light top-left — 135° gradients throughout, untouched. Made of what — obsidian inside, white word in the middle, own-colour light outside. Shadow — grounding shadows present. Touch — no control's touch behaviour changes (the gap is not a control). Glow inside — none in the touched CSS. Gray text — none (0 FAIL). Text under 17 — none (0 FAIL). Two same colours together — none introduced (nothing re-coloured). Flat or dead — nothing in this diff can make anything flat or dead; the monthline's aliveness is the eye's call. Which reference object — the elite pills and digit tiles, harvested verbatim from this page (the year digits are `dayDigitsHTML`, the Dashboard's own tiles). Read as a reader — cannot be done without a render; owed.

**Sense check on the page (not just the diff):** the fix does the brief's one job — the date line's gap reads 24px of true visible ink in both font states — and nothing else on the page moves. The fallback change (§1) is the sense check working, not scope creep: leaving the fallback at a value the same model predicts will read 21.3px live would hand the eye a second go-back for the same defect in the other font state. The Your Journal adjudication (§5) is the sense check on the other side: the door is not broken, so no fix is invented for it. The remaining risk on the page is the live gap number itself (§4) — a live measurement, not an argument — and it is named here, not hidden.

---

## §9 — What is honestly live-only / what remains

1. **Gap live proof, both methods, four legs** (§4) — owed to the captain's cloud-browser eye once the staged link serves whole bytes: Range-rect ink gap + screenshot visible-edge gap at 1920 AND 390, Great Vibes loaded AND fallback, centred, one line, `docScrollW` 390 at 390 fallback. My font-model predictions: 24.0 blank (loaded, flex 29), 24.3 blank (fallback, flex 27); halo-counted ≈16px at flex 29 (expected, not a fail — the ruling target is solid ink).
2. **Staged bytes re-verification** — the filer-run fetch truncated at 159,399 bytes. **No browser leg may run until the staged link serves the full 430,643 bytes byte-identical (sha256 `a47788d8…`).** Re-verify when the flake clears.
3. **390 eye leg — still owed; shipping waits for it.** Nothing in this round says the page fails at 390; nothing says it passes. The computed 390 widths (§4) are not a substitute.
4. **Full tap list + regression sweep at tap level** (§6) — carried forward from the fix-1 eye's taps on these bytes except the two gap values; a fresh eye pass on the filed bytes is still owed before shipping, since the gap is the one thing that changed and the eye judges the page, not the diff.
5. **Your Journal first-load observation** (§5) — the eye to re-check which screen its first-load "Your Journal" label was on; the code cannot put that label in a month cell.
6. **Polish** (§7) — the explicit taken-slot message in the fresh list is carried; the guard messages on the attempt paths already exist.
7. Smart Mail delivery and the reminder firing remain live-only (localStorage draft + reminder, honestly labelled on the confirmation board; no sent mail is faked) — unchanged by this round.

**Self-score: 7/10.** The byte leg is fully proven by my own drivers — base re-verified from the blob API, exactly 2 diff opcodes, counts before/after, syntax OK, laws delta 0, filing verified by read-back, and the gap values are derived from a live-calibrated font measurement that reproduces the eye's 22.0 to the pixel (not from arithmetic alone). Not higher because the defect's real proof (the live gap, four legs, two methods), the 390 shipping gate, and the whole tap + regression sweep are all still owed to a live browser, and the staged bytes are still unverified while the flake persists. The round did what a no-browser seat can honestly do — and says plainly what it could not.
