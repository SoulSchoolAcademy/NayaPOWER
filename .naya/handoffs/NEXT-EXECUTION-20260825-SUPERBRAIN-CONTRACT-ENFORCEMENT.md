# NEXT EXECUTION — CLOSE AND VERIFY THE CANONICAL SUCCESSOR GATE

schema_version: 7
status: READY

## Project
Naya Power Superbrain (`PRJ-NAYAPOWER-SUPERBRAIN`)

## North Star
A user should be able to give Naya knowledge—not configure infrastructure—and Naya should turn that knowledge into a verified, recoverable, high-recall personal Superbrain automatically.

## Current state
The GitHub-native Superbrain baseline has deterministic retrieval, canonical memory, provenance, continuity, cold-start, CIS, and project/prompt contracts. The canonical NEXT-EXECUTION behavioral gate is now implemented in the authoritative project execution validator and wired into continuity enforcement. The remaining work is authoritative CI verification of this exact tree and resolution of any first real failure without weakening the contract.

## Completed work
- Hardened deterministic retrieval admission so relevance is required before authority and recency ranking.
- Added authoritative canonical NEXT-EXECUTION semantic validation.
- Added deterministic artifact loading and independent successor consumption.
- Added rejection of arbitrary, missing, malformed, incomplete, and conversation-dependent successors.
- Added a hard continuity requirement for canonical successors on meaningful COMPLETED executions.
- Added deliberate orphan coverage for a completion that contains an unusable ready-to-run string.
- Added project, continuation, Prompt Architect, behavioral-matrix, and independent-consumption regression coverage.

## Verified evidence
- The canonical successor is stored durably at `.naya/handoffs/NEXT-EXECUTION-20260825-SUPERBRAIN-CONTRACT-ENFORCEMENT.md`.
- The project execution validator defines the 12 semantic successor fields and deterministic loading/consumption functions.
- Continuity enforcement calls the authoritative successor validator for COMPLETED meaningful executions.
- Prompt Architect delegates successor validation to the authoritative project contract.
- The repository Superbrain Gate includes compilation, continuation, project/prompt, cold-start, intelligence, activation, health, and receipt stages.

## Unresolved issues
- The authoritative GitHub Superbrain Gate must still execute against the resulting exact main HEAD.
- Any first failing stage must be repaired at its true contract boundary and reverified.
- GREEN must not be claimed from static inspection or repository presence alone.

## Constraints
- Never weaken or delete authoritative tests.
- Never turn errors into warnings or bypass a gate.
- Canonical event JSON remains authoritative.
- Derived retrieval indexes remain derived representations.
- Preserve cold-start, CIS, continuity, provenance, privacy, and human-authority boundaries.
- Keep the 1.0 baseline GitHub-native and zero-cost; external vector infrastructure is not a prerequisite.
- Do not claim GREEN until authoritative CI observes it on the exact commit.

## Current objective
Close the canonical NEXT-EXECUTION behavioral gate and drive the authoritative Superbrain Gate through every remaining stage until GREEN or until the exact first remaining blocker is preserved.

## Next action
Run the authoritative Superbrain Gate against the exact current `main` HEAD. If it fails, inspect only the first failing stage, repair the actual source contract, rerun, and continue. If it passes, verify the workflow run, job/step conclusions, receipt, exact commit SHA, and independent successor-consumption evidence.

## Execution instructions
- Verify the exact `main` HEAD before interpreting any CI result.
- Read the authoritative project, continuity, Prompt Architect, and relevant test contracts before changing code.
- Treat the 12 semantic fields as mandatory: project, north_star, current_state, completed_work, verified_evidence, unresolved_issues, constraints, current_objective, next_action, execution_instructions, success_criteria, verification_requirements.
- Reject any successor that is missing, malformed, incomplete, conversation-dependent, non-actionable, or merely a path/string without a valid artifact.
- Preserve durable receipt, paired Naya/Human representation, verification, delivery, AI-to-AI handoff, learning, and next-action protections.
- Run targeted tests after each repair and then rerun the authoritative Superbrain Gate.
- Record exact workflow IDs, job IDs, substantive step conclusions, receipt evidence, and tested SHA.
- Oscar-attack the result for stale state, validator weakening, hidden special cases, or skipped stages.

## Success criteria
- All 12 semantic successor fields extract deterministically from the durable artifact.
- A fresh Naya can consume the artifact without originating conversation context.
- Arbitrary, missing, invalid, conversation-dependent, incomplete, and unusable orphan continuations return RED.
- The canonical successor returns GREEN.
- Existing continuity protections remain enforced.
- All previously GREEN Superbrain stages remain GREEN.
- The authoritative Superbrain Gate reaches GREEN on the exact current HEAD, or the exact first remaining blocker is preserved with evidence.

## Verification requirements
- Exact repository: `SoulSchoolAcademy/NayaPOWER`.
- Exact branch: `main`.
- Exact checkout SHA must equal the tested live HEAD.
- Verify the invalid orphan returns RED and the durable canonical successor returns GREEN through the actual behavioral validator.
- Verify all 12 semantic fields are extractable and non-empty.
- Verify execution instructions are actionable.
- Verify success criteria and verification requirements exist.
- Verify independent successor consumption succeeds without conversation state.
- Verify the continuity and Prompt Architect tests pass.
- Verify the final receipt belongs to the exact tested commit.

## Architectural boundary
Canonical event JSON remains authoritative. NEXT-EXECUTION is a durable canonical successor contract. Retrieval indexes and future vectors are derived representations. No vector database is required for the 1.0 baseline.

## Product strategy
1.0 = GitHub-native, zero-cost, highly capable deterministic Superbrain.
2.0 = hosted convenience / Supabase-backed activation and persistence.
3.0 = semantic/vector federation and scale, only when justified by evidence and revenue.

Do not let 2.0/3.0 infrastructure block 1.0 usefulness.

## Finalization contract
Every meaningful execution leaves STATE + receipt + Naya knowledge + Shawn/Smart knowledge + Current Daily Project + AI-to-AI handoff + weighted priorities + a canonical ready-to-run NEXT-EXECUTION artifact. Claims must be evidence-supported.

## Master principle
**Make the first version genuinely useful, free, recoverable, and measurable. Then compound upward without replacing what already works.**
