# RECORD — FACTORY LANE L7 — ONE FLOW: ONE MAP, ONE ORDER, ONE WALL

## What it is

One Factory file — the live one on main, verified first — with one map, one order, one wall. The two Factories are converged into the file that is live on main: the steps run 1–2–3–4–5–6 in order, no duplicate ids, the 12-template wall appears once, the specimens sit outside the step flow, the top-nav tabs name the same steps in the same order, and the copy says "Six steps" because there are six.

## Why

The citizen was seeing two different pages. The BASE file numbers its steps 1-2-4-3-5 with a duplicate id, carries the template wall twice, and says "Four steps" over a five-step flow; the FLOW file's ids lagged its kickers by one, so the nav and the steps disagreed. L8, L9, and every later Factory lane build on the canonical Factory file, and until this lane it did not exist. This lane creates it — by converging the live file, not by rebuilding the page.

## Nutshell

- **The Factory is the FLOW file**, `TEAM-NITRO/factory-flow-fix4/factory-flow-fix4-20261111.html` on main — byte-identical to the local starting file (759,594 B, sha256 `dc901330…`, git blob `ca85f2dc…`). The BASE file also lives on main at its own path, but its bytes differ from the local BASE copy, and it is not the live Factory file this lane converges.
- **The convergence is 108 lines, nothing else.** Id renames (`step2-create`→`step2`, `step2`→`step3`, `step3-templates`→`step4`, `step4`→`step5`, `step5`→`step6`), nav `data-go` to match, "Four steps" → "Six steps" (2 cards + 2 aria-labels), step rails extended 4→6 dots, stale refs retargeted (orb gallery, pieces, contract, summary links), and one nesting repair (a stray `</div></div>` removed, a `</div></div>` seam added) that puts NAVIGATION + OVERLAYS back inside the pieces library so the page ends at the contract.
- **Proven by render, four probe runs + one nav-click run.** At 1440 the two makers' runs agree exactly in both files; zero overflow, zero console errors, zero failed requests at 1440/390/360 in every run. Real mouse clicks land exactly on all six steps. Cart, template select + VIEW, eye jewels (9 panels), BUILD guard, and the empty Step 1 fields all re-proven working. The design-contract gate gives the identical verdict on before and after (18 findings, all pre-existing, none new).
- **Honest score: 9/10.** What keeps it from 10 is named in the scorecard, not hidden.

## Step 1 — Which file is the Factory (read first-hand)

Main's tree, read first-hand on 2026-11-13 ~01:30Z (main HEAD then `09c59280`, 2026-11-13T01:14:55Z, "Team Transparency round: file NN-20261113 Team Transparency build"):

| File on main | Size | Git blob | Local match |
|---|---|---|---|
| `TEAM-NITRO/factory-flow-fix4/factory-flow-fix4-20261111.html` | 759,594 B | `ca85f2dc8e6a242698a9f839aa3e5713a838379b` | **Exact match** with local `lane-l7-probe/before-flow.html` (sha256 `dc901330…`) |
| `TEAM-NITRO/factory-base-f-20261111/smartfactory-base-f-20261111.html` | 580,300 B | `983d67267aa28e40a6d5238f74badf91234bcee0` | **No match.** Local BASE file is 580,186 B, sha256 `f9bfd25c…`, git blob `c3432bc8…` — 114 B different from main's BASE bytes |

**Decision: the FLOW file is the Factory.** It is the file live on main at the brief's starting bytes, and it is the file the L2 edit already landed in. Its repo home is `TEAM-NITRO/factory-flow-fix4/factory-flow-fix4-20261111.html` — so this lane has a repo home to merge to (not the L6 no-home case). The branch `factory/pi-align-l7-one-flow-20261111` did **not** exist on GitHub (404, "Branch not found") — the interrupted maker never created it; this maker creates it from main HEAD before filing.

**The BASE file becomes the archive.** It lives in git; nothing is deleted and it is not edited. One wrinkle, named plainly: the local BASE copy (580,186 B) is not the same bytes as main's BASE file (580,300 B). That 114 B drift is not this lane's work — the BASE is not the canonical file and nothing in this lane touches it — but a later lane that archives the BASE should re-read main's BASE bytes first-hand rather than trusting the local copy.

**A-item adjudication for the FLOW file** (from `MISALIGNMENT-LIST.md` §2 + `scout-a-factory-page.md` — each item checked against the FLOW file as Step 1 found it):

- **A-1 (two Factories)** — resolved by this Step 1: the FLOW file is the Factory; the BASE file is the archive.
- **A-2 (BASE numbers 1-2-4-3-5, duplicate id step4)** — BASE-only. The FLOW version is different: its ids lag its kickers by one (`step2-create`, `step2`, `step3-templates`, `step4`, `step5` against kickers STEP 1–5). The rename fixes exactly this.
- **A-3 (wall twice)** — BASE-only. The FLOW file renders the wall 12/12 once (proven in every probe run). **Not present as described — named, not assumed.**
- **A-4 (Smart Spaces hero specimen)** — BASE-only. The FLOW file has no `refHero` specimen in the flow (`refHero: false` in every probe run). **Not present as described.**
- **A-5 (Notifications drawer specimen)** — present in the FLOW file, and the nesting bug is its mechanism: the stray `</div></div>` before the ROWS railblock had ejected NAVIGATION + OVERLAYS from the pieces section, so they rendered after the contract as a direct child of BODY. The repair puts them back inside the library. The drawer is a library specimen in the OVERLAYS railblock; after the repair the page ends at the contract + footer.
- **A-25 (nav matches steps)** — the nav labels name the steps and run in the same order; the `data-go` values lagged the ids by one, exactly like the ids lagged the kickers. Fixed by updating `data-go` to the renamed ids.
- **A-27 (copy matches the real count)** — the page said "Four steps" over a six-step flow (2 library cards + 2 aria-labels). Changed to "Six steps" — the true count, in plain words — because the flow has six steps and the copy must tell the truth about it.
- **A-31 (refs point at the right step)** — orb gallery Step 3→5, pieces Step 3→5, contract Step 5→6, summary CHANGE links retargeted. Fixed.

## Step 2 — The convergence (108 lines, item by item)

The converged file is the on-disk FLOW file `factory-flow-fix4-20261111/factory-flow-fix4-20261111.html`, edited in place by the interrupted maker's `make_l7.py` and verified byte-identical to `lane-l7-probe/after-flow.html` (759,814 B, sha256 `78d83578e819022f041c4f78c4435bb424884c1e2c62c31d3649f92a19d527a9`, git blob `4f398992a5f85c887f0206c756311bbc2268ec6b`). The diff `before-flow.html` → `after-flow.html` is **108 lines, all accounted for**:

1. **Id renames (29 token occurrences, asserted by the script):** `step2-create`→`step2`, `step2`→`step3`, `step3-templates`→`step4`, `step4`→`step5`, `step5`→`step6`. `step1` and `stepAddons` unchanged.
2. **Nav `data-go` updated to match:** IDEA→step1, CREATE→step2, QUESTIONS→step3, PAGES→step4, PIECES→step5, CONTRACT→step6.
3. **Copy:** "Four steps" → "Six steps" in 2 library cards + 2 aria-labels. Step rails extended 4→6 dots.
4. **Stale refs fixed:** orb gallery Step 3→5, pieces Step 3→5, contract Step 5→6, summary CHANGE links retargeted.
5. **Nesting repair:** the stray `</div></div>` at line 3509 removed before the ROWS railblock; a `</div></div>` seam added before the NAVIGATION railblock at line 3674. This is the A-5 fix: NAVIGATION + OVERLAYS return inside the pieces library.
6. **JS selectors renamed consistently**, including the scroll-spy observer list → `["step1".."step6"]`.

**Nothing else changed.** No build logic, no processor, no contracts, no PI wiring, no prices, no doors, no live route. The before-file is kept byte-identical in the work dir (`lane-l7-probe/before-flow.html`, sha256 `dc901330…`, git blob `ca85f2dc…` — the same bytes as main).

**Pre-existing quirk found in the diff, NOT a regression, NOT in scope:** `syncPreview()` and the bottom-strip template handlers query `#step5.tcard2…` (the pieces section) while the template grid lives in step4 — a no-op in both before and after (the file's own comment at line ~4227 documents it). That is A-24 territory, for a later lane. The BUILD guard text ("Pick your template in Step 4 first") now names the true step by id as well as by kicker — a side-effect of the rename, not a change.

## Step 3 — Proof (Playwright, by eye)

Four probe runs (`before2.json`, `before-mine.json`, `after.json`, `after-mine.json`) plus one nav-click run (`navtest.json`), all in `lane-l7-probe/`. Playwright Chromium (Firefox fallback in the scripts). Widths 1440 / 390 / true 360, scroll 0 AND scrolled, screenshots by eye.

### Structure — identical in every run, both files at 1440

| | Before | After |
|---|---|---|
| Step ids in order | step1, step2-create, step2, step3-templates, step4, stepAddons, step5 | step1, step2, step3, step4, step5, stepAddons, step6 |
| Kickers in order | STEP 1–5 (+ add-ons) | STEP 1–6 (+ add-ons) |
| Duplicate ids | none | none |
| Nav (label → go → target exists) | IDEA→step1, CREATE→step2-create, QUESTIONS→step2, PAGES→step3-templates, PIECES→step4, CONTRACT→step5 — all exist | IDEA→step1, CREATE→step2, QUESTIONS→step3, PAGES→step4, PIECES→step5, CONTRACT→step6 — all exist |
| Wall rendered / source | 12 / 12, once | 12 / 12, once |
| "Four steps" / "Six steps" | 2 / 0 | 0 / 2 |
| Notif drawer top (1440) | 14,263 | 12,931 |
| Contract top (1440) | 10,944 | 14,854 |
| Document height (1440) | 15,116 | 16,446 |
| Overflow (top/bottom inner width) | 1440 / 1440 at every width | 1440 / 1440 at every width |
| Console errors / failed requests | 0 / 0 at every width | 0 / 0 at every width |

The two makers' runs agree **exactly** at 1440 in both files (notif top, contract top, document height identical to the pixel). At phone widths the structure is identical in every run; the heights vary (see "Phone-width heights" below).

### Nav clicks — real mouse, 1440, 1.5 s settle

| Pill | Before (scrollY vs target) | After (scrollY vs target) |
|---|---|---|
| IDEA | 758 = 758 ✓ | 758 = 758 ✓ |
| CREATE | 2,233 = 2,233 ✓ | 2,233 = 2,233 ✓ |
| QUESTIONS | 2,407 = 2,407 ✓ | 2,407 = 2,407 ✓ |
| PAGES | 3,683 = 3,683 ✓ | 3,683 = 3,683 ✓ |
| PIECES | 5,862 vs 5,869 (−7 px, smooth scroll still settling) | 5,181 = 5,181 ✓ |
| CONTRACT | 10,944 = 10,944 ✓ | 14,854 = 14,854 ✓ |

**The nav-click anomaly from the first probe is a probe artifact, not a page defect.** The first probe's synthetic click + 900 ms wait measured 3,683 for the QUESTIONS pill in 3 of 4 runs. With real mouse clicks and a 1.5 s settle, every pill lands exactly on its named step in both files. (One pre-existing wrinkle, same in both files: clicking CREATE lights the QUESTIONS pill in the scroll-spy — the CREATE section is only ~110–150 px tall, so the spy's band falls on QUESTIONS below it. Spy behavior, not a convergence issue.)

### No-regressions (§3 "what works", re-proven)

| Check | Before | After |
|---|---|---|
| Cart (deterministic test: click, center the button first) | clicked, badge "1", "In cart ✓", cart_len 1 | clicked, badge "1", "In cart ✓", cart_len 1 |
| Template select + VIEW | true / true | true / true |
| Eye jewels | opened, 9 panels — the nine Step 1 eye-panels (named below) | opened, 9 panels — the same nine |
| BUILD guard fires | true ("Pick your template in Step 4 first…") — fires only when no template is selected (stated below) | true (same text — now true by id too) |
| Step 1 fields empty on fresh profile (L2 pre-fill) | all empty | all empty |
| Live preview text | "LIVE PREVIEW — UPDATES AS YOU PICK YOUR TEMPLATE…" | same |

**Eye jewels — the nine panels, named.** The checker's count of 9 is the nine Step 1 field info panels, all inside `<section id="step1">` (lines 2390–2433 of the converged file): `eye-vision` (line 2394, VISION) · `eye-name` (2405, PAGE NAME) · `eye-title` (2408, TITLE) · `eye-subtitle` (2411, SUBTITLE) · `eye-goal` (2414, GOAL) · `eye-mission` (2417, MISSION) · `eye-about` (2420, ABOUT) · `eye-soul` (2423, SOUL COLOR) · `eye-photo` (2426, YOUR PHOTO). Each is a `.visioncard.elev-2.eye-panel` div with `id="eye-…"`, opened by an `.os-jewel.os-jewel-sm.eye-jewel` "i" button carrying the matching `data-panel="eye-…"`. These are NOT the JEWELS library railblock (21 cards, `NAYA-JWL-001`…`NAYA-JWL-021`) and NOT "Orbital nine" (`NAYA-BRD-027`, "center + nine satellites") — those are pieces-library specimens, different things, which is why the cloud-browser click-proof, searching by the name "eye-jewel panels", found neither and could not confirm the count by name. The maker's probe opened all nine by their `data-panel` ids.

**BUILD guard — where the text lives and when it shows.** The text is not static markup. It is a JavaScript string at line 4001 of the converged file, inside `function startBuild()` (line 3999), behind the condition `if(!document.querySelector('.tcard2.sel'))` (line 4000): it fires only when no template card carries `.sel` — i.e. no template selected in Step 4 — and `setBuildStatus` (line 3998) then writes it into `#buildStatus` / `#sumStatus`. The BUILD button wires it at line 3996 (`buildBtn.onclick = ()=>{startBuild(); openSummary();}`). In the cloud-browser click-proof the Personal template was already selected / restored in the draft, so `.tcard2.sel` existed, the guard never fired, and the text never entered the DOM — that is why the browser's accessible tree (1,576 refs) had no match. The checker verified the text identical statically in both files.

The first probe's `cart_clicked_ok: false` in both files was probe flake (the locator timed out without scrolling the button into view). The deterministic re-test passes on both files — the cart works, and the convergence did not touch it.

### Screenshots — by eye

Viewed by the maker: after 1440 top (hero, six pills, no overflow), after 1440 mid (BOARDS railblock, elite cards, no overlap), after 1440 bottom (S8–S13 checklist + BUILD button, page ends at the contract), before2 1440 bottom (MARKERS railblock + the empty black void — the nesting bug's signature, gone in after), after 390 top (six pills fit one line, hero, no overflow; H1 cut at the fold is pre-existing A-34), after 390 bottom (S11–S13 + BUILD, no specimen after the contract). In the after 1440 top shot the CONTRACT pill reads lit — a probe-timing artifact after scroll-to-bottom-and-back; the mid shot shows PIECES lit correctly at 45% scroll.

### Phone-width heights — the honest variance

At 390/360 the pieces-section height varies between loads, in **both** files, while the structure (ids, kickers, nav, wall, copy) is identical in every run:

| File @ width | Document heights across runs | Railblocks across runs |
|---|---|---|
| Before @ 390 | 16,867 / 21,579 / 16,867 / 18,610 | 11 / — / 11 / 13 |
| Before @ 360 | 17,422 / 17,388 / 17,422 / 17,422 | 11 / — / 11 / 11 |
| After @ 390 | 18,192 / 22,801 / 22,801 / 22,801 | — / — / 13 / 13 |
| After @ 360 | 18,748 / 29,463 / 18,748 / 18,714 | — / — / 13 / 13 |

What the evidence says: the foot-of-page rails rebuild re-parents the rails, and its timing varies per load. In the **before** file the NAVIGATION + OVERLAYS railblocks flip-flop in and out of the DOM (11 vs 13 blocks at 390) — the flip is real in the data. What is NOT proven is the mechanism this record first named: the rebuild IIFE (`after-flow.html` lines 4928–4962) works strictly inside each `.railblock` — it collects that block's `.pcard` cards, builds a new `.rail`, moves the cards into it, and replaces the old rail within the same block — and it never removes a railblock, so "dropped by the rebuild" is unproven and is withdrawn here. The cause of the flip stays open (A-24). In the **after** file the count is stable at 13 in all four nav-test loads, because the blocks now live inside the section the rebuild works on. But the section height can still swing on a single load (one after run at 360 measured 29,463 against ~18,730 in the other three), so the height variance is **pre-existing and not fully cured** by this lane. The structure is what L7 guarantees, and the structure is stable everywhere. The rebuild's internals are A-24 territory for a later lane — this lane does not touch the rebuild.

A timing test to pin the variance to measurement timing (`timingtest.py`, 360, 1.2 s vs 2.0 s) could not run: the VM browsers died again ~01:43Z (Chromium SIGTRAP, Firefox SIGSEGV on launch — the same intermittent failure as 17:32Z Nov 12, which cleared by 22:15Z). Two launch attempts failed. The variance is already documented with the evidence above; the timing test is not a gate for this lane and is not re-attempted here.

### Design-contract gate (a)–(i) + H1–H5

Machine gate run with `design-contract-gate/check-gate.py` on both files (static source check; live-render evidence above is stronger and agrees):

| Item | Before | After |
|---|---|---|
| (a) zero white/light backgrounds | PASS | PASS |
| (b) every element raised/elevated | PASS | PASS |
| (c) gauges present and alive | PASS | PASS |
| (d) no text-in-image, no pasted document | PASS | PASS |
| (e) no bare text blocks | PASS | PASS |
| (f) no look-alike buttons/gauges/numbers | **FAIL — 18 findings, pre-existing** | **FAIL — 18 findings, identical** |
| (h) no dictation-blunt phrases | PASS | PASS |
| (i) title + subtitle + nutshell + faces alternate | PASS (not applicable — no story boards) | PASS (same) |

There is no (g) item in this version of the gate script (the enumeration runs (a)–(f), (h), (i)). The (f) findings — `steppill` ×6, `inbox-mic` ×7, `tview` ×2, gold-theme CTA `primo theme-gold` ×3 — are the page's own button classes, present at the same lines (±1) in both files. The count is **18 in before and 18 in after**: zero new findings from the convergence. Fixing (f) would mean renaming the page's own button classes — a rebuild, explicitly NOT authorized. It is named here as pre-existing, not hidden, and it belongs to a later lane, not L7.

**H1–H5, attested by the maker from the rendered page and the screenshots:**
- **H1 Stranger test — PASS.** A stranger reads six steps in order (IDEA → CREATE → QUESTIONS → PAGES → PIECES → CONTRACT), each with its kicker and its boards, and the BUILD button at the end. The copy now says six because there are six.
- **H2 Perfect-words law — PASS.** Every label is copied from what it does; the only copy change is "Four steps" → "Six steps", the true count in plain words. No dictation pasted, no process talk in the page.
- **H3 Face quality — PASS.** The Naya faces beside the words render as before (the convergence touches no image, no face, no orb). No pixelation or blur introduced — nothing in the diff touches an image.
- **H4 Test in his head — PASS.** Six steps, one wall, nav that lands where it says, cart that works, guard that stops an empty build. A stranger can walk it cold.
- **H5 One ultimate ten — PASS.** One set, not two: one step order, one wall, one nav. Each step is a pain (build a page) + the solution (this step) + what is in it for them (the contract at the end).

## The five gates (on the merge decision, before the first PUT)

1. **Is it right?** Yes — one Factory, telling the truth about its own six steps, or it does not go in. The copy, the ids, the nav, and the wall all agree now.
2. **Is it what they truly need?** Yes — the captain needs one canonical file so L8, L9, and every later Factory lane build on the right base. Without this lane there is no canonical file.
3. **Is it mine to do?** Yes — this brief authorizes exactly the convergence. Build logic, processor, contracts, PI wiring, prices, doors, and the live route are untouched and remain NOT mine.
4. **Is now the time?** Yes — the loop is proven (Waves 1–2), the base is verified first-hand on main, the items are named, and the proof is in hand.
5. **Can I prove it?** Yes — the renders prove it: step ids, wall count, nav labels, and copy read back from the rendered file at three widths, in four probe runs plus a real-mouse nav run, with the before-file kept byte-identical for the diff.

## Self-check ×3 (each round found NEW things)

**Round 1 — the convergence itself (re-audit of the after file on disk).**
Re-ran the counts on the on-disk FLOW file: ids step1–step6 exactly once each; kickers STEP 1–6 in order; "Four steps" 0, "Six steps" 2; diff before→after 108 lines; diff before→on-disk file 108 lines; shas identical (`78d83578…`). **New findings:** the BUILD guard text ("Pick your template in Step 4 first") is now true by id as well as by kicker; the `tcard2` class occurs 36 times in the source (12 cards × the class's occurrences in markup, CSS, and JS) — the rendered wall count of 12 is the authority, not the grep count.

**Round 2 — the proof (re-read every JSON; ran the gate on both files).**
Re-read `before2.json`, `before-mine.json`, `after.json`, `after-mine.json`, `navtest.json` line by line and confirmed every number cited in this record. Ran `check-gate.py` on both files. **New findings:** the gate count is exactly 18/18 identical (no new findings); the local BASE file differs from main's BASE bytes by 114 B (the record now names it); the first probe's cart failure is flake, proven by two independent passing cart tests; the VM browsers died again ~01:43Z, which killed the timing test — named in the record, not hidden.

**Round 3 — the filing (done at PUT time, before the report to the captain).**
Re-checked main HEAD (moved 09c59280 → 091961ba between Step 1 and filing; the FLOW file's blob on main was unchanged, still `ca85f2dc…`), created the branch from the current HEAD, filed the three files one at a time, and read back every PUT from the branch. **New findings:** main HEAD moves under the lane while the Factory file stands still — the branch must be cut from the HEAD at filing time, not the HEAD at Step 1 time; the EPERM flake was active for file writes at 01:44–01:46Z (python + `cat` writes refused, 0-byte files left behind and removed) while GitHub writes and the record write went through — the flake is per-path and per-moment, not a stop. Read-back confirmed all three files byte-exact on the branch (see Filing).

## The seven pre-merge questions (answered IN WRITING)

1. **Three self-checks done?** Yes — Round 1 (convergence), Round 2 (proof + gate), Round 3 (filing read-back). Each found new things; each is written above.
2. **Honest 9+?** Yes — 9/10 (see the scorecard). The point off is the phone-height variance the lane does not cure and the pre-existing (f) gate FAIL, both named in the record.
3. **Blast radius named?** Yes — one file, `TEAM-NITRO/factory-flow-fix4/factory-flow-fix4-20261111.html`, on the lane branch only. The BASE file is untouched. No other file, no live route, no deploy. The merge, when it comes, replaces the FLOW file on main with the converged bytes and nothing else.
4. **Checks green?** The checks that belong to this lane are green: four probe runs + nav run, zero overflow, zero console errors, zero failed requests, all no-regressions passing, gate identical before/after. The one red item — gate (f), 18 pre-existing findings — fails identically on the before-file and is out of this lane's scope (renaming the page's own button classes would be a rebuild).
5. **Five gates?** Yes — run above, all five yes, before the first PUT.
6. **Real proof?** Yes — live bytes: the rendered structure read back at three widths, real mouse clicks landing on all six steps, the deterministic cart test, the gate run on both files, the 108-line diff, the byte-identical before-file, and the main-tree blob match. No claim without a measurement.
7. **No silent known defects?** Yes — every known defect is named in this record: the phone-height variance (§Step 3), the (f) gate FAIL (pre-existing), the `syncPreview` #step5 no-op (A-24), the CREATE-pill scroll-spy highlight (pre-existing), the H1 cut at the 390 fold (pre-existing A-34), the local-BASE 114 B drift, the VM browser flake that killed the timing test. Nothing silent.

## What is NOT done

- **The merge.** The maker merges only after the captain's double-check. The branch is filed and ready; the merge itself is not done in this round.
- **The live route (Q2).** Where the Factory lives live on nayanet.app is Shawn's hand, not this lane's. This lane converges the file; it does not deploy it.
- **The phone-height variance.** Named and bounded, not cured. The foot-of-page rails rebuild's internals are A-24 territory for a later lane.
- **Gate (f).** The 18 pre-existing look-alike findings belong to a later lane; fixing them means renaming the page's own button classes, which this brief forbids.
- **The `syncPreview` #step5 no-op.** A-24 territory, later lane.
- **The timing test.** `timingtest.py` is written and kept in the probe dir; it could not run because the VM browsers died ~01:43Z. It is not a gate for this lane.

## Filing

Branch `factory/pi-align-l7-one-flow-20261111` — created from main HEAD `091961ba` (2026-11-13T01:35:24Z; the branch did not exist, 404 on first check). Filed to the branch, one PUT at a time, each read back and confirmed:

| File on the branch | Size | Blob (read back) | Commit |
|---|---|---|---|
| `TEAM-NITRO/factory-flow-fix4/factory-flow-fix4-20261111.html` (converged) | 759,814 B | `4f398992a5f85c887f0206c756311bbc2268ec6b` | `d87518ef` |
| `TEAM-NITRO/factory-pi-align/lane-l7-one-flow-scorecard.md` | 6,667 B | `c4140dd5a0bc174ac05fc2d42215f9cad7223401` | `bf007de2` |

This record was filed in three PUTs (first at 23,632 B, blob `58e80398…`, commit `a5f16b11`; then with the Round 3 findings; then with this Filing correction) — the bytes on the branch are the final text. A record cannot name its own final blob or the branch head truthfully, because naming them changes them; the final head and the final read-back are carried in the maker's DONE report to the captain, not here. The converged file's blob on the branch (`4f398992…`) matches the local converged file's git hash exactly, and that number does not move.

## Evidence files

- Brief: `~/workspace/team-nitro/factory-pi-align/lane-l7-one-flow-brief.md`
- Work dir: `~/workspace/team-nitro/factory-pi-align/` — record + scorecard here.
- Probe dir: `~/workspace/team-nitro/factory-pi-align/lane-l7-probe/` — `before-flow.html` (sha256 `dc901330…`, the true pre-edit bytes), `after-flow.html` (sha256 `78d83578…`, the converged file), `before.json`, `before2.json`, `after.json`, `before-mine.json`, `after-mine.json`, `navtest.json`, `make_l7.py`, `probe_l7.py`, `check_order.py`, `check_notif.py`, `navtest.py`, `timingtest.py` (written, not run — VM browsers dead), `shots-before/`, `shots-before2/`, `shots-after/`, `shots-mine-before/`, `shots-mine-after/`.
- On-disk FLOW file: `~/workspace/team-nitro/factory-flow-fix4-20261111/factory-flow-fix4-20261111.html` (now the converged file, sha256 `78d83578…`).
- On-disk BASE file: `~/workspace/team-nitro/factory-base-f-20261111/smartfactory-live-base.html` (untouched, sha256 `f9bfd25c…`, 580,186 B).

## Corrections after the captain's double-check (2026-11-13 ~02:42Z)

The captain's double-check PASSED with three record corrections, applied here before the merge. No page bytes changed — the converged file on the branch is untouched (blob `4f398992…`); only this record was corrected, and the corrected record is filed to the branch in its own PUT before the merge. The captain's cloud-browser click-proof (task a62da827, 02:36–02:42Z) corroborated: nav — all six pills clicked, each landed on its step with the pill active (CREATE landing matches the maker's gap 2407−2233=174) · cart — Select on NAYA-BTN-001 Black Ground (M) gave badge "1", "In cart ✓", panel "Black Ground / NAYA-BTN-001 · size M / ×1", persisted across reloads · VIEW on Personal jumped to "Template preview — two views" (MOBILE tab, nayanet.app/your-name) · structure — steps 1–6 in order, 13 railblocks in Step 5, contract S1–S13 all ✓, page ends at BUILD with no ~450px black void · Step 1 fields empty on fresh load.

1. **Rail-flip mechanism withdrawn (§Step 3, "Phone-width heights").** The sentence claiming the ejected railblocks are "dropped by the rebuild" is withdrawn as unproven: the rebuild IIFE (lines 4928–4962) works strictly inside each `.railblock` and cannot remove one. The flip itself (before @390: 11 vs 13 across runs) is real in the data; its cause stays open (A-24).
2. **Eye-jewel panels named (§Step 3, no-regressions).** The nine panels are the Step 1 eye-panels `eye-vision`, `eye-name`, `eye-title`, `eye-subtitle`, `eye-goal`, `eye-mission`, `eye-about`, `eye-soul`, `eye-photo` (lines 2394–2426), each a `.visioncard.elev-2.eye-panel` opened by its matching `data-panel` button — not the 21 JEWELS library cards (`NAYA-JWL-001`…`021`) and not "Orbital nine" (`NAYA-BRD-027`).
3. **BUILD guard condition + line stated (§Step 3, no-regressions).** The text is a JS string at line 4001 inside `startBuild()` (line 3999), behind `if(!document.querySelector('.tcard2.sel'))` (line 4000) — it shows only when no template is selected in Step 4, written into `#buildStatus` / `#sumStatus` by `setBuildStatus` (line 3998). In the click-proof the Personal template was already selected in the restored draft, so the guard was inactive and the text never entered the DOM — which is why the browser found no match; the checker verified the text identical statically.

### The seven pre-merge questions — re-answered after the corrections

1. **Three self-checks done?** Yes — Rounds 1–3 as written above, plus this fourth correction pass (record-only, each correction re-grounded in the converged file's own lines before editing). Each round found new things.
2. **Honest 9+?** Yes — still 9/10. The corrections change no score: they clarify the record, they change no page byte and no proof. The point off is still the phone-height variance and the pre-existing (f) gate FAIL, both named.
3. **Blast radius named?** Yes — one page file, `TEAM-NITRO/factory-flow-fix4/factory-flow-fix4-20261111.html`, plus the two lane docs already on the branch and this corrected record, on the lane branch only. The BASE file is untouched. No other file, no live route, no deploy. The merge, when it comes, replaces the FLOW file on main with the converged bytes and files the lane record as written here.
4. **Checks green?** The checks that belong to this lane are green: four probe runs + nav run, zero overflow, zero console errors, zero failed requests, all no-regressions passing, gate identical before/after — now corroborated by the captain's cloud-browser click-proof on the branch bytes (nav, cart, VIEW, structure, empty Step 1 fields, all by real clicks). The two browser non-confirmations are explained in the record, not hidden: the BUILD guard text was inactive because a template was already selected, and the eye-jewel count is the nine named Step 1 panels, not the JEWELS library cards. The one red item — gate (f), 18 pre-existing findings — fails identically on the before-file and is out of this lane's scope. The timing test (leg 4) was not run — the cloud browser cannot set 390px or read document height — and stays in the probe dir for the next lane; overflow/console at 1440/390/360 were not measurable in the cloud browser and stay as the checker's priced gap.
5. **Five gates?** Yes — unchanged, all five yes (see above). The corrections touch the record only; nothing in them re-opens a gate.
6. **Real proof?** Yes — strengthened since the first answers: the click-proof ran real clicks against the converged branch bytes on the proof host and landed every leg it could run. No claim without a measurement.
7. **No silent known defects?** Yes — every known defect is named in this record, and the three statements the captain found imprecise are now corrected in place above. The rail-flip cause stays open (A-24), named, not silent. Nothing silent.
