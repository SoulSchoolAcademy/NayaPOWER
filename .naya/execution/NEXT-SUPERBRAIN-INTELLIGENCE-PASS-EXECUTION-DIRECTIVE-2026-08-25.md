# Naya Power — Next Superbrain Intelligence Pass

**Status:** EXECUTION-READY
**Purpose:** Give any Naya/apprentice AI an exact, dependency-ordered, evidence-first procedure for advancing the Superbrain toward measured 10/10 without redesigning working foundations.

## Master directive

Execute the maximum amount of **compatible, safe, reversible, verifiable** work in one execution. Do not create artificial one-task-at-a-time boundaries. Preserve green behavior. Never weaken validators, delete knowledge to obtain green, fabricate evidence, or claim completion from code existence.

The goal is not to complete 27 ceremonial tasks. The goal is to close the highest-value gaps in the correct dependency order and leave the repository measurably stronger.

## Definition of done

Every completed work item must have:
1. source-of-truth implementation identified;
2. smallest safe design chosen;
3. implementation completed where justified;
4. positive test(s);
5. deliberate failure/regression test(s) where applicable;
6. authoritative gate evidence;
7. state update;
8. Naya representation;
9. Shawn/Smart Note representation when meaningful;
10. AI-to-AI handoff with lessons and next action.

## Execution sequence

### Stage 0 — Restore and establish reality
1. Restore from repository state, not chat memory.
2. Read the canonical boot protocol, context manifest, current STATE, latest handoff, latest execution receipt, and authoritative gate configuration.
3. Record current commit and verified gate before changing anything.
4. Preserve every known green boundary.

### Stage 1 — Canonical event creation
5. Trace the real write path from event creation entry point through canonical storage.
6. Identify ID generation, validation, persistence, duplicate checks, and error handling.
7. Do not invent a parallel event writer if one already exists.
8. Document the exact call/data flow.

### Stage 2 — Idempotency
9. Define the idempotency key and identity contract using existing canonical identifiers where possible.
10. Determine behavior for first create, exact retry, conflicting retry, and malformed retry.
11. Implement the smallest compatible guard.
12. Add tests proving repeated identical creation returns the same identity/receipt and does not duplicate knowledge.
13. Add failure tests for conflicting payloads and invalid identity.

### Stage 3 — Entity resolution
14. Trace current exact-duplicate/entity candidate logic.
15. Keep exact duplicate detection separate from semantic/entity equivalence.
16. Define explicit decisions: CREATE, UPDATE, LINK, SUPERSEDE, REVIEW.
17. Preserve ambiguity instead of silently merging.
18. Add deterministic fixtures and tests before enabling automation.
19. Only automate decisions whose evidence threshold is justified; route uncertain cases to REVIEW.

### Stage 4 — Contradiction and supersession
20. Trace whether current events already carry authority, timestamps, provenance, and supersession fields.
21. Define contradiction as competing claims about the same entity/fact, not merely different wording.
22. Implement evidence-linked supersession without deleting historical truth.
23. Preserve old state as historical and identify the active state explicitly.
24. Add tests for new evidence, stale evidence, equal-authority conflict, and unresolved conflict.

### Stage 5 — Retrieval baseline
25. Trace how events enter the derived index and how retrieval currently ranks them.
26. Capture a deterministic baseline corpus and query set.
27. Measure current retrieval before adding semantic/vector infrastructure.
28. Preserve lexical, metadata, time, graph, authority, and verification signals already working.

### Stage 6 — Semantic retrieval
29. Identify the smallest safe insertion point for semantic/vector retrieval.
30. Add it as an additional retrieval signal, not a replacement for reliable lexical/metadata paths.
31. Define deterministic ranking/tie behavior.
32. Add fallback behavior when vector infrastructure is unavailable.
33. Test semantic paraphrases and adversarial irrelevant matches.

### Stage 7 — Retrieval benchmarking
34. Create a versioned benchmark set with expected relevant events.
35. Measure precision@k, recall@k, and useful ranking behavior.
36. Record the baseline and post-change results.
37. Fail CI only on explicitly defined regression thresholds; do not invent arbitrary targets after seeing results.

### Stage 8 — CIS compounding
38. Trace the existing Daily CIS generation and source-event selection.
39. Define how verified events become lessons, wins, unresolved questions, changes, and next actions.
40. Ensure today's report produces durable next-day starting intelligence.
41. Preserve provenance back to source events.
42. Add deterministic repeat/rebuild tests.

### Stage 9 — Health and cold-start
43. Define machine-readable health metrics: canonical count, duplicate count, unresolved reviews, graph integrity, index freshness, receipt completeness, continuity completeness, retrieval benchmark status, CIS freshness.
44. Build a health report without replacing existing diagnostics.
45. Create a true cold-start test: a clean AI must restore from repository artifacts and recover the same operational state required by the acceptance fixture.
46. Fail when required state cannot be reconstructed.

### Stage 10 — Outbox/recovery
47. Trace external-action receipt and delivery-state paths.
48. Identify whether actions are durable before delivery attempts.
49. Ensure retry does not create duplicate side effects when idempotency is available.
50. Add failure/retry/recovery tests.
51. Never mark delivered before evidence of delivery.

### Stage 11 — Gate and verification
52. Integrate only mature, tested checks into the authoritative Superbrain Gate.
53. Run focused tests first for rapid feedback.
54. Run the full existing test suite.
55. Run all new intelligence tests.
56. Run the authoritative gate.
57. Inspect actual logs and artifacts, not badges alone.
58. Compare final commit, gate run, job, and receipts.
59. If green, preserve the green boundary. If red, repair root cause; never weaken the gate.

### Stage 12 — Continuity closeout
60. Update canonical STATE with exact verified status and remaining gaps.
61. Create the Naya-facing note: technical state, implications, lessons, and recommendations.
62. Create the Shawn/Smart Note: plain-language accomplishment, proof, impact, and next move.
63. Create the AI-to-AI handoff: what happened, what changed, what was verified, what remains, what was learned, what to protect, and the next executable command.
64. Index all meaningful artifacts through the existing canonical mechanism.
65. Leave the system stronger and easier for the next AI to restore.

## Apprentice decision rules

- **Trace before designing.** The existing canonical path is the default place to extend.
- **Measure before optimizing.** Establish baseline before claiming improvement.
- **Additive before replacement.** Keep working retrieval and validation paths unless evidence proves replacement is better.
- **Explicit uncertainty beats false certainty.** REVIEW is a valid state.
- **History is never destroyed to simplify the present.** Supersede/link rather than erase.
- **Green must mean evidence.** A passing badge without inspected evidence is insufficient for a high-value claim.
- **Batch compatible work.** If stages are independent and safe, execute them in the same pass.
- **Stop only at a real boundary.** Examples: missing authority, destructive migration risk, unavailable required infrastructure, or ambiguous behavior that cannot be safely inferred.
- **Always leave learning.** If the work taught the system something reusable, preserve that lesson.

## Required final report

Return, in order:

1. WHAT I DID — numbered list of completed items.
2. HOW I DID IT — key implementation paths and design decisions.
3. WHAT CHANGED — exact files/artifacts and behavioral changes.
4. EVIDENCE — commits, tests, gate run/job, and relevant log results.
5. FAILURE TESTS — what was intentionally broken and whether the guard caught it.
6. CURRENT SCORECARD — green/yellow/red by capability.
7. LEARNINGS — reusable lessons and recommendations.
8. REMAINING GAPS — prioritized by dependency/value.
9. NAYA NOTE — AI-facing durable learning.
10. SHAWN/SMART NOTE — human-facing receipt.
11. AI-TO-AI HANDOFF — exact continuation state.
12. NEXT EXECUTION COMMAND — copy/paste-ready and dependency-aware.

**North Star:** extraordinary service through maximum useful progress, demonstrated by evidence, preserved through continuity, and compounded through learning.
