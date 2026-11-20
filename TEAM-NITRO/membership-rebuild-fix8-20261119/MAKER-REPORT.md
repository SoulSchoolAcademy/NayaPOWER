# MAKER REPORT — Membership rebuild fix-8

## Filing identity

| | Base (fix-7 tip) | Fixed (fix-8) |
|---|---|---|
| Branch | `membership/rebuild-fix7-20261119` | **`membership/rebuild-fix8-20261119`** |
| Tip | `ad3088a4` (`ad3088a41fadbe1eeae9150153d38f2865cf1bec`) | **`4d86ea278ef0c098faf87e409e47d8d4c5d41ff5`** |
| Blob | `56a552ed` | **`b13c17104a188e3b53bbbe77483fd4805afc29f2`** |
| Size | 2,374,360 B | **2,373,535 B** (−825 B) |
| sha256 | `0e9a65509322430d3e8b97d7d74d4639f6749291c88e4c6c0a1aca512991f995` | **`f576348d820aa10074c5b7ae9bfcafc7bae0852fe981b99945abfc120e6a4bf4`** |
| Lines | 23,707 (`wc -l`; brief said 23,708) | **23,699** (net −8) |

**Parent tip:** `ad3088a41fadbe1eeae9150153d38f2865cf1bec` (branch created fresh from the fix-7 tip via the git-data API; the fix-8 branch contains fix-7 by inheritance).

**Staged link:**
`https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/membership-rebuild-20261119/membership-rebuild.html&ref=membership/rebuild-fix8-20261119&cb=b13c17104a188e3b53bbbe77483fd4805afc29f2`

**Staged verification (curl, this round):** staged body sha256 `f576348d820aa10074c5b7ae9bfcafc7bae0852fe981b99945abfc120e6a4bf4`, 2,373,535 B — **exact match to the filed blob.** The filed bytes were also re-verified by a fresh blob-API read-back (size + sha256 recomputed by the filer). The staged copy contains 7 `naya-notif-bar` mentions (5 fallback lookups + 2 comments) and **zero** creation assignments.

**Base verification (this round):** the local fix-7 copy (`checker-independent/fixed.html`) sha256 `0e9a6550…91f995`, 2,374,360 B — **exact match to the coordinator-verified base** — so work started from those bytes, no fresh blob fetch needed. (The coordinator verified the base from the git blob API; I verified the local copy against the coordinator's sha before editing.)

**Filing method:** `maker/file_fix8.py` (adapted from fix-7's `file_fix7.py`: git-data API branch create from the fix-7 tip, contents-API PUT, fresh blob-API read-back). No multi-MB base64 staged to disk; bytes piped on stdin. Report filed separately to `TEAM-NITRO/membership-rebuild-fix8-20261119/MAKER-REPORT.md` on the same branch.

## Diff summary

**12 hunks, 40 removed lines, 32 added lines** (`diff base.html fixed.html`). Every hunk is inside the NayaNotif / bottom-bar wiring or its comments. **Nothing else changed.** In particular:

- The live bar's static markup (`<nav id="os-bottom3" …>`, six tiles) is **byte-identical** (sha of the extracted nav line matches base exactly). Order and colours untouched: ADD `#8e24aa` · MAIL `#0f52ba` · ACTIVITY `#07925f` · WORLDS `#d4a017` · ECOSYSTEM `#c2410c` · CONNECT `#c62828`.
- The fix-7 **F2 Space-gate line** (line 5845, `FIX-7 (item 3b)` — requires pane AND course visible) is **untouched**; the diff has no hunk near it. The fix-7 → fix-6 merge note carries forward unchanged: merging fix-7 onto the fix-6 branch conflicts on that one line; resolution takes fix-7's line.
- No CSS rule changed, no font-size changed, no lesson markup changed, no theatre/player code changed, no `updateDock` change. The lessons LIST plus/Add pill is untouched (Shawn's answer owed — his call, not mine).

## Defect 1 — DOUBLED BOTTOM BAR: FIXED, proven by real tap

**Root cause (found in the bytes, not guessed):** the stale bar was never static markup — `NayaNotif.init()` *built* it. The script runs mid-document, **before** the static `#os-bottom3` nav parses at the end of the file, so `getElementById('os-bottom3')` returned null at init time, the early-return path never ran, and init fell through to `document.createElement('nav')` with id `naya-notif-bar` (Mail · Activity · Spaces, harvested Hub trio) and appended it to the body. The static six-tile bar parsed afterwards. Both bars were `display:flex`, both fixed at the bottom, overlapping y 1002–1080 — the ghost icons the eye cropped.

**The fix (full removal, not `display:none`):**

| Hunk | Change |
|---|---|
| `init()` | The whole creation branch is deleted (ICONS, SEGS, `createElement`, append, its listeners). `init()` now only wires a bar that already exists; if none exists yet it returns, and the DOMContentLoaded call below retries once the document has parsed. No `createElement('nav')` remains anywhere in the file; no `id = 'naya-notif-bar'` assignment remains. |
| `window.NayaNotif.init()` | Deferred to DOMContentLoaded (readyState-guarded), so init now *sees* the static `#os-bottom3` and takes its early-return path: `refresh()` (count bubbles) and `syncStack()` land on the live bar. |
| Fold listener, `refresh()`, `syncStack()`, `init()`, `pad()` | All five `getElementById('naya-notif-bar')\|\|getElementById('os-bottom3')` lookups reordered to prefer `#os-bottom3` first (stale id kept only as a fallback). The fold's duplicated third operand (`\|\|…os-bottom3` twice) is simplified in the same line. |
| `saClose`, `saShowToc`, `saShowView` (audios) | The three `_nb` show/hide lines removed (they were guarded no-ops once the element can never exist). The FIX-2b comment that described hiding "the faded notif trio" is corrected to record that the trio is gone; the six-tile bar stays on Audios per FIX-6. |
| Fold comment | Corrected: the trio is the live six-tile bar, no longer "built by NayaNotif". |

**Why the deferred init is safe:** nothing else calls `NayaNotif.refresh()`/`tap()`/`bump()` (grep: only the definition + the init call). The stale bar's buttons were the only `tap()` callers. `body.has-notif` has no CSS rule (grep: only the two JS sets). `--notif-h` is set by `syncStack()` but consumed nowhere. `.notif-count` is `display:none` in CSS by default, so `refresh()` now writing `display:none` onto the live bar's zero-count bubbles changes nothing visible; when a count is > 0 the bubble now shows on the *live* bar, which is what the harvested component intended.

**Proof — bottom-bar census on every view (harness, real taps, Playwright Firefox):** `visibleBarCount == 1`, `staleExists == false`, `#os-bottom3` `display:flex` visible, on **every** probed view: fresh load, course, Day 1 lesson, Audios, Videos, chooser, theatre, lesson close — desktop 1920×1080 (bar y 980–1080, h 100) and phone 390×844 (bar y 752–844, h 92). Screenshots `80`, `81`, `85`, `86`, `90`, `91`, `95` show six clean tiles with **no ghost icons behind them** — compare the eye's `crop-6a-bottom.png` / `61` / `64`, where the faint envelope/pulse/house peeked out. The scroll-fold still drives the live bar: screenshot `92` (taken 1.2 s after a scroll) caught it mid-return, dimmed and rising — the fold listener now fades `#os-bottom3` itself.

## Defect 2 — LESSON VIDEO-HEADER TITLE CLIPPED AT 390: ATTRIBUTED, NOT A PAGE DEFECT — no fake rule shipped

**What I found (measured, not assumed).** The clipped text ("🔱 ACTIVATE YOU / E" / "NayaNET - Create. Connect. Gr…") is **YouTube's own embed title bar, rendered inside the cross-origin `youtube-nocookie` iframe**. Evidence, from `probe-defect2.py` at 390 in the Day 1 lesson view:

- **No page-DOM element holds the clipped strings.** A walk of every `body *` leaf found zero elements containing `NayaNET - Create` (the string occurs nowhere in page JS except the login bottombar `Create. Connect. Grow with us.` and a config value — neither is in the lesson view). The full title exists on the page in exactly one place: the lesson `h3`.
- **Geometry puts the title block inside the iframe.** `.sa-cover` y 2751–2901; `.sa-sixteen` / iframe y 2918–3066 (264×148); `h3` y 3194–3293. The title block in screenshots `61`/`64` sits inside the iframe's rect.
- **The iframe document is not reachable.** `frame.contentDocument` is `null` (cross-origin) — page CSS/JS cannot style anything inside it. YouTube's embed title bar is single-line with ellipsis at *every* width by design; there is no embed parameter that makes it wrap, and widening the player cannot make a ~70-character title read in it either.
- **The full title already reads on the page, directly below the player.** The lesson `h3` ("🔱 ACTIVATE YOU / EXPERIENCE ME! Day #1 of the Naya POWER Academy.🔱") wraps normally at 390: `scrollWidth == clientWidth == 266`, `whiteSpace: normal`, 99 px tall (3 lines at desktop, 4 lines in screenshot `92`). Harness step P1b proves it; screenshot `92-phone-h3.png` shows it in full.

**What I did:** nothing to the lesson markup or CSS. A `≤480px` media query "making the video-header title wrap" would have been a no-op on YouTube's chrome — shipping it would have claimed a fix I could not prove, and the re-eye would have failed it again. The brief's prescribed mechanism assumed the header was page markup; the bytes say it is not. I did not add a page-owned duplicate header above the player either: it would double the `h3` 200 px below it, and that presentation call belongs to Shawn / a later round, not a maker fix.

**What the coordinator / re-eye should judge:** the lesson title reads in full in the `h3` at 390 (screenshot `92`). If the re-eye still fails the *player chrome* truncation, the fix is a product decision (e.g. theatre-only playback, a custom thumbnail header, or accepting YouTube's standard narrow-width truncation) — not a CSS round. The theatre's own title (`#saTheatreTitle`, single-line ellipsis at 15 px, pre-existing chrome, not failed by the eye) is the same pattern and was left untouched.

## Regression — all proven by real tap (harness 31/31 PASS + feed-card probe)

Harness: `maker/harness.py` (Playwright Firefox, local fixed file), log `maker/harness-log.json`, screenshots `80`–`86`, `90`–`95`. Feed-card probe: `maker/probe-feedcard.py`, screenshot `96`.

| Item | Result |
|---|---|
| **Defect 1 — one bar, every view** | PASS — census `visibleBarCount 1`, `staleExists false` on all 9 desktop + 6 phone probes; tiles in order with exact deep colours (D0). |
| **F1 — resume re-lights ON AIR** | PASS (D3c) — bare pause leaves audio paused + deck ON AIR (documented); resume via `#dPlay` → playing (t 5.7 advancing) + deck ON AIR. |
| **F2 — Space gate** | PASS (D4a–d) — Space pauses in Audios; Space resumes in Audios; Space does **not** resume at course home; Space does **not** resume after course closed (audio stays paused, t frozen 15.63). |
| **F3 — theatre rebuild twice** | PASS — Videos Watch opens theatre twice, same title (D2a/b, "🔱 BECOME / COMPOUND! Day #5, Lesson #of 5"); feed-card ▶ Watch opens theatre too (probe: 5 Watch buttons visible, theatre title Day #1, lesson pane not open, one bar). |
| **Audio stops, all six leave paths** | PASS — Lessons tab 0.06 s, Videos tab 0.11 s, chooser 0.01 s, **ADD tile 0.10 s** (listened hardest), browser Back 0.26 s, Back button 0.62 s; deck READY after each. |
| **Lesson-view bar ADD-only, every entry path** | PASS — chooser pick (D6a), "Open Lessons →" card (D6b), "Next lesson →" Day 2 (D6c): `body.sa-lesson-open` true, rooms-plus `none`, feed add-tab `none`, one bar. Close → full bar returns (D6d: rooms-plus `grid`, feed add-tab `flex`). |
| **Phone 390 leg** | PASS (P0–P5) — door, Audios play (t advancing, ON AIR) / stop (paused), Videos Watch → theatre, lesson ADD-only bar, six-tile bar, `scrollW 390` throughout, no horizontal overflow. |
| **Lesson h3 at 390** | PASS (P1b) — full title wraps, `scrollW == clientW == 266`, screenshot `92`. |

Page errors seen during the harness: only the standing `updateDock is not defined` (carried forward below) and one `A network error occurred` in the feed-card probe (VM network wart; the theatre still opened). Audio was judged by page state (element paused / currentTime advancing / deck), never claimed as heard. Supabase reads are CORS-blocked in the VM browser and R2 / `i.ytimg.com` thumbnails do not load there — environmental, not page defects (the lesson cover paints black in the VM for that reason).

## Laws delta — 0

`check-design-laws.py` run on base and on fixed: **identical — 674 FAILs, 139 WARNs on both.** All 674 FAILs are pre-existing §2.3 below-17px font sizes spread across the whole file (largest groups: 14 px ×117, 13 px ×77, 11 px ×70); my diff touches no font-size, no colour, no text, so the delta is exactly zero. The standing sub-17px FAILs are not this round's scope and were not failed by the fix-7 eye.

## §11 design-laws check (in writing)

- **Five gates.** (1) Right: removing a doubled bar serves everyone who sees the page; refusing a fake CSS fix for defect 2 serves the truth over the appearance of progress. (2) What they truly need: the eye's GOES BACK asked for one bar and a readable lesson title — the bar is one, the title reads in full in the `h3`. (3) Mine to do: the brief's scope, staged only — no merge, no live deploy, no message to the user. Money, credentials, destructive actions untouched. Nothing removed or moved that he didn't ask to touch (the live bar is byte-identical; only the stale bar and its three dead references went). (4) Now: small round, landed inside the hour. (5) Prove it: census numbers, latencies, screenshots and staged sha256 above — receipt before report.
- **Real objects, obsidian inside, elevation:** the live bar is the harvested Hub bar, verbatim (file comment names blob `84e02035…`); nothing rebuilt, nothing restyled.
- **One set of colours, one bottom bar:** PASS now — one bar, six tiles, same order, same deep hexes on every view, both widths.
- **One icon that lights up:** PASS — ON AIR pill lights on resume; no icon-plus-separate-light duplication introduced.
- **Type / reading:** PASS on the page — the lesson `h3` reads in full at 390; the truncated line is YouTube's own chrome, outside the page (see defect 2).
- **Alive on hover:** NOT TESTED — headless Firefox has no mouse hover; not claimed. (The scroll-fold returning, caught in screenshot `92`, is observed behaviour, not a hover proof.)
- **Read as a reader:** the lesson reads cleanly top to bottom at both widths; the one remaining visual wart is YouTube's own title truncation inside the player, with the full title directly below it.
- **The sense check (the page, not the diff):** the page as Shawn would see it has one bottom bar and a fully readable lesson title. I did not double anything up, and I did not ship a rule that changes nothing the eye can see.
- **Scorecard — why not a 10:** (1) the player's own title bar still truncates at 390 — YouTube's chrome, not ours, but his eye will still see it; (2) the 674 pre-existing sub-17px FAILs stand; (3) hover aliveness is unproven headless. The round is a 9 as filed; the eye walk takes it to 10 or names the product call on defect 2.

## Standing watch items (carried forward, do not fix — same as the brief)

- `updateDock()` undefined — throws on every `play()` after lighting ON AIR; also aborts `play()` before `render()` runs (harvest-repair note for a later round). Seen in this harness's page errors.
- Fast error-page hole ≥ 250 ms settles silently.
- Bare `pause()` leaves ON AIR (documented player behaviour — re-proven D3b).
- False-alarm toast "Audio could not load" while audio plays (error code 3, R2 decode wart — seen in this harness: `err: 3` on every play while `currentTime` advances).
- "Lesson #of 5" Day 5 title (pre-existing Academy source defect — seen in theatre titles D2a/b).
- Lessons LIST plus/Add pill untouched (Shawn's answer owed).

## What I could not prove

- **Defect 2 as literally prescribed** (page CSS wrapping the video-header title): proven *unfixable* by page CSS, with the evidence above — the re-eye / coordinator must rule on it. I did not fake it.
- **Hover aliveness** (headless has no mouse) and **audible audio** (headless can't hear; judged by element + deck + ON AIR only).
- **YouTube player paint in the VM:** the lesson iframe's thumbnail/chrome do not paint in the VM browser (network-blocked `i.ytimg.com` / embed load); the eye's fix-7 diag already proved the chrome paints once scrolled into view, and my diff does not touch the player.

## Files (maker/)

`base.html` (verified base) · `fixed.html` (filed) · `staged-check.html` (staged read-back, sha-verified) · `harness.py` + `harness-log.json` (31/31) · `probe-defect2.py` (attribution) · `probe-feedcard.py` (F3 feed-card path) · `file_fix8.py` (filer) · screenshots `80`–`86`, `90`–`96`, `probe-d2-lesson390.png` · this report.
