# COMPUTATION EFFICIENCY MEASUREMENT CONTRACT — V1

## Purpose

Turn the NayaPOWER thesis — **accumulated verified intelligence should reduce repeated work** — into a measurable engineering property.

This contract measures **observable computation and resource use** first. It does not invent model-token, provider-cost, GPU, or dollar figures that the runtime cannot directly evidence.

## North-star metric

**Verified Responsible Value per Unit of Observable Computation**

A cheaper run is not an efficiency win if it produces a worse, unverified, unauthorized, or less trustworthy outcome.

## Paired experiment

### Cycle A — BASELINE / COLD RECONSTRUCTION
A fresh successor performs a frozen task without task-specific retained intelligence.

Measure:
- canonical source objects read
- source bytes/chars retrieved
- retrieval/search operations
- duplicate context objects
- tool/API calls
- model calls, only if directly observable
- tokens, only if directly observable
- wall-clock latency
- human intervention/time
- retries
- verification operations
- verified outcome

### Cycle B — COMPOUNDING / RETAINED INTELLIGENCE
The identical frozen task is executed using intelligence retained from Cycle A.

Measure the same fields plus:
- retained intelligence objects used
- exact learning IDs retrieved
- computation explicitly avoided
- verification evidence reused
- successor context reused

## Counterfactual rules

An avoided-computation claim is valid only when:
1. the task is frozen;
2. Cycle A actually performed the work claimed as avoided;
3. Cycle B retrieved a durable, provenance-bound intelligence object;
4. Cycle B used that object before the avoided work;
5. the resulting outcome is independently verified;
6. no authority boundary was bypassed;
7. no quality regression occurred.

Do not claim model-token/provider/GPU/dollar savings unless directly measured.

## Primary measurements

- `baseline_units`
- `compounding_units`
- `avoided_units = baseline_units - compounding_units`
- `context_objects`
- `context_bytes`
- `retrieval_calls`
- `search_calls`
- `tool_calls`
- `model_calls`
- `tokens`
- `wall_time_ms`
- `human_time_ms`
- `retries`
- `verification_calls`

Each resource is reported independently. Unlike units are never collapsed into a fabricated single number.

## Evidence states

- **MEASURED** — direct runtime evidence exists.
- **DERIVED** — arithmetic from measured evidence.
- **COUNTERFACTUAL** — baseline-supported avoided work.
- **UNKNOWN** — instrumentation unavailable.
- **NOT_CLAIMED** — deliberately not asserted.

## Required proof object

`NAYANET_COMPUTATION_EFFICIENCY_PROOF_V1`

It must contain:
- frozen task hash
- baseline trace/receipt
- compounding trace/receipt
- retained learning IDs
- resource measurements
- avoided-work calculations
- outcome comparison
- authority comparison
- provenance
- verification evidence
- source HEAD
- workflow run
- one successor action

## Acceptance

The first production benchmark passes when it proves, for at least one controlled paired task:

1. baseline and compounding cycles are the same task;
2. Cycle B consumes retained verified intelligence;
3. at least one repeated computation is demonstrably avoided;
4. the avoided computation is directly measured;
5. verified outcome quality is preserved or improved;
6. authority, privacy, and provenance are preserved;
7. the result is durably recorded;
8. a cold successor can retrieve the result and know the next action.

## What this does not claim

This does not establish universal computation savings across all models, providers, prompts, humans, or projects.

The first goal is a **real, reproducible, bounded engineering measurement**.

> **Measure the work we can actually observe. Never manufacture precision where instrumentation is missing.**
