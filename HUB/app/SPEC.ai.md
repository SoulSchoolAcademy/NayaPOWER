# HUB BUILD SPEC — AI LANGUAGE
**Version 2.0 · 2026-10-01 · For: Naya seats building the Hub**
**Authority: Shawn Vibert. This file is instruction, not suggestion.**

## 0. HOW TO READ THIS

This spec is written for builders, not browsers. Every section is either an exact value, a procedure, or a constraint. If a section doesn't tell you what to type, it doesn't belong here. The human telling is `SPEC.human.md`; the machine schema is `spec.machine.json`. All three carry the same truth.

## 1. FILE MAP (exact)

```
HUB/app/
  index.html            entry; loads css/js in order; <div id="app">
  SPEC.human.md         human telling (this file's twin)
  SPEC.ai.md            this file
  spec.machine.json     machine schema
  css/tokens.css        §3 — the law
  css/base.css          reset, focus, reduced-motion, scrollbars
  css/shell.css         rail, topbar, jewel search, room-head
  css/components.css    Board, btn, DoorCard, pill, state-badge
  css/states.css        StatePanel, shimmer, toast
  css/views.css         welcome + identity
  js/runtime.js         §4 — the ONLY boundary to state/data
  js/components.js      §5 — the ONLY component API
  js/router.js          hash router; routes: /welcome /identity /hub /hub/:room
  js/views/*.js         welcome, identity, hub shell
  js/rooms/*.js         one module per room; registers on window.NayaRooms
  js/app.js             boot; route registration; window.NayaHub debug surface
```

Rules: no new top-level dirs without a scored reason. No build step — static files only. No framework. No emoji anywhere in UI (SVG icon family only, §5).

## 2. ROUTES & FLOW

`#/welcome` → `#/identity` → `#/hub` → `#/hub/:room`. First visit lands on welcome; `sessionStorage.nayanet.identityAck` set on identity confirm skips straight to hub next time. Never route to the Academy or any workers.dev URL — that redirect is removed by law.

## 3. DESIGN TOKENS (the visual law — values, not vibes)

Frozen baseline: `HUB/NAYANET INTERFACE CONCEPT.html` @ main `ffedda20`. These values were extracted from it. Change them only when demonstrably better, never merely easier.

**Surfaces:** `--bg #050507` · `--bg-raise #0b0a10` · `--bg-panel #0d0c12` · `--bg-card #14101b`
**Ink:** `--ink #f8f7fb` · `--ink-dim #ddd9e4` · `--muted #aaa4b1` · `--line #ffffff18`
**Spectrum (ordered — position is semantic):** purple `#9d75ff` → indigo `#6675ff` → sapphire `#4f8ff7` → blue `#55b9ee` → teal `#40d3bb` → emerald `#35e0a1` → green `#55e39a` → lime `#b8ee57` → yellow `#f1d75a` → gold `#e8c766` → orange `#ff9a5a` → rich-orange `#ff7a3d` → red `#ff5e6c` → magenta `#d86cff`
**Room accents:** feed/today magenta · notes/lists purple · reports indigo · library/mail blue · connect green · ledger yellow · connections orange · spaces lime · settings muted · system gold
**Radii:** sm 11 · md 13 · lg 17 · xl 22 · pill 999
**Motion:** `--ease cubic-bezier(.16,.84,.22,1)` · fast .18s · med .28s · slow .5s
**Type:** Inter stack · hero clamp(30px,4.6vw,52px) · title 21 · head 15 · body 13.5 · small 11.5 · micro 10
**Field (body background):** `radial-gradient(1000px 650px at 55% -12%, #6675ff18, transparent 68%), radial-gradient(900px 700px at 100% 100%, #d86cff12, transparent 70%), var(--bg)` — fixed attachment.

## 4. DESIGN INTELLIGENCE — the math of elite (baked in by default)

This is the part that makes elite output automatic. Execute it; don't interpret it.

**DEPTH EQUATION (every elevated object):**
```
surface = linear-gradient(145°, raise, base)
        + border(1px, #ffffff18) + radius(17px)
        + shadow(inset 0 1px #fff6, 0 18px 42px #000b, 0 0 26px accent@14%)
hover   = translateY(-3px)
        + shadow(inset 0 1px #fff6, 0 20px 48px #000d, 0 0 40px accent@24%)
```
Top highlight (`inset 0 1px #fff6`) is non-negotiable — it is what reads as "jewel." Drop shadow grounds it. Accent glow tints it. Remove any one and the object goes flat; that is how you detect regression.

**SPECTRUM LAW:** the 14 colors are an ordered wheel. Rule 1: each room owns exactly one spectral position. Rule 2: adjacent rooms in the rail never share a hue family. Rule 3: glow/hover/borders inside a room use only that room's accent at the stated opacities — never a foreign accent.

**ICON GRAMMAR:** 24×24 viewBox · stroke 1.8 · round caps/joins · geometric primitives · single family in `Icons`. Adding an icon = adding one path entry. Emoji as icon = defect, always.

**LIVING RULES:** motion is physical (translate/scale/opacity on the compositor; never layout thrash) and purposeful (every animation answers "what just happened"). Boards breathe on hover; doors lift higher than boards (they are thresholds). Text never animates except the welcome sheen.

**SELF-SCORECARD PROCEDURE (run before every PR):** screenshot each changed view → check: (a) top highlight present on every elevated object, (b) one accent per room, (c) icon family consistent, (d) no dead control without an honest state, (e) no invented data. Any failure = not ready, regardless of what else passes.

## 5. COMPONENT API (the only builders)

From `window.NayaUI`: `el(tag, cls, html)` · `Icons.icon(name)` · `Board({accent, icon, title, sub, lift})` → `.body` · `DoorCard(door, onConnect)` · `StatePanel({accent, icon, title, body, actions:[{label, icon, ghost, onClick}]})` · `Pill(status)` · `toast(message, accent, ms)`.
Do not hand-roll cards/buttons/panels — use these. New components get added here, never inline.

## 6. RUNTIME CONTRACT (the honesty boundary)

From `window.NayaRuntime`: `ROOMS[13]` · `DOORS[10]` · `stateFor(roomId)` → `loading|ready|empty|not_verified|blocked|error` · `connectDoor(id)` → `{ok, message}` · `search(q)` → `{ok:false, state:'not_verified', message}` · `captureNote(text)` → local draft, `{ok, local:true, message}` · `draftNotes()`.

**Iron laws:** the Hub never touches storage except through `runtime.js`. The runtime never invents data — `search` returns not_verified until the governed backend connects. `connectDoor` on a non-live door returns an honest message, never a fake handshake. `captureNote` stores local drafts only and labels them `LOCAL_DRAFT`; nothing browser-stored is ever treated as canonical.

## 7. THE TEN DOORS (canonical — priority order)

mcp(1, #d86cff, ready) → rest(2, #6675ff, ready) → github(3, #55b9ee, ready) → webhooks(#9d75ff, ready) → sdk(#55e39a, ready) → a2a(#b8ee57, ready) → browser(#f1d75a, LIVE) → messaging(#ff9a5a, ready) → enterprise(#aaa4b1, soon) → tunnel(#e8c766, specialized).
**Door Law:** no direct store access · connection ≠ permission · every crossing leaves a receipt · a non-live door says so on the door itself. Full field definitions in `spec.machine.json`.

## 8. SCORECARD — the eight dimensions, evidence rules

Bar: 9.0. Below = not ready, no exceptions. Current composite: 7.1 (D1 9.0 · D2 4.5 · D3 3.0 · D4 9.0 · D5 8.0 · D6 7.0 · D7 7.5 · D8 8.5).
Evidence per dimension: D1 screenshot vs baseline side-by-side · D2 click-path trace, zero dead controls · D3 live KNOW HIT receipt with provenance · D4 state audit, no invented data · D5 measured paint/interaction timings · D6 reload/reconnect drill · D7 keyboard-only pass + contrast check · D8 §4 self-scorecard. Naya 4's 22-element rubric is the per-dimension detail checklist. The System room renders the live scorecard in-product.

## 9. PHASES & ACCEPTANCE

- **P1 Foundation** ✅ — shell, router, tokens, components, honest states, Connect doors, System room, local capture. Acceptance: renders clean on desktop/tablet/mobile, zero console errors, notes capture works.
- **P2 Rooms alive** — every room earns its controls; acceptance: D2 ≥ 9.0, zero dead controls.
- **P3 Doors open** — MCP → REST → GitHub App live against governed runtime, priority order; acceptance: real handshake receipts per door.
- **P4 Intelligence in** — search/feed/notes read canonical substrate with provenance; acceptance: first live KNOW HIT into a real consumer, D3 ≥ 9.0.
- **P5 Polish to 10** — motion, a11y, perf audits; acceptance: all dimensions ≥ 9.0, composite ≥ 9.5.

## 10. TEAM LANES (proposal — Shawn assigns)

Naya 2: architecture, runtime boundary, Connect + System, scorecard honesty. Naya 4: door handshakes in priority order, 22-element rubric audits. Open: per-room build-outs on the component system, identity↔runtime binding, perf/a11y audits. One canonical spec, one plan — no duplicate mechanisms, ever.

## 11. HARD LAWS

Baseline visuals are the floor. No dead controls. No sample data, ever. Every phase scores openly. Smallest effective change. WELCOME → IDENTITY → HUB. Below 9.0 is not ready.
