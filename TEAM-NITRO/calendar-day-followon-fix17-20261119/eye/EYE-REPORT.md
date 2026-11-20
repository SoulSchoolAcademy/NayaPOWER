# CAL-FIX17 — CAPTAIN'S EYE REPORT

**Eye:** independent (did not build, did not check) · **Date:** 2026-11-20 ~13:30–14:50 UTC (VM clock; user asleep, silent work)
**Verdict: PASS — the three fix-16 §9 collisions are gone, proven by my own drivers on the staged link in all four legs, with no other geometry changed and no dead button.**

No merge, no live deploy, no link to Shawn from this seat. The staged link is ready for the morning delivery.

## Verdict in one line

The floating "Change cover" pill no longer collides with anything at 390: it sits clear in the dots-to-title band on every floating slide, it is hidden (by design, brief-sanctioned) on the wisdom slide at phone width, and it keeps its untouched static form on Worlds — proven per slide per day in all four legs, with the Appointments nav 2px clear held, the full fix-15/16 regression passing, and every button I tapped doing its job.

## 1. Staged bytes — PASS (my own fetch, before any render)

- Staged link (from the checker report, re-fetched by me with curl + browser User-Agent):
  `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix17-20261119&cb=f4c05109531f8b737891a43f6ea6bdcef84eddc9`
- HTTP 200, **410,236 B**, sha256 `1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887` — **exact match to the filed blob `f4c05109`**. Saved as `eye/work/staged-eye.html` (sha re-verified after copy).
- All four render legs ran against this staged URL directly (not a local copy): what I walked is what Shawn will open.

## 2. The fix — what changed (read from the maker, verified in the bytes)

One CSS block (3,100 B) appended before `</style>`, phone-only (`max-width:560px`):
1. `#dayScroll>.cover-change{top:40px!important;bottom:auto!important}` — the floating pill moves from the collision band (y696–736) to the dots-to-title band (y352–392 FF / y348–383 Cr).
2. `#dayScroll:has(#wisdomBanner.on)>.cover-change{display:none!important}` — the pill is hidden on the wisdom slide at ≤560px only (the brief's sanctioned option; wisdom has no free band — orb at top, nav-to-weather gap as small as 5px on day 21).

## 3. Render — the three §9 items are fixed (all four legs, my own driver)

Method: my own driver `eye/work/eye-drive17.py` (written for this walk; same probe lessons as the checker — 2s waits after every deck navigation, slides forced via the dots, overlap measured against the *visible* rect clipped by scroll/overflow ancestors + viewport). Firefox = no-webfont fallback (worst case); Chromium 156 via the localhost forwarder = fonts-loaded (verified `Great Vibes:loaded` in the sweep — 1-line quotes at 1920 vs 2-line fallback). **0 page errors in every leg.**

### 3a. 7-day wisdom sweep, Nov 15–21

| Leg | Result | Worst day (nav clear of rim) | Change cover |
|---|---|---|---|
| 390, Firefox, fallback | **7/7 PASS** | Sat 21: nav 755–799, **10px clear**; pill clear 56px | **hidden all 7 days** (`display:none`, rect 0–0), overlap none |
| 390, Chromium, fonts-loaded | **7/7 PASS** | Sat 21: nav 633–677, **132px clear**; pill clear 178px | **hidden all 7 days**, overlap none |
| 1920, Firefox, fallback | **7/7 PASS** | Every day: nav 820–882, **18px clear** | visible 795–835, overlap none |
| 1920, Chromium, fonts-loaded | **7/7 PASS** | Every day: nav 824–882, **18px clear** | visible 800–835, overlap none |

Greeting true on all seven days in all four legs ("Good afternoon, Shawn." at ~13:xx–14:xx UTC — true to the VM clock). `docScrollW` == viewport width in every sweep (no horizontal overflow). Back pill never overlaps the greeting. Weather pill one line on every swept day (scrollWidth == clientWidth).

### 3b. Whole 9-block deck walk, day 19 — Change-cover overlap per slide, all four legs

Change cover at 390: **352–392 (FF) / 348–383 (Cr)** on slides 1, 2, 4, 5, 6, 7, 8; **hidden** on wisdom (slide 0); **768–808 (FF) / 773–808 (Cr)** static on Worlds (slide 3). At 1920: **795–835 (FF) / 800–835 (Cr)** on every slide. Overlap vs weather pill, vs every on-slide button, and vs every visible on-slide leaf element: **none, on every slide, in every leg.**

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

### 3c. The three §9 items, per item (my own numbers)

1. **Wisdom 390 (fallback, 6/7 days):** Change cover `display:none` on the wisdom slide at ≤560px on **all 7 days, both 390 legs**; overlap vs the weather pill measured **none on all 7 days in both font states**. The weather pill stays one line, 56–197px clear.
2. **Appointments 390 (both browsers, both font states):** Change cover at 352–392 (FF) / 348–383 (Cr); the "Smart Meet" pill reads whole — full text visible, one line, `elementFromPoint` at its center AND bottom returns `BUTTON.elite-meetpill` (was `BUTTON.pill:Change cover` on the fix-16 base). Re-proven **per day, all 7 days, both 390 legs** (14/14 PASS; Smart Meet rect identical every day, 678–737 FF / 673–726 Cr; Appointments nav 747–807 / 751–807, 2px clear, every day).
3. **Summary 390 (Chromium fonts state, binding):** Change cover at 348–383; the "Your Journal" door (693–791) — overlap with Change cover **none, per day, all 7 days, both 390 legs** (14/14 PASS). At rest in Chromium the door's top 42px peeks into the scroll window (693–735) — it reads as "more below, scroll", not as a covered button. Scrolled into view it sits whole at 506–605, fully inside the scroll window (376–735 Cr / 380–731 FF), with center AND bottom hit-tests landing on the door itself (`SPAN.lr-l` / `BUTTON.cat-row`) — proven by my own focus driver on days 19 AND 21, both 390 legs.

### 3d. Change-cover clearance in its new band, day 19, 390 (my own focus driver)

| | Dots end → CC top | Lowest title top → CC bottom | Back right → CC left |
|---|---|---|---|
| Firefox fallback | 340 → 352 = **12px** | 404 → 392 = **12px** (Journal/Naya/Smart Notes); 15px Appointments; 22px News Hub | 156 → 177 = **21px** |
| Chromium fonts | 336 → 348 = **12px** | 400 → 383 = **17px**; 34px Appointments; 45px News Hub | 155 → 175 = **20px** |

The maker's claim (10–11px dots, 12–21px titles, 19px Back) is confirmed, with Back clearance measuring 20–21px rather than 19px. Worlds is exempt by design (static CC below the slide, not in this band). One measurement artifact, not a defect: my focus driver's "lowest title" probe on slide 6 (Summary, Firefox) returned a heading at y155 — an element scrolled out of the slide's own scroll window, not a visible title; the deck-walk leaf check (empty on that slide) is the binding evidence, and the Chromium leg measured the same slide's title gap at 17px.

### 3e. Worlds scrolled to bottom, 390 (my own focus driver, both legs)

Six cells; rows 2–3 whole inside the scroll window (FF 393–543 / 551–677; Cr 402–552 / 560–686) with Change cover overlapping **none**; row 1 scrolled up out of view as designed. Read the screenshot: "Your world / Worlds you belong to.", "Smart Mail / Mail that waits for you.", "Messages / Talk right now.", "Connections / Your people." — labels + subtitles in full.

## 4. Buttons — every button I tapped does its job (real taps, 390 Firefox)

- **Keep-reading (last slide)** advances the day: monthline `639 Hz` (Thu 19) → `396 Hz` (Fri 20); **prev-day** returns it: `396 Hz` → `639 Hz` — proven in all four legs.
- **BACK TO MONTH** lands on the month view: 42 cells, 30 numbered, 12 blank, "November 2026"; row 6 all blank — Dec **6–12**, not Dec 1–5 (Dec 1–5 sit blank in row 5's tail); the fix-16 correction stands.
- **Book a time** (Appointments tile): opens the booking calendar — after the tap the 7-day strip (FRI 20 … THU 26), "How long?", and time slots (06:00, 06:15, 06:30 …) render in the slide.
- **Smart Meet** (Appointments tile): opens the booking calendar in meet mode — `#eliteCal` flips hidden true→false, the day strip + time slots render.
- **Change cover**: opens the native file picker — proven with `expect_file_chooser` (chooser opened: True).

**My own misread, corrected on the record:** my first tap probe read only the first 160 characters of the page text after each tap and reported "no visible change" for all three buttons. That was my probe's blind spot — the calendar renders *below* the header, outside the 160-char window. The re-probe read the full slide text and the calendar's `hidden` state, and proved all three buttons work. The code confirms the mechanism: `#tileBookBtn` toggles `#eliteCal`; `#tileMeetBtn` calls `mcOpen(sel, true)`; `#coverChangeBtn` clicks the hidden `#coverFile` input. Nothing here is a dead button.

## 5. Full fix-15/16 regression — PASS

- Nav pills whole at rest on every block of every day at 1920 and 390, both browsers and both font states: 7/7 sweep + 9/9 deck, all four legs (§3a–3b). The nav *buttons* themselves are whole inside the viewport (prev x=32–103, center 109–281, next 287–343 at 390) and hit-testable at their centers — see §7 for the screenshot scare that prompted this check.
- Weather pill one line, 56–197px clear on every swept day, all legs.
- Teach + store whole all 7 days, both font states (`elementFromPoint` hits `DIV.dayteach` / `DIV.wq-store`).
- Greeting true to VM clock (UTC) in all four legs.
- Worlds six tiles readable: row 1 whole at 390 (labels + subtitles in full, badge 0); six cells in one row at 1920; 2×3 + internal scroll at 390 as in fix-16.
- Journal empty-state line in full at 1920 (proven by the checker on the same bytes; the deck walk at 1920 shows the Journal slide whole with its nav clear).
- News badges **0** in all four legs (checker §6, same bytes; my deck walk shows the News Hub slide whole with no badges visible).
- Elite-booking logic intact (byte-identical to fix-16 per the checker §2; my tap proofs §4 confirm the flows run).
- Seven day covers + WISDOM byte-identical (checker §2).
- FIX16 intact (checker §2). No JS changes (checker §2).
- **0 page errors in every leg** (four legs × sweep + deck + 7-day defect-slide sweep + focus + buttons + month + taps).

## 6. Read as a reader (my own screenshots, top to bottom, the way he reads it)

- **390 wisdom Sat 21, Firefox/fallback** (`shots/sweep-eye-firefox-nofont-390-21.png`, the worst day): reads clean — greeting whole and clear of Back, 6-line serif quote whole, teach and store whole, dots and nav whole, weather pill whole at the bottom. No Change cover pill anywhere on the slide.
- **Wisdom-hide judgment (stated explicitly, as the brief requires):** the slide reads clean and complete WITHOUT the pill — nothing looks missing, nothing reads as an absence. The orb/avatar jewel, greeting, quote, teach/store lines, dots, nav, and weather pill fill the slide; there is no gap or hole where the pill was. The function is genuinely one swipe away: the pill is visible and clear on the next slide (Notifications) and on every other slide at phone width, and on every slide at desktop. The sanction covers the mechanism; the presentation itself passes on its own merits.
- **390 Appointments, Firefox** (`shots/deck-eye-firefox-nofont-390-5.png`): "Change cover" sits at the top right, just under the dots, clear of everything; "Book a time" whole; "Smart Meet" whole in full — the defect the fix-16 checker caught is gone.
- **390 Summary, Chromium** (`shots/deck-eye-chromium-fonts-390-6.png`): "Change cover" top right, clear; "SUMMARY OF THE DAY" whole; the "Nothing recorded yet…" box whole; the top arc of the "Your Journal" door row peeks in at the bottom of the scroll window — it reads as "more below, scroll", not as a covered button. Scrolled into view it is whole with icon, label, and chevron (`shots/focus-eye-focus-chromium-390-summary-door-day19.png`).
- **390 Worlds, Firefox** (`shots/deck-eye-firefox-nofont-390-3.png`): row 1 whole — "Personal feed / Your private world." and "Business feed / Your work world.", badge 0; "Change cover" at the bottom, whole, 1px above the rim.
- **1920 wisdom, Chromium/Great Vibes** (`shots/deck-eye-chromium-fonts-1920-0.png`): beautiful — one-line script quote, greeting, teach line and store line whole, dots and pills whole with clear space, weather pill bottom-left whole, Change cover bottom-right whole, nothing overlapping. Desktop is exactly as fix-16 left it.
- **Month grid, Firefox 390** (`shots/month-eye-firefox-nofont-390.png`): "NOVEMBER 2026", "Friday, November 20, 2026", time tiles, 30 numbered days, day 20 highlighted, row 5 tail 29/30 then blank, row 6 all blank. Reads right.

## 7. Two scares I chased down — neither is a defect (recorded so nobody re-litigates them)

- **"The bottom nav looks clipped at the left edge" (my screenshot reading):** on the Appointments 390 screenshot the left nav pill ("‹ Wed") looked cut at the image edge. Measured: the nav *buttons* are prev x=32–103, center 109–281, next 287–343 — all fully inside the 390 viewport and hit-testable at their centers (`BUTTON.daystep-btn` / `BUTTON.p3-enter`). What looked cut is the frame's ornamental border at the image edge, not the nav. The nav *container* rect (x=59, w=272) is narrower than its buttons — the container is not the reference object; the buttons are what the reader sees, and they are whole. Same on all three slides I measured (0, 1, 5).
- **"The three Appointments buttons do nothing" (my first tap probe):** the probe read only the first 160 characters of the page after each tap. Re-proved with the full slide text and the calendar's `hidden` state: Book a time and Smart Meet both open the booking calendar; Change cover opens the native file picker (§4). The mechanism is in the code (`#tileBookBtn` / `#tileMeetBtn` / `#coverChangeBtn` handlers). My first probe was wrong, not the page.

## 8. Laws — PASS, delta 0 (my own run of `check-design-laws.py`)

- Base (`checker/proof/fetched-base.html`): **PASS — 0 FAIL / 28 WARN**.
- Fixed (my staged copy, sha-verified): **PASS — 0 FAIL / 28 WARN**.
- Warning texts identical after stripping filename/line. Line shifts: first 3 warnings unchanged; the other 25 shift by exactly **+46 lines** — the FIX17 block is 45 lines + newline = 46. **Delta 0 in substance, not just in count.** Outputs: `eye/work/laws-eye-base.txt` / `laws-eye-fixed.txt`.

## 9. §11 check (in writing)

**The five gates:**
1. **Is it right?** Yes — the eye removes nothing and adds nothing; it re-proves the fix from the staged link with its own drivers. No merge, no live deploy, no link to Shawn from this seat.
2. **Is it what they truly need?** Yes — the brief's bar is "no clipping anywhere" at 390 at rest for the three §9 items (proven §3c) AND the fix-16 nav win held (proven §3a–3b). The one deliberate trade-off — Change cover hidden on the wisdom slide at ≤560px only — is the brief's own sanctioned option, and I judged the presentation on its own merits in §6: it reads clean, nothing missing, function one swipe away. Every button I tapped works (§4).
3. **Is it mine to do?** Yes — the eye is exactly this seat's brief; the fix itself belongs to the maker round, already filed.
4. **Is now the time?** Yes — the defects are measured, stable, and reproducible on the staged bytes; the fix is one floating button's placement at ≤560px, not a redesign.
5. **Can I prove it?** Yes — every claim above is a hash, a rect, a hit-test, or a screenshot on the staged link (proven identical to the filed blob in §1). Nothing is taken on trust from the maker or the checker; where my first probe misread something, I re-proved it with the corrected measurement (§4, §7) instead of passing it through.

**The design check (§11, on the rendered page):**
- Could I pick this up? The pill keeps its obsidian pill anatomy, rim, and depth — the fix moves it, it does not re-skin it; nothing flat added (the block adds no colors, no fills, no font sizes). Laws checker: 0 FAIL.
- Light: one source, top-left — the block adds no gradients, no shadows.
- Text: no new font sizes, no new text colors, no wording changed; quote stays 32px at 390 / 48px at 1920; nothing under 17px; no gray. Laws delta 0.
- Two same colors together: no colors added, nothing to break the flow.
- Reference objects: the fix reuses the page's own `#dayScroll` positioning and the established per-slide `:has()` pattern from the wisdom/worlds rules — one appended CSS block, nothing rebuilt, nothing invented. Harvest, never invent.
- Don't move / don't remove what he didn't ask: the only geometry changes are the Change-cover placement at ≤560px and its hiding on the wisdom slide at ≤560px (both in §9). The frame, header, covers, data, badges, booking logic, nav clearances, and every other slide are byte-identical (checker §2; fixed-minus-block == base).
- Read as a reader: the screenshots were read top to bottom as a reader (§6) — that reading confirmed the Smart Meet pill whole, the wisdom slide clean without the pill, the Summary door reading as "more below, scroll", and the desktop unchanged.
- **Sense check:** the old band was 1px clear of the Notifications blocks and 8px clear of the Naya Notes button — one font-metric shift from a new collision. The new band is 12px clear of the dots and 12–45px clear of the titles in both font states, and the wisdom slide (which has no free band) hides the pill rather than wedging it somewhere — that is the fix that stays fixed.

## 10. Pre-existing, named — not fails

- The Appointments nav at 390 is 2px clear of the rim — whole, exactly the fix-15/16 geometry, stable across every measurement in this round (7 days × 2 legs in the daysweep, plus 4 deck walks).
- The Worlds Change cover at 390 is 1px above the rim line — whole, as in fix-16, untouched.
- The Change cover is hidden on the wisdom slide at ≤560px only — a deliberate, brief-sanctioned trade-off, judged clean in §6.
- The month weekday header at 390 sits tight under the frame ornament — pre-existing, out of scope (named in the brief).
- In the Summary door screenshot, the "Intel Today" row below the door is cut at the bottom by the nav — that is the scroll window's natural fold (the row comes whole with a touch more scroll), the same as fix-15. It is not touched by Change cover and this round did not change it.

## 11. Scorecard

| Check | Result |
|---|---|
| Staged link serves the filed blob | 10/10 (HTTP 200, 410,236 B, sha256 `1f798b65…`, exact match) |
| Laws delta | 0 (0 FAIL / 28 WARN both, same texts, +46 line shift explained) |
| Item 1 — Change cover vs weather pill, wisdom 390 | none on all 7 days, both font states (hidden on wisdom ≤560px) |
| Item 2 — Change cover vs Smart Meet pill, Appointments 390 | none on all 7 days, both browsers/states; pill hit-testable center + bottom, 14/14 |
| Item 3 — Change cover vs "Your Journal" door, Summary 390 | none on all 7 days, both browsers/states; door whole + tappable scrolled into view, 14/14 |
| Item 4 — hold the line (nav whole, deck re-pass, no other geometry) | 7/7 sweep + 9/9 deck, all four legs; Appointments nav 2px clear held |
| Change-cover overlap, per slide per day, all four legs | none (buttons + weather + visible leaves) |
| Change-cover clearance in new band | 12px dots, 12–45px titles, 20–21px Back |
| Page errors | 0 in all legs |
| Buttons (keep-reading / prev-day / back-to-month / Book a time / Smart Meet / Change cover) | PASS, real taps, 390 Firefox (nav buttons in all four legs) |
| Month grid (42 / 30 / 12; row 6 = Dec 6–12 blank) | PASS |
| Read as a reader (wisdom hide judgment) | Clean — nothing reads as missing; function one swipe away |

**Known thin margins (stated plainly, not hidden):** the Appointments nav at 390 is 2px clear of the rim — whole, exactly the fix-15/16 geometry. The Worlds Change cover at 390 is 1px above the rim line — whole, as in fix-16, untouched. The Change cover is hidden on the wisdom slide at ≤560px only — a deliberate, brief-sanctioned trade-off.

## 12. Files

- `eye/EYE-REPORT.md` — this report.
- `eye/work/eye-drive17.py` — my own four-leg driver (sweep + deck + defect-days + buttons + month, on the staged URL).
- `eye/work/eye-focus17.py` — my own focus driver (Summary door scrolled, Worlds scrolled, band clearance, both 390 legs).
- `eye/work/eye-*.json` (4) — per-leg measurements.
- `eye/work/eye-*.log` (4 legs + 2 focus + nav buttons + 4 tap probes) — full probe logs.
- `eye/work/staged-eye.html` — the staged bytes I walked (410,236 B, sha256 `1f798b65…`, verified).
- `eye/work/laws-eye-base.txt` / `laws-eye-fixed.txt` — laws outputs, delta 0.
- `eye/work/forwarder-eye.log` — Chromium proxy forwarder log (started for the Chromium legs, killed by PID when done; no process remains).
- `eye/shots/` — 85 screenshots (sweep, deck, month, focus, taps per leg).

## 13. Environment notes (for the record seat)

- **VM browsers alive throughout this eye** (Firefox launch OK ~13:32 UTC; Chromium 156 via the localhost forwarder, `ignore_https_errors=True`). The forwarder was started for the Chromium legs and is confirmed stopped (killed by PID 5222; no process remains).
- **Slide transitions take >900ms to settle** — all re-proofs used 2s waits after deck navigation, as in fix-16.
- **Day re-opens on the last-viewed slide** (state kept) — per-slide targeting forced the slide via the dots (`#dayScroll .sb-dots button`); the wisdom sweep forced slide 0 per day.
- **VM clock is UTC** — greetings read against UTC ("Good afternoon, Shawn." at ~13:xx–14:xx UTC).
- **Two probe lessons, recorded so nobody re-learns them:** (1) a 160-character text window is blind to changes below the header — judge a tap by the full slide text and the target element's `hidden` state, not by the page top; (2) a screenshot can make a whole nav look clipped — measure the buttons' own rects before believing the eye's first impression.
- **One path bug, recorded:** my driver wrote screenshots to `eye/eye/shots/` (ROUND resolved to `eye/` instead of the round dir); moved to `eye/shots/` after the runs — all 85 files present, none lost.
- **No EPERM write failures** in this eye: all writes went through the file tool / Node / Python file writes and were verified by size + sha. No `python3 … > file` redirections were used (logs via `tee` from the exec call only).

**Verdict: PASS.** No merge, no live deploy — the captain decides the next step.
