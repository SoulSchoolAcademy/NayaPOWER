# Smart Connect — Room Three Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2` @ `d84c8fb`. Source: canonical
`BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json` (9 doors) via
`ConnectAdapter.parse` — projection, never a copy.
Verified: jsdom — 9 boards, 2 live / 7 design, 9 buttons, honest notices,
0 errors. Palette keyed by door id (stable identity, never list index).

## Score: 9.5/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | All 9 doors, exact IDs, statuses, capabilities. Nothing invented. |
| 2 | Honesty | 10 | LIVE vs IN DESIGN shown truthfully; no fake connect buttons — the notice tells the truth. |
| 3 | Color language | 10 | Each door owns its stable color AND its own jewel glyph, always lit (director palette 2026-10-02: GitHub purple, MCP indigo, A2A sapphire, Data cyan, Email lime, Calendar yellow, Voice gold, Web orange, Naya red). Full-perimeter 2px door-colored edge; live doors glow, design doors ignite on hover. Director-approved 2026-10-02. |
| 4 | Simplicity | 9 | Door → plain words → unlocks → authority → one button. Nothing else. |
| 5 | Button law | 10 | Silver-white at rest, the door's own color on highlight. |
| 6 | Completeness | 8 | The room presents doors; real connection flows (OAuth) belong to the Hub shell via `ctx.onConnect`. |

## Director corrections applied (2026-10-02)

- "AI Connect" was wrong: renamed to **A2A Connect** (agent-to-agent); canonical registry still says AI Connect until his A2A material lands.
- Data door: **cyan**, not beige (dictation correction). Forest green dropped unless he wants it as depth tone.

## Why not 10

- **−0.5 — the wires aren't real yet.** The room calls `ctx.onConnect(doorId)`; until the shell implements the GitHub App / provider OAuth flows, CONNECT opens the honest notice instead of a real flow. Room-side this is complete; system-side it's pending.
- Visual approval received from the director (2026-10-02: "100% better").

## What closes it

- Shell implements `onConnect` for GitHub first (the flagship door) → +0.5
- Shawn's visual pass → +0.3

## Noted for the hub shell (Shawn's call)

- "Smart Connect should be at the very top" of hub navigation — room doesn't control nav order; flagged for the main-hub seat.
