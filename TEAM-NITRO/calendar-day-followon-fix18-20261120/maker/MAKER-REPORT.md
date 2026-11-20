# CAL-FIX18 — Maker Report

**Verdict: FIXED and FILED — all three §4/addendum items proven on the filed bytes, in all four legs.**
**Date:** 2026-11-20 (VM clock UTC; Shawn live on a voice call, walking the Calendar day view)
**Maker:** Calendar day-followon fix-18, Team Nitro

## Filing identity

| Item | Value |
|---|---|
| Base branch | `calendar/day-followon-fix17-20261119`, tip `a955d7fa2299a6667ba70215dd4347c1de80386e` (verified live before filing: branch GET returns this tip; file at that tip is blob `f4c05109`) |
| Base file | `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html` |
| Base blob | `f4c05109531f8b737891a43f6ea6bdcef84eddc9`, **410,236 B**, sha256 `1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887` |
| New branch | `calendar/day-followon-fix18-20261120` (created from the fix-17 tip, HTTP 201; pre-checked absent first) |
| Filed commit | `ffd220c7d7d54fbbfc08c82ceed793ce1b0968a3` (parent `a955d7fa…`, the fix-17 tip) |
| Filed blob | `f7b14ce75d590738a9efb87a4fa056ee98f3561d`, **413,386 B**, sha256 `52ff950fb4dfeb942415c96ee2af393b815e06e9019c77a9758121a9f40770cc` |
| Staged link | `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix18-20261120&cb=f7b14ce75d590738a9efb87a4fa056ee98f3561d` |
| Verification | Filed blob re-read via the git blob API: 413,386 B, sha256 `52ff950f…`, byte-identical to the local fixed file; rebuilt (base − Hz segment + fix-18 block) == filed blob; fixed-minus-block + Hz-reinsert == base. Staged link curled with a browser User-Agent: HTTP 200, 413,386 B, sha256 `52ff950f…` — matches the filed blob. |

## 1. Defect reproduction — measured on the fix-17 bytes first

### Items 1–2 — the header (measured before designing the fix)

| Width / font state | Monthline as rendered | Monthline centre vs viewport centre | November→2026 gap |
|---|---|---|---|
| 1920, Firefox, no-webfont fallback | `November 2026 · 396 Hz`, one line | cx 960 = centre, **offset 0** | **8px** |
| 1920, Chromium, fonts-loaded | `November 2026 · 396 Hz`, one line | cx 960 = centre, **offset 0** | **7px** |
| 390, Firefox, fallback | **WRAPPED:** `November` / `2026 · 396 HZ` | line box cx 195, but the two lines land as separate centred fragments (year line 96–262, centre 179) | **−184px** (year on the line below) |
| 390, Chromium, fonts-loaded | **WRAPPED:** `November 2026 ·` / `396 HZ` | line box cx 195; first line spans 91–288, centre ≈190 | **5px** |

Root cause: the ≤560px rules set `.hl-center .hl-monthline{white-space:normal}` (base line 2856, winning over the global nowrap at line 2700), so the line wraps at phone width; and the November→2026 gap was a single space (7–8px). At 1920 the line was already dead-centre — the defect was the wrap at 390 and the tight gap at both widths. Screenshots read as a reader confirmed it: at 390 the month-year reads as two stacked fragments with the `· 396 HZ` tiles dangling on their own line; the header never reads as one centred title line.

### Item 3 — where the cover is actually visible (pixel-diff census, cover on vs cover off)

The cover layer (`#dayCoverBg`, z-index 0, `inset:0` inside `#dayScroll`) sits behind the slides; whether it shows depends on whether the slide's content leaves deck exposed. I measured it, per slide, by screenshotting the `#dayScroll` rect with the cover shown and with it `display:none`, counting interior pixels (>6px inside the deck edge) that change, against a drift baseline (two cover-on shots 300ms apart). Two method traps, recorded so nobody re-learns them:

- **Hash-only comparison lies:** my first pass compared PNG sha256s and reported "cover visible" on all 9 slides — ambient animation drift (pulsing jewels, rotating rings) changes pixels between any two captures. Pixel counts with a drift baseline are the measurement; hashes are not.
- **Freezing animations with a global style tag lies worse:** `*{animation-play-state:paused!important}` injected before navigating froze each new slide's `smartpop` entrance at opacity 0, making the whole deck transparent — the red cover showed fullscreen on slides 1–8 (96% of pixels, identical counts). The correct freeze is `document.getAnimations().forEach(a => a.pause())` only, applied per slide AFTER the 2.5s settle, with no persistent style tag.

Corrected census (day 20, Friday, `friday_red.jpg` — bright red, so the cover is unmistakable where it shows):

| Slide | 390 interior cover px (drift) | 1920 interior cover px (drift) | Verdict |
|---|---|---|---|
| 0 Wisdom | **14,371** (6) | 344 (60) | **COVER SHOWN at 390** — a solid red band below the board; rim-only at 1920 |
| 1 Notifications | 332 (0) | 690–3,030, unstable across runs (animation residue, no coherent region) | rim-only |
| 2 Journal | 337 (0) | 252 (0) | rim-only |
| 3 Worlds | **12,900** (202) | 252 (635) | **COVER SHOWN at 390** — a solid red band below the tiles; rim-only at 1920 |
| 4 News Hub | 332 (194) | 655 (1,348) | rim-only |
| 5 Appointments | 339 (640) | 261 (0) | rim-only |
| 6 Summary | 337 (761) | 257 (0) | rim-only |
| 7 Naya Notes | 332 (0) | 252 (0) | rim-only |
| 8 Smart Notes | 334 (0) | 253 (0) | rim-only |

Control: Thursday (day 19, green cover) at 1920 also rim-only on slides 0/1/3/5 (73–871 interior px) — the rim-only finding is not cover-colour-dependent. The red-band overlays (`shots18/cc-firefox-nofont-390-0.png`, `cc-firefox-nofont-390-3.png`) show the band plainly: at 390 the wisdom board and the worlds tiles are short, and the deck below them is the red cover photo. On the other seven slides the content fills the deck at both widths and the cover contributes only the 1–3px rim around the slide. Shawn's eye was right about Notifications: no cover is visible there.

**Adjudication note (for the checker, stated plainly):** at 1920 the cover is rim-only even on Wisdom and Worlds — the photo is plainly visible on those two slides only at 390. The rule below keeps the pill on Wisdom + Worlds at both widths anyway, because (a) the addendum names Wisdom as the keeper without width qualification, (b) those are the cover's slides by design — the cover layer is their backdrop, exposed whenever their content leaves deck showing — and (c) a width-dependent pill (showing on Wisdom/Worlds only on phones, nowhere on desktop) would kill the function on the surface where Shawn works. If the checker reads "visibly shown" as a strict per-width pixel rule, 1920 Wisdom/Worlds is the one place this round's rule and that reading differ; the measurement behind both readings is in this report and in `maker/proof/covercensus3-*.log`.

## 2. The fix — one CSS block + one JS string deletion

File: `maker/proof/fix18-block.css` (3,249 B after the comment rewording; see §6). The fixed file is the base plus exactly this block plus the Hz-segment deletion — verified `fixed-minus-block + Hz-reinsert == base` (bytecheck18.js, 28/28 PASS).

### Item 2 — Hz segment deleted from the monthline build (base line 4219)

Deleted exactly one occurrence (verified count 1 in base, 0 in fixed):

```
 + " \u00b7 <span style=\"white-space:nowrap\">" + dayDigitsHTML(DAY_FREQ[d.getDay()], dc) + " Hz</span></span>"
```
replaced with ` + '</span>'`. The space after the script `</span>` is kept (harmless in the flex monthline; graceful if CSS fails). The rendered header Hz is gone; the literal `396` count is unchanged (7 → 7) because the header 396 was rendered from `DAY_FREQ[5]` at runtime, never a literal — the bytecheck asserts this rather than pretending a literal was removed. The wisdom line (`#dayTeach`, two mentions), the `WISDOM` quote, `DAY_FREQ`, `DAY_COLORS`, `DAY_MEANING`, and the month screen's `monthName` are byte-identical.

### Item 1 — monthline: one nowrap flex line, exact 24px gap

```css
.hl-center .hl-monthline{display:inline-flex!important;align-items:center!important;gap:24px!important;white-space:nowrap!important}
```

- `display:inline-flex` + `gap:24px`: the whitespace-only text node between the script span and the year span is dropped in flex layout, so the gap is exactly 24px (multiple of 8, laws §4) in both font states — measured 24px in all four legs (was 7–8px; −184px wrapped at 390 FF).
- `white-space:nowrap` (appended after base line 2856, so it wins at ≤560px) + flex `nowrap` default: the line cannot wrap at 390 — measured one line in all four legs.
- `align-items:center`: November and the 2026 tiles now share a centre line (1920 Cr: nov cy 152, year cy 152 — the base had the year 7px below November's centre). No styling, colour, or size change: script "November" (Great Vibes 32px) and digit-tile "2026" harvested verbatim.
- **No reorder:** I considered moving the monthline above "Friday 20" at 390 ("at the top of the header"), and decided against it — the brief's own constraints rule it out: the time row (inside `hl-center`, under the monthline) and "Friday 20" are both ordered to stay where they are, and any monthline-above-Friday move at 390 necessarily displaces both. The monthline is the title line at the top of its column, above the time row, at both widths; the fix is that it now reads as one centred line. If Shawn wants it above "Friday 20" on phones, that is a reorder round with its own brief.

### Item 3 — one slide-state rule for the pill

```css
#dayScroll:not(:has(#wisdomBanner.on)):not(:has(.worlds-slide.on))>.cover-change{display:none!important}
```

One rule, not a per-slide list: the pill is hidden whenever NEITHER keeper slide is on. It hides the pill on all seven content slides at both widths in both browsers, and leaves it exactly where it was on Wisdom (floating bottom-right at 1920; hidden at ≤560px by the fix-17 rule, which stands) and Worlds (floating bottom-right at 1920; static-flow below the content at ≤560px, as before). The `:not(:has())` form is the safe default — a future slide with no cover hides the pill unless it is named a keeper. The Change cover function itself is unchanged where the pill remains (tap test, §3d). The fix-17 placement geometry (`top:40px`, wisdom hide ≤560px) is untouched and still governs where the pill sits when it shows.

**Consequence, named plainly:** at ≤560px the pill now appears on only one slide — Worlds (static-flow, 768–808). On Wisdom at ≤560px it stays hidden per fix-17; on the other seven slides it is hidden per item 3. Change cover at phone width is therefore a Worlds-only doorway; at desktop it is Wisdom + Worlds. That is the combined outcome of Shawn's fix-17 sanction and his item-3 instruction, not a choice I made silently.

**Side effect, measured:** at 390 the header compresses by 32px (the monthline went from two lines to one: stats-btn 248–292 → 216–260, timewrap 206–240 → 174–208). The deck moves up 32px with it; deck-internal geometry is unchanged (the fix-17 bands are measured inside `#dayScroll`), and the regression (§3c) re-proves the deck whole. The wisdom sweep nav clearances improved as a result (worst day 43px clear at 390 FF, was 10px in fix-17).

## 3. Re-proof — final filed bytes

All runs on the filed bytes (`fixed-fix18.html`, sha256 `52ff950f…`), real render, real taps, 2s waits after every deck navigation. 0 page errors in every run. VM clock is UTC; the greeting follows it ("Good afternoon, Shawn." at ~15:xx UTC — true to time of day).

### 3a. Item 1 — "November 2026" centred, one line, 24px gap (day 20, all four legs)

| Width / font state | Monthline text | Centre offset (cx − viewport centre) | November→2026 gap | One line? |
|---|---|---|---|---|
| 1920, Firefox, fallback | `November 2026` | **0px** (960 = 960) | **24px** | yes (323px wide) |
| 1920, Chromium, fonts-loaded | `November 2026` | **0px** (960 = 960) | **24px** | yes (259px wide) |
| 390, Firefox, fallback | `November 2026` | **0px** (195 = 195) | **24px** | yes (280px wide, x55–335 — overflows the 240px column 20px a side into clear black field, `docScrollW` stays 390) |
| 390, Chromium, fonts-loaded | `November 2026` | **0px** (195 = 195) | **24px** | yes (216px wide) |

Neighbours untouched in every leg: "Friday 20" left (1920: x392; 390: centred in its own row, y100–132, as in base); time row directly under the monthline, centred (cx 960 / 195); BACK TO MONTH left; Your Stats + orb right (stats x1388–1528 at 1920, x125–265 at 390; orb x1711–1775 / x300–336 — identical to base).

### 3b. Item 2 — no "396 HZ" in the header; wisdom untouched (all four legs)

- Rendered header text, all four legs: `Friday 2 0 November 2 0 2 6 <time> Your Stats` — no `HZ`, no `396` anywhere in the header (element census: monthline contains exactly **1** `.os-mini-num` span, the year; the Hz span is `None`).
- Wisdom line, all four legs, byte + render: `Friday · 396 Hz · red — The day of the ground — the root, 396 Hz. Stand firm; finish what stands.` — two mentions, exactly as in base. `WISDOM` quote untouched (bytecheck).

### 3c. Item 3 — per-slide pill census on the filed bytes (all four legs)

| Slide | 1920 FF | 1920 Cr | 390 FF | 390 Cr |
|---|---|---|---|---|
| 0 Wisdom | **shown** 1635, 795–835, hit-testable | **shown** 1633, 800–835, hit-testable | hidden (fix-17) | hidden (fix-17) |
| 1 Notifications | hidden (0×0) | hidden (0×0) | hidden (0×0) | hidden (0×0) |
| 2 Journal | hidden | hidden | hidden | hidden |
| 3 Your Worlds | **shown** 1635, 795–835, hit-testable | **shown** 1633, 800–835, hit-testable | **shown** static-flow 175, 768–808, hit-testable | **shown** static-flow 173, 773–808, hit-testable |
| 4 News Hub | hidden | hidden | hidden | hidden |
| 5 Appointments | hidden | hidden | hidden | hidden |
| 6 Summary | hidden | hidden | hidden | hidden |
| 7 Naya Notes | hidden | hidden | hidden | hidden |
| 8 Smart Notes | hidden | hidden | hidden | hidden |

Notifications pill-absent at both widths, both browsers, as Shawn asked. The `:not(:has())` selector works in both browsers (this census IS the proof — the pill is `display:none` with a 0×0 rect on all seven content slides in Firefox and Chromium alike).

### 3d. The pill still works where it remains (real taps, native file picker)

`tap18.py` (Firefox): 1920 Wisdom tap → file picker OPENED; 1920 Worlds tap → OPENED; 390 Worlds tap → OPENED; 1920/390 Notifications + 390 Wisdom → pill hidden, not clickable. The chosen photo still becomes that day's cover only (FIX11 item 15 — handler untouched, byte-identical).

### 3e. Fix-17 hold — full regression on the filed bytes (2 legs)

`prove18.py` (fix-17 harness, retargeted at the fixed bytes):

| Leg | Wisdom sweep 7 days | Deck 9 slides | Buttons | Month | Page errors |
|---|---|---|---|---|---|
| 390, Firefox, fallback | **7/7 PASS** (worst day Sat 21: nav 722–766, **43px clear**; pill hidden all 7 days) | **9/9 PASS** (Appointments nav 2px clear held; Smart Meet hit-testable centre + bottom; Worlds pill 768–808 hit-testable) | Keep-reading advances day, prev-day returns it; monthline `November 2026` throughout | 42 / 30 / 12, row 6 all blank | 0 |
| 1920, Chromium, fonts-loaded | **7/7 PASS** (nav 824–882, 18px clear every day; pill 800–835 on wisdom, clear of weather pill) | **9/9 PASS** (nav 824–882, 18px clear every slide; pill hit-testable on wisdom + worlds, hidden elsewhere) | Keep-reading / prev-day as above | 42 / 30 / 12, row 6 all blank | 0 |

Greeting true to VM clock (UTC) in all legs; `docScrollW` == viewport width in every run (no horizontal overflow at 390 or 1920).

### 3f. Read as a reader (screenshots)

- **390, Chromium/fonts** (`shots18/header-fixed-chromium-fonts-390.png`): "Friday 20", then "November 2026" on one centred line — script November, clear daylight, then the 2026 tiles — time below, Your Stats below that. No Hz anywhere. It reads nice and clean, exactly as he asked.
- **390, Firefox/fallback** (`shots18/header-fixed-firefox-nofont-390.png`): same one-line reading in the fallback face — "November" in plain serif, "2026" in tiles, gap visible, line spanning x55–335 but clear of the frame, the orb, and BACK TO MONTH. The worst-case font state still reads as one title line.
- **1920, Chromium/fonts** (`shots18/header-fixed-chromium-fonts-1920.png`): "November 2026" dead-centre at the top of the header with the gap you can see from across the room; "Friday 20" left, time centred below, Your Stats + orb right. Nothing else on the header moved.
- **Deck, 1920, Notifications** (`shots18/census-fixed-…` via `pillcensus18.py`): the notifications panel reads whole with no "Change cover" pill in the corner — the thing he pointed at is gone. On Wisdom and Worlds the pill sits bottom-right where it always did.

## 4. Design laws — delta 0

`check-design-laws.py` on base and fixed (`laws-check18.js`):

- Base: **PASS — 0 FAIL / 28 WARN**
- Fixed: **PASS — 0 FAIL / 28 WARN**
- Warning texts identical (diffed after stripping filename/line); line shifts: first 3 warnings (before the insertion point) unchanged; the other 25 shift by exactly **+42 lines** — the FIX18 block is 41 lines + newline = 42. **Delta 0 in substance, not just in count.**

## 5. §11 check (in writing)

**The five gates:**
1. **Is it right?** Yes — the header now reads as one centred title line (his words), the redundant third Hz mention is gone while the wisdom line keeps both of its mentions, and the pill now appears only where a cover is actually there to change; nothing else on the page changes. No merge, no live deploy, no link to Shawn from this seat.
2. **Is it what they truly need?** Yes — the brief's bar is the three items proven at 1920 AND 390 in both browsers (§3a–3c), plus the fix-17 win held (§3e). The two judgment calls — no reorder at 390 (§2, item 1) and the pill kept on Wisdom + Worlds at both widths (§1, adjudication note) — are named here with their reasons, not hidden.
3. **Is it mine to do?** Yes — the brief + addendum are the authority for exactly these three items; nothing outside them was touched (bytecheck 28/28, fixed-minus-block + Hz-reinsert == base).
4. **Is now the time?** Yes — the defects are measured and reproducible on the filed bytes; the fix is one CSS block + one 100-byte JS string deletion; the round is held from shipping by the captain until the list is complete, so landing it proven now is the right move.
5. **Can I prove it?** Yes — every claim above is a hash, a rect, a pixel count, a hit-test, or a screenshot on the filed bytes (re-derived from the staged link, sha-matched). Nothing is taken on trust.

**The design check (§11, on the rendered page):**
- Could I pick this up? The monthline keeps its harvested objects — script November, digit-tile 2026 — re-spaced, not re-skinned; the pill keeps its pill anatomy where it remains. Nothing flat added (the block adds no colours, no fills, no font sizes). Laws checker: 0 FAIL.
- Light: one source, top-left — the block adds no gradients, no shadows.
- Text: no new font sizes, no new text colours, no wording changed anywhere; nothing under 17px; no gray. The monthline's own text is the harvested script + tiles. Laws delta 0.
- Two same colours together: no colours added, nothing to break the flow.
- Reference objects: the fix reuses the page's own `.hl-center` flex column and the established per-slide `:has()` pattern from the wisdom/worlds rules — one appended CSS block + one string deletion, nothing rebuilt, nothing invented. Harvest, never invent.
- Don't move / don't remove what he didn't ask: the only changes are the monthline's spacing/wrap, the header Hz segment, and the pill's per-slide visibility (all three in §4/addendum). The frame, covers, data, badges, booking logic, nav clearances, and every other slide are byte-identical (§2 of the byte checks; fixed-minus-block + Hz-reinsert == base).
- Read as a reader: the screenshots were read top to bottom as a reader (§3f) — the 390 header reads as one clean title line in both font states, the 1920 header reads centred with daylight between November and 2026, and the Notifications slide reads without the pill.
- **Sense check:** the old 390 header wrapped the title across two lines and parked a redundant Hz line under it — one font-metric shift from wrapping differently again. A nowrap flex line with an exact 24px gap is the fix that stays fixed. On item 3, the old rule showed the pill on slides where the cover is a 1–3px rim and no reader could see a cover — the pill now follows the cover's actual visibility, measured slide by slide, instead of floating everywhere by default.

## 6. Scorecard

| Check | Result |
|---|---|
| Filing (branch, tip, parent, blob, staged sha) | 10/10 |
| Byte-diff discipline (one block + one 100-byte deletion; fix-17 intact) | 10/10 |
| COVER_DAY / WISDOM / booking / badges / monthName intact | 10/10 (bytecheck 28/28) |
| Laws delta | 0 (0 FAIL / 28 WARN both, same texts, +42 line shift explained) |
| Item 1 — "November 2026" centred, one line, gap | 0px offset + 24px gap, all four legs |
| Item 2 — header Hz gone, wisdom untouched | header Hz 0 everywhere; wisdom 2 mentions, byte-identical |
| Item 3 — pill only where a cover shows | wisdom + worlds only, all four legs; Notifications absent both widths/browsers; tap opens picker where it remains |
| Fix-17 hold | 7/7 sweep + 9/9 deck, 2 legs; Appointments nav 2px clear held |
| Page errors | 0 in all legs |
| Buttons (keep-reading / prev-day / back-to-month) | PASS, real taps |
| Month grid (42 / 30 / 12; row 6 blank) | PASS |

**Known thin margins and open points (stated plainly, not hidden):**
- The Appointments nav at 390 is 2px clear of the rim — whole, exactly the fix-15/16 geometry, stable across all measurements in this round.
- At 390 in the Firefox fallback state the monthline is 280px wide in a 240px column (the fallback "November" is 170px wide) — it overflows 20px a side into clear black field and `docScrollW` stays 390; in the fonts-loaded state (what Shawn sees) it is 216px and fits inside the column.
- At 1920 the cover photo is rim-only even on Wisdom and Worlds (see the §1 adjudication note) — the pill is kept there per the addendum's example and the 390 measurement, not per a 1920 pixel reading. The checker may read this differently; the numbers for both readings are in §1.
- At ≤560px the pill now appears on only one slide (Worlds). Change cover at phone width is a Worlds-only doorway until/unless Shawn asks for a phone path on Wisdom.
- The 390 header compresses 32px (monthline 2 lines → 1); the deck moves up with it. Deck-internal geometry is re-proven whole (§3e).
- Round time ran past the one-hour target (the item-3 census needed three method corrections — hash-only and global-freeze both lied before the pixel-diff-with-baseline method landed the truth). The work is landed proven; the time is named here, not hidden.
- **Held from shipping** per the brief — Shawn may add more calendar items; the captain confirms the list is complete before this ships. The ultimate appointment creator is a separate round and was not touched.

## 7. Files (all under `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/`)

- `maker/MAKER-REPORT.md` — this report.
- `maker/proof/fix18-block.css` — the fix (3,249 B: monthline flex + gap, item-3 rule).
- `maker/proof/fixed-fix18.html` — the filed bytes (413,386 B, sha256 `52ff950f…`).
- `maker/proof/base-fix17.html` — the verified base (410,236 B, sha256 `1f798b65…`).
- `maker/proof/fetched-fixed.html` / `fetched-base.html` / `fetched-staged.html` — blob-API + staged-link read-backs (hash-matched).
- `maker/proof/build-fixed18.js` — byte-safe build (Buffer ops) + scope proof.
- `maker/proof/bytecheck18.js` — byte regression (28/28 PASS).
- `maker/proof/laws-check18.js` + `laws-base18.txt` + `laws-fixed18.txt` — laws delta 0.
- `maker/proof/fetch-verify18.js` + `file18-step1.js` + `make-body18.js` + `put18.log` — filing + verification.
- `maker/proof/measure18.py` + `measure-base-*.log` + `measure-fixed-*.log` — header geometry, all four legs, base + fixed.
- `maker/proof/census18.py` + `covercensus18.py` / `covercensus318.py` + `covercensus3-*.log` + `diffvis*.py` — the item-3 cover-visibility census (including the two false methods, kept so nobody re-learns them).
- `maker/proof/pillcensus18.py` + `pillcensus-fixed-*.log` — per-slide pill census on the fixed bytes, all four legs.
- `maker/proof/prove18.py` + `prove18-ff-nofont-390.log` + `prove18-cr-fonts-1920.log` — fix-17 hold regression.
- `maker/proof/tap18.py` — Change-cover tap test (native file picker).
- `maker/proof/shots18/` — screenshots (header + full + census + diff overlays per leg).
- `maker/proof/forwarder18.log` — Chromium proxy forwarder log (started for the Chromium legs, killed by PID when done; no process remains).
