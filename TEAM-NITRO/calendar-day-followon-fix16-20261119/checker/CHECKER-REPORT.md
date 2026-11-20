# CAL-FIX16 — CHECKER REPORT

**Checker:** independent (did not build) · **Date:** 2026-11-20 ~05:20 MST (VM clock ~12:20 UTC)
**Verdict: GOES BACK — the nav pills are fixed, but the floating "Change cover" button now collides with content at 390 on three slides.**

No merge, no live deploy, no link to Shawn. The captain's eye follows only a PASS.

## Verdict in one line

Everything the round set out to fix is fixed and re-proven — nav pills whole at rest on every block of every day at 1920 and 390, in both browsers and both font states — but the round introduces one new visible overlap at phone width and leaves a second one it claimed as whole: the floating "Change cover" button sits in the content band at 390 and covers the weather pill on the wisdom slide (6 of 7 days, fallback state — NEW in fix-16) and the "Smart Meet" pill on the Appointments slide (both browsers, both font states — pre-existing, but the maker claimed it "reads whole" and it does not). A third, smaller instance covers the "Your Journal" door on the Summary slide in the Chromium fonts state. All three share one root cause and one fix. The fix list is §9.

## 1. Filing — PASS (re-derived via the git blob API, never the maker's word)

Re-derived with `checker/proof/fetch-verify16.js` (gh-direct.py CLI, blob API):

| Claim | Re-derived |
|---|---|
| Branch `calendar/day-followon-fix16-20261119` | HTTP 200, tip `360056cb4ebbdd93d7397095bacea70354bdb599` — matches |
| Parent = fix-15 tip | Commit parents `['cf9e1132e4540e978fb5b94255b438b91bb149e9']` — matches |
| Commit message | `CAL-FIX16: bottom nav pills whole at rest (1920 + 390); wisdom stack tightened, Back/hello clear; Worlds/Appointments exempt from phone padding` |
| Filed blob `cc67fbf98388fbcbcf26287d82f3a81eb9d5d7c3` | 407,135 B, sha256 `ffc03030c555f034dd1608d3f78996d8c6455a963462bec5e51b64fa8e548ca3` — matches |
| Base blob `76539677f05b71729d96ae108b56ce7ddca95503` | 401,766 B, sha256 `958788c30b53e61f4848c533dee1adf21db084bd9d13d6ae94995135d7134d3e` — matches |
| Rebuilt (base + claimed block before `</style>`) | 407,135 B, sha256 `ffc03030…` — **rebuilt == filed blob: true** |
| Filed-minus-block == base | **true** |

## 2. Byte-diff — PASS (rebuilt from fetched base + block; `checker/proof/byte-checks16.js`)

- Block present exactly once, immediately before `</style>`; prefix and suffix match base byte for byte. Delta 5,369 B = block 5,368 B + newline.
- No JS changes: 1 inline script, 162,101 chars, byte-identical base→fixed, `new Function` parses OK.
- `COVER_DAY` byte-identical (sha `95e34520…`), `WISDOM` byte-identical (sha `efcb5ad4…`) — same shas the maker claimed. (Note: both are `var […]` arrays, not `const {…}` objects — my first regex missed them; the corrected extraction confirms identity.)
- New font sizes in the block: only `19px` (×2) — nothing under 17px. New hex colors in the block: none.
- FIX15 intact: marker present, `margin-top:160px` rule still present (overridden, not deleted). Quote 32px + 48px headliner rules intact.
- Badges: `worldIcon(…null…)` calls 9 = 9; `worldCount("personal")` 2 calls, `worldCount("work")` 0 — fix-14's five nulls intact, Personal keeps its real count.
- Elite booking intact: `elite-bookpill`, `elite-meetpill`, `[15, 30, 60]`, `mcFreeTimes`, `+ 30` buffer, `No full slot list`, `now.getMinutes() + 60` (+60-min notice), greeting ternary byte-identical.
- Structural tags: `</style>`, `</script>`, `</html>` counts 1/1/1 in both.
- `renderMonth()`: `for (i = 0; i < 42; i++)`, out-of-month cells render `'<div class="cell blank" …></div>'` with the comment "The other months are not shown at all — the cell stays blank, no numbers bleeding into this month."

## 3. Staged link serves the filed blob — PASS

- `curl`-equivalent fetch (Node https, browser User-Agent) on the staged link (`…&ref=calendar/day-followon-fix16-20261119&cb=cc67fbf98388fbcbcf26287d82f3a81eb9d5d7c3`): HTTP 200, 407,135 B, sha256 `ffc03030…` — **exact match to the filed blob**. Saved as `checker/proof/fetched-staged.html`.

## 4. Laws — PASS, delta 0 (`checker/proof/laws-check16.js`, outputs `laws-base16.txt` / `laws-fixed16.txt`)

- Base: **PASS — 0 FAIL / 28 WARN**. Fixed: **PASS — 0 FAIL / 28 WARN**.
- Warning texts identical after stripping filename/line (the raw diff is only the path + line number in the prefix). Line shifts: first 3 warnings (before the insertion point) unchanged; the other 25 shift by exactly **+78 lines** — the FIX16 block is 77 lines + newline = 78. **Delta 0 in substance, not just in count.**

## 5. Render — the nav defect IS fixed (all four legs)

Method (my own harness `checker/proof/prove16b.py`, Playwright sync; 2-second waits after every navigation — see the timing note in §8): filed bytes via `set_content`; rim line = `.rf-rim` bottom − 3 (the purple rim is a 3px border at inset `var(--bw)`; at 390 `--bw` is 32px so the rim line top is 809, at 1920 `--bw` is 96px so it is 900). "Whole at rest" = nav bottom ≤ rim line top, nav inside the viewport, no horizontal overflow. Firefox = no-webfont fallback (worst case; `document.fonts` empty — no webfont faces at all); Chromium via the localhost forwarder = fonts-loaded Great Vibes (verified `Great Vibes:loaded`).

### 5a. 7-day wisdom sweep, Nov 15–21 (teach + store whole at rest, weather pill one line ≥4px clear, nav whole, no horizontal overflow)

| Leg | Result | Worst day (nav clear of rim) |
|---|---|---|
| 390, Firefox, fallback | **7/7 PASS** | Sat 21: nav 755–799, **10px clear**; quote 6 lines; teach 616–709, store 710–748, pill 804–840, pill clear 56px |
| 390, Chromium, fonts-loaded | **7/7 PASS** | Sat 21: nav 633–677, **132px clear**; quote 3 lines in Great Vibes |
| 1920, Firefox, fallback | **7/7 PASS** | Day 15: nav 823–884, **16px clear**; quote 48px, 2 lines; all other days 18px |
| 1920, Chromium, fonts-loaded | **7/7 PASS** | Every day: nav 824–882, **18px clear**; quote 48px, 1–2 lines in Great Vibes |

Greeting true on all seven days in all four legs ("Good afternoon, Shawn." at ~12:xx UTC — true to the VM clock). `docScrollW` == viewport width in every sweep (no horizontal overflow). Back pill never overlaps the greeting (hello starts below the Back pill's band in every leg).

### 5b. Whole 9-block deck walk, day 19 (nav whole at rest on every slide)

| Slide | 1920 FF (clear) | 1920 Cr (clear) | 390 FF (clear) | 390 Cr (clear) |
|---|---|---|---|---|
| Wisdom | 820–882 (18) | 824–882 (18) | 703–747 (62) | 633–677 (132) |
| Notifications | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Journal | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Your Worlds | 820–882 (18) | 824–882 (18) | 685–745 (64) | 694–750 (59) |
| News Hub | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Appointments | 820–882 (18) | 824–882 (18) | 747–807 (**2**) | 751–807 (**2**) |
| Summary of the day | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Naya Notes | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |
| Smart Notes | 820–882 (18) | 824–882 (18) | 739–799 (10) | 743–799 (10) |

**Nav pills: 9/9 PASS in all four legs.** The Appointments nav at 390 is 2px clear in both browsers — thin, whole, and stable: re-measured four independent times (two focused probes + two deck walks) at 11:58–12:0x UTC, identical every time. The wisdom slide at 1920 in Great Vibes is beautiful (see §7).

### 5c. Buttons — PASS (real taps, both widths, both browsers)

- Last-slide Keep-reading advances the day: monthline `639 Hz` (Thu 19) → `396 Hz` (Fri 20) at 390 and 1920, Firefox and Chromium.
- Prev-day (first nav button) returns it: `396 Hz` → `639 Hz` in every leg.
- BACK TO MONTH lands on the month view: 42 cells, 30 numbered, 12 blank, month visible, "November 2026".

### 5d. Month-grid adjudication — NOT WRONG (agrees with the maker, with one correction)

Rendered month: 42 cells, 30 numbered Nov 1–30, 12 blank, row 6 (cells 35–41) all blank with no `data-d`. The code builds 42 cells by design and renders out-of-month cells blank with no numbers — exactly §7 ("the other month's numbers are GONE entirely, not dimmed"). **Correction to the maker's description:** row 6 is Dec **6–12**, not Dec 1–5 — Dec 1–5 sit in row 5's tail (cells 33–34 are Dec 3–4… precisely: cells 30–41 are Dec 1–12; row 5 holds Nov 29–30 + Dec 1–5, row 6 holds Dec 6–12). The conclusion stands: the blank sixth row is correct by design and is left untouched. No fix.

### 5e. Fix-15 regression — PASS except the two overlaps in §6 (same root cause)

- Wisdom whole, greeting correct, Worlds row whole, deck reads well (see §5a–5b and §7) — except §6.
- Journal empty-state line in full **at 1920**: "Your words save as you write — nothing typed is lost. Images stay with this day." (rect 645–683 FF / 634–667 Cr, `elementFromPoint` hits `P.none-line`, scrollW == clientW). At 390 the line sits below the Journal slide's internal scroll fold (rect 831–941 FF / 811–882 Cr) — reachable by the slide's own scroll, as in fix-15; the brief requires it in full at 1920 only.
- News badges **0** in all four legs; doors Local / Provincial / Global, no badges.
- Worlds-row badges real-or-gone: six cells — "0 Personal feed / Your private world.", "Business feed / Your work world.", "Your world / Worlds you belong to.", "Smart Mail / Mail that waits for you.", "Messages / Talk right now.", "Connections / Your people." Personal keeps its real `0`; the other five show no number (null = gone), as in fix-15. At 390 the grid is 2×3 with internal scroll (row 1 at rest, rows 2–3 after scrolling to the bottom — re-measured scrolled: all six rows land inside the viewport); at 1920 all six sit in one row (531–732). Labels and subtitles whole.
- Elite-booking logic intact (§2). Seven day covers + WISDOM byte-identical (§2). Inline JS parses (§2).
- **0 page errors in every leg** (four legs × sweep + deck + buttons + details).

## 6. THE DEFECTS — one floating button, three collisions at 390

The "Change cover" button is a single absolutely-positioned element, a child of `#dayScroll` (the deck container), floating over the deck on every slide. Its position trails the on-slide nav by ~31px, so wherever a slide's content runs long, the button lands in a band another element already occupies. At 1920 it sits at the right (x1635, y795–835) clear of everything — no collision in any 1920 leg. At 390 it collides on three slides:

### Defect 1 — Wisdom slide, 390, fallback state: Change cover half-hidden behind the weather pill (NEW in fix-16)

| Day | Quote lines | Nav | Change cover | Weather pill | Collision |
|---|---|---|---|---|---|
| 15, 16, 19, 20 | 5 | 703–747 | **778–818** | 804–840 | **bottom 14px hidden behind the weather pill** |
| 17 | 4 | 670–714 | 745–785 | 804–840 | none (fully visible in the gap) |
| 18 | 6 | 736–780 | **811–851** | 804–840 | hidden behind weather pill + frame |
| 21 | 6 | 755–799 | **830–870** | 804–840 | hidden behind weather pill + frame |

Measured in the Firefox fallback sweep, all 7 days: `ccOverlapsWeather = true` on 6 of 7 days; only day 17 (shortest quote) is clear. Read as a reader on day 19 (`shots16/sweep-firefox-nofont-390-19.png`, `shots16b/sweep-firefox-nofont-390-19.png`): the "Change cover" pill shows its top half and disappears behind "WEATHER · ENTER YOUR CITY" — a clipped pill on the first slide the user lands on. **This is new:** on the fix-15 base the wisdom nav sat at 985–1045 (below the fold) and Change cover sat at 1068–1108 — below the fold, invisible, no collision. Fix-16 pulled the nav (and the button trailing it) into view and into the weather pill's band. In the Chromium fonts-loaded state the stack is shorter (nav 633–677) and there is no collision — so the defect is fallback-only, which is exactly the worst case the brief names.

The maker's eye screenshot for wisdom at 390 (`maker/proof/eye-firefox-390-wisdom21.png`) is day 21 — the one day the button hides entirely behind the weather pill and frame — so the reading missed it. The collision is worst on the 5-line days (15, 16, 19, 20).

### Defect 2 — Appointments slide, 390, BOTH browsers, BOTH font states: Change cover covers the "Smart Meet" pill (pre-existing, but claimed whole)

- Smart Meet pill rect 678–737; Change cover rect 696–736; `elementFromPoint` at the pill's center AND bottom returns `BUTTON.pill:Change cover`. Only the top ~18px ("Sma…") is visible; the pill's text cannot be read and its lower two-thirds cannot be tapped (taps land on Change cover).
- Re-measured on the **fix-15 base bytes** with the same harness (`checker/proof/appt-focus.py base`): identical rects (nav 747–807, Smart Meet 678–737, Change cover 696–736, same hit results) — so it predates fix-16, and fix-16's exemption restored it byte for byte, as claimed.
- But the maker's report (§3d) claims "the Smart Meet pill reads whole at 390 (2px spare, as in fix-15)". That is false: the "2px spare" measures the pill against its scroll container (pill bottom 737 vs scroll viewport bottom 739) — the wrong reference object. The pill's scroll container is `[359, 359]` — there is **no scroll path** to reveal it. The maker's own screenshot (`maker/proof/fixed16-deck-firefox-390-5.png`, 11:43 AM) shows "Sma" + Change cover on top of it. Read as a reader, the booking pill is not whole.
- Present identically in Firefox fallback and Chromium fonts-loaded at 390. At 1920 there is no collision (Change cover sits right, clear of the booking pills).

### Defect 3 — Summary slide, 390, Chromium fonts state: Change cover covers the "Your Journal" door button (minor, same root cause)

- Chromium fonts deck, slide 6: Change cover 701–736 overlaps a door button reading "Your Journal — Nothing…" (rect intersection measured; screenshot `shots16b/deck-chromium-fonts-390-6.png` shows only the top arc of its green icon peeking out from behind Change cover). Not present in the Firefox fallback leg (ccXbtns empty there) — font-metrics-dependent. Unlike Defect 2, this button sits inside the slide's scrollable content (Summary `sbScroll` 983 vs 351), so a user can scroll to reveal it — it is clipped at rest, not unreachable. Listed as a fix-list item because the brief's bar is "no clipping anywhere" at rest; the maker must make it clear or show it is scroll-reachable and acceptable by the same measurement.

### What is NOT a defect

- The Appointments nav at 2px clear is thin but whole, stable across four independent measurements, and identical to fix-15 geometry — not a defect, but the fix must not eat into it (see §9).
- The Worlds Change cover at 768–808 (bottom 1px above the rim line) reads whole — not a defect.
- The month weekday header at 390 sits tight under the frame ornament — pre-existing, out of scope, noted only as an observation.

## 7. Read as a reader (screenshots)

- **1920 wisdom, Chromium/Great Vibes** (`shots16b/deck-chromium-fonts-1920-0.png`): beautiful — one-line script quote, greeting, teach line and store line whole, dots and pills whole with clear space, weather pill bottom-left whole, Change cover bottom-right whole, nothing overlapping. This is the 10/10 presentation the round achieves at desktop.
- **390 wisdom Sat 21, Firefox/fallback** (`shots16/sweep-firefox-nofont-390-21.png`): reads well — 6-line serif quote, teach and store whole, dots and pills whole. (Change cover is hidden behind the weather pill/frame on this day only — see §6.1.)
- **390 wisdom Thu 19, Firefox/fallback** (`shots16/sweep-firefox-nofont-390-19.png`): reads well EXCEPT the clipped "Change cover" pill wedged behind the weather pill — the defect a reader sees first at the bottom of the first slide.
- **390 Worlds** (`shots16b/worlds-firefox-nofont-390.png`): row 1 whole — "Personal feed / Your private world." and "Business feed / Your work world.", badge 0, icons large, no overlap.
- **390 Appointments, both browsers** (`shots16b/deck-chromium-fonts-390-5.png`, `shots16/deck-firefox-nofont-390-5.png`): "Book a time" whole; "Smart Meet" struck through by "Change cover" — not whole.
- **390 Summary, Chromium** (`shots16b/deck-chromium-fonts-390-6.png`): a green door button half-hidden behind "Change cover".
- **390 month** (`shots16b/month-firefox-nofont-390.png`): November 2026, 30 numbered cells, today (20) highlighted, sixth row blank — reads well, no Dec numbers.

## 8. §11 check (in writing)

1. **Is it right?** Yes to check; no merge, no live, no link to Shawn from this seat. The GOES BACK names real, visible overlaps rather than passing a page the captain's eye would immediately flag.
2. **Is it what they truly need?** Yes — the brief's bar is "nav pills whole" (proven) AND "no clipping anywhere" at 390 (not met — §6). The fix list in §9 is the whole of what is owed, nothing more.
3. **Is it mine to do?** Yes for checking; the fix itself belongs to the next maker round.
4. **Is now the time?** Yes — the defects are measured, stable, and reproducible on the filed bytes; the fix is one floating button's placement, not a redesign.
5. **Can I prove it?** Yes — every claim above is a hash, a rect, a hit-test, or a screenshot on the fetched filed bytes (proven identical to the staged link in §1/§3). Nothing is taken from the maker's report on trust.

**Design check (§11, on the rendered page):**
- Could I pick this up? The nav pills, orb, and tiles keep their materials and depth — nothing flat added (the block adds no colors, no fills). Laws checker: 0 FAIL.
- Light: one source, top-left — the block adds no gradients, no shadows.
- Text: the only new font sizes are 19px; quote stays 32px at 390 / 48px at 1920; nothing under 17px; no gray; no new text colors. Laws delta 0.
- Two same colors together: no colors added, nothing to break the flow.
- Reference objects: the fix reuses the page's own flex layout and the fix-15 bytes verbatim — one appended CSS block, nothing rebuilt, nothing invented. Harvest, never invent.
- Don't move / don't remove what he didn't ask: the only geometry changes are the nav clearance, the wisdom stack tightening (in scope), and the two exemptions (which restore fix-15 geometry). The frame, header, covers, data, badges, booking logic, and every other slide are byte-identical (§2).
- Read as a reader: the screenshots were read top to bottom as a reader — that reading caught the Change-cover collisions that the nav geometry checks passed (the navs pass while the button overlaps). Both are named in §6 with the evidence.
- **Timing note (my own probe lesson, recorded so nobody re-learns it):** slide transitions take >900ms to settle. My first deck walk used 900ms waits and measured navs ~9px low mid-animation (e.g. Appointments 756–814). With 2s waits the numbers are stable and reproduce the maker's exactly (Appointments 747–807). Any re-proof must wait ≥2s after each deck navigation — and must measure the Change-cover button, not only the nav, on every slide.

**Maker-handoff note:** the task mentioned one exec in the maker's run failed with exit code 3 and the maker still filed. I re-proved every claim independently from the filed blob (filing, bytes, staged link, all four render legs, laws); nothing in this verdict depends on the maker's scripts or screenshots. Two of the maker's claims did not survive re-proof and are named in §6: "Smart Meet pill reads whole at 390 (2px spare)" (false — it is covered by Change cover, and the 2px measures the wrong reference) and the month-row labeling "Dec 1–5 in row 6" (row 6 is Dec 6–12; the adjudication itself — not wrong — stands).

## 9. THE FIX LIST (for the next round — exact, nothing more)

All three items share one root cause: the single floating "Change cover" button (`position:absolute`, child of `#dayScroll`) sits in the content band at 390 and collides with whatever a slide puts there. Fix the button's placement at ≤560px; do not redesign any slide, do not touch the nav clearances, do not change any wording, color, or font size.

1. **Wisdom 390 (fallback, 6/7 days):** Change cover must not overlap the weather pill (`#wxBottomLeft .wx-btn`, 804–840). Today it sits 31px below the nav and lands at 778–818 (5-line days), 811–851 and 830–870 (6-line days). Anchor it clear of the weather pill's band on every day — e.g. pin it to a fixed spot that never enters 804–840, or hide it on the wisdom slide at ≤560px — and re-prove all 7 days in BOTH font states (fallback is the binding case; Chromium fonts state already clears).
2. **Appointments 390 (both browsers, both font states):** Change cover must not cover the "Smart Meet" pill (678–737). The pill has no scroll path (`sbScroll` 359/359), so it must read whole at rest — the full text "Smart Meet" visible and tappable, not "Sma" under Change cover. Same placement fix as (1); re-prove in both browsers.
3. **Summary 390 (Chromium fonts state):** Change cover must not cover the "Your Journal" door button at rest. Same placement fix; re-prove in Chromium fonts state (it already clears in Firefox fallback).
4. **Hold the line:** after the fix, the Appointments nav must still be whole at rest at 390 (today 747–807, 2px clear — the fix must not eat into it), and the 7-day sweep + 9-slide deck walk must re-pass in all four legs (1920/390 × Firefox/Chromium, both font states), with the Change-cover overlap measured per slide per day and reported as none. No other geometry may change: re-verify fixed-minus-block == base for everything outside the new fix, and laws delta 0.

## 10. Scorecard

| Check | Result |
|---|---|
| Filing (branch, tip, parent, blob, staged sha) | 10/10 |
| Byte-diff discipline (only the block; fix-15 intact) | 10/10 |
| COVER_DAY / WISDOM / booking / badges intact | 10/10 |
| Laws delta | 0 (0 FAIL / 28 WARN both, same texts, +78 line shift explained) |
| Item 1 — nav pills whole at rest, every block, every day, 1920 | 7/7 sweep + 9/9 deck, both browsers |
| Item 1 — nav pills whole at rest, every block, every day, 390 | 7/7 sweep + 9/9 deck, both font states (Appointments 2px, stable) |
| Weather pill one line, ≥4px clear | 56–197px clear on every swept day, all legs |
| Day-teach + store line whole at rest, all 7 days, 390 | 7/7, both font states (elementFromPoint hits) |
| Greeting true to time of day | "Good afternoon, Shawn." at ~12:xx UTC, all legs |
| Worlds six tiles readable | 6 cells, labels + subtitles whole, 2×3 + scroll at 390, one row at 1920 |
| Month-grid sixth row adjudicated | Not wrong — left untouched (row 6 = Dec 6–12 blank) |
| Buttons (keep-reading / prev-day / back-to-month) | PASS, real taps, both widths, both browsers |
| Page errors | 0 in all legs |
| **Change cover vs weather pill, wisdom 390 fallback** | **FAIL — overlaps 6/7 days (NEW in fix-16)** |
| **Change cover vs Smart Meet pill, Appointments 390** | **FAIL — covered in both browsers/states (pre-existing, mis-claimed whole)** |
| **Change cover vs "Your Journal" door, Summary 390 Chromium** | **FAIL at rest (scroll-reachable; same root cause)** |

**What would make it 10/10 whole:** the §9 fix (one button's placement at ≤560px) re-proven by the same four legs with the Change-cover overlap measured per slide per day and reported as none — then the round is proven end to end and the captain's eye can follow.

## 11. Files

- `checker/CHECKER-REPORT.md` — this report.
- `checker/proof/fetch-verify16.js` — filing + staged-link re-derivation (§1, §3); writes `fetched-base.html`, `fetched-fixed.html`, `fetched-staged.html` (407,135 B, sha256 `ffc03030…`).
- `checker/proof/byte-checks16.js` — byte-diff on the fetched bytes (§2).
- `checker/proof/laws-check16.js` + `laws-base16.txt` + `laws-fixed16.txt` — laws delta 0 (§4).
- `checker/proof/prove16.py` — first render probe (superseded: 900ms waits measured mid-animation; kept for the record — its sweep numbers reproduce, its deck numbers run ~9px low).
- `checker/proof/prove16b.py` — full render proof, 2s waits (sweep + deck + journal/worlds/news + buttons + month, all four legs) (§5).
- `checker/proof/appt-focus.py` — focused Appointments probe, fixed vs base (§6.2).
- `checker/proof/cc-walk.py` — 9-slide Change-cover walk, fixed vs base (§6).
- `checker/proof/cc-probe.py`, `checker/proof/struct-probe.py` — Change-cover structure/ancestry (single absolute button, child of `#dayScroll`).
- `checker/proof/shots16/` — first-probe screenshots (sweep, deck, month, Appointments focus).
- `checker/proof/shots16b/` — v2 screenshots (sweep/deck/month/worlds per leg).
- `checker/proof/forwarder.log` — Chromium proxy forwarder log (started for the Chromium legs, confirmed stopped afterwards; no process remains).

## 12. Environment notes (for the coordinator)

- **VM browsers alive throughout this check** (Firefox launch OK ~11:51 UTC; Chromium 156 via the localhost forwarder, `ignore_https_errors=True`). The forwarder was started for the Chromium legs and is confirmed stopped (no process remains). Note: `pkill -f h1-proxy-forwarder.py` also SIGTERMed my own exec shell (the documented trap) — the Chromium 1920 run had already completed and its full output was delivered; kill by PID next time.
- **Slide transitions take >900ms to settle** — re-proofs must wait ≥2s after deck navigation or the nav rects read ~9px low mid-animation (§8).
- **Day re-opens on the last-viewed slide** (state kept) — per-slide targeting must force the slide via the dots (`#dayScroll .sb-dots button`), not by re-opening the day and stepping.
- **VM clock is UTC** — greetings read against UTC, not MST ("Good afternoon, Shawn." at ~12:xx UTC), per the brief.
- **No EPERM write failures** in this check: all checker writes went through the file tool / Node and were verified by size + sha. No `python3 … > file` redirections were used.
