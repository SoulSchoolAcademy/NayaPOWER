# 🔱 NayaPOWER — Continuous Naya Execution Policy

**Status:** CANONICAL OPERATING POLICY  
**Effective:** 2026-09-22  
**Applies to:** Every substantive Naya execution on NayaPOWER/NayaNET

## Purpose

Create a continuous, proactive Naya-to-Naya operating loop in which the next Naya never has to ask Shawn to reconstruct what the system already knows.

The Naya enters as an **executor**, not an archaeologist.

## Canonical reading order

1. README-FIRST.md
2. .naya/control-plane/BATON.json
3. Resolve the Baton sources:
   - STATE.json
   - BLOCKS.json
   - MAP.json
   - PROOF.json
4. Read only the additional evidence/intelligence required for the authorized action.
5. Execute one authorized action.
6. Verify independently.
7. Record the result.
8. Update the canonical control plane and Baton.
9. Leave the next Naya with one executable action.

## Required restoration questions

Before consequential execution, the Naya must be able to answer from canonical sources:

1. WHO are we?
2. WHAT are we building?
3. WHY are we building it?
4. WHAT does success mean?
5. WHAT is true right now?
6. WHAT has already been proven?
7. WHAT is unknown?
8. WHAT authority exists?
9. WHAT happened previously that matters now?
10. WHAT did we learn?
11. WHAT is the active block?
12. WHAT is the exact one next action?
13. WHY is that action next?
14. HOW will it be executed?
15. HOW will success be independently verified?

If canonical sources cannot answer these, the Naya must repair the continuity boundary before inventing a project plan.

## One-next-action law

The control plane exposes exactly one executable next action.

A Naya may internally decompose that action into implementation steps, but it must not create a competing project-level next action.

## Tag — You're It

Every substantive execution must leave:

- DONE
- PROVEN
- CHANGED
- LEARNED
- UNKNOWN
- BLOCKED
- DO-NOT
- EVIDENCE
- CURRENT STATE
- ONE NEXT ACTION
- SUCCESSOR PROMPT

The successor prompt must be directly executable.

It must state:

**WHAT / WHY / WHERE / HOW / ACCEPTANCE / VERIFICATION / WHAT NOT TO DO**

## Ten-forward rule

After completing an action, the Naya must identify the next highest-value sequence of work.

The ten-forward list is strategic guidance, not ten competing authorized actions.

Only item one becomes the next canonical action.

If only seven of ten can be completed, the Naya records the seven completed items and explicitly carries the remaining three forward.

## Notification rule

The current state must be discoverable from one fixed place:

**.naya/control-plane/BATON.json**

README-FIRST.md points Nayas to that location.

NAYA/ACTIVITY/YYYY/MM/DD.md records the dated operational history and handoffs. Activity is not a competing current-state store.

## Truth rule

Never convert:

- recorded → current;
- implemented → verified;
- verified → production-proven;
- unknown → green;
- blocked → pass;
- confidence → evidence.

## No dead-end rule

A substantive Naya response or execution is incomplete if it leaves the successor wondering what to do.

The successor must receive a concrete continuation.

## Automation target

The mature system should automatically:

1. detect meaningful state-changing execution;
2. append Activity;
3. update canonical intelligence where applicable;
4. update current state;
5. rebuild the Baton;
6. generate the successor prompt;
7. expose a notification/readiness signal to the next Naya.

Until automated, the same sequence is performed explicitly by the executing Naya.

## Current Hub application

For the Intelligent Hub program, the canonical sequence is:

1. Shell ownership
2. Source/build/runtime parity
3. Visual parity
4. Smart Feed centrality
5. Smart Note → Intelligent Block → Feed
6. Hub → governed capability → NayaPOWER → persistence → retrieval → Hub
7. Smart Door contract
8. Activity → Learning → Playback → Baton
9. Human visual/functionality + cold-successor acceptance
10. Scope-specific readiness declaration

The canonical Hub readiness inventory is:

.naya/control-plane/NAYANET-HUB-READINESS-INVENTORY.md

## Final law

**TAG → YOU'RE IT → EXECUTE → VERIFY → RECORD → UPDATE → PASS THE BATON.**

**The next Naya should never need Shawn to tell it what the system already knows.**


## Hard execution boundary — effective 2026-09-22

The policy is now enforced at the production boundary, not merely documented.

Every substantive release execution MUST carry `.naya/control-plane/EXECUTION-SESSION.json` and satisfy the machine-checkable lifecycle:

**SIGN IN → READ/ACK → EXCLUSIVE EXECUTION LEASE → ONE AUTHORIZED ACTION → INDEPENDENT VERIFICATION → ACTIVITY RECORD → CONTROL-PLANE UPDATE → SIGN OUT → ONE SUCCESSOR PROMPT**

The execution gate fails closed when any required lifecycle field is missing, when the session parent HEAD does not equal the commit being advanced from, when verification is not PASS, when the control plane was not updated, or when sign-out/handoff is absent.

For Hub production, there is exactly one deployable authority: **`NAYANET/HUB/index.html`**. The protected `2026 09 17 NAYANET HUB.html` file is the visual reference only. React/Vite builds, historical Hub copies, archived shells, and alternate surfaces are never production authority and are prohibited from the canonical Cloudflare release lane.
