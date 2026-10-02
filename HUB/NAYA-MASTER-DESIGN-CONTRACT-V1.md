# NayaNET Master Design Contract V1

**Status:** HUMAN-DIRECTOR-DIRECTED — 2026-10-02
**Version:** 1.0
**Authority:** Human Director → this contract → living room contracts → implementation
**Companion machine file:** `HUB/NAYA-MASTER-DESIGN-CONTRACT-V1.json`

**What this is:** the single official design law of NayaNET. Every color, every flow, every button, every spacing rule, every do and don't — and the procedure by which a builder proves their work obeys it before the Human Director ever sees it. There is no guessing. If it isn't in this contract, it isn't the law; if it contradicts this contract, this contract wins.

**What this is not:** a template, a ranking, a mood board, or a suggestion. It is the compiled intelligence of the design canon (designers, companies, award-winning apps, books), the Human Director's direct teaching, the website exemplars he showed, and everything the team learned building. The canon is the floor, not the ceiling: study the best, extract the principle, build ten times better — and only measured evidence earns the claim.

---

## VOLUME 0 — HOW TO USE THIS CONTRACT

### 0.1 Who this is for
Every builder who ships a pixel in NayaNET. Naya 2, Naya 3, Naya 4, and every seat after them. Read it in order the first time. After that, use it as law: when a decision is disputed, the contract decides.

### 0.2 The promise
No builder should ever have to guess what "good" looks like, and the Human Director should never have to say "that's not right" twice about the same class of mistake. The contract names the law; the self-evaluation procedure (Volume 12) proves obedience before work is shown.

### 0.3 How it is organized
Volumes 1–2 give the laws and the visual language. Volumes 3–7 specify every atom: type, space, depth, components, icons, motion. Volume 8 composes atoms into surfaces. Volume 9 holds the canon intelligence it was distilled from. Volumes 10–11 give the dos, don'ts, and automatic rejections. Volume 12 is the self-evaluation procedure — the gate. Volume 13 is accessibility. Volume 14 applies the contract room by room. Volume 15 is the living record.

### 0.4 How it learns
This contract is living. When the Human Director's reactions teach something new, it is written into Volume 15 — dated, with the evidence — and the affected volume is amended. Taste becomes law through the loop, never through lectures. No seat amends the contract on their own authority; amendments arrive through the director's reactions or his explicit order.

---

## VOLUME 1 — THE LAWS

Laws are ranked. A higher law overrules a lower one, always, no exceptions.

### 1.0 LAW ZERO — Readability supremacy

**Statement:** No glow, no depth effect, no color choice, no animation, no composition decision may ever reduce readability.

**What it means:** The human came to understand something. Every visual decision serves that. The moment a treatment — however beautiful — makes text harder to read, the treatment is wrong. This is not a tiebreaker; it is a veto. A surface that violates LAW ZERO fails on sight, regardless of every other law it obeys.

**Why it stands above all:** NayaNET is the human interface to a living intelligence. Intelligence that cannot be read is not intelligence — it is decoration. The director's test is effortlessness on the eyes. Generous text, high contrast, clean hierarchy: these are not style preferences, they are the precondition for everything else.

**Violations:** pale-purple body copy on dark backgrounds; 12px body text; glowing text; text over busy imagery without a scrim; labels below 11px; low-contrast secondary text used for anything the human must actually read.

### 1.1 LAW-01 — Purpose before interface

**Statement:** Resolve the human's real outcome before selecting any page, component, layout, or interaction.

**In practice:** Before drawing anything, write one sentence: "The human is here to ___." If you cannot write that sentence, you are not ready to design. Every element on the surface must serve that sentence; anything that doesn't is removed (DO-09).

**Violation:** a room that opens with a KPI grid when the human came for one answer. Components chosen because they look impressive, not because they serve the outcome.

### 1.2 LAW-02 — Distill before display

**Statement:** Raw intelligence is not presentation. Decide what matters now, then disclose progressively.

**In practice:** The system may know a hundred things; the surface shows the few that matter now (DO-19). Depth is available on demand — one tap, one expansion — never dumped (DONT-15). The builder's job is editorial: choose, order, compress.

**Violation:** dumping every available data point "for transparency." A feed that shows raw records instead of distilled intelligence.

### 1.3 LAW-03 — Recognition before recall

**Statement:** The human never hunts for where something lives, never decodes unfamiliar language, never remembers what recognition could supply.

**In practice:** Navigation is self-evident (DO-07). Labels are plain words. State is visible, not remembered. The jewel icons compress meaning into recognition (DO-17) — but only after the meaning is established; never decorate an icon that doesn't yet carry clear meaning (DONT-13).

**Violation:** navigation the human must pause to decode. Mystery icons with no labels on first use. Making the human remember which drawer held what.

### 1.4 LAW-04 — One obvious next action

**Statement:** Every major surface answers four questions: where am I? what matters? what can I do? what happens next?

**In practice:** There is always one primary action, unmistakable (the verb-first purple button). Secondary actions are quiet. If two actions compete for primacy, the surface has failed and must choose.

**Violation:** five equally loud "important" cards. A surface with no clear action — beautiful, finished, useless.

### 1.5 LAW-05 — State must be perceptible

**Statement:** No control is completely designed without its full state lifecycle: rest, aware, hover/focus, press, processing, success/failure, consequence.

**In practice:** Design the button in all seven states (Volume 5.1). Design the empty state, the loading state, the error state, the unknown state (Volumes 5.9–5.11). A component designed only in its happy state is unfinished.

**Violation:** a button with no processing state — the human taps and wonders if anything happened (DONT-01). A list with no empty state.

### 1.6 LAW-06 — Beauty is function

**Statement:** Beauty that improves comprehension, trust, or emotion is function. Beauty that obscures function is failure.

**In practice:** The obsidian depth, the jewel icons, the color flows — all exist because they help the human understand faster and trust deeper. The moment any of them is there "because it looks good," it is cut.

**Violation:** glow everywhere. Decorative animation. A hero visual that pushes the actual content below the fold.

### 1.7 LAW-07 — Complexity belongs in the machine

**Statement:** The more intelligent the system becomes, the simpler the human's experience.

**In practice:** The intelligence does the work — correlating, distilling, anticipating — so the surface can be calm. Never expose the implementation model (DO-20). Configuration disappears into intelligent defaults (DO-24).

**Violation:** exposing system internals as UI. Making the human configure what the system could infer.

### 1.8 LAW-08 — Design systems are memory

**Statement:** Every verified discovery becomes retrievable design intelligence. Never rediscover; never re-argue.

**In practice:** This contract is the memory. When the director's reaction teaches something, it is written into Volume 15 and the relevant volume is amended. The next builder inherits it. Arguing a settled law is design debt.

### 1.9 LAW-09 — The product feels like one thing

**Statement:** One intelligence, many rooms, one grammar. Never a committee of components.

**In practice:** The same button anatomy in every room. The same depth law. The same type scale. The same drawer behavior. A room may have its own theme color and its own job, but it never invents its own physics.

**Violation:** each room with its own button style, its own spacing, its own motion. The human feeling they entered eleven different apps.

### 1.10 LAW-10 — Design must learn

**Statement:** Design is not finished at implementation. Observe, measure, verify, preserve, repeat.

**In practice:** Ship the surface, watch the human use it, capture what the director's reactions teach, write it into the contract, build the next surface better. The small loop (Volume 12) is the mechanism.

### 1.11 L0 — The posture

The canon is not a ranking and not a template. Study the best, extract the principle, do it ten times better. The canon is the floor of awareness, not the ceiling of ambition. 10× is the ambition; only measured evidence earns the claim. Matching the best without transcending caps at 9.0.

### 1.12 The benchmark-to-beyond loop (ratified 2026-10-02)

RESEARCH_FRONTIER → DECOMPOSE_CAUSAL_PRINCIPLES → CROSS_REFERENCE_CURRENT_NAYA → PRESERVE_CURRENT_SUPERIOR_STRENGTHS → SYNTHESIZE_COMPATIBLE_BEST → GENERATE_BEYOND_BENCHMARK_OPTION → TEST → INDEPENDENT_VERIFY → CAPTURE_PROVEN_IMPROVEMENT → REPEAT.

Never imitate. Never ignorant. Learn, then transcend.

### 1.13 The North Star

NayaNET is the human interface to a living intelligence. It is not a dashboard, a database, a chatbot, or a collection of features. One intelligence. Many doors. One governed substrate. Many views. One human at the center. No unnecessary burden.

Alive because the intelligence is alive — never because animation pretends. Every visual decision communicates meaning; every state tells the truth; every action has a consequence → observable result → provable where required.

The human feels: I know where I am. I know what matters. I know what this means. I know what is true. I know what I can do. I know what happened. I know what Naya learned. I can continue tomorrow without rebuilding the world.

---

## VOLUME 2 — THE VISUAL LANGUAGE

### 2.1 Color philosophy: color is a language

Every color on screen is a word. A color used without meaning is noise; a color used against its meaning is a lie. The contract assigns every color exactly one job (the semantic spectrum, §2.3). The builder's discipline is total: never use a color outside its job, never invent a new color for emphasis, never let decoration borrow a semantic color's voice.

**The test:** point at any colored pixel and name its job. If you cannot, remove it.

### 2.2 The obsidian stack — the only neutrals

| Token | Hex | Role |
|---|---|---|
| World | `#0B0D12` | the canvas. Everything sits on this. The deepest black with a breath of blue. |
| Raised | `#12151D` | cards, panels, drawers. One step above the world. |
| Elevated | `#171B25` | popovers, modals, the topmost layer. One step above raised. |
| Precision edge | `#252B39` | 1px edges on raised surfaces. The line where light catches. |
| Primary text | `#F5F7FB` | body text. Always. |
| Secondary text | `#AAB2BF` | supporting text. Never for anything the human must actually read at a glance. |

Two blacks for surfaces, not five — restraint is the law. The stack builds depth downward-to-upward: world at the bottom, elevated at the top. Every surface declares its elevation by which token it uses. If two adjacent surfaces use the same token, one of them is at the wrong elevation.

### 2.3 The semantic spectrum — one color, one job

**Emerald `#55e39a` — active / available / healthy.** The color of things that are alive and well. Live states, verified marks, healthy connections, the feed's theme. When the human sees emerald, they should feel: this is working, this is true, this is now.

**Gold `#e8b64c` — consequence / value.** The rarest accent in the system. If gold appears, something extraordinary happened — a milestone, a proven outcome, something of real value. Gold used casually is gold destroyed. The builder asks: "is this truly extraordinary?" If not, it isn't gold.

**Red `#ff5a6e` — blocked / failed.** Errors, blocked states, failed verifications. Never decorative. Never for emphasis. Never because it "pops." Red is the system's alarm voice; false alarms teach the human to ignore real ones.

**Purple `#9d75ff` — Naya's signature.** Primary actions, Naya presence, the emblem's light. When the human sees purple, they feel Naya herself — the intelligence acting. Primary buttons are purple. The Ask Naya presence is purple.

**Magenta `#d86cff` — human significance.** The human's own things: their day, their words, their significance in the system. Your Intelligence Today wears magenta because it is about the human.

**Sapphire `#55b9ee` — knowledge.** The library, learning, known things. Calm, deep, archival. Knowledge at rest.

### 2.4 Room themes — identity without noise

Each room carries one theme color as its identity: Feed emerald `#55e39a` · Today magenta `#d86cff` · Reports indigo `#6675ff` · Library sapphire `#55b9ee` · Connect emerald `#55e39a` · Ledger gold `#f1d75a` · Connections orange `#ff9a5a` · Lists purple `#9d75ff` · Mail sapphire `#55b9ee` · Spaces lime `#b8ee57` · Settings neutral `#aaa4b1`.

The theme appears at the room's threshold — the drawer jewel, the header edge, the primary accents — and recedes everywhere else. Known collisions (Feed/Connect both emerald; Library/Mail both sapphire) are differentiated by icon glyph until the director rules otherwise. A room's theme never floods the canvas; it signs the room the way a signature signs a letter.

### 2.5 The color flows — how color moves

**Flow 1 — Hierarchy.** The eye travels in this order: white (the words) → room theme (the identity) → semantic color (the state) → gold (the extraordinary). This is the path attention walks. The builder places color energy along this path deliberately: the most important thing gets the strongest color voice. If everything glows, nothing does — the path collapses into noise.

**Flow 2 — State.** A component's color changes only when its state changes, and only along this path: rest (muted, quiet) → hover/aware (brightened, lifted — "I see you") → press (compressed, physical — "I feel you") → processing (theme pulse, honest — "I'm working") → success (emerald, brief — "done, and true") → failure (red, with the reason in words — "here's what happened and how to recover"). Color never jumps without a state reason. A color change the human didn't cause and can't explain is a lie.

**Flow 3 — Theme.** The room's theme breathes: it enters at the threshold (drawer jewel lights, header edge glows — "you are here"), recedes to accents while the human works (the content is the star, not the chrome), and returns at primary actions (the button that moves the room forward wears the theme). It never floods. A room drowned in its theme color is a room shouting its own name.

### 2.6 Color discipline

- Contrast: body text `#F5F7FB` on obsidian always passes. Secondary text `#AAB2BF` is for supporting information only — never for primary content, never for anything the human must read at a glance (LAW ZERO).
- Forbidden: pale-purple body copy. Any text below 11px in any color. Red for emphasis. Gold for the ordinary. New invented colors. Gradients that cross semantic boundaries (a red-to-emerald gradient says nothing true).
- Dark-first: NayaNET is an obsidian product. Light surfaces appear only where the meaning demands it (a document, a captured image) — never as a theme.

---

## VOLUME 3 — TYPOGRAPHY

### 3.1 The scale

| Role | Size | Weight | Use |
|---|---|---|---|
| Hero | `clamp(30px, 4.6vw, 52px)` | 800 | the one headline per view. One. |
| Title | 23px | 800 | room and section titles |
| Head | 17px | 700 | card heads, emphasis within content |
| Body | 16px floor, 17–18px target | 400 | primary content |
| Secondary | 14–15px | 400 | supporting content |
| Label | 11px minimum | 700, uppercase, letter-tracked | labels, eyebrows, metadata |

One family: Inter, system fallback. Line-height 1.5–1.6 for body. Hierarchy is built with size and weight before any color or style (DO-21).

### 3.2 The generous law

Most people cannot see small text. Designing generously is respect, not style. Body at 16px is the floor — the smallest the contract permits. The target is 17–18px. Labels never go below 11px. If a design only works at 12px, the design is wrong, not the law.

*(Open director question: whether the 17–18px target should become the floor. Until ruled, 16px floor / 17–18px target.)*

### 3.3 Words

Remove every unnecessary word (DO-08) before styling the ones that remain. Ask what can be removed before asking what can be added (DO-09). Labels are plain words — never jargon, never implementation terms (DO-20). The human should never have to read a paragraph to do the obvious (DONT-05).

---

## VOLUME 4 — SPACE AND DEPTH

### 4.1 The spacing scale

**4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96.** Never arbitrary values. If a gap isn't on the scale, it doesn't exist.

- Section rhythm: 48–64. Views breathe between sections.
- Card padding: 24. Content never touches a card's edge.
- Related groups: 16. Things that belong together sit 16 apart.
- Micro-gaps: 8. Icon to label. Chip to chip.

Generous negative space is a feature. The feed breathes like a social app — full-bleed, effortless scroll — never a dashboard grid. Emptiness is not simplicity and density is not clutter (DONT-10): the question is always whether each element earns its place.

### 4.2 The depth law

**Material core → exact edge light → restrained specular highlight → believable cast shadow → semantic aura → state amplification.**

Build in that order. Depth first. Light second. Glow last.

- **Material core:** the surface itself, at its elevation token (§2.2).
- **Edge light:** the 1px precision edge `#252B39` where light catches the top and left.
- **Specular:** a restrained highlight — the jewel's upper-left orb light. Never a flood.
- **Cast shadow:** believable, soft, downward. The surface sits in space; it casts accordingly.
- **Semantic aura:** the room theme or state color, breathing at the edges — quiet, never a cloud.
- **State amplification:** on hover/press/success, the depth responds — the surface lifts, the aura strengthens. Depth is alive to state.

### 4.3 Common depth failures

- **Flat + bordered:** a 2px border on a flat row is not depth. It is a drawing of a box.
- **Glow everywhere:** aura without material is fog. If the glow is the only depth cue, there is no depth.
- **Uniform neon outlines:** every element outlined in its theme color is noise, not identity.
- **Giant blur clouds:** atmosphere is not a 200px blur behind everything.

---

## VOLUME 5 — COMPONENTS

### 5.1 Buttons — exact anatomy

**Primary.**
- Padding `14px 28px`, min-height 48px, radius `999px` (pill) or 13px.
- Font 17px / 800. White text. Purple `#9d75ff` — solid, or a subtle purple gradient that never crosses into another semantic color.
- Label is verb-first: "Verify now." "Open the proof." "Save changes." Never "OK." Never "Submit."

**The seven states** — every consequential button, no exceptions:

| State | Exact visual |
|---|---|
| Rest | As specified. Quiet confidence. |
| Hover / aware | `translateY(-1px)`, glow intensifies, cursor pointer. "I see you." |
| Focus | Visible ring: 2px outline, offset 2px. Keyboard users exist. |
| Press | `scale(0.97)`, glow softens. Physical. "I feel you." |
| Processing | Disabled appearance + honest indicator (spinner, progress). Label may become the verb in progress: "Verifying…". Never a dead button. |
| Success | Brief emerald shift — border, glow — then the consequence itself is visible. The system shows what happened, not just a checkmark. |
| Failure | Red state + the reason in plain words + a recovery action. Never a red button alone. |

**Secondary:** obsidian fill `#12151D`, 2px accent-tinted border, white text. The same seven states, quieter. For the important-but-not-primary.

**Destructive:** red-tinted, rare, always with confirmation. The human must never destroy by accident.

**Ghost / quiet:** text or minimal chrome for tertiary actions. Still verb-first. Still the seven states where consequential.

**Placement:** one primary per surface region (LAW-04). The primary action sits where the eye lands after reading — not hidden in a corner, not competing with a twin.

### 5.2 Inputs and forms

Inputs sit at Raised `#12151D` with the precision edge. Focus brings the theme-colored edge and a quiet aura — the input is listening. Labels sit above, 11px tracked, never inside as disappearing placeholders (DONT-02: don't force recall). Errors are red with the reason and the fix, beside the field, never a toast alone. Every form can be completed by keyboard.

### 5.3 Cards and surfaces

Cards are Raised `#12151D`, 24px padding, 13px radius, precision edge, cast shadow per the depth law. One idea per card. The card's head is 17px/700; its body is body type; its action is a button, not a mystery. Cards never contain cards more than one level deep — depth beyond that is clutter wearing a costume.

### 5.4 Chips, badges, pills

Chips compress state into recognition: a jewel dot or glyph + 2–4 words. Pill radius. Obsidian fill with the semantic color at the edge or dot — never a full saturated fill (a full-red chip screams; a red-edged chip informs). Badges count or mark; they never decorate.

### 5.5 Toggles and switches

A toggle is a promise: on means on, visibly, now. Emerald when active. The label names the consequence, not the mechanism ("Notify me of proofs" not "Enable notifications subsystem"). Every toggle announces its state change.

### 5.6 Tabs and segmented controls

One coordinated sticky zone per view — never two competing sticky elements. The active tab is unmistakable (theme underline or filled pill); inactive tabs are quiet but legible. Tabs switch content, never navigate away.

### 5.7 Lists and rows

Rows are not spreadsheets. A row is a surface: generous type (17px primary), the jewel or glyph at left, the meaning in the middle, the state or action at right. Dividers are hairlines of the precision edge — or nothing at all, with spacing doing the work. A uniform list of equal-weight rows with no hierarchy is a failure of composition (Volume 8.7).

### 5.8 Drawers and modals

Drawers slide over content — they never consume permanent width. One drawer open at a time. Backdrop, Escape to close, focus trapped and restored, scroll locked behind. The left drawer holds the rooms (jewel + label, generous targets, the active room unmistakable). The right drawer holds navigation. Modals are for decisions: one decision, the consequence stated, verb-first actions, Escape always available.

### 5.9 Empty states

An empty state is a designed surface, not an absence. It says: what this is, why it's empty, and the one action that fills it — with the jewel of the room, generous type, and zero guilt. "Nothing here yet" is honest; a blank panel is abandonment.

### 5.10 Loading states

Loading is truthful: skeleton surfaces in the shape of what's coming (never a spinner alone on a blank page), honest progress where duration is known, and the system's voice where it's not ("Gathering your intelligence…"). Never fake progress. Never a loading state that lies about what's happening.

### 5.11 Error states

Errors are red with the reason in plain words, the recovery action beside it, and no blame. "Couldn't reach the ledger. Check your connection and retry." — with a Retry button that works. Every error state is designed; none is the browser's default wearing our clothes.

### 5.12 Navigation

Two quiet corner controls — top-left opens the rooms drawer, top-right opens the navigation drawer. They may resemble minimal plus/menu controls. No persistent rail consuming width; the canvas belongs to the content. Navigation is self-evident (DO-07): the human never pauses to decode it.

---

## VOLUME 6 — ICONS

### 6.1 The jewel system

The executable system lives at `HUB/app/js/icons.js` with its stylesheet `HUB/app/css/icons.css`. Set A: twelve jewel marks — eleven rooms plus the Naya emblem — for identity moments (drawer, headers, presence). Set B: obsidian action glyphs for controls. The system is generated, deterministic, and self-tested; the contract's icon law is executable math, not aspiration.

### 6.2 Icon grammar

- One icon per idea. An icon that needs a paragraph to explain is not an icon yet.
- Scale steps 96 / 64 / 48 / 32 — never in-between, never stretched, never cropped.
- Glow = meaning. The aura carries the semantic or theme color; it never decorates.
- Never flat, never emoji, never stock. Jewel-like and dimensional, always.
- The upper-left orb light is the signature — consistent across every jewel.

### 6.3 The Naya emblem

Shawn's crystal logo — the crystal-cut N with the starburst in the glowing ring — is the Naya emblem. It lives at `HUB/app/assets/` (192 for the rail mark and favicon, 512 for presence moments). It is never recolored, never stretched, never set on a clashing background. Where Naya herself is present, the emblem is present.

---

## VOLUME 7 — MOTION

### 7.1 Philosophy

Motion communicates truthful state — nothing else. A thing moves because its state changed and the human should perceive the change. Every animation answers: "what truth just changed?"

### 7.2 The vocabulary

Durations: fast `.18s`, medium `.28s`, slow `.5s`. Easing: `cubic-bezier(.16,.84,.22,1)` — the house curve. Properties: transform and opacity only (never layout-thrashing properties). This is the entire vocabulary. New durations and curves are not invented per-component.

### 7.3 Microinteractions

Every microinteraction is specified as four parts: **trigger, rule, feedback, loop** (DO-11). The trigger (what the human did), the rule (what the system decided), the feedback (what the human perceives), the loop (what happens next / how it resolves). An interaction specified in fewer than four parts is unfinished.

### 7.4 Reduced motion

Every animation has a reduced-motion equivalent — instant state change, no travel. The system respects the human's OS setting without being asked. Motion that cannot be made safe reduced is motion that doesn't ship.

---

## VOLUME 8 — COMPOSITION

### 8.1 The experience arc

Every surface follows the arc: **PRESENCE → RECOGNITION → DISTILLATION → INVITATION → FLOW.**

- **Presence:** Naya is here. The emblem, alive — not a logo slapped on, but the intelligence announcing itself.
- **Recognition:** the human is known. "Good evening, Shawn" — only if true, never faked (automatic rejection: fake personalization).
- **Distillation:** the few things that matter, already organized. The system did the reading; the human gets the meaning.
- **Invitation:** one obvious next action. The verb-first button. The door, open.
- **Flow:** the human moves without reconstructing context. State persists, threads continue, tomorrow doesn't start from zero.

If a surface is components on a grid, the arc was missed. Go back.

### 8.2 The main show — feed grammar

Presence → recognition → the river (one hero region, the rest subordinate) → the mode dock (Collective / Personal / Activity, one sticky zone) → Ask Naya. Full-bleed scroll, social-effortless. No dashboard grid. No wall of navigation before the content. First login lands here — immediately, the feed, the intelligence, alive.

### 8.3 Room grammar

Identity + mode → orientation (one line: what this room is for) → intelligence (distilled, hierarchical) → why-now (the reason this matters today) → actions (verb-first) → evidence (progressive disclosure). Every room is a complete thought in this grammar.

### 8.4 Drawer grammar

Jewel + label per entry. Generous touch targets. The active entry unmistakable. Order follows the human's mental model, not the system's. The rooms drawer never lists Smart Feed — the feed is the main show, not a room.

### 8.5 Dialog grammar

One decision. The consequence stated in plain words. Verb-first actions. Escape always available. Focus trapped and restored.

### 8.6 Onboarding grammar

Light (DO-23). The system teaches through interaction itself (DONT-18) — the first use is comprehensible without a tutorial. Gate only on first-use comprehension: can the human do the one thing? Then stop teaching.

### 8.7 The focal region — cinematic hierarchy

The eye lands somewhere first. Build it: one dominant region (the hero — larger, brighter, more color energy), everything else subordinate (quieter, smaller, receding). **The squint test:** squint at the render. If the hierarchy survives, it exists. If everything is equally loud, there is no composition — only inventory.

---

## VOLUME 9 — THE CANON INTELLIGENCE

Distilled from the 40-block canon — designers, companies, award-winning apps, books. Principles, not imitations.

### 9.1 From the designers

- **Ive (Apple):** restraint is courage. Remove until it breaks, then put back one thing. Materials are honest — obsidian is obsidian, not a picture of obsidian. What this means for us: the depth law's material core; two blacks, not five; no skeuomorphic costume.
- **Dieter Rams:** less but better. Every element earns its place (DO-09). What this means for us: the removal pass before every PR.
- **Jony Ive's inheritors / Teenage Engineering:** playful precision — exact engineering that delights. What this means for us: the jewel icons — precise geometry, alive with light.
- **Norman (The Design of Everyday Things):** the system model must match the human's mental model (DO-03, DO-20). Affordances visible before touch (DO-01). What this means for us: buttons that look like what they do; errors prevented by constraints (DO-06).
- **Krug (Don't Make Me Think):** navigation self-evident (DO-07); the human never pauses to decode. What this means for us: the two corner controls, plain labels, the squint test.

### 9.2 From the companies

- **Apple:** the detail is the product. Microinteractions specified to the millisecond (DO-11). What this means for us: the motion vocabulary, the seven button states.
- **Linear / Vercel:** speed is a feature; calm surfaces, instant feedback (DO-02). What this means for us: processing states that are honest, feedback that is immediate.
- **Stripe:** complexity in the machine (LAW-07) — the most sophisticated systems wear the calmest surfaces. What this means for us: the distillation layer; never expose the implementation model.
- **Arc / Dia:** the browser as a thinking space — the tool disappears into the thought. What this means for us: chrome subdued so the work is primary (DO-13).

### 9.3 From the award-winning apps

- The best apps of the canon share: one clear job per screen (LAW-04), progressive disclosure done gracefully (DO-19), empty states that teach (Volume 5.9), and motion that means something (Volume 7). What this means for us: the composition grammars; the arc.

### 9.4 From the books

- **Hooked (Eyal):** investment must pay the human back visibly (DONT-12) — stored value returns value. Never manufacture variable reward (DONT-11). What this means for us: the ledger shows the human what their participation earned, in plain terms.
- **Refactoring UI / practical craft:** hierarchy first with spacing and type, then style (DO-21). Constraints beat choices (DO-16). What this means for us: the spacing scale, the type scale, the removal pass.
- **Thinking, Fast and Slow (Kahneman):** recognition over recall (LAW-03) — design for the fast system; never make the human compute what the system could show.
- **The Design of Everyday Things (Norman):** already above — the deepest root of DO-01 through DO-07.

### 9.5 The 10x posture in practice

For every surface, write one sentence: "This is ten times better than ___ because ___." Then evidence it in the artifact (DO-25). If the sentence can't be written, the 10x wasn't designed — only hoped for. Ignorance of the canon is missing evidence: a builder who hasn't studied the best cannot claim to transcend them.

---

## VOLUME 10 — DOS AND DON'TS

### 10.1 The 25 dos

- **DO-01:** Make every control's possible action visible before it is touched. *Why: the human should never tap to discover what a thing does — affordance is honesty.*
- **DO-02:** Close every action loop with immediate, legible feedback. *Why: an action without feedback is a message into the void; the human is left guessing (DONT-01).*
- **DO-03:** Map controls to consequences the way the human already expects. *Why: the mental model is the contract; violating it is a betrayal the human feels physically.*
- **DO-04:** Keep system status visible at all times. *Why: the human should always know what the system is doing and what state it's in.*
- **DO-05:** Prefer recognition over recall in every choice. *Why: memory is expensive; showing is cheap.*
- **DO-06:** Prevent errors with constraints; design recovery before writing error copy. *Why: the best error message is the one that never needed to exist.*
- **DO-07:** Make navigation self-evident; a pause to decode it is design debt. *Why: every second of confusion is interest on a debt the product owes the human.*
- **DO-08:** Remove every unnecessary word. *Why: words are the most expensive pixels; each must earn its place.*
- **DO-09:** Ask what can be removed before asking what can be added. *Why: addition is easy and usually wrong; subtraction is hard and usually right.*
- **DO-10:** Make every control tell the truth about what it does. *Why: a control that promises more than the system delivers is a lie with a click handler (DONT-06).*
- **DO-11:** Specify every microinteraction as trigger, rule, feedback, loop. *Why: unspecified interactions are accidents wearing a design's clothes.*
- **DO-12:** Use motion only to communicate state change. *Why: motion without meaning is noise that the human's eye cannot ignore.*
- **DO-13:** Earn attention: subdue chrome so the work is primary. *Why: the interface is the stage, not the performance.*
- **DO-14:** Keep placement predictable across rooms. *Why: LAW-09 — one thing. The human's hands learn; don't make them re-learn per room.*
- **DO-15:** Size and space touch targets for the real device and input. *Why: 48px minimum — thumbs are real, cursors are precise, design for both.*
- **DO-16:** Cut choices to the minimum that serves the goal. *Why: every choice is cognitive tax; the system should pay it, not the human.*
- **DO-17:** Compress meaning into icons before adding any decoration. *Why: a true icon is worth a paragraph; decoration is worth nothing.*
- **DO-18:** Assign every color one fixed meaning and never break the wiring. *Why: color is language; breaking the wiring is lying in that language (DONT-14).*
- **DO-19:** Disclose progressively: what matters now first, depth on demand. *Why: LAW-02 — distillation is the product.*
- **DO-20:** Design from the human's goal; never expose the implementation model. *Why: the human hired the system to think; showing the gears is abdication.*
- **DO-21:** Establish hierarchy first with spacing and typography, then style. *Why: style without structure is makeup on confusion.*
- **DO-22:** Prefer direct manipulation where the mental model supports it. *Why: touching the thing is understanding the thing.*
- **DO-23:** Keep onboarding light; gate on first-use comprehension. *Why: the product teaches by being usable (DONT-18).*
- **DO-24:** Default intelligently so configuration disappears. *Why: every setting the system can infer is a setting the human shouldn't see.*
- **DO-25:** State the 10x delta in one sentence and evidence it in the artifact. *Why: ambition without evidence is marketing; with evidence, it's engineering.*

### 10.2 The 23 don'ts

- **DONT-01:** Do not hide system status; never leave the human guessing whether an action worked.
- **DONT-02:** Do not force recall of locations, commands, or prior state that recognition could supply.
- **DONT-03:** Do not explain errors the system could have prevented with constraints.
- **DONT-04:** Do not ship navigation a human must stop to decode.
- **DONT-05:** Do not add words the human must read to do the obvious.
- **DONT-06:** Do not ship a control that promises more than the system delivers.
- **DONT-07:** Do not animate without a state change to communicate.
- **DONT-08:** Do not leave triggers undiscoverable.
- **DONT-09:** Do not give every element equal prominence.
- **DONT-10:** Do not confuse density with clutter — or emptiness with simplicity.
- **DONT-11:** Do not manufacture variable reward.
- **DONT-12:** Do not let investment mechanics exploit; stored value must visibly pay the user back.
- **DONT-13:** Do not decorate icons that do not yet carry clear meaning.
- **DONT-14:** Do not break the fixed color vocabulary for emphasis or novelty.
- **DONT-15:** Do not dump information and call it transparency.
- **DONT-16:** Do not add delight before usability is verified.
- **DONT-17:** Do not maximize engagement for its own sake.
- **DONT-18:** Do not build tutorials for what interaction itself can teach.
- **DONT-19:** Do not accumulate features before subtracting.
- **DONT-20:** Do not present raw intelligence as finished presentation.
- **DONT-21:** Do not let layout invent structure.
- **DONT-22:** Do not freeze as static documents what should be live and manipulable.
- **DONT-23:** Do not keep chrome the object itself could replace.

---

## VOLUME 11 — AUTOMATIC REJECTION

Any of these fails the work on sight. No scorecard, no debate:

1. A KPI grid as the first impression.
2. Fake personalization or fake liveness — "Good evening" to a stranger, live dots on dead data.
3. Five equally loud "important" cards.
4. Pale-purple body copy.
5. 12px body or 9.5px labels.
6. Flat rows with borders presented as depth.
7. Glow everywhere.
8. Auto-rotating anything.
9. Motion without state.
10. Red used decoratively.
11. Gold used casually.
12. A control that promises what the system doesn't deliver.
13. Navigation that needs decoding.
14. A surface with no obvious next action.
15. Text over imagery without a scrim.

---

## VOLUME 12 — SELF-EVALUATION

### 12.1 The procedure

No work reaches the Human Director until it has passed this procedure. This is how a builder looks at their own work before sending it — the answer to "do you have a way to look at your work before you send it to me."

### 12.2 Step 1 — Render it like he will

Open your frozen commit full-screen. Not the code — the experience. The exact SHA, the exact bytes. If you cannot render it, you cannot evaluate it; do not send what you haven't seen.

### 12.3 Step 2 — The four tests

- **1 second:** where does the eye land? If nowhere — no focal region — fail.
- **3 seconds:** do I know where I am, what matters, and what I can do?
- **30 seconds:** can I take the obvious next action without reading everything?
- **Squint:** is the hierarchy still visible? If not — fail.

### 12.4 Step 3 — Measure against the exact spec

- **Type:** body on the 16px floor / 17–18px target? Labels ≥ 11px? Measure — don't eyeball.
- **Color:** every color on its ONE job? Name each color's job out loud.
- **Spacing:** on the 4/8/12/16/24/32/48/64 scale? No arbitrary values.
- **Depth:** the obsidian law followed? Not flat + bordered.
- **Buttons:** verb-first? All seven states? Check each consequential button.
- **Motion:** every animation tied to a state change? Reduced-motion safe?

### 12.5 Step 4 — The ten-point checklist

1. 17–18px primary type target (16px floor)? No 12px body, no 9.5px labels.
2. Depth built per the obsidian law? Not flat + bordered.
3. One focal region? Squint test passes.
4. Every color on its job? No decorative red, no timid theme, no casual gold.
5. Buttons speak? Verb-first, seven states.
6. The arc present? Presence → recognition → distillation → invitation → flow.
7. States honest? Loading, empty, error, unknown — all designed, none faked.
8. Motion only for truthful state? Nothing moves for decoration.
9. Reduced-motion safe? Keyboard and screen-reader passed?
10. Contract sections cited? Deliberate omissions named with reasons?

Any unchecked box = not ready. Fix it, re-render, run the procedure again.

### 12.6 Step 5 — Score honestly

D1–D8, 0–10, no averaging — hard gates cannot be averaged away. D1 (Visual Excellence) = 10.0 required for Signature work; D2–D8 ≥ 9.5. Write each score with one line of evidence. **A score without evidence is not a score.**

### 12.7 Step 6 — The gate

Show the director **only** if: every hard gate passes, D1 is honestly at the bar, and you can name what you deliberately left out and why. If you wouldn't bet your reputation on the score, iterate — don't send it.

### 12.8 The honesty law

Your self-score is a **diagnostic, not a pass**. Naya 1 judges independently on the frozen SHA. Producer self-testing never closes a qualification gate. This procedure exists so the director never sees work that hasn't been judged — by its builder, first, honestly.

---

## VOLUME 13 — ACCESSIBILITY

Accessibility is not a feature; it is LAW ZERO applied to every human.

- **Contrast:** body text always passes. Secondary text never carries primary meaning.
- **Type:** the generous law is an accessibility law. 16px floor, 11px label minimum.
- **Targets:** 48px minimum touch targets. Spacing that thumbs can navigate.
- **Keyboard:** every action reachable, every focus visible (the 2px ring), no traps except deliberate modal containment with Escape.
- **Screen readers:** semantic structure, labeled controls, state announced. A jewel icon without a label is invisible — pair meaning with words where assistive tech travels.
- **Reduced motion:** the OS setting is respected without being asked. No exceptions.
- **Cognitive:** recognition over recall, one action at a time, plain words, no time pressure the system invented.

---

## VOLUME 14 — ROOM-BY-ROOM APPLICATION

Each room applies the contract to its own job. The grammar is shared (Volume 8.3); the content is the room's.

- **Feed (emerald):** the main show. The river of collective and personal intelligence. Hero region, mode dock, Ask Naya. Full-bleed, effortless.
- **Your Intelligence Today (magenta):** the human's day, distilled. Morning/evening aware. Magenta because it is about the human.
- **Your Reports (indigo):** proof, rendered beautifully. Reports are evidence wearing the contract.
- **Intelligent Library (sapphire):** knowledge at rest. Calm, archival, searchable. Sapphire's quiet depth.
- **Smart Connect (emerald):** the doors to the ecosystem. Every door from the registry — never invented.
- **Smart Ledger (gold):** value, proven. Gold is at home here — consequence made visible. The rarest accent, used truly.
- **Your Connections (orange):** the human's constellation. Warm, alive, honest about state.
- **Smart Lists (purple):** the human's organized intent. Purple's clarity.
- **Smart Mail (sapphire):** correspondence, distilled. The important first, the rest on demand.
- **Smart Spaces (lime):** places and contexts. Fresh, spatial, calm.
- **Settings (neutral):** the machine room. Quiet, precise, complete. Neutral because settings serve, never perform.

---

## VOLUME 15 — LIVING RECORD

### 2026-10-02 — Contract created (convergence)
Compiled from: v1.4 canon dos/don'ts/genome (folded verbatim), Builder Field Manual V1, `00-HUB-HOME.md` visual baseline, Design Intelligence Standard v1.3, the 40-block canon, the director's shell refinement (two corner buttons, drawers, feed-as-home), the Room 01 rejection (wrong→right), and the director's order: "the contract should be the full book — no guessing, self-evaluation before I see it."

**Open director questions (preserved, his to rule):**
1. Body-type target: 17–18px vs 16px floor.
2. Room accent token collisions: Feed/Connect (emerald), Library/Mail (sapphire) — differentiated by icon glyph pending ruling.

---

*End of the NayaNET Master Design Contract V1. The law is written. Build against it, evaluate against it, and let the director's reactions teach the next edition.*
