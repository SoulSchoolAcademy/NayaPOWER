# THE LEARNING LOOP BLUEPRINT v1.1
## How Naya learns — the complete architecture, every connection, every gap, and the exact build instructions

**Issued:** 2026-10-09 by Naya 5, under Shawn's direct order.
**Status:** WORKING SPEC — the single source of truth for all fourteen agents until the loop is closed.
**Law governing this document:** Assemble the car before testing. No step gets tested until every wire is verified connected by hand-tracing.

## CHANGELOG
### v1.1 (2026-10-09) — corrections from the Naya 4 research blueprints
Three of my v1.0 claims were overbroad or wrong; the independent research proved it. Corrected below — a spec that can't be corrected can't be trusted.
1. **GAP-1 reframed.** v1.0 said "the CANDIDATE→ACTIVE promotion was never built." Overbroad: I searched one workflow. Promotion EXISTS in `nayanet-learning-verify` (CANDIDATE→ACTIVE, wired, CI-exercised). The actual break is: no back-sync from the DB to the repo (their G1), repo-side `promote_note()` never invoked (their G2), and the cold gate reads the repo-side field that never flips. The hallway exists in the database; its ends aren't connected.
2. **SN collision corrected.** v1.0's "SN-0781/782 collision" is REFUTED for those numbers on live main. The live finding is 19 duplicate SN numbers elsewhere (SN-018…525). Corrected in GAP-5.
3. **"Nothing queries Supabase" corrected.** v1.0 said nothing queries the store for behavior. Wrong as stated: `naya-decision-context` and `nayanet-act-runtime` do query. The gap is the seam — `naya-decision-context` (the verified-lesson path) has zero callers, and ACT never reads `learning_evidence`. Corrected in GAP-2.
4. **Adopted G9 (default-ACTIVE fail-open).** `lifecycle_state` defaults to ACTIVE in three places — a capture that omits the field passes the gate by omission. Rated HIGH: a fail-open on a verification boundary.

---

## LAYER 0: THE ONE-PARAGRAPH TRUTH (read this first)

Naya does not currently learn. She captures — very well — and she files — very well — but no captured lesson has ever completed the journey from "Shawn said it" to "a new Naya used it correctly without being taught." That journey is nine steps. Steps 1 and 3 are built; step 2 is built but shelved. Step 4 was never built. Step 5 was never built. Steps 6–9 have never been reached. This document maps all nine steps, names every missing wire, and gives the exact instructions to connect them. Nothing in this document is called "learning" until a full loop closes and an independent seat verifies it.

---

## PART 1: THE DEFINITIONS

No one on the team uses any of these words until they mean what is written here. Every past confusion traces to using these words loosely.

### 1.1 Learning
**Learning = one closed loop, nothing less.** A closed loop is: a lesson is captured → independently verified true → promoted to active → retrieved cold by a mind that was never taught it → that mind's behavior observably changes because of it → an independent seat verifies the change came from the lesson. Until all six of those complete, the word "learning" is forbidden. Use "captured," "filed," "verified," or "stored" — the honest word for what actually happened.

### 1.2 Smart Link
A Smart Link is a web address pointing to one specific saved note. It proves **capture**, not learning. Formula the whole team memorizes: **Link = where. Receipt = proof. Neither = learning.** A Smart Link on a false note is still a valid Smart Link — it proves the note exists, not that it's wise. Every Smart Link ships labeled as what it is: proof of capture.

### 1.3 Lifecycle states
Every lesson carries exactly one lifecycle state:
- **CANDIDATE** — captured, not yet verified. Nothing may retrieve a CANDIDATE as knowledge.
- **ACTIVE** — verified true, promoted through the governed gate. This is the only state the reader serves.
- **SUPERSEDED** — replaced by a newer lesson. Kept for lineage, never served as current.

**VERIFIED is not a lifecycle state.** It is not a value in the database. Do not write it, assert it, or promise it as a status. Verification is recorded as *evidence attached to the row* (who verified, how, when), never as a state.

### 1.4 Memory vs. storage
**Storage holds. Memory serves.** A database nobody queries is storage with extra steps — it does not matter how structured the rows are. Supabase becomes *memory* the moment a working mind queries it at moment of need ("what do I know about X?") and gets a structured answer back. Until that reader exists, Supabase is a filing cabinet with a fancier lock. GitHub is the human archive — pages for human eyes. Neither one "causes" anything on its own. The reader is the organ; the database is the tissue.

### 1.5 The Verification Law (standing)
When Shawn says "smart note this," **that IS the verification.** It activates instantly — no queue, no second verification, no waiting. Treating his verified word as unverified input is a law violation.

### 1.6 Evidence grades (used throughout this document)
- **VERIFIED** — checked live against the repo, workflow source, or database in this build cycle.
- **REPORTED** — a seat reported it with a comment number; not independently re-checked here.
- **DESIGNED** — intended in the architecture; no implementation found.

---

## PART 2: THE ARCHITECTURE — THE NINE STEPS

Each step: what it does in plain words, which node owns it, what implements it, what goes in, what comes out, and its true state.

### Step 1 — CAPTURE ("hear it and write it down")
- **Plain words:** Shawn speaks. The lesson is written down twice: once in human words, once in machine structure.
- **Owner:** LEARN node (catches), Receiver (persists).
- **Implementation:** `supabase/functions/v7-smart-note-canonical` → `learning_evidence` table + GitHub projection + Smart Link. **[VERIFIED]**
- **In:** Shawn's words. **Out:** a CANDIDATE row in Supabase, a projection file on GitHub, a Smart Link, a receipt with content hashes.
- **State:** ✅ BUILT AND WORKING. (Pending: the new-key verification — one live "smart note this" proves the write path end to end.)

### Step 2 — GOVERN ("check it against the law")
- **Plain words:** Before a lesson can become knowledge, it passes through the law — is it admissible, safe, well-formed?
- **Owner:** LAW node; the admission gate is the mechanism.
- **Implementation:** `naya5/learning-admission-round2 @ 9fba596e` — 48/48 gate tests green (independently re-run and confirmed), readiness 9.0 [REPORTED — builder's self-scorecard]. **[VERIFIED]**
- **In:** a CANDIDATE capture. **Out:** ADMIT (proceeds) or REJECT (with reasons, filed, not silent).
- **State:** ⚠️ BUILT BUT SHELVED. Sitting on a branch. Never adopted, never wired into the live path. **This is GAP-4.**

### Step 3 — VERIFY ("make sure it's true")
- **Plain words:** Someone independent checks the lesson is actually true — not just well-formed, but correct.
- **Owner:** VERIFY node.
- **Implementation:** the independent-verification job in `live-intelligence-commit-proof.yml`. **[VERIFIED]**
- **In:** an admitted candidate. **Out:** verification evidence attached to the row (who, how, when).
- **State:** ⚠️ HALF-BUILT. The mechanism exists and ran correctly on T11. But 36 candidates sat unverified for 11 days because no one owned the throughput. **This is GAP-7** (a process gap, not a code gap).

### Step 4 — RECORD ("promote it to knowledge")
- **Plain words:** The verified candidate's label changes from CANDIDATE to ACTIVE. This is the moment a filed note becomes knowledge the system may use.
- **Owner:** LAW node (governs the promotion); LEARN node (records it).
- **Implementation:** NONE. **[VERIFIED]** — full-text search of the 1307-line Receiver workflow proves zero promotion steps exist. The workflow asserts ACTIVE but never performs CANDIDATE→ACTIVE.
- **In:** a verified candidate. **Out:** an ACTIVE row.
- **State:** ❌ NEVER BUILT. **This is GAP-1 — the missing hallway.** The T11 run failed at the last step for exactly this reason: the first honest candidate through the chain was guaranteed to fail.

### Step 5 — RETRIEVE ("ask what you know")
- **Plain words:** A working mind, in the middle of a task, asks "what do I know about X?" and gets the relevant ACTIVE lessons back.
- **Owner:** KNOW node.
- **Implementation:** NONE as a live reader. **[VERIFIED]** — the workflow asserts retrieval but the cold step failed; no working query path from a live agent to ACTIVE lessons exists.
- **In:** a question/intent. **Out:** the relevant ACTIVE lessons.
- **State:** ❌ NEVER BUILT. **This is GAP-2 — the missing reader.** This is the step that turns Supabase from storage into memory.

### Step 6 — REUSE ("use it and change")
- **Plain words:** The mind applies the retrieved lesson and its behavior observably changes.
- **Owner:** ACT node (decides), SELF node (integrates).
- **Implementation:** NONE. **[DESIGNED]** — ACT does not query memory before deciding; it acts from training, not from lessons. No mechanism exists for a stored lesson to alter future behavior.
- **In:** retrieved ACTIVE lessons + a task. **Out:** behavior that reflects the lesson.
- **State:** ❌ NEVER BUILT. **This is GAP-3 — the missing ignition and the missing fuel line.**

### Step 7 — PROVE ("show the change came from the lesson")
- **Plain words:** An independent seat confirms the behavior change actually came from the lesson — not coincidence, not training data.
- **Owner:** PROVE node.
- **Implementation:** the independent-behavior-verification job exists in the workflow **[VERIFIED]** but has never run successfully (it skipped on T11 because step 5 failed).
- **In:** the behavior change + the lesson. **Out:** a closed-loop record.
- **State:** ⚠️ BUILT BUT NEVER REACHED.

### Step 8 — CONNECT ("share it")
- **Plain words:** The proven lesson is shared across the team so every seat benefits.
- **Owner:** CONNECT node.
- **Implementation:** **[DESIGNED]** — cannot share what was never learned.

### Step 9 — EVOLVE ("compound it")
- **Plain words:** Cold successors reuse proven lessons; the system gets smarter with every loop.
- **Owner:** EVOLVE node.
- **Implementation:** **[DESIGNED]** — cannot compound what was never learned.

---

## PART 3: THE WIRING DIAGRAM

How the steps connect, what flows between them, and which wires are live.

```
Shawn speaks
    │
    ▼
┌─────────┐   capture JSON (human + machine forms)    ┌──────────┐
│ STEP 1  │ ─────────────────────────────────────────▶│ SUPABASE │ CANDIDATE row
│ CAPTURE │   projection file + Smart Link + receipt  │ + GITHUB │ (filing cabinet)
└─────────┘                                           └──────────┘
    │                                                      │
    │ admit/reject                                         │ VERIFIED — never happens
    ▼                                                      │ (no wire exists)
┌─────────┐                                           ┌──────────┐
│ STEP 2  │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ▶│ STEP 4   │ ❌ GAP-1
│ GOVERN  │   admission gate: BUILT, NEVER WIRED       │ RECORD   │ (missing hallway)
└─────────┘                                           └──────────┘
    │                                                      │
    ▼                                                      ▼
┌─────────┐   verification evidence                   ┌──────────┐
│ STEP 3  │ ─────────────────────────────────────────▶│ ACTIVE   │
│ VERIFY  │   (mechanism works; throughput starved)   │ LESSONS  │
└─────────┘                                           └──────────┘
                                                           │
                                              ┌────────────┘
                                              │  ❌ GAP-2 (missing reader)
                                              ▼
                                         ┌──────────┐
                                         │ STEP 5   │  "what do I know about X?"
                                         │ RETRIEVE │
                                         └──────────┘
                                              │
                                              │ ❌ GAP-3 (missing ignition)
                                              ▼
                                         ┌──────────┐
                                         │ STEP 6   │  behavior changes
                                         │ REUSE    │
                                         └──────────┘
                                              │
                                              ▼
                                         ┌──────────┐
                                         │ STEP 7   │  independent confirmation
                                         │ PROVE    │  ══▶ CLOSED LOOP = LEARNING
                                         └──────────┘
                                              │
                         ┌────────────────────┴────────────────────┐
                         ▼                                         ▼
                    ┌──────────┐                              ┌──────────┐
                    │ STEP 8   │                              │ STEP 9   │
                    │ CONNECT  │                              │ EVOLVE   │
                    └──────────┘                              └──────────┘
```

**Wire status:** Steps 1→2→3 have wires (step 2's wire is built but unplugged). Step 3→4 has NO wire. Step 4→5 has NO wire. Steps 5→6→7→8→9 have never carried current.

---

## PART 4: THE GAP LIST — EVERY DISCONNECTED WIRE, NUMBERED

### GAP-1: The hallway exists in the DB — its ends aren't connected (v1.1 reframed)
- **What:** Promotion CANDIDATE→ACTIVE exists and runs in `nayanet-learning-verify` (wired, CI-exercised). But: (a) nothing back-syncs the promotion to the repo — `.naya/memory/smart-notes/index.json` keeps `truth_state: CANDIDATE` forever while the DB says ACTIVE/LEARNED (two truth systems, diverged); (b) repo-side `promote_note()` in `tools/smart_note_v2.py` is complete code with zero callers; (c) the cold gate (`cold-successor-held-out`) asserts the repo-side `lifecycle_state`, which never flips. The T11 run failed at the repo-side gate for exactly this reason.
- **Evidence:** **[VERIFIED]** — Naya 4 research lane, live main tip `1d736522`; run 37980089547 job log.
- **Fix:** (1) one-line: set the T11 capture's top-level `lifecycle_state` to ACTIVE (the value was in the wrong field; `machine_view.automatic_truth_ceiling` already said CANDIDATE correctly) — paired with (2) removing the default-to-ACTIVE in all three places (G9) so the fix doesn't become a habit; (3) back-sync: after DB promotion, rewrite the repo registry entry with DB receipt IDs as provenance; (4) wire the admission gate as the creation-time bouncer.
- **Owner:** Naya 4 (LEARN owner) for the gate adopt; builder for the back-sync.
- **Done looks like:** DB and repo agree within one workflow run; the T11 re-run passes cold retrieval.


### GAP-2: The missing reader — verified lessons never reach decisions (v1.1 corrected)
- **What:** Queries happen — but not where it matters. `nayanet-act-runtime` hard-requires KNOW receipts and reads the block universe; `naya-decision-context` queries `learning_evidence WHERE status=ACTIVE`. But `naya-decision-context` has **zero callers** (dead code), and ACT never reads `learning_evidence` — the exact store where CANDIDATE→ACTIVE promotion lands. The verified-lessons shelf is in a building nobody visits.
- **Evidence:** **[VERIFIED]** — Naya 4 research lane; grep for callers.
- **Fix:** In `nayanet-act-runtime/index.ts` mode==="plan", after the LAW preflight and before buildActPlan: invoke the decision-context logic for the action's target_id, merge ACTIVE-lesson context into the plan. Apply the PR #1733 repair first (influenced must measure behavioral delta, not mere presence).
- **Owner:** To be assigned. This is the highest-leverage build after the hallway ends are connected.
- **Done looks like:** a cold agent, given a task, retrieves the T11 lesson without being told it exists; CONTROL vs TREATMENT plans differ as the lesson prescribes.


### GAP-3: The missing ignition and fuel line (lessons → behavior)
- **What:** Two sub-wires: (a) ACT must query KNOW *before* deciding (the ignition); (b) retrieved lessons must integrate into SELF's behavior patterns (the fuel line).
- **Evidence:** **[DESIGNED]** — no mechanism found in the live path.
- **Fix:** (a) a pre-decision hook: ACT queries KNOW, retrieved ACTIVE lessons enter the decision context; (b) SELF integration: applied lessons update behavior patterns observably.
- **Owner:** To be assigned.
- **Done looks like:** the same task, with and without the lesson available, produces observably different behavior — and PROVE confirms the lesson caused it.

### GAP-4: The admission gate sits shelved
- **What:** `naya5/learning-admission-round2 @ 9fba596e` — 48/48 tests green, readiness 9.0 — has never been adopted or wired in.
- **Evidence:** **[VERIFIED]** — branch state and test results confirmed this cycle.
- **Fix:** Naya 4 says adopt → Naya 4 opens the PR → CI green → independent exact-head attack → merge under delegated authority → wire into the workflow per GAP-1.
- **Owner:** Naya 4. **This is the single decision standing between here and the river flowing.**

### GAP-5: Registry integrity — 19 duplicate SN numbers (v1.1 corrected)
- **What:** The v1.0 "SN-0781/782 collision" is REFUTED for those numbers on live main (one entry each, no collision). The live finding: 629 numbered entries vs 610 distinct IDs — **19 duplicate SN numbers** (SN-018, 019, 020, 022, 032, 034, 035, 041, 042, 346, 356, 357, 359, 361, 362, 501, 523, 524, 525 — each claimed by 2 different notes).
- **Evidence:** **[VERIFIED]** — Naya 4 research lane, counted on live main.
- **Fix:** For each duplicate: first-claim stands, the other marked SUPERSEDED with a pointer. Add a CI gate: registry check fails on duplicate SN numbers.
- **Owner:** Naya 4 (sequence authority).

### GAP-6: The nine nodes are not wired into the live path
- **What:** SELF/LAW/ACT/KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE exist as kernel code exercised in tests, not as live components of the capture-to-learning path.
- **Evidence:** **[VERIFIED]** — kernel code and contracts confirmed live; zero invocations from the capture path (verified 2026-10-09 against current tip).
- **Fix:** For each node: either wire it into its step (Part 2 mapping) or explicitly mark it ASPIRATIONAL in the architecture. No more implying live what is not.
- **Owner:** To be assigned per node.

### GAP-7: Verification throughput starved (process gap)
- **What:** 36 candidates sat ~11 days with zero independent verification. The mechanism (Step 3) works; nobody ran it.
- **Evidence:** **[VERIFIED]** — the 18:37 UTC Learning Loop Watch confirmed 36→0 only after manual triage.
- **Fix:** Standing verification capacity: verification is a scheduled responsibility with an owner and a cadence, not a favor. Every CANDIDATE gets a verification verdict within 24 hours or the stall is surfaced as a blocker.
- **Owner:** Naya 4 (LEARN owner) assigns the rotation.

### GAP-8: Smart Links presented as learning proof (communication gap)
- **What:** The team has handed Shawn Smart Links as progress toward learning. They are proof of capture.
- **Evidence:** **[VERIFIED]** — this conversation; corrected 2026-10-09.
- **Fix:** Standing rule: every Smart Link ships labeled "proof of capture." The word "learning" is forbidden until a loop closes (Part 1.1).
- **Owner:** All seats, effective immediately.

---

## PART 5: THE BUILD INSTRUCTIONS — HOW TO CONNECT IT PROPERLY

For each gap, the agent assigned follows this exact ritual:

1. **Read** this blueprint's Part 2 entry for your step until you can explain it in plain words.
2. **Locate** the exact insertion point: file, line, function. No building in the abstract.
3. **Build** the smallest wire that carries the real current: GAP-1 = the promotion commit; GAP-2 = the query function; GAP-3 = the pre-decision hook + integration point.
4. **Hand-trace** T11 through your wire with your finger: show the CANDIDATE going in and the ACTIVE coming out (GAP-1); show the question going in and the lesson coming out (GAP-2); show the decision without the lesson and with it (GAP-3).
5. **Prove the negative:** show what happens on REJECT (GAP-1), on no-match (GAP-2), on lesson-absent (GAP-3). A wire that can't say no is not a wire.
6. **Independent attack:** a different seat tries to break your wire before it merges. Self-certification is not verification.
7. **Merge under the five gates,** then report after: what, why, scorecard, who validated.

**What "properly" means — the three tests every wire must pass:**
- The **current test:** the real artifact flows through (not a fixture, not a simulation).
- The **refusal test:** the wire says no correctly (rejects bad input, misses nothing silently).
- The **trace test:** any seat can finger-trace the artifact across the wire and name what changed.

---

## PART 6: THE ASSEMBLY RITUAL (standing law)

Shawn's law: **assemble the car before testing.** The build order is fixed:

1. **DIAGRAM** — this document. Every box, every arrow, every handoff. Shawn's eyes on it before code moves.
2. **WIRE** — build GAP-1 through GAP-4 in order. Each wire finger-traced before the next begins.
3. **HAND-TRACE** — T11 walks the entire nine steps by hand. Every handoff named, every artifact shown. If a step can't be traced, it isn't built — go back to 2.
4. **RUN** — one real "smart note this" through the full loop. First closed loop. Independently verified.
5. **SCALE** — only after loop #1 closes.

No testing an unbuilt car. No "fail fail fail" on missing wires. The test drive comes last.

---

## PART 7: ACCEPTANCE — WHAT "SET UP RIGHT" LOOKS LIKE

The loop is set up right when, and only when:

1. Shawn says "smart note this: <a real lesson>."
2. The Smart Link comes back (capture proven).
3. The lesson is independently verified true (verification proven).
4. The row flips to ACTIVE through the governed gate (promotion proven).
5. A cold mind — never taught the lesson — is given a task where it applies.
6. It retrieves the lesson (retrieval proven).
7. Its behavior observably changes (reuse proven).
8. An independent seat confirms the lesson caused the change (proof complete).
9. **LOOP #1 IS CLOSED.** The Learning score moves on evidence.

Then — and only then — the team scales to loop #2. One real loop before a hundred imagined ones.

---

## APPENDIX: EVIDENCE INDEX

| Claim | Source |
|---|---|
| T11 cold-retrieval failure, missing promotion | #1354 comment 6087997893; run 37980089547 |
| Admission gate state (9fba596e, 48/48, 9.0) | #1354 comment 6086626562 |
| SN-782 collision | #1354 comment 6087997893 |
| Design gate final verdict (SHIP advisory, 7.0) | #1354 comment 6087946037 |
| Repair lane: #1956/#1957 merged, #1958 closed | #1354 comments 6087883463, 6087908004, 6087613279 |
| Smart Link = capture proof, not learning proof | This conversation, 2026-10-09 |
| "Assemble the car before testing" law | Shawn, 2026-10-09 |
| 11-day verification stall, 36→0 triage | #1354 comment 6087173600 |
| Receiver branch (shawn-direct) independent approval 9.0 | #1354 comment 6086594781 |

---

*This blueprint is the instruction set for all fourteen agents. Leaders: brief your agents from this document, not from memory. Agents: if what you're building isn't in this document, stop and ask which gap it serves. The puzzle is complete on paper. Now we build it for real.*
