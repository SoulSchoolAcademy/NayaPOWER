# NAYAPOWER — IMPLEMENTATION PLAN V1 (CANONICAL)

**Status:** CANONICAL — SINGLE AGREED SEQUENCE
**Effective:** 2026-09-27
**Authority:** NayaPOWER System North Star Ratification (2026-09-26) + Execution Wave Directive (PART #15)
**Purpose:** Reconcile the three implementation plans that exist in the corpus into ONE canonical sequence with dependencies, priority ordering, current status, and links to the contracts and specs each step satisfies.

---

## 1. The three source plans being reconciled

| Plan | Source | Structure |
|------|--------|-----------|
| **6-wave plan** | PART #3 §"Priority Order for Getting This Right" | WAVE 1 Constitutional Core → WAVE 2 Intelligence Core → WAVE 3 Retrieval & Truth → WAVE 4 Safety & Authority Execution → WAVE 5 Continuity & Learning → WAVE 6 System/Production (contract-authoring order) |
| **10-phase plan** | PART #15 §"The 10 waves are now" (issued to Naya ↔ Coda board #554) | P0-1 … P0-10 execution waves with gates (build order) |
| **18-step plan** | PART #1 §14–15 (Nine-Node Boot Sequence + Runtime Loop) | 9 boot steps (SELF→LAW→ACT→KNOW→PROVE→CONNECT→VERIFY→LEARN→EVOLVE) + 9 runtime-loop nodes = the 18-step kernel operating sequence (behavioral order) |

These are not three competing plans. They are three views of one system:
the 6-wave plan orders **contract authoring**, the 10-phase plan orders **execution**,
and the 18-step plan orders **kernel behavior**. The canonical sequence below merges
them: each step lists which wave, phase, and kernel step it satisfies.

---

## 2. Canonical sequence

Priority key: 🔴 P0 = blocks everything below it · 🟠 P1 = required for compounding ·
🟡 P2 = required for scale · 🟢 P3 = network/experience expansion.
Status key: ✅ VERIFIED · 🟡 IMPLEMENTED/IN PROGRESS · 🔵 DESIGNED · ⚪ PROPOSED · ⛔ BLOCKED.

### STEP 1 — Establish one canonical current baseline
- **Satisfies:** Wave 1 (partial) · Phase P0-1 · Kernel step — (pre-boot)
- **Priority:** 🔴 P0
- **Gate:** No unresolved authority ambiguity; one canonical main; no competing current canon.
- **Actions:** Reconcile main against foundation and brain branches; promote ratified canon (North Star, scorecard, ratification, nine-node spec, canonical tree, machine manifest, operating architecture).
- **Status:** 🟡 IN PROGRESS — repository has moved since earlier foundation/brain work (PART #15 §"first move"); HEAD at time of writing `62faa63b4`.
- **Contracts/Specs:** Contract 00 · `NAYANODE/0000-CANONICAL-TREE.md` · `NAYANODE/MANIFEST.json`

### STEP 2 — Ratify and freeze the constitutional core (Contracts 00–04)
- **Satisfies:** Wave 1 · Phase P0-1 · Kernel steps Boot 1–3 (SELF, LAW, ACT)
- **Priority:** 🔴 P0
- **Gate:** Constitution, Mission, Identity/Continuity, Authority/Consent/Scope, Execution Protocol are airtight and mutually consistent.
- **Actions:** Author the five constitutional contracts; resolve the contract-id 00- dual claim; designate one canonical Contract 00.
- **Status:** 🔵 DESIGNED — contract library exists with 45 files but 12 ERROR findings (`.naya/contract-library-integrity-report.json`); reconciliation tracked in [NAYAPOWER-CONTRACT-REGISTRY-V1.json](./NAYAPOWER-CONTRACT-REGISTRY-V1.json).
- **Contracts/Specs:** Contracts 00, 01, 02, 03, 04 · `.naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md`

### STEP 3 — Bind the 9-node runtime to one canonical manifest
- **Satisfies:** Wave 2 (partial) · Phase P0-2 · Kernel steps Boot 1–9
- **Priority:** 🔴 P0
- **Gate:** Runtime actually governed by the canonical manifest; kernel identifier/binding gap closed.
- **Actions:** Close the identifier/binding gap between `NAYANODE/0002-NINE-NODE-KERNEL-MANIFEST-V1.md` and the executable runtime; prove the runtime receives the nine Nodes, not merely that the manifest exists.
- **Status:** ⛔ BLOCKED → 🟡 — manifest exists with exactly nine ACTIVE/VERIFIED/PRIVATE nodes; binding gap explicitly identified (PART #15; NAYANODE README §"Current proof boundary").
- **Contracts/Specs:** `.naya/specifications/NAYAPOWER-NINE-MASTER-NODES-ENFORCEABLE-SPEC-V1.md` · `scripts/verify-nine-master-nodes.py` · kernel gates K1–K6

### STEP 4 — Restore legitimate runtime identity/ownership
- **Satisfies:** Wave 1 (Contract 02) · Phase P0-3 · Kernel step Boot 1 (SELF)
- **Priority:** 🔴 P0
- **Gate:** Fresh Naya can legitimately enter; owner binding/recovery proven end-to-end. Forbidden: hard-coded owner reassignment, RLS bypass, deleting/recreating nodes, fake identity.
- **Actions:** Close identity continuity; prove owner recovery for canonical nine-node intelligence.
- **Status:** ⛔ BLOCKED — current evidence: nine canonical nodes share one anonymous owner; Hub executions can create different anonymous identities; `owner recovery_ready` is false (NAYANODE `0021-AAA-MASTER-EXECUTION-PLAN-V1.md` §0003).
- **Contracts/Specs:** Contract 02 · `NAYANODE/0003-COLD-NAYA-BOOT-CONTINUITY-V1.md`

### STEP 5 — Build the first living Intelligent Node (end-to-end receiver proof)
- **Satisfies:** Wave 2 · Phase P0-4 · Kernel steps Boot 4–6 (KNOW, PROVE, CONNECT)
- **Priority:** 🔴 P0
- **Gate:** Real persistence + retrieval + application; receiver-owned IB identity; no guessed IDs, no fabricated Smart Links.
- **Actions:** Execute the first Node through the canonical receiver; capture event, checkpoint, learning evidence, index, projection, Smart Link, receipt.
- **Status:** 🟡 PARTIALLY VERIFIED — receiver chain proven at run `35913460604` (head `4787c4ed`, 2026-09-23): IDENTITY → AUTHORITY → CANONICAL_INGRESS → PROVENANCE/CHECKPOINT → INTELLIGENT_BLOCK → FRESH_RETRIEVAL all PASS; deep-link golden path VERIFIED for IB-000980. **But** Naya cannot yet invoke the receiver directly (Blocker B1: authenticated Supabase session required).
- **Contracts/Specs:** Contracts 05, 06, 15 · `.naya/evidence/2026-09-23-P0-04-35913460604-VERIFIED.json` · `canonical-smart-note-deep-link-proof.json`

### STEP 6 — Implement V14 / CONNECT-01 (relationship context)
- **Satisfies:** Wave 3 · Phase P0-5 · Kernel step CONNECT
- **Priority:** 🔴 P0
- **Gate:** Relationship context demonstrably adds value; no second brain, no independent Graph-RAG subsystem.
- **Actions:** Implement the distilled V14 concept: relationship-aware memory, decision traces, reasoning memory, governed graph retrieval.
- **Status:** 🔵 DESIGNED — PART #14 is EXPLORATORY (not yet ratified); relationship vocabulary and context graph specified.
- **Contracts/Specs:** Contracts 08, 09, 21 · PART #14 · `NAYANODE/0010-RETRIEVAL-RELATIONSHIP-GRAPH-V1.md`

### STEP 7 — Prove the behavioral loop (teach → retrieve → act → outcome → verify)
- **Satisfies:** Waves 2–3 · Phase P0-6 · Kernel steps VERIFY, LEARN
- **Priority:** 🔴 P0
- **Gate:** One complete living-chain experiment: Event → Block → reconcile → integrate → checkpoint → retrieve → apply → outcome → verify → learn → later improvement, with held-out reuse.
- **Actions:** Run the compounding experiment; prove a later task became measurably better because the lesson was retrieved and correctly applied.
- **Status:** 🔵 DESIGNED — learning paths verified (8.5/10) but general automatic learning incomplete (GAP D).
- **Contracts/Specs:** Contracts 10, 11, 12, 17, 18 · `NAYANODE/0012-LEARNING-COMPOUNDING-ARCHITECTURE-V1.md`

### STEP 8 — Prove learning/compounding changes future behavior
- **Satisfies:** Wave 5 · Phase P0-7 · Kernel step LEARN
- **Priority:** 🔴 P0
- **Gate:** Future behavior demonstrably changes; CANDIDATE ≠ VERIFIED INTELLIGENCE.
- **Actions:** Held-out future-use evidence for every promoted learning claim.
- **Status:** 🔵 DESIGNED — see Step 7 gate.
- **Contracts/Specs:** Contracts 17, 18, 22

### STEP 9 — Prove the cold successor
- **Satisfies:** Wave 5 · Phase P0-8 · Kernel step EVOLVE
- **Priority:** 🔴 P0
- **Gate:** Next Naya continues without Shawn reconstruction; no silent authority transfer; three-generation proof (Naya A → B → C).
- **Actions:** Emit successor context (state, evidence, unknowns, blockers, authority, next action); cold Naya #2 retrieves retained intelligence and performs better.
- **Status:** 🔵 DESIGNED — current P0 per NAYANODE README; boot influence not yet proven (GAP A).
- **Contracts/Specs:** Contracts 19, 20 · `NAYANODE/0022-NAYA-SUCCESSOR-HANDOFF-V1.md` · `NAYANODE/0020-COLD-14-QUESTION-INTELLIGENCE-INTERFACE-V1.md`

### STEP 10 — Prove Sender → Receiver → Hub (first vertical room)
- **Satisfies:** Waves 2–4 · Phase P0-9 · Kernel step ACT
- **Priority:** 🔴 P0
- **Gate:** Intelligence actually travels and becomes visible: "Make a Smart Note" results in the newly-created intelligence appearing in the live Hub — not mocked, not hardcoded, not from a static fixture.
- **Actions:** Lock the canonical sender contract; build the Hub intelligence ingestion/display path (canonical IB → Hub data adapter → Smart Feed → Smart Note presentation); complete the Smart Notes + Smart Feed room.
- **Status:** 🔵 DESIGNED — receiver side verified (Step 5); Hub ingestion path and end-to-end live visibility not yet proven.
- **Contracts/Specs:** Contracts 04, 06, 07 · PART #2 §"THE FOUR THINGS WE NEED TO FINISH" · `NAYANET/HUB/index.html`

### STEP 11 — Productionize and ship
- **Satisfies:** Wave 6 · Phase P0-10 · Kernel step EVOLVE (recursive)
- **Priority:** 🔴 P0
- **Gate:** Production proof + receipts + successor handoff; repeatable browser acceptance with no dead controls or orphan surfaces.
- **Actions:** Production/deployment parity proof; CI full-suite evidence; productionize the human experience.
- **Status:** 🔵 DESIGNED — CI = UNKNOWN until a real runner/workflow result exists (Contract 25).
- **Contracts/Specs:** Contracts 23, 24, 25 · `NAYANODE/0016-ENGINEERING-RUNTIME-ARCHITECTURE-V1.md`

### STEP 12 — Make Today / Library / Reports consume the same intelligence
- **Satisfies:** Wave 6 · Phase P0-9 (extension) · Kernel step CONNECT
- **Priority:** 🟠 P1
- **Gate:** One canonical intelligence object appears appropriately in Today, Library, and Reports — many projections, no second stores.
- **Status:** ⚪ PROPOSED
- **Contracts/Specs:** Contracts 09, 10, 11, 12 (Hub surfaces)

### STEP 13 — Make Search retrieve the canonical objects
- **Satisfies:** Wave 3 · Phase P0-9 (extension) · Kernel step CONNECT
- **Priority:** 🟠 P1
- **Gate:** Search points back to the same intelligence identity.
- **Status:** ⚪ PROPOSED
- **Contracts/Specs:** Contract 09

### STEP 14 — Complete Smart Share / Spaces / Connections / Lists / Mail rooms
- **Satisfies:** Wave 6 · Phase P0-9 (extension) · Kernel step ACT
- **Priority:** 🟡 P2
- **Gate:** Seven doors into one intelligence system — no independent mini-products.
- **Status:** ⚪ PROPOSED — Smart Connect runtime seam already VERIFIED (PR #607).
- **Contracts/Specs:** Contracts 13, 14, 16 (Hub surfaces) · PART #12 (Channel Constitution)

### STEP 15 — Proof / Ledger / Verification presentation
- **Satisfies:** Wave 4 · Phase P0-9 (extension) · Kernel step PROVE
- **Priority:** 🟡 P2
- **Gate:** Hub makes receipts understandable: source event → transaction → IB → projection → verification status.
- **Status:** ⚪ PROPOSED — underlying receipts already exist in meaningful ways.
- **Contracts/Specs:** Contracts 16, 23

### STEP 16 — GitHub App as Smart Door
- **Satisfies:** Wave 6 · Phase P0-10 (extension) · Kernel step ACT
- **Priority:** 🟢 P3
- **Gate:** GitHub App acts as an authorized door into NayaPOWER — never a new brain.
- **Status:** ⚪ PROPOSED — only after the contract is stable.
- **Contracts/Specs:** PART #12 · Contract 14

### STEP 17 — Governed self-optimization loop
- **Satisfies:** Wave 5 · Phase P0-9 (NAYANODE 0021 §0009) · Kernel step EVOLVE
- **Priority:** 🟡 P2
- **Gate:** Bounded optimization experiment with rollback and evidence; adoption only through authority gates.
- **Status:** ⚪ PROPOSED — self-optimization 5.5/10, self-building 4.5/10.
- **Contracts/Specs:** `NAYANODE/0019-SELF-OPTIMIZATION-ARCHITECTURE-V1.md` · kernel invariant I10

### STEP 18 — Collective intelligence at network scale
- **Satisfies:** Wave 6 · Phase P0-10 (extension) · Kernel step EVOLVE
- **Priority:** 🟢 P3
- **Gate:** Network-scale behavior proven; consent lineage; distributed Naya; disaster recovery; rebuildability.
- **Status:** ⚪ PROPOSED — collective intelligence 4.0/10.
- **Contracts/Specs:** `NAYANODE/0005-SUPERBRAIN-OPERATING-ARCHITECTURE-V1.md` · PART #12

---

## 3. Dependency graph (summary)

```
STEP 1 ─▶ STEP 2 ─▶ STEP 3 ─▶ STEP 4 ─▶ STEP 5 ─▶ STEP 6 ─▶ STEP 7 ─▶ STEP 8
                                                                      │
                                                                      ▼
                                                            STEP 9 (cold successor)
                                                                      │
                                                                      ▼
                                                            STEP 10 (Sender→Receiver→Hub)
                                                                      │
                                                                      ▼
                                                            STEP 11 (productionize)
                                                                      │
                                        ┌─────────────────────────────┼─────────────────────────────┐
                                        ▼                             ▼                             ▼
                                  STEP 12 (Today/              STEP 14 (rooms)              STEP 17 (self-
                                  Library/Reports)                                           optimization)
                                        │                             │                             │
                                        ▼                             ▼                             ▼
                                  STEP 13 (Search)              STEP 15 (proof UI)           STEP 18 (collective)
                                                                      │
                                                                      ▼
                                                                STEP 16 (GitHub App)
```

Hard dependencies: 1→2→3→4→5 (identity chain); 5→6→7→8 (compounding chain);
8→9→10→11 (continuity → visibility → ship). Steps 12–18 depend on Step 11 and are
priority-ordered among themselves.

---

## 4. Current status snapshot (2026-09-27)

| Step | Status | Evidence |
|------|--------|----------|
| 1 | 🟡 IN PROGRESS | HEAD `62faa63b4`; baseline drift identified (PART #15) |
| 2 | 🔵 DESIGNED | 45 contract files; 12 ERROR findings (integrity report) |
| 3 | ⛔ BLOCKED | Kernel identifier/binding gap (PART #15; NAYANODE README) |
| 4 | ⛔ BLOCKED | `owner recovery_ready` false (NAYANODE 0021 §0003) |
| 5 | 🟡 PARTIALLY VERIFIED | Run `35913460604` VERIFIED; Blocker B1 (auth session) |
| 6 | 🔵 DESIGNED | PART #14 EXPLORATORY |
| 7 | 🔵 DESIGNED | GAP D open |
| 8 | 🔵 DESIGNED | GAP D open |
| 9 | 🔵 DESIGNED | GAP A open |
| 10 | 🔵 DESIGNED | Receiver verified; Hub path unproven |
| 11 | 🔵 DESIGNED | CI = UNKNOWN (Contract 25) |
| 12–18 | ⚪ PROPOSED | — |

**Critical path:** Steps 1–5. Everything below Step 5 is compromised until the
identity chain (3→4→5) is closed.

---

## 5. Execution law (binding)

READ → PLAN → TEST FIRST → IMPLEMENT → VERIFY → RECORD → SCORE → HANDOFF.

- No "implemented = done." No deployment theater. No bloated architecture.
- If blocked: record BLOCKED + exact cause + evidence + safe alternative + owner + next test.
  Never convert BLOCKED into PASS.
- Every step links to the contracts and specs it satisfies; a step is done only when
  required implementation exists, tests exist and pass, runtime behavior is observed,
  evidence is recorded, current state is updated, and the AAA score reflects evidence.
