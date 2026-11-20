# MAKER REPORT — Personal frame fix-8

**Branch:** `personal/frame-round-fix8-20261119` (from tip `8113eef9`, branch `personal/frame-round-fix7-20261119`)
**File:** `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`
**Base (fix-7):** blob `5a5274fb69c73da52ca725d161672c1c8042eada`, 10,456,885 B, sha256 `59b17fa856afb5813330142e5fe1d4bb3e2606b6c429030b07a7ff0600320b52`
**Fixed (fix-8):** blob **`9b158924e927a239ccabcc5243bfff8d1a2fce12`**, **10,459,295 B**, sha256 **`5a43d01ae07d7a6346406f8919dbf720267f3bab8e29f630af2dc8cc5ad5c3a8`**
**Staged link:** `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix8-20261119&cb=9b158924e927a239ccabcc5243bfff8d1a2fce12&owner=flagship-personal` — **HELD until live proof lands; do not deliver to Shawn.**
**Date:** 2026-11-20. Maker: Naya Nitro Narzan.

## What fix-7's checker sent back (the go-back)

Fix-7's own label fix moved the room's side-topics to static in-flow rows (FRAG line 16920). With the room open that put the topics ON the cover: at 390 "Get Started" covered "Shawn Vibert" and the motto was cut to "Tog…"; at 800–1920 the end cover pills were covered. Fix-8's job: keep the icons-only label fix, move the side-topics out of the cover.

## The diff, hunk by hunk (base fix-7 → fixed, 5 opcodes, +2,410 B, +14 lines)

Verified with `difflib` on the full 51,897-line files — exactly 5 non-equal opcodes, all intended, nothing else moved.

1. **Insert after fix-7 item-4 block (base line 8385): cover-guard CSS + tablet `.top` trim — 8 lines.**
   - `body.ask-cover .naya-ask-room .side-topics{opacity:0!important;visibility:hidden!important;pointer-events:none!important}` — while the cover intersects the viewport, the fixed side-topic strip is invisible and untappable. Specificity (0,3,1) beats the FRAG rule (0,2,0); it only fires while the watcher (hunk 5) sets `body.ask-cover`.
   - `@media (min-width:761px) and (max-width:900px)` — `.top{padding:11px 8px;gap:4px}`, `.top .hub-obsidian-btn{padding:11px 8px;letter-spacing:0}`, `.top .top-title{white-space:nowrap}`. Measured need at 800 (feed view, room closed): the title `INTELLIGENT HUB` was squeezed to 78px clientW (scrollW 149) and wrapped to two lines; 71px more was needed. Computed savings ~107px (~36px slack at normal font, ~9px at +5%). No font-size change, no element removed. The rail-toggle (scrollW 63 vs clientW 46) was deliberately left untouched.
2. **Insert (base line 12871): `openWorld()` helper — 2 lines.** Beside `openMail` in `buildHubPlusMenus`: `fcOpenWorld()` if it exists, else `fcOpenCreator('post')`. Mirrors the composer menu's own Create-world handler exactly.
3. **Insert (base line 12877): Create-world ADD-menu item — 1 line.** `create.appendChild(item('Create world', '#a21caf', openWorld));` — the sixth ADD item. The `'#a21caf'` is a JS string argument, not a `color:` declaration, so the laws checker does not trip on it (verified, §laws below).
4. **Replace FRAG line (base line 16919): the go-back fix — 1 line replaced.** Decoded FRAG diff (see below): side-topics restored to base fixed strips verbatim; fix-7's `body.ask-reading .side-topics{display:none}` removed; mobile clearance restored to 452px.
5. **Insert (base line 16947): cover-watcher script — 3 lines.** Standalone `<script>` after the FRAG/rooms script block. `MutationObserver` + `IntersectionObserver` on `#phIntroBoard.closest('.os-view')` (threshold 0), toggling `body.ask-cover`. The observer watches the `.os-view` that holds name, motto, cover pills and the points orb — NOT the sticky `.top` (different branch; observing it would keep the guard on forever once scrolled). Contains no colour, font-size, or gray literals.

### FRAG diff (decoded `var FRAG`, fix-7 → fix-8): exactly 3 changes
- Line 455: `.naya-ask-room .side-topics{position:static;…}` → base verbatim `{position:fixed;top:auto;transform:none;left:0;right:0;width:auto;flex-direction:row;flex-wrap:nowrap;overflow-x:auto;overflow-y:hidden;gap:8px;padding:9px 12px;background:rgba(6,6,10,.86);…}` — the mobile fixed strip, byte-for-byte the fix-6 base text.
- Line 457: `body.ask-reading .naya-ask-room .side-topics{display:none}` — **deleted** (the base transform slide-down returns).
- Line 482: `main#mainEl{padding-bottom:calc(200px + env(safe-area-inset-bottom,0px))}` → `calc(452px + …)` — the fix-6 base clearance restored.

### Untouched, verified byte-identical
- **Fix-6 popstate guard:** the 12-line comment + guard at fix-7 lines 23603–23614 is byte-identical in the fixed file (found at lines 23617–23628, shifted +14 by the insertions; `match: True`).
- **Welcome banner, Academy:** no opcode touches them. The `.jlabel{display:none}` icons-only label fix and the side-topic `padding:8px` from fix-7 are kept.
- **Fix-7 items 1, 2, 3 (feed view), 5:** no opcode touches their code. (Live re-proof still owed — see §live proof.)

## Laws check — delta 0

`~/workspace/team-nitro/check-design-laws.py` run on base and on fixed: **normalised diff 0 lines; 0 FAILs and 0 WARNs on both sides.** The new CSS/JS contains no gray/grey, no `font-size`, no `color:` declaration. The `'#a21caf'` string is a JS argument, not a text colour.

## JS parse — 101 inline `<script>` blocks, 0 parse failures

(`new Function` on every inline script; fix-7 had 100 blocks — the +1 is the cover-watcher script.)

## Design decisions (why this shape)

- **Why hide instead of move:** a `position:fixed` element overlaps the cover at *some* scroll offset wherever it is placed — top, bottom, or side. The acceptance is "name, motto, whole `.top`, all 8 cover pills readable at every scroll position, at 5 widths". Hiding while the cover intersects is the only approach that satisfies it at all scroll positions. The topics return the moment the reader scrolls into the room (guard off when the cover leaves the viewport), so nothing is lost — they are still there, still tappable, in the room where they belong.
- **Why not restore `#pcComposerPlus`:** the brief allows "or" — the ADD menu is the real tap path that already exists and already opens. Reconstructing `#pcComposerPlus` markup from CSS alone would be inventing a part that does not exist in the live DOM.
- **Item 3 (PERSONAL yield):** at 390 room-open the bottom bar sits above the jewelbar (y682–772) and the PERSONAL seg rect (86,694,50×48) returns its own SVG tile from `elementFromPoint` — tappable there by real coordinate tap. At 1920 the bar is folded by the settled show-once law (must NOT be redesigned), so the yield there is **Back** (proven on fix-7 bytes both widths → `#/hub/feed`) and/or summoning the bar via the `#os-b3-hide` corner control, then PERSONAL. Lens tabs do not exist room-open and cannot be the yield path.
- **Item 4 (PERSONAL / CONNECT segs):** PERSONAL = `osShowView('home')` → hash `#home` (proven by real tap on fix-7 bytes at 390 feed view and by evaluate diagnostic). CONNECT (plus-connect) = `hubTogglePlusMenu('connect')` → `#hubPlusConnect` (All connections → `osShowView('people')`; Message → messenger panel). The checker's "no observable effect" is explained by taps landing on the folded bar (segs below the viewport at 1920) / the jewelbar-covered seg at room-open 1920 — not by broken handlers. No seg code change was needed; the proof is by real tap with the bar unfolded (owed — see §live proof).

## Live proof — BLOCKED (VM browser death, the documented flap) — FINAL STATUS

**The live verification could NOT run — both VM browsers stayed dead through every retry.**

- Firefox: SIGSEGV on launch, **5 attempts** (verify run; retests at ~16:36Z, ~16:39Z, and the retry watcher). Last good Firefox run in this VM was the fix-7 exploration probes earlier today (~15:52Z).
- Chromium (headless-shell and full `chrome-linux64`): SIGTRAP on launch, 2 attempts.
- Meta-chromium (`/opt/meta-chromium/chrome`): blocked by the Hatch WebGL domain policy (`chrome_main_delegate.cc:1283`), as documented in TOOLS.md.
- Memory/disk are fine (3.8 GB available, 7.3 GB free); the failure is the known flapping browser death (TOOLS.md: "browsers alive again 00:02Z … DEAD again ~02:27Z … The death flaps; re-test every time").
- The localhost forwarder (`h1-proxy-forwarder.py`) was UP on 127.0.0.1:18080 and proxying (200 on example.com); the page server on 127.0.0.1:8828 served the fixed bytes (sha re-verified: `5a43d01a…`).
- A retry watcher ran 16:36–16:45Z (every 2 min); its log writes were EPERM-blocked by the flake (0-byte log, "write error: Operation not permitted"), and it was stopped after direct retests still failed. **The branch is filed byte-proven so the live leg can be routed to a cloud-browser agent (the fix-18 captain's eye ran that way today) or retried when the flap clears. The live-proof section below is the exact checklist for that leg — nothing here is claimed proven.**

### To be proven by `verify8.py` (script ready in the round dir, `proof/` outputs pending)
1. **Item 1 — gate, room-open, scroll 0 AND scrolled (300 / 1400), at 390/800/1000/1200/1920:** name "Shawn Vibert" whole, motto whole, whole `.top` row, all 8 cover pills readable — read from screenshots as a reader; `body.ask-cover` on + side-topics `opacity:0` while the cover is on screen; topics back (`opacity:1`) once scrolled into the room. Screenshots `v8-<w>-room.png`, `v8-<w>-room-s300.png`, `v8-<w>-room-s1400.png`; rects in `proof/v8-item1.json`.
2. **Item 2 — ADD 6/6 by real menu tap at 1920 (and Create world + Message at 390):** Create world → `ibGrowDialog` "Create a world"; Make a post / Naya note / Smart note / Message / Mail each by real tap; Connect → Message → messenger panel. No URL-suffix counting.
3. **Item 3 — PERSONAL yield by real coordinate tap at 390 room-open; Back at 1920** → `#/hub/feed`.
4. **Item 4 — PERSONAL feed tap with bar unfolded → `#home`; CONNECT tap → `#hubPlusConnect` opens; All connections → people view.**
5. **Robustness — +5% wider-font probe on the 390 `.top` row (and the 800 `.top` trim):** reported honestly; the 390 slack (~1px) is NOT spent by any fix-8 change.
6. **No regression — fix-7 items 1, 2, 3 (feed view), 5 re-proven on fix-8 bytes.**

## §11 check (in writing)

- **Read the laws first:** `THE-NAYA-DESIGN-LAWS.md` read first, then Playbook, Intelligence Report, Orientation, Anatomy, Heart, Army Training — all before any edit.
- **Five gates:** (1) Right — a dispatched fix on a branch, no one harmed, no live change. (2) Truly needed — the checker's go-back, named by a reader's eye. (3) Mine to do — maker seat, branch filing only; no money, credentials, privacy, or live-deploy gate touched. (4) Now — the round is the current work; nothing it depends on is missing. (5) Provable — byte proofs complete (diff, FRAG diff, guard, JS parse, laws); live proof is the open item, named as open, not claimed.
- **Do not touch what he didn't ask to touch:** guard, welcome banner, Academy untouched and byte-verified; fix-7's proven items untouched in code.
- **Harvest, never invent:** the strips, clearance, and `fcOpenWorld` destination are all harvested verbatim from the fix-6 base and the page's own code; no new part invented.
- **Prove before report:** byte proof is complete and in this report; live proof is explicitly pending, not claimed.

## Self-score

- **Bytes: 10/10.** Diff is exactly the 5 intended opcodes; FRAG diff exactly the 3 intended changes; guard byte-identical; 101 scripts parse; laws delta 0.
- **Design: 9/10.** The hide-while-cover-visible approach is the only one that satisfies the acceptance at all scroll positions; the 800 `.top` trim has measured slack. One open concern: the rail-toggle's scrollW (63) vs clientW (46) at 800 was left untouched — it may still clip its glyph at +5% font; the probe will say.
- **Live proof: 0/10 — not run.** Blocked by the VM browser death, not by the build. This is the whole of what remains, and it is named, not hidden.

## What was NOT proven (do not present as proven)

- Any live behaviour of the fix-8 bytes (items 1–4, regressions, the +5% probes) — the browser flap blocked every live run.
- Whether VM Firefox loads Google Fonts once the room opens (affects whether 800 `.top` measurements are real-font or fallback-font). The Chromium run, when it happens, goes through the forwarder, so fonts should load; the measurement records `document.fonts` status.
- Whether the 761px edge of the `.top` trim fits at +5% font (expected marginal, ~6px short; gate widths are 800+).

## Files

- Working copy + scripts: `~/workspace/team-nitro/personal-frame-fix8-20261119/` (`fixed.html`, `fix8.js`, `verify8.py`, `browser-retry.sh`, `proof/`)
- This report: `~/workspace/team-nitro/personal-frame-fix8-20261119/maker/MAKER-REPORT.md`
- Base reference: `~/workspace/team-nitro/personal-frame-fix7-20261119/fixed.html`
