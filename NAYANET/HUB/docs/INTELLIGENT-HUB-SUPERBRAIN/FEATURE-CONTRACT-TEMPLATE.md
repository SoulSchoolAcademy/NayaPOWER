# Feature Contract Template

**Feature ID:** `XX-NAME`
**Parent:** Intelligent Hub / Superbrain
**Status:** `DEFINED | CONTRACTED | IMPLEMENTING | VERIFYING | LIVE | BLOCKED`
**Version:** `1.0`
**Last updated:** `YYYY-MM-DD`

## 1. What is it?

Define the feature in plain language and its exact boundary inside the Superbrain.

## 2. Why does it exist?

State the human problem, intelligence purpose, and user value it is responsible for.

## 3. How does it work?

Describe the lifecycle from input to canonical event/intelligence to rendered or delivered result.

## 4. Inputs and outputs

- Inputs:
- Outputs:
- Canonical event/data model:
- Evidence required:

## 5. Connections

List upstream dependencies, downstream consumers, shared services, and relationships to sibling parts. The feature must reuse the parent intelligence/event model rather than create an isolated competing system.

## 6. Privacy, consent, and authority

Define ownership, visibility, consent requirements, identity/source treatment, and any actions requiring authorization.

## 7. What must be built?

List the concrete implementation components required to make the feature real. Distinguish existing evidence from missing work.

## 8. Verification contract

Define source, contract, runtime, persistence, interaction, responsive, accessibility, visual, and release evidence required before the feature can be considered live.

## 9. Current state

State exactly what exists now, what is verified, what is not verified, and the current boundary of work.

## 10. Evidence

Link commits, files, tests, deployed URLs, runtime observations, or other durable proof. Never claim completion without evidence.

## 11. Activity

Record meaningful changes chronologically with date/time, actor, action, result, evidence, and next action.

## 12. Remaining work

List only real remaining work. Do not use generic TODOs.

## 13. Next authorized action

One concrete next action that moves the feature forward without exceeding its authority or scope.

## 14. Whole-system reconciliation

Before locking a change, confirm how it affects the parent Superbrain, shared event model, privacy boundaries, other parts, and release chain.
