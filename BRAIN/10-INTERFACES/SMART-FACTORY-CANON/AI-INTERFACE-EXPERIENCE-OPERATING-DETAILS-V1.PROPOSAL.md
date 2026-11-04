# Naya Smart-App Factory — Interface Experience Operating Details V1

**Status:** Additive review proposal for PR #3146 · not separately ratified · not a new renderer, design system, schema, gate, component library, or source of truth.  
**Purpose:** Give every Naya a precise, repeatable way to turn the existing RECIPE + PARTS + SHELL + DATA + GATE assembly language into exceptional screen-by-screen user experiences.

> **The Factory does not manufacture pages. It assembles a person's useful world from approved parts, real intelligence, and verified capabilities.**

This document extends the existing proposal in **AI-RECIPE-ASSEMBLY-LANGUAGE-V1.PROPOSAL.md**. It inherits the ratified Naya Design Contract, the ratified Anatomy of Naya Design, the Naya Design Intelligence Standard, current Project Intelligence, and the existing Smart Factory. It creates no parallel recipe vocabulary, JSON schema, component registry, scorecard, or dispatch path.

## 1. The one assembly language

Every Naya uses the same production sentence:

**RECIPE + PARTS + SHELL + DATA + GATE → AUTHORIZED HUMAN OUTCOME**

| Element | What the Naya must know before building |
|---|---|
| **RECIPE** | The authoritative PI child, exact source/version, audience, user job, human outcome, screen sequence, owner, non-goals, dependencies, and acceptance. |
| **PARTS** | Exact current canonical piece IDs, lifecycle status, importable source, compatibility, slots, dependencies, states, and actual specimen. A canonical/present piece is eligible to evaluate, not automatically qualified for production. |
| **SHELL** | The one approved NayaNET app shell, Smart Bars, identity, navigation, global context, fixed chrome, safe-area behavior, and responsive grammar. Reuse it; do not create a competing shell. |
| **DATA** | Canonical source, lineage, identity scope, authorization, privacy class, units, date range, freshness, derivation, read/write behavior, empty/error/denied behavior, and persistence receipt. |
| **GATE** | Structural RECIPE preflight, exact PARTS resolution, rendered screen review, responsive/accessibility checks, real-action tests, security/negative tests, different-seat verification, exact source/deployed SHA, and PI/continuity evidence. |

### 1.1 Shared words

Use the established terms in the existing RECIPE and SCENE contract:

- **WORLD** — the person's or group's context, identity, goals, relationships, data, and permissions.
- **APP** — a purposeful workspace in NayaNET, not a collection of unrelated routes.
- **ROOM** — a meaningful domain of work or information within an app.
- **SCENE** — the screen-level user job and visual/interaction composition.
- **HERO** — the one focal object or finding that should win first attention.
- **CONTEXT** — the few facts needed to understand the hero or act on it.
- **PRIMARY ACTION** — the main permitted verb for the current scene.
- **SECONDARY ACTION** — one subordinate action when needed; it must not compete with the primary.
- **AMBIENT** — quiet provenance, freshness, identity, or status that supports trust without competing for attention.
- **PART** — an exact registry-backed reusable interface element.
- **SHELL** — approved shared chrome and navigation.
- **DATASET** — the canonical data/read model or authorized external source.
- **ACTION** — a named capability with actor, permission scope, effect, and observable result.
- **STATE** — what is actually true now, represented honestly.
- **PROOF** — reproducible evidence of a claim.
- **RECEIPT** — the durable record of an attributable action, build, test, approval, or deployment.

Do not create synonyms for these fields inside different Nayas' prompts. A Naya may explain them to humans in natural language, but machine-facing artifacts must resolve to the same recipe vocabulary.

### 1.2 The SCENE contract

The existing SCENE card is the required planning unit:

**SCENE(id, human_job, hero, context[0..3], primary_action, optional_secondary, ambient_provenance, part_ids, data_refs, states, viewport_and_safe_area, proof, next)**

Before implementation, the Naya must be able to answer:

1. What is this screen for?
2. What is the one thing that matters most?
3. Which facts make that thing understandable?
4. What is the primary permitted action?
5. What will the user see after acting?
6. Which PARTS, DATASETS, and ACTIONS actually support the scene?
7. What happens when information is loading, empty, stale, offline, denied, or failed?
8. How does the scene compose in the real usable viewport?
9. What evidence proves the screen works?

CONTEXT [0..3] is a hierarchy constraint, not a content quota. A screen may use fewer context facts. It may not invent extra facts just to fill space.

## 2. The Naya experience promise

Every NayaNET app should feel like one member of a premium family, while being shaped around its own job. Consistency comes from the shared design anatomy, shell, parts, behavior, and truth standards—not from forcing every app into the same dashboard.

A successful screen lets a person quickly understand:
- where they are;
- why this matters now;
- what they can do;
- what happens next;
- what is real, current, and permitted.

The target is **maximum responsible human value with minimum necessary cognitive burden**. More machine capability should make the human's experience simpler, not add more cards, panels, settings, labels, or decisions.

## 3. Visual grammar: inherit the canon, do not invent a second one

The visual canon is the current ratified Naya Design Contract plus the ratified Anatomy of Naya Design and its human/AI/machine companions. This appendix does not replace or silently reinterpret those authorities.

### 3.1 Canonical physical material

The ratified Anatomy establishes the chosen Naya material language:

- **Button — physical jewel glass:** layered obsidian body, elevation shadow, multi-line rim, jewel icon chip, readable label, optional live slot, and truthful interaction state. Buttons rise; a press sinks.
- **Board — obsidian bento:** layered ground plane, related rim light, purposeful header, one meaningful subject in the body, category spine, and optional action zone. Boards and their rows should look like members of one physical family.
- **Icon — geometric glyph in a jewel chip:** consistent optical geometry, coherent stroke family, unique meaning, one semantic color job. An icon should remain identifiable when its label is absent.
- **Input — recessed composer/well:** inputs sink into the page; they are not styled like actions. The canonical composer is imported, not re-created per page. Its real capabilities (dictation, scheduling, attachment) must be present and work before they are shown as actions.
- **Stats — Smart Stats family:** Pulse Strip, Trend Panel, Mix Donut, Journey Funnel, Faces Board, Insight Feed, Heat & Streaks, and Health Gauge, used only where their data form and user question warrant them.
- **Shell — existing NayaNET chrome:** one approved bar/navigation implementation, one search mount where the service is integrated, and one shared app identity/navigation grammar. The Factory does not grow a second shell.

The Anatomy defines exact piece anatomy, state logic, and selected concepts. Use those definitions and actual approved source specimens; do not produce a local approximation.

### 3.2 Visual decisions must be source-backed

Nayas must not invent or hardcode a replacement:
- palette or spectrum sequence;
- idle/hover/pressed/selected behavior;
- body or detail type-size floor;
- elevation recipe, rim thickness, shadow/blur token, or motion timing;
- button/board/input geometry;
- icon family or chart color semantics.

Where a ratified source specifies an exact value, use it. Where the source says MEASURE-FROM-APPROVED, inspect the approved specimen/kit and record the measured value in the authorized machine token source. Do not estimate by eye and silently promote the estimate.

### 3.3 Explicit canonical reconciliation required

The currently retrieved ratified sources have differences that must not be silently resolved by a builder:

| Subject | Naya Design Contract v1.2 | Anatomy of Naya Design (ratified 2026-10-31) | Operating rule until resolved |
|---|---|---|---|
| Spectrum | Seven-token walk: purple → blue → green → gold → orange → red → magenta | Five-position walk: magenta → purple → blue → green → gold | Preserve current shipped/reference surfaces. Mark sequence automation as BLOCKED on the disputed scope. Route one explicit reconciliation to the canonical design owner/Human Director; update human, AI, machine contract, and tests together. |
| Type floor | Body 17–18px target, 16px floor | Geometry/type rule states ≥14px | Keep the explicit body 16px floor for body copy. Do not infer that the newer 14px statement overrides the body-copy rule. Resolve any detail/caption exceptions in the canonical source. |
| Rest/selected light | Visible white border/glow at rest; selected uses subtle white indicator and no permanent color glow | White light at rest; glow/halo exists only in response to touch/hover/focus; selected is described as a white-hot rim | Do not implement a global change to rest/selected styling until exact visual behavior is reconciled against approved shipping specimens. |
| Local color meaning | Spectrum roles and semantic exceptions are defined in v1.2 | One color job per element, stable meaning, magenta leads | Preserve semantic mappings already ratified for existing surfaces; do not reassign color meanings app-by-app. |

This is a governance reconciliation, not an invitation for each Naya to choose the version she prefers. The existing recipe proposal already flags these conflicts. The preflight must not pretend that unresolved visual-law questions have been machine-settled.

### 3.4 Living intelligence, honestly

“Alive” means the interface responds to real user input, current data, or real events. It does not mean perpetual movement.

- Presence indicators breathe only while the corresponding real state is live.
- Counters animate only when an actual value arrives or changes.
- Progress moves only when real progress is observed.
- A chart draws in from real data; it never invents activity to look dynamic.
- A loading skeleton reflects the actual shape of the content expected.
- A LIVE label, animated tick, or pulse requires a real underlying source/update contract.
- Reduced-motion users receive the same meaning and control without unnecessary animation.
- Unwired elements show an honest frame or are omitted; they do not pretend to be active controls.

Every numeric data surface must express **magnitude + shape + direction + a human sentence**. Include units, timeframe, scope, provenance, and a meaningful drilldown where relevant. The visual is not a substitute for the explanation or the data.

## 4. Screen-by-screen composition

### 4.1 One complete thought, not an artificial one-viewport page

The first viewport must orient the person, present the SCENE hero, give enough context to understand it, and expose its main useful action where one exists. It is measured **after the actual fixed/sticky shell chrome**, not from an imaginary full browser height.

A screen is not required to fit every report, list, long form, or complex workflow into one fixed height. Natural vertical scrolling is correct when the job needs more content. The requirements are:
- no clipping of essential information or controls;
- no primary action hidden under fixed bottom navigation or browser/safe-area chrome;
- no accidental nested-scroll traps;
- no shrinking type or controls merely to force a viewport screenshot;
- no automatic horizontal page scrolling;
- no loss of keyboard focus or validation messages behind sticky elements;
- the next scroll region should be a coherent next group, not a continuation of an overloaded card.

A two-dimensional data region may scroll explicitly when that is intrinsic to the task and remains keyboard/touch accessible. Page content itself should reflow.

### 4.2 First-glance anatomy

Use four composition layers as a design guide:

1. **HERO** — one dominant object, finding, task, person, visualization, or creation surface.
2. **CONTEXT** — up to three short facts that make the hero understandable and help the user act.
3. **ACTION** — one primary verb and, only when useful, one subordinate action.
4. **AMBIENT** — restrained source, freshness, scope, identity, or quiet status.

These are not a command to put four boxes on every screen. Read-only scenes may have no CTA. A workflow may need additional actions later in context. The first view still has an unmistakable hierarchy.

### 4.3 Screen map

The RECIPE owner maps the whole user journey before assigning screens:

**ENTRY → ORIENT → PRIMARY JOB → DETAIL / SUPPORT → DECISION / ACTION → RESULT → CONTINUATION**

For every SCENE identify route and entry condition; previous/next scene and back behavior; user job and first-glance purpose; hero and source of its content; data context and permission; main and optional secondary action; success/failure result; preserved state across navigation; scroll behavior; and completion evidence.

No dead-end screens. No orphaned action. No mystery navigation.

### 4.4 Screen families and appropriate composition

| Screen job | Preferred composition | User-experience risks to reject |
|---|---|---|
| **Home / World** | One current-world focal point; relevant next action; concise activity/context; meaningful doors into rooms | Generic marketing hero, many equally loud cards, fake activity, empty black void |
| **Today / Command** | Waiting-first ranked items, one main priority, why it matters, evidence, next action | Bare counts, unexplained rank, duplicative lists, false urgency |
| **Object detail** | Identity/title, current state, important facts, chronological story, authorized actions, evidence/history | Tab explosion, unrelated metrics, hidden owner/permission state |
| **Create / Edit** | Task-first composer/form, one decision at a time when appropriate, clear progress, save truth, recovery | Multi-field wall on mobile, ambiguous Save state, losing draft |
| **Search / Discovery** | One obvious search entry, scope/filter, explainable result list, clear preview/open action | One search per room, private-data leakage, unexplainable matching, result treated as consent |
| **Mail / Message** | Person and thread identity, conversation, waiting state, composer, send confirmation | Fake send success, unclear recipients, hidden scope, duplicate send |
| **Lists / Workflow** | List identity, progress/status, items, owner and next action, safe batch tools | Generic kanban where a list is better, unsafe bulk delete, hidden filter state |
| **Reports / Analytics** | Question/time window, human finding, chart matched to data, comparison, source/method, drilldown | Chart without a sentence, meaningless donut, bare numbers, hidden date range |
| **Connections / Space** | People/space identity, declared context, roles, content and permission-aware actions | Suggestions appearing as established relationships; public/private confusion |
| **Settings / Identity** | Grouped preferences with current state, consequence, reset/undo where possible | Unlabeled switches, settings duplicated across apps, unclear privacy effects |

A family is a reusable mental model, not a fixed template. Choose layout for the job and data.

## 5. Responsive and accessible composition

The required reference viewport matrix already defined by the RECIPE proposal is:
- 320 × 700 CSS px;
- 390 × 844;
- 768 × 1024;
- 1440 × 900.

Also test landscape where relevant, touch, mouse, keyboard, screen reader, 200% and 400% zoom, safe-area insets, and the software keyboard. A device matrix is a minimum repeatable baseline; actual breakpoints must follow content fit.

### 5.1 Responsive rules

- Design from a logical single-column flow; add columns only when both remain readable.
- Reorder content at narrow widths by user priority, not by desktop source order.
- Keep primary actions reachable. If fixed bottom chrome competes for height, use the approved compact/menu behavior rather than hiding the action.
- No important control requires hover. Touch, keyboard, and assistive technology must have equivalent paths.
- Text wraps without clipping; cards expand vertically; charts retain readable labels and provide text/data alternatives.
- Wide tables use a deliberate, named two-dimensional region only where comparison requires it.
- Forms remain usable while the on-screen keyboard is open; labels, errors, and actions stay connected and visible.
- Sticky chrome never covers focus, anchors, form errors, or submit actions.
- Respect reduced motion and zoom/reflow.

### 5.2 Accessibility baseline

Target WCAG 2.2 AA, and retain Naya's stricter house target of at least 44 × 44 CSS px for important touch controls. Do not describe that house target as the WCAG minimum.

Every SCENE requires semantic landmarks/headings/controls/labels/names; logical keyboard path and visible non-obscured focus; accessible validation/error messages and async announcements; contrast checked in real states; no color-only or animation-only meaning; reduced-motion equivalent; screen-reader equivalent for charts and complex data; zoom/reflow test; and touch target size/spacing verified after the real chrome is included.

A semantic JSON pass is not accessibility proof. Release proof needs the actual rendered interface and keyboard/assistive-tech checks.

## 6. The component/part operating method

**Compose, do not redraw.** The exact current PARTS rules from the RECIPE proposal and canonical piece index govern eligibility.

For every component:
1. resolve ID in CANONICAL-PIECE-INDEX.json;
2. resolve an importable working source in pieces.json and the actual component file;
3. inspect the specimen, variant, states, dependencies, CSS/JS, and compatibility;
4. verify that the component's exact purpose fits this SCENE;
5. import the approved part unchanged where possible;
6. adapt only documented content slots or variants;
7. verify the component still matches its canonical behavior and family.

Never infer that a historical reference is selectable. Never infer that canonical means visually reviewed or production-qualified. Never erase historical references to retired or superseded pieces. The preflight's job is to refuse unsafe new selection without destroying history.

### 6.1 Core anatomy checklist

| Part family | Essential behavior to inspect |
|---|---|
| **Buttons** | Obsidian physical object; layered rim and shadow; clear verb; jewel meaning; rest/hover/focus/pressed/selected/disabled; actual action; touch/keyboard/accessibility. Signature is an obsidian body, not a white body. |
| **Boards** | One meaningful subject; sibling rim/ground; purposeful header; category identity; readable body; actions as real buttons; responsive ratio/reflow. |
| **Inputs/composer** | Recessed well; label/help; focus ignition; typing/selection/error/success; dictation or attachment only if truly wired; unsaved draft recovery. |
| **Icons** | Unique semantic glyph; stable 24-unit construction; coherent stroke family; jewel chip; accessible label for icon-only use. Never emoji as system icon. |
| **Tabs/navigation** | Approved Smart Tabs and Smart Bars; selected/focus/scroll state; active identity and reachable back path; no duplicated navigation system. |
| **Charts/data** | Exact metric definition; period and unit; source/freshness; matching chart form; real drilldown; human sentence; honest empty frame; meaningful event-driven motion. |
| **Sheets/dialogs/toasts** | Consequence-proportional choice; focus management; escape behavior; only one decision per sheet; errors persist until understood; no silent success. |
| **Progress/loading/empty** | Actual progress event; real content skeleton; honest empty state explaining what belongs here and the one real action that can create it. |

## 7. Function and data are part of the design

A control is not finished because it is clickable. Define its causal contract:

**CONTROL → USER INTENT → ACTOR → SCOPE → AUTHORITY → PRECONDITIONS → CAPABILITY → EFFECT → OBSERVABLE RESULT → RECEIPT**

Every ACTION in DATA must name a real service/capability, permission reference, and outcome receipt. The screen must be honest about whether an action is wired. An unknown service is not a UI action.

### 7.1 Data contract for every visible metric/object

The RECIPE DATA datasets must make explicit:
- source and lineage;
- owner identity and access scope;
- permission reference;
- meaning, unit, time window and calculation;
- freshness and refresh policy;
- fields visible to this audience;
- loading, empty, stale, offline, denied, and error states;
- write result and receipt when the user mutates data.

A zero, null, missing, unknown, stale, cached, demo, predicted, and live value are different. Never coerce unknown to zero or demo to live. Never expose a private object just because a recommendation engine can score it.

### 7.2 Choosing a visual representation

Choose based on the question and the structure of data:
- **Single value:** metric with unit, baseline, direction, sentence, source.
- **Change over time:** line/area with date range, clear axis, no misleading scale.
- **Comparison:** aligned bars or a sortable table.
- **Composition:** donut/part-to-whole only when values form a meaningful whole.
- **Flow/sequence:** funnel, journey, or timeline.
- **Work status:** ranked list or structured board.
- **Relationships:** constellation/network only when actual relationships exist and are navigable.

Never use a gauge simply because it looks dramatic. A visualization is not decorative wallpaper. It must help the human understand, compare, discover, or act.

## 8. Team Naya orchestration

Assign responsibilities according to real work and dependencies. Do not spawn agents for activity or fragment the same file across multiple writers.

| Responsibility | Owns | Required handoff |
|---|---|---|
| **Integrator / conductor** | Current PI, current source, ownership, dependencies, branch convergence, no duplicate work | Ordered work packages and one next action |
| **Intent / product architect** | Human outcome, object model, journeys, room and SCENE map | Complete RECIPE |
| **Experience / art director** | Screen hierarchy, Naya composition, actual visual specimen, visual quality comparison | Screen design notes and references |
| **Parts librarian** | Exact piece lifecycle, source, dependencies, specimen, compatibility | PARTS manifest |
| **Data / action engineer** | Data ownership, scopes, permissions, service binding, receipts, idempotency | DATASETS and ACTIONS contract |
| **Builder** | Bounded implementation within the existing Factory source seam | Exact source commit and test results |
| **Device/accessibility reviewer** | Real rendered phone/tablet/desktop, keyboard, screen reader, touch, zoom, reduced motion | Viewport and accessibility receipts |
| **Independent verifier** | Reproduces primary journey, privacy denial, persisted result, deployed bytes, and visual outcome | Independent gate verdict |
| **Continuity steward** | PI/board/learning updates, truth labels, reusable lesson, handoff | Durable successor context |

The builder may not be its own independent verifier. A reviewer must inspect the exact frozen source/deployed SHA, not a moving branch or verbal claim. Seats may be combined for bounded tasks only when independent-review separation is preserved.

### 8.1 Parallel work without collision

Parallelize independent deliverables, not the same mutable artifact. One owner per file; one integrator for cross-file decisions. Every task states source SHA, file ownership, input/output, acceptance, and proof method. Before an agent begins, inspect current PRs, issues, branch work, and active claims. Extend an existing owner lane instead of creating duplicate work.

### 8.2 Fast without cutting corners

Speed comes from stable grammar, PI-backed briefs, reusable parts, approved shell, generated layouts, and executable preflight—not from skipping analysis or proof.

Measure separately:
- time from complete RECIPE to first render;
- time to first useful and functioning action;
- time to independently qualified release.

The proposed under-ten-minute build target applies only to suitable templated cases and must be measured across repeated builds. The three-minute target is a research goal, not an unconditional promise. A fast invalid screen is a failed Factory run.

## 9. The existing GATE: what must be proven

Use the proposal's existing eight dimensions: **visual, function, intelligence, honesty, performance, reliability, accessibility, craft**. This appendix adds checks as review prompts; it does not introduce a new scorecard or new global weights.

| Dimension | Questions the verifier must answer |
|---|---|
| **Visual** | Does the screen use current approved Naya anatomy? Is there a clear first-glance hero? Is hierarchy coherent at all required widths? |
| **Function** | Do all visible controls perform their declared action? Does the primary journey complete and recover from failure? |
| **Intelligence** | Are summaries/recommendations relevant, explainable, source-backed, and useful for this person/context? |
| **Honesty** | Are zero/unknown/stale/demo/live correctly distinguished? Do state labels and animations reflect real state? |
| **Performance** | Does the first useful action arrive quickly? Are animation, payloads, layout shifts, and rendering work restrained? |
| **Reliability** | Are errors, retry, duplicate submission, persistence, and recovery tested? |
| **Accessibility** | Are keyboard, touch, screen-reader, contrast, focus, reduced motion, zoom/reflow and target sizes verified? |
| **Craft** | Are the parts exact and coherent? Does the app feel like one premium Naya family rather than stitched templates? |

### 9.1 Hard stops

Regardless of numerical score:
- any unauthorized read/write/share;
- any false live/save/send/approve/persisted claim;
- any invented personal content, activity, score, or metric;
- any dead or misleading primary control;
- any inaccessible primary task;
- any obscured/clipped primary action at required viewports;
- any retired/superseded/missing part selected for a new build;
- any unresolved critical source, authority, or privacy scope;
- any mismatch between reviewed source SHA and deployed SHA;
- no independent verifier for a release claim.

A draft RECIPE may contain explicit unknowns, visibly recorded as OPEN. A release candidate may not claim completion while these conditions remain unresolved. The existing recipe_preflight_v1.py remains the structural check; actual rendering, auth, action, usability, security, and production evidence remain separate.

## 10. The build loop and handoff

1. **RESTORE** — current boot, protocol, constitution, PI, source branch, live owner and active work.
2. **UNDERSTAND** — human job, beneficiary, baseline, intended outcome, non-goals.
3. **INVENTORY** — actual current routes, shell, data, capabilities, parts, tests; preserve what works.
4. **RECIPE** — create one accurate app recipe and complete SCENE map.
5. **RESOLVE PARTS** — exact IDs, current lifecycle, working source, compatibility.
6. **DESIGN** — produce first-viewport layouts, states, responsive composition, and real data visualization plan.
7. **BUILD** — smallest complete vertical journey through real capability and canonical data.
8. **VERIFY** — exact source, actual rendered states, required viewport matrix, positive and negative paths.
9. **INDEPENDENTLY CHALLENGE** — different seat reproduces the primary task, owner-scope DENY, persistence, recovery, and visual/accessibility outcome.
10. **PROMOTE** — only through existing authority/release gates.
11. **OBSERVE** — real production usage, data, permissions, and device conditions.
12. **LEARN** — preserve candidate lessons with evidence, applicability, contradictions, owner, and enforcement path through existing NayaPOWER learning.

### 10.1 Required evidence handoff

The responsible lane leaves:
- current PI reference and exact source SHA;
- RECIPE and SCENE list;
- PARTS source/status manifest;
- DATASET and ACTION contracts with authority;
- preview URL or rendered screenshots at required viewports;
- test commands and raw results;
- accessibility/performance evidence;
- independent reviewer and verdict;
- known gaps/blocked fields and owner;
- deployment receipt and exact deployed SHA, where deployed;
- one next authorized action.

A proposal, recipe, generated file, local preview, passing preflight, and production-proven app are different outcomes. Report the exact one earned.

## 11. Adoption and integration sequence

This is a proposal that complements PR #3146. It does not authorize a parallel design system or automatic dispatch.

1. Existing Factory owners review this appendix against the already-proposed recipe language and current anatomy.
2. Resolve visual-law contradictions at the canonical design source, with one approved human/AI/machine contract and synchronized tests. Do not implement a private interpretation in the builder.
3. Add only those machine fields that are necessary to the existing NAYA_APP_RECIPE_V1 contract; update the same schema, sample, preflight, and tests together. Do not add a second schema or validator.
4. Run the existing Smart Lists sample as a DRAFT and verify explicit OPEN warnings; confirm RELEASE_CANDIDATE is denied while service, privacy, or independent proof remain unknown.
5. Use the existing Dashboard/first-viewport repair lane as the first real screen proof, rather than building a parallel dashboard.
6. Generate one bounded second app from the same approved parts. Measure first render, first useful action, and independently verified release separately.
7. Only after compatibility and independent proof may the existing Factory owner wire any accepted checks into dispatch/CI.

**This proposal does not change the app, database, permissions, generator, queue, deployment, or production runtime.**

## 12. Human-readable law

**BUILD THE HUMAN'S WORLD. COMPOSE FROM THE BEST PARTS. KEEP THE EXPERIENCE SIMPLE. MAKE IT FEEL ALIVE ONLY WHEN REAL LIFE MOVES. PROVE EVERY IMPORTANT PROMISE. LEARN FROM WHAT ACTUALLY HELPED.**
