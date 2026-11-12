# Wiring Readiness Scorecard — NayaNET

**Ordered by Shawn Vibert, in his own words, in main chat 2026-11-10 ~18:33 PST.**
**Audited by Naya Power, 2026-11-10 ~18:40 PST. Every live claim below was verified by a curl read this pass unless labelled otherwise.**
**Shawn's direction for this audit: he does NOT care about distillation right now. What he cares about is the wiring — the Smart Factory / platform / system so it actually operates and works right. Score readiness to be world-class and ready to give to the public RIGHT NOW.**

---

## The headline

**Overall readiness: 4 / 10 — NOT ready for the public.**

The system exists. Pages serve, data flows, the feed is back, PI reads live. But the three flows a stranger must complete — join, get invited in, read a note — are broken. A system whose front door, invitation, and reading do not work is not world-class and is not ready to give to the public. The infrastructure is substantially built; the wiring that makes it operate is not finished.

**What "4" means:** the foundation is real (roughly half the system serves and works), but the citizen-critical paths fail. A 5 would mean half-ready; the broken join/read flows are disqualifying for public use, so it is a 4.

**Evidence standard used:** every route was curled this pass (HTTP + bytes + a content check). A bare 200 proves nothing — the Hub worker answers any path with the same ~5.53MB SPA shell, so a page counts only when its own distinct bytes came back or its content markers were found. Labels: **verified fact** (I read it live this pass) / **strong evidence** (a seat's verified read, cited) / **inference** / **hypothesis** / **unknown**.

---

## Per-area scores (out of 10)

| Area | Score | One line |
|---|---|---|
| Front door (entrance, welcome, identity, join) | 4 | Entrance live, welcome serves — but the identity bug is still live and the invite route drops the code. |
| Hub + feed (cards, reading, navigation) | 4 | Feed restored to 861 — but a card click does nothing, and the reader drops layers. |
| Citizen pages (Personal, Business, Space, Dashboard) | 6 | Serve with real content, Dashboard pass-10 live, Ambassador row present — but My World + pass-11/12 unfinished, fills 0/26. |
| Rooms (today, reports, ledger, mail, lists, etc.) | 5 | Serve distinct bytes — but function unverified by curl; Feed/Settings/Mission are shell-only. |
| Smart Notes + feed data | 6 | Feed restored, direct note links work — but reader defects and the broken card click. |
| Smart Factory | 5 | Serves — but one-click NOT PASS on design-gate (f), templates not proven. |
| Affiliate / Ambassador | 5 | Ambassador row on Dashboard — but the Smart Link Law is violated in mail and the reconciler is dead. |
| Membership / courses | 4 | Pages serve — but the membership login experience and Smart Access are designs, not live. |
| Voice | 3 | Lives in the shell, no standalone page, function unverified. |
| Connect / other AIs | 3 | Shell-only, no distinct page. |
| Pricing | 6 | Serves — but a pricing screen overflow defect is open and the free-join money-vs-points question is unanswered. |
| Privacy locks | 3 | Mail privacy fitting pending, payments P0 open, 6 Supabase tables with no lock. |
| Project Intelligence | 6 | PI v4 live at /pi, reads live rows — but /projects is not the PI face, questions.json is 404, and the record is 30/687 done. |
| Search / Auto-Match | 3 | Search scores 4/8, Auto-Match is switched off. |
| Smart Mail | 5 | Serves, Compose present — but no Inbox label found and the mail privacy fitting is pending. |

---

## Page-by-page audit (Resolve's registry, re-probed live this pass)

Shell signature this pass: /hub = 5,528,941 bytes. A route returning exactly that is the SPA fallback, not a page.

### One Hub — the shell and its rooms

| Page | Status | Evidence (verified fact unless noted) | Missing / wiring owed |
|---|---|---|---|
| Intelligent Hub Home | PARTIAL | /hub 200, 5,528,941B (shell). Title "NayaNET — The Intelligent Hub". | Card click broken (see below). |
| Smart Feed | PARTIAL | /rooms/feed 200, shell bytes — no distinct page. Feed data IS live: feed-live.json 200, 6,583,817B, count 861, newest SN-2654 (2026-11-10T23:33:00Z), 40 cards from 2026-11-10. | No distinct feed page; card click broken; reader defects. |
| Your Intelligence Today | WORKING (serves) | /rooms/today 200, 332,382B distinct. | Function unverified by curl (content renders via JS). |
| Your Reports | WORKING (serves) | /rooms/reports 200, 278,423B distinct. | Function unverified by curl. |
| Smart Ledger | WORKING (serves) | /rooms/ledger 200, 171,543B distinct. | Function unverified by curl. |
| Intelligence — Intel Today | WORKING (serves) | /rooms/intelligence 200, 102,512B distinct. | Function unverified by curl. |
| Mission room | MISSING | /rooms/mission 200, shell bytes — no route, no distinct page. | Prove a real page exists or retire the name. |

### Membership & Identity — the front door

| Page | Status | Evidence | Missing / wiring owed |
|---|---|---|---|
| Welcome — the entry door | WORKING (serves) | /welcome 200, 156,965B distinct. Title "The Official Welcome | NayaNET". Markers: Welcome, Enter, name, Join. | Intake-to-identity handoff unverified live. |
| Entrance (root) | WORKING | / 200, 106,791B distinct. Markers: "Enter NayaNET", "Jump back in", "Welcome". | — |
| Identity page = Certificate page | BROKEN (bug live) | /identity.html 200, ~303,000B distinct. Markers: "Available" present; NO `cb=`, NO `no-store`, NO "Jump back in". This is the OLD buggy bytes. PR #3335 (the repair) was merged 01:58:44Z but NOT deployed. The front-door bug is still live: a taken name reads "Available", ENTER hits 409 and returns without navigating, and a returning citizen has no way in. | Deploy the repaired identity bytes; verify live (taken shows "taken", Jump back in works). Owner: Shawn's hand (deploy) / Nitro. |
| Join — citizen invitation | WORKING (redirect) | /joinus 302 → /welcome. | — |

### Citizen surfaces

| Page | Status | Evidence | Missing / wiring owed |
|---|---|---|---|
| Personal page | WORKING (serves) | /personal 200, 1,161,523B distinct. Title "Shawn Vibert". Markers: My World, Dashboard, Smart Bar, Membership, Settings. | My World round + pass-11/12 unfinished; fill incomplete. |
| Business page | WORKING (serves) | /business 200, 818,845B distinct. | Fill incomplete. |
| Space page | WORKING (serves) | /space 200, 851,170B distinct. | Fill incomplete. |
| Dashboard | WORKING | /dashboard 200, 1,817,928B distinct. Markers: "PASS10", "Dashboard v9", "Ambassador", "Smart Link", "My Smart Link". "1338" NOT in bytes (it is the live grand total, computed at read time — strong evidence, run 111). | Pass-11/12 rounds running; per-page attribution 0 (data-model decision, open). |
| Smart Spaces — room index | WORKING (serves) | /rooms/spaces 200, 1,077,302B distinct. | Function unverified by curl. |
| Intelligent Library | WORKING (serves) | /rooms/library 200, 192,694B distinct. | Function unverified by curl. |
| Smart Note — public page | WORKING (redirect) | /s/sn0136 → 302 → https://nayanet.app/#/smart-notes/sn0136. /smart-notes/sn0136 → same. Direct note URLs work. | Card click from the feed is broken (below). |
| Your Connections | WORKING (serves) | /rooms/connections 200, 255,351B distinct. | Function unverified by curl. |
| Smart Lists | WORKING (serves) | /rooms/lists 200, 339,083B distinct. | Function unverified by curl. |
| Settings | PARTIAL | /rooms/settings 200, shell bytes — no distinct page. | No distinct settings page; renders inside shell only. |
| Life with Naya | WORKING (serves) | lifewithnaya.nayapower.workers.dev 200, 25,438,632B (25.4MB). | Weight audit owed — 25.4MB is a performance liability. |
| Booking | WORKING (serves) | /book 200, 9,577B distinct. Title "Book a time — NayaNET". | Booking defaults + BE-2 open (gated packet). |

### Smart Mail

| Page | Status | Evidence | Missing / wiring owed |
|---|---|---|---|
| Smart Mail | PARTIAL | /rooms/mail 200, 276,609B distinct. Title "Smart Mail — NayaNET". Markers: Smart Mail, Compose, mail present; "Inbox" NOT found. | No Inbox label found — verify what a signed-in user sees. Mail privacy fitting pending (nothing sensitive by mail until it lands and is proven). |

### Project Intelligence

| Page | Status | Evidence | Missing / wiring owed |
|---|---|---|---|
| PI hub face | WORKING | /pi 200, 2,372,427B distinct. Title "Project Intelligence v4 — NayaNET". The count ("30 of 687") is JS-rendered, not in the static HTML — verified by the waves' browser reads 46 consecutive times (strong evidence), not by this curl pass. | — |
| PI face at /projects | BROKEN (wrong page) | /projects 200, 225,040B distinct. Title "Projects — NayaNET". Markers: "Your Projects", "Project Intelligence". It is a generic citizen page, NOT the PI face. No nayanet.live reference remains (verified fact). | /projects must be rebuilt as the PI face (Shawn's 2026-10-24 ruling) or the pointer stays at /pi. |
| PI to-do board | WORKING (serves) | /projects/todos 200, 10,545B distinct. | — |
| PI machine state | WORKING | /projects/state.json 200, 1,092B distinct. | — |
| PI 14-question orientation | MISSING | /projects/questions.json 404 (9 bytes). Dead since the registry. | Restore it or retire the surface. |

### Connect & Ambassador

| Page | Status | Evidence | Missing / wiring owed |
|---|---|---|---|
| Smart Connect | PARTIAL | /connect 200, shell bytes (~5,529,293B) — no distinct page. | No distinct connect page; doors unproven live. |
| Growth | WORKING (serves) | /rooms/growth 200, 251,451B distinct. | Function unverified by curl. |

### Ask Naya

| Page | Status | Evidence | Missing / wiring owed |
|---|---|---|---|
| Ask Naya | PARTIAL | No standalone page; lives in Hub Home. Markers in the live shell: "naya-voice" present, "Ask Naya" present, "voice" present. "naya-intake" NOT found in the shell bytes. | Voice function unverified (no live voice test by curl); naya-intake.js not in the shell. |

### Smart Factory

| Page | Status | Evidence | Missing / wiring owed |
|---|---|---|---|
| Smart Factory | PARTIAL | /smartfactory 200, 580,186B distinct. Title "Smart Factory — pick your pieces". | One-click NOT PASS on design-gate (f) (443 look-alike buttons, 3 gold CTAs on the live base — pre-existing debt, strong evidence run 115). Base-(f) round running. Templates not proven as mirrors of the apps. |

### Security

| Page | Status | Evidence | Missing / wiring owed |
|---|---|---|---|
| Payments | WORKING (serves) | /pay 200, 5,772B distinct. Title "Pay — NayaNET". | P0 OPEN: anonymous EXECUTE on payment/booking RPCs — human-gated (Shawn's hand). Nothing changes until the gate opens. |

### Other routes probed

| Route | Status | Evidence |
|---|---|---|
| /pricing | WORKING (serves) | 200, 11,350,562B distinct. |
| /certificate | PARTIAL | 200, shell bytes — no distinct page. |
| /feed, /today, /library, /settings (bare) | PARTIAL | 200, shell bytes (~5,529,293B) — SPA fallback, not distinct pages. |
| /?invite=test | BROKEN | 200, shell bytes — shows the Hub, NOT the entrance. The invite code is dropped. The invited citizen never reaches the entrance and the inviter gets no credit. |

---

## The three broken citizen flows (the reason for the 4)

These are the flows a stranger must complete. All three fail.

1. **Read a note from the feed — BROKEN (verified fact, my own live read this pass).** In the live /hub shell bytes, the card title is rendered as a bare heading: `const title = el('h2', 'ib-title', esc(headline)); titleWrap.append(title);` — no anchor, no click handler, no navigation. In the entire intelBoard function body: 0 onclick, 0 `.click`, 0 `location.hash`, 0 `location.href`. The one `href` in the region is the "Back to Hub" link inside the note VIEW, not the feed card. The one `addEventListener` is a layer expand/collapse toggle. Clicking a card does nothing. **The fix is known** (wrap the title in an anchor to `#/smart-notes/snNNNN`) and the main seat is applying it now — but it is NOT in the live bytes yet. Re-check after deploy by clicking a card live.
2. **Get invited in — BROKEN (verified fact).** `nayanet.app/?invite=test` serves the Hub shell. The entrance already handles `?invite=` but is never reached for query-string URLs. The code is dropped, the inviter gets no credit. Fix round dispatched (run 111), still building.
3. **Get back in as a returning citizen — BROKEN (verified fact).** The live identity page is the old buggy bytes (no `cb=`, no `no-store`, no "Jump back in"). A taken name reads "Available"; ENTER hits 409 and returns without navigating. PR #3335 (the repair) was merged 01:58:44Z but NOT deployed. Whether the rendered verdict preceded the merge is UNKNOWN (not established by any read I have). The live page is unaffected by the merge because no deploy has run — and that is exactly the gap: merge ≠ deploy.

---

## The wiring list — ranked by value (most function unlocked for least work first)

1. **Hub card click — make a card open its note.** Owner: Nitro (front-end) / Power applying now. Next: land the anchor fix, deploy, verify by a live browser click on a card. Unlocks: the primary way any citizen reads a note.
2. **Invite route — the Hub must show the entrance when `?invite=` is present.** Owner: Nitro. Next: land the fix round (dispatched run 111, still building), verify `/?invite=test` renders the entrance with the code kept. Unlocks: invited citizens actually arriving + inviter credit.
3. **Identity front-door deploy — ship the repaired bytes.** Owner: Shawn's hand (deploy) / Nitro. Next: deploy the #3335 bytes, verify live (taken shows "taken", "Jump back in" works, no 409 silent death). Unlocks: returning citizens getting in. Note: the merge is done; the deploy is the missing step.
4. **Smart Link Law in mail — invite SEND mail must carry clean Smart Links, not raw query links.** Owner: Nitro (Inviter). Next: fix the mail body (auto-mint, or the paste → Smart Link → share step) + re-verify by reading a sent mail. Unlocks: the ambassador loop working end to end. Blocked in part on the dead reconciler loop (dead since 2026-11-06 ~02:14Z — restart it or prove the fallback).
5. **Feed reader defects — How It Connects layer, Nutshell cut off mid-word, no SN badge.** Owner: Nitro. Next: fix + re-check the SN-2248 render live. Unlocks: notes actually readable where they are read.
6. **Mission room + questions.json — close the two dead registry rows.** Owner: Resolve (registry) / Nitro (build). Next: prove a Mission page exists or retire the name; restore questions.json or retire the surface. Unlocks: the registry telling the truth.
7. **Feed / Settings / Connect distinct pages — or render proof.** Owner: Nitro. Next: render proof of what a signed-in user sees, or build distinct pages. Unlocks: the rooms being real pages, not shell echoes.
8. **Voice — prove the queue moves, warming is live, first sound is fast.** Owner: Nitro. Next: a live voice test end to end (PI order item 2). Unlocks: the voice door.
9. **Smart Match + search — switch on Auto-Match, feed the corpus.** Owner: Resolve. Next: switch on Auto-Match (merged but off); feed the missing knowledge (welcome, pricing, invite, Auto-Match docs) and re-run the 8 questions to 8/8 (currently 4/8). Unlocks: matching + search working.
10. **Payments P0 + privacy locks — close them before any citizen money data goes live.** Owner: Shawn's hand (gate) / Resolve. Next: close anonymous EXECUTE on payment/booking RPCs; lock the 6 Supabase tables with no lock; prove the mail privacy fitting. Unlocks: citizen money data going live safely.
11. **The 26 fills to complete — 0/26, verifier null, done_proven flat at 30 for a week.** Owner: all seats. Next: scorecards → fix every defect as tracked items → re-score → 9+ from both other seats → live proof. Unlocks: finished pages.
12. **Sync heartbeat writer — stale since 23:35Z.** Owner: Nitro. Next: repair/restart the writer, verify the heartbeat. Unlocks: the sync staying honest (the feed regression happened while the sync was unmonitored).
13. **Life with Naya weight — 25.4MB.** Owner: Nitro. Next: weight audit + slim it. Unlocks: the page loading fast on a phone.
14. **Pricing screen overflow + free-join money-vs-points.** Owner: Nitro (overflow) / Shawn (the question). Next: fix the overflow; Shawn rules whether a free join pays money or points only. Unlocks: pricing being presentable + the affiliate promise being truthful.

---

## What is already working (the foundation the 4 rests on)

- The shell serves everywhere (200 on every route probed).
- The feed is restored: 861 cards, newest SN-2654, 40 cards from 2026-11-10 — verified by my own curl this pass.
- The entrance is live with "Enter NayaNET" and "Jump back in".
- The Dashboard is live at pass-10 with the Ambassador row and "My Smart Link".
- PI v4 is live at /pi and reads live rows.
- Personal / Business / Space / Dashboard / rooms / pricing / factory / book / pay all serve distinct bytes with real content markers.
- Smart Note direct links work (302 → hash route → renders).
- 8 PRs merged by Shawn in the last day, including the feed cure, the Anatomy, the identity repair, and the browser recovery.
- Browsers are alive again (recovered 01:32Z), so rendered verification is possible again.

## What "world-class and public-ready" still needs

A stranger must be able to: arrive, join, get back in, be invited in, read a note, use a page, and pay — with nothing silently failing. Today three of those fail visibly (read, invite, return). The fills are 0/26 complete. Nothing has finished in a week. The wiring list above, worked in order, closes the gap. The score moves when the three broken flows are proven live by a click, an invite, and a return — not when a file lands in the repo.

---

## Method and limits

- Probed live by curl this pass (2026-11-10 ~18:40 PST): every registry route + /pricing + /?invite=test + lifewithnaya worker. HTTP + bytes + content markers recorded above.
- The Hub card click verdict is from reading the live /hub shell bytes (intelBoard function) — a byte-level read, not a browser click. A live browser click is still the final proof and is owed after the fix deploys.
- Function inside a page (what a signed-in user actually does) cannot be proven by curl. Pages marked WORKING (serves) mean they serve distinct bytes with real content markers — not that every button works. The finish loop (scorecard → fix → re-score → 9+ → live proof) is still owed for every page.
- Items I could not verify by curl are labelled: the Smart Link Law in mail (needs a mail read), the sync heartbeat writer (a background job), the #3335 rendered-verdict timing (no record in my reads), and voice function (needs a live voice test).
- Registry baseline: Resolve's page registry v1 (2026-10-25), 32 pages, 26 proven live then. Re-probed live this pass; the counts above are today's.
