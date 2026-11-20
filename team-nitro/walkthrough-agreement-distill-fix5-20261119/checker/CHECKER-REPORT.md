# INDEPENDENT CHECKER — Agreement distill fix-5

**Branch:** `walkthrough/agreement-distill-fix5-20261119`
**Tip verified:** `f38e63402823ef884e439a9ed6e4550a7f2e296a` ("Agreement distill fix-5: file the filing verification")
**Chain (git API):** `f38e6340` (filing commit) → `b048f00269f61c821812f06ffe6bd8e96cf29d4b` ("Agreement distill fix-5: footer links reachable at 390 (F)") → `d5003b2f` (fix-4 tip). The tip is a filing commit on top of the fix commit; the fix commit's parent is the fix-4 tip, as the coordinator stated.
**Staged:** https://naya-walk-beginning-staging.nayapower.workers.dev/ — verified serving fix-5 bytes on all four routes (curl shas) and by a live browser geometry sweep on the staged bridge (0 unreachable links).
**Checker:** independent, cold. I did not build this. All measurements below are my own drivers, my own screenshots, my own rects — the maker's probe logs were read only after my own runs, and only to compare.
**Browser:** Playwright Firefox 157.0 in this VM, real taps, 390×844 first, then 1920×1080. Firefox was alive for every leg (re-tested before the drive; it never died in this round). Local servers served base (fix-4 tip) bytes on :18095 and fix-5 bytes on :18096 — same pages, same harness, both sides.
**No merge, no live deploy, no message to the user.**

## VERDICT: PASS

The fix-4 checker's go-back is answered in full. Defect F is fixed on both footer strips at 390 — all 12 links are reachable on the bridge (proven by real tap through the full citizen flow) and on the intro strip (proven through the page's own stage render; see §F-intro for the honest limit on the citizen click-path). Desktop 1920 is byte-identical in geometry. F9 passes at 390 and 1920. Defects A–E still hold, re-measured. Laws delta 0.

| Item | Verdict |
|---|---|
| F — footer links reachable at 390 (bridge) | **PASS** (12/12 reachable; was 7/12 on base) |
| F — intro strip | **PASS** (12/12 reachable on the real intro render; see the activation note) |
| Desktop 1920 regression | **PASS** (row still centred, 87px symmetric margins, no overflow) |
| F9 regression (390 + 1920) | **PASS** (unfold/deck/letter 1→37 sequential, bridge pair both ways, 0 console errors) |
| A–E re-check | **PASS** (all re-measured; numbers match fix-4) |
| Laws delta | **PASS** (0 on every file) |

## 1. BYTE VERIFICATION — all six files match

Fresh git blob-API reads (via `gh-direct.py`, never the contents API) against the branch tip. Sizes, sha256, and git blob shas all equal the maker's table. Log: `checker/work/blob-verify.json`.

| File | Bytes | sha256 (first 16) | Blob | Match |
|---|---|---|---|---|
| agreement-unfold-fixed.html | 142,532 | a3b3907f2f80d09a | 1f0b04747e3315be6… | ✓ |
| welcome-staged.html | 1,930,947 | 57ebe2d295b494eb | 00082c3d65801997f… | ✓ |
| walk-beginning-fixed.html | 4,363,683 | 856d392c439ebb5c | 2f7a5e3ef599e00c… | ✓ |
| identity-fixed.html | 404,147 | fef65d2cdbf2f1e8 | b3e5af088ef1d516… | ✓ |
| walk-beginning-staging-worker.js | 8,463,055 | c9bc8fedcbad3299 | 0413500982bc14df… | ✓ |
| build-v23-staging-worker.py | 96,371 | 7ce1a895051cd6e4 | 2299b99155e44225… | ✓ |

Staging curl after the maker's PUT (browser UA): `/` → `57ebe2d2…` (1,930,947 B), `/identity.html` → `fef65d2c…` (404,147 B), `/welcome` → `856d392c…` (4,363,683 B), `/agreement` → `a3b3907f…` (142,532 B). The staged host serves fix-5 bytes on every route.

## 2. SCOPE — the diff is exactly the two `safe center` values

I replayed the diff myself against the fix-4 tip files (not the maker's word). Proof: `checker/work/scope-proof.json`.

- **welcome-staged.html:** `safe center` occurs exactly 2× (0 on fix-4); `justify-content:center` falls 37 → 35. Undoing the two values reproduces the fix-4 file **byte-identically** (reconstruction: true). The two rules are the nowrap `.fp-legal-links` rules, intro (`html.fp-locked body.fp-stage-on.fp-intro #fpLegal .fp-legal-links{display:flex;flex-wrap:nowrap;overflow-x:auto;justify-content:safe center;gap:2px 20px;…}`) and bridge (same, `fp-bridge`). Byte delta +10.
- **walk-beginning-staging-worker.js:** `safe center` 3 → 5 (the two new ones plus the three pre-existing: `.naya-tabs` and the two `.sa-theatre-body` occurrences). Scoped reconstruction (reverting only the two `.fp-legal-links` rules) reproduces the fix-4 worker **byte-identically**. A naive global revert does NOT reproduce it — it would also revert the two pre-existing `.sa-theatre-body` `safe center` values, which is a property of my proof, not a worker diff; the aligned char-diff shows exactly two changed regions, both `center` → `safe center` in the `.fp-legal-links` rules. Byte delta +10.
- **build-v23-staging-worker.py:** +556 B. Seven asserts in both files; only assert #3 changed (welcome `237af4d4` → `57ebe2d2`), plus an 8-line FIX5 comment block. The other six asserts are byte-identical. No logic change.
- **agreement-unfold-fixed.html, walk-beginning-fixed.html, identity-fixed.html:** byte-identical to fix-4. **No change to F9 code, no desktop rule, no board content, no anthem/Listen wiring, no certificate logic.** The compare API (`d5003b2f...f38e6340`) confirms only these three files changed plus the maker report and work scripts.
- Scope check: **PASS.** Nothing else changed; nothing unasked was touched.

## 3. DEFECT F AT 390×844 — PASS

Method: my own driver (`checker/work/checker-drive1.py`, `checker-drive1b.py`), 50px sweep steps plus the max, against base bytes (:18095) and fix-5 bytes (:18096), then staged. Reachability = a link's rect fully inside the viewport [0,390] at some `scrollLeft`; I also checked the stricter strip-viewport criterion (fully inside the strip's own rect [8,382]) — both agree on every link.

### Base reproduced exactly (fix-4 tip bytes)

- Strip: `scrollWidth 1064`, `clientWidth 374`, `maxScroll 690`, `justify-content: center`, `nowrap`.
- At `scrollLeft = 0`: Terms `[-678,-548]`, Privacy `[-528,-415]`, Cookie `[-395,-286]`, Refund `[-266,-153]`, Acceptable Use `[-133,-10]` — **5 of 12 unreachable at every scrollLeft** (viewport and strip criteria agree). At max scroll Terms is at `[-1368,-1238]`. Screenshot `ck5-base-F-bridge-s0.png` opens on "Community Guidelines / Copyright / DMCA / A…" — Terms nowhere.
- My base rects are identical to the fix-4 checker's, to the pixel.

### Fixed (local fix-5 bytes, bridge — real tap: /agreement → 1→37 → "I agree" → bridge)

- Strip: `scrollWidth 1754` (the true content width is now exposed), `clientWidth 374`, `maxScroll 1380`, `justify-content: safe center`, `nowrap`.
- **All 12 links reachable, 0 unreachable (both criteria):**

| Link | First fully inside |
|---|---|
| Terms of Service | scrollLeft 0 — [12,142] at load |
| Privacy Policy | scrollLeft 0 — [162,275] |
| Cookie Policy | scrollLeft 50 |
| Refund Policy | scrollLeft 150 |
| Acceptable Use | scrollLeft 300 |
| Community Guidelines | scrollLeft 500 |
| Copyright / DMCA | scrollLeft 650 |
| Ambassador Terms | scrollLeft 850 |
| Membership & Billing | scrollLeft 1000 |
| Young Citizens | scrollLeft 1150 |
| Accessibility | scrollLeft 1300 |
| Disclaimer | scrollLeft 1380 (max) — [285,378] |

- At `scrollLeft = 0` the strip opens on "Terms of Service / Privacy Policy / Cookie Polic…" (screenshot `ck5-fix-F-bridge-s0.png`). At max scroll it ends on "Young Citizens / Accessibility / Disclaimer", all whole (`ck5-fix-F-bridge-smax.png`). 0 console errors.
- The reachability scroll positions match the maker's within my finer 50px step granularity (their 100px steps: Cookie 100, Refund 200; mine: 50, 150 — same links, earlier first-fully-inside points).

### Staged (live host, real tap)

- Same walk on https://naya-walk-beginning-staging.nayapower.workers.dev/agreement → agree → bridge: `scrollWidth 1754`, `maxScroll 1380`, `safe center`, **unreachable 0**, Terms `[12,142]` at scrollLeft 0 (screenshot `ck5-staged-bridge-s0.png`). 0 console errors.
- Note (honest): my first staged leg returned "no nav" — the bridge stage JS had not rendered `#fpLegal` within the 2500ms wait on the remote host. The re-run with a 5000ms wait and full diagnostics (`checker/work/checker-drive3b.py`) passes cleanly: after agree, URL `/?stage=bridge`, body `fp-stage-on fp-bridge fp-dialed`, `#fpLegal` display block. The first failure was my wait, not the page.

### Desktop 1920 — no regression

- Fix-5 bridge: `scrollWidth == clientWidth == 1904` (no overflow), `safe center`, first link left 87, last link right 1833 — symmetric 87px margins.
- Base bridge at 1920: identical link-for-link (first left 87, last right 1833, `scrollWidth == clientWidth == 1904`) — only the `justify-content` string differs (`center` vs `safe center`). Screenshot `ck5-1920-bridge.png`: all 12 links in one centred row. **Desktop unchanged.**

### F, intro strip — PASS, with the activation record stated plainly

The maker's one unproven item was the intro strip: `#fpLegal` is `display:none` on a cold `/` load and `?stage=intro` does not activate it. I tried to activate it, in this order:

1. **Cold `/`:** `#fpLegal` `display:none`; visible buttons are "Enter NayaNET →" (the login name form) and "Read the collective agreement ◆" (`#fpEnterDeal`, which navigates to `/agreement`). Confirmed.
2. **`?stage=intro`:** identical to cold — `display:none`. The boot only calls `enterStage()` for `deck`/`letter`/`bridge`. Confirmed, as the maker reported.
3. **Login name form → Enter:** submitting `#entryForm` with a name navigates to `/identity.html?name=…` (the certificate page), not the stage. With a name only, `#enterBtn` (ENTER) on identity does nothing visible — the page stays on identity. (My first intro screenshots, `ck5-intro-s0/smax.png`, were taken on that identity page; I deleted them rather than leave mislabelled evidence.)
4. **Bounded full walk (identity paired → ENTER → door → step-1):** the walk is 14 numbered steps + names + building + end; my bounded attempt (20 clicks) reached step-1 and stopped on the per-step controls. The walk's end offers only `/?stage=deck` and `/?stage=letter` links — never intro. "Jump back in" on the login goes to `/hub`, not the stage.
5. **Diagnostic activation — the one that worked:** on a cold `/` load, the page exposes `window.__fpStage.enter()` (the same `enterStage()` the `?stage=` hook and the agree/bridge-agreed restores call). Calling it renders the real intro view through the real `render()` path: body `fp-stage-on fp-intro fp-dialed`, `#fpLegal` display `block`, the choice pills ("Begin the visual story" / "Read the agreement") visible.

On that real intro render, my geometry sweep (`checker/work/checker-drive1b.py`, log `checker-log-intro.json`) gives: `scrollWidth 1754`, `clientWidth 374`, `maxScroll 1380`, `justify-content: safe center`, **all 12 links reachable, unreachable 0** — Terms `[12,142]` at scrollLeft 0, Disclaimer `[285,378]` at max, identical numbers to the bridge. Screenshots `ck5-intro-diag-s0.png` / `ck5-intro-diag-smax.png` show the choice view with the strip opening on Terms.

**Judgment:** I did not reach the intro strip through a citizen click, because no citizen click in the filed bytes opens the intro view directly (the walk end offers deck/letter only; the login offers the unfold; the restores land on agree/bridge). I do not pretend otherwise. I judge the intro fix sufficient on three legs: (a) the intro rule is the identical one-value change on the identical rule shape as the bridge rule, in the same file; (b) the bridge strip — the same strip, same widths, same trap — is proven end-to-end by real tap; (c) the intro strip itself is geometry-proven on the real render path through the page's own stage entry. If the eye wants the intro reached by click, that is a flow question for a later round, not a defect in this fix.

## 4. F9 REGRESSION — 390 and 1920, fixed bytes

All by real tap. (The fix-3 state machine 139/139 was not re-run; the live probes below cover the same F9 surface at both widths.)

| Check | 390 | 1920 | Result |
|---|---|---|---|
| Identity paired `?name=Shawn&alias=Shawn` | input `shawn`, hero `Shawn`, `data-text="Shawn"`, shown | same (hero `[500,388,1420,472]`, matching fix-4) | ✓ |
| Identity name-only `?name=Shawn` | input empty, hero empty/hidden | — (390 only) | ✓ |
| Identity plain (no params) | hero hidden; "This certifies that" shows (`[133,294,257,314]`) | — (390 only) | ✓ |
| Door holds 10 s untouched | still `["step-door"]` after 10 s | still `["step-door"]` after 10 s | ✓ |
| Continue → step-1 | `["step-1"]` after tap | `["step-1"]` after tap | ✓ |
| Unfold 1→37 by real tap | sequential 1/37…37/37 (stabilized sampler; see note) | board 37 title 25px, "Congratulations — you're hired" whole | ✓ |
| Deck 1→37 → bridge | sequential 37/37; "Enter NayaNET ◆" → bridge, pair shows | — (390 only) | ✓ |
| Letter 1→37 → bridge | sequential 37/37; "I agree ◆" → bridge, AGREED marker true | — (390 only) | ✓ |
| Bridge pair both ways | "Begin the visual story" → deck 1/37; "Read the agreement" → `/agreement` 1/37 (one context) | — (390 only) | ✓ |
| Console errors | 0 `pageerror` / console errors on every fixed leg | 0 on the desktop leg | ✓ |

**Unfold sampler note (honest):** my first two unfold walks recorded gaps (count 35, then nulls at transition boards). That was my sampler catching the counter mid-transition — the counter text is briefly absent during the slide animation, so a 150ms poll reads `null` and a fast transition skips a sample. It is not a skipped board: the re-run with a stabilize-wait (`checker/work/checker-drive2c.py`) records all 37 counters sequential, 1/37…37/37, and the deck/letter walks are sequential 37/37 on the first pass. The unfold code is byte-identical to fix-4b, where sequential was proven by the fix-4 checker and the maker.

## 5. DEFECTS A–E RE-CHECK — all still hold

Re-measured on fix-5 bytes at 390 with my own probes (`checker/work/checker-drive2.py`, `checker-drive2b.py`). Every number matches the fix-4 checker's fix-4b measurement.

| Defect | Re-measure (fix-5) | Verdict |
|---|---|---|
| A — hero name covers certificate title | Name 28.0625px `[19,301,371,329]`; title `[22,282,368,299]`; **overlap 0; gap 2px**; `.cert-certifies` `display:none` in the taken state | **PASS** (unchanged; the 2px gap reads clean, as fix-4 accepted) |
| B — door heading behind corner jewels | Padding 80px/80px; heading 4 lines x127–263; **crest overlap 0 on all 4 lines** | **PASS** |
| C — "already claimed" banner clipped | Banner 5 lines x103–287; **line-vs-crest overlap 0 on all 5**; frame stone `display:none`; stone overlap 0 | **PASS** |
| D — "Congratulations" under orb / photo | Unfold: title 22px, line 1 ends x217, orb `.frame-icon` starts x238 — **21px clear**. Deck: title 22px, line 1 ends x234, face photo starts x274 — **40px clear**. Letter: visible title **24px** (not 22px — the fix-4 correction stands), lines end x274, face photo starts x274 — **0px, touching, not overlapping** | **PASS** (see note) |
| E — deck photo covers text-box last lines | Deck nutshell `[30,232,300,500]` vs photo `[72,509,258,695]` — **overlap 0 (9px clear)**. Letter nutshell vs photo **overlap 0** | **PASS** |

**D letter note:** the letter's visible title line 1 ends exactly at the photo's left edge (x274 = x274). That is the pre-existing state — 24px on base and on fix-5, byte-identical, measured identically by the fix-4 checker, who passed it. Touching at the boundary, not covered; the screenshot (`ck5-fix-letter37.png`) shows the letter end state reading clean. It is not a fix-5 regression and not a go-back item; it is named here so the 0px is on the record. (My first D probe used a bare `.frame-icon` / `.fp-speak-face` selector that hit zero-rect hidden copies; the re-probe with visible-only elements gives the numbers above — the orb `[238,75,290,127]`, the deck face `[274,146,338,210]`, the letter face `[274,204,338,268]`.)

**Pre-existing caption nick (fix-4 flag (d)) — confirmed unchanged:** the sign photo still nicks the top of the "· NayaNET · The Deck" caption on deck 37 (visible in `ck5-fix-E-deck37.png`). Byte-identical files, out of scope, not a regression.

**Desktop 1920 note:** my unfold board-37 title rect at 1920 is `[516,122,1236,152]` (25px) — the block-level title element, wider than the fix-4 checker's `[691,121,1061,153]`. The screenshot (`ck5-1920-unfold37.png`) shows "Congratulations — you're hired" whole, centred, clear of orb and photo. The rect difference is which title copy the selector lands on; the reading is what matters, and it reads whole.

## 6. LAWS — §11 check in writing + checker delta

`check-design-laws.py` run on each changed file, base (fix-4) vs fix-5 (my own runs; outputs `checker/work/laws-base-welcome.txt` / `laws-fix5-welcome.txt` — line-for-line identical apart from the filename prefix):

| File | Base FAIL / WARN | Fix-5 FAIL / WARN | Delta |
|---|---|---|---|
| welcome-staged.html | 83 / 4 | 83 / 4 | 0 |
| walk-beginning-staging-worker.js | 829 / 154 | 829 / 154 | 0 |
| agreement-unfold-fixed.html | 1 / 2 | 1 / 2 | 0 |
| walk-beginning-fixed.html | 128 / 8 | 128 / 8 | 0 |
| identity-fixed.html | 11 / 2 | 11 / 2 | 0 |

The FAILs are pre-existing checker noise (sub-17px fonts throughout the base files; the word "gray" inside comments). None introduced by this round. Delta 0 on every file.

**§11 check, in writing:**
- **Five gates:** (1) Right — the round restores five unreachable legal links to the citizen reading at phone width; nothing harmful. (2) Truly needed — the fix-4 checker's go-back named exactly this defect with measured rects. (3) Mine to do — this check is verification only; no merge, no deploy, no message to the user. (4) Now — the round is staged and the staged host is proven to serve it. (5) Prove it — every claim above carries a measured rect, a log line, or a screenshot I took myself.
- **Real objects, one light, elevation, alive on hover:** untouched by this round — no element restyled, only the alignment of one strip. Pass.
- **Type 25/19/17, no grey text:** no text size or colour changed anywhere; the footer links keep their 13px size (pre-existing, counted in the 83 — out of scope for this round, which is charged with reachability only). The 22px board-37 deviation from fix-4 stands as accepted. Pass.
- **Harvest first, compose never create:** the fix edits the file's existing strip rules; nothing rebuilt, nothing redesigned, no new page, no new element. Pass.
- **Don't remove/move what he didn't ask to touch:** desktop rules untouched (1920 geometry proves it link-for-link); F9 code untouched; defects A–E untouched (all re-proven above). Pass.
- **Read as a reader:** I walked the whole flow top to bottom at 390 as a citizen would — identity, door, unfold 1→37, deck, letter, bridge — and read every screenshot I took. The footer strip now opens on "Terms of Service" and ends on "Disclaimer", all whole, at both ends of the scroll, on the bridge and on the intro choice view and on the staged host. A citizen swiping the strip reaches every link: the strip scrolls smoothly from Terms to Disclaimer with no dead zone and no link left behind the left edge. It reads clean.
- **Button destinations double-checked:** every button on the walk lands where it should — unfold → bridge, deck → bridge, letter → bridge, door Continue → step-1, pair → deck/agreement, "Read the collective agreement" → `/agreement`. No dead ends, no stale pages. Pass.
- **Phone first:** proven phone-first at 390, desktop confirmed unchanged at 1920. Pass.

**Scorecard (honest):** the page is a 10 on the F acceptance as written — all 12 links reachable on both strips, desktop unchanged, F9 intact, A–E holding, laws delta 0. The remaining known pre-existing items (the 83 laws-checker FAILs, the deck caption nick, the letter title's 0px touch, the missing apple-touch-icon) are unchanged from fix-4b and out of this round's scope.

## 7. WHAT WAS NOT PROVEN / OPEN ITEMS

- **The intro strip was not reached by a citizen click** (see §3). No click in the filed bytes opens the intro view directly; it is proven through the page's own stage entry + real render, plus the identical bridge rule proven by real tap. If the eye wants a click path to the intro view, that is a flow question for a later round.
- **The fix-3 state machine (139/139) was not re-run.** The F9 surface it covers is proven instead by the live probes in §4 at both widths, by real tap (including a stabilized sequential unfold 1→37).
- **My first staged leg failed on a wait, not on the page** (see §3): the bridge stage JS had not rendered `#fpLegal` within 2500ms on the remote host. The re-run with diagnostics passes. Nothing in this report rests on that first attempt.
- **My first D probe hit zero-rect hidden copies** (bare `.frame-icon` / `.fp-speak-face` selectors). The re-probe with visible-only elements gives the clearances in §5. The first numbers were a selector error, not a page defect.
- **The base local screenshot shows the N logo as a black square** (`ck5-base-F-bridge-s0.png`) — a local asset-redirect artifact (the local server 302s missing assets to staging and the logo did not load in that run), not a page defect; the fix-5 local and staged screenshots render the logo. The fix-4 checker recorded the same class of artifact.
- **The apple-touch-icon request** fails on every leg (base and fixed alike) — pre-existing missing asset, not a console error, not a page defect.

## 8. EVIDENCE

All under `~/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/checker/` (screenshots are mine throughout):

- **Logs (JSON):** `checker-log.json` (drive 1 — F bridge/intro/desktop), `checker-log-intro.json` (drive 1b — intro activation), `checker-log2.json` (drive 2 — F9 + A–E), `checker-log2b.json` (drive 2b — D clearances, visible elements), `checker-log2c.json` (drive 2c — unfold stabilized sequential), `checker-log3.json` (drive 3 — desktop + staged + bounded walk), `checker-log3b.json` (drive 3b — staged re-run with diagnostics).
- **Byte + scope proof:** `work/blob-verify.json`, `work/scope-proof.json`, `work/verify-blobs-fix5.cjs`, `work/laws-base-welcome.txt`, `work/laws-fix5-welcome.txt`, plus the fetched fix-5 file copies (`work/fix5-*.html`, `work/fix5-*.js`, `work/fix5-*.py`).
- **Drivers (mine):** `work/serve.cjs` (local base/fix-5 servers on :18095/:18096), `work/checker-drive1.py`, `work/checker-drive1b.py`, `work/checker-drive2.py`, `work/checker-drive2b.py`, `work/checker-drive2c.py`, `work/checker-drive3.py`, `work/checker-drive3b.py`.
- **Screenshots — base:** `ck5-base-F-bridge-s0.png`, `ck5-base-F-bridge-smax.png`.
- **Screenshots — fixed (local bytes):** `ck5-fix-F-bridge-s0.png`, `ck5-fix-F-bridge-smax.png`, `ck5-intro-diag-s0.png`, `ck5-intro-diag-smax.png`, `ck5-fix-B-door.png`, `ck5-fix-D-unfold37.png`, `ck5-fix-E-deck37.png`, `ck5-fix-letter37.png`, `ck5-1920-bridge.png`, `ck5-1920-unfold37.png`.
- **Screenshots — staged:** `ck5-staged-bridge-s0.png`.

## 9. HANDOFF

**Verdict: PASS.** Defect F is fixed: all 12 footer links are reachable at 390 on the bridge (real tap, local and staged) and on the intro strip (real render), desktop 1920 is unchanged link-for-link, F9 passes at 390 and 1920 with 0 console errors, A–E re-measure clean, laws delta 0. The staged link verified is https://naya-walk-beginning-staging.nayapower.workers.dev/ (fix-5 bytes on all four routes, bridge sweep 0 unreachable). The one honest limit is the intro strip's citizen click-path: no click in the filed bytes opens the intro view directly, so it is proven through the page's own stage entry and the identical bridge rule — stated in §3, not hidden. Ready for the eye.
