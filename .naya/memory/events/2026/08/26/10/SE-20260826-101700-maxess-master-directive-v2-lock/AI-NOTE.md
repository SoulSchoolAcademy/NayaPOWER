# MAXESS Master Directive V2 — AI Note

**Event:** `SE-20260826-101700-maxess-master-directive-v2-lock`  
**Project:** MAXESS  
**Effective:** 2026-08-26  
**Status:** ACTIVE / CANONICAL

## Operational mandate

Treat `PROJECTS/MAXESS/MAXESS-MASTER-ENGINEERING-DESIGN-DIRECTIVE-V2.md` as the active MAXESS execution/design authority. V1 remains historical lineage.

Do not continue isolated E00/E00.xx patching as the default strategy. Inventory existing artifacts, extract proven behavior, identify fragile/duplicated architecture, then converge on one authoritative implementation.

## Authority model

`E00` owns the assessment runtime/state/completion/scoring/result creation.

`E01–E09` remain the nine canonical Results sections. They are presentation consumers of one validated `MAXESS_RESULT_V1` contract and must not rescore or infer the result from DOM text, timing, or another section.

Target:

`ONE APP → ONE STATE MACHINE → ONE ASSESSMENT DEFINITION/COMPILER → ONE SCORING ENGINE → ONE RESULT CONTRACT → ONE RELEASE PATH → E01–E09.`

## Golden regression

AI Score is the reference assessment: 15 questions, 5 answers each, 0–4 answer values, five dimensions, deterministic aggregation, normalized 0–100 score. Preserve the existing authoritative dimension mapping and mastery thresholds after reconciling canonical source.

Q15 must persist before scoring. Result creation must be deterministic and occur exactly once per completion.

## Dynamic assessment foundation

Design the runtime around configuration and structured knowledge so the same engine can compile supported AI/life topics without a mandatory paid runtime LLM API.

Pipeline:

`TOPIC → DOMAIN/COVERAGE → KNOWLEDGE MAP → LEARNING OBJECTIVES → CAPABILITIES → QUESTION ARCHETYPES → 0–4 RUBRIC → 15 QUESTIONS → VALIDATE → RUN.`

Use coverage states such as STRONG/GOOD/DEVELOPING/LIMITED/UNSUPPORTED. Never fabricate expertise. Advanced topics such as quantum computing are valid future/secondary tests when knowledge coverage is sufficient.

## Design mandate

MAXESS is flagship. Controls should feel like luminous precision jewelry: tactile, dimensional, responsive, accessible, and fast. Naya is a present human-centered guide, not decoration. Design for clarity, warmth, depth, and high-tech elegance without performance waste.

## Verification mandate

Use:

`REQUIREMENT → IMPLEMENTATION → TEST → OBSERVED RESULT → EVIDENCE → VERIFICATION → DOCUMENTED STATE.`

Status semantics:

- GREEN = implemented and verified by evidence;
- YELLOW = implemented but verification incomplete/ambiguous;
- RED = not implemented or not verified.

Never label code existence as green.

## Continuity mandate

Every meaningful execution should leave a human-readable note, AI handoff, verification receipt, current state, and next execution. Human-readable delivery is the default human-facing receipt; JSON is optional machine infrastructure.

## Next execution

Perform the complete MAXESS source/architecture inventory first, then implement the highest-leverage coherent rebuild work. Do not add another tactical E00 patch unless the inventory and evidence demonstrate that it is the correct architectural action.
