# ✅ Truth, State & Interaction Law V1

## 1. Prime law

**Every state tells the truth. Every action has a consequence. Every important consequence can be observed.**

UI state is a claim.

Claims require reality behind them.

## 2. Canonical room/object states

- LOADING
- EMPTY
- READY
- BLOCKED
- NOT_VERIFIED
- VERIFIED
- ERROR

Additional object-specific states may exist, but must map into the truth model.

## 3. State semantics

### LOADING
A real request/process is in progress.

### EMPTY
The system successfully knows there is no applicable content.

### READY
Capability/content is available.

### BLOCKED
Known requirement prevents continuation.

### NOT_VERIFIED
Information exists but proof/current verification is insufficient.

### VERIFIED
Applicable evidence supports the state within a defined scope.

### ERROR
An attempted operation failed or system state cannot be resolved normally.

UNKNOWN should remain explicit when needed. It must never silently become EMPTY or VERIFIED.

## 4. Connection state

Never show CONNECTED because:
- a config value exists;
- the UI was rendered;
- a service was once connected.

CONNECTED requires current applicable backend evidence.

## 5. Action state machine

A consequential control should model:

`IDLE → INTENT → AUTHORITY/SCOPE CHECK → EXECUTING → OBSERVED → VERIFIED/NOT_VERIFIED/ERROR → CONTINUITY`

The user may not need to see every internal state, but the system must not skip them conceptually.

## 6. Optimistic UI

Optimistic updates may be used for reversible low-risk interactions.

Do not optimistically claim:
- sharing complete;
- permission granted;
- money/value transferred;
- verified;
- connected;
- deployed;
- saved permanently;
unless the system can reconcile and correct the state quickly and safely.

## 7. Confirmation

Confirm high-consequence actions when:
- destructive;
- public;
- privacy-changing;
- authority-changing;
- hard to reverse.

Avoid confirmation fatigue for trivial actions.

## 8. Receipts

Where important, success should expose:
- what happened;
- when;
- object;
- scope;
- result;
- evidence/receipt link.

Human-readable first. Machine detail available second.

## 9. Error recovery

Errors should answer:
- what failed;
- whether anything changed;
- what the user can do;
- whether retry is safe.

Never use generic "Something went wrong" when the system knows more.

## 10. Acceptance

A UI surface fails if:
- colors imply false success;
- loading continues after failure;
- a dead button looks active;
- VERIFIED lacks evidence;
- empty hides an error;
- one user's state is rendered as another's;
- actions have no observable consequence.
