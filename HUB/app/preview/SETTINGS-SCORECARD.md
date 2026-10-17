# Settings — Hub Control Surface — Scorecard (Naya 4, 2026-10-02)

Branch: `naya4/room-02-reports-v2` (uncommitted working tree; parent will review/push).
Room identity: SLATE `#94a3b8`. No adapter — pure control surface: every control
has a real, persisted, visible consequence inside the preview. Preview:
`~/workspace/your_files/settings-preview.html`.

## Score: 9.8/10

| # | Lens | Score | Note |
|---|------|-------|------|
| 1 | Effectiveness | 10 | Every control does something real, live, and persisted: density re-spaces the page, reduce-motion kills animations (class + OS media query), sim-live starts/stops the EKG, masking swaps the identity card, notifications move the "N of 3 on" summary, reset clears the store and repaints everything. A SAVED pill flashes on every persist. No decorative controls. |
| 2 | Quality | 9.5 | EKG is now a readable monitor sweep (long dash segment, beat flash); switches are obsidian tracks with silver knobs and top-light catches; seg/reset are obsidian buttons with slate ignite. |
| 3 | Pro level | 10 | Living depth everywhere: sections are layered gradients with top-light catches, deep shadows, and hover lift; controls lift on hover; header carries a faint slate ambient. |
| 4 | Contrast | 9.5 | Cards lift off the background with 2px slate borders that ignite on hover; text is clean white/silver on dark. |
| 5 | Clarity | 10 | Honest labels throughout: stream marked "local demo, no network"; mask desc says page-local ("Masks your name on this page's identity card (local demo)"); saved-confirmation on every change; two-step reset with explicit arm state. |
| 6 | Congruency | 10 | One visual family: obsidian black buttons (`linear-gradient(180deg,#1b1b21,#0b0b0e)`, inset top-light, deep shadow), NEVER grey; active ignites slate, rest whispers it. |
| 7 | Color | 9.5 | Slate is the stable room identity — section borders, switch ignite, EKG stroke, avatar, kicker; never from list position. |

## Why not 10

- **-0.1 — Shawn's visual sign-off pending.** Scores cap below 10 without his eyes.
- **-0.1 — production shell wiring pending.** In the converged Hub shell, `naya.settings`
  must drive the app (density/motion/stream applied shell-wide, notifications wired
  to real events). The room exposes the contract; the shell owns adoption.

## Verification

- `node --check` on `settings.js`: OK
- CSS braces balanced (72/72); reduced-motion: both `.st-stage.st-reduced` class and
  `@media (prefers-reduced-motion: reduce)` targeting `.st-stage *`
- Type floor: no font-size under 11px (16px body / 11px labels)
- `node HUB/app/preview/tests/settings-smoke.js`: **45 pass / 0 fail** — toggle
  persistence across reloads, density/reduce-motion/sim-live classes, mask identity,
  notif summary math, two-step reset clearing store + repainting, aria role/labels,
  saved-pill confirmation, obsidian/reduced-motion/type-floor CSS markers
- Rebuilt preview + headless-Chrome screenshot reviewed by eye: sections deep and
  glassy, obsidian controls, EKG sweep reads as a monitor trace, saved pill hidden
  at rest

## Files (repo-relative)

- `HUB/app/js/rooms/settings.js` — `window.NayaRooms.settings(el, ctx)` (changed: saved pill + persist(), honest mask desc)
- `HUB/app/css/settings.css` — (changed: obsidian switches/seg/reset, living-depth sections, EKG sweep, header ambient, OS reduced-motion query, 10px→11px label floors)
- `HUB/app/preview/tests/settings-smoke.js` — created; stub-DOM suite
- `HUB/app/preview/build-settings-preview.py` — unchanged
- `HUB/app/preview/SETTINGS-SCORECARD.md` — this file (rewritten, single current section)

NOT committed, NOT pushed, NOT merged, NOT ratified — awaiting parent review.
