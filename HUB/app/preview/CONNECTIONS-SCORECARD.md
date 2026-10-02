# Connections — Room Scorecard (subagent build, 2026-10-02)

Branch: `naya4/room-02-reports-v2` (uncommitted working tree; NOT pushed).
Contract: `ConnectionsAdapter.parseContacts(raw)` → `ctx.contacts` →
`window.NayaRooms.connections(el, ctx)`.
Verified: node syntax ×2, CSS brace balance, jsdom 11 pass / 0 fail.

## Score: 9.2/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | Five real contacts from the director's pack (Shawn, Naya 1–4); notes cross-checked against `~/memory/people/*.md`. No demo people, no invented contacts. |
| 2 | Button law | 10 | Silver-white at rest, rose ignite on hover/focus; every control (chips, new list, save-to-list, draft, close) has a real consequence. |
| 3 | Color law | 10 | Each contact owns their stable color — full-perimeter 2px border + glowing jewel avatar in it. Room identity stays rose (kicker, chips, buttons). |
| 4 | Lists | 9 | All + per-list filter chips, "New list" creator, toggle save-to-list per contact; persisted in `naya.connections.lists` (seed: "Team Naya" with all five). Repair pass drops stale member ids. |
| 5 | Messaging honesty | 10 | Quick-message box saves drafts to `naya.connections.drafts` and says plainly "not sent" / "Nothing is sent anywhere from here." No fake send. |
| 6 | Accessibility | 9 | Cards are role=button + tabindex + Enter/Space; modal has Escape + overlay-click close and initial focus. |

## Why not 10

- **-0.5 — no real send path.** Drafts are honest drafts; actual delivery belongs to the Smart Mail room / network layer (not built yet).
- **-0.3 — visual confirmation pending.** Structure verified via jsdom only; Shawn's eyes have not seen it.

## What closes it

- Smart Mail room wires drafts into real delivery -> +0.5
- Shawn's visual pass -> +0.3

## Files

- `HUB/app/js/rooms/connections-adapter.js`
- `HUB/app/js/rooms/connections.js`
- `HUB/app/css/connections.css`
- `HUB/app/preview/build-connections-preview.py`
- Preview: `~/workspace/your_files/connections-preview.html`

## Not done (parent's lane)

- Commit / push / merge — explicitly out of scope for this task.
