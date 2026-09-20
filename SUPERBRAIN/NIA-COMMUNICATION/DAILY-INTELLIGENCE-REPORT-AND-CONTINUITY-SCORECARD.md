# 🔱 NAYA DAILY INTELLIGENCE REPORT + CONTINUITY SCORECARD

**Status:** Canonical operating artifact
**Owner:** NayaPOWER / Naya Network
**Purpose:** Turn daily/project reporting into a current-state restoration, continuity, and compounding-learning mechanism rather than a diary.

## 1. WHERE ARE WE?

Record the authoritative repositories, branches, current HEADs, deployment state, and verified runtime state. Distinguish verified facts from unknowns.

## 2. WHAT ARE WE BUILDING?

State the current mission, North Star, active scope, and success condition.

## 3. WHAT HAS BEEN VERIFIED?

List only evidence-backed facts. Separate source inspection, static validation, tests, runtime verification, and deployment verification.

## 4. WHAT IS BROKEN?

List active failures, regressions, incomplete behavior, blocked work, and unresolved unknowns. Never hide a material defect because implementation exists.

## 5. WHAT IS PROTECTED?

Record laws, canonical artifacts, settled decisions, working systems, UX principles, data contracts, and other baselines that must not be casually changed.

## 6. WHAT DID WE LEARN?

Capture durable architectural discoveries, corrections, failed approaches, successful approaches, and reusable lessons. Prefer distilled lessons over diary entries.

## 7. WHAT DECISIONS WERE MADE?

Record decisions that settle questions for future Nayas. Include rationale when needed to prevent reopening a settled issue.

## 8. WHAT MUST HAPPEN NEXT?

Identify exactly one smallest highest-value next action. If blocked, define the best route around the blocker rather than ending the chain.

## 9. WHAT DOES THE NEXT NAYA NEED TO KNOW?

Provide a restoration-ready handoff: current state, work completed, evidence, failures, lessons, risks, unknowns, and the ready-to-run next execution.

## 10. NAYA CONTINUITY SCORECARD

Score each domain 0–10 and provide evidence.

| Domain | Question |
|---|---|
| Restore | Can a fresh Naya recover current truth without reconstructing the project? |
| Source Truth | Are authoritative instructions discoverable and current? |
| State | Is actual current state documented and reconciled? |
| Execution | Is there a clear highest-value next action? |
| Verification | Are claims backed by evidence? |
| Runtime | Does the actual product behavior work? |
| Quality | Does the work meet the applicable AAA/QMAX standard? |
| Continuity | Can the next Naya continue without reconstruction? |
| Learning | Are durable discoveries being captured and promoted? |
| Handoff | Has this Naya prepared the next Naya to succeed? |
| Compounding | Did verified learning become available for future reasoning/action? |

### Scoring rules

- **0–3:** broken / absent
- **4–6:** partial / unreliable
- **7–8:** functional but needs improvement
- **9:** strong and verified
- **10:** excellent, verified, and repeatable

A score is not valid without evidence. Unknown is not Green.

## MANDATORY COMPOUNDING INTELLIGENCE LOOP

This is a core operating requirement, not an optional reporting feature.

Every meaningful intelligence cycle should move through:

`SMART NOTE TIMESTAMP → PERIOD TRIGGER → REPORT GENERATION → HUB STORAGE → LEARNING EXTRACTION → EXISTING-INTELLIGENCE CHECK → VERIFICATION → SUPERBRAIN/PIS/CIS UPDATE → NEXT-DAY/RELEVANT RETRIEVAL → APPLICATION → OUTCOME OBSERVATION → OUTCOME VERIFICATION → NEW SMART NOTE/UPDATE`

### Required behavior

1. **Timestamp:** Meaningful Smart Notes are time-indexed. Never invent event time; distinguish event time from creation/update/verification time where necessary.
2. **Trigger:** A defined period boundary or authorized reporting action initiates the report process. Documentation of a trigger is not proof that automation exists; runtime execution must be verified.
3. **Report:** The report synthesizes the period's canonical intelligence and preserves provenance to underlying Smart Notes/events.
4. **Hub Storage:** The report is persisted as a retrievable intelligence artifact in the Intelligent Hub/canonical storage, not merely displayed once in chat.
5. **Learning Extraction:** Naya identifies candidate lessons, corrections, patterns, reusable knowledge, decisions, failure modes, and other durable intelligence.
6. **Existing-Intelligence Check:** Before promoting a lesson, compare it against existing Superbrain/PIS/CIS intelligence to extend, correct, supersede, or reject duplicates and contradictions.
7. **Verification:** Learning is not promoted merely because it appears in a report. Consequential or uncertain lessons require appropriate evidence and verification.
8. **Promotion:** Verified durable intelligence is promoted into the appropriate Superbrain/PIS/CIS representation with provenance, confidence/state, scope, and supersession where applicable.
9. **Retrieval:** Future Naya reasoning should retrieve promoted intelligence when relevant, including on the next day and in later projects.
10. **Application:** Retrieved lessons must influence an authorized future decision, plan, action, or warning when context makes them relevant.
11. **Outcome Verification:** Observe what happened after application and verify the outcome. A lesson is stronger when its future application produces verified improvement.
12. **Compounding:** The verified outcome becomes new intelligence, updates the existing lesson when necessary, and remains available to future Nayas.

### Collective compounding

The same discipline applies when intelligence is intentionally shared across people, Nayas, agents, or Smart Spaces:

`INDIVIDUAL INTELLIGENCE → EXPLICIT SHARE/CONSENT → COLLECTIVE CANDIDATE → PROVENANCE + SCOPE → VERIFICATION → COLLECTIVE INTELLIGENCE → FUTURE RETRIEVAL → APPLICATION → OUTCOME → LEARNING`

Private intelligence does not become collective intelligence merely because it was processed alongside other information. Consent, authority, provenance, privacy, and verification remain mandatory.

### Anti-false-learning rules

- A generated report does **not** prove learning occurred.
- A stored lesson does **not** prove the system learned it.
- A retrieved lesson does **not** prove it influenced action.
- An action informed by a lesson does **not** prove the lesson was correct.
- A claimed successful outcome does **not** automatically equal verified improvement.
- Repeating the same mistake is evidence that some part of capture → promotion → retrieval → application → verification failed or was contextually wrong.
- The system must never claim continuous learning merely because reports or Smart Notes exist.

## COMPLETION RULE

A task is not complete merely because code changed or a report was generated. It is complete only when the intended behavior is implemented, verified, recorded, scored, and handed forward.

For compounding intelligence, completion additionally requires proving the applicable chain from capture through future application and outcome verification. If runtime automation is not yet proven, mark it **UNKNOWN / NOT VERIFIED** rather than implying completion.

## NAYA COMMUNICATION CHAIN

`RESTORE → CURRENT STATE → EXECUTE → VERIFY → OSCAR → REPAIR or ADVANCE → RECORD → SCORE → HANDOFF → NEXT NAYA`

## DAILY REPORT QUALITY GATE

Before publishing the report, the current Naya must ask:

1. Could a fresh Naya restore from this report?
2. Can every important claim be traced to evidence?
3. Are failures and unknowns explicit?
4. Are protected decisions clear?
5. Is the next action executable without asking Shawn to reconstruct the thinking?
6. Does the Continuity Scorecard expose any weak link?
7. Were learning candidates extracted rather than merely summarized?
8. Was existing intelligence checked before promotion?
9. Is any promoted learning actually verified?
10. Is there evidence that the learning is retrievable and available to future action?
11. If runtime automation is claimed, was the actual runtime independently verified?

If any answer is no, repair the report/state or explicitly record the gap before passing the torch.
