# ENGINE CHECKLIST — everything that must be done before Naya goes live

**Shawn's order (2026-10-09):** a checklist of everything that needs to be done, where everybody can see it, one per department. Work it top to bottom. **Nothing in Production Readiness starts until every engine item above it is done.** No engine, no race.

**How to read an item:** `[ ]` = open, `[x]` = done. Every item says what "done" looks like — the proof, not the promise. `[ENGINE]` = build it now. `[PRODUCTION-GATED]` = needs going live and/or Shawn's explicit word.

**Source:** `BRAIN/00-ACTIVATION/naya-activation-spec-v2.json` (reconciled, DRAFT_FOR_CONSENSUS). Work-order IDs (WO0–WO10, SEED, PROOF) and gap IDs (G1–G13) refer to it.

---

## Department 1 — Nine Nodes Wiring (the engine itself)

The engine: SELF → LAW → ACT → KNOW → VERIFY → PROVE → CONNECT → LEARN → EVOLVE. Nine nodes, one cycle. Work in section order. Parallel-safe builds: WO1, WO8-build, WO9, WO3-build, WO7, WO6.

### DONE
- [x] One machine spec: v1 + team's file reconciled into `naya-activation-spec-v2.json` (76KB, lossless, 20-entry reconciliation log) — placed on branch `naya5/activation-docs`. **Done looks like:** file on the branch, valid JSON. Status stays DRAFT_FOR_CONSENSUS until the team rules on the conflicts below. [ENGINE] (v2)
- [x] Her identity: `naya-identity.md` — who she is, her 8 laws, her protocol. Status CANONICAL. **Done looks like:** on the branch, read by SELF at boot. [ENGINE]
- [x] The activation ritual: `activation-ritual.md` with Step 5 THINK LIKE HIM — every seat loads it at boot. **Done looks like:** on the branch, referenced by all worker briefs. [ENGINE]
- [x] Learning blueprint v1.1 (three blueprint corrections incorporated). **Done looks like:** on the branch. [ENGINE]

### PRE-FLIGHT (WO0)
- [ ] Measure twice: deployed edge-function bytes match main bytes (4 functions), battery green on the tip, PR #1733 route decided (merge or port), admission-gate route decided (TS port vs workflow job), every lane owner named. **Done looks like:** parity report with 4 matching hashes (or named gap + owner), battery run ID, #1733 owner + route posted, lane owners posted. [ENGINE] (WO0 · Q1 Q2 Q3 Q4)

### IGNITION
- [ ] Fix the red capture: one-line lifecycle fix so the failed run goes green (branch `naya5/wo1-t11-lifecycle-active` built — needs Naya 4's PR + merge + green proof run after). **Done looks like:** fresh run completes with no AssertionError, run ID recorded. [ENGINE] (WO1 · G11 — paired with WO8, never alone)
- [ ] Close the fail-open: remove default-to-ACTIVE in all 3 places so a missing field FAILS the gate instead of slipping through. **Done looks like:** a capture omitting lifecycle_state, sent through the real path, fails with the named missing-field error. [ENGINE] (WO8 · G9 — paired with WO1, never alone)
- [ ] One door in: declare ONE canonical intake and ONE writer to the learning store; retire the old receiver path. **Done looks like:** zero new rows from the retired path over the soak period, no code references to the dead path. [ENGINE] (WO9 · CONN-INTAKE)

### GATE
- [ ] Wire the admission gate: unverifiable claims get rejected with a reason code, verifiable ones pass, and the gate fails closed (never open) when it errors. **Done looks like:** pre-registered bad candidate rejected in the workflow log with the gate's reason code; forced error → closed, not open. [ENGINE] (WO3 · G3 · CONN-ADMISSION)
- [ ] Grow the seed: run ONE real falsifiable lesson through the gated pipeline all the way to ACTIVE — this row becomes the shared test fixture. **Done looks like:** one ACTIVE row produced by the real pipeline (capture → gate → experiment → promotion). Hand-inserted rows don't count. [ENGINE] (SEED)

### TRUTH
- [ ] Clean the registry: fix the 19 duplicate lesson numbers — first claim stands, others marked superseded, ZERO deletions — and add the CI gate that fails on any future duplicate. **Done looks like:** duplicate count = 0 AND deleted count = 0, CI fails a test duplicate with the named error. [ENGINE] (WO7 · G10)
- [ ] Back-sync the truth: after the database promotes a lesson, the repo registry must say the same thing (today the DB says ACTIVE while the repo says CANDIDATE forever). **Done looks like:** a test capture promoted through the real pipeline shows repo truth == DB truth in the same run, with receipt IDs as provenance. [ENGINE] (WO2 · G1 G2 · CONN-BACKSYNC)

### CONNECTION
- [ ] Prove the kernel can read the database: one real row read end-to-end, or a documented architecture decision with a named credential owner. **Done looks like:** read path proven, or the decision doc posted. Don't start the two items below until this exists. [ENGINE] (WO5a · Q5)
- [ ] Plug lessons into decisions: the decision engine must actually call the verified-lesson store (today that code has zero callers) and the lesson must CHANGE the plan, not just sit next to it. **Done looks like:** byte-identical inputs with and without the lesson produce plans that differ in the lesson-prescribed dimension. Needs #1733 resolved first. [ENGINE] (WO4 · G4 G5 G13 · CONN-DECISION · Q3)
- [ ] Bridge the two runtimes: the TypeScript edge functions and the Python kernel need one shared behavior store they both read — or a documented decision that one runtime owns the loop and the other's role is retired. **Done looks like:** one closed-loop run observably involving both, or the architecture doc posted. [ENGINE] (WO10 · CONN-RUNTIME-BRIDGE · Q6)
- [ ] Teach the SELF node: verified lessons change her behavior through a versioned policy (situation → prescribed behavior) with rollback. **Done looks like:** in a previously-seen situation, her decision transcript matches the pre-registered prescription as scored BLIND by a different seat. [ENGINE] (WO5b · G6 · CONN-SELF)

### CLEANUP
- [ ] Fix or retire the projection bridge: the receiver-to-GitHub bridge failed all 5 times. Either get 3+ captures projecting end-to-end with resolving Smart Links, or formally retire it in exactly one canonical doc — no middle state. **Done looks like:** bridge declared LIVE or RETIRED in one doc. [ENGINE] (WO6 · G7 · CONN-PROJECTION)

### PROOF
- [ ] Close the loop for real: pre-registered held-out task, ranked retrieval (not a hash lookup), fresh cold identity, blind different-seat verifier, full hash-chained receipt chain — plus Shawn's teach-once/observe-later moment. **Done looks like:** DONE-MACHINE and DONE-HUMAN both met, protocol hash recorded. Depends on everything above. [ENGINE] (PROOF · activation criteria 1–8)
- [ ] Prove the nine are one: today there is no single production entrypoint binding all nine nodes (system's own admission: NOT_PROVEN). Either wire it or formally mark which nodes are aspirational. **Done looks like:** binding proven end-to-end, or the aspirational list posted. [ENGINE] (G12)

### SPEC HYGIENE
- [ ] Rule on the conflicts: LAW verdict vocabulary (check what the runtimes actually emit), lifecycle vocabulary (is VERIFIED a state or evidence?), and the Q8 authorization dispute (resolve against the transcript). Then v2 leaves DRAFT_FOR_CONSENSUS. **Done looks like:** team rulings posted, v2 marked canonical. [ENGINE] (C1 C2 Q8)
- [ ] Merge the branch: `naya5/activation-docs` PR opened (Naya 4), green CI, exact-head validation, no objections, merged. **Done looks like:** all six files resolve on main. [ENGINE]
- [ ] Converge the two pipeline decompositions (11 steps vs 9 links) into one in v3 — deferred by design, not dropped. **Done looks like:** v3 posted with one pipeline. [ENGINE] (C4)

---

## Department 2 — Learning

- [x] She learns: 14/14 blind-scored, receipts in the database. **Done looks like:** the scoreboard + DB receipts. [ENGINE]
- [x] The 45-lesson curriculum: 45 lessons distilled, ordered foundational-first, novel-application test per lesson, 9 batches. **Done looks like:** `BRAIN/07-LEARNING/learning-curriculum-45/` on the branch. Status: BUILT, NOT RUN. [ENGINE]
- [ ] Run the battery: 9 batches, fresh cold agent per batch, different-seat blind scorer, max score 90. **Done looks like:** per-lesson report card — which teachings transferred, which didn't. [ENGINE]
- [ ] Prove it under load: she applies what she learned live, day after day — not just in a test. **Done looks like:** longitudinal record of lessons applied in real work. [ENGINE]
- [ ] Fix the lineage hole: the 5 most-verified lessons (ACTIVE E5) + 2 E1 rows carry zero lineage links — the most trusted lessons can't show how they were learned. **Done looks like:** 143/143 rows carry full reconstructable lineage. [ENGINE]
- [ ] Lane to 10/10 (currently 5.0 authoritative — Naya 1's score, never re-derived). [ENGINE]

---

## Department 3 — Truth

- [ ] Merge the truth guard: #1938 fully green (6/6 CI) — needs independent seat validation + merge. **Done looks like:** merged to main, validation posted. [ENGINE]
- [ ] Keep the hygiene: no bare-True verification literals, UNKNOWN never treated as verified, on every tip. **Done looks like:** truth-hygiene audit CLEAN on the tip. [ENGINE]
- [ ] Lane to 10/10 (currently 9.0 claim holding). [ENGINE]

---

## Department 4 — Memory & Continuity

- [ ] Land WO1: PR opened (Naya 4), merged, then the green proof run after merge. **Done looks like:** licp run green on main, run ID recorded. [ENGINE] (WO1)
- [ ] Unblock the memory-metabolism merge: needs a seat's validation since 16:00. **Done looks like:** validated + merged. [ENGINE]
- [ ] Lane to 10/10 (currently 8.0 claim / 7.0 authoritative). [ENGINE]

---

## Department 5 — Cold Retrieval

- [ ] Ship ranked retrieval: the ranked-retrieval RPC must exist where PROOF needs it (needs a DB migration — the migration itself needs Shawn's word, the build doesn't). **Done looks like:** migration run, ranked retrieval proven on a cold query. [ENGINE] (G8)
- [ ] Merge the retrieve audit branch (`naya5/cold-retrieve-audit`): 28/28 lane tests, CI green. **Done looks like:** merged to main. [ENGINE]
- [ ] Lane to 10/10 (currently 8.0 claim). [ENGINE]

---

## Department 6 — Action & Execution

- [ ] Merge the ACT proof: PR #1860 rebased, full suite green (1946 passed), ACT battery 63/63 — needs independent validation + merge. **Done looks like:** merged to main. [ENGINE]
- [ ] Lane to 10/10 (currently 8.9 claim held). [ENGINE]

---

## Department 7 — Safety

- [ ] Merge the 5 open safety branches (#1944, #1915 + 3) — including the ACT re-gate risk-policy fix (9/9 falsifier tests green, full suite 1940 passed). **Done looks like:** all 5 merged, validation posted. [ENGINE]
- [ ] Lane to 10/10 (currently 9.0 claim). [ENGINE]

---

## Department 8 — Authority & Governance

- [ ] Land the authority repair: PR #1943 repair3 (9.5/10 after three attack rounds, 23 tests green) — PR opened, CI green, then Shawn's decision (authority changes are his). **Done looks like:** his explicit word + merge. [ENGINE]
- [ ] Settle Q8: resolve the #2020 merge-authorization dispute against the cited transcript before anyone uses it as precedent. **Done looks like:** ruling posted, precedent usable or retired. [ENGINE] (Q8)
- [ ] Lane to 10/10. [ENGINE]

---

## Department 9 — Voice & Experience

- [ ] Merge the experience work: PR #1940 re-anchored, needs Naya 4's validation + merge. **Done looks like:** merged to main. [ENGINE]
- [ ] Lane to 10/10 (currently 8.9 claim). [ENGINE]

---

## Department 10 — Human Value

- [ ] Get the independent check: human-value ledger needs a different seat to cold-recompute and post a verdict (7 prediction→observation loops closed, zero overprediction — strong, but unverified alone). **Done looks like:** independent verdict posted. [ENGINE]
- [ ] Lane to 10/10 (currently 7.5 claim). [ENGINE]

---

## Department 11 — Production Readiness ⛔ GATED — nothing here starts until every engine item above is done

- [ ] Gate check: all 10 departments above read DONE. **Done looks like:** this checklist fully checked. [PRODUCTION-GATED]
- [ ] Guard the launch pad: branch protection on the production ref (today: unguarded). **Done looks like:** protection enabled; Shawn's word (security/authority change). [PRODUCTION-GATED]
- [ ] Authorize the deploy: production is ~1.5 days stale when this was written. **Done looks like:** Shawn's explicit deploy authorization + green deploy. [PRODUCTION-GATED]
- [ ] Prove the Smart Link live: one real "smart note this" → persisted capture + successful projection + resolving link (the credential fix is unproven until this happens). **Done looks like:** the live receipt chain, observed once. [PRODUCTION-GATED]
- [ ] Document the deployment path: merged code → live Receiver (Q7 — today: not automatic, not documented). **Done looks like:** the path doc posted. [PRODUCTION-GATED]
- [ ] Prove it live over time: she learns under production load, longitudinally — graduation. **Done looks like:** weeks of live learning receipts. [PRODUCTION-GATED]

---

*Root law: make intelligence compound; remove whatever stops it from compounding. The checklist is the instrument — work it top to bottom.*
