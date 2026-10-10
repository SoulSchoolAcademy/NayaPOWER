# THE NAYAPOWER LEARNING SYSTEM — COMPLETE BLUEPRINT v1

> **Relationship to canonical blueprint:** This document is the **deep diagnostic companion** to the canonical [Learning Engine Assembly Blueprint (PR #2037)](./LEARNING-ENGINE-ASSEMBLY-BLUEPRINT-2026-10-09.md), which is the authoritative assembly plan and 14-agent execution contract. This companion provides the evidence-tagged system truth, gap inventory, and detailed work orders with exact files/lines that the assembly blueprint builds on. If the two ever conflict on architecture, #2037 wins. If they conflict on current-state facts, this document's [PROVEN] tags win (it was verified against live code).

**Status:** v1 COMPLETE — all four research lanes verified against live main `1d73652231ac6127806640af5a31eb516c60738d`. Pending leader review.
**Authority:** Shawn Vibert, Human Director
**Purpose:** The single document every team leader and every agent follows to assemble the learning system correctly. No agent acts from memory or assumption — this document is the source of truth.
**Rule:** Nothing in this document is claimed without evidence. Every current-state claim carries a tag: [PROVEN] (read the code), [REPORTED] (a seat said it, not yet independently read), [UNVERIFIED] (could not confirm).

---

## PART 0 — THE ONE-PAGE PICTURE

*(For leaders: read this and you understand the whole system. For agents: this is the map; the detailed instructions follow.)*

```
YOU SAY "SMART NOTE THIS"
        │
        ▼
┌──────────────┐
│  1. CAPTURE  │  LEARN node distills your words → human note + machine record
└──────┬───────┘
       ▼
┌──────────────┐
│  2. PERSIST  │  Saved to GitHub (permanent file) AND Supabase (database row)
└──────┬───────┘  Label: CANDIDATE (unverified)
       ▼
┌──────────────┐
│  3. INDEX    │  KNOW node tags it: what situation, when it applies
└──────┬───────┘
       ▼
┌──────────────┐
│  4. VERIFY   │  Independent checker confirms the lesson is real and correct
└──────┬───────┘
       ▼
┌──────────────┐
│  5. PROMOTE  │  LAW node moves it CANDIDATE → ACTIVE   ← ⚠️ NEVER BUILT
└──────┬───────┘
       ▼
┌──────────────┐
│  6. INTEGRATE│  SELF weaves it into behavior patterns  ← ⚠️ NEVER BUILT
└──────┬───────┘
       ▼
┌──────────────┐
│  7. ACT      │  Before deciding, ACT queries KNOW      ← ⚠️ NEVER WIRED
└──────┬───────┘  Behavior changes because of the lesson
       ▼
┌──────────────┐
│  8. PROVE    │  PROVE documents the behavior change with evidence
└──────┬───────┘
       ▼
┌──────────────┐
│  9. SHARE /  │  CONNECT shares it · EVOLVE: a cold Naya retrieves
│    EVOLVE    │  and uses it correctly without being taught
└──────────────┘
```

**Plain English:** Steps 1–2 are a filing cabinet. Steps 3–9 are the brain. The filing cabinet works. The brain was never assembled.

**The Smart Link** is printed after step 2. It proves filing, not learning. Learning is proven at step 9.

---

## PART 1 — THE NINE NODES

**Evidence:** Researcher verified against live main tip `1d73652231ac6127806640af5a31eb516c60738d`. Every node-directory file read. [PROVEN]

### The honest headline

Each node's contract folder (`BRAIN/03-KERNEL/NODES/<NAME>/`) contains **only markdown — zero executable code**. The real implementations live in **two other places**: the `kernel/` Python package at the repo root, and the `supabase/functions/nayanet-*` TypeScript edge functions. (Note: `naya_kernel/` does NOT exist — earlier references to it were wrong.)

The system's own documents are honest about the gap: the nine-node contract states *"universal nine-node production binding remains NOT_PROVEN"* and `BRAIN/03-KERNEL/MANIFEST.json` says `runtime_binding.status: NOT_PROVEN, entrypoint: null`. The kernel code itself admits: *"This reference kernel has established only the decision/authority boundary. It must not claim ACT/KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE ran."*

**Plain English:** We have nine beautifully written job descriptions, and seven of the nine employees actually exist — but they work in different buildings and have never been in the same room together.

### The node table

| Node | What it's FOR (plain English) | Where it actually runs | Verdict |
|---|---|---|---|
| SELF | Who am I? Identity, mission, continuity | `kernel/self_node.py` (235 lines), `kernel/persona_loader.py`, `kernel/naya_identity_binding.py` — tested | BUILT [PROVEN] |
| KNOW | The memory — store and retrieve intelligence | `supabase/functions/nayanet-know-runtime/` (~25KB TS), `kernel/brain_registry.py` — tested | BUILT [PROVEN] |
| ACT | Do things safely — plan, check authority, execute, refuse when wrong | `kernel/act_pipeline.py` (440 lines: PLAN→EXECUTE, fail-closed), `kernel/value_calculus.py` (994 lines), `supabase/functions/nayanet-act-runtime/` (~42KB) — tested | BUILT [PROVEN] |
| VERIFY | Did it work? Check outcomes against expectations | Distributed: `nayanet-causal-verify` (19KB), `nayanet-verified-ai-action` (29KB) — no single module | BUILT (distributed) [PROVEN] |
| PROVE | Show your work — evidence, lineage, truth state | `supabase/functions/nayanet-prove-runtime/` (~22KB) — tested | BUILT [PROVEN] |
| CONNECT | Find related things — retrieval, relationships | Distributed: `_shared/connect_selector.ts`, `nayanet-intelligence-retrieve/` — no single module | BUILT (distributed) [PROVEN] |
| LAW | Permission — authorized, denied, or needs-a-human | `supabase/functions/nayanet-law-runtime/` (~11.6KB), `kernel/protocol/authority_gate.py` — tested | BUILT [PROVEN] |
| LEARN | Turn verified experience into future behavior | Seams exist: `nayanet-learning-verify` (39.8KB), `kernel/protocol/learning_capture.py` (44 lines — thin). **The closed loop (experience → behavior change → measured compounding) is NOT evidenced as a working pipeline.** | PARTIAL [PROVEN] |
| EVOLVE | Succession — a new Naya picks up where the last left off | Succession mechanics exist: cold-runtime-proof, cold-successor receipts. Improvement governance is spec-only. | PARTIAL [PROVEN] |

### What each node takes in and puts out

*(From each node's `0001-CONTRACT.md`, read at live tip [PROVEN])*

- **SELF** — In: constitution, mission, execution state, successor context. Out: identity context, current objective, known/unknown boundary.
- **KNOW** — In: canonical objects/events, retrieval requests, provenance. Out: intelligence context, retrieval candidates with provenance + uncertainty.
- **ACT** — In: authorized context from LAW, action plan, reversibility classification. Out: plan, action, execution state, receipts. Refuses fail-closed with codes.
- **VERIFY** — In: expected outcome, observed data, evidence. Out: SUCCESS / FAILURE / INCONCLUSIVE / NOT_PROVEN + verification receipt.
- **PROVE** — In: claims, evidence, verification methods. Out: truth state (CLAIMED/SUPPORTED/VERIFIED…), proof status + limitations.
- **CONNECT** — In: intelligence objects, retrieval queries, contradiction rules. Out: relevant intelligence set, applicability assessment, freshness indicators.
- **LAW** — In: actor identity, proposed action, governance contracts. Out: AUTHORIZED / DENIED / REQUIRES_CONFIRMATION / AMBIGUOUS / EXPIRED / REVOKED / OUT_OF_SCOPE.
- **LEARN** — In: observations, VERIFY's qualifying outcomes, contradiction reports. Out: learning candidate (CANDIDATE/VERIFIED/REJECTED/CONTRADICTED), promoted learning, compounding measurement.
- **EVOLVE** — In: current truth state, verified learnings, observed gaps. Out: successor package, improvement proposal, evolution state.

### Which workflows exercise which nodes [PROVEN]

`kernel-tests.yml` runs the Python `kernel/` package tests on every push. The `live-*-proof.yml` workflows exercise the Supabase runtimes: LAW, KNOW, ACT, CONNECT, PROVE, VERIFY (causal-verify), intelligence-commit (KNOW/LAW/CONNECT seams). Eleven other workflows (activation, design-gate, spec-integrity, etc.) do **not** invoke node code — they run `tools/*.py` gate scripts.

### What this means for the blueprint

Seven nodes have real, tested implementations. LEARN and EVOLVE are partial — the pieces exist but the loops they promise (learn → behavior change → compound; propose → authorize → adopt) are not evidenced as working pipelines. And no single entrypoint wires all nine together — that binding is NOT_PROVEN by the system's own admission.

**What was NOT verified:** whether test suites currently pass on tip (not executed), whether live-proof workflows recently passed (run history not checked), behavior inside the TS runtime files beyond existence/size.

---

## PART 2 — THE LEARNING CHAIN, STEP BY STEP

**Evidence:** Researcher verified every step by reading the actual workflow files and code at live main tip `1d73652231ac6127806640af5a31eb516c60738d`. All claims [PROVEN] unless marked.

### The chain as built

**Step 0 — Capture lands in `.naya/capture/` — EXISTS [PROVEN]**
A JSON capture file is authored and merged into main (e.g. PR #2020, merged 2026-10-09T19:25:09Z, added `.naya/capture/20261009-successor-t11-reserve-rule-canonical.json`). Nothing watches the directory itself — the file must reach main via commit/PR. The capture README states: capture requests may reach CANDIDATE automatically, *never VERIFIED/ACTIVE merely by being captured*. (~190 capture JSONs on main.)

**Step 1 — Receiver workflow fires — EXISTS [PROVEN]**
`.github/workflows/live-intelligence-commit-proof.yml` ("Live Intelligence Commit Proof") — the ONLY workflow with `.naya/capture` in its triggers. Fires on push to main touching `.naya/capture/**`.

**Step 2 — Canonical commit to runtime — EXISTS [PROVEN]**
The workflow POSTs to the Supabase edge function `nayanet-intelligence-commit-runtime`. Key line: `p_understanding_state: String(body.p_understanding_state ?? "CANDIDATE")` — the write path hardcodes the CANDIDATE ceiling. Writes to Supabase: event row, intelligent block, lineage, relationship, runtime-index entry, checkpoint, commit receipt.

**Step 3 — Independent re-read — EXISTS [PROVEN]**
A second short-lived identity re-reads the same persisted objects and asserts equality. (Not the same eyes that wrote it.)

**Step 4 — Projection + publish — EXISTS [PROVEN]**
`python -m tools.smart_note_v2 project` renders the human-readable note under `BRAIN/05-MEMORY/SMART-NOTES/.../` and `update_registry()` writes `.naya/memory/smart-notes/index.json` — registry `truth_state` ← runtime block's `understanding_state` (i.e. CANDIDATE). Then commits and pushes back to main (loop-guarded).

**Step 5 — Cold retrieval + lifecycle gate — EXISTS [PROVEN]**
Exact content-hash retrieval from the machine registry, then: `assert lifecycle_state in {"ACTIVE","SUPERSEDED"}` (via `tools/sn002_conformance.py:140`), plus a held-out behavioral test proving the retrieved note changes a decision on a task distinct from the capture prompt. On failure: RED, fail-closed.

**Step 6 — Learning candidate + causal experiment — EXISTS [PROVEN]**
`.github/workflows/live-supabase-runtime-proof.yml` fires on commit-proof completion. POSTs `{"mode":"candidate"}` to `nayanet-learning-verify`; runs the causal control-vs-treatment experiment; writes a `learning_evidence` row (status CANDIDATE) in Supabase.

**Step 7 — Promotion CANDIDATE → ACTIVE — EXISTS IN SUPABASE, NO BACK-SYNC [PROVEN]**
The same workflow POSTs a promotion payload to `nayanet-learning-verify` (`index.ts` lines 447–682): validates receipts, then sets `learning_evidence.status` → "ACTIVE", block `understanding_state` → "LEARNED". A fresh independent identity re-reads and asserts persistence.

**⚠️ THE GAP:** `live-supabase-runtime-proof.yml` has `contents: read` — nothing ever writes the promotion back to the repo. `.naya/memory/smart-notes/index.json` keeps `truth_state: CANDIDATE` forever. The database says LEARNED; the repo says CANDIDATE. Two truth systems, diverged.

**Step 8 — Repo-side promotion — EXISTS AS CODE, NEVER INVOKED [PROVEN]**
`tools/smart_note_v2.py` "PROMOTION WRITER" (`promote_note()`, ~line 721): real thresholds (≥2 evidence items, ≥2 distinct gatherers, promoter≠gatherer, ≤90-day evidence). **Zero callers repo-wide** (verified by grep). `.naya/memory/smart-notes/promotions/` does not exist on main — no promotion receipt has ever been written.

**Step 9 — Admission gate — EXISTS ON UNMERGED BRANCH ONLY [PROVEN]**
Branch `naya5/learning-admission-round2` @ `9fba596e8df01b3306c4bdacae6a17bc392e4593`: adds `tools/learning_admission_gate.py` (323 lines), `tools/learning_verification_queue.py`, tests, triage docs. **No PR exists. Zero callers.** The gate that rejects unverifiable candidates is itself not admitted.

**Step 10 — Retrieval servability — EXISTS [PROVEN]**
`nayanet-intelligence-retrieve/retrieve.ts:82` uses `SERVABLE_STATUS = {"ACTIVE","DURABLE","RELEASED"}`.

### The vocabulary problem [PROVEN]

Two different fields govern "is this lesson usable":
- `lifecycle_state` ∈ {ACTIVE, SUPERSEDED} — the capture/conformance gate (Step 5)
- `truth_state` / `understanding_state` ladder: CANDIDATE → TESTING → VERIFIED → RATIFIED → ACTIVE → LEARNED — the registry/runtime promotion (Steps 4, 7, 8)

The conformance gate and the promotion path operate on different fields. Worse: `lifecycle_state` defaults to ACTIVE in three places — a capture that omits the field passes the gate by default, not by assertion.

### What this means (corrected picture)

The earlier "missing hallway" framing needs correction. The promotion step EXISTS in the Supabase runtime path (Step 7). What's actually broken:

1. **No back-sync:** after the DB promotes to ACTIVE/LEARNED, the repo registry never learns about it. Anyone reading the repo sees CANDIDATE forever.
2. **Repo-side promotion is decorative:** `promote_note()` is complete tested code that nothing calls.
3. **The admission gate is stranded:** built, tested, no PR, no integration point.
4. **Two vocabularies** for the same question ("is this usable?"), with a default-ACTIVE hole in one of them.

**Plain English:** The hallway exists — it just doesn't connect to the rooms on either side. The database promotes lessons the repo never hears about. The repo has a promotion tool nobody runs. And the front door has a lock nobody installed.

**Not verified:** whether these workflows have run green end-to-end recently (Actions run history not checked); whether deployed Supabase functions match main bytes.

---

## PART 3 — GITHUB vs SUPABASE

**Evidence:** Researcher read the live receiver code, live Supabase rows (project `supabase-red-cable`, ACTIVE_HEALTHY), and the live main tree. All [PROVEN] unless marked.

### What each one is for

**Supabase = the runtime system of capture, verification, and authority.**
The canonical receiver (`supabase/functions/v7-smart-note-canonical/index.ts`, 608 lines) writes per Smart Note:
- `smart_note_events` — 1 row (id, subject, privacy_state, status INCOMPLETE→VERIFIED)
- `smart_note_artifacts` — exactly 4 rows: HUMAN_NOTE, NAYA_NOTE, MACHINE_NOTE, INTELLIGENCE_FEED_NOTE
- `smart_note_receipts` — 1 row proving four-artifact completeness
- `v7_smart_note_transactions` — 1 row with idempotency_key (the dedup mechanism) + 7 jsonb payloads
- Plus: a `learning_evidence` row (status CANDIDATE), a checkpoint event, a 15-minute authority grant, a projection receipt

**GitHub = the human-viewable projection library.**
Readable `.md` Smart Notes under `BRAIN/05-MEMORY/SMART-NOTES/<YYYY>/<MM>/<DD>/...` and the human-facing registry `.naya/memory/smart-notes/index.json` (630 entries, `next_sequence` 783). Smart Links point here, not at Supabase.

### The real functional difference today

**The two are parallel, not connected.** The intended bridge — receiver writes to Supabase, then projects the verified note to GitHub with a Smart Link — is dead in practice: all 5 live projection receipts are `failed` (3× TRANSACTION_NOT_FOUND, 2× GITHUB_COMMIT_FAILED:403). **Zero `IB-######` directories exist under `BRAIN/05-MEMORY/SMART-NOTES/` on main.** The workflow `project-canonical-smart-note.yml` that the receiver's authority grant references does not exist in `.github/workflows/`.

The Smart Notes actually on main came through a different pipeline: agents (brain-build) commit `.md` files + registry entries via PRs. These are the `SN-####` notes — registry/backfill artifacts, not rows in the receiver's `smart_note_*` tables.

**Plain English:** We have two filing cabinets. Cabinet A (Supabase) has a proper check-in desk, stamps every item, and tracks everything — but its delivery truck to Cabinet B never runs (all deliveries failed). Cabinet B (GitHub) is where everyone actually looks, and it gets filled by hand-carry, bypassing the check-in desk entirely.

### Does anything query Supabase to change behavior? — YES, with a caveat [PROVEN]

1. **`naya-decision-context`** SELECTs `learning_evidence` (status=ACTIVE) and returns `influenced: true/false`. **But it conflates presence with influence** (`influenced = !!evidence`). The separating repair is **PR #1733, OPEN and unmerged**.
2. **`nayanet-act-runtime`** `readEligibleUniverse()` SELECTs the entire `nayanet_intelligent_blocks` universe (181 rows, all DURABLE) — the ACT runtime reads stored intelligence to act on.
3. **`nayanet-intelligence-retrieve`** ranked retrieval: the RPC `nayanet_retrieve_blocks` **does not exist in production** (migration `20261006235900` is PENDING_REVIEW_NOT_PRODUCTION_APPLIED) — this path is non-functional in production.

**Plain English:** Something DOES read the memory before acting (correcting the earlier "nothing queries it" claim). But reading is not the same as being influenced — and the code that would prove the difference is sitting in an unmerged PR.

---

## PART 4 — THE SMART NOTE PIPELINE

### Capture → Smart Link trace [PROVEN]

Two pipelines exist. The one producing notes on main is the **v2 agent pipeline**:

1. **Capture** — an agent writes a capture JSON to `.naya/capture/<id>.json`. The README is explicit: ingestion boundary, not the Brain; capture reaches CANDIDATE at most.
2. **Commit** — the capture is POSTed to `nayanet-intelligence-commit-runtime` (GitHub-OIDC auth), which persists the canonical lineage and returns verification JSON.
3. **Project** — `python -m tools.smart_note_v2 project` reserves the SN in a registry transaction, renders the `.md`, appends the registry entry to `.naya/memory/smart-notes/index.json`.
4. **Merge** — the `.md` + registry land on main via PR.
5. **Smart Link** — `tools/smart_link.py` generates and CI-gates it: shape check, resolves check (blob exists on main), uniqueness check.

### What a Smart Link IS [PROVEN]

"A Smart Link is the human-viewable proof of an intelligent event" (`tools/smart_link.py:3`).

Format:
```
https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/<projection_path>
```

Example (SN-0781, live on main):
`https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/05-MEMORY/SMART-NOTES/2026/10/09/SYSTEM-INTELLIGENCE/SCORECARD-DISCIPLINE/GATE-EXECUTION/SN-0781/IB-SMART-NOTE-20261009-sn0781-scorecard-must-run-the-gate.md`

Statuses: `ACTIVE` | `ACTIVE_AUTH_GATED` (PRIVATE notes — 404 for strangers) | `PENDING` | `SUPERSEDED` | `BROKEN` | `COLLISION`. Main-only; branch URLs are rejected.

### What a receipt IS [PROVEN] — three layers

1. **V7 receiver DB receipt** (`smart_note_receipts`): `{status: VERIFIED, event_id, artifact_count: 4, missing_types: []}` — proves four-artifact completeness, **nothing about truth**.
2. **V7 completion receipt** (API response): `intelligent_block_id`, `event_id`, `intelligent_block_hash` (SHA-256), `feed_verification`, `smart_link` (null today), `hub_deep_link`. Carries the checkpoint rule: *"Checkpoint persistence does not by itself prove learning; later retrieval and behavior change are required."*
3. **V2 registry entry** (`.naya/memory/smart-notes/index.json`): `smart_note_id`, `content_hash` (SHA-256 of canonicalized lesson), `truth_state`, `projection_path`, `smart_link`, `provenance` (event/lineage/relationship/index/checkpoint/receipt IDs). Promotion receipts go to `.naya/memory/smart-notes/promotions/` — **which does not exist on main** (no promotion has ever been recorded).

### What a Smart Link does NOT prove [PROVEN]

- **Not truth.** Notes are CANDIDATE by default. SN-0781's own header says "not yet ratified as law."
- **Not learning or behavioral influence.** Availability ≠ causal proof (SN-0544 doctrine).
- **Not content integrity by itself** — requires recomputing `content_hash` against the registry.
- **Not governance.** Registry entries can be written by backfill without provenance (SN-0781's entry has `provenance: null`).
- **Not currency.** SUPERSEDED/BROKEN/COLLISION statuses exist because a link can point at stale intelligence.

### Registry and collision state [PROVEN] — corrections to earlier claims

- `next_sequence` = **783**. Max SN on main = **SN-782**. One entry each for SN-0781 and SN-782, one directory each — **NO SN-0781/SN-782 collision on live main.** The earlier collision claim is REFUTED for these numbers.
- **But a live collision class exists elsewhere:** 629 numbered entries vs 610 distinct IDs — **19 duplicate SN numbers on live main** (SN-018, 019, 020, 022, 032, 034, 035, 041, 042, 346, 356, 357, 359, 361, 362, 501, 523, 524, 525 — each claimed by 2 different notes).
- No open PR claims a second SN-0781.

**Not verified:** whether the v7 receiver edge function is currently deployed/healthy in production (source read on main, deployed state not checked); `naya-decision-context`'s deployed behavior.

---

## PART 5 — THE THREE MISSING CONNECTIONS (THE ENGINE)

**Evidence:** Researcher verified every claim against live code at main tip `1d73652231ac6127806640af5a31eb516c60738d`, ran the branch's tests, and read the failed workflow's job log. The earlier "three missing connections" framing has been corrected where the evidence demanded it.

### Connection 1 — Candidate admission (design validation at creation)

**Earlier claim:** "The CANDIDATE→ACTIVE promotion step was never built."
**Corrected verdict:** The promotion EXISTS. What's missing is the admission gate.

- The Receiver (`v7-smart-note-canonical`) inserts `learning_evidence` as CANDIDATE and never updates it — **by design** (the commit-proof workflow asserts `promote_to_verified: False`; the Receiver must not promote).
- The promotion lives in `nayanet-learning-verify` (lines 535–546): CANDIDATE→ACTIVE, block→LEARNED, relationship→VERIFIED. It is wired and exercised by `live-supabase-runtime-proof.yml`.
- **The real gap:** no creation-time design validation gates any CANDIDATE write. Branch `naya5/learning-admission-round2` @ `9fba596e8df01b3306c4bdacae6a17bc392e4593` holds the gate (`tools/learning_admission_gate.py`, 323 lines; researcher ran the tests: **48/48 passed**). But: **no PR exists, zero callers on main**, and the diff touches no workflow — there is no slot it drops into.
- **Fix location:** `supabase/functions/nayanet-learning-verify/index.ts` at the `mode === "candidate"` write site (~line 378) — port the gate's contract into the write path, or add a workflow job that gates before candidate creation.

**Plain English:** The promotion hallway exists and works. What's missing is the bouncer at the front door — right now any candidate gets in, and the bouncer we built is standing outside with no door assigned to him.

### Connection 2 — Verified lessons → decisions (the dead seam)

**Earlier claim:** "ACT never queries KNOW/memory before deciding."
**Corrected verdict:** REFUTED as literally stated — but the real gap is worse in a different way.

- ACT **does** hard-require KNOW context: `nayanet-act-runtime/act.ts` refuses planning without a persisted KNOW receipt (`BLOCKED / KNOW_RECEIPT_REQUIRED`). It reads the live `nayanet_intelligent_blocks` universe and replays the KNOW selector over it. CI proves KNOW→ACT end-to-end.
- **The real gap:** `supabase/functions/naya-decision-context/index.ts` (2,814 bytes) is the one mechanism that queries the **verified-lesson store** (`learning_evidence` WHERE status=ACTIVE) and returns `USE_VERIFIED_LEARNING_CONTEXT`. It has **zero callers** — dead code. Only its test and SN-0544 reference it.
- ACT reads `nayanet_intelligent_blocks`, **never** `learning_evidence`. The store where CANDIDATE→ACTIVE promotion lands is never queried by any decision path.
- **Fix location:** in `nayanet-act-runtime/index.ts` `mode==="plan"` handler, after the LAW preflight and before `buildActPlan`, invoke the decision-context logic for the action's `target_id` and merge ACTIVE-lesson context into the plan. No branch/PR holds this fix.

**Plain English:** The decision-maker checks the library before acting — but the library's "verified lessons" shelf is in a different building nobody visits. The shuttle bus between them exists but has no driver.

### Connection 3 — Verified lessons → SELF's behavior (CONFIRMED missing)

- `kernel/self_node.py` `record_experience()` appends a caller-supplied string to `state.known` — preservation, not integration. **Zero production callers** (only its own unit test).
- Nothing reads `learning_evidence` ACTIVE rows into SELF. Nothing mutates behavior patterns, configs, or prompts from verified lessons. `persona_loader.py`: zero lesson references. `nayanet-verified-ai-action`: zero lesson references.
- The closest mechanism is ACT's per-plan steering (ephemeral, per-plan, lives in ACT not SELF). No persistent behavior-pattern update exists.
- **Fix location:** `kernel/self_node.py` — add an `integrate_verified_lesson()` seam that pulls ACTIVE rows, validates the verifier chain (doer≠scorer≠verifier), and applies them to a behavior-policy store; plus wire real callers to `record_experience`. No branch/PR holds this fix.

**Plain English:** Lessons get verified and shelved. Nobody ever takes one off the shelf and changes how they behave because of it. The "learning" in the learning system is the one part with no machinery.

### The live red: #2020's one-line failure [PROVEN from the job log]

Run `37980089547` (push of merge `075b169e`): `fresh-lesson` ✅, `independent-verification` ✅, `cold-successor-held-out` ❌. Job log ends with `AssertionError: CANDIDATE` at `licp.yml:1090`: `assert lifecycle_state in {"ACTIVE","SUPERSEDED"}`.

**Root cause:** the #2020 capture file declares top-level `"lifecycle_state": "CANDIDATE"`. The author put the truth state in the wrong field — the same file correctly declares `machine_view.automatic_truth_ceiling: "CANDIDATE"` (what the workflow actually expects). Sibling captures use `"ACTIVE"` for the lifecycle field.

**Fix: one line** — set `"lifecycle_state": "ACTIVE"` in `.naya/capture/20261009-successor-t11-reserve-rule-canonical.json` on main, then re-run via `workflow_dispatch` with the new SHA. No fix-forward commit exists yet.

**Plain English:** The T11 lesson failed its final check because of a typo-grade field error — the right value was in the file, in the wrong box. One line fixes it.

---

## PART 6 — HONEST INVENTORY OF EVERY GAP

Every gap below is [PROVEN] — read from live code at main tip `1d73652231ac6127806640af5a31eb516c60738d` — unless marked.

| # | Gap | Where | Evidence | Severity |
|---|---|---|---|---|
| G1 | No back-sync after runtime promotion: DB says ACTIVE/LEARNED, repo registry says CANDIDATE forever | `live-supabase-runtime-proof.yml` (`contents: read`); `.naya/memory/smart-notes/index.json` | Promotion writes DB only; nothing re-writes the registry | HIGH — two truth systems diverge |
| G2 | Repo-side promotion never invoked: `promote_note()` complete, zero callers, zero receipts | `tools/smart_note_v2.py:721`; `.naya/memory/smart-notes/promotions/` absent on main | Repo-wide grep: zero invocations | HIGH — the repo ladder is decorative |
| G3 | Admission gate unmerged, uncalled | Branch `naya5/learning-admission-round2` @ `9fba596e`; no PR; zero callers | Branch diff + grep | MEDIUM — unverifiable candidates can still enter |
| G4 | `naya-decision-context` dead code: zero callers | `supabase/functions/naya-decision-context/index.ts` | Grep: only test + SN-0544 reference it | HIGH — verified lessons never reach decisions |
| G5 | ACT never reads `learning_evidence` | `nayanet-act-runtime/index.ts` | Only 4 functions touch that table; ACT isn't one | HIGH — promotion lands where nobody looks |
| G6 | SELF has no behavior integration; `record_experience()` has zero production callers | `kernel/self_node.py` | Read in full; caller search | HIGH — the "learning" with no machinery |
| G7 | Receiver→GitHub projection bridge dead: all 5 receipts failed, zero `IB-######` dirs on main | `nayanet_github_dispatch_receipts`; main tree | Live DB rows + find | MEDIUM — two pipelines run in parallel |
| G8 | Ranked retrieval RPC missing in production | `information_schema.routines`; migration ledger | `nayanet_retrieve_blocks` doesn't exist; migration pending | MEDIUM — retrieval path non-functional in prod |
| G9 | Two vocabularies for "usable": `lifecycle_state` vs `truth_state`/`understanding_state`; `lifecycle_state` defaults to ACTIVE in 3 places | `sn002_conformance.py:135`, `smart_note_v2.py:573`, workflow inline | Read the defaults | MEDIUM — captures pass the gate by omission |
| G10 | 19 duplicate SN numbers on live main | `.naya/memory/smart-notes/index.json` (629 entries, 610 distinct IDs) | Counted | MEDIUM — registry integrity |
| G11 | #2020 capture has wrong `lifecycle_state` value; licp run RED, no fix-forward | `.naya/capture/20261009-successor-t11-reserve-rule-canonical.json`; run `37980089547` | Job log `AssertionError: CANDIDATE` | HIGH — live red, one-line fix |
| G12 | Nine-node production binding NOT_PROVEN (system's own admission) | `0004-NINE-NODE-ORGANISM-CONTRACT-V1.md`; `BRAIN/03-KERNEL/MANIFEST.json` | Read both | HIGH — no single wired entrypoint |
| G13 | `naya-decision-context` conflates presence with influence (`influenced = !!evidence`); repair PR #1733 open/unmerged | `naya-decision-context/index.ts`; PR #1733 state | Read code; API check | MEDIUM — even if wired, measures wrong |

**What is NOT a gap (earlier claims corrected by evidence):**
- "Promotion was never built" → promotion exists in `nayanet-learning-verify`, wired and CI-exercised.
- "ACT never queries memory" → ACT hard-requires KNOW receipts and reads the live block universe.
- "Nothing queries Supabase for behavior" → `naya-decision-context` and `nayanet-act-runtime` both query; the issue is *what* they query and whether the seam is wired.
- "SN-0781/SN-782 collision" → no collision on live main for these numbers.

---

## PART 7 — HOW TO CONNECT EACH GAP (AGENT INSTRUCTIONS)

**For agents:** each item below is a work order. Follow it exactly. Do not invent steps. If a step says "verify," run the verification — do not skip it.

### Work order 1 — Fix the #2020 live red (G11) — DO FIRST, 15 minutes

1. Read `.naya/capture/20261009-successor-t11-reserve-rule-canonical.json` on main.
2. Change top-level `"lifecycle_state": "CANDIDATE"` → `"lifecycle_state": "ACTIVE"`. Do NOT touch `machine_view.automatic_truth_ceiling` (stays `"CANDIDATE"` — that's correct).
3. Verify: the file's sibling captures use `"ACTIVE"` — confirm yours matches the pattern.
4. Commit on a branch, open a PR, merge under the Scorecard Law (five-step receipt on #1354).
5. Re-run the commit-proof workflow via `workflow_dispatch` with the new main SHA.
6. Verify: the successor run goes green on `cold-successor-held-out`.

### Work order 2 — Back-sync promotion to the repo registry (G1)

1. Read `.github/workflows/live-supabase-runtime-proof.yml`. Find where promotion completes (the reread asserting `learning.status == "ACTIVE"`).
2. Add a final job (needs `contents: write` — note the workflow currently has `contents: read`; this is a permission change, flag it in the PR): after promotion is confirmed, update `.naya/memory/smart-notes/index.json` — set the promoted note's `truth_state` to match the DB (`ACTIVE`/`LEARNED`).
3. The update must be idempotent (re-running with the same promotion is a no-op) and must carry the DB receipt IDs as provenance.
4. Test: run the workflow on a test capture, confirm the registry entry's `truth_state` changes after promotion.
5. **Human gate check:** `contents: write` on this workflow is a permission expansion — the permission change itself must be called out in the PR body.

### Work order 3 — Wire the admission gate (G3)

1. Fetch branch `naya5/learning-admission-round2` @ `9fba596e8df01b3306c4bdacae6a17bc392e4593`. Verify head SHA matches before using.
2. Open a PR from the branch (it has none). In the PR body, state clearly: this is a creation-time gate, not a promotion step.
3. Wire it: in `supabase/functions/nayanet-learning-verify/index.ts`, at the `mode === "candidate"` write site (~line 378), call the gate's contract before the INSERT. If TypeScript porting is needed, port `tools/learning_admission_gate.py`'s falsifiable-claim / pre-registered-criterion / doer≠scorer checks.
4. Alternative (if the TS change is blocked): add a workflow job in `live-supabase-runtime-proof.yml` that runs the Python gate before the candidate POST.
5. Verify: submit a deliberately unverifiable candidate; confirm it is rejected with a named reason. Submit a verifiable one; confirm it passes.
6. Merge under the Scorecard Law.

### Work order 4 — Wire the verified-lesson→decision seam (G4, G5, G13)

1. Read `supabase/functions/naya-decision-context/index.ts` in full (2,814 bytes).
2. In `supabase/functions/nayanet-act-runtime/index.ts`, in the `mode==="plan"` handler, after the LAW preflight and before `buildActPlan`: invoke the decision-context logic for the action's `target_id`, and merge returned ACTIVE-lesson context into the plan's learning context.
3. Apply the PR #1733 repair first (or port it): `influenced` must measure actual behavioral delta, not mere presence. Do not wire the conflated version.
4. Verify: create a CONTROL plan (no ACTIVE lessons for the target) and a TREATMENT plan (with an ACTIVE lesson); confirm the plans differ in the way the lesson prescribes, and that `influenced=true` only when the delta is observed.
5. Merge under the Scorecard Law.

### Work order 5 — Build SELF's behavior integration (G6)

1. Read `kernel/self_node.py` in full (235 lines).
2. Add `integrate_verified_lesson()`: pulls ACTIVE rows from `learning_evidence`, validates the verifier chain (doer≠scorer≠verifier — reuse the admission gate's contract), and applies the lesson to a behavior-policy store (new file: `kernel/behavior_policy.py` — start simple: a JSON store mapping situation → lesson-prescribed behavior, versioned).
3. Wire at least one real caller to `record_experience()` — pick the ACT pipeline's post-execution hook.
4. Verify: feed a verified lesson through `integrate_verified_lesson()`; confirm a subsequent decision in the same situation reflects the lesson; confirm the policy store is versioned and the change is reversible (rollback test).
5. Merge under the Scorecard Law.

### Work order 6 — Repair or retire the projection bridge (G7)

1. Read the 5 failed rows in `nayanet_github_dispatch_receipts`. Classify each failure (TRANSACTION_NOT_FOUND vs GITHUB_COMMIT_FAILED:403).
2. Decision: if the 403s are a permissions fix, fix permissions and re-run one projection manually; if the architecture is superseded by the v2 agent pipeline, formally retire the bridge (document the retirement, remove the dead authority-grant scope referencing the nonexistent `project-canonical-smart-note.yml`).
3. Do not leave it in the "looks like it works but doesn't" state. Either green or gone.

### Work order 7 — Registry deduplication (G10)

1. From `.naya/memory/smart-notes/index.json`, list the 19 duplicate SN numbers.
2. For each: determine which IB is canonical (first-claim stands per SN-033). Mark the other SUPERSEDED with a pointer to the canonical.
3. Add a CI gate: registry check fails on duplicate SN numbers (the mechanical form of the no-duplicate rule).
4. Merge under the Scorecard Law.

### Work order 8 — Vocabulary unification (G9)

1. Remove the `lifecycle_state` default-to-ACTIVE in all three places (`sn002_conformance.py:135`, `smart_note_v2.py:573`, workflow inline). A missing field must FAIL the gate, not pass it.
2. Document the mapping: `lifecycle_state` (capture envelope) vs `truth_state`/`understanding_state` (registry/runtime) — one page in `BRAIN/07-LEARNING/`, linked from both code sites.
3. Merge under the Scorecard Law.

---

## PART 8 — WHAT "DONE RIGHT" LOOKS LIKE (ACCEPTANCE CRITERIA)

**The rule:** "tests pass" is not done. Done means **observed behavior change**, verified by someone who didn't build it.

### Per-connection acceptance

| Connection | Done looks like | How to verify (not just tests) |
|---|---|---|
| WO1: #2020 fix | licp run green on `cold-successor-held-out` | Read the workflow run: all jobs green, `AssertionError` gone |
| WO2: back-sync | After a promotion, the repo registry's `truth_state` matches the DB within one workflow run | Promote a test capture; `git show` the registry diff; DB query confirms match |
| WO3: admission gate | An unverifiable candidate is rejected with a named reason, visible in the workflow log | Submit a bad candidate; read the rejection; submit a good one; read the acceptance |
| WO4: decision seam | CONTROL vs TREATMENT plans differ as the lesson prescribes; `influenced=true` only on observed delta | Run both; diff the plans; confirm the delta matches the lesson's prescription |
| WO5: SELF integration | A decision in a previously-seen situation reflects the integrated lesson; rollback restores prior behavior | Before/after decision transcripts; rollback test |
| WO6: projection bridge | Either a projection succeeds end-to-end (Smart Link resolves) or the bridge is formally retired with docs | One green projection OR a retirement record |
| WO7: dedup | Registry has zero duplicate SN numbers; CI fails on new duplicates | Count query = 0; submit a duplicate in a test branch, watch CI fail |
| WO8: vocabulary | A capture omitting `lifecycle_state` fails the gate (not passes) | Submit a field-less capture in a test; confirm RED with the right error |

### System-level acceptance: the first closed loop

One lesson, all nine steps, eyes on each one:
1. A novel, falsifiable lesson is captured.
2. It captures, persists, indexes, verifies, promotes (DB + repo in sync).
3. A cold Naya — one that never saw the lesson — retrieves it and applies it correctly to a held-out task.
4. An independent verifier confirms the behavior change and that it came from the lesson (not from the prompt).
5. The receipt chain is complete: capture → promotion → retrieval → behavior → proof, every link carrying hashes.

**That is the first real proof the system learns. Everything before it is assembly.**

---

## PART 9 — ORDER OF OPERATIONS

### Phase 1 — Stop the bleeding (today)
1. **WO1** — one-line #2020 fix, re-run licp. (15 min. Unblocks the commit-proof pipeline.)
2. **WO8** — remove default-ACTIVE. (30 min. Closes the pass-by-omission hole.)

### Phase 2 — Connect the hallway (this week)
3. **WO3** — wire the admission gate. (Bouncer at the front door.)
4. **WO2** — back-sync promotion to the repo. (One truth, not two.)
5. **WO7** — registry dedup + CI gate. (Clean data before building on it.)

### Phase 3 — Close the loop (next)
6. **WO4** — wire the decision seam (with the #1733 presence≠influence repair).
7. **WO5** — SELF behavior integration.
8. **WO6** — repair or retire the projection bridge.

### Phase 4 — Prove it (then)
9. Run the first closed loop (Part 8, system-level). One lesson, nine steps, independent verifier.
10. Only then: automate, scale, and score.

**Why this order:** each phase unblocks the next. You can't prove learning (Phase 4) before decisions read lessons (Phase 3). You can't trust decisions (Phase 3) before the data is clean and single-sourced (Phase 2). You can't do any of it while the pipeline is red (Phase 1).

---

## APPENDIX A — EVIDENCE LOG

Every [PROVEN] claim in this document traces to one of:
- Live main tip `1d73652231ac6127806640af5a31eb516c60738d` (verified via `git/refs/heads/main`)
- Branch `naya5/learning-admission-round2` @ `9fba596e8df01b3306c4bdacae6a17bc392e4593` (researcher ran its tests: 48/48 passed)
- PR #2020 merged as `075b169e4b92c21c72f888c93d48588c7cd8fc32`
- Workflow run `37980089547`, job log `113988278289` (`AssertionError: CANDIDATE` at `licp.yml:1090`)
- Live Supabase project `supabase-red-cable` (`dahisasgpfvziswqvmvm`, ACTIVE_HEALTHY): `smart_note_events`, `smart_note_artifacts` (92/23), `smart_note_receipts`, `v7_smart_note_transactions`, `learning_evidence`, `nayanet_github_dispatch_receipts` (5 rows, all failed), `nayanet_intelligent_blocks` (181 rows, all DURABLE), `nayanet_intelligence_index` (418 rows)
- Files read in full or in verified part: `BRAIN/03-KERNEL/NODES/*/0001-CONTRACT.md` (all 9), `0004-NINE-NODE-ORGANISM-CONTRACT-V1.md`, `BRAIN/03-KERNEL/MANIFEST.json`, `kernel/self_node.py` (235 lines), `kernel/act_pipeline.py`, `kernel/nayapower_kernel.py` (admission comment), `.github/workflows/live-intelligence-commit-proof.yml` (1,307 lines), `.github/workflows/live-supabase-runtime-proof.yml`, `supabase/functions/v7-smart-note-canonical/index.ts` (608 lines), `supabase/functions/nayanet-learning-verify/index.ts` (promotion ~535–546, candidate write ~378), `supabase/functions/naya-decision-context/index.ts` (2,814 bytes), `supabase/functions/nayanet-act-runtime/act.ts` + `index.ts`, `tools/smart_note_v2.py` (PROMOTION WRITER ~721), `tools/sn002_conformance.py:140`, `tools/smart_link.py`, `.naya/capture/README.md`, `.naya/memory/smart-notes/index.json` (`next_sequence` 783, 629 entries / 610 distinct IDs)

## APPENDIX B — GLOSSARY

- **Smart Note:** a distilled lesson in three voices (human, Naya, machine) with provenance. A filing-cabinet entry until proven otherwise.
- **Smart Link:** a URL pointing at a Smart Note's file on main. Proves the note exists. Proves nothing about truth or learning.
- **Receipt:** a record carrying SHA-256 hashes binding a claim to exact bytes. Three layers: DB receipt (four-artifact completeness), completion receipt (API response), registry entry (the working receipt).
- **CANDIDATE:** a lesson that exists but is unverified. The default label. Not usable for decisions.
- **ACTIVE / LEARNED / VERIFIED:** promotion states. ACTIVE (learning_evidence) / LEARNED (block understanding_state) / VERIFIED (relationship epistemic_state) mean independent verification passed.
- **Cold retrieval:** a fresh identity — one that never saw the lesson — fetching and correctly applying it. The test that proves availability.
- **Held-out behavioral test:** proving the lesson changes a decision on a task different from the one that produced it. The test that proves influence.
- **Presence ≠ influence:** a lesson existing in memory does not prove it changed behavior. The doctrine that keeps us honest (SN-0544).
- **The nine nodes:** SELF (identity), KNOW (memory), ACT (doing), VERIFY (checking), PROVE (showing work), CONNECT (finding related things), LAW (permission), LEARN (improving), EVOLVE (succession).
- **Back-sync:** writing a runtime state change (e.g. promotion) back to the repo so both truth systems agree.
- **Admission gate:** a creation-time check that rejects unverifiable candidates before they enter the system.

## APPENDIX C — WHAT WE COULD NOT VERIFY

1. Whether the Python/TS test suites currently pass on tip (not executed — would require a full battery run).
2. Whether the `live-*-proof.yml` workflows have recently passed beyond the #2020 run (Actions run history not fully checked).
3. Whether deployed Supabase edge functions match main bytes (source read on main; deployed state not checked).
4. Behavior inside the TS runtime files beyond existence, size, and the specific lines read.
5. Exact rows in `nayanet_cognition_events` for receiver checkpoints (not sampled).
6. The `naya-decision-context` function's deployed behavior (source read; not invoked).
7. Whether PR #1733's repair is actually green (open PR, not on main — its claim is REPORTED, not PROVEN).

---

*End of Blueprint v1. Status: DRAFT pending leader review. Every claim carries its evidence tag. What isn't proven isn't claimed.*
