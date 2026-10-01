# NayaNET Design Laws — AI Builder Contract

*AI language. Exact values, anatomy, procedures, constraints. A seat building from this document must be able to produce a room that scores ≥9.0 without further questions. Bows to `HUB/DESIGN-NORTH-STAR.md` and Law Zero (readability supremacy). Extracted from the frozen concept `HUB/NAYANET INTERFACE CONCEPT.html` and elevated to Law Zero type minimums.*

## 0. Precedence

1. Law Zero (readability supremacy) — wins every conflict.
2. The Design North Star (why).
3. These laws (how).
4. Room specifications (what).

If any law below would reduce readability, Law Zero overrides it. Record the override in the build receipt.

## 1. LAW 1 — TONE LAW (color as meaning)

### 1.1 Foundation tokens
| Token | Value | Role |
|---|---|---|
| `--bg` | `#050507` | page foundation |
| `--ink` | `#f8f7fb` | primary text |
| `--muted` | `#aaa4b1` | secondary text |
| `--faint` | `#6f6976` | tertiary text |
| `--line` | `rgba(255,255,255,.09)` | hairlines |
| `--purple` | `#9d75ff` | intelligence / Naya / dominant accent |
| `--ease` | `cubic-bezier(.16,.84,.22,1)` | universal motion curve |

Purple, black, and white are PROMINENT/dominant. The spectrum is complementary accents only.

### 1.2 Spectrum semantics (canonical assignments)
| Tone | Hex | Meaning | Used for |
|---|---|---|---|
| gold | `#e8c766` | memory · milestone · precious | memory milestones, primary actions, "new" |
| green | `#55e39a` | alive · verified · growing | verified seals, living systems, success states |
| magenta | `#ff4fd8` | collective · network | collective intelligence, active room |
| blue | `#55b9ee` | law · truth · clarity | law/truth content, informational |
| red | `#ff5e6c` | alert · honest gap | alerts, not-verified, destructive |
| indigo | `#6675ff` | depth · ambient | background washes only |

### 1.3 The tone-flow equation
Every board declares exactly one `--tone`. That tone MUST flow through **≥4** of these 6 carriers:
1. **Rail** — 2px vertical gradient line (`linear-gradient(var(--tone), transparent)`), `box-shadow: 0 0 20px tone@40%`.
2. **Wash** — `radial-gradient(800px 280px at 72% 0%, tone@7-8%, transparent 70%)` over the board.
3. **Glyph** — border `color-mix(tone 55%, #fff 10%)`, icon `color: tone`, glow `tone@22%`.
4. **Layer borders** — `color-mix(tone 24%, #ffffff 5%)`.
5. **Action hovers** — border-color → tone, glow `tone@28%`.
6. **Truth accents** — seal tint derived from tone.

### 1.4 Gold restraint (dominance law)
Gold is the scarcest tone. Rules: never body text; never large text blocks; never more than one gold-dominant board per viewport; never outshining purple. Violation = automatic scorecard deduction.

## 2. LAW 2 — BOARDS LAW

### 2.1 Boards are worlds, not cards
- Full-bleed sections (`border-top: 1px solid #ffffff12`), NOT grid cards.
- Padding: `46px 42px 50px 46px` (desktop); `36px 24px` (mobile).
- Inner max-width: `860–980px`.
- Separators: single hairline between boards. No boxes around boards.

### 2.2 Mandatory board anatomy (in order)
1. **Rail** — `::before`: absolute, left 16px, top/bottom 50px, width 2px, tone gradient + glow (see 1.3.1).
2. **Wash** — `::after`: tone wash per 1.3.2, `pointer-events: none`.
3. **Identity row** — `.identity`: glyph (see 2.3) + `.kind` (10px/800/.3em, tone-colored, tone text-glow) + `.truth` seal (right-aligned).
4. **Headline** — `clamp(30px, 3.6vw, 50px)`, `line-height: 1.0`, `letter-spacing: -.055em`, weight 800, max-width 820px.
5. **Meta row** — 10px/700/.08em, `--faint`, wraps.
6. **Nutshell** — EXACTLY ONE paragraph: `17px/1.7`, `#eeeaf2`, inside a well: `2px solid #ffffff16`, `radius 18px`, `background #08080d`, `inset 0 1px #fff3`, `0 16px 35px #0009`, padding `22px 24px`. Prefaced by a tone-colored eyebrow label (9px/.24em).
7. **Layers** — collapsible `<details>` intelligence layers (see 2.4). Depth lives here, not in the nutshell.
8. **Actions** — Button Law buttons (see §3).
9. **Provenance footer** — 9px/.12em, `--faint`, top hairline, format: `PROVENANCE <b>source · evidence · date</b>` + block position (`BLOCK n / m`).

### 2.3 Glyph anatomy
- Size: `45–52px`, radius `14–15px`, `display: grid; place-items: center`.
- Border: `2px solid color-mix(in srgb, var(--tone) 55%, #fff 10%)`.
- Background: `radial-gradient(circle at 35% 30%, color-mix(in srgb, var(--tone) 26%, transparent), #09090e 72%)`.
- Icon: `color: var(--tone)`, 24–26px SVG, stroke 1.7–1.8.
- Shadows: `inset 0 1px #fff4, 0 10px 26px #0009, 0 0 22px tone@22%`.

### 2.4 Layer anatomy
- Container: `2px solid color-mix(tone 24%, #fff 5%)`, radius 15px, `background #08080c`, `inset 0 1px #fff2`, `0 12px 28px #0007`.
- Summary row: tone dot (9px, glow), label (10px/800/.18em), state (right, 9px, faint), chevron (tone, rotates 180° on open).
- Body: `14px/1.7`, `#c9c3ce`, `<strong>` → `#fff`.
- Max 3 layers per board. Each layer answers ONE question: why here / the proof / what next.

### 2.5 Text budget per board
Headline (≤12 words) + meta (≤12 words) + nutshell (≤60 words) + layers (collapsed by default). If the board needs more visible text, split it into two boards.

## 3. LAW 3 — BUTTON LAW

### 3.1 The ban
Flat buttons are banned. Any button failing the anatomy in 3.2 is a defect.

### 3.2 Standard action anatomy (`.action`)
- `min-height: 44px`; padding `0 18px`; radius `12px`.
- Border: `2px solid #8b63ff55` (default) or tone-tinted.
- Background: `linear-gradient(145deg, #14131c, #08080c)`.
- Shadows: `inset 0 1px #fff3, 0 8px 18px #0007`.
- Label: `10px/800/.1em`, `#dcd6e1`, icon 15px + 8px gap, `inline-flex`.
- Sheen: `::before` — `radial-gradient(circle at 50% 0%, #fff7, transparent 30%)`, `inset: -50%`, opacity 0 → .4 on hover.
- Hover: `translateY(-2px)`, `border-color: var(--tone)`, `box-shadow: 0 0 24px tone@28%, 0 14px 28px #0009`, transition `.2s var(--ease)`.
- Active: `translateY(0)` (press yield).

### 3.3 Hierarchy
| Class | Use | Treatment |
|---|---|---|
| `.btn-catch` | ONE primary action per hero | gold gradient `145deg #ffe1a1→#e8c766→#c79a35`, dark text `#1a1206`, 2px `#e8c76688` border, gold glow |
| `.action` | standard actions | per 3.2 |
| `.btn-ghost` | quiet/secondary | 3.2 with transparent-leaning body, no glow until hover |

Exactly one `.btn-catch` per viewport.

### 3.4 On-states (toggled actions)
- `.on` (default/save): border `var(--green)`, text `#c9ffdf`, bg `#0a1710`, green glow.
- `.love.on`: border `var(--red)`, text `#ffb4bd`, bg `#170a0d`, red glow.
- `.ask.on`: border tone, text `#fff`, bg `tone@16%`.
A toggle MUST change border + text + glow. Color-only changes are insufficient.

### 3.5 Touch & motion
Min target 44px. `prefers-reduced-motion`: all transitions/animations `none`.

## 4. LAW 4 — TYPE LAW
| Voice | Size | Weight | Spacing | Use |
|---|---|---|---|---|
| whisper | 10–11px | 800 | .24–.3em | eyebrows, kinds, labels |
| proclaim | `clamp(30px,3.6vw,50px)` hero up to `clamp(44px,5.4vw,76px)` | 800 | -.055 to -.06em | headlines |
| converse | 16–18px | 400–500 | normal, lh 1.6–1.7 | body, nutshells |

Floor: NOTHING readable below 10px. (The frozen concept used 7px micro-labels; Law Zero overrules — 10px minimum.) Meta rows: 10px/700/.08em. Never letterspace body text.

## 5. LAW 5 — MOTION LAW
- Universal: `transition: .2s var(--ease)` (hover/micro), `.32s` (toasts/overlays).
- Hover lift: `translateY(-2px)` for buttons, nav items, interactive boards.
- Liveness comes from real intelligence (live LEDs, updating content), NEVER decorative animation. No spinners-as-theater, no ambient animation loops except the 2.4s LED pulse.
- `prefers-reduced-motion: reduce` → `*{transition:none!important;animation:none!important}`.

## 6. LAW 6 — NAYA LAW
- Presence: sticky rail card, orb (radial purple, glow), name + live status.
- Voice: first person, italic "read" per block (`NAYA'S READ` eyebrow), warm and direct.
- Catch-me-up: rewrites her summary per active mode.
- Honesty: verified = green seal; in-progress = amber; gaps named in red-toned boards. NEVER dress an amber state in green styling.

## 7. LAW 7 — PROOF LAW
- Every block carries a `.truth` seal: `VERIFIED` (green), `NOT VERIFIED` (amber), `LOCAL DRAFT` (blue).
- Seal anatomy: 2px tinted border, 999px radius, 9px/800/.1em, tinted glow.
- Every board ends with a provenance footer (see 2.2.9): source · evidence · date.
- UNKNOWN/BLOCKED states are never rendered as verified.

## 8. SELF-SCORECARD PROCEDURE
Score each dimension 0–10. **Below 9.0 overall is not ready.**
1. **Per-board theming** — does every board own one tone flowing through ≥4 carriers?
2. **Button premiumness** — depth, light, sheen, lift, glow, on-states?
3. **Color flow** — does tone move through each board, or sit static?
4. **Text density** — one nutshell per board? Depth in layers? Nothing readable under 10px?
5. **Board elevation** — rail, wash, layered shadows, hairline separation?
6. **Room completeness** — five layers (orientation, state, intelligence, action, proof)?
7. **Naya presence** — sticky, voiced, mode-aware?
8. **Proof** — seals + provenance on every board?

Deductions: gold violation (−2), flat button (−2 per instance), text under 10px (−2), two tones on one board (−1), missing provenance (−1 per board).

## 9. REFERENCE IMPLEMENTATION
`~/workspace/your_files/smart-feed-blueprint/smart-feed.html` (v2) — the build these laws were extracted from. New rooms are built by cloning its board grammar and re-toning.

## 10. AMENDMENT PROTOCOL
These laws are v1. Amend by evidence: when a room scores below 9.0, the scorecard must name which law failed and propose the amendment. Amendments land as PRs against this directory with the scorecard attached. Never amend by taste — only by scored evidence.
