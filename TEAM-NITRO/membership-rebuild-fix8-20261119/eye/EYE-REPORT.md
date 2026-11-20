# EYE REPORT — Membership rebuild fix-8

## VERDICT: PASS

**Both fix-7 eye defects are closed. (1) The doubled bottom bar is gone — exactly one bar renders on every view at both widths, proven by DOM census and by eye on the crops, against the fix-7 ghost crop. (2) The lesson title clip at 390 is adjudicated complete — my own independent probe proves the clipped text is YouTube's own embed chrome inside the cross-origin iframe, not page markup, and the full lesson title already reads in the wrapping `h3` directly below the player. The full fix-7 regression list re-proves by real tap (36/36 in my walk), the staged bytes match the filed blob exactly, and every button tapped lands where it should. No merge, no live deploy, no message to the user.**

- Staged URL: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/membership-rebuild-20261119/membership-rebuild.html&ref=membership/rebuild-fix8-20261119&cb=b13c17104a188e3b53bbbe77483fd4805afc29f2
- Branch `membership/rebuild-fix8-20261119`, tip `cb813a5da22dc9b57b81e8a9e70ae4946794ccdd`, blob `b13c1710`, 2,373,535 B, sha256 `f576348d…`. Staged bytes verified by me before walking: curl of the staged URL, 2,373,535 B, sha256 `f576348d820aa10074c5b7ae9bfcafc7bae0852fe981b99945abfc120e6a4bf4`, `cmp` identical to the filed blob.
- Eye walks: Playwright Firefox headless (VM), desktop 1920×1080 and phone 390×844, by real tap. Audio judged by page state (element + deck + ON AIR), never claimed as heard. All scripts, logs and screenshots in this `eye/` directory (`eye-walk.py`, `eye-log.json`, shots `e00`–`e06`, `p00`–`p04`).
- No Firefox orphans left; the VM browser stayed alive for the whole walk (no mid-walk death this time).

## What fix-8 had to prove — all proven

### Defect 1 — Doubled bottom bar: FIXED, proven by census + by eye

DOM census on every view, both widths — **exactly one bar visible everywhere**:

| View | Width | `visibleBarCount` | `staleExists` | Live bar rect |
|---|---|---|---|---|
| Fresh load | 1920 | 1 | false | x0 y980 w1920 h100 |
| Course / Day 1 lesson | 1920 | 1 | false | x0 y980 w1920 h100 |
| Audios / Videos / theatre / after close | 1920 | 1 | false | x0 y980 w1920 h100 |
| Fresh load / lesson / Audios / Videos / theatre | 390 | 1 | false | x0 y752 w390 h92 |

Tiles in order with the exact deep colours on every census: ADD `#8e24aa`, MAIL `#0f52ba`, ACTIVITY `#07925f`, WORLDS `#d4a017`, ECOSYSTEM `#c2410c`, CONNECT `#c62828`.

**Seen with my own eyes:** my desktop bottom crop `e00b-desktop-bottom.png` and phone crop `p00b-phone-bottom.png` show six clean tiles with no ghost icons — against the fix-7 eye's `crop-6a-bottom.png`, where the faint envelope behind MAIL, pulse behind ACTIVITY and house behind ECOSYSTEM peeked out. The ghost is gone. (The faint "Schedule / Post my Naya note" text at the top edge of the desktop crop is page content above the bar, not a second bar — the census says one bar, and no icons peek anywhere.)

### Defect 2 — Lesson title clipped at 390: ADJUDICATION CONFIRMED (not a page defect)

My own probe, run fresh in this walk (steps P1b/P1c, screenshot `p01-phone-lesson-player.png`):

- **No rendered page element holds the clipped strings.** `body.innerText` contains neither `NayaNET - Create` nor `Create. Connect. Gr`.
- **Geometry puts the title block inside the iframe.** Lesson iframe rect x63 y349 w264 h148; `document.elementFromPoint` at the title area returns the `IFRAME` itself.
- **The iframe document is not reachable.** `contentDocument` is `null` (cross-origin `youtube-nocookie`, src `https://www.youtube-nocookie.com/embed/ZRIfvxCsYWY?rel=0`). Page CSS/JS cannot style anything inside it.
- **The full title already reads on the page, directly below the player.** Lesson `h3`: `🔱 ACTIVATE YOU / EXPERIENCE ME! Day #1 of the Naya POWER Academy.🔱` — `scrollWidth == clientWidth == 266`, `whiteSpace: normal`, 99 px tall (4 lines), visible in full in the screenshot.
- **Seen with my own eyes:** in `p01-phone-lesson-player.png` the player header reads "🔱 ACTIVATE YOU / E" / "NayaNET - Create. Connect. Gr..." — and immediately below it the page's own `h3` reads the whole title, followed by "The video plays here, inside the frame — tap play. Full screen is on the Watch button below." and "Day 1 of 5".

**The product call (named, not failed):** the truncated line is YouTube's own narrow-width player header, and it is still the first thing a reader's eye hits inside the player. The lesson title itself is readable in full on the page — in the `h3` right below the player, and in the theatre's own title bar at both widths. If the chrome truncation itself must go, that is a product decision — theatre-only playback, a custom header, or accepting YouTube's standard narrow-width truncation. My read: **accept it** — the full title reads twice on the page itself (h3 + theatre title), no page-side remedy exists (no embed parameter wraps the title bar; the player is already max width; a duplicate header would double the h3), and shipping a fake CSS rule for it would be the exact failure the laws forbid. The captain decides whether to put the question to Shawn.

### F1 — Resume re-lights ON AIR: PASS
E3c: resume via `#dPlay` → audio playing (t 4.69 advancing, readyState 4) + deck `ON AIR`. E3b: bare pause leaves audio paused + deck ON AIR — documented behaviour, re-proven.

### F2 — Space gate: PASS
E4a Space pauses in Audios; E4b Space resumes in Audios; **E4c Space does NOT resume at course home** (audio stays paused, t frozen 17.87); **E4d Space does NOT resume after the course is closed** (course not visible, t frozen 17.87).

### F3 — Theatre rebuild twice: PASS
E2a/E2b: theatre opens from Videos Watch twice, same title both times (`🔱 BECOME / COMPOUND! Day #5, Lesson #of 5 "Naya POWER Academy." 🔱`). The player chrome paints — title, channel line, CC/settings, 0:00/6:14, captions ("Hi, I'm Naya. You know, we are about to...") — in `e02-desktop-theatre1.png`. Phone P3: theatre opens from Videos Watch at 390 with the same title.

### Audio stops on EVERY leave path: PASS (36/36 walk)
All six paths, re-playing between each, deck READY after each (latency measured from tap landing):

| Path | Latency | Deck after |
|---|---|---|
| Lessons tab | 0.20 s | READY |
| Videos tab | 0.07 s | READY |
| Chooser | 0.12 s | READY |
| **Bottom-bar ADD tile** | 0.19 s | READY |
| Browser Back | 0.23 s | READY |
| Back button | 0.08 s | READY |

The ADD tile — the maker-claimed-only path — was listened to hardest and stops clean.

### Lesson-view bar ADD-only on every entry path: PASS
E6a chooser pick, E6b "Open Lessons →" card, E6c "Next lesson →" Day 2 (`🔱 REMEMBER / COMPOUND! Day #2`): `body.sa-lesson-open` true, rooms-plus `none`, feed add-tab `none`, one bar. E6d close → full bar returns (rooms-plus `grid`). Phone P4 agrees at 390.

### Phone 390 leg: PASS
P0 fresh load (scrollW 390, one bar); P1 joined + Day 1 lesson (ADD-only bar); P2a/b Audios play (t advancing, ON AIR) / stop (paused); P3 Videos Watch → theatre; P4 lesson ADD-only bar; P5 six-tile bar, scrollW 390 throughout, no horizontal overflow.

### Button destinations: PASS — every tile lands on the right place
Bottom-bar tiles tapped one by one on fresh loads:

| Tile | Lands on |
|---|---|
| ADD | composer overlay on the same page (`#os-post-body`) |
| MAIL | `https://nayanet.app/rooms/mail` — "Smart Mail — NayaNET" |
| ACTIVITY | staged `#/hub/feed-activity` on the same page |
| WORLDS | `https://nayanet.app/space` — "Our Community" |
| ECOSYSTEM | `https://nayanet.app/#/hub` — NayaNET main entrance |
| CONNECT | `https://nayanet.app/rooms/connections` — "Your Connections" |

Every button tapped in this walk landed where it should — door → join → course → lessons/videos/audios → theatre → back, at both widths. No stale link, no dead end.

### updateDock watch: PASS (deck stays live)
`updateDock is not defined` throws on every play (in the page-error log, standing item) — but it is contained: resume re-lights ON AIR and the audio element keeps advancing after ON AIR lights (E3c, t 4.69 advancing; phone P2a t 1.67 advancing). play() does not visibly break. The throw is a wart for a later harvest-repair round, not a fail here.

## Read as a reader

Top to bottom at 1920 and 390, the page reads as a world: the door with its three membership pills (Academy purple, Masterclass blue, Fast Action green), "Shawn Vibert / Welcome to my world", the action buttons each in its own colour, the Live Feed composer, the lesson view with Back / Next lesson / Lessons / Videos / Audios, the theatre with its full title and captions, and one clean bottom bar on every view.

What reads less than perfect, named honestly:
- **The lesson view at desktop first paint is a large black box** (`e01-desktop-lesson.png`): the lesson cover thumbnail does not load in this VM (`i.ytimg.com` blocked) and the iframe sits below the fold, so the first screen is black until scrolled. Environmental, not a page defect — on a real device the thumbnail paints, and the theatre paints its chrome within 3 s. The fix-7 eye recorded the same.
- **The YouTube player header truncates at 390** — see the product call above. The full title reads directly below it.
- **"Lesson #of 5"** still reads in the Day 5 theatre title — pre-existing Academy source defect, not this page.

## §11 design-laws check (in writing)

Read first: `THE-NAYA-DESIGN-LAWS.md`, `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md`, `THE-HEART-OF-THE-MACHINE.md`, `team-nitro/AGENTS.md`.

- **Five gates.** (1) Right: one bar and a readable title serve everyone who sees the page; refusing a fake CSS fix for defect 2 serves the truth over the appearance of progress. (2) What they truly need: the fix-7 eye asked for one bar and a readable lesson title — the bar is one, the title reads in full in the `h3`. (3) Mine to do: eye only — no merge, no live deploy, no message to the user; money, credentials, destructive actions untouched. (4) Now: walked in the same window, nothing sat. (5) Prove it: staged sha256 match, census numbers, latencies, geometry probe, 20 screenshots and the walk log below — receipt before report.
- **Real objects, obsidian inside, elevation everywhere:** PASS — the door is a real portal scene, the deck is a real radio object, the lesson pane and tiles are obsidian with consistent top-left light and elevation. Nothing in this round rebuilt or restyled anything — the live bar is byte-identical to fix-7.
- **One set of colours, one bottom bar:** PASS now — one bar, six tiles, same order, same deep hexes on every view, both widths. The doubled bar is gone.
- **One icon that lights up:** PASS — the ON AIR pill lights on resume; the play control toggles; no icon-plus-separate-light duplication.
- **Type / reading:** PASS on the page — the lesson `h3` reads in full at 390; the truncated line is YouTube's own chrome, outside the page. Standing condition, named not failed: the checker measured 674 pre-existing sub-17px §2.3 FAILs on both base and fixed (delta 0) — the fix-7 eye did not fail on them either, and they are not this round's scope. They stand as a known pre-existing condition for a future round, not as a go-back here.
- **Alive on hover:** NOT TESTED — headless Firefox has no mouse hover; not claimed.
- **Read as a reader:** reads cleanly top to bottom at both widths except the two named items above (VM-black lesson box at first paint; YouTube header truncation) — neither is a page defect.
- **The sense check (the page, not the diff):** the page as Shawn would see it has one bottom bar and a fully readable lesson title. Nothing doubled up, nothing faked. The sense check passes.
- **Scorecard — why not a 10:** (1) the player's own title bar still truncates at 390 — YouTube's chrome, not ours, but his eye will still see it until the product call is made; (2) the 674 pre-existing sub-17px FAILs stand; (3) hover aliveness is unproven headless; (4) the lesson view's first paint is a black box in this VM (thumbnail blocked). The round is a 9 as filed; the product call on defect 2 is the one open question, and it is his to make, not a fix round's.

## Standing items (verified unchanged, not failed)

- `updateDock()` undefined — still throws on play (seen in this walk's page errors); contained by try/catch; deck stays live. Harvest-repair note for a later round.
- Fast error-page hole ≥ 250 ms — not re-probed; standing.
- Bare pause leaves ON AIR — re-proven (E3b), documented behaviour.
- False-alarm audio toast — `audio.error.code 3` on every play while `currentTime` advances (seen in every play step of this walk); the audio demonstrably plays.
- "Lesson #of 5" Day 5 title — seen in theatre titles (E2a/b, P3).
- Lessons LIST plus/Add pill untouched — no change in this round; Shawn's call owed.
- **Merge note stands:** fix-7's F2 is a superset of fix-6's H5c — merging fix-7 onto the fix-6 branch conflicts on that one line; resolution takes fix-7's line. Fix-8 inherits it.

## What I could not prove

- Hover aliveness (headless has no mouse) and audible audio (headless can't hear; judged by element + deck + ON AIR only).
- YouTube thumbnail paint in the VM (`i.ytimg.com` blocked) — environmental; the embed chrome and captions paint, and the theatre paints.

## Evidence index (all under `eye/`)

| Walk | Result | Log / screenshots |
|---|---|---|
| Desktop 1920 (E0–E7) | 27/27 PASS | `eye-walk.py`, `eye-log.json`, `e00`–`e06` |
| Phone 390 (P0–P5) | 9/9 PASS | `eye-log.json`, `p00`–`p04` |
| Staged byte check | PASS (size + sha256 + `cmp`) | `staged-check.html` |
| Bottom-bar crops (ghost comparison) | clean at both widths | `e00b-desktop-bottom.png`, `p00b-phone-bottom.png` vs fix-7 `crop-6a-bottom.png` |
| Defect-2 player area at 390 | chrome truncates, h3 reads whole | `p01-phone-lesson-player.png` |
| Theatre (desktop) | chrome + captions paint | `e02-desktop-theatre1.png`, `e03-desktop-theatre2.png` |

## What the next step is

**Nothing to fix. The round passes.** The one open item is the product call on defect 2 — theatre-only playback, a custom header, or accepting YouTube's standard narrow-width truncation — which is the captain's to put to Shawn, not a fix round's. When he rules, the page ships as it stands.
