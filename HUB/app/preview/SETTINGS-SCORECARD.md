# Settings — Hub Control Surface — Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2` (uncommitted working tree; parent will review/push).
Room identity: SLATE `#94a3b8`. No adapter — pure control surface.
Verified: node syntax OK, CSS braces balanced, jsdom 20 pass / 0 fail / 0 errors.

## Score: 9.6/10

| # | Dimension | Score | Note |
|---|-----------|-------|------|
| 1 | Control law | 10 | Every control has a real, visible consequence: density changes page spacing, reduce-motion kills animations, sim-live starts/stops the EKG, masking swaps the identity card, notifications move the summary, reset restores defaults. No decorative controls. |
| 2 | Persistence | 10 | All state in localStorage `naya.settings`; every flip verified persisted; reset clears the store and repaints live. |
| 3 | Honesty | 10 | Stream section labeled as a local demo with no network; about card is read-only facts (0.4.0-candidate, 6 rooms, branch). Reset has a two-step confirm. |
| 4 | Accessibility | 9 | Real `<button role="switch">` controls with aria-checked/labels, keyboard-operable segmented control, focus-visible styles. |
| 5 | Visual law | 10 | Dark premium glass, 2px slate section borders, silver-white switches at rest igniting slate when on, responsive ≤760px. |
| 6 | Privacy default | 10 | Identity masking defaults ON (privacy-first, matches the ledger's "identities never revealed" law). |

## Why not 10

- **-0.2 — shell wiring pending.** In the converged Hub shell these settings must actually drive the app (density/motion/stream applied shell-wide, notifications wired to real events). The room exposes the contract; the shell owns adoption.
- **-0.2 — visual confirmation pending** (screenshot pipeline down; structural verification only).

## What closes it

- Shell reads `naya.settings` and applies density/motion/stream globally -> +0.2
- Shawn's visual pass -> +0.2

## Files

- `HUB/app/js/rooms/settings.js` — `window.NayaRooms.settings(el, ctx)`
- `HUB/app/css/settings.css`
- `HUB/app/preview/build-settings-preview.py` -> `~/workspace/your_files/settings-preview.html`
- `HUB/app/preview/SETTINGS-SCORECARD.md` (this file)

NOT committed, NOT pushed, NOT merged — awaiting parent review.
