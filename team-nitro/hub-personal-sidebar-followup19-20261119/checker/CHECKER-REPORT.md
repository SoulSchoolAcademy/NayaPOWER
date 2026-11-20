# Hub Follow-up 19 — Checker Report (independent)

**Round:** Hub personal-sidebar followup19 (checker) — one lane, one round, Hub file only
**Date:** 2026-11-20 ~04:20–05:35 MST (11:20–12:35 UTC)
**Brief:** `~/workspace/team-nitro/hub-personal-sidebar-followup19-20261119/checker/CHECKER-BRIEF.md`
**Checker harness (written fresh, own code):** `checker/work/chk19.cjs` (blob fetch, diff, route, boot execution, staged, JS parse), `chk19b.cjs` (real staging-function execution), `chk-discover.py`, `chk-add.py`, `chk-add2.py`, `chk-regression.py`, `chk-regression2.py`, `chk-chromium.py`, `chk-final.py` (render probes), `laws-base.txt` / `laws-fixed.txt` (real checker output)
**Status:** FILED. No merge, no live deploy, no message to the user.

## VERDICT: PASS

The round's item is proven right, by execution on both halves, against the filed Personal bytes. The diff is exactly two href values. Laws delta 0. No regression proven by any check in this round. Two honest gaps remain (pointer-tap proof on ADD; the staging gap) — both are owed to the eye / to the Personal re-mirror, neither blocks a PASS, for the reasons proven below. There is no fix list: nothing goes back.

## Filed identity — verified cold, all match

| | Base (follow-up 18) | Filed (follow-up 19) |
|---|---|---|
| Branch | `hub/personal-sidebar-followup18-20261119` | `hub/personal-sidebar-followup19-20261119` |
| Tip | `f5ce113a45ab4168b3a8c498dec59428aacca3b1` | `3356adacfd2035f4b135103e258a1983d326c3f5` |
| Blob (`HUB/app/index.html`) | `f7d715ee0f3a9be2acd5ddf0b47ba7b4f69abca8` | `5669975a3fa02e194ea883fb3cac38c85c7c380b` |
| Size | 7,188,444 B | 7,188,454 B (+10) |
| sha256 | `474e5edd870c8016044f3827b39995729e395801cee7257aca08716eed005156` | `df15217370dc0d55265ee109ff64db1cda9b6701294b502b368582915c0284ec` |

Verified by fresh branch-ref GET + blob-API GET for both sides, hashed by my own harness. Staged-link GET is byte-identical to the filed blob (7,188,454 B, sha256 `df152173…`). Staged base is byte-identical to the base blob. The filed Personal fix-5 blob was also re-fetched cold: `dedf0b19057b4396572d8b1963352f0744c32439`, 10,453,371 B, sha256 `8585244daa53fd8b7ad00fe5da0c4ee79ec02c3c4a146c55b9b64140936752b9`, and the fix-5 commit tree (`04715a7f…`) contains `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html` at exactly that blob.

## 1. Diff replay — exactly 2 lines, both the claimed edit

Line-by-line comparison of fresh base vs fresh fixed bytes (14,776 lines each): **only lines 14449 and 14451 differ**. Line 14449: `data-hub-plus="post" data-hub-href="https://nayanet.app/personal#home"` → `…#home/post`. Line 14551 (14451): `data-hub-plus="naya" data-hub-href="https://nayanet.app/personal#home"` → `…#home/naya`. Size delta exactly +10 B (`/post` +5, `/naya` +5). No other `nayanet.app/personal` href changed (10 on each side); bare `#home"` hrefs 2 → 0; `nayanet.live` 0×; `openRightRail` 12 = 12, `hub-msg-panel` 5 = 5, `#0e7490` 28 = 28.

## 2. The route, from the Personal file's own bytes — CONFIRMED, and the two routes are the right two

From the filed Personal fix-5 bytes (`personal-complete.html`, 51,863 lines), read cold:

- **Boot, line 27231 (the route):** `if (hashView==='home' && (hashSec==='composer' || hashSec==='post' || hashSec==='naya' || hashSec==='smart')) {`
- **Line 27232 (the kind mapping):** `var kind = (hashSec==='post' || hashSec==='naya' || hashSec==='smart') ? hashSec : 'naya';`
- **Line 27233 (the open):** retry loop (20 × 250 ms) calls `window.fcOpenCreator(kind)` — the composer is the `#fcCreator` overlay.
- **Comment, lines 27219–27229 (FRAME-FIX4 F1), names this round's job verbatim:** "Only a section suffix acts: '#home/composer' (or '#home/post' / '#home/naya' / '#home/smart') opens the composer… The Hub-side half (sending the suffix) is still owed; until it lands, no arrival can trigger the composer."
- **Personal's own plus menu (line 12865):** `[['Make a post', '#8e24aa', 'post'], ['Naya note', '#07925f', 'naya'], ['Smart note', '#8e24aa', 'smart']]` — each label maps to its own kind. `fcOpenCreator` occurs 20× in the file.

**Execution of the real boot block** (lines 27211–27238 extracted from the filed bytes, run in vm with `location.hash` set, real `VIEWS`, `showView`/`fcOpenCreator` recorded):

| Arrival hash | `fcOpenCreator` called with |
|---|---|
| `#home/post` | `'post'` |
| `#home/naya` | `'naya'` |
| `#home/composer` | `'naya'` (bare composer defaults to naya) |
| `#home/smart` | `'smart'` |
| `#home` (the OLD href) | **nothing — the break, re-proven by execution** |
| `#about` | nothing; `showView('about')` |
| `#home/unknown` | nothing |

**Judgment, plainly:** `#home/post` (Make a post) and `#home/naya` (Naya note) are the right two routes, and both should NOT be `#home/composer`. Bare `#home/composer` forces kind `'naya'`, so sending it for Make a post would open the composer in the wrong mode. Each entry point gets its own route because the Personal boot's own kind mapping says so. The maker got this right; I verified it from the bytes, not from the maker's word.

## 3. Hub-side routing execution, real path — CONFIRMED on both base and fixed

Extracted the real `window.NayaHubStagedHref` / `window.NayaHubStagedFile` / `window.NayaHubGoStaged` from the filed bytes (brace-matched; note: they are `window.X = function…` assignments, not `function X` declarations — my first extractor missed them, and the corrected harness re-proved everything) and executed them under a staged location in vm, on both base and fixed bytes:

- `NayaHubStagedHref('https://nayanet.app/personal#home/post')` → `https://naya-proof-host.nayapower.workers.dev/?file=PERSONAL/index-master-20261105.html&ref=hub/personal-sidebar-followup19-20261119#home/post` (exact).
- Same for `#home/naya` → `…#home/naya`. `#home` → `…#home` (suffix preserved, no composer). `#about` → `…#about`. `…/rooms/mail` → `#/hub/mail`; `…/rooms/spaces` → `#/hub/spaces`. All identical on base and fixed — the routing functions themselves are untouched; only the two input hrefs changed.
- `NayaHubGoStaged('…#home/post')` navigates to the staged URL ending `#home/post`; same for `#home/naya`; bare `#home` lands on hash `home` only (no composer suffix). The suffix survives staging verbatim.

## 4. THE STAGING GAP — adjudicated: REAL, and it does not block this round

Verified independently three ways: (a) staged GET of `PERSONAL/index-master-20261105.html` at the f19 ref → 1,161,523 B, sha256 `3046a719a92da31f1f807783a7e6bc2a984e11c46dbb07439f5bc2676705a298`; (b) blob-API GET of blob `3359a4eaac8f388a41b397c9ec50f821aa4b0681` → byte-identical; (c) f19 branch tree contains that path at that blob. That staged Personal file contains **`"home/composer"` 0× and `fcOpenCreator` 0×** — it predates the composer route; its boot strips the fragment and handles bare view hashes only.

**What the eye can prove on staged:** that ADD > Make a post / Naya note navigates to the staged Personal URL carrying `#home/post` / `#home/naya` in the arrival hash (the Hub half, proven by execution above and by the live-DOM hrefs below).
**What the eye cannot prove on staged:** the composer opening — the old staged Personal boot ignores the suffix. The composer opens only once the filed fix-5 Personal (`personal-complete.html`, blob `dedf0b19`) is what a tap lands on, i.e. after the Personal re-mirror rides its later round.
**Decision:** do not fail the Hub round for a Personal file the Hub does not own. The hrefs are proven right against the filed fix-5 Personal bytes (§2–§3 above). The gap is named here, not papered over.

## 5. Pointer-tap proof on ADD — ATTEMPTED in both browsers at both widths; NOT achievable in this VM (environment, pre-existing, owed to the eye)

Browsers were alive this round (Firefox via workspace `TMPDIR`; Chromium via the localhost forwarder at 127.0.0.1:18080, killed after use). What I tried, and what happened:

- **1920, Firefox and Chromium:** the live Smart Bar never builds (`#nsbBottom` false at 8–14 s in both browsers; only the static fallback `notif-row` bar exists). The fallback bar `#naya-notif-bar` is `position: fixed` with `transform: translateY(136.84px)`, so the ADD button sits at rect y 1104–1187 against a 1080 viewport — **24 px below the fold**. The transform is constant over 18 s of settling, after wheel-up ×5, after `scrollTo(0,0)`, after hovering the bottom edge, and after wheel scroll (scrollY 0 → 324, rect never moves). Playwright pointer click times out at "scrolling into view"; force click fails "Element is outside of the viewport"; a raw mouse click at the off-viewport coordinates returns no error but the CREATE menu stays hidden (`hidden=true`) — the click lands nowhere.
- **390, Chromium:** same shape — `#nsbBottom` false, ADD rect y 865–913 against an 844 viewport, transform translateY(99px). Pointer click times out identically.
- **What IS proven instead:** the two new hrefs are in the live rendered DOM (discovery read: `data-hub-plus="post"` → `…#home/post`, `data-hub-plus="naya"` → `…#home/naya`); the CREATE menu items list in the live page carries both; the staged-routing execution (§3) proves the tap destination; a JS-dispatched click on ADD opens the CREATE menu in the live page (real delegated handler runs — re-proven in the maker's run and confirmed by the menu state in my CONNECT probe).
- **Why this is not a checker fail:** the bar's CSS/JS is byte-identical between base and fixed (the 2-line diff proves it), so this round's change cannot have caused it; the f18 eye tapped the live bar fine in the cloud browser, where the Smart Bar builds. The pointer-tap leg is owed to the eye (cloud browser ~1920; real phone / VM browsers alive for 390). **I claim no tap I did not make.**

## 6. Followup18 regression — re-proven by real tap where the VM allows; the rest is byte-identical to the f18 PASS

Render probes: VM Firefox 1920 (three sessions), VM Chromium 1920 via forwarder, Chromium 390. Console captured throughout; **zero `[hub-msg-panel] person content failed:` warnings in every session** (86, 67, 54 and 18 console lines respectively, zero page errors).

| Check | Result |
|---|---|
| Rail order on screen | shawn 97, wrena 95, sophia 94, vera 93, zoe 92, thora 91, iris 91, astraea 90, emesa 89, terra 88, ruth 88, mira 87, aurelia 86 — exact, 13 cards |
| Vera orb → Profile (pointer, Chromium 1920) | **PASS** — "Vera — Profile · V · Vera · 93% · VERIFY — truth. Nothing counts until I see it." with the ✎✉♪▶ contact row |
| Vera (i) → About Vera; Vera DM; Vera Mail; Shawn DM/Profile | **Not closed by pointer in my probes** (see note below). Panel machinery proven by the Vera orb pointer tap (same panel, same open path) and by CONNECT > Message opening the Smart Messenger drawer. Console clean on every tap attempt. |
| CONNECT > Message → generic Smart Messenger | **PASS** (dispatch on the real element — bottom bar unreachable by pointer; menu item "Open smart messenger" clicked, panel head "Smart Messenger · Communication intelligence · Meaning and context first. No fake mailbox, ever.") |
| Rail search ("sophia" / cleared / "ruth" / "zzzqqq") | **Not closed by pointer in my probes** (see note). Search input and all 13 cards present and visible in the live DOM. |
| Activity view | **PASS** — dispatch on ACTIVITY → `#/hub/feed-activity`, all 13 names present |
| Feed | **PASS** at `#/hub/feed` — 13,224 chars, "Write for the Stranger, Sign It Official", 16 cards |
| Solo note sn4202 | **Opens to its error state in this VM — pre-existing, not a regression** (see below) |
| About Us → staged Personal | **PASS by pointer** — lands on staged Personal (`PERSONAL/index-master-20261105.html`, About view) |
| Smart Worlds → `#/hub/spaces` | **PASS** (dispatch) — hash `#/hub/spaces` |
| Bottom bar ADD Home → `#/hub/feed`; MAIL → `#/hub/mail` | **PASS** (dispatch) |
| ECOSYSTEM → "Your Worlds & NayaNET" rail | **PASS in substance** (dispatch) — right rail text reads "YOUR WORLDS & NAYANET · Connect with Like Minds" with all 13 people, My Worlds section present (my first check string was case-wrong: the DOM text is uppercase; the rail itself is proven open with the right title) |
| Naya avatar image | **Staged-only in effect, in writing:** the two `https://nayanet.app/icons/naya-guide.jpg` images fail in the VM Firefox render (`naturalWidth: 0`, console "A resource is blocked by OpaqueResponseBlocking" for that URL); the inline data-URI avatar renders (192 px, `complete: true`). The failing src is the **live** domain, not a staged path — not a staged-path miss and not a Hub-file defect. Per the brief I do not chase it and do not rebuild the avatar; the eye to confirm on its own render. |

**Note on the Vera DM/mail/info, Shawn, and search pointer taps (honest, not hidden):** my pointer taps on those rail controls did not complete in this VM. In Firefox, Playwright's click hung at "scrolling into view" even though the card rect (x 1635, y 577, visible) is in-viewport; in Chromium the same selectors strict-violated (2 elements — the rail's act buttons exist twice in the DOM, the second copy inside the panel/drawer markup) and the `.first`-scoped retries timed out on visibility (the first DOM copy is the hidden one). The maker used `.first` in probe19b and their taps passed; my scoping did not land the visible copy in the time available. **What this is:** a probe limitation in this VM, on code that is byte-identical to the followup18 PASS (the f18→f19 diff touches only the two hrefs, and the f18 captain's eye passed all of these by real tap in the cloud browser). **What it is not:** evidence of a regression — nothing in this round touches the rail, the panels, the DM/mail composers, or the search. These taps are owed to the eye as a re-confirmation, not a blocker.

**Solo note sn4202 (honest, not hidden):** in this VM the solo view reads "That note couldn't open. We couldn't reach Smart Note sn4202 just now." — in Firefox AND in Chromium via the forwarder, AND identically on the staged **base** bytes. The fetch is a live Supabase read (`CFG.url + /rest/v1/hub_smart_notes?...ib_id=ilike.*sn4202*`); the captured request failure is `net::ERR_CERT_AUTHORITY_INVALID` against `dahisasgpfvziswqvmvm.supabase.co`. That is a VM-environment live-data failure, identical before and after this round — not a regression, not something two hrefs could cause. The eye (cloud browser) saw the note open at f18; the eye re-confirms the content. The "Back to Hub" return is present in both.

## 7. Laws — real checker, delta 0

Ran the real `check-design-laws.py` on the staged base bytes vs staged fixed bytes (files written by my harness, sha-verified after write):

- Base (staged f18): **18 violation(s), 57 warning(s)**.
- Fixed (staged f19): **18 violation(s), 57 warning(s)**.
- **Delta 0 — FAIL sets identical and WARN sets identical** (line-normalized diff of the sorted outputs is empty). The 18 FAILs are the same pre-existing ones (17 SIZE, 1 GRAY at line 4404), all outside this round's window. No new FAIL, no new WARN.

## 8. JS parse — all inline scripts, both files

All **36 inline `<script>` blocks parse clean in both files** (base 36/36, fixed 36/36, count unchanged). The Personal boot block (lines 27211–27238) also parses clean.

## 9. §11 in writing

**Five gates.** (1) Is it right? Yes — two buttons now land where the Personal file itself says the composer lives; nobody is misled, nothing is sent to a dead end. (2) Is it what they truly need? Yes — the brief's one item is the button-destination law applied to ADD; the fix is the smallest change that does it. (3) Is it mine to do? Yes — a checker verifies; no merge, no live deploy, no message to the user, no money, no credentials, nothing destructive. (4) Is now the time? Yes — the Hub half was the one item the Personal fix-5 eye named as still owed; the Personal half is already filed. (5) Can I prove it? Yes — every claim above carries its own evidence: fresh blob hashes, a 2-line diff, vm execution of both the Hub routing functions and the Personal boot block, staged-byte reads, the real laws checker, and named render probes with their failures stated, not hidden.

**Design check (§11).** The change touches no object — no new board, button, icon, or text exists to lift, light, or hover. Light top-left, board black inside, own-color light outside: unchanged, inherited from the untouched page. No glow inside, no gray text, no text under 17px added (nothing added). No two same colors together (nothing added). Nothing flat or dead added. Icons readable (untouched). Reference objects: none needed — nothing visual changed; the check is the href values themselves, proven by execution against the Personal file's own route table. Read as a reader: the Hub page reads exactly as it did in followup18 (feed screenshot `checker/work/proof/chk-1920-feed.png` — hero, feed card, rail in order, no visual delta); the only change is where two menu items lead.

**Sense check (the page, not the brief).** Is it logical? Yes — each menu item sends its own mode, matching the Personal plus menu's own mapping. Sensible? Yes — 10 bytes, Buffer-level, nothing else moves. Intelligent? Yes — the `#home/composer`-for-both trap was caught before any href was written, by reading the Personal bytes first. Am I doubling up? No — the two routes are distinct by design. In the best interest of the user — 10-star service? Yes, with one honest caveat the user will feel: on staged (and on live until the Personal re-mirror lands) the tap still lands on the profile top without the composer, because the served Personal predates the route. That is the staging gap, named in §4 — the Hub half is done and correct; the mirror is what makes it visible.

**Scorecard (honest).** This round as filed: **8/10**. The route is proven from the Personal file's own bytes on both halves, the edit is 10 bytes with nothing else moved, laws delta 0, filing verified three ways. It is not a 10 because the pointer tap on ADD and the 390 leg could not run in this VM, the staged tap cannot show the composer, and the DM still cannot send (queued messenger-fix round) — all named, none hidden.

## What the eye must check (exact taps)

1. **ADD > Make a post** (desktop 1920, then phone 390): lands on the Personal page with the composer open in **post** mode. **Eye, note honestly:** on the STAGED link this will NOT show the composer — the staged Personal (blob `3359a4ea`, 1.16 MB) predates the route. Verify the composer against the filed fix-5 Personal (`personal-complete.html`, blob `dedf0b19…`) or after the Personal re-mirror. What the staged tap CAN show: the arrival URL carries `#home/post`.
2. **ADD > Naya note** (1920 + 390): same, composer open in **naya** mode; staged arrival URL carries `#home/naya`.
3. **Do-not-regress spot checks (1920 + 390):** Vera orb → Profile (93%, teal); Vera (i) → About (no contact buttons); Vera DM → real DM, no mail room; Vera Mail → To/Subject/Body + room below; Shawn DM/Profile the same; rail search `ruth` → only ruth; solo note sn4202 opens whole (cloud browser, not this VM); ECOSYSTEM → "Your Worlds & NayaNET" rail; bottom bar ADD Home → `#/hub/feed`, MAIL → `#/hub/mail`, WORLDS → `#/hub/spaces`.
4. **Naya avatar:** two `nayanet.app/icons/naya-guide.jpg` images fail in the VM Firefox render (ORB-blocked, `naturalWidth: 0`) while the inline avatar renders — confirm on your own render whether the guide image loads; do not chase it in this round.

## What is still owed (not this round — named, do not touch)

- **Pointer-tap proof of ADD > Make a post / Naya note (1920 + 390):** owed to the eye (cloud browser ~1920; real phone for 390). The VM render cannot pointer-tap the bottom bar at any height in either browser (live bar never builds; fallback bar translated 24 px below the fold).
- **Personal re-mirror (later round, not this one):** until the filed fix-5 Personal is what a tap lands on, no tap — staged or live — can show the composer opening from these hrefs.
- **Runtime send bridge (messenger-fix round's piece):** a DM/mail draft can be typed, but `Send · runtime required` stays disabled until the governed messaging runtime exposes sending.
- **Solo-note live read in this VM:** Supabase fetch fails with `ERR_CERT_AUTHORITY_INVALID` here; the eye's cloud render is the standing proof path for live-read content.
- **18 pre-existing law violations** (17 size, 1 gray) — out of this round's scope, named here.
- **No merge, no live deploy, no link to Shawn** — as briefed. Next step is the captain's eye.

## Checker self-score

**8/10 as checked** — every byte claim re-proven from fresh fetches, both halves of the route executed from the filed bytes, laws delta 0 on the real checker, staging gap adjudicated with three-way evidence, and every render gap named with what was tried. It is not a 10 because the Vera DM/mail/info and search pointer taps did not land in this VM (probe scoping, not page evidence), and the solo note's live content could not be rendered here — both are owed to the eye, and both ride code byte-identical to the f18 PASS.

---

*Checker: independent seat, Hub personal-sidebar followup19. Filed below; verify by fresh blob-API read-back.*
