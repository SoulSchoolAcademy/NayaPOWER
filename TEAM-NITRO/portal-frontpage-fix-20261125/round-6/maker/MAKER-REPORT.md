# Portal Round 6e — MAKER REPORT (the correction: the settled loop)

**The loop, in one line:** red orb dead center at the top (real live object, energy flowing around it) → click → straight to https://nayanet.app/agreement → go through the agreement → Agree at the end → back to put their name in. The agreement does not come up again after that.

**Staged:** https://portal-frontpage-fix-20261125-r6-staging.nayapower.workers.dev/
**Portal:** 13,887,202 B, sha256 `01051a8fb76f9b948a75505f7c6baa39a3f7d3fcd82be637448e344f23b3bc59`
**Agreement file:** `agreement-v25-fixed-r6.html` — 22,935,043 B, sha256 `410078e1a4102496706c3df64e04a20539a3ae9ce745df77a8c48ed857b57b7b`
**Certificate `/identity.html`:** the NEW fixed cert — 315,409 B, sha256 `0c11fdb8a0fcb7269d931584088f68629487e528c9e0fcffae47013933897365`
**Worker:** `portal-frontpage-fix-20261125-r6-staging`, 14,226,407 B, sha256 `19851052aeea583e6e45ee6bc6d1978e6bb8352a4b10bfe7969d93ff90d4a0f8`; subdomain enabled; KV binding `WELCOME_ASSETS` (namespace `1cf80db6183245d19dd5296645a12bd0`) unchanged.
**Branch:** `portal-frontpage-fix-20261125-r6` (repo `SoulSchoolAcademy/NayaPOWER`)
**Commits on the branch:**
- `7d5fc23ba187c63b0dd29ac7f035939cf8be78bf` — the agreement change (R6)
- `b2ab86d41f355c18e4f0c3a583f4448f3712e661` — the little N (R6, SUPERSEDED — see below)
- `f9e071c69a67c14906d3aab9527e984b2e71e8e5` — probe fixes (R6)
- `2c4bf1490c5bee50aec85c4f989630f967e7a28d` — probe fix 2 (R6)
- `fb721c5d72588e834c1217e2bef32030ad3df196` — **R6e: the correction** ← **HEAD**
**R6e blobs (verified via git blob API: decode == lane bytes + sha match):**
- `portal.html` → `50b6733dbbace998457e9cf8d205eee12e483f12` (13,887,202 B)
- `agreement-v25-fixed-r6.html` → `20fd336bb0975dc5679a5463dd4082eb2aff1620` (22,935,043 B)
- `identity.html` → `8f08d3dec576bbdbeb8f52950bbe0cfee755afa4` (315,409 B)
- `worker-consolidated.js` → `ebb36a8e8572973e3f9dc1333b901f5dbefdff36` (14,226,407 B)
**Base:** R5 staged — 13,883,771 B, sha `d4bb2102…`. Delta R6e vs R5: **+3,431 B**. Exact diff: `evidence/portal-diff-r6e.txt` (131 lines; the raw file is 1.5 MB because the removed footer button sits on a 760 KB line — the readable form is `evidence/portal-diff-r6e-readable.txt`, 9,955 B, with the giant line truncated and its exact change spelled out). Data URIs byte-identical to R5 (31 URIs, sha `c16946cd…`, 13,231,508 chars).
**Time:** the one-hour max was exceeded by a wide margin — the round ran from 08:17 MST through the correction (09:14 MST) and the build/probe/filing after it. Stated plainly, not hidden.

## What the correction changed (Shawn, 09:14:29 MST — SUPERSEDES the little-N/nutshell decision)

Steer 5's little-N-replaces-ⓘ + nutshell pop-up is **not built**. The R6 build that contained it (commits `b2ab86d4…` + `2c4bf149…`) is superseded by the R6e build in commit `fb721c5d…`, which replaces those parts with the correction:

1. **ONE ENTRY, dead center at the top.** The red N orb (`#fpCircleN`) is the ONLY agreement entry. Click → `window.location.href = 'https://nayanet.app/agreement'` — the exact URL, direct, no preview, no intermediate, no pop-up. Entry count: **1 of 1 entries lands on the exact URL.**
2. **NO bottom agreement button — 0 occurrences.** The footer `#fpEnterDeal` button ("Read the agreement ◆") is gone (element, handler, and its dead letter-script query with it). The only remaining `fpEnterDeal` / `openStory(0)` mentions are one dated `ROUND 3 — SUPERSEDED` historical comment, not live code. The `.fp-enter-deal` CSS rules remain as dead rules (harmless, noted).
3. **The orb is a real live object, upright N.** The `eco-spin 90s` is off both red-N imgs (the spin carried the glyph sideways — R5 checker: corner red N +138.3° over ~34.6s). The spin stays on the decorative rings. New: a bright energy ring (`::before`, conic arc white/red/violet, `eco-spin` at 12s, drop-shadow glow) + a breathing halo (`::after`, `@keyframes fpOrbHalo`, 4s). The black left N is untouched (upright, home link).
4. **Corner Ns are NOT entries.** The red corner N now links home (`https://nayanet.app/`, aria "NayaNET — home"), like the black N.
5. **The ⓘ stays exactly as R5** (3 occurrences, all in comments). No little N, no nutshell, no deed text restored on the front page.
6. **The agreement does not come up again.** Real mechanism: `localStorage['nayanet_agreement_done']` is set to an ISO timestamp on every Agree click — the portal's story Agree, the portal's stage-seal Agree, and the v25 file's `goToPortal()`. The front page never auto-opens the agreement, so after completion + return + reload the page is at rest and nothing re-appears or re-prompts. Proven by probe (flag `2026-11-26T16:40:08.528Z` phone, `16:42:10.263Z` desk; reload → `view: intro`, `stageOn: false`, `modalOpen: false`).

## What the agreement file is (`agreement-v25-fixed-r6.html`)

The live v25 file (22,953,906 B, sha `2c88513f…`, R2 bucket `nayanet-covers`, key `agreement-v25.html`, served by worker `nayanet`'s `/agreement` branch) edited as an **entry fix, not a text harvest** — no slide reworded, no legal page touched, no portrait/audio data touched (build `build-agreement-v26.mjs`, all V assertions pass, both inline scripts compile):

- **The preview intro is GONE, whole** — the `#screen-choice` section + its comment, its 17 CSS rules, its wiring IIFE (including the `?view=deck` / `?view=letter` deep links), the `screens.choice` entry, the `show()` choice branch. Counts in the fixed file: 0 "Begin the visual story", 0 "Read the agreement", 0 "Welcome. Let's begin with trust.", 0 `screen-choice`, 0 `choice-pill` / `choice-play` / `fpChoice`.
- **It opens on the welcome player** (`#screen-cover` is now the `active` screen): "NAYA'S WELCOME — THE COLLECTIVE AGREEMENT · WELCOME HOME: MEET NAYA, YOUR GUIDE TO A NEW INTERNET!", visual + audio 4:18. LET'S GO starts slide 1 "The Old Way". All 27 slides in exact order to the end slide with the Agree button.
- **Welcome player fixes:** the duplicate lower player bar is OUT (the `<audio>` element stays in the DOM, hidden, no `controls` — removing it would throw in the JS that assigns `audio.src`); the main play button sits BELOW the visual as a static row (disc + label), nothing covering the picture; the poster is `object-fit:contain`, centered, whole (the poster is 1000×750, 4:3, in a 16/9 frame — `cover` cropped it, `contain` shows it whole, pillarboxed). The audio works: duration 258.15s, readyState 4, transport controls ‹15s, ▶, ■, 30s›, `tDur` reads 4:18. Phone fit: the cover's caption strip and its (dead) arrows hide at ≤640px, the voice orb shrinks 116→96px, `.cover-n` 60→48px.
- **End slide, exact layout:** the slide holds the verbatim deed text ("By entering your name, you make it official — you are signing the Collective Agreement, and you get the deed to your own world: high-level digital real estate — your personal page, your business, your space — free forever.") and then the Agree button ("I agree ◆") — nothing else. Agree sits at the very bottom, just above the < > arrows, flashing (`agreeFlash` 2.4s green glow). The eight links (Our Vow, The Deal, Our Promise, The Governance, Our Constitution, Our Laws, Our Rules, Our Oath) sit on a bar BELOW the page, after the arrows, on the last page only. Click Agree → back to `https://nayanet.app/?from=agreement#userName` (the name entry).
- **Delta vs v25:** −18,863 B (the intro out, the R6e CSS + end-slide code in).

## Certificate wiring

- The staged portal serves the **NEW** certificate (315,409 B, sha `0c11fdb8…`), harvested byte-for-byte from the portal-consolidated staging URL. The portal's certificate links go to the live address `https://nayanet.app/identity.html` (entry-form submit keeps its `?name=` handoff; "this is me" too). The new cert goes live at nayanet.app/identity.html as part of this round's live step.
- **WALKTHROUGH GAP — named plainly, not silent.** The fixed cert's handoff is `WALKTHROUGH_URL = '/?walk=1'` on the same origin. The UPDATED 15-question walkthrough (the About+Skills Innovations-clone walkthrough, fix2 build) has **no `?walk=1` entry** — its file (`about-skills-clone.html`) contains zero hits for `walk=1`, `?walk`, `URLSearchParams`, `openWalk`/`showWalk`/`startWalk`/`autoOpen`. Serving it at `/?walk=1` would land on the About+Skills page, not the walkthrough. So the portal **cannot serve the updated walkthrough at /?walk=1 in this round** — the portal's built-in 15-question walk stays exactly as R5 proved it (ends "Almost there" on the known backend `/api/welcome/complete` 404). An auto-open (or a transplant into the portal's walk) is a separate build.
- **New from MEMORY.md while this round ran (voice call 2026-11-26 ~08:56–09:39 MST):** the walkthrough is now specified as **27 questions in a locked order** (door: certificate, first name, alias; beginning 8: country, language, province/state+city, age grouping, male/female+ethnicity, faith, community/church, sports+music; About ten 9–18 in the same words; Skills five 19–23 in NEW words — gift, benefit, uniqueness, work, connection with up to three social links; resume layer 24–27: industry→sub-industry→skills type-ahead, experience, achievements/awards, education), everything optional except the name, editable in settings, auto-detect country+language, feeding auto-match and the profile. The **three-panel structure law** is also locked (top bar: image, logo, question name; panel 1 = image; panel 2 = ALWAYS the audio player; panel 3 = input with the headline AS the question, Speak, Enter, an i button; the five hint jewels are OUT; the higher-quality winged-N emblem replaces the corner logos; examples are always "ours"). And **the 27 happen ONCE, then everything carries over** when they create a new world/space/business ("create", never "cloning" where they can see it). All of that is the walkthrough build's scope — it does not change this round, and this round does not build it. The captain's live step and the walkthrough build need to carry it.

## Staging + filing (proven, not claimed)

- **Worker deployed:** `portal-frontpage-fix-20261125-r6-staging` — PUT HTTP 200, deployment `67738c882c1d402aafdc3273a7564219`, modified 2026-11-26T16:32:06Z. (One propagation lag: the first curl after the PUT still served the old R6 `/` bytes; a re-curl 60s later served the new bytes. Noted so the checker doesn't trip on it.)
- **Staged bytes == lane bytes == blob by sha (curl + `verify-r6e.mjs`, all PASS):** `/` 13,887,202 B `01051a8f…` · `/identity.html` 315,409 B `0c11fdb8…` · `/agreement` 22,935,043 B `410078e1…` · `/sw.js` 567 B `abac2ab5…` (565 chars; the 567 vs 565 is chars-vs-bytes, the sha matches the R5 record).
- **KV:** `agreement-v25-r6.html` PUT to `WELCOME_ASSETS` (HTTP 200 `success:true`); the immediate GET 404'd twice (KV propagation, ~90s), then GET returned 22,935,043 B sha `410078e1…`, MATCH with the lane file. The worker's `/agreement` route serves it from KV (the file is too big to embed in the worker script).
- **GitHub:** commit `fb721c5d…` on branch `portal-frontpage-fix-20261125-r6` (HEAD was `2c4bf149…`); all four big blobs verified via the git blob API (decode == lane bytes + sha match). The 23 MB agreement file was filed piped (base64 → jq → gh-app-api, no intermediate file).
- **Builds:** `build-fix-r6e.mjs` 36/36 assertions PASS (all 10 inline scripts compile); `build-agreement-v26.mjs` all V assertions PASS (both inline scripts compile — script 1 is 21,601,487 B); `build-worker-r6e.mjs`; `verify-r6e.mjs` all PASS. One verify assertion was fixed in the pass (it checked for a `fpOrbSpin` keyframes name that was never the implementation — the ring uses the existing `eco-spin` keyframes at 12s; the build was right, the verify was wrong).

## Probe evidence (real renders + real taps, Chromium 1255 via forwarder; logs + screenshots read with my own eyes)

**Full loop — `evidence/probe-r6e-loop.py`, log `evidence/r6e-loop-log.json`, both widths (390×844 + 1440×900):**
- **Front:** orb present, center x = viewport center (195/195 phone, 720/720 desk), 56px, aria "The Collective Agreement — the red N", ring anim `eco-spin`, halo `fpOrbHalo`, img anim `none`; `fpEnterDeal` 0; no visible bottom "Read the agreement" button; ⓘ count 0 (the 3 in the file are comments, not rendered); menu 0 labels at rest, 9/9 tips opacity 0; heading "Naya Welcomes You"; red corner → `https://nayanet.app/` home; name input present; stage off.
- **N angles:** 0°/0°/0° (circle, red corner, black corner) at t0 and t12, both widths. **Ring moves:** jewel deltas ~55–56° over 12s (78s orbit), both widths.
- **Orb click:** intercepted navigations to the exact URL `https://nayanet.app/agreement` (2 hits per width — the navigation request + its retry after the abort; both the exact URL), both widths.
- **Cover (staged /agreement):** cover active, choice null, preview strings 0/0/0; poster 1000×750, `object-fit:contain`, `object-position:50% 50%`; facade 1, below the frame, covers-poster false; audio hidden, no controls, duration 258.15s, readyState 4; `tDur` 4:18; transport [Back 15 seconds, Play, Stop, Forward 30 seconds]; ON AIR / NAYA POWER RADIO; LET'S GO present. Screenshots `r6e-phone-cover.png`, `r6e-desk-cover.png` — the visual shows whole and centered, nothing covering it, the play button below it in the clear space.
- **Facade click → video:** iframe present, src `https://www.youtube.com/embed/a06pPpxRil4?autoplay=1&mute=0&playsinline=1&rel=0&enablejsapi=1`; frame `.playing`; facade hidden; status ON AIR. Follow-up `evidence/probe-r6e-video.py`: the deck clock advances after the click (0:00 → 0:02 → 0:04), proving playback; the video stream (`googlevideo.com/videoplayback`) flows. Sound itself is not audible in a headless probe — the player is unmuted (`mute=0`, `unMute` posted) and the audio recording's duration/transport are proven; stated plainly, not claimed heard. The earlier "PAUSED" frame in the +4s screenshot was transient buffering through the proxy. One source quirk: the deck total flips between 4:18 and 4:19 (audio 258.15s vs video 259s — a one-second difference in the source material).
- **27 slides:** Forward ×26, order_ok True, both widths — The Old Way → … → Your Franchise, exact order (titles 25/26 use curly apostrophes in the source, as the file has them).
- **End slide:** deed verbatim True; Agree "I agree ◆", animation `agreeFlash`; agree bottom 552 vs arrows top 558 (phone), 712 vs 718 (desk); 0 links on the slide; all 8 links in the bar below the page; bar after arrows, row before arrows; Agree visible in the viewport. Screenshots `r6e-phone-endslide.png`, `r6e-desk-endslide.png` — the layout is exactly the settled one.
- **Agree click:** intercepted `https://nayanet.app/?from=agreement` (the `#userName` fragment is client-side only — Playwright's request URL never carries it; the return leg confirms the full `/?from=agreement#userName` URL). Flag set (`2026-11-26T16:40:08.528Z` phone, `16:42:10.263Z` desk). Return: name input present + visible, stage off, flag persists. **Reload: stage off, view `intro`, flag persists, no modal — the agreement does not re-appear.**
- **Page errors:** 2 console.error "Failed to load resource: 404" (one per width) — both are the **favicon** (curl confirms staged `/favicon.ico` → 404; the portal has no favicon; same artifact as R6). Zero non-2xx requests on the staged `/agreement` load. The other `requestfailed` entries are the intentional route-aborts (my interception) and YouTube requests cut when the probe navigated on. **0 page errors on the staged portal/agreement themselves.**

**R5 items re-proven — `evidence/probe-r6e-r5.py`, log `evidence/r6e-r5-log.json`, 0 page errors:**
- Portal story (via `__fpOpenStory`): 27 slides, exact order (25/27 string-equal to my ASCII list; the other 2 are the curly-apostrophe titles, as the source has them), end-slide agree "I agree — show me my world ◆", 8 links. Screenshot `r6e-desk-story-end.png`.
- Certificate link: entry-form submit intercepted → `https://nayanet.app/identity.html?name=R6eCheck` (×2). Staged `/identity.html` renders the new cert (title "NayaNET — Smart Identity Activation", `/?walk=1` present).
- Returning view: alias `r6check01` stored, reload → returning True, "Welcome back, R6Check.", deed hidden, jump visible, form hidden. Screenshot `r6e-phone-returning.png`.
- **Nine destinations: 18/18 land** — desk 9/9 (`probe-nine-r6.py`: Home, How It Works, Innovations, 12 Elements, Skills, The Grand Mission, Powercast, Academy, Pricing, each on its exact href with the right title) and phone 9/9 (`probe-nine-r6-phone.py`, the fixed copy — `probe-nine-r6.py`'s phone leg still carries the known `{bubbles:true}` f-string bug and errored on all 9; the fixed phone file proves them).
- Menu hover/tap-tap: covered by the nine-probe (the tap-tap path is how the 9 phone destinations land) + the loop probe's rest state (0 labels, 9/9 tips opacity 0).

## §11 check (in writing)

- **§1 (one law, one language):** the portal speaks the R5 language unchanged; the agreement file is the v25 file edited, not rebuilt; the new CSS uses Marcellus 19px white for the deed text and the links label — the text laws.
- **§2 (text):** the deed text on the end slide is 19px Marcellus white; the orb's label is unchanged. Design-law checker: portal **81 violations + 4 warnings, identical messages to the R5 baseline** (only line numbers shifted) — zero new. Agreement file: **29 → 27 violations** (two fewer 13px violations — they were in the removed choice CSS), zero new, 0 warnings.
- **§3 (real objects):** the orb is a real object (obsidian ball, bright energy ring, breathing halo, drop-shadow glow, alive on hover); the play button is a real disc below the picture; the visual is a whole photograph, not a crop.
- **§4 (one light, top-left):** unchanged from R5/v25.
- **§5 (no flat):** nothing added is flat — the ring, the halo, the flashing Agree glow.
- **§6 (three boards, then a button):** unchanged (letter, three at a time); the end slide holds the deed text and then the Agree button — nothing else.
- **§7 (frame library):** the agreement frame is the v25 file's own frame, harvested, not redrawn; the portal frame is R5's.
- **§8 (alive on hover):** the orb ring orbits (12s), the halo breathes (4s), LET'S GO pulses, Agree flashes; the page ring orbits (78s).
- **§9 (2 seconds):** the agreement opens on the player immediately; LET'S GO is one tap to slide 1; the deed + Agree are pinned at the bottom of the end slide.
- **§10 (no text below 17px added):** the only new text is 19px; the 81/27 violations are the pre-existing base, unchanged in kind.
- **§11 (the check):** this report is the check — every claim above carries its receipt (bytes, shas, logs, screenshots read with my own eyes). The checker must still walk it live; Shawn's eye is the final gate.

## Live step (the captain's — not mine; nothing live from this round)

1. **Portal:** put the R6e portal (13,887,202 B, sha `01051a8f…`, blob `50b6733d…`, commit `fb721c5d…`) live at nayanet.app (replacing the old v2 build, 1,189,401 B, sha `e6207257…`).
2. **Agreement:** R2-PUT `agreement-v25-fixed-r6.html` (22,935,043 B, sha `410078e1…`, blob `20fd336b…`) to R2 bucket `nayanet-covers`, key `agreement-v25.html` (replacing the v25 file, sha `2c88513f…`). Worker `nayanet`'s `/agreement` branch (`env.COVERS.get("agreement-v25.html")`) serves it unchanged — no worker change. Do NOT worker-PUT the 23 MB file into the `nayanet` router (it would destroy the router). Local copy for the PUT: `~/workspace/team-nitro/portal-frontpage-fix-20261125/round-6/maker/agreement-v25-fixed-r6.html` (also filed on GitHub, blob `20fd336b…`, verified decode == bytes + sha).
3. **Certificate:** put the NEW cert (315,409 B, sha `0c11fdb8…`, blob `8f08d3de…`) live at nayanet.app/identity.html (replacing the 310,386 B live cert, sha `1b721d5c…`).
4. **Checker proves on the LIVE URLs after the live step:** opening https://nayanet.app/agreement lands directly on the welcome player (zero preview), LET'S GO → slide 1 "The Old Way", all 27 slides in order, end slide deed + Agree at the bottom → back to the name entry; the portal orb → the exact URL; the cert → the new bytes; the walkthrough gap (above) is a separate build.
5. **Serving path (grounded):** live `https://nayanet.app/agreement` = R2 bucket `nayanet-covers`, key `agreement-v25.html`, served by worker `nayanet`'s `/agreement` branch; zone route `/agreement*` → worker `nayanet`. Staged `https://portal-frontpage-fix-20261125-r6-staging.nayapower.workers.dev/agreement` = KV `WELCOME_ASSETS` key `agreement-v25-r6.html`, served by the staging worker's `/agreement` route.

## Carried items (pre-existing, named not hidden)

- Walkthrough backend `/api/welcome/complete` 404 (ends "Almost there") — pre-existing, not my scope.
- Phone end-slide franchise box/orb below the fold on arrival (R3 HOLD) — unchanged.
- Letter boards scroll internally (as R5).
- The cover screen scrolls on phone: the visual frame fits whole in the viewport, but the audio panel + LET'S GO sit below the fold (one short scroll). On desk the saying + cover-N orb sit just below the fold. The visual — the thing Shawn complained about — is whole, centered, and playing; the screen's scroll behavior is the v25 file's own.
- The end slide's board text scrolls under the fixed deed row (the deed + Agree are pinned at the bottom, as ordered; the slide's own text is reachable by scrolling the panel).
- The deck total flips 4:18/4:19 (audio 258.15s vs video 259s — a one-second difference in the source material).
- The portal's in-place letter view is now a fallback only: the staged `/agreement` serves the v25 file, so the portal's `/agreement` boot never fires on staging or live. The letter view code is untouched.
- The intro/bridge "Read the agreement" pills (`#fpChoiceLetter`, `#fpBridgeLetter`, `#fpNextBtn2`) are untouched — they are post-name-entry walk flow, not front-page entries, and are out of the correction's scope. They navigate to relative `/agreement`, which now serves the real agreement file.
- `/agreement-landing` (302 to the onboarding landing) stays in the worker — the front page no longer uses it; it is not an entry.
- No test certificate or alias was deleted. Deletion list (on Shawn's go-ahead only): `r4check26`, `r4check27`, `r2check25`, `r5check01`, `r6check01` (the last two are localStorage-only test aliases; `r6check01` was stored via `/?walk=1&alias=r6check01&name=R6Check`).

## Files (lane `~/workspace/team-nitro/portal-frontpage-fix-20261125/round-6/maker/`)

- `portal.html` (R6e, 13,887,202 B, `01051a8f…`), `portal-r5.html` (base), `agreement-v25-fixed-r6.html` (22,935,043 B, `410078e1…`), `identity.html` (NEW cert, 315,409 B, `0c11fdb8…`), `identity-consolidated.html` (OLD cert, 313,224 B — kept in the lane, no longer served), `sw.js` (567 B, `abac2ab5…`), `worker-consolidated.js` (14,226,407 B, `19851052…`), `worker-meta.json`
- `build-fix-r6e.mjs` (36/36), `build-agreement-v26.mjs` (all V), `build-worker-r6e.mjs`, `verify-r6e.mjs` (all PASS), `commit-r6e.mjs` (commit `fb721c5d…`)
- `evidence/`: `portal-diff-r6e.txt` (raw, 1.5 MB), `portal-diff-r6e-readable.txt`, `transform-r6e.cjs`, `kv-put-r6e.py`, `design-laws-r6e.txt`, `design-laws-r5.txt`, `design-laws-v25.txt`, `design-laws-v25-orig.txt`, `probe-r6e-loop.py`, `r6e-loop-log.json`, `probe-r6e-video.py`, `probe-r6e-r5.py`, `r6e-r5-log.json`, `probe-nine-r6.py`, `probe-nine-r6-phone.py`, `r6e-*-front.png`, `r6e-*-cover.png`, `r6e-*-playing.png`, `r6e-*-slide1.png`, `r6e-*-endslide.png`, `r6e-*-after-return.png`, `r6e-desk-story-end.png`, `r6e-phone-returning.png`, `r6e-phone-video-state.png`
