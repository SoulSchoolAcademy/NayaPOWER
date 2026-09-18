# Smart Note — Mission State + Runtime Gates + Evidence + Handoff Enforcement

**ID:** SN-20260828-MISSION-STATE-RUNTIME-GATES-EVIDENCE-HANDOFF
**DATE:** 2026-08-28
**STATUS:** CANONICAL SMART NOTE / ADOPTION REQUIRED
**SOURCE:** Naya operating review with Shawn
**PROJECT:** Naya Power / Superbrain

## Executive Lesson

The Superbrain already contains laws, continuity guidance, evidence requirements, mission-state concepts, and handoff concepts. The failure mode is that these can remain descriptive rather than becoming mandatory runtime gates.

A future Naya can read a large body of correct documentation and still fail to execute the intended continuity protocol if the runtime does not require the behavior before allowing substantive work to proceed.

## Problem Observed

Repeated future-Naya executions have sometimes failed to reliably:

- restore the current mission state before acting;
- understand what the previous Naya actually completed;
- distinguish verified state from assumptions;
- record what was done and what remains;
- preserve evidence for consequential claims;
- produce a useful next-execution handoff;
- prevent the next Naya from starting from a stale or reconstructed understanding.

The core diagnosis is:

> **Documentation is not enforcement. A law that can be skipped is guidance, not a runtime control.**

## Required Runtime Model

Every substantive Naya execution must operate through this minimum continuity contract:

**READ MISSION STATE → ESTABLISH CURRENT STATE → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE MISSION STATE → PRODUCE HANDOFF → PASS RUNTIME GATES**

The next Naya must consume the resulting mission state and handoff before substantive execution.

## Mission State — Required

Mission State becomes a first-class machine-readable runtime artifact containing, at minimum:

- mission / goal;
- desired state;
- success criteria;
- current verified state;
- unknowns;
- protected boundaries;
- active scope;
- current task/list;
- completed work;
- incomplete work;
- blockers/problems;
- decisions;
- assumptions;
- risks;
- evidence records;
- artifacts/commits/receipts;
- next best action;
- next execution handoff;
- timestamp/version/provenance.

## Runtime Gates — Required

A substantive execution is **NOT COMPLETE** unless the required gates pass.

### Gate 1 — START / RESTORE

- Mission State was located and read.
- Relevant authoritative source was identified.
- Current state was established.
- Protected / replaceable / unknown boundaries were identified.

### Gate 2 — EXECUTION

- The actual objective was executed rather than merely described.
- Material changes and decisions were recorded.

### Gate 3 — EVIDENCE

- Consequential claims have traceable evidence.
- Evidence tier reflects what was actually observed.
- Unknown or unverified items remain explicitly marked.

### Gate 4 — STATE UPDATE

- Mission State was updated with the new verified state.
- Completed, remaining, blocked, and changed items are recorded.

### Gate 5 — HANDOFF

- The next Naya receives a concise, actionable continuation state.
- The handoff identifies exactly what was done, what failed, what remains, why it matters, and the recommended next action.

### Gate 6 — COMPLETION

- All required gates pass.
- A durable receipt/evidence record exists where applicable.
- Only then may the execution be reported as complete.

## Failure Rule

If a required gate cannot pass:

> **DO NOT CLAIM COMPLETION.**

Record the failed gate, preserve the evidence, update Mission State, and create a recovery/next-execution handoff.

## Architectural Principle

This is the transition from a **constitution-heavy system** to an **executable operating system**:

**LAW → MACHINE-READABLE STATE → RUNTIME GATE → OBSERVED RESULT → RECEIPT → NEXT STATE**

The objective is not more documentation. The objective is reliable behavior across model/session boundaries.

## Adoption Decision

Adopt Mission State, Runtime Gates, Evidence Claims, and Handoffs as mandatory requirements for every substantive Naya/Superbrain execution.

Update the canonical Runtime Constitution and Smart Brain Operating System so this requirement is part of the operating contract, not merely a Smart Note.

## Verification Target

This Smart Note is considered adopted only when:

1. the note exists in canonical MASTER-NOTES;
2. the Runtime Constitution explicitly requires Mission State restoration and completion gates;
3. the Smart Brain Operating System explicitly requires the same;
4. future execution prompts can point to these canonical requirements without relying on conversational memory;
5. runtime implementation later demonstrates that gates actually block premature completion.
