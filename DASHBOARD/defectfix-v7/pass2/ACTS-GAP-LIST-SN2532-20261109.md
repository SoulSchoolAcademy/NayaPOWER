# Acts-Gap List — SN-2532 "What Naya Does" (2026-11-09)

Source note: SN-2532 "What Naya Does — Daily Reports, Smart Notes, Naya Notes, and Pages",
GitHub `BRAIN/05-MEMORY/SMART-NOTES/2026/11/09/PRODUCT/SN-2532/IB-SMART-NOTE-20261109-sn2532-what-naya-does.md`,
blob `4f6f4e5a`, 14,199B, verified on main 2026-11-09. The note itself is not rewritten here;
this file scores each of its ten acts against the live system. Built by the Dashboard
done-done pass-2 builder, 2026-11-09 ~17:55Z.

## Nutshell

One act of ten is PROVEN live. Nine are NOT YET — not because the rooms are missing
(the rooms are all live), but because the operated act itself — Naya doing it for a
citizen on request or on schedule, with a receipt — has no live evidence on record.
The manual groundwork underneath most acts is real and is named act by act, so the
gap is exactly the operated step, nothing wider. The sharpest gap is the first act:
the Reports room is frozen at October 23 while a verified 17-day backfill waits on a
service key — the exact failure mode SN-2532 itself names ("produced is not delivered").

## How to read this

- **PROVEN** means live evidence exists: a live check (HTTP, an independent audit, a
  live render) shows the act working, not just code that could do it.
- **NOT YET** means the act is claimed by the note but has no live receipt yet. What is
  missing is named exactly. Code that exists is listed under "Groundwork already proven"
  — it narrows the gap, it does not close it.
- Code read in the deployed Dashboard bytes is evidence the mechanism exists. It is
  never counted as live proof of the act. A live-browser tap is the verifier's check.

## Act 1 — Daily Intelligence Reports — NOT YET

- **Verdict:** NOT YET.
- **Evidence:** The Reports room is live — `https://nayanet.app/rooms/reports` returns
  HTTP 200 (curl, this VM, 2026-11-09). The room's newest report is October 23.
- **Missing:** Delivery. The 17-day backfill package (Oct 24 – Nov 9, 17 rows, all body
  hashes match, commit `dcc885cc`) is verified ready, but ingest is BLOCKED: the table
  `hub_daily_intelligence_reports` has RLS with anon SELECT only, and the test insert
  failed Postgres 42501. It needs a service_role-backed run of
  `~/workspace/reports-backfill-20261109/rows-seed.sql` (one INSERT, 17 tuples,
  ON CONFLICT re-runnable) by whoever holds the service key, or an INSERT policy.
  After that, a live check that Nov 9's report opens in the room. From this VM the
  Supabase live read fails (CORS/NetworkError, likely the egress proxy), so the room
  shows only its 6 baked reports here — a real-browser check is the one that matters.
  The room also carries a non-fatal `pad is not defined` pageerror.
- **Groundwork already proven:** Room live and serving; avatar fixed live 17:50Z
  (canonical `HUB/app/icons/naya-guide.jpg`, blob `3340de2d`, commit `9f409a64`,
  live 200 image/jpeg, renders 48x48 at 1440/390); backfill rows verified ready.

## Act 2 — Smart Notes — NOT YET

- **Verdict:** NOT YET.
- **Evidence:** None live of Naya entering a Smart Note on request or on schedule.
- **Missing:** One operated entry with a receipt: requested (or scheduled) → entered →
  visible where the citizen will see it.
- **Groundwork already proven:** The manual path is live in the deployed Dashboard
  bytes — Smart Note capture writes `smart_notes` rows with `k:'note'`, and the notes
  render reads those rows back (code read in the built file). The Hub feed carries
  Smart Notes. What is missing is only the operated step, not the storage.

## Act 3 — Naya Notes — NOT YET

- **Verdict:** NOT YET.
- **Evidence:** None live of Naya entering a Naya Note on request or on schedule.
- **Missing:** One operated entry with a receipt: requested (or scheduled) → entered →
  visible in the citizen's Naya Notes.
- **Groundwork already proven:** The manual path is live in the deployed Dashboard
  bytes — the Naya Notes card (`os-nn-card`) writes to the `naya_notes` table, and
  messages saved from the Inbox land there too (code read in the built file).

## Act 4 — Creating and filling pages — NOT YET

- **Verdict:** NOT YET.
- **Evidence:** None live of Naya creating and filling a page end-to-end on a citizen's request.
- **Missing:** One operated build with a receipt: request → page created → filled with
  content → openable by the citizen.
- **Groundwork already proven:** The pages themselves are real and live — all 18
  Dashboard-linked apps return HTTP 200 (curl, this VM, 2026-11-09; also the pricing
  v73 functional audit, 17:48Z: 18 View URLs all 200, real apps). The auto-build path
  (10 questions → factory pulls parts → app built) is documented, not live-receipted.

## Act 5 — Highlights (Intel Today nutshell digest) — NOT YET

- **Verdict:** NOT YET.
- **Evidence:** The Intel Today room is live — `https://nayanet.app/rooms/today`
  returns HTTP 200 (curl, this VM, 2026-11-09). No live render of the day's Smart
  Notes listed in a nutshell has been seen this session.
- **Missing:** A live-browser render showing today's Smart Notes standing listed in a
  nutshell in Intel Today.
- **Groundwork already proven:** The mechanism is live in the deployed Dashboard
  bytes — the Today view renders the day's Smart Notes list and the "Your daily
  brief" card from live ledger data on load, with no hand step (code read in the
  built file).

## Act 6 — Sending on your behalf — NOT YET

- **Verdict:** NOT YET.
- **Evidence:** None live of a send made by Naya on a citizen's behalf this session.
  No receipt exists for any of the four sends: mail, messages, feed posts, notes to
  another member.
- **Missing:** One receipted send of each kind — a mail sent, a message sent, a post
  on a feed, a note carried to another member — each visible where it was sent.
- **Groundwork already proven:** The send paths are live in the deployed Dashboard
  bytes — mail/message sends insert into `smart_mail_threads` /
  `smart_mail_messages`, wall posts insert into `smart_notes` with `k:'wall'`
  (code read in the built file). Notes to another member have no code path on
  record at all — that sub-part has no groundwork, not just no receipt.

## Act 7 — Smart Box — NOT YET

- **Verdict:** NOT YET.
- **Evidence:** The Smart Box room is live — `https://nayanet.app/smartbox` returns
  HTTP 200 (curl, this VM, 2026-11-09). No live store-and-recall receipt exists.
- **Missing:** One receipted round trip: enter something → it is remembered → it is
  recalled on request.
- **Groundwork already proven:** The room is reachable from the Dashboard's 18-page
  set. Nothing further is proven about its memory behaviour live.

## Act 8 — Smart Lists — NOT YET

- **Verdict:** NOT YET.
- **Evidence:** The Smart Lists room is live — `https://nayanet.app/rooms/lists`
  returns HTTP 200 (curl, this VM, 2026-11-09). No live receipt of Naya building a
  list on request exists.
- **Missing:** One operated list with a receipt: ask for contacts by username/alias,
  or a list of Smart Notes by link/name → the list stands built. Plus a live-browser
  render of the Lists room working.
- **Groundwork already proven:** The list machinery is live in the deployed Dashboard
  bytes — Smart Lists render in-page and write to `smart_lists` /
  `smart_list_items` (code read in the built file).

## Act 9 — Team mail (welcome email + updates) — NOT YET

- **Verdict:** NOT YET.
- **Evidence:** No sent welcome email, and no sent team update, has a receipt on record.
- **Missing:** One welcome email sent by her hand, with the new citizen's links, as
  part of joining — receipted (sent + received). Same for one team update.
- **Groundwork already proven:** The Welcome walk is live (`https://nayanet.app/welcome`,
  linked from the Dashboard and in the Dashboard search index). The mail-sending
  machinery exists in-page (see Act 6 groundwork). The welcome as an act has no receipt.

## Act 10 — Stats — PROVEN (Dashboard form only)

- **Verdict:** PROVEN — for the Dashboard form. The stats-report form and the
  per-page-stats-link form are NOT YET separately receipted (see Missing).
- **Evidence:** Live. The Dashboard shows live stats from the ledger: the pass-1
  re-verifier proved the stats flow live (780 → 781 moves the gauge 280 → 281 on a
  real event), and the pricing v73 functional audit (17:48Z, independent seat)
  confirmed the Dashboard read side queries `smart_links` +
  `smart_link_daily_stats` and displays them. The hero-fix page is live on
  `nayanet.app/dashboard` with the gauge following the number.
- **Missing:** A stats report delivered as a report, and a per-page stats link sent
  for a specific page — each with its own receipt. The worker → Supabase write hop
  behind the stats is UNVERIFIED (pricing audit 17:48Z) and belongs to the ledger-hop
  proof, not to this act.

## The umbrella + hook-up law — NOT YET (foundation gap, not one of the ten)

- **Umbrella:** "Naya operates all of NayaNET for you." It stands or falls with the
  ten acts above: one of ten proven live. The umbrella is NOT YET proven as a whole.
- **Hook-up law:** "Any citizen who hooks up their Muse gets a Naya who can operate
  inside NayaNET." No live receipt exists of a hooked-up citizen's Naya operating
  inside NayaNET on request or on schedule. Missing: one hooked-up citizen, one
  operated act end-to-end, receipted.

## Sources

- SN-2532, blob `4f6f4e5a`, 14,199B, read from main via `gh-direct.py` 2026-11-09.
- Reports room status 17:50Z Nov 9 (avatar fix live; ingest blocked on RLS 42501;
  backfill commit `dcc885cc`; work record
  `~/workspace/reports-backfill-20261109/WORK-RECORD-20261109.md`).
- Pricing v73 functional audit, 17:48Z Nov 9
  (`~/workspace/team-nitro/pricing/verify-v73-functional/FUNCTIONAL-AUDIT-V73.md`).
- Dashboard hero-fix live verification, 17:30–17:31Z Nov 9 (worker
  `naya-model-dashboard`, deployment `f8e2b2cc`, blob `1f09cafd`).
- HTTP statuses: curl from this VM, 2026-11-09 ~17:53Z. `nayanet.live` returns
  HTTP 000 from curl in this VM (VM-egress limitation, not a verdict on the link —
  the share `https://nayanet.live/s/sn2532` must be verified from a real browser).
