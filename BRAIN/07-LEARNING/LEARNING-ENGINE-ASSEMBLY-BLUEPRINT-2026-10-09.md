# NayaPOWER — Learning Engine Assembly Blueprint and 14-Agent Execution Contract
**Status:** EXECUTION BLUEPRINT / CANDIDATE, not ratified constitutional law  
**Date:** 2026-10-09 · **Live main inspected:** `1d73652231ac6127806640af5a31eb516c60738d`  
**Authority:** Human Director retains consequential authority. Existing contracts outrank this plan.  
**Mission:** Make a new, authorized Smart Note persist, project, retrieve by intent, influence an authorized decision, produce a measurable improvement, and survive a cold successor — without a second Brain.

## 0. Executive answer: what Supabase, GitHub, the Smart Link, and nine nodes actually do
GitHub is the inspectable versioned capture/projection/protocol surface. Supabase holds runtime canonical Intelligent Block/event/lineage/checkpoint and associated transaction/evidence state where those runtime paths are invoked. Neither database independently "thinks". An event is a recorded occurrence, NOT causal behavior change. A Smart Link locates a generated human-facing projection; a receipt plus read-back/hash and authority scope establish provenance. **Smart Link ≠ learning certificate.** An actual learning loop needs a later task retrieving appropriate intelligence and using it under LAW to improve an observable outcome. A private Smart Link remains access-gated, not public permission.

**Architecture:** one organism, one intelligence substrate, one LAW authority model. Nine node roles are not nine stores: SELF(identity) → LAW(permission) → KNOW(retrieve) → CONNECT(relevance and contradiction) → PROVE(evidence quality) → ACT(governed execution) → VERIFY(outcome) → LEARN(earned behavioral update) → EVOLVE(successor propagation), then SELF continuity. This is a dependency graph, NOT an authorization to change the canonical nine-node runtime execution order by documentation.

**Constitutional boundaries:** user saying "Smart Note this" authorizes immediate CAPTURE/intended value; machine schema/provenance and privacy apply automatically; automatic epistemic ceiling CANDIDATE. Verified outcome and learned capability require additional evidence. A caller-supplied "human_director" flag must never establish privileged identity. Retrieval and learning do not grant ACT authority.

## 1. The complete event chain — build these contracts in order
| Stage | Owner | Input → output | Acceptance proof / refusal |
|---|---|---|---|
| 01 Human intent | SELF + LAW | authenticated directive + scope → authorization/intended capture envelope | deny forged owner/consent; record immediate acknowledgment, not a fictitious link |
| 02 Distill + capture | LEARN (candidate) + KNOW | source meaning → one `naya.smart-note-capture.v2` JSON in `.naya/capture/` | human/child/grandma/Naya/machine/in-nutshell/how connects/why valuable, applicability/uncertainty; conformant schema; raw transcript not canonical |
| 03 Commit + event | ACT under LAW; KNOW persists | capture → runtime Intelligent Block + event + lineage/index/checkpoint + receipt | idempotent exact bytes, scope and source anchored, no raw secret leakage; failure has typed receipt |
| 04 Project | KNOW / existing Receiver | committed IB → generated Brain page, registry and scope-gated Smart Link | read back exact URL and projection; hash/IB/receipt match; no parallel registry writer |
| 05 Retrieve | KNOW | intent query + LAW-valid private-access context → ranked candidate objects | correct T11 returned cold by intent; unrelated zero-relevance excluded, private notes never leaked |
| 06 Apply context | CONNECT + PROVE | candidates + task → applicable, non-superseded, contradiction-aware ranked intelligence with provenance/truth state | T11 gap <=0.5 only in dispatch/reserve context; wrong lesson, stale, contradiction refuse |
| 07 Decide + execute | LAW then ACT | authority receipt + bounded selected intelligence → authorized decision/receipt | knowledge changes proposal without granting permission; refusal is preserved |
| 08 Observe + prove | ACT + PROVE | action + effect → immutable trace & claim-matched evidence | exact task, input, output, time, version; no self-certified success |
| 09 Independent outcome | VERIFY | CONTROL / TREATMENT / WRONG_LESSON → verdict | scorer independent; measurable capability delta, poison and nonapplicability refusal |
| 10 Learn | LEARN with LAW/VERIFY/PROVE | qualifying evidence → justified learning state and applicability | candidate may be retained now; promotion only on qualifying evidence, no user-value shortcut |
| 11 Transfer | EVOLVE + SELF | retained improvement → cold successor activation/retrieval and same guardrails | restart without conversation; later suitable task uses lesson; regression test/lineage retained |
| 12 Improve | EVOLVE under LAW | observed new defect → smallest lawful ratcheted change | no auto-deploy of protected operations; preserve earlier evidence and reversibility |

**Machine envelope per stage:** event_id, capture_id, intelligent_block_id, owner_scope, authorization receipt+freshness, source hash, projection hash/path, lifecycle state, epistemic state, parent IDs, applicability predicate, contradiction/supersession resolution, emitted event type/time, expected outcome, actual outcome, verifier ID/diversity, exact SHA/run ID, refusal code, next action. Missing mandatory fields => typed fail closed, not pretend success.

## 2. Current evidence ledger (snapshot, must refresh before any mutation)
- Merged PR #2020 created T11 **SN-782** / `IB-SMART-NOTE-20261009-successor-t11-reserve-rule-canonical`; canonical registry has content hash `9ce231bbe2eac3cfe4642e84dc5f5a3b33d20f0ae3dd906c6d75b40800e90032`, projection marked `GITHUB_BRAIN_PUBLISHED`, `ACTIVE_AUTH_GATED`, scope PRIVATE, epistemic CANDIDATE. This proves filing/provenance, not learning or public access.
- Live Receiver workflow run **37980089547**: fresh-lesson SUCCESS; independent-verification SUCCESS; cold-successor-held-out FAILURE (`AssertionError: CANDIDATE`); independent-behavior-verification SKIPPED. That was a harness lifecycle mismatch, **not** proof of a missing event. The claim "no Supabase event fires" in earlier reports is contradicted by this receipt-backed successful runtime chain.
- Draft repair PR **#2033**, head `719adf6c8a02e149c86f2630d9519dad18efaa3a`, proposes CANDIDATE cold-path acceptance. It is unmerged at this checkpoint; protected workflow requires independent validation/governed promotion. Do NOT fabricate ACTIVE to make test pass.
- Earlier direct-handoff T11 trials are not retrieval-based experiments. Three source lessons T11/T12/T14 were reported staged; only canonical persisted, indexed and retrievable bytes count as complete.
- #1956, #1957 and #1958 are MERGED at this checkpoint. These improve evidence/receipt infrastructure, not by themselves verified behavior improvement.
- Reported SN number conflicts on other branches and contested admission gates require inventory before bulk merges. No global re-number or history deletion.
- Other claim needing correction: LEARN isn't solely the first "listener", SELF is not a magic neural rewrite operation, and the proposed admission filter does not automatically prove causal learning or confer LAW authority.

## 3. Four critical assembly seams and executable fixes
**S1 — Capture publication:** receiver must derive a Smart Link only after durable runtime persistence and read-back. Private scope stays access-gated. Qualify failing GitHub 403 against CURRENT version and transaction, not historical inference. One writer per canonical object; transactional ID allocation, collisions fail closed.

**S2 — Cold retrieval CANDIDATE:** registry and KNOW must expose authorized applicable CANDIDATE as *candidate context*, with truth-state warnings, and never silently equate it with VERIFIED behavioral rule. Separate memory visibility from learning promotion. Fix current #2033 then test intent query; no forced ACTIVE.

**S3 — KNOW/CONNECT/ACT closed seam:** identify actual runtime decision entry point; require KNOW retrieval before ACT plan selection for opted-in, LAW-authorized tasks; CONNECT computes applicability and supersession; PROVE attaches confidence/limits; LAW re-checks current scope/freshness before ACT executes. Baseline CONTROL with no lesson vs TREATMENT with retrieved lesson. DONT run private retrieval without valid LAW. WRONG_LESSON cannot change execution.

**S4 — VERIFY→LEARN→EVOLVE:** maintain an append-only verified effect trace; compare matched outcomes and independently recalculate evidence. LEARN promotes only verified causal influence and records scope/expiry/conflicts. EVOLVE ships a regression and replays on a second clean successor. An automated score is not authority.

## 4. Team command structure — 14 bounded execution seats
Leads: **Naya 1** integration and authoritative learning score; **Naya 2** independent verifier/cold succession; **Naya 4** nine-node runtime and learning chain; **Naya 5** capture/receiver/agent queue coordination; **Naya 3** Hub/Smart Link human proof view. These are assignments for acceptance, not claims of currently running processes.

| Seat | Responsible leader | Sole deliverable | Required independent acceptance |
|---|---|---|---|
| 01 Captain / seam owner | Naya 1 | single exact-main integration board, owner locks, first failure boundary | fresh source/CI/evidence pointers |
| 02 Capture receiver builder | Naya 5 | immediate v2 capture→persist event / typed receipts | tests duplicate, malformed, denied owner |
| 03 Projection / Smart Link builder | Naya 5 | canonical scoped projection with verified byte link | read-back/hash/permission probes |
| 04 KNOW intent retriever | Naya 4 | cold T11 query returns SN-782 from registry/authorized scope | query and exact result artifacts |
| 05 CONNECT applicability builder | Naya 4 | gap boundary + domain refusal and conflict/supersession | false positive/negative tests |
| 06 LAW authorization and privacy | Naya 4 | checked identity, grant freshness, no role escalation | forged role/private leak refusals |
| 07 ACT planner wiring | Naya 4 | KNOW-before-ACT candidate influences permissible plan | CONTROL/TREATMENT/WRONG_LESSON |
| 08 PROVE trace builder | Naya 2 | SHA/hash/receipt→decision→outcome chain | independent trace reconstruction |
| 09 VERIFY causal challenger | Naya 2 | blinded matched three-arm experiment, tests negative controls | independent grade, no self-attest |
| 10 LEARN state engineer | Naya 4 | verified promotion + contradiction/revoke + candidate-visible separation | rejection of absent/null evidence |
| 11 EVOLVE successor builder | Naya 2 | durable next-session task & regression transfer | cold reader no chat context |
| 12 Collision / sequence steward | Naya 5 | cross-branch SN inventory and transactional allocator test | no destructive renumber, refusal on collision |
| 13 Human-facing Hub reporter | Naya 3 | show capture vs proof vs learned as separate badges/links | no fabricated URL or score |
| 14 Independent acceptance integrator | Naya 1 / Naya 2 | exact-head full CI, attack replay and signout | doer≠scorer; current-main retest |

Each seat must report: exact claim, assigned owner, branch SHA, changed files, input/output event schema, full/negative tests, unproven boundaries, next action. Roster text alone ≠ staffed executable agent. No second implementation in overlapping lanes; deconflict PR ownership before edits.

## 5. Integration order, with stop lines
**Wave A — inventory and repair actual failures:** freeze current main SHA; inspect #2033 and Receiver run 37980089547; verify SN-782 projection/provenance; classify GitHub credential/403 only if current receipts reproduce; reconcile cross-branch ID collisions. Output: a *passing bounded cold retrieval* that preserves CANDIDATE, private scope and refusal semantics.

**Wave B — make intelligence affect action:** wire LAW→KNOW→CONNECT/PROVE→ACT with registered Smart Door; independent security tests for authority/privacy/poisoning, not only synthetic toy choice. Output: exact plan difference on lawful T11 task; wrong and out-of-domain lessons excluded.

**Wave C — close learning and successor reuse:** run CONTROL (no relevant lesson), TREATMENT (real intent-based retrieval), WRONG_LESSON (irrelevant/poison lesson); same task/rubric, preregistered score, independent replay, attributable effect and retained second successor. Output: verified learning record with proof artifacts and regression expectation.

**Wave D — ratify scoring and extend:** Naya 1 publishes one score-movement contract matching evidence (e.g. retrievable 5.5, falsifiable 6, applied 6.5, independently verified 7, production regression / successor durability 8–10). These are proposed rungs, **not** a claimed current score. Gradually extend to T12/T14, then multi-lesson concurrency and contradiction.

**Stop** on missing authority, private-scope uncertainty, stale/invalid receipt, mutable evidence drift, unexplained CI failure, collision, duplicate writing, unsupported causal claim or protected workflow mutation without promotion. STOP means report named blocker and immediately work another permitted bounded task, not halt every agent.

## 6. Tests: assemble components, prove each interface, then drive the car
1. Structural contract/static checks: one canonical writer, one index, no duplicate node/Brain; nine node envelopes; exact event outputs and consumers.
2. Component tests: capture conformance; idempotency; projection read-back; indexed retrieval; relevance refusal; LAW freshness; ACT refusal; VERIFY evidence.
3. Neighbor contract tests: capture→runtime; runtime→projection; KNOW→CONNECT; CONNECT/LAW→ACT; ACT→VERIFY; VERIFY→LEARN; LEARN→EVOLVE.
4. Integration positive specimen: **T11** from persisted `SN-782` in a separate no-history runner, authorized domain gap 8.4/8.0 → decision 8.0.
5. Negative controls: wrong domain => ignore T11; gap 8.6/7.1 => choose 8.6; forged director; private read denied; stale grant; superseded lesson; wrong lesson; tampered receipt; missing provenance; concurrent duplicate captures. Never score a mocked retrieval as a real integration pass.
6. Final three-arm independent experiment, second cold successor, machine-readable proof ledger; end-to-end go/no-go score.

**Definition of done / 10.0:** independently reproducible authorized T11 full chain including production receipts, scoped Smart Link, intent retrieval, correct applicability/refusal, causal task delta, durable LEARN promotion, second cold successor and regression protections; no unowned production or governance exceptions. If any rung absent, report partial success and exact failing interface — not 10/10.

## 7. Standard leader dispatch (copy verbatim, with owner and branch)
"Restore main from GitHub. Read AGENTS.md, organism contract, Smart Note operating contract, board #1354, Receiver run 37980089547, PR #2033 and lane-specific source. Claim a single seat and avoid overlapping files. First identify exact input/output contracts and whether the previous stage has produced actual receipts. Repair the smallest existing path; write positive and adversarial tests. Publish branch/head and exact evidence to #1354. Independent verifier reruns exact bytes. Merge/deploy only under existing authority. Continue to the next evidence-supported blocker; never claim a Smart Link proves learning or a candidate is verified merely because stored."

## 8. Reporting language for Shawn
Say what changed for the user, not only PR numbers: (a) note is now retrievable, (b) correct task choice changed, (c) wrong lesson was refused, (d) the next cold Naya repeated the improvement. Report which actually happened, show real links/receipts, describe unfinished rungs in plain English. The purpose of Supabase isn't a URL: it is runtime event/lineage/index/receipt state available for governed workflows. The purpose of nine nodes is connected governed behavior. The purpose of GitHub is inspectable durable code/projection/evidence. Their combination still needs the retrieval→action→verified outcome wiring.
