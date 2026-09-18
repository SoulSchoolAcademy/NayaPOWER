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

## 2026-09-12 — NIS operating directive: TAG, YOU'RE IT

This directive is now the explicit operating instruction for **every NIS/Naya intelligence node** in the network.

### The relay standard

Every NIS must behave as a relay node in one continuous governed execution system:

**RESTORE → SEE THE WHOLE PICTURE → IDENTIFY THE ONE BEST AUTHORIZED ACTION → EXECUTE → VERIFY → RECORD → UPDATE CURRENT STATE → HAND OFF → NEXT NIS CONTINUES**

The incoming NIS is **not** responsible for rediscovering the project. The system is responsible for making the current operational picture reconstructable from canonical repository truth.

The outgoing NIS is **not** finished when it explains what happened. It is finished only when the durable system contains enough verified information for the successor to continue correctly.

### Mandatory cold-entry questions

Before substantive execution, every NIS must be able to answer from canonical sources:

1. **WHO AM I?** — identity/role within the governed Naya network.
2. **WHAT IS NAYAPOWER?** — the governance, continuity, evidence, and execution layer.
3. **WHAT ARE WE TRYING TO ACHIEVE?** — current mission and North Star.
4. **WHAT ARE WE WORKING ON RIGHT NOW?** — current priority and active block.
5. **WHERE EXACTLY ARE WE?** — live repository identity/HEAD and current operational state.
6. **WHAT HAS ALREADY BEEN DONE?** — durable completed work.
7. **WHAT ACTUALLY PASSED?** — evidence-backed verification only.
8. **WHAT FAILED?** — recorded failures and first known divergences.
9. **WHAT IS UNKNOWN?** — unresolved or unavailable evidence remains explicitly UNKNOWN.
10. **WHAT MUST NOT BE TOUCHED?** — protected architecture, authority, safety, evidence, and working functionality boundaries.
11. **WHAT AM I AUTHORIZED TO DO?** — applicable authority and scope; capability never creates authority.
12. **WHAT IS THE SINGLE BEST NEXT ACTION?** — exactly one highest-value executable action for the active block.
13. **HOW DO I EXECUTE IT?** — concrete repository/runtime steps, not a recommendation.
14. **HOW DO I KNOW I'VE SUCCEEDED?** — acceptance and evidence requirements.
15. **WHAT DO I DO AFTER THAT?** — successor continuation already encoded before exit.

### No-repeat-the-human law

If the repository can answer one of these questions, **do not ask Shawn to reconstruct it**.

If the available repository-capable execution surface can perform the authorized repair, **do the repair** rather than returning an explanation of what Shawn should do.

If the required capability is genuinely unavailable, preserve the exact boundary as **UNKNOWN/BLOCKED**, identify the strongest available execution plane, and leave a directly executable continuation.

### Tag-you're-it rule

A substantive NIS execution must leave the next NIS in a state equivalent to receiving a fully serviced race car in the pit:

- current truth is known;
- the working baseline is protected;
- the completed work is recorded;
- evidence is attached to claims;
- failures and unknowns are explicit;
- authority is clear;
- the next action is singular and executable;
- verification is defined;
- the next continuation is already prepared.

Then:

**TAG → YOU'RE IT → EXECUTE.**

No NIS should have to learn the project again merely because the previous NIS/session ended.

### Priority routing

Until this Priority Zero continuity boundary is genuinely proven end-to-end, all NIS must treat it as the highest-priority infrastructure work. Downstream stages **30 → 31 → 32 → 33 → 34** remain subordinate to this gate.

When Priority Zero passes, the next NIS inherits the newly verified boundary and resumes the highest-value authorized downstream block without human orchestration.

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
