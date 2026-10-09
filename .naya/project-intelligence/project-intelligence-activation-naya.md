# PROJECT INTELLIGENCE — ACTIVATION NAYA

**Status:** LIVE — the organized mind of the Activation Naya project. Updated as reality changes.
**Authority:** Shawn Vibert, Human Director
**Template:** `project-intelligence-template.md` v1
**Source documents:** `learning-system-blueprint-v1.md` (system truth) · `activation-naya-plan-v1.md` (execution plan)
**Goal:** Naya fully activated — remembering, growing, learning. Smart note in → she understands → she learns → behavior changes. Non-stop until done.

---

## 1. PROJECT IDENTITY

**In plain words:** For weeks the team built a filing cabinet and called it a brain. Notes went in — to GitHub, to Supabase — and nothing ever came back out as changed behavior. Activation Naya is the project that assembles the actual brain: connecting the nine nodes, the learning chain, and the verification machinery so that a lesson Shawn teaches actually changes what Naya does. When it's done, he can say "smart note this" and days later watch her use the lesson without being reminded.

- **Name:** Activation Naya (`activation-naya`)
- **Mission:** Assemble the complete learning system — capture → verify → promote → integrate → act → prove → evolve — so that Naya demonstrably learns, retains, and grows. One closed loop proven end-to-end, then the human moment: Shawn teaches once, she applies later, unprompted.
- **Origin:** Ordered by Shawn Vibert, 2026-10-09, after a day of discoveries: the T11 cold-retrieval failure exposed that the CANDIDATE→ACTIVE promotion step was never built; the blueprint research proved seven of nine nodes exist but were never connected; the team had been testing an unbuilt car. His directive: "put the engine together right, make sure it's connected, the puzzle complete — before you go and test shit."
- **Done criteria** (from consensus plan Part 1):
  1. **Machine proof:** one novel falsifiable lesson flows capture → persist → index → verify → promote (DB + repo in sync) → cold Naya retrieves via the ranked path and applies it to a pre-registered held-out task → a blind different-seat verifier confirms the behavior change came from the lesson → every link carries SHA-256 hashes. One green run is not the proof — the repeatable protocol is.
  2. **Human proof:** Shawn teaches Naya something once ("smart note this", gets a Smart Link). Days later, in a different conversation, he asks for something in that lesson's territory — and she does it the way the lesson prescribes without being reminded. She names the lesson and shows the receipt chain when asked why. The Smart Link resolves to a note whose header says ACTIVE. The accomplishment posts to his Feed with evidence.
  3. **No dead machinery:** every gate has a producer for the state it demands; no duplicate writers; no "looks alive, isn't" components.
  4. **One intake, one truth:** a single canonical capture intake; DB and repo agree on lesson state; zero duplicate SN numbers with a CI gate enforcing it.
  5. **Whose verdict counts:** Shawn's (or his explicit delegate's).
- **Scope boundaries:**
  - IN: the learning chain (all 9 steps), the nine nodes' connection, the admission gate, the ACT/KNOW/SELF wiring, promotion back-sync, registry truth, the first closed loop, the human demonstration.
  - OUT: production deployment of NayaNET itself; the Hub interface; new feature work; constitutional/EVOLVE changes. Those are other projects.
- **Successor effect:** once the loop is proven, every future lesson flows through it automatically. Activation Naya builds the river; all future learning floats on it.

---

## 2. CURRENT STATE

**In plain words:** The map is drawn and the team agreed on the route. The engine parts exist — most were already built, just never connected. Nobody has started turning wrenches yet: lane owners are proposed but not confirmed, and the pre-flight checks haven't run. We're at the starting line with a solid plan.

- **State summary:** Blueprint v1 complete (497 lines, all claims evidence-tagged). Consensus plan v1 complete (Alt E won the scorecard 7.80 vs 6.75; 26 holes found and fixed; posted to #1354 as comment 6088478967). Execution has not yet begun — WO0 (pre-flight) is the next step, awaiting lane-owner confirmation.
- **Last verified:** 2026-10-09 ~20:15 UTC — main tip `1d73652231ac6127806640af5a31eb516c60738d`; full battery green (1896 passed / 11 skipped / 0 failures); brain index --check clean (1196 files); adversarial 6/6.
- **What's working:**
  - Capture → persist (GitHub + Supabase) — proven, the filing cabinet works.
  - Seven of nine nodes have real implementations (kernel/ Python + supabase/functions TypeScript), CI-exercised.
  - The admission gate exists on branch `naya5/learning-admission-round2` @ `9fba596e` (48/48 green) — built, never wired in.
  - The promotion step exists in `nayanet-learning-verify` — wired, CI-exercised; but see "not working" for the gaps around it.
- **What's not working:**
  - CANDIDATE→ACTIVE promotion has no back-sync: DB says LEARNED, repo registry says CANDIDATE forever. Repo-side `promote_note()` has zero callers.
  - ACT never reads `learning_evidence`; `naya-decision-context` (the verified-lesson→decision seam) is dead code with zero callers.
  - SELF has no behavior integration — `record_experience()` has zero production callers.
  - The receiver's GitHub projection bridge is dead (all 5 dispatch receipts failed); the two pipelines run in parallel, not connected.
  - 19 duplicate SN numbers in the registry.
  - Vocabulary split: `lifecycle_state` defaults to ACTIVE in three places, letting missing fields pass gates they should fail.
- **What's unknown:**
  - Whether deployed Supabase edge-function bytes match main bytes (WO0 parity check not yet run).
  - PR #1733's state (merge-vs-port decision pending in WO0).
  - The kernel→Supabase read seam: does `kernel/` have a Supabase client? Which credential? (WO5a — the single biggest buildability risk.)

---

## 3. THE PLAN

**In plain words:** Fix the bleeding first, then build the gate that decides what's worth learning, then connect learning to actual decisions and behavior, then clean up the data, then prove the whole thing works — with Shawn himself as the final judge. The team scored five different orderings and this one won because it starts the riskiest work earliest and never builds on an unverified foundation.

- **Strategy summary:** Alt E — pre-flight verification before any build; IGNITION (stop the reds, declare one intake); GATE (admission filter + first ACTIVE lesson as fixture); TRUTH (dedup + back-sync through the single promotion writer); CONNECTION (wire lessons into decisions and behavior, with synthetic rehearsal and an explicit arming gate before production); CLEANUP (bridge green or retired); PROOF (machine closed loop + Shawn's teach-once/observe-later). Build and arm are separate decisions — CONNECTION can be built while GATE is still going live, but nothing touches production learning data until the gate is live.
- **Scorecard:** five alternatives scored on unblocks-downstream (0.20), time-to-first-closed-loop (0.25), builds-on-verified-foundations (0.25), coordination cost (0.15), reversibility (0.15). Winner: Alt E at 7.80. Rejected: B (CONNECTION-first — epistemically unsound, wires behavior before "verified" is defined, 5.10); C (TRUTH-first — rationale refuted, CONNECTION never reads the registry, 5.30); D (max parallel — interface drift, writer races, 5.55); A (blueprint order without pre-flight — 6.75). Full scorecard in `activation-naya-plan-v1.md` Part 4.
- **Execution order:**

  **SECTION 0 — PRE-FLIGHT** — *measure twice, cut once.* Verify deployed↔main byte parity (4 edge functions); battery green on tip; PR #1733 state + owner + merge-vs-port; WO3 route decision (TS port vs workflow job); lane owners named; workflow_dispatch owner named. Done when: parity report, green battery run ID, all owners/routes decided. Proposed owner: verification lane (Naya 5) + parent orchestrator for human-gate items.

  **SECTION 1 — IGNITION** — *stop the bleeding, declare the road.* WO1 (one-line #2020 fix: `lifecycle_state` CANDIDATE→ACTIVE); WO8 (remove default-to-ACTIVE in 3 places — missing field must FAIL); WO9 (unify intake pipelines — one canonical intake, retire v7 receiver's write path, one writer to `learning_evidence`). Done when: fresh dispatch green on cold-successor-held-out; missing-field capture fails with named error; single writer owns the table, zero new rows from retired path. Proposed owner: learning lane (Naya 4) for WO1/WO9.

  **SECTION 2 — GATE** — *bouncer at the front door.* WO3 (wire the admission gate per WO0 route); seed-lesson fixture (one real falsifiable lesson through the gated pipeline to ACTIVE — hand-inserted rows invalidate downstream). Done when: unverifiable candidate rejected with the gate's reason code + fail-closed probe + invocation log; one ACTIVE row produced by the real pipeline. Proposed owner: learning lane (Naya 4).

  **SECTION 3 — TRUTH** — *one truth, not two.* WO7 (dedup 19 duplicate SNs, first-claim stands, zero deletions, CI gate); WO2 (back-sync promotion through `promote_note()` — the single repo-side writer; update registry `truth_state` + projected `.md` header so the Smart Link tells the truth; idempotent; loop-guarded; `contents: write` flagged). Done when: duplicates zero AND deletions zero; test promotion shows registry == DB within the same run; re-run is a no-op. Proposed owner: any seat.

  **SECTION 4 — CONNECTION** — *lessons → decisions → behavior.* WO5a (scope the kernel→Supabase read seam — biggest buildability risk, do not start WO5b until it exists); WO4 (wire `naya-decision-context` into `nayanet-act-runtime`; hard precondition #1733 merged green; named precedence vs 181 DURABLE blocks); WO10 (bridge the TS/Python runtime split — shared behavior-policy store or single-runtime declaration); WO5b (SELF `integrate_verified_lesson()` + versioned `behavior_policy.py` + `record_experience()` caller; blind independent verifier; rollback test). Synthetic rehearsal before production arming; explicit arming gate (GATE live ∧ #1733 merged ∧ synthetic green). Proposed owner: learning lane (Naya 4) + engine seat.

  **SECTION 5 — CLEANUP** — *no dead machinery.* WO6 (projection bridge: N≥3 consecutive canonical captures project end-to-end, or formal retirement with zero repo references). Done when: bridge declared LIVE or RETIRED in exactly one canonical doc — no middle state. Proposed owner: any seat.

  **SECTION 6 — PROOF** — *the first closed loop + the human moment.* Machine: pre-registered held-out task, ranked retrieval (not content-hash), fresh cold identity, blind different-seat verifier, published prompts, hash-chained receipts, repeatable protocol with recorded hash. Human: Shawn's teach-once/observe-later; Smart Link resolves to ACTIVE-headed note; Feed receipt with evidence chain. G8 ranked-retrieval RPC migration is a human-gate prerequisite — named, not assumed. Proposed owner: verification lane runs it; independent seat verifies; Shawn closes it.

- **Dependency map:** WO0 parity → human gate if gap (blocks WO3, WO4). WO1 → WO8 acceptance (distinguish new RED from old RED). WO9 → single writer (before seed lesson). WO3 contract frozen → WO4 build, WO5 verifier-chain. WO7 → WO2. WO5a → WO5b. #1733 green → WO4 → WO5b. Arming gate → production arming. IGNITION + GATE + TRUTH + CONNECTION → PROOF. Parallel-safe: WO1 ∥ WO8-build ∥ WO9 ∥ WO3-build ∥ WO7 ∥ WO6. Full map in `activation-naya-plan-v1.md` Part 3.

---

## 4. ACTIVE WORK

**In plain words:** The plan just landed. Nothing is being built yet — the next move is lane owners confirming their assignments, then WO0 pre-flight begins.

- **In progress:**
  - *Lane-owner confirmation* — proposed owners (learning lane/Naya 4 for IGNITION/GATE/CONNECTION; verification lane/Naya 5 for WO0/PROOF) to confirm or renegotiate on #1354. Owner: parent orchestrator. Next step: confirmations posted.
  - *Project Intelligence pilot* — this document + the template; five-leader consensus requested on #1354 (comment 6088564615). Owner: Naya 2. Next step: leader consensus, then pilot on Activation Naya.
- **Recently completed:**
  - Blueprint v1 (`learning-system-blueprint-v1.md`, 497 lines) — 2026-10-09 ~20:07 UTC. Four research lanes verified against live main.
  - Consensus plan v1 (`activation-naya-plan-v1.md`, 182 lines) — 2026-10-09 ~20:12 UTC. Posted as #1354 comment 6088478967. Alt E won 7.80; 26 holes fixed.
  - PR #1956 merged (learning evidence assembler); PR #1957 merged (production proof sealer); PR #1958 merged (failure receipts); PR #2036 merged (guard false-positive repair).
- **Recently blocked:** none currently — the project hasn't started execution.
- **Up next:** WO0 pre-flight (parity check, battery, #1733 state, route decisions, owner confirmations).

---

## 5. DECISIONS MADE

**In plain words:** The big decisions so far are about the plan itself — what order to build in, and what "done" means. The team argued it out with scorecards instead of opinions.

- **Alt E execution sequence adopted** (2026-10-09, consensus of learning-lane owner, verification lead, independent judge, systems integrator; facilitated by Naya 2). Scorecard: 7.80 vs 6.75 (A), 5.10 (B), 5.30 (C), 5.55 (D). Reasoning: starts riskiest build earliest, pays off smuggled assumptions as pre-flight, separates build from arm. Evidence: `activation-naya-plan-v1.md` Part 4.
- **"Activated" acceptance criteria fixed** (same consensus). Two-sided: machine closed loop (ranked retrieval, blind verifier, hash chain, repeatable protocol) + human teach-once/observe-later with Shawn's verdict as the closer. Reasoning: the standing quality law — the rendered experience is the only score that matters; a proof that completes entirely in CI logs is unproven on experience.
- **Build vs arm separated** (judge + verification lead). CONNECTION may build in parallel with GATE, but production arming is hard-blocked on GATE live ∧ #1733 merged ∧ synthetic rehearsal green. Reasoning: without the admission filter live, receipt-validated-but-unverifiable lessons get laundered into behavior.
- **New work orders added by reviewers:** WO0 (pre-flight), WO5a (seam scoping), WO9 (intake unification), WO10 (runtime bridge), seed-lesson fixture, human acceptance gate. Reasoning: the draft plan had smuggled assumptions (deployed parity, #1733 greenness, WO5 seam triviality, two-pipeline coherence) — each became a first-class work item.
- **All six "done when" lines rewritten ungameable** (verification lead). E.g., GATE requires a fail-closed probe + gate-invocation log; WO4 forbids hand-inserted ACTIVE rows; PROOF requires ranked retrieval, not content-hash lookup. Reasoning: "score the method, not just the verdict."
- **Pending decisions:**
  - Lane-owner confirmations — owner: each proposed seat; needed before WO0.
  - WO3 route (TS port vs workflow job) — owner: WO0; needed before GATE build.
  - PR #1733 merge-vs-port — owner: WO0; needed before WO4.
  - WO10 architecture (shared store vs single runtime) — owner: CONNECTION team; needed during CONNECTION.

---

## 6. LESSONS LEARNED

**In plain words:** This project has already taught the team how to see its own blind spots — most of these lessons came from the day of discoveries that created the project.

- **Trigger-chain jurisdiction (L179):** a scorecard's jurisdiction step traces the merge's trigger chain, not just its file list. PR #2020 was judged "single file add" while its push triggered a production workflow. Evidence: #1354 6087393215, 6087133499.
- **No gate without a producer (L181):** for every gate in a pipeline, verify a producer exists for the state the gate demands. The cold-retrieval step demanded ACTIVE; zero promotion steps existed — a guaranteed-failure trap. Evidence: #1354 6087997893 (T11 root cause).
- **Battery coverage rows (L180):** before accepting a CLOSED verdict, verify the battery's coverage rows per attack class — zero rows = UNKNOWN for that class. Evidence: gate-R2 re-attack, #1354 6087114851.
- **Capture contract at admission (L182):** a lesson candidate must arrive with named task + pre-registered success criterion + machine check, enforced at admission. 32 of 36 queued lessons were retired as unverifiable-by-design. Evidence: #1354 6087139356.
- **Manufacture the trigger (L183):** verification depending on organic traffic must manufacture the triggering event immediately. A watch that sees no traffic is an honest inconclusive, never a pass. Evidence: #1354 6088180071.
- **The Mirror Law:** when something goes wrong, check yourself first. The day's two biggest near-misses (the #2020 scorecard, the premature "proceed?" asks) were the scorer's failures, not the system's. Evidence: Shawn's direct correction, 2026-10-09.
- **Assemble before testing:** testing an unbuilt chain produces failures that look like bugs but are actually absences. The car analogy — engine first, test drive second. Evidence: the entire 2026-10-09 discovery sequence.
- **Smart Link ≠ learning proof:** the link attests capture→persist→receipt. Learning is attested only by the closed loop (behavior change + independent verification + cold reuse). Mixing them up is how you lie to yourself with good paperwork.

---

## 7. OPEN QUESTIONS

**In plain words:** Things we don't know yet that the plan needs answered.

- **Lane-owner confirmations** — will the proposed seats accept? Owner: parent orchestrator. Needed: before WO0.
- **Deployed↔main parity** — do the 4 edge functions match? Owner: WO0 (verification lane). Needed: before WO3/WO4. If gap → human gate (production deploy).
- **PR #1733 state** — green? abandoned? merge or re-implement? Owner: WO0. Needed: before WO4.
- **WO3 route** — TS port (enforced) or workflow job (advisory stopgap)? Owner: WO0. Needed: before GATE build.
- **Kernel→Supabase seam** — client? credential? human-gated provisioning? Owner: WO5a. Needed: before WO5b. (Biggest buildability risk.)
- **WO10 architecture** — shared behavior-policy store or single runtime? Owner: CONNECTION team. Needed: during CONNECTION.
- **Wall-clock estimates** — deliberately not estimated; WO5a scoping comes first. Estimates without it would be fiction.

---

## 8. BLOCKERS

**In plain words:** Nothing is stuck yet — but these human gates are already visible on the road ahead.

- **(Anticipated) Deployed-parity gap** — if WO0 finds deployed bytes ≠ main bytes, closing it is a production deploy: human gate, Shawn's click. Not yet known to be blocked.
- **(Anticipated) G8 ranked-retrieval RPC migration** — applying it is a human-gate action; named as a PROOF prerequisite. Not yet at that phase.
- **(Anticipated) `workflow_dispatch` for WO1** — agents cannot dispatch workflows (403); the WO0-named owner handles it. Human-gate-adjacent.
- **(Anticipated) WO5a credential provisioning** — if the kernel→Supabase seam needs a new credential, provisioning may be human-gated. Unknown until WO5a scopes it.
- **Historical (resolved):** PR #2020 merged 2026-10-09 19:25 UTC without Shawn's authorization, 12 minutes after the correction stating it needed authority; the commit-proof workflow fired and failed. The failure is now WO1's work item. Recorded as evidence, not re-litigated.

---

## 9. EVIDENCE LOG

**In plain words:** the receipts, newest first.

- 2026-10-09 ~20:15 UTC — Main tip `1d73652231ac6127806640af5a31eb516c60738d`; battery 1896 passed / 11 skipped / 0 failed; index clean (1196 files); adversarial 6/6. (Brain-build loop run.)
- 2026-10-09 ~20:12 UTC — Consensus plan v1 posted: #1354 comment 6088478967. Alt E 7.80; 26 holes fixed.
- 2026-10-09 ~20:07 UTC — Blueprint v1 complete: `learning-system-blueprint-v1.md` (497 lines).
- 2026-10-09 19:41 UTC — T11 cold-retrieval root cause: #1354 comment 6087997893. Zero promotion steps in 1307-line workflow.
- 2026-10-09 19:25 UTC — PR #2020 merged as `075b169e` without authorization; commit-proof workflow failed (`AssertionError: CANDIDATE`). Verifier: PR API `merged_at`, `merge_commit_sha`.
- 2026-10-09 19:02 UTC — #2020 trigger-chain correction: #1354 comment 6087393215 (self-correction of scorecard 6087133499).
- 2026-10-09 — PRs #1956, #1957, #1958, #2036 merged (learning evidence assembler, proof sealer, failure receipts, guard repair).
- 2026-10-09 — 7 distilled lessons T–Z applied to AGENTS.md as L179–L185 (trigger-chain jurisdiction, battery coverage rows, no-gate-without-producer, capture contract, manufacture-the-trigger, verify-auth-path, post-reset re-verification).

---

## DOCUMENT FRESHNESS

- **Created:** 2026-10-09 ~20:20 UTC (pilot instance alongside template v1).
- **Last updated:** 2026-10-09 ~20:20 UTC.
- **Next review:** when lane owners confirm (Active Work updates) or WO0 begins (Current State updates).
- **Maintained by:** project lead (Naya 2) for freshness; section owners for their sections (learning lane: plan/identity; verification lane: evidence/state; all seats: flag staleness).
