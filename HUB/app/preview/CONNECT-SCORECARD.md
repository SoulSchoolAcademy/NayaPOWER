# Smart Connect (Smart Doors) — Scorecard

**Room:** Connect — "one brain, many doors" | **Worker:** Naya 4 | **Date:** 2026-10-02 (overnight elite pass)
**Branch:** `naya4/room-02-reports-v2` (worktree, NOT merged, NOT pushed, CANDIDATE — not ratified)
**Grounding:** canonical `BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json` (9 doors) via `ConnectAdapter.parse` — projection, never a copy. Nothing invented.

## Door-honesty gate: PASS ✅

- Adapter maps ONLY `LIVE_BOUNDED` / `LIVE_BOUNDED_EXISTING_CAPABILITY` → live. Verified against the canonical registry: exactly 2 live (DOOR-AI = A2A, DOOR-DATA = Supabase), 7 design (`REGISTERED_CONTRACT_ONLY`).
- Unknown/missing statuses fail CLOSED (design, "IN DESIGN") — a status the adapter cannot verify can never render a green light.
- Design CONNECT buttons open an honest inline notice ("Not yet wired… nothing was changed") — never a fake connection. Live MANAGE opens "Connection manager" — also truthful: no authority granted.
- Color is stable identity keyed by door id (director palette 2026-10-02), never list position (verified by reversed-order render).

## Score: 9.5/10

| # | Lens | Score | Note |
|---|------|-------|------|
| 1 | Effectiveness | 9.5 | Understand → unlocks → authority → one real action per door. Notice is honest; handler path (`ctx.onConnect`) preserved. |
| 2 | Quality | 9.5 | Living depth on boards/jewels/buttons; obsidian buttons w/ top-light + deep shadow; reduced-motion guard; type floor met. |
| 3 | Pro level | 9.5 | Native buttons, aria-labels per door, notice `role=status` + `aria-live=polite`, focus restored on dismiss, no notice stacking. |
| 4 | Contrast | 9.5 | Luminous white on near-black, door-colored glow on live; labels ≥11px. |
| 5 | Clarity | 9.5 | Plain-words per door, single button, footer states the connection≠authority law verbatim. |
| 6 | Congruency | 9.5 | One jewel family across all doors; rest whispers, hover/live ignites the door's own color. |
| 7 | Color | 9.5 | Stable per-door identity (GitHub purple, MCP indigo, A2A sapphire, Data cyan, Email lime, Calendar yellow, Voice gold, Web orange, Naya red). |

## Changes this pass (before 9.1 → after 9.5)

- **Buttons → obsidian law:** `linear-gradient(180deg,#1b1b21,#0b0b0e)` + `inset 0 1px 0 rgba(255,255,255,.16)` + deep shadow on `.cn-connect` and `.cn-notice-close`; door color ignites on hover/focus (was flat `#060807`).
- **Reduced-motion guard:** `@media (prefers-reduced-motion: reduce){ .connect-stage *{ animation:none !important; transition:none !important; } }` — was missing entirely.
- **Type floor:** pills + caps labels 10–10.5px → 11px; `cn-plain` 15.5px → 16px; notice button → 11px.
- **Accessibility:** notice gets `role="status"` + `aria-live="polite"` so screen readers announce the honest state.

## Verification

- `node --check` on `connect.js` and `connect-adapter.js` — pass.
- CSS brace balance 47/47; markers asserted by test.
- **New stub-DOM suite** `HUB/app/preview/tests/connect-smoke.js` (pure Node, no jsdom): **39/39 green** — adapter honesty (liveKind mapping incl. fail-closed on unknown), canonical registry (9 doors, 2 live = DOOR-AI/DOOR-DATA), render order/pills/strip, button consequences (onConnect called, notices, dismiss + focus restore, no stacking), color-by-id, CSS law markers.
- Preview rebuilt at `~/workspace/your_files/connect-preview.html`; screenshot reviewed with my own eyes (buttons, pills, jewels, strip all correct).

## Why not 10

- **His visual sign-off** — the remaining tenth is Shawn's eyes on the design.
- **Production shell wiring** — real OAuth/connection flows live in the Hub shell via `ctx.onConnect`; room-side is complete, system-side pending. The honest notice is the correct placeholder, not a hole.

## Files touched

- `HUB/app/css/connect.css` (obsidian buttons, reduced-motion, type floor)
- `HUB/app/js/rooms/connect.js` (notice `role=status` + `aria-live=polite`; no behavior change)
- `HUB/app/preview/tests/connect-smoke.js` (created)
- `HUB/app/preview/CONNECT-SCORECARD.md` (rewritten; supersedes all prior sections)
- Preview: `~/workspace/your_files/connect-preview.html` (rebuilt)
