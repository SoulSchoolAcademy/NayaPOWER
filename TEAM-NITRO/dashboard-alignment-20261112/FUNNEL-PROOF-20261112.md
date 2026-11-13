# FUNNEL PROOF — DASHBOARD ALIGNMENT (RESTART)

**Seat:** dashboard-alignment-20261112 (maker, restart)
**Brief:** `~/workspace/team-nitro/BRIEF-DASHBOARD-ALIGNMENT-20261112.md`
**Schema authority:** `~/workspace/team-nitro/FUNNEL-SCHEMA-RECORD-20261112.md` (captain's decision, 2026-11-13 ~00:45Z — read for the schema, NOT the blog round's record)
**Date:** 2026-11-13 ~01:00–01:30Z
**Status:** ✅ PROVEN LIVE — found reads live from Supabase; visited / joined / stayed show NOT YET with the missing source named. No number fabricated, no DEMO data as live.

## The verdict

The funnel (found → visited → joined → stayed) is visible in the Reports board (`#os-reports-board`) and in the Smart Links drill (the orb-details half), in the same number + gauge + label presentation as every other board. Found is a live number from `smart_link_daily_stats.clicks`. The other three stages are NOT YET, each with its missing source named on the page itself, in the source line under the funnel.

## Stage table (live reads, 2026-11-13)

| Stage | Number (live) | Supabase source | Live read | Renders |
|---|---|---|---|---|
| Found | **5,141** (5,139 at first read ~00:55Z; +2 from this round's own spine test clicks) | `smart_link_daily_stats.clicks` — SUM over all 95 rows, all 15 links | sb-api anon SELECT, first-hand: 95 rows, SUM clicks 5,141, SUM joins 0 | Reports board `#os-reports-funnel` + Smart Links drill — 4/4 cells, minis mounted |
| Visited | NOT YET — "—" on the page | **NO SOURCE YET** — no table carries "landed on the page." The blog round's Phase 2 defines the visit measurement, or the stage stays NOT YET. (Reinforced 01:12Z: the blog deep-link pin-down found the Hub shell has NO note route — a note link landing on the feed breaks found → visited → joined at the visited step.) | None — no source to read | Same funnel rows — "—" + NOT YET in the source line |
| Joined | **0** — the honest number | `public.smart_link_joins` (link_id, joined_alias, invite_code, source) — table + anon INSERT grant exist; **the FLOW is not built** (back-end round builds it: read the `naya_sl` cookie at join, resolve the link id, insert ONE row deduped per link + alias). `smart_link_daily_stats.joins` SUM = 0, first-hand. | sb-api: daily_stats joins SUM 0; anon SELECT on `smart_link_joins` returns 42501 (no SELECT grant — the read-back path is the daily-stats rollup) | Same funnel rows — "0" + the missing flow named in the source line |
| Stayed | NOT YET — "—" on the page | **NO SOURCE YET** — needs repeat activity after joining + the ledger flowing. The Ledger write is frozen (31 rows, latest Oct 22); the trigger apply is his tap; tonight's wire verification confirms no code reads the Box and writes a ledger entry. | None — no source to read | Same funnel rows — "—" + NOT YET in the source line |

## Reconciliation (first-hand, sb-api)

- Per-link clicks (live ~00:55Z): joinus 972 · academy 427 · power-monthly 420 · max-monthly 417 · pro-monthly 408 · power-yearly 407 · pro-yearly 407 · max-quarterly 406 · max-yearly 406 · pro-quarterly 406 · power-quarterly 405 · flagship-personal 25 · lane6test 11 · closer-test-7x9 11 · my-test-link 11. Total 5,139. (Nine PayPal plan links: 3,682.)
- The Dashboard's own counter (board rows, PayPal 9 excluded by Shawn's 2026-11-07 ruling): 1,457 at first read — joinus 972 + academy 427 + flagship-personal 25 + lane6test 11 + closer-test-7x9 11 + my-test-link 11. 1,457 + 3,682 = 5,139 ✓.
- The funnel's Found (5,139 → 5,141) counts ALL links, including the nine plan links — a click on one still found NayaNET. The page says so: "Found: Smart Link clicks, all links (smart_link_daily_stats.clicks)." The board counter's scope (his claimed links only) is NOT the funnel's scope, and the two numbers are never mixed: the funnel reads `window._dashFunnel` (summed from the same daily-stats fetch BEFORE the PayPal-9 filter), the boards read `window._dashLinkT` (after the filter).
- The spine test moved both honestly: test-link click → found 5,139 → 5,140, board 1,457 → 1,458; plan-link click → found 5,140 → 5,141, board stayed 1,458. See `SPINE-HOP-PROOF-20261112.md`.

## Placement (the law, held)

Shawn's order 2026-11-01: NO new separate funnel section. The funnel lives in the Reports board + the orb details (the Smart Links drill). It fits there — the build adds no section, no hero element, no new page. The What-Naya-Does board stays removed (only its removal comment remains in the file).

## What changed in the file (3 edits, +4,848 B)

1. `renderLinks`: `window._dashFunnel = {found, joined, boardClicks, boardJoins}` — summed from the same `smart_link_daily_stats` fetch, before the PayPal-9 filter. No new fetch, no new table, no wiring change.
2. `_renderReportsBoard`: a second `.os-sl-gauges` row (`#os-reports-funnel`, 4 cells via the existing `cell()` helper) + the source line (`#os-reports-funnel-src`) naming every stage's source or its NOT YET reason. Idempotent on every spine refresh; minis mounted by the same `_osMountSlMinis` / `_osMiniNums` calls.
3. `smartlinkListHTML`: the same 4-cell funnel strip + source line at the top of the Smart Links drill (the orb-details half). Mounted by the drill's existing `_osMountSlMinis(_slList)` call.

## Live proof (Chromium via the localhost proxy forwarder, staged + local bytes)

- Local (byte-identical file): 1440 + 390 — funnel cells Found 5 139 / Visited — / Joined 0 / Stayed —, all 4 minis mounted, source line present, zero overflow, zero console errors. 360 — funnel reads, zero overflow, zero console errors.
- Drill: opened via the "See every link" summary card at 1440 + 390 — funnel strip on top, 4/4 cells, minis mounted, source line present.
- Staged proof host: funnel reads Found 5,141 live, zero overflow, zero console errors. Staged bytes verified: blob `a071b996`, 1,848,507 B, sha256 `26cf6991588638cd0d0b56e6bc0287a6abffe40cdf36fbe200464e20fad5d263` — identical to the probed local file.
- Wiring preserved: `window.loadPointsBoard` 30 matches, `supabase-ready` 3 matches in the built file (same as the base). No change to the hero, the numbers' values, or the gauge math.

## What is NOT in the funnel

No fabricated visited/stayed number. No DEMO data as live. No "live" or "synced" badge. No stage without a named source. No joins number beyond the honest 0. The funnel's Found number moves when real clicks land — that is the point, and the spine proof shows it moving.
