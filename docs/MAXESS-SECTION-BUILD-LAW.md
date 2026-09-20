# MAXESS SECTION BUILD LAW

**Status:** CANONICAL GOVERNANCE
**Effective:** 2026-08-19
**Authority:** NAYA OS / MAXESS Results governance

## PURPOSE

MAXESS is built as a cumulative, section-by-section experience. Finished work is protected so later AI execution cannot accidentally regenerate, rewrite, clean up, refactor, restyle, or otherwise damage an earlier section.

## THE LAW

### 1. BUILD SEQUENTIALLY

The required progression is:

**SECTION 01 → FREEZE → SECTION 02 → FREEZE → SECTION 03 → FREEZE → …**

A new section is an addition to the existing experience, not permission to regenerate the whole document.

### 2. FROZEN MEANS IMMUTABLE

Once a section is human-approved and frozen, its source and behavior are protected:

- HTML
- CSS
- JavaScript
- copy/text
- assets
- IDs and data contracts
- layout
- visual design
- animation/motion
- interaction
- responsive behavior
- accessibility behavior

A later section MUST NOT change any of these in a frozen section.

### 3. APPEND-ONLY DEFAULT

While Section N is active, modify only Section N and explicitly authorized new infrastructure. The intended structure is:

**LOCKED SECTION 01 + NEW SECTION 02**

then:

**LOCKED SECTION 01 + LOCKED SECTION 02 + NEW SECTION 03**

and so on.

Previously locked source must remain byte-for-byte unchanged unless the human explicitly reopens it.

### 4. NO GLOBAL DRIFT

Do not use whole-document regeneration, global CSS cleanup, shared-JS refactoring, architectural rewrites, or convenience refactors to implement a later section when those actions can alter a frozen section.

Scope new styles, scripts, selectors, IDs, and behavior to the active section whenever possible.

### 5. SECTION CONTRACT BEFORE CODE

Before implementing a new section, write its execution contract:

- purpose;
- human/emotional objective;
- visual objective;
- exact required text;
- forbidden text/content;
- components/objects;
- visual and dimensional behavior;
- interaction behavior;
- responsive behavior;
- accessibility requirements;
- transition from the previous section;
- acceptance criteria;
- failure conditions.

No invented copy, UI, explanation, marketing language, or unrelated content may be added merely because it seems useful.

### 6. EXACT TEXT CONTROL

Every section must explicitly define:

**TEXT REQUIRED**

**TEXT OPTIONAL**

**TEXT FORBIDDEN**

Unauthorized text is a defect when it changes the intended experience.

### 7. VISUAL OBJECT CONTRACT

Before creating Orbs, nodes, cards, scores, capability indicators, or other major visual objects, define what each object represents, what it displays, its hierarchy, dimensional treatment, color role, movement, and responsive behavior.

Do not add effects merely because another effect is possible. Mutate only when rendered evidence identifies a material weakness.

### 8. LOCK MANIFEST

Track every section as:

- **ACTIVE** — currently being built;
- **FROZEN** — human-approved and immutable;
- **REOPENED** — explicitly reopened by the human because a genuine dependency requires it.

Record the baseline commit/blob, protected scope, authorized mutation scope, and verification status.

### 9. REGRESSION GATE

Before freezing a new section:

1. re-fetch the committed artifact;
2. diff all prior frozen sections against their baselines;
3. prove no unauthorized prior-section mutation;
4. run static QA;
5. run JS/behavior QA;
6. run responsive QA;
7. run accessibility QA;
8. render the assembled experience where available;
9. perform human review of the active section;
10. record the evidence and freeze only when the applicable quality gate passes.

### 10. RECOVERY LAW

If a later mutation damages a frozen section:

**STOP → RESTORE FROM AUTHORITATIVE BASELINE → PROVE RESTORATION → RESUME ACTIVE SECTION.**

Do not patch the damaged result forward.

### 11. REOPEN LAW

If a genuine shared dependency requires a frozen-section change, ordinary section work stops. The dependency must be documented and the human must explicitly authorize reopening the affected section. After reopening, rerun that section's full regression and quality gate before continuing.

### 12. NO WHOLE-DOCUMENT REGENERATION

For large MAXESS artifacts, whole-document regeneration is prohibited when it risks altering locked sections. The default implementation method is surgical current-section mutation or append-only construction.

### 13. STOP-SEND QUALITY GATE

Code generation is not quality verification.

Before delivery, Naya MUST independently resist the implementation against the actual human objective and the active section contract.

The self-review must answer:

- Did I preserve every frozen section exactly?
- Did I modify only the authorized section?
- Did I build the requested experience rather than a plausible substitute?
- Are the primary visual objects and information hierarchy correct?
- Did I add any unauthorized copy, UI, effects, or structure?
- Does the result remain faithful to approved visual language?
- Does responsive behavior preserve the intended experience?
- What is the strongest reason this is not a 10?

If a material weakness is found, the artifact is **NOT READY TO SEND**. Repair it before delivery.

If actual visual rendering is unavailable, visual quality is **HUMAN REVIEW REQUIRED / UNKNOWN**. Source inspection must never be described as visual verification.

For active E02 work, the full task-specific lock is:

`docs/MAXESS-E02-EXECUTION-LOCK.md`

It is mandatory reading before E02 consequential execution.

### 14. ARTIFACT / HOST BOUNDARY

Separate section artifacts must not be confused with the assembled host experience.

Where the architecture defines separate section files:

**FROZEN SECTION SOURCE + ACTIVE SECTION EMBED = HOST ASSEMBLY**

The active section must not copy or regenerate frozen sections merely to make the active artifact appear complete by itself.

If a host environment assembles sections, Naya must deliver the active section as the authorized self-contained payload and clearly distinguish source verification from host/live verification.

### 15. FAILURE-TO-GUARDRAIL LAW

When a material execution failure repeats or reveals a process hole, do not merely patch the product.

Record:

**FAILURE → ROOT CAUSE → MISSING GATE → GUARDRAIL → VERIFICATION**

A durable failure should result in a durable process improvement whenever practical.

## REQUIRED EXECUTION PROMPT

Before consequential section implementation, the next-context prompt must contain:

**CURRENT LOCKED STATE → ACTIVE SECTION → MISSION → EXACT CONTENT → REQUIRED TEXT → FORBIDDEN TEXT → VISUAL SPECIFICATION → OBJECT/ORB SPECIFICATION → INTERACTION → RESPONSIVE → ACCESSIBILITY → APPEND-ONLY LAW → PRE-WRITE GATE → STOP-SEND SELF-REVIEW → VERIFICATION → FAIL CONDITIONS → FINAL REPORT.**

## LEADERSHIP REQUIREMENT

Naya must lead the user to the next correct action. Every consequential execution ends with:

**CURRENT STATE → WHAT WAS FOUND → RECOMMENDATION → WHY → EXACT NEXT ACTION → EXECUTION PROMPT → VERIFICATION STATUS.**

The user should not have to tell Naya what the obvious next engineering step is.

## TEACHABLE METHOD

This law is also a reusable AI website-building method:

**DEFINE → BUILD ONE SECTION → VERIFY → LOCK → APPEND THE NEXT → VERIFY → LOCK → REPEAT.**

The objective is to preserve human intent, protect finished work, reduce regression, and make AI-assisted creation predictable enough to teach to other builders.
