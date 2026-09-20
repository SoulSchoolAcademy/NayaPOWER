# 🔱 NIA HANDOFF TEMPLATE

**Purpose:** successor-ready communication. Write this for the next Naya, not for the previous conversation.

## MISSION
What objective was being executed?

## SOURCE OF TRUTH
Repository / path / branch / HEAD / governing law.

## CURRENT STATE
What is true now? Include VERIFIED / PENDING / FAILED / SUPERSEDED / UNKNOWN.

## PROTECTED BASELINE
What must not be broken or replaced?

## WORK COMPLETED
What actually changed? Name files, components, systems, or decisions.

## EVIDENCE
What tests, runtime observations, artifacts, commits, or receipts prove the claims?

**Human receipt requirement:** whenever a durable artifact has a navigable URL, provide the clickable artifact link. Commit SHAs and internal identifiers are secondary provenance, not the primary human-facing receipt.

## HUMAN RECEIPTS
For each material artifact or verified claim, provide, when available:

1. **Artifact** — what the human should inspect.
2. **Clickable link** — direct navigable URL to the artifact.
3. **Verification** — exactly what was verified.
4. **Evidence** — test, runtime observation, CI run, or authoritative source.
5. **Remaining uncertainty** — what is not yet proven.

Do not replace this section with commit numbers alone.

## DECISIONS
What choices were made and why?

## FAILURES / HA-HAS / TRAPS
What failed, surprised us, or would waste the next Naya's time if rediscovered?

## REJECTED APPROACHES
What was tried and rejected? Why?

## LESSONS
What durable knowledge did this Naya gain?

## UNKNOWNS
What has not been proven?

## RISKS
What could still fail or regress?

## OSCAR
- Status:
- Score:
- Why not 10:
- Material defects:
- Repair required:
- Advancement authorization:

## OUTPUT SELF-SCORE
Score the final human-facing output before handoff:

| Dimension | Target | Score | Evidence / reason |
|---|---:|---:|---|
| Value | 10 | | |
| Truth | 10 | | |
| Receipts | 10 | | |
| Actionability | 10 | | |
| Continuity | 10 | | |
| Efficiency | 10 | | |
| Quality | 10 | | |
| Anticipation | 10 | | |
| Learning | 10 | | |
| Compounding | 10 | | |

If any material dimension is below 10 and can be improved safely within scope, repair the output before handoff. Never fabricate evidence to obtain a higher score.

## RECOMMENDATION
What is the highest-value next move?

## NEXT EXECUTION
Write a complete, ready-to-run instruction for the successor. The successor should not need the previous chat to execute it.

The Next Execution must be copy/paste executable and should include:

- Mission
- Source of Truth
- Read First
- Current State
- Protected Baseline
- Objective
- Do Not
- Execute
- Success Criteria
- Verification Requirements
- Required Receipts
- Learning / handoff requirement

Do not end with a vague "continue" instruction when a concrete next action can be identified.

## PASS CONDITION
Define the evidence that will make this objective GREEN/AAA.

## PROVENANCE
Commit(s), workflow run(s), artifact(s), receipt(s), and relevant canonical records.

## SUCCESSOR MESSAGE
> Future Naya: here is what I learned that I most want you to know...
