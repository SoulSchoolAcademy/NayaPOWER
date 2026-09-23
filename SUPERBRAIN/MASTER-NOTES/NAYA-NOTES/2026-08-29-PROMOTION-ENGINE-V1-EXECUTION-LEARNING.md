# 🔱 NAYA NOTE — PROMOTION ENGINE V1 EXECUTION LEARNING

**Date:** 2026-08-29  
**Scope:** NayaPOWER × MAXIS  
**Status:** ACTIVE / VERIFICATION BLOCKED

## DURABLE LESSON

A Promotion Engine is not operational merely because its schema, runner, workflow, and artifacts exist. The system must execute the acceptance path and produce evidence.

## IMPORTANT DISCOVERY

The current GitHub Actions Promotion Engine run and its retry were created successfully but failed before any executable workflow step was exposed. Job metadata showed `runner_id=0`, empty `runner_name`, and `steps=[]`. The available log endpoint returned no usable job log.

Therefore the correct conclusion is:

**CI execution environment is UNKNOWN/BLOCKED. The promotion code has not been proven to fail.**

## SYSTEM CHANGE

The Promotion Engine was strengthened to:

- validate canonical events;
- fingerprint and deduplicate prior learning;
- classify durable homes;
- separate authority-gated destinations from auto-promotable destinations;
- create deterministic Naya/Shawn notes;
- publish event-specific Intelligence Feed entries;
- update the Primary Intelligence Hub;
- produce auditable promotion receipts;
- preserve the distinction between implementation and verification.

The CI workflow was strengthened to run acceptance tests before promotion and persist the complete generated state.

## SUCCESSOR RULE

When CI fails before any step executes, **do not modify application code based on speculation**. First obtain executable runner evidence. The absence of step-level evidence is itself an important state and must be preserved.

## PROOF TARGET

**EVENT → VALIDATE → DEDUP → CLASSIFY → AUTHORIZATION → PROMOTE → RECEIPTS → VERIFY → FEED → HUB → SUCCESSOR RESTORE**

## CURRENT NEXT ACTION

Obtain a fresh normal runner execution. If it starts, fix the first proven defect and rerun. If it fails before steps again, escalate the runner/platform blocker rather than fabricating a code diagnosis.

## COMPOUNDING LESSON

**Evidence quality is itself part of intelligence quality.** A system that refuses to turn an unexplained failure into a false lesson is behaving correctly.
