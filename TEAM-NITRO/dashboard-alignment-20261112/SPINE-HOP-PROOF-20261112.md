# SPINE HOP PROOF — DASHBOARD ALIGNMENT (RESTART)

**Seat:** dashboard-alignment-20261112 (maker, restart)
**Brief:** `~/workspace/team-nitro/BRIEF-DASHBOARD-ALIGNMENT-20261112.md`
**Date:** 2026-11-13 ~01:00–01:20Z
**Status:** ✅ HOPS 1, 2a AND 3 PROVEN LIVE with before/after numbers. Hop 2b (the `ledger_entries` table) is NOT PROVEN — the Ledger write is frozen, and tonight's wire verification confirms no code writes it. The anon 401 on raw `smart_link_clicks` GET stands; the read-back path is the `smart_link_daily_stats` rollup, stated with evidence.

## Hop table

| Hop | Claim | Verdict | Evidence (first-hand, live) |
|---|---|---|---|
| Hop 1 — a real click on a tracked Smart Link lands as a row | A click on `https://nayanet.app/my-test-link` records a click row via the worker (`recordClick` POSTs to `/smart_link_clicks` with the anon key) | **PROVEN** | Browser navigation to `https://nayanet.app/my-test-link` at 2026-11-13T01:01:27Z → 302 to `https://example.com/my-page` (the link's target). The click is the same GET the Dashboard's own "Open it" button performs. |
| Hop 2a — the daily-stats rollup records it | `smart_link_daily_stats` ticks for the clicked link | **PROVEN** | sb-api anon SELECT before: my-test-link 11 clicks (2 rows). After the click: **12 clicks (3 rows) in 2.2s**. The rollup updates promptly — the face's 1,375 → 1,376 tick from the affiliate investigation is the same mechanism, re-proven. Read-back path: the daily-stats rollup (anon SELECT granted). Raw `smart_link_clicks` GET is 42501 for anon — the rollup IS the read-back path, as the schema record says. |
| Hop 2b — the Smart Ledger (`ledger_entries`) records it | The Ledger records the click | **NOT PROVEN** | The Ledger write is frozen: 31 rows, latest Oct 22, nothing in 21 days (back-end grounding 23:53Z). Tonight's wire verification (01:0xZ, read-only, first-hand): **no code reads the Box and writes a ledger entry; the ONLY writer of `ledger_entries` is `02-ledger-append.py`, hand-supplied CLI args only.** The click path proven here (click → `smart_link_clicks` → daily-stats rollup → Dashboard boards) does NOT pass through `ledger_entries`. The trigger DDL is prepared, NOT applied (his tap). This hop waits on the ledger trigger apply + the Box→Ledger wire (back-end round's Step 3 names the seams). |
| Hop 3 — the Dashboard boards show it (numbers move, gauge follows) | The Dashboard's board total + funnel Found move on the click | **PROVEN** | Built page before the click: `_dashLinkT.c` 1,457, `_dashFunnel.found` 5,139, `mixTotal` 1,462. After the click + reload: **1,458 / 5,140 / 1,463**. Every number moved by exactly 1, the funnel's Found tile re-read 5 140, zero console errors. |

## Plan-link check (Shawn's 2026-11-07 ruling, proven live)

A PayPal plan-link click must NOT move the Dashboard board total (plan links live in a separate counter Today's Intel surfaces) — but it MUST still count as found.

- Click: curl GET `https://nayanet.app/max-monthly` at 01:01:45Z → **302 to PayPal** (`paypal.com/webapps/billing/plans/subscribe?plan_id=P-7AL685984U3816414NLXDOMQ`).
- Rollup: max-monthly 417 → **418 in 2.5s** (rows 7 → 8).
- Dashboard after reload: board total **1,458 (unchanged)**; funnel Found **5,140 → 5,141**; mixTotal 1,463 (unchanged).
- Verdict: **PROVEN — the separate counter works exactly as ruled.** The board total never reads as the all-links total; the funnel Found is the all-links number and says so on the page.

## F2 re-check — RESOLVED (was "still loading" for 45 minutes on Nov 9)

"MY PERFORMANCE — MY SCORE" watched on the built page AND live data path:

- 1440: skeleton ("Ledger loading — your score appears when the ledger answers") cleared after **11.0s**; score tiles live.
- 390: cleared after **23.9s**.
- Every reload in the spine run (3 reloads at 1440): skeleton cleared, `scoreSkeleton: false`.
- Verdict: **F2 is RESOLVED — it resolves, slowly (11–24s), never stuck.** The 45-minute stuck state from Nov 9 is gone. The slowness itself (a ledger round-trip through the VM proxy) is noted, not hidden — on a real network it will be faster, and the skeleton says plainly what it is waiting for.

## Counter scope, labelled

- Board counter (`_dashLinkT.c`, "Smart Links LIVE — CLICKS"): his claimed links only — 1,458 after the test. PayPal plan links excluded by his ruling.
- Funnel Found (`_dashFunnel.found`): ALL Smart Link clicks — 5,141 after the test. Labelled on the page: "Found: Smart Link clicks, all links (smart_link_daily_stats.clicks)."
- mixTotal (Reports board "Dashboard total"): 1,463 = 4 posts + 0 msgs + 1 invite + 1,458 clicks + 0 joins. Reconciles exactly.

## Known blockers (named, not fixed here)

- **Anon 401/42501 on `smart_link_clicks` GET (and `ambassador_links` / `ambassador_events`)** — the wiring round's scope, or his hand. No RLS/grants change in this round; none was made. The read-back path used here is the daily-stats rollup, which anon CAN read.
- **Board-open tracking (`_osTrackBoardOpen`) is BROKEN live** — proven by a direct hook call 01:15Z: the insert promise resolves with an error and `POST /rest/v1/smart_notes` returns **401**; board-open row count stayed at 2 (newest 2026-11-09T18:39:26Z) across three click tests. Board clicks are therefore NOT tracked live right now, even though the hook exists in code and wrote rows on Nov 9. Same anon-write family as the mail 401. Owner: the wiring round / the privacy-fix follow-up — NOT this round (no RLS/grants change authorized here). Consequence: no 18-page row claims "tracked" in this round; the only tracking proven live is the click → rollup → boards hop above.
- **Ledger trigger apply** — his tap; DDL prepared, not applied.
- **Act 1 backfill / service key** — NAMED, never run (credentials action, his hand only).

## Wiring preserved

The built file carries the tracking wiring intact: `window.loadPointsBoard` (30 matches) and `supabase-ready` (3 matches) — same counts as the pass-13 base. No wiring change was made in this round. All 18 inline script blocks parse clean (`new Function` check, 0 bad).
