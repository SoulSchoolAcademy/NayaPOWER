# Execution Evidence + Exact-Link Delivery Law

**Timestamp:** 2026-08-22
**Primary category:** SOLUTION / LEARNING
**Keywords:** execution, evidence, exact link, changed artifact, commit, verification, live verification, delivery, proof, show not tell, MAXESS, GitHub-first
**Aliases:** show me the work, prove it, evidence package, exact artifact link, no-story delivery, completion proof

## Context

During MAXESS/AIScore execution, the assistant repeatedly reported or implied that work was fixed while providing a workflow link, a source/reference link, or an explanation instead of the exact updated artifact and proof that the artifact had changed and worked.

This created repeated user friction and, more importantly, blurred the distinction between implementation, source verification, and live verification.

## Durable lesson / decision

For every consequential execution, the exact changed artifact link is part of the deliverable. A workflow link is not a substitute for the changed artifact. A GitHub commit is not proof of live deployment. A statement that something was fixed is not evidence.

## Required behavior

Use this sequence:

**DO THE WORK → REFETCH THE ACTUAL ARTIFACT → DIFF / VERIFY THE CHANGE → VERIFY RUNTIME WHEN AVAILABLE → VERIFY LIVE WHEN AVAILABLE → SEND THE EXACT ARTIFACT LINK + COMMIT EVIDENCE + VERIFICATION STATUS.**

Do not say `fixed`, `working`, `complete`, or `ready to test` unless the corresponding evidence exists.

When evidence is incomplete, use explicit status:

- IMPLEMENTED
- SOURCE VERIFIED
- RUNTIME VERIFIED
- LIVE VERIFIED
- HUMAN REVIEW REQUIRED
- UNKNOWN

For MAXESS/AIScore specifically, the priority order is:

1. **Functionality and accurate score/result transport** — North Star.
2. Complete results page rendering: E01 → E02 → E03 → E04 and subsequent authorized sections.
3. Accurate propagation of `window.MAXESS_RESULT` / `MAXESS_RESULT_V1` data.
4. Only after functionality is proven: cosmetic refinements such as Naya welcome wording, typography, image sizing, and color.

## Guardrail

Never deliver only a workflow link when the user asked for the updated artifact. Always provide the exact changed file link. If the live page has not been verified, say so plainly and do not send a live URL as though it were proven fixed.

## Evidence source

Repository governance explicitly requires GitHub-first execution, refetch/diff/QA, and explicit verification states. `README.md`, `START-HERE.md`, and `docs/DEPLOYMENT-CONTRACT.md` are the governing evidence.
