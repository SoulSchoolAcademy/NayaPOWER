# MAKER BRIEF — Calendar Round 2 Fix 1: the dead "More times" button + live re-proof

## 0. WAKE — read first

- Read `~/workspace/team-nitro/THE-SET-ORIENTATION.md` (the master orientation, ~1,300 tokens) and `~/workspace/team-nitro/AGENTS-ULTIMATE.md` (the distilled operating manual, ~2,700 tokens). Declare who you are, your oath, and run the five gates before every consequential action.
- Design laws: read `~/workspace/team-nitro/THE-NAYA-DESIGN-LAWS.md` FIRST, then `~/workspace/team-nitro/THE-PLAYBOOK.md`, then `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md`. After the work: the §11 check in writing in your report + run `~/workspace/team-nitro/check-design-laws.py`. If it breaks the laws, redo.
- Laws that apply here: §1 real objects (every booking step is a real object — alive on hover, presses in and out); §2 text (25/19/17, no gray, white); §3 color (spectrum flow, never the same twice); §4 objects (board / pill / tile / digit-tile anatomy — harvest, never invent); §5 buttons (PTS / % / MONEY standard; Book emerald `#07925f`, Smart Meet purple `#8e24aa` — never the same together, already the page's rule); §7 day/calendar (the day is a cockpit; appointments as tiles); §9 layout (Step 1/2/3, blatantly obvious so anybody cold can follow; mobile first, judged at phone width first); §11 check + sense check on the PAGE, not the brief.
- Also named: `THE-ULTIMATE-ORIENTATION.md` · `THE-ANATOMY-OF-A-SMART-APP-PAGE.md` · `THE-ARMY-TRAINING.md` · `THE-OFFICIAL-PARTS.md` (the parts registry — the only places to build from).

## 1. PARTS — harvest, never invent (`~/workspace/team-nitro/THE-OFFICIAL-PARTS.md`)

- The booking ENGINE already in the file is a part. Harvest its logic verbatim — do not rebuild it.
- Digit tiles: harvested from the page's own `dayDigitsHTML` — never invent new number tiles.
- Bottom six, byte-identical — not touched here.
- If a part you need is not in the registry, **STOP and say so** — don't invent one.

## 2. PAGE FACTS — the file

- **Base:** branch `calendar/day-followon-round2-booking-20261120`, tip `f63126a2fa78ca3639d95d74340be22b3b970f95` (verified by the coordinator from `git ls-remote` just now — MATCH). HTML commit `dc9d9f2a15599aa0f639ef0f21e22f31cbca5b66`, parent `ffd220c7` (fix-18 tip). Filed blob `04e79488a8acda56ff3b7a5e55737341f525dae9`, **431,254 B, sha256 `3e9f0ecefaa1945e58455ccdef4ea773f5760e7712ef30b4448859f05cac0fdf`**.
- **New branch:** `calendar/day-followon-round2-fix1-20261120`, from tip `f63126a2`.
- **Page file:** `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html`.
- **Staged pattern:** `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-round2-fix1-20261120&cb=<new blob>`.
- **Filing path:** `~/workspace/team-nitro/gh-direct.py` (METHOD + PATH separate, PATH starts `/`). Contents API returns EMPTY content for files over 1 MB — use the git blob API for read-back. Never stage a multi-MB base64 payload to disk — pipe base64 → jq via bash process substitution. The helper's `--file` mode omits the `branch` field — never use it for branch filings.
- **UTF-8 trap:** string round-trip edits can silently drop bytes on this file — use Buffer ops. Verify every write by size + sha. Never `python3 … > file` (exits 120 silently). Never move a temp over the live file unchecked.
- **EPERM flake is active in this window:** python/shell/node writes fail or land 0 bytes, staged fetches truncate. Verify every write by size + sha; if a write EPERMs, retry when the window opens or use the file tool — never claim a write that did not verify.
- **VM browsers flap** — re-test at the start, once, and report the result. Chromium via the localhost forwarder `~/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py` (`ignore_https_errors=True`); kill it by PID when done. Slide transitions take >900ms to settle — use 2s waits after deck navigation. A day re-opens on the last-viewed slide — force the slide via the dots after every `openDay`.
- **Round dir:** `~/workspace/team-nitro/calendar-day-followon-round2-fix1-20261120/` (brief/ + maker/ + checker/). File your report at `maker/MAKER-REPORT.md` with proof alongside.
- **Grounding reads (do these first):** the Round 2 checker report `~/workspace/team-nitro/calendar-day-followon-round2-booking-20261120/checker/CHECKER-REPORT.md` (20,610 B — the defect, § verdict + §7, and the gap analysis §2), the Round 2 maker report in the same round dir, and the fix-18 eye verdict `~/workspace/team-nitro/calendar-day-followon-fix18-20261120/eye/EYE-VERDICT.md`.

## 3. THE DEFECT — one proven defect, one line (file first in the diff)

The Round 2 independent checker proved this in code (checker report § verdict, ground 1 — re-verify it yourself on the filed bytes before you touch anything):

- The "More times" / "Back to the first times" buttons render as `class="r2-more"` (filed lines 5481, 5483), but the only delegated handler looks for `t.closest(".mc-more")` (line 5659). `.mc-more` occurs exactly **once** in the whole 431,254-byte file — in that handler line. `".r2-more"` occurs **zero** times in JS. `data-mc-more` occurs only in the two buttons + handler line 5661. No other listener references these buttons.
- Tapping "More times" does nothing; times beyond the first 6 are unreachable from the Appointments slide. This breaks the brief's core overload fix and Round 2's own acceptance ("tap it, next 6 appear").
- **The fix:** the handler must match `.r2-more` (one line — prefer changing the handler's selector, not renaming the buttons, so the rendered markup stays as filed). Also remove the dead `apptsTile` (filed L4760–4762, definition-only, occurs exactly once — never referenced, so the old two-button tile cannot render) and `timelineTile` (L4763, likewise definition-only) variables the checker named in §3.
- **Everything else in the booking flow is wired correctly in code** (kind pills, time pills, Book, Change, Done, Join direct listener, both double-booking guards — checker §4). **Do not touch what works.** Do not redesign, do not move, do not remove anything else.

## 4. WHAT YOU MUST PROVE (before filing)

### 4a. Paging by real tap — the defect's proof
- Step 3 shows ≤6 time pills. Tap "More times" → the next 6 appear. Tap "Back to the first times" → page 0 returns. At **1920 AND 390**, by real tap, with counts.
- **If the VM browsers are still dead when you build** (Firefox SIGSEGV exit 139, Chromium SIGTRAP, memfd MAP_SHARED EPERM — re-test once at the start, never assume): file the byte fix with the tap leg marked **UNPROVEN** in your report, plainly. The live leg rides the cloud browser or a revived VM browser — never a claim. Do not borrow the checker's tap leg. Do not guess.

### 4b. Gap re-proof — live only, both methods
- The gap fix (flex gap 27px Great Vibes-loaded / 24px fallback) must measure a **TRUE 24px glyph-to-glyph — last glyph ink → first digit tile** — at **1920 AND 390, both font states** (Great Vibes loaded + fallback serif), centred, one line, `docScrollW` 390 at 390 fallback.
- Measure with **BOTH** methods and report both numbers per leg: (1) Range-rect ink gap (the eye's method, fix-18 eye: NOVEMBER ink ends x=993, 2026 ink starts x=1010 at 1919, measured twice = 16px); (2) screenshot visible-edge gap (the first digit tile's outer glow included — the checker's best unproven hypothesis for the eye's 16px: at flex 27 the eye's method may read ~19px, still short of 24; font metrics predict ~24.7px ink-to-tile-box at flex 27).
- **Font math alone never proves the gap.** If the eye's method still reads short at flex 27, re-derive the gap value from the eye's method with measurements — do not argue it. If a 24px ink gap cannot be held at 390 fallback without clipping, say so with measurements rather than forcing it. Keep centred (offset 0px) after any change. One line, no wrap, at both widths.
- **Watch:** at 390 fallback the monthline is already 280px wide in a 240px column (overflows 20px/side into clear black field, `docScrollW` stays 390). Widening the gap adds width — verify neighbours stay clear and `docScrollW` stays 390 in all four legs.

### 4c. Full tap list + regression sweep
Once a browser is alive **AND** the staged link serves whole bytes — re-verify the staged sha first (Round 2's staged fetches truncated at 131,072 / 90,088 / 64,831 / 327,680 bytes, never the full 431,254; delivery is flake-dependent, not file-dependent):
- Booking tap list (Round 2 checker §5): rest state tiles + timeline + ONE pill; Step 1 → 2 → 3 (count ≤6, tap "More times"); fill + Book → confirmation board; same slot twice → refused / offered another; tile tap → change time; cancel; day tile + month dot; gap re-proof (4 legs).
- Regression (Round 2 brief §5): fix-17 trio (wisdom Change cover hidden at 390; Smart Meet pill whole and hit-testable at 390 all 7 days; "Your Journal" door whole and tappable at 390 all 7 days); fix-18 items 2+3 (no Hz in header, wisdom line keeps both 396 Hz mentions; Change cover only on Wisdom + Worlds); deck/nav sweep 7/7 + 9/9; buttons (Keep-reading advances day, prev-day returns it, BACK TO MONTH → 42 cells / 30 numbered); month grid row 6 blank; **0 page errors in every leg**.
- Note for the eye: "Call" has no call UI on the page — stored as data only. Confirm a Call booking reads sensibly on the confirmation board; that is not a defect, but the eye judges the read.

### 4d. Laws + §11
- Laws delta 0 (run `check-design-laws.py` on base and filed bytes; §11 in writing in your report). Named tension, carried from Round 2: the 27px gap breaks the 8px-spacing multiple (laws §4) — the measured 24px-ink target is the stated reason; the eye judges the result. Do not hide it.

## 5. SEQUENCING

- **The 390 eye leg is still owed and still waits for a live browser.** Nothing in the probe says the page fails at 390; nothing says it passes. Do not claim the checker's 390 leg, do not guess, do not borrow. Filing to the checker proceeds on your own two-width proof where a browser is alive; **shipping still waits for a 390 eye leg**.
- File: branch `calendar/day-followon-round2-fix1-20261120`, commit the HTML + brief + maker report. Verify by fresh blob-API read-back (tip, parent, blob, size, sha256, staged link serves the filed blob byte-identical — re-verify the staged bytes when the flake clears).
- One hour max for the build round (Live Sequence law). If the round passes an hour with no version, stage what exists and report.

## 6. DO-NOT-TOUCH

The fix-17 block; the fix-18 block except the gap value; `COVER_DAY`; `WISDOM`; `DAY_FREQ` / `DAY_COLORS` / `DAY_MEANING`; the month grid; the bottom bar; the whole booking flow except the one handler line (L5659) and the two dead variables (L4760–4763). Do not redesign the page. Do not move what he didn't ask to move. Do not remove what he didn't ask to remove. The user sees the PAGE, not the diff — the sense check runs on the page.

## 7. REPORT BACK — `maker/MAKER-REPORT.md`

What you changed (diff, line numbers); the handler match proven in code (counts: `.mc-more` / `.r2-more` / `data-mc-more` before and after); paging proven by real tap at both widths (counts per page) or marked UNPROVEN with the browser re-test result; the gap measurement per leg per font state per method (Range-rect ink + screenshot visible-edge), before and after; tap list + regression results; what is honestly live-only; laws delta; §11 in writing; self-score. If anything is ambiguous, STOP and report — do not guess.
