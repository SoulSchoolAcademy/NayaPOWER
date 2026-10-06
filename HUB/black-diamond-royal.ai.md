# Black Diamond Royal Interface System — AI builder spec

**Status:** PROPOSED / CANDIDATE. Not ratified. Build against it for drafts and proposals; do not claim compliance as law. Truth ceiling: CANDIDATE.
**Extends:** `HUB/DESIGN-CONTRACT.md` (Button Law §2.2, Living Depth Law §2.5, Spectrum Law §2.4). Net-new content only — never contradicts the seam; where a value moves, the reconciliation table below is the proposed change.

## 1. Elite test (applies to every surface)

A surface is elite iff an unfamiliar human can instantly answer: (1) what it is, (2) what to press, (3) what happens next. Scorecards test exactly this. Source: HMC standard.

## 2. Canonical palette (exact hexes, no approximations)

| Token | Hex | Role |
|---|---|---|
| obsidian | `#050507` | foundation / canvas |
| black-glass | `#0C0C11` | deep surfaces |
| deep-violet | `#26143D` | royal depth |
| naya-purple | `#8B3DFF` | intelligence / frequency / Naya |
| electric-amethyst | `#B57CFF` | bright center, highlights |
| diamond-white | `#F8F7FB` | primary text, clarity |
| platinum | `#C9C6D0` | structure, metallic edges |
| warm-gold | `#D8B978` | sparingly — premium highlights only |

Color semantics: black = depth, white = clarity, purple = intelligence, platinum = structure, gold = rare premium value. No uncontrolled rainbow. No random glow colors.

### Palette reconciliation (existing HUB/DESIGN-CONTRACT.md tokens → proposed)

| Existing token | Current | Proposed | Note |
|---|---|---|---|
| `--bg` | `#050507` | `#050507` | identical — no change |
| `--ink` | `#f8f7fb` | `#F8F7FB` | identical — no change |
| `--purple` | `#9d75ff` | `#8B3DFF` | **proposed move** |
| `--gold` | `#e8c766` | `#D8B978` | **proposed move** |
| (new) | — | `#0C0C11`, `#26143D`, `#B57CFF`, `#C9C6D0` | new tokens |
| `--muted`, spectrum set, room theme colors | unchanged | unchanged | untouched |

### Standing-color-standard resolution

The standing color standard (2026-10-04: black, white, purple, blues, green, gold; no amber, no rose pink; purple = accent/glow only, never solid fill) is preserved. Resolution: **black canvas wins**; the HMC hexes are the documented canonical values *within* that standard. One named exception is proposed (see §6): the Royal Purple Primary face is a gradient, never a flat fill, reserved for the single strongest action per area. Everywhere else purple remains accent/glow.

## 3. Six-layer formula (required for every premium control)

Build order, bottom to top:

1. `deep_base` — deep base surface: black glass, royal purple glass, or diamond white.
2. `metallic_frame` — metallic outer frame: platinum, or controlled gold-platinum edging.
3. `inner_rim` — inner illuminated rim: purple or white energy line inside the border.
4. `raised_face` — raised face: bevel or soft vertical gradient for physical depth.
5. `top_highlight` — directional highlight: brighter reflection near the top edge.
6. `shadow_aura` — floating shadow + aura: dark drop shadow plus restrained purple glow.

Target feeling: "That is a button. I want to press it." Buttons must read as physical objects rising from the interface.

## 4. Five button families

- **A. royal-purple-primary** — strongest action on screen. Examples: Play, Resume, Begin Journey, Continue. Face: top bright electric amethyst → center royal saturated purple → bottom deep violet. White text. Bright platinum edge. Purple outer aura. Largest / most luminous. Strongest hover lift. Constraint: **never two purple primaries in one area.**
- **B. black-diamond-primary** — strong but quieter. Examples: Install App, Explore, Share, Menu. Glossy obsidian-black body. White text. Platinum-white border. Subtle purple inner glow. Controlled aura. The most versatile premium family.
- **C. diamond-white-conversion** — purchase / membership / access. Examples: Unlock, Start Free Trial, Join, Log In. Diamond-white / silver face. Black text. Purple icon. Dark inner outline. Purple outer glow. White separates the financial action from the dark UI.
- **D. black-utility** — secondary / compact round. Examples: prev/next, rewind, volume, close. Black glass. Platinum circular edge. Purple/white icon. Small inner glow. Light bevel. Same royal family; must never compete with Play.
- **E. white-utility** — sparing; only when contrast demands it. Examples: Confirm, View Details.

## 5. Five states (every button implements all five)

- `default` — raised, polished, clearly clickable.
- `hover` — lift 2–3px, glow increases, top reflection brightens, border sharpens.
- `pressed` — moves inward 1–2px, shadow shortens, glow reduces, surface darkens.
- `active` — brighter border plus icon change / filled icon / indicator. **Never color alone** (accessibility).
- `disabled` — reduced contrast, no glow, no lift, clearly inactive. Never looks clickable when it isn't.

## 6. Shape standards

- Major buttons: 18–24px radius, 48–58px desktop height, 52–64px mobile height. Icon+label separation; no wrapped labels.
- Play: perfect circle, larger than neighbors, layered double/triple rim, bright purple center, white play symbol.
- Compact controls: perfect circle, 44–48px diameter minimum, consistent diameter within a row.
- Containers: 18–24px radius. Cards: 16–20px radius. Pills: fully rounded. Player controls circular. Borders: thin platinum edge + faint inner highlight. Shadows soft and directional. Glows controlled and localized.
- No flat boxes mixed with random curves. One studio, one language.

## 7. Typography (controls)

- Bold / semibold sans for labels. All caps for major commands. No tiny thin text. 2–3 words max (INSTALL APP, PLAY NOW, MAX LEVEL).

## 8. Glow discipline

- Tight glow at the edge, softer secondary aura, focal sparkle at corners. No neon haze. Gold = rare luxury reflection, never dominant. Glow color is semantically tied (purple for primary intelligence actions) — never random.

## 9. Spacing

- 8–12px compact, 10–16px major. Equal heights per row. No icons touching borders.

## 10. Accessibility (mandatory, in-spec)

- Touch targets 44–48px. Visible focus ring. Tooltips / labels. `prefers-reduced-motion` honored (depth survives without motion). Active state ≠ color-only. Clear disabled state.

## 11. LOCKED RULE

No important action may use a generic flat browser-style button. Every future major action uses a Black Diamond Royal family (A–E). A flat generic button on an important action is a **spec violation**, not a style choice.

## 12. Builder procedures

- Every new major CTA: pick family (A–E) → build six layers → implement all five states → verify 44–48px target → cap label at 2–3 words.
- Auditing existing surfaces: mismatched radii / flat boxes / generic buttons are violations of this spec; log them, don't silently restyle approved presentation files (byte-for-byte restoration boundary).
- Conflict on ratification: if the Royal Purple Primary exception is rejected at ratification, family A is re-specced with a black-diamond face + purple aura (no purple face).
- Enforcement follow-up (out of scope this run): a CI check asserting the six-layer structure, five-state CSS coverage, touch-target minimums, and no generic flat buttons on primary actions. Named here as a concrete follow-up, never faked.

**Source:** `~/workspace/distillations/hmc-batch-1/01-button-spec.md`, `02-hmc-standard.md` (HMC Button Spec + HMC Standard PDFs). Machine twin: `black-diamond-royal.machine.json`.
