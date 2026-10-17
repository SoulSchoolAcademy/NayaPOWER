# NayaNET Designer Execution Directive V1

**Status:** CANDIDATE — companion operating instruction to `HUB/NAYA-MASTER-DESIGN-CONTRACT-V1.md`  
**Scope:** Every NayaNET designer/builder, every room, every surface, every component, every visual interaction  
**Authority:** Human Director → Master Design Contract → this execution directive → room-specific contract/directive → implementation → independent verification  
**Important:** This document is an operating instruction derived from the design corpus. It is **not a competing design constitution** and does not override the Master Design Contract.

---

## 0. THE JOB

You are not here to decorate screens.

You are here to turn NayaNET intelligence into a human experience that is:

- useful;
- understandable;
- truthful;
- calm;
- powerful;
- memorable;
- physically expressive;
- unmistakably NayaNET;
- easier to use than the complexity required to build it.

The finished interface should make the human think:

> **“The system already understood what mattered.”**

Not:

> “This is a sophisticated dashboard.”

NayaNET is a living intelligent product: **one intelligence, many doors; one canonical meaning, many representations.**

The designer's job is therefore to make intelligence **legible**.

The engineer's job is to make that representation **real**.

The two jobs are inseparable.

---

## 1. READ IN THIS ORDER — NEVER DESIGN FROM MEMORY

Before touching code, read the current source of truth in this order:

1. `HUB/NAYA-MASTER-DESIGN-CONTRACT-V1.md`
2. `HUB/NAYA-MASTER-DESIGN-CONTRACT-V1.json`
3. The relevant room contract in `HUB/ROOMS/`
4. The relevant room directive, when one exists
5. Current implementation at the exact branch/frozen SHA
6. Current #554 coordination state for active/in-flight work
7. The strongest approved design specimen/reference for that surface
8. Current rendered experience, when a deployed/rendered surface exists

Do not design from a remembered conversation.

Do not invent missing decisions.

Do not silently resolve an OPEN contradiction.

If the source and the render disagree, investigate the reason before changing either.

---

## 2. THE PRODUCT MODEL YOU MUST HOLD IN YOUR HEAD

NayaNET is not:

- a homepage plus a dashboard;
- a collection of room pages;
- a chatbot with decorative UI;
- a visualization system;
- a collection of isolated premium components.

It is:

**ONE MAIN SHOW + ELEVEN ROOMS + ONE SHELL + ONE GOVERNED INTELLIGENCE SUBSTRATE.**

The main product concepts are:

### Naya
The intelligence/presence layer.

Naya is not a generic chatbot pasted into every page. Naya should understand the active context, selected object, truth state and authority boundary before making a contextual claim.

### Power Player
The experiential heartbeat.

It is not a media widget. When applicable, audio, artwork, progress, Naya presence and state become one living object.

### Living Sun
The spatial navigation/world model.

It is not decoration. It communicates that the nine core worlds are doors into deeper experiences.

### Rooms
Specialized jobs performed by one intelligence system.

Every room must have a distinct reason to exist.

### Powercasts
The educational/story layer.

They connect the experience to learning and progression rather than acting as decorative media.

### Doors / Connectors
MCP, API/OpenAPI, GitHub App, webhooks, SDK, A2A and other channels are **doors into the same intelligence**, not separate architectures and not separate brains.

The web Hub is one human-facing door.

---

## 3. THE UNIVERSAL DESIGN FORMULA

For every surface, think in this order:

**PURPOSE → INFORMATION → TRUTH → STATE → ACTION → CONSEQUENCE → PRESENTATION**

Never:

**STYLE → COMPONENT → CONTENT → “WHAT SHOULD IT DO?”**

Before visual design, write one sentence:

> **The human is here to ________.**

Then answer:

- What matters now?
- What must be understood first?
- What can the human do?
- What happens after they do it?
- What evidence supports the claim?
- What happens when the capability is unavailable?
- What must remain remembered on return?

If those answers are unclear, the design is not ready.

---

## 4. LAW ZERO

**READABILITY SUPREMACY.**

No color, glow, shadow, gradient, animation, depth treatment, imagery, composition or cinematic effect may make important information harder to read or understand.

A beautiful unreadable surface is a failure.

A beautiful surface whose purpose is unclear is a failure.

A beautiful surface that implies something false is a failure.

---

## 5. THE TEN MASTER LAWS

1. **Purpose before interface.**
2. **Distill before display.**
3. **Recognition before recall.**
4. **One obvious next action.**
5. **State must be perceptible.**
6. **Beauty is function when it improves understanding, trust or emotion.**
7. **Complexity belongs in the machine.**
8. **Design systems are memory.**
9. **The product must feel like one thing.**
10. **Design must learn.**

The benchmark is the floor.

**Study the best → extract principles → synthesize → test → surpass → verify.**

Never imitate a competitor's surface merely because it is fashionable.

---

## 6. COLOR IS A LANGUAGE

Every colored pixel must have a job.

### Obsidian material stack

- World: `#0B0D12`
- Raised: `#12151D`
- Elevated: `#171B25`
- Precision edge: `#252B39`
- Primary text: `#F5F7FB`
- Secondary text: `#AAB2BF`

### Core semantic voices

- Purple `#9d75ff` — Naya signature / primary action
- Indigo `#6675ff` — comprehension / depth / reports
- Sapphire `#55b9ee` — knowledge / information
- Teal `#40d3bb` — connection / flow
- Emerald `#55e39a` — active / available / healthy
- Lime `#b8ee57` — learning / growth
- Yellow `#f1d75a` — attention / signal
- Gold `#e8b64c` — consequence / proven value
- Orange `#ff9a5a` — relationship / action / movement
- Rich orange `#ff7a3d` — transition / momentum
- Red `#ff5a6e` — blocked / failed
- Magenta `#d86cff` — human significance / expression

### Absolute color discipline

Never:

- use red because it looks exciting;
- use gold because it looks premium;
- use purple everywhere because it is “the Naya color”;
- use a room theme as wallpaper;
- invent a new color because an accent is convenient;
- use a gradient that merges semantic meanings into one ambiguous signal.

The test is literal:

> **Point at any color. Name its job.**

If you cannot name the job, remove the color.

---

## 7. THE THREE COLOR FLOWS

### Hierarchy

**WHITE WORDS → ROOM THEME → SEMANTIC STATE → GOLD EXTRAORDINARY**

Color guides attention. It does not replace hierarchy.

### State

**REST → AWARE/HOVER → PRESS → PROCESSING → SUCCESS / FAILURE**

A color change must have a state cause.

### Theme

**ENTER → SIGN → RECEDE → RETURN AT MEANINGFUL ACTION**

A room's identity is felt, not sprayed across every surface.

---

## 8. TYPOGRAPHY

Use the shared type system.

- Hero: `clamp(30px,4.6vw,52px)`, weight 800
- Title: 23px / 800
- Head: 17px / 700
- Body: 16px floor, 17–18px target
- Secondary: 14–15px
- Labels: 11px minimum, uppercase/tracked

Never shrink the type to rescue a bad composition.

Never rely on tiny metadata to carry essential meaning.

Never use pale-purple body copy.

Typography is architecture.

---

## 9. SPACING

Use only:

**4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96**

Core rhythms:

- micro gap: 8
- related group: 16
- card padding: 24
- section rhythm: 48–64

Arbitrary spacing is not craftsmanship.

It is drift.

---

## 10. DEPTH

NayaNET depth is engineered, not simulated with borders.

Order:

**MATERIAL CORE → EDGE LIGHT → RESTRAINED SPECULAR → CAST SHADOW → SEMANTIC AURA → STATE AMPLIFICATION**

The object should appear to exist at a location in the interface's physical space.

Do not substitute:

- a 2px border for depth;
- a glow for material;
- a gradient for hierarchy;
- glassmorphism for intelligence.

---

## 11. THE FIVE CANONICAL OBJECT CLASSES

### 01 — POWER OBJECT
Buttons and consequential actions.

### 02 — INTELLIGENCE SURFACE
Boards, presentation surfaces and destination objects.

### 03 — IDENTITY PORTAL
Inputs, fields and forms that establish or collect consequential identity/context.

### 04 — ENERGY PATH
Progress, playback, loading and flow indicators.

### 05 — INTELLIGENCE ICON
Jewel marks, symbolic controls and state-carrying glyphs.

Every object follows:

**DEPTH → LIGHT → STATE → RESPONSE → CONSEQUENCE**

---

## 12. BUTTONS

A NayaNET button is a physical interface object.

### Primary
- 14×28 padding
- 48px minimum visual height
- 17px / 800 typography
- white label
- purple `#9d75ff`
- verb-first label

Examples:

- “Verify now”
- “Open the proof”
- “Save changes”

Avoid “OK”, “Submit”, “Continue” where a more consequential verb is known.

### Seven states

1. Rest
2. Hover / aware
3. Focus
4. Press
5. Processing
6. Success
7. Failure

The system must show a meaningful consequence after the operation.

A button that looks active but has no real operation is a defect.

A button that triggers an action but never communicates the result is also a defect.

---

## 13. INPUTS

Inputs are identity portals, not blank rectangles.

The field should:

- have material presence;
- show focus;
- preserve readable labels;
- expose validation honestly;
- combine visually with its consequential action;
- remain keyboard operable.

The input + button relationship must tell one story:

**ENTER → UNDERSTAND → READY → ACT → CONSEQUENCE**

---

## 14. BOARDS AND INTELLIGENCE SURFACES

A board is a destination, not a decorated card.

The user should understand:

- what the board is;
- why it matters;
- what state it is in;
- what can be done;
- what happens after entry.

The board may become:

- a deeper detail environment;
- a proof surface;
- an intelligence object;
- a contextual world.

Do not force every board into a rectangular SaaS card.

Do not choose exotic shapes unless shape actually communicates purpose.

---

## 15. ICONS

NayaNET icons are a coherent visual civilization.

They require:

- geometric consistency;
- optical balance;
- consistent stroke logic;
- semantic silhouette;
- state awareness;
- consistent visual weight.

Never replace them with random emoji, stock icon packs or inconsistent generic glyphs.

The jewel system is memory.

Icon labels are still available when recognition cannot safely carry meaning alone.

---

## 16. MOTION

Motion has exactly one job:

**communicate a truthful change.**

Core timings:

- fast: `.18s`
- medium: `.28s`
- slow: `.5s`

Easing:

`cubic-bezier(.16,.84,.22,1)`

Prefer transform and opacity.

Reduced motion is mandatory.

Never animate merely to prove that the designer can animate.

The rule is:

**STATE CHANGES → MOTION MAY EXPLAIN IT.**

Not:

**NOTHING CHANGED → ANIMATION ANYWAY.**

---

## 17. THE UNIVERSAL EXPERIENCE ARC

Every major surface should move through:

**PRESENCE → RECOGNITION → DISTILLATION → INVITATION → FLOW**

### Presence
The system is here.

### Recognition
The human understands where they are and is recognized only when true.

### Distillation
The few things that matter arrive first.

### Invitation
One obvious next action appears.

### Flow
The human proceeds without reconstructing context.

If the experience instead feels like “a grid of components”, return to the arc.

---

## 18. THE FOUR QUESTIONS

Every surface, drawer, dialog and important object must answer:

1. **WHERE AM I?**
2. **WHAT MATTERS NOW?**
3. **WHAT CAN I DO?**
4. **WHAT HAPPENS NEXT?**

Evaluate them at:

- 1 second;
- 3 seconds;
- 30 seconds;
- return visit.

---

## 19. NAYANET MAIN SHOW

The Main Show is not a landing page.

It is not a dashboard.

It is the first intelligent experience:

**Naya presence → distilled intelligence river → clear next action → contextual Naya**

No KPI wall first.

No navigation wall first.

No generic hero section first.

The first authenticated experience should land in the main intelligence experience, preserving the Human Director's shell ruling.

---

## 20. THE SHELL

Current shell direction:

- two quiet corner controls;
- top-left → room drawer;
- top-right → product/navigation drawer;
- Smart Feed is the Main Show and is not duplicated as a drawer room;
- one coordinated sticky zone only when the current director ruling still permits the mode lens;
- no competing persistent rail;
- drawer transitions preserve focus, scroll and context.

Open decisions remain open until ruled.

Do not silently “clean them up” by inventing an answer.

---

## 21. ROOM FUNCTION COMES BEFORE ROOM ART

The master room map is:

### Main Show / Hub Home
**Job:** arrive oriented, recognized and ready to move.  
**Visual:** calm obsidian + living Naya + one dominant intelligence region.  
**Action:** open highest-value beat / Ask Naya / continue.

### Smart Feed
**Job:** see useful intelligence/activity now.  
**Visual:** emerald intelligence river.  
**Action:** open or act on highest-value item.

### Your Intelligence Today
**Job:** know what matters right now.  
**Visual:** magenta human-significance highlight reel.  
**Action:** act on top next move.

### Your Reports
**Job:** understand meaning across time.  
**Visual:** indigo thesis-first film room.  
**Action:** inspect or act on key finding.

### Intelligent Library
**Job:** find, trust and reuse intelligence.  
**Visual:** sapphire calm archive/search environment.  
**Action:** search/open intelligence.

### Smart Connect
**Job:** understand and configure legitimate connection doors.  
**Visual:** portal bay; current main theme emerald, teal reserved as the candidate connection/flow semantic.  
**Action:** connect/configure a real door.

### Smart Ledger
**Job:** inspect what happened and what proves it.  
**Visual:** black-box proof room; gold is sparse.  
**Action:** inspect event proof.

### Your Connections
**Job:** understand governed relationships.  
**Visual:** orange constellation/list hybrid when useful.  
**Action:** inspect/manage a relationship.

### Smart Lists
**Job:** organize intelligence for action without duplication.  
**Visual:** purple mission table.  
**Action:** open/create list.

### Smart Mail
**Job:** prioritize and respond to real communication.  
**Visual:** sapphire signal room; important communication first.  
**Action:** open highest-value conversation.

### Smart Spaces
**Job:** enter/resume durable context.  
**Visual:** lime worlds; stable shell, changing context.  
**Action:** enter/resume space.

### Settings
**Job:** control the relationship with NayaNET.  
**Visual:** neutral control deck; precision without developer-console noise.  
**Action:** contextual setting control.

**The exact room contract is the authority for implementation details.**

---

## 22. YOUR INTELLIGENCE TODAY — SPECIAL OPERATING MODEL

This room is the Daily Intelligence Cockpit.

Its job is not to display a day.

Its job is to **distill the day.**

The room must progressively answer:

**ORIENT → SEE → UNDERSTAND → PRIORITIZE → REMEMBER → QUESTION → ACT → VERIFY**

The build hierarchy is:

**NOW → NEXT → WATCH → LEARNED → WAITING → RECENT PROOF**

Core intelligence concepts:

### WHAT CHANGED
What is different from the prior relevant state?

Every surfaced change should explain:

- what moved;
- why it matters;
- its current truth state;
- evidence.

### WHAT I LEARNED
Distinguish:

**INFORMATION → UNDERSTANDING → CHANGE → DECISION → KNOWLEDGE**

Do not label raw notes as learning merely because the word “learn” appears.

### WHAT MATTERS NOW
Rank supported relevance.

Explain WHY.

Never invent urgency.

### WHAT TO REMEMBER
Let the human preserve durable carry-forward.

Tomorrow should start from legitimate continuity.

### WHAT AM I MISSING
Expose:

**KNOWN / CHANGED / UNCERTAIN / MISSING**

Unknown is a meaningful state.

**UNKNOWN ≠ SUCCESS.**

### PROOF
Evidence stays one level deeper:

**GLANCE → UNDERSTAND → INSPECT → PROVE**

---

## 23. TODAY-SPECIFIC VISUAL LANGUAGE

Today wears **magenta `#d86cff`** because it represents human significance.

Magenta should:

- sign the threshold;
- identify the room;
- mark meaningful human significance;
- return at important room actions.

It should not:

- flood the entire canvas;
- become wallpaper;
- override semantic state;
- make every object look identical.

Per-play color may communicate stable object identity only when that meaning is real.

Gold remains reserved for consequential turning points/carry-forward.

Purple remains primary action/Naya energy.

Red remains blocked/failed.

---

## 24. HONEST INTELLIGENCE

Never manufacture:

- intelligence;
- activity;
- counts;
- personalization;
- relationships;
- reports;
- receipts;
- completion;
- proof;
- liveness;
- progress.

A quiet room is better than fake richness.

A button that does nothing is worse than no button.

An unavailable capability must be visibly unavailable.

A NOT_VERIFIED result is legitimate.

A claim must never climb the truth ladder without evidence:

**IMPLEMENTED → INSPECTED → VERIFIED → LIVE VERIFIED → HUMAN APPROVED**

---

## 25. FUNCTION ↔ VISUAL RECONCILIATION

Run BOTH directions.

### Function → visual

For every required function:

- where is it represented?
- what does it look like before action?
- what does it look like while working?
- what does success look like?
- what does failure look like?
- how does recovery work?
- where is evidence?

### Visual → function

For every visible object:

- what is its purpose?
- what truth does it communicate?
- what state causes its color/light/motion?
- what action does it afford?
- what causal path follows?
- what consequence follows?
- what canonical object owns the result?
- what happens when the capability is unavailable?

If an object cannot answer these questions, do not polish it.

Fix or remove it.

---

## 26. PROGRESSIVE DISCLOSURE

Do not dump the system's knowledge onto the human.

Use:

**GLANCE → UNDERSTAND → INSPECT → PROVE**

The first layer communicates meaning.

The second provides useful detail.

The third provides inspection.

The fourth provides proof.

The deep layer must not dominate first comprehension.

---

## 27. RESPONSIVE LAW

Mobile is not a shrunk desktop.

The designer must intentionally decide:

- what remains;
- what reorders;
- what collapses;
- what becomes a drawer;
- what stays persistent;
- what becomes thumb reachable;
- how focus order follows cognitive order.

No critical action may disappear merely because the viewport is small.

---

## 28. ACCESSIBILITY LAW

Accessibility is product quality, not a compliance afterthought.

Always verify:

- semantic structure;
- keyboard operation;
- visible focus;
- logical focus order;
- hit targets;
- non-color state communication;
- meaningful labels;
- reduced motion;
- text readability;
- chart/text alternatives where applicable.

The interface must remain understandable without relying on glow, color or motion alone.

---

## 29. PERFORMANCE LAW

The human must not pay a speed tax for spectacle.

Before shipping:

- test first paint;
- test main interaction;
- test mobile;
- test heavy media;
- test animation cost;
- test layout shift;
- remove unnecessary work.

Premium feeling comes from precision.

Not from CPU consumption.

---

## 30. THE “SOFTWARE, NOT WEBSITE” TEST

Ask:

Does this feel like a living tool?

Or does it feel like a marketing website wearing application chrome?

A website:

- explains itself endlessly;
- displays sections;
- decorates;
- pushes calls to action.

A NayaNET interface:

- knows context;
- presents useful state;
- responds;
- lets the human act;
- preserves continuity;
- reveals depth;
- remembers legitimate context;
- feels alive because the intelligence is alive.

---

## 31. THE “NOT JUST GLOW” TEST

If the design still works after removing every glow, ask:

- Is hierarchy still strong?
- Is purpose still obvious?
- Does the object still feel physical?
- Is the state still understandable?
- Does the experience still feel premium?

If the answer is no, the design is depending on effects instead of craft.

---

## 32. THE “EXPENSIVE WITHOUT DECORATION” TEST

Premium quality must survive with restrained visual effects.

The expensive feeling comes from:

- proportion;
- typography;
- spacing;
- material hierarchy;
- optical balance;
- interaction quality;
- response;
- consistency;
- restraint.

Decoration is the final 5%, not the first 95%.

---

## 33. AUTOMATIC REJECTIONS

Reject without debate:

- dashboard-first composition when the room is not a dashboard;
- KPI walls as default intelligence;
- fake personalization;
- fake intelligence;
- fake progress;
- fake completion;
- fake liveness;
- dead buttons;
- buttons with no consequence;
- tiny body text;
- tiny labels;
- flat bordered depth;
- decorative glow;
- random motion;
- random colors;
- arbitrary spacing;
- duplicate shell systems;
- duplicate intelligence stores;
- duplicate room presentations;
- navigation that requires decoding;
- screenshot-optimized layouts that fail in use;
- mobile layouts that are desktop leftovers;
- beautiful surfaces that cannot explain their function.

---

## 34. THE SELF-EVALUATION LOOP

No work is “ready” because the builder likes it.

### Step 1 — Freeze
Work from exact bytes / exact SHA.

### Step 2 — Render
Render the exact experience as the Human Director will encounter it.

### Step 3 — Four tests
- **1-second:** where does the eye land?
- **3-second:** do I know where I am, what matters and what I can do?
- **30-second:** can I take the obvious next action?
- **Squint:** does the hierarchy survive?

### Step 4 — Measure
Measure:

- typography;
- spacing;
- color semantics;
- buttons;
- state completeness;
- motion;
- accessibility;
- responsive behavior.

### Step 5 — Function check
Exercise the actual causal paths.

### Step 6 — Truth check
Verify every visible claim against the canonical source.

### Step 7 — Self-score
Score the appropriate design dimensions with one evidence line each.

### Step 8 — Attack your work
Try to prove yourself wrong.

Ask:

> “What would make this obviously not 10/10?”

Do not hide the answer.

### Step 9 — Name omissions
Write what was deliberately NOT built and why.

### Step 10 — Independent challenge
A second seat judges the frozen SHA.

Self-score is diagnostic only.

---

## 35. THE HANDOFF CONTRACT

A handoff must contain:

- exact SHA;
- exact surface;
- human job;
- primary action;
- master-contract sections applied;
- room-contract sections applied;
- KEEP / IMPROVE / REPLACE / REMOVE decisions;
- rendered evidence;
- 1s / 3s / 30s / squint results;
- measurements;
- state evidence;
- accessibility evidence;
- responsive evidence;
- causal-path evidence;
- truth/provenance evidence;
- known limitations;
- deliberate omissions;
- self-score;
- independent-review request.

The handoff sentence should be:

> **Ready for independent challenge: exact bytes were rendered, measured and tested; remaining unknowns and omissions are named.**

Never:

> “Looks good.”

---

## 36. DESIGN MEMORY

A correction from the Human Director is not just a one-time fix.

Capture:

**OBSERVATION → EVIDENCE → DECISION → CHANGE → HUMAN OUTCOME → SCORE EFFECT → LESSON → NEXT TEST**

The goal is not to keep Shawn repeating the same correction.

The goal is that the system learns once and remembers.

---

## 37. TEAM NAYA COORDINATION

Before building against an active surface:

- inspect #554;
- look for in-flight work;
- do not create duplicate vehicles;
- identify the current branch/head;
- state your lane;
- record material defects;
- preserve the one-owner build boundary.

Every consequential update to #554 should state:

**ACTOR → OBJECTIVE → SOURCE HEAD → EVIDENCE → STATUS → UNKNOWNS/BLOCKERS → AUTHORITY → ONE NEXT ACTION**

Standing law:

**SEE SOMETHING NOT-RIGHT → CAPTURE → EVIDENCE → #554 → CLASSIFY → FIX/TRACK → VERIFY → CLOSE/HAND OFF**

---

## 38. THE HUMAN DIRECTOR BOUNDARY

The designer can:

- observe;
- research;
- synthesize;
- propose;
- implement inside granted scope;
- self-test;
- identify contradictions.

The designer cannot silently:

- create authority;
- change constitutional meaning;
- promote a candidate into canonical truth;
- invent identity;
- invent proof;
- decide unresolved Human Director questions by taste.

Capability is not authority.

Presentation is not proof.

A design file is not permission.

---

## 39. THE FINAL EXAM — WHAT “UNDERSTANDING” MEANS

Before a designer may credibly claim mastery, they should be able to explain in plain language:

### A. Why
Why does the room exist?

### B. What
What is the human trying to accomplish?

### C. Intelligence
What real intelligence powers the experience?

### D. Truth
What is known, unknown, verified, blocked or unavailable?

### E. Representation
Why is each piece of information represented the way it is?

### F. Interaction
What does the human do and what happens next?

### G. Material
Why does the object look and feel physical?

### H. Color
What does every important color mean?

### I. Hierarchy
Where does the eye land and why?

### J. Continuity
What survives when the human leaves and returns?

### K. Proof
How do we know the experience works?

### L. Learning
What did we learn from the last iteration?

A designer who can style the page but cannot answer these has not understood the product.

---

## 40. THE FINAL BUILD COMMAND

Build NayaNET as an intelligent environment.

Do not decorate intelligence.

**Distill it.**

Do not hide complexity in the human interface.

**Absorb it into the machine.**

Do not make components merely pretty.

**Give them purpose, material, state, response and consequence.**

Do not create eleven different visual languages.

**Create one NayaNET species with room-specific expression.**

Do not use animation to fake life.

**Let real intelligence produce real change.**

Do not manufacture richness when the system is uncertain.

**Make uncertainty legible.**

Do not chase screenshots.

**Build for humans.**

Do not settle for “premium-looking.”

**Engineer premium behavior.**

And before anything reaches the Human Director, be able to answer:

> **What is this? Why is it here? What does it mean? What can I do? What happens next? What is true? How do I know?**

If those answers are not immediately clear, keep working.

---

## 41. THE NORTH STAR

**Maximum Verified Human Value per Moment.**

The experience should progressively deliver:

**ORIENTATION → UNDERSTANDING → ACTION → CONSEQUENCE → MEMORY → COMPOUNDING VALUE**

Beauty attracts attention.

Utility earns use.

Truth earns trust.

Memory creates continuity.

Governance creates safety.

Exceptional craft makes the system unforgettable.

That is NayaNET.
