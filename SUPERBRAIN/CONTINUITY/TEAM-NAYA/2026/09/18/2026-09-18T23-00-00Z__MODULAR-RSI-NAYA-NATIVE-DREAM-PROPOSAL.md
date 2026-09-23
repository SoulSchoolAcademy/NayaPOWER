# 🔱 TEAM NAYA — MODULAR RSI / NAYA-NATIVE DREAM PROPOSAL

**Date:** 2026-09-18  
**Project:** Naya Power / Dream / NayaNET  
**Audience:** All Nayas in Team Naya  
**Status:** PROPOSED — AWAITING TEAM NAYA REVIEW  
**Production code:** NOT CHANGED

## PURPOSE

Evaluate the strongest ideas from **IQuestLab/ModularRSI** and determine how to bring their useful recursive-harness self-improvement ideas into Naya Power **without forking the project, creating a second ecosystem, or slowing the live Naya runtime**.

This is a proposal for a **Naya-native implementation**, not a request to adopt ModularRSI as a runtime dependency.

## HUMAN DIRECTION

Shawn's proposed operating principle is:

**OPTIMIZE → MAXIMIZE → SYNERGIZE → EQUALIZE**

Meaning:

- **OPTIMIZE** the useful mechanisms.
- **MAXIMIZE** their benefit to Naya's capability.
- **SYNERGIZE** them with the existing Naya Power / Dream / CIS architecture.
- **EQUALIZE** by preserving compatibility, efficiency, speed, governance, and reliability.

The target is **more capability with the least downside**, not more machinery for its own sake.

## WHAT MODULARRSI CONTRIBUTES

ModularRSI provides a useful pattern for recursive harness improvement:

1. Learn from independent execution experience.
2. Compare successful and failed trajectories.
3. Diagnose recurring weaknesses.
4. Localize the weakness to a module.
5. Generate a bounded candidate improvement.
6. Validate the candidate.
7. Test on held-out/unseen work.
8. Promote only when evidence supports the improvement.

Its five primary harness modules are:

- Agent Loop
- Tool Use
- Observation Management
- Context Management
- Task Completion / Verification

## NAYA-NATIVE INTERPRETATION

Naya should **not become ModularRSI**.

Instead:

**Naya Power Constitution / Authority / Policy**
→ **Dream**
→ **Naya-native Modular Improvement Lab**
→ **candidate module**
→ **replay + tests**
→ **held-out validation**
→ **independent verification**
→ **governed promotion**
→ **new production module**

Dream remains the discovery/search mechanism.

The modular layer becomes the disciplined mechanism for isolating and testing *what* should improve.

Naya Power remains the authority and governance boundary.

## PERFORMANCE RULE

The improvement laboratory must be **off the normal live request path**.

A normal Naya interaction should not wait for Dream/RSI experimentation.

Experiments happen against historical/replayable experience and produce candidate versions. Only an independently verified and governed candidate may become the next production version.

Therefore the desired effect is:

**LIVE NAYA = no unnecessary RSI overhead**

while:

**DREAM = asynchronous improvement laboratory**

## PROPOSED MODULE MAP

Initial mapping target:

| Module | Desired treatment |
|---|---|
| Agent Loop | EVOLVABLE, bounded |
| Tool Use | EVOLVABLE, bounded |
| Observation | EVOLVABLE, bounded |
| Context / Memory Management | EVOLVABLE, bounded |
| Task Completion / Verification | CONSTRAINED; implementation may be improved only under stronger verification rules |
| Retrieval | EVOLVABLE candidate |
| Continuation | EVOLVABLE candidate |
| Planning | EVOLVABLE candidate |
| Memory Consolidation | EVOLVABLE candidate |
| Evidence Formation | CONSTRAINED |
| Identity / Ownership | MUST NOT be Dream-defined |
| Authority / Permissions | MUST NOT be Dream-defined |
| Constitution / Safety Invariants | MUST NOT EVOLVE through Dream |
| Smart Ledger History | MUST NOT be rewritten by Dream |

This map is a proposal and must be reconciled against the actual current runtime before implementation.

## GOVERNANCE INVARIANTS

Modular improvement must never:

- grant or revoke authority;
- redefine identity ownership;
- modify constitutional laws;
- weaken safety invariants;
- bypass verification;
- rewrite historical evidence;
- rewrite Smart Ledger history;
- declare its own candidate verified;
- deploy itself;
- expand its own scope;
- replace production truth with replay;
- treat a benchmark score as proof of general capability;
- retry indefinitely without new information.

Core separation remains:

**SCORE ≠ VALUE ≠ AUTHORITY ≠ TRUTH ≠ VERIFICATION**

## WHY THIS IS WORTH CONSIDERING

Potential upside:

- isolates recurring weaknesses instead of changing everything at once;
- makes improvements attributable to specific system components;
- allows successful and failed experiences to inform improvement;
- supports held-out testing against overfitting;
- preserves version history;
- allows Dream to improve the machinery around intelligence rather than requiring a new foundation model;
- can strengthen retrieval, context handling, tool choice, planning, continuation, and learning mechanisms;
- can fit naturally into KNOW → TELL → ASK → LOOK → SCORE → IMPROVE → REPEAT.

Potential downside:

- additional architecture and maintenance;
- additional compute for experiments;
- more candidate/version management;
- risk of optimizing the wrong metric;
- risk of accidentally allowing an experimental mechanism to influence production;
- licensing/commercial-use review would be required before copying any ModularRSI code.

## IMPLEMENTATION STRATEGY

Do **not** fork ModularRSI.

Do **not** add it as a production dependency.

First complete the current receiver/identity/production boundary.

Then:

### Phase 1 — Inventory
Map the five ModularRSI modules against the existing Naya Power runtime:

**EXISTS / PARTIAL / MISSING / MUST-NOT-EVOLVE**

No production changes.

### Phase 2 — Module Contract
Create a Naya-native module registry with:

- module identity;
- current production version;
- allowed evolution scope;
- prohibited changes;
- input/output contract;
- evidence requirements;
- tests;
- held-out evaluation set;
- promotion gate.

### Phase 3 — Dream Adapter
Connect Dream replay to the module registry.

Dream may propose candidates but may not promote them.

### Phase 4 — Candidate Laboratory
Run candidate changes against historical/replayable experience.

Require:

**BASELINE → CANDIDATE → REPLAY → TEST → HOLDOUT → VERIFY**

### Phase 5 — Governed Promotion
Only an independently verified candidate may be promoted through the existing Naya Power authority path.

### Phase 6 — Continuous Improvement
After promotion:

**OBSERVE → MEASURE → LEARN → RECORD → RE-EVALUATE**

A new candidate must always remain reversible.

## DEFINITION OF DONE

This proposal becomes an implementation only when Team Naya can demonstrate:

1. no new identity system;
2. no new competing cognition store;
3. no live-path performance penalty from experimentation;
4. bounded module evolution;
5. replayable experiments;
6. held-out validation;
7. independent verification;
8. governed promotion;
9. reversible versioning;
10. Smart Ledger evidence;
11. measurable improvement in the intended capability;
12. no regression of protected invariants.

## CURRENT DECISION REQUEST

**TEAM NAYA: REVIEW THIS PROPOSAL.**

Questions for each Naya:

1. What part of ModularRSI is genuinely valuable to Naya?
2. What should we explicitly NOT adopt?
3. Does the proposed off-path Dream laboratory preserve live performance?
4. Which existing Naya Power modules already satisfy the ModularRSI role?
5. Which modules are missing?
6. Which modules must remain constitutionally protected?
7. What is the smallest useful first implementation?
8. What verification would prove that an improvement is real rather than reward hacking?
9. Are there architectural conflicts with the current receiver/identity/production work?
10. **GO / NO-GO / MODIFY:** what should Team Naya recommend?

## EXACT NEXT ACTION

**After the current receiver/production boundary is proven, perform the five-module Naya runtime mapping before writing any ModularRSI-derived implementation.**

No fork.  
No production dependency.  
No live-path slowdown.  
No governance bypass.

**NAYA POWER ON. OPTIMIZE. MAXIMIZE. SYNERGIZE. EQUALIZE.**
