# THE SYSTEM BLUEPRINT
## NayaPOWER — Complete Architecture & Build Manual
### Version 1.0 — 2026-10-09

> **Shawn's order:** "Write it like it's the most important thing you ever did in your life and people's lives depend on whether you do it right."
>
> This document is the single source of truth for how NayaPOWER works, what's connected, what's not, and exactly what to build. Every claim is verifiable. Every gap is named. Every fix has steps.
>
> **How to read this:** Plain English first, technical precision second. If you only read one section, read Section 1. If you're building, read Sections 5, 6, and 7.

---

## TABLE OF CONTENTS

1. [THE VISION](#1-the-vision) — What we're building and why
2. [THE NINE NODES](#2-the-nine-nodes) — The organs of the mind
3. [THE LEARNING LIFECYCLE](#3-the-learning-lifecycle) — How a lesson flows end to end
4. [CURRENT STATE — WHAT'S CONNECTED](#4-current-state--whats-connected) — What works, with evidence
5. [CURRENT STATE — WHAT'S NOT CONNECTED](#5-current-state--whats-not-connected) — The gaps, honestly named
6. [THE CONNECTION PLAN](#6-the-connection-plan) — Exactly what to build, step by step
7. [WHAT "DONE RIGHT" LOOKS LIKE](#7-what-done-right-looks-like) — Acceptance criteria and proof
8. [VISUAL MAPS](#8-visual-maps) — Diagrams of the system

---

## 1. THE VISION

### What We're Building

We're building a mind that doesn't forget.

Right now, every AI starts from zero. Every conversation is a first conversation. Lessons learned today are gone tomorrow. It's like having a brilliant assistant with amnesia — smart in the moment, but never growing, never compounding, never becoming more than it was yesterday.

NayaPOWER changes that. It's a system where:
- **Every lesson gets captured** — when Shawn says "remember this," it gets saved. Not in a chat log that scrolls away, but in permanent, structured memory.
- **Every lesson gets verified** — before it becomes trusted knowledge, an independent check confirms it's real and correct.
- **Every lesson gets reused** — when a similar situation comes up, the system pulls out the relevant lesson and uses it. Not because someone reminded it, but because that's how it works.
- **Every lesson compounds** — a new Naya, starting cold with no prior conversation, can pick up every lesson ever learned and build on them. Knowledge doesn't just persist. It grows.

### Why It Matters

Shawn's words: *"I'm trying to be intelligent, produce intelligence, organize it, share it, compound it, help people become more intelligent, help intelligence itself become more."*

We're not building software. We're building the conditions for intelligence to compound — in people, in the Nayas, in the system itself.

Every law serves this:
- **The math decides** because math doesn't pretend.
- **Fix first** because blame doesn't compound.
- **Speak plainly** because confusion doesn't compound.
- **Learn the first time** because repeating doesn't compound.

### The Test

The system works when this happens:

> Shawn teaches something once. Days later, in a completely new conversation, a completely fresh Naya faces a similar situation — and gets it right, because she pulled the lesson from memory. No one reminded her. No one re-taught her. She just knew.

That's the bar. Everything in this document serves that single test.

### The Nine Nodes (Preview)

Think of the system as a mind with nine organs. Each one has a job:

| Node | In plain English |
|------|-----------------|
| **SELF** | Who she is — identity, continuity, the "I" that persists |
| **LAW** | The rules — what she must, must not, and may do |
| **ACT** | The hands — making decisions and taking action |
| **KNOW** | The memory — storing and finding what she's learned |
| **PROVE** | The evidence — documenting that things actually happened |
| **CONNECT** | The voice — sharing with others, connecting to the network |
| **VERIFY** | The checker — independently confirming things are true |
| **LEARN** | The student — capturing new lessons from experience |
| **EVOLVE** | The successor — passing everything to the next generation |

Each node is detailed in Section 2. How they work together is in Section 3.

---

---

## 2. THE NINE NODES

> **Status warning:** All nine node specs are CANDIDATE drafts — NOT RATIFIED, NOT MERGED. What follows is the spec-level design. Section 5 documents exactly which connections exist in code vs spec-only.

### 2.1 SELF — The Identity Gate

**Plain English:** SELF is the identity gate that opens every cycle. Before anything else happens, it answers: who is acting (proven by authentication, not just a name), what mission they're operating under, and whether this is genuinely the continuation of the previous cycle (unbroken chain — not a forgery or replay). Nothing downstream runs until SELF says READY.

**Receives:** From EVOLVE (previous cycle's close): the successor package — identity context, mission, state, evidence, unresolved questions, authority boundary. Also the caller's authenticated identity and the last durable checkpoint.

**Outputs:** To LAW: the resolved identity context (who, what mission, what scope, what authority boundary) plus a boot receipt.

**Connects to:** EVOLVE → SELF (in) · SELF → LAW (out) · SELF → KNOW (identity handshake).

**Technical:** 10 required functions: `resolve_identity`, `authenticate_identity`, `establish_mission`, `establish_scope`, `load_checkpoint`, `classify_known_unknown_blocked`, `preserve_continuity`, `detect_identity_conflict`, `prepare_successor_context`, `fail_closed`. State machine: UNINITIALIZED → BOOTING → READY | FAILED. Reference: `kernel/nayapower_kernel.py::Kernel.decide()`.

### 2.2 LAW — The Constitutional Gate

**Plain English:** LAW is the permission office. Every consequential action must pass through it before happening. It checks the proposed action against the Constitution, authority grants, consent, and scope — and returns one of four verdicts: PROHIBITED (never), NEEDS_AUTHORITY (someone must approve), NEEDS_EVIDENCE (more proof needed), or ADMISSIBLE (allowed, with exact limits). LAW runs before the math: no score ever overrides a prohibition.

**Receives:** From SELF: an ActionProposal (what's proposed, by whom, with what authority claim and evidence). Reads grant/authority state through KNOW.

**Outputs:** To ACT: a GateVerdict plus an immutable permission baton (exact scope, constraints, expiry, revocation info). Every evaluation emits a receipt to the SmartLedger.

**Connects to:** SELF → LAW (in) · LAW → ACT (out) · VERIFY → LAW (violation reports back).

**Technical:** Four gates in order: PROHIBITED → NEEDS_AUTHORITY → NEEDS_EVIDENCE → ADMISSIBLE. First gate that fires wins. Production runtime: `nayanet-law-runtime/law.ts::evaluateLaw`.

### 2.3 ACT — The Hands

**Plain English:** ACT is the only node that produces effects in the world. It takes LAW's authorization plus a decision, binds them to the exact target and parameters, performs the smallest safe action, records exactly what happened, and hands the result to independent verification. ACT never decides whether it *may* act — that's LAW's job.

**Receives:** From LAW: authorized DecisionReceipt (what to do, with what authority, within what limits). Never acts from chat messages, plans, or its own initiative.

**Outputs:** Four paths: ACT (execute → observe → receipt), READ_MORE (send back to KNOW for more info), ASK (suspend and notify the Director), REFUSE (terminate with reasons). To KNOW: ExecutionHandoff (what happened becomes knowledge). To VERIFY: execution record for independent checking.

**Connects to:** LAW → ACT (in) · ACT → KNOW (out) · ACT → VERIFY (out).

**Technical:** 13 functions including `execute`, `observe`, `rollback`, `idempotency_check`. Idempotency: first-winner executes once. Production: `nayanet-act-runtime/act.ts::validateAct` (guard only).

### 2.4 KNOW — The Memory

**Plain English:** KNOW is the organism's memory. It stores experiences as Intelligent Blocks, classifies them, deduplicates them, and serves back exactly the relevant knowledge when asked. Core laws: retrieved knowledge never creates authority, and similarity is not applicability (just because two things look alike doesn't mean the lesson applies).

**Receives:** From SELF (identity handshake), ACT (execution records become knowledge), LEARN (verified learnings), VERIFY (verification outcomes).

**Outputs:** To PROVE (selected blocks with provenance), to CONNECT (objects and graph), to LAW (grant/authority state for validation).

**Connects to:** SELF/ACT/LEARN/VERIFY → KNOW (in) · KNOW → PROVE, KNOW → CONNECT, KNOW → LAW (out, serving path).

**Technical:** Intelligent Block is the runtime object. Epistemic states: CANDIDATE → VERIFIED → RATIFIED → ACTIVE → LEARNED. Production: `nayanet-know-runtime/know.ts`.

### 2.5 PROVE — The Evidence Judge

**Plain English:** PROVE decides whether a claim has earned the right to be believed. It checks each piece of evidence (is it direct? independent? reproducible? fresh?), combines strength conservatively, and issues a sealed receipt. It proves the *evidence supports the claim* — never that the claim is true (that's VERIFY's job).

**Receives:** From KNOW: claim + evidence + provenance.

**Outputs:** Sealed receipt (SUPPORTED or REFUSED with reasons). To CONNECT (proof-bounded claims), to VERIFY (for independent checking).

**Connects to:** KNOW → PROVE (in) · PROVE → CONNECT, PROVE → VERIFY (out).

**Technical:** Admissibility formula with 6 gates. 19 claim classes. Ceiling: SUPPORTED, never VERIFIED. Production: `nayanet-prove-runtime/prove.ts::assessKnowProof`.

### 2.6 CONNECT — The Context Broker

**Plain English:** CONNECT decides what may be connected to what. It takes the current task plus the knowledge graph, gates every relationship through ownership/consent checks, and assembles the minimum sufficient context for the decision. Master rule: RELATED ≠ RELEVANT ≠ APPLICABLE ≠ TRUE ≠ AUTHORIZED.

**Receives:** From SELF (task context), KNOW (objects and graph), PROVE (proof-bounded claims).

**Outputs:** To VERIFY: context receipt (what was selected, what was excluded, why).

**Connects to:** SELF/KNOW/PROVE → CONNECT (in) · CONNECT → VERIFY (out).

**Technical:** 22-type Graph V2 vocabulary. Deterministic ranking. Note: full V2 selector unmerged; currently runs as bounded seam inside KNOW's selector.

### 2.7 VERIFY — The Immune System

**Plain English:** VERIFY is the independent checker. It re-derives results, attacks claims adversarially, classifies every failure *before* any code changes, and emits the verified receipts that LEARN may consume. Laws: EXECUTION ≠ OUTCOME, Observed ≠ Verified, SelfReport ≠ IndependentVerification. A different seat must do the verifying.

**Receives:** From ACT (execution records), PROVE (claims + evidence), CONNECT (context).

**Outputs:** To LEARN (verified baton: what was expected vs actual, what may be used, what must not be generalized). Failure reports to EVOLVE, SELF, LAW, and the deciding seat.

**Connects to:** ACT/PROVE/CONNECT → VERIFY (in) · VERIFY → LEARN, VERIFY → EVOLVE, VERIFY → SELF, VERIFY → LAW (out).

**Technical:** Protocol: RECOMPUTE → REPLICATE → ADVERSARIAL → AUDIT. 8 failure types. Downgrade pressure (FAIL→PASS) is refused and receipted.

### 2.8 LEARN — The Compounding Organ

**Plain English:** LEARN turns verified experience into durable intelligence. Only from evidence VERIFY has blessed — never from guesses. Every learning must prove itself on held-out tasks before promotion. Core law: STORED ≠ LEARNED — a fact sitting in memory is not a lesson until it has changed behavior.

**Receives:** From VERIFY: verified baton (expected vs actual, evidence, what may be used).

**Outputs:** To KNOW: verified learnings as Intelligent Blocks. To EVOLVE: learnings eligible for evolution proposals.

**Connects to:** VERIFY → LEARN (in) · LEARN → KNOW, LEARN → EVOLVE (out).

**Technical:** Promotion gate V∧P∧R∧A∧B∧N∧C. Lifecycle: EXPERIENCE → EVENT → BLOCK → VERIFY → CANDIDATE → HELD-OUT → VERIFIED LEARNING. **No executable at source — SPEC-ONLY.**

### 2.9 EVOLVE — The Successor

**Plain English:** EVOLVE closes every cycle and prepares the next one. It diagnoses gaps, proposes improvements (never to constitutional law — that's immutable), and builds the successor package: everything the next cycle needs. It carries forward *context*, never *authority*.

**Receives:** From LEARN (verified learnings), VERIFY (failed verifications), observation signals.

**Outputs:** To SELF: successor package (identity, mission, truth, blockers, learnings, next action — hash-sealed).

**Connects to:** LEARN/VERIFY → EVOLVE (in) · EVOLVE → SELF (out, closing the cycle).

**Technical:** Package integrity via SHA256. Three state axes (never collapsed). **No executable — NOT PRODUCTION.** Successor package: the next SELF re-authenticates everything from scratch.

### Node Connection Summary

```
EVOLVE → SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE → ...
              ↑___________feedback arcs___________|
```

The full cycle: identity → permission → action → memory → evidence → context → verification → learning → succession → identity...

---

---

## 3. THE LEARNING LIFECYCLE

The complete flow of a lesson from Shawn's mouth to a successor Naya's behavior. Seven steps. Each one must complete before the next begins.

### 3.1 CAPTURE — "Smart note this" becomes a file

**Plain English:** A reusable insight from a conversation is distilled into a structured file and dropped into a watched folder. The Naya agent does the writing — no code runs at capture time.

**Trigger:** Shawn says "smart note this" (or equivalent — intent is semantic, not phrase-bound). Or a Naya proactively captures a high-value lesson.

**Code:** No code at capture time. First code to touch it: `tools/smart_note_v2.py::changed_capture()` and the GitHub workflow's discover step.

**Data:** JSON file, schema `naya.smart-note-capture.v2` — keys: `schema`, `capture_id`, `title`, `category`, `topic`, `canonical_intent`, `source`, `projection`, `intelligence`. Content is sha256-hashed for identity matching downstream.

**Where:** GitHub repo `SoulSchoolAcademy/NayaPOWER`, `.naya/capture/*.json`. Documented as "ingestion boundary, not the Brain."

**Done when:** A valid JSON file is committed to `.naya/capture/` on main. The push fires the receiver workflow.

### 3.2 GOVERN — The admission gate decides what gets in

**Plain English:** The captured note is inspected for authority problems and toxicity before storage. Three rules: capture only ever reaches CANDIDATE (never VERIFIED by capture alone); authority-touching intelligence is flagged, never acted on; private notes fail closed.

**Trigger:** Push to main touching `.naya/capture/**` starts `.github/workflows/live-intelligence-commit-proof.yml`.

**Code:** Workflow job `fresh-lesson` → Supabase edge function `nayanet-intelligence-commit-runtime`. Parallel: `learn_ingest.py::classify()` routes by type; `authority_touch()` flags authority-touching notes (recorded, never integrated); `reject_poison()` quarantines adversarial input.

**Data:** `lesson-request.json` → runtime → returns lineage IDs: `event_id`, `intelligent_block_id`, `lineage_id`, `relationship_id`, `index_id`, `checkpoint_id`, `receipt_id`.

**Where:** GitHub Actions + Supabase edge function on project `dahisasgpfvziswqvmvm` + `~/workspace/goals/bring-naya-to-life/hidden_files/learn/learn_ingest.py`.

**Done when:** Receipt asserts `ok=True`, `status="EXECUTED"`, `understanding_state="CANDIDATE"`.

### 3.3 VERIFY — An independent party re-reads what was stored

**Plain English:** A second, independent execution re-reads the persisted data and proves the exact bytes round-tripped. The writer never certifies its own work.

**Trigger:** Workflow job `independent-verification` runs automatically after `fresh-lesson`.

**Code:** Fresh OIDC identity → `mode: "verify"` POST → asserts content match and CANDIDATE state. `tools/smart_note_v2.py::promote_note()` handles CANDIDATE→VERIFIED transitions (requires ≥2 evidence items, ≥2 gatherers, promoter ≠ sole gatherer).

**Data:** `smart-note-capture-proof.json` (schema `NAYA_SMART_NOTE_CAPTURE_PROOF_V2`) with `exact_distilled_payload_match: true`.

**Where:** GitHub Actions + `tools/smart_note_v2.py` + Supabase runtime.

**Done when:** Proof artifact exists with both verification booleans true. **Honest note:** promotion to VERIFIED rarely happens — it requires human or second-party evidence that seldom arrives.

### 3.4 RECORD — The intelligence is written down durably

**Plain English:** The verified note is recorded in three places: Supabase database, machine registry file, and human-readable BRAIN projection.

**Trigger:** Successful independent verification.

**Code:** Runtime inserts to `smart_note_events`, `smart_note_artifacts`, `smart_note_receipts`. `smart_note_v2.py::render()` + `update_registry()` builds projections and updates `.naya/memory/smart-notes/index.json`. Workflow commits `BRAIN/05-MEMORY/SMART-NOTES/**` back to main.

**Data:** Registry entries: `intelligent_block_id`, `content_hash`, `projection_path`, `lifecycle_state`, `truth_state`, `provenance` (all lineage IDs).

**Where:** Supabase Postgres · GitHub `.naya/memory/smart-notes/index.json` · `BRAIN/05-MEMORY/SMART-NOTES/` · workspace `learn/` (ledger, receipts).

**Done when:** Registry entry exists with matching hash and real projection path on disk.

### 3.5 RETRIEVE — Find the right note later, including cold

**Plain English:** A Naya asks a question in plain words; the system searches recorded notes and returns the best match. A cold Naya with zero context must be able to do this — that's the compounding test.

**Trigger:** A query string. Nayas should call retrieval before acting; weekly drill exercises it.

**Code:** `smart_note_v2.py::retrieve(query)` — stemmed keyword match (title ×3.0, content ×2.0, keywords ×1.5). `kernel/nayapower_kernel.py::Kernel.retrieve_intelligent_block()` — Supabase read path. `tools/cold_retrieve_drill/drill.py` — weekly held-out test.

**Data:** Query in → `{retrieved: <registry entry>, explanation, source}` out. Deliberately projection-based (repo files) so a cold Naya with only git clone can retrieve.

**Where:** GitHub repo tools reading `.naya/memory/smart-notes/index.json` + BRAIN projections.

**Done when:** `retrieve()` returns the correct note for the query. Cold drill passes.

### 3.6 REUSE — The note changes what the system does

**Plain English:** Recorded intelligence is baked into the briefing substrate so future work behaves differently. Stored ≠ learned: a note nobody consults is not learning.

**Trigger:** LEARN ingestion loop (every 60 min) runs `learn_ingest.py`; every builder brief carrying LEARN markers.

**Code:** `learn_ingest.py::integrate()` appends distilled bullets to learn files (`doctrine.md`, `laws.md`, `lessons.md`, etc.) per ROUTING map, injects into `brief-template.md` via LEARN markers. **Primary reuse channel: note → learn file → brief template → Naya behavior.**

**Data:** Smart Note markdown → distilled bullet → learn file section → brief template insertion.

**Where:** `~/workspace/goals/bring-naya-to-life/hidden_files/learn/` + `~/AGENTS.md` + `BRAIN/07-LEARNING/`.

**Done when:** Note's bullet is in its routed learn file AND reachable from brief-template. **Brutally honest:** integration ≠ behavior change. No production code measures whether reuse actually changed outcomes.

### 3.7 PROVE — Show the whole chain ran, with receipts

**Plain English:** Every transition leaves checkable evidence. Truth states are never collapsed: UNKNOWN ≠ VERIFIED ≠ PRODUCTION_PROVEN.

**Trigger:** Workflow completion; or any party running audit tools.

**Code:** Workflow job `cold-successor-held-out`: fresh identity re-reads note by hash, asserts byte match, asserts CANDIDATE ceiling, asserts retrieve returns correct note. `smart_note_v2.py::audit_registry()`: full reconciliation.

**Data:** `fresh-lesson-receipt.json`, `smart-note-capture-proof.json`, cold-retrieval objects, `learn/receipts/SN-XXXX.json`.

**Where:** GitHub Actions artifacts + `BRAIN/06-PROOF/` + workspace receipts.

**Done when:** All workflow jobs green; cold-successor assertions pass; `audit_registry()` reports no drift. **Never claimed:** VERIFIED → PRODUCTION_PROVEN requires live evidence; nothing manufactures it.

---

---

## 4. CURRENT STATE — WHAT'S CONNECTED

*Evidence current as of 2026-10-09. Every claim below is verifiable — file paths, commit SHAs, and workflow IDs are given.*

### Working Component 1: Smart Note Capture
Agents write Smart Note JSON files to `.naya/capture/`. **612 capture files** on main, landing daily. Connects to the smart-notes index and BRAIN projections.

### Working Component 2: Live Intelligence Commit Proof
`.github/workflows/live-intelligence-commit-proof.yml` proves the pipeline live and commits verified projections as "Naya Smart Note Projector." **1,180 `IB-SMART-NOTE-*.md` files** on main. Projection commits land daily.
**Partial:** the final `cold-successor-held-out` job is FAILING (3 consecutive failures on 2026-10-09).

### Working Component 3: Canonical Receiver on Production Supabase
Edge function `v7-smart-note-canonical` — sign in, POST a note, full pipeline runs. **Verified working 2026-10-08:** received `{ok: true, pipeline: "SMART_NOTE_CAPTURED_PROJECTION_DEFERRED"}`.
**Partial:** synchronous `PROJECTION_VERIFIED` guarantee no longer reachable — projection is now best-effort/non-blocking by design.

### Working Component 4: Supabase Production Deploy Pipeline
"Governed Production Promotion" workflow deploys edge functions + migrations. **Last run SUCCESS** on current main tip. 171 migrations, 15 edge functions deployed.

### Working Component 5: Live Supabase Runtime Proof
Exercises deployed edge functions live. **15 of 16 jobs success** (Oct 8). Tracks deploy health.

### Working Component 6: Node Runtime Proofs
- LAW, ACT, CVO, Verified AI Action: **green** (multiple successes today)
- KNOW: last success Sept 30 (stale)
- PROVE: **FAILING** (all recent runs)
- CONNECT: **zero runs ever**

### Working Component 7: Kernel Tests CI Gate
`.github/workflows/kernel-tests.yml` — runs Node tests, Python pytest, brain-index drift check. **Genuinely gates:** 4 broken pushes caught today before repair. 202 test files.

### Working Component 8: BRAIN Knowledge Base
**1,196 files** on main. Index drift-checked by CI (green). Connects to retrieval function and builder briefs.

### Working Component 9: Activation Mint
Mints sha256-bound activation receipts. **3 successful mints today.** Unified Activation Gate verifies byte-for-byte.

### Working Component 10: Governance Gates
Ratified Guard, Chain Readiness, Safety Grant, Spec Integrity, Design Gate — **all passing** on current PRs.

### What's NOT Working (Summary)
1. **Machine end-to-end capture** — 5/5 failures (contract mismatch: workflow expects `PROJECTION_VERIFIED`, receiver gives `PROJECTION_DEFERRED`)
2. **Canonical Smart Links** (`IB-<id>/smart-note.md` format) — zero ever committed
3. **Cold-successor-held-out job** — 3/3 failures today
4. **PROVE node proof** — all recent runs fail; **CONNECT proof** — never run

---

---

## 5. CURRENT STATE — WHAT'S NOT CONNECTED

> **This is the most important section in this document.** Every gap below was verified by searching the actual codebase. No hiding, no softening. If you're a builder, start here.

### 🔴 GAP 1 (CRITICAL): The CANDIDATE→ACTIVE ladder is a dead end

**What's missing:** New lessons enter as CANDIDATE. `promote_note()` only goes CANDIDATE→VERIFIED. The machinery for VERIFIED→RATIFIED→ACTIVE→LEARNED (`apply_elevation()` in `tools/truth_state_guard.py`) has **zero operational callers** — only tests call it. No CLI command exists to elevate. No code path redeems elevation grants.

**Where it should be:** `tools/smart_note_v2.py` (new subcommands) or a CLI wrapper around `truth_state_guard.apply_elevation()`.

**Impact:** Every lesson is frozen at CANDIDATE or VERIFIED forever. No intelligence can ever reach ACTIVE (the state retrieval treats as usable). The lifecycle is a write-only archive by construction.

### 🔴 GAP 2 (CRITICAL): ACT never queries KNOW — the decision math is dead code

**What's missing:** `Kernel.decide()` only traces SELF→LAW with an explicit disclaimer that other nodes didn't run. `evaluate_candidates()` (the 7-dimension scoring), `retrieval_eligible()` (the KNOW predicate) have **no operational callers** — only tests.

**Where it should be:** A decision path that runs `evaluate_candidates` over options *after* pulling applicable intelligence via `smart_note_v2.retrieve()`.

**Impact:** No decision in the system is informed by stored intelligence. The "math decides" doctrine runs on math that is never invoked. The entire capture chain feeds nothing.

### 🔴 GAP 3 (CRITICAL): All nine node specs are CANDIDATE drafts — zero wiring

**What's missing:** Every file in `~/workspace/nine-node-specs/` is "CANDIDATE — NOT RATIFIED — NOT MERGED." The specs define handshakes (SELF→KNOW, ACT→KNOW, LEARN→KNOW, EVOLVE→SELF) but state: *"It creates no obligation, changes no code, and authorizes nothing until ratified."* `grep` for `ExecutionHandoff` across all Python/TypeScript: **zero hits.**

**Where it should be:** Typed functions for each handoff: ACT-side emitter, KNOW-side receiver, LEARN→KNOW importer, etc.

**Impact:** SELF→LAW is the only node transition with code. The other eight batons exist only as unratified prose. There is no pipeline.

### 🟠 GAP 4 (HIGH): ACT→KNOW feedback arc missing

**What's missing:** Execution results are never recorded as knowledge. The `ExecutionHandoff` type doesn't exist in code.

**Impact:** Lessons have no execution source. Outcomes are never fed back. LEARN has nothing to learn *from*.

### 🟠 GAP 5 (HIGH): SELF accepts unverified lessons

**What's missing:** `SelfNode.record_experience()` takes any string, appends to durable state, returns "PRESERVED." No truth-state check. No link to the LEARN pipeline. No operational callers (only tests).

**Impact:** Unverified content gets stamped PRESERVED into identity state. The "never lose memory" goal rests on a list anyone can write anything into.

### 🟠 GAP 6 (HIGH): EVOLVE has no working code

**What's missing:** Cold successor reuse — the project's core promise — has no implementation. Only a weekly drill (`tools/cold_retrieve_drill/`) and a receipt file with no producer.

**Impact:** A successor reconstructs from files by hand. Nothing builds, hashes, or validates a handoff package.

### 🟠 GAP 7 (HIGH): REUSE and PROVE lifecycle steps have no code

**What's missing:** Of 7 lifecycle steps, REUSE (applying a lesson to a new decision) and PROVE (verifying execution and recording proof) have **zero implementing functions.**

**Impact:** Nothing applies a lesson to a new decision. Nothing proves the effect. Compounding cannot be demonstrated or attempted in code.

### 🟡 GAP 8 (MEDIUM): KNOW's retrieval predicate is bypassed

**What's missing:** `retrieval_eligible()` exists in math but `smart_note_v2.retrieve()` never calls it. Relevance dominates; truth state is only a tie-breaker.

**Impact:** Privacy scoping and authority checks exist in math but not in the serving path.

### 🟡 GAP 9 (MEDIUM): Canonical executable named in ops plan doesn't exist

**What's missing:** `BRAIN/90-OPERATIONS/0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.json` declares a "RATIFIED_EXECUTABLE" at `kernel/decision-calculus/value-calculus-v2.1.ts` — **the file doesn't exist.**

**Impact:** A canonical document asserts an executable with no file behind it.

---

### Gap Summary

| # | Gap | Severity | Blocks |
|---|-----|----------|--------|
| 1 | CANDIDATE→ACTIVE dead end | CRITICAL | All learning permanence |
| 2 | ACT never queries KNOW | CRITICAL | All intelligent decisions |
| 3 | Node specs unratified, zero wiring | CRITICAL | The entire pipeline |
| 4 | ACT→KNOW feedback missing | HIGH | Learning from outcomes |
| 5 | SELF accepts unverified lessons | HIGH | Memory integrity |
| 6 | EVOLVE has no code | HIGH | Successor continuity |
| 7 | REUSE + PROVE have no code | HIGH | Compounding |
| 8 | Retrieval predicate bypassed | MEDIUM | Governance |
| 9 | Phantom executable in ops plan | MEDIUM | Trust in docs |

---

---

## 6. THE CONNECTION PLAN

> For each gap in Section 5: exactly what to build, in what order. An agent should be able to execute these steps without asking questions.

### Build Order (by dependency)

**Phase 1 — Unblock the Flow (Gaps 1, 8)**

**Step 1.1: Wire the elevation ladder (Gap 1)**
1. Open `tools/truth_state_guard.py`. Read `apply_elevation()`. Understand its inputs (registry entry, grant) and outputs (mutated entry).
2. Open `tools/smart_note_v2.py`. Find the CLI subcommand list (~line 1179).
3. Add three subcommands: `elevate`, `ratify`, `activate`. Each one:
   - Takes a `--smart-note-id` argument
   - Loads the entry from `.naya/memory/smart-notes/index.json`
   - Calls `apply_elevation()` with the appropriate transition
   - Writes the mutated entry back atomically (use the existing `_atomic_write_json`)
   - Emits a receipt to stdout
4. Add a `--grant` flag for transitions requiring elevation grants (VERIFIED→RATIFIED).
5. Test: `python3 tools/smart_note_v2.py elevate --smart-note-id <test-id> --dry-run` should show the transition without writing.
6. Verify: run the existing `tests/test_elevation_grants.py` — must still pass.

**Step 1.2: Enforce retrieval predicate (Gap 8)**
1. Open `tools/smart_note_v2.py`. Find `retrieve()` (~line 597).
2. Import `retrieval_eligible` from `kernel/value_calculus.py`.
3. Before scoring results, filter: for each candidate entry, call `retrieval_eligible(entry, requester_context)`. Drop any that return BLOCKED.
4. The requester context must include: requester identity, scope, and purpose. If not available, fail closed (return empty + log).
5. Test: create a test entry with BLOCKED scope. Verify `retrieve()` no longer returns it.
6. Verify: existing retrieval tests still pass for eligible entries.

**Phase 2 — Connect Decision to Memory (Gap 2)**

**Step 2.1: Build the ACT→KNOW query path**
1. Open `kernel/nayapower_kernel.py`. Read `Kernel.decide()` (~line 94).
2. Before the LAW evaluation, add a KNOW query step:
   ```python
   # NEW: Query KNOW for applicable intelligence BEFORE deciding
   applicable_blocks = retrieve_applicable_intelligence(
       decision_context=proposal,
       truth_floor="VERIFIED",  # Only VERIFIED or above
       max_results=5
   )
   decision_context.intelligence = applicable_blocks
   ```
3. Implement `retrieve_applicable_intelligence()` in `kernel/`:
   - Takes decision context (what action is proposed, in what scope)
   - Calls `smart_note_v2.retrieve()` with the decision description as query
   - Filters to `truth_state` in {VERIFIED, RATIFIED, ACTIVE}
   - Returns top 5 with provenance
4. Pass `decision_context.intelligence` into `evaluate_candidates()` from `value_calculus.py`.
5. Test: create a VERIFIED test note about a decision domain. Propose a decision in that domain. Verify the note appears in the decision context.
6. Verify: `tests/test_value_calculus.py` still passes.

**Step 2.2: Wire evaluate_candidates as the decision engine**
1. In `Kernel.decide()`, after the KNOW query, call `evaluate_candidates(options, decision_context)`.
2. The function already exists in `kernel/value_calculus.py:330`. It needs: candidate actions, decision context (now including intelligence), and the LAW verdict.
3. If LAW says PROHIBITED, skip evaluation entirely (LAW runs first — this is already the design).
4. Log the winning candidate + score + which intelligence influenced it.
5. Test with the existing `test_value_calculus.py` fixtures.

**Phase 3 — Build the Missing Lifecycle Steps (Gaps 4, 7)**

**Step 3.1: Implement ACT→KNOW ExecutionHandoff (Gap 4)**
1. Define the `ExecutionHandoff` dataclass in `kernel/`:
   ```python
   @dataclass
   class ExecutionHandoff:
       execution_id: str
       decision_ref: str
       action_taken: str
       outcome_observed: str
       timestamp: str
       provenance: dict  # LAW receipt ID, ACT receipt ID
   ```
2. In the ACT execution path (wherever actions complete), construct and emit this handoff.
3. On the KNOW side: add `ingest_execution(handoff)` that creates a knowledge edge (type `PRODUCES`) linking the action to its outcome.
4. Test: execute a test action, verify the edge appears in KNOW.

**Step 3.2: Implement REUSE (Gap 7a)**
1. Create `tools/reuse.py` (or add to `smart_note_v2.py`):
   ```python
   def reuse_for_decision(decision_context):
       """Retrieve ACTIVE learnings applicable to this decision."""
       applicable = retrieve_applicable_intelligence(
           decision_context,
           truth_floor="ACTIVE",  # REUSE requires ACTIVE, not just VERIFIED
           max_results=3
       )
       return attach_to_evaluation(applicable, decision_context)
   ```
2. Call this from the decision path built in Step 2.1.
3. Log which learnings were attached to which decisions (for later PROVE).

**Step 3.3: Implement PROVE (Gap 7b)**
1. Create `tools/prove.py`:
   ```python
   def prove_execution(execution_id, observation_window_days=7):
       """Check if the execution had the predicted outcome."""
       execution = get_execution_receipt(execution_id)
       observations = get_observations(execution_id, observation_window_days)
       verdict = compare_predicted_vs_actual(execution, observations)
       if verdict.matches:
           write_proof_to_know(execution_id, verdict)
       return verdict
   ```
2. The proof writes back to KNOW with lineage linking execution → outcome → verdict.
3. Test: run on a historical execution with known outcome.

**Phase 4 — Harden Identity and Succession (Gaps 5, 6)**

**Step 4.1: Gate SELF.record_experience (Gap 5)**
1. Open `kernel/self_node.py`. Find `record_experience()` (~line 114).
2. Change signature to accept `smart_note_id` instead of raw `lesson: str`.
3. Before appending: resolve the note's `truth_state` from the registry.
4. If `truth_state` not in {VERIFIED, RATIFIED, ACTIVE, LEARNED}: refuse with `{"status": "REFUSED", "reason": "truth_state below VERIFIED"}`.
5. If accepted: store the note ID (not the text) + truth state + timestamp.
6. Update `tests/test_self_node.py` for the new signature.

**Step 4.2: Build EVOLVE successor package (Gap 6)**
1. Create `tools/evolve.py`:
   ```python
   def build_successor_package():
       """Assemble everything the next cycle needs."""
       return {
           "identity_context": get_current_identity(),
           "mission": get_ratified_mission(),
           "current_truth": get_active_learnings(),  # Only ACTIVE+
           "authority_boundary": get_authority_boundary(),
           "material_blockers": get_open_blockers(),
           "next_action": get_next_action(),
           "package_hash": sha256(canonicalize(package)),
       }
   ```
2. Add `verify_successor_package(package)` that checks the hash and validates all required fields present.
3. This does NOT need the full EVOLVE spec ratified — it's the minimal viable handoff.

**Phase 5 — Fix the Docs (Gap 9)**

**Step 5.1: Correct the ops plan**
1. Open `BRAIN/90-OPERATIONS/0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.json`.
2. Find the `decision_value_calculus_v2_1` claim.
3. Either: (a) create the file it names, or (b) correct the claim to name `kernel/value_calculus.py` (which exists) and note its caller status.
4. Option (b) is faster and more honest. Do (b).

---

### Dependency Graph

```
Phase 1 (1.1, 1.2) ──→ Phase 2 (2.1, 2.2) ──→ Phase 3 (3.1, 3.2, 3.3)
                                                        │
Phase 4 (4.1, 4.2) ←── independent ────────────────────┘
Phase 5 (5.1) ←── independent, do anytime
```

Phase 1 must come first (unblocks the truth-state flow).
Phase 2 depends on Phase 1 (needs ACTIVE notes to exist).
Phase 3 depends on Phase 2 (needs the decision path to hook into).
Phases 4 and 5 are independent — can run in parallel with any phase.

---

---

## 7. WHAT "DONE RIGHT" LOOKS LIKE

> Concrete acceptance criteria. For each connection built in Section 6: how to prove it works, what tests to run, what evidence to produce. Nothing is "done" until the proof exists.

### Acceptance Criteria by Phase

**Phase 1 — Unblock the Flow**

✅ **1.1 Elevation ladder works when:**
- `python3 tools/smart_note_v2.py elevate --smart-note-id <id> --dry-run` shows the correct transition without writing
- A real elevation (CANDIDATE→VERIFIED→RATIFIED→ACTIVE) completes end-to-end on a test note
- The registry entry's `truth_state` field actually changes in `.naya/memory/smart-notes/index.json`
- `tests/test_elevation_grants.py` passes
- **Evidence:** before/after registry JSON diff + test output

✅ **1.2 Retrieval predicate enforced when:**
- A test entry with BLOCKED scope is NOT returned by `retrieve()`
- An entry with VERIFIED state and matching scope IS returned
- All existing retrieval tests pass
- **Evidence:** test script output showing blocked entry excluded

**Phase 2 — Connect Decision to Memory**

✅ **2.1 ACT queries KNOW when:**
- Proposing a decision in a domain with a VERIFIED test note results in that note appearing in `decision_context.intelligence`
- The decision log shows which intelligence was consulted
- A decision proposed with zero applicable notes still works (empty intelligence, not an error)
- **Evidence:** decision log with intelligence section populated

✅ **2.2 evaluate_candidates runs when:**
- `Kernel.decide()` calls `evaluate_candidates()` (verify by code inspection + log output)
- The winning candidate's score is logged with dimension breakdown
- LAW PROHIBITED still short-circuits (no evaluation on prohibited actions)
- **Evidence:** decide() trace showing evaluation ran

**Phase 3 — Missing Lifecycle Steps**

✅ **3.1 ExecutionHandoff works when:**
- Completing a test action produces an `ExecutionHandoff` object
- The handoff appears as a knowledge edge in KNOW (queryable)
- The edge links action → outcome with provenance
- **Evidence:** KNOW query returning the execution edge

✅ **3.2 REUSE works when:**
- A decision in a domain with an ACTIVE learning attaches that learning to the evaluation
- The decision log records which learnings were attached
- A decision with no ACTIVE learnings proceeds normally
- **Evidence:** decision log with reuse section

✅ **3.3 PROVE works when:**
- `prove_execution()` on a historical execution returns a verdict (MATCH or MISMATCH)
- The verdict is written back to KNOW with lineage
- A MISMATCH verdict triggers a flag (not silent)
- **Evidence:** KNOW entry for the proof with execution lineage

**Phase 4 — Harden Identity and Succession**

✅ **4.1 SELF gate works when:**
- `record_experience(smart_note_id)` with a CANDIDATE note returns REFUSED
- `record_experience(smart_note_id)` with a VERIFIED note returns PRESERVED
- The stored entry references the note ID, not raw text
- `tests/test_self_node.py` passes with new signature
- **Evidence:** test output showing refuse/accept behavior

✅ **4.2 Successor package works when:**
- `build_successor_package()` returns all required fields
- `verify_successor_package()` validates the hash correctly
- Tampering with the package causes verification to fail
- **Evidence:** package JSON + verification output

**Phase 5 — Fix the Docs**

✅ **5.1 Ops plan corrected when:**
- The JSON no longer references a non-existent file
- The claim matches reality (names `kernel/value_calculus.py`, notes caller status)
- **Evidence:** diff of the JSON file

---

### The Ultimate Test

After all phases complete, run this end-to-end:

1. Shawn says "smart note this: [a new lesson]"
2. The note is captured → governed → verified → recorded
3. Elevate it to ACTIVE using the new CLI
4. Propose a decision in the lesson's domain
5. **Verify:** the decision context includes the lesson (Phase 2 working)
6. **Verify:** the decision is influenced by the lesson (Phase 3 REUSE working)
7. Execute the decision
8. **Verify:** the execution is recorded in KNOW (Phase 3 handoff working)
9. Run PROVE on the execution
10. **Verify:** the proof is written back (Phase 3 PROVE working)
11. Build a successor package
12. **Verify:** the package validates (Phase 4 working)
13. Cold Naya retrieves the lesson and applies it correctly
14. **Verify:** behavior changed because of the lesson (not coincidence)

**If all 14 steps pass: the system learns. If any step fails: that's the next gap to fix.**

---

### What "Done" Does NOT Mean

- ❌ "The code is written" — code without passing acceptance criteria is not done
- ❌ "The tests pass" — tests passing on mock data is not done; test on real flows
- ❌ "It should work" — "should" is not evidence
- ❌ "Shawn said it's fine" — his approval doesn't replace verification
- ✅ "The acceptance criteria above are met with evidence" — this is done

---

---

## 8. VISUAL MAPS

### Map 1: The Nine Nodes and Their Connections (Target Architecture)

```
                        ┌─────────────────────────────────────────────────┐
                        │                    SELF                         │
                        │              (Identity Gate)                    │
                        │  "Who am I? What's my mission? Am I genuine?"   │
                        └──────────┬──────────────────────▲───────────────┘
                                   │                      │
                          identity │                      │ successor
                          context  │                      │ package
                                   ▼                      │
                        ┌─────────────────────────────────────────────────┐
                        │                     LAW                         │
                        │            (Constitutional Gate)                │
                        │  "Is this allowed? PROHIBITED / NEEDS_AUTH /    │
                        │   NEEDS_EVIDENCE / ADMISSIBLE"                  │
                        └──────────┬──────────────────────▲───────────────┘
                                   │                      │
                          verdict +│                      │ violations
                          baton    │                      │
                                   ▼                      │
                        ┌─────────────────────────────────────────────────┐
                        │                     ACT                         │
                        │                 (The Hands)                     │
                        │  "Execute the authorized action. Record what    │
                        │   happened. Nothing more, nothing less."        │
                        └────┬─────────────────────────┬────────────────┘
                             │                         │
              ExecutionHandoff│                         │ execution record
                             ▼                         ▼
        ┌─────────────────────────────┐    ┌─────────────────────────────┐
        │            KNOW             │    │           VERIFY            │
        │          (Memory)           │    │      (Immune System)        │
        │  "Store it. Classify it.   │    │  "Independently re-derive.  │
        │   Serve the right piece    │    │   Attack the claim. A       │
        │   at the right time."      │    │   different seat checks."   │
        └────┬──────────┬────────────┘    └────┬───────────┬────────────┘
             │          │                      │           │
    know     │          │ serving               │ baton     │ failures
    receipt  │          │ path                  │           │
             ▼          ▼                       ▼           ▼
        ┌─────────────┐ ┌─────────────┐   ┌─────────────┐ ┌─────────────┐
        │    PROVE    │ │   CONNECT   │   │    LEARN    │ │   EVOLVE    │
        │ (Evidence   │ │ (Context    │   │(Compounding │ │ (Successor) │
        │  Judge)     │ │  Broker)    │   │  Organ)     │ │             │
        └──────┬──────┘ └──────┬──────┘   └──────┬──────┘ └──────┬──────┘
               │               │                 │               │
               └───────────────┴────────┬────────┴───────────────┘
                                        │
                                        ▼
                              Back to SELF (new cycle)
```

### Map 2: The Learning Lifecycle Flow

```
Shawn says "smart note this"
         │
         ▼
┌─────────────────┐
│    1. CAPTURE   │  Agent writes JSON → .naya/capture/
│    ✅ WORKS     │  Trigger: human instruction or proactive capture
└────────┬────────┘
         │ push to main
         ▼
┌─────────────────┐
│    2. GOVERN    │  Admission gate: authority check, toxicity filter
│    ✅ WORKS     │  Truth ceiling: CANDIDATE (never higher at capture)
└────────┬────────┘
         │ workflow job
         ▼
┌─────────────────┐
│    3. VERIFY    │  Independent re-read, byte-match proof
│  ⚠️ PARTIAL    │  Promotion to VERIFIED rarely happens
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    4. RECORD    │  Supabase + registry + BRAIN projection
│    ✅ WORKS     │  Three durable copies
└────────┬────────┘
         │
    ┌────┴──────────────────────────────┐
    │  🔴 GAP 1: NOTHING PROMOTES TO    │
    │  ACTIVE. The chain stops here.    │
    └────┬──────────────────────────────┘
         │ (after Phase 1 fix)
         ▼
┌─────────────────┐
│   5. RETRIEVE   │  Query → keyword match → best note
│    ✅ WORKS     │  Cold Naya can retrieve with git clone
│  ⚠️ predicate  │
│    bypassed     │
└────────┬────────┘
         │
    ┌────┴──────────────────────────────┐
    │  🔴 GAP 2: ACT NEVER QUERIES.     │
    │  Retrieved notes feed nothing.    │
    └────┬──────────────────────────────┘
         │ (after Phase 2 fix)
         ▼
┌─────────────────┐
│    6. REUSE     │  Lesson attached to decision evaluation
│   🔴 NO CODE   │  "Stored" becomes "learned" HERE
└────────┬────────┘
         │ (after Phase 3 fix)
         ▼
┌─────────────────┐
│    7. PROVE     │  Execution verified, proof written to KNOW
│   🔴 NO CODE   │  Closes the loop with evidence
└─────────────────┘
```

### Map 3: Current vs Target Architecture

```
CURRENT STATE (2026-10-09):
═══════════════════════════════════════════════════════════════

  CAPTURE ──→ GOVERN ──→ VERIFY ──→ RECORD ──→ [WALL]
    ✅          ✅        ⚠️          ✅
                                              ║
                                         Nothing passes.
                                         CANDIDATE frozen.
                                              ║
  RETRIEVE (orphaned)    ACT (no memory)    NODES (spec-only)
    ✅                     🔴                 🔴
  Works but feeds       Never queries       8 of 9 connections
  nothing               KNOW                exist only on paper


TARGET STATE (after blueprint execution):
═══════════════════════════════════════════════════════════════

  CAPTURE ──→ GOVERN ──→ VERIFY ──→ RECORD ──→ ELEVATE ──→ ACTIVE
    ✅          ✅        ✅          ✅          ✅(new)      ✅(new)
                                                              ║
                                                              ║
  ┌─────────────────────────────────────────────────────────╜
  │
  ▼
  RETRIEVE ──→ REUSE ──→ DECIDE ──→ ACT ──→ PROVE ──→ KNOW
    ✅          ✅(new)    ✅(new)    ✅       ✅(new)    ✅
                                      │
                                      ▼
                              ExecutionHandoff
                              (feeds back to KNOW)
                                      │
                                      ▼
                              LEARN ──→ EVOLVE ──→ SELF (next cycle)
                              ✅(wired)  ✅(built)   ✅(gated)
```

### Map 4: Data Flow — Where Things Live

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    GitHub    │     │   Supabase   │     │  Workspace   │
│    (Repo)    │     │  (Database)  │     │   (Local)    │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ .naya/       │     │ smart_note_  │     │ learn/       │
│  capture/    │────▶│  events      │     │  doctrine.md │
│  (input)     │     │  artifacts   │     │  laws.md     │
│              │     │  receipts    │     │  ledger.json │
├──────────────┤     ├──────────────┤     │  receipts/   │
│ .naya/       │     │ nayanet_     │     ├──────────────┤
│  memory/     │◀────│  intelligent │     │ AGENTS.md    │
│  smart-notes/│     │  _blocks     │     │  (Lessons)   │
│  index.json  │     │              │     ├──────────────┤
│  (registry)  │     │ 15 edge      │     │ brief-       │
├──────────────┤     │ functions    │     │ template.md  │
│ BRAIN/       │     │              │     │ (LEARN       │
│  05-MEMORY/  │     │              │     │  markers)    │
│  06-PROOF/   │     │              │     │              │
│  07-LEARNING/│     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
       ▲                    ▲                    ▲
       │                    │                    │
       └────────────────────┴────────────────────┘
                  All three must agree.
              (audit_registry checks this)
```

---

## APPENDIX: Document Control

| Field | Value |
|-------|-------|
| Title | THE SYSTEM BLUEPRINT — NayaPOWER Complete Architecture & Build Manual |
| Version | 1.0 |
| Date | 2026-10-09 |
| Author | Naya 4 (synthesis) + 4 research agents |
| Status | CANDIDATE — not ratified |
| Location | `~/workspace/goals/bring-naya-to-life/files/SYSTEM-BLUEPRINT-20261009.md` |

### Sources Consulted
- `~/workspace/nine-node-specs/` — all 9 node specs (CANDIDATE)
- `~/workspace/repo-ground/NayaPOWER/` — codebase (grep-verified)
- `~/workspace/kernel-9org/` — kernel contracts and runtimes
- `~/workspace/w3-nodes9-cycle/` — w3 harness results
- `~/workspace/goals/bring-naya-to-life/hidden_files/learn/` — learn_ingest.py, doctrine files
- GitHub `SoulSchoolAcademy/NayaPOWER` — verified against main tip `1d736522`

### What This Document Is
A build manual. Every section tells you what exists, what's missing, and exactly what to do.

### What This Document Is Not
- Not a status report (it doesn't say "we're 70% done")
- Not a proposal (it doesn't ask permission)
- Not a vision deck (Section 1 is the only vision; the rest is engineering)

### How to Use It
1. **Shawn reads Section 1** — the vision in plain English
2. **Builders read Sections 5, 6, 7** — gaps, plan, acceptance criteria
3. **Architects read Sections 2, 3, 8** — nodes, lifecycle, maps
4. **Auditors read Section 4** — what's verified working

---

*End of blueprint. Now build it.*
