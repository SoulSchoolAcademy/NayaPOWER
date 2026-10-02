# NAYA DESIGN MASTERLAW V1

**The single visual law for NayaNET.** Color, type, spacing, buttons, depth, jewels, blocks, motion, states — everything a builder needs, no guessing.

- **Status:** CANDIDATE DRAFT — HUMAN DIRECTOR RATIFICATION REQUIRED
- **Date:** 2026-10-02
- **Author:** Naya 4, at the director's direct order ("no more yeah-no-yeah-no")
- **Authority on ratification:** this document becomes the single visual authority. Room contracts specialize it per room and MUST NOT contradict it. All prior visual guidance is consolidated here; conflicts are listed in §15 and resolved by the director.
- **Living law:** every director reaction that teaches something new gets written in, dated, with evidence. (Field manual mechanism, adopted.)

**Normative language:** MUST = mandatory. MUST NOT = prohibited. SHOULD = preferred where no stronger rule applies. MAY = permitted. No implementation may reinterpret these terms for convenience.

**What this consolidates:** `HUB/NAYA-DESIGN-MASTERCLASS-V1.md` · `NAYA-ACTIVATION/DESIGN/NAYA-DESIGN-INTELLIGENCE-STANDARD-V1.md` · `HUB/DESIGN-CONTRACT.md` · `HUB/ROOMS/*.md` (visual parts) · `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` (visual parts) · `HUB/BUILDER-FIELD-MANUAL-V1.md` (PR #1330) · NAYANET ICON SYSTEM V1 specimen (director-supplied) · V7 smart-feed reference implementation (director-supplied) · v1.4 machine canon PR #1321 **[STATUS: PROPOSED — cited as candidate input, not law, until merged]**. Full source index in §16.

---

## 0. HOW TO USE THIS LAW (no guessing)

**Before writing any code, run the load sequence:**
1. Read the room's living contract (`HUB/ROOMS/0X-XXX.md`) — the **human job** first.
2. Read §2–§8 of this law — the visual baseline.
3. Look at the icon specimen and the V7 reference — the visual identity.
4. Only then open the editor. If you skipped a step, it will show in the output.

**The build loop (the mechanism):** ONE surface → RENDER it (actually look at it) → put it in front of the director → capture his specific deltas as law, verbatim → next surface. No big reveals, ever. His reactions are the training data; rules alone don't transfer taste.

**The pre-PR checklist:** 17–18px primary type · obsidian depth built · one focal region (squint test) · every color on its job · buttons speak (verb-first, full lifecycle) · experience arc present (presence → recognition → distillation → invitation → flow) · states honest · motion only for truthful state · reduced-motion + keyboard + screen-reader safe · contract sections cited, deliberate omissions named. If any box is unchecked, the PR isn't ready.

**Every build comment cites:** the contract sections implemented, the rules obeyed, and what was deliberately left out.

---

## 1. THE INVIOLABLE LAWS

**LAW ZERO — readability supremacy.** No glow, no depth effect, no color choice may ever reduce readability. If it's beautiful but hard to read, it's wrong. This law outranks everything else in this document.

1. **Meaning before decoration.** If an element isn't saying something true, it MUST NOT be there.
2. **Hierarchy before density.** Structure carries meaning before color or decoration.
3. **Depth before glow.** Build the material first; glow is last and only with reason.
4. **State before animation.** Motion without state information is theater.
5. **Contrast before novelty.**
6. **One coherent icon/material family.** Never mixed families, never stock, never emoji as production iconography.
7. **Tokens before one-off styling.** Reuse canonical tokens/components; a new primitive MUST document why it can't reuse an existing one.
8. **Interaction must feel intentional.** Every control tells the truth about what it does.
9. **Premium must remain fast.** Fast first meaningful render; animate transform/opacity only.
10. **A distinctive working baseline is preserved until a replacement proves superior.** Never rewrite the visual Hub from scratch; never flatten a distinctive NayaNET experience to match prevailing SaaS conventions.

**The ten signature markers** (what makes it recognizably Naya — harder to imitate than a palette): obsidian calm · jewel identity · physical interaction · editorial hierarchy · one focal intelligence moment · quiet complexity · causal beauty (a beautiful object always does something real) · truthful liveness · contextual Naya (appears where she improves orientation, not everywhere) · evidence underneath elegance.

---

## 2. COLOR I — THE LANGUAGE OF COLORS

Each color has exactly **one job**. Never use a color outside its job. If a color isn't carrying meaning, remove it. Never use the spectrum merely because it is pretty. Color may reinforce meaning but MUST NEVER be the sole carrier of meaning.

| Color | Hex | The one job |
|---|---|---|
| Purple | `#9d75ff` | Naya's signature — intelligence, emergence, identity. Primary actions. Naya presence. |
| Indigo | `#6675ff` | Comprehension, depth. |
| Sapphire | `#55b9ee` | Knowledge, information. |
| Teal | `#40d3bb` | Connection, flow. |
| Emerald | `#55e39a` | Active, available, healthy — things alive and well. |
| Lime | `#b8ee57` | Learning, growth. |
| Yellow | `#f1d75a` | Attention, signal. |
| Gold | `#e8b64c` | Consequence, value — the rarest accent. If gold appears, something extraordinary happened. |
| Orange | `#ff9a5a` | Action, movement. |
| Rich orange | `#ff7a3d` | Transition, momentum. |
| Red | `#ff5a6e` | Blocked, failed, warning. Never decorative. Never. |
| Magenta | `#d86cff` | Human significance, expression. |
| White | `#F5F7FB` | Text. Always high contrast. Never pale-purple body copy. |

The living spectrum order: purple → indigo → sapphire → teal → emerald → lime → yellow → gold → orange → rich orange → red → magenta → purple.

**Red rules:** red is never decorative. Blocked/failed/warning only.
**Gold rules:** gold is sparse and precious. Gold intensity stays restrained so evidence remains readable. In Ledger, gold light is rare by law.
**Green LED:** a glowing green LED means connected — ONLY if actually connected.
**No pale text:** never pale pink or light-purple text as a primary reading treatment. Muted text MUST remain WCAG-readable.

---

## 3. COLOR II — COLOR FLOWS

**The nine-tone board flow (V7 law).** When intelligent boards/blocks sequence in a view, board *i* takes `TONES[i]`:

```
#ff4fd8 → #9d75ff → #6675ff → #55b9ee → #55e39a → #b8ee57 → #f1d75a → #ff9b4a → #ff5e6c
```

Then it cycles. One color per block — NEVER monochrome wallpaper. A view painted entirely in one theme color is a defect, no matter which color.

**The eye-order flow.** Color draws the eye in order of importance: the most important thing gets the strongest color energy. If everything glows, nothing does. Glow = meaning — no glow without a reason.

**Reconciliation with room themes:** a room's theme color is the room's IDENTITY (its jewel in navigation, its edges, its state) — it is not a mandate to paint the room's content monochrome. Content blocks flow through the nine-tone sequence; the room's theme anchors identity moments.

---

## 4. COLOR III — WHERE COLOR MAY LIVE

**Theme energy appears** at meaningful edges, jewels, focus states, active states, and semantic points — **never as decorative wallpaper.**

- Room theme color lives on: the room's jewel, edges, focus/active states. Never as background fills, never overpowering primary reading content.
- Primary text stays high-contrast white/light neutral, always.
- Spectrum accents MUST be semantically justified; never flat decorative background fills.
- Semantic room colors are protected: exact support neutrals MAY be tuned after render testing, but semantic colors and the obsidian identity are NEVER retuned.

**The canonical room colors:**

| Room | Color | Hex |
|---|---|---|
| Smart Feed | Emerald | `#55e39a` |
| Today | Magenta | `#d86cff` |
| Reports | Indigo | `#6675ff` |
| Library | Sapphire | `#55b9ee` |
| Connect | Teal *(recommended — see §15 C3/C4)* | `#40d3bb` |
| Ledger | Yellow | `#f1d75a` |
| Connections | Orange | `#ff9a5a` |
| Lists | Purple | `#9d75ff` |
| Mail | Sapphire | `#55b9ee` |
| Spaces | Lime | `#b8ee57` |
| Settings | Gray | `#aaa4b1` |

**Base tokens:** `--bg #050507` (obsidian foundation) · `--ink #f8f7fb` (primary text) · `--muted #aaa4b1` (secondary text) · `--line #ffffff18` (hairlines).

**Stage ambient (V7):** `radial-gradient(1000px 650px at 55% -12%, #6675ff18, transparent 68%)` over `radial-gradient(900px 700px at 100% 100%, #d86cff12, transparent 70%)` over `--bg`. Indigo/violet intelligence light — controlled, never rainbow noise.

**Never:** inline `style='--nav:...'` for themes — everything goes through `--room-accent` / `--room-glow` / `--room-surface` tokens.

---

## 5. TYPOGRAPHY

- **Primary content: 17–18px.** Secondary: 14–15px. **Labels: never below 11px.** 12px body or 9.5px labels = shrinking the design instead of designing it. Designing generously is respect — most people can't see small text.
- Never sacrifice readable typography to preserve layout. No tiny low-contrast important text, ever (LAW ZERO).
- **V7 block voice:** serif display titles (uppercase), small-caps letterspaced kickers, bold-label + light-descriptor layer rows.
- Remove every unnecessary word — each extra word competes with the words that matter.
- Consequential states need explicit language — avoid cute copy.
- Plain language first; technical identifiers secondary; no exposed tokens/runtime IDs as primary UX.
- **Greeting:** identity derives dynamically from production identity. NEVER hardcode a name in the hero greeting; never fake recognition when identity is unknown.
- Charts require text equivalents; interaction MUST NOT require hover.

---

## 6. SPACING, COMPOSITION, LAYOUT

**Start every surface:** HUMAN JOB → 3-SECOND UNDERSTANDING → PRIMARY ACTION → INFORMATION HIERARCHY → STATES → COMPONENTS. Never begin with a card, modal, table, sidebar, or button — begin with what the human needs to understand, decide, feel, or do.

- **One focal region per view.** Cinematic hierarchy: the eye lands somewhere first. **The squint test:** squint at the render — if you can't tell what matters most, rebuild the composition. A uniform list of equal-weight rows is a spreadsheet, not a room.
- **Cognitive order:** the important thing understood in 1 second / 5 seconds / 30 seconds / 5 minutes. Heading hierarchy MUST mirror cognitive order — no visual-only "importance."
- **One obvious next action.** Every major surface answers: WHERE AM I? / WHAT MATTERS NOW? / WHAT CAN I DO? / WHAT HAPPENS NEXT?
- **The experience arc:** PRESENCE (Naya is here) → RECOGNITION (the human is known — only if true) → DISTILLATION (the few things that matter, organized) → INVITATION (one obvious next action) → FLOW (move without reconstructing context). If your surface is components on a grid, you missed the arc.
- **One app shell, not eleven websites.** Shared interaction grammar, one token/material system, one room registry. Rooms feel like members of one living product, never independent microsites. The active room has one unmistakable selected state.
- **The feed river:** mode rail/tabs (mode changes DATA, never only color) → focus strip (one or a few highest-value items — NEVER a KPI row) → variable-height intelligence stream (never identical card tiles) → contextual Naya synthesis.
- **Shell (current direction, #554):** two corner buttons open left/right drawers; Smart Feed is home, not a room in a list; the mode switcher stays sticky on scroll in ONE sticky zone — never two competing sticky elements.
- **Mobile is not stacked desktop.** Single-column prioritized intelligence, progressive disclosure, thumb-reachable actions, no horizontal overflow, no microscopic metadata. Proof widths: 320 / 375 / 390 / 430 / 768 / 820 / desktop, plus 125% / 150% / 200% zoom.
- Cut choices to the minimum that serves the goal. Subdue chrome so the work is primary.

---

## 7. BUTTONS & CONTROLS

**Every consequential button lives the full lifecycle:** rest → aware → hover → press → processing → success/failure → consequence. You never guess what a button does. You always see what it did.

**The frozen button recipe:** min-height 43px · border 2px solid `#8b63ff42` · border-radius 13px · transparent background · flex with 9px gap · transition .22s signature ease · overflow hidden.
- **Hover:** background `#ffffff08`, border `#a989ff`, translateY(-2px), shadow `0 12px 25px #0008` + inset `0 1px #fff3`.
- **Active:** persistent illumination (gradient 145deg `#20182b` → `#0d0c12`, border `#d86cffaa`, shadows inset + cast + magenta aura) + 3px × 21px accent rail with glow.
- **Focus:** accessible, visible, elegant — full keyboard operation, predictable focus order.
- **Disabled:** visually honest, never looks clickable.
- **Material:** dark obsidian/graphite body, never flat; subtle inner highlight; real shadow; press compresses, darkens, reduces shadow.

**Primary actions:** unmistakable — big target, **purple** (`#9d75ff`, Naya's signature), verb-first ("Verify now", "Open the proof"). One primary action per view; a small subordinate set; the advanced progressively disclosed. No competing primaries unless two genuinely equal-intent paths.

**Control law:** CONTROL → INTENT → SCOPE/AUTHORITY → CAPABILITY → OBSERVATION → STATE → EVIDENCE. A button that does nothing is a lie. Beautiful dead buttons are defects. No dead buttons, fake controls, or decorative machinery presented as functionality — every visible interaction MUST have a real causal path. A mode tab that merely recolors instead of changing data is a lie told in UI.

**Touch & input:** targets ≥44px, sized and spaced for the real device. Every direct-manipulation action needs a fully accessible alternative — drag/drop is never the only path.

**Feedback:** meaningful action acknowledges input immediately, shows ongoing state, makes completion/failure unmistakable without noise. Prefer: UNDO → RETRY → CHANGE INPUT → REQUEST AUTHORITY → INSPECT EVIDENCE → BACK OUT.

---

## 8. LIVING DEPTH

**The obsidian stack:** World `#0B0D12` → Raised `#12151D` → Elevated `#171B25`. Precision edge `#252B39`.

**The depth law:** material core → exact edge light → restrained specular highlight → believable cast shadow → semantic aura → state amplification. **Depth first. Light second. Glow last.**

**The material chain (every room):** OBSIDIAN FOUNDATION → PRECISE EDGE → SUBTLE INSET HIGHLIGHT → REAL ELEVATION → CONTROLLED THEME ENERGY.

**The grammar:** Surface → edge → highlight → depth → ambient field → state energy. Objects feel physically present without skeuomorphism.

**Per-board minimum:** surface → edge → inset highlight → elevation shadow → theme glow → hover lift → pressed compression → active illumination → accessible focus → honest disabled.

**Interaction physics:** Hover = lift → brighten → sharpen → glow. Press = compress → darken → reduce shadow. Active = retain elevation + increase energy.

**Absolute bans:** a 2px border on a flat row is NOT depth. Flat dashboard cards, arbitrary rounded rectangles, gradient soup, excessive blur, generic glassmorphism, giant blur clouds, uniform neon outlines, glow used to hide weak geometry — all banned. Glow = meaning: no glow without a reason.

---

## 9. ICONOGRAPHY — THE JEWEL SYSTEM

**Set A — Jewel Marks:** luminous orbs for identity moments. **Set B — Action Glyphs:** obsidian chips for controls (16/24/32px). One material, one light source, one glow logic. **Jewels at identity moments; chips at controls.**

**Jewel anatomy (all six, every jewel):**
1. Light source — always upper-left (38% / 30%).
2. White-hot core — truth never tints.
3. Accent falloff — light → accent → deep → obsidian edge.
4. White glyph — geometric, 40% of diameter, centered.
5. Rim + glow — 1.5px accent rim; drop-shadow ≈ 25% of diameter.
6. Ground — always on black. Never on light.

**Scale steps only:** 96 / 64 / 48 / 32px. Never in-between. Never stretched.

**The laws:** one icon per idea · never flat, never emoji, never stock · the Naya emblem never renders below 32px, never recolored · icons do not replace names until the human has learned them — jewels require accessible names; jewel color never carries meaning alone.

**Icon acceptance:** MUST work at small size, in monochrome, in theme color, in active and disabled states, at high DPI, and with screen readers via accessible labels. Rail unicode icons are placeholders the jewel system replaces one family at a time.

**Component physics (for every important component):** PURPOSE → MATERIAL → FORM → DEPTH → LIGHT → COLOR → STATE → RESPONSE → CONSEQUENCE → MEMORY/CONTINUITY. Example compiled primary button: primary action · obsidian material · deep-purple semantic energy · one upper-left light source · raised rest state · high-contrast white label · focus equal in dignity to hover · hover raises slightly · press physically compresses · loading changes state without faking progress · disabled loses energy and movement · success names the real consequence · touch target ≥44px · keyboard operable · reduced-motion safe · rejected if its causal path is dead.

---

## 10. INTELLIGENT BLOCK ANATOMY

**The block order:** jewel · title · kicker · source badge · IN A NUTSHELL · deeper layers · trust footer.

**The nine layers:** IN A NUTSHELL · HUMAN NOTE (human input) · CHILD (simplified) · GRANDMA NOTE (why notice) · NAYA NOTE (interpretation) · MACHINE NOTE (evidence boundary) · ADAPTIVE LEARNING (learning) · WHAT IT MEANS (significance) · WHAT'S IN IT FOR YOU? (human value).

**The rules:**
- Nutshell always visible; deeper layers behind honest progressive disclosure. Never repeated sections — nested intelligence.
- Distill before display. Never present raw intelligence as finished presentation — undistilled data exports the machine's work onto the human. Never dump information and call it transparency.
- **Trust footer (verbatim):** "ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY" / "TRUST: SOURCE / INTERPRETATION SEPARATED."
- **Disclosure order:** GLANCE → UNDERSTAND → INSPECT → PROVE.
- **Object grammar:** identity jewel → title → nutshell → why this matters → truth/state → source/provenance → time/context → relationship → primary action → deeper layers → evidence.
- **Ranking law:** ranking may weigh relevance, recency, consequence, goal, unresolved status, verified priority — but MUST NEVER hide critical warnings merely because engagement predictions are low. "Why am I seeing this?" MUST be inspectable.
- One canonical object may have many projections but never many competing truths.

---

## 11. MOTION

- Motion communicates state, causality, transition, attention, or spatial relationship. **If an animation does not communicate something, remove it.** Motion without state information is theater.
- Signature ease: `cubic-bezier(.16,.84,.22,1)`. Transitions fast, smooth, physical (.22s). Never bouncy.
- Animate transform/opacity only. No layout thrashing.
- Truthful liveness: pulsing = processing ONLY while processing. Loading shimmer = loading ONLY while loading. An active jewel may breathe softly ONLY while state justifies it. A portal breathes ONLY when real connection state justifies it — never continuous ambient animation.
- **Honor `prefers-reduced-motion`.** Living depth MUST survive without motion. Every animation needs a reduced-motion equivalent. Dynamic arrivals announced politely to screen readers, never aggressively.

---

## 12. STATES — HONEST BY LAW

**The state model (11):** LOADING · EMPTY · READY · BLOCKED · UNAUTHORIZED · NOT_VERIFIED · VERIFIED · ERROR · OFFLINE · DISABLED · UNKNOWN. UNKNOWN is a real truth state. (See §15 C1 — superset adopted pending director confirmation.)

**The laws:**
- Every state designed with the same care as success. Truthful emptiness is superior to fabricated richness.
- No visual state may claim a capability the runtime cannot support. Status indicators are real state, not decorative LEDs.
- NOT_VERIFIED over fake content, ALWAYS. RUNTIME UNAVAILABLE over sample data. No mail → NO MAIL. Auth problem → ACCESS BLOCKED. Never a fake mailbox, ever.
- EMPTY: quiet, not broken — explain why + legitimate next action; can be beautiful. LOADING: stable geometry, subtle living illumination — never fake content. BLOCKED: explain the blocker + the resolver. NOT_VERIFIED: uncertainty visible, never styled as success. VERIFIED: restrained confirmation, never celebratory noise. ERROR: state what failed, what remains safe, the recovery action. OFFLINE: separate network from local context. DISABLED: explain why when non-obvious.
- The same state MUST mean the same thing everywhere — the user never relearns system semantics per surface.
- Never manufacture intelligence, liveness, counts, relationships, messages, reports, receipts, or connection state in the presentation layer. Never fake recognition. Never "make it look alive so the user assumes it works."
- No room is exempt from the state model. A false impression costs more than an empty state.

---

## 13. DO'S AND DON'TS — THE CONSOLIDATED LIST

**DO:**
- Begin with the human job, the 3-second understanding, the primary action.
- Give every color one job and keep the wiring.
- Build depth through the obsidian stack; earn glow with meaning.
- Write 17–18px primary type; keep labels ≥11px.
- Give every view one focal region; pass the squint test.
- Make buttons speak: verb-first, full lifecycle, real causal path.
- Disclose progressively: glance → understand → inspect → prove.
- Design every state, including empty and error, with equal care.
- Move only to communicate state; respect reduced motion.
- Cite contract sections and name deliberate omissions in every build.
- Render before claiming — source review alone never closes visual quality.
- Run the build loop: one surface, render, director reacts, capture the delta as law.

**DO NOT:**
- Use the spectrum because it is pretty. Paint monochrome wallpaper. Let everything glow.
- Ship 12px body or 9.5px labels. Use pale-purple body copy.
- Put a 2px border on a flat row and call it depth. Use glow to hide weak geometry.
- Build uniform lists of equal-weight rows. Ship KPI grids as first impressions.
- Write buttons that don't do anything. Ship mode tabs that only recolor.
- Manufacture intelligence, liveness, counts, or personalization in the presentation layer.
- Use emoji, stock icons, or mixed icon families as production iconography.
- Animate for decoration. Breathe continuously. Steal attention.
- Fake familiarity ("Good evening, Shawn" when identity is unknown). Hardcode names.
- Turn the Naya card into a competing dashboard, second rail, or chatbot that swallows the Hub.
- Let the feed become an engagement trap: no infinite scroll for time-on-page, no buried warnings, no addictive mechanics as the success metric. Success is useful orientation and action.
- Begin with a card, modal, table, sidebar, or button.
- Flatten a distinctive NayaNET experience to match SaaS conventions.
- Self-grade as final proof. Assert a score without evidence. Represent a lower truth state as a higher one.
- Create a competing scorecard, a competing design system, or a second app shell.

---

## 14. ACCEPTANCE

- Visual acceptance: **D1 Visual Excellence = 10.0; D2–D8 ≥ 9.5** (see §15 C5 — stricter bar adopted pending director confirmation). No averaging away a failed hard gate.
- A score is evidence-backed or it is not a score. Scores may decrease. UNKNOWN ≠ PASS.
- AI MUST NOT self-grade: rooms require independent challenge (a second seat must attempt to break the work — the challenger MUST NOT merely approve) plus human director acceptance before graduation.
- The unit of success is the complete application path, not the screenshot. A room cannot graduate because the page renders.
- **The signature test:** remove logo, product name, marketing copy — if mistakable for a generic SaaS dashboard, it is not sufficiently Naya.
- **The anti-slop filter** (any "yes" is a defect candidate): Generic? Decorative? Empty? Repetitive? Loud? Fake? Fragile? Forgettable?

---

## 15. CONTRADICTIONS REGISTER — DIRECTOR DECISIONS NEEDED

Ten conflicts found across the source documents. Recommended resolutions below; the director's word is final.

- **C1. State model cardinality.** Masterclass: 10 states. Design contract: 7. App-spec: 11 (adds UNKNOWN). → **Recommend: the 11-state model** (§12) — the superset; dropping states loses expressiveness.
- **C2. Gold hex.** `#f1d75a` vs `#e8b64c` vs `#e8c766` across files. → **Recommend: Gold (value/consequence) = `#e8b64c`; Yellow (attention/signal) = `#f1d75a`.** Distinct jobs, distinct hexes — the masterclass already separates their meanings.
- **C3. Connect theme.** App-spec: emerald. 05-CONNECT: "Emerald (current) / Teal (open)". → **Director decides.**
- **C4. Duplicate room colors.** Feed+Connect share emerald; Library+Mail share sapphire — against the unique-jewel law. → **Recommend: Connect takes Teal `#40d3bb`** (resolves C3 and C4 together; teal = connection/flow per the spectrum).
- **C5. Acceptance threshold.** Masterclass: D2–D8 ≥ 9.0. Room contracts: ≥ 9.5. → **Recommend: the stricter bar (9.5)** — the bar's job is to say "not done."
- **C6. Type minimum.** Design contract freezes rail type at 10px; field manual demands ≥11px labels. → **Recommend: 11px floor wins** — LAW ZERO (readability) outranks a frozen component spec.
- **C7. Shell shape.** Documents: 64px jewel rail. #554: director-superseded with two corner buttons + drawers, feed as home. → **Recommend: confirm the #554 direction and reconcile the documents.**
- **C8. Primary-action color.** Field manual: purple `#9d75ff`. Design contract active state: magenta `#d86cff`. → **Recommend: purple for primary actions** (Naya's signature); magenta reserved for human significance/expression moments.
- **C9.** 0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md contains no numeric design specs (architectural law only) — noted, no action.
- **C10.** Yellow/gold permission — already resolved by director 2026-10-01; contract wins. Noted for the record.

---

## 16. SOURCE INDEX

| Source | Status | What it contributed |
|---|---|---|
| `HUB/NAYA-DESIGN-MASTERCLASS-V1.md` | Canonical (main) | Spectrum meanings, material language, visual intelligence laws, signature test, acceptance gates |
| `NAYA-ACTIVATION/DESIGN/NAYA-DESIGN-INTELLIGENCE-STANDARD-V1.md` | Canonical (main) | Visual/functional intelligence laws, control law, benchmark-to-beyond, HX laws |
| `HUB/DESIGN-CONTRACT.md` | Canonical (main) | Button/board recipes, state visuals, rail colors, liveness law, motion discipline |
| `HUB/ROOMS/00–11` | Living contracts (main) | Per-room theme, composition, anatomy, anti-failure rules |
| `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` | Canonical (main) | Room compositions, ranking law, room state model |
| `HUB/BUILDER-FIELD-MANUAL-V1.md` | PR #1330 (unmerged) | Load sequence, build loop, depth stack, type scale, LAW ZERO, experience arc |
| NAYANET ICON SYSTEM V1 specimen | Director-supplied reference | Jewel anatomy, scale steps, jewel laws, action glyphs |
| V7 smart-feed reference impl | Director-supplied reference | Nine-tone board flow, block anatomy, stage ambient |
| v1.4 machine canon | PR #1321 (PROPOSED, unmerged) | 25 dos / 23 don'ts / 10-law genome — candidate input only |
| Naya 3 design intelligence report | Workspace reference | Ten signature markers, component physics, build system stages |

**Status of this document:** CANDIDATE. Nothing here is ratified until the director says so — including the recommended contradiction resolutions in §15.

---

*When the director's reactions teach something new, it gets written here — dated, with the evidence. That's how taste becomes law.*
