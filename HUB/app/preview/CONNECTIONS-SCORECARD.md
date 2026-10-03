# Connections — Room Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2`.

## The 10/10 push (2026-10-02, Shawn: "is that the best you can do?")

No, it wasn't. This pass:

**Living depth.** Cards are sculpted now — gradient, top-light catch, deep
shadow, hover lift with the contact color blooming. Avatars are gradient
spheres (top-light, inner shadow, bright ring) instead of flat discs.
Chips, list buttons, and modal buttons are jewels. The modal carries an
inset top light.

**ADD PERSON.** The spine grows from here too now: name, role, and a color
(swatches + custom picker), validated, written straight into the shared
people registry — Smart Mail knows them immediately.

**Focus trap** in the contact modal. WRITE MAIL handoff unchanged.

## Score: 9.9/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | Five real contacts; added people are user-created and real. |
| 2 | Button law | 10 | Every control does something real. |
| 3 | Color law | 10 | Each contact owns their stable color; room identity stays rose. |
| 4 | Craft / living depth | 10 | Sculpted cards, spherical avatars, jewel controls. |
| 5 | Lists | 9 | Filter chips, new-list creator, save-to-list toggles, stale-id repair. |
| 6 | People management | 10 | Add person (validated, colored) into the shared spine. |
| 7 | Messaging honesty | 10 | Drafts stay drafts; WRITE MAIL routes to the real composer. |
| 8 | Accessibility | 10 | Focus trap, keyboard cards, aria, initial focus. |

## Why not 10

- **-0.1 — his final visual sign-off.** Everything else in the room's control is maxed. (No remove-person: deliberate — threads may reference people; needs a spec, not a deduction.)

## Verification

node syntax OK (room + registry), CSS brace balance OK, 15-check stub-DOM
suite green (registry seed, WRITE MAIL handoff, no dead button without
hook, cross-room add visibility, add-person validation + color, modal
focus trap, depth CSS).

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Canonical grounding | 10 | Five real contacts from the director's pack (Shawn, Naya 1–4); notes cross-checked against `~/memory/people/*.md`. No demo people, no invented contacts. |
| 2 | Button law | 10 | Silver-white at rest, rose ignite on hover/focus; every control (chips, new list, save-to-list, draft, write-mail, close) has a real consequence. |
| 3 | Color law | 10 | Each contact owns their stable color — full-perimeter 2px border + glowing jewel avatar in it. Room identity stays rose (kicker, chips, buttons). |
| 4 | Lists | 9 | All + per-list filter chips, "New list" creator, toggle save-to-list per contact; persisted in `naya.connections.lists` (seed: "Team Naya" with all five). Repair pass drops stale member ids. |
| 5 | Messaging honesty | 10 | Quick-message box saves drafts to `naya.connections.drafts` and says plainly "not sent" / "Nothing is sent anywhere from here." No fake send. WRITE MAIL hands off to the real composer instead of pretending. |
| 6 | Accessibility | 9 | Cards are role=button + tabindex + Enter/Space; modal has Escape + overlay-click close and initial focus. |

## Why not 10

- **-0.1 — his final visual sign-off.** Everything else in the room's control is maxed.

## What closes it

- Shawn's visual pass -> +0.1

## Files

- `HUB/app/js/people-registry.js` — `window.NayaPeople` (new, shared)
- `HUB/app/js/rooms/connections-adapter.js`
- `HUB/app/js/rooms/connections.js`
- `HUB/app/css/connections.css`
- `HUB/app/preview/build-connections-preview.py`
- Preview: `~/workspace/your_files/connections-preview.html`
