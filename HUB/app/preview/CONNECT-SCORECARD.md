# Smart Connect — Room Three Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2` @ `d84c8fb`. Source: canonical
`BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json` (9 doors) via
`ConnectAdapter.parse` — projection, never a copy.
Verified: jsdom — 9 boards, 2 live / 7 design, 9 buttons, honest notices,
0 errors. Palette keyed by door id (stable identity, never list index).

## Score: 9.2/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | All 9 doors, exact IDs, statuses, capabilities. Nothing invented. |
| 2 | Honesty | 10 | LIVE vs IN DESIGN shown truthfully; no fake connect buttons — the notice tells the truth. |
| 3 | Color language | 9 | Each door owns its color (GitHub purple, MCP orange, AI magenta, Data green, Email sky, Calendar coral, Voice teal, Web blue, Naya gold). Live lit; design rests white, ignites on hover. |
| 4 | Simplicity | 9 | Door → plain words → unlocks → authority → one button. Nothing else. |
| 5 | Button law | 10 | Silver-white at rest, the door's own color on highlight. |
| 6 | Completeness | 8 | The room presents doors; real connection flows (OAuth) belong to the Hub shell via `ctx.onConnect`. |

## Why not 10

- **−0.5 — the wires aren't real yet.** The room calls `ctx.onConnect(doorId)`; until the shell implements the GitHub App / provider OAuth flows, CONNECT opens the honest notice instead of a real flow. Room-side this is complete; system-side it's pending.
- **−0.3 — visual confirmation pending.** Structure verified; the per-door ignition needs Shawn's eyes (screenshot pipeline still down).

## What closes it

- Shell implements `onConnect` for GitHub first (the flagship door) → +0.5
- Shawn's visual pass → +0.3

## Noted for the hub shell (Shawn's call)

- "Smart Connect should be at the very top" of hub navigation — room doesn't control nav order; flagged for the main-hub seat.
