# Hub Follow-up 19 — Captain's Eye Report

**Round:** Hub personal-sidebar followup19 (captain's eye)
**Date:** 2026-11-20 ~11:42–12:1x UTC (04:42–05:1x MST)
**Branch:** `hub/personal-sidebar-followup19-20261119`, tip `87e5ad94be3346024638c0f50bb40bbd5f616e24`
**Hub file commit:** `22b78d3ddbde1a1099842aeed4cec007006f3bea`, blob `5669975a3fa02e194ea883fb3cac38c85c7c380b`, 7,188,454 B, sha256 `df15217370dc0d55265ee109ff64db1cda9b6701294b502b368582915c0284ec`
**Base:** followup18 blob `f7d715ee0f3a9be2acd5ddf0b47ba7b4f69abca8`, 7,188,444 B
**Staged:** https://naya-proof-host.nayapower.workers.dev/?file=HUB%2Fapp%2Findex.html&ref=hub%2Fpersonal-sidebar-followup19-20261119&cb=5669975a3fa02e194ea883fb3cac38c85c7c380b
**Activation read before any verification:** THE-NAYA-DESIGN-LAWS.md (full) · THE-PLAYBOOK.md (full) · DESIGN-INTELLIGENCE-REPORT.md (full) · THE-ULTIMATE-ORIENTATION.md (full) · THE-ARMY-TRAINING.md (full) · THE-ANATOMY-OF-A-SMART-APP-PAGE.md (full) · ~/workspace/team-nitro/AGENTS.md (full).
**Status:** COMPLETE — byte leg, adjudication, separating test, 390 + 1920 render legs all done. Verdict below.

## VERDICT: PASS

The two-line fix is proven from the filed bytes, the ADD taps are proven by real pointer tap at 390 and 1920 (VM) and ~1920 (cloud browser), the composer is proven to open in the right mode for each route (separating test 3/3), and the followup18 regression holds by my own pointer taps at 1920. One phone-width re-confirmation remains open (the 390 rail-orb/info pointer taps — VM scroll-into-view hang, named in §4, not a page failure). No merge, no live deploy — the captain decides the next step.

## 1. Byte leg — proven cold from fresh blob-API fetches

- Base blob `f7d715ee…`: 7,188,444 B, sha256 `474e5edd870c8016044f3827b39995729e395801cee7257aca08716eed005156` — matches maker + checker.
- Fixed blob `5669975a…`: 7,188,454 B (+10), sha256 `df15217370dc0d55265ee109ff64db1cda9b6701294b502b368582915c0284ec` — matches maker + checker.
- Staged GET (curl, browser UA): 7,188,454 B, sha256 `df152173…` — **byte-identical to the filed blob**. The staged link serves exactly what was filed.
- Diff replay (line-by-line, 14,776 lines each): **only lines 14449 and 14451 differ.**
  - L14449: `data-hub-plus="post" data-hub-href="https://nayanet.app/personal#home"` → `…#home/post`
  - L14451: `data-hub-plus="naya" data-hub-href="https://nayanet.app/personal#home"` → `…#home/naya`
  - Size delta exactly +10 B (`/post` +5, `/naya` +5). Line count unchanged.
- Do-not-touch counts (eye's own count): `nayanet.app/personal` hrefs 10 = 10; bare `#home"` hrefs 2 → 0; `nayanet.live` 0 = 0; `openRightRail` 12 = 12; `hub-msg-panel` 5 = 5; `#0e7490` 28 = 28.
- Personal fix-5 filed blob re-fetched cold: `dedf0b19057b4396572d8b1963352f0744c32439`, 10,453,371 B, sha256 `8585244daa53fd8b7ad00fe5da0c4ee79ec02c3c4a146c55b9b64140936752b9` — matches maker + checker.
- Personal fix-5 boot block read from the filed bytes (lines 27211–27238): L27231 route `if (hashView==='home' && (hashSec==='composer' || hashSec==='post' || hashSec==='naya' || hashSec==='smart'))`; L27232 kind mapping (`post`/`naya`/`smart` else `'naya'`); L27233 retry loop (20 × 250 ms) calling `window.fcOpenCreator(kind)`; L27219–27229 FRAME-FIX4 comment names this round's job verbatim ("The Hub-side half (sending the suffix) is still owed"). Plus menu L12865: post→`'post'`, naya→`'naya'`, smart→`'smart'`. `fcOpenCreator` occurs 20×.
- **The two routes are the right two, confirmed independently from the Personal bytes:** bare `#home/composer` forces kind `'naya'`, so sending it for Make a post would open the composer in the wrong mode. The maker and checker both got this right; I verified it from the bytes, not their word.

## 2. Adjudication — where the hash is lost (the cloud-browser leg vs the checker)

**The conflict.** The checker executed the Hub routing from the real bytes in vm and reported "staged URLs end exactly `#home/post` / `#home/naya`". The captain's cloud-browser leg (real taps, 11:42–11:44Z) reported both taps landed on `…?file=PERSONAL/index-master-20261105.html&ref=hub/personal-sidebar-followup19-20261119` with **NO hash at all**, no composer, and the two landings indistinguishable. That goes beyond the known staging gap (which predicted: arrival hash present, composer does not open). I traced the real code from the filed bytes; the code decides.

**The trace (filed fixed bytes, eye's own read).**
- Tap handler, L7238–7262: for `data-hub-plus="post"`/`"naya"` (not `message`/`mail`/`world`/`home`, not `data-hub-composer="smart-note"`), it reads `data-hub-href` and calls `window.NayaHubGoStaged(href)`; if that function is absent it falls back to `location.href = href`. The handler does NOT build a destination itself — it navigates to exactly the href on lines 14449/14451.
- `NayaHubGoStaged`, L11925–11935: `staged = NayaHubStagedHref(href)`; if staged starts with `#` it goes through the router, else `location.href = staged`.
- `NayaHubStagedHref`, L11901–11923: parses `https://nayanet.app/personal#home/post` with `new URL`; `hash = u.hash` = `#home/post`; path `/personal` → `NayaHubStagedFile('PERSONAL/index-master-20261105.html', hash)`.
- `NayaHubStagedFile`, L11887–11899: returns `location.origin + location.pathname + '?file=' + file + '&ref=' + ref + (hash || '')` — i.e. `…?file=PERSONAL/index-master-20261105.html&ref=hub/personal-sidebar-followup19-20261119#home/post`.

**Conclusion 1: the Hub is right. The checker was right about the URL the Hub navigates to; the Hub code provably sends `#home/post` / `#home/naya`. Adjudication (b) — the handler building a hash-less destination — is REFUTED.**

**Where the hash actually goes — the destination strips it.** The old staged Personal's own boot block (read from the staged bytes, 1,161,523 B, sha256 `3046a719…`, `home/composer` 0×, `fcOpenCreator` 0×) contains, at line 10415–10416, the "Back (wave #6)" boot:
```
var hash=(location.hash||'').replace('#','');
try { history.replaceState({osView:bootView}, '', location.pathname+location.search); } catch(e){}
if (VIEWS.indexOf(hash)>=0 && hash!==bootView) showView(hash, true);
```
It runs at boot, reads the hash, then **unconditionally strips the fragment from the address bar** (`location.pathname+location.search` carries no hash), and only acts if the hash is a bare view name in VIEWS — `'home/post'` is not one, so nothing happens. The browser's "still no hash after settling" is exactly this: the fragment arrived, the destination read it, stripped it, and ignored it. The maker's own About Us probe observed the same behavior for `#about` (final URL carried no hash). The fix-5 Personal boot does the same strip (L27218) — but it reads the hash FIRST and opens the composer from the saved variables, so on fix-5 the composer opens and the URL still shows no hash afterward. **"No hash in the URL after load" is therefore NOT evidence the Hub failed to send it, on either Personal.**

**Conclusion 2: the loss is downstream of the Hub — in the served old Personal's boot block, not in the proof-host mapping and not in the Hub handler.** The landed URL matches `NayaHubStagedFile`'s output exactly, minus the fragment the destination stripped. No redirect evidence: the landed URL carries no `&cb=` and matches the code-built URL. The staging gap stands, refined: on staged, the tap lands on the old Personal, which strips and ignores the suffix; the composer cannot open until the filed fix-5 Personal is what a tap lands on (Personal re-mirror).

**What remains to be proven by tap:** the composer opening in the right mode from the fragment — the separating test (staged fix-5 Personal, direct fresh loads with `#home/post` and `#home/naya` appended). **DONE — 3/3 PASS, see §4b.** The fragment survives the proof host to a boot that reads it, and the composer opens in the right mode for each route. The Hub→Personal chain is proven end to end except for the re-mirror (staged Hub taps land on the OLD Personal, which strips and ignores the suffix — that is the re-mirror's job, not this round's).

## 3. Laws — real checker, delta 0 (proven)

Ran the real `check-design-laws.py` on the eye's own saved base vs fixed bytes:
- Base: **18 violation(s), 57 warning(s)**. Fixed: **18 violation(s), 57 warning(s)**.
- Filename-normalized sorted diff of the full outputs: **empty — delta 0, FAIL sets identical and WARN sets identical** (17 SIZE + 1 GRAY at line 4404, all pre-existing, all outside this round's window).
- JS parse: **36/36 inline `<script>` blocks parse clean in both files**, count unchanged.
- This round adds no text, no font size, no color — two href values only. Laws delta must be 0, and it is 0.

## 4. Render leg — 390 (VM Firefox, real taps)

**Browser:** VM Firefox (alive this window, workspace TMPDIR), 390×844. 9/21 probe steps passed; the 12 failures are dissected below — most are the known VM Firefox scroll-into-view hang (a probe limitation, not page evidence), one was my own probe bug (corrected and re-proven), and the rest are named honestly.

**PASSED by real render at 390:**
- Hub loads ("Smart Feed — NayaNET"); install modal dismissed via "Not now".
- Rail order exact, 13: shawn 97, wrena 95, sophia 94, vera 93, zoe 92, thora 91, iris 91, astraea 90, emesa 89, terra 88, ruth 88, mira 87, aurelia 86.
- Feed renders (9,206 chars).
- Bottom-bar geometry recorded: live Smart Bar never builds (`#nsbBottom` false); fallback ADD rect [47, 865, 46, 48] — 69 px below the 844 fold; no "Show the bottom bar" button visible at 390.
- Activity view via router: 13 cards, hash `#/hub/feed-activity`.
- Smart Worlds via router: `#/hub/spaces`.
- Rail search `ruth` → only ruth (pointer fill).
- Console: zero `[hub-msg-panel]` warnings (7 errors total, all CORS `feed-live.json` + 2 page errors — see below).

**NOT closed by pointer at 390 — the Firefox scroll-into-view hang (probe limitation, code byte-identical to the f18 PASS):** Vera orb → Profile, Vera (i) → About, Vera DM, Vera Mail, Shawn orb, About Us — every one timed out in Playwright's actionability wait ("waiting for element to be visible") after the locator RESOLVED to the right element, even with `scrollIntoView({block:'center'})` first (final micro-probe: Vera (i) and Shawn orb both timed out; Vera orb likewise — no screenshot landed). This is the same hang the checker hit in Firefox (their Vera taps passed at 1920 with the same selectors). The elements exist and are the right ones; the VM Firefox will not scroll the 390 rail's cards into view to click. **What this is:** a VM probe limitation at phone width. **What it is not:** evidence of a regression — the same taps pass by my own pointer at 1920 (§5b), the maker passed them at 1920, and the f18 eye passed all four people by real tap in the cloud browser on code byte-identical to this round except the two hrefs. **The one remaining phone-width re-confirmation:** the 390 rail-orb/info pointer taps, owed to a real phone or the cloud browser at phone width. It does not block this verdict — the round's own item (the two ADD hrefs) IS proven at 390 by pointer tap (below), and the regression is proven at 1920 by my hand.
- **ADD taps at 390 — CLOSED by pointer in the retry:** clicking the corner control `#os-b3-hide` (aria-label "Show the bottom bar") recalls the bar, then ADD → CREATE menu → "Make a post" / "Naya note" by pointer tap. Both landed on `…?file=PERSONAL/index-master-20261105.html&ref=hub/personal-sidebar-followup19-20261119` (no hash — adjudicated in §2: the old staged Personal strips it). Screenshots `shots/390/30-addmenu-post.png`, `31-landing-post.png` (and naya equivalents).
- CONNECT > Message dispatch: FAIL in my first attempt — my probe bug, not the page: the `[data-hub-menu]` click handlers bind lazily on FIRST menu open (fixed.html L6368), and I dispatched without ever opening the menu, so no handler was bound. **Closed in the final retry (§5b)** — the menu that holds those items opens from the top-right hamburger `[data-hub-menu-btn]`, not from ADD.

**Avatar at 390:** zero `naya-guide.jpg` imgs in the DOM at 390 — the Hub at phone width does not render those images at all (census re-run at 1920, §5). Not a failure of this round; the f18 eye saw the guide image on desktop.

**Solo note sn4202 at 390:** not proven open — the load returned the Hub chrome text without the note body; consistent with the checker's finding (live Supabase read fails in this VM with `ERR_CERT_AUTHORITY_INVALID`, identical on base). The eye's cloud render is the standing proof path for live-read content; the f18 eye saw the note open.

**Console errors at 390 (named, not hidden):** 5× CORS `feed-live.json` (live feed reads blocked in VM Firefox — pre-existing environment), `PAGEERROR: handler is not a function`, 2× `PAGEERROR: can't access property "tone", note is undefined`. The `tone` page errors and the `handler` error also appear on the f18 base in this VM (feed render path) — they are pre-existing environment/render noise, not regressions from two hrefs; the feed still renders (9,206 chars) and the console carries zero `[hub-msg-panel]` warnings.

## 4b. The separating test — staged fix-5 Personal, fresh document loads (CORRECTED)

My first separating-test attempt was VOID: the two Personal URLs differ only by fragment, so the second `goto` was a same-document hash change — boot never re-ran, the composer stayed open in post mode from the first load, and my visibility check (`offsetParent !== null`) is false for `position:fixed` elements. I re-ran it correctly: each case navigates via `about:blank` first (a real fresh document load), mode read from `window.osNoteMode` + `.tg-mode.on` + `#fcTitleText`, visibility from `creator.hidden` + computed display + `body.fc-open`. **3/3 PASS:**

| Arrival | Composer | Mode | Evidence |
|---|---|---|---|
| `#home/post` | OPEN (display flex, `fc-open`) | **post** | `osNoteMode='post'`, active tab `post`, title "Make a post", hint post text, button "✎ Post it" |
| `#home/naya` | OPEN (display flex, `fc-open`) | **naya** | `osNoteMode='naya'`, active tab `naya`, title "Naya note", hint naya text, button "✦ Post my Naya note" |
| (no hash — control) | CLOSED (`hidden`, display none, no `fc-open`) | — (defaults to naya in static markup, composer closed) | — |

Screenshots `shots/390/10-sep-post.png` and `10-sep-naya.png` show it with my own eyes: post load — "Make a post" tab lit, "Post it" button; naya load — "Naya note" tab lit (green), "Post my Naya note" button. **The fragment survives the proof host to a boot that reads it, and each route opens the composer in its own right mode.** The hash is stripped from the URL afterward on both (the fix-5 boot's own `replaceState`, L27218) — which is why "no hash in the URL after load" is not evidence of failure.

**Observation (pre-existing Personal behavior, not this round's):** on the `#home/naya` fresh load, the "Install NayaNET" modal popped over the composer ("Install the app" / "Not now"). The composer stands open underneath; "Not now" dismisses it. A citizen arriving via ADD on a fresh load will see that modal first. Named, not failed — the modal is the Personal page's own install prompt, untouched by this round.

## 5. Render leg — 1920 (VM Firefox, real taps)

**Browser:** VM Firefox (alive this window, workspace TMPDIR), 1920×1080. First run 11/21; a focused retry (corrected selectors/sequencing) closes the five open items — results below.

**PASSED by real render at 1920:**
- Hub loads ("Smart Feed — NayaNET"); install modal: none visible on this load (it appears intermittently — "Not now" dismisses it when present).
- Rail order exact, 13 (same list as 390).
- Feed renders (12,268 chars).
- Bottom-bar geometry recorded: live Smart Bar never builds (`#nsbBottom` false); fallback ADD rect [654, 1104, 59, 82] — 24 px below the 1080 fold, identical to the checker's measurement. The "Show the bottom bar" control is `#os-b3-hide` (aria-label, text '▴' — which is why my first probe's text search missed it); the retry taps it by pointer.
- **Vera orb → Profile (pointer) PASS** — "Vera — Profile | × | V | Vera | 93% | VERIFY — truth. Nothing counts until I see it. | i | ✎✉♪▶" with the contact row.
- Activity view via router: 13 cards, `#/hub/feed-activity`.
- **About Us → staged Personal (pointer) PASS** — lands on `…?file=PERSONAL/index-master-20261105.html&ref=hub/personal-sidebar-followup19-20261119` (the old Personal strips `#about` from the URL via `replaceState` — the maker's note, confirmed from the staged bytes in §2).
- Smart Worlds via router: `#/hub/spaces`.
- Rail search `ruth` → only ruth (pointer fill).
- Console: zero `[hub-msg-panel]` warnings (9 errors total: CORS `feed-live.json` + `handler is not a function` + `fetchWall is not defined` + `tone` page errors — pre-existing environment/render noise, same family as on base; the feed still renders).
- **Solo note sn4202 OPENS WHOLE (my own eyes, screenshot `shots/1920/07-solo-sn4202.png`)** — "What is NayaNET, ultimately?" with the full anatomy boards (In a Nutshell, Child Note, Grandma Note), "← Back to Hub", dated "Friday, November 20, 2026 2:23 AM · 9 h ago", rail in order. My probe step marked it FAIL only because its text check looked for the literal id `sn4202` in the rendered text (the id is not rendered as text) — the screenshot proves it open. The checker's "error state" was their session's live-read failure; in my session the note renders whole. **Corrected to PASS.**

**NOT closed in the first 1920 run — retried with corrected sequencing (see retry results below):**
- ADD > Make a post / Naya note (pointer): same scroll-into-view timeout — ADD sits 24 px below the fold and Playwright will not scroll it into view. The cloud browser DID these taps at ~1920 (bar collapsed → "Show the bottom bar" → ADD → menu → tap → arrival URL recorded, §2). The retry taps `#os-b3-hide` by pointer first.
- Vera (i) → About: strict-mode violation — `[data-pc-info="vera"]` resolves to 2 elements (the rail's act buttons exist twice in the DOM, second copy inside panel/drawer markup — the checker's exact finding). Retry scopes to the visible rail card.
- Vera DM / Vera Mail: pointer timeouts on the orb re-tap — my `close_panel()` (Escape + class removal) did not actually close the Vera panel, leaving the orb covered. Retry uses a fresh load per tap.
- CONNECT > Message (dispatch): panel still showed Vera's profile — same stale-panel cause, plus my dispatch ran before the `[data-hub-menu]` handlers were bound (they bind lazily on first menu open, fixed.html L6368). Retry opens the menu by pointer first, then taps the messenger item by pointer.
- Avatar: zero `naya-guide.jpg` imgs on the Hub feed view (1 img total in the DOM). The checker found the two guide images on the Mail view, not the feed view. Retry censuses imgs with the mail panel open.

### 5b. Retry results — 1920 (focused, corrected) — ALL CLOSED

- **ADD > Make a post (pointer, via `#os-b3-hide`) PASS** — corner control recalls the bar, ADD opens the CREATE menu (`['home','post','smart','naya','message','mail','world']`), tap lands on the staged Personal URL. Screenshot `shots/1920/20-addmenu-post.png` (menu open, bar visible, "Good morning. Friday, November 20, 2026 11:58:37 AM" live). The ADD rect still measured [1104, 1187] after the corner-control click — the measurement and the screenshot disagree (the bar IS visible in the screenshot); the tap landing is what counts, and it landed.
- **ADD > Naya note (pointer, via `#os-b3-hide`) PASS** — same path, same landing URL.
- **Vera (i) → About, no contact buttons (pointer, scoped to the rail card) PASS** — "About Vera", panel buttons are messenger chrome (Close smart messenger, IMPORTANT, RESPOND, FOLLOW UP, DRAFTS, SENT) — no DM/Mail contact buttons.
- **Vera DM → real DM (pointer, fresh load) PASS** — "DM — Vera | Direct message with Vera. | No messages with Vera yet. | The conversation with Vera starts here — nothing is invented to fill it. | Send · runtime required", no mail room.
- **Vera Mail → To/Subject/Body (pointer, fresh load) PASS** — "Mail to Vera | To: Vera | Subject | Body | Send · runtime required | Communication intelligence | Meaning and context first. No fake mailbox, ever."
- **CONNECT > Message → Smart Messenger (pointer) PASS** — the three-state menu opens from the top-right hamburger `[data-hub-menu-btn]` (aria-label "Menu — sidebar, smart messenger, or neither"); menu `#hubMenuChoices` opens, handlers bind (`__hubMenuChoicesBound: true`); "Open smart messenger" tap → panel "Smart Messenger | × | Communication intelligence | Meaning and context first. No fake mailbox, ever. | The room separates what needs attention from noise…". Screenshots `shots/1920/33-choices-menu.png`, `34-messenger.png`. (My first two attempts targeted the wrong menu — ADD's CREATE menu — and a stale install overlay intercepted the hamburger click once; the passing run dismissed the overlay first and verified `bound: true` before tapping.)
- **Shawn orb → Profile 97% (pointer) PASS** — "Shawn — Profile | × | S | Shawn | 97% | Welcome to my world — post, message, make yourself at home. | i | ✎✉♪▶" (after `scrollIntoView`; screenshot `shots/1920/31-shawn.png`).
- **Avatar — CONFIRMED failing on my own render (pre-existing, not this round's, not a fail):** in the Ask Naya room, `https://nayanet.app/icons/naya-guide.jpg` loads with `naturalWidth: 0, complete: true` — the live-domain image fails in VM Firefox (ORB-blocked, same as the checker's finding). The inline data-URI avatar renders. The failing src is the live domain, not a staged path; the Hub file does not own it. Per the brief I do not chase it. A citizen on a real browser may or may not see the guide image — the eye notes it, does not fail the round on it.

## 6. §11 in writing

**Five gates.** (1) Is it right? Yes — two buttons now send the composer route the Personal file itself defines; nobody is misled, nothing lands on a dead end, and the staging gap is named honestly rather than faked. (2) Is it what they truly need? Yes — the brief's one item is the button-destination law applied to ADD, and the fix is the smallest change that does it (10 bytes). (3) Is it mine to do? Yes — an eye verifies; no merge, no live deploy, no message to the user, no money, no credentials, nothing destructive. (4) Is now the time? Yes — the Hub half was the one item the Personal fix-5 eye named as still owed; the Personal half is already filed; the re-mirror is a later round's job, not a reason to hold this one. (5) Can I prove it? Yes — every claim above carries its own evidence: fresh blob hashes, a two-line diff replay, a line-by-line trace of the tap handler and the staging functions, the destination's own `replaceState` strip read from its bytes, the corrected separating test 3/3 with mode read from `osNoteMode` + `.tg-mode.on` + title text, real pointer taps at 390 and 1920 with screenshots, the real laws checker with delta 0, and every gap named with what was tried.

**Design check (§11).** The change touches no object — no new board, button, icon, or text exists to lift, light, or hover. Light top-left, board black inside, own-color light outside: unchanged, inherited from the untouched page. No glow inside, no gray text, no text under 17px added (nothing added). No two same colors together (nothing added). Nothing flat or dead added. Icons readable (untouched). Reference objects: none needed — nothing visual changed; the check is the href values themselves, proven by execution against the Personal file's own route table and by real taps. Read as a reader: the Hub page reads exactly as it did in followup18 — hero "NayaNET — create, learn and grow together", "Good morning.", live clock ticking, feed card "Write for the Stranger, Sign It Official", rail in order, bottom bar with six labeled tiles (screenshot `shots/1920/20-addmenu-post.png`); the only change is where two menu items lead.

**Sense check (the page, not the brief).** Is it logical? Yes — each menu item sends its own mode, matching the Personal plus menu's own mapping. Sensible? Yes — 10 bytes, Buffer-level, nothing else moves. Intelligent? Yes — the `#home/composer`-for-both trap was caught before any href was written, by reading the Personal bytes first, and my own cloud-vs-checker contradiction was adjudicated from the code, not by picking a side. Am I doubling up? No — the two routes are distinct by design. In the best interest of the user — 10-star service? Yes, with one honest caveat the user will feel: on staged (and on live until the Personal re-mirror lands) the tap still lands on the profile top without the composer, because the served Personal predates the route and strips the suffix. That is the staging gap, named in §2 and §4b — the Hub half is done and correct; the mirror is what makes it visible. And one more the user will feel: on a fresh Personal load the "Install NayaNET" modal pops over the composer ("Install the app" / "Not now") — pre-existing Personal behavior, named in §7.

**Scorecard (honest).** This round as eyed: **9/10**. The route is proven from the Personal file's own bytes on both halves and by real pointer tap at both widths, the edit is 10 bytes with nothing else moved, laws delta 0, filing verified three ways, and the full followup18 regression re-proven by my own hand at 1920. It is not a 10 because the 390 rail-orb/info pointer taps could not land in this VM (scroll-into-view hang, owed to a real phone / cloud phone width), the staged tap cannot show the composer until the re-mirror lands, the DM still cannot send, and the live-domain guide avatar fails in this render.

## 7. What the eye spotted (pre-existing, next round's list — not this verdict)

1. **Install modal over the composer on fresh Personal loads.** On the `#home/naya` separating-test load, "Install NayaNET — Your intelligent hub, on your home screen…" popped over the open composer. The composer stands open underneath; "Not now" dismisses it. Pre-existing Personal behavior (the install prompt returns until the app is installed), untouched by this round. Worth a look before the re-mirror lands: a citizen arriving via ADD on a fresh load meets the install ask before the composer.
2. **The bottom bar starts folded in the VM render** (live Smart Bar never builds in VM Firefox; fallback bar sits below the fold until `#os-b3-hide` recalls it). The cloud browser found the same collapsed bar with the same corner control. That is the bar's fold behavior doing its job — not a defect — but it is why no VM seat could pointer-tap ADD until the corner control was found. Named so the next seat does not re-learn it.
3. **Console noise, pre-existing, same on base:** CORS `feed-live.json` (live feed reads blocked in VM Firefox), `PAGEERROR: handler is not a function`, `fetchWall is not defined`, `can't access property "tone", note is undefined`. The feed still renders (9,206 chars at 390; 12,268 at 1920) and zero `[hub-msg-panel]` warnings appear in any session. Not regressions from two hrefs.
4. **The 390 rail-orb/info pointer taps** (Vera orb/info/DM/Mail, Shawn orb) could not land in this VM even with `scrollIntoView` — the one remaining phone-width re-confirmation, owed to a real phone or the cloud browser at phone width.
5. **The live-domain guide avatar** (`nayanet.app/icons/naya-guide.jpg`, `naturalWidth: 0` in VM Firefox) — confirmed on my own render in the Ask Naya room. Pre-existing, not a Hub-file defect, not chased here.

## 8. What is still owed (not this round)

- Personal re-mirror: until the filed fix-5 Personal is what a tap lands on, no tap — staged or live — can show the composer opening from these hrefs. The Hub half is done; the Personal half is the mirror.
- Runtime send bridge: a DM/mail draft can be typed, but `Send · runtime required` stays disabled until the governed messaging runtime exposes sending.
- 18 pre-existing law violations (17 size, 1 gray) — out of scope, named.
- 390 rail pointer taps (§7.4) — real phone / cloud phone width.
- No merge, no live deploy, no link to Shawn — as briefed. Next step is the captain's decision on the verdict.
