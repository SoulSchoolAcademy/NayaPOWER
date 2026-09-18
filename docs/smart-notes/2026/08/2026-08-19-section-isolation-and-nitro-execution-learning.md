# Section Isolation + Nitro Execution Learning

**Timestamp:** 2026-08-19
**Category:** LEARNING / SOLUTION

## Keywords

Section 01, Section 02, section freeze, section isolation, frozen baseline, same-file mutation, GitHub connector, artifact retrieval, reconstruction, large artifact, Nitro, Naya Lead, execution loop, raw Groove artifact, human review, AAA

## Aliases / synonyms

section freeze, section lock, current-section-only, protect prior sections, no regression across sections, same artifact mutation, GitHub-first, blocker-to-solution, raw Groove embed delivery, progressive mutation workflow

## Related paths / concepts

- `NAYA-OS.md`
- `START-HERE.md`
- `docs/REPOSITORY-MAP.md`
- `docs/NAYA-NITRO-MODE.md`
- `docs/NAYA-EXECUTION-PROMPT-TEMPLATE.md`
- `docs/NAYA-SMART-NOTES-SYSTEM.md`
- `E01-SECTION-01-WORKING.html`
- MAXESS Results section-by-section build model

## Context

During MAXESS E01 Section 01 refinement on 2026-08-19, repeated same-file mutations became reliable once the workflow consistently followed repository truth, complete-artifact retrieval, surgical mutation, re-fetch, diff, QA, commit, re-fetch, and raw GitHub delivery for human Groove review.

The user explicitly established a stronger working principle: technical constraints are not stopping conditions. When a transfer mechanism, payload limit, or other mechanism fails, Naya must identify the constraint, change the mechanism, and continue toward the same objective rather than presenting the limitation as the solution.

The user also established a section progression rule: once Section N reaches its quality gate and is frozen, work proceeds to Section N+1 without modifying the frozen section. Each section is developed and reviewed in isolation.

## Durable learning

The productive loop is:

**GITHUB FIRST → ESTABLISH STATE → IDENTIFY HIGHEST-VALUE WEAKNESS → SURGICAL SAME-FILE MUTATION → RE-FETCH → DIFF → STATIC QA → REGRESSION QA → COMMIT → RE-FETCH → PROVE → RAW GITHUB DELIVERY → GROOVE HUMAN REVIEW → FEEDBACK → NEXT MUTATION**

When a connector cannot expose a large artifact in one response, use authoritative retrieval in batches and reconstruct only from complete repository evidence. Never guess missing content. The objective is artifact integrity, not loyalty to one transfer mechanism.

The default delivery for Groove human review is the raw GitHub artifact URL pinned to the new committed SHA. The public live URL is a separate verification state and must not be substituted for the raw artifact delivery when the workflow calls for a Groove embed review.

## Required behavior

1. Inspect GitHub before consequential work.
2. Read current governance and task-relevant documents.
3. Establish branch, artifact, baseline SHA/blob, protected behavior, failures, and scope.
4. Preserve the complete working artifact.
5. Solve transfer or tooling constraints by changing mechanism, not objective.
6. Mutate only the current in-scope artifact/section.
7. Re-fetch the exact committed artifact and prove the intended mutation exists.
8. Use explicit verification states; never claim live verification without rendered evidence.
9. Deliver the raw GitHub artifact URL for Groove review when requested.
10. End consequential work with current state, recommendation, exact next action, and a complete next execution prompt.
11. Once a section is human-approved at the required quality gate, freeze it.
12. While building the next section, do not modify earlier frozen sections unless the human explicitly reopens them because a genuine shared dependency requires it; if reopened, rerun the earlier section's regression and quality gate.

## Quality rule

AAA is the minimum completion target for a visually complete section: **9.5/10 or higher across every material category within the evaluated evidence**. 10/10 is aspirational. Do not advance a section as visually complete when a material category remains below 9.5.

## Evidence

- `main:NAYA-OS.md` now contains the Section Isolation + Freeze Law.
- `maxess-results-v21-working:E01-SECTION-01-WORKING.html` reached the V39 refinement state with visible DEMO_SCORE=82 fallback, real `window.MAXESS_RESULT.overallScore` override, score-reactive palette, protected Orb geometry/motion, Naya speech lifecycle, and accessibility structure.
- Repeated 2026-08-19 E01 iterations demonstrated that surgical same-file mutation followed by re-fetch/diff/QA/commit/re-fetch is the productive execution pattern.
