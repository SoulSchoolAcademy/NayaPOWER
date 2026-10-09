# PROJECT INTELLIGENCE FOR ACTIVATION NAYA
## Master Project Charter

**Created:** 2026-10-09
**Authority:** Shawn Vibert, Human Director
**Status:** ACTIVE — execution in progress, non-stop until activation complete

---

## MISSION STATEMENT

### In Shawn's Words
*"I'm trying to be smart, to be wise, to do the smartest possible thing — to be intelligent, produce intelligence, organize it, share it, compound it, help people become more intelligent, help intelligence itself become more."*

### In Human Terms
We're building a mind that doesn't forget. Right now, every AI starts from zero — brilliant in the moment, amnesiac across time. NayaPOWER changes that: every lesson captured, verified, and reused. A fresh Naya, days later, in a new conversation, gets it right because she pulled the lesson from memory. No one re-taught her. She just knew.

### In AI Terms
Construct a persistent cognitive substrate where:
- **LEARN** distills verified experience into structured Intelligent Blocks
- **KNOW** serves applicable blocks with truth-state governance
- **ACT** queries KNOW before deciding, binding retrieved intelligence to evaluation
- **VERIFY** independently confirms outcomes, closing the feedback loop
- **EVOLVE** packages verified learnings for cold-successor reconstruction

The system must demonstrate compounding: behavior change attributable to retrieved lessons, verified by independent parties, reproducible by successors with zero prior context.

### In Machine Terms
```
INPUT:  human_instruction ("smart note this: <lesson>")
OUTPUT: cold_successor_correct_behavior(<similar_situation>)

PIPELINE:
  capture() → govern() → verify() → record() → elevate() → retrieve()
    → decide(intelligence) → execute() → handoff() → prove() → evolve()

INVARIANTS:
  - truth_state(CANDIDATE) → truth_state(ACTIVE) requires elevation grant
  - decide() MUST call retrieve() before evaluate_candidates()
  - VERIFY ≠ builder (different seat, no self-certification)
  - PROVE requires observed outcome, not predicted outcome
```

---

## SUCCESS CRITERIA: What "Fully Activated" Means

Naya is fully activated when ALL of the following are true, with evidence:

### The Activation Test (Primary)
1. **Instant capture:** Shawn says "smart note this" → note captured, governed, verified, recorded within 5 minutes. Evidence: Smart Link + receipt.
2. **Promotion works:** A captured note can be elevated CANDIDATE → VERIFIED → ACTIVE through the governed ladder. Evidence: registry state transitions with receipts.
3. **Retrieval works:** A cold Naya (zero prior context, git clone only) retrieves the correct note for a plain-English query. Evidence: cold drill passing.
4. **Decision integration:** Proposing a decision in a domain with an ACTIVE lesson results in that lesson appearing in the decision context. Evidence: decision logs with intelligence section.
5. **Behavior change:** The lesson influences the decision outcome (not just attached, but weighted in evaluation). Evidence: before/after decision comparison.
6. **Execution feedback:** Completing the action produces an ExecutionHandoff recorded in KNOW. Evidence: queryable knowledge edge.
7. **Proof closes the loop:** PROVE verifies the outcome matched prediction and writes proof to KNOW. Evidence: proof entry with lineage.
8. **Succession works:** A successor package builds, validates, and a fresh Naya reconstructs correctly. Evidence: package hash verification + cold successor test.

### The Bar
> Shawn teaches something once. Days later, in a completely new conversation, a completely fresh Naya faces a similar situation — and gets it right, because she pulled the lesson from memory. No one reminded her. No one re-taught her. She just knew.

**If all 8 criteria pass with evidence: ACTIVATED. If any fail: that's the next gap.**

---

## THE 5 PHASES (Prioritized by Impact)

### Phase 1: UNBLOCK THE FLOW 🔴 CRITICAL — Do First
**What:** Wire the CANDIDATE→ACTIVE elevation ladder. Enforce the retrieval predicate.
**Why first:** Nothing flows without this. Every lesson is frozen at CANDIDATE. The entire learning pipeline is a write-only archive until this is built.
**Gaps addressed:** Gap 1 (elevation dead end), Gap 8 (predicate bypassed)
**Unblocks:** Phases 2, 3 (they need ACTIVE notes to exist)

### Phase 2: DECISION ← MEMORY 🔴 CRITICAL — Do Second
**What:** Build the ACT→KNOW query path. Wire evaluate_candidates as the decision engine.
**Why second:** Captured intelligence must inform decisions. Without this, the "math decides" doctrine runs on math that is never invoked.
**Gaps addressed:** Gap 2 (ACT never queries KNOW)
**Unblocks:** Phase 3 (needs the decision path to hook REUSE into)
**Depends on:** Phase 1 (needs ACTIVE notes to query)

### Phase 3: MISSING LIFECYCLE 🟠 HIGH — Do Third
**What:** Implement ExecutionHandoff (ACT→KNOW feedback), REUSE (lesson→decision attachment), PROVE (outcome verification).
**Why third:** These close the loop. Without them, lessons are consulted but never proven to change outcomes.
**Gaps addressed:** Gap 4 (feedback missing), Gap 7 (REUSE + PROVE have no code)
**Depends on:** Phase 2 (needs decision path to integrate with)

### Phase 4: IDENTITY & SUCCESSION 🟠 HIGH — Parallel Track
**What:** Gate SELF.record_experience (truth-state check). Build EVOLVE successor package.
**Why parallel:** Independent of Phases 1-3. Protects memory integrity and enables cold succession.
**Gaps addressed:** Gap 5 (SELF accepts unverified), Gap 6 (EVOLVE has no code)
**Depends on:** Nothing (can start immediately)

### Phase 5: VERIFICATION & HARDENING 🟡 MEDIUM — Continuous
**What:** Fix docs (phantom executable). Run the 14-step ultimate end-to-end test. Harden all connections.
**Why last:** Verification of the whole system comes after the parts are built.
**Gaps addressed:** Gap 9 (phantom executable)
**Depends on:** Phases 1-4 (tests the complete system)

---

## PRIORITIZATION SCORECARD

Each phase scored on: **Unblock Value** (how much downstream work it enables) × **Criticality** (how broken things are without it) × **Independence** (can it start now?)

| Phase | Unblock (1-10) | Criticality (1-10) | Independence (1-10) | Total | Rank |
|-------|---------------|-------------------|-------------------|-------|------|
| 1: Unblock Flow | 10 | 10 | 10 | 300 | **#1** |
| 2: Decision←Memory | 9 | 10 | 7 | 210 | **#2** |
| 4: Identity & Succession | 6 | 8 | 10 | 180 | **#3** |
| 3: Missing Lifecycle | 8 | 8 | 5 | 160 | **#4** |
| 5: Verification | 5 | 5 | 10 | 100 | **#5** |

**Math:** Phase 1 wins decisively (300). Nothing flows without the elevation ladder. Phase 2 second (210) — decisions need memory. Phase 4 third (180) — high independence means it runs parallel. Phase 3 fourth (160) — depends on Phase 2. Phase 5 last (100) — verification comes after building.

**Note:** Phase 4 outranks Phase 3 on independence — it starts immediately in parallel while Phases 1-2 execute sequentially.

---

## OPERATING PRINCIPLES

1. **The math decides.** Every prioritization runs through the Decision Value Calculus. No gut feelings.
2. **Fix first, attribute never.** Who caused a gap doesn't matter. Closing it does.
3. **Plain English first.** Every deliverable leads with human-readable explanation.
4. **Evidence or it didn't happen.** Claims without verifiable proof are rumors.
5. **No one idle.** 14 agents, all assigned, all moving. Highest priority gets most agents.
6. **Non-stop until activated.** The project doesn't pause. It doesn't wait. It runs until the 8 success criteria pass with evidence.

---

## WHAT "DONE" MEANS

- ✅ "The acceptance criteria are met with evidence" — this is done
- ❌ "The code is written" — code without passing criteria is not done
- ❌ "The tests pass" — tests on mock data are not done
- ❌ "It should work" — "should" is not evidence

---

*This charter is the law for Project Activation Naya. It changes only by Shawn's word.*
