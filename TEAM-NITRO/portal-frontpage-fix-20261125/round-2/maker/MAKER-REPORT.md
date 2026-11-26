# Portal Front-Page Fix — ROUND 2 — Maker Report

**Maker:** Portal Front-Page Fix Round 2 seat · **Round started** ~2026-11-25 23:45 MST · **Report** 2026-11-26 ~01:10 MST
**Base:** round-1 staged portal, branch `portal-frontpage-fix-20261125`, commit `ee1cb356`, 1,904,285 B, sha `737fca6b…`
**Staged (round 2):** https://portal-frontpage-fix-20261125-r2-staging.nayapower.workers.dev/
**Portal:** 1,907,038 B, sha256 `66664c07a1b4ae3b73f69af318a405a29d1848589d535424917f8229e0e49ead`
**Identity (certificate):** 313,224 B, sha256 `57bdd3873f65104f3ee6f4648cfec4a1a556a78ea8b7fb57153cd49da528af4b` — byte-identical to R2, untouched
**Branch:** `portal-frontpage-fix-20261125-r2` (from the round-1 branch head `ee1cb356`)
**Code commit:** `4b194f93b100086a22654ae0c76911ae52710485` (tree `b524093d…`)
**Worker:** `portal-frontpage-fix-20261125-r2-staging`, Cloudflare account `b5e2a51b…`, deployment `05f3e980268a45629ad8814e5ac25468` (the redeploy after the bug fix; the first deployment `8e18aa5ca1574a29a94fdea31389720b`, created 2026-11-26T00:05:29Z, carried the nested-`<style>` bug and was superseded — see below)
**Nothing live, nothing to Shawn.** Staged only. A separate independent checker verifies next.

## In one line
The red N now visibly spins — the gold N itself turns, proven by timed captures at 390×844 and 1440×900 — and the phone heading clears the rim at the exact width the eye saw it collide (573×355), fresh and returning.

## F1 — THE RED N DOES NOT SPIN — diagnosed, then fixed

**Diagnosis (proven, not assumed).** I fetched the live agreement fresh (https://nayanet.app/agreement, v25, 22,953,906 B, sha `2c88513f…`) and read how ITS ball is animated. There is **no ball rotation to harvest**: `.orb-wrap.jewel` carries only `animation:floaty 5.5s ease-in-out infinite` — a vertical bob — and `orbit-spin` sweeps a ring custom-property (`@keyframes orbit-spin{to{--oa:360deg}}`). The agreement's ball never turns. The portal corner's only motion in R1 was the thin `.ncorner::before` ring (`eco-spin 90s`) — a symmetric arc that reads as static — while the ball img itself measured `animation: none 0s` and `transform: none` at t0 AND t25. The central jewel-dot ring's parent (`.naya-color-orbit`, `nayaSpectrum 78s`) does rotate, but 108 evenly spaced jewels read as static to the eye. That is why the eye saw nothing move in 3 minutes, and why the round-1 checker's "eco-spin 90s orbit" was a declaration, not a proven motion.

**Fix.** The portal's own `eco-spin 90s linear infinite` keyframes now run on the right-corner IMG itself (`.ncorner-right img{animation:eco-spin 90s linear infinite;}`) — 90 s ambient, inside the laws' 60–180 s band. The gloss span stays fixed above the ball (z-index 4), so the light stays top-left while the ball turns under it. Asset, alt, size, position and destination unchanged; the left (black) N untouched; reduced-motion disables the spin too.

**My proof (read with my own eyes, not just measured).**
- Phone 390×844: img computed transform t0 `matrix(0.847, 0.531, …)` → t25 `matrix(-0.967, 0.254, …)` — the gold N turns from a tilted "Z"-like angle to an upright N. Captures: `evidence/r2-phone390-corner-t0.png` / `r2-phone390-corner-t25.png`.
- Desktop 1440×900: t0 `matrix(0.753, 0.658, …)` → t25 `matrix(-0.797, -0.604, …)` — the N turns from sideways to upright-ish. Captures: `evidence/r2-desk-corner-t0.png` / `r2-desk-corner-t25.png`.
- Even a plain screenshot catches it mid-turn: the bottom-right N reads as a "Z"-like angle in the desktop and phone front captures.

## F2 — PHONE-WIDTH HEADING COLLISION — reproduced, then fixed

**Reproduction (exact).** At 573×844 and 573×700 there is NO collision in either view — heading one line, 147–176 px clear. At **573×355** (a short window; the Hub R12 eye walk recorded a shrink to 573×355) it reproduces exactly: the portal shrinks to its 250 px floor, content narrows to 187 px, the heading wraps to two lines and its top line is wider than the circle's chord at its height, so the rim slices the word — returning view showed "NAYA WELCOME" with the S cut by the rim and "YOU" under it; "Welcome back," tight against the same rim.

**Fix.** New rule block gated `@media (max-width:640px) and (max-height:700px)`: the heading stays ONE line (`white-space:nowrap`, `letter-spacing:0` — deliberately NO new `font-size` declaration, so the design-law counts cannot move) and the stack compresses (`.input` 38 px, `.enter` 40 px, margins/gaps tightened) so the heading sits lower, in the wide band of the circle. Desktop, 390×844 and 573×844 are untouched by the gate.

**My proof (numbers + screenshots).** Text-width measured with a Range over the heading text node, chord computed at the text's own height:
- 573×355 fresh: text 134 px wide vs chord 212 px (78 px spare), 52 px clear of the portal top; heading 1 line, 14 px tall.
- 573×355 returning: text 134 px vs chord 199 px (65 px spare), 42 px clear; "Welcome back," clear below it.
- 390×844 fresh: 2 lines (34 px tall, unchanged from R1), text 143 px vs chord 224 px, 54 px clear — fine by design.
- 573×844 fresh: 1 line, 179 px vs chord 433 px.
- Screenshots read with my own eyes: `evidence/r2-w573h355-front.png` (one-line heading, green dot, input, Enter, ⓘ all inside the circle) and `evidence/r2-ret573h355-front.png` ("Welcome back, Return Test." clear; "Jump back in →" + New-user pill inside; "This is me" correctly hidden again).

## The bug my own probe caught — and fixed

The first R2 build I deployed was **broken**, and my probe found it before anyone else saw it. My F2 insertion emitted a literal `<style>…</style>` wrapper **inside** the already-open `<style>` element (the anchor — the end of the 480 px media block — sits mid-stylesheet; the RETURNING VIEW v2 rules follow it inside the same element). The inserted `</style>` closed the element early and stranded those rules as visible body text: the desktop screenshot showed the whole "PORTAL RETURNING VIEW v2" comment block and its rules rendered as page text at the top, the stage pushed down 216 px, "This is me" reappeared in the returning view (its `display:none` rule was stranded), and the F2 `@media` itself was swallowed by the CSS parser (its prelude fused with the bogus `<style>` line), so the heading fix never applied.

**Fix:** the F2 insertion now emits only the CSS comment + `@media` block — no style tags. Two new build-time guards in `build-fix-r2.mjs`: the style-element count must stay 6/6 (R1's count), and the RETURNING rules must still sit inside a style element. All 19 build assertions pass; the diff vs R1 is exactly **6 hunks** (`evidence/portal-diff-r2.txt`, 93 lines). The worker was redeployed (same R2 worker, new deployment id above) and the staged bytes re-verified by curl read-back (1,907,038 B, sha `66664c07…` matches the lane file exactly). The broken first deployment (`8e18aa5c…`) never reached the checker.

## Round-1 pass items — all re-verified after the fix

- Clean front page on desktop: only NAYA WELCOMES YOU + "What do we call you?" + "Enter NayaNET →" + centred ⓘ; agreement sentence nowhere on the front page.
- ⓘ opens the agreement reader, copy verbatim ("By entering your name, you make it official — you are signing the Collective Agreement…"), "1 of 13" → Next → "2 of 13", at both 390 and 1440.
- Bottom-left black N present, byte-identical to EMBED.logo; red N → `https://nayanet.app/agreement`, black N → `https://nayanet.app/` (hrefs verified in the bytes).
- Returning view premium: gold Marcellus name, "Jump back in →" to the Hub, no "This is me", no flat green text (screenshot + bytes).
- All nine top-menu destinations land live (9 `eco-item` anchors, same as R1).
- Certificate: 5 real jewels, sha unchanged (`57bdd387…`).
- 0 page errors: the single console.error on phone 390 is the known `/favicon.ico` 404 — it 404s identically on the R1 worker; no failed requests, no request failures (probe log).
- Design-law counts identical to the R2 baseline: portal **81 violations + 4 warnings**, identity **3 violations** — zero new (re-run on the final file).

## Other observations

- **(a) Reader overlaps the heading — FIXED.** While the reader is open the jewel-dot ring fades (`body.fp-reader-open .naya-orbit{opacity:0;}` + class toggled in the reader open/close handlers). Probed: ring opacity 0 + class set while open, at both widths.
- **(b) Name from `?name=…` not on the certificate until an alias is typed — FOLLOW-ON.** The install-veil code and the certificate name logic live only in `identity.html`, which is behind the do-not-touch-certificate rule. Named, not fixed.
- **(c) "Install NayaNET" PWA prompt popped up unprompted and covered ENTER — FOLLOW-ON.** Same: the `beforeinstallprompt` handling lives only in `identity.html` (7 matches, 0 in portal.html/sw.js). Whether it should be gated is a decision for the captain/Shawn, not this round.
- **(d) Corner N images intermittently reported failed though they rendered — CONFIRMED SOUND.** Both corner images are inline data URIs, not network fetches: the red ball WEBP 182,452 B (sha `2a4b10fd…`, byte-identical to live agreement v25 EMBED.ball) and the black N JPEG (byte-identical to EMBED.logo, sha `08b753d3…`) are present in the staged bytes; the probe recorded 0 failed requests and both images render in every capture. The intermittent "failed" report was the probe's image check, not the assets.

## Registry — the eye's test identity

**captaineye — certificate WAS minted: Nº 893**, name "CaptainEye", created `2026-11-25T23:41:32.625867+00:00`, `has_world: false`. It joins the deletion list. **NOT deleted — deletion waits for Shawn's go-ahead.** All known test certs confirmed present and untouched: r2check25 Nº 884, eyetestnov24 Nº 876, spinetest1 Nº 877, checknov25b Nº 881, fixnov25a Nº 883.

## §11 Design-Law check (in writing)

- Read first, in order: `THE-NAYA-DESIGN-LAWS.md`, `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-ULTIMATE-ORIENTATION.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md`, round-1 maker + checker reports, `team-nitro/AGENTS.md`. The laws win over the brief on conflict — no conflict arose.
- §2.1 text scale: no new `font-size` declaration anywhere in the round (the F2 fix was designed around this); the checker counts every sub-17 px `font-size` as a violation, and the counts are unchanged (81 + 4 / 3).
- §2.2 colour: no new colours; the spin and the ring fade reuse existing keyframes and classes.
- Real Object Law: nothing redrawn, nothing rebuilt — the ball is the harvested asset, turned by the portal's own keyframes; the gloss stays fixed so the light stays top-left.
- Harvest first: base is the R1 staged portal, edited, never rebuilt; the diff is 6 hunks.
- Checker: `python3 ~/workspace/team-nitro/check-design-laws.py portal.html` → 81 violation(s), 4 warning(s); `identity.html` → 3 violation(s), 0 warning(s). Identical to the R2 baseline. Zero new.

## Self-scorecard

- F1 spin, proven by timed captures I read myself at both widths: **10/10** — the N is visibly at different angles.
- F2 heading clear at the reproduced width, fresh + returning, numbers + screenshots: **10/10**.
- (a) ring fade while reader open: **9/10** — proven at both widths; the desktop reader still sits inside the circle by design (unchanged from R1).
- No regressions in the round-1 pass set: **10/10** (every item re-probed).
- Own-goal caught by my own probe (the nested `<style>`): **the round's lesson** — an insertion's context (inside an open element) matters as much as its content; the two new build guards now make that class of bug fail the build instead of the page. Score for catching it before handoff: 10/10. Score for shipping it in the first place: 0 — the first deployment was broken, and only the probe saved it from the checker.
- Overall: **9/10**. The work is proven; the hour ran long (the bug + its re-proof cost the round its timebox), and the checker must still do its independent pass.

## What I proved vs what the checker must prove

**Proved by me:** F1 rotation (matrices + captures read with my own eyes, both widths); F2 clearance (text-width/chord numbers + screenshots at 390, 573×844, 573×355 fresh + returning); reader 1→2 of 13 + ring fade; staged bytes == lane bytes (portal + identity + sw.js); design-law counts unchanged; certificate sha unchanged; the 404 is favicon only; the nested-`<style>` bug found and fixed; captaineye Nº 893 recorded.

**Checker must prove (independently, fresh eyes):** the same rotation captures on its own run (≥20 s apart, true 390×844 and 1440); the heading at 573 px width on its own viewport; all nine top-menu destinations landing live by clicking; the returning view end-to-end; the certificate's 5 jewels rendering on identity.html; 0 page errors on its own run; the diff vs R1 is the 6 hunks named here and nothing else; and that nothing in the round-1 pass set regressed that I did not re-probe (in particular the full walkthrough flow beyond the front page, which this round did not touch).

## Evidence

- `evidence/probe-r2.py` + `probe-r2-log.json` (full probe, final run) · `evidence/measure-text.py` (text-width/chord numbers)
- `evidence/r2-phone390-corner-t0.png` / `r2-phone390-corner-t25.png` · `evidence/r2-desk-corner-t0.png` / `r2-desk-corner-t25.png`
- `evidence/r2-phone390-front.png` · `evidence/r2-desk-front.png` · `evidence/r2-w573h355-front.png` · `evidence/r2-ret573h355-front.png` · `evidence/r2-w573h844-front.png` · `evidence/r2-ret573h844-front.png`
- `evidence/portal-diff-r2.txt` (6 hunks vs R1) · `evidence/harvest-r2.json` · `evidence/agreement-live.html` (live v25, sha `2c88513f…`)
- `build-fix-r2.mjs` (19 assertions, all PASS) · `build-worker-r2.mjs` · `verify-r2.mjs` (15 checks, all PASS against the staged worker) · `commit-r2.mjs`
- Diagnosis: `evidence/probe-diagnose.py` + `diag-log.json` · `probe-diagnose2.py` + `diag2-log.json` · `probe-diagnose3.py` + `diag3-log.json` + `diag3-fresh573x355.png` / `diag3-ret573x355.png`
