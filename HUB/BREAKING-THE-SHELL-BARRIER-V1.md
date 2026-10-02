# 🔱 Breaking the Shell Barrier — Interface Completion Doctrine V1

**Status:** HUMAN-DIRECTOR-DIRECTED · PROPOSED CANONICAL OPERATING DOCTRINE  
**Authority:** Shawn Vibert, Human Director  
**Applies to:** NayaNET Hub and any future NayaPOWER multi-room/multi-page product work  
**Companion intelligence:** `SN-019 — Complete the App Doctrine — Finish the House, Not the Shell`  
**Coordination:** Issue #554  
**Implementation owner:** Issue #1270

## 0. The problem

AI interface work repeatedly stalls at a recognizable failure state:

- attractive shell;
- working router;
- some good buttons;
- one impressive page;
- many empty/thin rooms;
- incomplete runtime behavior;
- inconsistent state;
- regressions when another room is touched;
- visual polish without whole-product usefulness.

The failure is not solved by saying **"no more shells."**

The build machinery itself must make shell-only completion impossible to confuse with a finished application.

## 1. Why AI builders tend to stop at shells

### 1.1 Builders often work without enough visual observation

Source code can look coherent while the rendered product is visibly wrong.

Therefore:

> **BUILD → RENDER → LOOK → CLICK → MEASURE → FIX → RE-VERIFY**

must be a required loop, not an optional final QA pass.

### 1.2 Training/examples bias toward fragments

Single-page demos, components, snippets and isolated screens are easier to generate than a complete application whose rooms share state, navigation, data ownership and interaction law.

The system must therefore represent **whole-app coherence explicitly** rather than expect a builder to keep it all in working memory.

### 1.3 Multi-room coherence is a contract problem

Every room must agree on:

- design tokens;
- shell geometry;
- type scale;
- component physics;
- canonical object IDs;
- state vocabulary;
- routing;
- persistence;
- runtime data ownership;
- authority/privacy rules;
- error behavior;
- responsive behavior;
- cross-room handoffs.

Those agreements must live in machine-readable contracts and tests.

### 1.4 Shells optimize for visible progress

Chrome appears quickly. Deep behavior is less visible.

Therefore activity metrics and "route renders" are not completion evidence.

Completion is measured by **usable end-to-end journeys and evidence**, not by number of screens or commits.

### 1.5 Long product work requires accumulated judgment

A human designer/engineer improves an app through hundreds or thousands of small decisions while continuously seeing the whole product.

An AI system needs the same compounding loop:

> **STATE → TASK → BUILD → OBSERVE → SCORE → REPAIR → CHECKPOINT → NEXT TASK**

The important capability is not raw speed. It is **persistent judgment without regression**.

## 2. The high-rise rule

Think of the application as a 24-floor building.

A builder may not:
- circle the fifth floor forever;
- rebuild floors 1–3 every time floor 6 is attempted;
- demolish a completed floor accidentally;
- call floor 5 "the building";
- skip structural systems shared by all floors.

Every accepted floor becomes a **non-regression baseline**.

Progress must be monotonic in completed capability unless evidence proves an intentional replacement is superior.

## 3. One shell, many rooms, one product

The shell is infrastructure.

The rooms are the product experiences.

The governed runtime is the shared substrate.

A room must inherit the shell/design/runtime contracts rather than invent another mini-app.

**One shell does not mean one layout.**

Each room must have its own signature instrument and user job while preserving common laws.

## 4. Contracts before pages

Before substantial room implementation, establish:

1. canonical route/room registry;
2. design tokens;
3. component/state contracts;
4. canonical object identity rules;
5. runtime/data owner for each surface;
6. authority/privacy boundaries;
7. cross-room handoff contracts;
8. acceptance journeys;
9. responsive/accessibility requirements;
10. proof expectations.

The builder should not "remember" these informally.

The system should be able to test them.

## 5. The Interface Completion Engine

For each declared room/surface, maintain machine-visible state:

```
NOT_STARTED
→ SPEC_READY
→ DESIGN_READY
→ IMPLEMENTED
→ TESTED
→ INTEGRATED
→ INDEPENDENTLY_VERIFIED
→ PRODUCTION_PROVEN
```

A room does not skip states because it looks finished.

### Minimum room completion dimensions

Every applicable room must close:

- ORIENTATION — human knows where they are;
- CURRENT STATE — real state/data is visible;
- INTELLIGENCE — useful interpretation exists where promised;
- ACTION — meaningful actions work;
- PROOF — provenance/evidence available where needed;
- LOADING;
- EMPTY;
- BLOCKED;
- UNAUTHORIZED;
- NOT_VERIFIED;
- VERIFIED;
- ERROR;
- OFFLINE;
- UNKNOWN;
- responsive behavior;
- keyboard/focus;
- text scaling/zoom;
- performance;
- persistence/continuity;
- cross-room identity/handoff;
- negative/refusal behavior.

## 6. Eyes-on-the-work law

A UI builder must observe the rendered product.

Required applicable loop:

1. launch the actual app;
2. capture baseline screenshots;
3. make bounded change;
4. reload actual app;
5. capture same states/viewports;
6. compare;
7. click all affected controls;
8. inspect scroll/layout;
9. inspect browser console/network;
10. test keyboard;
11. test mobile/tablet;
12. test long-content/empty/error states;
13. score;
14. repair;
15. repeat.

Source review alone cannot close visual/interaction gates.

## 7. Independent-eye law

The builder does not close its own interface gate.

Use an independent Naya/verifier to inspect:

- screenshots;
- browser journeys;
- room completion matrix;
- state coverage;
- visual regressions;
- accessibility;
- performance;
- causal paths.

Self-score is useful diagnostic information.

It is not qualification.

## 8. Behavior-before-decoration sequencing

The build loop should not reward decorative completeness before causal completeness.

For each room:

1. establish correct canonical data/read model;
2. establish truthful states;
3. establish primary causal journey;
4. establish persistence/cross-room behavior;
5. establish responsive/accessibility behavior;
6. apply elite visual system;
7. micro-polish;
8. independent proof.

This does **not** mean "make it ugly first."

The approved design system is used throughout.

It means beauty may not substitute for behavior.

## 9. Vertical-slice rule

A first complete room is a **reference implementation**, not the finished application.

Its purpose is to prove:

- shell;
- tokens;
- runtime adapter;
- state system;
- data identity;
- interaction law;
- evidence;
- responsive behavior;
- quality process.

Then the pattern compounds into every declared room.

Do not leave ten rooms thin forever because one masterpiece exists.

## 10. Cross-room coherence gate

The app is not complete until important objects survive movement across rooms.

For a canonical intelligence object:

```
Feed → Today → Library → List → Space → Ledger/Evidence
```

must preserve the same canonical identity where applicable.

Navigation and projection may change.

Canonical meaning must not silently fork.

## 11. Completion matrix is mandatory

Maintain one authoritative machine-readable matrix that answers:

- What rooms exist?
- What state is each room in?
- What functions are still missing?
- What dependencies block them?
- What is independently verified?
- What regressed?
- What is the highest-value next action?

A cold successor should not reconstruct this from conversation.

## 12. Regression ratchet

When a surface reaches INDEPENDENTLY_VERIFIED:

- snapshot visuals;
- preserve acceptance journey;
- preserve state tests;
- preserve causal-path tests;
- preserve responsive checks.

Future work that weakens it must fail the regression gate or explicitly supersede the baseline with evidence.

A later room may not quietly destroy an earlier room.

## 13. 24-hour / continuous-agent operating loop

For long-running app work, the agent should repeatedly execute:

```
RESTORE CURRENT TRUTH
→ READ COMPLETION MATRIX
→ SELECT HIGHEST-VALUE UNBLOCKED GAP
→ BUILD SMALLEST COMPLETE IMPROVEMENT
→ RENDER + INTERACT
→ TEST
→ SCORE
→ INDEPENDENTLY CHALLENGE WHEN GATE-RELEVANT
→ UPDATE MATRIX
→ CHECKPOINT
→ REPEAT
```

Stop only for:
- true authority requirement;
- external dependency that cannot be routed around;
- unresolved canonical conflict;
- safety/privacy/governance decision requiring Human Director judgment.

Do not stop merely because "a version exists."

## 14. No-shell acceptance law

Automatic failure conditions:

- route/title exists but no real function;
- placeholder card counted as feature completion;
- sample data presented as live;
- client-local state presented as canonical;
- dead control looks active;
- missing room hidden by navigation;
- room has no error/empty behavior;
- mobile visibly breaks;
- completed room regresses while another is built;
- self-score used as final approval;
- Human Director must enumerate ordinary missing work.

## 15. Success

The Shell Barrier is broken when:

- the whole declared app scope is visible in one completion matrix;
- rooms advance monotonically through evidence states;
- builders see and interact with rendered output continuously;
- independent review catches regressions before Shawn does;
- one complete room becomes reusable architecture for the rest;
- no finished room is casually destroyed;
- cross-room identity/state works;
- all declared rooms become genuinely usable;
- Human Director becomes taste/mission authority rather than manual missing-work detector.

> **PLAN THE WHOLE → BUILD THE WHOLE → LOOK AT THE WHOLE → PROVE THE WHOLE → KEEP THE WHOLE.**
