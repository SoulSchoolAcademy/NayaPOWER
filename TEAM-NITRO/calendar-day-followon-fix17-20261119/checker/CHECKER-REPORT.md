# CAL-FIX17 — CHECKER REPORT

**Checker:** independent (did not build) · **Date:** 2026-11-20 ~13:00–13:30 UTC (VM clock; user asleep, silent work)
**Verdict: PASS — all three fix-16 §9 items are fixed and re-proven by my own drivers, in all four legs, with no other geometry changed.**

No merge, no live deploy, no link to Shawn. The captain's eye may follow.

## Verdict in one line

The floating "Change cover" pill no longer collides with anything at 390: it sits clear in the dots-to-title band on every floating slide, it is hidden (by design, brief-sanctioned) on the wisdom slide at phone width, and it keeps its untouched static form on Worlds — proven per slide per day in all four legs, with the Appointments nav 2px clear held and the full fix-15/16 regression passing.

## 1. Filing — PASS (re-derived via the git blob API, never the maker's word)

Re-derived with `checker/proof/fetch-verify17.js` (gh-direct.py CLI, blob API):

| Claim | Re-derived |
|---|---|
| Branch `calendar/day-followon-fix17-20261119` | HTTP 200, tip `f8500a845dd6501f104319aa53d53ba11359802c` — matches |
| Parent = fix-16 tip | Commit parents `['572265f25d80146fb9d8a1ff7f3bb56215143f0d']` — matches |
| Commit message | `CAL-FIX17: Change cover clear at 390 — floating pill to deck top, hidden on wisdom (phone only)` |
| Filed blob `f4c05109531f8b737891a43f6ea6bdcef84eddc9` | 410,236 B, sha256 `1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887` — matches |
| Base blob `cc67fbf98388fbcbcf26287d82f3a81eb9d5d7c3` | 407,135 B, sha256 `ffc03030c555f034dd1608d3f78996d8c6455a963462bec5e51b64fa8e548ca3` — matches |
| Rebuilt (base + claimed block before `</style>`) | 410,236 B, sha256 `1f798b65…` — **rebuilt == filed blob: true** |
| Filed-minus-block == base | **true** |

## 2. Byte-diff — PASS (on the fetched bytes; `checker/proof/byte-checks17.js`)

- Block present exactly once, immediately before `</style>`; prefix and suffix match base byte for byte. Delta 3,101 B = block 3,100 B + newline.
- No JS changes: 1 inline script, 162,101 chars, byte-identical base→fixed, `new Function` parses OK.
- `COVER_DAY` byte-identical, `WISDOM` byte-identical — shas `7e2653d0…` / `d3783c23…`, exactly as the maker claimed (see the harness note below on how the shas were extracted).
- New font sizes in the block: none. New hex colors in the block: none.
- FIX16 intact: marker present, `margin-top:160px` rule still present (overridden, not deleted). Quote 32px + 48px headliner rules intact.
- Badges: `worldIcon(…null…)` calls 9 = 9; `worldCount("personal")` 2 calls, `worldCount("work")` 0 — fix-14's five nulls intact, Personal keeps its real count.
- Elite booking intact: `elite-bookpill`, `elite-meetpill`, `[15, 30, 60]`, `mcFreeTimes`, `+ 30` buffer, `No full slot list`, `now.getMinutes() + 60` (+60-min notice), greeting ternary byte-identical.
- Structural tags: `</style>`, `</script>`, `</html>` counts 1/1/1 in both.
- `renderMonth()`: 42-cell design present (`i < 42`), out-of-month cells blank with the "not shown at all" comment. The month grid is proven by render in §5 (§6), not by the regex alone (see harness note).

**Harness note (not a defect):** the `byte-checks17.js` COVER_DAY/WISDOM shas printed in its log (`517271eb…` / `8654ad1c…`) come from its lazy `var … = […];` regex, which includes the declaration prefix and stops at the first `];`. Identity (`identical: true`) is what the script proves. I re-extracted both arrays with a bracket-balanced parse: shas `7e2653d03f6a82fc…` and `d3783c231be492ae…` — exactly the maker's. Likewise the script's `renderMonth found: false` is its regex missing the loop's exact spacing; the function exists and the rendered month is 42/30/12 (§5/§6).

## 3. Staged link serves the filed blob — PASS

- Fetch (Node https, browser User-Agent) on the staged link (`…&ref=calendar/day-followon-fix17-20261119&cb=f4c05109531f8b737891a43f6ea6bdcef84eddc9`): HTTP 200, 410,236 B, sha256 `1f798b65…` — **exact match to the filed blob**. Saved as `checker/proof/fetched-staged.html`.

## 4. Laws — PASS, delta 0 (`checker/proof/laws-check17.js`, outputs `laws-base17.txt` / `laws-fixed17.txt`)

- Base: **PASS — 0 FAIL / 28 WARN**. Fixed: **PASS — 0 FAIL / 28 WARN**.
- Warning texts identical after stripping filename/line. Line shifts: first 3 warnings (before the insertion point) unchanged; the other 25 shift by exactly **+46 lines** — the FIX17 block is 45 lines + newline = 46. **Delta 0 in substance, not just in count.**

## 5. Render — the three §9 items are fixed (all four legs, my own harness)

Method: my own harness `checker/proof/prove17c.py` (Playwright sync; 2-second waits after every deck navigation; slides forced via the dots `#dayScroll .sb-dots button`; rim line = `.rf-rim` bottom − 3). Firefox = no-webfont fallback (worst case; `document.fonts` empty); Chromium 156 via the localhost forwarder = fonts-loaded (verified `Great Vibes:loaded`, `Marcellus:loaded`). **Change-cover overlap was measured against the visible rect** — clipped by every scroll/overflow ancestor and the viewport — not against raw `getBoundingClientRect`, because content scrolled out of its container is not painted there (see §5e for the two places the naive check misfires and how I proved them instead). All runs on the fetched fixed bytes (sha256 `1f798b65…`, re-verified after the runs).

### 5a. 7-day wisdom sweep, Nov 15–21 (teach + store whole, weather pill one line, nav whole, Change cover hidden at 390, no horizontal overflow)

| Leg | Result | Worst day (nav clear of rim) | Change cover |
|---|---|---|---|
| 390, Firefox, fallback | **7/7 PASS** | Sat 21: nav 755–799, **10px clear**; pill clear 56px | **hidden all 7 days** (`display:none`, rect 0–0), overlap none |
| 390, Chromium, fonts-loaded | **7/7 PASS** | Sat 21: nav 633–677, **132px clear**; pill clear 178px | **hidden all 7 days**, overlap none |
| 1920, Firefox, fallback | **7/7 PASS** | Every day: nav 820–882, **18px clear** | visible 795–835, overlap none |
| 1920, Chromium, fonts-loaded | **7/7 PASS** | Every day: nav 824–882, **18px clear** | visible 800–835, overlap none |

Greeting true on all seven days in all four legs ("Good afternoon, Shawn." at ~13:xx UTC — true to the VM clock). `docScrollW` == viewport width in every sweep (no horizontal overflow). Back pill never overlaps the greeting.

### 5b. Whole 9-block deck walk, day 19 — Change-cover position + overlap per slide, all four legs

Change cover at 390: **352–392 (FF) / 348–383 (Cr)** on slides 1, 2, 4, 5, 6, 7, 8; **hidden** on wisdom (slide 0); **768–808 (FF) / 773–808 (Cr)** static on Worlds (slide 3). At 1920: **795–835 (FF) / 800–835 (Cr)** on every slide. Overlap vs weather pill, vs every on-slide button, and vs every visible on-slide leaf element: **none, on every slide, in every leg.** `elementFromPoint` at the pill's center returns `BUTTON.pill:Change cover` itself wherever it is visible (tappable).

| Slide | 1920 FF (nav clear) | 1920 Cr (nav clear) | 390 FF (nav clear) | 390 Cr (nav clear) |
|---|---|---|---|---|
| Wisdom | 820–882 (18) | 824–882 (18) | 703–747 (62) | 633–677 (132) |
| Notifications | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Journal | 828–888 (12) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Your Worlds | 820–882 (18) | 824–882 (18) | 685–745 (64) | 694–750 (59) |
| News Hub | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Appointments | 820–882 (18) | 824–882 (18) | 747–807 (**2**, whole as in fix-15/16) | 751–807 (**2**) |
| Summary of the day | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Naya Notes | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Smart Notes | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |

**9/9 PASS in all four legs.** The Appointments nav at 390 is 2px clear in both browsers — whole, exactly the fix-15/16 geometry; the fix did not eat into it. (One 1920 variation, not a defect: the Journal nav at 1920 Firefox is 828–888, 12px clear rather than 18px — whole.)

### 5c. Change-cover clearance in its new band, day 19, 390 (`checker/proof/titleclear17.py`)

| | Dots end → CC top | Lowest title top → CC bottom | Back right → CC left |
|---|---|---|---|
| Firefox fallback | 340 → 352 = **12px** | 404 → 392 = **12px** (Journal/Summary/Naya/Smart Notes); 15px Appointments; 22px News Hub | 156 → 177 = **21px** |
| Chromium fonts | 336 → 348 = **12px** | 400 → 383 = **17px**; 34px Appointments; 45px News Hub | 155 → 175 = **20px** |

The maker's claim (10–11px dots, 12–21px titles, 19px Back) is confirmed, with Back clearance measuring 20–21px rather than 19px. Worlds is exempt by design (static CC below the slide, not in this band).

### 5d. The three §9 items, per item

1. **Wisdom 390 (fallback, 6/7 days):** Change cover `display:none` on the wisdom slide at ≤560px on **all 7 days, both 390 legs**; overlap vs the weather pill measured **none on all 7 days in both font states**. The weather pill stays one line, 56–197px clear. Judgment on the hide: §7.
2. **Appointments 390 (both browsers, both font states):** Change cover at 352–392 (FF) / 348–383 (Cr); the "Smart Meet" pill reads whole — full text visible, `elementFromPoint` at its center AND bottom returns `BUTTON.elite-meetpill` (was `BUTTON.pill:Change cover` on the base). Re-proven **per day, all 7 days, both 390 legs** (`daysweep17c.py`: 14/14 PASS; Smart Meet rect identical every day, 678–737 FF / 673–726 Cr; Appointments nav 747–807 / 751–807, 2px clear, every day).
3. **Summary 390 (Chromium fonts state, binding):** Change cover at 348–383; the "Your Journal" door (693–791) — overlap with Change cover **none, per day, all 7 days, both 390 legs** (14/14 PASS in `daysweep17c.py`). The door rides in the slide's own scroll below, as in fix-15: scrolled into view it sits whole at 420–518, fully inside the scroll window (380–731 FF / 376–735 Cr), 28–37px clear of Change cover's bottom, with center AND bottom hit-tests landing on the door itself (`SPAN.lr-l` / `BUTTON.cat-row`) — proven per day, all 7 days, both 390 legs. At rest it is below the scroll fold (Firefox: 755–853, fully below the 380–731 window; Chromium: top 42px visible at 693–735) — that is the pre-existing fix-15 design, unchanged by this round, and Change cover no longer touches it. This is the same adjudication as fix-16 §6.3, now with the overlap gone.

### 5e. Two places my first strict check flagged — adjudicated, not defects (recorded so nobody re-litigates them)

- **Worlds, naive leaf overlap:** my first leaf check (raw rects) flagged three row-2 spans overlapping CC 768–808. Those spans belong to row-2 cells whose rects (694–844) sit **below the slide's scroll viewport (380–677)** — clipped, not painted at rest. Re-proven with the clipping-aware visible-rect check (`prove17c.py`): overlap none; and scrolled to the bottom, all six cells land whole inside the viewport (236–677 FF / 224–686 Cr) with CC overlapping none (`focus17.py`, both 390 legs). Row 1 at rest, rows 2–3 after scrolling — exactly the fix-16 accepted geometry, untouched.
- **Summary door hit-test at rest:** a hit-test at the door's center at rest returns `SECTION.cat`, because the door is below the scroll fold at rest and not painted at its center point. That is a property of the scroll design, not of Change cover. The brief's item is Change-cover overlap (none, §5d.3); whole + tappable is proven scrolled into view, per day, both legs.

### 5f. Buttons — PASS (real taps, both widths, both browsers, all four legs)

- Last-slide Keep-reading advances the day: monthline `639 Hz` (Thu 19) → `396 Hz` (Fri 20).
- Prev-day (first nav button) returns it: `396 Hz` → `639 Hz`.
- BACK TO MONTH lands on the month view: 42 cells, 30 numbered, 12 blank, "November 2026"; row 6 all blank — Dec **6–12**, not Dec 1–5; the fix-16 correction stands.

## 6. Full fix-15/16 regression — PASS

- Nav pills whole at rest on every block of every day at 1920 and 390, both browsers and both font states: 7/7 sweep + 9/9 deck, all four legs (§5a–5b).
- Weather pill one line, 56–197px clear on every swept day, all legs.
- Teach + store whole all 7 days, both font states (`elementFromPoint` hits `DIV.dayteach` / `DIV.wq-store`).
- Greeting true to VM clock (UTC) in all four legs.
- Worlds six tiles readable: row 1 whole at 390 (screenshot, labels + subtitles in full, badge 0); six cells in one row at 1920 (531–732 FF / 530–731 Cr); 2×3 + internal scroll at 390 as in fix-16.
- Journal empty-state line in full at 1920: "Your words save as you write — nothing typed is lost. Images stay with this day." (rect 645–683 FF / 634–667 Cr, hit `P.none-line`, scrollW == clientW).
- News badges **0** in all four legs; doors Local / Provincial / Global, no badges.
- Worlds-row badges real-or-gone: byte-identical to fix-16 (§2).
- Elite-booking logic intact (§2). Seven day covers + WISDOM byte-identical (§2).
- FIX16 intact (§2). No JS changes (§2).
- **0 page errors in every leg** (four legs × sweep + deck + 7-day defect-slide sweep + focus + buttons + month).

## 7. Read as a reader (screenshots, top to bottom, the way he reads it)

- **390 wisdom Sat 21, Firefox/fallback** (`shots17c/sweep-firefox-nofont-390-21.png`, the worst day): reads clean — greeting whole and clear of Back, 6-line serif quote whole, teach and store whole, dots and nav whole, weather pill whole at the bottom. No Change cover pill anywhere on the slide.
- **Wisdom-hide judgment (stated explicitly, as the brief requires):** the slide reads clean and complete WITHOUT the pill — nothing looks missing, nothing reads as an absence. The orb/avatar jewel, greeting, quote, teach/store lines, dots, nav, and weather pill fill the slide; there is no gap or hole where the pill was. The function is genuinely one swipe away: the pill is visible and clear on the next slide (Notifications) and on every other slide at phone width, and on every slide at desktop. The sanction covers the mechanism; the presentation itself passes on its own merits.
- **390 Appointments, both browsers** (`shots17c/deck-firefox-nofont-390-5.png`, `shots17c/deck-chromium-fonts-390-5.png`): "Change cover" sits at the top right, just under the dots, clear of everything; "Book a time" whole; "Smart Meet" whole in full — the defect the fix-16 checker caught is gone in both browsers.
- **390 Summary, Chromium** (`shots17c/deck-chromium-fonts-390-6.png`): "Change cover" top right, clear; "SUMMARY OF THE DAY" whole; the "Nothing recorded yet…" box whole; the top arc of the "Your Journal" door row peeks in at the bottom of the scroll window — it reads as "more below, scroll", not as a covered button. Scrolled into view it is whole with icon, label, and chevron (`shots17c/focus-chromium-fonts-390-6-door.png`).
- **390 Worlds, Firefox** (`shots17c/deck-firefox-nofont-390-3.png`): row 1 whole — "Personal feed / Your private world." and "Business feed / Your work world.", badge 0; "Change cover" at the bottom, whole, 1px above the rim.
- **1920 wisdom, Chromium/Great Vibes** (`shots17c/deck-chromium-fonts-1920-0.png`): beautiful — one-line script quote, greeting, teach line and store line whole, dots and pills whole with clear space, weather pill bottom-left whole, Change cover bottom-right whole, nothing overlapping. Desktop is exactly as fix-16 left it.

One pre-existing observation, not a defect and out of scope: in the Summary door screenshot, the "Intel Today" row below the door is cut at the bottom by the nav — that is the scroll window's natural fold (the row comes whole with a touch more scroll), the same as fix-15. It is not touched by Change cover and this round did not change it.

## 8. §11 check (in writing)

**The five gates:**
1. **Is it right?** Yes — the check removes nothing and adds nothing; it re-proves the fix from the filed bytes with its own drivers. No merge, no live deploy, no link to Shawn from this seat.
2. **Is it what they truly need?** Yes — the brief's bar is "no clipping anywhere" at 390 at rest for the three §9 items (proven §5d) AND the fix-16 nav win held (proven §5a–5b). The one deliberate trade-off — Change cover hidden on the wisdom slide at ≤560px only — is the brief's own sanctioned option, and I judged the presentation on its own merits in §7: it reads clean, nothing missing, function one swipe away.
3. **Is it mine to do?** Yes — checking is exactly this seat's brief; the fix itself belongs to the maker round, already filed.
4. **Is now the time?** Yes — the defects are measured, stable, and reproducible on the filed bytes; the fix is one floating button's placement at ≤560px, not a redesign.
5. **Can I prove it?** Yes — every claim above is a hash, a rect, a hit-test, or a screenshot on the fetched filed bytes (proven identical to the staged link in §1/§3). Nothing is taken on trust from the maker's report; where my first strict check flagged something, I re-proved it with the corrected measurement (§5e) instead of passing it through.

**The design check (§11, on the rendered page):**
- Could I pick this up? The pill keeps its obsidian pill anatomy, rim, and depth — the fix moves it, it does not re-skin it; nothing flat added (the block adds no colors, no fills, no font sizes). Laws checker: 0 FAIL.
- Light: one source, top-left — the block adds no gradients, no shadows.
- Text: no new font sizes, no new text colors, no wording changed; quote stays 32px at 390 / 48px at 1920; nothing under 17px; no gray. Laws delta 0.
- Two same colors together: no colors added, nothing to break the flow.
- Reference objects: the fix reuses the page's own `#dayScroll` positioning and the established per-slide `:has()` pattern from the wisdom/worlds rules — one appended CSS block, nothing rebuilt, nothing invented. Harvest, never invent.
- Don't move / don't remove what he didn't ask: the only geometry changes are the Change-cover placement at ≤560px and its hiding on the wisdom slide at ≤560px (both in §9). The frame, header, covers, data, badges, booking logic, nav clearances, and every other slide are byte-identical (§2; fixed-minus-block == base).
- Read as a reader: the screenshots were read top to bottom as a reader (§7) — that reading confirmed the Smart Meet pill whole, the wisdom slide clean without the pill, and the desktop unchanged.
- **Sense check:** the old band was 1px clear of the Notifications blocks and 8px clear of the Naya Notes button — one font-metric shift from a new collision. The new band is 12px clear of the dots and 12–45px clear of the titles in both font states, and the wisdom slide (which has no free band) hides the pill rather than wedging it somewhere — that is the fix that stays fixed.

## 9. Scorecard

| Check | Result |
|---|---|
| Filing (branch, tip, parent, blob, staged sha) | 10/10 |
| Byte-diff discipline (only the block; fix-16 intact) | 10/10 |
| COVER_DAY / WISDOM / booking / badges intact | 10/10 |
| Laws delta | 0 (0 FAIL / 28 WARN both, same texts, +46 line shift explained) |
| Item 1 — Change cover vs weather pill, wisdom 390 | none on all 7 days, both font states (hidden on wisdom ≤560px) |
| Item 2 — Change cover vs Smart Meet pill, Appointments 390 | none on all 7 days, both browsers/states; pill hit-testable center + bottom, 14/14 |
| Item 3 — Change cover vs "Your Journal" door, Summary 390 | none on all 7 days, both browsers/states; door whole + tappable scrolled into view, 14/14 |
| Item 4 — hold the line (nav whole, deck re-pass, no other geometry) | 7/7 sweep + 9/9 deck, all four legs; Appointments nav 2px clear held; fixed-minus-block == base |
| Change-cover overlap, per slide per day, all four legs | none (buttons + weather + visible leaves) |
| Change-cover clearance in new band | 12px dots, 12–45px titles, 20–21px Back |
| Page errors | 0 in all legs |
| Buttons (keep-reading / prev-day / back-to-month) | PASS, real taps, both widths, both browsers |
| Month grid (42 / 30 / 12; row 6 = Dec 6–12 blank) | PASS |
| Read as a reader (wisdom hide judgment) | Clean — nothing reads as missing; function one swipe away |

**Known thin margins (stated plainly, not hidden):** the Appointments nav at 390 is 2px clear of the rim — whole, exactly the fix-15/16 geometry, stable across every measurement in this round (7 days × 2 legs in the daysweep, plus 4 deck walks). The Worlds Change cover at 390 is 1px above the rim line — whole, as in fix-16, untouched. The Change cover is hidden on the wisdom slide at ≤560px only — a deliberate, brief-sanctioned trade-off, judged clean in §7.

## 10. Files

- `checker/CHECKER-REPORT.md` — this report.
- `checker/proof/fetch-verify17.js` + `fetch-verify17.log` — filing + staged-link re-derivation (§1, §3); writes `fetched-base.html`, `fetched-fixed.html`, `fetched-staged.html` (410,236 B, sha256 `1f798b65…`).
- `checker/proof/byte-checks17.js` + `byte-checks17.log` — byte-diff on the fetched bytes (§2).
- `checker/proof/laws-check17.js` + `laws-base17.txt` + `laws-fixed17.txt` + `laws-check17.log` — laws delta 0 (§4).
- `checker/proof/prove17c.py` + `prove-ff-nofont-390.log` / `prove-cr-fonts-390.log` / `prove-ff-nofont-1920.log` / `prove-cr-fonts-1920.log` — full render proof, 2s waits, clipping-aware leaf overlap (sweep + deck + journal/worlds/news + buttons + month, all four legs) (§5a–5b, §6).
- `checker/proof/daysweep17c.py` + `daysweep-ff.log` / `daysweep-cr.log` — 7-day Appointments + Summary sweep, both 390 legs, incl. scrolled-into-view door proof (§5d).
- `checker/proof/focus17.py` + `focus-ff-nofont-390.log` / `focus-cr-fonts-390.log` — Worlds scrolled + Summary door scrolled-into-view (§5d–5e).
- `checker/proof/titleclear17.py` + `titleclear-ff.log` / `titleclear-cr.log` — Change-cover clearance vs dots/titles/Back per slide (§5c).
- `checker/proof/shots17c/` — 82 screenshots (sweep, deck, worlds, month, focus per leg).
- `checker/proof/forwarder17c.log` — Chromium proxy forwarder log (started for the Chromium legs, killed by PID when done; no process remains).

## 11. Environment notes (for the coordinator)

- **VM browsers alive throughout this check** (Firefox launch OK ~13:00 UTC; Chromium 156 via the localhost forwarder, `ignore_https_errors=True`). The forwarder was started for the Chromium legs and is confirmed stopped (killed by PID 269210; no process remains).
- **Slide transitions take >900ms to settle** — all re-proofs used 2s waits after deck navigation, as in fix-16 (§8).
- **Day re-opens on the last-viewed slide** (state kept) — per-slide targeting forced the slide via the dots (`#dayScroll .sb-dots button`).
- **VM clock is UTC** — greetings read against UTC ("Good afternoon, Shawn." at ~13:xx UTC), per the brief.
- **Two probe lessons, recorded so nobody re-learns them:** (1) a raw-rect overlap check misfires on scroll-clipped content — overlap must be measured against the *visible* rect (clipped by scroll/overflow ancestors + viewport), as in `prove17c.py`; (2) a hit-test at rest is meaningless for an element below its slide's scroll fold (the Summary door) — judge it on Change-cover overlap at rest plus whole + tappable scrolled into view, as in `daysweep17c.py`.
- **No EPERM write failures** in this check: all checker writes went through the file tool / Node and were verified by size + sha. No `python3 … > file` redirections were used.
