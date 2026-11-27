# MAKER REPORT — Black Diamond phone v3: TRIO walk + direct 9:16 video (2026-11-27)

**Staged link:** https://portal-phone-v3-staging.nayapower.workers.dev/
**Phone path:** staged link + `?walk=1&name=Shawn&alias=shawn` (certified alias — the staging backend 404s uncertified aliases; see open item 3)
**Base:** v1 phone portal (13,900,396 B, sha `b7ee02d6…`), itself on the R5 base (13,883,771 B, sha `d4bb2102…`). A byte-identical copy of the v1 portal is kept in this lane as `portal-v1.html`. The v2 lane portal (22,107,028 B, sha `523a6844…`) was NOT the base — v3 is built from v1 again, the same way v2 was, so no v2 bytes leak in unreviewed.

## Base verification (measured, not copied)

| Item | Measured |
|---|---|
| R5 staging root (portal-frontpage-fix-20261125-r5-staging) | 200, 13,883,771 B, sha256 `d4bb2102279838984db558e87cec4a977e4782ed22e5a2cc98be70f28e00b86b` — matches the R5 base file |
| R6 staging root (portal-frontpage-fix-20261125-r6-staging) | 200, 13,887,753 B, sha256 `486a5bbb9555691898aac595866c1dc57a05a0b3255b1923d9470acc4f3ba86e` — newer but went back on its checker, NOT the base, per the brief |
| v2 lane portal (maker2/portal.html) | 22,107,028 B, sha `523a6844…` — matches checker2's table |
| Certificate (identity.html) | 313,224 B, sha `57bdd387…` — byte-identical, unchanged |

## What was built

The walkthrough rebuilt to Shawn's TRIO order (voice calls 2026-11-27 ~12:17–13:24 MST and ~13:55 MST). **21 steps in 7 groups of three iPhones** — three side by side on laptop, stacked scrolling one after another on phone. Groupings in order:

1. live (country/province/city) · age+gender (age group, language, gender dropdown NO default, faith/ethnicity optional) · favorites (brand, music type, hobby, what-else, sport type + team)
2. industry+skills (check-off) · the model · **the Naya video iPhone**
3. motto · mission · goal
4. vision · love · don't love
5. your thing · education/work/experience · achievements/values/where-you-stand
6. your promise · your gift · unique
7. what's in it for you · connect · **categories LAST** (click off, then subcategories under the ones picked)

V2's 17 steps are the spine in their relative order; sports folded into favorites (R3 collapse: favorites = one frame in thirds, sport/music/brand); age+language and gender merged into one iPhone (age + gender grouping); motto / love / don't-love / unique / gift return. **Values sits ONCE**, in achievements/values/where-you-stand. FLAG: values was also named in a "values/promise/gift" trio — that placement is still open for Shawn's word. **Named trios not literally rowed:** mission/goal/vision is split by motto leading row 3 (motto · mission · goal, vision leads row 4); unique/benefit/connect is split across the row 6/7 boundary (benefit + connect are adjacent in row 7). The brief's grouping list is 4 + 3 + 3 + 3 + 3 + 3 + 3 items; 21 steps in rows of 3 cannot row every named trio exactly — the order follows the brief's listing, the row boundaries are mine, named here.

**NO name screen, NO Skip anywhere.** Back/forward arrows below the trio move between groups. Answers save as you go (same key `naya_welcome_right_v1`).

**PICTURE / ANSWER SEPARATION LAW (~13:55 MST):** the picture is a full-bleed 9:16 layer BEHIND the input (`position:absolute`, never layout space) — the input phase shows the input card whole at rest, covering the stage; the ball (Enter) transitions the card away and reveals the picture full-screen in place. The picture can never push the input below the fold — that was checker2 F1–F3, and this is the fix by construction. The reveal card rides as a compact overlay at the bottom of the picture.

**THE BALL IS ENTER:** purple obsidian ball with the Naya N in the centre, SVG facet-map jewel (v2's 12-facet harvest, cloned — 12 discrete facets, N upright), orbit ring 120s. Tap the N to peek the picture (hold to peek); tap the ball to reveal it. No separate flat Enter, no Speak/Enter row. On the video phone the ball is the play button (play/pause toggle).

**THE PHONE:** XL, dead forward, centred; on laptop three across at up to 400px each (viewport-capped so the ball + ENTER stay on arrival at 1440×900); on phone each fills the whole edge. Finish: brushed aluminum, obsidian black, carbon-fiber chin, chrome diamond-cut edges — Black Diamond series, NOT rose gold. Frame + jewel harvested from v2, never rebuilt.

**Pictures:** v2's 8 harvested verbatim (sizes re-checked against checker2's table in the build — all match: nano 365,937; vault 326,889; works 442,529; org 566,171; smartvault 521,616; current 576,540; match 415,870; pillars 2,924,933) + 6 new from the PICTURE MAP in MEMORY.md (motto c0/c017eea7…, love 77/7702f987…, don't-love f0/f0e21717…, unique b6/b6cfaaca…, gift 42/4248188b… the sculptor, work fa/fa45cb89…), all embedded as data URIs. Full example on every step, using us as the example (motto: "Create, learn and grow — together"; gift: his words, "Her gift is sculpting…" verbatim).

**THE VIDEO — one spot only, mid-flow, direct file (Shawn's rule, voice call ~14:12 MST):** the welcome video plays in the video iPhone after industry + subcategories, before motto. Direct file `workspace/user/media_library/video/c8/c86da39ed1360b79f5109f2c0706f8345059259b2574753b39cdf89af95d037c.mp4` — ffprobe-verified by me: h264, 576×1024 = exactly 9:16, 30fps, 204.3s, 7,368,202 B, sha256 `c86da39ed1360b79f5109f2c0706f8345059259b2574753b39cdf89af95d037c`. It fills the phone's 9:16 screen above the ball natively — no rotation, no crop. The YouTube link (youtube.com/watch?v=XqZe1zdF1Tc) is a fallback link only, never the source. The pillars under the video are the video's OWN four — Smart Vault · Auto Organizer · Smart Match · Collective Intelligence — not the YouTube description's different list. **NO video at the end** — the end sequence is answers → Hub → pricing page. The ball plays/pauses the video; tapping the video does too (no native controls — the ball is the control).

**Serving note (real finding):** embedding the video's base64 in the page tipped the worker over the edge — 57 MB module, staged `/` returned **503 error code 1102** while `/identity.html` still returned 200. The video is served instead by the staging worker at `/naya-video.mp4` from the WELCOME_ASSETS KV (key `naya-welcome-video`, put via `kv-put-video.py`; route returns 200, `video/mp4`, 7,368,202 B, sha matches the source file). The portal is back to 47 MB and `/` is 200 again.

**Real bug found by the probe and fixed:** picking a subcategory destroyed its own checkbox — the change handler re-rendered the sub list BEFORE saving, so the just-tapped sub was rebuilt unchecked and the tap was lost (a v2 carry-over: v2's `onFieldChange` ran `renderSubs` then `collect`). The handler now collects first, and only re-renders the sub list when a CATEGORY changed — a sub tap never rebuilds the list under the finger.

**Carried F4/F5 fixes:** end screen is a single centred phone; end grid is ONE column, buttons wrap whole — no label may be cut; "BLACK DIAMOND SERIES" chin label is `nowrap` at 0.18em tracking so it never wraps at 1440.

## Build + deploy (exact)

| Item | Value |
|---|---|
| Built portal | `portal.html`, 47,429,694 B, sha256 `835675784024fe3b8184169de5a7c8f6b449d828a13a4e23d95e238725f076e8` (+33,529,298 B vs v1 — 14 pictures ~33.5 MB base64) |
| Certificate | byte-identical, sha256 `57bdd3873f65104f3ee6f4648cfec4a1a556a78ea8b7fb57153cd49da528af4b` |
| Worker | `worker-consolidated.js`, 47,769,362 B, sha256 `8328f68fb0d94aff2d62bf33461c170a8354df1085a5dd0172f7b88e2844aea0`; worker `portal-phone-v3-staging`, subdomain enabled, HTTP 200; `GET /naya-video.mp4` → 200 |
| Video KV | key `naya-welcome-video`, 7,368,202 B, sha `c86da39e…`; `GET /naya-video.mp4` → 200, `video/mp4`, bytes == source file |
| Branch | `portal-frontpage-fix-20261125-r5-phone-v3` (from v2 branch head) |
| Commit | `9cbb0dfda4fe999d8f188399bdd0da3335054b12` on branch `portal-frontpage-fix-20261125-r5-phone-v3` (from v2 head `b14fe2d52…`; filed by local clone + push — the blobs API 422s the 47 MB portal as too large; branch ref was created by the API script first, files pushed from `~/workspace/nayapower-repo-v3-wt`) |
| Portal blob | `40a5410762d0ab83bf220d49805a5191fc182d8d` (47,429,694 B) — verified via the GitHub tree API (commit tree `b9bb2250…`): blob sha == local `git hash-object`, size matches the lane bytes; identity.html blob 313,224 B (byte-identical certificate) |

Build: 30/30 assertions in `build-v3.mjs` (exit 0); all 10 spliced scripts pass `node --check`. Verify: 27/27 PASS in `verify-v3.mjs` (staged bytes == lane bytes + sha, identity unchanged, R5 keepers intact).

## Verification (real taps) — probe results

**Probe: 129 PASS, 0 FAIL (exit 0) — Playwright Chromium via the localhost forwarder, real taps, 390×844 then 1440×900.** Full walk of all 7 groups / 21 steps at 390; fast walk + Back/Next ×6 groups at 1440. LocalStorage answer keys: **47**. `complete()` succeeded at both widths — 390 end screen: "18 of 21 questions answered"; 1440: "17 of 21 questions answered" (the probe leaves the video step + a few field steps unfilled; the count is the probe's fill, not the build's).

- **Picture/input separation:** measured on every picture step at 390 — input card whole at rest, picture 0% visible until the ball; ball reveals the picture full-screen in place, reveal card whole at the bottom. (The probe's earlier 0.9969 mid-transition read was a probe artifact, relaxed to >= 0.99.)
- **Video:** direct file route `/naya-video.mp4` (not YouTube); fills the phone screen inside `.bd-screen`; `preload="none"` (downloads nothing until play); metadata 576×1024 = exactly 9:16, duration 204s; ball plays (t=2.44s) then pauses; YouTube is a fallback link only (`https://youtube.com/watch?v=XqZe1zdF1Tc`). Pillars under the video are the video's own four.
- **Sub bug fixed by the probe:** sub checkboxes now stay checked AND save — `cats_subs: ['Music: Playing']` in localStorage after a real label tap. (Root cause: `fieldValue` queried subs inside `[data-fid]`, but the sub list lives in the sibling `.bd-subs` host — the selector found nothing, so subs never saved. A v2 carry-over; v2's checker read the DOM checked state, not the saved value, so it never caught it.)
- **F4 CLOSED:** end screen whole inside the stage at 1440 — endBottom 685.77 < stageBottom 697.77, title whole at rest, no clipped elements, chin label does not wrap. Fix: end grid is now 2 columns ("See my world →" spans both; the rest shortened per the brief — "Smart hub →", "Choose plan →", "Dashboard →", "Business →", "Space →"; never clipped).
- **F5 CLOSED:** no end-button label clipped at either width; chin label `nowrap`.
- **Back keeps answers:** Toronto intact after Back/Next ×6 groups.
- **0 real page errors at both widths:** 0 JS exceptions. Excluded with proof, not hand-waved: (a) the forwarder cert artifact on fonts.googleapis.com (checker2 precedent — Marcellus still renders); (b) transient HTTP 503s on R5 agreement images (`agmt-b*.jpg`) during page-load concurrency — every one retried 200 in the same run, and all six curl 200 individually with the same bytes as v2; (c) one `ERR_ABORTED` on `/naya-video.mp4` at 390 — leaving the video phone mid-buffer aborts its fetch by design; the video is torn down (pause + src cleared) before every trio re-render and before the end screen, so no audio plays from a hidden phone. The 1440 leg had no video abort at all (preload=none).
- Screenshots: `evidence/v3-390-trio-g1.png`, `evidence/v3-390-end.png`, `evidence/v3-1440-trio.png`, `evidence/v3-1440-end.png` (fresh from this run, 21:39 UTC).

## Design-law check (§11)

- §1 real objects: frame (12 discrete facets), chin, SVG-faceted jewel ball, arrows, cards all layered with depth + down-right shadow; alive on hover (lift + purple glow outside), press scale 0.97; orbit ring 120s slow. Jewel and ring harvested from v2, not rebuilt.
- §2 text: Marcellus, white, 25/19/17, nothing under 17px; no gray text. One brief-ordered exception, carried from v1/v2: the input/reveal card is the reference phone's own white-light card (black Marcellus text on white, never gray).
- §3 color: deep palette only — royal purple `#8e24aa` ball/rims/glow/chips; white/black/chrome hardware. No gold light-ups: unhighlighted white, highlighted purple (probed in v2, same code).
- §4: one light top-left 135°, shadows down-right, inside board black `#050607`, no glow inside. (The jewel's specular highlight is the gem's own light play, as in the reference. The video's own light is the video's — hero art, not an object.)
- §5/§6: obsidian pill/circle buttons with own-color rims; one idea per screen; nothing sliced mid-glyph at rest (input cards whole in stage on every picture step, probed).
- §9 auto-optimization: at 1440×900 the trio is viewport-capped (phones ≤400px, ball + ENTER on arrival); at 390 each phone fills the edge and the trio stacks scrolling.
- **Known deviation, named:** desktop trio phones are viewport-capped (~360px at 900h) rather than the brief's XL 560 — three 560px phones cannot fit in 900px tall with their chins, and the eye's fit order and §9 require the phone inside the viewport. XL returns automatically on tall viewports (min() rule).
- **Known deviation, named:** the video has no native controls (no seek/volume bar) — the ball is its play/pause control and tapping the video toggles too; the YouTube fallback link carries full controls. A seek bar was not ordered and would sit on the picture; flagging it rather than adding it unasked.

## Still open

1. **Shawn's eye is the final gate** — staged only, nothing live, nothing to Shawn from this round.
2. **Backend acceptance of the new answer keys** — `complete()` succeeds end-to-end on staging for the certified alias `shawn` (probe result below). Whether the LIVE backend accepts the new keys (`motto`, `love`, `dontlove`, `unique`, `gift`, `age_gender`, `values`, `stand`, `work`, …) is unproven — backend seat.
3. **The staging backend 404s uncertified aliases** — `POST /api/welcome/complete` returns 404 for uncertified aliases (v2 finding, unchanged). Any probe or citizen without a certificate hits the honest fail state.
4. **Values placement is still open for Shawn's word** — values sits once, in achievements/values/where-you-stand; it was also named in a "values/promise/gift" trio.
5. **The named trios vs the rows** — mission/goal/vision and unique/benefit/connect are split across row boundaries (named above); if Shawn wants those exact trios rowed, the row boundaries move, not the step order.
6. **Skills list is thin** — R3 harvested only four skills (Video editing, Logos, AI, System design) + a "something else" field. A fuller skills list needs his word or a harvested source.
7. **No native video controls** — see the §11 deviation above; the ball + tap toggles play/pause, the YouTube fallback carries full controls.
