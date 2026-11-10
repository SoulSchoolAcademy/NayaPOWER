# Dashboard Pass-6 — Builder Record

**Branch:** `dashboard/pass6-orb-numbers-20261110`
**Base:** `DASHBOARD/defectfix-v7/pass5/dashboard-pass5.html`, branch `dashboard/pass5-no-gray-text-20261110`, blob `4b4084e1aad4e3fbd64d1052abc2f48cdc56ac23`, 1,778,959 B, sha256 `0e4ef2fef4ccf54c178155f86d14176a56418d1d7590732ce39321b583b4a388` (verified on fetch, byte-identical to local pass-5 file).
**File:** `DASHBOARD/defectfix-v7/pass6/dashboard-pass6.html` — blob `9fb49a377de6e0f00c2e550bdf7859477b12d551`, 1,783,285 B (+4,326), sha256 `034f9f8139112458…` (full: see `apply-pass6.py` run output).
**Link:** https://github.com/SoulSchoolAcademy/NayaPOWER/blob/dashboard/pass6-orb-numbers-20261110/DASHBOARD/defectfix-v7/pass6/dashboard-pass6.html
**Status:** BUILT + SELF-SCORED — 18/18 probe runs clean, screenshots viewed by eye. No merge. No deploy live. Shawn's eye is the final gate.

## The job (brief, as amended by Shawn's word twice over)

1. The 9 hero orb numbers are too small to read — make them a lot bigger, readable at a glance at 390 + 1440. **Same font as the orbs wear now** (it looks good); the eye decides whether the bigger size stays or the orbs go back and the big numbers go elsewhere.
2. The tiny `#os-pts-note` line must stop overlaying the gauge face; the % mode readout must be readable.
3. The Ambassador link board must show the real ambassador link as a sample, harvested from live Smart Links data, never invented.
4. (Amendment) The "Quiet — nothing measured yet." caption goes; the gauge center must show a live number in every mode (PTS / % / MONEY) — never a dash. Diagnose the quiet state: if the state is quiet while the page holds live numbers, the state is wrong and gets fixed, not hidden.
- Mini gauges below: NOT touched. Purple FEATURED tag: NOT touched. "Page tracking connects soon" lines: NOT touched. EDIT the base file, never rebuild; no new page file.

## What was actually wrong (diagnosis, all measured)

**The orb numbers are TILES, not text.** `.os-ld-n` holds `.os-mini-num.orbnum` tiles (A-star/B-star law), and the tile rules capped the digits at **13px desktop / 10px phone** — that is why Shawn's eye saw tiny numbers. Changing `.os-ld-n` font-size to 52px (my first pass) did nothing visible: the digits live in `.os-mini-tile .rd`. The real enlargement is the tile size. Both were done: `.os-ld-n` 28px → 52px desktop / 40px phone (covers the plain-text compact form "1.1K" and the "—" state) AND the orb tiles 16px/13px → 26px/24px desktop, 11px/10px → 20px/18px phone. Same font throughout (inherit, weight 900) — only sizes grew.

**The % readout was broken by a clobber, not by size.** The mode flip wrote "44%" into the orb; the debounced re-tile (150ms) re-rendered it from the stored POINTS back to "280" — probe: "44%" at +50ms, "280" at +200ms, unit already "% OF SCORE". Root cause: `miniConvert`'s already-tiled branch re-rendered blindly from `el._osMiniPts`. Fixed in place: re-tile the CURRENT displayed value; fall back to stored points only when the current text is not a tileable number. Behaviour-preserving for every other tile (boards, drills, minis — proven 30/30 identical, see below).

**The quiet state was wrong, not the caption alone.** `readSpine()` returned quiet whenever the featured holder was a page with no numbers (`_featuredDial.noData`), even though the world spine was live (score 1,120, 3,937 clicks). Shawn's browser holds a persisted featured holder `{kind:'page', id:'business'}` — hence Business on his screen, a dash in the gauge center, and the Quiet caption on a page full of live numbers. Fix: when the featured page has no numbers but the world spine has a finite score, the gauge shows the world's live number. The caption branch now sets an empty caption. The "—" numeral survives ONLY for a ledger that answered empty with no live number anywhere — inventing a number there would be a lie.

**The note overlapped the gauge because of a stale-short box.** `#os-hero-fit` has `transform: scale(s)` and CSS height = natH×s; the note's `bottom:64px` anchored to that box and landed mid-gauge on desktop (measured ~1,910px² in % mode, ~2,056px² in money mode at 1440 in the baseline). Fix: the note moved in-flow, just before the toggle, with its slot always reserved (`min-height:45px`, `visibility` toggled, never `display:none`), so the fit scale never jumps between modes.

## Edits applied (16, via `apply-pass6.py`, each asserted exactly-once)

1. Orb number, same font: ultimate override 28px → **52px** desktop.
2. Phone media query: orb number **40px**.
3. Phone orbs bigger: `ldLayoutNodes` mobile `nd` 64/66 → **96**; mobile orbit gap 40 → **32**.
4. `#os-pts-note` moved in-flow before the toggle; flow CSS, **15px**, `min-height:45px`.
5. `_refreshPtsNote`: `hidden` → `visibility` (text logic identical).
6. `readSpine`: featured-page `noData` falls back to the live world spine.
7. Quiet caption: `paintRest` quiet branch now `setCap('')`. "Quiet — nothing measured yet" count in the file: **0**.
8. Ambassador sample added to `#os-feat-panel` (+ CSS, obsidian chip, 17px, purple headliner glow).
9. Orb tiles desktop: 16px/13px digit → **26px/24px digit**.
10. Orb tiles phone: 11px/10px digit → **20px/18px digit**.
11. `miniConvert`: re-tile the current displayed value (fixes the % clobber).

Diff vs pass-5 base: **15 hunks, 130 diff lines** — every hunk maps to one of the edits above; no stray hunks. Untouched markers verified identical in count: `scroll-margin-bottom:20px` 1=1 (D4-R1), "Ambassador payouts land every Wednesday" 1=1, "page tracking connects soon" 5=5, `.os-mini-num.med .os-mini-tile{width:54px` 1=1. Mini tile CSS rules identical (only line-shifted).

## Ambassador link — harvested live (never invented)

Live Smart Links, `sb-api` `GET /rest/v1/smart_links` (`owner_alias=eq.flagship-personal`, `active=eq.true`), 2026-11-10 ~05:20Z: **14 active links** (matches the Dashboard's "14 links out in the world — 3,937 clicks"). The system's own definition (code comment + `_resolveHolder`): the ambassador link is the citizen's first Smart Link = earliest `created_at` = rows[0]. That is: name **`joinus`**, short address **`nayanet.app/joinus`**, target **`https://nayanet.app/welcome`**, id `5011fe87-7d29-4208-8d86-a6bc98d508f3`, created `2026-10-23T15:57:23.116941+00:00`. Verified live with curl 05:20:58 UTC: `https://nayanet.app/joinus` → **302 → `https://nayanet.app/welcome`**. The board sample renders exactly that: text `nayanet.app/joinus ↗`, href `https://nayanet.app/joinus`, 17px. Full live data: `smartlinks-live.json`.

## Measurements (after-probe, `probe-after.py`, Playwright Firefox, synthetic spine score 1,120 + synthetic ledger; 2 scenarios × 3 widths × 3 modes = 18 runs, `after/after.json`)

### Orb numbers — tile digits (the number the eye actually sees)

| width | pass-5 tile digit | pass-6 tile digit | pass-6 tile width (visual) | orb diameter |
|---|---|---|---|---|
| 1440 | 13px | **24px** | 14.1px (26 × 0.542 fit) | 73.1px (was 76) |
| 390 | 10px | **18px** | 17.4px (20 × 0.87 fit) | 83.5px (was 61) |
| 360 | 10px | **18px** | 16.7px (20 × 0.837 fit) | 80.3px (was 60) |

All 9 orbs tiled in every mode/scenario. Orb values render real numbers (Clicks 1100, Joins 0, Smart notes 280, Invites 50, Creations 100, Saves 5; page-holder scenario: Clicks 1293, Joins 200). Plain-text compact form ("1.1K") renders at 52px desktop / 40px phone via the `.os-ld-n` rule. Same font family/weight as before, all 9 orbs, all modes. Zero console errors, no horizontal overflow, all 18 runs.

### % mode — percentages stick (the clobber is gone)

% mode, 3s after the click, every scenario/width: notes **44%**, invs **8%**, posts **16%**, saves **1%**, shares/comments/likes **0%**, joins **0%** (link) / **31%** (page, 200 of the page's world). Sales stays **1100** (a count stays a count — PASS 4 fail 3 law). Gauge numeral **220%** (link, target 1100) / **224%** (page, target 1120). Money mode: gauge **$1 100** (link) / **$1 120** (page); orbs stay counts, as the law requires.

### Gauge + Quiet (the amendment's exact change #4)

`data-state=live` in **every** mode/scenario/width; caption empty; `quietOnPage=False` everywhere; "Quiet — nothing measured yet" appears **0 times** in the file and **0 times** on any rendered page. The page-holder scenario (localStorage `{kind:'page', id:'business'}`, reproducing Shawn's screen) now engages — marker `★ FEATURED — BUSINESS`, name `Business` — and the gauge is live there too: numeral live in PTS/%/MONEY, no dash, no caption. Proven by eye in `p6-hero-page-390-pts.png` (big tiles "1 1 1 0", orbs 1293/200/280, no Quiet text anywhere).
- Gauge sweep honesty: the numeral eases and lands on its target in ~6–8s (tracked: 863 → 1048 → 1093 → **1 100 → 1 100**; identical in pass-5 base — pre-existing, not a pass-6 regression). At the probe's 3s settle the numeral reads mid-sweep (e.g. 1 021); the screenshots catch the same mid-sweep. The number is always live, never a dash.

### #os-pts-note — overlap 0px everywhere

Note is 15px, color `rgba(255,255,255,0.88)` (a later rule wins over the `#fff` I wrote — still near-white, readable). Hidden in PTS mode, visible in %/MONEY. Overlap vs the dial SVG: **area 0px² in all 18 runs** (PTS / % / MONEY, 390 / 1440 / 360, link + page). At 1440 the note sits at y 837–862, directly above the toggle (toggle top 861.7) — below the dial bottom (~724). At 390 it sits at y 726–787, toggle directly below it.

### Minis — unchanged (H5 substance)

30/30 mini values **identical** between the pass-5 base and the pass-6 file at 1440 and at 390 (`probe-diff.py`, `diff-check.json`: "minis 1440 identical: True, minis 390 identical: True"). The shared `miniConvert` function text changed (the % fix); no mini renders differently. Mini tile CSS rules byte-identical (line-shifted only).

## The eye verdict (the amendment makes the eye the judge)

Viewed: `p6-hero-link-1440-pts.png`, `p6-hero-link-390-pts.png`, `p6-hero-link-390-pct.png`, `p6-hero-link-1440-pct.png`, `p6-hero-link-390-money.png`, `p6-hero-page-390-pts.png`, `p6-feat-1440.png`, `p6-feat-390.png`.
- **The bigger numbers look better — they stay.** The 24px/18px tile digits fill the orb without touching the bezel; single digits don't look lost; 4-digit numbers ("1 1 0 0", "2 8 0") read at a glance at both widths. The orbs do NOT go back to the original font; no big numbers need moving elsewhere.
- % reads at a glance ("44%", "8%", "16%" on the orbs; "220%" in the big tiles). Money reads ("$1 100"). The note reads cleanly in white, clear of the gauge face.
- The Ambassador sample chip looks like a real elite object on the board at both widths; the minis below it are untouched and look good.

## Self-scorecard (maker first — the three-step verification, step 1)

**Why it is not a 10:** at 1440 scroll-0 the note's line tucks partly behind the fixed bottom bar in %/money modes (fully readable on scroll; fully visible at 390); the phone fit scale still drifts across mode flips (390: 0.87 → 0.823 → 0.801); the gauge sweep takes ~6–8s to land; the same orb shows two number sizes by state (tiled 24px digits vs plain-text 52px compacts); the toggle sits ~32px deeper behind the fixed bar at 390 scroll-0 than in pass-5.

**10 things I love:** (1) the tiles finally read at a glance — 13px → 24px digits; (2) % sticks — 44%/8%/16% survive the flip; (3) the Quiet fix proven in the exact Business-holder state from Shawn's screenshot; (4) the note is 0px off the gauge face in every mode; (5) the sample chip looks like a real elite object; (6) minis 30/30 identical to pass-5; (7) zero console errors in all 18 runs; (8) no horizontal overflow anywhere; (9) the same font throughout — nothing redesigned; (10) the % clobber was caught by measurement, not by Shawn's eye.

**10 things I don't love:** (1) 1440 note vs fixed bar; (2) fit-scale drift on phones; (3) 6–8s gauge sweep; (4) tile vs plain-text size mismatch (24px vs 52px); (5) toggle deeper behind the bar at 390; (6) desktop orbs shrank 76 → 73.1px from the reserved note slot; (7) the gauge plate shows the dial position ("76"), not the full number, mid-sweep; (8) the sample renders on the Business board too (static, not holder-aware); (9) money-mode orbs stay points — a first-time eye may expect $ there (settled law, but it will be asked); (10) the note's effective color is .88 white, not the #fff written (a later rule wins).

**10 things to make it 10x better:** (1) fitHero subtracts the fixed bar height so nothing sits behind it at scroll-0; (2) tile the compact "1.1K" form so orbs never flip between plain 52px and tiled 24px; (3) make the gauge sweep land in <2s; (4) pin the fit scale across mode flips (cache by viewport only); (5) grow desktop orbs back to 76px+ despite the note slot; (6) show the full number in the gauge plate, not just the dial position; (7) make the sample holder-aware; (8) resolve the note color to #fff as written; (9) money-mode orb $ tiles for non-count orbs (needs Shawn's word — counts-stay-counts is settled law); (10) a live render check on the real Hub with the real ledger.

**10 solutions to apply right now:** (1) ship this round as-is — all brief changes measured-pass; (2) file the bar-overlap + fit-drift + sweep notes as owed verifier checks (below); (3) the miniConvert clobber fix is in the code with its comment; (4) this record carries the full measurement tables; (5) push to the new branch, read-back verified; (6) hand the verifier the exact live checks owed (real ledger, real Hub render, sample-link tap); (7) no merge, no deploy; (8) the eye verdict is recorded (bigger stays); (9) the amendment's "eye decides" is answered with the eight screenshots viewed; (10) the record + probes stay in `pass6/` for the next seat.

**Self-score: 9/10.** The brief's four changes are done and proven; the deductions are the scroll-0 bar tuck, the fit drift, and the slow sweep — all pre-existing in kind, none blocking the brief. By my own accord it is 9+, so it goes to the next seat; it is not a 10, and I say so plainly.

## H1–H5 self-attestation (with evidence)

- **H1 — Orb numbers bigger + readable at a glance, 390 + 1440: PASS.** Tile digits 13px → 24px (1440), 10px → 18px (390/360), all 9 orbs, all modes; viewed by eye in 8 screenshots.
- **H2 — #os-pts-note 0px overlap + % readable: PASS.** Overlap area 0px² in all 18 runs (PTS/%/MONEY); % orbs read 44%/8%/16% and stick; gauge 220%/224%.
- **H3 — Ambassador sample is the real harvested link: PASS.** `nayanet.app/joinus` on the board matches sb-api rows[0] (`joinus`, `https://nayanet.app/welcome`, created 2026-10-23) and the live 302; 17px, href `https://nayanet.app/joinus`.
- **H4 — Quiet gone, live number in every mode: PASS.** `data-state=live`, caption empty, `quietOnPage=False` in all 18 runs; page-holder (Business) state proven by eye and JSON; gauge lands on target (tracked to 1 100).
- **H5 — Nothing else touched: PASS.** Minis 30/30 identical to pass-5 base; mini CSS identical; FEATURED tag, "page tracking connects soon" lines (5=5), D4-R1 rule (1=1), payout line (1=1) all untouched. One honest note: the shared `miniConvert` function text changed (the % fix) — its mini output is proven identical, but the function is not byte-identical to pass-5.

**OVERALL: PASS** (self-attested; Shawn's eye is the final gate).

## DONE + NOT-DONE

**DONE:** orb numbers enlarged in the same font (tiles + plain text); phone orbs enlarged (96px); note in-flow, 15px, 0px gauge overlap, slot reserved; % clobber fixed (percentages stick); Quiet state fixed at its root (world-spine fallback) + caption removed; Ambassador sample (real harvested link) on the board; minis verified unchanged; 18/18 probe runs clean; 8 screenshots viewed by eye; diff checked (15 hunks, all intended); pushed to the new branch, read-back verified.
**NOT-DONE:** no merge, no deploy live (Shawn's hand only); the sample link tap on the live Hub (needs the live browser — the probe proves the href + the live 302, not the tap); a live render with the real ledger (sandbox used synthetic data); the 1440 scroll-0 note-vs-bar tuck, the phone fit-scale drift, and the 6–8s gauge sweep are noted, not fixed (pre-existing in kind, out of this brief's scope).

## Verifier checks owed (live, not sandbox)

1. Real ledger: orbs show the live numbers on the real Hub; gauge lands on the live score.
2. Real Hub render at 390 + 1440: orb tiles read at a glance; note clear of the gauge; % and money readouts legible.
3. Tap the sample link on the board — lands on `https://nayanet.app/welcome`.
4. Business-holder state (Shawn's persisted featured holder): gauge live, no Quiet caption, no dash.
5. Minis below the board: values match pass-5.

## Git

- Base blob `4b4084e1aad4e3fbd64d1052abc2f48cdc56ac23` (pass-5) — untouched.
- Pass-6 file blob `9fb49a377de6e0f00c2e550bdf7859477b12d551`, 1,783,285 B.
- Branch `dashboard/pass6-orb-numbers-20261110` — created from main HEAD (read live at push time).
- Commits: `80b9b60af56d055e4bfb84179e95145907d2aae3` (pass-6 HTML; base main `7b54c435ce196f8f85ce09b601521c4535246bd5`); the record + supporting files follow in the next commit on this branch (head SHA in the handoff report).
- HTML blob read-back via git-blobs API: byte-identical, sha256 `034f9f813911245828b4a727e8af8f9080966ed0a76d5d9899f65fd3a12a367e`.
- Supporting files on the branch: `PASS6-BUILDER-RECORD.md`, `apply-pass6.py`, `probe-after.py`, `probe-pct.py`, `probe-diff.py`, `probe-toggle.py`, `probe-bar.py`, `after/after.json`, `diff-check.json`, `smartlinks-live.json`. Screenshots stay in the workspace at `~/workspace/team-nitro/dashboard/defectfix-v7/pass6/after/`.
