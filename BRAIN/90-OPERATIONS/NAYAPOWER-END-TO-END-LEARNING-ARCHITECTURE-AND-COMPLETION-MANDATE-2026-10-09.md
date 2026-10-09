# NayaPOWER End-to-End Learning Architecture — Contract, Wiring Map, and Completion Mandate

**Status:** Architecture contract / implementation plan. This document is not a claim that the whole runtime is currently working.
**Authority:** Human Director retains consequential authority. No merge, deployment, production promotion, credential/permission change, or H13 grant is authorized by this document.
**North star:** Prove that a lesson changes future behavior and is reused by a cold successor.
**Truth rule:** `IMPLEMENTED ≠ VERIFIED`; `STORED ≠ LEARNED`; `URL EXISTS ≠ CAPTURE RECEIPT`; `CAPTURE RECEIPT ≠ LEARNING RECEIPT`; `UNKNOWN/BLOCKED ≠ PASS`.

## 1. Executive definition

NayaPOWER is not a pile of notes, a Supabase table, nine labels, or a URL generator. It is a governed intelligence pipeline that turns a human lesson into durable, attributable knowledge and then proves that the knowledge changes behavior in a future situation.

A **Smart Note / Intelligent Block (IB)** is the canonical intelligence object: it must preserve the human-distilled lesson, machine-usable meaning, provenance, applicability, authority/truth state, lifecycle, and links to its evidence. Human prose, machine-readable records, database rows, indexes, Hub cards, and Smart Links are representations or projections of that object; they must not become competing authorities.

A **Smart Link** is a receiver-bound URL identifying one specific persisted projection. It answers “where is the saved object?” It may be issued only after persistence is confirmed and the returned projection is independently read back and byte/hash checked against the intended object. It is a locator, not a learning certificate.

A **capture receipt** attests the exact capture/persistence transaction and binds the object identity, projection identity, content digest, provenance, and relevant event/lineage identifiers. A **learning receipt** is separate and can be issued only after a complete, independently verified behavioral loop closes.

Supabase is valuable only if it does real work beyond storing another copy: it must provide a governed, queryable, durable event/record boundary used by runtime retrieval, lineage, state transitions, and evidence. A row or database event alone does not mean that a model has understood or learned anything. GitHub is the reviewable source/projection and change-history surface; Supabase is the operational record/query surface. The system must define which record is canonical for each field and how parity is checked—never permit silent dual authority.

## 2. The complete user-visible path

When Shawn says **“make a Smart Note from this; I want the Smart Link”**, the expected behavior is:

1. **Receive the instruction.** Authenticate/identify the authorized receiver, preserve the original input and request context, and assign a trace/correlation ID. If authorization or required context is absent, stop with a precise blocked receipt.
2. **Distill meaning.** Produce (a) human-readable note, (b) machine-readable semantic record, and (c) an explicit relation map: who/what/why, affected actors (including child/grandma/Naya/machine when relevant), use conditions, expected benefit, risks, examples, and non-examples. Do not invent facts; mark unknowns.
3. **Validate before writing.** Check schema, identity uniqueness, provenance, consent/scope, truth state, lifecycle state, applicability, and duplicate/collision policy. A candidate is allowed to be saved as a candidate; it must not be silently treated as ratified knowledge.
4. **Persist transactionally/idempotently.** Write the canonical IB plus the required event/lineage/checkpoint data to the designated durable record system. Use an idempotency key so retries cannot create conflicting objects or duplicate learning effects. Define the consistency/compensation behavior if GitHub and Supabase cannot be updated atomically.
5. **Read back and verify bytes.** Independently retrieve the persisted object through the receiver/query path—not from the same in-memory request body. Compare canonicalized content digest, object ID, revision, scope, and provenance. A successful write response without read-back is insufficient.
6. **Issue the capture receipt.** Record requested and persisted IDs, digest, event/lineage IDs, receiver, timestamps, status, and verification method. Distinguish success, partial, retryable failure, and blocked. A receipt must not overclaim.
7. **Mint the Smart Link.** Only now return a receiver-bound URL to the exact saved projection, with access policy enforced. Verify the URL resolves to that object under the intended identity/scope. Do not make private content public merely to make a link work. If the link is gated, say so.
8. **Make it retrievable.** Index it by meaning, situation, tags, actors, applicability, time/version, authority, and lifecycle. Search must return the object with provenance and state, not a detached text fragment. Candidate notes may be retrievable for review but must not enter ratified decision context as active law.
9. **Run governed admission.** Independent verification evaluates the candidate against the applicable acceptance contract. Only an authorized admission policy may transition candidate truth/authority state to ratified/active. Keep `truth_state` and `lifecycle_state` semantically distinct. Never “fix” a retrieval failure by blindly relabeling a candidate ACTIVE. Record the decision, policy version, verifier identity, evidence, and reason. Rejected or blocked candidates remain inspectable with explicit status.
10. **Activate it at the point of use.** Before a relevant decision/action, ACT must query KNOW/retrieval for applicable active lessons and governing law. It must evaluate scope, freshness, precedence, conflicts, consent, and authority. The decision trace records which lessons were retrieved, which were applied/rejected, and why. No relevant lesson found is an explicit outcome, not an invisible fallback.
11. **Apply the lesson.** The agent produces an observable action or response under the lesson. The system records a baseline/expected behavior and the actual outcome. Merely retrieving, summarizing, or repeating the note is not application.
12. **Observe a behavior delta.** Compare behavior before/without the lesson against behavior with it under a controlled, preregistered scenario. Define the expected change, counterexamples, and pass/fail criteria before running. Prevent leakage from the lesson into the supposedly cold evaluator.
13. **Independently verify.** A verifier who did not implement the change evaluates the raw evidence and adversarial cases. The verifier checks that the behavior delta is caused by correct use of the lesson, not fixture leakage, hardcoding, a fallback path, or a stale pre-seeded ACTIVE fixture.
14. **Prove cold-successor reuse.** Start a new Naya/agent/session with no hidden transcript, no developer handoff containing the answer, and no fixture that preloads the lesson. It must retrieve the same canonical IB, explain its applicable meaning, apply it to a held-out but in-scope scenario, identify when it does not apply, and provide provenance.
15. **Issue the learning receipt.** Only after independent verification and cold-successor reuse pass may the system attest learning for that specific lesson/version and scenario set. The receipt references the capture receipt and Smart Link but has its own status and proof artifacts.
16. **Close the loop and compound.** Update the cognitive checkpoint / current intelligence projection and append the verified learning event. Later lessons may build on this lesson through explicit lineage. Preserve old versions, invalidations, and supersession; never erase the history needed to explain a decision.
17. **Report honestly.** Tell Shawn: what was saved; its Smart Link; capture receipt status; whether it is merely a candidate or admitted active knowledge; whether behavior changed; whether independent verification passed; whether a cold successor reused it; and the exact blockers. Never compress these distinct states into “learned.”

## 3. Smart Link vs. Supabase vs. learning

| Artifact / component | What it proves | What it does not prove |
|---|---|---|
| GitHub Smart Note projection | A reviewable representation exists at a revision | Runtime use, active memory, comprehension |
| Supabase row/event | A database record/event exists under the defined transaction semantics | That an agent consumed it or changed behavior |
| Smart Link | Where the exact saved projection is located, with intended access controls | That the object is valid, admitted, understood, or learned |
| Capture receipt | The identified content was persisted and independently read back/hash-checked | That it changed behavior |
| Retrieval trace | A runtime query returned a particular object/state | That the agent understood or correctly applied it |
| Admission receipt | A governed decision promoted/rejected/blocked a candidate under a named policy | That future behavior actually changed |
| Behavior verification receipt | The preregistered behavior criteria passed under independent review | That a cold successor can repeat the result |
| Learning receipt | Observed behavior change plus independent verification and cold-successor reuse for a defined scope/version | Universal competence outside the tested scope |

A Supabase trigger, webhook, database insert, or GitHub workflow may orchestrate the next step, but none of these alone is “learning.” Learning is a demonstrated, reproducible change in behavior supported by lineage and independent evidence.

## 4. The nine nodes: responsibility and required hand-offs

The nine nodes are not nine decorative labels and not nine isolated test suites. They are governed responsibilities in one execution path. The exact existing runtime implementation must be inspected before assigning a node as “wired”; this table defines the required contract.

| Node | Required responsibility | Required input → output / evidence |
|---|---|---|
| **SELF** | Establish agent identity, current checkpoint, capabilities, limits, and continuity context; integrate only authorized verified lessons into the current working model/checkpoint | Identity + checkpoint + verified intelligence → versioned self-state and provenance |
| **LAW** | Enforce authority, consent, privacy, precedence, truth/lifecycle rules, allowed transitions, and fail-closed behavior | Request + policy + candidate/active states → allow/deny/require-verification decision with policy/version/reason |
| **ACT** | Plan and perform the requested action; query memory before relevant decisions; apply/reject retrieved lessons explicitly | Request + LAW decision + KNOW results → action/decision trace naming applied intelligence |
| **KNOW** | Canonical retrieval and semantic/contextual indexing; resolve identity, version, scope, freshness, and lineage | Query/context → ranked eligible records plus excluded/conflicting records and reasons |
| **PROVE** | Build evidence/receipts that bind claim to exact inputs, outputs, bytes, code revision, and runtime | Stage outputs → verifiable evidence manifest with hashes and trace IDs |
| **CONNECT** | Move records/events between GitHub, Supabase, receiver, Hub, and agents without dropping identity, scope, or lineage | Typed event/object → acknowledged delivery and parity/transport receipt |
| **VERIFY** | Independently assess contract compliance, bytes, transitions, behavior delta, and adversarial/negative cases | Preregistered criteria + raw evidence → pass/fail/blocked verdict with reproducible basis |
| **LEARN** | Turn a verified candidate into governed, reusable intelligence; record what changed and why; create the learning receipt only when the loop closes | Candidate + admission decision + behavior evidence → versioned verified lesson/learning event |
| **EVOLVE** | Reuse verified intelligence in a cold successor; test held-out transfer, limitations, regression, and compounding | Active lesson + fresh successor + held-out scenario → successor reuse receipt and updated checkpoint/lineage |

### Mandatory edge contracts

Every edge must be implemented as an explicit typed hand-off, not an implied narrative:

- **SELF → LAW:** request identity, authority, scope, current checkpoint.
- **LAW → ACT:** permitted action and constraints; denial must stop execution.
- **ACT → KNOW:** context/situation query before the decision/action when memory could apply.
- **KNOW → ACT:** eligible lessons, versions, provenance, applicability, conflict/exclusion reasons.
- **ACT → PROVE:** actual action and decision trace, not just intended plan.
- **CONNECT → PROVE:** delivery acknowledgements and source/destination identities.
- **PROVE → VERIFY:** immutable evidence bundle and preregistered acceptance criteria.
- **VERIFY → LEARN:** independent verdict; only eligible PASS can advance the governed learning state.
- **LAW → LEARN:** allowed state-transition policy; no node may self-ratify outside authority.
- **LEARN → SELF:** verified intelligence/checkpoint update with lineage.
- **EVOLVE → KNOW/LEARN:** cold successor retrieval/reuse evidence feeding the next compounding cycle.

If current code does not implement one of these edges, record it as **MISSING**, not “conceptually covered.” If multiple nodes are implemented inside one process, separate conceptual ownership is still required through typed interfaces, trace spans, and tests.

## 5. Canonical object, states, events, and identity rules

### Object identity and versioning
- Each IB has one immutable stable identity and explicit content revision/version. Human projection, machine record, Supabase row, index entry, receipt, and Smart Link must point to that same identity/version.
- Enforce unique IDs and collision detection at the write boundary. Never silently overwrite or merge conflicting objects. Preserve both objects and stop promotion until the collision is resolved by authorized policy.
- A retry with the same idempotency key returns the same transaction/object outcome; it does not mint duplicate IDs or duplicate learning events.
- Store a canonical digest of the exact normalized payload and define normalization precisely (encoding, line endings, whitespace policy, field ordering). Hash the same representation at write and read-back boundaries.

### State dimensions are distinct
Do not conflate:
- **Truth/ratification state**: candidate, ratified, rejected, conflicted, unknown (use the repository's actual canonical enum after audit).
- **Lifecycle state**: active, superseded, archived, revoked (again, verify actual enum and definitions).
- **Execution state**: pending, running, succeeded, failed, blocked, retryable.
- **Evidence state**: absent, partial, verified, invalidated.
- **Access state**: private, gated, authorized, denied.

The exact enum set and transitions must be reconciled against schemas, code, fixtures, and production configuration before implementation. Never infer one dimension from another. A CANDIDATE is not automatically retired. A URL with gated access is not automatically broken. A test fixture marked ACTIVE must not make a candidate's admission path appear proven.

### Minimum event envelope
Every stage event must include: schema version; event ID; correlation/trace ID; idempotency key; IB ID and revision; source/destination; actor/agent identity; event type; timestamp; content digest; parent/causation event ID; policy/verifier version when applicable; outcome/status; evidence URI/IDs; and a structured failure reason when not successful.

Required event classes include capture requested, distilled, validation completed, persistence committed, read-back verified, capture receipt issued, Smart Link minted/resolved, retrieval attempted/result, admission evaluated/transitioned, lesson applied, behavior observed, independent verification completed, successor reuse completed, learning receipt issued, checkpoint updated, and invalidation/supersession recorded.

## 6. Supabase's job and its connection to GitHub

Supabase must be assessed against concrete operational responsibilities, not the claim “it's the official memory”:

1. Persist structured IB metadata and/or canonical operational records according to the repository's declared source-of-truth policy.
2. Persist append-only events/lineage and evidence references.
3. Support authorized retrieval by identity, semantic/context context, lifecycle, truth/authority, scope, and version.
4. Enforce access and row-level policy; private notes remain private.
5. Provide transaction/idempotency semantics and explicit error handling.
6. Trigger or enqueue downstream work only through durable, observable mechanisms; retries are safe and deduplicated.
7. Expose runtime health, queue age, failures, dead letters, and reconciliation/parity status.
8. Support independent read-back and audit without trusting the writer's in-memory response.

GitHub's role must also be explicit: reviewable source/projections, version history, policy/code changes, generated indexes, and durable developer evidence. A commit or markdown file does not imply Supabase ingestion. A Supabase row does not imply GitHub projection. A workflow success does not imply runtime deployment parity. Reconciliation must detect missing, stale, duplicate, or hash-mismatched projections and fail visibly.

**Required architecture decision:** identify field-by-field which store is authoritative (for example: authored source/policy in Git; operational event/transaction state in Supabase; derived indexes/projections generated from the canonical object). Document the exact conflict-resolution policy and one-way projection directions. No second brain or competing authority may be introduced.

## 7. Admission gate: the missing hallway must be proven, not assumed

The reported T11 failure indicates a cold-retrieval assertion expected lifecycle ACTIVE or SUPERSEDED but observed CANDIDATE, while the Receiver path appeared to assert ACTIVE without performing a governed candidate-admission transition. The admission filter reportedly exists on a separate branch. These are leads to verify against current main and actual runtime; they are not permission to wire it blindly.

The team must:
1. Locate the actual admission implementation, branch/commit, contract, tests, and owner; verify it is current and its 48/48 result reproduces from the exact commit.
2. Define the permitted transition and required evidence: independent verifier result, authority/policy version, scope/consent, collision-free identity, valid provenance, content digest, and explicit decision reason.
3. Insert the gate at the correct boundary between independent verification and active retrieval/learning consumption, preserving fail-closed semantics.
4. Keep candidate capture successful even when admission is blocked; report “captured, not admitted” instead of discarding the note or falsely claiming learning.
5. Resolve the reported SN-782 identifier/claim collision before promotion. Preserve both objects and lineage; do not overwrite, rename, or delete silently.
6. Test lawful candidate→active promotion; blocked promotion with missing evidence; rejected candidate; stale/wrong-repository receipt; digest mismatch; duplicate/collision; revoked/superseded lesson; and unauthorized caller.
7. Prove the actual Receiver → admission gate → retrieval path in CI and a protected live runtime test. A unit test or branch-ready statement is not proof of runtime wiring.

## 8. The engine: ACT must consume KNOW and LEARN must alter future behavior

Two separate links must be implemented and verified:

### A. ACT → KNOW → ACT (use at decision time)
- Before any action in a domain where a lesson may apply, ACT issues a context-rich query.
- KNOW returns eligible lessons with provenance, version, authority, scope, freshness, and confidence/limitations; it also reports excluded candidates and conflicts.
- LAW governs which returned records can influence action.
- ACT must record whether each relevant lesson was applied, rejected, or deemed irrelevant and why.
- Test with a unique synthetic lesson whose instruction is not present in base prompts, a relevant scenario, an irrelevant scenario, conflicting lessons, stale version, candidate state, and missing retrieval service. Missing KNOW must not silently masquerade as “no lesson exists.”
- The lesson's correct application must change an observable decision/action relative to the preregistered baseline.

### B. LEARN → SELF/checkpoint → cold successor (retain and compound)
- Only independently verified behavior changes can become a learning claim.
- Update the canonical current-intelligence/checkpoint projection with links to the source IB, evidence, verifier verdict, scope, and version.
- A cold successor must start without hidden access to the source conversation or builder-only context; its only route to the lesson is the governed retrieval path.
- The successor must retrieve, explain, apply to a held-out scenario, and state limitations/counterexamples.
- A repeat of the same answer embedded in a fixture, prompt, code branch, or handoff is leakage and invalidates the proof.
- Learning must survive a fresh process/session and the documented restart/reload boundary.
- A new lesson should be able to reference prior verified lessons through explicit lineage; regression and invalidation must propagate without erasing historical evidence.

## 9. Build before testing: integration inventory and dependency order

The instruction is **assemble the whole path first, then run staged verification**. Do not repeatedly launch end-to-end tests while required components or interfaces are known to be absent. Tests are still needed during development, but their role is to validate each built contract—not to substitute for architecture or wiring.

**Phase 0 — Source-of-truth audit**
- Freeze a SHA of current main and record environment/branch/commit for every finding.
- Read the actual node manifest/spec, kernel/runtime loader, receiver workflow, Smart Note schema/registry, index generator, Supabase migrations/functions/RLS, event/receipt contracts, admission branch, and existing learning tests.
- Produce a component/edge matrix with code path, owner, input/output schema, current status (PROVEN / IMPLEMENTED-UNVERIFIED / MISSING / BLOCKED / CONFLICTED), and evidence URL/hash.
- Resolve terminology and identity collisions. Do not build a parallel framework.

**Phase 1 — Contract and schema**
- Ratify one canonical event envelope, IB identity/version/digest rules, state enums/transitions, receipt types, error taxonomy, idempotency, privacy, and store-authority map.
- Define typed interfaces for all nine nodes and mandatory edge contracts.
- Add machine-enforced schema and transition validators. Unknown node/component classes and undocumented state transitions fail closed.

**Phase 2 — Persistence and capture**
- Complete receiver validation, durable writes, idempotency, independent read-back, byte/hash parity, capture receipt, Smart Link resolution, privacy/access, and reconciliation.
- Capture should return a useful partial-success status if later learning stages are blocked.

**Phase 3 — Index and admission**
- Complete meaning/context indexing and state-aware retrieval.
- Wire the governed admission gate and collision protection. Distinguish candidate visibility from eligible active knowledge.
- Ensure regeneration/index checks are deterministic on a clean checkout and do not require local uncommitted fixes.

**Phase 4 — Runtime use**
- Wire ACT→KNOW→ACT and LAW enforcement at the real decision point.
- Wire LEARN→SELF/checkpoint and the event/receipt chain.
- Add observability for each edge: trace IDs, stage outcomes, latency, retries, queue age, and failures.

**Phase 5 — Verification harness**
- Define a preregistered golden path and adversarial cases before running the final test suite.
- The harness must use a real captured candidate, real persistence, the real receiver, the real admission path, the real retrieval path, and the real successor runtime. No fallback-only success, pre-seeded ACTIVE fixture, mocked-out central edge, or same-process memory may satisfy end-to-end acceptance.
- Separate component tests, integration tests, live-runtime tests, behavior-delta tests, and cold-successor tests in the report.

**Phase 6 — Independent proof and ship decision**
- Naya 2 / independent verifier audits the evidence bundle against this contract and tries to falsify it.
- Builders cannot self-certify their own result.
- The Human Director decides any protected merge, deployment, H13 grant, or production promotion. A green CI run alone does not grant those authorities.

## 10. Required acceptance suite (positive and negative)

### Positive end-to-end golden path
1. Capture a new unique lesson that has never appeared in the model prompt, fixtures, or repo as a pre-seeded active lesson.
2. Verify canonical IB persisted in each declared authoritative system, with matching identity/version/digest and lineage.
3. Read back independently; verify capture receipt and Smart Link resolve to the exact private/gated projection.
4. Show the note's initial state explicitly (normally candidate pending governed admission).
5. Pass the independent admission gate and record the authorized state transition.
6. Query via the actual runtime retrieval path and show the candidate is now eligible under the defined policy.
7. Ask ACT to handle a preregistered in-scope scenario; record retrieval and application trace.
8. Compare baseline and treatment behavior; show the expected delta.
9. Have an independent verifier inspect raw traces and run adversarial checks.
10. Start a cold successor with no hidden context; require correct retrieval, explanation, held-out application, limitations, and provenance.
11. Issue separate capture and learning receipts; verify every referenced hash/ID.
12. Restart the runtime and repeat retrieval/reuse; prove durable retention.
13. Confirm no forbidden access, duplicate event, or unauthorized state transition occurred.

### Mandatory negative/adversarial cases
- Write response says success but read-back is absent or mismatched.
- Smart Link points to wrong IB/revision or cannot resolve under authorized scope.
- Private link is accessible to an unauthorized identity.
- Supabase write succeeds but GitHub projection fails, and vice versa; reconciliation/partial status is honest.
- Duplicate idempotency retry; duplicate IB ID; SN-782-like collision.
- Candidate incorrectly treated as retired, or candidate treated as active without admission.
- Missing verifier evidence; forged/stale/wrong-repository receipt; altered content digest.
- ACT skips KNOW; KNOW unavailable; empty result silently treated as proof of no memory.
- Conflicting, superseded, revoked, stale, or out-of-scope lesson.
- Builder leaks lesson into prompt/fixture/handoff; successor uses a hidden fallback.
- Behavior doesn't change; behavior changes in wrong direction; lesson is overgeneralized to an irrelevant scenario.
- Event replay, out-of-order delivery, duplicate trigger, retry exhaustion, dead-letter event.
- Restart loses checkpoint/retrieval or changes behavior without provenance.
- Undocumented component class, unknown schema version, unauthorized transition, and missing policy version.

Every negative case must assert both the correct failure outcome and the absence of forbidden side effects.

## 11. Evidence and receipt requirements

Every claimed stage needs a durable receipt with:
- Claim and status (PASS / FAIL / BLOCKED / UNKNOWN / CONFLICTED).
- Exact repo, branch, commit SHA, workflow/run/job, runtime/environment, and timestamp where applicable.
- Input/output IDs, object revision, digest, event/correlation/causation IDs.
- Exact command or reproducible action and exit status.
- Raw artifact/log links, verifier identity, criteria version, and known limitations.
- Whether evidence is unit, integration, live runtime, behavioral, or cold-successor evidence.
- For failure: first failing edge, observed vs expected, safe recovery, owner, and next action.

A Smart Link is included as a locator, never used as a substitute for the receipt. The capture receipt and learning receipt must be distinct objects with explicit cross-references.

## 12. Fourteen-agent operating contract

All fourteen agents operate under one shared architecture contract. Team leads divide implementation work, but no lead may redefine truth labels or bypass another team's interface.

- **Naya 1 — Proof / verification lead:** own independent evidence rubric, preregistration, adversarial suite, scorecard, and ship-readiness recommendation. Do not self-stamp builder work.
- **Naya 2 — Law / governance and independent audit:** own policy/authority semantics, truth-vs-lifecycle separation, admission transition contract, spec integrity, and independent review across teams.
- **Naya 3 — Interfaces / Hub and innovation:** ensure Hub displays distinct capture/admission/learning states and Smart Link semantics; no UI may present a saved note as “learned” without a learning receipt.
- **Naya 4 — Learning and architecture execution lead:** own full pipeline integration, receiver/admission wiring, ACT↔KNOW and LEARN↔SELF edges, end-to-end completion plan, and coordination of builders/testers. Her adoption word is not a substitute for proof or Human Director authority.
- **Naya 5 — Brain / memory and evolution:** own canonical IB, registry, indexing, durable checkpoint, retrieval, lineage, cold-successor continuity, and reuse.
- **All other agents (to be named from the current roster, not guessed):** take explicit bounded work packages assigned by a team lead, with one doer and a different tester; each reports exact paths, edge contract, commit, tests, evidence, unresolved risk, and next action. Do not invent missing agent names or infer owners from old notes.

### Work-package partition
A. Architecture/source audit + edge matrix (Naya 4 coordinates; Naya 2 checks law; Naya 1 verifies claims).
B. Capture/persistence/receipt/Smart Link + Supabase/GitHub reconciliation (engineering doer + independent tester).
C. Admission/state transition/collision policy (Naya 2 defines; Naya 4 wires; Naya 1 adversarially verifies).
D. KNOW indexing/retrieval + ACT consumption (Naya 5 memory/retrieval; Naya 4 runtime wiring; independent tester).
E. Behavior-delta and cold-successor harness (Naya 1 defines acceptance; Naya 5 builds continuity; Naya 4 integrates; independent verifier controls held-out cases).
F. Hub/report/Smart Link status UX (Naya 3).
G. Integration/observability/reconciliation/CI enforcement (Naya 4 coordinates engineering; Naya 1 verifies).
H. Whole-system audit and ship recommendation (Naya 2 independent audit with Naya 1 evidence; Human Director retains protected decision).

The current 14-agent roster and actual feed ownership must be fetched from the live repository/feed before assignments are finalized. Do not fabricate sign-ins or claim an agent accepted work without a recorded acknowledgement. Team leads must post sign-in, bounded assignment, doer/tester, evidence link, and sign-out in their own current team feeds; #1354 receives concise cross-team rollups.

## 13. Work discipline and reporting

Every team follows **OBSERVE → RANK → SIGN IN → ACT → VERIFY → SIGN OUT → SCORECARD → LEARN → REPEAT**.

- Produce → test → produce → test, but do not mistake isolated green tests for integrated proof.
- Each team lead reports hourly while active: measured score, what shipped, evidence, top three next actions, risks/blockers, and what Shawn can do to help.
- Use current main and current feed evidence; label historical facts as historical.
- No “merged,” “wired,” “live,” “learned,” “green,” or “10/10” without a direct receipt supporting that exact claim.
- Scores below 9.0 are not accepted as complete; 9.0–9.49 is minimum acceptable only when explicitly reported; 9.5+ is AAA target. A score moves only with measured evidence. A 7.5 honestly defended beats a wished-for 9.0.
- Fix the weakest proven edge first. Do not spend another round polishing secondary work while the end-to-end learning loop is blocked.
- Do not pause for Shawn to make routine decisions that the written policy has already decided. Do stop at actual protected authority boundaries.
- No merge, deployment, production promotion, credential/permission change, or H13 grant without the Human Director's explicit authorization.

## 14. Required deliverables before declaring the architecture assembled

1. **Canonical architecture report** — this contract reconciled against actual code, with every statement tagged verified/current, planned, missing, or conflicted.
2. **Runtime wiring map** — nine nodes and every required edge mapped to concrete files/functions/workflows/DB functions and actual call paths.
3. **Truth/state-transition matrix** — canonical enums, allowed transitions, owners, evidence prerequisites, and fail-closed behavior.
4. **Source-of-truth/data-flow map** — GitHub/Supabase/receiver/index/Hub directions, canonical fields, idempotency, retries, reconciliation, access policy.
5. **Gap ledger** — one row per missing/unverified edge, severity, owner, doer, independent tester, dependency, proof needed, current status.
6. **Runnable integration harness** — a genuine candidate flows through real persistence, admission, retrieval, behavior change, independent verification, and cold successor.
7. **Adversarial proof pack** — all mandatory negative cases with raw logs and no-side-effect assertions.
8. **Operator runbook** — how to run, observe, recover, reconcile, and safely retry; exact commands and environment requirements.
9. **Independent scorecard and ship decision** — each area scored from evidence, unresolved risks stated, no self-certification.
10. **Human Director brief** — plain-language explanation of what now works, what does not, what the evidence proves, and what protected decision is requested (if any).

## 15. Definition of done

The system is **not done** merely because the note saves, Supabase contains a row, a Smart Link returns, a PR merges, a workflow is green, or all nine node modules import.

The end-to-end learning loop is proven only when:
- one unique lesson is captured and durably persisted;
- its exact projection is independently read back and hash-verified;
- a Smart Link and capture receipt identify that exact object;
- admission is governed and evidenced;
- ACT retrieves the admitted lesson through the actual runtime path;
- ACT applies it and an observable, preregistered behavior delta occurs;
- an independent verifier passes both positive and adversarial cases;
- a cold successor with no hidden context retrieves and applies the lesson to a held-out case;
- the learning receipt binds all evidence and lineage;
- the lesson survives the defined restart boundary and remains correctly scoped;
- all negative cases fail closed with no forbidden side effects;
- CI and protected live-runtime proof refer to the exact current code and configuration;
- Naya 2 independently audits the evidence, and the Human Director retains the final protected ship decision.

Until then, report the exact furthest proven stage and first missing/broken edge. Never call the system “learning” merely because it is storing information.

## 16. Immediate next actions

1. Fetch current main SHA and the live team/agent roster; sign in to #1354 and the relevant team feeds.
2. Audit the actual current code against Sections 4–8; produce the evidence-linked wiring/gap matrix before changing code.
3. Verify the reported admission implementation/commit and the SN-782 collision against current main. Preserve all conflicting objects.
4. Assign bounded work packages to all fourteen agents through their real leaders/feeds; record doer, separate tester, dependencies, and acceptance proof.
5. Assemble missing edges in dependency order; run component tests during construction and the full golden path only when its prerequisites are present.
6. Have Naya 1/Naya 2 independently attack the integrated path and publish raw receipts.
7. Return to Shawn with a plain-language daily report and evidence links. Keep all protected changes unmerged/un-deployed unless explicitly authorized.

**Final law:** The purpose of the Smart Link is to locate the exact saved intelligence object. The purpose of the capture receipt is to prove that the exact object was persisted. The purpose of the nine-node governed runtime is to retrieve, evaluate, apply, verify, retain, and reuse that intelligence. The purpose of the learning receipt is to prove that the loop actually changed behavior and survived cold succession. These are connected stages—but they are not interchangeable claims.


---

## 17. Current-main source audit addendum — code facts vs integration gaps

**Audit basis:** repository `main` observed at `1d73652231ac6127806640af5a31eb516c60738d` on 2026-10-09. This is a source inspection, not a claim that current production deployment is byte-identical to this SHA. Re-fetch main and run the runtime-parity gate before treating it as current production truth.

This audit corrects a dangerous oversimplification: **the system is not merely a filing cabinet. Real capture, persistence, checkpoint, projection, and learning-verification machinery exists. The unresolved question is whether the exact user Smart Note object flows into the same governed learning/retrieval/cold-successor path, with identity and provenance intact.** The architecture must not be rebuilt from scratch or duplicate existing mechanisms.

### 17.1 Existing capture/receipt/Smart Link path — source-confirmed

Source: [`supabase/functions/v7-smart-note-canonical/index.ts`](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/1d73652231ac6127806640af5a31eb516c60738d/supabase/functions/v7-smart-note-canonical/index.ts)

The reviewed source shows this path:
1. Authenticates an actual Supabase user session; requires both human and Naya note views and an idempotency key.
2. Calls `v7_create_smart_note` to persist the capture envelope, machine view, Intelligent Block, evidence/receipt, and hub state. The receiver owns the canonical event and IB identity; repository code must not guess it.
3. Independently checks the persisted transaction response for canonical event, receipt, content digest, and lineage completeness.
4. Creates/reuses a `learning_evidence` record in `CANDIDATE` state, level `E1_UNDERSTANDS`, target `smart-note:<eventId>`. This is a learning candidate, not an earned learning result.
5. Persists a checkpoint through `nayanet_record_cognition_event`, binds it to the source Smart Note event, IB hash, receipt, and learning evidence, reads the checkpoint back, and verifies it is visible in the authenticated owner's Smart Feed.
6. Obtains a narrow, short-lived authority grant for the one repository projection.
7. Calls `nayanet-github-dispatch` for `project-canonical-smart-note.yml`. It accepts a canonical Smart Link only when the projection response says `ok=true`, `pipeline=PROJECTION_VERIFIED`, and returns a URL matching the exact `main/.../IB-######/smart-note.md` pattern.
8. If projection dispatch fails, the receiver intentionally preserves the successful capture and returns `SMART_NOTE_CAPTURED_PROJECTION_DEFERRED` / `PROJECTION_FAILED`, with a retry instruction. It does not manufacture a link.

**What this proves from source:** Supabase is doing real operational work—canonical write, idempotency/replay checks, learning-candidate creation, checkpoint persistence, feed verification, authority-scoped projection dispatch, and receipt assembly. The Smart Link is the final generated human projection URL, not a Supabase URL, PR URL, workflow URL, or raw capture-envelope URL.

**What it does not prove by source inspection alone:** that the currently deployed function matches this code; that every production request succeeded; that the generated projection was used by ACT; or that the lesson changed behavior in a cold successor.

### 17.2 The learning-verification machinery exists — but its input contract differs

Source: [`supabase/functions/nayanet-learning-verify/index.ts`](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/1d73652231ac6127806640af5a31eb516c60738d/supabase/functions/nayanet-learning-verify/index.ts), plus the current-main reconciliation document [`RECONCILIATION-ai1-seam.md`](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/1d73652231ac6127806640af5a31eb516c60738d/RECONCILIATION-ai1-seam.md).

The reviewed verifier has a real `candidate` mode and `verify` mode. Candidate mode revalidates an Event → Intelligent Block → Lineage → Relationship → Index → Checkpoint chain, checks source receipts and provenance, and creates/repairs a `learning_evidence` candidate. Verify mode validates evidence references, requires a well-formed causal-verification ID, evaluates the LAW lock-in boundary before mutations, and then performs governed learning-state changes. The source explicitly says this is the governed candidate-promotion path; `LEARNED` is not to be manufactured for convenience.

**Important input-contract seam requiring direct integration proof:**
- The Smart Note receiver creates its source event in `smart_note_events` (the receiver's comments explicitly distinguish this from `nayanet_cognition_events`), then separately creates a cognition/checkpoint event.
- The learning verifier's candidate mode, as reviewed, looks up its source event in `nayanet_cognition_events` by event ID plus receipt ID, and expects the surrounding block/lineage/relationship/index/checkpoint records in the `nayanet_intelligent_blocks` / related schema.
- The receiver-created candidate is keyed to `target_id="smart-note:" + eventId`; the verifier's candidate path creates node learning against `target_id="NAYA-NODE-0001"`.
- The Smart Note receiver's own checkpoint metadata says future applicability, behavior change, and outcome verification remain open.

These differences may be intentional boundaries between two flows, but **the reviewed source does not by itself establish a complete adapter from the receiver's exact Smart Note transaction to the verifier's exact candidate input contract**. Treat this as a highest-priority integration question, not as proof that no admission machinery exists. The team must show either (a) a durable, explicit, tested mapping that preserves source identity/receipt/digest and semantics, or (b) implement the smallest canonical adapter. Do not duplicate the learning verifier or silently change IDs/states to make it pass.

### 17.3 Current cold-runtime proof is valuable but bounded

Sources:
- [`supabase/functions/nayanet-cold-runtime-proof/index.ts`](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/1d73652231ac6127806640af5a31eb516c60738d/supabase/functions/nayanet-cold-runtime-proof/index.ts)
- [`tests/test_cold_successor_continuity.py`](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/1d73652231ac6127806640af5a31eb516c60738d/tests/test_cold_successor_continuity.py)
- [`tools/verify_nine_node_independent.py`](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/1d73652231ac6127806640af5a31eb516c60738d/tools/verify_nine_node_independent.py)
- [`.github/workflows/live-supabase-runtime-proof.yml`](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/1d73652231ac6127806640af5a31eb516c60738d/.github/workflows/live-supabase-runtime-proof.yml)

There is an actual OIDC-bound live runtime proof path and a cold-successor test that forbids handing the lesson directly to the successor, recomputes behavior from retrieved state, verifies a distinct successor identity, and proves authority is not inherited. The independent verifier requires a multi-part bundle (executor, cold, graph, graph verification, promotion, reread, evolve), checks source-revision consistency, distinct executor/verifier identities, and reconstructs control/treatment behavior from raw persisted receipts.

**Scope limit:** the currently inspected cold-runtime code uses a fixed canonical node lesson / fixed task registry. This proves the specific fixture/lesson and the specific non-inheritance behavior it exercises. It does not automatically prove that an arbitrary newly captured Smart Note from `v7-smart-note-canonical` reaches that exact path and is learned/reused. The live workflow must be traced to determine whether its fresh producer artifact is the same IB and learning ID consumed by every later stage, not merely a separate fixture.

### 17.4 Source-backed status table at the audit basis

| Capability | Source-level status | What remains to prove |
|---|---|---|
| Authenticated Smart Note capture | IMPLEMENTED in `v7-smart-note-canonical` | Exact live deployed revision + fresh invocation evidence |
| Canonical event/IB/receipt creation | IMPLEMENTED via `v7_create_smart_note` contract | Independent read-back against exact returned IDs/hashes in live run |
| Learning candidate creation | IMPLEMENTED; initial state CANDIDATE | Candidate identity is the same object the governed verifier later consumes |
| Checkpoint + authenticated Feed verification | IMPLEMENTED in receiver source | Current live parity and same-object lineage through downstream learning |
| GitHub human projection + canonical Smart Link | IMPLEMENTED as a guarded dispatch; can be deferred/fail | Successful exact Smart Link receipt for the fresh capture and byte/projection identity match |
| Candidate revalidation / governed promotion | IMPLEMENTED in `nayanet-learning-verify` | Adapter/contract compatibility with receiver-created Smart Note candidate and source event |
| ACT/KNOW runtime use | A bounded KNOW/selector and cold-runtime path exist in source | Fresh user Smart Note is retrieved through the actual decision-time path; no fixed fixture/fallback |
| Behavioral influence | Control/treatment harness and independent verifier exist | Exact fresh Smart Note causes the preregistered held-out behavior delta |
| Cold successor | Cold-successor path and regression guards exist | Same fresh Smart Note identity flows into successor; no prompt/fixture/handoff leakage |
| Compounding/evolution | Evolution evidence fields and verifier bundle exist | Same-run, same-revision, same-lineage evidence from fresh capture through later successor |
| Production parity | Separate parity gate exists in live workflow | Current `main` equals deployed function/config and the same run proves it |

### 17.5 The most likely seam to resolve first

Do not start by rewriting the nine nodes or adding another event bus. Trace one fresh Smart Note end to end across these exact boundaries:

`v7-smart-note-canonical`
→ `v7_create_smart_note` transaction result
→ canonical IB/event/receipt/checkpoint IDs
→ receiver-created `learning_evidence` candidate
→ projection workflow and Smart Link
→ `nayanet-learning-verify` candidate mode
→ `nayanet-learning-verify` verify/promotion mode
→ KNOW selector / cold-runtime query
→ ACT control/treatment task
→ independent verifier
→ cold successor
→ evolve/checkpoint receipt.

At each arrow, assert equality of the canonical IB ID, source event ID, learning ID, content digest, checkpoint/lineage references, source SHA, and run correlation ID where that field is applicable. Where schemas legitimately differ, document the explicit mapping and test it. If the candidate cannot pass from the receiver to the verifier because it belongs to a different target/event schema, that is the actual broken connector to repair.

The first deliverable from engineering is **not another green unit test**: it is a trace table for one fresh capture with every input/output identity, the exact function/workflow/SQL operation, the current state, and the first mismatch or missing edge. Only after that table closes should the team run the complete fresh-note golden path.

### 17.6 Protected authority note

The learning verifier's source explicitly guards lock-in mutations behind LAW authorization and accepts only an authorized in-scope grant or a valid, applicable scorecard receipt under its implemented contract. Do not bypass this by editing database rows or forging evidence. This mandate grants no H13 authority and no deployment/merge permission. If lawful promotion is blocked by missing authority, record BLOCKED and continue all non-mutating architecture, schema, harness, and negative-path work; request the protected decision only when the evidence makes it concrete.

### 17.7 Correction to earlier conversational shorthand

The statement “Supabase is just a filing cabinet and nothing wakes up” is too broad for current source. The receiver does orchestrate durable capture, candidate creation, checkpointing, Feed verification, and projection dispatch. The accurate unresolved claim is narrower and more important:

**We have several real pipeline components. We must prove they are one identity-preserving, policy-governed behavioral learning loop for the same freshly captured Smart Note.**

That is the integration bar.


## 18. Live backend + entrypoint audit — the actual disconnect

**Read-only live inspection performed 2026-10-09** against Supabase project `dahisasgpfvziswqvmvm`. No rows were mutated, no capture was invoked, and no deployment was performed.

### 18.1 The previously reported “ghost table” is not a current confirmed absence

A read-only live schema query confirmed that all of these tables currently resolve in `public`: `v7_smart_note_transactions`, `smart_note_events`, `nayanet_intelligent_blocks`, `nayanet_cognition_events`, `nayanet_intelligence_lineage`, `nayanet_brain_relationships`, `nayanet_intelligence_index`, `learning_evidence`, `nayanet_project_cognition_state`, `nayanet_execution_receipts`, and `nayanet_github_dispatch_receipts`.

Therefore the old SN-0520 claim that `v7_smart_note_transactions` does not exist is **historical evidence, not current ground truth**. Do not reopen it as a live table-absence defect without a new failing query. The table exists now. The current dispatch code and deployed dispatch both query it.

### 18.2 Current deployed function/source parity observations

The live Edge Function inventory reported:
- `v7-smart-note-canonical`: ACTIVE, version 19, updated 2026-10-07. Its deployed `index.ts` was byte-equivalent to the current `main` source after normalizing the BOM/newline/trailing-file boundary.
- `nayanet-github-dispatch`: ACTIVE, version 36, updated 2026-10-09. Its deployed source differs from current `main` (deployed source has additional sanitized GitHub failure detail around commit errors). It still references `v7_smart_note_transactions`, which exists in the live schema. This is a **source/deployment drift to reconcile**, not evidence that the table is absent.
- `nayanet-learning-verify`: ACTIVE, version 98, updated 2026-10-08. The deployed source differs from current `main`; notably, the current-main source imports and uses `resolveScorecardReceiptAuthority`, while the deployed source inspected does not. The operational impact must be tested against the actual intended authority contract. Do not assume the main change is live.
- `nayanet-cold-runtime-proof`: ACTIVE, version 130, updated 2026-10-08. Its deployed source matched current-main source after substituting its intentional deployment stamp `00f50bb32c1c7fadfbe5cd03d0319646ab9dc0e9` for the source placeholder `UNSTAMPED`. This is consistent with a stamped deployment of that code body.

These observations are time-bound. Recheck versions/hashes before any ship decision. They do not authorize a deployment.

### 18.3 Two real entrypoints currently serve different paths

**Path A — governed agent capture / returned Smart Link**
- `.github/workflows/nayanet-agent-capture.yml` accepts a workflow-dispatch payload, signs in as the dedicated `naya-runtime` Supabase auth user using repository-held credentials, and invokes the unchanged `v7-smart-note-canonical` with a real user JWT.
- The receiver performs canonical persistence, candidate creation, checkpoint/feed verification, and calls `nayanet-github-dispatch`.
- The agent-capture workflow validates the returned `IB-######` and Smart Link and prints a structured capture receipt plus the link in its logs.
- The receiver/dispatch path is responsible for producing the direct GitHub `smart-note.md` URL.

**Path B — Git capture commit / behavioral proof workflow**
- `.github/workflows/live-intelligence-commit-proof.yml` discovers changed `.naya/capture/*.json` files, canonicalizes and hashes their intelligence payload, then calls `nayanet-intelligence-commit-runtime` (or verifies/reconciles an existing registry object).
- It records exact event/IB/lineage/relationship/index/checkpoint/receipt IDs and leaves the fresh block in CANDIDATE state.
- `.github/workflows/live-supabase-runtime-proof.yml` is triggered by completion of **Live Intelligence Commit Proof** (or by an explicit workflow dispatch). It consumes the producer run's fresh-lineage artifact, invokes `nayanet-learning-verify` candidate mode, runs a control/treatment causal experiment, independent verification, learning promotion, graph control/treatment, and active-learning generalization/cold-successor stages.

These are both real paths in source. They may be useful front doors for different callers, but they must not silently become two competing canonical memory/learning systems.

### 18.4 Confirmed orchestration gap: Smart Link capture is not shown triggering the learning proof chain

The reviewed `nayanet-agent-capture.yml` finishes after invoking the canonical receiver, validating the returned Smart Link/IB identity, and printing the capture receipt. It does not itself dispatch `Live Intelligence Commit Proof` or `Live Supabase Runtime Proof`. The latter workflow is wired to `workflow_run` from `Live Intelligence Commit Proof`, not from `NayaNET Agent Capture`.

Therefore, **the source does not currently demonstrate that a successful “Smart Note this” transaction through the agent-capture/Smart-Link route automatically continues into the same behavioral learning and cold-successor proof path.** The file-capture proof path does continue into learning proof, but that alone does not prove that it is the same canonical transaction as the Smart Link route.

This is the key root-to-top question the implementation team must resolve:
- Either make one canonical route the orchestrator and have all supported entrypoints call it with the same canonical identity, idempotency semantics, and receipts; or
- explicitly bridge the receiver's returned transaction/IB/event/learning IDs into the existing downstream learning workflow, with a durable hand-off/outbox and idempotent retries.

Do not solve this by creating a second memory or learning system, by re-capturing the lesson into a different IB, or by treating two semantically similar notes as the same object.

### 18.5 Required next engineering artifact — one end-to-end transaction trace

For a single fresh Smart Note, trace the route actually used by the human/agent command:
1. Input command and caller identity.
2. Capture envelope/payload hash and idempotency key.
3. Receiver transaction ID, canonical event ID, IB ID, IB content hash, capture receipt ID, learning candidate ID and target/state.
4. Checkpoint ID + checkpoint receipt and authenticated feed verification.
5. Smart Link projection dispatch receipt, resolved URL, repository path, projected file hash, and proof the URL opens the exact IB revision.
6. Downstream learning-verification request: exact input IDs and whether the verifier reads this same event/IB/candidate without re-capture.
7. Admission result and lawful authority receipt (or explicit BLOCKED status).
8. KNOW query and returned record IDs/state/applicability.
9. ACT treatment/control inputs and outcomes.
10. Independent verifier identity, raw persisted receipts, source/deployment revision.
11. Cold-successor retrieval/use, held-out result, unrelated-case refusal, and no inherited authority.
12. Learning receipt and updated checkpoint/lineage, with the same canonical IB and trace ID throughout.

Every boundary needs a test that deliberately substitutes the wrong IB/event/receipt/hash and proves the next stage refuses it. A successful receipt must be bound to the same transaction—not merely to a lesson with similar text.

### 18.6 Immediate priority order, updated by evidence

1. **Map and connect the two entrypoints without duplicate intelligence.** The exact fresh Smart Note from Path A must either flow into the downstream verifier/learning workflow or Path B must be formally selected as the only route and the Smart Link path made a projection of that same canonical object.
2. **Reconcile live/deployed source drift.** In particular, compare `nayanet-learning-verify` deployed v98 to current-main source and determine whether the scorecard-receipt authority bridge is intended and present in production. Do not deploy without authorization.
3. **Close the human return path.** Verify the invoking Naya/Hub/conversation receives the exact `smart_link` and capture receipt, not only that the URL is printed in a workflow log.
4. **Run the full proof on that same fresh object.** Use the existing candidate/admission, causal control/treatment, independent verifier, graph, generalization, and cold-successor machinery rather than creating another harness.
5. **Only then** make a protected ship recommendation with exact runtime parity, all receipts, risks, and authority state.

This is a more precise diagnosis than “nothing is wired”: substantial components exist, but the single transaction's hand-off from capture/Smart Link to the behavioral learning proof has not yet been established by the reviewed orchestration source.
