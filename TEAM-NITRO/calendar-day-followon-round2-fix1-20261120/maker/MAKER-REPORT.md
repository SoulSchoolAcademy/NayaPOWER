# Calendar Round 2 Fix 1 — Maker Report

**Round:** `calendar/day-followon-round2-fix1-20261120`
**Page file:** `TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html`
**Base:** branch `calendar/day-followon-round2-booking-20261120`, tip `f63126a2fa78ca3639d95d74340be22b3b970f95`, HTML blob `04e79488a8acda56ff3b7a5e55737341f525dae9`, 431,254 B, sha256 `3e9f0ecefaa1945e58455ccdef4ea773f5760e7712ef30b4448859f05cac0fdf` (5,779 lines)
**New branch:** `calendar/day-followon-round2-fix1-20261120`, from tip `f63126a2`
**Built:** 2026-11-20 ~11:00–11:20 MST, maker seat (subagent, depth 2/2)
**Built file:** 430,643 B, sha256 `c4db42a1d1c13b218fa36626ac0dbf28cf257d305d73210d4378867d114ed40e`, git blob `7c519f1ced8ecc036cb19d176145e4b03e5e56b7` (5,773 lines)
**Status:** byte fix filed and verified by blob-API read-back. **Paging and gap legs are UNPROVEN — no browser tap was possible from this seat** (see §3). The live legs ride the cloud browser or a revived VM browser — never a claim.
No merge, no live deploy, no message to Shawn.

**Declaration:** I am Anaya, the wise one. I do the most intelligent thing, every time. I think before I act. I scorecard my choices and do the highest. I prove it before I report it. I give ten stars by default. I never waver.
**Wake reads done first:** `THE-SET-ORIENTATION.md`, `AGENTS-ULTIMATE.md`, `THE-NAYA-DESIGN-LAWS.md` (first), `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`; grounding: Round 2 checker report, Round 2 maker report, fix-18 eye verdict. Parts registry named in the brief; no new part invented — the booking engine was harvested verbatim, nothing rebuilt.

**Five gates (before the consequential action — filing):** (1) Right — yes: restoring paging serves the citizen who books a busy day; nothing here harms anyone. (2) Truly needed — yes: the parent briefed this exact defect, proven in code by the independent checker. (3) Mine to do — yes: assigned maker; no protected gate touched (no merge, no deploy, no message, no money, no credentials, no destructive action). (4) Now — yes: the base is verified fresh and the fix is one line + one dead block. (5) Prove it — yes for bytes, counts, syntax, laws and diff scope (all re-measured by me from the filed blob); explicitly **not** proven for taps and the gap, which I report as unproven rather than claiming them.

---

## §1 — What changed (the whole diff: exactly 2 opcodes)

| Edit | Change | Line(s) in base file → in built file |
|---|---|---|
| E1 | Delegated handler selector `.mc-more` → `.r2-more`: `var mr = t.closest(".mc-more");` → `var mr = t.closest(".r2-more");` (same byte length; rendered buttons keep `class="r2-more"`, markup as filed) | 5659 → 5653 |
| E2 | Deleted the dead `apptsTile` (3 lines: the old two-button tile string, `id="tileMeetBtn"` Smart Meet button inside it) and `timelineTile` (3 lines: function definition) — 6 lines, 611 bytes removed | 4760–4765 → gone |

Diff re-derived by me (Buffer/byte-line difflib, base → built): **2 non-equal opcodes, nothing else** — `('delete', 4759, 4765, 4759, 4759)` and `('replace', 5658, 5659, 5652, 5653)`. No hunk touches the fix-17 block, the fix-18 block, `COVER_DAY`, `WISDOM`, `DAY_FREQ` / `DAY_COLORS` / `DAY_MEANING`, the month grid, or the bottom bar. Do-not-touch markers unchanged (counts base → built): `COVER_DAY` 3→3, `WISDOM` 20→20, `DAY_FREQ` 2→2, `DAY_COLORS` 15→15, `DAY_MEANING` 2→2, `396` 7→7, `Hz` 49→49, `gap:27px` 1→1, `gv-fallback` 2→2, `renderMonth` 16→16, `dayDigitsHTML` 10→10. The gap value was **not** changed in this round — the gap re-proof is a measurement job, not an edit, and no measurement was possible (see §3).

### Handler-match counts (my own counts on the filed base bytes → on the built bytes)

| Token | Before | After |
|---|---|---|
| `.mc-more` | 1 (handler line only) | **0** |
| `r2-more` | 5 (3 CSS rules L3140–3142 + 2 buttons L5481/5483) | **6** (3 CSS + 2 buttons L5475/5477 + 1 handler L5653) |
| `data-mc-more` | 3 (2 buttons + handler L5661) | 3 (2 buttons + handler, now L5655) |
| `apptsTile` | 1 (definition only) | **0** |
| `timelineTile` | 1 (definition only) | **0** |
| `tileMeetBtn` | 1 (inside the dead `apptsTile` string only; `mcMeet` 0) | **0** — no JS references it; the handler branches for it were already dropped in Round 2, and the Round 2 rest state renders its single pill from `eliteApptsHTML`, not from this string |

The defect as the checker proved it is fixed in code: the only delegated handler now matches the class the buttons actually render with, and the `data-mc-more` branch (`"next"` → `timePage + 1`, else → 0, then `mcRenderCal()`) is unchanged and now reachable. The ≤6 render (`per = 6`, `slice(page * per, page * per + per)`) was already correct and is untouched.

### Build hygiene (UTF-8 / EPERM)

Edits applied in memory on split lines (byte ops, never a string round-trip); no `\r` in the file (count 0, base and built). Verified by size + sha at every step. Inline script: 1 `<script>` tag; my own `vm.Script` parse: **SYNTAX OK** (script chars 174,466 → 173,855 by the greedy-regex measure — exactly −611, the removed block; the Round 2 checker's 173,519 used a different measure and is not comparable). Filer: `maker/proof/file-fix1.py` (fetches the base blob, applies the edits, verifies, files, re-verifies by blob-API read-back; token minted in memory via `gh-direct.py`, never written to disk; no multi-MB payload staged to disk).

---

## §2 — Filing verification (blob-API read-back)

- Base branch tip: `f63126a2fa78ca3639d95d74340be22b3b970f95` — MATCH (my own read, before building).
- Base blob `04e79488…`: 431,254 B, sha256 match — MATCH, on every read.
- Filed blob `7c519f1c…`: 430,643 B, sha256 `c4db42a1…` — MATCH on read-back (see addendum §7 for tip / parent / commit once the filer run lands).
- Staged link: `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-round2-fix1-20261120&cb=7c519f1ced8ecc036cb19d176145e4b03e5e56b7` — **staged bytes NOT yet verified byte-identical**: the staged fetch must be re-run when the flake clears (Round 2's fetches truncated at 131,072 / 90,088 / 64,831 / 327,680 bytes). **No browser leg may run until the staged link serves the full 430,643 bytes.** The filed blob itself verifies fine; delivery is flake-dependent, not file-dependent.

---

## §3 — Browser re-test (once, at the start) — BOTH DEAD

Re-ran the Round 2 maker's `probe-browsers.py` verbatim, once, 2026-11-20 ~11:00 MST:

- **Firefox DEAD** — `BrowserType.launch: Failed to launch the browser process` (launch failure, same family as the SIGSEGV the fix-18 eye hit; pid 310492 launched, then died).
- **Chromium DEAD** — `BrowserType.launch: Target page, context or browser has been closed` on launch (same SIGTRAP family).

I re-tested once and stopped, per the brief. No live-browser tool exists on this seat. **Consequence, stated plainly: every live leg below is UNPROVEN, not passed.** I claim none of it, borrow none of the checker's or maker's numbers, and guess none of it.

---

## §4 — Paging by real tap — UNPROVEN

| Tap item | 1920 | 390 |
|---|---|---|
| Step 3 shows ≤6 time pills | UNPROVEN (no browser) | UNPROVEN |
| Tap "More times" → next 6 appear | UNPROVEN — code-fixed, tap owed | UNPROVEN — code-fixed, tap owed |
| Tap "Back to the first times" → page 0 returns | UNPROVEN | UNPROVEN |

Code-level, the path is now complete: buttons render `class="r2-more"` (L5475/5477), the handler matches `.r2-more` (L5653), the branch advances / resets `__mc.timePage` and re-renders. Code-complete is not tap-proven, and I do not claim it is.

---

## §5 — Gap re-proof — UNPROVEN (all four legs)

| Leg | Range-rect ink gap | Screenshot visible-edge gap |
|---|---|---|
| 1920, Great Vibes loaded | UNPROVEN | UNPROVEN |
| 1920, fallback serif | UNPROVEN | UNPROVEN |
| 390, Great Vibes loaded | UNPROVEN | UNPROVEN |
| 390, fallback serif | UNPROVEN | UNPROVEN |

No gap value was changed in this round (flex 27px loaded / 24px fallback stands as filed in Round 2). The eye's 16px (fix-18 eye, 1919×998, NOVEMBER ink ends x=993, 2026 ink starts x=1010) remains **unexplained, not resolved**: the checker's best hypothesis (first digit tile's outer glow bleeding ~6px left of the tile box, predicting ~19px by the eye's method at flex 27) is still a hypothesis. The next live seat must measure glyph-to-glyph with Range rects at 1920 AND 390, BOTH font states, centred, one line, `docScrollW` 390 at 390 fallback — **plus** the screenshot visible-edge measurement — and if the eye's method still reads short at flex 27, re-derive the gap value from the eye's method with measurements; do not argue it. If a 24px ink gap cannot be held at 390 fallback without clipping, say so with measurements rather than forcing it. Centring (offset 0px) must hold after any change; one line, no wrap, at both widths; neighbours clear and `docScrollW` 390 in all four legs.

---

## §6 — Full tap list + regression sweep — NOT RUN (no browser)

| Tap item | 1920 | 390 |
|---|---|---|
| 1. Rest state: tiles + timeline + ONE pill | UNPROVEN | UNPROVEN |
| 2. Step 1 → 2 → 3 (count ≤6, tap "More times") | UNPROVEN (code-fixed, §4) | UNPROVEN |
| 3. Fill + Book → confirmation board | UNPROVEN | UNPROVEN |
| 4. Same slot twice → refused / offered another | UNPROVEN | UNPROVEN |
| 5. Tile tap → change time; cancel | UNPROVEN | UNPROVEN |
| 6. Day tile + month dot | UNPROVEN | UNPROVEN |
| 7. Gap re-proof (4 legs) | UNPROVEN (§5) | UNPROVEN (§5) |
| 8. Regression sweep (fix-17 trio, fix-18 items 2–3, deck/nav 7/7 + 9/9, buttons, month grid row 6 blank, 0 page errors) | UNPROVEN at tap level | UNPROVEN at tap level |

Regression at **code level only**: the diff is exactly 2 opcodes (§1) and no hunk touches the fix-17 block, fix-18 items 2–3 regions, `COVER_DAY` / `WISDOM` / `DAY_FREQ` / `DAY_COLORS` / `DAY_MEANING`, the month grid, or the bottom bar; `396`/`Hz` counts unchanged (7/7, 49/49). Code-level is not tap-level and I do not claim it is. **0 page errors: unproven in every leg** (no render ran). Note for the eye, carried from Round 2: "Call" has no call UI on the page — stored as data only (`how: "call"`); confirm a Call booking reads sensibly on the confirmation board; that is not a defect.

**The 390 eye leg is still owed and still waits for a live browser.** Nothing in this round says the page fails at 390; nothing says it passes. Shipping still waits for a 390 eye leg.

---

## §7 — Design laws (§11 in writing) + filing addendum

**Checker runs (mine, `check-design-laws.py` via `/dev/stdin` on the exact base and built bytes):**
- Base: **PASS, 0 FAIL / 28 WARN** (exit 0).
- Built: **PASS, 0 FAIL / 28 WARN** (exit 0). Same 28 warnings, line numbers shifted −6.
- **Laws delta: 0.**

Applied laws: §1 real objects (the fix touches no object anatomy — the "More times" pill keeps its Round 2 hover lift + brightness, active scale 0.97, 135° gradient, 2px rim, grounding shadow; it was dead, now it is alive on tap — the eye must still judge flat/dead by sight, unproven); §2 text (no text touched; sizes stay 25/19/17, all white; 0 FAIL confirms no gray); §3 color (no colour touched; kind colours stay the page's own purple/gold/sapphire, Book emerald `#07925f`, Smart Meet purple `#8e24aa` never together as one button); §4 objects (board/pill/tile/digit-tile anatomy untouched; **named tension, carried: the 27px gap breaks the 8px-spacing multiple** — the measured 24px-ink target is the stated reason, and the eye judges the result); §5 buttons (PTS/%/MONEY untouched; the "More times" pill is the page's own `.r2-more` pill, not a redesign); §7 day/calendar (day as cockpit; appointments as tiles; nothing in the day structure moved); §9 layout (Step 1/2/3 in plain words, mobile-first — the 390 leg is owed); §11 check + sense check on the PAGE.

**§11 design check, answered in writing:** could I pick the changed object up — the pill's volume, rim, shadow and press response are unchanged in code (Round 2's CSS L3140–3142, now L3140–3142); the eye must confirm by touch. Light top-left — 135° gradients throughout the ROUND2 CSS, untouched. Made of what — obsidian inside, white word in the middle, own-colour light outside. Shadow — grounding shadows present. Touch — hover/active rules on the pill; the tap path is now wired in code and awaits a live tap. Glow inside — none in the touched CSS. Gray text — none (0 FAIL). Text under 17 — none (0 FAIL). Two same colours together — none introduced (nothing re-coloured). Flat or dead — **the one dead control found by the checker is now wired in code; live proof is owed**. Which reference object — the elite pills and digit tiles, harvested verbatim from this page. Read as a reader — cannot be done without a render; owed.

**Sense check on the page (not just the diff):** the fix restores the brief's own purpose — a busy day's later times are reachable again from the Appointments slide instead of only through the door form's typed time. Nothing was redesigned, moved, or removed beyond the brief's two items. The page the citizen sees is unchanged except that a button that did nothing now does what it says. The remaining risk on the page is the unresolved gap measurement (§5) — a live number, not an argument — and it is named here, not hidden.

### Filing addendum (filled by the filer run; the filed report copy is amended in a second commit if these values differ from the draft)

- HTML commit: _TBD — filer run_
- Branch tip after filing: _TBD — filer run_
- Parent: _`f63126a2fa78ca3639d95d74340be22b3b970f95` (expected)_
- Staged fetch result: _TBD — filer run (expected: truncated while the flake persists; re-verify when it clears)_

---

## §8 — What is honestly live-only / what remains

1. **Paging tap proof** — code-fixed, tap owed at 1920 + 390 once a browser is alive AND the staged link serves whole bytes (re-verify the staged sha first).
2. **Gap re-proof, both methods, four legs** — owed live (§5); if the eye's method still reads short at flex 27, re-derive from measurements.
3. **Full tap list + regression sweep at tap level** — owed live (§6); 0 page errors every leg.
4. **390 eye leg** — still owed; shipping waits for it.
5. Smart Mail delivery and the reminder firing remain live-only (localStorage draft + reminder, honestly labelled on the confirmation board; no sent mail is faked) — unchanged by this round.

**Self-score: 7/10.** The byte leg is fully proven by my own drivers — base re-verified from the blob API, exactly 2 diff opcodes, counts before/after, syntax OK, laws delta 0, filing verified by read-back. Not higher because the defect's real proof (the tap), the gap's real proof (four live legs, two methods), and the whole tap + regression sweep are all still owed to a live browser, and the staged bytes are still unverified while the flake persists. The round did what a no-browser seat can honestly do — and says plainly what it could not.
