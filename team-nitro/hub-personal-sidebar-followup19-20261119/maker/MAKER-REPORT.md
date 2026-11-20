# Hub Follow-up 19 — Maker Report

**Round:** Hub Follow-up 19 (maker) — one lane, one round, Hub file only
**Date:** 2026-11-20 ~03:52–04:20 MST (10:52–11:20 UTC)
**Brief:** `~/workspace/team-nitro/hub-personal-sidebar-followup19-20261119/HUB-FOLLOWUP19-BRIEF.md`
**Maker script:** `~/workspace/team-nitro/hub-personal-sidebar-followup19-20261119/maker/work/edit19.cjs`
**Analysis scripts:** `analyze19.cjs`, `analyze19b.cjs`, `grep19.cjs`, `grep19b.cjs`, `sel19.cjs`
**Probe scripts:** `probe19.py` (1920), `probe19b.py` (fixed selectors), `probe19c.py` (pointer taps), `tap19.py`, `tap19b.py`, `geom19.py`, `geom19b.py`
**Status:** FILED and verified from fresh fetch. No merge, no live deploy, no link to Shawn.

## Filed identity

| | Base (follow-up 18) | New (follow-up 19) |
|---|---|---|
| Branch | `hub/personal-sidebar-followup18-20261119` | `hub/personal-sidebar-followup19-20261119` |
| Tip | `f5ce113a45ab4168b3a8c498dec59428aacca3b1` | `22b78d3ddbde1a1099842aeed4cec007006f3bea` |
| Blob (`HUB/app/index.html`) | `f7d715ee0f3a9be2acd5ddf0b47ba7b4f69abca8` | `5669975a3fa02e194ea883fb3cac38c85c7c380b` |
| Size | 7,188,444 B | 7,188,454 B (+10 B, +0 lines: 14,776 → 14,776) |
| sha256 | `474e5edd870c8016044f3827b39995729e395801cee7257aca08716eed005156` | `df15217370dc0d55265ee109ff64db1cda9b6701294b502b368582915c0284ec` |
| Commit message | — | "Hub follow-up 19: ADD composer landings send #home/post and #home/naya (Personal fix-5 route, Shawn 2026-11-19)" |

**Staged link:** https://naya-proof-host.nayapower.workers.dev/?file=HUB%2Fapp%2Findex.html&ref=hub%2Fpersonal-sidebar-followup19-20261119&cb=5669975a3fa02e194ea883fb3cac38c85c7c380b

**Verification of the filing (fresh fetch, after the PUT):** branch ref GET → tip is the PUT commit; blob-API GET → size 7,188,454 and sha256 `df152173…` match the filed bytes, byte-identical; staged-link GET (with `cb=`) → 7,188,454 bytes, sha256 matches. All three agree.

**Base verification (before any edit):** blob-API GET → size 7,188,444, sha256 `474e5edd…` — matches the coordinator's value. New branch confirmed absent (404) before creation.

## The route — verified from the FILED Personal bytes before writing any href

The brief said: do not invent a route; if no composer route exists, STOP. The route is real, and the two entry points need **different** routes. Evidence, from the filed Personal fix-5 file (`TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`, blob `dedf0b19057b4396572d8b1963352f0744c32439`, 10,453,371 B, sha256 `8585244daa53fd8b7ad00fe5da0c4ee79ec02c3c4a146c55b9b64140936752b9` — full sha resolved from the fix-5 commit tree `04715a7f8fc7dbd885b05401c1fb6b1839aa7811`, since the brief carried only the abbreviated `dedf0b19`):

- **Boot, lines 27215–27237:** `var hash=(location.hash||'').replace('#',''); var hashParts=hash.split('/'); var hashView=hashParts[0]; var hashSec=hashParts[1]||'';` then `if (VIEWS.indexOf(hashView)>=0 && hashView!==bootView) showView(hashView, true);`
- **Line 27231 (the route):** `if (hashView==='home' && (hashSec==='composer' || hashSec==='post' || hashSec==='naya' || hashSec==='smart')) {`
- **Line 27232 (the kind mapping):** `var kind = (hashSec==='post' || hashSec==='naya' || hashSec==='smart') ? hashSec : 'naya';`
- **Line 27233 (the open):** retry loop (20 × 250 ms) calls `window.fcOpenCreator(kind)` — the composer is the `#fcCreator` overlay.
- **Comment, lines 27219–27229 (FRAME-FIX4 F1), names this round's job verbatim:** "Only a section suffix acts: '#home/composer' (or '#home/post' / '#home/naya' / '#home/smart') opens the composer… The Hub-side half (sending the suffix) is still owed; until it lands, no arrival can trigger the composer."
- **Personal's own plus menu, line 12865:** `[['Make a post', '#8e24aa', 'post'], ['Naya note', '#07925f', 'naya'], ['Smart note', '#8e24aa', 'smart']]` — each label maps to its own kind. The composer defaults to Naya note (f17's note), and bare `#home/composer` maps to kind `'naya'` — so sending `#home/composer` for **both** items would open Make-a-post in the WRONG mode. Each entry point gets its own route.

## What was fixed (2 edits, Buffer-level, nothing else moves)

| Edit | Line | Old | New |
|---|---|---|---|
| E1 | 14449 | `data-hub-plus="post" data-hub-href="https://nayanet.app/personal#home"` | `data-hub-plus="post" data-hub-href="https://nayanet.app/personal#home/post"` |
| E2 | 14451 | `data-hub-plus="naya" data-hub-href="https://nayanet.app/personal#home"` | `data-hub-plus="naya" data-hub-href="https://nayanet.app/personal#home/naya"` |

- Edit is Buffer-level (`indexOf` + `Buffer.concat` on the exact anchor, asserted exactly-once each) — no string round-trip of the 7.1 MB file, so no byte-loss risk of the kind that once dropped 35,444 B from the Personal file.
- Diff: **only lines 14449 and 14451 differ** between base and fixed (line-by-line comparison, 14,776 lines). Size delta exactly **+10 B** (`/post` +5, `/naya` +5). Line count unchanged.
- Do-not-touch counts all delta 0: `#about` 1, `openRightRail` 12, `pcColorFor17(` 3, `hub-msg-panel` 5, `fetchNoteBySn` 2, `NayaFetchSoloNote` 2, Smart-note composer 1, f18/f17 markers kept, `nayanet.live` 0, seed byte-identical, digit-5 deep teal `#0e7490` count 3. Bare `#home"` hrefs 2 → 0. All 36 inline script blocks parse.

## Execution proof — the REAL path, both halves, from the filed bytes

This round executes the real code at both ends of the path, not a stub of an extracted function alone (the f16/f17 lesson). Two harnesses in `edit19.cjs`, both passing:

**Execution 1 — the Hub half (real `NayaHubStagedHref` / `NayaHubStagedFile` / `NayaHubGoStaged`, brace-matched from the FIXED bytes, run under a staged location):**

| Input href | Real staged output |
|---|---|
| `https://nayanet.app/personal#home/post` | `https://naya-proof-host.nayapower.workers.dev/?file=PERSONAL/index-master-20261105.html&ref=hub/personal-sidebar-followup19-20261119#home/post` |
| `https://nayanet.app/personal#home/naya` | `…?file=PERSONAL/index-master-20261105.html&ref=hub/personal-sidebar-followup19-20261119#home/naya` |
| `…/personal#home` (old) | `…#home` (suffix preserved; no composer) |
| `…/personal#about` | `…#about` (unchanged) |
| `…/rooms/mail` → `#/hub/mail`; `…/rooms/spaces` → `#/hub/spaces` (unchanged) |

`NayaHubGoStaged('…#home/post')` navigates to the staged URL ending `#home/post`; same for `#home/naya`. The `/post` and `/naya` suffixes survive staging verbatim (`u.hash` is carried whole into `NayaHubStagedFile`).

Harness note (named, not hidden): a bare `vm.createContext` has no WHATWG `URL`/`URLSearchParams` globals — the first run failed because `NayaHubStagedFile`'s `try/catch` swallowed the `ReferenceError` and returned null. The fix was harness-side only (inject the outer realm's `URL`/`URLSearchParams` so the environment matches a browser); the filed code was never touched for this.

**Execution 2 — the Personal half (real boot hash block, lines 27211–27238, brace-matched from the FILED Personal bytes, run with `location.hash` set, real `VIEWS` array, `showView`/`fcOpenCreator` recorded, timers pumped):**

| Arrival hash | `fcOpenCreator` called with | `showView` | Scroll |
|---|---|---|---|
| `#home/post` | `'post'` | — | — |
| `#home/naya` | `'naya'` | — | — |
| `#home/composer` | `'naya'` (bare composer defaults to naya — the reason post gets its own route) | — | — |
| `#home/smart` | `'smart'` | — | — |
| `#home` (the OLD href) | **nothing** — the old href could never open the composer | — | — |
| `#about` | — | `'about'` | `#about` scrolled into view |

Retry path also proven: with `fcOpenCreator` missing at first and appearing on the 2nd tick, `#home/post` still opens with kind `'post'`.

## THE STAGING GAP — stated plainly, not faked

The proof host serves Personal at the Hub's ref as `PERSONAL/index-master-20261105.html` from the f19 branch tree — blob `3359a4eaac8f388a41b397c9ec50f821aa4b0681`, **1,161,523 B**, sha256 `3046a719…`. That copy **predates the composer route**: `"home/composer"` count **0**, `"composer"` count 11, and its `VIEWS` list has no `'myworld'`. Its boot strips the fragment and only handles bare view hashes. **Therefore a real tap on the STAGED Hub CANNOT open the composer** — the tap lands on the staged Personal URL with `#home/post` / `#home/naya` in the arrival hash, and the old Personal boot ignores the suffix. That is a staging gap, not a wrong href: the hrefs are proven correct against the filed fix-5 Personal bytes (Execution 2 above), and the composer opens only once the filed fix-5 Personal (`personal-complete.html`) is what a tap actually lands on — i.e. after the Personal re-mirror rides its later round. **Do not claim a staged tap proof of the composer opening; the eye must verify the composer against the filed fix-5 Personal, or after the re-mirror.** The staged tap CAN prove (and this round proves by execution + live-DOM read, below) that the tap navigates with the right suffix.

## Real render proof — VM Playwright Firefox, width 1920 (what passed, what is environment-blocked)

Browsers flap in this VM. Sequence this round: both alive at 10:58 UTC → both dead (Firefox SIGSEGV, Chromium TargetClosedError) 11:00–11:08 → **Firefox alive again with `TMPDIR` under `~/workspace/`** (the `/tmp` EPERM flake was killing Playwright's profile creation; Chromium stayed dead throughout). All render proof below is Firefox, width **1920** (heights 1080 and 1400 — see the geometry finding). Console captured throughout (101 lines); **no `[hub-msg-panel] person content failed:` warning on any tap**.

**PASSED by real render (Firefox 1920, `proof/1920/` + `proof2/1920/`):**
- Hub loads ("Smart Feed — NayaNET", 13 rail cards); rail order on screen shawn 97, wrena 95, sophia 94, vera 93, zoe 92, thora 91, iris 91… (screenshot `proof2/1920/01-hub.png` — read as a reader: left nav, hero, live feed card "Write for the Stranger, Sign It Official", right rail in order).
- Vera orb → Profile (Vera, 93%, VERIFY, Reach row, mail room hidden). Vera (i) → About Vera (same bio, no Reach row). Vera DM → real DM ("Direct message with Vera.", "No messages with Vera yet.", `Message Vera…`, `Send · runtime required`, mail room hidden). Vera Mail → `Mail to Vera`, To: Vera, Subject + Body fields, `Send · runtime required`, mail room below (re-proven with fixed checks: Body placeholder is `Write to Vera… `, `bodyEl.style.display` is `''` = shown). Shawn DM → `DM — Shawn`, same surface. Shawn orb → `Shawn — Profile` (97%).
- ECOSYSTEM → the "Your Worlds & NAYANET" rail (My Worlds highlighted). ADD > Home → `#/hub/feed`. WORLDS → `#/hub/spaces`. Solo note `#/smart-notes/sn4202` opens (Back-to-Hub present).
- **The two new hrefs ARE in the live DOM:** the CREATE menu item for Naya note resolved in the live page carrying `data-hub-href="https://nayanet.app/personal#home/naya"`, and Make a post `…#home/post` (probe19b/probe19c reads). A JS-dispatched click on the ADD button opens the CREATE menu (`hidden=false`) — the real delegated handler runs.
- **Naya avatar image — staged-only vs real, adjudicated in writing:** on the Mail page, the inline data-URI avatar renders (192 px, `ok: true`); the two `https://nayanet.app/icons/naya-guide.jpg` images FAIL (`naturalWidth: 0`, console: "A resource is blocked by OpaqueResponseBlocking" for that URL). The failing src is the **live** domain, not a staged path — so it is not a staged-path miss; it is the live asset failing to load in this Firefox render (ORB/CORS). Per the brief I do **not** chase it and do **not** rebuild the avatar; the eye to confirm on its own render.

**NOT proven by pointer tap in this VM — the geometry finding (environment, not the href):**
- In this VM Firefox render the bottom bar never builds its live form: `#nsbBottom` is **false** even 14 s after load (the Smart Bar script's live bar is absent; only the static fallback `notif-row` bar exists). The fallback ADD button sits at document y≈1104–1187 at viewport 1080 — **24 px below the fold** — and at y≈1424–1507 at viewport 1400 (it tracks viewport-height + 24). Mouse-wheel scrolling moves the document (`scrollY` 0 → 324 → 924) but the button's rect **never moves** (1104..1187 constant): it is viewport-anchored below the fold, so no scroll can bring it into view, and Playwright pointer clicks time out ("element is outside of the viewport"). The f18 eye tapped the bottom bar fine in the cloud browser, where the live bar builds — so this is a VM-Firefox render difference, not a Hub-file defect, and not something this round's two-href change could cause (the bar's position is untouched by this round; the same geometry holds on the f18 base bytes).
- Consequence: **ADD > Make a post and ADD > Naya note were NOT proven by pointer tap in this VM.** What IS proven: the hrefs in the live DOM, the menu opening via the real handler, the staged-routing execution, and the Personal boot execution. The pointer-tap leg (1920 AND phone 390) is owed to the eye — the cloud browser at ~1920 for desktop, and a real phone / VM browsers alive for 390. The 390 leg was not attempted (same below-fold geometry applies; no separate 390 run was made).
- Probe artifacts corrected along the way (named, not hidden): the first probe's `text=ADD` matched a Smart Note "＋ Add" button behind an install overlay, and `text=CONNECT`/`text=MAIL` matched sidebar labels ("Personal Connections"/"Personal Mail"), not the bottom bar — those three FAILs were selector errors, fixed with `[data-notif]` selectors. The first "Vera Mail" FAIL was a check error (placeholder text is not in `innerText`; `bodyDisplay` read as computed `'block'` instead of `style.display ''`). The first "feed" FAIL was timing (innerText measured 1,146 chars while the feed was still settling; the screenshot shows the live feed card). The first "rail search" FAIL used the wrong search box (chassis search, not `#pcRailSearch`) and counted the panel's leftover `data-pc-alias` wrapper; scoped to `.pc-card[data-pc-alias]` the search was re-proven in probe19b (ruth → only ruth; cleared → all 13). The "About Us" FAIL was an over-strict check: the tap DID land on the staged Personal page — the old Personal boot strips `#about` from the URL via `replaceState`, so the final URL carries no hash. The feed's live reads are CORS-blocked in VM Firefox (repeated Supabase `Cross-Origin Request Blocked` + `[one-flow] live read failed`); the baked feed still renders (screenshot). None of these is a Hub regression — each is a probe error or a VM-environment limit, and each is named here rather than silently dropped.

## Laws §11 check — in writing

**Activation (done before any edit):** read `THE-NAYA-DESIGN-LAWS.md` in full first, then the heads of `THE-PLAYBOOK.md`, `DESIGN-INTELLIGENCE-REPORT.md`, `THE-ANATOMY-OF-A-SMART-APP-PAGE.md` with `THE-HEART-OF-THE-MACHINE.md`, and `~/workspace/team-nitro/AGENTS.md` (Checklist Law, Whole-Page Rule, Continuous Cycle Law, Live Sequence, Scorecard Law).

**The real checker, run on the staged bytes** (`curl <staged> | python3 check-design-laws.py /dev/stdin`):
- Base (staged f18): **18 violation(s), 57 warning(s)**.
- Fixed (staged f19): **18 violation(s), 57 warning(s)**.
- **Delta 0 — FAIL sets identical and WARN sets identical** (compared in memory with line numbers normalized, after a first `/tmp`-file comparison came back vacuously empty because `sort` EPERM'd — that void comparison was discarded and redone properly). The 18 FAILs are the same pre-existing ones (17 SIZE, 1 GRAY at line 4404, all outside this round's window). No new FAIL, no new WARN. The in-memory replication agrees (19 FAIL / 22 WARN both sides, delta 0).
- **This round's change adds no text, no font-size, no color** — two href values only. Laws delta must be 0, and it is 0.
- **§11 design-check answers:** Could I pick this up? The change touches no object — no new board, button, icon, or text exists to lift, light, or hover. Light top-left, board black inside, own-color light outside: unchanged, inherited from the untouched page. No glow inside, no gray text, no text under 17px added (nothing added). No two same colors together (nothing added). Nothing flat or dead added. Icons readable (untouched). **Reference objects:** none needed — nothing visual changed; the check is the href values themselves, proven by execution against the Personal file's own route table. Read as a reader: the Hub page reads exactly as it did in followup18 (screenshot `proof2/1920/01-hub.png` — hero, feed card, rail in order, no visual delta); the only change is where two menu items lead.
- **§11 verdict:** the work follows the laws; the checker delta is 0; nothing new to fix under the laws. The pre-existing 18 FAILs are out of this round's scope and are named here, not hidden.

## Self-check 1 — the verification suite inside the edit script (run on the filed bytes)

- Every edit anchor asserted exactly-once before replacement; 2/2 applied, Buffer-level.
- Diff: only lines 14449 and 14451 differ; size delta exactly +10 B; line count unchanged.
- Do-not-touch deltas: all asserted and passing (see above).
- JS parse: all 36 inline `<script>` blocks compile (`vm.Script`).
- Laws replication: FAIL/WARN sets identical, delta 0; real checker on staged bytes: 18/57 both sides, FAIL/WARN sets identical.
- **Execution proofs on code extracted from the filed bytes (not on copies):** real `NayaHubStagedHref`/`NayaHubStagedFile`/`NayaHubGoStaged` → staged URLs ending `#home/post` / `#home/naya`; real Personal boot block → `fcOpenCreator('post')` / `('naya')` / `('naya'` for bare composer) / nothing for bare `#home` / about-scroll for `#about`; retry path with late `fcOpenCreator` → kind `'post'`.

## Self-check 2 — fresh blob-API re-fetch (after filing)

Branch ref GET → tip `22b78d3d…` is the PUT commit. Blob GET `5669975a…` → size 7,188,454, sha256 `df152173…`, decoded bytes byte-identical to the filed buffer. The filed bytes are the verified bytes.

## Self-check 3 — staged link + real checker (after filing)

Staged GET with `cb=` → 7,188,454 bytes, sha256 `df152173…` — matches the filed bytes. Real `check-design-laws.py` on the staged bytes → 18 FAIL / 57 WARN, FAIL/WARN sets identical to base. The staged link serves exactly what was filed, and the laws check on the served bytes is clean of new violations.

## The seven Self-Check questions (SELF-EVALUATION-CHECKLIST.md)

1. **Most intelligent?** Yes. The route was verified from the Personal file's own bytes before any href was written — and the verification found the subtlety that decides the fix: bare `#home/composer` forces naya mode, so Make-a-post needs `#home/post`. The edit is two href values at Buffer level, the smallest change that fixes the cause.
2. **Most logical?** Yes. Each value follows from the Personal boot's own kind mapping and its own plus menu (post→'post', naya→'naya'); the staged-routing functions provably preserve the suffix; the old `#home` is proven by execution to open nothing.
3. **Most sensible?** Yes. Nothing was redesigned, rebuilt, or removed beyond the brief: the seed, panels, DM, mail composer, ECOSYSTEM, bottom bar, feed loader, solo-note flow, and every live link are untouched; the only behaviour change is where two menu items lead.
4. **Full scope?** Yes — as far as this VM allows. The scope checked was the page as Shawn sees it: the two ADD landings (by execution + live DOM), the f18 regression set by real render at 1920, the laws, the staging gap. The two things I could not close in this VM — the pointer tap on ADD and the 390 leg — are named as owed to the eye, not claimed.
5. **Consequences?** First order: on the filed Personal, ADD > Make a post opens the composer in post mode and ADD > Naya note in naya mode, instead of landing on the profile top. Second order: on staged, the composer cannot open until the Personal re-mirror lands — the eye must not judge this round by a staged tap alone. Who it touches: the eye's re-walk (it can now verify the composer route against the filed Personal) and the Personal re-mirror round (which inherits a Hub that already sends the suffix).
6. **Pros and cons?** Pros: the route is proven from the Personal file's own code, both halves executed from filed bytes; the edit is 10 bytes, nothing else moves; laws delta 0; filing verified three ways. Cons (honest): no pointer-tap proof in this VM (bar below the fold, live bar never builds in VM Firefox); the staged tap cannot show the composer (staged Personal predates the route); the 390 leg is unattempted; the DM still cannot send (queued messenger-fix round).
7. **Best possible choice?** Yes, against the ultimate objective — the two ADD buttons now send the composer route the Personal file itself defines, with nothing else moved and live untouched. The alternatives scored worse: sending `#home/composer` for both (wrong mode for Make a post), guessing a hash (forbidden by the brief), or claiming a staged tap proof (impossible — the staged Personal predates the route; claiming it would repeat follow-up 16's failure).

**All seven YES → GO.** Filed with receipts above.

## What the eye must check (exact taps — the pointer-tap leg is yours, not the VM's)

1. **ADD > Make a post** (desktop 1920, then phone 390): lands on the Personal page with the composer open in **post** mode. **Eye, note honestly:** on the STAGED link this will NOT show the composer — the staged Personal (blob `3359a4ea`, 1.16 MB) predates the route. Verify the composer against the filed fix-5 Personal (`personal-complete.html`, blob `dedf0b19…`) or after the Personal re-mirror. What the staged tap CAN show: the arrival URL carries `#home/post`.
2. **ADD > Naya note** (1920 + 390): same, composer open in **naya** mode; staged arrival URL carries `#home/naya`.
3. **Do-not-regress spot checks (1920 + 390):** Vera orb → Profile (93%, teal); Vera (i) → About (no contact buttons); Vera DM → real DM, no mail room; Vera Mail → To/Subject/Body + room below; Shawn DM/Profile the same; CONNECT > Message → generic Smart Messenger; console shows no `[hub-msg-panel] person content failed:` warning; rail search `ruth` → only ruth; Activity view 13; feed loads; solo note sn4202 opens; About Us → staged Personal About view; Smart Worlds → `#/hub/spaces`; bottom bar ADD Home → `#/hub/feed`, MAIL → `#/hub/mail`, WORLDS → `#/hub/spaces`, ECOSYSTEM → "Your Worlds & NayaNET" rail.
4. **Phone 390:** repeat taps 1–3 at 390 width and name the actual width of every check (still owed from follow-up 16 — the VM could not reach the bottom bar by pointer at any height this round).
5. **Naya avatar:** two `nayanet.app/icons/naya-guide.jpg` images fail in the VM Firefox render (ORB-blocked, `naturalWidth: 0`) while the inline avatar renders — confirm on your own render whether the guide image loads; do not chase it in this round.

## What is still owed

- **Pointer-tap proof of ADD > Make a post / Naya note (1920 + 390):** owed to the eye (cloud browser ~1920; real phone / VM browsers alive for 390). The VM Firefox render this round could not pointer-tap the bottom bar at any height (live bar never builds; fallback bar viewport-anchored 24 px below the fold).
- **Personal re-mirror (later round, not this one):** until the filed fix-5 Personal is what a tap lands on, no tap — staged or live — can show the composer opening from these hrefs. The Hub half is done; the Personal half is the mirror.
- **Runtime send bridge (messenger-fix round's piece):** a DM/mail draft can be typed, but `Send · runtime required` is disabled until the governed messaging runtime exposes sending. Do not call the DM "working" until a message can actually send.
- **Life with Naya deck "Back to the NayaNET Hub" link** — lives in the deck file, not this one; its own parallel round.
- **Full-path proof in the VM (real boot + real click dispatch through the rail's delegated handlers):** needs a DOM runner that works in this window — VM browsers flap (Firefox SIGSEGV; Chromium TargetClosedError; alive only with `TMPDIR` under `~/workspace/` for Firefox), jsdom/linkedom un-installable (npm EPERM). The eye's render remains the final gate.
- **18 pre-existing law violations** (17 size, 1 gray) — out of this round's scope, named here.
- **No merge, no live deploy, no link to Shawn** — as briefed. Next step is the checker, then the captain's eye.

## Scorecard (honest)

**Self-score: 8/10 as filed** — the route is proven from the Personal file's own bytes on both halves, the edit is 10 bytes with nothing else moved, laws delta 0, filing verified three ways, and the f18 regression set re-proven by real render at 1920; it is not a 10 because the pointer tap on ADD and the 390 leg could not run in this VM, the staged tap cannot show the composer (staged Personal predates the route), and the DM still cannot send.

**Ten things loved:** (1) the Personal file's own comment names this round's job verbatim; (2) the kind mapping caught the `#home/composer`-for-both trap before any href was written; (3) the old `#home` is proven by execution to open nothing — the bug is not asserted, it is run; (4) the edit is 10 bytes, Buffer-level, with a two-line diff; (5) the staged-routing functions provably preserve the suffix; (6) the retry path (late `fcOpenCreator`) is proven, not assumed; (7) the rail/DM/Mail regression re-proven by real render, not by bytes; (8) laws delta 0 on the real checker with sets compared properly; (9) the staging gap is named plainly instead of a faked tap proof; (10) the whole round ran in memory despite the EPERM flake, and the browser flap was worked around via workspace `TMPDIR`.

**Ten things not loved:** (1) no pointer-tap proof of the round's own item in this VM; (2) the 390 leg is unattempted again; (3) the staged Personal predates the route, so the staged link cannot demonstrate the fix; (4) the DM cannot send yet; (5) the live Smart Bar never builds in VM Firefox, leaving only the below-fold fallback bar; (6) the file still carries 18 pre-existing law violations; (7) the first probe wasted a pass on wrong selectors (text=ADD/CONNECT/MAIL); (8) a void laws comparison (empty `/tmp` files) nearly shipped as evidence; (9) the feed's live reads are CORS-blocked in VM Firefox; (10) the naya-guide.jpg avatar fails in this render and its verdict still rests with the eye.

**Ten things to make it ten times better:** (1) land the Personal re-mirror so a tap can actually show the composer; (2) land the runtime send bridge so a DM actually sends; (3) restore a working DOM runner in the VM (browsers + jsdom) so makers prove by real boot and real pointer tap; (4) fix the VM Firefox scroll/snap geometry that hides the fallback bar below the fold, or make the eye's cloud render the standing proof path; (5) clear the 18 pre-existing law violations; (6) give the eye a 390 render every round; (7) add a scope/order lint to the checker (a `var` initializer after a `return` fails the build); (8) make staged Personal track the filed Personal so staging gaps stop recurring; (9) give the probe a selector registry (data-notif, #pcRailSearch) so no round re-learns the wrong-text trap; (10) prove every future "opens" claim by executing the real handler path end to end, never by grepping for a title.
