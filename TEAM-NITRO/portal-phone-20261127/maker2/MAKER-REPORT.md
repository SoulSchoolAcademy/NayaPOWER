# MAKER REPORT — Black Diamond phone v2: collapsed walk + checker D1–D7 + eye fixes (2026-11-27)

**Staged link:** https://portal-phone-v2-staging.nayapower.workers.dev/
**Phone path:** staged link + `?walk=1&name=Shawn&alias=shawn` (certified alias — the staging backend 404s uncertified aliases; see open item 3)
**Base:** v1 phone portal (13,900,396 B, sha `b7ee02d6…`), itself on the R5 base (13,883,771 B, sha `d4bb2102…`). A byte-identical copy of the v1 portal is kept in this lane as `portal-v1.html`.

## What was built

The walkthrough is rebuilt to Shawn's ~10:0x collapsed flow (MEMORY.md — supersedes the v1 brief's three location screens and the R5 15-question list). **17 steps, personal first, deep stuff at the end, categories LAST, no Skip anywhere:**

1. Where do you live — country + province/state + city in ONE box
2. Age + language — ONE box (age groups, never a specific age)
3. Gender — dropdown (male / female / prefer not to say), NO default (+ faith + ethnicity optional, same box, R3 harvest)
4. What you love — three boxes one after another: brand / music type / hobby + what else you love
5. Sports — type-of-sport dropdown, then your team under it
6. Who do you want to connect with — dropdown + your own words (picture 6 Smart Match)
7. Industry + skills — check-off dropdowns (industry select, skills chips, something-else)
8. Your experience — experience / achievements / education in ONE box
9. The model — how your world should work
10. Vision — picture 3 Nanoverse (our example: R5 vision, verbatim)
11. Goal — picture 1 The Vault (R5 goal)
12. Mission — picture 4 How Naya Works (R5 mission)
13. Your thing — picture 7 Auto Organizer (R5 thing)
14. Values — what you stand for — picture: the five glowing crystal pillars (R5 values)
15. Your promise — picture 5 Smart Vault (R5 declaration)
16. What's in it for you — picture 2 How Current Works (R5 help)
17. Categories LAST — click off, then subcategories under the ones picked (R3 harvest, verbatim)

Pictures are harvested verbatim from `workspace/user/media_library/image/` (filenames carry the typos: `2_HOW_WE_SNYC`, `7_AUTO_ORGINIZED`) and embedded as data URIs — no invented pictures. The picture renders full-frame in the 9:16 stage above the ball on input (flex-fill, 586px tall at 390) and compact above the reveal card. The ball IS Enter (reveals in place with your answer + our example); only the ‹ › arrows navigate. Answers save as you go (same key `naya_welcome_right_v1`); the review screen copies every answer out.

**Checker D1–D7 — all fixed and re-proven by real taps:**
- D1 ball vanishes on the end screen — `finish()` no longer hides `enterBtn`; the ball + ENTER stay on the end screen (probed visible).
- D2 end screen sliced at 390 — end screen rebuilt as a tight 2-column grid with a "Welcome home." title; every destination button measured whole inside the 9:16 screen.
- D3 Skip pill wraps — NO Skip anywhere (his ~10:41 count: no skip button; click forward to advance). The element stays in the DOM hidden because `finish()` still touches it; there is no handler and no pill.
- D4 jewel reads as sunburst rays — rebuilt as an SVG facet map: central octagon table + 16 chunky triangular crown/pavilion facets, deep purples, N upright, spin on the facet layer only (18 polygons, probed).
- D5 frame ring reads as striping — 12 discrete 30° conic facets, alternating light/dark chrome.
- D6 phone 897px in an 844px viewport — 831.5px at 390 (ball 92, tight chin); ENTER visible on arrival, no scroll.
- D7 reveal card is an empty white slab — cards size to content; the picture fills the stage instead.

**Eye verdict (v1) findings in this lane — all fixed and re-proven:**
- EYE-1 phone overflows at BOTH widths (1,145 in 900 at 1440) — the phone is now viewport-capped: `#fpWalk{max-width:min(560px,calc((100vh - 280px)*0.5625 + 48px))}`. At 1440×900 the phone is 845.1px tall, ball + ENTER at 795px, reachable without scrolling; XL (560) returns on tall viewports.
- EYE-2 Q18 example clipped mid-line — on reveal the stage scrolls so the whole reveal card (question + answer + our example) sits inside the 9:16 area; probed card box wholly inside stage box on the vision step; reveal picture is compact (16/8, max 150px) so the card fits.
- EYE-3 stray `Unexpected token '<'` at 1440 — hunted, not reproduced: 0 page errors at both widths across two full probe runs (390 full walk + 1440 fast walk to complete). The only console noise is the known forwarder cert artifact on fonts.googleapis.com (same as v1 checker). The one real failed request seen during the hunt was the staging backend's `POST /api/welcome/complete` 404 for the uncertified alias `tester` (see open item 3) — a backend gate, not a page error.
- EYE-4 reveal is text-only — pictures now render full-frame in the stage on all seven picture steps (probed `naturalWidth > 0` + 586px tall at 390 on vision).

**Real bug found by the probe and fixed:** step keys `gender` and `connect` collided with field ids of the same name, so the step summary overwrote the field's own answer (`"gender": "Male or female: Female"`). `collect()` now writes the summary only when no field owns the step key; `finish()` still counts those steps via the field value.

## Base + diff (exact)

| Item | Value |
|---|---|
| v1 base | `portal-v1.html`, 13,900,396 B, sha256 `b7ee02d6177628e5700ae57f819cb7e87f532689245cf639e6d228b080559ee0` |
| R5 base | `portal-r5-base.html`, 13,883,771 B, sha256 `d4bb2102279838984db558e87cec4a977e4782ed22e5a2cc98be70f28e00b86b` |
| Built portal | `portal.html`, 22,107,028 B, sha256 `523a6844df4bb508529da2386fc6d825360130352d0d3473106e340852085e70` (+8,206,632 B vs v1 — the 8 harvested pictures, ~8.2 MB base64) |
| Certificate | byte-identical, sha256 `57bdd3873f65104f3ee6f4648cfec4a1a556a78ea8b7fb57153cd49da528af4b` |
| Branch | `portal-frontpage-fix-20261125-r5-phone-v2` (from v1 branch head) |
| Commit | `f1652863a18f3fc6f178bc3d6f8e8bf4fd661aee` (+ correction commit below for the worker sha in this report) |
| Portal blob | `221c77588d73e5e291d049ce2fe022ae0c2b1238` (blob-API read-back verified: decodes to 22,107,028 B, sha `523a6844…`) |
| Worker | `worker-consolidated.js` 22,445,919 B, sha256 `72859d1d3334ba6c41511aba506292d7e72bc91c9ae11e15e0792daf2476dffa`; worker `portal-phone-v2-staging`, subdomain enabled, HTTP 200 |

**Splices (all in `portal.html`, nothing else in the v1 portal touched):**
1. Walk `<section id="fpWalk">` swapped whole for the v2 phone markup (SVG jewel, `#bdPic` + `#bdFields`, hidden Skip, 2-column end grid).
2. Phone `<style>` swapped whole for v2 (12-facet ring, smaller ball/chin, vh-capped width, full-frame picture, compact reveal picture, check chips white-unhighlighted / purple-highlighted, no-Skip).
3. Phone `<script>` swapped whole for v2 + 8 harvested pictures embedded as data URIs. (Build bug caught by the probe: the placeholder line kept a literal `{}` after the injected object — `window.BD_PICS = {...}{};` — which failed the whole phone script to parse and left the ball dead. Fixed to `window.BD_PICS = {...};` and all three spliced scripts now pass `node --check` before deploy.)
4. `QUESTIONS` replaced with the 17-step collapsed flow (`steps.js` — R3 field options + R5 example answers harvested verbatim; connect example is ours, in plain words).
5. Walk engine replaced (`engine.js` — `var idx = 0;` … `function complete(){`): multi-field renderer (text/select/checks/subs), per-field save-as-you-go, ball reveals, Next/Back navigate, no Skip handler, `render()` at the end.
6. `finish()`: the `enterBtn.hidden = true;` line removed (D1). `complete()` / verify-before-declare untouched.
7. `build-v2.mjs` asserts 26/26 (ran clean, exit 0).

**Files filed to the branch:** `portal.html`, `portal-v1.html`, `portal-r5-base.html`, `identity.html`, `identity-consolidated.html`, `worker-consolidated.js`, `worker-meta.json`, `sw.js`, `build-v2.mjs`, `build-worker-v2.mjs`, `verify-v2.mjs`, `commit-v2.mjs`, `phone-section2.html`, `phone-style2.html`, `phone-script2.html`, `steps.js`, `engine.js`, `MAKER-REPORT.md`, `evidence/probe-v2.py`.

## Verification (real taps)

Build: 26/26 assertions in `build-v2.mjs`, exit 0. Worker build clean. Staged: `verify-v2.mjs` — 23/23 PASS, staged bytes == lane bytes + sha (portal sha `523a6844…`), identity unchanged.
Browser (Playwright Chromium via the localhost forwarder): **60/60 PASS** (`evidence/probe-v2.py`, run twice — second run ALL PASS) — 390×844 + 1440×900, 0 page errors at both widths (forwarder cert artifact excluded, checker precedent), real taps through all 17 steps: one-box location, age+language, gender with NO default, three favorites boxes, sports type+team, connect with picture, industry+skills check-off (chips read purple `rgb(142, 36, 170)` when checked), resume, model, vision with full-frame picture, Back keeps answers, all answers in localStorage key `naya_welcome_right_v1`, full walk to the end screen at both widths (certified alias `shawn`), ball visible on the end screen, Copy my answers flips to "Copied".
Screenshots: `evidence/v2-390-reveal-q1.png`, `evidence/v2-390-reveal-vision.png`, `evidence/v2-390-end.png`, `evidence/v2-1440-reveal.png`.

## Design-law check (§11)

- §1 real objects: frame (12 discrete facets), chin, SVG-faceted jewel ball, arrows, cards all layered with depth + down-right shadow; alive on hover (lift + purple glow outside), press scale 0.97; orbit ring 120s slow. The jewel and ring now read as faceted objects, not ray/striping pictures — D4/D5 closed.
- §2 text: Marcellus, white, 25/19/17, nothing under 17px; no gray text. One brief-ordered exception, carried from v1: the input/reveal card is the reference phone's own white-light card (black Marcellus text on white).
- §3 color: deep palette only — royal purple `#8e24aa` ball/rims/glow/chips; white/black/chrome hardware. No gold light-ups: unhighlighted white, highlighted purple (probed).
- §4: one light top-left 135°, shadows down-right, inside board black `#050607`, no glow inside. (The jewel's specular highlight is the gem's own light play, as in the reference.)
- §5/§6: obsidian pill/circle buttons with own-color rims; one idea per screen; nothing sliced mid-glyph at rest (end grid + reveal card both probed inside the stage).
- §9 auto-optimization: the phone now fits the viewport it is viewed in (831.5 in 844 at 390; 845.1 in 900 at 1440) — nothing below the fold on arrival.
- **Known deviation, named:** desktop width is viewport-capped (~365px at 900h) rather than the brief's XL 560 — the eye's fit order and §9 require the phone inside the viewport, and 560px cannot fit in 900px tall with the chin. XL returns automatically on tall viewports (min() rule).

## Still open

1. **Shawn's eye is the final gate** — staged only, nothing live, nothing to Shawn from this round.
2. **Backend acceptance of the new answer keys** — `complete()` succeeds end-to-end on staging for the certified alias `shawn` (world ready, 17/17). Whether the LIVE backend accepts the new keys (`country`, `province`, `city`, `age`, `language`, `gender`, `brand`, `music`, `sports`, `connect`, `industry`, `skills`, `categories`, …) is unproven — backend seat.
3. **The staging backend 404s uncertified aliases** — `POST /api/welcome/complete` returns 404 `{"error":"That alias is not certified yet — your certificate comes first, then this walk knows your name."}` for alias `tester` (and `/api/welcome/me` the same). The walk then shows its honest fail state ("your world isn't ready yet… Tap Try again"). This is the same "connection dropped" the eye flagged for another lane — the coordinator's backend lane, not this build. Any probe or citizen without a certificate hits it.
4. **NEW ORDER LANDED DURING THIS ROUND — needs a re-brief, NOT folded in:** MEMORY.md gained "WALKTHROUGH — THE 3D IPHONE" (voice call 2026-11-27 ~12:17–13:24 MST), which supersedes parts of the brief this round was built to: steps grouped in THREES of iPhones (country/province/city · age+gender · favorites · industry+subcategories, then the Naya video iPhone before motto · motto · mission/goal/vision · love/don't love/thing · education/work/experience · achievements/values/where-you-stand · unique/benefit/connect); three iPhones side by side on laptop, stacked scrolling on phone; the picture full-screen BEHIND the input (tap the picture to go to the input, enter flips to the picture); motto / love / don't-love / unique / gift steps return (this build drops motto, love, don't-love, unique, gift per the ~10:0x brief); values sits in two trios (unresolved, his word owed). This build satisfies the brief it was given; the trio layout is a substantial rebuild and cannot be folded into the remaining minutes of this round. The parent should re-brief it as the next round.
5. **No Naya video asset** — the end-sequence video does not exist (honest slot in the other flow, nothing faked here); the trio order puts a video iPhone before motto.
6. **Skills list is thin** — R3 harvested only four skills (Video editing, Logos, AI, System design) + a "something else" field. A fuller skills list needs his word or a harvested source.
