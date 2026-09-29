# ACT Node Contract V1

**ID:** NAYA-KERNEL-ACT

## Purpose

ACT converts governed intent into safe execution. It ensures that authorized actions are performed with appropriate care, reversibility awareness, and outcome tracking.

## Inputs

- Authorized context from LAW
- Action plan and parameters
- Reversibility classification
- Expected outcome definition
- Proof requirements

## Outputs

- Plan (selected approach)
- Action (executed operation)
- Execution state (progress, status)
- Observation target (what to measure)
- Proof requirement (what evidence is needed)

## MUST Rules

- Consume authorized context before any action.
- Validate LAW evaluation time before private intelligence access or execution: it must be present, parseable and no later than the current clock. Enforce the registered Door's maximum age. A missing or malformed timestamp cannot establish freshness.
- Reject malformed non-null expiry on the LAW decision or current live grant. Null or absent expiry is unbounded; expiry at the current clock is expired. Reread live authority even when the LAW receipt remains fresh.
- Select the minimum sufficient action.
- Respect refusal, confirmation and reversibility boundaries.
- Define expected outcome and proof before consequential execution where practical.
- Record execution state throughout.
- Produce receipts for all actions.

## MUST NOT Rules

- Decide its own authority.
- Claim success from execution alone.
- Repeat a failed strategy unchanged without new information.
- Execute consequential actions without proof requirements.
- Skip receipt generation.

## Acceptance Criteria

- Every action traces to an authorization decision.
- Minimum sufficient action is selected.
- Reversibility boundaries are respected.
- Execution state is fully recorded.
- Receipts are produced for all actions.
- Expected outcomes are defined before execution.

## Failure States

| Failure | Behavior |
|---|---|
| Authorization missing | Halt; do not execute |
| LAW evaluation time missing, malformed or future | Persist `LAW_RECEIPT_TIME_INVALID` refusal before intelligence access |
| Authority expiry malformed | Persist `LAW_AUTHORITY_TIME_INVALID` or `LIVE_AUTHORITY_TIME_INVALID` refusal before intelligence access |
| Execution fails | Record failure; emit receipt; do not retry blindly |
| Reversibility violated | Halt; alert; attempt rollback |
| Proof requirement unmet | Mark outcome as UNVERIFIED |
| Receipt generation fails | Mark action as UNVERIFIED; alert |
