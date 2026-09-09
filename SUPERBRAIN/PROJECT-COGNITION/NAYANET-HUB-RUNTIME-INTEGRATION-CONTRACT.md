# NayaNET Intelligent Hub — Persistent Cognition Runtime Integration Contract

**Version:** 1.0  
**Status:** CANONICAL / ACTIVE / IMPLEMENTATION REQUIRED  
**Authority:** Naya Persistent Cognitive Execution Protocol  
**Project:** NayaNET Intelligent Hub

## Objective

Turn the persistent project cognition state from documentation into a real runtime capability without creating a competing source of truth.

## Runtime lifecycle

```text
NAYA ENTERS
  ↓
LOAD PROJECT COGNITION
  ↓
RESTORE CURRENT VERIFIED STATE
  ↓
RUN COGNITIVE GATE
  ↓
SELECT ONE HIGHEST-VALUE NEXT ACTION
  ↓
EXECUTE
  ↓
OBSERVE ACTUAL RESULT
  ↓
ATTACH EVIDENCE / RECEIPT
  ↓
RECONCILE STATE
  ↓
CAPTURE LEARNING
  ↓
WRITE VERSIONED STATE
  ↓
GENERATE TORCH-PASS
  ↓
NAYA EXITS
```

## Hard requirements

1. **Persistent:** state survives model/session changes.
2. **Versioned:** every material mutation has revision, actor, timestamp, and event identity.
3. **Auditable:** state changes link to execution events and evidence.
4. **Conflict-safe:** stale revisions cannot overwrite newer state silently.
5. **Evidence-bound:** confidence is never treated as proof.
6. **Current-truth aware:** current verified state outranks historical narrative.
7. **Protected:** approved Hub functionality/design remains protected unless explicitly authorized to change.
8. **Recoverable:** interrupted execution resumes from the latest durable checkpoint.
9. **Human-readable:** the user can see useful operational state without private chain-of-thought disclosure.
10. **Successor-ready:** the next Naya receives a concrete, executable handoff.

## Source-of-truth boundary

The cognition state is an **operational coordination layer**, not the authoritative home of product truth. Code, deployment state, tests, receipts, canonical architecture, and project state remain authoritative according to the NayaPOWER authority hierarchy.

The runtime must reconcile cognition against those authorities before consequential action.

## Minimum API/service behavior

### `loadCognition(projectId)`
Returns the newest valid project cognition revision.

### `beginExecution(projectId, actor)`
Creates an execution context and snapshots the starting revision.

### `updateCognition(projectId, patch, expectedRevision)`
Applies a validated state transition only when the expected revision matches current state. Otherwise return a conflict and require reconciliation.

### `recordEvidence(projectId, evidence)`
Stores or references evidence supporting an observed result.

### `completeExecution(projectId, result)`
Records observed reality, evidence, learning, and resulting state transition.

### `createHandoff(projectId)`
Produces a ready-to-run successor instruction from durable state.

## Atomicity rule

The state update and its execution receipt should be committed as one logical transition where the persistence technology permits it. If atomicity is impossible, the system must expose the incomplete state rather than presenting it as complete.

## Concurrency rule

Use optimistic concurrency/version checks. A Naya must never silently replace a newer Naya's work.

## Failure rule

If execution fails:

**STOP → RECORD FAILURE → PRESERVE KNOWN-GOOD → UPDATE UNKNOWN/FAILED STATE → CAPTURE LEARNING → DEFINE NEXT ACTION → HANDOFF.**

## AAA acceptance test

Runtime integration is complete only when an independent test demonstrates:

- Naya A loads state.
- Naya A performs an action.
- The result is observed and evidenced.
- State revision increments.
- Naya A exits with a handoff.
- Naya B enters without conversation history.
- Naya B restores the same durable state.
- Naya B knows the prior result, evidence, remaining work, and exact next action.
- A stale Naya cannot overwrite Naya B's newer revision.
- The exact live Hub runtime reflects the persisted state.

**Documentation is not runtime proof. This contract remains OPEN until the above behavior is tested at the exact runtime.**
