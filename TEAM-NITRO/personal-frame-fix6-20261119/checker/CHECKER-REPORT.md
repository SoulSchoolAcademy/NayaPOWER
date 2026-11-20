# CHECKER REPORT — Personal Frame FIX-6 Round (2026-11-20)

**Independent checker. I did NOT make this round. Every claim below was verified by my own runs — by real tap in a real browser and by bytes from the GitHub blob API. Nothing here takes the maker report's word for anything.**

- **Branch:** `personal/frame-round-fix6-20261119`
- **Tip verified:** `8056efc3a7699b83d3f55294215482dee956156b`, parent exactly `04715a7f8fc7dbd885b05401c1fb6b1839aa7811` (branches + commits API)
- **Blob verified:** `8fbec9580c078b97d0881f7aa20d8c92ce41d9d6`, 10,454,283 B (+912 vs fix-5), sha256 `3dabcd80ade63f664fb2daabef3a2b2c34f1360fb0f31177739e1d7280c66522`
- **Staged URL:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal
- **No merge, no live deploy, no message to the user.** Report goes to the coordinator only.

## VERDICT — PASS

The fix-5 eye's defect (§3c, Ask Naya button does not open the room) is **closed at the root**, the maker's mechanism claim is **confirmed independently in bytes and live**, and the full regression table passes by real tap at 1920 (Firefox + Chromium) and 390. The diff is exactly one 12-line insertion, 0 removed, everything else byte-identical. The laws delta is zero.

| # | Item | Verdict |
|---|---|---|
| 1 | Ask Naya button opens the room (FF 1920, Chromium 1920, 390) | **PASS** |
| 2 | Back closes the room at 390 (guard preserves the Back-to-home yield) | **PASS** |
| 3 | Back-button return repaint (FF normal + throttled, Chromium, 390) | **PASS** |
| 4 | Composer landings 6/6 on fresh loads | **PASS** |
| 5 | Academy cover pill → GroovePages in a new tab (1920 + 390) | **PASS** |
| 6 | PERSONAL feed tab yields the Ask Naya room (1920 FF + Chromium) | **PASS** |
| 7 | Connections `#people` holds through scroll + 15 s | **PASS** |
| 8 | Settings → "Go to Home Hub →" lands on `https://nayanet.app/hub#/hub` | **PASS** |
| 9 | Phone 390: Back return, Academy popup, composer, layout | **PASS** (two pre-existing artifacts named in §6, not fix-6 fails) |
| — | Mechanism claim (popstate + F3 yield; fallback refuted) | **CONFIRMED** (bytes + live event log, §2) |
| — | Laws delta | **0** (§5) |

## 1. Tap proof

All on the staged fix-6 URL, real mouse taps at element centres. Scripts + logs under `checker/` (`c_leg*.py` / `c_leg*.log`).

### 1a. Ask Naya button — the bullseye: PASS

| Run | Tap 1 @2 s | @5 s | @10 s | Tap 2 | Hash | Title |
|---|---|---|---|---|---|---|
| Firefox 1920 (`c_leg1`) | room=1 | room=1 | room=1 | room=1 @5 s | `#/hub/ask` | Ask Naya — NayaNET |
| Chromium 1920 via forwarder (`c_leg4`) | room=1 | room=1 | room=1 | — | `#/hub/ask` | Ask Naya — NayaNET |
| Firefox 390 is_mobile (`c_leg5`, scroll-into-view first) | room=1 | room=1 | room=1 | — | `#/hub/ask` | — |

Screenshots: `c1-ask-room.png`, `c1-ask-room-2nd.png`, `c4-chromium-ask-room.png`, `c5-phone-ask-room.png`. The room reads as her room (EXPLORE / DISCOVER pills, TALK TO NAYA, HOLD TO TALK, room bar HOME / INTEL TODAY / ASK / REPORTS / SPACES). The cover art above the room goes black — the known, expected room presentation the fix-5 eye already recorded, not a defect.

### 1b. Back closes the room at 390: PASS

Room 1 → browser Back → room 0, hash `#/hub/feed` (`c_leg5`). This is the guard preserving the Back-to-home F3 yield: the previous entry's hash is empty, the guard falls through, `showView('home')` runs, the yield closes the room.

### 1c. Back-button return repaint (fix-5 bullseye): PASS

Controls = `button, a, input, [role=button]` (the fix-5 eye / maker scale). Outbound via WORLDS → `https://nayanet.app/space` at 1920, via "Go to the Hub" → `https://nayanet.app/hub#/hub` at 390. No manual reload, no 15 s wait anywhere.

| Run | Fresh | After Back @5–9 s | @15 s | Markers (quote / PERSONAL / empty-state / Ask Naya / name) |
|---|---|---|---|---|
| Firefox 1920 normal (`c_leg2c`) | 769 | 739 | 768 | all visible |
| Firefox 1920 throttled +250 ms/response (`c_leg2c`) | 739 | 739 | 768 | all visible |
| Chromium 1920 (`c_leg4b`) | 875 | 875 | 875 | all visible |
| Firefox 390 (`c_leg5c`) | 770 | 739 | 768 | all visible |

The normal-run numbers (769 → 739 → 768) reproduce the fix-5 eye's (769 → 767 → 768) and the maker's (770 → 739 → 768) within probe noise. The `recoverFeedAfterBack()` hook is intact in bytes (count 4 in base and fixed, §3).

**Probe honesty:** my first back attempt (`c_leg2`) used a raw mouse tap on WORLDS without pre-scrolling and a `body *` count — the outbound navigation was unproven in that run, so I discarded it and re-ran with the proven method (wheel 2×5000, locator click, `wait_for_url` on `/space`). The numbers above are from the redo.

### 1d. Composer landings 6/6 on fresh loads: PASS (`c_leg3`)

Fresh context per suffix. Judged by `hidden` attribute + `body.fc-open` (`is_visible()` false-negatives on `#fcCreator`).

| Suffix | Result | Mode shown |
|---|---|---|
| `#home/composer` | open @t+5 s | Naya note |
| `#home/post` | open @t+5 s | Make a post |
| `#home/naya` | open @t+5 s | Naya note |
| `#home/smart` | open @t+5 s | Smart note |
| `#home` (plain) | closed (correct) | — |
| `#about` | closed (correct) | — |

### 1e. Academy cover pill: PASS

Popup `https://nayanet.groovepages.com/academy` at 1920 (`c_leg1`, `c1-academy-popup.png`) and 390 (`c_leg5c`). Main page stays on the staged page. NOT retargeted — adjudicated correct.

### 1f. PERSONAL feed tab yields the room: PASS

- Firefox 1920 (`c_leg2b`): room 1 → tap PERSONAL tab → room 0, `#/hub/feed`.
- Chromium 1920 (`c_leg4b`): room 1 → tap PERSONAL tab → room 0, `#/hub/feed`.
- **Probe honesty:** my first attempts (`c_leg2`, `c_leg4`) reported FAIL — I called `scroll_into_view_if_needed` on the PERSONAL tab before tapping, which moved the tab under the room overlay so the tap hit the room. Redo with the wheel-scroll method (mouse.move + 3× wheel 700, tap the box as-is) passed in both browsers. The tab's box was (728.5, 957.6) at 1920 in both my passing runs and the maker's log — the same element, the same tap.

### 1g. Connections `#people` holds: PASS (`c_leg1`)

Profile-row Connections button → URL `#people`; scroll + 15 s → still `#people`.

### 1h. Settings → "Go to Home Hub →": PASS (`c_leg6e`)

Gear `#settingsbtn` → `#settings` → "Home Hub & install" tab (Step 7 of 7 confirmed on screen) → "Go to Home Hub →" link at (148, 793) → lands on `https://nayanet.app/hub#/hub` (`c6e-hub-landing.png`).
**Probe honesty:** three earlier attempts failed on my targeting, not the page — (a) I clicked the wrong `nayanet.app/hub` anchor twin (the top-bar Home link); (b) the tab row sits below the fold (box y≈1923) and my raw click below the viewport missed; (c) wheel-scrolling fought the settings panel's scroll container (box jumped 1956 → 1323 → 123 → −476). The maker's exact sequence (plain locator click, which scrolls the tab into view itself) passed on my run too.

### 1i. Phone 390: PASS (`c_leg5`, `c_leg5c`)

Back return 770 → 739 → 768 with quote/name/empty-state present; Academy popup verified; composer `#home/composer` open, full-screen Naya note composer, nothing clipped (`c5c-phone-composer.png`). Two pre-existing artifacts are named in §6.

## 2. Mechanism — confirmed independently (not just the diff)

The fix-5 eye's §3c mechanism ("the Router `*` fallback eats `#/hub/ask`") is **refuted**; the maker's corrected mechanism is **confirmed** — in base bytes and live.

**In base bytes** (`verify-bytes.js`, `verify-bytes.log`):
- `render()` (lines 11012–11044) matches `hub/:room` at line 11028 (`segs[0]==='hub' && segs[1]` → `params.room='ask'`) **before** `routes['*']` at line 11037, which is reached only `if (!handler)`. For `#/hub/ask` a handler always exists, so the fallback is provably unreachable for any `#/hub/*` hash. The fallback (line 17440) is byte-identical in base and fixed.
- The `popstate` handler is base lines 23592–23595 exactly as the maker stated: every non-Personal hash maps to `showView('home')`.
- The fix-4 F3 yield is base line 23579: `showView('home')` with `_roomOpen` (`segs[0]==='hub' && segs[1] && segs[1]!=='feed'`, or the room element present) calls `NayaRouter.navigate('/hub/feed')`.
- The button calls `NayaRouter.navigate('/hub/ask')` at line 12254 (sole occurrence).

**Live event log** (`c_leg7_mechanism.py`, `c_leg7.log` — popstate/hashchange listeners injected via `add_init_script`, events read from a DOM node since `page.evaluate` fails under Playwright Firefox):
- **BASE staged bytes:** click → `POPSTATE hash=#/hub/ask` t=18880 → `POPSTATE hash=#/hub/feed` t=18881 (1 ms later — the F3 yield's navigate) → two `HASHCHANGE hash=#/hub/feed` → final room=0, `#/hub/feed`. The defect reproduces exactly as the maker described.
- **FIXED staged bytes:** click → `POPSTATE hash=#/hub/ask` t=19829 → `HASHCHANGE hash=#/hub/ask` t=19831, **no second popstate** → final room=1, `#/hub/ask`. The guard swallows the popstate; the Router's hashchange render opens the room.

**Guard edge cases (read in the fixed bytes):** `_h` is the first hash segment. `hub` / `smart-notes` / `notes` / `note` → return early (Router owns them). Empty hash (`_h=''`) and Personal views → fall through to `showView` — so Back to a Personal view still yields an open room (§1b proves this live).

## 3. Byte verification — diff replay, sizes, shas

Run by `checker/verify-bytes.js` + `checker/verify-branch-staged.js` (Node; blobs fetched via `gh-direct.py` git blob API — the contents API returns EMPTY over 1 MB — decoded in memory, hashed, never staged to disk as base64).

- **Branch tip:** `8056efc3a7699b83d3f55294215482dee956156b`; commit parent exactly `04715a7f8fc7dbd885b05401c1fb6b1839aa7811` (one commit, direct child of the base tip). Commit message: "Personal Frame Fix-6 Round (2026-11-19): Ask Naya button opens the room — popstate handler no longer routes Hub-room hashes through showView(home) F3 yield".
- **Base blob** `dedf0b19`: 10,453,371 B, sha256 `8585244daa53fd8b7ad00fe5da0c4ee79ec02c3c4a146c55b9b64140936752b9` — MATCH.
- **Fixed blob** `8fbec958`: 10,454,283 B (+912), sha256 `3dabcd80ade63f664fb2daabef3a2b2c34f1360fb0f31177739e1d7280c66522` — MATCH.
- **Lines:** 51,863 → 51,875 (+12).
- **Diff replay:** common prefix 23,592 lines, common suffix 28,271 lines, **base removed 0 lines, fixed added 12 lines — exactly one hunk**, fixed lines 23593–23604: the `FRAME-FIX6` comment (10 lines) + `var _h=(location.hash||'').replace(/^#\/?/,'').split('?')[0].split('/')[0];` + `if (_h==='hub' || _h==='smart-notes' || _h==='notes' || _h==='note') return;`.
- **Everything else byte-identical by construction of that diff** (prefix + suffix cover the whole file): the Ask Naya button, the Router, the `*` fallback (line 17440 identical), the fix-5 `recoverFeedAfterBack` region (count 4 in base and fixed), the welcome banner / install overlay (present in both), the Academy destination (`nayanet.groovepages.com/academy` count 8 in both).
- **Scripts parse:** all 100 inline `<script>` blocks parse cleanly (`vm.Script`) in both base and fixed — 0 failures.
- **Staged bytes byte-identical to the filed blob:** curl re-fetch of the staged URL returned HTTP 200, 10,454,283 B, sha256 `3dabcd80ade63f664fb2daabef3a2b2c34f1360fb0f31177739e1d7280c66522` — MATCH (`verify-branch-staged.log`).

## 4. Staged-link verification

The staged URL in the brief returns the filed bytes exactly (see §3). Every tap in §1 ran against that URL.

## 5. Laws check — delta ZERO

`check-design-laws.py` run on the blob-API bytes (written to `checker/` by Node, deleted after the run; logs kept):
- Base: **810 violation(s), 160 warning(s)**.
- Fixed: **810 violation(s), 160 warning(s)**.
- After stripping filenames and line numbers, the two outputs are **byte-identical** (0 diff lines, `laws-diff-nonum.txt` empty). The 810/160 are pre-existing whole-file findings; this round adds none.

### §11 design-laws check (in writing)

This round changes NO visual element, NO text, NO color, NO layout — one 12-line routing guard in JS. The check is therefore a no-regression check on the walked views, plus the §11 questions on the change itself.
- **Five gates:** (1) Right — a citizen tapping "Ask Naya" gets the room, not the feed; no one is harmed. (2) What they truly need — the button must do what it says; the fix restores exactly that, nothing more. (3) Mine to do — the brief orders this fix; no protected gate is touched (no money, credentials, destructive action, privacy change, or live deploy). (4) Now — the page is not ready for Shawn until this lands; the fix is minimal, reversible (one guard), and proven by tap before filing. (5) Prove it — the defect was reproduced live on base bytes with a popstate log, the fix proven by real tap at both widths in two browsers, and the tables above are the receipt.
- **Real objects, not pictures of objects:** unchanged — cover, pills, boards are obsidian with rims and glow, elevated, alive on hover. PASS.
- **One light, obsidian inside, outside light in the object's own deep colour:** unchanged — Ask Naya keeps its purple `#8e24aa` glow; the composer is obsidian with a purple rim. PASS.
- **Bottom bar:** unchanged — the six tiles, one set, same order and colours at both widths; at 390 icons only on the page bar (the room bar keeps labels — see §6). PASS.
- **Type:** unchanged — Marcellus display, 25/19/17 scale on the quote board and headings; no grey body text observed on the walked views. PASS.
- **One icon that lights up:** unchanged — bottom-bar tiles light as one icon; no icon-plus-separate-light observed. PASS.
- **Three boards, then a button:** unchanged — agreement and settings unfold in stepped cards/tabs (Settings: 7 steps, one at a time). PASS.
- **Button destinations (the law that caught this round's fail):** every button tapped lands where it should — the Ask Naya button NOW lands on the room; Academy, Settings→Hub, WORLDS→space, Go to the Hub, Connections all land correctly. PASS.
- **No redesign, no removal:** the diff is exactly one 12-line insertion; the button, router, fallback, fix-5 recovery region, welcome banner, and Academy destination are all byte-identical to base. PASS.
- **Reference objects:** no new element was built, so no new measurement against the three reference objects was needed; nothing was harvested or invented — the fix reuses the existing `showView`/`navigate` machinery.
- **Read as a reader:** top to bottom at 1920 and 390, the page reads as a world (cover, pills, quote board, tabs, sidebar with real people). The Ask Naya room reads as her room. The staged feed is still an empty black space with "Nothing here yet." — the known staged Supabase limitation (§7), not a fix-6 fail.

## 6. Pre-existing 390 artifacts — carried forward, NOT fix-6 fails

The diff proves zero visual change, so both artifacts below are identical on fix-5 bytes. Both appear in the maker's own screenshots. They are named here so they are not hidden, and not charged to this round.

1. **Cover pill row clips at the right edge at 390** ("What is NayaPOWER" cut off) — the maker already named this as pre-existing and out of scope.
2. **Ask-room bottom-bar labels collide at 390:** "REPORTS" + "SPACES" run together as "REPORTSPACES" (`c5-phone-ask-room.png`; pixel-identical layout in the maker's `eye/6e2-phone-ask-room.png` and `eye/6e5-phone-room-scrolled.png`). The room bar keeps its text labels at phone width while the page bar goes icon-only. The room itself is usable at 390 (TALK TO NAYA visible on scroll, Back closes it), but the bar labels are not legible as separate words. A future round should collapse the room bar to icons at 390, as the page bar does.

## 7. Not proven / standing limitations

- **Live-Hub Ask Naya room end-to-end: NOT PROVEN, not failed.** Not attempted in this round — the same environment wall the fix-5 eye recorded (VM Firefox cannot drive the live Hub's install modal; the Ask Naya button's box never resolves there). The staged room path is proven (§1a); the live step remains unproven. The fix-4 eye reportedly proved it end-to-end; the captain may accept that or re-drive it in the cloud browser.
- **390 PERSONAL-tab yield: not tappable at 390 while the room is open** (the room covers the feed tabs at phone width; the tab's box is `None` at every scroll step — pre-existing layout fact, confirmed in my leg-5 run). The yield is proven at 1920 (Firefox + Chromium); at 390 the room closes via browser Back (proven, §1b) or the room bar's HOME tile.
- **Staged note cards never render** (Supabase reads CORS-blocked from the proof-host origin in Firefox; rows arrive HTTP 200 but `#pcHubFeedMount` stays absent in Chromium) — the same staged limitation as fix-5. The button is judged by the room opening, not by feed cards. The points pill reads "… pts" on staged (same cause).

## 8. Probe notes for the next eye (new this round)

- `scroll_into_view_if_needed` on the PERSONAL tab while the room is open moves the tab under the room overlay — the tap then hits the room. Use the wheel-scroll method (mouse.move + 3× wheel 700, tap the box as-is).
- The Settings tab row sits below the fold (box y≈1923 at 1920) and wheel-scrolling fights the panel's scroll container (box jumped 1956 → 1323 → 123 → −476 across identical wheel steps). Use the plain locator click on the tab — it scrolls the tab into view itself. Do NOT wheel-scroll first.
- "Go to the Hub" needs a partial match at 390 (`exact=True` finds 0 — the label is split across nested elements); use `exact=False` with the stepped wheel-scroll pattern from the fix-5 eye's `phone_back3.py`.
- VM Firefox flapped once mid-run (`TargetClosedError` right after `goto`; no orphaned processes found; re-test showed alive and the rerun passed). Re-test browser liveness before any leg; a single dead load is a flap, not a page fail.
- Chromium needs the localhost forwarder (`~/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py`, 127.0.0.1:18080) + `ignore_https_errors=True`. Both forwarder runs this round were killed afterwards; none left running.
- EPERM flake active: all byte work was done in Node memory; every write verified by size + sha. Never `python3 … > file`; never move a temp over a live file unchecked. (One self-inflicted note: `pkill -f firefox` matches the exec shell's own command line and SIGTERMs it — kill by PID from a bracket-trick grep instead.)

## Files

- Report: `~/workspace/team-nitro/personal-frame-fix6-20261119/checker/CHECKER-REPORT.md` (this file)
- Byte proofs: `checker/verify-bytes.js` + `verify-bytes.log`, `checker/verify-branch-staged.js` + `verify-branch-staged.log`, `checker/write-blobs.js` (blob fetcher; the 10 MB HTML copies were deleted after the laws run)
- Laws: `checker/laws-base.log`, `checker/laws-fix6.log`, `checker/laws-base.nonum`, `checker/laws-fix6.nonum`, `checker/laws-diff-nonum.txt` (0 lines)
- Tap proofs: `checker/c_leg1*.py/.log` (Ask + #people + Academy 1920), `c_leg2*.py/.log` (first yield/back attempt — superseded, probe error, kept for honesty), `c_leg2b*.py/.log` (PERSONAL yield redo), `c_leg2c*.py/.log` (Back return redo), `c_leg3*.py/.log` (composer 6/6), `c_leg4*.py/.log` (Chromium first attempt — superseded), `c_leg4b*.py/.log` (Chromium redo), `c_leg5*.py/.log` (phone first attempt), `c_leg5b*.py/.log` (phone back-return attempt — superseded, exact-match probe error), `c_leg5c*.py/.log` (phone redo), `c_leg6*.py/.log`, `c_leg6b*.py/.log`, `c_leg6c*.py/.log`, `c_leg6d*.py/.log` (Settings attempts — superseded, probe targeting), `c_leg6e*.py/.log` (Settings redo, PASS), `c_leg7*.py/.log` (mechanism event log, BASE vs FIXED)
- Screenshots: `checker/c1-*.png`, `c2-*.png`, `c2b-*.png`, `c2c-*.png`, `c3-*.png`, `c4-*.png`, `c4b-*.png`, `c5-*.png`, `c5b-*.png`, `c5c-*.png`, `c6-*.png`, `c6b-*.png`, `c6c-*.png`, `c6d-*.png`, `c6e-*.png`, `c7-mech-*.png`
- **Filed to the branch** (one checker commit on top of the maker tip): this report, all scripts/logs/laws outputs above, and the key screenshots (`c1-ask-room.png`, `c1-ask-room-2nd.png`, `c1-academy-popup.png`, `c2b-after-personal-yield.png`, `c2c-back-normal-after-back-15s.png`, `c2c-back-throttled-after-back-15s.png`, `c4-chromium-ask-room.png`, `c4b-chromium-after-back-15s.png`, `c5-phone-ask-room.png`, `c5-phone-room-back.png`, `c5c-phone-after-back-15s.png`, `c5c-phone-academy-popup.png`, `c5c-phone-composer.png`, `c6e-settings-tab6.png`, `c6e-hub-landing.png`, `c7-mech-fixed.png`, `c7-mech-base.png`). The remaining screenshots live only in the local workspace copy of `checker/`.
