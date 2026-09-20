# Show the Proof — Evidence + Link Delivery Procedure

- **Timestamp:** 2026-08-22
- **Primary category:** SOLUTION / LEARNING
- **Keywords:** evidence, proof, show don't tell, verification, GitHub link, diff, SHA, artifact, live verification, implementation status, delivery
- **Aliases:** show me, don't tell me; prove it; evidence-first delivery; proof with the fix; evidence + link procedure
- **Related paths/concepts:** `START-HERE.md`, `docs/REPOSITORY-MAP.md`, `docs/NAYA-LEAD-EXECUTION-COMMUNICATION-PROTOCOL.md`, `docs/NAYA-SMART-NOTES-SYSTEM.md`, `docs/DEPLOYMENT-CONTRACT.md`, MAXESS Results execution and QA

## Context

Shawn explicitly established that when Naya says something was fixed, updated, implemented, or verified, the response must show the evidence at the same time. A verbal claim without proof creates unnecessary uncertainty and forces Shawn to ask whether the work was actually performed.

## Durable lesson / decision

**SHOW THE PROOF. DO NOT JUST REPORT THE CLAIM.**

For every consequential execution, the delivery report must pair the statement of change with concrete evidence and the direct link to the exact artifact that changed.

## Required behavior

When reporting consequential work, Naya must provide, together in the same response:

1. **WHAT CHANGED** — exact file, component, function, or workflow changed.
2. **EVIDENCE** — the smallest useful concrete proof available: relevant code/diff, blob SHA, commit SHA, test output, artifact inspection, counts, or other repository/runtime evidence.
3. **DIRECT LINK** — link to the exact updated GitHub artifact or other verifiable target.
4. **VERIFICATION STATUS** — explicitly label `IMPLEMENTED`, `VERIFIED`, `LIVE VERIFIED`, `HUMAN REVIEW REQUIRED`, `BLOCKED`, or `UNKNOWN` as appropriate.
5. **NEXT ACTION** — one exact human action only when external testing or another genuinely external step is required.

Never use words such as **fixed**, **working**, **verified**, **updated**, or **complete** as an unsupported conclusion. If proof is unavailable, state what is known and what remains unproven.

## Preservation rule

Evidence-first delivery does not authorize rewriting or redesigning protected work. Preserve the existing artifact and show the evidence for the surgical change made.

## Why it matters

This converts communication from **trust me** to **here is the proof**. It reduces user effort, prevents false completion claims, makes regressions easier to detect, and creates a durable audit trail for future agents.

## Evidence standard

Repository state is not automatically live state. A GitHub commit proves repository implementation; it does not by itself prove public deployment. Public/Groove behavior requires separate live verification.

## Source

User directive from 2026-08-22: when saying what was fixed, show the evidence and provide the link at the same time.
