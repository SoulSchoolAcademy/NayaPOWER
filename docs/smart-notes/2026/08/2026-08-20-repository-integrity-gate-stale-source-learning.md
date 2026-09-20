# Repository Integrity Gate Stale Source — CI Must Follow Current Authority

- Timestamp: 2026-08-20 20:15 PDT
- Last Updated: 2026-08-20 20:15 PDT
- Category: PROBLEM
- Status: RESOLVED
- Scope: TECHNICAL
- Keywords: CI, GitHub Actions, repository integrity, stale gate, source authority, Smart Notes, BASELINE-WORKING, legacy source, verification, guardrail
- Aliases: stale CI gate, obsolete source check, integrity workflow drift, verification gate mismatch
- Related: `.github/workflows/repository-integrity.yml`, `docs/SOURCE-AND-MEMORY-MAP.md`, `docs/NAYA-GOVERNANCE-REGISTRY.md`, `docs/NAYA-SMART-NOTES-SYSTEM.md`, PR #8

## Context

PR #8's repository integrity workflow failed before reaching AIScore-specific QA. Investigation showed the workflow was checking for a legacy Results source file named `20260817 912am RESULTS PAGE CODE` that is not present in the current repository state and is not identified as the current source authority by the current source/memory map.

The same workflow also contained an older Smart Notes integrity contract that expected root-level daily note files and an index phrase that are inconsistent with the current canonical `docs/NAYA-SMART-NOTES-SYSTEM.md` and nested `docs/smart-notes/YYYY/MM/` convention.

## What We Learned / Decided

A CI gate is itself part of the project's verification architecture and must be governed by current source-of-truth rules.

If the gate encodes historical paths or schemas that no longer represent the canonical system, it becomes a false failure detector and blocks valid work without proving a real product defect.

The correct repair is not to add obsolete files merely to satisfy CI. The correct repair is:

**IDENTIFY CURRENT AUTHORITY → CLASSIFY STALE CHECK → UPDATE GATE → VERIFY NEW GATE**

The current repository map identifies `BASELINE-WORKING.html` as a current working source artifact and `docs/NAYA-SMART-NOTES-SYSTEM.md` plus `docs/smart-notes/INDEX.md` as the durable memory system.

## Why It Matters

Verification is only useful when it verifies the current system. Stale tests can create false failures, encourage destructive compatibility shims, and hide the actual quality work behind infrastructure noise.

This is a direct application of the Naya Law failure loop:

**FAILURE → ROOT CAUSE → REPAIR → VERIFICATION → SAFEGUARD**

## Required Behavior

When a repository gate fails:

1. inspect the exact failing step;
2. determine whether the failure is in product code, test logic, governance drift, or deployment state;
3. compare the gate against the canonical authority map;
4. never add obsolete artifacts solely to make a stale test pass;
5. repair the gate when it is demonstrably stale;
6. record the learning;
7. rerun the gate and verify that the repaired gate now checks the intended current system.

## Evidence / Source

GitHub Actions run `32442701495` for PR #8 failed in `Repository identity and map gate`. The workflow explicitly referenced the absent legacy file `20260817 912am RESULTS PAGE CODE`. Current `docs/SOURCE-AND-MEMORY-MAP.md` and `docs/NAYA-GOVERNANCE-REGISTRY.md` define current authority and historical-reference rules. The repair was applied to `.github/workflows/repository-integrity.yml` on `feat/aiscore-clean-v1` in commit `d1d1516`.

## Follow-up

Confirm the repaired workflow passes. If a future gate fails, classify the failure before changing product code.
