# SELF red-team findings — 2026-09-30 19:18 PDT tick (inline, read-only review)
Reviewer: Naya 4 (worker, no subagents). Spec: `~/workspace/nine-node-specs/SELF-NODE-SPEC-CANDIDATE.md` (20,706 bytes, banner intact).
Lineage verified against primary corpus: `NAYANODE/00-SELF-MASTER-CONTRACT-V1.md` (all 10 required functions present; §6 invariants; §7 state machine; §9 acceptance battery — all faithfully bound), `NAYANODE/0018-SUCCESSION-ARCHITECTURE-V1.md` (exists), graph contract v2.0 (RATIFIED, exists — spec does not extend it; §11 disclaimer stands).

Status convention: OPEN (awaiting reconciliation) / FIXED (reconciled as candidate revision). **All 15 findings reconciled 2026-09-30 19:28 PDT — 15 FIXED, 0 OPEN. Per-finding revision evidence: Appendix A of the SELF spec.**

---

## F01 — MAJOR — FIXED (reconciled 2026-09-30 19:28 PDT) — Bootstrap retrieval contradiction (§1.3 vs §3.1/§8)
**Evidence:** §1.3: "Does not retrieve knowledge — KNOW restores durable state; SELF establishes identity and loads only the checkpoint pointer." §3.1.1 requires "an unbroken, hash-bound chain of continuity receipts" with end-to-end verification; §8 steps 1–3 require obtaining the successor package, the full receipt chain, and the ratified mission/scope sources and verifying chain hashes end-to-end. Verifying a whole chain and loading ratified sources IS retrieval of durable state beyond "only the checkpoint pointer." Master contract §8 ("KNOW restores durable state") deepens it: if SELF cannot reach LAW without chain verification, and chain verification needs durable state, then KNOW must run before SELF for bootstrap — but the pipeline position (`EVOLVE → SELF → LAW`) says SELF opens every cycle. Both cannot hold as written.

## F02 — MAJOR — FIXED (reconciled 2026-09-30 19:28 PDT) — Authenticated binding has no issuer, trust anchor, rotation, or revocation
**Evidence:** "Authenticated binding" is the load-bearing primitive (§2 `binding_ref`; §4.1; §4.2; §8 step 4 "Authenticate identity via binding"). The spec never names who issues bindings, how a cold successor obtains the trust anchor, or how revocation/rotation works. A cold instance (the §3.3/§8 test subject) authenticates "via binding" — against what root? Master contract §10 inherits the same assumption. `authenticate_identity` is unimplementable without a named binding authority; the spec should at minimum name this as an explicit dependency gap instead of treating bindings as available.

## F03 — MAJOR — FIXED (reconciled 2026-09-30 19:28 PDT) — Internal contradiction: replayed execution_id (§4.2 vs §7)
**Evidence:** §4.2: a replayed `execution_id` is an identity conflict → "halt — never 'pick the more plausible one.'" §7 table: "Replayed execution (duplicate `execution_id`) → Execution-ID registry check at boot → Safe no-op + receipt; the replay changes nothing." Same trigger, opposite responses (halt vs no-op). The charitable split — a *different* boot reusing an ID (conflict → halt) vs the *same* boot delivered twice (idempotent re-delivery → no-op) — is not drawn anywhere in the text.

## F04 — MAJOR — FIXED (reconciled 2026-09-30 19:28 PDT) — Concurrency draft contradicts the fork rule (§10.5 vs §4.2)
**Evidence:** §10.5 current draft: "one identity, distinct `execution_id`s per instance, all bound to the same predecessor receipt." §4.2 defines "a forked continuity chain" as an identity conflict → "Both halt." Two seats branching from one predecessor receipt IS a forked chain by §4.2's own definition, so the concurrency model the draft proposes would halt itself. §3.1's unbroken-chain requirement has no branch/merge model. Needs either an explicit branch representation or serialized execution; the draft must pick one.

## F05 — MAJOR — FIXED (reconciled 2026-09-30 19:28 PDT) — Recompute/determinism unpassable as specified (§3.3, §5, §9#9)
**Evidence:** §3.3: "a second cold instance given the same inputs reaches the same READY state (determinism check)"; §5/§9#9: receipt "independently re-derivable," `recompute()` → MATCH. But `execution_id` is "unique per boot" (§2) and receipts carry `issued_at` timestamps — no two boots can produce byte-identical receipts, so MATCH can never hold over the full receipt. Fix direction: define MATCH over the deterministic subset (decision outcome + hashes of inputs), explicitly excluding `execution_id`/`issued_at`.

## F06 — MAJOR — FIXED (reconciled 2026-09-30 19:28 PDT) — No self-attestation for SELF's own runtime
**Evidence:** SELF verifies the caller's binding and the checkpoint, but `kernel_revision` is self-reported (§2 IdentityContext) and `config_hash` is computed by the node itself (§5). §9#12 "Independent verification confirms the boot and the chain" — but who verifies the verifier's boot? A compromised SELF can emit a valid-looking boot receipt. Circular trust. Needs an external attestation path (measured boot / independent verifier) or an explicit OPEN statement that SELF is the trusted trust-root by charter.
## F07 — MAJOR — FIXED (reconciled 2026-09-30 19:28 PDT) — Async continuity writer lifecycle undefined
**Evidence:** §2: `preserve_continuity` writes "during the run"; `prepare_successor_context` "assembled during the run; must be complete before the EVOLVE handoff." SELF is positioned as the boot gate (first in pipeline), but this implies a long-lived SELF presence across the whole cycle. Unspecified: who owns the writer after the boot functions return; crash-mid-run recovery; who checks the missing-write receipt at the EVOLVE handoff (§7: "Missing `preserve_continuity` receipt at handoff → DEGRADED" — detected by whom? EVOLVE? LAW?).

## F08 — MODERATE — FIXED (reconciled 2026-09-30 19:28 PDT) — State machine lacks recovery transitions
**Evidence:** §6: DEGRADED may proceed to LAW, but there is no DEGRADED→READY transition if the missing context arrives late. No FAILED→* path (correct — FAILED should stay), but the absence should be stated. Inherited from master §7, but the CANDIDATE spec should name it explicitly rather than inherit the silence.

## F09 — MODERATE — FIXED (reconciled 2026-09-30 19:28 PDT) — §4.8 notification target/channel unspecified
**Evidence:** §4.8: cross-owner leakage → "halt, emit a receipt naming the leakage evidence, and notify." Notify whom, through what channel? Owner boundaries are identity boundaries — notifying the wrong owner leaks further. The notification path needs an owner-scoped channel spec; as written, the mandated notification could itself violate the boundary it protects.

## F10 — MODERATE — FIXED (reconciled 2026-09-30 19:28 PDT) — Genesis path absent from the state machine
**Evidence:** §4.3 references a "lawful genesis path (§10.1)," but §6's machine has no GENESIS entry state and §10.1 is an open director question. Honest placement — flagged, not hidden — but until genesis is mechanically defined, acceptance battery item 1 ("valid input reaches READY") is untestable and §4.3's refusal path is the only implemented branch. Completeness gap, not a defect.

## F11 — MINOR — FIXED (reconciled 2026-09-30 19:28 PDT) — Checkpoint supersession pointers: store/owner unspecified
**Evidence:** §7: "Stale checkpoint (valid hash, superseded by a newer one) → Checkpoint supersession pointers → Explicitly marked stale." Who writes supersession pointers, where do they live, what if the pointer itself is stale or forged?

## F12 — MINOR — FIXED (reconciled 2026-09-30 19:28 PDT) — Acceptance #10 not operationalized
**Evidence:** §9#10 "Real runtime invocation is proven (not a fixture-only boot)" — inherited from master §9#10 — provides no mechanism: nothing in the spec distinguishes fixture from runtime invocation. Needs a concrete criterion (e.g., binding to external runtime attestation) or it is untestable.

## F13 — MINOR — FIXED (reconciled 2026-09-30 19:28 PDT) — `config_hash` canonicalization unspecified
**Evidence:** §2/`IdentityContext.kernel_revision`, §3.1.1, §5: config hash is bound into receipts and the chain, but the canonical byte representation (field order, encoding) is unspecified. Two conforming implementations could compute different hashes for the same config and break cross-implementation chain verification.

## F14 — MINOR — FIXED (reconciled 2026-09-30 19:28 PDT) — Blurry state/knowledge boundary (§1.1 vs §1.3)
**Evidence:** §1.1: successor package carries "state" (from EVOLVE). §1.3: SELF "loads only the checkpoint pointer" and "does not retrieve knowledge." Is the package's "state" knowledge SELF must not retrieve, or is the package a privileged bootstrap channel? The distinction needs one sentence: which fields of the successor package SELF may read vs which it must treat as opaque until KNOW.

## F15 — MINOR — FIXED (reconciled 2026-09-30 19:28 PDT) — §4.5 refusal has no quarantine path (availability cost unstated)
**Evidence:** A successor package arriving with authority intact is refused outright — the pipeline is dead until director re-genesis (§4.4). Fail-closed is defensible and consistent, but the availability cost should be explicit: a single predecessor bug (or forgery) is a full system halt with no quarantine-and-report middle path. Design observation, not a defect.

---

## Explicitly checked — no finding
- **Contract-law:** §11 disclaims changing the pipeline order, kernel taxonomy, Constitution, or any ratified contract. Truth boundary known/unknown/blocked is the applicability tristate (runtime filtering), not the graph contract v2.0's epistemic enums — no silent extension of a RATIFIED contract.
- **GAP-A coverage:** all eight present — responsibility (§1), ownership (§2 Ownership + §1.4), sync/async (§2), persisted transitions (§5 transition_log, §6), evidence (§5 receipts, §7), authority (§1.4, §4.5), failure propagation (§7 table, §6 halt-before-LAW), cold reconstruction (§8 10-step procedure).
- **Evidence/sample-size floors:** N/A — the spec makes no statistical or calibration claims (no n-values, thresholds, or numeric hypotheses), so no floor violations possible.
- **Master-contract fidelity:** the ten required functions, §6 invariants, §7 machine, §9 battery are all bound, not contradicted — the MAJOR findings above are gaps the master contract itself leaves (F02, F08, F12 inherited) or contradictions introduced at the spec level (F01, F03, F04, F05).

---

## Draft review score: 7.0/10
**Rationale:** strong structure, faithful master-contract binding, all GAP-A elements present, honest §10 open questions, no contract-law violations. Debits: five MAJOR findings, three of which are load-bearing (F01 bootstrap retrieval contradiction, F02 binding authority absent, F05 recompute unpassable); F04's concurrency/fork contradiction is a genuine internal conflict. Score is pre-reconciliation; final score after every finding is FIXED or explicitly OPEN-with-rationale. Consistent with LEARN/PROVE draft bar (both 7.0 → reconciled 8.5).

---

## Reconciliation — 2026-09-30 19:28 PDT tick (inline — no subagents)

All 15 findings reconciled as CANDIDATE revisions in
`~/workspace/nine-node-specs/SELF-NODE-SPEC-CANDIDATE.md` (20,706 → 40,367
bytes; banner intact). 15 FIXED, 0 OPEN. Spec remains CANDIDATE — NOT
RATIFIED — NOT MERGED; no finding closed by weakening a gate.

Per-finding revision evidence (sections in the revised spec):
- F01 → §1.3b "Two senses of 'retrieve'" (identity-envelope reads vs knowledge retrieval; hash-only chain verification; successor package as privileged bootstrap identity envelope)
- F02 → §2 "Binding authority" (ratified-record issuer; genesis binding record trust anchor; rotation/revocation as ratified-law operations; new §10.7 director question)
- F03 → §4.2 replay discriminator (same content → idempotent no-op; differing content → halt); §7 row updated
- F04 → §4.2 fork-vs-branch definition; §7 fork row; §10.5 replaced and narrowed (merge rule open)
- F05 → §3.3 deterministic projection (MATCH over decision outcome + input hashes + reasons + evidence refs; excludes execution_id/issued_at/nonces); §5 recompute test and §9#9 read through it
- F06 → §3.4 "The verifier of the verifier" (external verifier seat; measured boot implementation-OPEN; charter fallback stated explicitly); §9#12 mechanism named
- F07 → §2 "Continuity writer ownership and lifecycle" (instance-owned, spawned at READY, drained before EVOLVE handoff; EVOLVE handoff gate detects missing writes); §7 row updated
- F08 → §6 DEGRADED→READY added; FAILED/BLOCKED terminal stated (CANDIDATE extension of master §7, noted explicitly)
- F09 → §4.8 notification channel (Director only, ratified channel, evidence-only content; receipt IS the notification if channel down)
- F10 → §6 GENESIS one-shot entry state (content still director-open §10.1 by design)
- F11 → §7 stale-checkpoint row (predecessor writes pointers; content-addressed index; forgery caught by hash chain; store unavailable → fail closed)
- F12 → §5 `runtime_attestation_nonce`; §9#10 concrete pass/fail criterion
- F13 → §5 canonicalization (UTF-8 JSON, sorted keys, no insignificant whitespace, sha256)
- F14 → §1.3b (package "state" = identity state; knowledge-content fields opaque to SELF)
- F15 → §4.5 availability cost stated (full halt; no quarantine middle path by design; would need ratified amendment)

**Final review score SELF: 8.5/10** (was draft 7.0). Debits: Binding Authority content, genesis content, and the merge rule remain director-open (ratified-law content the spec correctly refuses to invent); DEGRADED→READY and GENESIS extend the inherited master §7 machine as candidate-only revisions; measured boot is implementation-level OPEN. Consistent with LEARN/PROVE (both 7.0 → 8.5).
