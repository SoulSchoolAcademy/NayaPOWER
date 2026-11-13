# RECORD — Hub Shell Bars: round black circles + the three ultimate gems
## 2026-11-13 · Maker seat (Factory / PI / Hub) · Branch `hub/shell-bars-20261113`

**Bullseye (one line):** the Hub shell carries round black circle icons and the three ultimate gems at the very bottom — the square chips row is gone.

**Staged link (the deliverable):** https://naya-public-blog-staging.nayapower.workers.dev/s/sn2696
**Proof-host link (secondary, same bytes):** https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/hub-shell-bars-20261113/index-intel-today.html&ref=hub/shell-bars-20261113&cb=bdff418ea320e911754ad8c9c3c3905673c61c21
**Correction (second commit on this branch):** the first commit carried this link with an uppercase `TEAM-NITRO/` path, copied from the bottom-icons pattern — but this round's files live under lowercase `team-nitro/` (the repo carries both casings; the slug round filed lowercase too), so the uppercase link 404d. The link above is the corrected lowercase path, verified 200 + byte-identical; nothing else changed.
**Fixed shell:** `index-intel-today.html` — **5,559,180 B**, sha256 `a687f16a666f27875dcc2cdb6dbe5fca113cf7eed610d76ff5b39ee8fc8d02ac` (+3,622 B over base)
**Index blob SHA:** bdff418ea320e911754ad8c9c3c3905673c61c21
**Branch:** `hub/shell-bars-20261113`, created first from main tip `89cd51451c2c640ac9773385ab6748aa6b7019cb` (re-read first-hand via `git ls-remote` before branching; unchanged at filing). No merge, no PR, no live touch, no deploy beyond staging, no SN approval, no mail.
**Work directory:** `~/workspace/team-nitro/hub-shell-bars-20261113/`
**Status: DONE — the bullseye is proven on staging.** The upper bar is nine round black circles with labels; the very bottom is the three ultimate gems (amethyst Personal, emerald Business, diamond Thing) with live counts; the square chips row is gone. Nothing touched live.

## The verdict, in one line

Nine round black circles above, three ultimate gems below, one flush stack, content clear — measured on staging at 390 / 1440 / 360 with 9 trio clicks + 9 upper clicks all landing.

## Nutshell

Ground truth re-verified first-hand: base shell byte-identical to the brief (5,555,559 B, sha `727abfd1…`), main tip `89cd5145`, the bar regions read line by line, the harvests read first-hand (bottom-icons Hub leg, gate tile, messenger gems, the shell's own eco CSS). One scorecard cycle (10 loves / 10 don'ts / 10x value / 10 solutions — `SCORECARD-HUB-SHELL-BARS-20261113.md`). The fix is an edit to the base shell in 9 hunks, all inside the bar regions: the Activity pill removed; the upper jewels restyled into the shell's own eco circles (46/44px, 50%); the trio transplanted verbatim from the bottom-icons Hub leg (gate tile + messenger gems, SEGS re-keyed to worlds, counts live, taps by full URL); the eco-offset fallback follows the new trio height. The `.main` clearance was measured, not assumed — computed 220px desktop / 380px phone clears the new stack (≈166 / ≈145px) by a wide margin, so no clearance change was made, and the brief's 161/193 prescription was deliberately NOT applied (it would under-clear the obb-bar stack: 161 < 166 — see §3). Staged to `naya-public-blog-staging` only (phase-1 worker unchanged, read back byte-exact), shell read back byte-identical to local, and the full verification passes at all three widths with zero console/page errors and zero overflow. The ask-room override was PROVEN (71px lift, flush stack), not left open. One behavior is characterized honestly, not hidden: programmatic smooth scrolls of the upper row settle unsnapped in this Firefox — identical in the base shell, mechanism untouched, the user-gesture (wheel) path snaps correctly (see §5).

## 1. Ground truth re-verified first-hand at round start

Every number below was measured by the maker in this round, not taken from the brief.

- **Main tip at round start:** `89cd51451c2c640ac9773385ab6748aa6b7019cb` (fresh `git ls-remote origin refs/heads/main`), same at filing. Branch `hub/shell-bars-20261113` free at dispatch and at filing.
- **Base file:** `~/workspace/team-nitro/hub-slug-resolution-20261113/index-intel-today.html` — **5,555,559 B**, sha256 `727abfd1a96469fa27bceaefd027e0810a8b5577b410f67647fdb47b4f68cd24` — exactly the brief's figures. Working copy verified byte-identical before editing.
- **Upper bar `#obb-bar` (markup lines 9682–9694, CSS 9697–9711):** ten `.obb-pill` anchors; `.obb-pill` 58×52px, `border-radius:14px`; `.obb-jewel` 29px, `border-radius:9px`. Activity pill line 9685 carries the `.obb-badge os-b3-badge` — and `os-b3-badge` occurs NOWHERE else in the file (grep: 1 hit), so removing the pill removes the badge entirely. No JS queries `.obb-pill` by count.
- **Bottom bar `#naya-notif-bar` (CSS 366–429, JS 5541–5600):** SEGS line 5583 `[['mail','MAIL','#3fb8ff'],['activity','ACTIVITY','#2fe89e'],['spaces','SPACES','#ffbf3d']]`; `.notif-tile` 54px, `border-radius:16px`, no labels in the built markup; taps `/hub/mail`, `/hub/feed-activity`, `/hub/spaces` via `NayaRouter`.
- **Already in the shell, unused by the markup:** `.eco-bb-btn` / `.eco-bb-ico` (lines 308–357) — 46px desktop / 44px phone (phone rule line 360), `border-radius:50%`, round black circle with own-color hover glow. The round-circle object is already in the file; the markup uses the pills instead.
- **Clearance (COMPUTED, not stylesheet text):** `.main` computed `padding-bottom` is **220px desktop / 380px phone** — the stylesheet text says 186/380, but the later rule `.main { min-width: 0; padding-bottom: 220px; }` (line 705) wins at desktop (same specificity as line 431, later in the sheet); at ≤640px the `body .main` 380px rule wins by specificity. The brief's warning ("stylesheet text lies here") is confirmed in the other direction: the text understates the desktop clearance.
- **Ask-room override (lines 2699–2714):** `body:has(.naya-ask-room) .notif-bar{bottom:calc(71px + ...)}` — the 71px is the ASK-ROOM's own height, not the trio's; the eco leg follows `var(--notif-h)` (measured), and the obb-bar follows via its lane script. Unchanged by this round in principle; proven in §5.
- **Eco dock:** `.eco-bottombar` does NOT mount on the note landing (baseline: 0 buttons at all widths) — so the eco-offset rule is not exercised here; it still guards every other view. The lane script for the obb-bar measures `#nsbBottom`, `.notif-bar`, `.jewelbar` (not the eco dock) — the stack on this page is obb-bar + notif-bar only.
- **Callers of the trio (checked before re-keying):** `NayaNotif.set('mail', n)` (line 7545) and `NayaNotif.bump('spaces')` (line 7624) write the SAME storage keys the new counts read (`business` ← `mail`, `thing` ← `spaces`) — compatible, untouched. `refresh()` is key-agnostic. `data-notif` occurs only inside `NayaNotif`. `obb-badge` occurs exactly 2x (1 CSS rule + 1 markup span) — both removed.
- **Harvests re-verified first-hand:** bottom-icons Hub leg `hub-fixed.html` (5,018,313 B, blob `529326da…`): trio CSS lines 376–427, gem ICONS lines 6986–6988, SEGS line 6991, segment creation lines 6997–7002 — all extracted programmatically at apply time (never retyped). Messenger gems confirmed distinct by SVG hash in §5. Gate tile confirmed as the leg's source (its own comment cites `hub-bar-round-icons-fixed.html` lines 9691–9705).
- **Staged shell before the round:** `GET /hub` on staging, 5,555,559 B, sha `727abfd1…` — exactly the base shell.

## 2. Baseline (the page as it stood, before the edit)

Playwright Firefox, fresh profile per width, start at `/s/sn2696` (`probe-baseline.py`, `baseline-results.json`, screenshots `baseline-*.png`).

| Width | Note landing | Upper jewels | Trio tiles | Stack | `.main` computed | Errors / overflow |
|---|---|---|---|---|---|---|
| 390 | title SN-2696, hook yes, no "isn't here" | 10 pills, 26px, 9px | 54px, 16px, no labels | obb 67 + trio 79 = 146 | 380px | 0 / 0 |
| 1440 | same | 10 pills, 29px, 9px | 54px, 16px, no labels | obb 77 + trio 79 = 156 | 220px | 0 / 0 |
| 360 | same | 10 pills, 26px, 9px | 54px, 16px, no labels | obb 67 + trio 79 = 146 | 380px | 0 / 0 |

- `--notif-h` 79px (old trio: row 78 + 1 border). `--obb-below` lives on the bar element, not `:root` (read from `#obb-bar` inline style in the final probe).
- **Cover, baseline:** the lowest `.main` text at max scroll ends 328px above the obb-bar top at 390 (and higher at 1440) — `.main` content clears by a wide margin. The only text rects under the bars are (a) the body-level `button.naya-search-button` ("Search") at the document end — the search entry point, OUT of scope (search rides Personal-complete), pre-existing; and (b) the left rail's nav labels (`aside.rail.left`) — the side rail, OUT of scope, pre-existing. Named here, not hidden, not moved by this round.
- **Seen by eye (baseline bar shots):** ten square chips with colored borders; three big colored square tiles with no labels; a stray green dot floating on the upper bar's top edge (the Activity badge, `top:-7px`) — the doubling-up Shawn saw.

## 3. The fix (apply-fix.py — anchored, count-asserted, aborts on any move)

Script: `apply-fix.py` in this work dir. Base asserted (sha `727abfd1…`) before editing. Edit, never rebuild. **9 hunks, all inside the bar regions** — full text in `diff-vs-base.txt`:

| Hunk (base lines) | Change |
|---|---|
| 1. Markup 9685 | Activity pill removed (with its badge span). 9 doors remain, same order, same destinations. |
| 2. CSS 9705–9711 | Upper-row circles: `.obb-pill` becomes the transparent column button (`.eco-bb-btn` harvest); `.obb-jewel` becomes the 46px circle (`border-radius:50%`, obsidian radial gradient, own-color rest glow via `--obb`); hover/focus lift lands on the jewel; `.obb-badge` rule deleted; phone: 44px circle. `.obb-lbl` unchanged (visible label under each icon). |
| 3. CSS 385–418 | Trio CSS transplanted VERBATIM from the bottom-icons Hub leg (gate tile: 38px desktop / 27px phone, `border-radius:50%`, two-tone rim, twin gradients, 5-layer shadow, own-color glow; hover/active rules; old `::before` gloss deleted; `.notif-lbl` 12px; phone block 27px/14px/10px/20px bubble). |
| 4. CSS 429 + 2700 | Eco-offset fallback `79px` → `85px` at both sites (new trio height per the round) + named comment at 429. The measured `--notif-h` still rules; the fallback is pre-init only. |
| 5. JS 5544 | `counts()` re-keyed: `{ personal: ActivityLog unread, business: mail, thing: spaces }`. Storage keys keep their names. |
| 6. JS 5556–5560 | `tap(k)` re-keyed: full-URL `location.href` to `https://nayanet.app/personal` / `/business` / `/space`; count clears on tap as before. |
| 7. JS 5579–5593 | Gem ICONS (verbatim extraction: amethyst / emerald / diamond) + SEGS (verbatim: `personal/Business/Thing`, third never "space") + segment creation (verbatim: `id=segPersonal/...`, `data-gem`, `aria-label "... activity — open"`, label in flow). |
| — | NO hunk touches the note, `SLUG_MAP`, the maybeAuto guard, the feed, the search, or the side rail. NO `.main` clearance change (see below). |

**Fixed shell:** `index-intel-today.html` — **5,559,180 B**, sha256 `a687f16a666f27875dcc2cdb6dbe5fca113cf7eed610d76ff5b39ee8fc8d02ac`, **+3,622 B** over base.

**Clearance decision (measured, not assumed):** after the edit the stack is trio 86 + obb 84 = **170px desktop** and trio 72 + obb 76 = **148px phone** (measured in §5). Computed `.main` padding (220 / 380) clears it by 50 / 232px, and the cover probe confirms the lowest `.main` text ends 145px above the bar top at 1440 and 326px above at 390/360. The brief's conditional ("IF the computed padding does not clear the stack, set the later `.main` rule as the round did (161px desktop / 193px ≤640px)") does NOT fire — and applying 161/193 would have been WRONG here: 161px desktop is BELOW the new 170px stack, so it would have put content under the bars. The 161/193 numbers were calibrated for the live Hub stack (eco + trio, no obb-bar); this shell's stack adds the obb-bar. The scorecard records this decision before the build; the probe proves it after.

## 4. Stage (staging only)

`deploy_hub_assets.py stage` into the NEW dir `staging-assets` in this work dir (the slug round's staging dir untouched). Stage ran against main head **`89cd51451c2c`** — the branch base. Stage result: **39 `HUB/app` files, 37 downloaded** (2 overlaid). Overlay `index.html` 5,559,180 B + `feed-live.json` 8,012,323 B (same sha as the slug round's — the feed is unchanged). The stage also fetched main's `HUB/hub-worker.js` (27,225 B) beside the staging dir — **deleted immediately after staging** so it could never be confused with the phase-1 worker; never deployed. Stage diff vs the slug round's set: **exactly one file differs** — `./index.html`.

Deploy: `deploy-shell-bars-staging.py` (modeled on the slug round's script). `run_worker_first` base 8 + phase-1 extra 4 — no phase-2 patterns. Script asserted before the PUT: `hub-worker-phase1.js` 49,174 B, sha `8ee4f859…` — **unchanged, read, never edited**. Deploy: manifest **39 files / 22,414,626 B**, 1 bucket / 1 file uploaded (HTTP 201 — only the changed shell), PUT success, `etag=81fbb511c95657ca`.

- **Read-back, staged shell:** `GET /hub` on staging, **5,559,180 B**, sha256 `a687f16a…` — **exactly the fixed shell**.
- **Curl battery:** browser GET `/s/sn2696` → **302** to `https://naya-public-blog-staging.nayapower.workers.dev/#/smart-notes/sn2696` (as before).
- **Live untouched:** no live read or write in this round beyond the click destinations (see §5) — the trio/upper clicks navigate to live pages as a fresh visitor would; no account, no save, no mail.

## 5. Verification (Playwright Firefox, real browser, staged)

Method: `probe-verify.py` (full results in `verify-results.json`; screenshots `verify-*.png`). Fresh profile per width — 390 FIRST, then 1440, then 360. Start at the staged note link `/s/sn2696`; note landing confirmed first. Counts preset via init script (`localStorage` mail=3, spaces=2) before page scripts run.

**Note landing (all widths):** URL `…/#/smart-notes/sn2696`, title `SN-2696 · SYSTEM / INTELLIGENCE / FEEDS — NayaNET`, hook present, no "isn't here", 1 `.intel-board` (same single layer as the baseline — the note is untouched), no install overlay at first paint, **zero console errors, zero page errors, zero overflow** (scroll 0 and scrolled). Full-id control at 390 (`#/smart-notes/IB-SMART-NOTE-20261112-the-infinite-smart-feeds`) renders identically — same title, hook, 1 board, 9 pills, 3 segs, 0 overflow, 0 errors.

**Bars (computed `border-radius` of the icon element itself):**

| Width | Upper jewels | Trio tiles | Labels | Gems (SVG sha, 12 hex) |
|---|---|---|---|---|
| 1440 | 9 × 46px, 50%, all labels visible | 3 × 38px, 50% | Personal / Business / Thing | `3a8d9520e018` / `044446e6eb3d` / `694dec628d28` — three distinct |
| 390 | 9 × 44px, 50%, all labels visible | 3 × 27px, 50% | Personal / Business / Thing | same three hashes |
| 360 | 9 × 44px, 50%, all labels visible | 3 × 27px, 50% | Personal / Business / Thing | same three hashes |

Exactly **1** `#naya-notif-bar`, exactly **3** `.notif-seg`, **9** `.obb-pill`, **0** Activity pills. No square chips anywhere in either bar (no 16px / 14px / 9px radius on a bar icon). The eco dock does not mount on the note landing (0 buttons, all widths) — the stack is obb-bar + trio only.

**Counts (preset mail=3, spaces=2):** Business bubble `3` shown, Thing bubble `2` shown, Personal `0` hidden — at all three widths. Live from the shared stores, not stubs.

**Stack (measured):** `--notif-h` **86px desktop / 72px phone** (the round's numbers, reproduced exactly); `--obb-below` **86px / 72px** (measured by the lane script, on the bar element); obb-bar bottom == trio top at all widths (flush: 814/814, 772/772, 728/728). New stack: 170px desktop / 148px phone.

**Cover (rect-by-rect at max scroll, fixed-ancestor-excluded):** lowest `.main` text ends **145px above** the obb-bar top at 1440, **326px above** at 390, **326px above** at 360 — clears by a wide margin. (The only text rects under the bars are the pre-existing Search button and rail labels named in §2 — out of scope, unchanged.)

**Clicks — trio 3/3 at every width (fresh load each):**

| Width | Personal | Business | Thing |
|---|---|---|---|
| 390 / 1440 / 360 | → `https://nayanet.app/personal` ("Shawn Vibert") | → `https://nayanet.app/business` ("Acme Corp") | → `https://nayanet.app/space` ("Our Community") |

**Clicks — upper row 9/9 at 1440 (fresh load each):** Mail → `https://nayanet.app/rooms/mail` ("Smart Mail — NayaNET") · Dashboard → `/dashboard` ("Smart Score Dashboard — NayaNET") · Business → `/business` ("Acme Corp") · Space → `/space` ("Our Community") · Growth → `/rooms/growth` ("Smart Growth — NayaNET") · Connections → `/rooms/connections` ("Your Connections") · Smart Lists → `/rooms/lists` ("Smart Lists") · Reports → `/rooms/reports` ("Reports — NayaNET Intelligent Hub") · 10 apps → `https://nayanet.app/#/hub` (title is the live entrance title, "NayaNET — Main entrance, variant C…" — the href is unchanged from the base shell; the title is whatever live serves a fresh visitor at that URL, recorded as observed).

**Ask-room override — PROVEN (390):** the "Ask Naya" nav button opens the room; with it open the trio lifts by exactly **71px** (bottom 773 vs viewport 844) and the obb-bar rides flush above it (obb top 625, obb bottom 701 == trio top 701). The lifted stack composes; no overlap between the bars. The brief's "prove it or name it open" is answered: proven.

**Snap (upper row, characterized honestly — `probe-snap.py`, `probe-snap2.py`):** the mechanism is byte-identical to the base (same `scroll-snap-type:x mandatory`, `scroll-padding`, `scroll-snap-align:start` — the diff touches none of it). User-gesture scrolls snap correctly: a real mouse-wheel scroll settles with a whole circle at the snapport start (DASHBOARD at 390/360, three trials, every time) and all 9 are reachable (max scroll: 10 APPS whole at all widths); at rest the leftmost circle (MAIL) is whole at all widths; at 1440 the row does not scroll (all 9 fit). The trailing circle peeks at the right edge — the affordance the brief names. **One pre-existing nuance, named not hidden:** programmatic smooth scrolls (`scrollTo({behavior:'smooth'})`) settle unsnapped in this Firefox (390: 208, three trials, every time) — and they do the SAME in the base shell (115 after smooth-120), so this is not a regression and not something this round changed; no user gesture ever triggers a programmatic row scroll. The snap verdict is: mechanism kept, user path proven, programmatic path characterized as pre-existing.

**Screenshots read by eye:** `verify-bars-1440.png` (nine lit circles, three gems with bubbles 3/2, one family), `verify-bars-390.png` / `verify-bars-360.png` (circles + gems + labels at phone widths), `verify-note-*.png`, `verify-scrolled-*.png`, `verify-askroom-390.png`.

## 6. Design-contract gate (a)–(i) + human checks H1–H5 + L1–L7

- (a) Zero white/light backgrounds — PASS: the change adds only obsidian gradients; no light background introduced.
- (b) Every element raised/elevated — PASS: tiles carry the 5-layer shadow + rim; circles carry the eco shadow + glow; bars carry their shadows.
- (c) Gauges/numbers alive — PASS (scoped): the bar's numbers are the count bubbles, live from the shared stores (3/2 proven).
- (d) No text-in-image — PASS: no new images; gems are inline SVG.
- (e) No bare text blocks — PASS (bar): labels live in segments/pills.
- (f) No look-alike — PASS: tiles ARE the harvested gate object verbatim; gems verbatim from the messenger; circles ARE the shell's own eco object.
- (g) `##` sections — PASS: this record's sections.
- (h) No dictation-blunt phrases — PASS: no new public copy; labels are single words (Personal, Business, Thing).
- (i) Title+subtitle+nutshell + faces alternate — PASS (scoped): labels are the titles; gems are the faces of the doors, three distinct silhouettes.
- H1 stranger test — PASS: nine labelled round doors above, three labelled gem doors below; the screenshots answer "where do I go" with the doors themselves.
- H2 perfect-words law — PASS: labels are his words (Personal, Business, Thing), crafted, no process talk on the page.
- H3 face quality — PASS: three distinct gem silhouettes by hash and by eye (amethyst orb, emerald cut, diamond).
- H4 test in his head — PASS: 10-star? Round black circles + gems as ordered. Obvious? Labels + gems. Useful? Doors to their worlds. Done clearly? Measured throughout §5.
- H5 one ultimate ten — PASS: the round is judged as one ultimate ten; the scorecard carries the ten-lists.
- L1–L7: as H1–H5 above; L3 — the bars are nav, not boards; their single-word labels are their titles by design; L6 — `##` sections throughout this record; L7 — one ultimate ten, scored honestly below.

## 7. Self-checks + seven pre-merge answers

**Self-check 1 (the build itself):** all anchors counted 1x before each edit; the apply script aborted twice on its own assertions (an over-broad radius assertion, then a stale line-list bug, then a comment tripping its own assertion) and the working copy stayed at the base sha until all three were fixed — the guards work. The diff is exactly 9 hunks in the bar regions; the slug fix hunks are absent from the diff (verified: no hunk near `SLUG_MAP` / maybeAuto).
**Self-check 2 (the browser proof, new evidence):** the staged bars measure 50% / 46-44 / 38-27 at all widths; counts 3/2 live; clicks 9 + 9 land; cover clears by 145–326px; the ask-room override proves the 71px lift. Found the snap nuance (programmatic smooth settles unsnapped — base does the same) and characterized it with a controlled base-vs-fixed experiment instead of smoothing it over.
**Self-check 3 (the proof itself, new evidence):** re-read the diff hunk by hunk (9 hunks, named in §3); re-verified the staged bytes equal the local bytes by curl + sha; re-ran the full-id control (identical); confirmed the "10 apps" destination title is live's entrance title (href unchanged); confirmed main did not move mid-round (89cd5145 at start and at filing).

**Score: 9/10, honestly.** What earns the 9: ground truth re-verified completely; harvest-only edits with verbatim extraction; diff confined to the bar regions; stage/deploy/read-backs byte-exact; full verification green at all three widths (radii, sizes, labels, gems, counts, 18 clicks, cover, zero errors, zero overflow); ask-room proven; full-id control identical. What keeps it from 10: the snap characterization — a programmatic smooth scroll of the upper row settles unsnapped in this Firefox (pre-existing, identical in the base, user-gesture path proven). The round's own deliverable (the bars on the page) is 10/10; the one behavior I could not prove to the letter is named above.

**Seven pre-merge questions:**
1. **Three self-checks done?** Yes — §7 above, each finding new things (the apply-script guard trips; the snap nuance + base-vs-fixed experiment; the "10 apps" live-entrance title + main-stability re-check).
2. **Honest 9+?** Yes — 9/10, with the deduction named (the snap characterization) and the bullseye fully proven.
3. **Blast radius named?** Staging worker only: the staged shell (read-back verified). Phase-1 worker, phase-1 record, and assets untouched. Live untouched (no live write; the click proofs navigate to live pages as a fresh visitor would). No main change except this branch filing. No mail. Nothing to roll back except the staged shell itself, which the next deploy replaces by the same flow.
4. **Checks green?** Yes — curl read-back green; verification green at 390/1440/360; full-id control identical. One known exception, named in §5: programmatic smooth scrolls settle unsnapped in this Firefox (pre-existing, base-identical).
5. **Five gates?** Yes, with evidence: right (the square bars Shawn called wrong are replaced by the doors he ordered, through harvested objects, nothing faked); truly needed (his words on the staged note page named exactly this fix); mine to do (briefed maker seat, bar only, staged only, approval held for Shawn, live leg named not executed); now (dispatched as the next mission, base + harvests in hand); provable (every count cited first-hand, screenshots filed, read-backs byte-exact).
6. **Real proof?** Yes — live bytes, shas, line numbers, counts, browser measurements and screenshots, all read first-hand in this round and listed in §1–§5.
7. **No silent known defects?** None silent — the snap nuance, the Search-button/rail-label cover notes (pre-existing, out of scope), the "10 apps" live-entrance title, the Mail/Activity doors leaving the bar (a real UX change — mail lives in the inbox / Smart Mail), and the `nayanet.notif.spaces` key keeping its name while the segment is labelled Thing are all named here.

## 8. DONE / NOT-DONE

**DONE:** ground truth re-verified first-hand (base sha, main tip, bar regions, harvests, callers, clearance computed not assumed) · one scorecard cycle with the ten-lists · fix applied as 9 hunks to the base shell, diff-proven, slug fix byte-identical · staged into a new dir, byte-diff clean (only `index.html`) · deployed to staging only, shell read back byte-exact · full verification at 390/1440/360 (radii, sizes, labels, gems by hash, counts 3/2, 9 trio + 9 upper clicks, cover, zero errors, zero overflow) · ask-room override proven · full-id control identical · branch filed, one commit, read-back verified · record + scorecard + receipt written.
**NOT-DONE (not mine, or not yet):** the live leg (Shawn's tap — the fixed shell + the branch workflow; live still serves the SN-sync rebake with no note route) · SN-2696's approval (Shawn's hand) · the feed / search / side rail (Personal-complete round — includes the Search button and rail labels sitting under the bars at max scroll, pre-existing) · the top-bar chips on other pages (out of scope) · per-world live delivery path (counts use the existing shared stores, per the trio spec) · the snap nuance (programmatic smooth scrolls settle unsnapped in this Firefox — pre-existing, base-identical; user-gesture path proven) · checker + captain double-check still owed; merge + live deploy wait for Shawn's eye and his tap.

## The next step, recommended

Bring the staged link to Shawn with the phone-width bar shot: nine round black circles, three gems below, counts live. Then the live leg on his tap: fixed shell through the branch workflow, a walked live entrance after it lands — and the Personal-complete round for the feed, search, and side rail.
