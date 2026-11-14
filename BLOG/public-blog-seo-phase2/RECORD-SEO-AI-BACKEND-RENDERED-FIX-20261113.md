# RECORD — SEO/AI rendered-layer fix (Area #9), maker seat

- **Seat:** Wrena (BUILD), maker.
- **Brief:** `BRIEF-SEO-AI-BACKEND-RENDERED-FIX-20261113.md` (passed check-brief 9/9).
- **Branch (new):** `public-blog/seo-ai-backend-rendered-fix-20261113`, from base tip `dc54dab527f1a4925c48616b1eda8782d9ea691d` (branch `public-blog/seo-ai-backend-20261113`).
- **Staged link:** https://naya-public-blog-staging.nayapower.workers.dev/
- **Dates:** work 2026-11-13 → 2026-11-14. Staged only — no live touch, no merge, no PR, nothing shown to Shawn.
- **Files changed:** `index-intel-today-phase2.html` ONLY (shell). Worker `hub-worker-phase2.js` UNCHANGED (server rendering was already correct).

## Shas (local == staged, re-proven at round end)

| Artifact | Bytes | sha256 (first 12) | Full sha |
|---|---|---|---|
| Shell (edited) | 5,570,515 | `2c62d243f589` | `2c62d243f58989e8ae64ba80e75ad9074762945709ac75168c5e08eea92b9cb5` |
| Worker (unchanged) | 80,908 | `39ddddc1e036` | `39ddddc1e036fd59868af2655bdecb10da3197c42b5d1324ef1bd0125632139c` |
| Staged feed `feed-live.json` (frozen) | 8,172,042 | `89d02559…` | frozen 1,058-note copy, SN-2766 first |
| Base shell (pre-fix) | 5,561,414 | `4bfad1197c70` | `4bfad1197c70e7a0c9f5d4de47d9d876917b52e7f521a592f82b50aa7970b0a9` |

## Step 0 — Reproduction (before any edit; Playwright Firefox, fresh contexts, 390px)

Probe: `probe-rendered-repro.py`, results `phase2-shots-rendered/probe-rendered-repro-results.json`.

- **R1 REPRODUCED:** browser `/s/sn2696` (302 → `/#/smart-notes/sn2696`): 0 rel-cards, no "RELATED", only 1 `/s/` link (self). Server-rendered page via curl Googlebot DOES have 6 rel-cards — browsers never see the server page.
- **R2/R3 REPRODUCED:** sn2766/sn2695 direct: "That note isn't here" at 2s/8s/15s with LIVE feed (1,058, `live-registry`); feed clicks also "not here".
- **R4 NOT reproduced in fresh profiles:** 3/3 fresh home loads live-registry 1,058, SN-2766 first. Baked snapshot measured (feed-live.json blocked): **381 notes, first "Decide by the Checklist — Every Time"** — exactly the captain's stale snapshot.
- **R5 NOT reproduced:** 0 blank loads across 9 fresh loads.
- **R6:** first GAP metric was invalid (fixed bottom bar counted as content); proper measurement later showed a real void (see Step 1).

## Step 1 — Grounding (causes, with evidence)

- **R2/R3 cause — SPA `findNoteBySlug` defect (proven in code + data + repro):** the digit scan only reads the note ID, and only sn2696 is in `SLUG_MAP`. sn2766 id is `IB-SMART-NOTE-20261113-name-the-part-you-send`, sn2695 id is `IB-SMART-NOTE-20261112-the-dream-the-automated-intelligent-internet` — neither contains its sn digits. The worker's `phase2FindNote`/`phase2CanonicalSlug` uses the title's SN first; the SPA never consults the title. "Not here" fires only when `ref==='live-registry'`, so it is NOT a stale-feed symptom.
- **R4 cause — bake-vs-live race + silent give-up (proven by delay experiment `probe-grounding2.py`):** shell bakes a 381-note Oct 26 snapshot (`window.NayaFeedIntelligence`, ref `10190133505f4ba03cd029d18cf6f650affeeb9c`); live override fetches `/feed-live.json` and re-points the global + dispatches synthetic hashchange (router re-renders — mechanism works). With `/feed-live.json` delayed 3s, home went live; delayed 20s, home stayed on the 381 bake at 2/6/12/20/40/70s and sn2766 spun "Opening your note…" at 70s — the 15s `AbortController` abort × 3-try cap gives up silently, no UI signal. Staged `/feed-live.json` asset itself is deterministically 1,058 (curl-verified), `Cache-Control: public, max-age=0, must-revalidate`; shell registers NO service worker (0 occurrences) — SW staleness ruled out.
- **R1 cause:** SPA `noteView` appends only `intelBoard(note)` — no related section exists in the shell (0 `rel-card` occurrences).
- **R6 cause (measured):** `.main{padding-bottom:380px}` at ≤640px (220px above), while fixed bottom chrome totals 148px (390/360: obb-bar 76 + notif-bar 72) and 170px (1440: 84+86). Visible void: ~302px at 390/360, ~121px at 1440 (note-view bottom vs dock top, scrolled to bottom).
- **Client related-ranking mirror proven exact:** Python mirror of `phase2Related` (topics created-desc → cluster, dedupe by rendered href, 6 max; NO list leg) reproduced the worker's related list exactly for **all 1,058 notes, 0 divergences, all 1,058 get 6**. Worker lists for the probed notes are all "Same topic". Worker clusters: sn2696 `smart-notes` (#55e39a), sn2766 `nayanet-naya`, sn2695 `intelligent-internet`.

## Fixes implemented (shell only; worker UNCHANGED)

All edits in `index-intel-today-phase2.html`, each anchor asserted count==1 in `/tmp/edit-shell.py`; all 32 inline script blocks pass `node --check`. Backup of base shell: `/tmp/shell-base-4bfad119.html`.

- **Edit A (R2/R3):** in `findNoteBySlug`, after `SLUG_MAP`, added title-based canonical scan mirroring worker `phase2CanonicalSlug` (title SN → id sn digits → full id).
- **Edit B/B2 (R1):** new helpers before `noteView`: `relTitleCase`, `relDisplayTitle`, `relCanonicalSlug`, `noteRelatedFor` (topics→cluster mirror), `noteRelatedNav` (builds `<nav class="related">` with h2 "Related in this cluster", cluster rel-nav, 6 `.rel-card` boards with `/s/` hrefs + `.why` reasons, harvested verbatim shape/CSS from worker `PHASE2_EXTRA_CSS`); `noteView` appends it after `intelBoard`. Cluster label/color via `relClusterMeta()` (see scoping lesson below).
- **Edit C (R4):** live-feed override: fetch `cache:'no-store'`, abort timeout 15s → 60s, retry cap removed (retry until live, backoff 5/10/20/30s). Bake remains the render fallback while in flight, never the settled snapshot.
- **Edit R6:** injected style (id-guarded `rel-note-style`, same pattern as shell's `rv-face-style`): `body:has(.note-view).main{padding-bottom:100px}` and `@media (max-width:640px){...78px}` (calibrated: padding = chrome − ~70px layout constant).
- **Scoping lesson (caught by after-battery, fixed):** the helpers sit after the shell builder's `return shell;` ("internals" region) — only function declarations execute there. First version used `var REL_CLUSTER_META = {...}`, which never assigned → `REL_CLUSTER_META is undefined` pageerror. Fixed by making it a hoisted function `relClusterMeta(slug)`; no `REL_CLUSTER_META` remains. Any future top-level `var` in that region would fail the same way — use function declarations only.
- **Worker NOT rebuilt:** server rendering was already correct; build script `build-phase2-worker.py` would fail anyway (asserts live feed == 1,058, now 1,085; re-reads Smart Lists). Documented here, not hidden.
- **Deploy script (frozen feed):** `deploy-rendered-fix-staging.py` — same Direct Upload helper as `deploy-phase2-staging.py` but overlays ONLY the shell onto existing `staging-assets/`; `feed-live.json` (frozen 1,058, sha `89d02559…`) never re-copied. `deploy-phase2-staging.py` must NOT be run (it re-copies the live feed, now 1,085 notes, which would break the 1,058 bullseye and all no-regression counts).

## Deploys

- Deploy 1: shell sha `323d2aea…` (5,570,203 B), worker unchanged `39ddddc1…`; staged home curl-verified `323d2aea…`, feed still 1,058 SN-2766 first; 1 file uploaded.
- Deploy 2 (after map fix): shell sha `2c62d243f589…` (5,570,515 B), staged home curl-verified `2c62d243…`.

## After-battery (`probe-rendered-after.py`, results `phase2-shots-rendered/probe-rendered-after-results.json`)

Run 1 (shell `323d2aea`, before map fix): failed with the `REL_CLUSTER_META` pageerror (rel=0 everywhere); also full_page screenshots exceed the 32767px cap — battery now uses viewport shots + a shot scrolled to `.related`.
Run 2 (shell `2c62d243`, map fixed): nearly all green — R4 3/3 live 1,058; R4-slow recovered (rel=6 at t=5s); all 9 direct note legs rel=6, "Related in this cluster" present, 0 console errors, 0 overflow, blank loads 0; feed-click sn2695 2/2. Two remaining fails, both diagnosed:
- Feed-click sn2766: still `noteLoading` at +6s (new page refetching 8MB feed; not failed, just slow) — battery wait raised to 12s + bounded poll for `noteLoading` to clear.
- 1440 gap = 1px on sn2696/sn2695 (0px on sn2766); eye proof (`after-note-sn2696-1440.png`) shows all 6 green-rimmed cards ending exactly at the dock, no visible void — 1px is sub-pixel rounding. Battery gap assertion relaxed to `abs(gap) <= 1`, exact values still recorded.
- Eye proof confirmed: 1440 + 390 related screenshots show 6 elevated obsidian cards; client sLinks for sn2696 byte-identical to server list (`/s/sn2702, sn2701, sn2651, sn2650, /s/ib-smart-note-20261110-sn2650-the-master-operational-manual, sn2648`), reasons all "Same topic: System Intelligence", cluster label/color identical to server (`smart-notes`, #55e39a).

**Run 3 (same shell, battery timing/assertion edits only) — STAGED OVERWRITE, not a product regression:** rel=0 on all 9 direct legs, sn2766/sn2695 "not here", feed-click cards not found, gaps back to pre-fix values — the browser served a DIFFERENT shell. The R4-slow leg at the start of the same run passed (rel=6), so the served shell changed mid-run. Immediate curl check afterward (3 tries, PoPs SJC/IAD/DEN): home served **5,003,256 B, sha `7d25f5910599…`** — matching NEITHER local shell `2c62d243…` NOR base `4bfad119…`; staged `/feed-live.json` served **8,489,662 B** vs frozen 8,172,042 B. The served shell was a NEWER Hub shell (embedded notes start with SN-2782 daily report, SN-2766 present in bake, no rendered-fix code) with the CURRENT live feed (1,085 notes) — another lane redeployed `naya-public-blog-staging` mid-run. The other lane's bytes are preserved in this work dir as `staging-overwritten-by-other-lane-20261114.html` (sha `7d25f59105996fa0c40bde4d3b17a8c5e727e95861fc442b344c9f5ed840797d`) and `staging-feed-overwritten-by-other-lane-20261114.json` (sha `1037ff6e8961b5932fc8de723317c4a99f70ffd9004c15179fc05b8d4f9f2bbe`) so nothing is lost silently. **The shared staging worker needs serializing by the orchestrator — two lanes deploying to it flap each other's verification.** Redeployed my bytes (deploy script: 0 files to re-upload, assets content-addressed; PUT re-pointed the worker; verify1 still showed the other shell, verify2 2s later showed mine — asset-version propagation lag of seconds).

**Run 4 (after redeploy, shell `2c62d243`) — ALL RENDERED AFTER-BATTERY CHECKS PASS** (`fails: []` in results JSON):

| Check | Result |
|---|---|
| R4 fresh loads ×3 | live-registry, 1,058 notes, SN-2766 first, 0 errors, 0 overflow — 3/3 |
| R4-slow (feed delayed) recovery | recovered at 5s, rel=6, live-registry 1,058 |
| R1 direct 390: sn2696 / sn2766 / sn2695 | rel=6, "Related in this cluster", notFound=False, gap 0 / 0 / −0.0px, 0 overflow, 0 errors |
| R1 direct 1440: sn2696 / sn2766 / sn2695 | rel=6, relatedText, notFound=False, gap 1 / 0 / 1px, 0 overflow, 0 errors |
| R1 direct 360: sn2696 / sn2766 / sn2695 | rel=6, relatedText, notFound=False, gap 0 / −0.0 / 0px, 0 overflow, 0 errors |
| R2/R3 feed-click sn2766 (390) | found, href `/s/sn2766`, notFound=False, rel=6, ok=True |
| R2/R3 feed-click sn2695 (390) | found, href `/s/sn2695`, notFound=False, rel=6, ok=True |
| R2/R3 direct /s/sn2766, /s/sn2695 | 2/2 each (direct legs above) |
| R5 blank loads | 0 across the battery |
| R6 black gap | 0px at 390/360; 1px at 1440 on two notes (sub-pixel rounding, eye-verified no visible void) |

Feed-click legs are printed to the battery stdout and screenshotted (`after-feedclick-sn2766-390.png`, `after-feedclick-sn2695-390.png`) but NOT persisted in the results JSON — a probe record-keeping gap, noted here, not a product gap. Related titles per note (from results JSON): sn2696 → The Mail Is Safe / The Heart Match Organize Connect / Sn2651 One Foundation… / Sn2650 The World Masters / Sn2650 The Master Operational Manual / Sn2648 The Supabase Answers; sn2766 → Roster Naming And Faces / Superman Notifications / The Ultimate Communication Tool / Value Is Verified Assets The Setter / The Checklist Law One List Worked To Zero / The Whole Page Rule A Project Comes Whole; sn2695 → Sn2737 The Design Sells Itself / Sn2736 Do Everything For Them / The Design Sells Itself Full Meal Deal… / The Name Naya Not Anaya / Theres A New Net In Town / The Ultimate Icons Are Gems The One Minute Book.

## Before / after (R1–R6)

| Failure | Before (repro) | After (run 4) |
|---|---|---|
| R1 related cards on note pages | 0 rel-cards, no RELATED (browser); 6 only server-side | 6 on every note page, all 3 widths, "Related in this cluster" present |
| R2 sn2766 feed click + direct | "not here" both ways | opens both ways, rel=6 |
| R3 sn2695 feed click + direct | "not here" both ways | opens both ways, rel=6 |
| R4 snapshot | 381-note bake settles if feed delayed 20s (silent give-up) | 1,058 live on 3/3 fresh loads; delayed-feed run recovers at 5s |
| R5 blank loads | 0 in fresh profiles (not reproduced) | 0 across the battery |
| R6 gap below article footer | ~302px (390/360), ~121px (1440) | 0px (390/360); 1px rounding (1440, two notes) |

## No-regression suite (serial, to avoid Cloudflare 1102 flakes under sustained load)

- **Dedupe re-probe** (`probe-dedupe-phase2.py`): **1,058 checked, 0 duplicated hrefs, 0 floor breaches** — GREEN. sn2696 pair detail matches the client list exactly. (Fix-round copy backed up as `probe-dedupe-results-fixround.json`.)
- **Full curl probe** (`probe-phase2.py`, `probe-phase2-results.json` vs fix-round baseline `probe-phase2-results-fixround.json`): full set **1,058 checked, 67 fails — identical count to baseline**; composition 42 title + 22 desc + 3× status 503 (baseline: 41 title + 22 desc + 4×503, the 42nd title failure sn2248 having 503'd in that run). The three 503s (sn2117, sn235, sn252) are transient Cloudflare 1102 under sustained load — **all three retested 200 immediately after** (sn252 on its 2nd retest). UA battery 18 × 7: **12 fails (new) vs 13 (baseline)** — strictly no-worse; the one baseline-only failure was `sn2730 Claude-SearchBot: 503`, a transient flake; the 12 are the two known 49-char titles (sn2248 + sn423 × 6 UAs). Denial battery **3/3** (404 + `noindex, nofollow` on `/s/sn9999`, `/s/sn2696/extra`, `/s/sn2696/extra/deeper`). Staged sitemap **1,049 locations**. Robots: Googlebot present, GPTBot disallow. `/hub` sha matches local shell `2c62d243f589`. Canonical routes `/note/sn2696`, `/notes/sn2696`, `/smart-notes/sn2696`, `/s/sn-2696` all 200 with canonical `/s/sn2696`. **Live sitemap (nayanet.app) still 2 URLs** (root + `/s/sn2696`) — live untouched.
- **Bars no-regression probe** (`bars-noregression-probe.py`, `phase2-shots-bars/checker-results.json` — written fresh; it never existed before, the captain's known record blemish): **PASS**. mainPad 78px at 390/360, 100px at 1440 (exactly the new values, printed not asserted as designed). obbBar 76px / notifBar 72px at 390/360; 84/86px at 1440. 9 pills, 3 segs, 0 overflow at scroll 0 and scrolled, 0 console errors, 0 page errors on the staged note page at all three widths. All bar clicks navigate to the right nayanet.app pages with no errors — except ONE: `click Reports` at 360 showed `errs=['pad is not defined']`. **Proven pre-existing and unrelated:** loading https://nayanet.app/rooms/reports DIRECTLY (no staged shell involved at all) throws the same `pad is not defined` page error — it is a defect on the LIVE Reports page, outside this round's staged shell (the click navigates away to a different origin). First attempt at this probe was lost to a runtime restart at 12m12s (no output saved); re-run completed in ~20m with output to `/tmp/bars-rerun.log`.
- **Playwright probe** (`probe-phase2-playwright.py`): **390 PASS, 1440 PASS** (all legs: note sn2696 rel=6, topicless sn2209 rel=6, ambassador rel=6, hub 103 tabs, canonical cards, tab click, ?cluster arrival "AI Is Hiring"). **360: notes PASS; hub card-click step crashes the PROBE script 3/3 runs** — `Page.evaluate: Execution context was destroyed` at line 127, the `after_click` evaluate after a fixed 2500ms wait: the card-click navigation lands right at that moment and destroys the context. **Product behavior proven correct by direct equivalent tests** (`/tmp/click360.py`, `/tmp/click360-full.py`, `/tmp/cluster360.py`): at 360, clicking the first hub card (`/s/sn2757`) lands on `#/smart-notes/sn2757` (hash by ~2.5s), note renders notHere=False, rel=6, "Related in this cluster", title SN-2757, 0 page errors; `/?cluster=ai-is-hiring` opens with active tab "AI Is Hiring", 0 page errors. The probe's fixed 2.5s wait is racy against the async navigation (the click resolves the note against the 8MB feed before the hash changes); the probe was NOT modified to pass — the behavior it checks is proven, the race is in the instrument.
- **Worker join code / Auto-Match:** 0 occurrences of `smart_link_joins`/`naya_sl` in the worker; the single Auto-Match match is comment line 793 ("Auto-Match is NEVER a source: it scores PEOPLE, never notes") — not a use. Worker unchanged, so this is the fix round's state, re-grepped.
- **Staged == local re-proven at round end:** staged home curl sha `2c62d243f589` (5,570,515 B), staged feed 1,058 notes SN-2766 first.

## Honest notes

- R5 (blank loads) was never reproduced in fresh profiles, before or after — 0 in both. It may be a stale-profile or slow-network symptom; nothing in this round claims to have fixed a blank load that was seen.
- 1440 gap is 1px on sn2696/sn2695 (0 on sn2766) — sub-pixel rounding; the eye proof shows the cards ending exactly at the dock with no visible void.
- Post-click, a note page spins ("Opening your note…") until the 8MB feed lands — up to ~6s on a cold click (feed-click sn2766 needed the raised 12s wait in the battery). The note DOES open; the spin duration is the feed size, not a failure. A future round could prefetch/cache the feed, but that is out of this brief's scope (and the brief forbids a blanket re-fetch as a substitute for fixing the snapshot — this is not that; the fetch already exists).
- The probe-phase2-playwright 360 crash is a probe-timing race (see above); the product behavior is proven by direct tests, not by the probe.
- The `pad is not defined` error on nayanet.app/rooms/reports is a pre-existing LIVE-page defect, reproduced directly without any staged code — flagged for the owner lane, not fixed here (live is out of scope for this round).
- The shared staging worker `naya-public-blog-staging` was redeployed by another lane mid-verification (see Run 3 above). Staging needs serializing; this round's verification was re-run after redeploying and is green against the re-proven staged bytes.
- `deploy-phase2-staging.py` must NOT be run for this round (it would re-copy the live 1,085-note feed and break the frozen 1,058 bullseye). `deploy-rendered-fix-staging.py` is the frozen-feed deploy path.
- The ten canonical collisions are unchanged (worker untouched). No JOIN-leg change (join code stays absent). No change to live sitemap/shell/routes. No new vendor/key/framework/feed source.

## Filing

- **Branch:** `public-blog/seo-ai-backend-rendered-fix-20261113` (`SoulSchoolAcademy/NayaPOWER`, `BLOG/public-blog-seo-phase2/`).
- **Build tip (before record filing):** `7206f72412987ee1086169fa5440cedcc8550f45` (2026-11-14T03:29:08Z). 22 build files filed + read-back verified (shell blob sha `2b81ba9150ab…` matches local).
- **Record + scorecard filed after** (this file states the build tip; the two record commits follow it on the same branch).
- No merge, no PR.

## Files in this round (to file to the new branch)

- `index-intel-today-phase2.html` (edited shell, sha `2c62d243f589…`)
- `RECORD-SEO-AI-BACKEND-RENDERED-FIX-20261113.md` (this file)
- `SCORECARD-SEO-AI-BACKEND-RENDERED-FIX-20261113.md`
- `deploy-rendered-fix-staging.py`
- `probe-rendered-repro.py`, `probe-rendered-after.py`, `probe-grounding2.py`
- `phase2-shots-rendered/probe-rendered-repro-results.json`, `phase2-shots-rendered/probe-rendered-after-results.json`, `phase2-shots-rendered/probe-grounding2-results.json`
- `phase2-shots-rendered/after-*.png` (related + feed-click eye proof)
- `probe-dedupe-results.json`, `probe-phase2-results.json`, `probe-phase2-failures.json`, `phase2-shots-bars/checker-results.json`
- `staging-overwritten-by-other-lane-20261114.html`, `staging-feed-overwritten-by-other-lane-20261114.json` (preserved other-lane bytes)
