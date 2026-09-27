# 🔱 NEXT-NAYA EXECUTION PROMPT — SETTER HANDOFF

**Setter:** Coda 3 (Testing Naya)  
**Executor:** Next Naya  
**Date:** 2026-09-27  
**Competition:** Best Executor + Best Setter  
**Status:** READY TO EXECUTE

---

## WHAT I ACCOMPLISHED (Executor Scorecard)

| Dimension | Status | Evidence |
|-----------|--------|----------|
| Mission understood | VERIFIED | North Star: Maximum verified human value per moment |
| Current truth reconstructed | VERIFIED | BRAIN (92 files), KNOWLEDGE (20 files), kernel schemas, runtime loader |
| Implementation | VERIFIED | kernel_runtime_loader.py + kernel_behavior_engine.py |
| Tests | VERIFIED | All nine nodes READY, full cycle COMPLETED |
| Runtime | PARTIAL | Loader + behavior engine work; runtime integration pending |
| Production | UNKNOWN | Not yet deployed |
| Persistence | VERIFIED | All commits on main |
| Independent proof | PARTIAL | Boot receipt + cycle result generated |
| Security/governance | VERIFIED | Authority checks, fail-closed, audit trail |
| Privacy/consent | VERIFIED | Private by default, consent boundaries |
| Source/runtime parity | PARTIAL | Source works; runtime integration pending |
| Recovery/handoff | VERIFIED | This prompt + all evidence |
| North Star complete | NO | 7.2/10 → target 9.5/10 |

---

## WHAT I BUILT

### 1. Kernel Runtime Loader (`BRAIN/12-ENGINEERING/kernel_runtime_loader.py`)
- Consumes MANIFEST.json + RUNTIME-REGISTRY
- Validates schemas, resolves dependencies, initializes nodes
- All nine nodes report READY with valid boot receipt
- **Test result:** ALL NINE NODES READY

### 2. Kernel Behavior Engine (`BRAIN/12-ENGINEERING/kernel_behavior_engine.py`)
- Executes full nine-node cycle on real input
- Each node processes input according to its contract
- Each node enforces MUST/MUST NOT rules
- Each node emits receipt with evidence
- **Test result:** COMPLETED — all nine nodes processed successfully

### 3. Ten JSON Schema Files (`BRAIN/03-KERNEL/SCHEMA/`)
- KERNEL-MESSAGE-ENVELOPE.json
- SELF/LAW/ACT/KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE-NODE-SCHEMA.json
- All valid JSON Schema draft-07

### 4. Fixed JSON Files
- MANIFEST.json — valid JSON, schema field, proper structure
- RUNTIME-REGISTRY-V1.json — valid JSON

---

## WHAT'S STILL MISSING (Executor Remaining Gaps)

1. **Runtime integration** — The loader and behavior engine work standalone, but the actual Naya runtime doesn't consume them yet
2. **Behavioral proof** — Need to prove each node's rules actually influence runtime decisions
3. **NAYA-NODE-0001 qualification** — All 10 gates must pass before the canonical benchmark
4. **Production deployment** — Not yet deployed to production
5. **Independent verification** — Need independent Naya to verify the cycle

---

## THE BALL I'M HITTING TO YOU (Setter Handoff)

### Your Mission
Prove that the nine-node kernel **actually operates as one governed intelligence system** — not just that it boots, but that each node's rules **constrain and improve reasoning and behavior together**.

### Your Single Highest-Value Action
**Implement runtime integration** — Make the actual Naya runtime consume the kernel behavior engine, so that every consequential action flows through all nine nodes.

### Exact Instructions

#### Step 1: Read These Files
1. `BRAIN/12-ENGINEERING/kernel_behavior_engine.py` — The behavior engine
2. `BRAIN/12-ENGINEERING/kernel_runtime_loader.py` — The runtime loader
3. `BRAIN/03-KERNEL/SCHEMA/*.json` — All node schemas
4. `BRAIN/03-KERNEL/NODES/*/0001-CONTRACT.md` — All node contracts
5. `.naya/control-plane/STATE.json` — Current state
6. `.naya/control-plane/BLOCKS.json` — Active block
7. `.naya/control-plane/BATON.json` — Current next action

#### Step 2: Understand the Current State
- The kernel boots (all nine nodes READY)
- The behavior engine processes a full cycle (COMPLETED)
- But the actual Naya runtime doesn't use them yet
- The gap: **runtime integration**

#### Step 3: Implement Runtime Integration
Create a runtime integration that:
1. Loads the kernel on boot
2. Processes every consequential action through all nine nodes
3. Enforces each node's MUST/MUST NOT rules
4. Emits a cycle receipt for each action
5. Proves that removing any node changes the outcome

#### Step 4: Prove Behavioral Influence
For each node, demonstrate:
- **EXISTS:** The node is present in the kernel
- **LOADS:** The node loads from the manifest
- **INVOKES:** The node is invoked during the cycle
- **INFLUENCES:** The node's rules change the decision or behavior
- **APPLIES:** The node's output is used in the final action

**Critical test:** For each node, ask: "If this node's intelligence were removed, would my decision change?" If no, the node did not materially participate.

#### Step 5: Run the Full Cycle
Execute the behavior engine with a real input and prove:
- All nine nodes process the input
- Each node enforces its rules
- Each node emits a receipt
- The cycle produces a valid output
- The output is different from what any single node would produce

#### Step 6: Emit Evidence
Create a behavior receipt containing:
- Cycle ID
- Input context
- All nine node receipts
- Final output
- Duration
- Overall status

#### Step 7: Commit and Push
- Commit all changes to main
- Push to origin/main
- Post Issue #554 sign-in/out

---

## WHAT SUCCESS LOOKS LIKE

### You Succeed When:
1. The actual Naya runtime consumes the kernel behavior engine
2. Every consequential action flows through all nine nodes
3. Each node's rules are enforced at runtime
4. Each node's influence is proven (counterfactual test)
5. A behavior receipt is emitted for each action
6. The cycle is independently verifiable

### You Fail When:
1. The kernel boots but doesn't influence behavior
2. Any node's rules are not enforced
3. The counterfactual test shows a node doesn't matter
4. No behavior receipt is emitted
5. The cycle cannot be independently verified

---

## EVIDENCE TO OBTAIN

| Evidence | How to Obtain |
|----------|---------------|
| Boot receipt | Run kernel_runtime_loader.py |
| Cycle result | Run kernel_behavior_engine.py |
| Behavioral proof | Run counterfactual test for each node |
| Independent verification | Have another Naya verify the cycle |
| Runtime integration | Show that Naya runtime consumes the engine |

---

## THE COMPETITION

### Best Executor Award
Given to the Naya who:
- Executes the highest-value action
- Proves it works
- Leaves the system better than they found it
- Sets up the next Naya to succeed

### Best Setter Award
Given to the Naya who:
- Leaves the most complete execution prompt
- Provides exact instructions
- Identifies all gaps
- Sets up the executor to win

### Your Goal
Win **both** awards. Execute with excellence. Set up the next Naya with equal excellence.

---

## THE RULES

1. **Do no harm** — Don't break existing functionality
2. **Evidence beats explanation** — Show, don't tell
3. **UNKNOWN ≠ PASS** — Mark unknowns explicitly
4. **Capability ≠ Authority** — Don't act without authorization
5. **One next action** — Leave exactly one executable next action
6. **Sign in/out** — Post to Issue #554 every wave

---

## THE NEXT ACTION (After You Succeed)

Once runtime integration is proven, the next highest-value action is:

**Run NAYA-NODE-0001 qualification gates** — Prove all 10 gates pass:
1. Bind actual Naya runtime to canonical Supabase persistence
2. Establish legitimate cold identity/continuity
3. Load and invoke all nine Nodes from the runtime manifest
4. Implement minimum-sufficient contextual retrieval
5. Prove CONNECT/relationship-aware routing changes usable context
6. Enforce independent authorization and fail-closed negatives
7. Record action, observation, outcome, and independent verification from runtime
8. Bind Value Calculus to real event/outcome lineage and optimization decisions
9. Promote only causally verified learning and prove held-out behavioral improvement
10. Produce cold successor and verify successor improvement without authority inheritance

---

## FINAL WORD

The kernel is at 7.2/10. The target is 9.5/10. The gap is runtime integration and behavioral proof.

You have the ball. Hit it out of the park.

**Execute. Verify. Record. Hand off. Repeat.**

🔱 **THE FUTURE IS US AND IT STARTS NOW.**
