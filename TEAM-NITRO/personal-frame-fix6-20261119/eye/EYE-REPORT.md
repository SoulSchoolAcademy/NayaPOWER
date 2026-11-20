# EYE REPORT — Personal frame fix-6

**Verdict: GOES BACK — one item.**
**Subject:** Personal frame fix-6, branch `personal/frame-round-fix6-20261119`, branch tip `073d920e`, HTML tip `8056efc3`, blob `8fbec958`, 10,454,283 B, sha256 `3dabcd80…`. Base = fix-5 tip `04715a7f`, blob `dedf0b19`.
**Staged:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal
**Eye:** captain's eye, re-dispatched. VM Firefox, phone 390×844 first, then desktop 1920×1080. Activation read in full before any verification: `THE-NAYA-DESIGN-LAWS.md`, `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-ULTIMATE-ORIENTATION.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md`, `THE-ARMY-TRAINING.md`.
**Staged link HELD — do not deliver to Shawn until the go-back round passes this eye.**

## The one go-back item

**ADD → Create menu → "Message" does nothing on tap.** Four real taps, zero results.

- My taps (VM Firefox 1920, leg1920c): the Create menu opens visibly (`eye-61-create-menu-1-1920.png` — all five items: Make a post, Naya note, Smart note, Message, Mail). The Message item's box is real: (572.8, 773.1), 212×50. I tapped it by real locator click. After the tap (`eye-62-after-message-1-1920.png`): the menu closes and **nothing appears** — no composer, no messenger panel, no navigation. Measurements after the tap: `body.msg-open` = 1 (the class was added), `.hub-msg-panel` count = 0, visible = false, URL unchanged. Repeated on a second fresh load: identical — `body.msg-open` = 1, panel count 0, visible false.
- The cloud-browser 1920 leg tapped it twice with the same result: menu closes, no composer, no navigation, no visible panel.
- **Root cause, read from the fixed bytes:** the menu item calls `openMessenger()`, which is only `document.body.classList.add('msg-open')` — it never calls `ensureMsgPanel()` / `openMsgPanel()`, the only functions that build the panel. The CSS (`body.msg-open.hub-msg-panel{transform:none}`) reveals a panel that only exists if `ensureMsgPanel()` built it; on a fresh staged load it has not been built, so the tap adds a class to a panel that does not exist. Pre-existing: the fix-6 diff (0 removed / 12 added, popstate handler only) cannot affect it. No seat ever tapped ADD → Message before: the checker and the fix-5 eye proved "composer 6/6" via URL suffixes on fresh loads, never via the menu — so the menu path was never proven until the cloud leg found it dead.
- **Why this is a go-back, not a next-round item:** Shawn's button-destinations rule (2026-11-19): "A page passes only when its buttons go where they should." This button goes nowhere. It is the same class as the fix-5 Ask Naya go-back — a pre-existing dead button found by the eye — and the fix-5 precedent says that goes back even when it predates the round. The page he sees is the scope; he taps ADD → Message and nothing happens on a page I passed. That is the failure this eye exists to prevent.
- **What the return round must do:** wire the Message item to build and open the messenger panel on first tap (call `ensureMsgPanel()` / `openMsgPanel()` in the Message path, the way Mail opens its composer). **Acceptance:** fresh load → ADD → Message → messenger panel visible on the first tap, at 390 and 1920. **Regression for the return round:** Ask Naya guard (room = 1 at 2/5/10 s, `#/hub/ask`), Back closes room, Back repaint, composer 6/6 **via the menu by real tap** (all six items, not URL suffixes), Academy popup, `#people` holds 15 s, Settings → Go to Home Hub, bottom-bar destinations.

## What passes — the guard is proven

### §1 Byte leg (my own run, fresh bytes)
- Base blob `dedf0b19`: 10,453,371 B, sha256 `8585244d…`, git blob sha matches. Fixed blob `8fbec958`: 10,454,283 B (+912), sha256 `3dabcd80…`, git blob sha matches.
- Diff replay: common prefix 23,592 lines, common suffix 28,271 lines, **base removed 0, fixed added 12 — exactly one hunk**, fixed lines 23593–23604 (the `FRAME-FIX6` comment + `_h` first-segment parse + `if (_h==='hub' || _h==='smart-notes' || _h==='notes' || _h==='note') return;`).
- Staged GET: HTTP 200, 10,454,283 B, sha256 matches the filed blob exactly.
- Mechanism re-verified from my own read of the fixed bytes: `render()` matches parametric `hub/:room` before the `*` fallback, so the `*` fallback is unreachable for `#/hub/ask` — the fix-5 eye's fallback mechanism is refuted and the checker's corrected mechanism stands. The button calls `NayaRouter.navigate('/hub/ask')`; the guard stops the popstate handler from yielding back to `/hub/feed`.
- Counts: `recoverFeedAfterBack` 4 = 4; `fcOpenCreator` 20 = 20; Academy GroovePages count 8 = 8.
- JS parse: all 100 inline `<script>` blocks parse cleanly in both base and fixed.

### §2 Ask Naya guard — PASS, both widths, my own taps
- **Phone 390 (leg390b, real taps):** room = 1 at 2/5/10 s, URL `#/hub/ask`, guard held. Screenshots `eye-21-ask-room-390.png`, `eye-22-room-scrolled-390.png`.
- **Desktop 1920 (leg1920, real taps, ×2):** room = 1 at 2/5/10 s both taps, URL `#/hub/ask`, title "Ask Naya — NayaNET". Screenshots `eye-31-ask-room-1920.png`, `eye-33-ask-room-2nd-1920.png`.
- Folded in: checker (Firefox 1920 ×2, Chromium 1920, phone 390) and the cloud-browser 1920 leg (both taps PASS). The fix-5 eye's defect is closed: the room opens and stays open.

### §3 Back closes the room, Back repaint — PASS
- **390:** Back with room open → room 0, `#/hub/feed`. Back repaint: fresh 739 controls → 739 @5 s → 767 @15 s, markers present ("Shawn Vibert", "Nothing here yet", "PERSONAL"). "Go to the Hub" → `https://nayanet.app/hub`, Back returns fully repainted. Screenshots `eye-14-back-fresh-390.png`, `eye-15-after-back-390.png`, `eye-16-after-back-15s-390.png`, `eye-23-after-back-390.png`.
- **1920:** Back closes room → room 0, `#/hub/feed` (my tap, leg1920). Back repaint at 1920 folded in from the checker (769 → 739 → 768) and the cloud leg (WORLDS → `https://nayanet.app/space`, Back fully repainted at once). My own 1920 back-repaint attempt missed its WORLDS tap (box off-viewport at x=1952 — wrong first match, probe error, not a page failure).

### §4 Composer — 5 of 6 via the menu; Message is the go-back
- Make a post, Naya note, Smart note PASS via the menu (checker + cloud leg, real taps, both widths). ADD → "Mail" opens the composer ("Message this app" form at `#message`) — do not confuse with Message.
- **Message FAILS — see the go-back item above.**

### §5 Academy — PASS
- Academy pill → new tab `https://nayanet.groovepages.com/academy` (my tap, 1920, leg1920; cloud leg agrees). Screenshot `eye-38-academy-1920.png`.

### §6 Settings → Go to Home Hub — PASS (my own tap)
- Settings → "Home Hub & install" tab → the **link** `a.ph-msg[href="https://nayanet.app/hub#/hub"]` → lands on the live Hub (`eye-82-hub-landing-1920.png`: "Good afternoon", "Intel Today", "Friday, November 20, 2026", "226 Smart Notes", the Hub's own bottom bar with MAIL / DASHBOARD / BUSINESS / SPACE / GROWTH / CONNECTIONS / SMART LISTS / REPORTS / 10 APPS). My first three attempts failed because I clicked the `text=Go to Home Hub` **heading**, not the link — probe error, corrected by targeting `a.ph-msg`. Checker §1h and cloud item 8 agree.

### §7 #people, WORLDS / ECOSYSTEM / CONNECT — folded proof, my taps missed on targeting
- `#people` holds 15 s: checker §1g + cloud item 7. My attempts missed (CONNECT tile outside the viewport in VM Firefox at 1920×1080; profile-row Connections first match was the wrong element). No contrary evidence; I do not claim my own tap.
- Bottom-bar WORLDS / ECOSYSTEM / CONNECT: cloud item 9 PASS. My attempts missed (bar sits below the fold at 1920×1080 in VM Firefox; WORLDS first match x=1952 off-viewport). No contrary evidence. MAIL / ACTIVITY are not provable on staged (the staged Personal bottom bar has no MAIL or ACTIVITY button; they exist on the live Hub only).

## Adjudication (B) — "PERSONAL feed tab yields the Ask Naya room": EXPECTATION CORRECTED

- **What the fix-5 eye meant by "yield":** with the room OPEN, tap the PERSONAL feed tab → the room YIELDS (gives way): room closes (room = 0), URL `#/hub/feed`. Proven by real tap by the fix-5 eye (§3b), the fix-6 checker (§1f, Firefox 1920 + Chromium 1920 + phone 390, tab box 728.5, 957.6), and the fix-4 checker (§151: open room → tap PERSONAL in the bottom bar → home feed, room gone; tap again → URL normalises to `#home`).
- **What the cloud leg tested:** the opposite direction — tap PERSONAL expecting the room to OPEN. The page behaved correctly in its own terms (PERSONAL → `#home` / `#/hub/feed`). Its "FAIL" was a misread expectation, not a page failure. The room is reachable only via the "Ask Naya" button itself, which is correct: PERSONAL is the way home, not the way into the room.
- **My own attempts (five, all probe failures, no page failure):** (1) first 390 leg — Ask Naya box below the viewport, PERSONAL tab box off-canvas; (2) leg1920 — tab box (-304, 117), clicked off-viewport; (3) leg1920b — picked the 72×24 bottom-bar tile label at y=1070, clicked 2 px below the viewport; (4) leg1920c — picked a 174×50 right-rail PERSONAL element, room stayed open; (5) leg1920d — bottom-bar PERSONAL tile click **refused by Playwright**: the room's own Ask Naya jewel (`<a class="jewel active" aria-label="Ask Naya — current room">`) intercepts pointer events — which **confirms the fix-5 eye's note verbatim**: "The bottom-bar PERSONAL tile does not exist while the room is open — the room bar replaces it." The yield path is the feed tab, not the bottom-bar tile. (6) Final leg — dragging the tab strip does not move the tab; it stays at (-304, 117, 272×60).
- **Disposition:** expectation corrected. The yield stands proven by the checker on these exact bytes (blob `8fbec958`); my attempts produced no contrary evidence — every miss was my targeting, and the interception finding confirms the page's structure as the fix-5 eye described it. I state plainly that I did not land the feed-tab tap myself; the checker's proof on these bytes is the evidence, and it is unrebutted.

## Live-Hub end-to-end — NOT PROVEN (environment, not a site failure)

- One attempt in VM Firefox at 1920 (`eye-90-live-hub-1920.png`): live Hub loaded, install modal present and **dismissed** (force click, 10 s timeout — the fix-5 eye's "undismissable" wall is beaten), 11,947 controls — but the "Ask Naya" button's box never resolves (15 s timeout). Same wall the fix-5 eye hit in three attempts; the cloud leg could not tap the ~1.2 MB DOM either (deadline, button present and visible).
- The fix-5 eye's sentence "The checker report records the fix-4 eye proving it end-to-end" is **not supported by anything I could find**: no fix-4 eye report file exists in `personal-frame-fix4-20261119/` (no `eye/` dir), and the fix-4 checker report records only the composer end-to-end gap. **No report I have read proves the live-Hub Ask Naya end-to-end by real tap. It remains unproven.**
- This does not block the verdict: the fix-6 guard lives in the Personal file and is proven on staged Personal (the exact bytes that will go live). The live Hub's own Ask Naya button is Hub code, a different control, and the live Personal page serves older bytes — so a live end-to-end cannot prove fix-6 before deploy in any case. The staged proof stands.

## Pre-existing 390 defects — the fix-7 list (not fix-6 fails; the one-hunk diff proves zero visual change)

Confirmed with my own eyes at 390 (`eye-21-ask-room-390.png`, `eye-22-room-scrolled-390.png`, `eye-24-bottom-bar-390.png`):
1. **Room bottom-bar labels fuse as "REPORTSPACES" at 390.** Fix: collapse the room bar to icons at 390 as the page bar does.
2. **Cover pill row clips at the right edge at 390** ("What is NayaPOWER" cut off; "Life with Naya" also cut).
3. **Room pills overlap the cover name** (seen at 1920 too, `eye-31-ask-room-1920.png`: "Smart Notes" pill covers "Shawn Vibert", "Intelligent Blocks" covers "…ether we grow"; cover art black above the room). Pre-existing room presentation.
4. Also seen at 390 (`eye-24`): the feed-tab strip clips at both edges (PERSONAL cut at the left, "The Intelligent Intern…" cut at the right) — same family as (2), name it in fix-7.

## §11 — Design-laws check, in writing

Ran `check-design-laws.py` on my own saved bytes, base vs fixed: **base 810 violations / 160 warnings; fixed 810 / 160; filename-and-line-number-normalised diff 0 lines — delta 0.** The fix adds no visible text, no new element, no colour, no type change — one comment and one guard in the popstate handler. The 390 presentation defects above are byte-identical on base (proven by the one-hunk diff) and are therefore pre-existing, not introduced. The laws check passes for this fix. Type scale 25/19/17, Marcellus, no grey text: untouched by the diff. **§11: PASS for the fix.**

## Button destinations (touched by this eye)

| Button | Lands | Verdict |
|---|---|---|
| Ask Naya (390 + 1920) | `#/hub/ask`, room opens, holds | PASS |
| Browser Back (room open) | `#/hub/feed`, room closes | PASS |
| Back repaint (390; 1920 folded) | Fully repainted at once | PASS |
| ADD → Make a post / Naya note / Smart note | Composer opens (checker + cloud) | PASS |
| ADD → Mail | "Message this app" composer at `#message` | PASS |
| **ADD → Message** | **Nowhere — menu closes, nothing appears** | **GOES BACK** |
| Academy pill | `https://nayanet.groovepages.com/academy` (new tab) | PASS |
| Settings → Go to Home Hub → | Live Hub `https://nayanet.app/hub#/hub` | PASS |
| WORLDS / ECOSYSTEM / CONNECT | Correct rooms (cloud leg) | PASS (folded) |
| #people | Holds 15 s (checker + cloud) | PASS (folded) |
| PERSONAL feed tab (yield) | Room yields to `#/hub/feed` (checker, these bytes) | PASS (folded; see adjudication B) |

## Verdict, again

**GOES BACK on one item: ADD → Create menu → "Message" is a dead button.** Everything else in this round passes: the guard is proven at both widths by my own real taps and three seats, the regression holds, adjudication (B) is expectation corrected with the checker's proof on these bytes standing, and the §11 laws check passes with delta 0. The return round is small — wire Message to build and open the messenger panel — and its acceptance is named above. The staged link stays held until that round passes this eye. The fix-7 list (390 presentation) rides the next presentation round, not this go-back.
