# Factory Base (f) — Maker Record (2026-11-11)

Maker: Factory base-(f) seat, under captain Naya Nitro Narzan.
Brief: `~/workspace/team-nitro/factory-base-f-20261111/BRIEF.md` (checker 9/9 PASS).
Branch: `factory/base-f-20261111`, repo SoulSchoolAcademy/NayaPOWER.
Base: live Factory page bytes, fetched live from nayanet.app/smartfactory,
580,186 bytes, sha256 `f9bfd25cade628709e5c90da23d2d9c9a20a476faf776f08b3a33c091c2d0784`.

## VERDICT: OVERALL PASS (static) — gate (f) 0/0, no other gate worse than baseline; rendered legs QUEUED (browsers dead)

## 1. REPRODUCED BASELINE (maker's own measurement, before editing)
- Gate (f) on the live base: look-alike buttons **443** / gold CTAs **3** (brief says 443 / 3 — reproduced, not trusted). Breakdown reproduced: 437 classed + 6 bare, 49 distinct class-sets, attribute-addressed 2.
- Full gate (a)–(i) on the live base (in-memory via imported check-gate.py):
  (a) PASS (0 light surfaces) · (b) PASS (0.976, 41 missing depth) · (c) **FAIL** (no gauge mount, no needle, 0 teeth — pre-existing) · (d) PASS (0 text-in-image, 2 imgs) · (e) PASS (0.868, 27 bare) · (f) **FAIL** (443 / 3) · (h) PASS (0 banned) · (i) PASS (0 story boards, n/a).

## 2. THE FIX (per class-set: cite with verified source, or re-class)
- Harvest-sources file: `~/workspace/team-nitro/factory-base-f-20261111/harvest-sources.txt` — **25 citations**, all verified line-by-line (see below).
- **v2 (final): 9 tag edits only.** 3 gold re-themes + 6 bare buttons gain `primo-btn`. All 437 classed buttons are left UNTOUCHED — excused by genuine citations (437 harvest-excused in the gate run).
- Re-themed gold CTAs (all → `theme-purple`, the page's signature harvested theme, precedent: the one-click round's CREATE button `primo theme-purple elev-2`):
  - line 2438 — piece-card demo `primo theme-gold elev-2` "Gold" (NAYA-BTN-008 Primo Gold) → `primo theme-purple elev-2`
  - line 3718 — `#buildBtn` `primo theme-gold elev-3` "★ BUILD APP — DRAFT MY CONTRACT" (Step 5) → `primo theme-purple elev-3`
  - line 3757 — cart drawer `primo theme-gold elev-2` "★ BUILD APP" (clicks buildBtn) → `primo theme-purple elev-2`
  - The gold rim of the calculator gauge is untouched; the `.theme-gold` CSS definition itself stays (1 remaining occurrence) — only the 3 buttons changed theme. The piece card keeps its name "Primo Gold".
- Bare buttons (6 — the only `primo-btn` uses): line 3439 voice tabs Human / Naya / Machine (role="tab") and line 3597 nav Today / Reports / Spaces — each gained `class="primo-btn"`. No class to cite, so the brief's re-class method applies; `primo-btn` has 0 occurrences in the base (no CSS, no JS, no uses), so look and wiring cannot change.
- Re-classed buttons: none besides the 6 bare — every classed button was cited, not re-classed.
- Base bytes preserved: reconstruction check — reversing all 9 edits on the edited file returns the base byte-identical. All 13 script blocks and all 5 style blocks byte-identical. Class-token diff base→edited is exactly `{primo-btn: +6, theme-gold: −3, theme-purple: +3}`. Card mentions 376 / 376.

### The citations (25) — and how each was verified
- **Factory stylesheet** `~/workspace/personal-app/factory.css` (2026-10-21, 171 KB, 1017 rules) — the shared Factory CSS library. Provenance, three independent evidences: (1) the live page's own `<style id="factory-sync-css">` comment (SYNC-ADDED 2026-11-08) names it "Source:" for rules the page copied; (2) the Hub (`~/workspace/user/files/index-2.html:2706`) treats it as the definition source for naya-btn foundation variants; (3) the file predates the page sync (Oct 21 vs Nov 8), and cited rules are byte-identical to the page's copies where compared (btn-select, tview, eco-bb-btn, bh-btn).
  - `.btn-select` :1282-1283 · `.btn-notes` :1282-1283 · `.tview` :1328-1329 · `.steppill` :432 · `.day-dot` :1481-1484 · `.naya-btn` :545-569 · `.living-btn` :475-490 · `.cx-btn` :531-533 · `.naya-toggle` :1525-1528 · `.smarttab` :1802-1803 · `.vtog` :160-162 · `.tgl` :1187-1188 · `.sn-btn` :1190-1192 · `.btn-chrome` :1411-1414 · `.orbit-btn` :784-787 · `.like-pill` :1472-1475 · `.act-chip` :1478-1480 · `.send-cta` :1485-1488 · `.mic-btn` :1489-1492 · `.fab` :1494-1496 · `.ref-select-btn` :1890-1899 · `.naya-brand` :1733-1736 · `.sumbtn` :1371-1372
- **Hub board** `~/workspace/user/files/index-2.html`:
  - `.eco-bb-btn` :284-339 — defines the part; Hub JS line 6865 creates it as an anchor (`a.className='eco-bb-btn'`); the Factory's 18 are anchors too, same CSS verbatim. (18 buttons)
  - `.bh-btn` :8959 — defines `.board-h .bh-btn`; Hub JS 8896/9139 creates `<button class="bh-btn">` inside `.board-h`; the Factory's 8 sit inside `.board-h`, scoped rule governs by specificity. (8 buttons)
- **Refused citations (the cite path was policed, not rubber-stamped):** Hub defines NONE of btn-select, btn-notes, tview, naya-btn, steppill, day-dot, smarttab (Hub grep); THE-INVENTORY.md and CANONICAL-PIECE-INDEX.md define none of them either. Hub's `.tab-pop .tgl` (index-2.html:1118-1123) was NOT cited for the Factory's tgl button — different context (tab-pop toggle vs the Factory's "Live" piece-card toggle); the Factory's tgl traces to factory.css:1187 instead.
- **JS check:** no class was renamed or removed (class-token diff proves it: only +6/−3/+3). The 13 script blocks are byte-identical, so no JS selector can have broken. `primo-btn` occurs 0 times in the base — no JS references the added class. The edit script cross-checked its own tag scanner against the gate's parser element-by-element (tag, line, classes) before editing.

### v1 → v2 (honest history — nothing hidden)
- **v1** was built and filed first: 420 edits — all 437 classed buttons gained `primo-btn` (vehicle), 6 bare + 3 gold. It gated (f) 0/0 (page blob `eeaa521c00843381fea7797bb4360ac7b6d4442b`, commit `b4b7ccbd67f3d6e882dbf91aff9cea7ef4aeed71`; harvest blob `1364ada9…`, human-checks blob `63476750…`, build-script blob `7b279361…`). Then `~/workspace/personal-app/factory.css` was found and verified as a genuine source, so v1 was superseded by v2 (real citations, 9 edits). The v1 commits stay in branch history; the v2 files are the current tip.

## 3. GATE — RE-RUN ON THE EDITED FILE (v2, with --harvest-sources)
- (f): look-alike buttons **0** / gold CTAs **0** · harvest-excused **437** · attribute-addressed 2.
- Full gate (a)–(i) on the edited file: (a) PASS · (b) PASS (0.976, 41 missing — identical) · (c) **FAIL** (identical to baseline: no gauge — pre-existing base debt, owned by the one-click branch, fixed when the branches merge) · (d) PASS · (e) PASS (0.868, 27 bare — identical) · (f) **PASS** (0/0) · (h) PASS (0) · (i) PASS (0 boards, n/a).
- No other gate is worse than baseline on any letter. H1–H5: all PASS (source-level; file on branch).
- No-regressions: 158 cards — card mentions 376 / 376 · Factory page still works — 13 script blocks + 5 style blocks byte-identical, no JS touched, no class renamed/removed.

## 4. SELF-SCORECARD (three-step verification, step 1 — the maker scores their own work first)
**Construction score: 9/10. Round score: 9/10** (held back only by queued rendered verification and the pre-existing (c) FAIL — neither fixable by the maker alone).
- Why it is not a 10 (every reason): (1) never seen rendered — browsers dead, so the purple re-theme is proven static-only; (2) (c) still FAILs on the bare base (pre-existing, owned by the one-click branch); (3) the 6 bare buttons still use the primo-btn vehicle (no class to cite — unavoidable, and the brief's own method); (4) factory.css direction-of-copy is not provable rule-by-rule (some rules may have been extracted from an earlier Factory page into factory.css — the file is still the workspace's canonical shared stylesheet, the page names it Source, and the brief's test is met, but a strict verifier could debate it); (5) citation paths are workspace-local (`~/workspace/...`), not repo paths — durable in this workspace only.
- 10 things I love: (1) true EDIT — 9 tag edits, base byte-identical under reversal; (2) (f) 443/3 → 0/0 with 437 REAL citations, not labels; (3) the factory.css find — the page's own "Source:" comment turned a thin vehicle fix into a real-pedigree fix; (4) zero visual change except the 3 ordered re-themes (token diff proves it); (5) zero JS/CSS/text touched (13 script + 5 style blocks byte-identical); (6) two refused citations (Hub .tab-pop .tgl; Hub for btn-select etc.) — the cite path was policed, not rubber-stamped; (7) deterministic rebuild reproduced the sha exactly across runs and across v1→v2; (8) read-back + proof-host both sha-MATCH; (9) v1 was filed, then superseded transparently (history shows the improvement, nothing hidden); (10) the build script is on the branch — the verifier can reproduce everything.
- 10 things I don't love: (1) no rendered proof; (2) (c) still red on the bare base; (3) 6 bare buttons still vehicle-labeled; (4) factory.css direction-of-copy not provable rule-by-rule; (5) workspace-local citation paths; (6) the Primo Gold demo button is now purple while the piece is named Gold; (7) v1's 4 commits are superseded history (noise on the branch); (8) the full-gate in-memory run skips check_file's <link> stylesheet leg; (9) one duplicate exec + one service restart mid-task (my double-send); (10) the local base file was 0 bytes until the EPERM flake cleared (now filled: 580,186 bytes, sha verified).
- 10 things to make it 10x better: (1) rendered verification 390/1440/360 with screenshots; (2) live tap-through of buildBtn + cart BUILD APP after re-theme; (3) merge with the one-click branch so (c)+(f) close together (captain's call); (4) move factory.css into the repo and re-point citations to repo paths; (5) a rendered before/after pixel-diff to prove "same look" by eye; (6) gate-side provenance check for harvest sources (file date vs page sync date); (7) give the 6 bare buttons real ids/data-* hooks from their roles instead of a vehicle class; (8) rename the Primo Gold piece or keep a gold demo exempt — needs Shawn's eye, not mine; (9) single-pass atomic filing (page+record together); (10) a faster reconstruction check in the gate tooling (difflib crawls on 580KB).
- 10 solutions applied right now: (1) gold-before-harvested ordering fix in the edit (F2 fires regardless of pedigree — caught by the tally assertion); (2) O(n) reversal reconstruction replacing the crawling difflib check (it killed a run at 216s); (3) vehicle zero-footprint proof before use (`.btn` ruled out — it IS styled in-page); (4) both Hub citations verified line-by-line (CSS + JS use + tag context); (5) Hub .tab-pop .tgl citation REFUSED on context; (6) factory.css provenance established from three independent evidences (page's "Source:" comment, Hub reference, Oct 21 predating file) with every cited line verified; (7) tag scanner cross-checked against the gate's own parser element-by-element; (8) script/style blocks asserted byte-identical + exact class-token diff; (9) deterministic rebuild asserted before each filing; (10) branch created from the reconciled main tip 63eb1d80, branch named on every PUT (never --file without a branch), read-back + proof-host sha-MATCH on both versions.

## 5. FILING (v2 = current tip; v1 superseded, see §2)
- Edited file blob: `983d67267aa28e40a6d5238f74badf91234bcee0` (580,300 bytes, sha256 `105a559f950a9215229a66931db71cda37c6043cedb8eaeea7839531d426655e`).
- Harvest-sources blob: `955e641a3d18fd3ceb7f627a29ca5230e26d0a44`.
- Human-checks blob: `736e04bcae545bdb352ee3e5638546b50a289fc9`.
- Build-script blob: `ce5388f15b9cfc743e2412378270291f378843ac`.
- Record blob: (filled after filing — see report).
- Branch tip commit: `7f9dc4c7e3011d625eaea2b412ba00d367cf4f08` (before the record file).
- Staged link: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/factory-base-f-20261111/smartfactory-base-f-20261111.html&ref=factory/base-f-20261111&cb=983d67267aa28e40a6d5238f74badf91234bcee0 — HTTP 200, 580,300 bytes served, sha256 MATCH.
- v1 (superseded): page blob `eeaa521c00843381fea7797bb4360ac7b6d4442b`, commit `b4b7ccbd67f3d6e882dbf91aff9cea7ef4aeed71` (420 edits, sha `0231672370ba41b5ab73d7419cc7c845af06854dc9fa98c6c677a3805bb7df36`).

## 6. NOT-DONE (honest list)
- Rendered verification QUEUED (browsers dead — cause proven, probe cron every 15 min). No screenshot, no live tap-through, no pixel-diff. The verifier runs the rendered legs the moment a browser launches.
- (c) on the bare base: FAIL, pre-existing, owned by the one-click branch (fixes it when the branches merge — captain's call).
- The Primo Gold piece (line 2438) now shows a purple button while keeping its name — Shawn's eye decides whether that stands.
- No merge, no deploy, no PR opened by the maker. The smart note for this work (brief §verification) is NOT filed in this record — the coordinator owns the note + feed step.
- Local copies: `~/workspace/team-nitro/factory-base-f-20261111/` holds BRIEF.md, RECORD.md (this file), harvest-sources.txt, human-checks-base-f-20261111.txt, build-f.py, and smartfactory-live-base.html (580,186 bytes, sha verified after the EPERM flake cleared).

## VERIFIER'S EXACT LIVE CHECKLIST (different seat — never the maker)
Staged link above. Playwright (or real browser) at **390 + 1440 (+360)**, scroll 0 AND scrolled, **zero console errors**, zero horizontal overflow.
1. Open the staged link: the Factory page renders whole — 158 piece cards present; scroll 0 shows the step rail; scrolled shows the cards, the eco bar, Step 5.
2. The 3 re-themed buttons render purple (not gold): the "Gold" demo button in the Primo Gold card (~line 2438), Step-5 BUILD APP (~line 3718), cart-drawer BUILD APP (~line 3757). Click Step-5 BUILD APP → contract drafts exactly as on the live page; click the cart BUILD APP → it clicks buildBtn and closes the drawer.
3. The 6 bare buttons work: voice tabs Human/Naya/Machine switch; nav Today/Reports/Spaces navigate.
4. No-regressions: every Select / Notes / View button on the cards still works (they keep their original classes + JS); the Hub drawer still opens; Step-5 contract + build flow untouched.
5. Gate: re-run `design-contract-gate/check-gate.py --harvest-sources harvest-sources.txt` on the staged file — confirm (f) is 0 look-alikes / 0 gold CTAs, (c) still FAIL (pre-existing, one-click branch's), every other letter identical to the live baseline. Check every citation against its source file + lines (factory.css + Hub), and confirm no class was renamed (class-token diff vs live base is only primo-btn +6, theme-gold −3, theme-purple +3).
6. Report DONE + NOT-DONE to the captain only. A NOT PASS goes back to the seats, never to Shawn's eyes.

## ENVIRONMENT NOTES (for the next seat)
- EPERM flake was ACTIVE during the build: 580 KB shell redirects failed (curl exit 23) and the local base file sat at 0 bytes; small writes worked. The whole build ran in memory (fetch → edit → gate → file via in-process GitHub API, token minted via imported `gh-direct.py`); the local base file was filled only after the flake cleared.
- `urllib` fetch of the live page hits `IncompleteRead` on chunked encoding; `curl | python` (pipe, no disk) is the reliable fetch.
- Contents API omits base64 > 1 MB on GET — read-back was done via `GET /git/blobs/{full-sha}`.
- `difflib.SequenceMatcher` crawls on 580 KB texts (a run sat 216 s with no output) — the reconstruction check reverses the recorded edits instead (O(n)).
- Branch `factory/base-f-20261111` did NOT exist at dispatch — the maker created it from the reconciled main tip `63eb1d80262db76926dbb94278c66857e8daa219` via `POST /git/refs`. Every PUT named the branch explicitly in the body — never --file mode without a branch.
