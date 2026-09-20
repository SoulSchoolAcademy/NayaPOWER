# Smart Note — MAXESS E118 / E0796 Engine Recovery

**Date:** 2026-08-26
**Project:** MAXESS assessment/results engine
**Category:** PROJECT / SMART NOTE / ENGINE RECOVERY
**Status:** ACTIVE — NORTH STAR LOCKED

## North Star

**Get the MAXESS engine fully functioning end-to-end.**

The objective is not to preserve a particular implementation merely because it exists. The objective is a working, coherent, verified system in which the page's component/code sections communicate correctly, the assessment state flows correctly, scoring/results work, and the whole experience survives verification.

## Current known state

- The current live implementation is reported by Shawn as **E118**.
- **E0796/E00796** is a larger implementation, approximately 700 lines, while E118 is a condensed implementation, approximately 118 lines.
- Shawn reports that both implementations work independently.
- The decision between E118 and E0796 is intentionally **not locked yet**.
- The immediate engineering problem is integration: the pieces are part of one page but are not reliably communicating with one another.
- The correct approach is therefore to evaluate the complete system and establish the actual dependency/data/event flow before choosing which implementation becomes canonical.

## Decision rule: E118 vs E0796

Do **not** choose based on line count.

Choose the implementation that provides the strongest combination of:

1. verified behavior;
2. complete required functionality;
3. clean integration boundaries;
4. maintainability;
5. compatibility with the surrounding page;
6. least regression risk;
7. easiest deterministic verification.

If E0796 contains valuable logic missing from E118, selectively preserve and integrate that logic rather than blindly replacing a working implementation. If E118 is sufficient and materially simpler, prefer E118. If neither is sufficient alone, use the smallest safe hybrid that restores the canonical engine behavior.

## Engineering method

**PRESERVE → INSPECT → MAP → ISOLATE → INTEGRATE → TEST → VERIFY → ADOPT**

1. Establish the actual live/canonical code and protected behavior.
2. Inventory every MAXESS page component that participates in assessment state, navigation, scoring, results, Naya interaction, and persistence.
3. Map inputs/outputs/events/shared state between components.
4. Identify the exact communication boundary or contract that is failing.
5. Fix the smallest root cause rather than rewriting functioning sections.
6. Test the complete user path, not isolated snippets only.
7. Record observed evidence and keep unresolved unknowns explicit.
8. Only then promote the chosen implementation to canonical.

## Verification target

At minimum, establish evidence for:

- assessment loads;
- answers render;
- answer selection updates state;
- Continue activates only when appropriate;
- question progression works;
- progress is correct;
- scoring receives the complete answer set;
- score is calculated correctly;
- results are visibly rendered;
- mastery band/dimensions/fingerprint are correct;
- all 15 questions can be completed;
- the integrated page does not break adjacent components;
- relevant responsive behavior remains intact.

## Anti-loop rule

Do not repeatedly patch isolated snippets without restoring whole-system context first. Every repair must state:

**WHAT IS BROKEN → WHY → WHAT CONTRACT IS SUPPOSED TO HAPPEN → WHAT CHANGED → HOW IT WAS VERIFIED → WHAT REMAINS**

## AI handoff requirement

Every AI/session doing meaningful MAXESS work must leave a durable handoff containing:

- current project;
- North Star;
- current state;
- exact work performed;
- evidence/verification;
- unresolved issues;
- protected behavior;
- decisions made;
- lessons learned;
- exact next action;
- ready-to-run next execution.

The next AI must be able to continue from the repository without reconstructing the previous chat.

## Relationship to Superbrain operating law

This project follows the Naya Power constitutional execution contract: understand, restore context, define North Star, execute, verify, learn, document, hand off, and leave a Next Execution. The repository is the durable handoff layer; conversation memory is not authoritative when repository evidence exists.

## Next Execution

**Inspect the full MAXESS implementation currently present in `SoulSchoolAcademy/NayaPOWER`, identify the canonical E118/E0796 artifacts and all communicating page components, then produce an evidence-backed dependency/data/event map and root-cause diagnosis before making any integration change.**

Success means we can name exactly which code is live, which code is authoritative, what each section owns, where communication fails, and the smallest safe change that can make the complete engine work.
