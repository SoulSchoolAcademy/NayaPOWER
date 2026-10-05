# AutoResearch Harness Deep Dive — What NayaPOWER Should Learn, Keep, and Reject

**Date:** 2026-10-01  
**Status:** RESEARCH / EXTERNAL INTELLIGENCE — NOT A NEW ARCHITECTURE  
**Prepared for:** NayaPOWER / NayaNET  
**Human Director:** Shawn Vibert  
**Canonical NayaPOWER base inspected:** `a726a8376559609a3620f948ec7bfcabdba50abb`  
**AutoResearch source snapshot inspected:** `karpathy/autoresearch@228791fb499afffb54b46200aca536f79142f117`

## Executive conclusion

AutoResearch is highly valuable to study, but it is **not a replacement for NayaPOWER, not a better governance system, and not a reason to fork or redesign the Nine-Node organism**.

Its strongest contribution is much narrower and very important:

> **A capable AI becomes dramatically more effective when the experimental world around it is made tiny, fixed, measurable, comparable, and easy to revert.**

AutoResearch compresses autonomous research into a small loop:

`BASELINE → MUTATE ONE BOUNDED SURFACE → RUN A FIXED-BUDGET EXPERIMENT → MEASURE ONE FROZEN EVALUATOR → KEEP IF BETTER / REVERT IF WORSE → REPEAT`.

NayaPOWER already has the broader and more governed architecture:

`RESOLVE → GATE → SCORE → COMPARE → SELECT → ACT/ESCALATE → OBSERVE → VERIFY → LEDGER → LEARN → RECALIBRATE`

plus:

`OBSERVE → UNDERSTAND → PROPOSE → BUILD → TEST → VERIFY → LEARN → ADOPT → REUSE`.

The best synthesis is therefore:

> **Keep NayaPOWER's governance, authority, memory, evidence, SmartLedger, Value Calculus, cold-successor continuity, and Nine-Node ownership. Add AutoResearch-grade experimental compression inside the existing EVOLVE/self-optimization seam.**

The six external mechanics worth adopting are:

1. immutable evaluator contract;
2. explicit mutable surface;
3. mandatory frozen baseline;
4. bounded experiment resource envelope;
5. automatic keep/revert when evidence is decisive and authority permits;
6. search-stagnation / novelty redirect.

Everything else should be reconciled against existing NayaPOWER seams before implementation. No second brain, ledger, authority model, scorecard, or learning path is justified.

---

## 1. Sources reviewed

### Canonical / primary AutoResearch sources

- GitHub repository: https://github.com/karpathy/autoresearch
- README: https://github.com/karpathy/autoresearch/blob/master/README.md
- Agent program / harness instructions: https://github.com/karpathy/autoresearch/blob/master/program.md
- Frozen preparation/evaluator surface: https://github.com/karpathy/autoresearch/blob/master/prepare.py
- Mutable research target: https://github.com/karpathy/autoresearch/blob/master/train.py
- Explainer site supplied by Shawn: https://autoresearch.lol/#how-it-works

### Community evidence / proposals reviewed

These are **not canonical AutoResearch law**; they are useful evidence of real operating pressure and missing features users have noticed.

- Long-term memory / guidance-agent proposal: https://github.com/karpathy/autoresearch/issues/179
- Experiment memory + UCB1 exploration + early abort proposal: https://github.com/karpathy/autoresearch/issues/284
- Experiment novelty / repeated-search concern: https://github.com/karpathy/autoresearch/issues/613
- Permission / autonomous cloud-running friction: https://github.com/karpathy/autoresearch/issues/396
- Research integration / validation-process proposal: https://github.com/karpathy/autoresearch/issues/261

### NayaPOWER sources used for reconciliation

- `AGENTS.md`
- `NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md`
- `kernel/value_calculus.py`
- `.naya/NAYAPOWER-SYSTEM-AAA-SCORECARD-V1.md`
- `KNOWLEDGE/NAYAPOWER-IMPLEMENTATION-PLAN-V1.md`
- `KNOWLEDGE/NAYA POWER CONCEPT PART #6.md`
- `NAYA-ACTIVATION/CURRENT-REALITY/NEXT-ACTION.md`
- current Nine-Node kernel candidate PR #1216

---

## 2. What AutoResearch actually is

AutoResearch is deliberately small.

The canonical README says only three files really matter:

- `prepare.py` — fixed constants, data preparation, tokenizer, dataloader and evaluator; the agent is not supposed to modify it;
- `train.py` — the single mutable research file; architecture, optimizer, hyperparameters and training loop are fair game;
- `program.md` — human-authored instructions describing how the autonomous research agent should operate.

The research loop is intentionally simple:

1. establish the baseline;
2. modify `train.py`;
3. commit the experiment;
4. run the experiment for a fixed five-minute training budget;
5. read `val_bpb` and peak memory;
6. keep the commit if `val_bpb` improved;
7. reset if it did not;
8. record the experiment;
9. repeat until the human stops the process.

The frozen metric is validation bits-per-byte (`val_bpb`), where lower is better.

The fixed five-minute budget is important because candidate systems cannot win simply by training for longer. On one GPU, the README estimates roughly 12 experiments per hour and around 100 over a human sleep period.

This is the real harness:

```
ONE OBJECTIVE
+ ONE FROZEN EVALUATOR
+ ONE MUTABLE SURFACE
+ ONE COMPARABLE BUDGET
+ ONE KEEP / DISCARD DECISION
+ FAST REVERSIBILITY
= HIGH AUTONOMOUS EXPERIMENT THROUGHPUT
```

---

## 3. What the system is optimizing

AutoResearch is excellent when the problem can be reduced to:

> **Find code changes that improve one objective under a fixed resource budget.**

That is a narrower problem than NayaPOWER.

AutoResearch does not attempt to solve, in its core loop:

- user authority;
- privacy;
- owner isolation;
- consent;
- conflicting principals;
- epistemic truth states;
- production authorization;
- multi-domain risk;
- causal learning across humans/projects;
- network-level memory;
- human-worth / reputation boundaries;
- cold successor reconstruction from governed intelligence.

That is not a criticism. It is why AutoResearch can be so compact.

The correct lesson is:

> **Do not compare the systems as if they have the same job. Compare the experimental mechanics they use for the overlapping self-optimization problem.**

---

## 4. Claim check: “100× cheaper”

The canonical AutoResearch repository supports a claim of **high experiment throughput**, not a universal claim of “100× cheaper work.”

What is directly supported:

- fixed five-minute experiments;
- roughly 12 experiments/hour in the intended environment;
- roughly 100 experiments overnight;
- low human supervision after setup;
- automatic discard/revert of regressions.

What was **not established from the canonical source**:

- a universal 100× cost reduction;
- 100× cheaper coding;
- 100× cheaper AI-agent operation;
- 100× lower GPU cost.

The right interpretation is:

> **AutoResearch can produce a very large reduction in human orchestration cost and dramatically increase experiments per unit of human attention. Exact monetary/compute savings are workload-dependent and must be measured, not repeated as a universal multiplier.**

NayaPOWER should preserve that truth boundary.

---

## 5. Why AutoResearch is effective

### 5.1 The evaluator is outside the agent's mutation surface

The agent changes `train.py`, but not `prepare.py` or the evaluator.

This is a powerful anti-reward-hacking boundary.

The agent cannot claim improvement merely by changing the measurement that judges it.

**Naya lesson:** During a governed experiment campaign, freeze the evaluator identity and hash separately from the mutable implementation.

### 5.2 Every experiment starts from a comparable baseline

The initial run establishes current performance before optimization begins.

**Naya lesson:** We already have the stronger baseline-relative value formula:

`ΔV(a|b)=PV(a)-PV(b)`.

The missing operational improvement is to require a **frozen baseline receipt** at campaign start.

### 5.3 Resource use is normalized

Every experiment has a fixed wall-clock budget.

This makes competing changes comparable and strongly discourages improvements that only come from consuming unbounded resources.

**Naya lesson:** Add a bounded resource envelope to experiments: time, agent tokens, compute, external calls, diff size, changed files, and any relevant infrastructure cost.

### 5.4 Mutation scope is tiny

One editable file makes the agent's search space easier to reason about and makes diffs easy to review and revert.

**Naya lesson:** Every self-optimization campaign should explicitly state `mutable_paths` / `mutable_operations` and `immutable_paths` / `immutable_contracts`.

### 5.5 Revert is first-class

A failed experiment is cheap because the branch can return to the previous best state.

**Naya lesson:** Promotion and rollback should be built into the experiment contract rather than treated as manual cleanup.

### 5.6 The human programs the organization, not each experiment

`program.md` acts like a lightweight organizational program.

The human does not need to approve experiment 17, 18, 19, etc. after a bounded campaign begins.

**Naya lesson:** Naya should compile existing law, objective, evaluator, scope, budget and stop conditions into a compact campaign projection so the worker does not need the Human Director to project-manage each step.

---

## 6. What NayaPOWER already does better

### 6.1 Governance and authority

NayaPOWER explicitly separates:

`CAPABILITY ≠ AUTHORITY`.

LAW decides whether an action may execute. ACT does not manufacture permission. A score cannot bypass a hard gate.

AutoResearch's default loop is intentionally much looser because its sandbox is narrow.

**Decision:** keep NayaPOWER.

### 6.2 Truth and evidence

NayaPOWER preserves:

`UNKNOWN ≠ PASS`  
`IMPLEMENTED ≠ VERIFIED`  
`VERIFIED ≠ PRODUCTION-PROVEN`.

AutoResearch primarily cares whether the experiment metric improved and whether the code ran.

**Decision:** keep NayaPOWER's proof ladder.

### 6.3 Multi-objective value

AutoResearch has one primary scalar objective.

NayaPOWER has:

- hard gates;
- Q = decision soundness;
- baseline-relative ΔV;
- conservative value;
- tail risk;
- evidence/confidence floors;
- Pareto comparison;
- human burden and simplicity;
- authority state;
- delayed verification.

**Decision:** do not replace Value Calculus V2.1 with a single metric.

### 6.4 Memory and successor continuity

AutoResearch's simple history/log pattern is enough for short bounded runs, but community issues already identify long-session memory loss and repeated local exploration as limitations.

NayaPOWER has a much richer intended path:

`EVENT → INTELLIGENT BLOCK → LINEAGE → GRAPH → INDEX → RETRIEVAL → APPLY → OUTCOME → VERIFY → LEARN → SUCCESSOR`.

**Decision:** keep NayaPOWER's memory architecture.

### 6.5 SmartLedger

AutoResearch's experiment log is intentionally lightweight.

NayaPOWER needs stronger receipts because decisions can cross authority, users, systems and time.

**Decision:** use AutoResearch-like simplicity in the human view, but preserve full SmartLedger evidence behind it.

### 6.6 Independent verification

AutoResearch's research agent largely participates in its own experiment loop.

NayaPOWER explicitly gives VERIFY an independent role.

**Decision:** do not weaken separation-of-duty.

---

## 7. Naya assessment scorecard

These scores are an internal architectural assessment, not claims published by AutoResearch.

| Dimension | AutoResearch | NayaPOWER | Interpretation |
|---|---:|---:|---|
| Objective clarity | 9.8 | 9.7 | AutoResearch is exceptionally narrow; Naya has broader explicit objectives |
| Bounded mutation | 10.0 | 8.2 | AutoResearch's single-file scope is cleaner today |
| Fair evaluation | 9.2 | 9.3 | Auto freezes evaluator/time; Naya adds independent verification |
| Iteration efficiency | 9.7 | 6.8 | Biggest current advantage for AutoResearch |
| Evidence/provenance | 7.8 | 9.3 | Naya receipts/lineage are stronger |
| Long-term memory | 5.5 | 8.7 | Naya architecture is materially stronger |
| Governance/authority | 3.5 | 9.8 | Different problem scope; Naya is much stronger |
| Anti-Goodhart / risk | 5.5 | 9.5 | Naya's gate/value/risk separation is stronger |
| Independent verification | 4.0 | 9.2 | Strong Naya advantage |
| Cold successor / continuity | 4.5 | 7.2 | Naya still incomplete but structurally stronger |

Approximate score under the **NayaPOWER objective**:

- AutoResearch: **~6.9 / 10**
- NayaPOWER: **~8.9 / 10**

Approximate score only for **bounded autonomous experiment-loop execution**:

- AutoResearch: **~9.7 / 10**
- current NayaPOWER: **~6.8 / 10**

That narrow gap is the value of this research.

---

## 8. The six mechanics NayaPOWER should adopt

### 8.1 Immutable evaluator contract

For each experiment campaign, freeze:

- evaluator identity;
- evaluator code/hash;
- metric definition;
- acceptance version;
- risk/authority profile version where applicable.

The mutable implementation must not be able to edit the thing grading it.

### 8.2 Explicit mutable surface

Every campaign should declare exactly what may change.

Example:

```yaml
mutable:
  paths:
    - kernel/retrieval_ranker.py
  operations:
    - edit
    - test
immutable:
  paths:
    - kernel/value_calculus.py
    - NAYANODE/constitutional-law.md
```

The exact schema should reuse existing Naya contracts rather than inventing a parallel policy engine.

### 8.3 Mandatory frozen baseline

Before mutation:

```
baseline_sha
baseline_environment
baseline_test_result
baseline_metric
baseline_cost
baseline_latency
evaluator_hash
```

No candidate is an improvement without a reproducible baseline.

### 8.4 Experiment resource envelope

A campaign should bound relevant resources:

```
wall_time
agent_tokens
compute
external_calls
changed_files
diff_size
network_calls
financial_cost
```

This creates honest efficiency comparisons.

### 8.5 Automatic keep/revert within standing authority

If:

- LAW permits;
- scope is bounded;
- evaluator is intact;
- result is independently verified;
- candidate clearly dominates the baseline under V2.1;
- rollback is available;

then the machine should not need a new human round-trip to keep/revert a low-consequence experimental candidate.

Human authority remains required where existing Naya law requires it.

### 8.6 Stagnation / novelty redirect

This is the clearest net-new control identified by the review.

NayaPOWER currently has strong value/verification logic, but no clearly canonical experiment-search controller that notices repeated local search.

Candidate rule:

```
IF recent experiment window shows:
  - no material verified ΔV improvement, OR
  - repeated mutation of the same search dimension, OR
  - repeated rediscovery of rejected patterns
THEN:
  SEARCH_STATE = STAGNATING
  retrieve historical near-misses / rejected patterns
  widen candidate generation
  force exploration of a materially different dimension
```

This should live inside the existing LEARN → EVOLVE optimization path, not as another agent brain.

---

## 9. High-value optional mechanics

These were not part of the canonical six, but are worth testing later.

### Early abort

If a bounded candidate is already clearly worse than the baseline by a predeclared threshold before the full budget is consumed, terminate early.

Benefits:

- lower compute waste;
- higher experiment throughput;
- faster feedback.

Caution: an early signal can be misleading. The abort criterion must be predeclared, evidence-backed and versioned.

### Exploration vs. exploitation

Community proposal #284 suggests UCB1-style dimension selection.

NayaPOWER should **not blindly adopt UCB1**, but the underlying principle is sound:

> repeatedly exploiting the same successful category can trap an autonomous optimizer in a local optimum.

A Naya campaign can track experiment dimensions and deliberately balance:

- exploit known promising directions;
- explore under-tested directions.

Use evidence to choose the exact search policy.

### Separate strategic context from mechanical execution

Community issue #298 argues that verbose experiment execution can destroy the primary agent's context.

This aligns with Team Naya specialist delegation:

- Naya/integrator owns objective, law, campaign state and ranking;
- bounded specialist runs mechanical experiment;
- specialist returns compact evidence;
- integrator decides keep/revert.

This is already consistent with NayaPOWER and may be strengthened without new architecture.

---

## 10. What not to copy

### Do not adopt “NEVER STOP” as a global Naya law

AutoResearch's `program.md` says once experimentation starts, the agent should not keep asking the human whether to continue.

That is appropriate for its bounded sandbox.

NayaPOWER's stronger law is:

> Continue all safe, authorized, evidence-supported work without unnecessary human orchestration. Stop only the blocked/consequential action at a genuine authority, safety, privacy, credential, money or evidence boundary. Continue unrelated authorized work.

### Do not adopt one scalar metric for general intelligence

One metric works for the narrow benchmark.

For human systems it creates Goodhart risk.

Naya keeps:

`LAW → Q → VALUE → RISK → AUTHORITY → VERIFY`.

### Do not use Git history as the whole memory system

Git is excellent project evidence but is not sufficient to represent all intelligence, applicability, outcome, learning and privacy semantics.

### Do not build a parallel AutoResearch subsystem

The correct target is:

`NayaPOWER EVOLVE + bounded Experiment Campaign profile`.

### Do not copy code merely because it is open source

The README states MIT, but the root snapshot inspected did not include a conventional `LICENSE` file and GitHub's repository metadata did not expose a detected license. There is no reason to import code for the current objective anyway.

Learn the pattern. Keep the codebase separate unless a later bounded need justifies reuse and license hygiene is verified.

---

## 11. Proposed NayaPOWER synthesis

The desired experimental heartbeat is:

```
HUMAN / SYSTEM OBJECTIVE
↓
FREEZE BASELINE
↓
FREEZE EVALUATOR
↓
DECLARE MUTABLE / IMMUTABLE ENVELOPE
↓
DECLARE RESOURCE BUDGET
↓
LAW
↓
GENERATE CANDIDATE
↓
ACT
↓
BOUNDED EXPERIMENT
↓
EARLY ABORT IF PREDECLARED FAILURE CONDITION FIRES
↓
OBSERVE
↓
INDEPENDENT VERIFY
↓
DECISION VALUE CALCULUS
↓
KEEP / REVERT / READ_MORE / ASK
↓
SMARTLEDGER RECEIPT
↓
LEARN
↓
STAGNATION / NOVELTY CHECK
↓
EVOLVE
↓
NEXT EXPERIMENT
↓
PERIODIC COLD SUCCESSOR RECONSTRUCTION
```

This is not a new brain.

Nine-Node placement remains:

- **SELF** — campaign objective, baseline, current state;
- **LAW** — mutable envelope, permissions, hard gates, budget authority;
- **ACT** — performs the bounded mutation/experiment;
- **KNOW** — retrieves prior experiments and applicable lessons;
- **PROVE** — preserves execution/evidence claims;
- **CONNECT** — connects related experiments, dimensions, dependencies, near-misses and supersessions;
- **VERIFY** — independently evaluates output and recomputes result;
- **LEARN** — identifies verified patterns and failed/search-stagnation lessons;
- **EVOLVE** — proposes/promotes the next bounded candidate within governance.

---

## 12. Recommended Experiment Campaign projection

This should be a compact projection over existing contracts, not a new source of truth.

Candidate fields:

```yaml
campaign_id:
objective:
baseline:
  sha:
  metrics:
  environment:
evaluator:
  path:
  hash:
  version:
mutable_surface:
  paths:
  operations:
immutable_surface:
  paths:
resource_envelope:
  wall_time:
  agent_tokens:
  compute:
  external_calls:
  max_changed_files:
  max_diff_size:
metrics:
  primary:
  guard_metrics:
decision_profile:
  value_calculus_version:
  risk_policy_version:
keep_rule:
revert_rule:
early_abort_rule:
stagnation_rule:
authority_basis:
stop_conditions:
ledger_receipt_policy:
cold_successor_check:
```

The fields must ultimately map onto existing LAW / Value / SmartLedger / LEARN / EVOLVE ownership.

---

## 13. Proof required before general use

Do not generalize this pattern merely because it sounds good.

Prove one low-risk experiment:

```
BASELINE
→ FROZEN EVALUATOR
→ BOUNDED CANDIDATE
→ RUN
→ INDEPENDENT VERIFY
→ VALUE COMPARISON
→ KEEP OR REVERT
→ SMARTLEDGER RECEIPT
→ COLD REREAD
```

Acceptance evidence:

- exact source SHA;
- exact baseline;
- evaluator hash;
- allowed mutation set;
- resource budget;
- candidate diff;
- experiment result;
- independent verifier output;
- V2.1 decision receipt;
- keep/revert result;
- preserved history of discarded attempt;
- cold successor can explain the decision without original conversation context.

Only after that should the experiment-campaign profile expand.

---

## 14. Decision

### Do now

- preserve this research as reusable NayaPOWER intelligence;
- keep references to AutoResearch and the useful community issues;
- use the six mechanics as design inputs;
- add a future bounded Governed Experiment Campaign lane to the existing EVOLVE/self-optimization seam;
- do not disturb current Nine-Node proof work to rush this in.

### Do not do now

- do not fork AutoResearch;
- do not import AutoResearch code;
- do not create another optimization engine;
- do not replace Decision Value Calculus;
- do not replace SmartLedger;
- do not weaken human authority;
- do not make current Nine-Node proof dependent on this external research.

---

## 15. Highest-value lesson

The most reusable lesson is not a model-training trick.

It is a systems-design law:

> **Do not make the agent carry complexity the environment can remove.**

When an experiment has:

- a frozen baseline;
- a frozen evaluator;
- a small mutation surface;
- a known budget;
- an objective result;
- automatic rollback;

the AI has fewer ways to misunderstand the problem, overfit the process, manufacture a win, or waste human attention.

NayaPOWER already has the harder governance and intelligence architecture.

The opportunity is to make the **experimental container around Naya as clean as AutoResearch makes the container around its research agent**.

That is how we gain AutoResearch's speed without giving up NayaPOWER's trustworthiness.

---

## 16. Final synthesis

**AutoResearch contributes the experimental heartbeat.**

**NayaPOWER contributes the governed brain.**

The desired combination is:

```
AUTORESEARCH-GRADE EXPERIMENTAL COMPRESSION
+
NAYAPOWER LAW
+
NAYAPOWER VALUE CALCULUS
+
NAYAPOWER SMARTLEDGER
+
NAYAPOWER MEMORY
+
NAYAPOWER VERIFY
+
NAYAPOWER LEARN / EVOLVE
+
NAYAPOWER COLD SUCCESSOR
=
GOVERNED SELF-OPTIMIZATION
```

The architecture does not need to be replaced.

It needs to become easier to experiment inside.

**Preserve what works. Make the smallest effective change. Prove one campaign before scaling it.**
