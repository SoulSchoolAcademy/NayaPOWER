# MAXESS AAA REFERENCE SPEC

Status: ACTIVE MASTER REFERENCE
Purpose: Define the exact product standard for the MAXESS Results experience and serve as the reference implementation for the AI Product Completion System.

## 1. Mission

MAXESS helps a person understand why they are struggling to get exceptional results from AI and gives them a personalized map from current capability to stronger capability.

Core transformation:
DATA → INSIGHT → UNDERSTANDING → RECOGNITION → FOCUS → ACTION → CAPABILITY

The experience is a Personal AI Mastery Report, not a dashboard, SaaS admin screen, template, or sales page.

## 2. Product promise

The visitor arrives frustrated by mediocre AI results and wants to know:
- Where am I now?
- Why am I getting these results?
- What am I already good at?
- What is my biggest opportunity?
- What should I do next?
- Where can Naya help me?

The report must answer those questions clearly, personally, and beautifully.

## 3. Definition of AAA / 10

AAA means every material layer is excellent enough to be proudly shown to a demanding human audience.

A 10 is not a feeling and is never granted merely because code passes. A requirement is COMPLETE only when:
1. it exists in the intended source;
2. it matches the project contract;
3. real data drives it where applicable;
4. its intended interaction works;
5. it survives regression checks;
6. it works at required responsive sizes;
7. it meets accessibility requirements;
8. it does not introduce unnecessary complexity;
9. human review finds no material defect.

AAA dimensions:
- purpose: the feature advances the North Star;
- clarity: a first-time user understands it without technical knowledge;
- personalization: the experience clearly belongs to this person;
- visual craft: hierarchy, typography, spacing, color, depth, geometry, and motion are deliberate;
- interaction craft: controls feel physical, clear, responsive, accessible, and reliable;
- data integrity: no invented production data;
- architecture: one clear owner per behavior and one authoritative result source;
- responsive quality: desktop, tablet, and mobile are intentional;
- accessibility: semantic structure, focus, labels, contrast, reduced motion, and touch targets are handled;
- performance: animation and DOM work are efficient and bounded;
- release reliability: no broken media, missing sections, or deployment-only surprises;
- print/PDF: the report remains professional outside the browser.

## 4. Visual language

Primary visual language:
- black / near-black foundations;
- white / near-white report surfaces;
- purple as the signature NayaNET/MAXESS energy;
- restrained gold only when it adds premium emphasis;
- organic geometry over repetitive rectangles;
- Orb/rings/radar/fingerprint/energy fields;
- depth through light, glow, scale, layering, and motion;
- generous editorial spacing;
- strong contrast;
- premium but readable typography.

Preferred rhythm:
DARK → LIGHT → DARK/PURPLE → LIGHT → DARK → PURPLE, with transitions serving cognition rather than decoration.

Avoid:
- monotonous card grids;
- generic SaaS cards;
- excessive borders;
- excessive shadows;
- noisy gradients;
- decorative elements with no semantic value;
- duplicate hero objects;
- duplicate CTAs;
- unexplained scores.

## 5. Information architecture

Default MAXESS narrative:
1. Naya arrival / Your AI Score
2. What your score means
3. Your AI Fingerprint
4. Personalized Report
5. Your Pattern
6. Your Strength
7. Your Biggest Lever
8. Your Next Move
9. 18 Naya Masters / Best-fit pathways
10. Naya / AI Playground / practice
11. Final personalized continuation CTA

Sections may be reordered only when evidence shows a materially stronger user journey.

## 6. Section contracts

### 6.1 Hero / Naya arrival
Purpose: create recognition, trust, curiosity, and a sense that Naya has looked at this person's actual result.
Required:
- Naya identity/profile image;
- personalized headline when identity exists;
- “This isn’t your judgment. It’s your map.” framing;
- exactly one primary LISTEN TO NAYA action;
- primary MAXESS score dominant in the signature Orb;
- mastery stage visible without competing with the score.

### 6.2 What your score means
Purpose: translate the number into plain-language meaning and eliminate score anxiety.
Required:
- stage interpretation;
- what the current level means;
- how the person should use the score;
- no judgmental framing;
- action bridge: Create → Score → Improve.

### 6.3 AI Fingerprint
Purpose: reveal the shape of the five dimensions as a system rather than five isolated numbers.
Required five dimensions:
- Direction
- Communication
- Evaluation
- Iteration
- Systems Thinking

Required:
- radar/fingerprint visual;
- five values from MAXESS_RESULT;
- clear labels;
- meaningful descriptions;
- visual relationship between axes;
- mobile-safe scaling.

### 6.4 Personalized Report
Purpose: provide the save-worthy written interpretation.
Required:
- overall result;
- mastery stage;
- strongest signal;
- biggest opportunity;
- plain-language interpretation;
- invitation to continue.

### 6.5 Pattern
Purpose: explain relationships among dimensions.
Required:
- relationship language, not only score repetition;
- strongest supporting relationship;
- opportunity relationship;
- clear “why this matters” explanation;
- Naya interpretation.

### 6.6 Strength
Purpose: create recognition and confidence.
Required:
- dynamic strongest capability;
- explanation of why it matters;
- three ways to compound it;
- connection to next move;
- positive framing.

### 6.7 Biggest Lever
Purpose: focus attention on the highest-value improvement.
Required:
- dynamic lowest/highest-leverage dimension as supported by the data model;
- explicit “opportunity, not verdict” framing;
- one real task;
- one deliberate improvement;
- repeat loop.

### 6.8 Next Move
Purpose: convert insight into action.
Required three steps:
1. protect strength;
2. build lever;
3. create → score → improve.
Every action should connect back to the user's result.

### 6.9 18 Naya Masters
Purpose: provide useful continuation pathways.
Required:
- preserve all validated pathways;
- dynamic relevance where supported by data;
- Best Match / Strong Match treatment;
- useful descriptions;
- usable CTAs;
- relationship to Strength / Lever / Next Move.

### 6.10 Playground / practice
Purpose: move from understanding to doing.
Required:
- Understand → Decide → Practice framing;
- preserve working video/audio/controls;
- reliable lower-page rendering;
- mobile usability.

### 6.11 Final CTA
Purpose: make the next step obvious and personally meaningful.
Required:
- personalized bridge from result to continuation;
- Naya voice;
- clear CTA;
- no generic hard-sell language.

## 7. Components

Every major component must have:
- purpose;
- visual specification;
- data inputs;
- states;
- interactions;
- accessibility;
- responsive behavior;
- acceptance criteria.

Core components:
- MAXESS Orb;
- Naya profile/panel;
- LISTEN TO NAYA control;
- fingerprint/radar;
- dimension orb/control;
- report surface;
- insight card/surface;
- action step;
- Master pathway item;
- Playground host;
- final CTA.

## 8. Data contract

Authoritative result source:
window.MAXESS_RESULT

Production rules:
- never invent a user's score;
- never create a competing production scoring engine in Results;
- derive all personalized output from authoritative data;
- fail safely when data is missing;
- development fixtures must never masquerade as production data.

## 9. Interaction contract

Every interactive element must define:
- default;
- hover;
- active;
- focus-visible;
- disabled/error state where relevant;
- touch behavior;
- keyboard behavior;
- reduced-motion behavior.

Primary LISTEN TO NAYA must have one visible owner.

## 10. Responsive contract

Verify:
- widescreen;
- desktop;
- tablet;
- mobile.

Never rely only on CSS existence. Inspect actual behavior.

## 11. Accessibility contract

Required:
- semantic headings;
- useful labels;
- focus visibility;
- contrast;
- no color-only meaning;
- reduced motion;
- touch targets;
- accessible interactive controls.

## 12. Performance contract

Required:
- bounded animation;
- no uncontrolled MutationObserver loops;
- no repeated initialization;
- no duplicate event listeners;
- no redundant renderers;
- no unnecessary libraries;
- graceful degradation.

## 13. Preservation contract

Before any edit:
- identify what already works;
- preserve useful behavior;
- preserve working media and Groove compatibility;
- preserve real data handoff;
- preserve validated assets.

Never replace a complete working artifact with a miniature test renderer.

## 14. Change contract

Every requested change becomes a change item with:
- ID;
- requirement;
- section/component;
- reason;
- target state;
- acceptance criteria;
- evidence;
- status.

Status values:
DRAFT / READY / IN PROGRESS / VERIFIED / FROZEN / RELEASED

## 15. Smart Notes

During execution Naya must update durable project notes when any material decision occurs:
- design decision;
- architecture decision;
- rejected alternative;
- discovered dependency;
- bug root cause;
- regression safeguard;
- release decision.

Conversation is temporary. Smart Notes are durable.

## 16. Completion gate

Do not declare a section complete until:
- contract satisfied;
- source contains the implementation;
- functionality works;
- regression passes;
- responsive behavior passes;
- accessibility passes;
- no material visual defect remains;
- human review has no material objection.

## 17. Release gate

Engineering complete:
all technical checks pass.

Ready for Groove test:
artifact rebuilt and verified, awaiting human visual review.

Live verified:
Groove deployment confirmed in the real public environment.

These states must never be conflated.

## 18. Oscar challenge

Before final release, actively ask:
- What is still generic?
- What is still confusing?
- What feels unfinished?
- What is merely decorative?
- What did we break?
- What is not actually personalized?
- What would a skeptical expert reject?
- Would a recipient be proud to receive this?
- Would we confidently show this to thousands or millions?

If a material answer is yes, continue work.
