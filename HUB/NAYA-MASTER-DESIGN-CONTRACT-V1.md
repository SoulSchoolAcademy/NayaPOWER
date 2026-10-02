# NayaNET Master Design Contract V1

**Status:** HUMAN-DIRECTOR-DIRECTED — 2026-10-02
**Version:** 1.0
**Authority:** Human Director → this contract → living room contracts → implementation
**Supersedes as the single reference:** the scattered design-intelligence pieces are converged here — v1.4 canon (#1321, folded verbatim), Builder Field Manual V1 (#1330), `00-HUB-HOME.md` §3 baseline, Design Intelligence Standard v1.3, the 40-block canon. Nothing here competes with those; this IS those, made official and complete.

**The promise:** there is no guessing. The exact colors, the color flows, the button anatomy, spacing, dos and don'ts — everything — is in this document. And no work reaches Shawn until it has passed the self-evaluation procedure in Part 4.

---

## PART 1 — THE LAWS

Laws are ranked. A higher law overrules a lower one, always.

### LAW ZERO — Readability supremacy
No glow, no depth effect, no color choice, no animation may ever reduce readability. If it's beautiful but hard to read, it's wrong. This outranks everything.

### The ten laws
1. **PURPOSE BEFORE INTERFACE** — resolve the human's real outcome before selecting any page, component, layout, or interaction.
2. **DISTILL BEFORE DISPLAY** — raw intelligence is not presentation; decide what matters now, then disclose progressively.
3. **RECOGNITION BEFORE RECALL** — the human never hunts for where something lives or decodes unfamiliar language.
4. **ONE OBVIOUS NEXT ACTION** — every surface answers: where am I? what matters? what can I do? what happens next?
5. **STATE MUST BE PERCEPTIBLE** — no control is finished without rest, aware, hover/focus, press, processing, success/failure, consequence.
6. **BEAUTY IS FUNCTION** when it improves comprehension, trust, or emotion. Beauty that obscures function is failure.
7. **COMPLEXITY BELONGS IN THE MACHINE** — the smarter the system, the simpler the human's experience.
8. **DESIGN SYSTEMS ARE MEMORY** — every verified discovery becomes retrievable intelligence. Never rediscover; never re-argue.
9. **THE PRODUCT FEELS LIKE ONE THING** — one intelligence, many rooms, one grammar. Never a committee of components.
10. **DESIGN MUST LEARN** — design isn't finished at implementation. Observe, measure, verify, preserve, repeat.

### L0 — The posture
The canon is not a ranking and not a template. Study the best, extract the principle, do it ten times better. The canon is the floor of awareness, not the ceiling of ambition. 10× is the ambition — only measured evidence earns the claim.

### The benchmark-to-beyond loop (ratified)
RESEARCH_FRONTIER → DECOMPOSE_CAUSAL_PRINCIPLES → CROSS_REFERENCE_CURRENT_NAYA → PRESERVE_CURRENT_SUPERIOR_STRENGTHS → SYNTHESIZE_COMPATIBLE_BEST → GENERATE_BEYOND_BENCHMARK_OPTION → TEST → INDEPENDENT_VERIFY → CAPTURE_PROVEN_IMPROVEMENT → REPEAT.

### The North Star
NayaNET is the human interface to a living intelligence. One intelligence. Many doors. One human at the center. No unnecessary burden.

---

## PART 2 — EXACT VISUAL SPECIFICATION

### 2.1 Color

**The obsidian stack (the only neutrals):**

| Token | Hex | Use |
|---|---|---|
| World | `#0B0D12` | the canvas — everything sits on this |
| Raised | `#12151D` | cards, panels, drawers |
| Elevated | `#171B25` | popovers, modals, the topmost layer |
| Precision edge | `#252B39` | 1px edges on raised surfaces |
| Primary text | `#F5F7FB` | body text, always |
| Secondary text | `#AAB2BF` | supporting text, never below readable contrast |

Two blacks for surfaces, not five. Restraint is the law.

**The semantic spectrum (each color has exactly ONE job):**

| Color | Hex | The ONE job | Where it lives |
|---|---|---|---|
| Emerald | `#55e39a` | active / available / healthy | live states, verified, things working |
| Gold | `#e8b64c` | consequence / value | the rarest accent — if gold appears, something extraordinary happened |
| Red | `#ff5a6e` | blocked / failed | errors, blocked states — never decorative |
| Purple | `#9d75ff` | Naya's signature | primary actions, Naya presence, the emblem's light |
| Magenta | `#d86cff` | human significance | the human's own things — their day, their words |
| Sapphire | `#55b9ee` | knowledge | library, learning, known things |

**Room themes** (identity, from the registry): Feed emerald `#55e39a` · Today magenta `#d86cff` · Reports indigo `#6675ff` · Library sapphire `#55b9ee` · Connect emerald `#55e39a` · Ledger gold `#f1d75a` · Connections orange `#ff9a5a` · Lists purple `#9d75ff` · Mail sapphire `#55b9ee` · Spaces lime `#b8ee57` · Settings neutral `#aaa4b1`. Known collisions (Feed/Connect, Library/Mail) differentiate by icon glyph; token fix is a director decision.

**The color flows (how color moves):**

1. **Hierarchy flow** — the eye travels in this order: white (text) → room theme (identity) → semantic color (state) → gold (the extraordinary). Color draws the eye in order of importance. If everything glows, nothing does.
2. **State flow** — a component's color changes only with its state, and only through this path: rest (muted) → hover (brightened, lifted) → press (compressed) → processing (theme pulse, honest) → success (emerald, brief) → failure (red, with the reason in words). Color never jumps without a state reason.
3. **Theme flow** — the room's theme enters at the threshold (drawer jewel, header edge) → recedes to accents on state → returns at primary actions. It breathes with the room. It never floods the canvas.

### 2.2 Typography

| Role | Size | Weight | Use |
|---|---|---|---|
| Hero | `clamp(30px, 4.6vw, 52px)` | 800 | the one headline per view |
| Title | 23px | 800 | room/section titles |
| Head | 17px | 700 | card heads, emphasis |
| Body | 16px minimum, 17–18px target | 400 | primary content — generous or it fails |
| Secondary | 14–15px | 400 | supporting content |
| Label | 11px minimum | 700, uppercase, tracked | labels — never below 11px |

*(Body target 17–18px vs 16px floor: open director question. Until ruled, 16px is the floor, 17–18px the target.)*

One family (Inter, system fallback). Never pale-purple body copy. Line-height 1.5–1.6 for body. Every element earns its place — remove words before styling them.

### 2.3 Spacing

The scale: **4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96.** Never arbitrary values.

- Section rhythm: 48–64
- Card padding: 24
- Related groups: 16
- Micro-gaps: 8
- Generous negative space is a feature — the feed breathes like a social app, not a dashboard grid.

### 2.4 Depth

The obsidian depth law: **material core → exact edge light → restrained specular highlight → believable cast shadow → semantic aura → state amplification.**

Depth first. Light second. Glow last. No giant blur clouds. No uniform neon outlines. No glow used to hide weak geometry.

### 2.5 Buttons — exact anatomy

**Primary:**
- Padding `14px 28px`, min-height 48px, radius `999px` (pill) or 13px
- Font 17px / 800, white text, purple `#9d75ff` (solid or subtle gradient)
- Label is verb-first: "Verify now," "Open the proof," "Save changes"

**The seven states (every consequential button, no exceptions):**

| State | Exact visual |
|---|---|
| Rest | as specified above |
| Hover/aware | `translateY(-1px)`, glow intensifies, cursor pointer |
| Focus | visible ring: 2px outline, offset 2px (keyboard users) |
| Press | `scale(0.97)`, glow softens — it feels physical |
| Processing | disabled appearance + honest indicator (spinner/progress); label may become "Verifying…" |
| Success | brief emerald shift (border/glow), then the consequence is visible |
| Failure | red state + the reason in plain words + a recovery action |

**Secondary:** obsidian fill `#12151D`, 2px accent-tinted border, white text. Same seven states, quieter.
**Destructive:** red-tinted, rare, always with confirmation.

### 2.6 Icons

The executable jewel system (`HUB/app/js/icons.js`): Set A jewel marks (12: 11 rooms + the Naya emblem) for identity moments; Set B action glyphs (obsidian chips) for controls. Scale steps 96/64/48/32 — never in-between, never stretched. One icon per idea. Glow = meaning. Never flat, never emoji, never stock. Shawn's crystal logo is the Naya emblem (`HUB/app/assets/`).

### 2.7 Motion

Motion communicates **truthful state only**. Durations: fast `.18s`, medium `.28s`, slow `.5s`. Easing `cubic-bezier(.16,.84,.22,1)`. Transform/opacity only. Nothing moves for decoration. Every animation has a reduced-motion equivalent. Auto-playing carousels are rejected on sight.

### 2.8 The shell (director-refined)

Two corner buttons only — top-left opens the rooms drawer, top-right opens the nav drawer. The left drawer holds the rooms (jewel marks; Smart Feed is NOT listed — it is the main show). The right drawer holds HOME, NAYA POWER, 5-DAY CHALLENGE, ENTER FREE, POWERCAST, WHITE PAPER, ABOUT US, LOGIN. First login lands directly in the feed: full-bleed, social-style intelligence scroll. The mode switcher (Collective / Personal / Activity) docks into one sticky zone — never two competing sticky elements.

---

## PART 3 — DOS AND DON'TS

### Do
- DO-01: Make every control's possible action visible before it is touched.
- DO-02: Close every action loop with immediate, legible feedback.
- DO-03: Map controls to consequences the way the human already expects.
- DO-04: Keep system status visible at all times.
- DO-05: Prefer recognition over recall in every choice.
- DO-06: Prevent errors with constraints; design recovery before writing error copy.
- DO-07: Make navigation self-evident; a pause to decode it is design debt.
- DO-08: Remove every unnecessary word.
- DO-09: Ask what can be removed before asking what can be added.
- DO-10: Make every control tell the truth about what it does.
- DO-11: Specify every microinteraction as trigger, rule, feedback, loop.
- DO-12: Use motion only to communicate state change.
- DO-13: Earn attention: subdue chrome so the work is primary.
- DO-14: Keep placement predictable across rooms.
- DO-15: Size and space touch targets for the real device and input.
- DO-16: Cut choices to the minimum that serves the goal.
- DO-17: Compress meaning into icons before adding any decoration.
- DO-18: Assign every color one fixed meaning and never break the wiring.
- DO-19: Disclose progressively: what matters now first, depth on demand.
- DO-20: Design from the human's goal; never expose the implementation model.
- DO-21: Establish hierarchy first with spacing and typography, then style.
- DO-22: Prefer direct manipulation where the mental model supports it.
- DO-23: Keep onboarding light; gate on first-use comprehension.
- DO-24: Default intelligently so configuration disappears.
- DO-25: State the 10x delta in one sentence and evidence it in the artifact.

### Don't
- DONT-01: Do not hide system status; never leave the human guessing whether an action worked.
- DONT-02: Do not force recall of locations, commands, or prior state that recognition could supply.
- DONT-03: Do not explain errors the system could have prevented with constraints.
- DONT-04: Do not ship navigation a human must stop to decode.
- DONT-05: Do not add words the human must read to do the obvious.
- DONT-06: Do not ship a control that promises more than the system delivers.
- DONT-07: Do not animate without a state change to communicate.
- DONT-08: Do not leave triggers undiscoverable.
- DONT-09: Do not give every element equal prominence.
- DONT-10: Do not confuse density with clutter — or emptiness with simplicity.
- DONT-11: Do not manufacture variable reward.
- DONT-12: Do not let investment mechanics exploit; stored value must visibly pay the user back.
- DONT-13: Do not decorate icons that do not yet carry clear meaning.
- DONT-14: Do not break the fixed color vocabulary for emphasis or novelty.
- DONT-15: Do not dump information and call it transparency.
- DONT-16: Do not add delight before usability is verified.
- DONT-17: Do not maximize engagement for its own sake.
- DONT-18: Do not build tutorials for what interaction itself can teach.
- DONT-19: Do not accumulate features before subtracting.
- DONT-20: Do not present raw intelligence as finished presentation.
- DONT-21: Do not let layout invent structure.
- DONT-22: Do not freeze as static documents what should be live and manipulable.
- DONT-23: Do not keep chrome the object itself could replace.

---

## PART 4 — THE SELF-EVALUATION PROCEDURE

**No work reaches Shawn until it has passed this procedure.** This is how a builder looks at their own work before sending it.

### Step 1 — Render it like Shawn will
Open your frozen commit full-screen. Not the code — the experience. If you can't render it, you can't evaluate it; do not send what you haven't seen.

### Step 2 — The four tests
- **1 second:** where does the eye land? (If nowhere: no focal region — fail.)
- **3 seconds:** do I know where I am, what matters, and what I can do?
- **30 seconds:** can I take the obvious next action without reading everything?
- **Squint:** is the hierarchy still visible? (If not: fail.)

### Step 3 — Measure against the exact spec
- Type: body on 16px floor / 17–18px target? Labels ≥ 11px? (Measure, don't eyeball.)
- Color: every color on its ONE job? (Name each color's job out loud.)
- Spacing: on the 4/8/12/16/24/32/48/64 scale? (No arbitrary values.)
- Depth: obsidian law followed? (Not flat + bordered.)
- Buttons: verb-first? Seven states? (Check each consequential button.)

### Step 4 — The checklist (Builder Field Manual § "quality checklist")
All ten boxes. Any unchecked box = not ready.

### Step 5 — Score honestly
D1–D8, 0–10, no averaging. D1 = 10.0 required for Signature; D2–D8 ≥ 9.5. Write the scores down with one line of evidence each. **A score without evidence is not a score.**

### Step 6 — The gate
Show Shawn **only** if: every hard gate passes, D1 is honestly 10 (9.5+ minimum for non-signature), and you can name what you deliberately left out and why.

### The honesty law
Your self-score is a **diagnostic, not a pass**. Naya 1 judges independently. If you wouldn't bet your reputation on the score, iterate — don't send it.

---

## PART 5 — COMPOSITION GRAMMARS

- **Main show (feed):** presence → recognition → the river (one hero region, the rest subordinate) → sticky mode dock → Ask Naya. Full-bleed scroll. No dashboard grid.
- **Room:** identity + mode → orientation (one line) → intelligence → why-now → actions → evidence (progressive).
- **Drawer:** jewel + label per entry, generous touch targets, the active state unmistakable.
- **Dialog:** one decision, the consequence stated, verb-first actions, escape always available.

---

## PART 6 — AUTOMATIC REJECTION

Any of these fails the work on sight, no scorecard needed: KPI grid as first impression · fake personalization or fake liveness · five equally loud "important" cards · pale-purple body copy · 12px body / 9.5px labels · flat rows with borders presented as depth · glow everywhere · auto-rotating anything · motion without state · red used decoratively · gold used casually · a control that promises what the system doesn't deliver · navigation that needs decoding.

---

## PART 7 — LIVING RECORD

This contract learns. When Shawn's reactions teach something new, it is written here — dated, with the evidence, as a new dated entry. Taste becomes law through the loop, not through lectures.

### 2026-10-02 — Contract created (convergence)
Compiled from: v1.4 canon dos/don'ts/genome (folded verbatim), Builder Field Manual V1, `00-HUB-HOME.md` visual baseline, Design Intelligence Standard v1.3, the 40-block canon, Shawn's shell refinement (two corner buttons, drawers, feed-as-home), and the Room 01 rejection (wrong→right). Open director questions preserved: body-type target (17–18px vs 16px floor), room accent token collisions (Feed/Connect, Library/Mail).
