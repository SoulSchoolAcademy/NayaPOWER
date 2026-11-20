# Calendar Round 2 — Maker Report

**Round:** `calendar/day-followon-round2-booking-20261120`
**Page file:** `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html`
**Base:** branch `calendar/day-followon-fix18-20261120`, tip `ffd220c7d7d54fbbfc08c82ceed793ce1b0968a3`,
HTML blob `f7b14ce75d590738a9efb87a4fa056ee98f3561d`, 413,386 B,
sha256 `52ff950fb4dfeb942415c96ee2af393b815e06e9019c77a9758121a9f40770cc`
**New branch:** `calendar/day-followon-round2-booking-20261120`, from tip `ffd220c7`
**Built:** 2026-11-20, maker seat (subagent, depth 2/2)
**Built file (in memory):** 431,254 B, sha256
`3e9f0ecefaa1945e58455ccdef4ea773f5760e7712ef30b4448859f05cac0fdf` (5,779 lines)
**Status:** built and proven at code level. **No browser taps were possible from this seat** — see §3.
No merge, no live deploy, no message to Shawn.

---

## §1 — Item 1: the gap fix (first in the diff)

### What changed

| Edit | Change | Line(s) in built file |
|---|---|---|
| E2 | Fix-18 rule `gap:24px` → `gap:27px` on `.hl-center .hl-monthline` (Great Vibes loaded) | 3113 |
| E2b | New fallback rule `.hl-center .hl-monthline.gv-fallback{gap:24px!important}` | 3127 |
| E4/E5 | `r2SyncMonthlineFont()` — a JS font-load class: adds `gv-fallback` to the monthline when Great Vibes has NOT loaded, removes it when it has; called from `openDay` where the monthline is built | 5405 (def) |

The gap is now **per font state**, because one value cannot give a true 24px ink gap in both states.

### Why 27 / 24 — measured, not assumed

I measured the actual font files at 32px "November" (Pillow/FreeType, in memory):

| Font state | Advance | Ink width | Trailing overhang past the box |
|---|---|---|---|
| Great Vibes (loaded) | 106.3 | 110.0 | **2.7px** (ink runs 2.7px past its box) |
| DejaVu Serif (VM Firefox fallback — matches the fix-18 fallback box width 170 exactly) | 169.3 | 170.0 | −0.7px (ink ends at the box edge) |
| Noto Sans / Noto Serif / Liberation Serif | 158.2 / 160.6 / 135.1 | 158.0 / 161.0 / 135.0 | ≤0.7px |

So at flex gap 24 the ink-to-tile gap is **21.3px** with Great Vibes loaded and **≈24px** on fallback.
The fix: **27px when Great Vibes is loaded** (24 + 2.7 overhang = 26.7 → 27, ink 24.3px)
and **24px on fallback** (ink ≈24.2–24.7px). The 27 breaks the 8px-grid preference;
the measured 24px-ink target wins, and this tension is named here, not hidden.

### The honest measurement conflict

The eye's 16px (desktop leg, cloud browser 1919×998, NOVEMBER ink ends x=993, 2026 ink
starts x=1010) **does not reproduce from font metrics in any font state at 32px**:
every fallback face ends its ink at the box edge (bearing ≤0.7px), so fallback ink gap ≈
flex gap ≈ 24; Great Vibes gives 21.3. No state gives 16. The eye's absolute coordinates
(span 837–1078, 241 wide) match no measured layout of the monthline (Great Vibes total
259, fallback totals 280–323). Possible contributors, not proven: the script's thin
trailing flourish and the digit tiles' soft glow being read as visible edges in a
screenshot. **Only a live-browser re-measurement settles this.** The 27/24 fix is the
best calculation from the font evidence; it is not a re-proof of the eye's 16px.

### What is still owed on the gap (checker / eye)

- Re-prove glyph-to-glyph with Range rects at **1920 and 390, both font states** (Great
  Vibes loaded + fallback), and confirm the ink gap is 24px in all four legs, centred
  (offset 0px), one line, no wrap, `docScrollW` stays 390 at 390 fallback.
- At 390 fallback the monthline is 280px wide in a 240px column (overflows 20px/side
  into clear black field). Widening the gap adds width — the checker must verify
  neighbours stay clear and `docScrollW` stays 390. If a 24px ink gap cannot be held
  at 390 fallback without clipping, say so with measurements rather than forcing it.

---

## §2 — Item 2: the ultimate booking (inside the Appointments slide, index 5)

### What changed

| Edit | Change | Line(s) |
|---|---|---|
| E1 | `LS_KEYS` gains `maildraft: "nayacal.maildraft.v1"`, `reminders: "nayacal.reminders.v1"` | 3481 |
| E3 | ROUND2 CSS: kind pills (`.r2-kind`, one lit), step labels, 6-per-page times, "more times", refused note, confirmation board (`.r2-confirm`, emerald rim), mail/reminder lines, change/done actions | 5357+ |
| E4/E5 | `__mc` gains `kind` (null until picked; `'meet'` if opened with meet=true), `timePage` (0), `confirmed` (null), `refused` (null) | — |
| E6 | New `mcRenderCal`: **Step 1** kind pills (Smart Meet purple `#8e24aa` / In person gold `#d4a017` / Call sapphire `#0f52ba`, one lit via `aria-pressed`); **Step 2** the 7-day strip harvested from fix-12 (`mcRenderCal` weekday colours, no-free-time days dimmed); **Step 3** the next **6** open times as digit-tile pills (`per = 6`, `times.slice(page * per, page * per + per)`) with a "More times · N left" / "Back to the first times" step; duration select kept (15/30/60) | 5448 |
| E7 | New `mcRenderForm`: name/alias + "What is it?" + "Who is it with?" (harvested from the current form), the kind carried as the lit choice (changeable in place), ONE Book button (emerald `#07925f`) | 5493 |
| E8 | New `mcOpen`: opens the slide flow; kind defaults to `'meet'` only when opened from a Smart Meet doorway | — |
| E9 | New `mcBook`: **double-booking guard** — recomputes `mcFreeTimes` and refuses with "That time is taken now — here are the next open times." if the slot is gone (except the edit's own time); on success stores `{time, title, meet, who, dur, how}`, saves a mail draft (localStorage `nayacal.maildraft.v1`, capped at 50) and a reminder (localStorage `nayacal.reminders.v1`, 30 min before, capped at 50), sets `__mc.confirmed` | 5518 |
| E9b | `r2RefreshTiles()`: rebuilds the booked tiles + timeline in place using openDay's row template verbatim, re-wires Join buttons | 5562 |
| E9c | `mcRenderConfirm()`: confirmation board — "Booked", title, when-line, "With X · kind", Join button if Smart Meet (`id="r2Join"`, **direct listener** → `openMeetRoom(found)`, not `data-join`), "Smart Mail — draft saved… It sends when Smart Mail connects.", "Reminder set — 30 minutes before, kept on this device.", Change time / Done | 5583 |
| E10 | `eliteApptsHTML(dc, apptRows, tl)`: rest state now shows the day's booked tiles + the **full 6 AM–9 PM timeline** (timelineHTML — it was computed and passed in but never shown on this slide) + **ONE** doorway pill ("Book a time"). The second bare button (Smart Meet) is gone — Smart Meet is a kind inside Step 1 now | 5627 |
| E11 | `openBookFor(timeHHMM)`: a timeline slot books on the Appointments slide (not in the door); the slot's hour pre-picks its first open time, or reports "That hour is full" | 5356 |
| E12 | Call site passes the timeline in: `eliteApptsHTML(dc, apptRows, tl)` | — |
| E13 | Delegated handler: kind pills + more-times branches added; `tileMeetBtn` / `mcMeet` branches dropped; day/time/duration changes reset page + refused note; edit carries kind + clears confirm; dead `#tileMeetBtn` CSS rule dropped | — |
| E14 | The door's book form gets the same no-double-booking guard (refuses taken times, stores `dur: 60, how`) | — |

### The engine — harvested verbatim, not rebuilt

`mcFreeTimes` (6 AM–9 PM, 15-min steps, 30-min buffer after every booking, no booking
inside the next hour), `dayDigitsHTML` time pills, `mcDayHasFree`, edit (tap a tile to
change its time) + Cancel (`mcCancelIdx`), localStorage persistence (`LS_KEYS.appts`,
`saveStores`), the 7-day strip, the Smart Meet toggle + join flow (`openMeetRoom`,
`data-join` wiring on the tiles — untouched), and `renderMonth` (one dot per booking,
up to 3, on the month cell) are all unchanged. The full-list time render
(`times.map(...)` — up to 60 pills, the wall) is gone: the only render is the 6-per-page
slice (verified: `slice(page * per, page * per + per)` with `per = 6`; the old
full-list string occurs 0 times in the built file).

### Sense-check decisions (made, not duplicated)

- **"How to meet" appears ONCE.** The brief listed it as Step 1 and again after Step 3.
  It is the same choice, so it is presented once as Step 1 and carried through to the
  form and the confirmation as the lit kind (changeable in place). Duplicating it
  would have been doubling up.
- **"Call" has no pre-existing part on the page.** The kinds come from the page's own
  vocabulary: Smart Meet (the pill + the meet room) and "in person" (the meet-room
  fallback text "meet in person"). "Call" rides the same pill choice and is stored as
  data (`how: "call"`); there is no call UI on the page to harvest. Named here rather
  than inventing a call category.

### What is honestly live-only

- **Smart Mail is NOT connected on this page** (the door says so: "Smart Mail is not
  connected yet — no mail to show for this day"). The confirmation stores a mail draft
  in localStorage and says "It sends when Smart Mail connects." **No sent mail is
  faked.** Actual mail delivery needs live Smart Mail.
- **The reminder is stored in local state** (30 min before, kept on this device).
  Firing it needs the live scheduler.
- **The other person's calendar ("theirs")** needs live — a booking shows on OUR day
  (tile) and OUR month (dot); the invitee's side cannot be proven on staged.

### Booking acceptance — status per item

| Acceptance item | Status from this seat |
|---|---|
| A stranger cold can book in three steps | Built (Step 1 kind → Step 2 day → Step 3 time, then name + one Book button). **Tap proof owed — see §3.** |
| Every step proven by real tap at 1920 and 390 | **NOT PROVEN — browsers dead (§3). Checker/eye must tap.** |
| Confirmation lands + Smart Mail composed + reminder set | Confirmation board renders from state (code-verified); mail draft + reminder are localStorage writes (code-verified, 1 occurrence each). **Tap proof owed.** |
| Change/cancel in one tap | Built (`r2Change` re-opens edit; tile tap edits; `mcCancelIdx` cancels). **Tap proof owed.** |
| No double-booking | Guard built in `mcBook` + the door form; refuse path renders "That time is taken now…". **Live double-book tap test owed.** |
| Shows on the DAY (tile) and the MONTH (dot) | Built (`r2RefreshTiles` + `renderMonth` dots, unchanged). **Tap proof owed.** |
| Slide at rest reads as a real booking app | Built: booked tiles + timeline + one doorway. **Eye read owed.** |

---

## §3 — Proof status: what is proven, what is not (read this first)

### Proven from this seat (in memory, verified bytes)

- **Build:** all E1–E14 replacements applied with exact occurrence counts; all 10 scope
  checks pass (fix-17 block intact, wisdom hide intact, fix-18 item-3 rule intact,
  Hz segment 0, gap 27 present, fallback rule present, ROUND2 marker, `tileMeetBtn`
  count 1 = the dead `apptsTile` string only, `mcMeet` toggle 0, full-list time render
  gone). Inline script syntax OK (`vm.Script`, 173,519 chars, 1 script tag).
- **Emit identity:** 431,254 B, sha256
  `3e9f0ecefaa1945e58455ccdef4ea773f5760e7712ef30b4448859f05cac0fdf` — the same
  bytes the filer sends (the filer re-verifies size + sha from the pipe before filing).
- **Invariants grep-verified on the emitted bytes:** `mcFreeTimes` definition intact;
  `eliteApptsHTML(dc, apptRows, tl)` call site; `per = 6` paging slice; kind pills 13
  occurrences (`r2-kind`); mail draft + reminder keys 1 each; confirmation Join is a
  direct listener (`r2Join` → `openMeetRoom`); door guard present; Book emerald
  `#07925f` and Smart Meet purple `#8e24aa` present; `mcCancelIdx` + `renderMonth` present.
- **Laws:** `check-design-laws.py` run on the emitted bytes (via `/dev/stdin`) — **PASS,
  0 FAIL / 28 WARN**; base file run the same way — **PASS, 0 FAIL / 28 WARN**.
  **Laws delta 0** (the same 28 warnings, line numbers shifted +40 by my insertions).

### NOT proven — the blocker, stated plainly

**No browser taps were possible from this seat.** The VM browsers are dead in this
window (re-tested 2026-11-20 ~17:30 MST with `probe-browsers.py`: Firefox SIGSEGV on
launch, Chromium "Target page, context or browser has been closed" on launch — the
same deaths the fix-18 eye hit). This subagent also has no live-browser tool. So:

- The gap re-proof (Range rects, 1920 + 390, both font states) is **owed**, not done.
- Every booking tap (steps, counts, confirmation, change/cancel, double-booking
  refusal, day + month markers) at 1920 and 390 is **owed**, not done.
- The full regression sweep (fix-17, fix-18 items 2–3, deck/nav 7/7 + 9/9, buttons,
  month grid row 6 blank, 0 page errors) is **owed at tap level**, not done.
  Code-level scope checks for the regression items pass (see §4), which is not the
  same as a tap sweep — I do not claim it is.

**Filing proceeds on my own proof per the corrected sequencing (§3/§6 of the brief):
the 390 eye leg does not exist and is not waited for. Shipping still waits for a
390 eye leg.**

### Tap list for the checker / eye (run on the staged link, both widths)

1. Open a day, go to Appointments: booked tiles + timeline + ONE "Book a time" pill at rest.
2. Book a time → Step 1 kind pills (3, one lit) → Step 2 day strip (7 days, weekday
   colours, dimmed where no free time) → Step 3 shows **≤6** time pills + "More times".
   Count the pills. Tap "More times" — the next 6 appear.
3. Fill name + "What is it?" + "Who is it with?" → ONE Book button → confirmation board
   shows title, when, with whom, how; mail line says the draft is saved and sends when
   Smart Mail connects; reminder line says 30 minutes before.
4. Book the same slot twice — the second must be refused or offered another time.
5. Tap the booked tile → change its time (one tap); cancel (one tap).
6. Check the booking shows on the DAY as a tile and on the MONTH as a dot.
7. Gap: Range-rect ink gap 24px at 1920 + 390, Great Vibes loaded and fallback;
   centred, one line, `docScrollW` 390 at 390 fallback.
8. Regression sweep (§4) at both widths; 0 page errors in every leg.

---

## §4 — Regression (code-level; tap level owed per §3)

- Fix-17 block intact (scope check OK); wisdom hide rule intact; fix-18 item-3 rule
  intact; Hz segment 0 occurrences; `tileMeetBtn` only in the dead `apptsTile` string
  (never inserted); month grid, bottom bar, `COVER_DAY`, `WISDOM`, `DAY_FREQ` /
  `DAY_COLORS` / `DAY_MEANING` untouched (no edit touches them — E1–E14 are all inside
  the monthline rule, the booking functions, `eliteApptsHTML`, `openBookFor`, the
  delegated handler, and the door's book form).
- Do-not-touch list honoured: the fix-17 block; the fix-18 block except the gap value;
  `COVER_DAY`; `WISDOM`; `DAY_FREQ` / `DAY_COLORS` / `DAY_MEANING`; the month grid;
  the bottom bar. Nothing moved that he didn't ask to move; nothing removed that he
  didn't ask to remove (the two bare buttons and the wall of pills were the brief's
  explicit removals).

---

## §5 — Design laws (§11 check, in writing)

Applied laws: §1 real objects (every booking step is a real object — kind pills,
time pills, Book button, confirmation board: alive on hover, press in/out, per the
ROUND2 CSS depth treatment); §2 text (25/19/17, no gray, white — checker PASS, 0
FAIL); §3 color (spectrum flow; Friday ruby `#c62828`, 396 Hz untouched; kind colours
are the page's own: Smart Meet purple, In person gold, Call sapphire — never the same
together with Book emerald); §4 objects (board/pill/tile/digit-tile anatomy; 135°
gradient per the law book — the brief's "145°" paraphrase is superseded by the law
book's 135°; 1px border, inset top highlight crescent, grounding shadow, accent glow);
§5 buttons (Book emerald `#07925f`, Smart Meet purple `#8e24aa` — never the same
together); §7 day/calendar (the day is a cockpit; appointments as tiles; the timeline
is now shown); §9 layout (Step 1/2/3, blatantly obvious; mobile first, judged at phone
width first — the 390 gap leg is owed, §3); §11 check + sense check on the PAGE.

**§11 check:** I ran `check-design-laws.py` on the emitted bytes — PASS, 0 FAIL /
28 WARN, delta 0 against the base. I checked the page, not just the diff: the
Appointments slide at rest now presents booking as a real thing (tiles + timeline +
one doorway) instead of two bare buttons on blank space; the "how to meet" choice is
made once, not twice; the wall is gone (6 at a time, never 60). Parts came from
`THE-OFFICIAL-PARTS.md` / the page itself (`mcFreeTimes`, `dayDigitsHTML`,
`mcRenderCal` strip, `openMeetRoom`, `timelineHTML`, the day row template) — harvested,
never invented. No part was needed that the registry lacks.
**Sense check on the page:** a stranger cold sees Step 1/2/3 and one Book button; the
confirmation tells them what, when, with whom, how, and honestly what happens next
(draft saved, sends when Smart Mail connects) instead of faking a sent mail.

**Self-score: 7/10.** The build is complete and code-proven, the laws hold, the gap
math is measured — but a 7, not a 10, because no browser tap has landed from this
seat: the gap re-proof, the booking flow, and the regression sweep are all owed to
the checker/eye. A 10 needs the taps.

---

## §6 — Filing

- **How:** the EPERM flake blocked every file write from this seat for the whole
  build window (Node `writeFileSync`/`writeSync` EPERM, `curl -o` exit 23, shell
  redirects and `cat`/`head`/`cp` EPERM even at 100 bytes, 10 consecutive emit
  attempts EPERM, 5 pipe-cat attempts EPERM over ~100 s — while the file tool
  `muse.write`/`muse.edit` lands reliably). The built file was therefore **never
  materialised on local disk**. It is filed **in memory**: the build script emits
  the bytes to a pipe, the filer reads them from stdin, verifies size (431,254)
  + sha256 (`3e9f0ece…`), and PUTs them to GitHub via the contents API
  (`gh-direct.py` token minting, in memory). The local `fixed-round2.html` in
  `maker/proof/` is 0 bytes — a flake casualty, not the file; do not trust it.
  Rebuild it any time with `EMIT_STDOUT=1 node build-round2.js | cat > fixed-round2.html`
  once the flake clears, and verify against the sha above.
- **Files filed (one commit on `calendar/day-followon-round2-booking-20261120`,
  parent `ffd220c7`):**
  - `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html`
    (update; current blob `f7b14ce7…`)
  - `TEAM-NITRO/calendar-day-followon-round2-booking-20261120/CAL-ROUND2-BRIEF.md`
    (the brief, filed under the fix-17 naming pattern)
  - `TEAM-NITRO/calendar-day-followon-round2-booking-20261120/maker/MAKER-REPORT.md`
    (this report)
- **Filed and verified (amended after read-back):**
  - Branch `calendar/day-followon-round2-booking-20261120`. Filing identity (stable):
    HTML commit `dc9d9f2a15599aa0f639ef0f21e22f31cbca5b66`, parent `ffd220c7`,
    followed by the brief commit `0670141ea1b890761f202edaffd3cfd93423b873` and
    report commits. The branch tip moves when this report is amended — read the
    tip from the branch, not from this line.
  - HTML blob `04e79488a8acda56ff3b7a5e55737341f525dae9`, 431,254 B, sha256
    `3e9f0ecefaa1945e58455ccdef4ea773f5760e7712ef30b4448859f05cac0fdf` —
    read back from the blob API: size-ok, sha-ok.
  - Brief blob `68d9f6448bfad2bfe7459cf682269bcce9de139b`; report blob
    `f49fe05f6d6d99e98a5046dccbf2219c9afe3798` (this report, as filed).
  - Staged link serves the filed blob byte-identical — verified 3× by curl:
    431,254 B, sha256 `3e9f0ece…`, match True every time.
- **Staged link:**
  `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-round2-booking-20261120&cb=04e79488a8acda56ff3b7a5e55737341f525dae9`

## §7 — What the checker / eye must do next

1. Tap list §3 (booking flow + double-booking + change/cancel + day/month markers).
2. Gap re-proof §1 (Range rects, both widths, both font states).
3. Regression sweep §4 at both widths, 0 page errors.
4. Shipping still waits for a 390 eye leg (full re-proof at 390 once a browser is alive,
   or via a cloud-browser 390 leg).

## §8 — Environment notes for the record

- EPERM flake, seventh refinement (2026-11-20 ~17:13–17:30 MST): in this window the
  flake blocks **all** file writes from exec'd processes — Node sync writes, shell
  redirects, `cat`/`head`/`cp`/`printf` (even 100-byte literal writes), at both
  `/tmp` and the workspace — while the runtime file tool lands and while reads,
  pipes, and network calls work. It flips on a seconds-to-minutes scale (writes
  landed at ~17:23–17:24 and failed seconds before and after). A 0-byte file poisons
  its path; `process.exit()` after async stdout writes drops the bytes (the first
  emit landed 0 bytes for exactly this reason — fixed by removing the exit and
  letting the streams drain). `node --check` passes; the build script's own checks
  all pass. Lesson for the next seat: **never trust a redirect for a large file in
  a flake window — pipe to a verifier, or file from memory.**
- `sed -i` destroyed `build-round2.js` once in this session (truncated to 0 bytes);
  the script was rebuilt via the file tool and is intact at 35,150 B
  (`maker/proof/build-round2.js`, chunks 1–3 + the emit fix).
- The `fonts/` dir in `maker/proof/` holds a 0-byte `GreatVibes.ttf` from a failed
  write — delete before reuse; the font measurement was done in memory and does not
  depend on it.
