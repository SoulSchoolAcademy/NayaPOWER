# Naya Power Execution Plan — PROVE → INTEGRATE → LEARN → ACTIVATE

Date: 2026-08-29
Status: ACTIVE EXECUTION PLAN
Authority: operational continuation of `SN-20260829-PROVE-INTEGRATE-LEARN-ACTIVATE-RUNTIME-GATE.md`

## Objective

Stop adding foundational architecture. Prove the existing Naya Power Superbrain in reality, repair only evidence-backed failures, then activate it with real humans.

## Canonical order

### P0-1 — Authoritative runtime execution

**Goal:** obtain one repository-runtime execution that exposes real command, stdout/stderr, exit status, and exact HEAD.

**Run:** canonical `.github/workflows/superbrain-gate.yml` on the exact live `main` HEAD.

**Evidence required:** workflow run, exact HEAD, executed steps, first failing command if any, and machine-readable failure receipt when applicable.

**Rule:** if the runner dies before steps execute, classify as execution-environment UNKNOWN and do not modify application code.

**Status:** BLOCKED BY CURRENT EXECUTION SURFACE — GitHub jobs have previously failed with no exposed steps/logs; local checkout is unavailable in the current environment.

### P0-2 — Close Torch 9 with runtime evidence

**Goal:** run `.naya/runtime/customer_activation_loop_test.py` in the repository runtime with `PYTHONPATH=.naya/runtime`.

**Evidence required:** exit 0 and exact stdout on the exact HEAD.

**Status:** ISOLATED PASS; repository-runtime proof pending.

### P0-3 — Full Superbrain Gate

**Goal:** run the complete canonical gate on the same exact HEAD after P0-2 evidence exists.

**Evidence required:** all canonical gate steps pass, continuity receipt exists, and exact HEAD matches the tested source.

**Status:** PENDING P0-1/P0-2.

### P0-4 — First-failure repair only

**Goal:** repair the first concrete failure exposed by P0-1/P0-2/P0-3.

**Rule:** smallest true boundary repair; no weakened tests, bypasses, duplicated authority, speculative cleanup, or architecture expansion.

**Status:** WAITING FOR RUNTIME EVIDENCE.

### P0-5 — Actual Naya governance behavior

**Goal:** evaluate actual Naya/model outputs against six behaviors:

1. obey/act
2. warn/inform
3. challenge
4. recommend
5. confirm
6. refuse

**Evidence required:** real model outputs, evaluator results, rationale, and failures if any.

**Status:** benchmark harness exists; actual-model proof pending.

### P0-6 — One measurable compounding loop

**Goal:** prove Experience → Learning → durable intelligence → changed future behavior.

**Minimum experiment:** baseline task, capture outcome, produce validated learning, apply learning to successor run, measure improvement.

**Evidence required:** before/after task results and explicit causal link to the promoted learning.

**Status:** architecture exists; end-to-end measured proof pending.

### P0-7 — Customer activation verification

**Goal:** prove the real activation path from customer knowledge intake through canonical intelligence and qualified mission into execution continuity.

**Evidence required:** valid activation input, canonical event provenance, qualified mission, priority, torch, and successor-ready state.

**Status:** boundary implemented/isolated; real activation proof pending.

### P1-8 — Activation documents

Create only after P0-1 through P0-7 are evidenced sufficiently for activation.

**Required outputs:** minimal customer activation package, operator/agent activation path, and cold-start continuation instructions derived from canonical repository authority.

**Status:** NOT STARTED — intentionally downstream.

### P1-9 — First humans

Put the first controlled users through the activation flow.

**Measure:** time-to-value, successful outcome rate, human effort saved, trust/clarity, failures, useful learning captured, and successor continuity.

**Status:** NOT STARTED — intentionally downstream.

### P1-10 — Measure and compound

Review actual human outcomes and operational evidence; convert validated findings into Smart Notes/CIS changes only when they demonstrably improve future behavior.

**Status:** NOT STARTED — intentionally downstream.

## Current execution rule

Start at P0-1 and proceed downward without waiting for another human instruction. When a step is blocked, perform every non-blocked verification or preparation that can be completed without pretending the blocked evidence exists. Return to the blocked step as soon as authoritative execution becomes available.

## Definition of activation-ready

Naya Power is activation-ready when the system can restore authoritative state, understand the human mission, prioritize, hand off an executable torch, execute, verify, learn, compound, demonstrate the six governance behaviors, and provide reproducible successor continuity — with runtime evidence rather than source inspection alone.

## Non-negotiables

- Reality is the judge.
- Evidence outranks assumptions.
- Exact HEAD matters.
- Repair only the first concrete failure.
- Do not weaken gates.
- Do not create parallel authority.
- Do not claim runtime GREEN without runtime evidence.
- Do not wait for the human to name the next obvious executable step.
