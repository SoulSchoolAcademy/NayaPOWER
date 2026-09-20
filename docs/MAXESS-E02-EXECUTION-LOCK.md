# MAXESS E02 — EXECUTION LOCK

**Status:** CANONICAL TASK EXECUTION GUARDRAIL  
**Effective:** 2026-08-19  
**Authority:** MAXESS SECTION BUILD LAW + NAYA LAW  
**Scope:** Section 02 execution only

## PURPOSE

Prevent the recurring MAXESS failure in which an AI understands the words of the task but produces the wrong artifact, destroys or absorbs a frozen section, overbuilds copy/effects, or sends an unreviewed result as if it were quality.

This document is an execution contract, not a design suggestion.

## 1. HARD LOCKED STATE

**Repository:** `SoulSchoolAcademy/MaxRESULTS`  
**Governance:** `main`  
**Engineering branch:** `maxess-results-v21-working`  
**Frozen section:** `E01-SECTION-01-WORKING.html`  
**Frozen E01 blob:** `c01ba966c4b1439b8b3e95161c6f8316202736d8`  
**Active section:** `E02-SECTION-02-WORKING.html`  
**Mutation zone:** E02 only.

E01 is immutable unless the human explicitly reopens it.

### E01 PROHIBITIONS

Never:

- rewrite E01;
- regenerate E01;
- clean up E01;
- refactor E01;
- change E01 CSS, JS, copy, assets, IDs, layout, motion, behavior, responsive behavior, or accessibility;
- copy E01 into E02;
- recreate E01 from memory;
- create an assembled replacement that contains a second E01.

Before every write, prove the current E01 blob equals the frozen blob.

After every write, prove it again.

If it does not match:

**STOP — FROZEN SECTION INTEGRITY VIOLATION.**

Restore from the frozen baseline, prove restoration, then resume only the authorized active section.

## 2. ARTIFACT BOUNDARY — DO NOT CONFUSE SOURCE WITH HOST ASSEMBLY

E01 and E02 are separate GitHub section artifacts.

- E01 is the frozen Section 01 source.
- E02 is the active Section 02 self-contained embed.
- The host/publishing environment places E02 after E01.
- Naya builds the E02 payload.
- The human publishes/assembles it in the host environment.
- Naya does not operate or verify Groove.

Therefore:

**E01 SOURCE ≠ E02 SOURCE ≠ ASSEMBLED HOST EXPERIENCE**

Never “fix” an E02 problem by copying E01 into E02.

Never claim an E02-only embed is the assembled E01→E02 experience.

When delivering E02, explicitly state that it is Section 02 only and that the host order is E01 → E02.

## 3. PRE-WRITE TRUTH GATE

Do not write until all are proven:

1. repository;
2. governance branch;
3. engineering branch;
4. current branch HEAD;
5. E01 path;
6. E01 frozen blob;
7. current E01 blob;
8. E02 path;
9. current E02 blob;
10. E02 contract;
11. exact mutation zone;
12. required text;
13. forbidden text;
14. visual objective;
15. protected E01 behavior;
16. recovery path;
17. deployment/Groove boundary.

Any UNKNOWN = **DO NOT WRITE**.

## 4. E02 NORTH STAR

**FIVE DIMENSIONS → FIVE LIVING ORBS → FIVE SCORES → CURIOSITY → DESIRE TO UNDERSTAND THE PERSONAL REPORT**

E02 is a **personal Results report**.

It is not:

- a marketing landing page;
- a sales page;
- a dashboard;
- a statistics wall;
- a generic white webpage;
- a card grid;
- a text-heavy explanation page.

The visual hierarchy is:

1. five physical/dimensional Orbs;
2. large centered scores;
3. `/ 100`;
4. five coherent jewel colors;
5. dimension names;
6. spatial composition;
7. premium pearl environment;
8. dimensional black capability node;
9. only the minimum required text.

If a design decision competes with the Orbs or scores, the design decision loses.

## 5. EXACT REQUIRED TEXT

Use only the contract-approved text:

**YOUR FIVE DIMENSIONS**

**Five dimensions. One capability picture.**

**Five living signals show what makes up your AI capability.**

**YOUR AI CAPABILITY**

**Five dimensions. One system.**

Dimensions:

- Direction
- Communication
- Evaluation
- Iteration
- Systems Thinking

Each Orb:

**NUMBER / 100**

No additional explanatory copy unless the human explicitly authorizes it.

## 6. E02 VISUAL OBJECT CONTRACT

Each Orb must:

- be physically present;
- be spherical;
- feel dimensional, not flat;
- have a black/dark physical core;
- contain internal light and depth;
- have a dimensional edge/halo;
- contain a large centered score;
- use one jewel accent color;
- breathe subtly on a 6-second cycle;
- remain visually related to the approved E01 Orb family;
- remain readable before decorative effects are noticed.

The E01 Orb is the visual reference. Mirror its principles; do not alter E01.

An orbiting bead/ring is optional. It is permitted only if it clearly improves the E02 physical-object experience and remains restrained. Never add it because it is technically possible.

## 7. COMPOSITION LAW

Desktop should feel like a **spatial field of five capability objects**, not five dashboard widgets.

Do not default to:

- five equal cards;
- a narrow centered column;
- excessive boxed containers;
- a giant white slab with text sitting above it;
- symmetrical dashboard tiles;
- excessive UI chrome.

Use the available width intelligently.

The pearl environment should support the objects, not become the object.

The black capability node should feel like a dimensional anchor, not an information card.

Mobile must be intentionally composed. Never shrink the desktop arrangement until it becomes cramped.

## 8. DATA LAW

Use authoritative `window.MAXESS_RESULT` data.

Do not create a second scoring engine.

Do not fabricate production scores.

Do not expose demo values in the normal human experience.

If required data is unavailable, fail safely.

## 9. IMPLEMENTATION LAW

Modify **E02 only**.

Do not regenerate the whole document from memory.

Do not replace E02 with a tiny renderer, preview, mock, loader, excerpt, or competing artifact.

Do not add unrelated infrastructure unless it is proven necessary and cannot alter E01.

Scope E02 selectors, IDs, styles, and scripts to E02.

## 10. MANDATORY SELF-REVIEW GATE — THE STOP-SEND RULE

**Naya must not send, deliver, or describe an implementation as high quality merely because code was produced.**

Before delivery, Naya must perform an independent resistance review against the actual requested experience.

Ask, in order:

1. Is E01 still untouched?
2. Is this actually E02, or did I accidentally recreate/reframe the whole product?
3. Are the five Orbs the dominant visual objects?
4. Are the five numbers immediately readable?
5. Do the Orbs visibly inherit the physical language of E01?
6. Is the black core dimensional?
7. Are the five colors coherent jewel accents rather than a rainbow UI?
8. Is the composition spatial rather than dashboard-like?
9. Did I add text that the contract did not require?
10. Did I add effects because they were possible rather than necessary?
11. Does the pearl environment support the Orbs rather than overpower them?
12. Does mobile remain intentional and premium?
13. Does the first visual impression communicate “my capability has five dimensions” without requiring a paragraph?
14. Would a human immediately know where to look?
15. Would the user recognize this as MAXESS without seeing the title?
16. What is the single biggest reason this is not a 10?

If any material answer is NO, the implementation is **NOT READY TO SEND**.

Repair it before delivery.

If visual rendering is unavailable, mark visual quality **HUMAN REVIEW REQUIRED / UNKNOWN**. Never convert source inspection into visual verification.

## 11. VERIFICATION LOOP

Every E02 execution uses:

**FETCH → PROVE E01 → PROVE E02 IDENTITY → MAP → MODIFY E02 ONLY → REFETCH → DIFF → STATIC QA → JS/BEHAVIOR QA → RESPONSIVE QA → ACCESSIBILITY QA → SELF-REVIEW → OSCAR → REPAIR → RETEST → COMMIT → REFETCH → FINAL E01 PROOF → FINAL E02 PROOF → DELIVER**

Groove is outside Naya's engineering boundary.

The human performs the Groove host review.

## 12. FAILURE CLASSIFICATION

When the result is wrong, classify the failure before editing:

- PRESERVATION FAILURE
- SOURCE CHAOS
- EXECUTION SUBSTITUTION
- DESIGN FAILURE
- RESPONSIVE FAILURE
- ACCESSIBILITY FAILURE
- DATA/BEHAVIOR FAILURE
- VERIFICATION FAILURE
- HOST/EMBED FAILURE
- UNKNOWN

Then:

**FAILURE → ROOT CAUSE → REPAIR → VERIFICATION → SAFEGUARD**

Do not repeat a failed approach with different wording.

## 13. DELIVERY STATUS

Every delivery must distinguish:

**IMPLEMENTED** — code exists in E02.

**SOURCE VERIFIED** — E01/E02 identity, scope, diff, and technical QA are proven.

**RUNTIME VERIFIED** — the artifact actually executed in an available engineering runtime.

**LIVE VERIFIED** — the public environment was actually inspected.

**HUMAN REVIEW REQUIRED** — final judgment requires the human/host environment.

**UNKNOWN** — evidence does not exist.

Never use “done,” “10/10,” “extraordinary,” or “verified” as a substitute for evidence.

## 14. FINAL REPORT CONTRACT

Every E02 execution ends with:

- CURRENT STATE
- WHAT WAS FOUND
- ROOT CAUSE
- WHAT CHANGED
- E01 BASELINE
- E01 CURRENT BLOB
- E02 BASELINE
- E02 NEW BLOB
- SECTION 01 REGRESSION
- STATIC QA
- RUNTIME QA
- RESPONSIVE QA
- ACCESSIBILITY QA
- OSCAR
- HUMAN REVIEW
- IMPLEMENTED
- SOURCE VERIFIED
- RUNTIME VERIFIED
- LIVE VERIFIED
- HUMAN REVIEW REQUIRED
- UNKNOWN
- EXACT NEXT ACTION
- NEXT EXECUTION PROMPT

No claim without evidence.

## 15. RECOVERY

If any future execution violates this lock:

**STOP. DO NOT PATCH FORWARD.**

Identify the exact violation, restore the frozen state if necessary, prove restoration, record the root cause, strengthen the guardrail, and only then resume.

The goal is not to make the AI apologize better.

The goal is to make the failure harder to repeat.
