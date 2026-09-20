# AIScore Execution Branch Guardrail — Consequential Writes Must Name the Active Branch

- Timestamp: 2026-08-20 20:15 PDT
- Last Updated: 2026-08-20 20:15 PDT
- Category: LEARNING
- Status: ACTIVE
- Scope: TECHNICAL
- Keywords: AIScore, GitHub, branch safety, active branch, main branch, feature branch, execution guardrail, source of truth, Naya Law, PR #8, branch drift
- Aliases: branch guardrail, wrong-branch write, main branch mistake, feature branch protection, GitHub execution safety
- Related: `.naya/NAYA-LAW-SYSTEM-PROTOCOL.md`, `START-HERE.md`, `docs/NAYA-SMART-NOTES-SYSTEM.md`, `docs/DEPLOYMENT-CONTRACT.md`, PR #8

## Context

During MAXESS AIScore CLEAN V1 execution, a consequential file-creation attempt initially omitted the explicit branch argument and targeted the repository default branch. The issue was detected before the AIScore implementation was allowed to proceed on the wrong branch. The temporary artifacts were removed from `main`, and the actual AIScore work continued on `feat/aiscore-clean-v1`.

## What We Learned / Decided

A repository operation can be syntactically valid and still be operationally wrong if the target branch is not explicit.

For MAXESS/Naya work, the active engineering branch is part of the execution state and must be treated as a protected parameter, not an implicit default.

Required sequence before consequential GitHub writes:

**REPOSITORY → GOVERNANCE BRANCH → ACTIVE ENGINEERING BRANCH → AUTHORITATIVE ARTIFACT → WRITE**

Never rely on a tool default branch when the task explicitly names an engineering branch.

## Why It Matters

A wrong-branch write creates source confusion, can contaminate governance/reference history, and makes later verification less trustworthy. Catching the mistake is good; designing the workflow so it is harder to make is better.

This is a concrete example of the Naya Law principle:

**FAILURE → ROOT CAUSE → REPAIR → VERIFICATION → SAFEGUARD**

## Required Behavior

Before every consequential GitHub write:

1. identify the exact repository;
2. identify `main` as governance/reference branch when applicable;
3. identify the requested active engineering branch;
4. verify the branch exists;
5. pass the active branch explicitly to the write operation;
6. verify the resulting commit branch and changed path immediately;
7. never assume a successful GitHub API response means the write landed in the intended branch.

If a write lands on the wrong branch, classify it as a **WRONG SOURCE / BRANCH SAFETY FAILURE**, stop normal progression, remove or repair the unintended change safely, verify the affected branch, and record the learning.

## Evidence / Source

Observed during the 2026-08-20 MAXESS AIScore CLEAN V1 execution cycle. The repository operating laws already require GitHub-first inspection, branch identification, preservation, verification, and durable learning; this note records the concrete failure mode and its reusable safeguard.

## Follow-up

Continue using explicit branch parameters for all consequential GitHub writes and retain this learning as a recurring pre-write guardrail.
