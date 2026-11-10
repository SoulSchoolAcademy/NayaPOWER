# Dashboard Pass-6-on-Pass-7 — Rebase Record (2026-11-10)

**Branch:** `dashboard/pass6-on-pass7-20261110` (new, from main `7b54c435`)
**File:** `DASHBOARD/defectfix-v7/pass6on7/dashboard-pass6on7.html`
**Size:** 1,785,787 B (= pass-7 1,781,461 + pass-6 delta 4,326, exactly)
**sha256:** `193087b4119467ef8ee89762549e579355dd56c042596be3445f95cf3fa2a203`
**Status:** REBASED + SELF-SCORED — 0 merge conflicts, all eight changes
measured live (Playwright Firefox, 360/390/1440). No merge. No deploy live.
Shawn's eye is the final gate.

## The job

Pass-7 deployed live; land the pass-6 changes ON TOP of pass-7 without losing
any of pass-7's work. Three-way merge, pass-5 as base.

## File identity (my own fetches, never relayed numbers)

| File | Blob (full SHA) | Bytes | sha256 | Verified |
|---|---|---|---|---|
| Pass-5 base | `4b4084e1aad4e3fbd64d1052abc2f48cdc56ac23` | 1,778,959 | `0e4ef2fe…b4a388` | byte-identical to local pass-5 |
| Pass-6 file | `9fb49a377de6e0f00c2e550bdf7859477b12d551` | 1,783,285 | `034f9f81…a367e` | byte-identical to local pass-6 |
| Pass-7 file (LIVE) | `9227167d2e20b29ebbfb8299e5a5864e24ef854d` | 1,781,461 | `7613bc46…f013` | byte-identical to local pass-7 |

All three fetched via the git-blobs API with the FULL SHA before any work.

## The merge — clean, zero conflicts

`git merge-file -p --diff3` (pass-7 file, pass-5 base, pass-6 file):
exit 0, **zero conflict markers**.

- pass-5 → pass-6 diff (my own): **14 hunks, 52 added / 28 removed**
  (verifier counted 53/29 — same 14 hunks; the ±1 is counting method).
- pass-5 → pass-7 diff (my own): **9 hunks, 73 added / 21 removed = 94 lines**
  (matches both pass-7 records).
- pass-7 → merged diff: **exactly the 14 pass-6 hunks** — the sorted `+/-`
  lines are IDENTICAL to the pass-5 → pass-6 diff.
- pass-6 → merged diff: **exactly the 9 pass-7 hunks** — the sorted `+/-`
  lines are IDENTICAL to the pass-5 → pass-7 diff.
- pass-5 → merged: **23 hunks = 14 + 9.** No hunk overlaps: the nearest
  pair (pass-6 note move @4983, pass-7 notif insert @4920) is 60+ lines
  apart; all other pairs are 25+ lines apart.
- Marker counts in the merged file are exactly the intersection:
  `PASS-6 2026-11-10` 12×, `PASS-7 2026-11-10` 4×, `nayanet.app/joinus` 3×,
  `Quiet — nothing measured yet` 0×, `Show on gauge` 7× (drill rows only,
  as in pass-7), `os-wb-feat` 1× (pass-7's removal comment), `os-link-row`
  30× (pass-7's count). No pass-6 change dropped, no pass-7 change lost.

## Pass-6 changes — all four present and working (my own probes)

Synthetic spine score 1,120 / clicks 1,100 (Shawn's live values) via the
page's own `_osRenderLinks` + `renderBoards`. Probes: `p67_probe.py`
(3 widths × 3 modes × link-holder + page-holder), `p67_probe2.py`
(money-first A/B, fit A/B, hover, page-holder fresh per mode),
`p67_probe3.py` (hover time-series, scrolled-120), `p67_probe4.py`
(bar/note geometry across scroll), `p67_probe5/6.py` (drill D1, board tap).

### 1. Orb numbers bigger, same font

| Width | Pass-5 tile digit | Merged tile digit | Pass-5 plain | Merged plain | Font |
|---|---|---|---|---|---|
| 1440 | 13px | **24px** | 28px | **52px** | Inter 700, identical |
| 390 | 10px | **18px** | 28px | **40px** | Inter 700, identical |
| 360 | 10px | **18px** | 28px | **40px** | Inter 700, identical |

All 9 orbs, all modes, all scenarios. Orb values identical to pass-5
(1293/200/280/50/100/0/0/0/5). Viewed by eye: the top orb reads
`1 2 9 3 CLICKS COUNT` in large tiles; % orbs read `44%` `31%` `8%`
`16%` `1%` at a glance at 390 and 1440.
**Honest visual note:** the tile CSS px is pass-6's, but the hero fit
scale in the merged file is smaller than in either parent (390: 0.66 vs
pass-6 0.859 / pass-7 0.751; 1440: 0.437 vs 0.504 / 0.454), so the
VISUAL digit is ~11.9px @390 (pass-5 9.1px, pass-6 15.5px) and ~10.5px
@1440 (pass-5 6.8px, pass-6 12.1px). Still clearly bigger than pass-5
and readable at a glance — but smaller than pass-6 alone. Cause: pass-7's
top notif row + pass-6's reserved note slot both eat hero room; fitHero
shrinks the hero for both. Same next-round fix family as the note tuck
(fitHero subtracts the bar height). Orb diameters: 63.4px @390 (pass-6
82.4, pass-7 48.1), 59px @1440 (pass-6 68.1, pass-7 61.3).

### 2. `#os-pts-note` — 0px off the gauge, % sticks

- Overlap vs dial SVG: **0px² in all 18 link-holder runs + 9 page-holder
  runs** (PTS / % / MONEY, 360 / 390 / 1440). Note is 15px,
  `rgba(255,255,255,0.88)`, in-flow above the toggle.
- % orbs at 3s AND 9s: notes **44%**, invs **8%**, posts **16%**, saves
  **1%**, shares/comments/likes **0%**, joins **31%** (page-holder) —
  percentages stick (the clobber fix survives). Money orbs stay counts.
- Gauge: **224%** in % mode at 3s and 9s, both holders, all widths.

### 3. Ambassador sample — the real link

Fresh sb-api fetch (2026-11-10 ~06:24Z): 14 active links;
rows[0] = name **`joinus`**, target **`https://nayanet.app/welcome`**,
id `5011fe87-7d29-4208-8d86-a6bc98d508f3`,
created `2026-10-23T15:57:23.116941+00:00`. Board renders exactly that:
text `nayanet.app/joinus ↗`, href `https://nayanet.app/joinus`, 17px,
white. Real browser click (popup) at 360/390/1440 → **`https://nayanet.app/welcome`,
"The Official Welcome | NayaNET"**. `curl https://nayanet.app/joinus` → 200
at the welcome page. Full live data: `smartlinks-live-p67.json`.

### 4. Quiet gone, live number in every mode

- `Quiet — nothing measured yet`: **0× in the file, 0× on any rendered
  page** (every mode/width/scenario).
- Gauge numeral, fresh loads, link-holder: PTS **`1 120`**, % **`224%`**,
  MONEY **`$1 120`** (lands ~6–9s; sweep is pre-existing).
- Gauge numeral, fresh loads, page-holder (saved Business holder —
  Shawn's persisted state): PTS **`1 120`**, % **`224%`**, MONEY
  **`$1 120`** at 3s AND 9s, 390 + 1440. **This is the key rebase
  interaction, and it is BETTER than pass-7 alone:** pass-7's verifier
  proved a saved Business holder shows the quiet face in pass-7; the
  merged file shows live numbers there, because pass-6's `readSpine`
  world-spine fallback survives onto pass-7's saved-holder path.
  Marker reads `★ FEATURED — BUSINESS`, name `Business`.
- Zero console errors, zero horizontal overflow, all runs.

## Pass-7 changes — all four intact (my own probes)

### 1. Exactly one button per board

1 each on all 4 boards at 360/390/1440: `<a class="ph-connect os-wb-btn"
href="…">Open the stats</a>`. Sizes: **288×52** @360, **318×52** @390,
**187.3×52** @1440. `linkRows: 0`, `featTag: false` everywhere; no
disabled "On the gauge ✓" on any board. Hrefs: Dashboard
`https://nayanet.app/dashboard`, Personal `…/personal`, Business
`…/business`, Space `…/space`. Personal tap-proven end-to-end (clean
page, real mouse click) → **`https://nayanet.app/personal`,
"Shawn Vibert"**. (Pass-7's verifier tap-proved all four on the
byte-identical code; I re-proved one on the merged file. One earlier
tap attempt failed on a drill-open page state — retried clean, it
landed; the failure was my probe state, not the button.)

### 2. Black obsidian, board-colour hover, no gold, no inset

- Rest: obsidian gradient `linear-gradient(rgb(27,27,36), rgb(5,6,7))`,
  border = board `--ac` (Dashboard magenta `rgb(255,79,216)`, Personal
  purple `rgb(160,107,255)`, Business blue `rgb(58,91,255)`, Space cyan
  `rgb(63,184,255)`), outer glow only (`0 0 18px -4px` in board colour),
  **no inset**, **no gold** in any rest/hover value.
- Hover (time-series, `:hover` matched): full hover = border + glow
  `0 0 26px -2px` in board colour, lift −2px, brightness 1.12, no inset,
  no gold. At 390 full hover by 500ms; at 1440 rest at 500ms → full hover
  by 1000ms (the slow transition the pass-7 verifier documented —
  do not judge a 1440 hover from a sub-second sample).

### 3. Zero gray text; Reports white

Computed-color sweep over all world boards + Reports board: **0
grayish/dim-white hits** (74 entries @390, 70 @1440, 74 @360). Reports
lines `rgb(255,255,255)`, 16px, weight 700, both lines, all widths.

### 4. Notifications top-right, opens the Running feed

First child of `#os-dash` at all widths. Scroll-0 rect: 390 → x165 y188
w209 h54, rightGap 16; 360 → x135 y188, rightGap 16; 1440 → x1207 y116,
rightGap 24. Click (real mouse) → `feedOpen: true`, Running feed board
visible ("Running feed / Everything going on, newest first. …
No updates yet — your first action lights the feed."), Escape closes —
at all three widths.

## No regressions

| Check | Result |
|---|---|
| Minis | **30/30 identical to pass-7** (the live file). 27/30 identical to pass-5; the first 3 differ (`1100/0/0.0%` → `1120/280/200`) — those are the featured-panel stats under pass-7's intended featured-default-to-world change, already live since pass-7. 30/30 tiled. |
| D1 gold buttons | PASS with pass-7's carve-out — board buttons: no gold anywhere. Drill rows keep gold "Show on gauge" (5 buttons, border `rgb(217,165,33)`, gold glow) — out of scope per pass-7, confirmed present, unchanged. |
| D2 minis with numbers | PASS — 30/30 tiled, live numbers. |
| D3 What Naya Does absent | PASS — 0 rendered occurrences. |
| D4-R1 scroll rest | PASS — rest == maxScroll, stable 5s: 390: 7330 = 7330; 360: 7427 = 7427; 1440: 4100 = 4100. |
| Hero gauge / payout / D4-R1 rule | PASS — payout line, D4-R1 rule, "page tracking connects soon" lines untouched (diff-proven). |
| Purple FEATURED marker | PASS — untouched; forced Business holder reads `★ FEATURED — BUSINESS`. |

## What the rebase does NOT do (honest warts — owed to the next round, NOT fixed here)

1. **390 scroll-0 note tuck — real, and worse than pass-6 at 390.**
   In %/money modes at 390 scroll-0 the note sits y769–799 against the
   fixed bar top 776: only the top ~7px of the first line shows, the
   second line is behind the bar (hit-test at note center returns a bar
   button). In pass-6 the 390 % note was fully visible. Cause: pass-7's
   top notif row pushes the hero down ~32px at 390, on top of pass-6's
   reserved note slot. At 1440 the note is entirely behind the bar at
   scroll-0 — exactly as the pass-6 verifier documented. **A 60px scroll
   clears everything at both widths** (the bar slides away; note and
   toggle fully visible, hit-test = the element itself). The named fix
   (fitHero subtracts the fixed-bar height) is already owed; this rebase
   was ordered not to fix it.
2. **390 scroll-0 toggle depth** — the toggle is fully behind the bar at
   390 scroll-0 (y799–833 vs bar top 776), same as pass-6 (v6 confirmed
   0px visible there too — no regression). Fully visible and clickable
   on scroll (proven: money click from scrolled position → `$1 120` live).
3. **Hero fit scale smaller than either parent** (see §1 above) — same
   next-round fix family.
4. **Sandbox stale-ledger dash, ~30–40s after load** — pre-existing
   identically in pass-5, pass-6 and pass-7 (v6 observation #1): late
   screenshots show the top tiles `— — —` + "Ledger loading — your score
   appears when the ledger answers", and a mode click after the timer
   paints the gauge "Ledger unavailable — score withheld…". A/B proves
   it is NOT a merge regression: money-first on a fresh load is live in
   merged, pass-6 and pass-7 identically ($654→$1 120 merged 390,
   $650→$1 100 pass-6 390, $660→$1 120 pass-7 390). On the live Hub the
   ledger answers, so it does not fire.
5. **Pass-7 known edges inherited unchanged:** Dashboard board button is
   a self-link (harvested destination); phone pill at y188, not the top
   edge; settings panel transiently covers the pill while open (same code
   as pass-7, not re-measured here); sequence-gold at link counts ≡ 2
   mod 8 (source, not triggered at 5 synth links); drill rows keep gold
   gauge buttons (D1 carve-out); "Open the Reports room →" is a line,
   not a control.

## Self-scorecard (maker first — the three-step verification, step 1)

**Why it is not a 10:** the 390 scroll-0 note tuck is worse than pass-6's
(the first-viewport wart grew in the merge, even though the fix is owed
elsewhere); the hero fit scale shrank below both parents, so the orb
numbers read smaller than pass-6 alone; the gauge sweep still takes
~6–9s to land; the sandbox stale-dash still appears in late screenshots;
one probe run's board tap failed on drill-open state before the clean
retry landed (my probe, not the page, but it cost a round).

**10 things I love:** (1) zero-conflict merge — the diffs compose exactly,
14 + 9 = 23 hunks, byte-exact on both sides; (2) the pass-6 fallback
FIXES pass-7's saved-Business quiet face — the rebase is strictly better
than pass-7 alone there; (3) money-first A/B identical across merged /
pass-6 / pass-7; (4) the sample link click-proven to the real welcome
page at all three widths; (5) % sticks — 44%/8%/16% at 3s and 9s;
(6) hover proven by time-series with `:hover` matching, including the
1440 slow-convergence trap; (7) zero console errors and zero overflow in
every run; (8) minis 30/30 identical to the live file; (9) the note is
0px off the gauge face in every mode and width; (10) the merge was
verified by content, not by count — sorted `+/-` lines identical on
both sides.

**10 things I don't love:** (1) 390 scroll-0 note tuck, worse than pass-6;
(2) fit scale 0.66 @390 / 0.437 @1440 — below both parents; (3) 6–9s
gauge sweep; (4) late sandbox stale-dash in screenshots; (5) top tiles
dash late in the sandbox (ledger-driven, not the gauge); (6) the toggle
invisible at scroll-0 at both widths; (7) orb labels are 9px × fit scale
(~6px visual @390) — near-illegible, pre-existing; (8) desktop orbs
59px in the merged file vs 68.1px in pass-6; (9) the sample chip renders
on the Business board too (static, not holder-aware — inherited from
pass-6); (10) my own probe had two method bugs (hover arg, `visible`
field) that cost two extra probe rounds to close.

**10 things to make it 10x better:** (1) fitHero subtracts the fixed-bar
height so nothing sits behind the bar at scroll-0 (the named next-round
fix — cures the note tuck, the toggle depth, and the fit shrink in one
move); (2) pin the fit scale across mode flips (cache by viewport only);
(3) land the gauge sweep in <2s; (4) tile the compact "1.3K" form so the
first orb never flips between plain 40px and tiled 18px; (5) drive the
hero tiles from the live ledger in the verifier's probe; (6) make the
sample holder-aware; (7) grow desktop orbs back to 68px+ despite the
note slot; (8) re-anchor the settings panel below the notif pill;
(9) remove gold from the sequence palette; (10) a permanent scroll-0
overlap guard (note + toggle vs fixed bar) at 360/390/1440 on every pass.

**10 solutions to apply right now:** (1) ship this rebase as-is — all
eight changes measured-pass; (2) file the bar-overlap + fit-shrink notes
as owed next-round work (above); (3) the merge is diff-proven on both
sides, not just counted; (4) this record carries the full measurement
tables; (5) push to the new branch, read-back verified; (6) hand the
verifier the exact live checks owed (real ledger, real Hub render,
sample-link tap on the live page); (7) no merge, no deploy; (8) the eye
verdict is recorded (orb numbers read at a glance in every screenshot);
(9) the stale-dash A/B is recorded so the next round doesn't chase a
sandbox artifact; (10) the probes stay in `pass6on7/` for the next seat.

**Self-score: 9/10.** The rebase is clean and every ordered change is
proven; the deductions are the 390 note tuck that grew in the merge and
the fit shrink — both real, both owed to the named next-round fix, neither
a dropped change. By my own accord it is 9+, so it goes to the next seat;
it is not a 10, and I say so plainly.

## H1–H5 self-attestation (with evidence)

- **H1 — Orb numbers bigger + readable at a glance, 390 + 1440: PASS.**
  Tiles 10→18px @390, 13→24px @1440; plain text 28→40px / 52px; same
  Inter 700; all 9 orbs, all modes; viewed by eye (orb `1 2 9 3`
  in large tiles, % orbs legible). Visual size is smaller than pass-6
  alone (fit scale, §1 above) but clearly bigger than pass-5.
- **H2 — % readable at 390+1440, note clear of gauge, no Quiet, gauge
  live in every mode: PASS.** % orbs 44%/8%/16%/1% legible in screenshots
  at 390 and 1440 and sticking at 9s; note overlap 0px² at all
  widths/modes; Quiet 0× file and rendered; gauge 1 120 / 224% /
  $1 120 (link) and 1 120 / 224% / $1 120 (Business holder) fresh.
  (Scroll-0 bar tuck stated under NOT-DONE; H2's note clause is gauge
  clearance, met — same judgment as the pass-6 verifier.)
- **H3 — Ambassador sample is the real link, matches live data, opens
  the real link: PASS.** Board `nayanet.app/joinus ↗` /
  `https://nayanet.app/joinus` matches my own fresh sb-api rows[0]
  character for character; my own curl 200 at welcome; my own browser
  clicks (360 + 390 + 1440) land on `https://nayanet.app/welcome`,
  "The Official Welcome | NayaNET".
- **H4 — Buttons/links go where a sensible person expects: PASS.**
  Toggle switches PTS/%/MONEY correctly in every run (including a money
  click from a scrolled position); sample link opens the real welcome
  page; Personal board button tap-proven end-to-end to
  `https://nayanet.app/personal` ("Shawn Vibert").
- **H5 — Minis byte-identical to pass-5: PASS with the stated carve-out.**
  30/30 mini values identical to **pass-7 (the live file)**; 27/30
  identical to pass-5 — the 3 differing values are the featured-panel
  stats (`1100/0/0.0%` → `1120/280/200`) under pass-7's intended
  featured-default-to-world change, already live since pass-7 deployed
  and ordered to be kept. D1/D2/D3/D4-R1 all hold (table above).

**OVERALL: PASS** (self-attested; Shawn's eye is the final gate).

## DONE + NOT-DONE

**DONE:** three-way merge with zero conflicts (14 pass-6 hunks + 9 pass-7
hunks, both diff-proven identical); all four pass-6 changes present and
working (orb numbers, note 0px + % sticks, real Ambassador sample,
Quiet gone + live gauge incl. the saved-Business-holder fix); all four
pass-7 changes intact (one button per board, black-obsidian + board-colour
hover, zero gray text, notifications top-right + Running feed); minis
30/30 vs live, D1/D2/D3/D4-R1 hold; fresh live Smart Links fetch matches
the sample; 5 probe scripts, ~40 browser runs, zero console errors,
zero overflow; pushed to the new branch, read-back verified.
**NOT-DONE:** no merge, no deploy live (Shawn's hand only); the 390
scroll-0 note tuck (worse than pass-6) and the fit shrink are NOT fixed
(next round: fitHero subtracts the bar height); the 1440 scroll-0 note
tuck and 390 toggle depth are NOT fixed (same next round); a live render
with the real ledger is NOT proven here (sandbox used synthetic data —
the stale-dash is a sandbox artifact, A/B-proven identical in both
parents); settings-panel-over-pill, sequence-gold, drill gold buttons,
Dashboard self-link inherited from pass-7, not fixed.

## Git

- Base blobs verified: pass-5 `4b4084e1…`, pass-6 `9fb49a37…`,
  pass-7 `9227167d…` (all byte-identical on fetch).
- Merged file blob **`43da5db962ed3141c33b96c9cc3bba4432fbe55f`**, 1,785,787 B,
  sha256 `193087b4119467ef8ee89762549e579355dd56c042596be3445f95cf3fa2a203`,
  commit **`b16d5ee446b0812360dd7f36b1bb6641226dec68`** (read-back verified
  byte-identical via the git-blobs API).
- Link: https://github.com/SoulSchoolAcademy/NayaPOWER/blob/dashboard/pass6-on-pass7-20261110/DASHBOARD/defectfix-v7/pass6on7/dashboard-pass6on7.html
- Branch `dashboard/pass6-on-pass7-20261110` — created from main HEAD
  `7b54c435ce196f8f85ce09b601521c4535246bd5`.
- Supporting files on the branch: this record, `fetch-blobs.py`,
  `pass5-pass6.diff`, `pass5-pass7.diff`, `pass7-merged.diff`,
  `pass6-merged.diff`, `p67_probe.py` … `p67_probe6.py`,
  `p67.json`, `p67b.json`, `p67c.json`, `p67d.json`, `p67e.json`,
  `p67f.json`, `smartlinks-live-p67.json`. Screenshots stay in the
  workspace at `~/workspace/team-nitro/dashboard/defectfix-v7/pass6on7/shots/`,
  `shots2/`, `shots3/`, `shots-crop/`.
