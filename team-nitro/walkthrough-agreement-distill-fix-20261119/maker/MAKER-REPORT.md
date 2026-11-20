# MAKER REPORT — Agreement-Distill Fix Round

**Round:** walkthrough/agreement-distill-fix-20261119 — maker seat
**Date:** 2026-11-19 (task 20:59 MST; filed same night)
**Base:** repo `SoulSchoolAcademy/NayaPOWER`, branch `walkthrough/agreement-distill-20261119`, tip `3e5647cf3ea95a1fa57aa7c51c16e47055913bf6`
**New branch:** `walkthrough/agreement-distill-fix-20261119`
**Staged worker:** https://naya-walk-beginning-staging.nayapower.workers.dev/
**Verdict:** the seven eye fails are fixed in the bytes and proven by a DOM harness that drives the pages' real JavaScript tap by tap — **54 assertions, 0 failures**. No merge, no live deploy, no link to Shawn. Checker and captain's eye come next.

## Files (all verified by sha256)

| File | Bytes | sha256 |
|---|---|---|
| `team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` | 141,781 | `5fe1a3ec2231c128774c6eb00736913d93117d3eaa06278e2a16183cdebee6ab` |
| `team-nitro/walk-v23-assembly-20261114/welcome-staged.html` | 1,913,241 | `c3c750b72a2b0330d15de8831e9b24719116991e6c0df9dbc5d329834fbbaed5` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html` | 4,361,369 | `0f05b3f96ce8edd0ecb094c0f64972098f788c3943e22b5446c8bb60e9b0e2fd` |
| `team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js` | 8,438,106 | `cd2ed5438546f42dc8b7acce2aef70933bbe3abdcf2b7ea93540503e81c9567c` |
| `team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` | 92,883 | `78742b801f57a2170e7803f5ffd4610b79fc4f1787fedb4d1ae3355dc0400a23` |
| `team-nitro/walkthrough-agreement-distill-fix-20261119/AGREEMENT-DISTILL-FIX-BRIEF.md` | 9,437 | `d2e239aa1fcef3eed9a48a82e3d8d89e370371c53897ee438e466afbc1457f18` |

Unchanged and NOT re-filed: identity (`3279dc35…`, 401,040 B), personal template (`61002d15…`, 1,486,773 B), mp3 (unwired — the anthem round owns it, queued behind this one).

The worker was built twice in memory from the fixed bytes, byte-identical both times, and its embeds verified: WALK `0f05b3f9`, IDENTITY `3279dc35`, WELCOME `c3c750b7`, UNFOLD `5fe1a3ec`, TEMPLATE `61002d15`. `node --check` passes on the worker and on every script block of the fixed unfold and welcome.

## Fix-by-fix table (the seven eye fails)

### 1. CORE — /agreement stacked all 37 boards; Next moved only the pill
**Root cause (proven in the distill bytes, not assumed):** the hide rule `.letter-beat:not(.frame-now){display:none!important}` (specificity 0,2,0) is defeated by a LATER rule `#deckBody .letter-beat{height:100%!important;display:flex!important}` (1,1,0). Every beat displayed flex; `showFrame()` only moved the `.frame-now` class the pill reads. That is the long scrollable page and the buttons nudged half below the fold.
**Fix:** a new `#fpFixDistill` style block at the end of `<head>`: `#deckBody .letter-beat:not(.frame-now){display:none!important}` (1,2,0 — outranks it) plus the matching `frame-now` flex rule and `overflow-x:hidden` on `#deckBody`.
**Proof:** DOM harness scenario 1 — at load exactly one board has `frame-now` and the CSS cascade (real specificity + `!important` + source order, evaluated over the file's own `<style>` blocks) shows exactly one board `display:flex` and the other 36 `display:none`; 36 Keep-reading taps walk 1→37 with the pill reading `N / 37` at every step and the cascade showing exactly one board each time; Back 37→36 works.

### 2. Deck — two taps per image board, void, cut-off headings/footer, photo half off-screen
**Root cause:** `wireDeck` / `wireLetterUnfold` / `wireLetter` ran a two-phase Smart Block (first tap = visual alone, second tap = advance); the stage CSS hid the showcase in talk phase (`body.fp-stage-on #fpAgreement .fp-now.fp-smart-talk .lb-showcase{display:none}`) while the ≥900px grid still reserved its column — the empty right column is the void; `__fpPlaceFaces` centred the face on the speaking line and alternated it left/right by `face-right`, so odd boards put it half off the left edge.
**Fix (one phase, everywhere):** the visual-first branches are removed from all three handlers (counted: 2 + 1); `render()` always sets talk, never visual (deck/letter/letterPage, counted 1 each); `derive()` always sets `S.phase='talk'` (3 sites); `deckEnd()`/`letterEnd()` are the last board, full stop; the stage-click end-anchor branch is gone; the showcase is forced visible in talk view (stage + plain page) by the `#fpFixDistill` block; the stage layer and every board clip horizontally (`overflow-x:hidden`); faces are forced right (`side:'right'`) and pinned to the board's top edge (+12px, clamped inside the board). Guards in the transform assert zero `S.phase='visual'`, zero `add('fp-smart-visual')`, zero `S.phase==='visual'` remain.
**Proof:** harness scenarios 3–4 — the mirror Next walks 1→37 in 36 taps (one per board), exactly one board shown at each step, the jewel reading `N / 37`, no beat ever carrying `fp-smart-visual`; deck board 1 is talk; zero `.ib-subtitle` in the deck.

### 3. Deck words ≠ /agreement words; two metaphors
**Fix:** one story. Board 11's line is "she's a Bugatti on a **superhighway**" in all three routes (the road a Bugatti drives on — supercomputer dropped everywhere). The deck's 37 extra quote lines (`<p class="ib-subtitle">`, counted 37) are removed — the letter and /agreement never carried them. Board 4: the eye's wording ("if a child can understand it", three differing sentences) has **0 hits in the distill bytes of either file** (workspace-wide grep confirms it exists only in the fix brief itself) — the difference cannot be reconciled from two text sources because both routes already render from the same `BOARDS` data; the one-story fix (same boards, same order, same words, subtitles removed) is the structural answer, and the eye should re-check board 4 on the new staging.
**Proof:** harness — deck board 1/11/37 nutshell text equals letter board 1/11/37 nutshell text by index; no `supercomputer` remains in either file; no `ib-subtitle` remains in the deck.

### 4. ?stage=letter broken; /agreement ignores ?stage=
**Root cause:** the unfold file has no stage handling, so the parameter was ignored there; `?stage=letter` opened the letterPage view, whose `updateChrome()` branch set the button but never the jewel — no progress at all. The letter also never got the deck frame (`wireDeckAF` turned it on for `deck` only).
**Fix:** the unfold redirects `?stage=deck|letter|bridge` → `/?stage=<same>` via `location.replace` (plain /agreement untouched); the letterPage branch now updates the jewel (number + bar + tone, mirroring the letter branch); the deck frame turns on for `?stage=letter` at boot and on the letter choice buttons.
**Proof:** harness scenario 2 — all three redirects fire with the exact URL; scenario 4 — `?stage=letter` opens the letterPage view with the jewel reading `1 / 37` at load and `N / 37` at every step through 37.

### 5. Five button destinations
- **(a) Hero "Read the collective agreement ◆":** its handler entered the in-page stage. Now `window.location.href='/agreement'`. Proven: harness scenario 5, the click navigates to exactly `/agreement`.
- **(b) Deck board-37 "Enter NayaNET":** the `deckJoin` path already called `showNHold(goBridgeAfterAgree)`; the last board's Keep reading had no exit (dead end), so a tap on the board button went nowhere. Added the `window.__fpStageEnd` hook (stage-only): the last board's Keep reading ends the story the same way the mirror button does. Proven: harness scenario 3 — at 37 the mirror reads "Enter NayaNET ◆", the click shows the N hold, and 3.3 s later the bridge view is up.
- **(c) Bridge Enter → hold → identity:** the name-form submit went straight to `/identity.html`. It now checks the agreed key / the bridge name-entry flag and, when the citizen came through the agreement, shows the N hold first (via the newly exposed `window.__fpHoldThen`), then navigates. Proven: harness scenario 5 — agreed submit shows the hold, then lands on `/identity.html?name=Test%20Name`.
- **(d) ?stage=bridge name-entry flips back to the login hero:** there is **no ~60 s timer in the welcome bytes** — the full timer inventory is 250 ms dial, 650/900 ms face settle, 1500 ms orb fade, 3 s hold, 10 s agree countdown (which goes to the bridge, not the login), 2 s/2.5 s speech watchdogs, 650 ms focus. What the bytes DO lose is the name-entry state on reload: `goBridgeToName` clears the agreed keys, so a reload lands on the login hero. Fix: `goBridgeToName` sets a session flag (`nayanet_fp_from_bridge`); the boot re-opens the name form when the flag stands (never while the stage is on); the flag clears on submit and on Back-to-login. Proven: harness scenario 5 — a reload with the flag re-opens the name form.
- **(e) /welcome blank black ~5 s:** the walk boot holds the questionnaire behind the `/api/claim` ownership gate (up to 4 s) with nothing painted. Fix (one line in the walk file, the only walk touch): boot paints the door at once (`showDoor()` before the gate). The gate itself is untouched (FIX6 ownership check intact).
**Proof:** harness scenarios 3–5 cover (a)–(d) end to end; (e) is a one-line paint fix whose gate is unchanged — the eye should confirm the door paints at once on /welcome.

### 6. Frame — light inside, buttons fully visible, images reliable
**Light:** the interior stays board black — Design Laws §4 (§5: no glow inside, ever). The specified light is the flowing light inside the rim, and it is present on all three routes: the unfold's `.frame-light` div (12 px white dot, purple glow, `frameLight` 60 s loop around the rim) plus the `.naya-frame` master-frame overlay; the deck/letter's `.af-deck-frame` with `.af-deck-light` (60 s) and corners, now also turned on for the letter. No new light was invented; the existing one is verified present.
**Buttons:** the one-board fix (fail 1) puts the foot and its buttons inside the frame on every tap — proven by the harness walk (36 taps, pill in sync, no stacked page to push buttons below the fold).
**Images:** the unfold already had showcase-error hide + face retry-once + crystal-N fallback (F3/F5). The welcome had none. Added a capture-phase error handler: a failed face retries once onto the crystal N (harvested verbatim from the unfold) then hides; a failed showcase retries once cache-busted, then hides its frame so the words still read. No picture is invented or swapped.
**Not proven by bytes:** the eye's one-load black circle / 0-height image was intermittent; the retry/fallback is the fix, but only the eye can confirm it never recurs on a live load.

### 7. Reader text
- Board 1's internal note is gone: `fpAudioState` now reads "Naya's reading arrives with her video"; the audio note and anthem note are rewritten in plain reader words ("Nothing is wired here yet" is gone). The audio/anthem wiring itself stays unwired — the queued anthem round owns it.
- "99 out of 100 people fail on it" is removed from board 1 in all three routes.
- "You're hired" now appears once, on board 37 ("Congratulations — you're hired"): board 15's title is "The work, done for you." and its line drops the clause; board 34's title is "Your card" and its line drops the clause. (The read-aloud SCRIPT still says "And you're hired" once — audio, owned by the anthem round; see carried items.)
- The letter/deck count is true: "Thirty-seven boards. One beautiful story."
- One metaphor: superhighway everywhere (fail 3).
- **Carried, not fixed — board 2 and board 22 baked-image jargon:** the infographic (slide-1) and machine-view (slide-6) pictures have their jargon baked into the image pixels; no text edit can change them, and the alt text does not reveal the baked words. All 8 unfold showcases and all 9 slides + 9 faces are already used by the 37 boards — there is no unused harvested picture to swap in, and a blind swap would duplicate a picture. This needs the captain's eye to pick a replacement picture (or a re-render) — it is the one carried item from the seven fails. The board TEXT on 2 and 22 is already plain.

## Proof — the DOM harness (this round's answer to the last round's failure)

The last round failed here: the checker passed in bytes and the eye found the story doesn't unfold. Bytes do not prove render. The VM browsers are dead (Chromium SIGTRAP, Firefox SIGSEGV), so there is no render. The strongest available proof was built instead: `maker/work/dom-harness.js` — a hand-rolled minimal DOM (no jsdom in this VM; npm install is EPERM-blocked) that parses the pages' **real HTML**, runs their **real `<script>` blocks** in a Node `vm` context, and drives the **real handlers** tap by tap.

**Result: 54 assertions, 0 failures**, across five scenarios:

1. **/agreement (unfold, plain)** — 37 boards; exactly one `frame-now` at load; the pill reads `1 / 37`; the CSS cascade (real specificity + `!important` + source order over the file's own `<style>` blocks, at 1920) shows exactly one board and hides the other 36; 36 Keep-reading taps walk 1→37 with the pill in sync and exactly one board visible at every step; Back 37→36; board text checks; 0 script errors.
2. **/agreement?stage=deck|letter|bridge** — all three redirect to `/?stage=<same>`.
3. **/?stage=deck** — stage on, deck view, jewel `1 / 37`, exactly one board shown; the mirror Next walks 1→37 in 36 taps (one per board) with the jewel in sync, including a Back mid-walk; no beat ever visual; at 37 the mirror reads "Enter NayaNET ◆"; the click shows the N hold; 3.3 s later the bridge view is up; 0 script errors.
4. **/?stage=letter** — letterPage view, jewel `1 / 37`; deck/letter board 1, 11 and 37 words identical by index; the mirror Next walks 1→37 in 36 taps; at 37 the mirror reads "I agree ◆"; the click opens the agree view; the agree button shows the N hold; 3.3 s later the bridge view is up; 0 script errors.
5. **/ plain** — the hero Read button navigates to `/agreement`; an agreed name-form submit shows the N hold, then lands on `/identity.html?name=Test%20Name`; a reload with the name-entry flag re-opens the name form; 0 script errors.

The harness itself found two real defects during the run (both fixed in this round, both in the transform): the letterPage jewel never updated, and the in-beat Back was a no-op in the stage (it unhid the previous beat but never hid the current one, so `derive()`'s `lastShown` landed back on the current beat — the fix hides the current beat in the stage only; off-stage the beats stay stacked for scrolling). It also caught that the letter's `data-beat` is 0-based (for its dots) while the deck's is 1-based — internal only, left alone because re-numbering would break the dot lighting.

**What the harness proves:** the state machine over the real code paths — visibility, progress, routing, holds, destinations. **What only the eye can prove:** pixels — the 1920 and 390 renders, whether the void is truly gone to the eye, whether the photo sits top-right and whole, whether the footer is whole, whether the frame light reads as specified, whether the image retry ever fires on a live load, and the board 2/22 pictures. Nothing in this report claims a render that was not seen.

## Three self-checks

1. **After the transform:** every replacement is counted and asserted — 40+ counted edits across the two files, each with its expected count; any miss throws and nothing is emitted. The transform ran clean. Board text, subtitles (37 removed), phase removal, and the final guards (zero `S.phase='visual'`, zero `add('fp-smart-visual')`, zero `S.phase==='visual'`) all verified in the transform itself.
2. **After the harness:** 54/0 across the five scenarios above, run against the final fixed bytes (the harness re-runs the transform itself, so the bytes it proves are the bytes filed). Two harness-found defects fixed and re-proven in the same run.
3. **After the rebuild:** the worker built twice from the fixed bytes, byte-identical (`cd2ed543…`, 8,438,106 B); every embed verified by sha256; `node --check` passes on the worker and on every script block of both fixed files; the laws delta is 0 (below).

## The seven questions (SELF-EVALUATION-CHECKLIST.md)

1. **Most intelligent?** Yes — the fixes go at the root cause in the code (a specificity defeat, a two-phase design, a missing jewel update, a state lost on reload) instead of patching symptoms, and the proof is a harness that runs the real code rather than a claim about bytes.
2. **Most logical?** Yes — each fix follows from a probed fact in the distill bytes (counts, anchors, timer inventory, the `lastShown` semantics), with every replacement counted; where the evidence ran out (board 4's wording, the ~60 s timer, the baked-image jargon) the report says so instead of inventing a cause.
3. **Most sensible?** Yes — one tap per board, one story, one metaphor, buttons that go where they say, a hold before identity, a name form that survives a reload. Nothing was redesigned; the frame, the jewel, the hold and the crystal fallback are all harvested verbatim.
4. **Full scope?** Yes — the whole walkthrough file (unfold + welcome + walk + worker + builder), the passes that must not regress, the queued anthem round (untouched), the captain's eye and checker still to come, and the carried item named with its reason.
5. **Consequences?** First order: the agreement unfolds one board at a time on all three routes and the bridge/identity flows hold. Second order: the letterPage jewel and stage Back fixes change behaviour the eye had not yet named but the reader would have hit. Who it touches: every citizen entering through the agreement — the gate to everything going live.
6. **Pros and cons?** For: root-cause fixes, counted edits, a 54/0 harness, laws delta 0. Against: no render was seen (VM browsers dead) — the eye is still the final gate; the walk file was touched for one line (fail 5e is in the brief, but it is outside the named base files — flagged here, not hidden); board 2/22 pictures are carried; the read-aloud SCRIPT keeps its old long wording (audio round's scope).
7. **Best possible choice?** Yes — scored against the ultimate objective (the agreement is the gate to going live; it must unfold, read true, and route right): all seven fails addressed except the one carried item, proven 54/0, laws delta 0, nothing removed that he didn't ask to remove, nothing live without his tap.

## §11 design check (in writing)

- **Reference objects:** every object is harvested, none created — the frame (master-frame.png overlay + travelling light), the red N seal and the N hold, the crystal-N fallback, the deck slides and faces, the stage jewel. The fix adds no new visual object.
- **Hover every object:** `:hover` rules are present in both files (the checker reports no NO-HOVER warning on either). The new controls (the hold hook, the flag restore) add no new visible object; the buttons they drive already answer touch.
- **Gray-text grep:** the checker's GRAY hits are regex matches in comments and strings, not rendered gray text — unfold 1 FAIL (the word "gray" inside a CSS comment, line 210, pre-existing, unchanged); welcome 83 FAIL identical before/after (all pre-existing). No gray text was added; the new wording is white on obsidian.
- **Size grep:** the SIZE hits are pre-existing sub-17px rules, identical before/after. The fix adds no `font-size` anywhere (the `#fpFixDistill` blocks carry only display/overflow rules).
- **Flow check:** the unfold walks 1→37 one board at a time with the pill in sync; the deck and letter walk 1→37 one tap per board with the jewel in sync; the bridge, hold and identity flows land where they say. Read as a reader: board 1 opens on the old internet with no false claim; board 11 drives the Bugatti on a superhighway; board 37 hires once, at the climax.
- **Laws delta: 0.** Unfold 1 FAIL / 2 WARN before and after; welcome 83 FAIL / 4 WARN before and after; zero added failures (run `maker/work/law-fix.py`). The walk's one-line change adds no new failure (its comment carries no gray/size/color trigger).

## Passes verified not regressed

37 boards in order (harness counts 37 on all three routes); no dots asserted by the cascade (the unfold hides them) — the eye should confirm no dots render; no long-text link (the plain-text dialog path is untouched); the two "Read the agreement" buttons → /agreement (hero proven; the bridge/choice buttons were already /agreement and are untouched); board-37 "I agree — show me my world" → `/?stage=bridge` (the unfold's agree path is untouched by this round — verified by the redirect + bridge flow, not by a direct agree click on the unfold; the checker should click it); "Begin the visual story" opens the deck at 1/37 (boot path, untouched); "Continue — enter your name" opens the bridge (untouched); /welcome Skip/Back of 14, Terms of Service legal deck, red "N" seal, no autoplay, "Hi, I'm Naya" — all in files/paths this round did not touch, and the harness ran the full welcome scripts with 0 errors.

## Work files (filed with the branch)

`maker/work/` — `transform-fix.js` (the fix transform, counted replacements), `build-fix.py` (in-memory build), `law-fix.py` (laws delta), `dom-harness.js` (54/0 proof), `debug-letter.js` (the letter probe), `probe-fix.js`, `probe-fix2.js`, `probe-fix3.js`, `probe-fix4.js` (the diagnosis probes), `boards-distill.js`, `transform-distill.js`, `build-mem.py`, `law-distill.py`, `probe-distill.py` (copied from the distill round — the base it operates on).

## For the checker and the captain's eye

- Re-run the harness (`node dom-harness.js` in `maker/work/`) — it must print 54/0.
- Render at 1920 and 390 and walk the whole flow by hand: /agreement 1→37, ?stage=deck 1→37, ?stage=letter 1→37, Enter NayaNET → hold → bridge → name → hold → identity, and the /welcome door painting at once.
- Confirm no dots render, the footer is whole, the photo sits top-right and whole, and the frame light reads as specified.
- Decide the board 2/22 pictures (carried item) and the board-4 wording re-check.
- No merge, no live deploy — the branch waits for the checker's verdict and Shawn's tap.
