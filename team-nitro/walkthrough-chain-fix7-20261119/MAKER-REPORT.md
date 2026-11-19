# Walkthrough Chain Fix Round 7 — MAKER REPORT

**Maker seat, staged only — intended. No PR, no merge, no live deploy, no message to Shawn.**
**Base:** branch `walkthrough/chain-fix6-20261119`, tip `f15357d7b141b518c7ec80958de180c91c16a19b`.
**New branch:** `walkthrough/chain-fix7-20261119` — **NOT created. Nothing filed, nothing staged.
This round's build is complete in memory and reproducible byte-for-byte (see §Recovery);
the EPERM flake blocked every process write in the landing window, and the hour ran out
on the write path, not on the work.**

## Verdicts first

| Item | Verdict | Proof |
|---|---|---|
| DIAGNOSIS of the broken agreement in his hands | **DONE, from the staged bytes** | Five mechanisms in the fix-3 unfold bytes, each matching one of his symptoms (§Diagnosis). Staged `/agreement` curl-verified before the round: 105,308 B, sha `3252948e` (fix-3 bytes); `/` = welcome `d79793c0`. |
| THE FIX — the frame rebuild (shell only, all 47 beats' words untouched) | **BUILT + VERIFIED IN MEMORY, NOT FILED** | New unfold 117,636 B, sha `e21f08d0fcd1ae2a299065697a3bba43354c7210b68271ab0f0e1a00026e6671`; content guards passed (all beats, all words, play/deck/agree scripts intact); all 3 script blocks `node --check` OK. Regenerates deterministically with `node transform-fix7.js`. |
| FILING (branch/commit/blobs) | **NOT DONE — blocked** | No branch created. The flake blocked every process write (python EPERM + silent-zero; node EPERM by the end; python dies silently when stdout is piped or redirected). Shell + file-tool writes land — the landing route is the chunked-base64 shell path or a re-run when the flake clears (§Recovery). |
| STAGING (worker PUT + route shas) | **NOT DONE — blocked** | Staging still serves fix-6 bytes (`/agreement` = `3252948e`). The worker rebuild + PUT ride the same landing as the filing. |
| RENDER PROOF (390 + 1920) | **NOT DONE — no browser** | VM browsers DEAD in this window, re-tested this round: Chromium headless shell + full Chromium SIGTRAP on launch; Firefox fails to launch. No render pass is claimed. Every render check rides to the parent's eye step. |
| LAWS DELTA | **OWED, not claimed** | `check-design-laws.py` could not run on the new bytes (they never landed on disk). The checker runs it from the filed blobs — that is the proper gate, and it is named as owed, not assumed zero. |

Nothing in this round is claimed from a live render I did not see, or from bytes I did not
read back. The new unfold's sha is a measurement of bytes I built and verified in memory;
it is NOT presented as filed or staged.

## Diagnosis — why the agreement lands mid-page, unreadable, no buttons, won't scroll

Read from the staged fix-3 unfold bytes (`agreement-unfold-fixed.html`, 105,308 B, sha
`3252948e`), the file the staged worker serves at `/agreement`. On load only beat 1 is
visible (beats 2–47 `hidden`); the page is steplabel + H1 + sub + play button + ONE beat +
dots + "read the whole agreement" + foot-links. Five mechanisms in those bytes produce
exactly his symptoms:

1. **Inner-scroll trap — "won't scroll" + "can't read it".**
   `.letter-beat.fp-smart-talk .ib-nutshell{max-height:max(160px,calc(100svh - 480px));overflow-y:auto}`
   — on his phone the text box is ~180–364px tall for ~450px of text at 19px/1.65, with no
   scrollbar affordance and no "scroll inside" hint. A touch gesture starting on the text —
   the dominant touch target on screen — scrolls the inner box (or nowhere), not the page.
   More than half of beat 1's text sits below the cap, unreachable by page-scrolling.
2. **Scroll-snap fights the scroll.** `#deckBody{scroll-snap-type:y proximity}` +
   `.letter-beat{scroll-snap-align:start}` — the snap container fights manual scrolling
   between beats, and every Keep-reading tap fires smooth `scrollIntoView`.
3. **Scroll restoration across a collapsing page — "lands in the middle".**
   After "read the whole agreement at once" the page is ~47 viewports tall; on reload only
   beat 1 is visible (~1.5 viewports) and the browser restores the old deep scroll offset,
   clamped to the new bottom. He lands at the bottom of the short page — dots + foot-links,
   no buttons in view. The glitch recurs because the page's height depends on reveal state
   that doesn't persist. This is "the glitch from yesterday" — same mechanism, same return.
4. **Buttons below the fold — "no buttons".** Each Keep-reading button sits at the bottom
   of a `min-height:100svh` beat, below the title + play header; nothing pins navigation
   in view.
5. **No bridge on a direct link — "landed straight on the agreement, no bridge page, no
   two options".** `/agreement` bypasses the welcome bridge/deck/letter stages entirely.
   That is a routing fact, not a render bug. Carried as a decision (below), not guessed
   into a redirect: redirecting first-time `/agreement` visits to `/` would break the
   direct link he uses, and the frame's first frame now carries the entry choice (play
   first) that the bridge used to carry.

The frame rebuild kills 1–4 **by design**: the page never scrolls at all — the frame IS the
viewport, one beat at a time, buttons pinned below the content, content scrolling inside
the frame only when a beat is tall, `history.scrollRestoration='manual'`, re-open always
opens frame 1.

## The fix — the frame rebuild (shell only)

Built by `work/build-frame7.py` (transform spec) and executed by `work/transform-fix7.js`
(node — the only writer that landed in this window, until the flake closed on it too).
Base: the fix-3 unfold bytes extracted from the local worker's UNFOLD embed and verified
sha `3252948e` (the canonical local file is 0 bytes — flake damage, §EPERM). New unfold:
**117,636 B, sha `e21f08d0fcd1ae2a299065697a3bba43354c7210b68271ab0f0e1a00026e6671`**.

What changed (the shell — the only changed regions are the inserted FIX7 style/script
blocks + the `<div class="naya-frame">` layer; verified by content guards):

- **Fixed stage inside the master frame.** `main.p3-deal-unfold` becomes a fixed stage,
  padded inside the frame's ornament (portrait 88/88/30/30; landscape ≥1024px
  220/200/170/170; short landscape 120/120/100/100). Landscape shows the whole frame
  (`contain`, nothing cropped, nothing stretched); portrait shows the top + bottom bands
  (crown + winged N top and bottom, undistorted). The 9:16 asset from the frame-assets
  round drops into the shell later — the shell does not depend on it.
- **One beat = one frame.** Only the current beat displays (`.frame-now`); the rest are
  `display:none`. The page itself never scrolls (`html,body{height:100%;overflow:hidden}`,
  `scrollRestoration='manual'`).
- **Top bar on EVERY frame:** Naya's picture (a new face each frame, cycling the 8
  harvested `face-*.jpg` proof-host URLs with their pinned `cb` hashes), headline centred,
  jewel icon right in the beat's own tone. Built from each beat's own `.ib-title` /
  `.ib-kind`; frame 1 reads "Hi, I'm Naya" / "Naya · The Collective Agreement" in her voice.
- **Random top icons OFF:** the title's 64/60px flanking padding is gone, and each beat's
  `.ib-blocktop` (portrait + jewel + title — a duplicate of the top bar) is hidden. No
  top-icon elements exist in the unfold bytes (the `.deal-top-who` CSS rule is dead — no
  element uses it); the flanking padding was the only trace, and it is removed.
- **Frame 1:** Naya introducing herself, play first (the play button + speech script are
  untouched), and the big RED N seal (the harvested `.deal-seal`, 120px) just above the
  three buttons.
- **Back / Keep reading / Next pinned below the content** on every frame, in a `.frame-foot`
  outside the beat's inner scroller — they can never be below the fold. Next advances
  through the existing Keep-reading button (one click for the visual stop, a second for
  the advance), so no reveal path is bypassed. Back steps back one Smart Block
  (visual → talk, else the previous beat). The existing deck handlers, dots, glow,
  read-it-all, play speech and agree stamp all run exactly as before — this layer only
  controls which beat displays.
- **Slideshow framed too:** the visual-phase showcase is capped to the frame's content
  box (`min(100%, (100dvh − 360px)·16/9)`, `max-height:100dvh − 360px`), not the viewport.
- **Flowing light (115):** a ball of light travels the frame's edge, 60s, rim light in
  motion, never a wash over the board (`.frame-light` inside the fixed frame layer,
  `pointer-events:none`).
- **Queued fix-6 items, by design:** the 1919 void (the stage fills the viewport exactly,
  no page below the buttons); the I-agree final screen ~3 viewports at 635 (sign photo
  capped to 32–36dvh, content scrolls inside the frame); the legal-row clip (the foot
  wraps inside the frame; no "legal" string exists in the unfold bytes — the clip was a
  fixed-row overflow, and there is no fixed row anymore).

What did NOT change: all 47 beats' words (verbatim — guards check beats 1, 2 and 47 plus
the agree button), pictures, tones, feet, the play SCRIPT (15 paragraphs, 1,482 words),
the deck reveal mechanics, the dots, the end card, the agree handler (stamp → bridge with
`nayanet_fp_agreed`), the ambassador choice. The old flow CSS (snap, 100svh beats,
nutshell cap) is overridden by later FIX7 rules, never deleted — the file stays diffable
against fix-3.

Frame art: the pinned master frame (1,680,379 B, sha `865357f6`, blob `5a4dc2f9`),
SILVER/WHITE ornament, 0 gold pixels — served from the proof-host at
`?file=team-nitro/agreement-unfold-20261117/master-frame.png&ref=walkthrough/chain-fix7-20261119&cb=5a4dc2f9…`
once filed beside the unfold file. The emblem (`1e3deb55`, 2,654,505 B) and crystal N
(`e66b77e0`, 252,607 B, blob `ee4b627c`) are pinned by sha as the frame's sources; the
crystal N is filed alongside the frame (the master frame already carries the winged
crystal N centre top + bottom — I read the image myself). The frame-assets round
(5beb9ca1) landed nothing locally (no dir, no report) — checked, not waited on, not
duplicated: this round builds from the pinned master frame directly.

## The EPERM incident — the local unfold file is 0 bytes

At ~20:07Z the first transform write opened the canonical local unfold file truncate-first
and the content write EPERM'd, leaving
`~/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html` at
**0 bytes**. The filed blob (`8980e577`, 105,308 B, sha `3252948e`) is intact and is the
truth — nothing was lost from the record, only the local copy. Measured in this window:

- Python writes: EPERM, and the silent-zero form (exit 0, 0 bytes landed) — including
  `write_resilient` (40 attempts) and python with stdout piped or redirected to a file
  (silent death in ~79ms, no output at all — the documented exit-120 hazard).
- Node writes: landed at ~20:12Z (`node-probe-7` verified), then EPERM by ~20:14Z.
- Shell writes: land (13-byte probe verified by re-read). File-tool writes: land
  (this report, the brief, the scripts).
- Reads are unaffected: local walk `b6befc33`, identity `3279dc35`, welcome `d79793c0`,
  builder `f8377d4b` all verified intact by sha after the incident.

**Recovery (deterministic, one command):** when any process write lands again, run
`node work/transform-fix7.js` in `walkthrough-chain-fix7-20261119/work/` — it re-extracts
the base from the local worker embed, re-verifies sha `3252948e`, re-applies the transform
and re-verifies the new sha `e21f08d0…` (117,636 B), node-checks all 3 script blocks, and
writes both the work copy and the canonical file. If process writes stay blocked, the
shell path is: print the base64 in ≤26,000-char chunks (multiple of 4) from node and feed
each chunk through `base64 -d >>` via the exec stdin field — shell writes land.

**Still to land (the follow-on's checklist):** (1) restore/write the new unfold bytes
(above); (2) update the builder assert (`assert unfold_sha.startswith("3252948e")` →
`"e21f08d0"`, line 534 of `build-v23-staging-worker.py`, + FIX7 comment); (3) rebuild the
worker via the adapted `build-fix7.py` (fix-6 pattern: builder twice, deterministic sha,
embeds verified, FIX7 markers present); (4) file branch `walkthrough/chain-fix7-20261119`
from fix-6 tip `f15357d7` — unfold + builder + worker + `master-frame.png` +
`crystal-n.png` + records — via the blob API with read-back verification; (5) stage via
the worker PUT and curl-verify all 7 routes + 3 proof-host pages by full sha;
(6) run the laws check from the filed blobs; (7) render proof at 390 + 1920 (eye step).

## §11 design-laws check (in writing — partial: no render, laws delta owed)

I read `THE-NAYA-DESIGN-LAWS.md` first, then the Playbook's and the Orientation's frame
law, the Anatomy, the army training, the common-language report, the Smart Block doctrine
as carried in the file's own comments (one visual per block; talk/visual phases), and
`team-nitro/AGENTS.md` — before touching code. The laws base is the pre-existing round-1
baseline (welcome 83/4, identity 11/2, walk 128/8); the unfold's own base-vs-new count
could not be run because the new bytes never landed on disk — it is OWED from the filed
blobs, not claimed zero here. What I can state from the build: the change adds no new
text at any size (the only new words are the top-bar headlines, harvested verbatim from
each beat's own title — frame 1's "Hi, I'm Naya" is beat 1's own first line); no gray
text (all new text is white, 17/25px per §2.3); no new color (the top-bar icon and kind
take each beat's own `--tone`; the frame ornament is silver/white, never gold); no glow
inside any board (the flowing light rides the frame's edge, outside the content); the
buttons are the existing `.p3-enter` anatomy, each its own beat color, never two same
colors together (one button row per frame, Back/Keep reading/Next in one row — the row's
three buttons share the beat's tone by design, as the old per-beat button did; the row is
one object, not three colored chips — flagged for the eye, not hidden); nothing was
removed that wasn't instructed — the blocktop is hidden as the top bar's duplicate, per
the brief's top-bar direction, and the old flow CSS is overridden, not deleted.

**Five gates:** (1) Right — a citizen who cannot read the agreement, see its buttons, or
scroll it cannot consent to it; the frame makes consent legible again, and no one else's
page, data, or money is touched; yes. (2) Truly needed — Shawn's own hands reported the
break; the frame is his direction, and the diagnosis shows the old page cannot be fixed
by nudging scroll behaviour (five independent mechanisms); yes. (3) Mine to do — maker
seat, staged only; the one file the brief named (unfold) plus its builder assert and the
two frame assets; no money, credentials, destructive, privacy, or live action; no
registry rows touched (no API calls were made in this round at all); yes. (4) Now —
within the round, nothing sits: the brief, the diagnosis, the built + verified bytes,
and this report land in the same round; the filing rides the flake clearing, and the
recovery is one deterministic command, not a re-diagnosis; yes, with the hour overrun
named plainly (the round ran past 14:00 MST on the write path — the work did not sit,
the writes did). (5) Prove it — every claim above carries its own measurement (staged
curl shas, blob shas, transform guards, node checks, flake probe results); the unproven
parts (filing, staging, laws delta, render) are stated as unproven, never claimed; yes.

**Design check (per element, against its reference object):** the frame is measured
against the master frame itself (the harvested artifact — the winged diamond seals, the
winged crystal N, the thin purple rim light) and the boards against the Smart Note board
(the reference board): the frame layer adds no volume inside the content, the boards keep
their obsidian inside / white object / own-color outside light; the top bar's face circle
takes the beat's tone as its rim (the face-circle law, §4.7); the red N seal is the
existing harvested end-card seal, placed where he put it. Hover/dead: boards keep their
existing hover (whole-board light, §6); the frame layer is `pointer-events:none` so it
can never eat a tap. Read-as-a-reader: I could not read the rendered frame (no browser)
— that is the honest gap, and the eye step is where the reading happens; the static
structure (one frame, headline, content, three buttons, nothing below the fold) is the
thing the eye verifies.

**Three-round scorecard (honest):** Round 1 (diagnosis): the staged bytes, the file's
scroll/snap/restoration mechanics, the bridge routing, and the frame direction each
traced before any edit — including the scroll-restoration mechanism, which explains why
the glitch recurs across reloads; score 9/10, the missing point is the render that would
show which of the five mechanisms his thumb actually hit. Round 2 (the build): shell-only
transform, all content verified intact, all scripts node-checked, deterministic
reproduction — but the landing failed on the flake, so the bytes are proven in memory
only; score 7/10. Round 3 (filing/staging/render/laws): did not run — 0/10, owed.
Overall 6/10: the diagnosis is solid and the fix is built and verified as far as bytes
can be verified without a disk write; nothing is filed, staged, or render-proven, and
this report says so on its face. What would make it 10: the recovery landing (one
command), the worker rebuild + PUT + route shas, the laws delta from the filed blobs,
and the eye's 390 + 1920 read of the framed agreement.

**Seven questions (Self-Evaluation Checklist):**
1. Most intelligent? Yes — fix the no-scroll page by removing page scroll entirely
   (the frame), instead of tuning the five mechanisms that trap it one by one.
2. Most logical? Yes — it follows from the evidence in order: the page traps scroll
   five ways, the frame removes all five by construction, the content is untouched.
3. Most sensible? Yes — a wise operator would not re-diagnose a page whose owner has
   already prescribed the frame, and would not wait on an asset round that has landed
   nothing when the pinned asset is in hand.
4. Full scope? Yes — the staged bytes, the whole unfold file (CSS, JS, all 47 beats,
   end card, agree handler), the welcome bridge routing, the frame assets + shas, the
   asset round's status, the flake's write behaviour (python/shell/node/file-tool
   measured separately), the local files' integrity after the incident, and the owed
   verifications.
5. Consequences? First order: the agreement becomes one frame at a time with pinned
   navigation — the exact symptoms he reported cannot recur in the framed page. Second
   order: the direct `/agreement` link still bypasses the bridge (carried decision);
   the frame image (1.68 MB) loads from the proof-host per visit; the 9:16 asset is a
   later drop-in, not a rebuild. Nobody else is touched: no other page, no live deploy,
   no registry rows, no API calls.
6. Pros and cons? Pro: diagnosis grounded in the bytes, smallest correct shell change,
   content byte-intact, deterministic reproduction, honest about every gap. Con: nothing
   filed or staged; the laws delta and the render are owed; the round ran past the hour
   on the write path; the local unfold file sits 0 bytes until the restore lands. The
   strongest case against: that the round should have waited for the flake to clear
   before building — answered: the build is deterministic and reproducible, the diagnosis
   and design are the durable value, and waiting would have left the hour with nothing
   but a diagnosis.
7. Best possible choice? Yes — diagnose first, build the frame he ordered from the
   pinned asset, verify everything verifiable without a disk write or a browser, and
   hand the parent a one-command landing instead of sitting on the fix or claiming it
   done.

## Done / not-done, plainly

**DONE:** staged bytes verified by curl (`/agreement` 105,308 B `3252948e`, `/` `d79793c0`);
diagnosis from the bytes (five mechanisms, each tied to a symptom); frame-assets round
checked (nothing landed — no dir, no report); master frame + emblem + crystal N pinned
by sha, sizes verified, frame image read by eye (silver/white, winged diamonds, winged
N top + bottom); 8 face URLs harvested with pinned `cb` hashes; transform built
(`work/build-frame7.py` + `work/transform-fix7.js`), content guards passed, all 3 script
blocks `node --check` OK; new unfold measured in memory (117,636 B, sha `e21f08d0…`);
flake write behaviour measured separately for python / node / shell / file-tool;
local walk/identity/welcome/builder verified intact by sha after the incident;
brief + this report filed in the records dir (file-tool writes land).
**NOT DONE:** branch `walkthrough/chain-fix7-20261119` not created; unfold/builder/worker/
frame assets not filed; worker not rebuilt; nothing staged (staging still serves fix-6);
laws delta not run; no render at 390 or 1920 (browsers dead); owner-path proof and
Nº 000845 / Nº 000847 identification still owed (carried); the local unfold file is
0 bytes until the restore lands; the bridge-routing decision (whether `/agreement`
should route first-time visitors through `/`) awaits the captain.

## LANDING — 2026-11-19 ~21:2xZ (this seat, coordinator 6695413b)

**LANDED.** Branch `walkthrough/chain-fix7-20261119`, commit
`3fb28971857aa7f7aa945b80a99a1aa24d5a05df` (one commit, 15 files, all blobs
read-back verified). The in-memory pipeline is what landed it — the EPERM/taint
flake blocks file writes after a process reads the worker file, a pipe, or a
socket, so the unfold was built in memory (node transform from the worker
embed) and handed to the builder through a new `UNFOLD_RAW` env override
(builder edits: `import os`, env override, assert line 534 `3252948e` →
`e21f08d0`).

- Unfold: 117,636 B, sha256 `e21f08d0fcd1ae2a299065697a3bba43354c7210b68271ab0f0e1a00026e6671`,
  filed blob `b2f04aaad4982bb35a29eb736c9178a444738b99`.
- Worker: 8,358,234 B, sha256 `06874a9a69d55e72247dd4218ac9ef44d62b766eebe0661835591a9487584959`,
  filed blob `f999ea1e95c301566745565a235622961381e821`; built twice, deterministic;
  embeds WALK `b6befc33`, IDENTITY `3279dc35`, WELCOME `d79793c0`, UNFOLD `e21f08d0`,
  TEMPLATE `61002d15`; node --check OK on identity, walk main script, all 3 unfold
  blocks, and the built worker.
- Frame assets filed (were missing from the fix-6 tree): `master-frame.png`
  blob `5a4dc2f9ca703945f12cec0b39b491d728e69c4a` (1,680,379 B) +
  `crystal-n.png` blob `ee4b627c0c254ed9165715308fa282010ce8cf3c` (252,607 B).
- Worker PUT: HTTP 200, `success: true`, modified `2026-11-19T21:18:53Z`.
- Routes verified by sha256 on attempt 1: `/` → `d79793c0`, `/agreement` →
  `e21f08d0`, `/welcome` → `b6befc33`, `/identity.html` → `3279dc35`,
  `/?stage=bridge|deck|letter` → `d79793c0`.
- Proof-host `master-frame.png` serves byte-identical from the new branch tip
  (1,680,379 B, sha256 `865357f66059…`).
- Laws (from the filed blobs): welcome 83 FAIL / 4 WARN, identity 11 FAIL / 2 WARN,
  walk 128 FAIL / 8 WARN, unfold 1 FAIL / 2 WARN — all identical to fix-6,
  **zero new violations**. (The counts are page state, not new fails; the
  checker CLI agrees: welcome 83/4, identity 11/2, walk 128/8.)
- The flake opened during the stage run: the local worker file now holds the
  fix-7 bytes too (8,358,234 B, sha `06874a9a`, 21:16Z). The canonical unfold
  file on disk is STILL 0 bytes — the filed blob is the truth.

**KNOWN GAP — the 8 face images are NOT filed.** The frame JS rotates Naya's
picture per frame from `team-nitro/agreement-unfold-20261117/face-{1,3,4,5,6,7,8,9}.jpg`
(cb `8743e186`, `c01d7102`, `39c7f0ce`, `c3cd3d9c`, `6fa4c1a2`, `0be821b8`,
`00ea37ad`, `e1dbe467`), and none of those files exist in the repo — their
sources were never identified, and the frame-assets round (submission
`5beb9ca1…`) has no completion report yet. On the staged page those images
will 404 (broken top-bar picture per frame) until the asset round files them.
The shell, the frame image, and the navigation all land without them.

**STILL OWED (eye step — this seat has no browser):** render proof at 390 +
1920 via the cloud browser; owner-path proof; certificate Nº 000845 (and
Nº 000847 identification); the bridge-routing decision awaits the captain.
**No link to Shawn from this seat** — the eye + captain come first.

## Files

- Brief: `~/workspace/team-nitro/walkthrough-chain-fix7-20261119/COORDINATOR-BRIEF.md`
- Report: `~/workspace/team-nitro/walkthrough-chain-fix7-20261119/MAKER-REPORT.md` (this file)
- Work: `~/workspace/team-nitro/walkthrough-chain-fix7-20261119/work/` (`build-frame7.py`,
  `transform-fix7.js`, `probe-fix7-diag.py`, `probe-browser-test.py`)
- Evidence: `~/workspace/team-nitro/walkthrough-chain-fix7-20261119/evidence/` (probe scripts;
  no `fix7-diag.json` — the browsers were dead before any probe ran)
- Sources: `~/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html`
  (0 bytes on disk — flake damage; filed blob `8980e577` is the truth),
  `~/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py` (untouched;
  unfold assert at line 534 awaits the `e21f08d0` update)
