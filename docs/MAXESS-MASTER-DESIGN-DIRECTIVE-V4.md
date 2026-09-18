# MAXESS RESULTS — MASTER DESIGN DIRECTIVE V4

Status: PROPOSED — ADVERSARIAL / ANTI-DRIFT MASTER DIRECTIVE
Repository: `SoulSchoolAcademy/MaxRESULTS`
Branch: `maxess-results-v21-working`
Relationship: V4 supersedes V3 when the two documents conflict. V3 rules remain active unless explicitly replaced below.

Purpose: make the intended MAXESS experience sufficiently precise that an implementing AI, human designer, frontend engineer, QA system, and non-technical reviewer converge on substantially the same result without guessing.

This is a design-and-execution contract, not a mood board. It incorporates lessons learned from MAXESS implementation: context loss, multiple renderer ownership, technically valid but visually wrong output, weak generated copy, oversized edits, stash-based mutation loss, and QA passes that do not prove human excellence.

---

# 01 — NON-NEGOTIABLE NORTH STAR

DATA
→ INSIGHT
→ UNDERSTANDING
→ ACTION
→ CAPABILITY

MAXESS must turn an assessment result into an extraordinary personal experience that helps a user:

1. feel seen;
2. understand the result;
3. recognize what is already working;
4. understand the shape of their capability;
5. understand what the result means in practical language;
6. discover useful pathways through Naya;
7. trust the system;
8. see a clear next action;
9. choose whether to continue.

MAXESS is not a generic dashboard, school report card, wall of cards, sales funnel disguised as a report, effects showcase, or excuse to add more sections.

MAXESS is:

A PERSONAL REVEAL
→ USEFUL UNDERSTANDING
→ VISUAL SELF-RECOGNITION
→ PROOF OF DEPTH
→ TRUSTED INVITATION.

---

# 02 — ULTIMATE HUMAN RESULT

The user should finish thinking:

“I feel seen.”
“I know my score.”
“I understand what it means.”
“I can see what makes up my score.”
“I can see my pattern.”
“I recognize something I am already good at.”
“I understand where I may grow.”
“I can see how Naya could help.”
“I understand what is included.”
“I know what I can do next.”
“I want the keys.”

If a section does not advance one of these outcomes, it must justify why it exists.

---

# 03 — SOURCE-OF-TRUTH PRECEDENCE

When sources disagree, use this order:

1. explicit human-approved locked decision in the active directive;
2. current MAXESS Master Contract;
3. current MAXESS product specification;
4. current authoritative data contract;
5. current active component ownership registry;
6. current source implementation;
7. previous directives and legacy layers;
8. AI inference.

AI inference is LAST.

The AI must never silently choose a lower-precedence source when a higher-precedence source exists.

If two high-authority sources conflict and precedence cannot resolve them:

CONFLICT
→ OPTIONS
→ IMPACT
→ RECOMMENDATION
→ REQUIRED HUMAN DECISION.

Do not invent a compromise.

---

# 04 — DEFINITION OF AAA / 10

AAA does not mean more.

AAA means every meaningful choice has a job and earns its place.

A major experience unit is AAA only when all have evidence:

PURPOSE
+ PSYCHOLOGY
+ VISUAL COMMUNICATION
+ COPY
+ DATA CORRECTNESS
+ INTERACTION
+ RESPONSIVE BEHAVIOR
+ ACCESSIBILITY
+ PERFORMANCE
+ EDITABILITY
+ PRESERVATION
+ CONVERSION ROLE.

Target unit score: 9.5+.

No major scoring category below 9.

Automated QA is necessary but is not the definition of excellence.
A source diff is proof of change, not proof of quality.
A screenshot is proof of appearance, not proof of correctness.

AAA requires convergence of:

HUMAN RESULT
+ VISUAL RESULT
+ TECHNICAL RESULT.

---

# 05 — ANTI-DRIFT TRANSLATION RULE

Terms such as premium, beautiful, high-tech, 3D, alive, luminous, organic, memorable, and extraordinary are not implementation instructions by themselves.

Every qualitative requirement must be translated into:

OBJECT
+ MATERIAL
+ GEOMETRY
+ COLOR
+ LIGHTING
+ SPACING
+ MOTION
+ INTERACTION
+ PSYCHOLOGICAL JOB
+ ACCEPTANCE TEST.

If a requirement cannot be translated into those concrete terms, it is not yet implementation-ready.

---

# 06 — NO FLAT PRIMARY DESIGN

Flatness is a defect for primary MAXESS visual objects.

Primary objects include hero object, signature Orb, mini-Orbs, major CTA buttons, report sheet, major Naya presence, pathway doors, and final CTA.

Required depth vocabulary:

- layered surfaces;
- edge definition;
- internal highlight;
- lower shadow;
- ambient shadow;
- controlled glow;
- scale hierarchy;
- optical separation;
- restrained motion.

Forbidden:

- flat primary buttons;
- generic gradient rectangles;
- random glassmorphism;
- fake chrome;
- uncontrolled neon;
- excessive blur;
- decorative effects that reduce readability.

Target:

TACTILE
→ LUMINOUS
→ ORGANIC
→ POLISHED
→ CONTROLLED.

---

# 07 — EXPERIENCE ARCHITECTURE

Primary narrative units:

01 — NAYA ARRIVAL / HERO REVEAL
02 — SCORE ORB + FIVE MINI-ORBS
03 — PERSONAL AI MASTERY REPORT / PDF MASTER
04 — FINGERPRINT / PATTERN
05 — STRENGTH / RECOGNITION
06 — NAYA IN PRACTICE / VIDEO EXPERIENCE
07 — ONE MEMBERSHIP / EVERYTHING INCLUDED + 18 NAYA MASTERS
08 — FINAL NAYA INVITATION + MASTER KEY CTA

Explicitly remove from the primary narrative:

- standalone Opportunity / Lever chapter;
- standalone Practice / Playground chapter;
- Results-page login gate.

Useful existing functionality may remain technically where it does not compete with the narrative.

---

# 08 — ATTENTION BUDGET

Only one object owns primary attention in each unit.

01 Hero / Orb Reveal
02 Mini-Orb Constellation
03 Personal Report Sheet
04 Fingerprint
05 Strength Orb
06 Video Theater
07 Naya Doors
08 Final Invitation / CTA

Supporting elements must be visibly subordinate.

WHEN EVERYTHING SHOUTS, NOTHING MATTERS.

No unit may contain competing primary CTAs, equal-weight hero objects, or multiple dominant headings.

---

# 09 — SCENE CHOREOGRAPHY

Preferred rhythm:

DARK REVEAL
→ ELECTRIC DARK DATA
→ WARM EDITORIAL REPORT
→ DARK PATTERN
→ DRAMATIC RECOGNITION
→ CINEMATIC VIDEO
→ PREMIUM LIGHT MEMBERSHIP
→ DARK / PURPLE INVITATION.

Dark = depth / intelligence / mystery / Naya / Orb / discovery.
Light = reading / clarity / ownership / reflection.
Purple = transformation / possibility / commitment.
Gold = earned achievement / milestone / rarity.

Neighboring scenes must have intentional contrast.

A scene transition must communicate a cognitive transition. Preferred devices are Orb energy flow, constellation migration, atmospheric hue change, organic curve, luminous edge sweep, or subtle light seam. Use one strong device per transition.

---

# 10 — MASTER COLOR TOKENS

Primary Black `#06040B`
Deep Black `#0B0810`
Raised Dark `#120C1D`
Pure White `#FFFFFF`
Warm Light `#F7F4FA`
Soft Editorial `#EDE8F2`
Deep Purple `#35106F`
Electric Purple `#8B3DFF`
Luminous Purple `#C58CFF`
Ultra-Light Purple `#E9D6FF`
Gold `#D8B25C`
Warm Gold `#F0D58B`

Dimension accents:
Direction `#FF9D3D`
Communication `#FFD84A`
Evaluation `#39DF91`
Iteration `#4C9DFF`
Systems Thinking `#965DFF`

These colors are semantic tokens. Do not alter them for arbitrary variety.

---

# 11 — SCORE-STAGE COLOR ENGINE

Stage bands:

Supporting 0–20
Foundation 21–50
Developing 51–75
Advancing 76–90
Mastering 91–100

Stage color must interpolate continuously within bands and visually smoothly across boundaries.

Supporting `#FF3B5C` → `#C52B5B`
Foundation `#E6454D` → `#FF8A35`
Developing `#FF9D3D` → `#FFD84A`
Advancing `#39DF91` → `#4C9DFF`
Mastering `#8B3DFF` → `#C58CFF`

Optional milestone highlight `#F0D58B`.

Stage color may affect the Orb arc, Orbital Bead, halo, stage pill, and selected mini-Orb emphasis. It must never reduce text contrast or replace semantic labels.

---

# 12 — TYPOGRAPHY CONTRACT

Hero display: 44–88px desktop, 800–950 weight, 0.92–1.02 line height, -0.055em to -0.075em tracking.

Section titles: 34–64px, 800–900 weight, 0.98–1.08 line height, -0.04em to -0.06em tracking.

Body: 17–19px desktop, 15–17px mobile, 1.55–1.70 line height.

Micro labels: 10–12px, 800–950 weight, 0.14em–0.22em tracking, uppercase.

Score: 96–170px desktop, 68–104px mobile, 900–950 weight, -0.06em tracking.

Optical hierarchy overrides raw mathematical size.

---

# 13 — BUTTON CONTRACT

Every major button must declare:

NAME
PURPOSE
LOCKED TEXT
ICON
MATERIAL
GEOMETRY
IDLE
HOVER
FOCUS
PRESSED
ACTIVE
DISABLED
MOTION
ACCESSIBILITY
CONVERSION ROLE.

## B4 — LISTEN TO NAYA

Base `#08070D`
Border `1px solid rgba(255,255,255,.28)`
Purple perimeter `rgba(197,140,255,.65)`
Inner highlight `rgba(255,255,255,.08)`
Shadow `0 18px 40px rgba(0,0,0,.40)`
Height 54–60px desktop / 48–54px mobile.
Radius 999px.
Text white, weight 800.
Icon: play triangle inside circular sound/wave ring.

The button must look physically raised, crisp, premium, black, and invitation-like.

Hover: +2px lift, +1.5% scale, +4% brightness.
Pressed: 0px lift, .985 scale.
Playing: pause icon + soft sound-ring pulse.
Reduced motion: no transform; state still changes.

## B6 — CHOOSE YOUR KEY

Locked text: `CHOOSE YOUR KEY`
Supporting line: `ZERO COST TO START`

Material: luminous purple layered surface with visible physical separation from the final scene.

This is the strongest commitment object on the page.

---

# 14 — ICON CONTRACT

All finished icons belong to one family:

- rounded geometry;
- consistent stroke logic;
- consistent optical scale;
- clean negative space;
- readable at small sizes.

Semantic examples:
LISTEN = waveform / sound ring
PLAY = play capsule
EXPLORE = compass / directional spark
PATTERN = constellation
STRENGTH = radiant star
PATHWAY = door / route
ACTION = directional energy
AI = intelligence spark
SUCCESS = radiant check.

Do not ship arbitrary Unicode symbols as the premium icon layer.

---

# 15 — SIGNATURE ORB MODEL

The MAXESS Orb is a first-class brand asset.

Layer order:

1 atmospheric field
2 outer halo
3 secondary orbit
4 MAXESS ORBITAL BEAD
5 score arc
6 luminous shell
7 inner energy field
8 dark core
9 score number
10 micro label
11 optional stage pill.

Hero diameter:
320–430px desktop
260–330px tablet
210–270px mobile.

Core:
`radial-gradient(circle at 35% 28%, #1A1128 0%, #0B0810 45%, #050408 100%)`

Shell: subtle upper-left highlight only.
Score arc: 6–10px desktop, 5–8px mobile, rounded caps, actual score percentage.
Outer orbit: 1px, 30–60% opacity, 8–12s rotation.
Breathing: 5–7s cycle, scale 0.985–1.000, no layout movement.

The Orb must visually communicate: “this number is alive, meaningful, and part of a larger system.”

---

# 16 — MAXESS ORBITAL BEAD

MANDATORY.

The small luminous ball travelling around the outside of the Orb is a named identity component.

Name: `MAXESS ORBITAL BEAD`

Psychological job: prevent the Orb from becoming a static score badge.

User inference: “This system is alive and active.”

Geometry: 10–16px desktop; 8–12px mobile.
Position: 100–108% of Orb radius.
Orbit duration: 8–12s hero; 9–14s mini-Orbs.
Velocity: constant or near-constant.
Core: white-to-luminous-purple or score-aware color.
Halo: inner 4–8px; outer 12–24px.

When Naya speaks:
brightness +20–35%; halo +10–20%; orbit ring +10–20%.

Idle: continuous quiet motion; no flashing.
Reduced motion: stop positional movement; retain static luminous bead and safe non-transformative glow.

The Bead is required in the main Orb and in every mini-Orb unless a specific accessibility/device constraint requires an equivalent static representation.

---

# 17 — FIVE MINI-ORB CONSTELLATION

The five dimensions are living components, not generic score circles.

Center: main Score Orb.

Desktop normalized anchors:
Direction `50% 12%`
Communication `86% 33%`
Evaluation `72% 82%`
Iteration `28% 82%`
Systems Thinking `14% 33%`

Diameter:
Desktop 92–132px.
Tablet 78–112px.
Mobile 64–92px.

Each mini-Orb contains:

- dark core;
- dimension glow;
- score ring;
- Orbital Bead;
- score;
- short dimension label.

Selection:
selected Orb +8–12%; selected Bead +20–35% brightness; connection brightens; other Orbs dim 8–15%; interpretation panel enters.

Do not collapse to a generic five-card grid.

---

# 18 — PERSONAL REPORT / PDF MASTER

Psychological job:
turn results into something personal the user feels ownership of.

The report must feel like:

A PREMIUM PERSONAL LETTER
+
A TRUSTED PROFESSIONAL REPORT.

Warm Light scene `#F7F4FA`.

Report sheet:
860–920px max width
22–30px radius
1px warm gray/lilac border
soft layered shadow
optional extremely subtle paper texture only if legibility and performance remain excellent.

Required hierarchy:

masthead
name
score
stage
personal interpretation
what it means
what is already strong
pattern
recommended focus
Naya note
next invitation.

The online report and PDF must share the same hierarchy and content meaning.

Nothing critical to understanding the report may exist only online.

---

# 19 — NAYA PROFILE ASSET CONTRACT

Approved Naya portraits are named product assets.

NAYA BLACK
NAYA WHITE

Use by scene contrast.

Never substitute a random Naya face.

Every Naya Master uses the approved profile treatment consistently.

The portrait must communicate that Naya is introducing the specialist, not merely decorating the card.

---

# 20 — COPY AUTHORITY + NO FILLER

Three copy types only:

LOCKED
DATA-FILLED
GENERATED-BY-NAYA.

Locked copy cannot be rewritten without explicit human approval.

Data-filled copy keeps fixed sentence structure and inserts authoritative variables.

Generated Naya interpretation is constrained to approved tone, length, inputs, purpose, and prohibited claims.

Tone:
warm, intelligent, direct, specific, truthful, human, helpful, non-judgmental, non-salesy.

No filler copy.

Every sentence must primarily help the user:
UNDERSTAND
FEEL
TRUST
REMEMBER
ACT.

If it does none, delete it.

Generated interpretation maximums:
Hero 45 words; score meaning 90; dimension 60; pattern 90; strength 80; Master relevance 45 per Master; final invitation 65.

Prohibited generated claims:

- invented facts;
- invented scores;
- invented history;
- diagnosis;
- guaranteed outcomes or income;
- false urgency;
- unsupported scientific certainty;
- fabricated pathway relevance.

---

# 21 — PERSONALIZATION CONTRACT

Use the user's name only when authoritative identity exists.

Recommended frequency:
Hero once.
Report masthead once.
Optional Naya report note once.
Final invitation once.

Never fabricate a name.

Results-page login is not mandatory and is not part of this directive.

---

# 22 — RESPONSIVE INVARIANTS

Across desktop, tablet, mobile:

- Naya remains identifiable;
- score remains dominant data point;
- Orb remains same recognizable object;
- Orbital Bead remains visible or has intentional static equivalent;
- five dimensions remain visibly related to the score;
- primary CTA remains primary;
- reading order remains logical;
- no critical copy clips;
- controls remain operable;
- sections do not become flat merely because of breakpoint constraints.

Mobile is a re-composition, not a shrink.

---

# 23 — ACCESSIBILITY INVARIANTS

Never rely on color alone for meaning.

Every animation has reduced-motion behavior.

Every interactive control has accessible name, keyboard access, visible focus, adequate target size, and state communication beyond color.

SVGs need accessible text alternatives.

Contrast must remain appropriate for actual type size and weight.

---

# 24 — DATA CONTRACT

Production data MUST originate from `window.MAXESS_RESULT`.

Never hard-code a production score.
Never create a competing scoring engine.
Never invent stage data.
Never invent dimension scores.

Missing data must degrade gracefully without fabrication.

Visual transformation may change appearance but never facts.

---

# 25 — ACTIVE OWNER CONTRACT

Exactly one visible active owner per major component.

Before editing identify:

COMPONENT
→ OWNER
→ SOURCE REGION
→ DATA DEPENDENCIES
→ STYLE DEPENDENCIES
→ RENDER PATH.

A historical renderer is not active merely because it contains similar markup.

A QA tool is not a product owner.

If ownership cannot be proven, STOP BEFORE MUTATION.

---

# 26 — EDIT BOUNDARY CONTRACT

MICRO EDIT = one component or one local property family.
SECTION EDIT = all dependent components inside one experience unit.
RELEASE EDIT = cross-section architecture or contract change.

Micro-edit rule:
NO UNRELATED SECTION CHANGES.

Before commit compare changed regions against declared scope.

If unrelated source regions change without explicit dependency justification:
FAIL THE EDIT.

---

# 27 — MUTATION CHECKPOINT CONTRACT

Verified product mutation must never exist only in stash, working tree, chat, or temporary files.

Permanent flow:

MUTATE
→ PROVE SOURCE DELTA
→ COMMIT
→ PUSH
→ BUILD
→ VERIFY
→ RESCORE
→ FREEZE
→ CONTINUE.

Do not move to the next unit while a verified mutation is only local.

---

# 28 — QA SEPARATION

MICRO QA checks local syntax, owner, scope, and behavior.
SECTION QA checks the complete experience unit.
RELEASE QA checks cross-page integrity and readiness.

Do not use a release gate to avoid local visual judgment.
Do not use a section gate to excuse data failure.
Do not use visual review to excuse syntax failure.

---

# 29 — OSCAR / HUMAN QUALITY GATE

Automated tests ask:
“Did machine requirements pass?”

Oscar asks:
“Does this feel exceptional?”

Oscar must actively search for:

- generic treatment;
- weak hierarchy;
- flatness;
- clutter;
- weak contrast;
- weak copy;
- unnecessary text;
- unnecessary sections;
- weak transitions;
- poor personalization;
- repetitive visuals;
- technically correct but emotionally dead presentation;
- anything that still feels like a 7–8.

A QA pass never overrides an Oscar finding.

---

# 30 — HUMAN APPROVAL BOUNDARIES

Human approval is required before changing:

- locked copy;
- stage names;
- brand colors;
- final CTA language;
- approved Naya assets;
- major experience architecture;
- scoring semantics;
- conversion promise.

AI should not stop for trivial implementation details that the contract resolves.

---

# 31 — MANDATORY PRE-MUTATION CHECK

Before changing product code, the AI must produce an internal execution brief containing:

TARGET UNIT
TARGET OWNER
CURRENT STATE
TARGET STATE
ALL REQUIRED EDITS IN THE UNIT
LOCKED DECISIONS
DATA INPUTS
DEPENDENCIES
VALIDATION PLAN
PRESERVATION PLAN
EXPECTED SOURCE DELTA.

If any of these are unknown, resolve the unknown before mutation.

---

# 32 — MANDATORY POST-MUTATION CHECK

Immediately after mutation:

1. source changed as intended;
2. no unrelated source changed;
3. target language validates;
4. data authority remains intact;
5. renderer ownership remains singular;
6. preserved functionality remains present;
7. expected visual object exists;
8. expected interaction exists;
9. responsive invariants still hold;
10. accessibility invariants still hold.

Only then proceed to build and section QA.

---

# 33 — OPTICAL QUALITY CONTRACT

Optical correctness beats mathematical correctness.

The AI must inspect rendered appearance for:

- optical centering;
- perceived weight;
- glow spill;
- text/border balance;
- icon alignment;
- perceived button depth;
- Orb silhouette;
- mini-Orb spacing;
- mobile crowding.

CSS numbers alone do not prove visual correctness.

---

# 34 — DENSITY CONTRACT

Every unit declares:

PRIMARY CONTENT
SECONDARY CONTENT
OPTIONAL CONTENT.

Primary content must be immediately understandable.
Secondary content supports the primary message.
Optional content must earn its place.

If optional content can be removed without harming understanding, remove it.

---

# 35 — MOTION CONTRACT

Every motion effect must communicate exactly one of:

REVEAL
RELATIONSHIP
ACTIVITY
FEEDBACK
TRANSITION.

Maximum simultaneous attention-driving animations in a local viewport: 3.

Orbital Bead may remain continuously active because it is identity motion.

Animation must never compete with reading.

---

# 36 — PERFORMANCE CONTRACT

Premium does not mean slow.

Avoid unnecessary DOM duplication, repeated large SVG creation, excessive blur, unoptimized images, needless render loops, and dozens of independently animated objects when one composited layer can communicate the same idea.

Prefer transforms, opacity, composited animation, SVG where appropriate, lazy loading below the fold, and asset reuse.

---

# 37 — FAILURE OWNERSHIP

Every failure belongs to exactly one primary owner:

PRODUCT
BUILD
VALIDATOR
RUNTIME
DESIGN
RELEASE
DATA
COPY
OWNERSHIP.

Repair the actual owner.

Do not mutate product to satisfy a stale validator.
Do not weaken a valid product requirement to obtain PASS.

---

# 38 — BETTER-IDEA PROTOCOL

AI may discover a better alternative.

AI may not silently replace a locked decision.

Record:

PROBLEM
→ ALTERNATIVE
→ BENEFIT
→ RISK
→ RECOMMENDATION.

Locked decisions require human approval.

Uncontrolled design drift is not optimization.

---

# 39 — CONTEXT / MEMORY CONTRACT

Before every material edit, read current project memory and the current active design directive.

Do not rely on conversation memory for locked decisions when the authoritative document exists.

Every material discovery that could prevent recurrence must be recorded as Smart Note.

The project memory is the externalized long-term context.

Do not assume “I remember this” is sufficient evidence.

---

# 40 — FINAL ANTI-RAIL-DRIFT TEST

Before implementation, ask:

Could two elite AIs read this and build materially different Hero Orbs?
Could they choose different button materials?
Could they use different copy?
Could they change different owners?
Could they render the mini-Orbs differently?
Could they produce a flat report?
Could they make the CTA more salesy?
Could they add unnecessary content?
Could they pass automated QA and still produce a 7?

If YES to any critical question:
that area remains insufficiently defined.

---

# 41 — V4 VERDICT

V3 established strong visual detail.

V4 adds the operational controls needed to make that detail survive real AI execution:

- source-of-truth precedence;
- pre-mutation execution brief;
- post-mutation verification;
- context/memory discipline;
- owner enforcement;
- scope enforcement;
- optical-quality inspection;
- anti-flatness rules;
- copy authority boundaries;
- human approval boundaries;
- automated-vs-human QA separation;
- mutation checkpointing.

V4 target:

MAXIMUM USEFUL PRECISION
+
MINIMUM INTERPRETATION DRIFT
+
FAST LOCAL EDITABILITY
+
VISIBLE HUMAN QUALITY
+
AUTHORITATIVE MEMORY
+
REPEATABLE EXECUTION.

STATUS:
PROPOSED — HUMAN APPROVAL REQUIRED BEFORE ACTIVATION.

FINAL GATE:

READY FOR HUMAN APPROVAL
or
MATERIAL REVISIONS STILL REQUIRED.
