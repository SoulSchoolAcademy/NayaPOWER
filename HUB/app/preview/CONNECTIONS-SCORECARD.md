# Connections — Room Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2`.

## People-spine slice (2026-10-02, Shawn's integration ruling)

Shawn: Mail, Connections, Spaces, Lists are parts of each other — one
organism. First slice built:

1. **`HUB/app/js/people-registry.js` — the shared people spine.**
   `window.NayaPeople` over `localStorage['naya.people.registry']`:
   load/save/ensureSeeded/add/get. First room opened seeds it from
   `ctx.contacts`; every room after reads the same truth. No more four
   copies of the contact list.
2. **Connections reads the spine.** Same cards, same lists — now resolved
   against the registry. Someone added in Smart Mail appears here.
3. **WRITE MAIL on every contact card** — hands the contact to Smart Mail's
   composer via `ctx.onCompose` (the shell routes it; previews use a
   `naya.mail.compose.request` handoff key, same pattern as the
   Today→List save key). The button only renders when the hook exists —
   no dead buttons.

## Score: 9.2/10 (unchanged — the spine is cross-room infrastructure)

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | Five real contacts from the director's pack (Shawn, Naya 1–4); notes cross-checked against `~/memory/people/*.md`. No demo people, no invented contacts. |
| 2 | Button law | 10 | Silver-white at rest, rose ignite on hover/focus; every control (chips, new list, save-to-list, draft, write-mail, close) has a real consequence. |
| 3 | Color law | 10 | Each contact owns their stable color — full-perimeter 2px border + glowing jewel avatar in it. Room identity stays rose (kicker, chips, buttons). |
| 4 | Lists | 9 | All + per-list filter chips, "New list" creator, toggle save-to-list per contact; persisted in `naya.connections.lists` (seed: "Team Naya" with all five). Repair pass drops stale member ids. |
| 5 | Messaging honesty | 10 | Quick-message box saves drafts to `naya.connections.drafts` and says plainly "not sent" / "Nothing is sent anywhere from here." No fake send. WRITE MAIL hands off to the real composer instead of pretending. |
| 6 | Accessibility | 9 | Cards are role=button + tabindex + Enter/Space; modal has Escape + overlay-click close and initial focus. |

## Why not 10

- **-0.5 — no real send path.** Drafts are honest drafts; WRITE MAIL now routes to Smart Mail's composer, which sends inside the network. True external delivery is still unbuilt.
- **-0.3 — visual confirmation pending.** Structure verified via stub-DOM (5 checks) only; Shawn's eyes have not seen it.

## What closes it

- Shell routes onCompose natively (previews already demonstrate the handoff) -> +0.2
- Real delivery / network layer -> +0.3
- Shawn's visual pass -> +0.3

## Verification

node syntax OK (room + registry), 5-check stub-DOM suite green (registry seed, WRITE MAIL handoff, no dead button without hook, cross-room add visibility).

## Files

- `HUB/app/js/people-registry.js` — `window.NayaPeople` (new, shared)
- `HUB/app/js/rooms/connections-adapter.js`
- `HUB/app/js/rooms/connections.js`
- `HUB/app/css/connections.css`
- `HUB/app/preview/build-connections-preview.py`
- Preview: `~/workspace/your_files/connections-preview.html`
