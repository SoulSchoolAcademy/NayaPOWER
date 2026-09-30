# NayaNET Channel Contract V1

**Status:** PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED

## Purpose

The Channel Contract defines how external interfaces (Hub, API, NayaNET, MCP, webhooks, A2A, SDKs) connect to the canonical brain. **One Brain. Many Doors.** Every channel enters the same governed sequence.

## Scope

- Channel identification and authentication
- Authorization and consent verification
- Canonical capability exposure
- Action execution through governed kernel
- Receipt, verification, and learning capture

Out of scope: independent intelligence storage, authority creation, truth determination.

## Key Rules

1. Every channel enters the same governed sequence: `CHANNEL → IDENTIFY → AUTHENTICATE → AUTHORIZE → GOVERN → CANONICAL CAPABILITY → ACTION → RECEIPT → VERIFY → LEARN`.
2. Channels are projections/connectors, not independent intelligence authorities.
3. No channel may bypass the kernel governance sequence.
4. All channel actions produce receipts and are subject to verification.
5. Channel-specific UI never becomes canonical state.
6. Authorization is per-channel, per-action, and time-bounded.

## Input/Output

| Direction | Content |
|---|---|
| Input | Channel requests, credentials, action parameters, context |
| Output | Governed responses, receipts, verification results, learning captures |

## Acceptance Criteria

- All channels pass through the full governance sequence.
- No channel can act without authorization.
- Receipts are produced for every action.
- Channel projections are clearly marked as projections.
- Verification and learning capture occur for all channel actions.

## Failure States

| Failure | Behavior |
|---|---|
| Authentication failure | Deny; log; do not retry automatically |
| Authorization failure | Deny; emit explicit reason |
| Governance sequence violation | Halt; alert; preserve evidence |
| Channel projection divergence | Mark as PROJECTION; do not promote |
| Receipt generation failure | Mark action as UNVERIFIED |
