# CAL-FIX17 — Maker Report

**Verdict: FIXED and FILED — all three §9 items proven on the filed bytes, in all four legs.**
**Date:** 2026-11-20 (VM clock UTC; user asleep, silent work, no message sent)
**Maker:** Calendar day-followon fix-17, Team Nitro

## Filing identity

| Item | Value |
|---|---|
| Base branch | `calendar/day-followon-fix16-20261119`, tip `572265f25d80146fb9d8a1ff7f3bb56215143f0d` |
| Base file | `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html` |
| Base blob | `cc67fbf98388fbcbcf26287d82f3a81eb9d5d7c3`, 407,135 B, sha256 `ffc03030c555f034dd1608d3f78996d8c6455a963462bec5e51b64fa8e548ca3` |
| New branch | `calendar/day-followon-fix17-20261119` (created from the fix-16 tip, HTTP 201) |
| Filed commit | `f8500a845dd6501f104319aa53d53ba11359802c` (parent `572265f2…`) |
| Filed blob | `f4c05109531f8b737891a43f6ea6bdcef84eddc9`, **410,236 B**, sha256 `1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887` |
| Staged link | `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix17-20261119&cb=f4c05109531f8b737891a43f6ea6bdcef84eddc9` |
| Verification | Filed blob re-read via the git blob API: 410,236 B, sha256 `1f798b65…`, byte-identical to the local fixed file; rebuilt (base + claimed block) == filed blob; filed-minus-block == base. Staged link curled with a browser User-Agent: 410,236 B, sha256 `1f798b65…` — matches the filed blob. |

## 1. Defect reproduction — root cause (measured on the fix-16 bytes first)

The "Change cover" pill is ONE element, a child of `#dayScroll`, floating over the deck on every slide. Its base rule pins it `bottom:84px` — at 390 that is y696–736 (Firefox fallback) / y701–736 (Chromium fonts), right where slides put content. I re-measured the defects on the base bytes before designing the fix (full per-slide element dumps, `dump17.py`, both browsers — every visible leaf element, not just buttons):

- **Wisdom 390 fallback:** the static-flow pill lands 778–818 (5-line days), 811–851 / 830–870 (6-line days) against the fixed weather pill 804–840 — 6/7 days overlapping. Chromium fonts state already clears (708–743).
- **Appointments 390, both browsers/states:** Smart Meet pill 678–737 (FF) / 673–726 (Cr); Change cover 696–736 / 701–736; `elementFromPoint` at the pill's center AND bottom returns `BUTTON.pill:Change cover`. The pill has no scroll path (`sbScroll` 359/359) — the fix-16 "2px spare" measured the scroll container, the wrong reference object; the checker was right and the fix-16 claim was false.
- **Summary 390, Chromium fonts:** "Your Journal" door 693–791 vs Change cover 701–736 — overlapped at rest (scroll-reachable, but clipped at rest).
- At 1920 the pill sits at the right (x1635, y795–835) clear of everything — no collision in any 1920 leg.

## 2. The fix — one CSS block, inserted before `</style>`

File: `maker/proof/fix17-block.css` (3,100 B). The fixed file is the base plus exactly this block — verified `fixed-minus-block == base` (bytecheck17.js). No JS, no data, no markup touched. No wording, color, or font size changed (no font sizes and no hex colors in the block at all).

| Rule | Mechanism | Why |
|---|---|---|
| **(1) Floating pill to the top of the deck** `#dayScroll>.cover-change{top:40px!important;bottom:auto!important}` (≤560px only) | Moves the pill from the collision band (y696–736) to the one band measured empty on every floating slide in BOTH font states: the gap between the dots row and the slide title. Dots end y342 (FF) / y337 (Cr); the lowest title top is y404 (FF) / y400 (Cr); the Back pill ends x156. `top:40px` puts the pill at y352–392 (FF, 40 tall) / y348–383 (Cr, 35 tall) — 10–11px clear of the dots above, 12–21px clear of the titles below, 19px clear in x of Back. Same selector as the base floating rule, later in the file, so it wins; the wisdom/worlds `:has()` rules outrank it and keep their own forms. | One spot, same on every slide — predictable, and uniformly clear with ≥10px margins everywhere, where the old band was 1px clear of the Notifications blocks and 8px clear of the Naya Notes button. |
| **(2) Wisdom: pill hidden** `#dayScroll:has(#wisdomBanner.on)>.cover-change{display:none!important}` (≤560px only) | The brief's sanctioned option. Wisdom has NO free band: the orb fills the top (y312–352, x177–213 — this killed my first idea, a top-right placement), the hello/label/quote fill the middle, and the nav-to-weather gap varies by day from 90px (day 17) to 5px (day 21) — no fixed spot fits all 7 days. Same specificity as the wisdom static-flow rule, later in the file, so `display:none` wins. | The pill stays visible and clear on the other 8 slides at phone width and on every slide at desktop, so cover-change is never more than one swipe away. The `#dayScroll` overflow + `#wisdomBanner` flex rules from the wisdom block are separate rules and are untouched. |

**Worlds untouched:** its `:has(.worlds-slide.on)` static-flow rule outranks the new rule, so it keeps flowing below the slide (768–808, 1px above the rim, whole) — as the brief requires ("do not touch").

**Two measured non-levers (recorded so nobody re-learns them):**
- The wisdom top-right corner is occupied by the avatar jewel (y312–352) — a top placement there would cover the orb. Found by the full element dump, not by the button-only probe.
- No fixed bottom spot fits wisdom on all days: the nav bottom moves 714–799 across the 7 days while the weather pill stays at 804–840, so the gap collapses to 5px on day 21. Any absolute `bottom:` value collides on some day.

## 3. Re-proof — final filed bytes

All runs on the filed bytes (`fixed-fix17.html`, sha256 `1f798b65…`), real render, real taps, 2s waits after every deck navigation. 0 page errors in every run. VM clock is UTC; the greeting follows it ("Good afternoon, Shawn." at ~12:xx UTC — true to time of day).

### 3a. 7-day wisdom sweep, Nov 15–21 (teach + store whole, weather pill one line, nav whole, Change cover vs weather = none)

| Width / font state | Result | Worst day (nav clear of rim) | Change cover |
|---|---|---|---|
| 390, Firefox, **no-webfont fallback** (worst: 6-line quotes) | **7/7 PASS** | Sat 21: nav 755–799, **10px clear**; pill clear 56px | **hidden all 7 days, overlap none** |
| 390, Chromium + forwarder, **fonts-loaded Great Vibes** | **7/7 PASS** | Sat 21: nav 633–677, **132px clear**; pill clear 178px | **hidden all 7 days, overlap none** |
| 1920, Firefox, fallback | **7/7 PASS** | Every day: nav 820–882, **18px clear** | visible 795–835, overlap none |
| 1920, Chromium, fonts-loaded | **7/7 PASS** | Every day: nav 824–882, **18px clear** | visible 800–835, overlap none |

Greeting true on all seven days in both font states; `docScrollW` == viewport width in every sweep (no horizontal overflow at 390 or 1920); Back never overlaps the greeting.

### 3b. Whole 9-block deck walk, day 19 — Change-cover overlap per slide, all four legs

Change cover at 390: **352–392 (FF) / 348–383 (Cr)** on slides 1, 2, 4, 5, 6, 7, 8; **hidden** on wisdom (slide 0); **768–808 (FF) / 773–808 (Cr)** static on Worlds (slide 3). At 1920: **795–835 (FF) / 800–835 (Cr)** on every slide. Overlap vs weather pill and vs every on-slide button: **none, on every slide, in every leg.** `elementFromPoint` at the pill's center returns `BUTTON.pill:Change cover` itself wherever it is visible (tappable).

| Slide | 1920 FF (nav clear) | 1920 Cr (nav clear) | 390 FF (nav clear) | 390 Cr (nav clear) |
|---|---|---|---|---|
| Wisdom | 820–882 (18) | 824–882 (18) | 703–747 (62) | 633–677 (132) |
| Notifications | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Journal | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Your Worlds | 820–882 (18) | 824–882 (18) | 685–745 (64) | 694–750 (59) |
| News Hub | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Appointments | 820–882 (18) | 824–882 (18) | 747–807 (**2**, whole as in fix-15/16) | 751–807 (**2**) |
| Summary of the day | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Naya Notes | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Smart Notes | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |

**9/9 PASS in all four legs.** The Appointments nav at 390 is 2px clear in both browsers — whole, exactly the fix-15/16 geometry; the fix did not eat into it.

### 3c. The three §9 items, per item

1. **Wisdom 390 (fallback, 6/7 days):** Change cover hidden on the wisdom slide at ≤560px; overlap vs the weather pill measured **none on all 7 days in both font states** (sweep §3a). The weather pill stays one line, 56–197px clear.
2. **Appointments 390 (both browsers, both font states):** Change cover at 352–392 (FF) / 348–383 (Cr); the "Smart Meet" pill reads whole — full text visible, `elementFromPoint` at its center AND bottom returns `BUTTON.elite-meetpill:Smart Meet` (was `BUTTON.pill:Change cover` on the base). Re-proven **per day, all 7 days, both 390 legs** (`daysweep17.py`: 14/14 PASS; Smart Meet rect identical every day, 678–737 FF / 673–726 Cr).
3. **Summary 390 (Chromium fonts state):** Change cover at 348–383; the "Your Journal" door (693–791) reads whole at rest — overlap **none**. Re-proven per day, all 7 days, both 390 legs (14/14 PASS alongside Appointments).

### 3d. Full fix-15/16 regression (§5 of the brief)

- Nav pills whole at rest on every block of every day at 1920 and 390, both browsers and both font states: 7/7 sweep + 9/9 deck, all four legs (§3a–3b).
- Weather pill one line, 56–197px clear on every swept day, all legs.
- Teach + store whole all 7 days, both font states (`elementFromPoint` hits `DIV.dayteach` / `DIV.wq-store`).
- Greeting true to VM clock (UTC) in all four legs.
- Worlds six tiles readable: row 1 whole at 390 (screenshot, labels + subtitles in full, badge 0); six cells in one row at 1920 (531–732); 2×3 + internal scroll at 390 as in fix-16.
- Buttons (real taps, both widths, both browsers): last-slide Keep-reading advances the day (monthline 639 Hz Thu → 396 Hz Fri); prev-day returns it (396 → 639 Hz); BACK TO MONTH lands on the month view (42 cells, 30 numbered, 12 blank, "November 2026"; row 6 all blank — Dec **6–12**, not Dec 1–5; the fix-16 correction stands).
- Journal empty-state line in full at 1920: "Your words save as you write — nothing typed is lost. Images stay with this day." (rect 645–683, hit `P.none-line`, scrollW == clientW).
- News badges **0** in all four legs; doors Local / Provincial / Global, no badges.
- Worlds-row badges real-or-gone: byte-identical to fix-16 (`worldIcon` null-arg calls 9 = 9; `worldCount("personal")` 2, `worldCount("work")` 0).
- Elite-booking logic intact: `elite-bookpill`, `elite-meetpill`, `[15, 30, 60]`, `mcFreeTimes`, `+ 30` buffer, `No full slot list`, `now.getMinutes() + 60` (+60-min notice), greeting ternary byte-identical.
- Seven day covers + WISDOM byte-identical (`COVER_DAY` sha `7e2653d0…`, `WISDOM` sha `d3783c23…`).
- FIX16 intact: marker present, `padding-bottom:24px/8px` rules present, quote 32px + 48px headliner rules intact, `margin-top:160px` still present (overridden, not deleted).
- No JS changes: 1 inline script, 162,101 chars, byte-identical base→fixed, `new Function` parses OK.
- Structural tags: `</style>`, `</script>`, `</html>` counts 1/1/1 in both.
- **0 page errors in every leg** (four legs × sweep + deck + 7-day defect-slide sweep + buttons + month + regression).

### 3e. Read as a reader (screenshots)

- **390 wisdom Sat 21, Firefox/fallback** (`shots17/sweep-firefox-nofont-390-21.png`, the worst day): reads well — greeting whole and clear of Back, 6-line serif quote whole, teach and store whole, dots and pills whole, weather pill whole. No Change cover pill anywhere on the slide — it is hidden by design on wisdom at phone width, and nothing about the slide looks missing; the reader sees a clean wisdom slide.
- **390 Appointments, both browsers** (`shots17/deck-firefox-nofont-390-5.png`, `shots17/deck-chromium-fonts-390-5.png`): "Change cover" sits at the top right, just under the dots, clear of everything; "Book a time" whole; "Smart Meet" whole in full — the defect the checker caught is gone in both browsers.
- **390 Summary, Chromium** (`shots17/deck-chromium-fonts-390-6.png`): "Change cover" top right, clear; "SUMMARY OF THE DAY" whole; the "Your Journal" door is no longer under the pill — it rides in the slide's own scroll below, as in fix-15.
- **390 Worlds, Firefox** (`shots17/deck-firefox-nofont-390-3.png`): row 1 whole — "Personal feed / Your private world." and "Business feed / Your work world.", badge 0; "Change cover" at the bottom, whole, 1px above the rim.
- **1920 wisdom, Chromium/Great Vibes** (`shots17/deck-chromium-fonts-1920-0.png`): beautiful — one-line script quote, greeting, teach line and store line whole, dots and pills whole with clear space, weather pill bottom-left whole, Change cover bottom-right whole, nothing overlapping. Desktop is exactly as fix-16 left it.

## 4. Design laws — delta 0

`check-design-laws.py` on base and fixed (`laws-check17.js`):

- Base: **PASS — 0 FAIL / 28 WARN**
- Fixed: **PASS — 0 FAIL / 28 WARN**
- Warning texts identical (diffed after stripping filename/line); line shifts: first 3 warnings (before the insertion point) unchanged; the other 25 shift by exactly **+46 lines** — the FIX17 block is 45 lines + newline = 46. **Delta 0 in substance, not just in count.**

## 5. §11 check (in writing)

**The five gates:**
1. **Is it right?** Yes — the fix removes three visible overlaps at phone width and removes nothing else; no merge, no live deploy, no link to Shawn from this seat.
2. **Is it what they truly need?** Yes — the brief's bar is "no clipping anywhere" at 390 at rest (proven §3b–3c) AND the fix-16 nav win held (proven §3a–3b). The one deliberate trade-off — Change cover hidden on the wisdom slide at ≤560px only — is the brief's own sanctioned option, and the function stays one swipe away on the other eight slides; it is named here, not hidden.
3. **Is it mine to do?** Yes — the brief is the authority for exactly this placement fix; nothing outside §9 was touched.
4. **Is now the time?** Yes — the defects are measured, stable, and reproducible on the filed bytes; the fix is one floating button's placement at ≤560px, not a redesign.
5. **Can I prove it?** Yes — every claim above is a hash, a rect, a hit-test, or a screenshot on the fetched filed bytes (proven identical to the staged link). Nothing is taken on trust.

**The design check (§11, on the rendered page):**
- Could I pick this up? The pill keeps its obsidian pill anatomy, rim, and depth — the fix moves it, it does not re-skin it; nothing flat added (the block adds no colors, no fills, no font sizes). Laws checker: 0 FAIL.
- Light: one source, top-left — the block adds no gradients, no shadows.
- Text: no new font sizes, no new text colors, no wording changed; quote stays 32px at 390 / 48px at 1920; nothing under 17px; no gray. Laws delta 0.
- Two same colors together: no colors added, nothing to break the flow.
- Reference objects: the fix reuses the page's own `#dayScroll` positioning and the established per-slide `:has()` pattern from the wisdom/worlds rules — one appended CSS block, nothing rebuilt, nothing invented. Harvest, never invent.
- Don't move / don't remove what he didn't ask: the only geometry changes are the Change-cover placement at ≤560px and its hiding on the wisdom slide at ≤560px (both in §9). The frame, header, covers, data, badges, booking logic, nav clearances, and every other slide are byte-identical (§2 of the byte checks; fixed-minus-block == base).
- Read as a reader: the screenshots were read top to bottom as a reader (§3e) — that reading confirmed the Smart Meet pill whole, the wisdom slide clean without the pill, and the desktop unchanged.
- **Sense check:** the old band was 1px clear of the Notifications blocks and 8px clear of the Naya Notes button — one font-metric shift from a new collision. Moving the pill to a band with ≥10px clearance on every slide in both font states is the fix that stays fixed; leaving it in the old band with per-slide exceptions would have been the fragile one.

## 6. Scorecard

| Check | Result |
|---|---|
| Filing (branch, tip, parent, blob, staged sha) | 10/10 |
| Byte-diff discipline (only the block; fix-16 intact) | 10/10 |
| COVER_DAY / WISDOM / booking / badges intact | 10/10 |
| Laws delta | 0 (0 FAIL / 28 WARN both, same texts, +46 line shift explained) |
| Item 1 — Change cover vs weather pill, wisdom 390 | none on all 7 days, both font states (hidden on wisdom ≤560px) |
| Item 2 — Change cover vs Smart Meet pill, Appointments 390 | none on all 7 days, both browsers/states; pill hit-testable center + bottom |
| Item 3 — Change cover vs "Your Journal" door, Summary 390 | none on all 7 days, both browsers/states |
| Item 4 — hold the line (nav whole, deck re-pass, no other geometry) | 7/7 sweep + 9/9 deck, all four legs; Appointments nav 2px clear held; fixed-minus-block == base |
| Change-cover overlap, per slide per day, all four legs | none |
| Page errors | 0 in all legs |
| Buttons (keep-reading / prev-day / back-to-month) | PASS, real taps, both widths, both browsers |
| Month grid (42 / 30 / 12; row 6 = Dec 6–12 blank) | PASS |

**Known thin margins (stated plainly, not hidden):** the Appointments nav at 390 is 2px clear of the rim — whole, exactly the fix-15/16 geometry, stable across all measurements in this round. The Worlds Change cover at 390 is 1px above the rim line — whole, as in fix-16, untouched. The Change cover is hidden on the wisdom slide at ≤560px only — a deliberate, brief-sanctioned trade-off: no free band exists on that slide (orb at top, nav-to-weather gap as small as 5px on day 21), and the function stays one swipe away on the other eight slides and everywhere at desktop.

## 7. Files (all under `~/workspace/team-nitro/calendar-day-followon-fix17-20261119/`)

- `maker/MAKER-REPORT.md` — this report.
- `maker/proof/fix17-block.css` — the fix (3,100 B), the only change.
- `maker/proof/fixed-fix17.html` — the filed bytes (410,236 B, sha256 `1f798b65…`).
- `maker/proof/base-fix16.html` — the verified base (407,135 B, sha256 `ffc03030…`).
- `maker/proof/fetched-fixed.html` / `fetched-base.html` / `fetched-staged.html` — blob-API + staged-link read-backs (hash-matched).
- `maker/proof/build-fixed17.js` — byte-safe build (Buffer ops) + verification.
- `maker/proof/bytecheck17.js` — byte regression (diff, JS parse, covers, badges, booking).
- `maker/proof/laws-check17.js` + `laws-base17.txt` + `laws-fixed17.txt` — laws delta 0.
- `maker/proof/fetch-verify17.js` — filing + staged-link re-derivation (§1).
- `maker/proof/make-body17.js` — Contents-API body generator (base64 piped, never staged).
- `maker/proof/prove17.py` — full render proof, 2s waits (sweep + deck + buttons + month, all four legs).
- `maker/proof/daysweep17.py` — 7-day Appointments + Summary sweep, both 390 legs.
- `maker/proof/explore17.py` + `dump17.py` — base-geometry exploration (per-slide element maps, both browsers).
- `maker/proof/regress17.py` — journal-line / Worlds-row / news-badge regression at 1920.
- `maker/proof/*.log` — probe logs.
- `maker/proof/shots17/` — screenshots (sweep + deck + month per leg).
- `maker/proof/forwarder17.log` — Chromium proxy forwarder log (started for the Chromium legs, killed by PID when done; no process remains).
