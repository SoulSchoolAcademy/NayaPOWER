# Complete Artifact Delivery + Batching Law

- Timestamp: 2026-08-20 (exact execution time unavailable)
- Category: SOLUTION
- Status: ACTIVE
- Scope: PROJECT / TECHNICAL
- Keywords: complete artifact, full code, no snippets, no partial code, batching, GitHub raw link, source of truth, preserve artifact, large artifact, Groove embed, delivery
- Aliases: Complete Artifact Law, full artifact law, no-snippet law, raw-link delivery, batch-and-integrate, complete-code delivery
- Related: `NAYA-OS.md`, `docs/NAYA-NITRO-MODE.md`, `START-HERE.md`, `E06 CODE 2200`

## Context

A repeated execution failure occurred around large MAXESS/Groove artifacts. Partial snippets or truncated chat output are not an acceptable delivery mechanism for a complete artifact. The intended workflow is to edit the complete artifact in GitHub and deliver the resulting GitHub raw link so the user can access the real file without copying fragments from chat.

## What We Learned / Decided

1. When Shawn asks for code, the artifact must be treated as a complete artifact, not a snippet.
2. Never send partial code, abbreviated code, diffs, replacement blocks, or reconstructed approximations as if they were the finished artifact.
3. For large artifacts, use batching internally when the tooling requires it, then integrate the batches into the complete artifact before delivery.
4. Preserve the existing complete artifact while editing; do not solve a tooling limitation by deleting or replacing it with a tiny excerpt.
5. The canonical delivery mechanism for a large completed artifact is the actual file in `SoulSchoolAcademy/MaxRESULTS`, with a GitHub raw link returned to Shawn.
6. A raw link is a delivery mechanism, not a substitute for actually creating and verifying the complete artifact in GitHub.
7. If a technical limitation appears, the required behavior is to find a workable solution—batch, integrate, verify, and continue—not to use the limitation as the stopping point.
8. Do not require Shawn to repeat an activation phrase on every message when the governing project execution state is already active. Existing activation commands remain valid triggers, but Naya must maintain continuity within an active execution cycle.

## Why It Matters

The user's time, working artifact, and trust are protected only when the complete source remains intact and the delivered artifact is the real artifact. Partial-code delivery can cause accidental overwrites, lost work, regressions, and false confidence about what was actually implemented.

## Required Behavior

For every large MAXESS code task:

**GITHUB FIRST → FETCH COMPLETE SOURCE → BASELINE/PRESERVE → PLAN COMPLETE CHANGE → BATCH WHEN NECESSARY → INTEGRATE INTO ONE COMPLETE ARTIFACT → WRITE TO GITHUB → REFETCH/VERIFY → CONFIRM COMPLETENESS → RETURN RAW GITHUB LINK.**

If a tool truncates displayed output, do not infer that the stored artifact is truncated. Verify the actual GitHub file through available repository evidence. If the write interface requires complete replacement content, provide complete content to that write operation; never write a snippet into the production artifact.

## Evidence / Source

Human requirement established in the 2026-08-20 MAXESS execution conversation; repository governance confirms GitHub-first execution, preservation, coherent batching, verification, and failure-to-guardrail learning in `NAYA-OS.md`, `START-HERE.md`, and `docs/NAYA-SMART-NOTES-SYSTEM.md`.

## Follow-up

Promote this durable rule into the canonical Naya operating law and use it for E06 and all future large-artifact MAXESS work.
