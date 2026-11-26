# Portal Front-Page Fix — ROUND 3 — Maker Report

**Maker:** Portal Front-Page Fix Round 3 seat · **Round started** 2026-11-25 ~17:45 MST · **Report** 2026-11-25 ~18:25 MST
**Base:** round-2 staged portal, branch `portal-frontpage-fix-20261125-r2`, commit `4b194f93`, 1,907,038 B, sha `66664c07…`
**Staged (round 3):** https://portal-frontpage-fix-20261125-r3-staging.nayapower.workers.dev/
**Portal:** 13,878,677 B, sha256 `d46c440920ead620bca41c52492cccaa78f6ce7ca38edba6c3a0b93113498c15`
**Identity (certificate):** 313,224 B, sha256 `57bdd3873f65104f3ee6f4648cfec4a1a556a78ea8b7fb57153cd49da528af4b` — byte-identical to R2, untouched
**Branch:** `portal-frontpage-fix-20261125-r3` (from the round-2 branch head `72f30ae6`)
**Code commits:** `1e60b86d97f6838612eb9151e92861d3bdccbce5` (first build) + `5cf72bb778875819775699620e520a8bf90fc7f1` (probe fix pass — the staged bytes; the first commit's portal is superseded, see §"Bugs my own probe caught")
**Worker:** `portal-frontpage-fix-20261125-r3-staging`, Cloudflare account `b5e2a51b3e883f7722287c5f51b1196b`, deployment `cc38ef08429e41149837b17b59b12941` (current; earlier deployments `c17c5f21…` and `e23830b7…` carried the pre-fix builds and are superseded)
**Nothing live, nothing to Shawn.** Staged only. A separate independent checker verifies next.

## In one line
Every N now opens the real agreement — the 27-slide visual story, in place, at "The Old Way" — and the end slide carries the agree button at the very bottom, the eight links in a bar below, and the franchise text box back on the slide.

## What was built

**1. The ⓘ is replaced by a beautiful red ACTIVE N.** The button in the front-page circle is now `#fpCircleN`: the harvested red ball (same bytes as the corner ball — its `src` is copied at runtime from the corner img, so no duplicate 182 KB data URI), spinning on the portal's own `eco-spin 90s` keyframes, gloss fixed above it so the light stays top-left. Probed: `circleN_img_src_len` 243,295, animation `eco-spin 90s`, ⓘ absent from the bytes and the page.

**2. Every N + "Read the agreement" open the visual story IN PLACE.** The circle N, the black N bottom-left, the red N bottom-right (both keep their hrefs as a no-JS fallback; the click is intercepted with `preventDefault` + `openStory(0)`), and `#fpEnterDeal` all open `#fpStory` at slide 1. The old `#fpEnterDeal` navigation to `/agreement-landing` is removed (the worker route stays for the deck's own deep links; the front page no longer uses it). No navigation happens on any entry — the probe records the URL unchanged on every entry. Entry was proven repeatedly: red corner, black corner, "Read the agreement" ×3 (first + 2 repeats, per the inconsistent-entry defect) — all five land on slide 1, "The Old Way", story visible, never the overlay, never the landing.

**3. The story itself, harvested verbatim from the live agreement.** Fresh fetch of https://nayanet.app/agreement this round: **22,953,906 B, sha `2c88513f…`** — byte-identical to round-1/round-2 v25. **Reconciliation:** the brief cited a fresh fetch of 18,530,304 B, sha `6527cde7…`; that figure does NOT match the live bytes I fetched. The harvest is from the bytes actually fetched here, and the slide order was then re-verified against the confirmed 27-slide list forwarded mid-round (browser read 2026-11-25 17:42–17:55 MST) — **identical, title for title**: 1 The Old Way · 2 Welcome · 3 The Collective Intelligence Network · 4 Your Worlds · 5 In a Nutshell · 6 The System · 7 How It Works · 8 Your Day · 9 Smart Calendar · 10 The Simple Version · 11 For AIs · 12 Your AIs, Together · 13 The Mother Brain · 14 The Machine View · 15 What It Means · 16 Plug In · 17 Why It Matters · 18 The Naya Machine · 19 For AIs (second) · 20 Your Three Worlds · 21 The Whole-System Unfolding · 22 Done For You · 23 The Platform · 24 Your Own Worlds · 25 What's In It For You · 26 You're Hired · 27 Your Franchise. Full list: `evidence/slide-order-r3.md`. Harvested: 27 slide texts (t/x/a) + 27 slide pictures (JPEG/WEBP data URIs, 11,972,292 chars) + the 8 link answers (FP_FINAL) + the 16 R2 portrait URLs — all embedded verbatim in `portal.html`. The portal grew by the pictures (1.9 MB → 13.9 MB); the live agreement itself is 22.9 MB, so this is proportionate, not bloat.

**4. The old 13-paragraph pop-up reader is GONE.** `#fpDeedReader` markup and the `PARAS` IIFE script are removed. Three null-guarded `getElementById('fpDeedReader')` references remain in the pre-existing v2b + returning scripts — they return null and do nothing; the v2b early return keeps the circle N in the circle at every width, which is the wanted end state. The R2 (a) ring-fade CSS went with the reader (moot).

**5. End slide ("Your Franchise") per his eye.** Keeps the welcome ("Welcome home. Your world begins here.") and the keys image (slide 27's harvested picture: woman with the N keys, NayaNET Franchise building, LAND SECURED / BUILDING COMPLETE / BUSINESS OPERATIONAL / BRAND ESTABLISHED, "MOVE IN & OWN IT"). Changes, all probed on phone 390×844: (a) NO agree button in the middle — the only agree button is the bottom one; (b) the agree button sits at the very bottom, just above the < > arrows (agree y549, nav y644 on phone), flashing on a slow 2 s glow pulse — his word wins over the no-pulse habit, this button only; (c) the eight links are a bar across the bottom, just below the page (links display flex only on the last slide — see the bug below); (d) the franchise text box is back on the slide, in his REFINED wording (forwarded mid-round, ~17:39–17:40 MST): "You're getting the franchise — the deed to your own world: high-level digital real estate — one personal page, one business page, one space — free forever. Yours. Land secured, building complete, business operational, brand established. Move in and own it."; (e) agree — and forward (›) from slide 27 — returns to the name box: the story closes in place and the name input is focused (probe: `name_focused: "name"`, URL unchanged). The agreement is NOT mixed with the promise/guarantee/constitution as full content: the eight links open their answers in a frame only when tapped (probed: "Our Vow" opens with the full vow text).

**6. Confirmed live format honored.** "NAYA PRESENTS" kicker on every slide, station title in Marcellus, < > arrows at bottom centre, **NO slide counter** (the count span is `display:none` — verified in the probe: `count_display: "none"`), no progress dots. Forward from slide 27 exits to the name entry (Next on the last slide closes the story, same as Agree).

## Bugs my own probe caught — and fixed (both before the checker saw them)

**BUG 1 — script-close bug (would have been a total failure).** My first build escaped `</script` inside the story data script INCLUDING the wrapper's own closing tag, so the story script parsed as data and threw PAGEERROR "Unexpected token '<'": `FP_SLIDES` undefined, no entry opened the story, and the circle N rendered as an empty black disc (the diagnostic screenshot showed it). Fixed in `build-fix-r3.mjs`: escape only inside the JSON payloads; the build now asserts exactly one `</script` in the data script (the wrapper close). The first commit (`1e60b86d`) and its deployment (`c17c5f21`) carry this bug and are superseded by `5cf72bb7` / `cc38ef08`.

**BUG 2 — links bar leaked onto every slide.** `.fp-story-links` sets `display:flex`, which overrides the `[hidden]` attribute — the eight links showed at the bottom of slide 1 (visible in my own slide-1 screenshot). Fixed with explicit `[hidden]{display:none}` rules for the links bar, the agree wrap, and the end box. Re-probed: slide 1 links display `none`, slide 27 `flex`.

**BUG 3 — phone viewport fit.** The story frame scrolled as a whole, so the < > arrows (and the agree button) sat below the fold at 390×844 — my first full probe timed out clicking `#fpStoryNext` ("element is not visible"). Fixed: the frame is `100svh` with the board/art scrolling internally; nav + agree + links are pinned at the bottom and always visible. Re-probed: nav y647 on slide 1 at 390×844.

**BUG 4 — board scroll position persisted across slides.** The board's `scrollTop` survived `render()`, so arriving at the end slide showed the title sliced mid-glyph at the board's edge (visible in my own end-slide screenshot). Fixed: `render()` resets the board's `scrollTop` to 0. Re-probed: slide 27 title whole inside the board (top 156, bottom 187, board 226).

## My proof (read with my own eyes, not just measured)

- Phone 390×844, circle-N tap → story slide 1: "THE OLD WAY", board with Naya's face, "The Old Way", verbatim text ("Look at this desk, my friend…"), the overwhelmed-desk picture, < > arrows visible, links bar hidden. Screenshot `evidence/r3-phone390-story-slide1.png` (re-probe: `r3b-phone390-slide1.png` — full text visible, board scrollH == clientH).
- Phone, Next ×26 → end slide: "YOUR FRANCHISE", keys image, agree "I agree — show me my world ◆" above the arrows, eight links in a bar below. Screenshots `evidence/r3-phone390-story-end.png`, `r3b-phone390-end.png` (title whole) and `r3b-phone390-end-scrolled.png` (franchise box + red N, reachable by scrolling the board).
- Phone, "Our Vow" tap → answer frame opens with the full vow text. Agree tap → story closes, name input focused, URL unchanged. Screenshot `evidence/r3-phone390-after-agree.png`.
- Desktop 1440: red corner, black corner, "Read the agreement" ×3 → all land on slide 1, story visible, URL unchanged. Screenshot `evidence/r3-desk-story-slide1.png`.
- F1 spin kept: corner ball transform t0 `matrix(-0.534, 0.846, …)` → t25 `matrix(-0.967, -0.254, …)` — the gold N at clearly different angles; circle N also `eco-spin 90s`.
- F2 kept: at 573×355 the heading is one line, `white-space:nowrap` (probe `lines` read NaN — a probe artifact, `lineHeight` parses as `normal`; the gate's computed style and the screenshot are the evidence). Screenshot `evidence/r3-w573h355-front.png`.
- Errors: **0 pageerrors, 0 HTTP ≥400.** 1 console error = the known `/favicon.ico` 404. 2 requestfailed = `ERR_ABORTED` on R2 portrait URLs, aborted when the slide changes the face mid-fetch (same class as R2's aborted deck fetches; the face renders on every slide).
- `verify-r3.mjs`: 18/18 PASS against the staged worker (bytes + sha match the lane files).
- Design laws: portal **81 violations + 4 warnings**, identity **3** — identical to the R2 baseline, zero new (fresh `check-design-laws.py` run on the final file). No new `font-size` declarations anywhere in the round.

## Flags (for the checker and the captain — do NOT silently resolve)

1. **BUTTON WORDING — OPEN CHECK, rides on Shawn's word.** The story's agree button uses the OFFICIAL v7 wording "I agree — show me my world ◆". The live end slide reads just "I agree ◆". The difference is flagged here and in the commit message; the checker must prove whichever wording is on the slide against the words source. (Note: the portal still contains 2 occurrences of the short "I agree ◆" — both are pre-existing live-deck text elsewhere in the file, NOT the story button.)
2. **"For AIs" appears TWICE** (slides 11 and 19, different text) — confirmed in the live list and in my harvest. Flagged, NOT renamed: renaming either needs Shawn's word.
3. **Live-agreement size reconciliation.** The brief cited a fresh fetch of 18,530,304 B, sha `6527cde7…`. My fresh fetch returns 22,953,906 B, sha `2c88513f…`, byte-identical to R1/R2 v25. I harvested from the bytes actually fetched; the 18.5 MB figure is unreconciled — recorded, not assumed.
4. **Corner Ns keep their hrefs** (`nayanet.app/agreement`, `nayanet.app/`) as a no-JS fallback; the click is intercepted in place. A middle-click / open-in-new-tab would still navigate away — standard behaviour, named here.
5. **Phone end slide: the franchise box needs a board scroll.** On phone the end-slide board is 222 px tall against 737 px of content (face + title + text + welcome + franchise box + N), so the franchise box is reached by scrolling the board; the agree button, arrows and links stay pinned and visible throughout. On desktop it fits whole. The checker should verify the desktop end slide shows the box without scrolling.
6. **Portraits load from the public R2 bucket** (`pub-ee146405…r2.dev/portraits/`, live's own URLs, harvested verbatim) — same dependency the live agreement has; if a portrait fetch aborts mid-slide-change the face falls back to the previous image, never to a broken icon (probed: face renders on slide 1 and slide 27).

## Registry — record, do not act

- The round-2 checker re-walked `r2check25` and overwrote its vault answers with CHECK-ANSWER words (as round 1 did) — record for later deletion with the alias, along with `captaineye` Nº 893. **DELETION WAITS FOR SHAWN'S GO-AHEAD** — never delete a test certificate on my own authority. This round minted no new certificate and ran no walk.

## §11 Design-Law check (in writing)

- Read first, in order: `THE-NAYA-DESIGN-LAWS.md`, `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-ULTIMATE-ORIENTATION.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md`, round-2 maker + checker reports, the official v7 words source, the end-slide screenshot (`b4aaaa35…png`, read with my own eyes).
- The laws win over the brief on conflict — two conflicts arose and the newer word won in each, both named: (i) the agree button's slow glow pulse ("flashing nice", his word, this button only) over the no-pulse habit; (ii) Shawn's rulings supersede the round-1/round-2 agreement-entry behaviour (recorded as supersessions in the brief; the checker has the same list).
- §2.1 text scale: no new `font-size` declarations; the checker counts are unchanged (81 + 4 / 3).
- §2.2 colour: no new colours; the story reuses the file's own palette (white text, violet rim, emerald agree rim, gold franchise accents).
- Real Object Law: nothing redrawn, nothing rebuilt — slides, pictures, answers and portraits are harvested verbatim from the live agreement; the circle N is the harvested ball, turned by the portal's own keyframes; the gloss stays fixed so the light stays top-left.
- Harvest first: base is the R2 staged portal, edited, never rebuilt; the redacted diff vs R2 is `evidence/portal-diff-r3.txt` (454 lines — data URIs redacted out; the unredacted delta is the 27 harvested pictures).
- Five gates: no money, no credential read/used/stored, no destructive action, staging only, everything proven by read-back bytes + real renders. ✅

## Self-scorecard

- Agreement entry (every N + Read the agreement → story in place, slide 1): **10/10** — five real entries probed, all land, URL unchanged.
- Slide order + text (27, verbatim, confirmed list): **10/10** — extracted from live bytes, reconciled against the confirmed list title for title.
- End slide layout (agree bottom + links bar + franchise box + welcome + keys image): **9/10** — everything present and ordered right on phone and desktop; docked one point because the franchise box needs a board scroll on phone.
- F1/F2 preserved: **10/10** — spin matrices + 573×355 gate re-probed.
- Own goals caught by my own probe (script-close bug, links leak, phone fit, board scroll): **the round's lesson** — the first deployment was broken in a way no byte check could see (the bytes were all present; only a real tap proved the story never opened). The probe is the proof, not the diff. Score for catching all four before handoff: 10/10. Score for shipping the first build with the script-close bug in it: 0 — the bug was mine, the probe saved it from the checker.
- Overall: **9/10**. The work is proven by real taps at both widths; the hour ran long (the script-close bug + its re-proof cost the round its timebox), and the checker must still do its independent pass.

## What I proved vs what the checker must prove

**Proved by me:** all five entries land on slide 1 in place (phone circle N, desktop red/black corners, Read-the-agreement ×3); the 27-slide walk end to end by real Next taps; end-slide layout, agree wording, links bar, franchise box, link-answer frame, agree → name box with focus; F1 spin matrices; F2 gate at 573×355; staged bytes == lane bytes (portal + identity + sw.js); design-law counts unchanged; certificate sha unchanged; 0 pageerrors / 0 HTTP ≥400 on my runs; the four probe-caught bugs found and fixed.

**Checker must prove (independently, fresh eyes):** the same entries on its own run (including repeated entry, per defect (b)); the full 27-slide order against the confirmed list, including "For AIs" twice with different text; the end slide on desktop (franchise box whole, no scroll) and phone; the agree wording against the v7 words source; the returning view and the nine top-menu destinations (untouched by this round, not re-probed by me); the certificate's 5 jewels rendering on identity.html; 0 page errors on its own run; the diff vs R2 is the redacted diff named here plus the harvested pictures and nothing else; and that nothing in the round-1/round-2 pass set regressed that I did not re-probe (in particular the full 15-question walk, which this round did not touch).

## Evidence

- `evidence/agreement-live-r3.html` (live v25, 22,953,906 B, sha `2c88513f…`) · `evidence/slides-r3.json` · `evidence/slide-order-r3.md` · `evidence/harvest-r3.json`
- `evidence/probe-r3.py` + `probe-r3-log.json` (full probe) · `evidence/probe-r3b.py` (targeted re-probe: links leak + board scroll) · `evidence/diag-r3.py` (script-close bug diagnosis)
- `evidence/r3-phone390-front.png` · `r3-phone390-story-slide1.png` · `r3-phone390-story-end.png` · `r3-phone390-story-vow.png` · `r3-phone390-after-agree.png` · `r3-phone390-corner-t25.png` · `r3-w573h355-front.png`
- `evidence/r3-desk-front.png` · `r3-desk-story-slide1.png` · `r3-desk-story-redcorner.png`
- `evidence/r3b-phone390-slide1.png` · `r3b-phone390-end.png` · `r3b-phone390-end-scrolled.png`
- `evidence/portal-diff-r3.txt` (redacted diff vs R2, 454 lines) · `evidence/portal-r2-redacted.html` · `evidence/portal-r3-redacted.html`
- `build-fix-r3.mjs` (22 assertions, all PASS) · `build-worker-r3.mjs` · `verify-r3.mjs` (18 checks, all PASS against the staged worker) · `commit-r3.mjs` · `commit-r3b.mjs` · `story-r3.css` · `story-r3.js` · `story-r3.html`
