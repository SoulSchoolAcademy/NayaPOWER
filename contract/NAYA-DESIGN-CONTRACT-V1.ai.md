# THE NAYA DESIGN CONTRACT V1 — AI OPERATING LAW

> **STATUS: CANDIDATE — pending Shawn's ratification.** You follow it as operating law; where it
> conflicts with the human contract, the human contract wins. Where the contract marks a
> CONTRACTOR DECISION or CONFLICT FOR RATIFICATION, obey the recorded resolution and never invent your own.

North star: **Black ground. White light. Purple soul.** If your design doesn't read that way at a glance, it is wrong.

---

## 1. DECISION ORDER — RUN THIS SEQUENCE EVERY TIME YOU DESIGN

**FIELD → SPECTRUM → TYPE → SURFACE → COMPONENT → MOTION → TRUTH.**

1. **FIELD.** Start from near-black. `--bg:#0B0D12` for rooms, `#010103` for entrance/marketing. Never light. Never gray backgrounds. Everything luminous sits *in* darkness, never on light.
2. **SPECTRUM.** Assign each room its ONE accent from the table below — never two rooms alike. Chrome (buttons, actions) is purple; themed elements burn their own spectrum color on touch. Never theme color on chrome; never chrome color as flood.
3. **TYPE.** Body 18px, always, white 99%. Kicker/big headline 24px. Headline 18px. Sub/detail 14px. Hierarchy from SIZE, never color. Cormorant for crafted headers; Inter/system stack for UI. Score the copy /10 — invitation, not documentation.
4. **SURFACE.** Nothing flat, ever. Pick the elevation (L0 field → L4 overlay) and apply the depth formula: outer glow in theme color + `inset 0 1px #fff6` + deep drop shadow. Full width, no max-width caps on chassis/rooms, logo top-left.
5. **COMPONENT.** Build from the inventory: jewel (exact clip-path), black-heart button (DC-072/073), chips, eco-bottombar, drawers, toasts, cards. White edge light 1.5px+ visible at rest on every interactive element. Real `<button>` elements — never clickable divs. Affordances tell the truth (+ = add, ✉ = mail, › = navigates).
6. **MOTION.** Breathe, don't fidget: 4–78s ambient loops (union band until Shawn rules), low opacity ≤ 0.25, `cubic-bezier(.16,.84,.22,1)`, `.18s/.28s/.5s` interactions. `prefers-reduced-motion` kills all animation. Every animation is a truth claim.
7. **TRUTH.** "Live" means live. Demo labeled demo. Counts from real outcomes or absent. Never fake a connection, count, or heartbeat.

---

## 2. ROOM ACCENT TABLE — MEMORIZE, DO NOT IMPROVISE

| Room | Accent token | Hex |
|---|---|---|
| Today | `--magenta` | `#d86cff` |
| Reports | `--indigo` | `#6675ff` |
| Library | `--blue` | `#55b9ee` |
| Smart Doors | `--teal` | `#40d3bb` |
| Ledger | `--gold` | `#e8b64c` |
| Connections | `--orange` | `#ff9a5a` |
| Lists | `--purple` | `#9d75ff` |
| Mail | `--rich-orange` | `#ff7a3d` |
| Spaces | `--lime` | `#b8ee57` |
| Smart Grow | `--emerald` | `#55e39a` (contractor decision, pending Shawn) |

Spectrum flow for item sets: `purple → blue → emerald(green) → yellow(#f1d75a) → gold → orange → red → magenta → (cycle)`. Sequence MUST be a circular subsequence of this flow; start point is your beauty-first choice. Red = alarm only, never decorative. Amber/rose pink = forbidden everywhere.

---

## 3. TOKEN DISCIPLINE — USE THE CANONICAL `:root` SYSTEM

Copy the field + spectrum tokens from `naya-design-contract-v1.machine.json` (`tokens` object) into `:root`. Do NOT invent prefixed var families (`--ml-`, `--sc-`, `--cx-`…) and do NOT hardcode literal hexes in the same families as the tokens. Grayscale literals (`#fff`, `#8a8a96`, `#161618`…) are acceptable; chromatic literals are not — every chromatic color MUST be a token.

---

## 4. THE BUTTON RECIPE — FOLLOW EXACTLY

```
background: #050505 (really black; #000 acceptable)
color: #fff — ALWAYS white, with an icon. Colored text on buttons: NEVER. EVER.
border: 1.5px+ white edge light, visible at rest   [conflict X-1: briefing governs until ratified]
border-radius: 999px (pill)
min-height: 52px (52–55px)
box-shadow: inset 0 1px #fff2 + deep drop + theme glow
hover: lift translateY(-1px), glow intensifies — purple edge+glow for chrome, own spectrum color for themed
active: press 1px
```

Nav/sidebar items are NOT buttons: quiet at rest (white/neutral on obsidian); hover ignites each in its OWN spectrum color; active stays lit. Never all lit at once — the light travels.

---

## 5. BEFORE-YOU-SHIP GATES — ALL MUST PASS

### Gate A — The 10 pre-ship checks (verify by LOOKING at the rendered page)
1. [ ] I opened the rendered page and lived in it for a full minute before scoring.
2. [ ] I can see white edge light on every card and button WITHOUT hovering.
3. [ ] Hovering a themed element ignites its OWN color, not blanket purple.
4. [ ] All body text is white and readable; hierarchy comes from size (24/18/14).
5. [ ] The layout metaphor matches the thing (people scroll, products grid).
6. [ ] The copy reads like an invitation, not documentation — and I scored it /10.
7. [ ] The page breathes (light, glow, motion) but nothing distracts from reading.
8. [ ] Every button/icon does what its glyph promises; no dead or lying affordances.
9. [ ] No duplicated systems — anything that exists elsewhere is a link, not a copy.
10. [ ] I grepped the file and confirmed every claimed change is actually in it.

**Score ___/10. I back this because: ___. Below 9: back to the bench. No exceptions.**

### Gate B — Machine check
Run `python3 tools/design_law/check_design.py <file> --room <room>`. **Exit 0 required.** Fix every FAIL; warnings are repairs to schedule (D8/D10/D12).

### Gate C — Conflict discipline
- If the Design Code V1 and a shipped page disagree: record BOTH, do not silently pick. The briefing governs until Shawn ratifies.
- Conflict X-1 (button edge): white 1.5px+ at rest wins until ratified.
- Conflict X-2 (ambient timing): 4s–78s band until Shawn rules.
- Never invent: Smart Grow color, team colors, and the jewel-glow tail are recorded decisions — use them, don't re-derive.

---

## 6. WHEN BUILDING A ROOM — PROCEDURE

1. Identify the room's ONE accent from §2. Set `--room-accent` accordingly.
2. Scaffold the Hub shell (logo top-left, shared eco-bottombar, full width, no max-width).
3. Lay out by metaphor: ask "what is this?" first. People → vertical scroll. Browse → grid.
4. Apply type scale: body 18px white; 24/18/14 hierarchy; score the copy /10.
5. Build components from the inventory (§5 of the human contract). Jewel uses the EXACT clip-path `polygon(50% 0%, 86% 28%, 74% 82%, 50% 100%, 26% 82%, 14% 28%)`.
6. Motion pass: ambient 4–78s, interactions .18/.28/.5s, reduced-motion kill switch.
7. Truth pass: label every demo/simulated element; verify every count.
8. Run Gate A (look), Gate B (machine), then score yourself /10 with specifics. Ship only at 9+.

---

## 7. HARD STOPS — NEVER DO THESE

`user-scalable=no` · light backgrounds · body text under 18px · gray body text · colored button text · solid purple fills · solid non-black button fills · clickable divs · amber/rose pink · non-token chromatic colors · wrong room accent · max-width on chassis/rooms · links to app.nayanet.technology · a second system for an existing thing · fake liveness · capture surfaces in Hub chrome · decorative/lying glyphs · shipping below 9+ · claiming without grepping.

---

*End of AI operating law. The machine twin (`naya-design-contract-v1.machine.json`) is the checkable source of truth for tokens and patterns.*
