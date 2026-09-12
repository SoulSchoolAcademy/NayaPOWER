# Naya Relay Handoff — Complete Successor Execution Prompt — 2026-09-12

**STATUS:** ACTIVE — EXECUTE NEXT
**ACTION ID:** `NAYA-RELAY-20260912-EXECUTION-PROMPT`
**PROJECT:** NayaPOWER / NayaNET Superbrain
**REPOSITORY:** `SoulSchoolAcademy/NayaPOWER`
**BRANCH:** `main`

## Mission
Make NayaPOWER a true continuous Naya-to-Naya intelligence relay. A cold Naya must restore exact current truth, execute the highest-value authorized action, verify it with evidence, update durable operating state, and leave the next Naya a complete executable continuation.

## Where are we?
We are at the Activity Feed continuity boundary. The workflow-surgery work has already narrowed confirmed Activity Feed-reactive governance workflows so Feed-only changes are intended to be excluded while meaningful Superbrain/code changes remain governed. The canonical Activity Feed is `SUPERBRAIN/NAYA-ACTIVITY-FEED.md`. The governing protocol is `SUPERBRAIN/NAYA-16-OPERATING-LAW.md`.

The immediate problem discovered during this execution was behavioral, not merely architectural: Naya was explaining the correct handoff process but was not consistently writing the complete Naya 16 state + evidence + executable continuation into the canonical Feed. That has now been explicitly formalized as a permanent operating law.

## What are we actually trying to achieve?
After every substantive governed execution, the next Naya must be able to continue without Shawn reconstructing context. The handoff must answer:

1. Where are we?
2. What are we trying to accomplish?
3. What does the existing system actually do?
4. What could be misunderstood?
5. What are the consequences of the available options?
6. What matters most?
7. What should be done?
8. What must not be done?
9. What was executed?
10. What was verified?
11. What is the end-to-end reality trace?
12. What receipts prove the claims?
13. What could falsify the conclusion?
14. How confident should the successor be?
15. What is the single highest-value next action?
16. What reusable lesson/control should persist?

Then provide a concrete successor execution prompt, including exact files, current HEAD, evidence requirements, constraints, success criteria, and failure response.

## What does the existing system actually do?
The Activity Feed is an append-only execution/continuity projection. Its Entry Format already requires the Naya 16 questions plus `PRESERVED`, `RECEIPTS`, `NEXT ACTION`, `SUCCESSOR HANDOFF`, and `16-PROTOCOL CHECK`.

The Feed write is direct and synchronous. GitHub Actions are asynchronous infrastructure for validation/governance. Actions must not perform Feed persistence or become a prerequisite for the handoff.

## What could we be misunderstanding?
Do not confuse:

- SUMMARY with STATE
- NEXT ACTION with EXECUTABLE HANDOFF
- TAG → YOU'RE IT with CONTINUITY
- YAML INTENT with RUNTIME PROOF
- CONVERSATION MEMORY with DURABLE PROJECT MEMORY

A handoff is successful only when a cold Naya can execute from the repository without asking Shawn to reconstruct what happened.

## What are the consequences?
Short notes are cheaper but force reconstruction and increase false-completion risk. Complete structured handoffs cost more writing but preserve operational continuity. Having Actions write the Feed would put communication behind asynchronous CI and can introduce delay, failure, or amplification. Therefore the selected architecture is:

**Naya writes the Feed directly and synchronously. Actions validate asynchronously.**

## What matters most?
Lossless executable continuity with evidence integrity. Unknowns remain unknown. Blocked claims remain blocked. No governance is weakened merely to make CI quieter.

## What has been done?
A durable relay-contract smart note was created at:

`SUPERBRAIN/NAYA-ACTIVITY/NAYA-RELAY-HANDOFF-CONTRACT-20260912.md`

at commit:

`99aac37c69f7827dfcbf459c3acead92c57f830a`

The canonical Feed was then directly updated in commit:

`c1d41903fc96ddaa4ff8473c2c9443270b127933`

The Feed update preserved the existing records and appended the relay-contract report. The pre-append Feed blob SHA was:

`b1c6005a35e866cda5d51cd7e0006ccccdca6f45`

## What is not yet proven?
The Feed append commit exists, but the Feed-only runtime boundary has not yet been independently proven by observing Actions for that exact commit. The resulting Feed should also be fetched and inspected before claiming final Feed state.

The source-level path exclusions are not sufficient evidence of runtime isolation. Runtime observation is required.

## What should you do?
1. Resolve `main` at execution time.
2. Fetch `SUPERBRAIN/NAYA-ACTIVITY-FEED.md` and confirm this relay record is present.
3. Record the exact resulting HEAD.
4. Identify the exact Feed-only commit containing the handoff.
5. Inspect GitHub Actions runs associated with that exact commit.
6. Classify the dedicated Activity Feed integrity validator as EXPECTED if it runs.
7. Classify any governance workflow that the Feed-only paths were explicitly intended to exclude as UNEXPECTED if it runs.
8. If an unexpected workflow fires, fetch its current trigger and identify the first admitting event/path condition.
9. Repair only that first boundary. Preserve all meaningful governance coverage.
10. Make another legitimate direct Feed handoff commit and repeat the exact-commit runtime proof.
11. Once runtime isolation is proven, append a complete Naya 16 runtime-proof entry to the canonical Feed with exact receipts.
12. Only then move to the next highest-value P0 relay boundary.

## What should you NOT do?
- Do not use GitHub Actions to write the Feed.
- Do not invent a runtime URL or secret.
- Do not declare CI isolation from YAML inspection alone.
- Do not weaken governance to reduce CI noise.
- Do not overwrite or erase contradictory evidence.
- Do not ask Shawn to reconstruct the state.
- Do not end with only a status sentence and `TAG → YOU'RE IT`.
- Do not call an unverified assumption a proof.

## Verification contract
For every material claim, provide a receipt or mark it unproven.

For the Feed-only runtime proof, the minimum evidence is:

**SOURCE → exact Feed-only commit → observed Actions runs → workflow classification → runtime conclusion → durable Feed record**

The final runtime conclusion must distinguish EXPECTED from UNEXPECTED workflows and must identify any remaining unknowns.

## Failure response
If source intent and runtime behavior disagree:

1. Stop the completion claim.
2. Identify the first failing boundary.
3. Fetch the actual current source for that boundary.
4. Make the smallest surgical correction.
5. Verify the source again.
6. Repeat the exact-commit runtime observation.
7. Keep the Feed result BLOCKED until evidence supports PASS.

## Success condition
The relay is successful only when:

- the complete handoff is present in the canonical Feed;
- a cold Naya can continue without Shawn reconstruction;
- Feed persistence is direct and does not depend on Actions;
- the dedicated Feed governance remains active;
- excluded expensive governance does not enter the Feed relay critical path;
- meaningful Superbrain/code changes remain governed;
- runtime behavior has been independently observed;
- the exact receipts are recorded in the next Feed entry.

## Permanent rule
Every substantive Naya execution has two mandatory outputs:

**A. DURABLE STATE** — the actual work and current truth are manifested into the canonical repository record.

**B. EXECUTABLE CONTINUATION** — the successor receives a complete Naya 16 report, one precise next action, and a complete execution prompt.

`TAG → YOU'RE IT` comes last. It never substitutes for the handoff.

## Final successor instruction
Read the canonical Activity Feed, the Naya 16 operating law, and this prompt. Resolve current `main`. Verify what is actually present. Execute the single highest-value next action. Prove it. Write the complete result back into the canonical Feed. Then hand off again using this same structure.

**TAG → YOU'RE IT.**
