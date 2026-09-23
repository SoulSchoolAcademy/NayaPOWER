# NAYA POWER SUPERBRAIN OPERATING SYSTEM BLUEPRINT V1

STATUS: UNRATIFIED DESIGN ARTIFACT. Not a constitution. Does not create authority.
PRODUCED: 2026-09-16
REPOSITORY: SoulSchoolAcademy/NayaPOWER (origin: https://github.com/SoulSchoolAcademy/NayaPOWER.git)
AUTHORING WORKTREE: C:/Users/Admin/NayaPOWER-Windows
AUTHORING BRANCH: naya/universal-execution-gate-v1
AUTHORING HEAD: 7ce7cac14ecfe46439c46f594dc046f170e0d04d
origin/main (fetched): 94d2c561d4e6410c03a116f691186bead710b78c
local main: 896594e9453312d85b00a5d4c6e5d41d29f72d76
AUTHORITY: None. This document recommends. Only Shawn (human authority) authorizes.

---

## SECTION 0. HOW TO READ THIS DOCUMENT

This is the required output of the mission "SANDBOX == REAL ENGINE, PROVE IT". It is
simultaneously (a) a repository-truth audit and (b) the operating-system design that would
make the repository self-explaining and self-operating. Every factual claim below is either
(a) verified by direct inspection during this audit, or (b) explicitly marked UNKNOWN or
UNVERIFIED. Nothing here is asserted from memory of prior conversations.

Ground-truth anchors used throughout:
- git worktree list -> two worktrees exist (see §4, §42).
- .naya/control-plane/STATE.json -> machine-declared current state (see §12).
- .naya/codex/11-RUNTIME-CONSTITUTION.md -> present.
- SUPERBRAIN/NAYAPOWER-CANONICAL-SOURCE-MAP.md -> present.
- .naya/execution/, .naya/state/, .naya/runtime/, .naya/governance/, .naya/contracts/,
  .naya/actions/, .naya/memory/, .naya/codex/, .naya/handoffs/, .naya/execution-prompts/
  -> inspected.

---

## SECTION 1. EXECUTIVE UNDERSTANDING

The repository already contains the organs of a self-operating network: a runtime
constitution (`.naya/codex/11-RUNTIME-CONSTITUTION.md`), a control plane that resolves live
HEAD rather than trusting recorded state (`.naya/control-plane/STATE.json`), a fail-closed
governance kernel, an authority registry, an execution controller, a model/tool gateway, an
evidence runtime, an independent verifier (OSCAR), a continuity enforcement layer, a
canonical event store, canonical Action schemas, a verification-receipt schema, a rich memory
runtime, a canonical source map, a Hub Read-First gate, and a continuous-project-execution
loop contract in AI-BOOT.

What it does NOT have is a single nervous system connecting them into one continuously
running, self-verifying, self-recording loop - and, more urgently, it does not currently have
ONE authoritative line of work.

The single most important audit finding is NOT a missing capability. It is this:

> The repository is currently carrying AT LEAST TWO divergent governed-execution efforts in
> two linked worktrees, plus uncommitted work in the active worktree, while the canonical
> control plane declares a THIRD, different current mission. A cold Naya cannot determine
> which line of work is current without human adjudication.

This is the highest-value bottleneck. Everything else - the supervisor, the quality gate, the
regression guard, automatic Activity, boot wiring - is downstream of resolving which branch,
which worktree, and which queue are canonical.

Detailed evidence is in §4, §12, §41, §42, §43.

---

## SECTION 2. MISSION

The enduring mission (from `.naya/control-plane/STATE.json`):
"Make it dramatically easier for an ordinary human with a meaningful vision to accomplish
extraordinary things with AI without becoming an AI project manager."

The Superbrain Operating System's mission: make the repository capable of continuously
building NayaNET itself - a cold Naya can enter, understand the whole machine, determine the
single highest-value authorized action, execute it under governance, prove it, record it, and
hand the next action forward without routine human clarification.

North star (control plane): "Maximum verified human value per unit of effort, with compounding
intelligence and continuity."

---

## SECTION 3. SYSTEM ONTOLOGY

The repository is to function simultaneously as: MEMORY (what happened), KNOWLEDGE (what we
know), ARCHITECTURE (how it fits), GOVERNANCE (what is permitted), STATE (where we are),
INTENT (what we are trying to do), WORK QUEUE (what must happen), EXECUTION SYSTEM (how work
happens), EVIDENCE SYSTEM (how we know), QUALITY SYSTEM (is it good enough), ACTIVITY SYSTEM
(who/what/when/why), CONTINUITY SYSTEM (what the next Naya needs), LEARNING SYSTEM (what we
discovered), OPTIMIZATION SYSTEM (what should improve), CONTROL PLANE (what is authoritative),
COLLECTIVE INTELLIGENCE (how agents cooperate without chaos).

Ontological law: every claim about "what is true" must resolve to exactly one surface, and
every surface must have exactly one authority. Where two surfaces claim the same truth, that
is a CONFLICT and must be classified, not merged.

---

## SECTION 4. REPOSITORY MAP

Physical topology (VERIFIED via `git worktree list`):

| Worktree | Branch | HEAD | Notes |
|---|---|---|---|
| C:/Users/Admin/NayaPOWER-Windows | naya/universal-execution-gate-v1 | 7ce7cac1 | Active session. DIRTY: 6 modified files, +798/-188; 6 untracked test files; untracked __pycache__ |
| C:/Users/Admin/AppData/Local/Temp/opencode/naya-main | wiz/autonomous-hardening | 375814fd | Linked worktree. Holds M1 Work Queue + Progress Index (see below) |

Divergence: HEAD (7ce7cac1) is not an ancestor of origin/main and origin/main is not an
ancestor of HEAD; `git merge-base HEAD origin/main` returned empty at the current fetch depth
(see §42 for the honest reading of this). `git rev-list --left-right --count origin/main...HEAD`
reported `22  5883`.

Canonical surfaces by role:

| Surface | Location | State on this branch |
|---|---|---|
| Runtime Constitution | .naya/codex/11-RUNTIME-CONSTITUTION.md | PRESENT |
| Runtime completeness laws | .naya/codex/12-RUNTIME-COMPLETENESS-LAWS.md | PRESENT |
| Control plane | .naya/control-plane/{MAP,STATE,BLOCKS,PROOF}.json | PRESENT |
| Governance kernel | .naya/governance/governance_kernel.py | PRESENT (duplicate exists, §41) |
| Authority registry | .naya/governance/{authority-registry.json,NAYA-AUTHORITY-REGISTRY-V1.json} | PRESENT |
| Action ledger | .naya/governance/ACTION-LEDGER.json | PRESENT |
| Runtime primitives | .naya/runtime/*.py | PRESENT (large) |
| Contracts | .naya/contracts/* | PRESENT incl. VERIFICATION-RECEIPT-SCHEMA, PRIMARY-INTELLIGENCE-SYSTEM-CONTRACT |
| Action schema | .naya/contracts/NAYA-ACTION-V1.schema.json AND .naya/actions/NAYA_ACTION_V1.schema.json | DUPLICATE |
| Action records | .naya/actions/ | PRESENT, records 001-005 dated 2026-09-15 |
| Work Queue | .naya/execution/WORK-QUEUE.json + validate_work_queue.py | ABSENT on this branch; PRESENT only on wiz/autonomous-hardening |
| Progress Index | .naya/state/CHECKPOINT-001.json + validate_progress_index.py | ABSENT on this branch; PRESENT only on wiz/autonomous-hardening |
| Measurement contracts | .naya/state/excellence-operating-contract.v1.json | PRESENT |
| Memory | .naya/memory/ | PRESENT, extensive |
| Handoffs | .naya/handoffs/ | PRESENT (dozens) |
| Next-action prompts | .naya/execution-prompts/ | 26 files, dated 2026-09-15 |
| Canonical source map | SUPERBRAIN/NAYAPOWER-CANONICAL-SOURCE-MAP.md | PRESENT |
| Boot chain | SUPERBRAIN/AI-BOOT/{START-HERE.md, AI-OPERATING-FEED.md, NAYA-CONTINUOUS-PROJECT-EXECUTION-LOOP.md, NAYA-POWER-ACTIVATION-PROTOCOL.md, NAYANET-HUB-READ-FIRST.md} | PRESENT |
| Product | NAYANET/HUB/ (PROTECTED) | PRESENT |
| Workflows | .github/workflows/ (35 files) | PRESENT; no 513-*; no authorized-vercel-release.yml |

---

## SECTION 5. COLD-NAYA ENTRY PATH

Intended path:
START-HERE.md -> AI-OPERATING-FEED.md -> control plane (MAP/STATE/BLOCKS/PROOF) -> Hub
Read-First gate (for Hub work) -> canonical source map -> current Activity -> Work Queue ->
Progress Index -> next authorized action.

VERIFIED GAP: `START-HERE.md` contains ZERO references to continuous execution or to
`NAYA-CONTINUOUS-PROJECT-EXECUTION-LOOP.md` (Select-String for "continuous" and
"CONTINUOUS-PROJECT-EXECUTION" returned nothing). The loop contract exists (17,663 bytes) but
is not wired into the boot path. The Work Queue and Progress Index exist only on a different
branch and are therefore invisible here. Cold-start is therefore PARTIAL.

---

## SECTION 6. SOURCE-OF-TRUTH HIERARCHY

1. Human authority (Shawn) - constitutional, final.
2. .naya/codex/11-RUNTIME-CONSTITUTION.md (+ amendments treated as records of change, never parallel constitutions).
3. Control plane MAP -> STATE -> BLOCKS -> PROOF (live-HEAD resolution beats recorded state).
4. Governance kernel + authority registry.
5. Contracts and schemas.
6. Action records + evidence/receipts.
7. Activity events.
8. Implementation code.
9. Historical/frozen artifacts (never authority).

Rule (already encoded in STATE.json truth_rules): "LIVE authoritative source outranks recorded
state"; "RECORDED_BUT_STALE is not CURRENT"; "UNKNOWN is not VERIFIED"; "BLOCKED is not PASS".

---

## SECTION 7. AUTHORITY MAP

Human-reserved (cannot be delegated to machine):
- Selecting the canonical branch/worktree and reconciling history.
- Deployment/release authority and the runtime target.
- Cloudflare credential/execution surface; PIS authority; 509 lane freeze/retire.
- Any push to main or protected branch.
- Protected-path changes.

Machine-authorized (repo-side, additive, reversible):
- Building/validating queue, progress index, supervisor composition, boot wiring, tests,
  evidence, Activity records - on the branch the human designates as canonical.

Hard prohibition (already in STATE.json protected_boundaries):
- Never fabricate runs/artifacts/logs/success; never weaken fail-closed behavior; never promote
  historical evidence to current proof; never treat BLOCKED as PASS; never create a second
  constitutional authority; never guess NAYA_POWER_TARGET_URL.

---

## SECTION 8. GOVERNANCE MAP

`governance_kernel.evaluate` -> DecisionObject (Epistemic / Risk / VerificationPlan) ->
authority resolution against `authority-registry.json` -> fail-closed on ambiguity. Tests:
`test_governance_kernel.py`, `test_behavioral_bypasses.py`, `test_naya_execution_boundaries.py`.
Stewardship: `stewardship_runtime.py`.

VERIFIED DEFECT: two `governance_kernel.py` files exist
(`.naya/control-plane/governance_kernel.py` and `.naya/governance/governance_kernel.py`).
This is a duplicate-authority hazard and is carried in §41.

---

## SECTION 9. ARCHITECTURE MAP

Six horizontal layers plus two verticals and one cross-cut:

Layers: Constitution -> Control Plane -> Governance -> Runtime/Execution -> Evidence/Quality ->
Continuity/Activity.
Verticals: Product (NAYANET/HUB), Release/Runtime.
Cross-cut: Measurement (Progress Index).

---

## SECTION 10. RUNTIME MAP

Primitives present in `.naya/runtime/`: restore_context, priority_decision, execution_controller,
model_tool_gateway, universal_execution_gate, portable_authorization, release_authorization,
release_execution_boundary, evidence_runtime, execution_evidence_adapter, oscar, outbox,
canonical_event_store, continuity_enforcement, project_execution_contract, executable_torch,
torch_execution_adapter, risk_engine, value_math_engine, naya_power_kernel,
naya_power_orchestrator, naya_power_live, system_health, promotion_runtime, and many CCT tests.

VERIFIED: no single top-level entry point composes restore -> select -> govern -> execute ->
observe -> verify -> score -> record -> continue. The pieces exist; the composition does not.

---

## SECTION 11. EXECUTION MAP

Target transaction:
READ -> UNDERSTAND -> GOVERN -> PRIORITIZE -> PLAN -> ASSEMBLE -> EXECUTE -> OBSERVE -> TEST ->
VERIFY -> SCORE -> REPAIR -> RESCORE -> ACCEPT -> RECORD -> LEARN -> SELECT NEXT -> CONTINUE.

Current reality: primitives + (on another branch) a durable queue + (on another branch) a
measurement layer, but no composed transaction and no consumer that runs the loop.

---

## SECTION 12. WORK QUEUE MODEL (AND THE CURRENT-STATE CONFLICT)

The Work Queue model (built on `wiz/autonomous-hardening`) is correct in design: one durable
`WORK-QUEUE.json`, each task carrying MISSION, OBJECTIVE, CURRENT STATE, WHY IT MATTERS,
DEPENDENCIES, AUTHORITY, CONSTRAINTS, PROTECTED BOUNDARIES, ACCEPTANCE CRITERIA, TESTS,
EVIDENCE, SCORECARD, MINIMUM SCORE, TARGET SCORE, RISK, ROLLBACK, SUCCESSOR ACTION, plus
priority metadata. Validate/select/self-test exist.

BUT (verified): that queue is NOT present on branch naya/universal-execution-gate-v1. It
exists only on the linked worktree branch. And the canonical control plane on THIS branch
declares a different current mission:

- `.naya/control-plane/STATE.json` -> priority "P0 - MACHINE TRUTH RESTORATION";
  current_block "TORCH-59-MACHINE-TRUTH-RESTORATION"; status ACTIVE; single_next_action =
  reconcile the missing Assistant-lane Cloudflare release mechanism/target.

So the repository currently presents three candidate "current missions":
(A) control plane: Assistant-lane Hub baseline restoration (TORCH-59).
(B) wiz/autonomous-hardening: build the execution supervisor (M2) atop the M1 queue.
(C) naya/universal-execution-gate-v1: universal execution gate / gateway / release-closure.

This is the central continuity failure. A cold Naya cannot resolve it from the repository
alone. Resolution requires human authority (§7).

---

## SECTION 13. AGENT ORCHESTRATION MODEL

Roles are FUNCTIONS invoked by the supervisor, not a fixed agent roster: Architect,
Governance, Execution, Runtime, Test, Evidence, Quality/OSCAR, Security, Continuity, Activity,
Intelligence, Product, Deployment, Research, Repair, Optimization, Red-Team. Orchestration
lives inside the composed supervisor; role count is determined per task.

---

## SECTION 14. AGENT-SPAWNING POLICY

Spawn a specialist iff: expected specialist contribution - coordination cost - risk > marginal
value of a single agent. One agent for trivial/reversible work. Multiple INDEPENDENT
perspectives for architectural, security, deployment, or release-critical work. Builder and
verifier are always separated (§7 of the mission).

---

## SECTION 15. EVIDENCE MODEL

Claim -> Evidence -> Verification -> Receipt, via `evidence_runtime` and
`.naya/contracts/VERIFICATION-RECEIPT-SCHEMA.json`. Evidence must bind to an exact revision.
The five-way separation (SPECIFICATION / IMPLEMENTATION / EVIDENCE / VERIFICATION /
PRODUCTION_TRUTH) must be preserved as distinct fields.

---

## SECTION 16. VERIFICATION MODEL

Independent adversarial verification by OSCAR (`oscar.py`). The builder may not self-accept.
The verifier must attempt to falsify its own claim and record what it could not disprove.

---

## SECTION 17. QUALITY MODEL

`.naya/state/excellence-operating-contract.v1.json` defines the dimension set (16 dimensions).
Floor 9.0; target 9.5+; objective 10.0. Any critical failure blocks acceptance; any score
below 9.0 blocks acceptance; sub-10 requires a written "WHY IS THIS NOT A 10?" and the exact
list of what would make it a 10. A per-task runtime quality gate is NOT yet implemented.

---

## SECTION 18. REGRESSION MODEL

Before/after comparison against applicable scores and protected-path state; any net reduction
=> REJECT / REPAIR / REVERT. `.naya/control-plane/PROGRESS-CHECKPOINT.json` provides
anti-rewind semantics. A scored regression guard is NOT yet implemented.

---

## SECTION 19. ACTIVITY MODEL

Canonical Activity is `.naya/activity/` (dated events; a structural validator exists). On this
branch, `.naya/activity/` contains both flat historical files and a `2026/` directory -
format coherence must be verified before automatic writing is enabled (see §41). Automatic
Activity creation from governed execution is NOT yet wired.

---

## SECTION 20. MEMORY MODEL

`.naya/memory/` provides memory_runtime, entity_resolution, duplicate_entity_audit,
relationship_graph, contradiction_supersession, retrieval manifest/benchmark, plus AI/HUMAN/
MACHINE notes and a canonical event lifecycle. `canonical_event_store.py` (runtime) provides
idempotent event creation. Layers: episodic (Activity), semantic (contracts/maps), working
(STATE).

---

## SECTION 21. CONTINUITY MODEL

`.naya/runtime/project_execution_contract.py`, `.naya/handoffs/` (dozens of AI-TO-AI handoffs),
`.naya/continuations/`, `.naya/execution-prompts/` (26 next actions), and
`executable_torch.py`. Continuity content exists in abundance; what is missing is a single
enforced successor contract that the execution system emits automatically.

---

## SECTION 22. LEARNING MODEL

Every checkpoint, score, defect, and repeated human question becomes durable memory and,
where legitimate, a queued task. Learning output is always a new task or an improved contract,
never a silent behavior change.

---

## SECTION 23. OPTIMIZATION MODEL

Optimization is a queued task class. Confirmed optimization targets: duplicate
governance_kernel (2), duplicate NAYA-ACTION schema (2), competing PIS builders, competing
deployment lanes, dead Hub shells, and duplicated orchestration logic between
`naya_power_kernel.py`, `naya_power_orchestrator.py`, `naya_power_live.py`, and the two
worktree efforts.

---

## SECTION 24. DEPLOYMENT / RELEASE MODEL

35 workflows exist in `.github/workflows/`. VERIFIED: no `513-*` workflow and no
`authorized-vercel-release.yml` on this branch. Competing/candidate release lanes present
include `nayanet-canonical-hub-production-release.yml`, `naya-canonical-react-build-handoff.yml`,
`assistant-cloudflare-hub-release.yml`, `verify-nayanet-hub-build-only.yml`, and many 509-*.

CONTROL-PLANE-DECLARED BLOCKER: the recorded canonical Assistant-lane Cloudflare release
mechanism is absent; the runtime target is UNKNOWN; deployment remains default-deny. Release
authority is HUMAN and is currently unsatisfied.

---

## SECTION 25. HUMAN-INTERFACE MODEL

Humans receive: morning report, evidence-backed decision packages (candidate / purpose / who
deploys / what it serves / live content / source / artifact / dependencies / verification /
risks / migration cost / recommended status), and the Progress Index. Humans are not asked
"which worker?" or "what now?" - those must be answerable from the repository.

---

## SECTION 26. HUMAN CLARIFICATION MODEL

Track Human Clarification Rate; classify each question as: answerable-from-repo /
genuine-authority / missing-docs / conflicting-authority / missing-runtime-evidence. Every
avoidable question spawns a task. The current audit demonstrates the classification working:
the branch-canonicalization question is a GENUINE-AUTHORITY question and must not be answered
by the machine.

---

## SECTION 27. SECURITY / PRIVACY BOUNDARIES

Secrets never logged or committed; consequential actions gated behind a claim
(`model_tool_gateway`); forged-authority and fabricated-authority regression tests exist
(`test_behavioral_bypasses.py`, gateway boundary tests); protected paths enforced; fail-closed
on ambiguity; never guess the runtime target URL.

---

## SECTION 28. FAILURE / REPAIR MODEL

BUILD -> BREAK -> TEST -> FIND DEFECTS -> REPAIR -> VERIFY -> RESCORE -> ACCEPT. Any score
below 9.0 or any regression routes to repair; unrepairable => BLOCKED with a reason and
exactly one executable next action.

---

## SECTION 29. RECOVERY MODEL

Restart-safe idempotent transactions; canonical event store REPLAY/CONFLICT; anti-rewind
checkpoint; per-task rollback plans; `outbox` delivery state machine.

---

## SECTION 30. COLD-START PROTOCOL

Read boot chain -> load control plane (live HEAD) -> Hub Read-First gate (if Hub) -> canonical
source map -> current Activity -> Work Queue -> Progress Index -> identify authorized next
action. STATUS: PARTIAL (boot chain does not reference the loop; queue/index absent on this
branch).

---

## SECTION 31. WARM-START PROTOCOL

Restore last transaction + STATE + open blockers; verify exact revision; if proof/revision is
stale relative to live HEAD, mark STALE and do not promote.

---

## SECTION 32. SUCCESSOR-NAYA PROTOCOL

On completion emit: WHAT HAPPENED / PROVEN / FAILED / REPAIRED / UNKNOWN / MUST-NOT-TOUCH /
NEXT / WHY / EXACTLY HOW TO CONTINUE - machine-readable and human-readable. This audit's
handback (§ below, in chat) is an instance of this protocol.

---

## SECTION 33. CONTINUOUS EXECUTION PROTOCOL

SELECT -> EXECUTE -> VERIFY -> SCORE -> RECORD -> INSPECT QUEUE -> SELECT NEXT -> CONTINUE.
Halt on: authorized work complete; no legitimate high-value task; hard safety/governance
boundary; required authority genuinely unavailable; or unresolvable uncertainty. Never
fabricate permission; never infer authority.

---

## SECTION 34. MACHINE-READABLE STATE REQUIREMENTS

One current-state projection exposing: revision, branch, mission, current task, status, active
agents, blockers, recent verified accomplishments, defects, quality score, risk, protected
boundaries, last Activity event, next action, authority-required-if-any.

VERIFIED: `.naya/control-plane/STATE.json` implements most of this well (status LIVE_BOUND,
live HEAD resolution, known/unknown/failures/protected_boundaries/bottleneck/single_next_action/
next_actions/ready_to_run_execution/truth_rules). What is missing is linkage to the Work Queue
and Progress Index, and a single authoritative branch.

---

## SECTION 35. MACHINE-READABLE TASK REQUIREMENTS

The queue task schema (on wiz branch) satisfies this. It must be adopted on the canonical
branch and linked to each task's acceptance receipt.

---

## SECTION 36. MACHINE-READABLE EVIDENCE REQUIREMENTS

Each task declares required evidence; evidence binds an exact revision; the
VERIFICATION-RECEIPT-SCHEMA provides the envelope.

---

## SECTION 37. MACHINE-READABLE AUTHORITY REQUIREMENTS

Authority registry + per-task authority source/scope + governance-kernel resolution. Requires
removal of the duplicate kernel to be unambiguous.

---

## SECTION 38. ACCEPTANCE CRITERIA

Accepted iff: tests pass; independent verification passes; score >= 9.0; no regression;
protected paths untouched; Activity recorded; successor present; evidence bound to the exact
revision.

---

## SECTION 39. ADVERSARIAL TESTS

Cold-Naya 30-question test; queue fail-closed; supervisor refuses ungoverned execution;
auto-Activity (Property B); sub-9.0 blocked; regression rejected; no-legal-action clean stop;
exact-revision evidence binding; protected paths untouched; forged authority rejected;
duplicate-authority detection; two-worktree divergence detection (the test that would have
caught this audit's central finding).

---

## SECTION 40. MISSING CAPABILITIES

1. Canonical branch/worktree resolution (BLOCKS EVERYTHING).
2. Composed execution supervisor.
3. Per-task quality gate (16 dimensions).
4. Scored regression guard.
5. Automatic Activity writer.
6. Boot wiring of loop + queue + progress index.
7. One current-state projection linking STATE + queue + progress index.
8. Canonical release workflow actually present on the canonical branch.

---

## SECTION 41. DUPLICATE CAPABILITIES

VERIFIED duplicates:
1. Two `governance_kernel.py` files (control-plane, governance).
2. Two NAYA-ACTION schemas (`.naya/contracts/NAYA-ACTION-V1.schema.json`,
   `.naya/actions/NAYA_ACTION_V1.schema.json`).
3. Two governed-execution efforts in two worktrees.
4. Multiple overlapping orchestrators (`naya_power_kernel`, `naya_power_orchestrator`,
   `naya_power_live`, plus worktree-B supervisor effort).
5. Overlapping PIS builders referenced across docs vs runtime.
6. Multiple candidate release workflows.

---

## SECTION 42. CONTRADICTIONS (VERIFIED)

1. Two linked worktrees on divergent branches; active session branch is
   `naya/universal-execution-gate-v1`, not the branch holding the latest governed-execution
   work (`wiz/autonomous-hardening`).
2. On this branch, `git merge-base HEAD origin/main` returned empty; `origin/main` is not an
   ancestor of HEAD. HONEST READING: this may indicate genuinely unreconciled histories OR a
   partial fetch; it is at minimum a divergence that must be reconciled by human authority
   before any "current" claim is made. It is NOT safe to assert "unrelated histories" without
   a full fetch.
3. Control plane declares mission TORCH-59 (Hub baseline restoration) while two branches
   pursue execution-engine work.
4. `START-HERE.md` does not reference the continuous loop.
5. `.naya/state/` and `.naya/execution/` are empty of the queue/progress-index artifacts on
   this branch, so the boot path cannot find them.
6. No `.gitignore` in this worktree; `__pycache__` directories are untracked pollution.

---

## SECTION 43. DEPENDENCIES

Canonical branch resolution -> adopt queue + progress index on that branch -> dedupe
governance kernel and action schemas -> compose supervisor -> quality gate -> regression guard
-> automatic Activity -> boot wiring -> re-score -> one real end-to-end governed run.

---

## SECTION 44. IMPLEMENTATION SEQUENCE

PHASE 0 (HUMAN AUTHORITY - cannot be done by the machine):
 Decide the canonical branch/worktree; reconcile or retire the others; confirm the current
 mission (TORCH-59 vs execution-engine); decide what happens to uncommitted work.

PHASE 1 (AUTONOMOUS, additive, on the chosen branch):
 Adopt Work Queue + Progress Index; dedupe governance kernel and Action schemas; add a
 duplicate-authority detector and a worktree/branch divergence detector.

PHASE 2 (AUTONOMOUS):
 Compose the supervisor over EXISTING primitives; dry-run first; fail-closed; no second
 controller/kernel/event-store.

PHASE 3 (AUTONOMOUS):
 Per-task quality gate (16 dimensions) -> regression guard -> automatic Activity writing.

PHASE 4 (AUTONOMOUS):
 Boot wiring: START-HERE -> AI-OPERATING-FEED -> loop contract -> queue -> progress index.

PHASE 5 (AUTONOMOUS then HUMAN):
 Re-score the Progress Index at the reconciled HEAD; run one full governed transaction;
 advance autonomy L2 -> L3.

PHASE 6 (HUMAN-AUTHORITY-GATED):
 Hub/release work via the composed system, after D1 (runtime/release authority) and related
 decisions are authorized.

---

## SECTION 45. AUTONOMY MATURITY MODEL

L1 OBSERVE - proven. L2 RECOMMEND - mechanism exists. L3 EXECUTE - not composed. L4 VERIFY -
partial (OSCAR exists, not loop-integrated). L5 REPAIR - no. L6 CONTINUE - no. L7 COMPOUND -
no. L8 CONTINUOUS - no.

Credible current level: L2, with L1 proven. (The mission statement's claim of L3/L4 capability
is NOT supported by the repository in its current state: there is no consumer of the queue and
no composed transaction.)

---

## SECTION 46. METRICS / KPIs

Progress Index score by subsystem; accepted vs rejected ratio; mean accepted quality; defects
found/resolved; regressions; Human Clarification Rate and avoidable rate; tasks blocked by
authority vs by defect; cold-Naya question pass rate; time-to-first-authorized-action;
percentage of tasks with exact-revision evidence.

---

## SECTION 47. EXACT PATH: CURRENT REPO -> SELF-OPERATING SYSTEM

1. HUMAN: choose canonical branch/worktree; reconcile histories; confirm current mission.
2. MACHINE: place queue + progress index on the canonical branch; dedupe authorities.
3. MACHINE: compose supervisor over existing primitives (dry-run, fail-closed).
4. MACHINE: add quality gate + regression guard + automatic Activity.
5. MACHINE: wire the boot chain.
6. MACHINE: re-score at the reconciled HEAD; run one real governed transaction end-to-end.
7. MACHINE: hand back with a successor contract; advance to L3/L4.

---

## SECTION 48. EXACT PATH: SELF-OPERATING SYSTEM -> CONTINUOUSLY IMPROVING NAYANET

Run the Hub as the first real workload through the composed machine; obtain the remaining
human decisions (runtime/release authority, Cloudflare credential surface, PIS authority, 509
lane disposition); let the loop draft and execute Hub/intelligence tasks under governance;
measure every checkpoint; drive the Progress Index from its baseline toward 9.0, then 9.5,
then 10.0 with the loop doing the work and humans supplying only constitutional authority.

PROPOSED PERSISTENCE PATH: SUPERBRAIN/NAYA-POWER-SUPERBRAIN-OPERATING-SYSTEM-BLUEPRINT-V1.md
