# CAL-FIX16 — Maker Report

**Verdict: FIXED and FILED — all scope items proven on the filed bytes.**
**Date:** 2026-11-20 (VM clock UTC; user asleep, silent work, no message sent)
**Maker:** Calendar day-followon fix-16, Team Nitro

## Filing identity

| Item | Value |
|---|---|
| Base branch | `calendar/day-followon-fix15-20261119`, tip `cf9e1132e4540e978fb5b94255b438b91bb149e9` |
| Base file | `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html` |
| Base blob | `76539677f05b71729d96ae108b56ce7ddca95503`, 401,766 B, sha256 `958788c30b53e61f4848c533dee1adf21db084bd9d13d6ae94995135d7134d3e` |
| New branch | `calendar/day-followon-fix16-20261119` (created from the fix-15 tip, HTTP 201) |
| Filed commit | `360056cb4ebbdd93d7397095bacea70354bdb599` (parent `cf9e1132…`) |
| Filed blob | `cc67fbf98388fbcbcf26287d82f3a81eb9d5d7c3`, **407,135 B**, sha256 `ffc03030c555f034dd1608d3f78996d8c6455a963462bec5e51b64fa8e548ca3` |
| Staged link | `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix16-20261119&cb=cc67fbf98388fbcbcf26287d82f3a81eb9d5d7c3` |
| Verification | Filed blob re-read via the git blob API: 407,135 B, sha256 `ffc03030…`, byte-identical to the local fixed file. Staged link curled with a browser User-Agent: 407,135 B, sha256 `ffc03030…` — matches the filed blob. |

## 1. Defect reproduction — root cause (measured on the fix-15 bytes)

**The defect (fix-15 eye, confirmed by measurement):** the three bottom nav pills
("‹ prev day", "Keep reading ◆", "next day ›") have their bottoms sliced off at the
day-view card's bottom edge on every block of every day at 1920×999, and the page
does not scroll to reveal them.

**Root cause, measured in Firefox + Chromium at 1920 and 390:**

- The nav is the last flex child of every slide and sits **flush at the block's
  bottom (nav bottom = block bottom − 1px)** on every slide, both widths.
- The royal frame (`.royal-frame`, fixed, z-40, `inset:0`, `--bw:96px` desktop /
  32px phone) has a purple rim (bottom edge y900–903 at 1920×999) and an ornate
  band below it (903–999). The deck bottom is y919, so the card extends 16px
  under the rim/band (8px at 390: deck bottom 820 vs rim top 809). The pills'
  bottoms (906 wisdom, 913 other slides at 1920) are painted over by the rim +
  band. Confirmed by pixel scan (purple line at y≈900–902 across all columns),
  `elementFromPoint`, and the rim rect.
- **There is no scroll path at desktop:** document scrollH == clientH == viewport;
  `#dayScroll` overflow is hidden at desktop. Nothing can reveal the pills.
- **At 390** the same flush geometry holds (non-wisdom navs 747–807 vs rim top 809,
  2px clear) and fix-15's `margin-top:160px` on the wisdom nav pushes it to
  985–1103 — 201px below the viewport, reachable only by an invisible deck scroll.
  Fix-15's maker claimed that scroll was the path; the eye proves it false.
  **That mechanism is not repeated.**
- FIX11's own comment states the intent the bytes fail: "the nav sits just above
  the frame edge."

## 2. The fix — one CSS block, inserted before `</style>`

File: `maker/proof/fix16-block.css` (5,368 B). The fixed file is the base plus
exactly this block — verified `fixed-minus-block == base` (bytecheck16.js).
No JS, no data, no markup touched. The quote stays 32px; nothing is hidden;
the frame, the header, and every other slide are untouched.

| Rule | Mechanism | Why |
|---|---|---|
| **§A — desktop/tablet** `@media(min-width:561px)`: `#dayScroll .smart-block{padding-bottom:24px!important}` | 24px of breathing room below the nav on every slide. | The scroll area absorbs it (smallest slack below any slide's last content row is 42px, wisdom), so no content is lost. Lifts every pill 18–21px clear of the rim at every viewport height (rim top = viewport − 99). |
| **§B — phone** `@media(max-width:560px)`: `#dayScroll .smart-block{padding-bottom:8px!important}` | 8px of breathing room below the nav on every slide. | Lifts the tall slides' navs 8px (807 → 799, 2px → 10px clear). 24px would clip Worlds row 1 at rest. |
| **Wisdom nav margin removed** `#dayScroll #wisdomBanner .sb-nav{margin-top:0!important;padding-top:0!important}` | Deletes fix-15's `margin-top:160px` (later in the file, same specificity, so it wins). | The margin is what put the wisdom nav below the fold at 390. The stack below is tightened instead, so the nav reads whole at rest. |
| **Wisdom stack tightened (≤560px)** | Orb 50→36px, hello 25px two lines → 19px one line, greet gap 8→24, label margins 1px, quote lh 1.15→1.03, teach lh 1.25→1.1, store lh 1.15→1.1, banner padding-top 0, nav buttons 52→36px, dots 10→7px. | The longest quotes must fit the 508px phone deck with the nav whole above the rim in the **worst** state (no-webfont fallback, 6-line quotes). Total saving ≈154px against 138px needed. The greet stays stacked (orb above the hello) because the absolute "Back" pill owns the top-left corner — a horizontal greet would sit under it. |
| **Greet gap is 24, not 4** | The hello must start at y60, 2px below the "Back" pill's band (top:14, 44px tall, y14–58). | My first tightening used gap 4, which put the hello at y40 — **under the Back pill, hiding "Good "** — caught by reading the screenshot as a reader, not by any geometry check (the orb did not overlap, so the overlap check passed while the greeting was unreadable). The +20px the gap costs is recovered exactly by the leading/margin cuts above. |
| **Exemptions** `#dayScroll .smart-block.worlds-slide{padding-bottom:0!important}` and `#dayScroll .smart-block[data-unfold-sec="appointments"]{padding-bottom:0!important}` (≤560px only) | The phone padding shrinks the scroll viewport 8px, which clipped two exact-fit slides: Worlds row 1 (subtitle ends 3px below the viewport) and Appointments (the Smart Meet pill ends 3px below it). Both slides' navs are already whole without the lift (Worlds 64px clear, Appointments 2px clear, exactly as in fix-15), so they are exempt — restoring their fix-15 geometry byte for byte. | Caught by the 9-slide content audit (base vs fixed, `slide-audit.py`), not by the nav checks — the navs passed while the content clipped. |

**Two measured non-levers (recorded so nobody re-learns them):**

- At 390 the wisdom slide is **content-driven**, 6px short of the deck cap — the
  bottom padding does **not** move its nav (nav bottom 804 with padding 8px and
  with 10px, identical). The nav moves only by cutting content above it, 1:1.
- At 390 the Worlds slide height is **pinned at 432px**, so the padding shrinks
  its scroll viewport instead of moving its nav.

## 3. Re-proof — final filed bytes

All runs on the filed bytes (`fixed-fix16.html`, sha256 `ffc03030…`), real render,
real taps. 0 page errors in every run. VM clock is UTC; the greeting follows it
("Good morning, Shawn." at 11:xx UTC — true to time of day).

### 3a. 7-day wisdom sweep, Nov 15–21 (teach + store whole at rest, weather pill one line ≥4px clear, nav whole, no horizontal overflow)

| Width / font state | Result | Worst day (nav clear of rim) |
|---|---|---|
| 390, Firefox, **no-webfont fallback** (worst: 6-line quotes) | **7/7 PASS** | Sat 21: nav 755–799, **10px clear**; teach 616–709, store 710–748, pill 804–840, pill clear 56px |
| 390, Chromium + forwarder, **fonts-loaded Great Vibes** (first build; later changes only shrink the stack and restore Worlds/Appointments to base geometry, so the final state is bounded by the Firefox worst case) | **7/7 PASS** | Sat 21: nav 723–769, **40px clear**; quote 5 lines |
| 1920, Firefox, fallback | **7/7 PASS** | Day 21: nav 820–882, **18px clear**; quote 2 lines |
| 1920, Chromium, fonts-loaded | **7/7 PASS** | Every day: nav 821–882, **18px clear**; quote 2 lines |

Greeting true on all seven days in both font states; `docScrollW` == viewport width
in every sweep (no horizontal overflow at 390 or 1920).

### 3b. Whole 9-block deck walk, day 19 (nav whole at rest on every slide)

| Slide | 1920 Firefox (clear) | 1920 Chromium (clear) | 390 Firefox (clear) | 390 Chromium (clear) |
|---|---|---|---|---|
| Wisdom | 820–882 (18) | 821–882 (18) | 703–747 (62) | 670–716 (94) |
| Notifications | 830–890 (10) | 821–882 (18) | 739–799 (10) | 740–799 (10) |
| Journal | 828–888 (12) | 821–882 (18) | 739–799 (10) | 740–799 (10) |
| Your Worlds | 820–882 (18) | 821–882 (18) | 685–745 (64) | 679–738 (71) |
| News Hub | 820–882 (18) | 821–882 (18) | 739–799 (10) | 740–799 (10) |
| Appointments | 820–882 (18) | 821–882 (18) | 747–807 (**2**, whole as in fix-15) | 740–799 (10) |
| Summary of the day | 820–882 (18) | 821–882 (18) | 739–799 (10) | 740–799 (10) |
| Naya Notes | 828–888 (12) | 821–882 (18) | 739–799 (10) | 740–799 (10) |
| Smart Notes | 820–882 (18) | 821–882 (18) | 739–799 (10) | 740–799 (10) |

**9/9 PASS in all four legs.** The Appointments nav at 390 in Firefox is 2px
clear — whole, exactly the fix-15 geometry (its slide is exempt from the phone
padding; see §2). The "Back" pill never overlaps the orb or the greeting in any
leg (hello starts 2px below the Back pill at 390 in both browsers, measured).

**Button destinations (clicked through, 1920, both browsers):** last-slide
Keep-reading advances the day (monthline 639 Hz Thu → 396 Hz Fri); the prev-day
button returns it (396 → 639 Hz); BACK TO MONTH lands on the month view (30
cells visible). No errors.

### 3c. Month-grid sixth row — adjudication

**Not wrong. Left untouched.** `renderMonth()` builds 42 cells by design; the
code comment states "The other months are not shown at all — the cell stays
blank, no numbers bleeding into this month." Nov 1 2026 is a Sunday, so rows
1–5 hold Nov 1–30 and row 6 holds Dec 1–5 (blank) + Dec 6–12 (blank). The month
screenshot shows the blank row reading as quiet empty space in the grid's own
treatment — not an error, and per §7 the next month's numbers correctly do not
bleed in. No fix.

### 3d. Full fix-15 regression

- Wisdom whole, greeting correct, Worlds row whole, deck reads well — see §3a–3b
  and the screenshots read as a reader (below).
- Every button lands right — see §3b.
- Keep-reading last-slide behaviour — advances the day, slide kept per FIX11
  item 9 (dayShow wraps + key remap) — see §3b.
- Journal empty-state line in full at 1920 — screenshot `fixed16-deck-firefox-1920-2.png`:
  "Your words save as you write — nothing typed is lost. Images stay with this day."
- News badges **0** — screenshot `fixed16-deck-firefox-1920-4.png`: Local /
  Provincial / Global doors carry no badges.
- Worlds-row badges real-or-gone — byte-identical to fix-15 (null count 9 = 9);
  Personal feed shows a real "0", the other five worlds show no number (null =
  gone), as in fix-15.
- Elite-booking logic intact — `elite-bookpill` / `elite-meetpill` present in
  both bytes; the Smart Meet pill reads whole at 390 (2px spare, as in fix-15).
- Seven day covers byte-identical to fix-15 — `COVER_DAY` sha `95e34520…`,
  `WISDOM` sha `efcb5ad4…`, verified identical.
- 0 page errors in both font states, all four legs.
- JS parses (single inline script, 162,101 chars, `new Function` OK).

### 3e. Read as a reader (screenshots)

- **1920 wisdom, Chromium/Great Vibes** (`eye-chromium-1920-wisdom19.png`):
  "Do no harm, to yourself or to others — all is connected, all is one." in the
  certificate script face, 2 lines, generous; greeting, teach, store line, dots
  and pills all whole with clear space above the rim; weather pill whole.
- **390 wisdom Sat 21, Firefox/fallback** (`eye-firefox-390-wisdom21.png`):
  the worst case reads well — greeting whole and clear of Back, 6-line serif
  quote, teach and store whole, dots and pills whole, weather pill whole.
- **390 Worlds** (`reprove-firefox-390-worlds2.png`): row 1 subtitles read in
  full — "Your private world." / "Your work world." with their periods.
- **1920 Journal / News Hub** (§3d): empty-state line in full; no news badges.

## 4. Design laws — delta 0

`check-design-laws.py` on base and fixed:

- Base: **PASS — 0 FAIL / 28 WARN**
- Fixed: **PASS — 0 FAIL / 28 WARN**
- Warning sets identical (diffed after stripping filenames/line numbers) → **delta 0**.

## 5. §11 check (in writing)

1. **Text laws:** the only text touched is spacing/leading — no wording changed.
   Quote stays 32px (the floor the brief sets); the 25/19/17 scale is untouched.
2. **Real objects:** no element is flattened or re-skinned; the pills, the orb,
   the tiles keep their materials and depth. The nav lift is breathing room, not
   a redesign.
3. **Harvest first:** the fix reuses the page's own flex layout and the fix-15
   bytes verbatim — one appended CSS block, nothing rebuilt, nothing invented.
4. **Don't move what he didn't ask to move:** the only geometry changes are the
   nav clearance, the wisdom stack tightening (in scope: the pills must read
   whole), and the two exemptions (which *restore* fix-15 geometry). The frame,
   header, covers, data, badges, booking logic, and every other slide are
   byte-identical.
5. **Read as a reader:** the screenshots were read top to bottom as a reader —
   that reading caught the Back/hello overlap and the Worlds/Appointments clips
   that the geometry checks passed. Both are fixed and re-proven.
6. **Prove before reporting:** every claim above is a measured rect, a hash, or
   a screenshot on the filed bytes — not a maker assertion.

## 6. Scorecard

| Check | Result |
|---|---|
| Pills whole at rest, every block, every day, 1920 | 7/7 sweep + 9/9 deck, both browsers |
| Pills whole at rest, every block, every day, 390 | 7/7 sweep + 9/9 deck, both font states (Firefox worst case binding) |
| Weather pill one line, ≥4px clear | 52–147px clear on every swept day |
| Day-teach + store line whole at rest, all 7 days, 390 | 7/7, both font states (elementFromPoint hits) |
| Greeting true to time of day | "Good morning, Shawn." at 11:xx UTC, all legs |
| Worlds six tiles readable | Row 1 whole, subtitles in full (screenshot + geometry = base) |
| Month-grid sixth row adjudicated | Not wrong — left untouched |
| Fix-15 regression | Full pass (§3d) |
| Laws delta | 0 (0 FAIL / 28 WARN both) |
| Page errors | 0 in all legs |

**Known thin margins (stated plainly, not hidden):** the Appointments nav at 390
in Firefox is 2px clear of the rim — whole, exactly the fix-15 geometry, and the
checker will re-measure it on the filed bytes. The wisdom worst day (Sat 21,
Firefox fallback) is 10px clear. Both are deterministic (same bytes, same
browser, same viewport) and will reproduce.

## 7. Files (all under `~/workspace/team-nitro/calendar-day-followon-fix16-20261119/`)

- `maker/MAKER-REPORT.md` — this report.
- `maker/proof/fix16-block.css` — the fix (5,368 B), the only change.
- `maker/proof/fixed-fix16.html` — the filed bytes (407,135 B, sha256 `ffc03030…`).
- `maker/proof/base-fix15.html` — the verified base (401,766 B).
- `maker/proof/staged-fix16.html` — the staged-link read-back (hash-matched).
- `maker/proof/build-fixed16.js` — byte-safe build (Buffer ops) + verification.
- `maker/proof/bytecheck16.js` — byte regression (diff, JS parse, covers, badges).
- `maker/proof/prove-fixed16.py`, `prove-1920.py` — render probes (7-day sweep + deck walk).
- `maker/proof/reprove-390.py`, `worlds-check.py`, `worlds-mech.py`, `slide-audit.py` — targeted re-proves and the 9-slide content audit.
- `maker/proof/eye-shots.py` — eye screenshots (wisdom 1920 + 390, Worlds).
- `maker/proof/*.log`, `laws-*.txt` — probe logs and the laws warning sets.
- `maker/proof/fixed16-*.png`, `eye-*.png`, `reprove-*.png` — screenshots (sweep, deck, month, Worlds, wisdom).
- `maker/proof/branch-body.json` — branch-creation record. (`put-body.json` removed after filing; the filed bytes live in `fixed-fix16.html`.)
