# CAL-FIX18 — CHECKER REPORT

**Checker:** independent (did not build) · **Date:** 2026-11-20 ~15:30–16:10 UTC (VM clock)
**Verdict: PASS — all three items are fixed and re-proven by my own drivers, in all four legs, with no other geometry changed.**

No merge, no live deploy, no link to Shawn. The captain's eye may follow. The round is held from shipping until the captain confirms the list is complete.

## Verdict in one line

"November 2026" reads as one centred title line at both widths in both font states with an exact 24px gap; the header Hz is gone while the wisdom line keeps both of its 396 Hz mentions; the "Change cover" pill is gone from Notifications and every other content slide and remains only on Wisdom + Worlds, opening the file picker where it remains — proven per slide per leg with my own pixel-diff cover census, with the fix-17 win held whole.

## 1. Filing — PASS (re-derived via the git blob API, never the maker's word)

Re-derived with `checker/proof/verify18c.js` (`gh-direct.py` only, blob API):

| Claim | Re-derived |
|---|---|
| Branch `calendar/day-followon-fix18-20261120` | HTTP 200, tip `ffd220c7d7d54fbbfc08c82ceed793ce1b0968a3` — matches |
| Parent = fix-17 tip | Commit parents `['a955d7fa2299a6667ba70215dd4347c1de80386e']` — matches |
| Commit message | `Calendar day-view fix-18: November 2026 centered title line (24px gap), 396 Hz off the header, Change cover only where a cover shows (wisdom + worlds)` |
| Filed blob `f7b14ce75d590738a9efb87a4fa056ee98f3561d` | **413,386 B**, sha256 `52ff950fb4dfeb942415c96ee2af393b815e06e9019c77a9758121a9f40770cc` — matches |
| Base blob `f4c05109531f8b737891a43f6ea6bdcef84eddc9` | **410,236 B**, sha256 `1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887` — matches |
| Rebuilt (base − Hz segment + claimed block before `</style>`) | 413,386 B, sha256 `52ff950f…` — **rebuilt == filed blob: true** |
| Fixed-minus-block + Hz-reinsert == base | **true** (byte-level, Buffer ops — see note below) |
| Staged link serves the filed blob | HTTP 200, 413,386 B, sha256 `52ff950f…` — **exact match** |

**Harness note (not a defect):** my first reverse-scope attempt printed `false` because it spliced with a *string* index into a *Buffer* — the file contains multi-byte UTF-8, so the string index landed mid-character. Redone with pure byte-level anchors (`dayDigitsHTML(d.getFullYear(), dc)` + the Hz segment), the reverse check is `true`. The forward rebuild (base − Hz + block == filed) passed on the first run and is the strong direction; both directions now agree.

## 2. Byte-diff — PASS (on the fetched bytes)

- Fix-18 block present exactly once, immediately before `</style>`; prefix and suffix match base byte for byte. Delta 3,150 B = block 3,249 B + Hz-segment deletion (−100 B) + newline.
- Hz segment: the exact old string occurs **1× in base, 0× in fixed**; the new tail `+ '</span>'` occurs 1× in fixed at the monthline (anchored). The deletion removes exactly one `DAY_FREQ` *usage* (3 → 2 occurrences); the `DAY_FREQ` data array itself (`[963, 417, 528, 741, 639, 396, 852]`) is byte-identical, as are `DAY_COLORS` / `DAY_MEANING`.
- `COVER_DAY` byte-identical (3 occurrences both sides); `WISDOM` +2 and `dayTeach` +1 are exactly the fix-18 block's own comment mentions (verified by counting inside `fix18-block.css`: `WISDOM` 2, `dayTeach` 1). The `#dayTeach` assignment line (`__dt.innerHTML=…DAY_FREQ…Hz…DAY_MEANING…`) is byte-identical base→fixed. `monthName` contexts identical.
- `396` literal count unchanged, 7 → 7 (the header 396 was runtime-rendered from `DAY_FREQ[5]`, never a literal — as the maker states).
- Fix-17 block intact in the fixed bytes (byte-identical occurrence); fix-17 placement geometry (`top:40px`, wisdom hide ≤560px) untouched.
- No JS changes except the one Hz-segment deletion; booking logic, badges, `renderMonth()` untouched (proven by render in §6, not by regex alone).
- Structural tags: `</style>`, `</script>`, `</html>` counts 1/1/1 in both.

## 3. Render — the three items (all four legs, my own harness)

Method: my own harness `checker/proof/check18.py` (Playwright sync; 2-second waits after every deck navigation; slides forced via the dots `#dayScroll .sb-dots button`). Firefox = no-webfont fallback (worst case; `document.fonts` empty); Chromium 156 via the localhost forwarder = fonts-loaded (verified `Great Vibes:loaded`, `Marcellus:loaded`). All runs on the fetched fixed bytes (sha256 `52ff950f…`, re-verified after the runs). **0 page errors in every leg.**

### 3a. Item 1 — "November 2026" centred, one line, 24px gap (day 20)

| Width / font state | Monthline text | Centre offset (cx − viewport centre) | November→2026 gap | One line? |
|---|---|---|---|---|
| 1920, Firefox, fallback | `November 2026` | **0px** (960 = 960), x799–1122, w323 | **24px** | yes (h37; nov cy 152 = year cy 152) |
| 1920, Chromium, fonts-loaded | `November 2026` | **0px** (960 = 960), x831–1090, w259 | **24px** | yes (h37; nov cy 152 = year cy 152) |
| 390, Firefox, fallback | `November 2026` | **0px** (195 = 195), x55–335, w280 | **24px** | yes (h32; nov cy 156 = year cy 156) |
| 390, Chromium, fonts-loaded | `November 2026` | **0px** (195 = 195), x87–303, w216 | **24px** | yes (h32; nov cy 156 = year cy 156) |

Neighbours untouched in every leg: "Friday 20" left (1920: x392; 390: centred in its own row, y100–132, as in base); time row directly under the monthline, centred (cx 960 / 195, 19–20px below the monthline bottom); BACK TO MONTH left; Your Stats + orb right (stats x1388–1528 at 1920, x125–265 at 390; orb x1711–1775 / x300–336 — identical to base). The monthline carries exactly **1** `.os-mini-num` span (the year) in every leg.

**Method note (not a finding):** my Range-tops line counter reported "2 lines" in every leg (tops 6–11px apart). That counter collects distinct tops of text-node Range rects — the script glyph's ink top and the digit-tile text top differ by a few px *within one line box*. The one-line verdict rests on the box: monthline height 32–37px (the base at 390 FF measured **64px** wrapped — §3e), November and the 2026 tiles sharing one centre line (cy equal in all four legs), and the screenshots read as a reader (§7). I record the artifact so nobody re-litigates it.

### 3b. Item 2 — no "396 HZ" in the header; wisdom untouched (all four legs)

- Rendered header text, all four legs: `Friday 2 0 November 2 0 2 6 <time> Your Stats` — no `HZ`, no `396` anywhere in the header (`headerHasHz: false` in every leg; element census: monthline contains exactly 1 `.os-mini-num` span, the year; no Hz span).
- Wisdom line, all four legs, byte + render: `Friday · 396 Hz · red — The day of the ground — the root, 396 Hz. Stand firm; finish what stands.` — **two mentions**, exactly as in base. `WISDOM` quote untouched (§2).

### 3c. Item 3 — per-slide pill census on the filed bytes (day 20, all four legs)

| Slide | 1920 FF | 1920 Cr | 390 FF | 390 Cr |
|---|---|---|---|---|
| 0 Wisdom | **shown** 1635, 795–835, hit `BUTTON.pill:Change cover` | **shown** 1633, 800–835, hit-testable | hidden (fix-17) | hidden (fix-17) |
| 1 Notifications | hidden (0×0, `display:none`) | hidden | hidden | hidden |
| 2 Journal | hidden | hidden | hidden | hidden |
| 3 Your Worlds | **shown** 1635, 795–835, hit-testable | **shown** 1633, 800–835, hit-testable | **shown** static-flow 175, 768–808, hit-testable | **shown** static-flow 173, 773–808, hit-testable |
| 4 News Hub | hidden | hidden | hidden | hidden |
| 5 Appointments | hidden | hidden | hidden | hidden |
| 6 Summary | hidden | hidden | hidden | hidden |
| 7 Naya Notes | hidden | hidden | hidden | hidden |
| 8 Smart Notes | hidden | hidden | hidden | hidden |

Notifications pill-absent at both widths, both browsers, as Shawn asked. The `:not(:has())` selector works in both browsers — the pill is `display:none` with a 0×0 rect on all seven content slides in Firefox and Chromium alike.

### 3d. The pill still works where it remains (real taps, native file picker)

`expect_file_chooser` taps in every leg: **1920 Wisdom → OPENED; 1920 Worlds → OPENED; 390 Worlds → OPENED** (both browsers). 390 Wisdom → pill hidden, not clickable (fix-17). 1920/390 Notifications → pill hidden, not clickable.

### 3e. My own cover-visibility census (pixel diff, cover on vs cover off)

Method (my own, validated before trusting its numbers): per slide, after the 2s settle, pause animations with `document.getAnimations().forEach(a => a.pause())` only — no persistent style tag — then screenshot the `#dayScroll` rect with the cover shown twice (drift baseline) and once with `#dayCoverBg` set `display:none`. Count interior pixels (>6px inset) whose RGB sum differs by >60. Drift was **0px on every slide in every leg** — the pause works and the numbers below are signal, not animation noise. Day 20, Friday, `friday_red.jpg` (bright red, unmistakable where it shows).

| Slide | 390 FF (drift) | 390 Cr (drift) | 1920 FF (drift) | 1920 Cr (drift) |
|---|---|---|---|---|
| 0 Wisdom | **23,298** (0) | **48,469** (0) | 262 (0) | 304 (0) |
| 1 Notifications | 269 (0) | 291 (0) | 126 (0) | 159 (0) |
| 2 Journal | 273 (0) | 291 (0) | 129 (0) | 159 (0) |
| 3 Worlds | **12,660** (0) | **11,888** (0) | 126 (0) | 159 (0) |
| 4 News Hub | 269 (0) | 291 (0) | 126 (0) | 159 (0) |
| 5 Appointments | 272 (0) | 290 (0) | 130 (0) | 163 (0) |
| 6 Summary | 267 (0) | 289 (0) | 129 (0) | 162 (0) |
| 7 Naya Notes | 269 (0) | 291 (0) | 126 (0) | 159 (0) |
| 8 Smart Notes | 272 (0) | 289 (0) | 126 (0) | 162 (0) |

Reading: at 390 the cover photo is plainly visible as a solid band below the slide content on Wisdom (23k–48k px) and Worlds (12k px) and on no other slide (~270–290 px = the 1–3px rim). At 1920 the content fills the deck on every slide (126–304 px = rim only). My numbers confirm the maker's census in kind and in scale on every slide (their 390 FF: 14,371 / 12,900 / 332–339; mine differ in absolute count because my clip is the whole deck rect and my threshold differs — the verdict per slide is identical).

## 4. Adjudication points — ruled with my own evidence

### Point 1 — Pill kept on Wisdom + Worlds at 1920, where the cover is rim-only. **RULED: SATISFIES the bar. PASS.**

My 1920 measurements confirm the maker's open point: the cover photo is rim-only at 1920 even on Wisdom (262 FF / 304 Cr interior px) and Worlds (126 / 159 px) — no reader at 1920 can see the cover photo on either slide. On a strict per-width pixel reading, the 1920 pill fails "actually visible to change".

I do not apply the strict per-width reading, for three reasons, all grounded in the brief and the measurements:

1. **The addendum names Wisdom as the keeper without width qualification** ("e.g. the wisdom slide, where the day's cover is the board's background") — the cover is the board's background as a property of the slide, not of the viewport.
2. **"Actually visible" is a slide property, and the slide-level test is decisive:** on Wisdom and Worlds the cover is the slide's backdrop and shows plainly whenever the content leaves deck exposed — proven at 390 (23,298–48,469 px on Wisdom, 11,888–12,660 px on Worlds). On the other seven slides the cover never shows at *either* width (≤291 px at 390, ≤163 px at 1920) — rim at both. The pill rule draws exactly that line: cover slides vs content slides. Notifications is the proof: no cover visible at any width, pill gone at both.
3. **The strict reading produces an absurd outcome:** at 1920 no slide exceeds 304 px, so a per-width rule would hide Change cover on *every* slide at desktop — removing a working function from the surface where Shawn works, which he never asked for. The pill changes the same cover the 390 reader sees; the 1920 reader changes it blind only in the sense that the content currently fills the deck.

Recorded plainly so the captain can overrule: if Shawn wants the strict per-width rule, the fix is a width-gated pill (hide on Wisdom/Worlds above 560px) — but I recommend against it, and it is his call, not a GOES BACK from this seat. The numbers for both readings are in §3e.

### Point 2 — At ≤560px the pill now shows on only one slide (Worlds). **CONFIRMED — that is what the two instructions produce.**

390 census: Wisdom hidden (fix-17 rule, brief-sanctioned), Worlds shown (static-flow 768–808 / 773–808), the other seven hidden (item 3). Change cover at phone width is therefore a Worlds-only doorway; at desktop it is Wisdom + Worlds. That is the combined outcome of Shawn's fix-17 sanction and his item-3 instruction — named plainly, not a silent choice, and not a defect. The wisdom slide at 390 reads clean without the pill (§7); the function is one swipe away (Worlds) and present on every slide at desktop.

### Point 3 — 390 Firefox-fallback monthline: 280px in a 240px column. **VERIFIED — no scroll, no clipping, reads clean. PASS.**

My measurements: monthline x55–335, w280, overflowing the 240px centre column 20px a side into clear black field; `docScrollW` stays **390** in every leg. Neighbours are clear of it: BACK TO MONTH y48–94, orb y54–90, "Friday 20" y100–132 — the monthline (y140–172) overlaps none of them. The screenshot reads as one clean title line in the fallback face (§7). In the fonts-loaded state (what Shawn sees) the line is 216px and fits inside the column. The overflow is a worst-case-font-state property of the 170px fallback "November", not a layout break.

### Point 4 — 390 header compresses 32px; deck moves up with it. **VERIFIED — deck geometry whole in all four legs. PASS.**

My own base-vs-fixed measurement at 390 Firefox: base monthline h64 (two lines), stats 248–292, timewrap 206–240, deck top 312; fixed monthline h32, stats 216–260, timewrap 174–208, deck top 280. **Every anchor moves up exactly 32px; the deck moves up with it.** Deck geometry re-proven whole: sweep 7/7 + deck 9/9 in all four legs (§6); nav clearances held (worst Appointments 2px at 390, as in fix-15/16; wisdom worst day 43px clear at 390 FF, improved from 10px in fix-17); Change-cover clearances held (Worlds pill 768–808 hit-testable; wisdom pill hidden at 390).

## 5. The no-reorder judgment (item 1) — **RULED: the maker's call is correct. PASS.**

The maker did not move the monthline above "Friday 20" at 390. I judge that call right, on the page:

- **At 1920** the monthline is literally at the top of the header (y134, same row as BACK TO MONTH / "Friday 20" / Your Stats) — the strict reading of "center it at the top of the header" is satisfied outright.
- **At 390** the header stacks: BACK TO MONTH, "Friday 20", then "November 2026", then the time row, then Your Stats. The monthline is the centred title line at the top of its column, directly above the time row. It reads as the title — the biggest, centred line in the header, with daylight between November and 2026 (§7).
- A reorder above "Friday 20" at 390 would invert the natural date order (weekday → month-year) and contradict the brief's own stay-put constraints ("Friday 20 stays left", "the time row below stays where it is"). The brief's §4 reads as one instruction: re-centre and re-space the line *where it sits*, above the time row — which is exactly what landed. If Shawn wants it above "Friday 20" on phones, that is a reorder round with its own brief.

## 6. Fix-17 hold — PASS (full regression on the filed bytes, all four legs)

| Leg | Wisdom sweep 7 days | Deck 9 slides | Buttons | Month | Page errors |
|---|---|---|---|---|---|
| 390, Firefox, fallback | **7/7 PASS** (worst day Sat 21: nav 722–766, **43px clear**; pill hidden all 7 days) | **9/9 PASS** (Appointments nav 2px clear held; Worlds pill 768–808 hit-testable) | Keep-reading Thu 19 → Fri 20, prev-day returns it; monthline `November 2026` throughout | 42 / 30 / 12, row 6 all blank | 0 |
| 390, Chromium, fonts-loaded | **7/7 PASS** (worst day nav 127px clear; pill hidden all 7 days) | **9/9 PASS** (Appointments nav 2px clear held) | Keep-reading / prev-day as above | 42 / 30 / 12, row 6 all blank | 0 |
| 1920, Firefox, fallback | **7/7 PASS** (nav 820–882, 18px clear every day; pill 795–835 on wisdom, clear of weather pill) | **9/9 PASS** (nav 820–882, 18px clear every slide; pill hit-testable on wisdom + worlds, hidden elsewhere) | Keep-reading / prev-day as above | 42 / 30 / 12, row 6 all blank | 0 |
| 1920, Chromium, fonts-loaded | **7/7 PASS** (nav 824–882, 18px clear every day; pill 800–835 on wisdom) | **9/9 PASS** (nav 824–882, 18px clear every slide) | Keep-reading / prev-day as above | 42 / 30 / 12, row 6 all blank | 0 |

Greeting true to VM clock (UTC) in all legs ("Good afternoon, Shawn."); `docScrollW` == viewport width in every run (no horizontal overflow at 390 or 1920). Buttons proven by real taps with the full header text as the witness (Thu 19 → Fri 20 → Thu 19), not by the monthline alone — the monthline is "November 2026" on both days, so the weekday+day digits are the proof.

**Harness note (not a defect):** my first Firefox-390 run scored the sweep 0/7 because the cover census before it had left the deck on slide 8, and the day re-opens on the last-viewed slide — so the wisdom banner wasn't active when I measured it. That was my probe's order, not the page: forcing slide 0 via the dots before each sweep measurement gives 7/7. Recorded so nobody re-learns it: **a sweep must force its slide after every open_day, not just once.**

## 7. Read as a reader (screenshots, top to bottom, the way he reads it)

- **390, Chromium/fonts** (`shots18c/header-chromium-fonts-390.png` — what Shawn sees on phone): "Friday" in script, "20" tiles, then "November" in Great Vibes script with clear daylight, then the "2026" tiles — one centred line, time below, Your Stats below. It reads nice and clean, exactly as he asked.
- **390, Firefox/fallback** (`shots18c/header-firefox-nofont-390.png`): the same one-line reading in the fallback face — "November" in plain serif, "2026" in tiles, gap visible, line spanning x55–335 but clear of the frame, the orb, and BACK TO MONTH. The worst-case font state still reads as one title line.
- **1920, Chromium/fonts** (`shots18c/header-chromium-fonts-1920.png`): "November 2026" dead-centre at the top of the header with the gap you can see from across the room; "Friday 20" left, time centred below, Your Stats + orb right. Nothing else on the header moved.
- **1920, Firefox/fallback, Wisdom** (`shots18c/census-firefox-nofont-1920-0.png`): the wisdom board fills the deck; the cover photo is not visible as a photo — only the thin red rim at the deck edge. The "Change cover" pill sits bottom-right, whole. This screenshot is the visible evidence behind adjudication point 1.
- **390, Firefox/fallback, Wisdom** (`shots18c/full-firefox-nofont-390-day20.png`): greeting, quote, teach line with both 396 Hz mentions in red, store line, dots and nav whole — and the red cover photo plainly visible as the band below the board, which is why the pill belongs to this slide. The slide reads clean without the pill at phone width.
- **390, Firefox/fallback, Notifications** (`shots18c/census-firefox-nofont-390-1.png`): the notifications panel reads whole with no "Change cover" pill in the corner — the thing he pointed at is gone.

## 8. Laws — PASS, delta 0 (`checker/proof/laws-base18c.txt` / `laws-fixed18c.txt`)

- Base: **PASS — 0 FAIL / 28 WARN**. Fixed: **PASS — 0 FAIL / 28 WARN**.
- Warning texts identical (diffed after stripping filename/line). Line shifts: first 3 warnings (before the insertion point) unchanged; the other 25 shift by exactly **+42 lines** — the FIX18 block is 41 lines + newline = 42. **Delta 0 in substance, not just in count.**

## 9. §11 check (in writing)

**The five gates:**
1. **Is it right?** Yes — the check removes nothing and adds nothing; it re-proves the fix from the filed bytes with its own drivers, including its own cover-visibility census. No merge, no live deploy, no link to Shawn from this seat.
2. **Is it what they truly need?** Yes — the brief's bar is the three items proven at 1920 AND 390 in both browsers (§3), plus the fix-17 win held (§6). The four adjudication points are ruled here with their evidence (§4–§5), not waved through — including the one place the maker's rule and a strict pixel reading differ (point 1), where I rule for the slide-level reading and record the strict alternative for the captain.
3. **Is it mine to do?** Yes — checking is exactly this seat's brief; the fix itself belongs to the maker round, already filed.
4. **Is now the time?** Yes — the defects are measured and reproducible on the filed bytes; the round is held from shipping by the captain until the list is complete, so landing it proven now is the right move.
5. **Can I prove it?** Yes — every claim above is a hash, a rect, a pixel count, a hit-test, or a screenshot on the fetched filed bytes (proven identical to the staged link in §1). Nothing is taken on trust from the maker's report; where my first strict check flagged something (the reverse-scope `false`, the 0/7 sweep, the "2 lines" counter), I re-proved it with the corrected measurement instead of passing it through.

**The design check (§11, on the rendered page):**
- Could I pick this up? The monthline keeps its harvested objects — script November, digit-tile 2026 — re-spaced, not re-skinned; the pill keeps its pill anatomy where it remains. Nothing flat added (the block adds no colours, no fills, no font sizes). Laws checker: 0 FAIL.
- Light: one source, top-left — the block adds no gradients, no shadows.
- Text: no new font sizes, no new text colours, no wording changed anywhere; nothing under 17px; no gray. The monthline's own text is the harvested script + tiles. Laws delta 0.
- Two same colours together: no colours added, nothing to break the flow.
- Reference objects: the fix reuses the page's own `.hl-center` flex column and the established per-slide `:has()` pattern from the wisdom/worlds rules — one appended CSS block + one string deletion, nothing rebuilt, nothing invented. Harvest, never invent.
- Don't move / don't remove what he didn't ask: the only changes are the monthline's spacing/wrap, the header Hz segment, and the pill's per-slide visibility (all three in §4/addendum). The frame, covers, data, badges, booking logic, nav clearances, and every other slide are byte-identical (§2; fixed-minus-block + Hz-reinsert == base).
- Read as a reader: the screenshots were read top to bottom as a reader (§7) — the 390 header reads as one clean title line in both font states, the 1920 header reads centred with daylight between November and 2026, and the Notifications slide reads without the pill.
- **Sense check:** the old 390 header wrapped the title across two lines and parked a redundant Hz line under it — one font-metric shift from wrapping differently again. A nowrap flex line with an exact 24px gap is the fix that stays fixed. On item 3, the old rule showed the pill on slides where the cover is a 1–3px rim and no reader could see a cover — the pill now follows the cover's actual visibility, measured slide by slide, instead of floating everywhere by default. The one place the rule and a strict pixel reading differ (1920 Wisdom/Worlds) is ruled in §4 point 1 with the reasoning and the alternative named.

## 10. Scorecard

| Check | Result |
|---|---|
| Filing (branch, tip, parent, blob, staged sha) | 10/10 |
| Byte-diff discipline (one block + one 100-byte deletion; fix-17 intact) | 10/10 |
| COVER_DAY / WISDOM / booking / badges / monthName intact | 10/10 |
| Laws delta | 0 (0 FAIL / 28 WARN both, same texts, +42 line shift explained) |
| Item 1 — "November 2026" centred, one line, gap | 0px offset + 24px gap, all four legs |
| Item 2 — header Hz gone, wisdom untouched | header Hz 0 everywhere; wisdom 2 mentions, byte-identical |
| Item 3 — pill only where a cover shows | wisdom + worlds only, all four legs; Notifications absent both widths/browsers; tap opens picker where it remains |
| Cover visibility (own pixel-diff census, drift 0) | band on Wisdom + Worlds at 390 only; rim-only elsewhere and at 1920 |
| Fix-17 hold | 7/7 sweep + 9/9 deck, all four legs; Appointments nav 2px clear held |
| Page errors | 0 in all legs |
| Buttons (keep-reading / prev-day / back-to-month) | PASS, real taps, header-text witness Thu 19 → Fri 20 → Thu 19 |
| Month grid (42 / 30 / 12; row 6 blank) | PASS |
| Adjudications 1–4 | Ruled with evidence (§4); no-reorder ruled correct (§5) |

**Known thin margins and open points (stated plainly, not hidden):**
- The Appointments nav at 390 is 2px clear of the rim — whole, exactly the fix-15/16 geometry, stable across all measurements in this round.
- At 390 in the Firefox fallback state the monthline is 280px wide in a 240px column — it overflows 20px a side into clear black field and `docScrollW` stays 390; in the fonts-loaded state (what Shawn sees) it is 216px and fits inside the column.
- At 1920 the cover photo is rim-only even on Wisdom and Worlds (§4 point 1) — the pill is kept there per the addendum's example and the 390 measurement, not per a 1920 pixel reading. The strict-reading alternative and its fix are named in §4; the captain can overrule.
- At ≤560px the pill now appears on only one slide (Worlds). Change cover at phone width is a Worlds-only doorway until/unless Shawn asks for a phone path on Wisdom.
- The 390 header compresses 32px (monthline 2 lines → 1); the deck moves up with it. Deck-internal geometry is re-proven whole (§6).

## 11. Files (all under `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/`)

- `checker/CHECKER-REPORT.md` — this report.
- `checker/CAL-FIX18-CHECKER-BRIEF.md` — the checker brief.
- `checker/proof/verify18c.js` — filing re-derivation (branch, tip, parent, blob, staged) + scope rebuild.
- `checker/proof/fetched-fixed.html` (413,386 B, sha256 `52ff950f…`) / `fetched-base.html` (410,236 B, sha256 `1f798b65…`) / `fetched-staged.html` (413,386 B, sha256 `52ff950f…`) — blob-API + staged-link read-backs (hash-matched).
- `checker/proof/check18.py` — my own four-leg probe (header, pill census, cover-visibility pixel diff, sweep, deck, buttons, month, tap test).
- `checker/proof/check18-firefox-nofont-390.log` / `check18-firefox-nofont-1920.log` / `check18-chromium-fonts-390.log` / `check18-chromium-fonts-1920.log` (+ `check18-ff-nofont-390.log`, first-run artifact log) — per-leg outputs.
- `checker/proof/laws-base18c.txt` / `laws-fixed18c.txt` (+ `.norm` diffs) — laws delta 0.
- `checker/proof/shots18c/` — 156 screenshots (header, full, per-slide census, per-slide cover on/off pairs, month per leg).
- `checker/proof/forwarder18c.log` — Chromium proxy forwarder log (started for the Chromium legs, killed by PID 149386 when done; no process remains).

## 12. Environment notes (for the coordinator)

- **VM browsers alive throughout this check** (Firefox launch OK; Chromium 156 via the localhost forwarder, `ignore_https_errors=True`; forwarder killed by PID, confirmed gone).
- **Slide transitions take >900ms to settle** — all re-proofs used 2s waits after deck navigation.
- **Day re-opens on the last-viewed slide** (state kept) — per-slide targeting forced the slide via the dots; a sweep must force its slide after every open_day (§6 note).
- **VM clock is UTC** — greetings read against UTC ("Good afternoon, Shawn." at ~15:xx–16:xx UTC), per the brief.
- **Two probe lessons, recorded so nobody re-learns them:** (1) a string index into a Buffer is not a byte index — reverse-scope splices must use byte-level anchors when the file has multi-byte UTF-8 (§1 note); (2) a Range-tops line counter counts glyph ink tops, not lines — one-line verdicts rest on the box height + shared centre line + the screenshot (§3a note).
- **No EPERM write failures** in this check: all checker writes went through the file tool / Node and were verified by size + sha. No `python3 … > file` redirections were used.
