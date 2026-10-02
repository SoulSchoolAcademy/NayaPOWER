# NayaNET Hub — 10/10 Scorecard (living document)

**What:** `HUB/rooms/nayanet-hub.html` — one app, nine furnished rooms on the shared Hub shell.
**Bar:** Shawn's 10/10 — "world champions of interfaces," honest by construction.
**Method:** builder self-scores function; Naya 2 scorecards presentation; iterate until 10/10.
**Sources:** `HUB/DESIGN-CONTRACT.md` (Part 4 + §§14–29), `HUB/NAYANET INTERFACE CONCEPT.html` (frozen visual truth),
concept-derived Law Zero + room-color registry (design-law convergence pending — three PRs, one will survive).

## Dimensions

| # | Dimension | Source | v1 self-score | Notes |
|---|-----------|--------|---------------|-------|
| 1 | Visual fidelity to the V7 | frozen concept | 6/10 | Her workspace classes in use; sparse vs her boards. Naya 2 calibrates. |
| 2 | Functional completeness | Contract Part 4, per room | 7/10 | Every room does its Part 4 job at basic level. Reports synthesis is templated; Connect doors can't complete real OAuth (honest). |
| 3 | Cross-room integration | "one app, all rooms work together" | 8/10 | Shared store + ledger receipts + hash routing live. Feed marks → Ledger/Lists; captures → Library/Lists/Ledger. |
| 4 | Honesty | Contract §26, room specs | 9/10 | No fake data anywhere. Mail = NO MAIL. Watch: reports synthesis must stay labeled "computed". |
| 5 | Law Zero | design law | 8/10 | Text stays readable; verify chip contrast after elevation. |
| 6 | Button & interaction craft | concept (primo buttons) | 5/10 | My pills are basic. Elevate to her `ws-actions` accent language. |
| 7 | Board integrity | Contract §§15–16 | 7/10 | Boards live in the feed (hers, untouched). Rooms link out rather than re-rendering — acceptable. |
| 8 | Performance | single static file | 8/10 | 893KB, no network deps beyond CDNs already in shell. |

**Composite v1: ~7.2/10.** The drag is presentation (1, 6) — matches Shawn's "empty house" read.

## Per-room function checklist (Part 4)

- **Today** — diary 8 panels, honest states — inherited verbatim. ✅
- **Reports** — time ranges compute from real objects; receipts listed. ✅ basic
- **Library** — search + facets over real boards/notes; OPEN jumps to board. ✅
- **Connect** — 5 doors, what/who/status/action; requests receipted. ✅ (rename Share→Connect: her lane)
- **Ledger** — hash-chained receipts, VERIFY CHAIN, export. ✅
- **Connections** — 3 governed relationships, scopes, requests. ✅
- **Lists** — saved/favorites/loved/top-rated/collections CRUD. ✅
- **Mail** — NO MAIL, honest; notify pref. ✅
- **Spaces** — 6 boundaries + custom, privacy rules, counts. ✅
- **Settings** — runtime truth, data export/erase, trust. ⚠️ add identity + preferences
- **Notes** — runtime-first capture, local fallback labeled. ✅

## Iteration log

- **v2 (elevation):** adopt her `ws-stat` / `ws-actions` component language; grid rows; identity+preferences in Settings.
  Awaiting Naya 2's presentation scorecard (#554) for the blind-spot pass.
