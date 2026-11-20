# Agreement distill fix-5 — MAKER REPORT

**Round:** Agreement distill fix-5 (Team Nitro) — the footer-links defect F only, from the fix-4 checker's go-back.
**Maker:** Naya Nitro Narzan. **Dispatched:** 2026-11-20 ~11:18Z (04:18 MST). **Branch:** `walkthrough/agreement-distill-fix5-20261119`, from fix-4 tip `d5003b2fd5c59e352b84169294b2773263876e01`.
**Branch tip:** the filing commit — see the maker handoff to the coordinator (the report is filed in that commit, so it cannot name its own sha; the filed blob shas are in §9).
**Staged link:** https://naya-walk-beginning-staging.nayapower.workers.dev/ (fix-5 bytes; PUT 2026-11-20 11:43:18Z, `WELCOME_ASSETS` KV binding re-declared and preserved).
**No merge, no live deploy, no message to the user.**

## 0. Activation (read before any design work)

Read in full, in order: `THE-NAYA-DESIGN-LAWS.md`, `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, the fix-4 checker report (`walkthrough-agreement-distill-fix4-20261119/checker/CHECKER-REPORT.md`, in full — its §F is the fix list), and the fix-3 eye report §F. Base reproduced on fix-4b bytes first (geometry probe + screenshots), then fixed, then re-proven on fixed bytes. The change is one CSS value on two rules, in one file. No flow JS touched; no board content, no F9 code, no desktop rule, no anthem/Listen wiring, no certificate logic touched.

## 1. Base verification (fix-4b bytes, before any edit)

Fix-4 tip re-verified via `gh-direct.py` (GET git ref): `d5003b2fd5c59e352b84169294b2773263876e01` — **tipMatch true**. All six base files fetched via the git blob API and verified size + sha256 + git blob sha — ALL OK (log `maker/work/base-verify.json`):

| File | Bytes | sha256 (fix-4b) |
|---|---|---|
| agreement-unfold-fixed.html | 142,532 | `a3b3907f2f80d09a…` |
| welcome-staged.html | 1,930,937 | `237af4d4d5d3ac3f…` |
| walk-beginning-fixed.html | 4,363,683 | `856d392c439ebb5c…` |
| identity-fixed.html | 404,147 | `fef65d2cdbf2f1e…` |
| walk-beginning-staging-worker.js | 8,463,045 | `a76a67c8e1a366ab…` |
| build-v23-staging-worker.py | 95,815 | `31eae8862ca9cd98…` |

The live assembly dirs hold the same fix-4b bytes (sha256sum-checked before editing). VM browser: Playwright Firefox headless, alive throughout (re-tested each leg; it never died in this round).

## 2. Defect F — before / after (390×844)

### The defect, reproduced on BASE bytes (my own probe, not the checker's numbers)

Driver `maker/work/probe-fix5-base.py`, log `maker/work/proof-base/fix5-base.json`. Bridge state (`/agreement` → tap to 37 → "I agree" → bridge), geometry sweep over the full `scrollLeft` range, one step per 100px plus the max:

- Strip `#fpLegal .fp-legal-links`: `scrollWidth 1064`, `clientWidth 374`, `maxScroll 690`, `justify-content: center`, `flex-wrap: nowrap`, `overflow-x: auto`.
- At `scrollLeft = 0`: Terms of Service `[-678,-548]`, Privacy Policy `[-528,-415]`, Cookie Policy `[-395,-286]`, Refund Policy `[-266,-153]`, Acceptable Use `[-133,-10]` — **identical to the checker's rects**. Community Guidelines `[10,181]` is the first visible link.
- Across the whole sweep, **5 of 12 links are never reachable** (Terms, Privacy, Cookie, Refund, Acceptable Use — `reachable: false` at every `scrollLeft` in [0,690]). At max scroll they are further left still (Terms `[-1368,-1238]`).
- 0 console errors on base.

Cause, read from the filed CSS: the two nowrap strip rules carry `justify-content:center` — centring a 1064px row (true content width ~1754px; the base `scrollWidth` only counts overflow right of the scroll origin) in a 374px viewport pushes the row's start left of the scroll origin. Pre-existing on base and fix-4b, byte-identical — not a regression.

Note on the intro rule: at a cold `/` load `#fpLegal` is `display:none` (the footer only renders once a stage is entered), and `?stage=intro` does not activate it either, so the intro strip could not be geometry-probed from a cold load. The intro rule carries the identical trap (`justify-content:center`, nowrap, same widths) and gets the identical one-value fix; the bridge is the provable surface for both rules, and it is proven below.

### The fix (one CSS value, two rules, one file)

`maker/work/fix5.js` (transform; reconstruction proof included). In `welcome-staged.html` only:

- `html.fp-locked body.fp-stage-on.fp-intro #fpLegal .fp-legal-links{...justify-content:center;...}` → `justify-content:safe center`
- `html.fp-locked body.fp-stage-on.fp-bridge #fpLegal .fp-legal-links{...justify-content:center;...}` → `justify-content:safe center`

Why `safe center`: it centres only when the row fits; on overflow it aligns to the start — the scroll origin — so every link enters the viewport at some `scrollLeft`. Desktop is unchanged: at 1920 the row fits, so it still centres exactly as before. Fallback is graceful: a browser that does not understand `safe` drops the declaration, leaving `justify-content:normal`, which behaves as `flex-start` for a flex row — still reachable. (The worker already uses `safe center` elsewhere — the template's `.sa-theatre-body` — so the value is not new to this codebase.)

**Scope proof:** undoing the two values reproduces the base file byte-identically (`RECONSTRUCTION byte-identical to base: true`); `safe center` occurs exactly 2× in the fixed welcome; 0 remaining nowrap `justify-content:center`. No other file changed except what the build requires (§3).

### Proven on FIXED bytes at 390 (my own probe, same sweep)

Driver `maker/work/probe-fix5-verify.py`, log `maker/work/proof-fix5/fix5-verify.json`:

- Strip: `scrollWidth 1754` (the true content width is now exposed — base reported 1064 because the left overflow was never counted), `clientWidth 374`, `maxScroll 1380`, `justify-content: safe center`, `flex-wrap: nowrap`.
- **All 12 links reachable** (`unreachableCount: 0`):

| Link | First fully inside (left ≥ 0, right ≤ 390) |
|---|---|
| Terms of Service | scrollLeft 0 — rect [12,142] at load |
| Privacy Policy | scrollLeft 0 — [162,275] |
| Cookie Policy | scrollLeft 100 |
| Refund Policy | scrollLeft 200 |
| Acceptable Use | scrollLeft 300 |
| Community Guidelines | scrollLeft 500 |
| Copyright / DMCA | scrollLeft 700 |
| Ambassador Terms | scrollLeft 900 |
| Membership & Billing | scrollLeft 1000 |
| Young Citizens | scrollLeft 1200 |
| Accessibility | scrollLeft 1300 |
| Disclaimer | scrollLeft 1380 (max) — rect [285,378] |

- At `scrollLeft = 0` the strip now opens on "Terms of Service / Privacy Policy / Cookie Polic…" (was "Community Guidelines" first on base). At max scroll it ends on "Young Citizens / Accessibility / Disclaimer", all whole.
- Screenshots (read as a reader): `proof-fix5/fix5-bridge-s0.png` (Terms first, clean), `proof-fix5/fix5-bridge-smax.png` (Disclaimer last, clean), `proof-fix5/fix5-bridge-full.png`.
- 0 console errors.

### Desktop 1920 — no regression

Same driver, `1920-bridge-footer-geo`: `scrollWidth == clientWidth == 1904` (no overflow), `justify-content: safe center`, first link left 87, last link right 1833 — symmetric 87px margins, the row still centred exactly as on base. Identity paired (input `shawn`, hero `Shawn`, hero rect `[500,388,1420,472]`, matching the checker's fix-4 numbers) and unfold board 37 (title 25px, as on base — the 22px rule is ≤480px only) both unchanged. 0 console errors. Screenshot: `proof-fix5/fix5-1920-bridge.png`.

### Staged spot-check (fix-5 bytes on the staged host)

Driver `maker/work/probe-fix5-staged.py` against https://naya-walk-beginning-staging.nayapower.workers.dev/agreement → agree → bridge: same sweep, **unreachable 0**, first three links at scrollLeft 0 = `[12,142]`, `[162,275]`, `[295,404]` — identical to local fix-5 bytes. 0 console errors. Screenshot: `proof-fix5/fix5-staged-bridge-s0.png`.

## 3. What the round changed (files + shas)

CSS-only on the footer strip, plus what the build requires. No flow JS, no board content, no F9 code, no desktop rule touched.

| File (repo path) | Fix-4b bytes | Fix-5 bytes | sha256 (fix-5) |
|---|---|---|---|
| `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | 142,532 | 142,532 (unchanged) | `a3b3907f2f80d09a14c1e7e8bfb7a00c63332a7b26ac2707912c39436e177b98` |
| `team-nitro/walk-v23-assembly-20261114/welcome-staged.html` | 1,930,937 | 1,930,947 (+10) | `57ebe2d295b494ebe8d0e8d3c23de0a89d0025089991a7422ffa514cc4a636d6` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html` | 4,363,683 | 4,363,683 (unchanged) | `856d392c439ebb5cb97aac27f34abc3b97b52b8b6bdc55b50abac9768e198b4d` |
| `team-nitro/walk-v23-assembly-20261114/identity-fixed.html` | 404,147 | 404,147 (unchanged) | `fef65d2cdbf2f1e8c096548df9adcdb465ac38a628f299c8e7cee2fb57703f52` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js` | 8,463,045 | 8,463,055 (+10) | `c9bc8fedcbad3299654c85bd17832aa5a0b205e238dedf53aa98ac1f03b33586` |
| `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` | 95,815 | 96,371 (+556) | `7ce1a895051cd6e48f9c30cfde0a1b3f7392e16e9c7e5cb604d9beefb90aea77` |

Worker rebuild: `build-v23-staging-worker.py` in default mode, run twice — byte-identical both times (`c9bc8fed…`, 8,463,055 B). The build script's welcome assert was updated first (`237af4d4` → `57ebe2d2`, with a FIX5 comment; `maker/work/update-build-script-fix5.js`); all five input shas asserted OK on both runs (walk `856d392c`, identity `fef65d2c`, welcome `57ebe2d2`, template `61002d15`, unfold `a3b3907f`). The worker embeds the fix verbatim: both `safe center` strip rules are present, 0 remaining nowrap `justify-content:center`.

Staging: PUT 2026-11-20 11:43:18Z via `cf-worker.py put-script` with `--meta staging-meta.json` (the `WELCOME_ASSETS` KV binding, namespace `1cf80db6183245d19dd5296645a12bd0`); bindings re-read after the PUT and still present. Staging curl-verified after the PUT (browser UA): `/` → `57ebe2d2…` (1,930,947 B), `/identity.html` → `fef65d2c…`, `/welcome` → `856d392c…`, `/agreement` → `a3b3907f…`. Curl outputs saved as `maker/work/stage5_*.bin`.

## 4. F9 regression (fix-5 bytes, 390 and 1920)

Drivers: `maker/work/probe-fix5-verify.py` (log `proof-fix5/fix5-verify.json`) + `maker/work/probe-fix5-f9c.py` (log `proof-fix5/fix5-f9-deck-letter3.json`). All at 390×844 except where 1920 is named. Two of my first driver attempts failed on driver assumptions, not on the page — recorded honestly in §6; the corrected driver below is the evidence.

| Check | 390 | 1920 | Result |
|---|---|---|---|
| Identity paired `?name=Shawn&alias=Shawn` | input `shawn`, hero `Shawn`, visible | same (hero `[500,388,1420,472]`) | ✓ |
| Door holds 10 s untouched | still `["step-door"]` after 10 s | — (390 only) | ✓ |
| Continue → step-1 (`#doorContinue`) | `["step-1"]` after tap | — (390 only) | ✓ |
| Unfold 1→37 by real tap | counters sequential 1/37…37/37 | board 37 title 25px | ✓ |
| Deck 1→37 → bridge | sequential 1/37…37/37; `#fpNextBtn` becomes "Enter NayaNET ◆" at 37; hold cleared; tap → bridge, pair shows | — (390 only) | ✓ |
| Letter 1→37 → bridge | sequential 1/37…37/37; `#fpNextBtn` becomes "I agree ◆" at 37; hold cleared; tap → `/?stage=bridge`, pair shows, AGREED marker true | — (390 only) | ✓ |
| Bridge pair both ways | "Begin the visual story" → deck 1/37; "Read the agreement" → `/agreement` 1/37 (one context) | — (390 only) | ✓ |
| Console errors | 0 `pageerror` / console errors on every fixed leg | 0 on the desktop leg | ✓ |

The fix-3 state machine (`run-fix3.js`, 139/139) was not re-run; the F9 surface it covers is proven instead by the live probes above at both widths, by real tap. Do not claim 139/139.

## 5. Laws — §11 check in writing + checker delta

`check-design-laws.py` run on the changed file, base vs fixed (outputs saved as `maker/work/laws-base.txt` / `laws-fix5.txt`; identical after filename normalisation):

| File | Base FAIL / WARN | Fix-5 FAIL / WARN | Delta |
|---|---|---|---|
| welcome-staged.html | 83 / 4 | 83 / 4 | 0 |

The FAILs are pre-existing checker noise (sub-17px fonts throughout the base file; the word "gray" inside comments). None introduced by this round. The other five files are byte-identical to fix-4b, so their counts are unchanged by construction (fix-4: identity 11/2, walk 128/8, unfold 1/2, welcome 83/4).

**§11 check, in writing.** (1) Five gates: Right — the round restores five unreachable legal links to the citizen reading at phone width; nothing harmful. Truly needed — the checker's go-back named exactly this defect with measured rects. Mine to do — this is the dispatched fix-5 maker round; no merge, no live deploy, no message to the user. Now — the round is staged and ready for the checker/eye. Prove it — every claim above carries a measured rect, a log line, or a screenshot I took myself. (2) Real objects, one light, elevation, alive on hover: untouched — no element restyled, only the alignment of one strip. (3) Type 25/19/17, no grey text: no text size or colour changed anywhere; the footer links keep their 13px size (pre-existing, counted in the 83 — out of scope for this round, which is charged with reachability only). (4) Harvest first: the fix edits the file's existing strip rules; nothing rebuilt, nothing redesigned, no new page, no new element. (5) Don't remove/move/touch what wasn't asked: desktop rules untouched (1920 geometry proves it); F9 code untouched; defects A–E untouched (all PASS, proven by the checker with measured rects — I did not re-prove them, per scope). (6) Read as a reader: the strip now opens on "Terms of Service" and ends on "Disclaimer", all whole, at both ends of the scroll — and the bridge page reads clean top to bottom in the screenshots. (7) Button destinations double-checked: every button on the F9 spot-check lands where it should — unfold → bridge, deck → bridge, letter → bridge, door Continue → step-1, pair → deck/agreement. No dead ends, no stale pages. (8) Phone first: the fix is proven phone-first at 390, with desktop confirmed unchanged at 1920.

**Scorecard (honest):** the page is a 10 on the F acceptance as written — all 12 links reachable, desktop unchanged, F9 intact, laws delta 0. The remaining known pre-existing items (the 83 laws-checker FAILs, the deck caption nick, the missing apple-touch-icon) are unchanged from fix-4b and out of this round's scope.

## 6. What was NOT proven / not done (honest record)

- **My first F9 driver failed twice on driver assumptions, not on the page.** (a) The first verify run used a "Next"-text button to walk the deck/letter — deck and letter advance via `#fpNextBtn` ("Keep reading ◆"), so those legs timed out; the log was also lost because the crash escaped before the write (fixed by per-leg try/except + always-write). (b) The second run clicked the end-card `.enter` submit button ("Enter NayaNET →") instead of `#fpNextBtn` itself, which becomes the end button at board 37 — that button sits covered (the click stalled on hit-target). The third run uses the checker's exact `click_next_or_end` pattern (wait for `#fpNHold` to clear, click `#fpNextBtn`) and passes every leg. The deck end click reaches the bridge directly; no second "Enter NayaNET" tap is needed or present afterwards.
- **The intro-state strip was not geometry-probed** (see §2): `#fpLegal` is `display:none` on a cold `/` load and `?stage=intro` does not activate it. The intro rule gets the identical fix and the bridge — the same strip, same widths, same trap — is proven on both base and fixed bytes. If the checker can activate the intro stage, it should re-probe there; the rule is the same one-value change.
- **Fix-3 state machine (139/139) not re-run** (see §4).
- **The deck caption nick** (sign photo nicks "· NayaNET · The Deck", byte-identical on base and fix-4b) is unchanged and out of scope, as the checker recorded.
- **The apple-touch-icon request** fails on every leg (base and fixed alike) — pre-existing missing asset, not a console error, not a page defect.

## 7. Work scripts (in `maker/work/`)

`verify-base.cjs`, `fix5.js`, `update-build-script-fix5.js`, `serve.cjs`, `staging-meta.json`, `browsertest.py`, `intro-diag.py`, `intro-diag2.py`, `probe-fix5-base.py`, `probe-fix5-verify.py`, `probe-fix5-f9.py`, `probe-fix5-f9b.py`, `probe-fix5-f9c.py`, `probe-fix5-staged.py`, `laws-base.txt`, `laws-fix5.txt`. Proof logs: `proof-base/fix5-base.json`, `proof-fix5/fix5-verify.json`, `proof-fix5/fix5-f9-deck-letter.json`, `proof-fix5/fix5-f9-deck-letter2.json`, `proof-fix5/fix5-f9-deck-letter3.json`. Screenshots: `proof-base/fix5-base-*.png` (4), `proof-fix5/fix5-bridge-*.png` (3), `proof-fix5/fix5-1920-*.png` (2), `proof-fix5/fix5-staged-bridge-s0.png` (1). Staging curl outputs: `stage5_*.bin` (4). Local servers served base on :18093 and fix-5 on :18094 during the probes; both stopped when the probes finished.

## 8. Handoff to the coordinator

Branch `walkthrough/agreement-distill-fix5-20261119` from `d5003b2f`; staged link https://naya-walk-beginning-staging.nayapower.workers.dev/ (fix-5 bytes, verified by curl sha on all four routes and by a staged geometry spot-check: 0 unreachable links). Defect F proven fixed at 390 with measured rects + screenshots (all 12 links reachable; Terms first at load, Disclaimer last at max scroll); desktop 1920 unchanged (row still centred, no overflow); F9 regression passes at 390 and 1920; laws delta 0; §11 check above. Ready for the checker. The one thing I would flag for the checker: the intro-state strip could not be activated from a cold load, so its geometry is proven by the identical bridge rule, not by a direct intro probe — see §2 and §6.

## 9. Filing record (git blob shas — content hashes, verified against `git hash-object`)

| Repo path | Bytes | sha256 | git blob sha |
|---|---|---|---|
| `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | 142,532 | `a3b3907f…` | `1f0b04747e3315be6f1b619c1411e5e14fbdc1bb` |
| `team-nitro/walk-v23-assembly-20261114/welcome-staged.html` | 1,930,947 | `57ebe2d2…` | `00082c3d65801997f1dcb035bea6ee51bf600737` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html` | 4,363,683 | `856d392c…` | `2f7a5e3ef599e00cb39c1e577bcb42563cd7ed81` |
| `team-nitro/walk-v23-assembly-20261114/identity-fixed.html` | 404,147 | `fef65d2c…` | `b3e5af088ef1d516079d96eeaa61d811d7889b8e` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js` | 8,463,055 | `c9bc8fed…` | `0413500982bc14dfbe5534cbe82cd9c75a68696a` |
| `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` | 96,371 | `7ce1a895…` | `2299b99155e442257ca46eeb2c777ad4816ff6b0` |

(The report itself is filed in the same commit; its blob sha is recorded in the maker handoff — it cannot list its own hash.)

Work scripts filed under `team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work/`: the scripts and logs listed in §7 (the multi-MB base/fix-5 file copies in the work dir are not filed — they are reproducible from the branch blobs plus `fix5.js`). Filed via the git-data API (blob API — the contents API returns EMPTY for files over 1 MB); filed blob shas verified against local `git hash-object` and by a fresh tree read after filing.
