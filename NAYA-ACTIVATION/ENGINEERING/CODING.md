# ENGINEERING / CODING

## Operating sequence
READ -> CLASSIFY -> PLAN ONE CAUSAL UNIT -> CHANGE MINIMALLY -> TEST -> VERIFY -> RECORD -> HAND OFF.

## Before writing
Inspect AGENTS.md, activation contracts, control-plane state, project-intelligence, relevant source, tests, issues and PRs. Establish whether the request is documentation, behavior, infrastructure or proof work.

## Change discipline
Prefer the smallest effective change that advances the actual acceptance criterion. Preserve working behavior. Reuse canonical seams. Do not create parallel pipelines, stores or authority layers merely because an existing implementation is inconvenient.

## Evidence
A commit proves that code changed. A passing unit test proves a narrow behavior. A workflow receipt proves what that workflow observed. Production proof requires production evidence.

## Completion
No done claim without changed artifacts, test or verification evidence, known limitations and one next action.

## Whole-application completion law

For substantive app/interface builds, also read:
- `NAYA-ACTIVATION/DESIGN/COMPLETE-APP-BUILD-STANDARD-V1.md`
- the product's machine-readable completion matrix.

Do not close the task because the shell compiles or one vertical slice works.

Engineering completion requires the declared route/page/room inventory, shared services, causal actions, state/error handling, integration journeys, regression protection, and applicable proof to reach their declared gates.

**IMPLEMENTED ≠ TESTED ≠ INTEGRATED ≠ INDEPENDENTLY VERIFIED ≠ PRODUCTION-PROVEN.**

When work must hand off before full product closure, leave the completion matrix truthful and successor-ready. The Human Director is not the missing-work detector.
