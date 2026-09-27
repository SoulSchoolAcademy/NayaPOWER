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
- Execution state (PLANNED, AUTHORIZED, EXECUTING, COMPLETED, FAILED, HALTED, ROLLED_BACK)
- Observation target (what to measure)
- Proof requirement — proof status (DEFINED, MET, UNMET, UNVERIFIED)

## MUST Rules

- Consume authorized context before any action.
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
| Execution fails | Record failure; emit receipt; do not retry blindly |
| Reversibility violated | Halt; alert; attempt rollback |
| Proof requirement unmet | Mark outcome as UNVERIFIED |
| Receipt generation fails | Mark action as UNVERIFIED; alert |
