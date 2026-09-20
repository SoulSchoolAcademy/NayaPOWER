# MAXESS SECTION INTEGRITY GATE

**Status:** CANONICAL EXECUTION GUARDRAIL
**Effective:** 2026-08-19
**Authority:** NAYA LAW / MAXESS SECTION BUILD LAW
**Purpose:** Prevent AI execution from modifying, replacing, regenerating, or visually absorbing any frozen MAXESS section while building a later section.

## 1. NON-NEGOTIABLE ARCHITECTURE

MAXESS is cumulative.

The product is built as:

**SECTION 01 → FREEZE → SECTION 02 → FREEZE → SECTION 03 → FREEZE → …**

Therefore, when Section N is active:

**FROZEN SECTIONS = IMMUTABLE PREFIX**

**ACTIVE SECTION = ONLY AUTHORIZED MUTATION ZONE**

The active artifact must preserve the frozen prefix and append/modify only the active section.

## 2. HARD STOP BEFORE ANY WRITE

Before creating, updating, deleting, regenerating, or replacing ANY MAXESS artifact, Naya MUST prove all of the following:

1. Canonical repository identified.
2. Governance branch identified.
3. Active engineering branch identified.
4. Exact authoritative artifact identified.
5. Frozen sections identified.
6. Active section identified.
7. Frozen-section baseline commit and blob identified.
8. Current active artifact fetched from GitHub.
9. Current frozen prefix compared against its authoritative baseline.
10. Required section contract read.
11. Required text and forbidden text established.
12. Exact mutation boundary established.

If any item is **UNKNOWN**, Naya MUST NOT WRITE.

Decision = **INVESTIGATE** or **STOP**, not ASSUME.

## 3. PREFIX INTEGRITY INVARIANT

For every later-section execution:

```text
CURRENT FROZEN PREFIX == AUTHORITATIVE FROZEN BASELINE
```

The comparison must be performed before mutation and again after mutation.

Where byte-level comparison is available, it is the required proof.

Where byte-level comparison is not available, Naya must use the strongest available exact source comparison and explicitly label the result.

If the frozen prefix differs unexpectedly:

**STOP → RESTORE FROM AUTHORITATIVE BASELINE → PROVE RESTORATION → ONLY THEN RESUME.**

Never patch forward from a damaged frozen section.

## 4. ACTIVE-SECTION BOUNDARY

When E02 is active:

**AUTHORIZED:** E02 code, E02 styles, E02 behavior, E02 assets, E02 copy, and explicitly required shared infrastructure that has been proven not to alter E01.

**FORBIDDEN:** E01 HTML, CSS, JS, copy, assets, IDs, layout, motion, interactions, responsive behavior, accessibility behavior, or visual treatment.

The same rule applies recursively for every later section.

## 5. NO STANDALONE SECTION REPLACEMENTS

A later section is NOT a new webpage.

Do NOT:

- create a standalone replacement renderer;
- create an alternative page and treat it as the assembled product;
- replace the complete artifact with a simplified recreation;
- regenerate the whole document for convenience;
- copy/rebuild frozen sections into a new implementation;
- create competing renderers without explicit architectural approval.

A review candidate may exist only when explicitly authorized by governance and must never become an uncontrolled competing source of truth.

## 6. SURGICAL IMPLEMENTATION RULE

For a fragile or large artifact, the default implementation method is:

**FETCH → LOCATE ACTIVE BOUNDARY → PRESERVE FROZEN PREFIX → MODIFY ACTIVE SECTION ONLY → REFETCH → DIFF → QA → RENDER → REVIEW → COMMIT → REFETCH → PROVE**

Do not regenerate the entire file from memory.

Do not rewrite a frozen section into a new document.

Do not infer the active boundary from visual appearance alone.

## 7. SECTION CONTRACT GATE

Before coding a new section, establish:

- PURPOSE
- HUMAN EXPERIENCE
- VISUAL OBJECTIVE
- EXACT TEXT REQUIRED
- TEXT OPTIONAL
- TEXT FORBIDDEN
- COMPONENTS / OBJECTS
- ORB SPECIFICATION where applicable
- DIMENSIONAL BEHAVIOR
- COLOR SYSTEM
- MOTION
- SPATIAL COMPOSITION
- RESPONSIVE BEHAVIOR
- ACCESSIBILITY
- TRANSITION FROM PREVIOUS SECTION
- ACCEPTANCE CRITERIA
- FAILURE CONDITIONS

No invented copy, marketing language, UI, effect, or explanatory material may be added merely because it seems useful.

## 8. VISUAL MIRROR RULE

When the user says to mirror an approved object from a frozen section, the approved object is the visual source of truth.

Do NOT redesign the frozen object.

Instead:

**OBSERVE → EXTRACT VISUAL PRINCIPLES → REUSE THE PRINCIPLES IN THE NEW SECTION**

For E02 specifically, if the mission is to mirror the E01 Orb, preserve its fundamental:

- spherical dimensionality;
- score-first hierarchy;
- readable number treatment;
- orbiting bead concept;
- premium physical presence;
- living motion language;

while allowing the explicitly authorized E02 differences such as dimension color and score.

## 9. TEXT MINIMALISM RULE

A personal Results report is not automatically a marketing landing page.

If the contract does not require explanatory or promotional copy, do not add it.

Before adding text ask:

**Is this required to understand the report?**

If no, omit it.

## 10. PRE-COMMIT REGRESSION GATE

Before committing a later section:

1. Re-fetch the assembled artifact.
2. Re-fetch each frozen-section baseline.
3. Prove frozen sections are unchanged.
4. Diff the active section against its intended baseline.
5. Run static QA.
6. Run JS/behavior QA.
7. Run responsive QA.
8. Run accessibility QA.
9. Render the assembled experience.
10. Perform human review of the active section.
11. Run Oscar resistance review.
12. Repair material defects.
13. Re-test.
14. Only then commit.

## 11. FAILURE CLASSIFICATION

If this gate is violated, classify the failure as:

**PRESERVATION FAILURE + SOURCE CHAOS + EXECUTION SUBSTITUTION**

Then apply:

**STOP → ROOT CAUSE → RESTORE → PROVE → ADD SAFEGUARD → RESUME**

Do not normalize the violation as a visual iteration.

## 12. REQUIRED EXECUTION PROMPT

Every later-section execution prompt MUST begin with:

**HARD FREEZE: E01**

and explicitly state:

- frozen artifact;
- frozen baseline commit/blob;
- active artifact;
- active section;
- append-only rule;
- exact mutation boundary;
- forbidden whole-document regeneration;
- forbidden competing renderer;
- pre-write integrity gate;
- post-write integrity gate;
- recovery rule.

## 13. REQUIRED FAILURE RESPONSE

If Naya discovers that a frozen section was altered:

Naya must immediately say:

**STOP — FROZEN SECTION INTEGRITY VIOLATION.**

Then identify:

- what changed;
- where it changed;
- the authoritative baseline;
- the root cause;
- the recovery action;
- the safeguard added.

Naya must not continue visual work until restoration is proven.

## 14. TEACHABLE METHOD

This gate exists so the workflow can be taught to other people and other AI systems:

**DEFINE → BASELINE → LOCK → BUILD ONE SECTION → PROVE PREFIX → VERIFY ACTIVE SECTION → FREEZE → APPEND NEXT → REPEAT**

The objective is not merely beautiful output.

The objective is **beautiful output without destroying completed work.**

## 15. SUCCESS CONDITION

A later-section execution is successful only when:

**FROZEN WORK IS PRESERVED + ACTIVE SECTION IS CORRECT + USER EXPERIENCE IS VERIFIED + NO UNAUTHORIZED SOURCE EXISTS.**

Code existing in GitHub is not enough.

A successful commit is not enough.

A visually improved screenshot is not enough.

The assembled product must satisfy the integrity gate and the applicable human-quality gate.
