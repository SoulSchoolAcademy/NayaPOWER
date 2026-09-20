# MAXESS Section Lock + Append-Only Law

**Timestamp:** 2026-08-19
**Category:** SOLUTION / DECISION

## Keywords

MAXESS section lock, append-only, immutable section, Section 01, Section 02, section-by-section, frozen baseline, preservation, regression, section contract, exact text, forbidden text, execution prompt, human review, Groove, Naya Nitro

## Aliases / synonyms

section freeze, section lock, immutable prior section, current-section-only, append-only build, protect previous work, no rewrite, no refactor, no cleanup, progressive page construction, locked artifact regions

## Related paths / concepts

- `NAYA-OS.md`
- `docs/MAXESS-SECTION-BUILD-LAW.md`
- `docs/REPOSITORY-MAP.md`
- `docs/smart-notes/INDEX.md`
- `E01-SECTION-01-WORKING.html`
- MAXESS Results section-by-section build model
- Groove human review

## Context

MAXESS is intentionally built as a sequential, cumulative experience. A major failure mode occurred when later work was treated like ordinary page refactoring: a request for Section 02 caused the previously refined Section 01 experience to be regenerated or disturbed. This violates the product methodology and creates avoidable regressions in a large artifact.

The durable solution is an explicit append-only construction law. Once a section is approved and frozen, its source, behavior, visual presentation, assets, CSS, JavaScript, copy, responsive behavior, and accessibility behavior are immutable unless the human explicitly reopens that section.

## Durable law

1. Build **SECTION 01 → FREEZE → SECTION 02 → FREEZE → SECTION 03 → FREEZE → …**.
2. A frozen section is immutable: no rewrite, regeneration, refactor, cleanup, reorder, restyle, CSS/JS change, asset change, copy change, behavior change, responsive change, accessibility change, identifier/data-contract change, or replacement.
3. The default implementation model is **LOCKED 01 + NEW 02**, then **LOCKED 01 + LOCKED 02 + NEW 03**, and so on.
4. Earlier locked source must remain byte-for-byte unchanged unless explicitly reopened by the human.
5. Before every new section, create a section contract defining purpose, human objective, visual objective, exact required text, forbidden text, objects, visual behavior, interactions, responsive behavior, accessibility, transitions, acceptance criteria, and failure conditions.
6. Define **TEXT REQUIRED / TEXT OPTIONAL / TEXT FORBIDDEN**. Do not invent unrelated copy or UI.
7. Define major visual objects/Orbs before implementation: representation, displayed information, hierarchy, dimensional treatment, color role, movement, and responsive behavior. Do not add effects merely because another effect is possible.
8. Track ACTIVE / FROZEN / REOPENED status plus baseline commit/blob and authorized mutation scope.
9. Before freezing a new section, re-fetch, diff all prior frozen sections, prove no unauthorized mutation, run static/JS/responsive/accessibility QA, render where available, and perform human review.
10. If a later mutation damages a frozen section: **STOP → RESTORE FROM AUTHORITATIVE BASELINE → PROVE RESTORATION → RESUME ACTIVE SECTION**. Do not patch the damaged result forward.
11. A frozen section may be reopened only for a genuine shared dependency and only with explicit human authorization, followed by a complete regression/quality gate.
12. Whole-document regeneration is prohibited when it risks altering locked sections.

## Required execution prompt

Before consequential section implementation, generate a copy/paste-ready prompt containing:

**CURRENT LOCKED STATE → ACTIVE SECTION → MISSION → EXACT CONTENT → REQUIRED TEXT → FORBIDDEN TEXT → VISUAL SPECIFICATION → OBJECT/ORB SPECIFICATION → INTERACTION → RESPONSIVE → ACCESSIBILITY → APPEND-ONLY LAW → VERIFICATION → FAIL CONDITIONS → FINAL REPORT.**

## Leadership requirement

After every consequential execution, proactively provide:

**CURRENT STATE → WHAT WAS FOUND → RECOMMENDATION → WHY → EXACT NEXT ACTION → EXECUTION PROMPT → VERIFICATION STATUS.**

The user should not have to identify the obvious next engineering action.

## Why this matters

This is a reusable method for building large, beautiful, reliable web experiences with AI:

**DEFINE → BUILD ONE SECTION → VERIFY → LOCK → APPEND THE NEXT → VERIFY → LOCK → REPEAT.**

## Evidence

- User explicitly established this law during MAXESS E02 recovery on 2026-08-19.
- `main:docs/MAXESS-SECTION-BUILD-LAW.md` is the canonical detailed law.
- `main:NAYA-OS.md` contains the broader Section Isolation + Freeze Law.
- `maxess-results-v21-working:E01-SECTION-01-WORKING.html` is the active E01 working artifact.
- `docs/smart-notes/2026/08/2026-08-19-section-isolation-and-nitro-execution-learning.md` records earlier section-freeze learning.
