# NayaPOWER Brain — File Inventory & Race Readiness V1

> **Reconciliation banner (2026-09-30):** this document is the **2026-09-27 hardening-pass inventory (77-file world)**. It is preserved as historical evidence — its per-file table, readiness percentages, and the 8.4/10-adjacent scoring below describe that pass, not the current tree. The current machine-verified inventory is **157 files** across 15 domains + ROOT (see `BRAIN/REAL-TREE.json`, regenerated from live Git by `tools/regenerate_brain_index.py`). Do not read the table below as a current file list.

**Review date:** 2026-09-27 — hardening pass 2  
**Repository:** SoulSchoolAcademy/NayaPOWER  
**Scope:** `BRAIN/` on `main`  
**Inventory count at time of writing:** 77 files in the BRAIN tree at the 2026-09-27 pass (directories excluded). Current count: **157** (see reconciliation banner above).  
**Purpose:** Turn the Brain into an executable work inventory: what exists, what is ready, what is blocked by proof, what needs hardening, and what another Naya should do next.

## Readiness law

**Artifact readiness is not living-system proof.** A file can be 100% ready for its semantic role while the system that consumes it remains unproven. The percentage below is therefore **file-role readiness**, not a claim that NayaPOWER is race-qualified.

Race entry still requires the whole system to pass the canonical cold/runtime/behavioral proof ladder. A single critical runtime or proof gap can block race entry even when most files are ready.

## Executive scorecard

| Area | File count | Role readiness | Race implication |
|---|---:|---:|---|
| SPEC | 7 | 88% | Strong; machine-checkable type/naming hardening remains. |
| GOVERNANCE | 3 | 88% | Strong; runtime enforcement must be proven. |
| ARCHITECTURE | 3 | 92% | Strong boundaries; automate dependency parity. |
| KERNEL | 15 | 86% | Manifest/registry exist; actual runtime consumption remains open. |
| INTELLIGENCE | 18 | 89% | Graph/object structure is strong; live graph behavior remains open. |
| MEMORY | 2 | 89% | Contract ready; application cold continuity remains open. |
| PROOF | 2 | 90% | Contract ready; independent production evidence remains open. |
| LEARNING | 2 | 90% | Promotion law ready; held-out behavioral effect remains open. |
| SUCCESSION | 2 | 90% | Contract ready; independent successor improvement remains open. |
| EVOLUTION | 2 | 90% | Governance law ready; governed self-improvement remains proof work. |
| INTERFACES | 2 | 90% | Channel boundary ready; Hub integration remains open. |
| KNOWLEDGE | 7 | 91% | Corpus and maps strong; object-level population remains partial. |
| ENGINEERING | 3 | 92% | Truth law strong; scorecard now becomes inventory anchor. |
| OPERATIONS | 2 | 94% | Execution doctrine strong. |
| ARCHIVE | 1 | 90% | Boundary clear. |
| ROOT | 5 | 95% | Tree receipts are synchronized; index/inventory linkage is current. |

**BRAIN artifact-role readiness: ~91% overall after this hardening pass.**  
**Whole-system race readiness: NOT YET QUALIFIED.**  
**Primary blocker:** convergence of the executable Nine-Node runtime with the canonical Supabase persistence/retrieval boundary on the canonical branch.

## Critical findings fixed in this pass

1. **Nine Node objects had empty relationship arrays** even though the canonical graph seed defined their relationships. All nine objects were updated to v1.1 and aligned to the graph seed with explicit incoming/outgoing relationship lineage.
2. **The file inventory/receipt is stale.** The current BRAIN tree has 77 files; `REAL-TREE.json` now records 75 counted files while excluding the two receipt files themselves.
3. **The runtime registry is not the runtime.** `MANIFEST.json` and `0003-RUNTIME-REGISTRY-V1.json` correctly define the machine contract, but main does not yet prove that the actual application entrypoint consumes them.
4. **The Brain documentation is ahead of executable convergence.** The BRAIN is coherent as a semantic substrate, but the race gate remains blocked until the nine-node runtime, canonical Supabase persistence, retrieval, authority, outcome, learning and successor loop are one verified executable lineage.

## File inventory

| Domain | File | Readiness | Status | Why / next work |
|---|---|---:|---|---|
| 00-SPEC | `0001-INTELLIGENT-GRAPH-AND-TREE-SPEC-V1.md` | 95% | READY | Graph/tree semantics are strong; runtime enforcement remains external proof. |
| 00-SPEC | `0002-TREE-AND-GRAPH-NAMING-LAW-V1.md` | 95% | HARDENED | Machine-checkable identity format, normalization, collision/non-reuse and validator law are now explicit. Runtime validator execution remains proof work. |
| 00-SPEC | `0003-REPRESENTATION-LAW-V1.md` | 95% | READY | Strong parity law; automatic parity proof still belongs in engineering. |
| 00-SPEC | `0004-KNOWLEDGE-POPULATION-SPEC-V1.md` | 95% | HARDENED | Canonical envelope, promotion gates, dispositions and rejection receipts are now explicit. Runtime population proof remains open. |
| 00-SPEC | `0005-TREE-V1.md` | 90% | READY | Canonical layer ordering is clear; runtime parity remains proof. |
| 00-SPEC | `0006-OBJECT-TYPES-V1.md` | 95% | HARDENED | Universal envelope and minimum semantic fields are defined for every registered type. Machine validator execution remains open. |
| 00-SPEC | `README.md` | 90% | READY | Navigation only; no material race blocker. |
| 01-GOVERNANCE | `0001-GOVERNANCE-CONTRACT-V1.md` | 90% | READY | Core authority/consent boundary is present; runtime enforcement is proof work. |
| 01-GOVERNANCE | `0002-PROMOTION-AND-REVOCATION-V1.md` | 95% | HARDENED | State-transition invariants, revocation/supersession receipts and fail-closed law are explicit. Runtime enforcement remains proof work. |
| 01-GOVERNANCE | `README.md` | 90% | READY | Navigation only. |
| 02-ARCHITECTURE | `0001-SYSTEM-BOUNDARIES-V1.md` | 95% | READY | Correctly separates substrate, interfaces, source control and persistence. |
| 02-ARCHITECTURE | `0002-DEPENDENCY-ORDER-V1.md` | 90% | READY | Correct ordering; needs automated dependency validation. |
| 02-ARCHITECTURE | `README.md` | 90% | READY | Navigation only. |
| 03-KERNEL | `0001-KERNEL-CONTRACT-V1.md` | 95% | READY | Clear universal input/output and fail-closed law. |
| 03-KERNEL | `0002-KERNEL-ACCEPTANCE-V1.md` | 95% | READY | Correctly separates structural through successor gates. |
| 03-KERNEL | `0003-RUNTIME-REGISTRY-V1.json` | 85% | BINDING BLOCKED | Registry is explicit and fail-closed; actual entrypoint is intentionally unresolved until source inspection identifies it. |
| 03-KERNEL | `MANIFEST.json` | 85% | BINDING BLOCKED | Nine IDs and runtime-binding contract are explicit; actual application consumption remains unproven. |
| 03-KERNEL | `NODES/ACT/0001-CONTRACT.md` | 85% | READY / PROOF PENDING | Semantic contract is clear; invocation proof pending. |
| 03-KERNEL | `NODES/CONNECT/0001-CONTRACT.md` | 85% | READY / PROOF PENDING | Semantic contract is clear; relationship/runtime proof pending. |
| 03-KERNEL | `NODES/EVOLVE/0001-CONTRACT.md` | 85% | READY / PROOF PENDING | Semantic contract is clear; successor/evolution proof pending. |
| 03-KERNEL | `NODES/KNOW/0001-CONTRACT.md` | 85% | READY / PROOF PENDING | Semantic contract is clear; canonical memory proof pending. |
| 03-KERNEL | `NODES/LAW/0001-CONTRACT.md` | 85% | READY / PROOF PENDING | Semantic contract is clear; runtime authority proof pending. |
| 03-KERNEL | `NODES/LEARN/0001-CONTRACT.md` | 85% | READY / PROOF PENDING | Semantic contract is clear; future behavior proof pending. |
| 03-KERNEL | `NODES/PROVE/0001-CONTRACT.md` | 85% | READY / PROOF PENDING | Semantic contract is clear; evidence runtime proof pending. |
| 03-KERNEL | `NODES/SELF/0001-CONTRACT.md` | 85% | READY / PROOF PENDING | Semantic contract is clear; cold identity proof pending. |
| 03-KERNEL | `NODES/VERIFY/0001-CONTRACT.md` | 85% | READY / PROOF PENDING | Semantic contract is clear; independent outcome proof pending. |
| 03-KERNEL | `README.md` | 90% | READY | Navigation only. |
| 04-INTELLIGENCE | `0001-FIRST-LIVING-NODE-SPEC-V1.md` | 90% | READY / PROOF PENDING | Excellent proof target; execution must use canonical runtime. |
| 04-INTELLIGENCE | `0001-INTELLIGENT-OBJECT-CONTRACT-V1.md` | 90% | READY | Required object questions are well defined. |
| 04-INTELLIGENCE | `0002-GRAPH-CONTRACT-V1.md` | 95% | HARDENED | Runtime query contract, filtering order and behavioral CONNECT acceptance are explicit. Live runtime proof remains open. |
| 04-INTELLIGENCE | `0003-INTELLIGENCE-LIFECYCLE-V1.md` | 95% | HARDENED | Durable transition receipts, truth-state separation and failure law are explicit. Runtime coverage remains open. |
| 04-INTELLIGENCE | `GRAPH/0001-KERNEL-GRAPH-SEED-V1.json` | 90% | READY / PROOF PENDING | Seed is explicit, provenance-bound and now aligned with node objects. |
| 04-INTELLIGENCE | `GRAPH/0002-KNOWLEDGE-TO-NODE-MAP-V1.json` | 90% | READY | Mapping is machine-readable; promotion remains incomplete. |
| 04-INTELLIGENCE | `GRAPH/README.md` | 90% | READY | Navigation only. |
| 04-INTELLIGENCE | `MASTER-INDEX.json` | 90% | READY | Core index is coherent; add automated parity check. |
| 04-INTELLIGENCE | `OBJECTS/NAYA-KERNEL-ACT.json` | 88% | ALIGNED / PROOF PENDING | Graph relationships now populated; runtime behavior still pending. |
| 04-INTELLIGENCE | `OBJECTS/NAYA-KERNEL-CONNECT.json` | 88% | ALIGNED / PROOF PENDING | Graph relationships now populated; runtime behavior still pending. |
| 04-INTELLIGENCE | `OBJECTS/NAYA-KERNEL-EVOLVE.json` | 88% | ALIGNED / PROOF PENDING | Graph relationships now populated; runtime behavior still pending. |
| 04-INTELLIGENCE | `OBJECTS/NAYA-KERNEL-KNOW.json` | 88% | ALIGNED / PROOF PENDING | Graph relationships now populated; runtime behavior still pending. |
| 04-INTELLIGENCE | `OBJECTS/NAYA-KERNEL-LAW.json` | 88% | ALIGNED / PROOF PENDING | Graph relationships now populated; runtime behavior still pending. |
| 04-INTELLIGENCE | `OBJECTS/NAYA-KERNEL-LEARN.json` | 88% | ALIGNED / PROOF PENDING | Graph relationships now populated; runtime behavior still pending. |
| 04-INTELLIGENCE | `OBJECTS/NAYA-KERNEL-PROVE.json` | 88% | ALIGNED / PROOF PENDING | Graph relationships now populated; runtime behavior still pending. |
| 04-INTELLIGENCE | `OBJECTS/NAYA-KERNEL-SELF.json` | 88% | ALIGNED / PROOF PENDING | Graph relationships now populated; runtime behavior still pending. |
| 04-INTELLIGENCE | `OBJECTS/NAYA-KERNEL-VERIFY.json` | 88% | ALIGNED / PROOF PENDING | Graph relationships now populated; runtime behavior still pending. |
| 04-INTELLIGENCE | `README.md` | 90% | READY | Navigation only. |
| 05-MEMORY | `0001-MEMORY-CONTINUITY-CONTRACT-V1.md` | 88% | PROOF PENDING | Contract is correct; cold continuity must be proven through the live application runtime. |
| 05-MEMORY | `README.md` | 90% | READY | Navigation only. |
| 06-PROOF | `0001-PROOF-CONTRACT-V1.md` | 90% | READY / PROOF PENDING | Truth-state ladder is correct; runtime evidence production remains open. |
| 06-PROOF | `README.md` | 90% | READY | Navigation only. |
| 07-LEARNING | `0001-LEARNING-CONTRACT-V1.md` | 90% | READY / PROOF PENDING | Correct learning promotion law; held-out future behavior is still required. |
| 07-LEARNING | `README.md` | 90% | READY | Navigation only. |
| 08-SUCCESSION | `0001-SUCCESSOR-CONTRACT-V1.md` | 90% | READY / PROOF PENDING | Authority non-inheritance is explicit; independent successor improvement remains open. |
| 08-SUCCESSION | `README.md` | 90% | READY | Navigation only. |
| 09-EVOLUTION | `0001-SELF-BUILDING-CONTRACT-V1.md` | 90% | READY / PROOF PENDING | Self-building law correctly requires authority and verification. |
| 09-EVOLUTION | `README.md` | 90% | READY | Navigation only. |
| 10-INTERFACES | `0001-CHANNEL-CONTRACT-V1.md` | 90% | READY / PROOF PENDING | Correct single-brain/many-doors boundary; live Hub integration remains open. |
| 10-INTERFACES | `README.md` | 90% | READY | Navigation only. |
| 11-KNOWLEDGE | `00-CONCEPT-CORPUS-REGISTER.md` | 95% | READY | Corpus is explicitly bounded at #1–#15. |
| 11-KNOWLEDGE | `0001-CANONICAL-DISTILLED-KNOWLEDGE-V1.md` | 90% | READY / PROOF PENDING | Strong synthesis; object-level promotion still incomplete. |
| 11-KNOWLEDGE | `0001-CONCEPT-TO-NODE-PROTOCOL-V1.md` | 95% | HARDENED | Candidate envelope, deterministic dispositions and rejection law are explicit. Population proof remains open. |
| 11-KNOWLEDGE | `0002-KNOWLEDGE-BANK-DISTILLATION-LEDGER-V1.md` | 90% | READY | Good lineage ledger; runtime population proof remains. |
| 11-KNOWLEDGE | `0003-KNOWLEDGE-POPULATION-MAP-V1.json` | 90% | READY | 15-source mapping is explicit and reconciled. |
| 11-KNOWLEDGE | `0004-HUMAN-AI-MACHINE-REPRESENTATION-V1.md` | 95% | READY | Strong parity contract. |
| 11-KNOWLEDGE | `README.md` | 90% | READY | Navigation only. |
| 12-ENGINEERING | `0001-ENGINEERING-TRUTH-LAW-V1.md` | 95% | READY | Correctly prevents implementation/test/deployment conflation. |
| 12-ENGINEERING | `0002-BRAIN-AAA-SCORECARD-V1.md` | 92% | UPDATED IN THIS PASS | Now needs to track this inventory and live-runtime convergence rather than stale pre-repair assumptions. |
| 12-ENGINEERING | `README.md` | 90% | READY | Navigation only. |
| 90-OPERATIONS | `0001-MAX-10-EXECUTION-QUEUE-V1.md` | 92% | UPDATED / ACTIVE | Correct next frontier is runtime convergence and behavioral proof. |
| 90-OPERATIONS | `0002-AAA-BRAIN-EXECUTION-PROMPT-V1.md` | 95% | READY | Strong execution law; should point directly to the file inventory. |
| 90-OPERATIONS | `README.md` | 90% | READY | Navigation only. |
| 99-ARCHIVE | `README.md` | 90% | READY | Correct archive boundary; historical material must not become canonical. |
| ROOT | `MASTER-MAP.md` | 92% | READY / PROOF PENDING | Strong navigation map; status is intentionally not a runtime claim. |
| ROOT | `NAYAPOWER-BRAIN-INDEX.json` | 92% | UPDATED REQUIRED | Should include this inventory and explicit runtime-convergence state. |
| ROOT | `README.md` | 90% | READY | Navigation only. |
| ROOT | `REAL-TREE.json` | 95% | REGENERATED | Structural receipt now records 75 counted BRAIN files (77 total minus the two receipt files). |
| ROOT | `REAL-TREE.md` | 95% | REGENERATED | Markdown receipt is synchronized to the current Git-tree receipt. |

## Completion categories for Nayas

### A — Kernel / Runtime Convergence
**Files:** 03-KERNEL + 12-ENGINEERING runtime surfaces.  
**Goal:** Make the canonical manifest/registry the actual runtime loader and bind that runtime to Supabase.  
**Why:** Until this is one executable lineage, the Brain can describe itself without being the thing that runs.

**Copy/paste assignment:**

> Inspect `BRAIN/03-KERNEL/MANIFEST.json` and `BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json`. Locate the actual application runtime entrypoint. Make the runtime load these canonical files directly. The runtime must use canonical Supabase persistence/retrieval, not SQLite/in-memory/file-backed state. Add a failing integration test proving manifest → runtime loader → canonical retrieval, then implement the smallest fix and verify it. Record commit SHA, test result, runtime version and proof boundary.

### B — Graph / CONNECT
**Files:** 04-INTELLIGENCE, especially GRAPH + OBJECTS + CONNECT contract.  
**Goal:** Turn the graph seed into the actual governed relationship/retrieval path.  
**Why:** CONNECT is where stored intelligence becomes context. The graph must change what is retrieved, not merely exist as JSON.

**Copy/paste assignment:**

> Starting from `BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json`, trace the live retrieval path to canonical Supabase Intelligent Blocks. Prove typed relationship expansion, owner/scope filtering, evidence/provenance filtering, temporal/supersession handling and minimum-sufficient-context selection. Add a held-out test where CONNECT changes the selected context and therefore changes later behavior. Do not create another graph store.

### C — Governance / ACT / PROVE / VERIFY
**Files:** 01-GOVERNANCE, 06-PROOF, relevant 03-KERNEL node contracts.  
**Goal:** Keep retrieval, authority, action, observation, outcome and verification separate.  
**Why:** Intelligence must never manufacture authority, and successful execution must never automatically become proof.

**Copy/paste assignment:**

> Trace RETRIEVE → AUTHORITY → ACT → OBSERVE → OUTCOME → VERIFY in the real runtime. Add fail-closed tests for missing, wrong-owner, wrong-scope, expired and revoked authority. Add a Causal Verification Object bound to the actual event/action/outcome/evidence lineage. Verify with an independent verifier identity. A successful action without a verified outcome must remain NOT_PROVEN.

### D — Learning / Compounding
**Files:** 07-LEARNING + KNOW/VERIFY/LEARN objects.  
**Goal:** Promote learning only after a later task retrieves it and behavior measurably changes.  
**Why:** A stored lesson is memory, not learning.

**Copy/paste assignment:**

> Run one real control/treatment or equivalent held-out task using a lesson created by the runtime. Prove Naya B retrieved the retained lesson, changed behavior because of it, and produced an independently verified improvement. Promote CANDIDATE → ACTIVE only after the evidence chain passes. Record the learning evidence and why the promotion is justified.

### E — Succession / Cold Naya
**Files:** 05-MEMORY + 08-SUCCESSION + SELF/EVOLVE objects.  
**Goal:** Destroy the first runtime context, cold boot a successor, retrieve canonical intelligence, and continue without inherited authority.  
**Why:** This is the actual “Nayas do not lose memory” test.

**Copy/paste assignment:**

> Create a genuine cold successor context with no inherited execution authority. Restore identity, current state, applicable intelligence, provenance, unresolved unknowns, blockers, next action and proof. Then run a held-out continuation task. Prove the successor used retained intelligence and did not receive authority merely by inheriting context.

### F — Knowledge Population / Parity
**Files:** 00-SPEC + 11-KNOWLEDGE + 04-INTELLIGENCE OBJECTS.  
**Goal:** Finish deterministic source → object population and human/AI/machine parity.  
**Why:** The corpus is mapped, but not every durable proposition is yet a complete promoted object.

**Copy/paste assignment:**

> Audit Concepts #1–#15 against the population map and canonical distilled knowledge. For each durable proposition, ensure stable object ID, type, source lineage, epistemic state, applicability, relationships, authority implications and proof state. Add automated parity validation for human/AI/machine views. Keep #7/#8 merged because they are byte-identical. Do not promote source text merely because it was distilled.

### G — Brain Receipts / Operations
**Files:** MASTER-MAP, INDEX, REAL-TREE, scorecard, queue, execution prompt.  
**Goal:** Keep documentation synchronized with actual Git state and proof state.  
**Why:** A brain that lies about its own inventory is not trustworthy.

**Copy/paste assignment:**

> Regenerate `BRAIN/REAL-TREE.json` and `BRAIN/REAL-TREE.md` from the actual canonical tree after all structural changes settle. Update the Brain Index and AAA scorecard from the same source. Every status must distinguish DESIGNED / IMPLEMENTED / TESTED / VERIFIED / PRODUCTION-PROVEN. No stale file count or old branch SHA may remain.

## What is genuinely complete vs not

### COMPLETE AT THE ARTIFACT LEVEL
- 15-domain Brain organization.
- Nine stable Node IDs and semantic contracts.
- Machine-readable manifest and runtime registry.
- Canonical graph seed with provenance-bearing edges.
- Nine Node objects aligned to that graph seed **after this pass**.
- 15-source knowledge corpus registration and population map.
- Human/AI/machine representation contract.
- Explicit truth/authority/learning/succession laws.
- AAA execution doctrine.

### NOT COMPLETE AT THE LIVING-SYSTEM LEVEL
- Main-branch executable runtime consuming the canonical BRAIN manifest.
- Proven runtime convergence with canonical Supabase persistence/retrieval.
- All nine Nodes demonstrably loading, invoking, influencing and applying in one runtime.
- Relationship-aware retrieval demonstrably changing behavior in a held-out task.
- Full application-level cold Naya continuity.
- Independent future-task learning proof and successor improvement.
- Production/browser/deployment parity.
- Final NAYA-NODE-0001 race qualification.

## Race-entry gate

The Brain should **not enter the definitive NAYA-NODE-0001 race yet**. The artifact layer is strong enough to support the race, but the executable convergence gate is not closed.

The first gate to close is:

**BRAIN MANIFEST → ACTUAL RUNTIME ENTRYPOINT → CANONICAL SUPABASE RETRIEVAL → NINE-NODE EXECUTION → PROOF RECEIPT**

Once that path is real, the remaining gaps become measurable runtime tests instead of architecture archaeology.

**Rule:** no new architecture, no second brain, no second persistence store. Repair the canonical lineage.
