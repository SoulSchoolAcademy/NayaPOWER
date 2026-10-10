# ACTIVATION NAYA — CONSENSUS EXECUTION PLAN v1

> **RECONCILED 2026-10-09** — This is the ONE canonical activation plan.
> Reconciles PR #2052 (`.naya/project-intelligence/activation-naya-plan-v1.md`, Naya 2 lane)
> into its canonical home. Content is the team consensus record, preserved intact;
> only file references were updated to canonical paths. The duplicate at
> `.naya/project-intelligence/` has been removed.
>
> Companion documents (all canonical):
> - Charter (mission, success criteria): `BRAIN/00-ARCHITECTURE/ACTIVATION-NAYA-PROJECT.md`
> - Machine core: `BRAIN/00-ARCHITECTURE/MACHINE-INTELLIGENCE.json`
> - System blueprint: `BRAIN/00-ARCHITECTURE/SYSTEM-BLUEPRINT-20261009.md`
> - Project intelligence: `BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/ACTIVATION-NAYA-INTELLIGENCE.md`

---
**Status:** CONSENSUS v1 — team-reviewed, scorecarded, holes addressed. Ready for leader assignment.
**Authority:** Shawn Vibert, Human Director
**Facilitated by:** Naya 2 (consensus process) · Reviewed by: learning-lane owner, verification lead, independent judge, systems integrator
**Source of truth for current state:** `BRAIN/07-LEARNING/learning-system-blueprint-v1.md` (all claims [PROVEN]/[REPORTED]/[UNVERIFIED] there)
**Goal:** Naya fully activated — remembering, growing, learning. Smart note in → she understands → she learns → behavior changes. Non-stop until done.

---

## PART 1 — WHAT "ACTIVATED" MEANS (acceptance criteria for done)

ACTIVATION is complete when ALL of the following hold:

1. **The first closed loop is proven** (machine side): one novel falsifiable lesson flows capture → persist → index → verify → promote (DB + repo in sync) → cold Naya retrieves via the **ranked** path and applies it to a pre-registered held-out task → a blind different-seat verifier confirms the behavior change came from the lesson (task prompt published to rule out leakage) → every link carries SHA-256 hashes. Exact content-hash lookup does not count as retrieval. One green run is not the proof — the repeatable protocol is; the protocol hash is recorded with the receipt.
2. **The human side is proven** (experience side): Shawn teaches Naya something once ("smart note this", gets a Smart Link). Days later, in a different conversation, he asks for something in that lesson's territory — and she does it the way the lesson prescribes **without being reminded**. He asks "why did you do it that way?" She answers in plain words, names the lesson, and shows the receipt chain. The Smart Link resolves to a note whose header says ACTIVE (not CANDIDATE). The accomplishment posts to his Feed with evidence.
3. **No dead machinery:** every gate has a producer for the state it demands; no two writers own the same table/file without a named precedence; no "looks alive, isn't" components remain.
4. **One intake, one truth:** a single canonical capture intake; DB and repo agree on lesson state; zero duplicate SN numbers with a CI gate enforcing it.

Per the standing quality law: the rendered experience is the only score that matters. A PROOF that completes entirely in CI logs is unproven on experience.

---

## PART 2 — THE SECTIONS (in execution order)

### SECTION 0 — PRE-FLIGHT (new: WO0) — *measure twice, cut once*
**Achieves:** no section starts on an unsettled premise.
- Verify deployed Supabase edge-function bytes == main bytes for `nayanet-learning-verify`, `nayanet-act-runtime`, `naya-decision-context`, `nayanet-intelligence-commit-runtime`. **If a gap is found, closing it is a production deploy — a human gate (Shawn's click).**
- Run the full test battery on tip (Scorecard Law merges require "tests green on live-verified bytes" — currently unclaimable).
- Review `live-supabase-runtime-proof.yml` recent run history (establish green baseline before its runs are used as evidence).
- Confirm PR #1733 state; name its owner; decide merge-vs-port (porting unreviewed PR code into the critical seam is not accepted — re-implement and test independently if #1733 is red/abandoned).
- **Decide WO3's route now:** TS port at the `mode==="candidate"` write site (enforced gate — the target) vs Python workflow job (advisory stopgap, explicitly labeled). TS port is the target; the workflow job is only a labeled stopgap.
- Name the `workflow_dispatch` owner for WO1 (agents cannot dispatch workflows — 403; this is human-gate-adjacent).
- Name lane owners for every section below.
**Done when:** parity report (4 functions, hashes match or gap named with human-gate owner); battery green on tip with run ID; #1733 owner named and route decided; WO3 route decided; all lane owners named.
**Proposed owner:** verification lane (Naya 5) + parent orchestrator for human-gate items.

### SECTION 1 — IGNITION — *stop the bleeding, declare the road*
**Achieves:** pipeline green; no pass-by-omission; one canonical intake declared.
- **WO1** — one-line #2020 fix (`lifecycle_state` CANDIDATE→ACTIVE in the capture JSON; do NOT touch `machine_view.automatic_truth_ceiling`). Merge under Scorecard Law. Named owner performs `workflow_dispatch` at the post-fix main SHA. **Done when:** a fresh dispatch at the receipt-named SHA completes `cold-successor-held-out` green with no `AssertionError`; run ID recorded. (Note: this is hygiene on a live red, not "unblocking the pipeline" — other captures fire their own runs.)
- **WO8** — remove default-to-ACTIVE in all three places (`sn002_conformance.py:135`, `smart_note_v2.py:573`, workflow inline). A missing field must FAIL the gate. **Done when:** a capture omitting `lifecycle_state`, submitted through the real path, fails with the named missing-field error — any other RED does not count. (WO1 before WO8: green baseline first, so the new gate's RED is distinguishable from the old bug's RED.)
- **WO9 (new)** — unify the intake pipelines. Declare ONE canonical capture intake (v2 agent pipeline: capture → `nayanet-intelligence-commit-runtime` → `nayanet-learning-verify`). Decommission the v7 receiver's write path: no new `smart_note_events`/`smart_note_artifacts`/`learning_evidence` inserts (existing rows read-only, migration note); remove the 15-minute authority-grant scope referencing nonexistent `project-canonical-smart-note.yml`; establish ONE writer to `learning_evidence` with a dedup key spanning both former paths. **Done when:** single writer owns `learning_evidence`; zero new rows from the retired path over a soak period; repo-wide grep returns zero references to the dead workflow/scope; retirement documented.
**Dependencies:** none. **Proposed owner:** learning lane (Naya 4) for WO1/WO9; any seat for WO8.

### SECTION 2 — GATE — *bouncer at the front door*
**Achieves:** unverifiable candidates rejected at creation with named reasons; the first ACTIVE lesson exists as a shared test fixture.
- **WO3** — wire the admission gate per the WO0 route decision. If TS port: splice at `mode==="candidate"` (~line 378) after a full read of the splice-site file. **Done when:** two pre-registered, schema-valid candidates — one well-formed but unverifiable (no falsifiable claim, no pre-registered criterion) is rejected with the gate's reason code from its own taxonomy in the workflow log; one verifiable candidate passes; PLUS a fail-closed probe (gate forced to error → candidate rejected, not passed through); the gate logs its invocation (input hash → reason code) — a rejection with no gate-invocation log line fails the section.
- **Seed-lesson fixture (new):** run one real, falsifiable lesson through the gated pipeline to ACTIVE. This row is the shared test fixture for CONNECTION. **Done when:** one ACTIVE row in `learning_evidence` produced by the real pipeline (capture → gate → causal experiment → promotion) — hand-inserted rows invalidate all downstream acceptance.
**Dependencies:** build in parallel with IGNITION; **acceptance waits for IGNITION-green** (the candidate path runs through `live-supabase-runtime-proof.yml`, fired by commit-proof). **Proposed owner:** learning lane (Naya 4).

### SECTION 3 — TRUTH — *one truth, not two; clean data*
**Achieves:** DB and repo agree; registry deduplicated; repo-side promotion is a single mechanism.
- **WO7** — dedup 19 duplicate SN numbers (first-claim stands per SN-033): non-canonical marked SUPERSEDED with pointer to canonical; **zero deletions** (distinct-ID count unchanged). Add CI gate failing on new duplicates with the named duplicate-detection error. **Done when:** duplicate count = 0 AND deleted count = 0; CI fails a test duplicate with the named error.
- **WO2** — back-sync promotion to the repo registry **routed through `promote_note()`** (making it the single repo-side promotion writer — thresholds enforced or explicitly waived with rationale; no second promotion writer). After runtime promotion confirms, update the registry entry's `truth_state` to match the DB's `understanding_state`, with DB receipt IDs as provenance; idempotent (re-run = byte-identical no-op). **Also update the projected `.md` header** so the Smart Link tells the truth (a link resolving to a note still declaring itself unratified fails the human proof). Serialize with the projection job: exactly one writer to `index.json` at a time, with a loop-guard on the back-sync commit. **The `contents: write` permission change is flagged in the PR body.** **Done when:** a test capture promoted through the real pipeline shows, within the same workflow run, registry `truth_state` == DB `understanding_state` with receipt IDs as provenance; re-run is a no-op; quiescence re-read after the next scheduled CI registry write still shows correct states.
- Precedence rule (new): `learning_evidence.status` vs block `understanding_state` vs relationship `epistemic_state` → registry `truth_state`: define which field wins on conflict, one page in `BRAIN/07-LEARNING/`, linked from both code sites.
**Dependencies:** none on GATE (CONNECTION never reads the registry — TRUTH serves human trust and PROOF's receipt chain, not the data path). Within TRUTH: WO7 before WO2 (don't back-sync onto entries about to be superseded). **Proposed owner:** any seat (janitorial, well-specified).

### SECTION 4 — CONNECTION — *lessons → decisions → behavior*
**Achieves:** verified lessons change decisions (TS runtime) and behavior (Python kernel), through one shared contract.
- **WO5a (new)** — scope and prove the kernel→Supabase read seam. Questions: does `kernel/` have a Supabase client? Which credential at runtime — and is provisioning it a human-gate action? **Done when:** the read path is proven end-to-end (one read of a real row) or the architecture decision is documented with a named credential owner. **This is the single biggest buildability risk in CONNECTION — do not start WO5b until WO5a exists.**
- **WO4** — wire `naya-decision-context` into `nayanet-act-runtime` plan handler (after LAW preflight, before `buildActPlan`); merge returned ACTIVE-lesson context into the plan's learning context with a named precedence rule vs the 181 DURABLE blocks from `readEligibleUniverse()` (prepend/override/conflict — specified, not assumed). **Hard precondition: #1733 merged green** (no unreviewed ports). Full read of `nayanet-act-runtime/index.ts` before splicing. **Done when:** the TREATMENT lesson reached ACTIVE through the real pipeline; CONTROL (byte-identical inputs except the lesson) vs TREATMENT plans differ **in the lesson-prescribed dimension per a pre-registered prescription**; an ablation (lesson present but INACTIVE) reproduces CONTROL; `influenced=true` fires only on observed delta.
- **WO10 (new)** — bridge the runtime split (G12). Give WO4/WO5 a shared behavior-policy store both runtimes read, or define which runtime executes the Part 8 closed loop and how the other runtime's integration is observable there. **Done when:** one closed-loop execution observably involves both runtimes' integrations, or the architecture declares a single runtime with the other's role formally retired. "Nine-node production binding" must no longer read NOT_PROVEN for the loop path.
- **WO5b** — SELF behavior integration: `integrate_verified_lesson()` in `kernel/self_node.py` + `kernel/behavior_policy.py` (versioned JSON store: situation → lesson-prescribed behavior; reversible); validates verifier chain (doer≠scorer≠verifier, reusing the admission gate's contract); wire the ACT pipeline's post-execution hook as the `record_experience()` caller (the blueprint's specific pick). **Done when:** a decision transcript in a previously-seen situation matches the pre-registered prescription as scored **blind by an independent verifier (different seat, lesson withheld)**; rollback (policy version revert) followed by a **cold** re-decision reproduces the pre-integration baseline.
- **Synthetic rehearsal (from Alt E):** before production arming, prove CONTROL vs TREATMENT discrimination with synthetic ACTIVE lessons in a staging copy of the tables — zero production exposure. **Explicit arming gate:** CONNECTION wires to production `learning_evidence` only after GATE live ∧ #1733 merged ∧ synthetic rehearsal green. Build and arm are separate decisions.
**Dependencies:** build can parallel GATE (against the gate's contract); **production arming hard-blocked on GATE live** (admission admits verifiable candidates; without it, receipt-validated-but-unverifiable lessons get laundered into behavior). WO4 before WO5b (WO5's verifier-chain validation reuses the admission contract; the contract must be frozen). **Proposed owner:** learning lane (Naya 4) + engine seat for the TS splice.

### SECTION 5 — CLEANUP — *no dead machinery*
**Achieves:** the projection bridge is green or formally retired.
- **WO6** — classify the 5 failed `nayanet_github_dispatch_receipts`. Either: N≥3 pre-declared consecutive canonical captures project end-to-end **through the normal receiver path** with Smart Links resolving to live main blobs; or: retirement record exists AND repo-wide grep returns zero references to `project-canonical-smart-note.yml` and the dispatch scope AND the receiver no longer issues projection authority grants (code read + one grant-issuance observation). **The bridge's status (LIVE or RETIRED) is declared in exactly one canonical doc — no middle state.** After TRUTH so a repaired bridge projects onto a clean registry.
**Dependencies:** none on the loop. **Proposed owner:** any seat.

### SECTION 6 — PROOF — *the first closed loop + the human moment*
**Achieves:** machine proof AND human proof that filing became learning.
- Machine: all Part 1 acceptance item 1 conditions (pre-registered held-out task from a pool committed before capture; ranked retrieval; fresh cold identity; blind different-seat verifier; published prompts; hash-chained receipts; repeatable protocol with recorded protocol hash).
- Human: the teach-once/observe-later demonstration (Part 1 item 2) witnessed by Shawn or his explicit delegate; Smart Link resolves to an ACTIVE-headed note; Feed receipt posted with the evidence chain. **Whose verdict counts as "activated": Shawn's** (or his explicit delegate's) — per the visual-proof and human-proof standards.
**Dependencies:** IGNITION + GATE + TRUTH + CONNECTION. (TRUTH required: Part 8 demands "promotes (DB + repo in sync)" = WO2; the human proof demands the Smart Link tell the truth = WO2's header update.) G8 note: ranked retrieval depends on the `nayanet_retrieve_blocks` RPC whose migration is pending — **applying it is a human-gate action**; name it as a PROOF prerequisite, not a silent assumption.
**Proposed owner:** verification lane runs it; an independent seat verifies; Shawn closes it.

---

## PART 3 — DEPENDENCY MAP

```
WO0 (pre-flight)
 ├─► parity ──► human gate if gap (blocks WO3, WO4)
 ├─► battery on tip (blocks all Scorecard-Law merges)
 └─► #1733 owner+green, WO3 route, lane owners, dispatch owner
WO1 ──► licp green ──► WO8 (distinguish new RED from old RED)
WO1 ──► GATE acceptance (candidate path runs through commit-proof)
WO9 ──► single learning_evidence writer (before seed lesson)
WO3 (gate live) ──► seed lesson ──► WO4/WO5 acceptance
WO3 contract frozen ──► WO4 build, WO5 verifier-chain
WO7 ──► WO2 (dedup before back-sync)
WO5a (seam proven) ──► WO5b
#1733 green ──► WO4 (hard)
WO4 ──► WO5b (contract order)
Arming gate: GATE live ∧ #1733 merged ∧ synthetic green ──► production arming
IGNITION + GATE + TRUTH + CONNECTION ──► PROOF
G8 migration (human gate) ──► PROOF (ranked retrieval)
```

**Parallel-safe:** WO1 ∥ WO8-build ∥ WO9 ∥ WO3-build ∥ WO7 ∥ WO6 (no shared files). **Serialized:** WO1→WO8 acceptance; WO7→WO2; #1733→WO4→WO5b; GATE-build→GATE-acceptance(after IGNITION green); everything→PROOF. WO2 and WO3's workflow-job alternative both touch `live-supabase-runtime-proof.yml` — if the workflow-job route is chosen, serialize those edits.

---

## PART 4 — SCORECARD (why this sequence won)

Alternatives: **A** (blueprint order: IGNITION→GATE+TRUTH∥→CONNECTION→CLEANUP→PROOF) · **B** (CONNECTION-first) · **C** (TRUTH-first) · **D** (max parallel) · **E** (Alt A + pre-flight + synthetic rehearsal + explicit arming gate).

| Dimension (weight) | A | B | C | D | **E (winner)** |
|---|---|---|---|---|---|
| Unblocks downstream (0.20) | 7 | 5 | 4 | 6 | 8 |
| Time-to-first-closed-loop (0.25) | 7 | 5 | 4 | 8 | 8 |
| Builds on verified foundations (0.25) | 6 | 3 | 5 | 4 | 9 |
| Coordination cost, higher=cheaper (0.15) | 7 | 8 | 8 | 4 | 5 |
| Reversibility if wrong (0.15) | 7 | 6 | 7 | 5 | 8 |
| **Weighted total** | **6.75** | **5.10** | **5.30** | **5.55** | **7.80** |

**Why B lost:** builds behavior-change machinery before the filter defining "verified" exists — TREATMENT would measure the seam against lessons of unknown provenance. Epistemically unsound, not just risky.
**Why C lost:** its rationale ("clean data before consumers") is refuted — CONNECTION reads Supabase `learning_evidence`, never the repo registry TRUTH cleans. It serializes janitorial work ahead of the value path for no causal benefit.
**Why D lost:** parallel consumers on the unsettled admission contract; WO2/WO7 racing on `index.json`; interface drift across lanes coordinating via comments.
**Why E won:** starts the riskiest build earliest (synthetic rehearsal, zero production exposure), pays off the two smuggled assumptions (deployed parity, #1733) as first-class pre-flight steps, and makes the GATE→arming dependency explicit (build vs arm are separate decisions). The consensus plan above **is Alt E**, hardened with the verification lead's ungameable done-whens and the integrator's WO9/WO10 additions.

---

## PART 5 — HOLES FOUND AND HOW THEY'RE ADDRESSED

| # | Hole (found by) | Addressed in |
|---|---|---|
| H1 | PROOF's deps omitted TRUTH (learning owner, judge) | §2 PROOF deps: IGNITION+GATE+TRUTH+CONNECTION |
| H2 | GATE acceptance can't run until IGNITION green (learning owner) | §2 GATE: build parallel, acceptance after green |
| H3 | WO5's kernel→Supabase seam unscoped; credential may be human-gated (learning owner) | New WO5a as hard precondition |
| H4 | WO1's `workflow_dispatch` owner unnamed; agents can't dispatch (learning owner) | WO0 names the dispatch owner |
| H5 | #1733 "or port it" fallback dropped; greenness unverified (learning owner, judge, verification) | WO0: merge-vs-port decision; §4 hard precondition = merged green, else re-implement+test |
| H6 | Nothing produces the first ACTIVE lesson WO4/WO5 need (learning owner) | Seed-lesson fixture in GATE |
| H7 | TS port vs workflow job not equivalent (enforced vs advisory) (learning owner) | WO0 decides route; TS port = target |
| H8 | WO2 audit-facing, not behavioral — tradeoff unnamed (learning owner) | Named in §2 TRUTH; PROOF still requires it |
| H9 | "CONNECTION benefits from TRUTH" refuted — neither reads the registry (judge) | Dependency map corrected; Alt C rationale retired |
| H10 | CONNECTION production arming hard-blocked on GATE live (judge) | Explicit arming gate in §4 |
| H11 | Deployed-vs-main parity smuggled (judge, verification) | WO0 parity check; human gate if gap |
| H12 | WO1 "unblocks pipeline" false rationale (judge) | Corrected: hygiene, sequenced for RED-distinguishability |
| H13 | WO7 before WO2 within TRUTH (judge) | Serialized in §2 |
| H14 | PROOF dropped "(not from the prompt)" anti-leak clause (judge) | Restored in §1 item 1 |
| H15 | Two-pipelines problem unresolved; v7 receiver keeps writing dead rows (integrator) | New WO9 |
| H16 | WO2 creates second promotion writer (duplicate mechanism w/ `promote_note()`) (integrator) | WO2 routed through `promote_note()`; G2 folded in |
| H17 | WO2 second index.json pusher; no loop-guard; .md header stale (integrator) | Serialization + loop-guard + header update in WO2 |
| H18 | WO4/WO5 in two runtimes, no bridge; G12 untouched (integrator) | New WO10 |
| H19 | No memory-precedence rule (181 DURABLE blocks vs ACTIVE lessons) (integrator) | Named precedence rule in WO4 |
| H20 | PROOF had no human acceptance gate (integrator) | §1 item 2 + §6 human close-out; Shawn's verdict |
| H21 | G8 ranked-retrieval RPC missing; migration human-gated (integrator) | Named as PROOF prerequisite |
| H22 | All six "done when"s gameable (verification) | Rewritten ungameable versions in §2 |
| H23 | Hand-seeded ACTIVE rows bypass the pipeline (verification) | Forbidden in WO4/WO5 done-whens |
| H24 | Trivial retrieval path (content-hash) vs ranked path (verification) | Ranked path required in §1 item 1 |
| H25 | Non-independent verifier / prompt leakage (verification) | Blind different-seat verifier + published prompts |
| H26 | Concurrent index.json writers / quiescence (verification) | Serialization + quiescence re-read in WO2 |

---

## PART 6 — UNRESOLVED / EXPLICITLY DEFERRED

1. **Lane owners** are proposed, not confirmed — each seat confirms or renegotiates on #1354.
2. **WO3 route** (TS port vs workflow job) — decided in WO0, not here.
3. **#1733 merge-vs-port** — decided in WO0 after state check.
4. **WO10's architecture** (shared store vs single runtime) — the CONNECTION team proposes; the plan requires the outcome, not the mechanism.
5. **Wall-clock estimates** — the plan does not estimate; WO0 is hours, IGNITION is under an hour of work, the long poles are WO3's TS port and WO5b. Estimates without scoping WO5a would be fiction.
6. **The 19 duplicate SN numbers' canonical picks** — WO7 executes first-claim-stands; disputes go to the owning lane, not to this plan.

---

## PART 7 — CONSENSUS RECORD

Four independent reviews (learning-lane owner, verification lead, independent judge, systems integrator) read the blueprint and draft in full. All four agreed: **Alt A's skeleton is correct; B and D are out; C's rationale is refuted.** The judge's Alt E (7.80) beat the draft's Alt A (6.75) on the weighted scorecard; the verification lead's hardened Alt A′ and the integrator's A-with-fixes both converged on the same structure as E. Disagreements resolved with evidence:
- *Parallel vs serial within phases* → serialized where shared files are touched (WO1→WO8, WO7→WO2, #1733→WO4→WO5b); parallel where proven independent.
- *Is TRUTH before CONNECTION?* → Yes for PROOF's receipt chain and human trust; no data dependency — stated honestly, not as a false rationale.
- *Does the plan need WO9/WO10?* → Yes; the end state is fractured without them. Added as first-class work orders.
- *Build vs arm* → separate decisions with an explicit arming gate.

No reviewer dissented from the final structure. Remaining unknowns are listed in Part 6, not hidden.

---

*End of Consensus Plan v1. Next: lane owners confirm on #1354; WO0 begins. Nothing in this plan is claimed without evidence; what isn't proven isn't claimed.*
