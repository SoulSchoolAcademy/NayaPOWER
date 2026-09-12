# NAYA POWER — DIRECT ACTIVITY EVENT / WRITE ARCHITECTURE V1

DATE: 2026-09-12
STATUS: CANONICAL WRITE ARCHITECTURE V1
NUMBER: 44

## PURPOSE
Make consequential Activity Feed records reliable by writing canonical events directly from the execution surface instead of depending on GitHub Actions as the default relay.

## 1. LAW

EXECUTION → DIRECT EVENT WRITE → PERSISTENCE → PROJECTION → VERIFICATION → CONTINUATION.

GitHub Actions may be a processor, validator, scheduled job, or evidence source. It is not the sole or default Activity Feed writer.

## 2. EVENT WRITE REQUIREMENTS

Every consequential write contains:
- stable event_id;
- event_type;
- actor;
- timestamp;
- source;
- mission/context;
- correlation/causation identifiers;
- payload/reference;
- authority/authorization context;
- verification state;
- privacy/publication state;
- idempotency key.

## 3. RELIABILITY

Writes must be idempotent. Failed delivery must be observable and retryable. The system must not display an action as recorded merely because an HTTP/UI request was attempted.

## 4. FEED PROJECTION

The write path creates canonical truth once. Activity, Personal, and Collective projections consume authorized events.

## 5. HUMAN/AI ACTIONS

Naya's direct execution surface must be able to write an Activity event immediately after a consequential action when authorized. This is the mechanism that prevents the no-orphan continuation from ending without a record.

## 6. GITHUB ACTIONS

Actions can consume or validate events and can generate evidence of repository operations. They must not be assumed to have successfully relayed Activity unless independently observed.

## 7. FAILURE

If direct write fails: preserve the action result, mark recording as FAILED/UNKNOWN as appropriate, expose the failure, and provide a retry/repair continuation. Never fabricate a feed receipt.

## 8. ACCEPTANCE

A real test action must create a canonical event without requiring a GitHub Action to run. The event must be retrievable and appear in Activity with its original identity and evidence state.
