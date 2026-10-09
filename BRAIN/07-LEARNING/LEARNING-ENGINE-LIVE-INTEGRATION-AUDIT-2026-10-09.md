# NayaPOWER Learning Engine — Live Integration Audit and Gap Ledger

**Purpose:** Code-backed companion to the canonical execution blueprint in [PR #2037](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2037). This document does not create a second architecture, a second brain, or a competing node order. PR #2037 owns the top-level learning-engine assembly blueprint and fourteen-seat execution contract; this companion supplies deeper source/live evidence, exact integration seams, and corrections that must be reflected in the implementation plan.

**Authority:** Human Director retains all consequential authority. No merge, deployment, H13 grant, production promotion, or permission/credential change is authorized by this document.

**Truth law:** IMPLEMENTED ≠ VERIFIED; STORED ≠ LEARNED; SMART LINK ≠ LEARNING RECEIPT; UNKNOWN/BLOCKED ≠ PASS.

**Audit basis:** current-main source SHA `1d73652231ac6127806640af5a31eb516c60738d` plus read-only Supabase project inspection on 2026-10-09. Re-fetch main and deployed versions before a ship decision.

**Primary implementation tracker:** [Issue #2046](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2046) — same-object Smart Note → learning proof and fallback-proof prevention.

**Canonical assembly blueprint:** [PR #2037](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2037). Existing constitutional contracts and the canonical runtime manifest outrank both drafts. Node responsibilities in this companion do not authorize changing the canonical nine-node execution order.

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


### 18.7 Critical acceptance risk: the learning-proof producer can use a fallback lesson

The reviewed `.github/workflows/live-intelligence-commit-proof.yml` has a real-capture branch when `tools.smart_note_v2 discover` finds a changed `.naya/capture/*.json` file. But the single-capture path also has an explicit `else` branch when `capture-path.txt` is empty: it manufactures a bounded test lesson titled `Naya runtime flow lesson` with content including `Preserve provenance before applying retained intelligence.`, then commits that lesson through the same runtime and writes a fresh-lineage artifact. The downstream `.github/workflows/live-supabase-runtime-proof.yml` starts from the producer run and consumes its `fresh-lesson-lineage-ids.json` artifact; the reviewed downstream path does not, at its entry, require proof that the producer artifact came from a real user capture rather than the fallback branch.

This fallback may be useful for isolated runtime smoke tests. It must **never satisfy the acceptance claim that Shawn's Smart Note was learned**. Without an explicit source-kind gate, a complete green behavioral proof could describe the fallback test lesson rather than the user's actual note.

**Required machine-enforced repair:**
- Producer receipt must include `capture_kind=USER_CAPTURE` or `capture_kind=TEST_FALLBACK`, the exact `capture_id`, source capture path, content digest, and a source event/IB identity.
- The learning-acceptance workflow must require `capture_kind=USER_CAPTURE`, non-empty exact capture ID/path, and a digest that matches the canonical IB before it may publish a **user Smart Note learned** verdict.
- Fallback runs must remain explicitly labelled test-only and cannot satisfy the Smart Note golden-path gate, scorecard, or learning receipt for a human-authored lesson.
- The downstream verifier must recompute the binding from the producer artifact and persisted canonical record; it must not trust a caller-supplied boolean or the workflow's display label.
- Add negative CI proofs showing that (a) no capture path, (b) fallback capture, (c) mismatched capture ID, (d) wrong IB, and (e) digest mismatch all fail the user-learning acceptance gate even if the fallback behavioral test itself passes.
- Preserve the fallback for component smoke tests if useful, but separate test-success from user-learning-success in workflow conclusions and receipts.

This is a separate, confirmed source-level risk from the Path A/Path B orchestration gap in §18.4. Both must be closed: the user's real capture must reach the learning chain, and the chain must refuse to certify any substitute object.
