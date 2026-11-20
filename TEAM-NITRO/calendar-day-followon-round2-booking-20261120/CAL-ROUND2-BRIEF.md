# MAKER BRIEF — Calendar Round 2: the gap fix + the ultimate booking

## 0. WAKE — read first

- Read `~/workspace/team-nitro/THE-SET-ORIENTATION.md` (the master orientation, ~1,300 tokens) and `~/workspace/team-nitro/AGENTS-ULTIMATE.md` (the distilled operating manual, ~2,700 tokens). Declare who you are, your oath, and run the five gates before every consequential action.
- Design laws: read `~/workspace/team-nitro/THE-NAYA-DESIGN-LAWS.md` FIRST, then `~/workspace/team-nitro/THE-PLAYBOOK.md`, then `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md`. After the work: the §11 check in writing in your report + run `check-design-laws.py`. If it breaks the laws, redo.
- Laws that apply here: §1 real objects (every booking step is a real object — alive on hover, presses in and out); §2 text (25/19/17, no gray, white); §3 color (spectrum flow, never the same twice; Friday ruby `#c62828`, 396 Hz); §4 objects (board / pill / tile / digit-tile anatomy; depth equation: 145° gradient, 1px border, inset top highlight crescent, grounding shadow, accent glow); §5 buttons (PTS / % / MONEY standard; Book emerald `#07925f`, Smart Meet purple `#8e24aa` — never the same together, already the page's rule); §7 day/calendar (the day is a cockpit; appointments as tiles); §9 layout (Step 1/2/3, blatantly obvious so anybody cold can follow; mobile first, judged at phone width first); §11 check + sense check on the PAGE, not the brief.
- Also named: `THE-ULTIMATE-ORIENTATION.md` · `THE-ANATOMY-OF-A-SMART-APP-PAGE.md` · `THE-ARMY-TRAINING.md` · `THE-OFFICIAL-PARTS.md` (the parts registry — the only places to build from).

## 1. PARTS — harvest, never invent (`~/workspace/team-nitro/THE-OFFICIAL-PARTS.md`)

- **Day covers + Wisdom cover:** calendar fix-17 verified byte-identical (`COVER_DAY` `7e2653d0…`, `WISDOM` `d3783c23…`). Do not touch.
- **Digit tiles:** harvested from the page's own `dayDigitsHTML` — never invent new number tiles. The current booking's time pills already use them; reuse them.
- **The booking ENGINE already in the file is a part** (see §4). Harvest its logic verbatim.
- **Bottom six, byte-identical** — not touched here.
- If a part you need is not in the registry, **STOP and say so** — don't invent one.

## 2. PAGE FACTS — the file

- **Base:** branch `calendar/day-followon-fix18-20261120`, tip `ffd220c7d7d54fbbfc08c82ceed793ce1b0968a3`. HTML blob `f7b14ce75d590738a9efb87a4fa056ee98f3561d`, 413,386 B, sha256 `52ff950fb4dfeb942415c96ee2af393b815e06e9019c77a9758121a9f40770cc`. Parent: fix-17 tip `a955d7fa` (blob `f4c05109`, eye PASS, lane closed).
- **New branch:** `calendar/day-followon-round2-booking-20261120`, from tip `ffd220c7`.
- **Page file:** `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html`.
- **Staged pattern:** `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-round2-booking-20261120&cb=<new blob>`.
- **UTF-8 trap:** string round-trip edits can silently drop bytes on this file — use Buffer ops. Verify every write by size + sha. Never `python3 … > file` (exits 120 silently). Never move a temp over the live file unchecked.
- **VM browsers flap** — re-test at the start. Chromium via the localhost forwarder `~/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py` (`ignore_https_errors=True`); kill it by PID when done. Slide transitions take >900ms to settle — use 2s waits after deck navigation. A day re-opens on the last-viewed slide — force the slide via the dots after every `openDay`.
- **Round dir:** `~/workspace/team-nitro/calendar-day-followon-round2-booking-20261120/` (brief/ + maker/ + checker/). File your report at `maker/MAKER-REPORT.md` with proof alongside.

## 3. ITEM 1 — THE GAP FIX (file first in the diff)

- The eye's verdict (`~/workspace/team-nitro/calendar-day-followon-fix18-20261120/eye/EYE-VERDICT.md` — READ IT): "NOVEMBER 2026" centred (offset −2px), one line, but the **glyph-to-glyph gap measures 16px, twice, 8px short of the 24px target**.
- **Root cause:** fix-18 set `.hl-center .hl-monthline{display:inline-flex;gap:24px}` (`maker/proof/fix18-block.css` in the fix-18 round dir). That 24px is the gap between the two flex ITEM boxes. The script "November" glyph's ink ends ~8px before its box edge (Great Vibes trailing bearing), so the INK gap is 16px. The fix-18 maker and checker both measured element boxes (24px) — the wrong method. The eye measured glyph ink edges: NOVEMBER ink ends x=993, 2026 ink starts x=1010 at 1919, measured twice.
- **The measurement, clarified (eye report §1, §8):** the checker's "24px" is the CSS flex gap between span boxes; the eye's 16px is visible ink-to-tile. The fix must make the **GLYPH-TO-GLYPH gap a true 24px — last glyph ink → first digit tile** — at 1920 AND 390, re-proven the same way. **Do not accept a flex-gap number as proof.**
- **Your fix:** measure glyph-to-glyph with Range rects on the text nodes (the eye's method), in BOTH font states (Great Vibes loaded + Firefox fallback serif) at 1920 AND 390, and set the flex gap so the **INK gap is exactly 24px** at both widths, both font states. Do NOT assume 32px — measure; the shortfall may differ per font state. Re-prove 24px the same way after the fix.
- **Watch:** at 390 fallback the monthline is already 280px wide in a 240px column (overflows 20px/side into clear black field, `docScrollW` stays 390). Widening the gap adds width — verify neighbours stay clear and `docScrollW` stays 390 in all four legs. If a 24px ink gap cannot be held at 390 fallback without clipping, say so with measurements rather than forcing it.
- Keep centred (offset 0px) after the change. One line, no wrap, at both widths.

## 4. ITEM 2 — THE ULTIMATE BOOKING (start on this NOW; the big item)

- **Shawn's order (08:14 MST, his words):** the current booking is "complete mess, not useful at all". At rest the Appointments slide shows two bare buttons + "Nothing booked for this day yet." Clicking "Book a time" opens a wall of time pills — up to 60 digit-tile pills at once (every 15 min, 6 AM–9 PM). That wall is the overload he pointed at. **The PRESENTATION goes.**
- **What stays — the ENGINE, harvested verbatim (it is a part, not a presentation):** the free-time computation in the file (`mcFreeTimes`: 6 AM–9 PM, 15-min steps, 30-min buffer after every booking, no booking inside the next hour), the no-double-booking guard, edit (tap a tile to change its time) + Cancel (`mcCancelIdx`), localStorage persistence (`LS_KEYS.appts`, `saveStores`), `dayDigitsHTML` time pills, the 7-day strip with weekday colours and dimmed days (`mcRenderCal`), the Smart Meet toggle + join flow (`openMeetRoom`, `data-join`). Do NOT rebuild this logic from scratch — that is the waste he named. If you judge the logic itself is the problem, say so in your report with evidence rather than silently keeping it or silently replacing it.
- **What goes — the PRESENTATION:** the two bare buttons at rest; the wall of time pills; the short form as it stands. Rebuild it as the ultimate booking app INSIDE the Appointments slide (slide index 5), not a separate page:
  - **Step 1 — pick the kind of time.** The kinds come from the page's own vocabulary: Smart Meet / in person / call. If the kinds aren't clear from the page, name the gap in your report rather than inventing categories.
  - **Step 2 — pick the day.** The 7-day strip, harvested from `mcRenderCal`: days in their weekday colours, a day with no free time dimmed.
  - **Step 3 — pick a real open time.** A FEW open times at a time, never a wall — the next few open times as digit-tile pills, with a "more times" step to see the rest. This is the overload fix; prove it by count (how many pills on screen at once).
  - **Then — how to meet:** Smart Meet / in person / call (pill choice, one lit).
  - **Then — name or alias + one line** ("What is it?" + "Who is it with?" — harvested from the current form).
  - **Then — ONE Book button** (emerald `#07925f`, the page's own rule: Book emerald, Smart Meet purple, never the same together).
  - **Then — confirmation:** a board that says what is booked, when, with whom, how — plus Smart Mail + reminder. Prove what can be proven on staged (confirmation board renders with the right details; reminder set in local state); name HONESTLY what needs live (actual mail delivery — do not fake a sent mail).
  - **One-tap change** (tap the booked tile to change its time) **and one-tap cancel. No double-booking:** prove by booking the same slot twice — the second must be refused or offered another time.
  - **Both calendars:** the booking must show on the DAY (as a tile) AND on the MONTH (count/marker) — prove both. Name honestly what "theirs" (the other person's calendar) needs live.
  - **The slide at rest must PRESENT booking as a real thing** — the day's timeline + what's on + the booking doorway, aligned, elegant, real-object feel (laws §1, §4, §7). Not two bare buttons on blank space (laws §12.16: buttons on blank space).
- **Acceptance:** a stranger cold can book in three steps; every step proven by real tap at 1920 and 390; confirmation lands + Smart Mail composed + reminder set; change/cancel in one tap; no double-booking; the slide at rest reads as a real booking app.

## 5. REGRESSION — must hold, re-proven by your own taps

- Fix-17: wisdom Change cover hidden at 390; Smart Meet pill whole and hit-testable at 390 all 7 days; "Your Journal" door whole and tappable at 390 all 7 days.
- Fix-18 items 2 and 3: no Hz in header (wisdom line keeps both 396 Hz mentions); Change cover only on Wisdom + Worlds.
- Deck/nav sweep 7/7 + 9/9; buttons (Keep-reading advances day, prev-day returns it, BACK TO MONTH → 42 cells / 30 numbered); month grid row 6 blank; 0 page errors in every leg.
- Laws delta 0 (run `check-design-laws.py`; §11 in writing in your report).

## 6. SEQUENCING

- **UPDATE (captain, 2026-11-20 ~09:43 MST): the fix-18 eye record is filed — combined verdict GOES BACK (item 1 only).** Eye record on branch `calendar/day-followon-fix18-20261120`, tip `1ab1c70e395c01fc7454c1f69648cd3bb70acbdf`, tree `683eab9e…`, parent `70a142cb`; 4 files, 19,730 B, 4/4 verified by fresh blob-API read-back; HTML blob `f7b14ce7` untouched. Full report: `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/eye/EYE-REPORT.md` (§2 = the 390 leg, §8 = what the next round must do). The eye also verified independently: filing identity (maker proof sha = filed blob; base sha = fix-17 blob), laws delta 0 (0 FAIL / 28 WARN both sides, own run), 0 page errors in the desktop leg.
- **THE 390 VERDICT DOES NOT EXIST — do not wait for it.** The eye's phone-390 leg is **BLOCKED on environment, not on the page**: Firefox SIGSEGV on launch, Chromium closed on launch, the localhost forwarder dead, staged fetches landing 0 bytes in the same EPERM flake window. The eye re-tested once per instruction and stopped; it did NOT claim the checker's 390 leg. Nothing in the probe says the page fails at 390; nothing says it passes. The earlier instruction in this brief ("do not file until the 390 verdict is read") is **superseded** — there is no 390 verdict to read.
- **New sequencing:** fix the gap at BOTH widths and prove it glyph-to-glyph at both widths with your OWN drivers (Range rects, both font states, 1920 and 390), exactly as §3 requires. If the VM browsers are dead when you build, re-test once, then say so honestly in your report and name what is unproven — do not claim the checker's 390 leg, do not guess, do not borrow. Filing to the checker proceeds on your own two-width proof; **shipping still waits for a 390 eye leg** (the eye re-proves 390 in full once a browser is alive, or via a cloud-browser 390 leg).
- File: branch `calendar/day-followon-round2-booking-20261120`, commit the HTML + brief + maker report. Verify by fresh blob-API read-back (tip, parent, blob, size, sha256, staged link serves the filed blob byte-identical).

## 7. DO-NOT-TOUCH

The fix-17 block; the fix-18 block except the gap value; `COVER_DAY`; `WISDOM`; `DAY_FREQ` / `DAY_COLORS` / `DAY_MEANING`; the month grid; the bottom bar. Do not redesign the page. Do not move what he didn't ask to move. Do not remove what he didn't ask to remove.

## 8. REPORT BACK — `maker/MAKER-REPORT.md`

What you changed (diff, line numbers); the gap measurement per leg per font state, glyph-to-glyph, before and after; the booking proven step by step with real taps at both widths; what is honestly live-only; regression results; laws delta; §11 in writing; self-score. If anything is ambiguous, STOP and report — do not guess.
