# Verified AI Action Contract

**Status:** V1 — derived from the proven Causal Verification Object.

## Purpose

A Verified AI Action is the reusable operational contract for an AI action that can be traced from human intent through authority, permission, execution, observation, evidence, independent verification, result, receipt, and learning.

It does **not** create a new persistence layer. Existing execution receipts, cognition events, evidence, verification receipts, Smart Ledger records, and learning records remain authoritative.

## Contract

`INTENT → AUTHORITY → PERMISSION → ACTION → OBSERVATION → EVIDENCE → VERIFICATION → RESULT → RECEIPT → LEARNING`

### Required proof

An action may be labeled **VERIFIED** only when all of these are present:

1. Intent: action + expected result.
2. Authority: authenticated/authorized authority status plus authority grant.
3. Permission: scope sufficient for the action.
4. Action: concrete executed action.
5. Observation: actual observed result.
6. Evidence: one or more evidence references.
7. Independent verification: verification state is `OUTCOME_VERIFIED`.
8. Result: execution status is `SUCCESS`.
9. Receipt: existing execution receipt is identified.
10. Learning: learning references may be empty, but the contract preserves them when present.

Any missing proof becomes an explicit causal gap. The contract never upgrades an action to VERIFIED by inference.

## Statuses

- `VERIFIED` — every required proof condition is satisfied.
- `PARTIAL` — execution exists, but causal proof is incomplete.
- `BLOCKED` — execution was blocked.
- `REJECTED` — reserved for an explicitly rejected action/result.

## Architecture rule

**One action, one existing execution receipt, one causal verification view.**

The Verified AI Action contract is a generalized interface over existing NayaPOWER truth sources. It is not another database, ledger, event stream, or parallel receipt system.

## Universalization rule

Every future NayaPOWER action surface should be able to produce or reference this same chain, regardless of action type: Smart Mail, Smart Notes, Hub actions, learning promotion, sharing, external-agent actions, or future capabilities.

The action-specific implementation may vary. The proof contract does not.
