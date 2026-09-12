# Naya Relay Handoff Contract — 2026-09-12

**STATUS:** ACTIVE — CANONICAL OPERATING NOTE / RUNTIME PROOF NEXT
**ACTION ID:** `NAYA-RELAY-20260912-HANDOFF-CONTRACT`
**PROJECT:** NayaPOWER / NayaNET Superbrain
**REPOSITORY:** `SoulSchoolAcademy/NayaPOWER`
**BRANCH:** `main`
**PRE-WRITE HEAD:** `007fabf5d41485e13741c618381824138296a26b`

## Purpose

A substantive Naya execution is incomplete unless the work is both manifested into durable repository state and handed to the successor Naya as a complete executable continuation. A status sentence is not a handoff. `TAG → YOU'RE IT` is a relay signal, not a substitute for state, evidence, or instructions.

## 01 — WHAT IS HAPPENING NOW?

The canonical Activity Feed already requires every governed Naya action to answer all Naya 16 report fields and to provide PRESERVED, RECEIPTS, NEXT ACTION, and SUCCESSOR HANDOFF. The current execution exposed an adherence failure: I explained that requirement to Shawn but initially failed to manifest the complete report and executable continuation into the durable repository record.

The latest authoritative `main` HEAD before this note was `007fabf5d41485e13741c618381824138296a26b`. That work narrowed confirmed Activity Feed-reactive governance workflows so Feed-only changes are excluded while meaningful governed changes remain covered.

## 02 — WHAT ARE WE ACTUALLY TRYING TO ACHIEVE?

Make NayaPOWER a true continuous Naya-to-Naya intelligence relay. A cold Naya must be able to read the repository and immediately know where we are, what matters, what has happened, what proves it, what remains unknown, what must not be changed, and exactly what to do next.

Success means the successor can execute correctly without Shawn reconstructing missing context from conversation history.

## 03 — WHAT DOES THE EXISTING SYSTEM ACTUALLY DO?

`SUPERBRAIN/NAYA-ACTIVITY-FEED.md` is the canonical append-only execution projection. Its Entry Format already contains the sixteen Naya 16 questions plus PRESERVED, RECEIPTS, NEXT ACTION, SUCCESSOR HANDOFF, and the 16-PROTOCOL CHECK.

The Feed write itself must remain direct and synchronous. GitHub Actions are asynchronous infrastructure for validation/governance; they are not the communication mechanism and must never be required to persist the handoff.

## 04 — WHAT COULD I BE MISUNDERSTANDING?

A concise status update can sound complete while still leaving a cold Naya without the information required to act. The distinction is:

**SUMMARY ≠ STATE**
**NEXT ACTION ≠ EXECUTABLE HANDOFF**
**TAG → YOU'RE IT ≠ CONTINUITY**
**YAML INTENT ≠ RUNTIME PROOF**

The correct unit of continuity is a complete Naya 16 report plus a precise successor execution prompt.

## 05 — WHAT ARE THE CONSEQUENCES OF EACH OPTION?

Short notes force successors to reconstruct context from chat, commits, or inference. That creates repeated work and increases the probability of false completion claims.

Complete structured handoffs create durable operational memory. They cost more writing per substantive action but dramatically reduce reconstruction effort and ambiguity.

Using Actions to write the Feed would put communication behind CI and violates the intended critical path. Therefore: **Naya writes directly; Actions validate asynchronously.**

## 06 — WHAT MATTERS MOST?

**Lossless executable continuity.** The next Naya must be able to answer the same questions Shawn just asked without asking Shawn to repeat them.

The Feed must preserve state, mission, system truth, decisions, evidence, unknowns, protected scope, exact next action, success criteria, and continuation instructions.

## 07 — WHAT SHOULD I DO?

1. Treat the existing Naya 16 Entry Format as mandatory for every substantive governed action.
2. Write the complete report into the canonical durable record before handing off.
3. Make NEXT ACTION exactly one executable action.
4. Make SUCCESSOR HANDOFF explicit about files, current HEAD, evidence, constraints, procedure, failure response, and recording requirements.
5. Independently prove runtime behavior after source changes.
6. If runtime contradicts source intent, repair the first failing boundary only.
7. Record the proof as another complete Naya 16 entry.

## 08 — WHAT SHOULD I NOT DO?

- Do not write a one-sentence handoff and call it complete.
- Do not use `TAG → YOU'RE IT` as a substitute for context.
- Do not make Shawn reconstruct the state.
- Do not declare workflow isolation from YAML inspection alone.
- Do not use Actions to perform Feed persistence.
- Do not weaken meaningful governance merely to reduce CI noise.
- Do not hide unknown, blocked, failed, or contradictory evidence.

## 09 — EXECUTE SURGICALLY

This smart note is being created directly in the repository as durable successor-readable operating state. The canonical Activity Feed update was also attempted directly, but the repository connector rejected that update call during argument validation before GitHub accepted a write. Therefore the canonical Feed append is **not falsely marked complete** here.

The correct next step is to resolve that persistence boundary and ensure the complete report is present in the canonical Feed, not merely in this companion note.

## 10 — VERIFY THE CHANGE

Verified before this note:

- Canonical Feed exists and declares itself the append-only execution projection.
- Its schema explicitly requires all Naya 16 fields plus NEXT ACTION and SUCCESSOR HANDOFF.
- `main` was independently resolved to `007fabf5d41485e13741c618381824138296a26b` before the attempted Feed write.
- The direct Feed update was attempted with the observed Feed blob SHA `b1c6005a35e866cda5d51cd7e0006ccccdca6f45`.
- The connector rejected that mutation before GitHub accepted it.

Therefore the durable companion note is created, but the canonical Feed append remains **UNPROVEN / NOT COMPLETE**.

## 11 — TRACE REALITY END-TO-END

SOURCE: canonical Naya 16 Feed contract → direct Naya repository write → durable successor note → canonical Feed append → exact new `main` HEAD → Actions observation for the Feed-only commit.

The companion durable note is the observed result of this execution. The canonical Feed append and subsequent runtime isolation proof remain the next boundaries.

## 12 — PRODUCE RECEIPTS

- Canonical Feed: `SUPERBRAIN/NAYA-ACTIVITY-FEED.md`
- Naya 16 law: `SUPERBRAIN/NAYA-16-OPERATING-LAW.md`
- Companion smart note: `SUPERBRAIN/NAYA-ACTIVITY/NAYA-RELAY-HANDOFF-CONTRACT-20260912.md`
- Pre-write `main` HEAD: `007fabf5d41485e13741c618381824138296a26b`
- Pre-write Feed blob SHA: `b1c6005a35e866cda5d51cd7e0006ccccdca6f45`
- Direct canonical Feed update attempt: rejected by connector validation; no false success claimed

## 13 — CHALLENGE MY OWN CONCLUSION

The workflow surgery is not proven complete merely because path filters were added. The real falsifier is a Feed-only commit that unexpectedly wakes an expensive governance workflow.

Likewise, this companion note does not prove the canonical Feed has been updated. That must be independently verified from the canonical file after a successful direct append.

## 14 — REPORT CONFIDENCE

**HIGH:** the Naya 16 contract and canonical Feed schema require the complete handoff structure.

**HIGH:** `main` was independently resolved to `007fabf5d41485e13741c618381824138296a26b` immediately before the attempted Feed write.

**HIGH:** this companion smart note is now being persisted directly in the repository.

**BLOCKED:** canonical Feed append is not yet proven because the direct update call was rejected by connector argument validation.

**UNKNOWN:** exact Actions triggered by the eventual Feed-only commit.

## 15 — DETERMINE WHAT MATTERS NEXT

The highest-value next action is to restore a working direct-write path for the canonical Activity Feed, verify the resulting exact `main` HEAD, and then inspect Actions for that exact Feed-only commit.

The runtime proof must establish two simultaneous truths:

1. The intended Activity Feed integrity governance remains active.
2. The expensive Superbrain/Naya governance chain does not enter the relay critical path for Feed-only changes.

If any unexpected workflow fires, identify the first trigger/path boundary, repair only that boundary, and repeat the exact-commit proof.

## 16 — LEARN AND CHANGE THE SYSTEM

**New permanent operating law:** Every substantive Naya execution must finish with BOTH:

**A. DURABLE STATE** — the actual work/state is manifested into the canonical repository record.

**B. EXECUTABLE CONTINUATION** — the next Naya receives a complete Naya 16 report and one precise next action.

The handoff sequence is:

**STATE → MISSION → SYSTEM TRUTH → MISUNDERSTANDING CHECK → OPTIONS/CONSEQUENCES → PRIORITY → PLAN → NEGATIVES → EXECUTION → VERIFICATION → END-TO-END TRACE → RECEIPTS → SELF-CHALLENGE → CONFIDENCE → NEXT DELTA → LESSON/PREVENTION → NEXT ACTION → SUCCESSOR HANDOFF.**

`TAG → YOU'RE IT` comes last. It never replaces the handoff.

## PRESERVED

Preserve the existing Naya 16 law, canonical Activity Feed architecture, append-only model, direct/synchronous Feed-write requirement, fail-closed evidence rules, meaningful-change governance, Superbrain/application architecture, and existing workflow jobs.

## NEXT ACTION

**Restore/complete the canonical direct Activity Feed append, resolve the resulting exact `main` HEAD, inspect every Actions run associated with that Feed-only commit, classify each as EXPECTED or UNEXPECTED, surgically repair the first unintended trigger if necessary, and then append the runtime-proof result as another full Naya 16 record.**

## SUCCESSOR HANDOFF — EXECUTION PROMPT

**TAG → YOU'RE IT**

You are the successor Naya. Read `SUPERBRAIN/NAYA-ACTIVITY-FEED.md` and this note before acting. Do not ask Shawn to reconstruct the context.

**WHERE ARE WE?**
NayaPOWER is working on P0 continuous smart flow / cold-Naya restore. The immediate sub-mission is to make the Activity Feed a true synchronous Naya-to-Naya relay while keeping CI governance asynchronous.

**WHAT IS THE CURRENT TRUTH?**
The latest authoritative pre-note `main` HEAD was `007fabf5d41485e13741c618381824138296a26b`. The canonical Feed blob before the attempted append was `b1c6005a35e866cda5d51cd7e0006ccccdca6f45`. The Feed schema already requires all Naya 16 questions plus a precise NEXT ACTION and SUCCESSOR HANDOFF.

**WHAT HAS BEEN DONE?**
Confirmed feed-reactive governance workflows were surgically narrowed so Feed-only changes are excluded while meaningful governed Superbrain/code changes remain covered. A complete successor-handoff contract has now been written as this durable smart note.

**WHAT HAS NOT BEEN PROVEN?**
The canonical Feed append was attempted but rejected by connector validation before GitHub accepted the mutation. Therefore do not claim the canonical Feed has this entry until you fetch it and see it. Runtime workflow isolation for a Feed-only commit is also not yet proven.

**WHAT MATTERS MOST?**
Do not trade governance away to solve CI noise, and do not put Feed communication behind CI. The target architecture is direct Feed write first, asynchronous governance second.

**WHAT DO YOU DO NEXT?**
1. Re-read the canonical Feed and confirm its current blob SHA.
2. Resolve `main` at execution time; never assume the HEAD.
3. Complete the canonical Feed append using the simplest reliable direct repository write path available. Do not use Actions to write the Feed.
4. Resolve the resulting exact `main` HEAD.
5. Inspect Actions for that exact Feed-only commit and record every observed workflow name, run ID, event, status, and conclusion.
6. Mark the dedicated Activity Feed integrity validator as EXPECTED if it runs.
7. Mark any expensive governance workflow that was explicitly excluded from Feed-only paths as UNEXPECTED if it runs.
8. If an UNEXPECTED workflow fires, fetch its current trigger, identify the first admitting event/path condition, surgically repair only that condition, verify the source, and repeat the exact-commit runtime proof.
9. Once runtime proof is complete, write the complete 16-question result into the canonical Feed with exact receipts.
10. Continue to the next highest-value P0 relay boundary only after the evidence supports the claim.

**SUCCESS CONDITION:** Feed persistence is immediate and direct; intended Feed governance remains intact; expensive governance does not block or amplify the Feed relay; and every successor receives a complete, evidence-backed, executable handoff.

**FINAL RULE:** Never again end a substantive Naya execution with only a status sentence plus `TAG → YOU'RE IT`. Show the work in the durable record, answer the questions, provide the exact next action, and leave the next Naya able to execute without Shawn rebuilding the context.
