# CHECKER REPORT — Membership rebuild fix-8 (INDEPENDENT)

## VERDICT: PASS

**Fix-8 passes. Both fix-7 eye defects are closed: (1) the doubled bottom bar is gone — exactly one bar renders on every view at both widths, by full removal of the stale bar's creation, not by hiding; (2) the lesson title clip at 390 is adjudicated complete — my own probe proves the clipped text is YouTube's own embed chrome inside the cross-origin iframe, not page markup, and the full lesson title already reads in the wrapping `h3` directly below the player. No page-side remedy was wrongly dismissed (see Defect 2). The full fix-7 regression list re-proves by real tap (33/33 in my harness + a focused feed-card probe), the laws delta is 0, the staged bytes match the filed blob exactly, and the three-way cross-check proves my harness detects the defect on the base. No merge, no live deploy, no message to the user.**

- Independent checker: fresh seat, did not build fix-8. Every claim below was re-proven by my own runs; the maker's report was read as input only, never as proof. My harness (`checker_harness.py`) was written fresh; it does not reuse the maker's harness code.
- Staged URL: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/membership-rebuild-20261119/membership-rebuild.html&ref=membership/rebuild-fix8-20261119&cb=b13c17104a188e3b53bbbe77483fd4805afc29f2
- Browser: Playwright Firefox headless (VM), desktop 1920×1080 and phone 390×844, against the local blob-verified files served on 127.0.0.1:8821. Audio judged via page state (element + deck + ON AIR), never claimed as heard.

## 1. Filing verification (git blob API, `gh-direct.py`)

| | Base (fix-7 tip) | Fixed (fix-8) |
|---|---|---|
| Branch | `membership/rebuild-fix7-20261119` | `membership/rebuild-fix8-20261119` |
| Tip | `ad3088a41fadbe1eeae9150153d38f2865cf1bec` | HTML commit `4d86ea278ef0c098faf87e409e47d8d4c5d41ff5`; branch tip `cb813a5da22dc9b57b81e8a9e70ae4946794ccdd` (report commit, parent `4d86ea27`) |
| Blob | `56a552edf37acb03f59e5bebd96f6d41922316cc` | `b13c17104a188e3b53bbbe77483fd4805afc29f2` |
| Size | 2,374,360 B | 2,373,535 B (−825 B) |
| sha256 | `0e9a65509322430d3e8b97d7d74d4639f6749291c88e4c6c0a1aca512991f995` | `f576348d820aa10074c5b7ae9bfcafc7bae0852fe981b99945abfc120e6a4bf4` |
| Lines | 23,707 (`wc -l`) | 23,699 (net −8) |

Verified by my own script (`verify_blobs.py`): branch refs, contents metadata, and blob-API fetches all agree; saved copies re-read and re-hashed after write. Maker report filed at `TEAM-NITRO/membership-rebuild-fix8-20261119/MAKER-REPORT.md`, blob `dcbb94b170227967f04934f28ecc3cd4a1eb5314`, size 16,458 B, sha256 `37da655da7fa31b59daed7d408fa55310d5a6cd93a509a14a0e132daddab4db4` — all match the maker's claims. (Note: the branch tip is the report commit `cb813a5d`, not the HTML commit `4d86ea27`; the HTML commit's parent is the fix-7 tip, so fix-8 contains fix-7 by inheritance. Consistent with the maker's report.)

**Staged byte-match: PASS.** `curl` of the staged URL: HTTP 200, 2,373,535 B, sha256 `f576348d820aa10074c5b7ae9bfcafc7bae0852fe981b99945abfc120e6a4bf4`, `cmp` identical to the filed blob.

## 2. Diff replay — exactly as claimed, nothing else

`diff -U0 base.html fixed.html`: **12 hunks, 40 removed / 32 added lines, net −8.** Every hunk is inside the NayaNotif / bottom-bar wiring or its comments, plus three `_nb` show/hide removals (`saClose`, `saShowToc`, `saShowView`). Nothing else changed. Verified in detail:

- **Live bar byte-identical:** the `#os-bottom3` nav line sha256 is `8e6f457a2d9e262daec714fb65ce6d645387b01803b94e268ee1bf32c48311de` in both files. Order and colours untouched: ADD `#8e24aa` · MAIL `#0f52ba` · ACTIVITY `#07925f` · WORLDS `#d4a017` · ECOSYSTEM `#c2410c` · CONNECT `#c62828`.
- **Fix-7 F2 Space-gate line untouched:** line 5845 sha256 `a250a0d9406aa3a147f42034b603a942a4faa23845680a80d145844e4a8f1ce5` in both files. The fix-7 → fix-6 merge note carries forward unchanged.
- **Full removal, not `display:none`:** zero `createElement('nav')` and zero `id = 'naya-notif-bar'` assignments remain in the fixed file (base had both, line 14667). Remaining `naya-notif-bar` mentions in fixed: 7 — five fallback lookups (`getElementById('os-bottom3')||getElementById('naya-notif-bar')`) plus two FIX-8 comments. No JS still references the stale element in a way that throws (harness page errors contain no NayaNotif error).
- **Root cause independently confirmed from the base bytes** (not taken from the maker): in the base, `NayaNotif.init()` is defined at ~line 14657 and called synchronously at line 14687 (`window.NayaNotif.init();`), while the static `#os-bottom3` nav does not parse until line 23707. So at init time `getElementById('os-bottom3')` returned null, the early-return path never ran, and init fell through to the creation branch (`document.createElement('nav')`, id `naya-notif-bar`, Mail · Activity · Spaces), appending a second bar that rendered behind the live six. The maker's root-cause claim is correct.

## 3. Defect 1 — doubled bottom bar: FIXED

DOM census on every view, both widths — **exactly one bar visible everywhere**:

| View | Width | `visibleBarCount` | `staleExists` | Live bar rect |
|---|---|---|---|---|
| Fresh load | 1920 | 1 | false | x0 y980 w1920 h100 |
| Course / Day 1 lesson | 1920 | 1 | false | x0 y980 w1920 h100 |
| Audios | 1920 | 1 | false | x0 y980 w1920 h100 |
| Videos | 1920 | 1 | false | x0 y980 w1920 h100 |
| Theatre (×2) / feed-card theatre | 1920 | 1 | false | x0 y980 w1920 h100 |
| Lesson close / after close | 1920 | 1 | false | x0 y980 w1920 h100 |
| Fresh load | 390 | 1 | false | x0 y752 w390 h92 |
| Lesson / Audios / Videos / theatre | 390 | 1 | false | x0 y752 w390 h92 |

Tiles in order with exact deep colours on every census: ADD `#8e24aa`, MAIL `#0f52ba`, ACTIVITY `#07925f`, WORLDS `#d4a017`, ECOSYSTEM `#c2410c`, CONNECT `#c62828`.

**Visual comparison:** my desktop bottom crop `c80b-desktop-bottom.png` and phone crop `c90b-phone-bottom.png` show six clean tiles with no ghost icons, against the eye's `crop-6a-bottom.png` where the faint envelope behind MAIL and house behind ECOSYSTEM peeked out. The ghost is gone.

## 4. Defect 2 — lesson title clipped at 390: ADJUDICATED COMPLETE (not a page defect)

**Ruling (a): the clipped text is YouTube's own embed chrome inside the cross-origin iframe, and the page `h3` reads fully. The round is complete on defect 2 by adjudication.** My own probe evidence (fresh probe, `probe_d2_geometry.py`, plus harness steps P1b/P1c at 390):

- **No rendered page element holds the clipped strings.** A walk of every `body *` leaf found zero rendered elements containing `NayaNET - Create` or `Create. Connect. Gr`. The only matches were inside `STYLE`/`SCRIPT` source text (the login bottombar string `Create. Connect. Grow with us.` in JS) — not rendered, not in the lesson view.
- **Geometry puts the title block inside the iframe.** Lesson iframe rect x63 y349 w264 h148 (`.sa-sixteen` x62 y−1 w266 h150); `document.elementFromPoint` at the centre of the title area (iframe centre, 25% down) returns the `IFRAME` itself. The title block in screenshots `c92-phone-d2-lesson.png` / `c97-phone-player-geometry.png` sits inside that rect.
- **The iframe document is not reachable.** `contentDocument` is `null` (cross-origin `youtube-nocookie`, src `https://www.youtube-nocookie.com/embed/ZRIfvxCsYWY?rel=0`). Page CSS/JS cannot style anything inside it.
- **The full title already reads on the page, directly below the player.** Lesson `h3`: `🔱 ACTIVATE YOU / EXPERIENCE ME! Day #1 of the Naya POWER Academy.🔱` — `scrollWidth == clientWidth == 266`, `whiteSpace: normal`, 99 px tall (4 lines), visible in full in `c92`/`c97`.
- **No page-side remedy was wrongly dismissed.** The player is already at maximum available width (264 px inside a 282 px cover inside a 326 px card at 390); widening cannot make a ~70-character title read in a 264 px title bar. The embed's only parameter is `rel=0`; YouTube offers no embed parameter that makes its title bar wrap (the title bar is single-line with ellipsis by design at every width). Shipping a `≤480px` media query for it would have been a no-op the re-eye would fail again — the maker was right not to ship one, and right not to add a duplicate page header above the player (it would double the `h3` 200 px below). **If the chrome truncation itself must go, that is a product decision for the captain's eye (e.g. theatre-only playback, a custom thumbnail header, or accepting YouTube's standard narrow-width truncation) — not a checker fail.** I do not fail the round for it.

## 5. Fix-7 regression — all proven by real tap (my harness, 33/33 PASS)

Harness `checker_harness.py` (Playwright Firefox, local blob-verified fixed file), log `checker-log.json`; screenshots `c80`–`c87`, `c90`–`c97`.

| Item | Result |
|---|---|
| **F1 — resume re-lights ON AIR** | PASS (C3c) — bare pause leaves audio paused + deck ON AIR (documented, C3b); resume via `#dPlay` → playing (t 7.26 advancing) + deck ON AIR. |
| **F2 — Space gate** | PASS (C4a–d) — Space pauses in Audios; Space resumes in Audios; Space does **not** resume at course home; Space does **not** resume after course closed (audio stays paused, t frozen 14.31). |
| **F3 — theatre rebuild twice** | PASS — Videos Watch opens theatre twice, same title (C2a/b, `🔱 BECOME / COMPOUND! Day #5, Lesson #of 5`); feed-card ▶ Watch opens theatre too (focused probe `probe_feedcard.py`: 5 Watch buttons visible, theatre title Day #1, lesson pane not open, one bar). |
| **Audio stops, all six leave paths** | PASS — Lessons tab 0.10 s, Videos tab 0.03 s, chooser 0.12 s, **ADD tile 0.01 s** (listened hardest), browser Back 0.09 s, Back button 0.02 s; deck READY after each. |
| **Lesson-view bar ADD-only, every entry path** | PASS — chooser pick (C6a), "Open Lessons →" card (C6b), "Next lesson →" Day 2 (C6c, h3 `🔱 REMEMBER / COMPOUND! Day #2`): `body.sa-lesson-open` true, rooms-plus `none`, feed add-tab `none`, one bar. Close → full bar returns (C6d: rooms-plus `grid`, feed add-tab `flex`). |
| **Phone 390 leg** | PASS (P0–P5) — door, Audios play (t advancing, ON AIR) / stop (paused), Videos Watch → theatre, lesson ADD-only bar, six-tile bar, `scrollW 390` throughout, no horizontal overflow. |

Page errors seen in my harness: `updateDock is not defined` (standing, twice) and `A network error occurred.` (VM network wart; the theatre still opened). Audio judged by page state only.

## 6. Three-way cross-check — harness detects the defect on the base

Same harness run against the fix-7 base bytes (`checker_harness.py cross`, log `checker-log-cross.json`): **2/2 as expected — the doubled bar is present.** Fresh load: `visibleBarCount == 2`, `staleExists == true`, stale `#naya-notif-bar` `display:flex` visible at x0 y1002 w1920 h78 overlapping the live bar (y980 h100); lesson view identical. Screenshots `x90-base-fresh.png`, `x91-base-lesson.png`, crop `x90b-base-bottom.png`. The harness that passes on fixed fails exactly the defect-1 behaviours on base — it proves what it claims.

## 7. Laws — delta 0

`check-design-laws.py` run by me on base and on fixed: **674 FAILs / 139 WARNs on both, delta 0.** All 674 FAILs are pre-existing §2.3 below-17px font sizes across the whole file; the diff touches no font-size, no colour, no text. The standing sub-17px FAILs are not this round's scope and were not failed by the fix-7 eye.

## §11 design-laws check (in writing)

Read first: `THE-NAYA-DESIGN-LAWS.md`, `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md`, `THE-HEART-OF-THE-MACHINE.md`, `team-nitro/AGENTS.md`.

- **Five gates.** (1) Right: removing a doubled bar serves everyone who sees the page; refusing a fake CSS fix for defect 2 serves the truth over the appearance of progress. (2) What they truly need: the eye's GOES BACK asked for one bar and a readable lesson title — the bar is one, the title reads in full in the `h3`. (3) Mine to do: checking only — no merge, no live deploy, no message to the user; money, credentials, destructive actions untouched. (4) Now: checked in the same window, nothing sat. (5) Prove it: blob-API hashes, diff replay, census numbers, latencies, geometry probe, screenshots and staged sha256 above — receipt before report.
- **Real objects, obsidian inside, elevation:** PASS — the live bar is the harvested bar, byte-identical; nothing rebuilt, nothing restyled.
- **One set of colours, one bottom bar:** PASS now — one bar, six tiles, same order, same deep hexes on every view, both widths.
- **One icon that lights up:** PASS — ON AIR pill lights on resume; no icon-plus-separate-light duplication introduced.
- **Type / reading:** PASS on the page — the lesson `h3` reads in full at 390; the truncated line is YouTube's own chrome, outside the page (see §4).
- **Alive on hover:** NOT TESTED — headless Firefox has no mouse hover; not claimed.
- **Read as a reader:** the page reads cleanly top to bottom at both widths (`c80` desktop fresh, `c91`/`c92`/`c97` phone lesson). The one remaining visual wart is YouTube's own title truncation inside the player, with the full title directly below it — a product call, not a checker fail.
- **The sense check (the page, not the diff):** the page as Shawn would see it has one bottom bar and a fully readable lesson title. Nothing doubled up, nothing faked.
- **Scorecard — why not a 10:** (1) the player's own title bar still truncates at 390 — YouTube's chrome, not ours, but his eye will still see it until the product call is made; (2) the 674 pre-existing sub-17px FAILs stand; (3) hover aliveness is unproven headless. The round is a 9 as filed; the eye walk takes it to 10 or names the product call on defect 2.

## Standing items (verified unchanged, not failed)

- `updateDock()` undefined — still throws on play (seen in my harness page errors). Unchanged (2 mentions in both files).
- Fast error-page hole ≥ 250 ms — not re-probed; standing.
- Bare pause leaves ON AIR — re-proven (C3b), documented behaviour.
- False-alarm audio toast — `audio.error.code 3` on every play while `currentTime` advances (seen in every play step of my harness).
- "Lesson #of 5" Day 5 title — seen in theatre titles (C2a/b).
- Lessons LIST plus/Add pill untouched — no hunk near it; the diff touches only NayaNotif wiring/comments.

## What I could not prove

- Hover aliveness (headless has no mouse) and audible audio (headless can't hear; judged by element + deck + ON AIR only).
- YouTube player paint in the VM: the lesson cover thumbnail does not load here (`i.ytimg.com` blocked), but the embed chrome title block paints (screenshots `c92`/`c97`) and the theatre paints — environmental, not a page defect.

## Files (checker-independent/)

`verify_blobs.py` · `base.html` (blob-verified) · `fixed.html` (blob-verified) · `staged-check.html` (staged read-back, sha-verified) · `diff.txt` (12 hunks, 40−/32+) · `checker_harness.py` + `checker-log.json` (33/33) + `checker-log-cross.json` (2/2 on base) · `probe_feedcard.py` · `probe_d2_geometry.py` · screenshots `c80`–`c87`, `c90`–`c97`, `x90`–`x91` · this report.
