# ACT — Red-Team Findings (2026-09-30 ~19:58 PDT tick, inline, read-only)

Reviewer: Naya 4 (supervisor worker). Spec: `~/workspace/nine-node-specs/ACT-NODE-SPEC-CANDIDATE.md`
(22,179 bytes, banner intact: CANDIDATE — NOT RATIFIED — NOT MERGED).
Primary corpus: `~/workspace/repo-ground/NayaPOWER` (note: `/tmp/nayapower-main` used by prior
ticks no longer exists — ephemeral; repo-ground copy used instead, STALE — no V2.1 calculus file).
Corpus facts verified BEFORE writing: `NAYANODE/00-ACT-MASTER-CONTRACT-V1.md` EXISTS (89 lines);
`BRAIN/06-PROOF/2026-09-30-ACT-CONCURRENT-IDEMPOTENCY-PROOF.md` (repair #1095/#1116, source/test
verified, live race pending); `tests/test_verified_ai_action_runtime_contract.py`
(`IDEMPOTENCY_KEY_REQUIRED`, `IDEMPOTENCY_KEY_REUSE_CONFLICT`, `persistedFingerprint` vs
`requestFingerprint`, `status: "BLOCKED"`); Constitution Act V1 (18 articles; "irreversible cost"
language present, no "AskHuman Consequential Irreversibility law").

Draft review score: **7.0/10** (consistent with LEARN/PROVE/SELF/LAW draft bar).

---

## MAJOR

### F01 — Master functions unbound; planning-role contradiction (§0 lineage, §1.3 vs master §1/§3)
The master contract lists 13 required functions: `plan_action, validate_action,
select_minimum_sufficient_action, bind_authority, define_expected_outcome,
define_proof_requirements, execute, timeout, retry, rollback, observe, emit_receipt,
idempotency_check` (master §3). The candidate spec binds NONE of them to spec sections —
there is no function-binding section at all (contrast SELF, where all 10 master functions
were verified bound). Worse: candidate §1.3 ("Does not decide... ACT never re-scores, never
overrides the verb") contradicts master §3's `plan_action` + `select_minimum_sufficient_action`
and master §1's purpose question "What is the smallest authorized action that should happen
now?" The spec resolves the tension by assigning all choosing to LAW, but that is a
redesign of the master's function list, not a binding of it. §10.1 admits the master was
"not verified in this draft... presumed by analogy" — the file exists in the corpus and
contradicts the presumption. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F02 — §7.3 TRANSIENT retry violates master invariant (§7.3 vs master §6)
Master §6 invariant: "Never retry without new information." Candidate §7.3 permits retries
on TRANSIENT errors (timeout, rate limit, temp outage) for idempotent tools with backoff —
none of which constitutes new information. A timeout retried with identical params is
exactly what the invariant forbids. The spec needs either a master-amendment argument or a
"new information" definition under which backoff qualifies (it does not, on its face).
Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F03 — §5.1 "Every execution is claimed under an idempotency key" overstates the verified repair (§5.1 vs proof record)
The verified repair (`2026-09-30-ACT-CONCURRENT-IDEMPOTENCY-PROOF.md`): the key column is
NULLABLE and the unique index is PARTIAL ("enforces `(user_id, project_id, action,
idempotency_key)` uniqueness **when a key is present**"). The test suite asserts
`IDEMPOTENCY_KEY_REQUIRED` only in execute mode for **consequential** actions
(`test_consequential_action_requires_idempotency_key`). Non-consequential executions can
therefore run keyless — §5.1's universal claim is false against the verified repair, and
§0's "This spec formalizes that repair as contract" is inaccurate on this point: the spec
silently TIGHTENS the repair without noting the delta. Related: §5.1's `"act:"+hex(...)`
key format vs already-persisted production keys — format compatibility unverified; a format
change could orphan existing keys. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

---

## MODERATE

### F04 — §7.2 lifecycle omits two of the four execution paths (§7.2 vs §1.2/§2.2/§2.3/§6)
§6 defines `path ∈ {EXECUTED, READ_MORE_LOOP, ASK_SUSPENDED, REFUSED, FAILED, CANCELLED,
TIMED_OUT}`; §1.2 and §2.2/§2.3 define READ_MORE and ASK as first-class paths. The §7.2
state machine has NO state for ASK_SUSPENDED or READ_MORE_LOOP — the diagram cannot
represent half the path enum. §8 step 6 cold-reconstructs ASK_SUSPENDED, but the lifecycle
that §8 claims to rebuild from has no such state. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F05 — Async onset: two conflicting protocols (§2.1 vs §7.1)
§2.1: "Sync when the tool completes within its bounded timeout; async with an
`ExecutionTicket` when it does not" (timeout-triggered async). §7.1: "long-running tools
return an `ExecutionTicket` immediately" (tool-declared async). These are different
protocols with different receipt timing and different KNOW handoffs; acceptance §9 has no
test distinguishing them, so the battery is unpassable as written. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F06 — Pre-check cannot distinguish bare CLAIM from receipt; claim supersession undefined (§5.2 vs §8 step 4)
§5.2 step 1: "read the execution ledger for the key. Hit → return the existing
receipt/ticket." A dead CLAIM row (no receipt — the exact crash case §8 addresses) IS a
hit, but has no receipt to return. §8 step 4 then says re-execute "under a new
execution_id with the same idempotency key" — but the dead CLAIM still occupies the key,
and the atomic CAS in §5.2 step 2 would collide with it. No claim-supersession rule
exists. Contrast the verified repair's explicit semantics: replay without a persisted
outcome row is `INCONCLUSIVE` with `IDEMPOTENT_REPLAY_OUTCOME_MISSING`. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F07 — READ_MORE loop bound unenforceable: no lineage identifier (§2.2 vs §1.1/§5.1)
§2.2 bounds "a single decision lineage" to k READ_MORE traversals. But each loop produces
a NEW LAW decision (new receipt id — §2.3 establishes answers arrive "as a new decision,
not an edit of the old receipt"; same logic applies to KNOW's return). `DecisionReceipt`
(§1.1) carries NO lineage identifier, and §5.1's fingerprint includes `decision_receipt_id`
— so each loop iteration derives a DIFFERENT idempotency key. Neither the receipt nor the
key can count traversals. The bound is unimplementable as specified. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F08 — Coalescing leaks cancel authority (§4.5/§5.2 step 3 vs §7.1)
The loser "returns the winner's ticket (coalesce, don't duplicate)". §7.1 defines the
ticket as containing `cancel_handle`. A second, unrelated caller that happened to submit
the same action now holds a cancel handle over the winner's execution — cancel authority
crosses caller boundaries with no scoping rule. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F09 — Revocation check has no mechanism (§1.1/§4.2)
"ACT refuses stale receipts (expired, superseded config, or issued under a revoked
authority)." Expiry and config-hash are checkable; REVOCATION is not — no revocation feed,
no subscription to LAW's temporal-validity machinery (the LAW reconciliation added
ADMISSIBLE→SUSPENDED transitions; ACT names no consumer of them). "Issued under a revoked
authority" is unimplementable as specified. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F10 — `required_authority: predicate` underspecified (§3)
Predicate language, evaluator, and evaluation context are unnamed. Two conforming
implementations could evaluate "the envelope the decision must satisfy" differently —
same decision, authorized under one and refused under another — breaking the
determinism the spec demands elsewhere (§8's "deterministic reconstruction"). Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F11 — Receipt `path`/`outcome` enums don't cover each other (§6)
`outcome ∈ {SUCCESS, FAILURE, TIMEOUT, REFUSED, CONFLICT}`; `path` includes
READ_MORE_LOOP, ASK_SUSPENDED, CANCELLED. A READ_MORE_LOOP receipt carries which outcome?
An ASK_SUSPENDED receipt? CANCELLED → FAILURE? The mapping is undefined, so §9's
cold-successor test ("is it safe to touch again") cannot be answered from the schema alone.
Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F12 — Circuit-breaker and heartbeat state missing from cold reconstruction (§7.3/§5.4 vs §8)
§8's inventory covers CLAIMED / EXECUTING / ASK_SUSPENDED ledger rows. Circuit-breaker
trip state (§7.3) and lease heartbeats (§5.4) are runtime memory with no named store —
a crash resets the breaker, and a flailing tool resumes unthrottled. The heartbeat
writer/store is likewise unspecified (ledger? separate?). Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F13 — KNOW "knowledge edges" name no graph edge type (§1.2 vs ratified graph contract v2.0)
"KNOW records executions as knowledge edges (what was done, with provenance)". The
ratified graph contract v2.0 fixes a 22-type relationship enum (per the LAW review's
corpus verification). ACT's handoff names no edge type — the implementer must either
reuse an existing type (which one?) or touch the ratified contract. Contract-law
boundary: the handoff must name the type or file the amendment proposal itself.
Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F14 — V2.1 calculus lineage status ungrounded; §4.1 hard-gate depends on it (§0 lineage, §4.1)
Spec lists the calculus as CANDIDATE and §4.1 hard-refuses any decision that fails
`recompute()` under the bound configHash. Two failure modes: (a) if V2.1 stays
CANDIDATE forever, ACT can never execute — the gate has no fallback; (b) memory
records #1186 (ratify+bind V2.1→SmartLedger) merged 2026-09-30 16:36 PDT, which would
make the lineage stale. The repo-ground corpus copy is itself stale (no 0027 file), so
this review could not verify current status. Reconciliation MUST verify the calculus's
current ratification state against live main before touching §4.1. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

---

## MINOR

### F15 — Wrong cross-reference (§1.3)
"Does not act without being able to receipt the act (§4.8)" — the receipt rule is §4.7;
§4.8 is budget exhaustion. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F16 — "Notifies the Director" unspecified (§2.3)
Channel and target unnamed (same class as SELF-F09). Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F17 — "Registry order" undefined (§5.5)
"locks are always acquired in registry order with a bounded wait" — registry order is
undefined (registration time? tool_id lexical? authority_class?). The deadlock-avoidance
claim is ungrounded until the order is total and named. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F18 — "AskHuman Consequential Irreversibility law" is not law (§3c)
No such named law exists in the ratified Constitution. The Constitution contains adjacent
principles (clarify material ambiguity affecting irreversible cost; prefer the minimum
sufficient safe action) but the named "law" is candidate V2.1 machinery. Label it
honestly, as the LAW review did for its false constitutional attributions (LAW-F02/F03).
Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

### F19 — "Two identical receipts" underspecified (§9.2)
Byte-identical receipts are impossible (`issued_at`, `execution_id` differ). The verified
repair's semantics is same-receipt replay ("losing request replays the same persisted
receipt"). §9.2 should say that. Status: FIXED (reconciled 2026-10-01 ~20:08 PDT as CANDIDATE revisions; see Appendix A of the spec).

---

## Explicitly checked — no finding
- **GAP-A coverage complete:** responsibility (§1), execution ownership (§1 — "the only node
  that produces effects"), sync/async (§7), persisted transitions (§7.2 + §6
  `state_transitions`), evidence (§6 ExecutionReceipt), authority (§1.1/§3), failure
  propagation (§7.3 table + receipts), cold reconstruction (§8). Registry ownership is
  §10.8-open by design, not a gap.
- **Contract law:** §6's `execution` stream is OPENLY proposed (schema marked "proposed",
  §10.6 question, §11 disclaimer stands) — no silent extension. No graph edge types
  written by ACT (F13 is a naming gap, not an extension). No contract text altered.
  The `execution`-stream proposal needs the amendment-proposal treatment at
  reconciliation if a ratified stream topology exists.
- **Repair grounding (positive):** §4.4/§5.3 fail-closed on conflicting reuse is REAL in
  the verified repair — `IDEMPOTENCY_KEY_REUSE_CONFLICT`, `persistedFingerprint` vs
  `requestFingerprint` comparison, `status: "BLOCKED"` (tests/test_verified_ai_action_runtime_contract.py).
  §5.2's atomic-claim/loser-coalesce matches the proof record's "unique-key loser rereads
  the winner receipt rather than executing again" (PR #1095, #1116; source/test verified,
  live race pending exact deployment).
- §2.4 refusal semantics; §4.1 recompute gate concept; §4.6 hard-stop flags; §4.7
  receipt-or-refuse — internally consistent.
- **Evidence floors:** N/A — no statistical claims in spec.
- **LEARN/EVOLVE quality bar:** §8's determinism acceptance (§9.8/§9.13) matches the bar;
  weakened by F04/F06/F12 (states the reconstruction can't see).
