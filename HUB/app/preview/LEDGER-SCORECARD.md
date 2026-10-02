# Smart Ledger — Room Four Scorecard v2 (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2` @ HEAD.
Director direction (2026-10-02): the ledger is the heartbeat of the system —
a living graph dashboard, not receipt boards. Demo content authorized for
design review and system testing; the live stream replaces it at launch.
Verified: jsdom — 15 pass, 0 fail (5 views, 28 demo beats, smart-id modal,
copy, raw view, 0 errors).

## Score: 9.4/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | Adapter parses real decision + execution receipts; demo stream is seeded, deterministic, and every entry labeled DEMO. |
| 2 | Honesty | 10 | DEMO banner; proof ladder law stated; a below-zero ACT and a REFUSE are in the demo data — the dashboard shows gates working, not just wins. |
| 3 | Heartbeat | 9 | Pulse line with 28 beats, sweep, live ticker, smart-ID chips. Ambient until the live stream lands. |
| 4 | Value views | 9 | Four-stage engine strip with live counts; ΔV diverging bars; Q bars with the 9.0 line; prediction-vs-observed calibration. |
| 5 | Smart IDs | 10 | Deterministic friendly names backed by full hashes; inspect modal with copy + view-raw, the token-explorer pattern. |
| 6 | Button law | 10 | Silver at rest, gold on highlight; every control works. |

## Why not 10

- **-0.4 — live stream not wired.** The room renders `ctx.entries`; the Supabase -> shell -> room read path is shell work (protected: production writes need Shawn's word).
- **-0.2 — visual confirmation pending** (screenshot pipeline still down).

## What closes it

- Shell feeds the production ledger into `ctx.entries` (demo flag off) -> +0.4
- Shawn's visual pass -> +0.2

## Sync architecture (director question, 2026-10-02)

What exists today: Smart Ledger foundation migrations (Sep 19) + V2.1 decision-value
binding migration (Oct 1) on Supabase; `kernel/value_calculus.py` executable reference;
ratified V2.1 math; local demo receipts (stand-ins, never production writes).
What does NOT exist: the live write path (app -> Supabase ledger), the GitHub
canonical mirror of receipts, or the shell read path into `ctx.entries`.
Proposed running shape: app/kernel emits a receipt -> Supabase `nayanet_smart_ledger` /
`nayanet_execution_receipts` (the live stream) -> hash-addressed mirror committed to
GitHub (canonical record, cold-successor replayable) -> Hub shell reads recent entries
-> this dashboard. Wiring the production sync is protected-gate work: needs Shawn's
explicit word. This room is built for it and does not care which store feeds it.
