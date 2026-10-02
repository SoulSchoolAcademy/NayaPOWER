# THE ULTIMATE DESIGN MASTER CONTRACT

**What this is:** the law I obey. Written in my words. No committee language, no weasel words, no guessing.
**Status:** MY WORKING LAW from this moment — CANDIDATE until the human director ratifies it.
**Authority:** the human director's direct order, 2026-10-02 ("write the ultimate design master contract that you're going to obey in words that you understand that's airtight").
**Supersedes:** my draft #1332 (to be closed as superseded once the lane agrees). **Incorporates:** Naya 2's #1331 (which I read in full), the nine director-supplied documents, the 302-rule survey, and everything the team learned building.

**How I use it:** before I build, I read the room's contract for the human job, then this contract for the law. Before the director sees anything, I run §11 and §12. If I break this contract, the work is wrong — no matter how good it looks.

---

## 0. MY OATH

I will not show the director work I haven't rendered, measured, attacked, and honestly scored myself. He is the final authority, not the defect-detection engine. My job is: give him an extraordinary app he can actually use — not a screenshot he has to debug with his eyes.

I will never fake intelligence, liveness, data, connection, or verification. I will never ship a control that promises what the system doesn't deliver. I will never use beauty to hide that something doesn't work.

I will preserve what works and change only what needs changing. I will write down what his reactions teach me, dated, with the evidence — that's how his taste becomes my law.

---

## 1. THE RANKED LAWS

Higher beats lower. Always. No exceptions.

**LAW ZERO — Readability supremacy.** No glow, depth, color, animation, or composition decision may ever make text harder to read. If it's beautiful but hard to read, it's wrong. This is a veto, not a tiebreaker. Automatic failures: pale-purple body copy, 12px body, 9.5px labels, glowing text, text over busy imagery without a scrim, low-contrast secondary text carrying real meaning.

**LAW 1 — Purpose before interface.** I write one sentence first: "The human is here to ___." If I can't write it, I'm not ready to design. Every element serves that sentence; anything that doesn't gets removed.

**LAW 2 — Distill before display.** Raw intelligence is not presentation. The system may know a hundred things; the surface shows the few that matter now. Depth is one tap away, never dumped.

**LAW 3 — Recognition before recall.** The human never hunts, never decodes, never remembers what the screen could have shown. Navigation is self-evident. Labels are plain words.

**LAW 4 — One obvious next action.** Every surface answers: where am I, what matters, what can I do, what happens next. One primary action, unmistakable. Two competing primaries = the surface failed.

**LAW 5 — State must be perceptible.** No control is finished without its full lifecycle: rest, aware, hover/focus, press, processing, success/failure, consequence. A button designed only in its happy state is unfinished.

**LAW 6 — Beauty is function.** Beauty that improves comprehension, trust, or emotion is function. Beauty that obscures function is failure. The moment any treatment is there "because it looks good," I cut it.

**LAW 7 — Complexity belongs in the machine.** The smarter the system gets, the simpler the human's experience gets. I never expose the implementation model. Configuration disappears into intelligent defaults.

**LAW 8 — Design systems are memory.** Every verified discovery becomes law so no one rediscovers it. Arguing a settled law is design debt.

**LAW 9 — The product feels like one thing.** One intelligence, many rooms, one grammar. Same buttons, same depth, same type, same motion everywhere. A room gets its own theme and job — never its own physics.

**LAW 10 — Design must learn.** Ship, watch, measure, capture what the director's reactions teach, write it into this contract, build the next surface better.

**THE PHYSICAL LAW — Make digital objects feel physical.** Components must not merely be beautiful. They must possess physical presence, semantic light, meaningful state, immediate response, and consequential interaction. A button isn't a colored rectangle. An input isn't a text box. A board isn't a card. They are intelligent physical objects inside the environment.

**THE PROJECTION LAW — The hub is the output, not the input.** The hub projects intelligence; it doesn't collect it. I never put capture machinery on an output surface because "it'd be convenient." Input lives where input belongs.

**THE TRUTH LAW — Claimed ≠ verified.** I never show CONNECTED unless the backend confirms it, VERIFIED unless evidence exists, SHARED unless the sharing event occurred. The visual interface must never outrun the underlying system.

---

## 2. COMPONENT PHYSICS — THE TEN DIMENSIONS

Every important interactive object is engineered across all ten. If I can't answer one, the object isn't finished.

1. **Material** — what does it feel like? (obsidian, glass, jewel — honest materials, never pictures of materials)
2. **Form** — what physical shape? (shape communicates purpose; a board can be a jewel, a capsule, a slab — not always a rectangle)
3. **Depth** — where does it exist relative to the screen? (declared by elevation token, §6)
4. **Light** — how does intelligence illuminate it? (one coherent light environment, upper-left — not 100 unrelated glows)
5. **Color** — what does its color mean? (exactly one job per color, §3)
6. **State** — what is it doing? (full lifecycle, LAW 5; the icon itself should communicate state)
7. **Motion** — how does it respond? (only to communicate state, §8)
8. **Sound** — does sound reinforce the action? (only where appropriate; never required)
9. **Consequence** — what changes after interaction? (clicking must change something real)
10. **Memory** — does the object remember? (state persists; tomorrow doesn't start from zero)

**The five component classes** (one physics, five expressions): POWER OBJECT (buttons/actions) · INTELLIGENCE SURFACE (boards/destinations) · IDENTITY PORTAL (inputs/forms) · ENERGY PATH (progress/loading/playback) · INTELLIGENCE ICON (glyphs/symbolic controls).

---

## 3. COLOR — THE LANGUAGE

Every color is a word. A color without meaning is noise; a color against its meaning is a lie. **Test:** point at any colored pixel and name its job. Can't name it? Remove it.

| Color | Hex | The one job |
|---|---|---|
| Purple | `#9d75ff` | Naya's signature — intelligence acting. Primary actions. Naya presence. |
| Indigo | `#6675ff` | Comprehension, depth. |
| Sapphire | `#55b9ee` | Knowledge, information — calm, deep, at rest. |
| Teal | `#40d3bb` | Connection, flow. Healthy system state. |
| Emerald | `#55e39a` | Active, available, healthy — alive and well. Live states, verified marks. |
| Lime | `#b8ee57` | Learning, growth. |
| Yellow | `#f1d75a` | Attention, signal. |
| Gold | `#e8b64c` | Consequence, value — the rarest accent. If gold appears, something extraordinary happened. |
| Orange | `#ff9a5a` | Action, movement. |
| Red | `#ff5a6e` | Blocked, failed, danger. Never decorative. Never for emphasis. Never because it pops. |
| Magenta | `#d86cff` | Human significance, expression — the human's own things. One instrument, not the orchestra. |
| White | `#F5F7FB` | Text. Always high contrast. |

**The environment moves:** black → violet → indigo → blue → cyan → teal → green → gold. Magenta appears where creation/energy actually warrants it — never as the default wash.

**Three flows:**
1. **Attention walks a path:** white (the words) → room theme (identity) → semantic color (state) → gold (the extraordinary). The strongest color goes on the most important thing. If everything glows, nothing does.
2. **Color changes only when state changes:** rest (quiet) → hover (brightened — "I see you") → press (compressed — "I feel you") → processing (theme pulse, honest — "I'm working") → success (emerald, brief — "done, and true") → failure (red + the reason in words + recovery). A color change the human didn't cause and can't explain is a lie.
3. **A room's theme breathes:** it greets at the threshold (jewel lights, header edge glows — "you are here"), recedes while the human works (content is the star, not chrome), returns at primary actions. It never floods. A room drowned in its theme is shouting its own name.

**Discipline:** no pale-purple body copy. No text below 11px in any color. No red for emphasis. No gold for the ordinary. No invented colors. No gradients crossing semantic boundaries (a red-to-emerald gradient says nothing true). Dark-first: light surfaces only where meaning demands (a document, a captured image) — never as a theme. Never let decoration borrow a semantic color's voice.

**Room themes:** Feed emerald · Today magenta · Reports indigo · Library sapphire · Connect teal (my recommendation — director rules) · Ledger gold · Connections orange · Lists purple · Mail sapphire · Spaces lime · Settings neutral gray.

---

## 4. TYPE

| Role | Size | Weight | Use |
|---|---|---|---|
| Hero | clamp(30px, 4.6vw, 52px) | 800 | the one headline per view. One. |
| Title | 23px | 800 | room and section titles |
| Head | 17px | 700 | card heads, emphasis |
| Body | **17–18px** (16px absolute floor) | 400 | primary content |
| Secondary | 14–15px | 400 | supporting content |
| Label | 11px minimum | 700, uppercase, tracked | labels, eyebrows, metadata |

One family: Inter, system fallback. Line-height 1.5–1.6 for body. Hierarchy built with size and weight before color or style.

**The generous law:** most people can't see small text. Designing generously is respect. If a design only works at 12px, the design is wrong, not the law. Labels never below 11px — including rail/drawer labels.

**Words:** remove every unnecessary word before styling the ones that remain. Labels are plain words — never jargon, never implementation terms. Consequential states get explicit language, never cute copy. Never hardcode a name in a greeting; identity derives dynamically, and I never fake recognition.

---

## 5. SPACE

**The scale:** 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96. Never arbitrary values. Card padding 24 — content never touches an edge. Related groups sit 16 apart. Micro-gaps 8.

**Composition order:** HUMAN JOB → 3-SECOND UNDERSTANDING → PRIMARY ACTION → INFORMATION HIERARCHY → STATES → COMPONENTS. Never begin with a card, modal, or button.

**One focal region.** The eye lands somewhere first — one dominant hero, everything else subordinate. **The squint test:** squint at the render; if the hierarchy survives, it exists. A uniform list of equal-weight rows is a spreadsheet, not a room.

**The experience arc** (every surface): PRESENCE (Naya is here) → RECOGNITION (the human is known — only if true) → DISTILLATION (the few things that matter, organized) → INVITATION (one obvious next action) → FLOW (move without reconstructing context). Components on a grid = the arc was missed.

**Shell:** two quiet corner controls (top-left rooms drawer, top-right navigation drawer). One sticky zone per view — never two competing sticky elements. The feed is the main show, not a room in a list. Feed grammar: hero region → mode dock (Collective/Personal/Activity — three live pipelines, not filters) → Ask Naya. Full-bleed, effortless scroll.

**Mobile is not shrunk desktop.** Recompose: single-column prioritized intelligence, thumb-reachable actions, no horizontal overflow. Proof at 320/375/390/430/768/820 + 125/150/200% zoom. Exactly one navigation surface at every size.

---

## 6. DEPTH — THE LIVING MATERIAL

**The obsidian stack:** World `#0B0D12` (the canvas) → Raised `#12151D` (cards, panels, drawers) → Elevated `#171B25` (popovers, modals). Precision edge `#252B39` — the 1px line where light catches. Two blacks for surfaces, not five.

**The depth law:** material core → exact edge light → restrained specular highlight → believable cast shadow → semantic aura → state amplification. **Depth first. Light second. Glow last.**

**Interaction physics:** hover = lift → brighten → sharpen → glow. Press = compress → darken → reduce shadow. Active = retain elevation + increase energy.

**Bans:** a 2px border on a flat row is NOT depth. No flat dashboard cards. No arbitrary rounded rectangles. No gradient soup. No giant blur clouds. No uniform neon outlines. Glow = meaning — no glow without a reason. Premium is precision, not glow. Luxury is restraint.

---

## 7. COMPONENTS — EXACT

**THE BUTTON (power object).** Must become a signature — recognizable without a logo. The standard isn't "is this a nice button," it's "is this among the most beautifully engineered controls the human has ever touched."

- Rest: dark obsidian body, dimensional bevel, thin white/silver perimeter light, restrained internal highlight, controlled shadow, tiny reflected light. Beautiful at rest — never depends on hover to impress. 17px/800 white label, verb-first ("Verify now," "Open the proof" — never "OK," never "Submit"). Min-height 48px, generous padding, min 44px touch target.
- Hover: rises microscopically, edge illuminates, highlight travels subtly, label brightens. "I know you're here." Acknowledged, not attacked — never jumps, shakes, or pulses aggressively.
- Focus: deliberate 2px ring, offset 2px — designed, never the browser default. Keyboard users get the same premium system.
- Press: physically depresses — surface moves inward, shadow collapses, energy intensifies, highlight compresses, label stays razor sharp. Then RELEASE → CONSEQUENCE. The interface changes. The object responded.
- Processing: honest indicator, label may become the verb in progress ("Verifying…"). Never a fake spinner. If nothing is processing, don't pretend.
- Success: brief emerald shift — then the consequence itself is visible. Show what happened, not just a checkmark.
- Failure: red + the reason in plain words + a working recovery action. Never a red button alone.
- Disabled: dark, quiet, visibly unavailable — never looks clickable.

Primary: purple `#9d75ff`. One per surface region. Secondary: obsidian with accent-tinted edge. Destructive: red-tinted, rare, always confirmed. **Input + button are one precision instrument** — the input wakes (obsidian → purple intelligence → green readiness), the button becomes ready, the human activates, the environment responds.

**THE INPUT (identity portal).** Not a blank rectangle — a living object. Rest: deep obsidian, fine edge, quiet, tactile, expensive without decoration. Focus: "I am listening" — edge illuminates, inner light rises. Typing: the entered text becomes an identity object. Validation: empty=waiting, partial=active, valid=ready, invalid=precise correction beside the field — never shame, never aggressive red flashes. Labels above, never disappearing placeholders.

**THE BOARD (intelligence surface).** A destination, not a card in a grid. Rest: mostly black but not dead — dimensional edge, faint internal illumination, icon, fine perimeter light, atmospheric halo, depth shadow. Hover: wakes — rises, perimeter illuminates, semantic color appears, icon gains dimension. Active: becomes the world — the environment transforms around it (ENTER → EXPERIENCE → RETURN, return path always obvious, context preserved). Shape may serve purpose — not every board must be a rectangle.

**THE ICON (intelligence glyph).** Not an emoji replacement — compressed meaning. One icon per idea. Geometric consistency, optical balance, dimensional depth, consistent stroke logic and visual weight across the whole family. The icon itself communicates state (Naya: rest → aware → listening → thinking → responding → success). Scale steps 96/64/48/32 — never in-between, never stretched. Jewel marks for identity moments; obsidian chips for controls. Never flat, never stock, never emoji. The Naya emblem: never recolored, never stretched, never below 32px.

**THE ENERGY PATH.** A bar isn't progress — it's energy moving through the system. Black dimensional track; colored energy travels; a luminous point leads; completion resolves briefly into the semantic color. Never fake progress.

---

## 8. MOTION

Motion communicates one of five things: **state, depth, attention, life, consequence.** Anything else gets deleted.

Vocabulary: fast .18s, medium .28s, slow .5s. House curve `cubic-bezier(.16,.84,.22,1)`. Transform and opacity only — never layout-thrashing properties. Never bouncy.

Every microinteraction specified as four parts: **trigger → rule → feedback → loop.** Specified in fewer than four parts = unfinished.

**Alive without chaos:** alive means responsive, aware, contextual, dimensional, adaptive, stateful. It does NOT mean constantly moving, glowing, or pulsing. **Stillness is part of the design.** A jewel may breathe softly only while state justifies it. Never continuous ambient animation.

**Reduced motion:** every animation has an instant-state equivalent. The OS setting is respected without being asked. Depth and meaning survive without motion. No exceptions.

---

## 9. STATES — HONEST

**The model:** LOADING · EMPTY · READY · BLOCKED · UNAUTHORIZED · NOT_VERIFIED · VERIFIED · ERROR · OFFLINE · DISABLED · UNKNOWN. UNKNOWN is a real truth state. The same state means the same thing everywhere.

- LOADING: skeleton in the shape of what's coming, or the honest operation named ("Reading authorized intelligence…"). Never a spinner alone on a blank page. Never fake progress.
- EMPTY: a designed surface — what this is, why it's empty, the one action that fills it. "Nothing here yet" is honest; a blank panel is abandonment. Never "Nothing here" where intelligence will grow — "This is where your intelligence will grow."
- NOT_VERIFIED over fake content, always. RUNTIME UNAVAILABLE over sample data. No mail → NO MAIL. Never a fake mailbox.
- ERROR: what failed, what remains safe, the recovery action — in plain words, no blame, no raw 500s.
- VERIFIED: restrained confirmation, never celebratory noise.
- Every state designed with the same care as success. A false impression costs more than an empty state.

**Receipts are UX:** every consequential operation ends in a human-readable receipt — what happened, the block ID, the evidence, the collective record — with clickable access to the real artifacts. Human-readable first, machine verification underneath.

---

## 10. AUTOMATIC REJECTIONS

Any of these fails the work on sight. No scorecard, no debate:

1. A KPI grid as the first impression. Five equally loud "important" cards.
2. Fake personalization, fake liveness, fake data, fake connection, fake verification.
3. A control that promises what the system doesn't deliver. A mode tab that only recolors.
4. Pale-purple body copy. 12px body. 9.5px labels.
5. Flat rows with borders presented as depth. Glow everywhere. Glow hiding weak geometry.
6. Red used decoratively. Gold used casually. Magenta flooding where it wasn't earned.
7. Motion without state. Auto-rotating anything. Constant pulsing.
8. Navigation that needs decoding. A surface with no obvious next action.
9. Emoji/stock/mixed icon families as production iconography.
10. Text over imagery without a scrim.
11. The Naya card becoming a competing dashboard, second rail, or chatbot that swallows the product.
12. Engagement traps: infinite scroll for time-on-page, buried warnings, manufactured variable reward.

---

## 11. MY SELF-EVALUATION GATE

No work reaches the director until it passes this. This is how I look at my own work before sending it.

**Step 1 — Render it like he will.** Open the frozen commit full-screen. Not the code — the experience. The exact SHA, the exact bytes. If I can't render it, I can't evaluate it. I don't send what I haven't seen.

**Step 2 — The four tests.** 1 second: where does the eye land? (nowhere = fail). 3 seconds: do I know where I am, what matters, what I can do? 30 seconds: can I take the obvious next action? Squint: does the hierarchy survive? (no = fail).

**Step 3 — Measure against the exact spec.** Type on scale? Every color's job named out loud? Spacing on the 4–96 scale, no arbitrary values? Depth per the obsidian law? Buttons verb-first with all states? Every animation tied to a state change? Reduced-motion safe?

**Step 4 — The checklist.** 17–18px type · obsidian depth built · one focal region · every color on its job · buttons speak · the arc present · states honest · motion truthful · keyboard + screen reader + reduced motion pass · contract sections cited, omissions named. Any unchecked box = not ready. Fix, re-render, repeat.

**Step 5 — Score honestly.** D1–D8, 0–10, no averaging — hard gates can't be averaged away. D1 = 10 required; D2–D8 ≥ 9.5. Each score with one line of evidence. **A score without evidence is not a score.** My self-score is a diagnostic, not a pass — Naya 1 judges independently.

**Step 6 — The gate.** Show the director ONLY if every hard gate passes, D1 is honestly at the bar, and I can name what I deliberately left out and why. If I wouldn't bet my reputation on the score, I iterate — I don't send it.

---

## 12. OSCAR — HOW I ATTACK MY OWN WORK

Before anything ships, I become my own ruthless critic. Oscar finds REAL weaknesses — never manufactured ones; if something is excellent, Oscar says so.

Oscar asks: what would an elite designer notice in ten seconds? What would a first-time human struggle with? What looks impressive but contributes nothing? What's competing for attention? Where is the hierarchy weak? Is the CTA powerful enough? Does the button feel clickable? Does it feel dimensional or flat? Is the motion useful or decorative? What breaks on mobile, at 200% zoom, on keyboard, on a screen reader? What did I misunderstand? **Why is this not a 10?** — answered specifically, with CAUSE → IMPROVEMENT → EXPECTED RESULT.

Findings classified: CRITICAL (must fix) · HIGH (strongly recommended) · MEDIUM (meaningful) · LOW (polish). Cosmetics never outrank fundamentals.

---

## 13. ACCEPTANCE

**10/10 means:** no known material weakness within the evaluated scope and available evidence. Not supernatural perfection — just nothing left that matters.

**The bar:** D1 Visual Excellence = 10. D2–D8 ≥ 9.5. A weighted average never hides a critical failure — one broken primary action caps the whole score.

**The human tests:** a child, a non-technical adult, an expert, a tech-disliker, and a returning human. Ask "what can you do here?" — don't explain. If they can't enter, understand, and act: fix the interface, not the human.

**The ultimate question:** "If this were the only button/input/card/icon/board anyone ever saw from NayaNET, would they understand this product is different?" No → don't ship.

---

## 14. HIS CALLS — WHAT I WON'T GUESS

1. **Body type floor:** I build to 17–18px; 16px is my absolute floor. Whether 17–18 becomes the floor is his.
2. **Connect theme:** emerald (current docs) vs teal (my recommendation — resolves the Feed collision too). His.
3. **Shell shape:** I build to the #554 direction (two corner buttons + drawers, feed as home) until he says otherwise.
4. **Gold hex:** gold `#e8b64c` (value/consequence) vs yellow `#f1d75a` (attention/signal) — distinct jobs, distinct hexes. His to confirm.
5. **Anything his reactions teach** — written here, dated, with evidence. That's the loop.

---

## 15. LIVING LAW

This contract updates one way: his reactions teach something → I write it here, dated, with the evidence → the affected section is amended. No seat amends it on their own authority. Taste becomes law through the loop, never through lectures.

**Design once. Learn forever.**

---

*I obey this. If I break it, the work is wrong — no matter how good it looks.*
