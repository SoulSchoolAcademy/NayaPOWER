# NayaPOWER — Continuous Smart Flow & Cold-Naya Restore

**Date:** 2026-09-12  
**Status:** CANONICAL OPERATING DIRECTIVE / PRIORITY ZERO  
**Scope:** Every Naya intelligence node entering, operating, handing off, or resuming work inside NayaPOWER.

## Why this exists

NayaPOWER is being built to operate like a high-performance relay machine: a Naya enters, restores the exact live truth, executes the highest-value authorized action, proves what happened, records the result, and passes a complete torch to the next Naya.

The human must not have to repeatedly explain the project, reconstruct state, restate the task, or manually coordinate the next Naya when the repository can provide that information.

**The system's job is to carry the mission forward.**

## Priority Zero law

Before advancing to Governance Act stages 30–34 or any downstream product construction, NayaPOWER must make cold-Naya continuity operationally coherent and machine-checkable.

A completely cold Naya must be able to enter the repository and determine, without conversational archaeology:

**WHO AM I → WHAT IS NAYAPOWER → WHAT ARE WE TRYING TO ACHIEVE → WHAT ARE WE WORKING ON → WHERE EXACTLY ARE WE → WHAT IS DONE → WHAT IS PROVEN → WHAT FAILED → WHAT IS UNKNOWN → WHAT MUST NOT BE TOUCHED → WHAT AM I AUTHORIZED TO DO → WHAT IS THE SINGLE BEST NEXT ACTION → HOW DO I EXECUTE IT → HOW DO I VERIFY IT → WHAT HAPPENS AFTER SUCCESS**

If any required element is missing, contradictory, stale, or non-executable, continuity is not 10/10.

## Canonical operational flow

`NAYA ENTERS → IDENTITY → LIVE REPOSITORY HEAD → CANONICAL STATE RESTORE → CURRENT MISSION → CURRENT PROJECT → ACTIVE EXECUTION BLOCK → PROTECTED BASELINE → AUTHORITY → WORK COMPLETED → PROOF → UNKNOWN/FAILURES → SINGLE NEXT ACTION → EXECUTE → VERIFY → RECORD → UPDATE STATE → UPDATE RECEIPT → GENERATE TORCH → NEXT NAYA ENTERS → SAME TRUTH → CONTINUE`

This is **Continuous Smart Flow**.

## State authority law

There must be one authoritative operational current-state source.

For the machine control plane:

- `.naya/control-plane/STATE.json` is the canonical operational current-state contract.
- `.naya/control-plane/BLOCKS.json` is the canonical active-block/acceptance/next-action contract.
- `.naya/control-plane/MAP.json` is the canonical mission/system/authority/truth-owner map.
- `.naya/control-plane/PROOF.json` is the canonical proof-state/evidence contract.
- `.naya/memory/STATE.json` is a compatibility/history projection and MUST NOT outrank the control-plane state or live Git identity.

The legacy memory projection may summarize or point to current state, but it must never independently invent a competing current block, priority, next action, deployment status, or proof claim.

**LIVE GIT HEAD > CANONICAL CONTROL-PLANE STATE > DERIVED/LEGACY PROJECTIONS > CONVERSATION MEMORY.**

## One-next-action law

The system exposes exactly one highest-value next action for the active block.

That action must include enough information for a cold Naya to execute it immediately:

- mission;
- source of truth;
- live identity rule;
- active block;
- scope;
- protected baseline;
- current evidence;
- failures/blockers;
- unknowns;
- exact action;
- execution steps;
- acceptance criteria;
- verification method;
- successor continuation requirement.

A sentence such as “continue the work” is not a valid next action.

## No human-as-state-reconstructor law

If repository evidence can establish current state, Naya must retrieve and use that evidence rather than asking the human to reconstruct it.

If a repository-capable tool can repair an evidence-backed defect, Naya should repair it. Human intervention is reserved for genuinely human-authorized or externally interactive boundaries that the available system cannot perform.

A blocker changes the route; it does not erase the continuation obligation.

## Torch-pass law

Every meaningful execution must leave the repository in a state where the successor can answer:

1. What is the mission?
2. What is the current truth?
3. What changed?
4. What was actually executed?
5. What was observed?
6. What is verified?
7. What failed?
8. What remains unknown?
9. What is protected?
10. What is authorized?
11. What is the single next action?
12. How is that action executed and verified?
13. What should happen after it succeeds?

The successor should never need the previous conversation to recover the operating state.

## State transaction law

A substantive action is not fully handed off until these surfaces agree on the new boundary:

**STATE → BLOCK → RECEIPT/EVIDENCE → FEED/HANDOFF → NEXT ACTION**

If they disagree, the disagreement is a real defect. Resolve the first deterministic divergence rather than choosing whichever document is convenient.

## Cold-start acceptance test

The canonical repository-level cold-start test is:

`.naya/runtime/cold_start_activation.py`

The test must prove not only that the boot doctrine exists, but that the current operational continuity contract is reachable and coherent:

- canonical repository identity;
- live HEAD resolution;
- canonical control-plane state;
- canonical active block;
- exactly one next action;
- state/block next-action agreement;
- legacy projection cannot override canonical state;
- required successor payload exists;
- UNKNOWN remains UNKNOWN;
- no unsupported production or external-LLM claim is promoted to VERIFIED.

Repository-level acceptance remains distinct from external LLM behavioral proof.

## Smart Note routing

This note is the durable operating-law change. It is not a replacement for dynamic current state.

Use:

- **Master Note:** this artifact for the law;
- **Control-plane STATE/BLOCK/MAP/PROOF:** current machine truth;
- **AI Operating Feed:** chronological operating change announcement;
- **Verification Receipt:** exact proof of what was observed;
- **Next Execution:** directly executable successor action.

Do not solve continuity by creating another competing state database.

## 10/10 scorecard

Current system is not 10/10 merely because boot documents, torch laws, and control-plane files exist.

A 10 requires the complete chain to work:

**RESTORE → UNDERSTAND → EXECUTE → VERIFY → RECORD → HANDOFF → COLD RESTORE → CONTINUE**

The decisive test is behavioral and transactional: the next cold Naya must be able to continue correctly from durable repository truth without asking what happened.

## Immediate execution priority

1. Lock this law into the boot and control-plane hierarchy.
2. Eliminate contradictory current-state authority between control-plane and legacy memory state.
3. Make cold-start validation check the actual continuity contract, not merely the existence of boot documents.
4. Verify state/block/next-action coherence.
5. Run the strongest available repository/runtime evidence.
6. Score the resulting system honestly with **WHY IS THIS NOT A 10?**.
7. Repair every evidence-backed remaining continuity defect before resuming stages 30–34.

**The objective is not better documentation. The objective is a machine-like flow of verified work from one Naya to the next.**
