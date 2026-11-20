# Personal Frame FIX-6 Round — MAKER REPORT (2026-11-20 ~02:30–05:30 MST)

One lane, one round, one file: `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`.
Base: branch `personal/frame-round-fix5-20261119`, tip `04715a7f8fc7dbd885b05401c1fb6b1839aa7811`,
blob `dedf0b19057b4396572d8b1963352f0744c32439`, 10,453,371 B, sha256
`8585244daa53fd8b7ad00fe5da0c4ee79ec02c3c4a146c55b9b64140936752b9`
(re-verified from the GitHub blob API by this seat before editing).

## VERDICT — FILED, the one defect closed, full regression green

- **The defect (Ask Naya button does not open the room): REAL DEFECT, fixed at the root.**
  The mechanism is NOT what the fix-5 eye report said in bytes — the live stack
  trace refutes it (see §Mechanism). The fix is one 12-line guard in the
  `popstate` handler. The button now opens the room by real tap at 1920
  (Firefox + Chromium) and 390, and holds at 2/5/10 s and after a second tap.
- **Fix-5's proven work: all still passing by real tap** (table below).
- **No merge, no live deploy, no message to the user.** User asleep; this
  report goes to the coordinator only.

## Filing (verified three ways: branch tip, blob API sha/size/sha256, staged hash)

- Branch: `personal/frame-round-fix6-20261119`
- Commit: `8056efc3a7699b83d3f55294215482dee956156b`
- Commit parent: exactly `04715a7f8fc7dbd885b05401c1fb6b1839aa7811` (one commit, direct child of the base tip)
- Blob: `8fbec9580c078b97d0881f7aa20d8c92ce41d9d6`, 10,454,283 B (+912),
  sha256 `3dabcd80ade63f664fb2daabef3a2b2c34f1360fb0f31177739e1d7280c66522`
- Lines: 51,863 → 51,875 (+12, pure insertion)
- Staged URL (curl re-fetch piped through Node sha256, no disk write):
  `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal`
  → 10,454,283 B, sha256 `3dabcd80…` — byte-identical to the filed blob.
- Diff replay: exactly one hunk — common prefix 23,592 lines, common suffix
  28,271 lines, base removed 0 lines, fixed added 12 lines. Nothing else
  changed. All 101 inline `<script>` blocks parse cleanly in both base and
  fixed (`vm.Script`, 0 failures).
- PRs untouched, unmerged. No live deploy, no link to Shawn.
- Work files: `~/workspace/team-nitro/personal-frame-fix6-20261119/maker/`
  (`fetchBase6.js`, `edit-fix6.js` — the transform; `file-fix6.js` — the filer;
  `verify6.js` — the byte proofs; `repro6*.py` — the mechanism proofs;
  `reg6_*.py` — the tap proofs) and `…/eye/` (50 screenshots + logs).
- Environment: EPERM flake active — all work from API-fetched bytes held in
  Node memory (Buffer/latin1 round-trip); every write verified by size + sha.
  Local 10 MB test copies were deleted after use; no local copy remains.
  VM Firefox alive (re-tested this round); Chromium alive via the localhost
  forwarder (started for the Chromium leg, killed after; PID 28836).

## The defect — the mechanism, corrected (the eye's byte-reading was wrong)

**What the eye said:** the Router `*` fallback (line 17440) takes the first
hash segment (`hub`), finds it outside its allow-list, and rewrites
`#/hub/ask` to `#/hub`.

**What the live evidence says:** the fallback never runs in this path.
`render()` (lines 11012–11044) matches `hub/:room` parametrically before it
ever reaches `routes['*']` — for `#/hub/ask`, `segs = ['hub','ask']`,
`routes['hub/:room']` matches, `params.room = 'ask'`. The fallback is
provably unreachable for any `#/hub/*` hash. It was left untouched.

**The real chain, proven live on the fix-5 staged bytes:**

1. The Ask Naya button calls `NayaRouter.navigate('/hub/ask')` (line 12254).
   `navigate()` sets `location.hash = '#/hub/ask'` (line 11007).
2. **Firefox fires a `popstate` event when `location.hash` is assigned.**
   Proven by log (`repro6c`): boot `POPSTATE hash=#/hub` from the boot
   assignment at line 17463, and on the ask click `POPSTATE hash=#/hub/ask`
   at +0 ms, before any `hashchange` event.
3. The Personal frame's `popstate` handler (lines 23592–23595) mapped EVERY
   non-Personal hash to `showView('home')`:
   `var v=(e.state && e.state.osView) || (location.hash||'').replace('#','');
   showView(VIEWS.indexOf(v)>=0?v:'home', true);` — `'hub/ask'` is not in
   `VIEWS`, so it called `showView('home', true)`.
4. `showView('home')` runs the fix-4 F3 yield (line 23579): with the hash
   now `#/hub/ask`, `_roomOpen` is true (`segs[0]==='hub' && segs[1]==='ask'`),
   so it calls `NayaRouter.navigate('/hub/feed')` — 6 ms after the ask click,
   before the `hashchange` render ever runs.
5. The room never opens. URL lands on `#/hub/feed`, room count 0.

Proven by stack trace (`repro6b`): the `NAVIGATE(/hub/feed)` call's stack is
`showView@…:23579` ← `@…:23594` (the popstate handler) ← `navigate@…:11007`
← the askBtn click handler `@…:12254`. And by the popstate log (`repro6c`):
`POPSTATE hash=#/hub/ask` then `POPSTATE hash=#/hub/feed`, then two
`HASHCHANGE hash=#/hub/feed` events (one real, one synthetic from the
fix-4 nudge at lines 10285/10526).

**The fix (one guard, in the popstate handler — the root, not the surface):**

Base lines 23592–23595:
```
  window.addEventListener('popstate', function(e){
    var v=(e.state && e.state.osView) || (location.hash||'').replace('#','');
    showView(VIEWS.indexOf(v)>=0?v:'home', true);
  });
```
Fixed lines 23592–23607 (the first line unchanged, 12 lines inserted after it):
```
  window.addEventListener('popstate', function(e){
    /* FRAME-FIX6 2026-11-19 (F6): a Hub-room hash is NOT a Personal-view popstate.
       Firefox fires popstate when location.hash is assigned, so the Hub-bar
       Ask Naya button's navigate('/hub/ask') used to land here, showView('home')
       ran, and its fix-4 F3 yield forced the room straight back to '/hub/feed'
       (proven by live stack trace + popstate log, fix-6 repro6b/6c — the
       Router '*' fallback at 17440 never runs for hub routes: hub/:room
       matches first, so it was not the eater). Hub/note hashes belong to the
       Router's hashchange render — leave them alone. Personal views (and an
       empty hash) still route here, so Back to a Personal view still yields
       an open room through showView('home'). */
    var _h=(location.hash||'').replace(/^#\/?/,'').split('?')[0].split('/')[0];
    if (_h==='hub' || _h==='smart-notes' || _h==='notes' || _h==='note') return;
    var v=(e.state && e.state.osView) || (location.hash||'').replace('#','');
    showView(VIEWS.indexOf(v)>=0?v:'home', true);
  });
```

Why this is the root and why it is safe:
- The handler's job is Personal-view routing on Back/forward. A Hub-room hash
  is not a Personal view; the Router's `hashchange` render owns it. The guard
  uses the same first-segment test the fallback uses, plus the note routes
  (`smart-notes`, `notes`, `note`) that the Router also owns.
- `showView('home')` and its F3 yield are untouched, so the PERSONAL-tab
  yield still works (proven below, twice at 1920 + Chromium).
- Back from `#/hub/ask` still yields: the previous entry's hash is empty/a
  Personal view, `_h` is not a hub route, `showView('home')` runs, the F3
  yield closes the room to `#/hub/feed` (proven at 390 below).
- The `*` fallback, the button handler, and the fix-5 `recoverFeedAfterBack`
  region are all byte-identical to base (verified: fallback string present,
  askBtn string present, `recoverFeedAfterBack` count 4 in both).

## Tap proof — Ask Naya button (the bullseye)

All on the staged fix-6 URL unless noted. Real mouse taps at element centres.

| Run | Tap 1 @2 s | @5 s | @10 s | Tap 2 | Hash | Title |
|---|---|---|---|---|---|---|
| Firefox 1920, staged (`reg6_a`) | room=1 | room=1 | room=1 | — (probe locator went strict-mode on 3 Ask matches once room open; room stayed 1) | `#/hub/ask` | Ask Naya — NayaNET |
| Firefox 1920, staged (`reg6_a2`, `.hub-obsidian-btn` locator) | room=1 @5 s | — | — | room=1 @5 s | `#/hub/ask` | Ask Naya — NayaNET |
| Chromium 1920 via forwarder (`reg6_chromium`) | room=1 | room=1 | room=1 | — | `#/hub/ask` | Ask Naya — NayaNET |
| Firefox 390 is_mobile (`reg6_phone2`, scroll-into-view first) | room=1 | room=1 | room=1 | — | `#/hub/ask` | Ask Naya — NayaNET |
| Local pre-file bytes (`tap6_local`) | room=1 | room=1 | room=1 | — | `#/hub/ask` | Ask Naya — NayaNET |

Screenshots: `eye/6a-ask-room.png`, `eye/6a2-ask-room-2nd.png`,
`eye/6d-chromium-ask-room.png`, `eye/6e2-phone-ask-room.png`,
`eye/6e5-phone-room-scrolled.png` (390 room: TALK TO NAYA + HOLD TO TALK +
room bottom bar HOME / INTEL TODAY / ASK / REPORTS / SPACES, clean, nothing
clipped). Logs: `maker/reg6_a.log`, `reg6_a2.log`, `reg6_chromium.log`,
`reg6_phone2.log`, `reg6_phone5.log`.

Pre-fix reproduction (fix-5 staged bytes, same taps): two taps land on
`#/hub/feed`, room=0 at 2/5/10 s (`maker/repro6.log`, `repro6b.log`,
`repro6c.log`, screenshot `maker/r6-ask-after-click.png`).

Probe notes from this round (for the next eye):
- At 390 the Ask Naya button sits BELOW the viewport at load (box y≈869 in
  an 844 viewport) — a raw click at its box misses. Scroll it into view
  first (fix-5 phone_back3 pattern), then tap. My first 390 run clicked
  below the viewport and reported room=0 — probe error, not a page fail.
- Once the room is open, `get_by_role("button", name="Ask Naya")` resolves
  to 3 elements (strict-mode violation) — use
  `.hub-obsidian-btn[aria-label="Ask Naya"]` for the Hub-bar button.
- At 390 with the room open, the PERSONAL feed tab's box is `None` at every
  scroll step — the room covers the feed tabs at phone width, so the
  PERSONAL-tab yield is not tappable at 390 (pre-existing layout fact, not
  a fix-6 change; the yield is proven at 1920 + Chromium). At 390 the room
  closes via browser Back (proven below) or the room bar's HOME tile (eye
  §3b: lands on the live portal).

## Regression table (all by real tap, staged fix-6 URL)

| Item | Result | Evidence |
|---|---|---|
| Ask Naya button opens room (1920 FF + Chromium, 390) | **PASS** | table above |
| Back-button return repaint, Firefox 1920 normal | **PASS** — fresh 770 controls → after Back 739 → 768 @15 s, all 5 markers visible, no reload, no wait | `reg6_back.log`, `eye/6b-normal-*.png` |
| Back-button return repaint, Firefox 1920 throttled (+250 ms/response) | **PASS** — fresh 770 → after Back 739 → 768 @15 s, all markers visible | `reg6_back_thr2.log`, `eye/6b2-throttled-*.png` (first attempt's WORLDS locator click timed out on the navigation wait under throttle — probe timeout, retried with a 120 s timeout and it landed; second attempt's raw mouse click at a below-fold box missed — probe error, not a page fail) |
| Back-button return repaint, Chromium 1920 | **PASS** — fresh 900 → after Back 899 → 899 @15 s, all markers visible | `reg6_chromium.log`, `eye/6d-chromium-after-back*.png` |
| Back-button return, phone 390 via "Go to the Hub" → Back | **PASS** — lands on `https://nayanet.app/hub#/hub`, Back → 708 controls @5 s → 737 @15 s, quote/name/empty-state present | `reg6_phone4.log`, `eye/6e4-phone-after-back*.png` (matches fix-5 eye's 708/737) |
| Back closes the Ask room at 390 | **PASS** — room 1 → browser Back → room 0, hash `#/hub/feed`, markers present (proves the popstate guard preserves the Back-to-home F3 yield) | `reg6_phone4.log`, `eye/6e4-phone-room-back.png` |
| Composer landings 6/6 on fresh loads | **PASS** — `#home/composer` Naya note, `#home/post` Make a post, `#home/naya` Naya note, `#home/smart` Smart note (all open @t+5 s); plain `#home` and `#about` correctly closed | `reg6_c.log`, `eye/6c-composer-0..5.png` |
| Academy cover pill → GroovePages in a new tab | **PASS** — popup `https://nayanet.groovepages.com/academy` at 1920 and 390; main page stays staged | `reg6_c.log`, `eye/6c-academy-popup.png`, `reg6_phone.log`, `eye/6e-phone-academy-popup.png` |
| PERSONAL feed tab yields the Ask Naya room | **PASS** — room 1 → tap PERSONAL tab → room 0, `#/hub/feed`, no reload (Firefox 1920 ×2, Chromium 1920, local bytes) | `reg6_a.log`, `reg6_a2.log`, `reg6_chromium.log`, `tap6_yield.log` |
| Connections `#people` holds through scroll + 15 s | **PASS** — hash `people` after Connections, still `people` after scroll + 15 s | `reg6_a2.log`, `eye/6a2-people-hash.png` |
| Settings → "Go to Home Hub →" | **PASS** — gear → `#settings`, "Home Hub & install" tab (step 7 of 7, locator click) → link at (54, 969) → lands on `https://nayanet.app/hub#/hub` | `reg6_settings4.log`, `eye/6s4-hub-landing.png` (earlier attempts: the link's off-canvas twin at x=-304 and the "Go to Home Hub" heading are not the link — probe targeting errors, not page fails) |
| Phone 390: Back return, Academy popup, composer | **PASS** — see rows above; composer `#home/composer` open=True at 390 | `reg6_phone.log`, `reg6_phone4.log` |
| Layout at 390 | Clean; room renders with TALK TO NAYA / HOLD TO TALK / room bar. The cover pill row ("What is NayaPOWER") clips at the right edge — the cover's horizontal pill strip, pre-existing, outside this round's scope. | `eye/6e5-phone-room-scrolled.png` |

Staged limitation (named, not a fail — same as fix-5): note cards never render
on the staged page (Supabase reads CORS-blocked from the proof-host origin in
Firefox; rows arrive HTTP 200 but `#pcHubFeedMount` stays absent in Chromium)
— the button is judged by the room opening, not by feed cards. The points
pill reads "… pts" on staged (same cause).

## §11 design-laws check (in writing)

Read against THE-NAYA-DESIGN-LAWS.md (activation read, before work) and
observed on the rendered page at both widths. This round changes NO visual
element, NO text, NO color, NO layout — one routing guard in JS. The check
below is therefore a no-regression check on the walked views, plus the
§11 questions on the change itself.

- **Five gates:** (1) Right — a citizen tapping "Ask Naya" gets the room, not
  the feed; no one is harmed. (2) What they truly need — the button must do
  what it says; the fix restores exactly that, nothing more. (3) Mine to do —
  the brief orders this fix; no protected gate is touched (no money,
  credentials, destructive action, privacy change, or live deploy).
  (4) Now — the page is not ready for Shawn until this lands; the fix is
  minimal, reversible (one guard), and proven by tap before filing.
  (5) Prove it — the defect was reproduced live with a stack trace and a
  popstate log, the fix was proven by real tap at both widths in two
  browsers, and the full regression table above is the receipt.
- **Real objects, not pictures of objects:** unchanged — cover, pills, boards
  are obsidian with rims and glow, elevated, alive on hover. PASS.
- **One light, obsidian inside, outside light in the object's own deep
  colour:** unchanged — Ask Naya keeps its purple `#8e24aa` glow, Life with
  Naya its green; the composer is obsidian with a purple rim. PASS.
- **Bottom bar:** unchanged — the six tiles, one set, same order and colours
  at both widths; at 390 icons only. PASS.
- **Type:** unchanged — Marcellus display, 25/19/17 scale on the quote board
  and headings; no grey body text observed on the walked views. PASS.
- **One icon that lights up:** unchanged — bottom-bar tiles light as one
  icon; no icon-plus-separate-light observed. PASS.
- **Three boards, then a button:** unchanged — agreement and settings unfold
  in stepped cards/tabs (Settings: 7 steps, one at a time). PASS.
- **Button destinations (the law that caught this round's fail):** every
  button tapped lands where it should — the Ask Naya button NOW lands on
  the room; Academy, Settings→Hub, WORLDS→space, Go to the Hub, Connections
  all land correctly. PASS.
- **No redesign, no removal:** the diff is exactly one 12-line insertion in
  the `popstate` handler; the button, the router, the fallback, the fix-5
  recovery region, the welcome banner, and the Academy destination are all
  byte-identical to base. PASS.
- **Reference objects:** no new element was built, so no new measurement
  against the three reference objects was needed; nothing was harvested or
  invented — the fix reuses the existing `showView`/`navigate` machinery.
- **Read as a reader:** top to bottom at 1920 and 390, the page reads as a
  world (cover, pills, quote board, tabs, sidebar with real people). The Ask
  Naya room reads as her room (EXPLORE / DISCOVER pills, TALK TO NAYA,
  HOLD TO TALK, room bar). The staged feed is still an empty black space
  with "Nothing here yet." — the known staged Supabase limitation, not a
  fix-6 fail.

## Laws delta — ZERO

`check-design-laws.py` run on base and fixed bytes:
- Base: **810 violation(s), 160 warning(s)**.
- Fixed: **810 violation(s), 160 warning(s)**.
- After stripping filenames and line numbers, the two outputs are
  **byte-identical** (0 diff lines) — the only differences are the +12 line
  numbers of findings after the insertion point. The 810/160 are pre-existing
  whole-file findings (mostly the checker's naive sub-17px SIZE greps and
  GRAY greps matching comments/strings across 51,863 lines); this round adds
  none. Logs: `maker/laws-base.log`, `maker/laws-fix6.log`,
  `maker/laws-diff-nonum.txt` (0 lines).

## What was NOT touched (standing)

- The welcome banner (pending Shawn's ruling).
- The Hub-side half (the Hub must send `#home/composer` instead of bare
  `#home` in the two ADD data-hub-hrefs — a Hub round, not this one).
- The Academy destination (`https://nayanet.groovepages.com/academy`,
  adjudicated correct).
- The fix-5 back-button recovery region (`recoverFeedAfterBack` — count 4 in
  base and fixed, byte-identical).
- The Router `*` fallback (line 17440) — proven unreachable for hub routes,
  left byte-identical. **Correction for the record:** the fix-5 eye report's
  §3c mechanism ("the fallback eats `#/hub/ask`") is refuted by the live
  stack trace and popstate log; the eater was the `popstate` handler +
  fix-4 F3 yield. The brief's framing ("the fallback's allow-list is the
  suspect") was followed to the evidence, not past it — the sense check
  demanded the real root, and the real root is what was fixed.

## Open / not proven

- Live-Hub Ask Naya room end-to-end (the fix-5 eye's second open item): not
  re-attempted this round — same environment wall (VM Firefox cannot drive
  the live Hub's install modal). The staged room path is proven; the live
  step remains unproven, not failed. The fix-4 eye proved it end-to-end;
  the captain may accept that or re-drive it in the cloud browser.
- The 390 PERSONAL-tab yield: not tappable at 390 while the room is open
  (tab box `None` at every scroll step — pre-existing). The yield is proven
  at 1920 (Firefox ×2, Chromium) and on local bytes; at 390 the room closes
  via browser Back (proven) or the room bar's HOME tile (eye §3b).
