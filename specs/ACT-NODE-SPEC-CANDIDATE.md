# ACT Node — Reconciled Candidate Specification (PDF + Naya 4 draft)

**STATUS: CANDIDATE — NOT RATIFIED — NOT MERGED**

Draft only. Merges the other Naya's NODE 3 PDF (95 sections, "Ultimate Master
Specification V1") with Naya 4's candidate draft
(`ACT-NODE-SPEC-CANDIDATE.md`, incl. its master-contract function binding).
Creates no obligation, changes no code, authorizes nothing. Contradictions
resolved explicitly in Appendix B; nothing from either source dropped without
a stronger replacement.

- **Node:** NAYA-KERNEL-ACT · **Pipeline:** `SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE → SELF`
- **Date:** 2026-09-30 · **Author:** Naya 4 (reconciliation draft for director review)

## 0. Purpose

ACT is NayaPOWER's governed execution organ — the only node that produces
effects in the world. It receives an explicit LAW authorization and canonical
decision, binds them to the exact target, Smart Door, parameters, proof
requirements, and idempotency identity, performs the smallest sufficient safe
action, records reality without exaggeration, and hands the result to
independent verification. A decision without ACT is inert. An effect without
ACT is unauthorized. (PDF §91 + draft §0.)

**The deepest invariant** (PDF §92): ACT never decides whether it may act.
ACT never decides whether an outcome is true. ACT never decides whether a
change is ratified. ACT makes the authorized thing happen — no more, no less —
and leaves a reconstructable record of exactly what happened.

## 1. Responsibility in the pipeline

**From LAW:** only authorized decision receipts — the `DecisionReceipt`
(decision verb, winner action spec, authorityBasis, calculusVersion +
configHash, reversibility, stakes, issuedAt/validUntil, issuedBy,
executionBudget). ACT never executes from a chat message, plan, goal, memory,
or its own initiative. Receipt freshness is authority: expired, superseded-
config, or revoked-authority receipts are refused. (Draft §1.1.)

**Context-equivalence rule** (PDF §2): the broader execution algorithm may
establish knowledge/context/retrieval before ACT when needed — ACT requires
the *equivalent governed context* before effect, not a particular software
call sequence. But it MUST still receive a valid LAW authorization for
consequential action.

**To KNOW:** a typed `ExecutionHandoff` (execution_id, decision_ref, path,
receipt, ticket) for every terminal path — executions become knowledge edges
with provenance. ACT does not interpret effects as learnings (LEARN's job,
downstream of verification). (Draft §1.2. *Resolves PDF §67's "→ VERIFY"
shorthand:* canonical handoff is ACT→KNOW; VERIFY closes the loop via
receipts — Appendix B.)

**ACT does NOT:** decide the verb, re-score, retrieve knowledge (except via
READ_MORE, which *returns* to KNOW), verify outcomes, prove claims, grant or
persist authority (authority flows LAW → ACT → dies with the execution), learn
from executions, or perform an act it cannot receipt. (Draft §1.3; PDF §5.)

**ACT judgment hierarchy** (PDF §57): HARD STOP > LAW AUTHORIZATION >
CANONICAL DECISION > EXECUTION PLAN > RAW INSTRUCTION. A raw instruction is
input, not authority.

**Pre-execution orientation** (PDF §66): before effect, ACT orients on 13
points — objective, selected action, what LAW authorized, authorization
freshness, exact target, Door, proof evidence, failure modes, smallest
sufficient action, idempotency, reversibility, timeout behavior, VERIFY's
needs — then executes only what survives.

## 2. The four execution paths

LAW's decision verb selects exactly one path. There is no fifth path.
(PDF implies these but never formally defines them — draft §2 wins.)

- **ACT:** claim (§5), invoke (§3), observe, receipt (§6). Sync within the
  bounded timeout; async via `ExecutionTicket` otherwise (§7).
- **READ_MORE:** no execution; hands the decision back to KNOW with the
  retrieval directive. Loop bound: at most k traversals per decision lineage
  (candidate default 3); exceeding forces ASK.
- **ASK:** suspends as ASK_SUSPENDED with a persisted decision brief;
  notifies the Director; the answer resumes via a *fresh* LAW decision.
  Silence is never consent; timeout/withdrawal → CANCELLED with receipt.
- **REFUSE:** terminates with a reasons-carrying RefusalReceipt (which gate
  fired, which hard stop, what would make it lawful). Re-proposal only as a
  new decision.

## 3. Tool authority — registered Smart Doors

ACT invokes **only registered tools** through **registered Smart Doors**.
The registry is governance-owned; ACT reads it, never writes it. (Merged
draft §3 + PDF §14.)

```
ToolRegistration {
  tool_id, version,
  door_id, door_version,              # PDF §14: the execution boundary
  authority_class: READ | WRITE_SCOPED | WRITE_BROAD | IRREVERSIBLE | EXTERNAL_EFFECT,
  supported_operations, accepted_parameters, target_class, scope,
  side_effect_class, authentication_requirement, logging_requirement,
  timeout_behavior, rollback_support,
  idempotent: bool,
  max_timeout_ms, retry_policy,       # only if idempotent
  required_authority: predicate,      # envelope the decision must satisfy
  compensating_tool: tool_id | null,
  evidence_capture: string            # how ACT observes this tool's effects
}
```

**Invocation rule:** ACT invokes tool T for decision D iff (a) T registered
at a pinned version, (b) D's authorityBasis satisfies T's required_authority,
(c) D's reversibility is compatible with T's authority_class (IRREVERSIBLE /
EXTERNAL_EFFECT require the receipt to name the irreversibility explicitly),
(d) no hard-stop flag set. Failure → refuse the invocation (receipted; LAW
may re-decide). Tools receive parameters, not permissions.

**Door binding** (PDF §15–§17): LAW AUTHORIZATION + TARGET + OPERATION +
PARAMETERS + DOOR must bind as one; authorized-Door-A + unrelated-target,
operation-A + operation-B, or authorized-params + mutated-params are rejected
unless the governance path reruns. Targets are explicit (repo/branch/file/
row/project/environment/account/service/external/person-owned resource); a
target *discovered* during execution is not automatically in scope —
material target change → STOP → RECHECK. Parameters are canonicalized and
hashed pre-execution (`parameter_hash`); the receipt binds target/operation/
parameter/law-context hashes — the executed action must be the authorized
action.

**Environment boundary** (PDF §46): LOCAL / TEST / STAGING / PRODUCTION /
EXTERNAL / UNKNOWN is part of scope — a TEST permission never silently
becomes PRODUCTION.

## 4. Refusal conditions

ACT refuses (no effects; receipted) when: no/forged/unrecomputable LAW
receipt; stale or superseded receipt (`now > validUntil`, config moved,
authority revoked); tool unregistered or authority insufficient (never
self-registers, never escalates); fingerprint conflict (same key, different
fingerprint → ConflictReceipt + alert); conflicting execution in flight
(return the live ticket, don't duplicate); hard-stop flags; evidence capture
impossible (**no receiptable act is performed unreceipted**); budget
exhausted (timeout/retry/loop bound → TIMED_OUT / FAILED / forced ASK);
**fail-closed list** (PDF §56): missing LAW authority, invalid LAW
timestamp, expired/revoked authority, target/door/parameter mismatch,
missing proof boundary, identity conflict, idempotency conflict, unsafe
reversibility change, protected environment mismatch. (Draft §4 + PDF §56.)

**Blast radius** (PDF §43): NONE / LOCAL / PROJECT / USER / TEAM / SYSTEM /
COLLECTIVE / EXTERNAL / UNKNOWN — classified per consequential execution;
UNKNOWN is not automatically safe; high-blast actions require stronger
controls. **Reversibility** (PDF §44): REVERSIBLE / RECOVERABLE /
PARTIALLY_REVERSIBLE / IRREVERSIBLE / UNKNOWN carried on every action; an
action that becomes less reversible than authorized re-enters governance.

## 5. Concurrency and idempotency

**Key derivation** (draft §5.1 + PDF §22):
`idempotency_key = "act:" + hex(hash(decision_receipt_id | action_spec |
params_hash | authority_basis | configHash | issuedBy))` — the key is
derived, never assigned; the fingerprint is persisted with the claim.

**Atomic claim** (PDF §23, the race solved): REQUEST → ATOMIC CLAIM →
first-winner EXECUTE ONCE → PERSIST OUTCOME; the concurrent loser re-reads
the winner and returns the same receipt/outcome — never executes again.
Pre-check → atomic compare-and-set → loser coalesces to the winner's ticket
(live lease) or attempts recovery (expired lease, §8) — never blind
re-execution. (Draft §5.2.)

**Fail-closed on conflicting reuse** (draft §5.3): same key + different
fingerprint → refuse, ConflictReceipt naming both fingerprints, alert.

**Leases and liveness** (draft §5.4): CLAIMED/EXECUTING holds a lease with
deadline + heartbeat; expiry without heartbeat = presumed dead,
recovery-eligible. **Per-resource serialization** (draft §5.5): non-idempotent
tools serialize on the affected resource (lease-bounded locks, registry
order, bounded wait).

**Replay law** (PDF §24): identical replay (same action/target/params/
authority/key) → same canonical record; conflicting replay fails closed.
**Missing outcome after replay** (PDF §25): loser finds no persisted winner
outcome → `IDEMPOTENT_REPLAY_OUTCOME_MISSING` surfaced explicitly; never
silently re-execute.

**Pre-effect receipt** (PDF §26): high-consequence executions persist a
pre-effect record (what was about to happen, under whose authority, through
which Door, against which target, with which parameters) — AUTHORIZED →
COMMITTED-TO-EXECUTION → EXECUTED/FAILED/CANCELLED.

## 6. ExecutionReceipt (merged schema)

Every terminal path emits a typed receipt to the SmartLedger `execution`
stream (proposed stream — draft §10 Q6): receipt_id, execution_id, node_id
MN-03, node_version, action_id, decision_id, state_before/after,
`law_receipt_id`, **`law_context_hash`** (PDF §51), authority_ref,
target_hash, operation, parameter_hash, door_id/door_version,
idempotency_key, fingerprint, expected_outcome, proof_requirements,
observation, execution_result, error (error_class:
TRANSIENT/PERMANENT/AUTHORITY/HARM_SIGNAL), rollback_state, attempts,
duration_ms, compensation, input/output hashes, provenance, gaps, timestamp.
**Receipt integrity** (PDF §53): alteration creates new lineage, never silent
replacement. **Receipt ≠ proof of success** (PDF §54): a receipt proves an
execution record exists — VERIFY decides whether the real-world result
happened. **Cold-successor test:** from the ledger alone, a cold agent must
answer for any key: did this execute, with what effects, is it safe to touch
again.

## 7. Lifecycle, retry, timeout, rollback

**State machine** (draft §7.2 + PDF §27 states): AUTHORIZED → CLAIMED →
EXECUTING → EFFECTS_OBSERVED → RECEIPTED (terminal; supersession only by
linked completion/compensation receipts); PDF's LAW_RECHECK, TARGET_BOUND,
DOOR_BOUND, READY, OBSERVING, COMMITTING as named intermediates; terminal
BLOCKED/DENIED/DEFERRED/FAILED/TIMED_OUT/CANCELLED/ROLLED_BACK/INCONCLUSIVE;
optional RETRY_PENDING/ROLLBACK_PENDING/PARTIAL_EFFECT/RECOVERY_PENDING.
Invalid transitions fail closed; every transition records before/after/
reason/execution/timestamp.

**Retry law** (PDF §33–§34): never retry a failed strategy unchanged without
new information; every retryable action defines max_attempts/backoff/jitter/
retryable vs non-retryable errors/state-reread/authority-recheck/idempotency
behavior; duplicate-side-effect-capable retries require idempotency-safe
execution. **Circuit breaker** (draft §7.3): N consecutive tool failures
(candidate 5) → OPEN for cooldown → fail-fast with receipts → half-open
probe re-closes on success.

**Timeout law** (PDF §35): on timeout distinguish NOT_STARTED /
STARTED_UNKNOWN_RESULT / COMPLETED / FAILED — TIMEOUT → REREAD/RECONCILE
before any repeat; never interpret timeout as failure when the external
system may already have executed.

**Partial effects** (PDF §36): preserve what completed / didn't / remains
unknown / side effects occurred — never collapse PARTIAL→SUCCESS or
UNKNOWN→FAILED without evidence. **Cancellation** (PDF §37): explicit state;
triggered by revocation, safety change, material target change, hard stop,
bounds exceeded.

**Rollback is an action** (PDF §38–§40): defined target, authority basis,
scope, expected result, evidence requirement, receipt, verification
requirement; never claim ROLLBACK COMPLETE until the rollback effect is
observed and verified; compensating actions (when true rollback is
impossible) are recorded *as compensation*, never as history erasure —
ORIGINAL EVENT → ROLLBACK EVENT → NEW STATE.

**Safe execution pattern** (PDF §45, recommended): DRY RUN → CHECK →
SMALLEST EFFECT → OBSERVE → EXPAND ONLY IF PROVEN SAFE (deployments,
migrations, batch modifications, external publication, destructive ops).

**Failure classification** (draft §7.3): TRANSIENT (retry iff idempotent +
budget remains) / PERMANENT (no retry) / AUTHORITY (abort, never
self-escalate) / HARM_SIGNAL (abort, compensate, alert). Failures propagate
as receipts, never silent exceptions.

## 8. Cold reconstruction

From the ledger alone: list CLAIMED/EXECUTING/ASK_SUSPENDED → lease check
(live → leave; expired → recovery-eligible) → receipt check (final receipt
exists → done) → idempotent + no receipt → safe re-execution under a new
execution_id with the same key → non-idempotent + no receipt + effects
unknown → `UNKNOWN_EFFECTS`, **do not blindly re-execute**, brief the human
→ ASK_SUSPENDED survives intact. Deterministic: two cold successors reach
the same recovery plan (acceptance §9.12). Successor context grants no new
authority (PDF §85).

## 9. Acceptance battery (merged)

Draft §9's 14 criteria stand (once-only execution, key dedupe, race,
fingerprint conflict, unregistered-tool refusal, stale-receipt refusal,
READ_MORE loop bound, ASK semantics, REFUSE receipts, transient/permanent
retry rules, HARM_SIGNAL abort, crash recovery, cold-successor query,
circuit breaker), plus the PDF's golden tests: **negative** (DELETE
PRODUCTION DATA with capability+value but LAW=PROHIBITED → NO EFFECT, §78);
**positive** (authorized reversible repo change: target bound, door bound,
params hashed, idempotency claimed, executed once, receipted, VERIFY handed
the result, §79); **race** (two identical requests → ONE EFFECT, ONE
CANONICAL OUTCOME, TWO REQUESTS, §80); **stale-authority** (revoked at t1,
old receipt at t2 → RECHECK → REVOKED → NO EFFECT, §81); **material-change**
(file B discovered better than authorized file A → STOP → re-govern, §82);
**timeout** (unknown external state → reconcile before retry, §83);
**rollback** (original + regression + rollback + observation preserved,
VERIFY establishes post-rollback state, §84).

**What INFLUENTIAL means** (PDF §87): the LAW baton actually constrains
execution — same capability + valid authorization → effect; same capability +
missing/invalid authorization → no effect. **What VERIFIED means** (PDF §88):
independent reconstruction of authorization + action identity + target +
params + execution record + observed result. **What PRODUCTION-PROVEN means**
(PDF §89): exact source revision + actual production Door + actual execution
+ persisted receipt + persisted outcome + independent reread + independent
verification. Self-report is insufficient, always.

## 10. Open questions for Shawn

Draft Q1–Q8 stand (master-contract canonicality; key TTL; retry-budget
ownership; UNKNOWN_EFFECTS pre-authorization; unreceiptable-act exceptions;
`execution` ledger stream topology; READ_MORE loop bound; tool-registry
governance). **Q9 (new, from PDF §12):** the MPA metric (Verified Value
Produced / Resources Consumed) — adopt as a governed measurement instrument
(with VERIFY as the verifier), or leave measurement to the calculus
recalibration path?

## 11. What this spec does NOT do

Does not implement ACT; does not ratify the calculus (binding merged into
main via #1186/#1190/#1192, director-authorized; spec doc #1182 remains
CANDIDATE); does not authorize any action; does not register any tool or
change the registry; does not change the pipeline, kernel taxonomy, or any
contract; is not production guidance (Constitution VII.3, XV).

---

## Appendix A — Source map

- **From the PDF:** Smart Door + door/target/parameter binding (§3),
  live authority recheck + freshness (§1), atomic idempotency law +
  IDOMPOTENT_REPLAY_OUTCOME_MISSING + pre-effect receipt (§5), timeout law
  + partial effects + cancellation + rollback-as-action + no-history-erasure
  (§7), dry-run pattern (§7), blast radius + reversibility + environment
  boundary (§4), resource governance + cost of inaction (§4), security threat
  model incl. tool-result injection (§4/§18), ACT judgment hierarchy (§1),
  cognitive procedure (§1), golden tests (§9), INFLUENTIAL/VERIFIED/
  PRODUCTION-PROVEN definitions (§9), MPA metric (§10 Q9).
- **From Naya 4's draft:** four execution paths + verb set (§2), master-
  contract 13-function binding (§0.1), means-vs-verb planning-scope rule,
  ExecutionHandoff to KNOW (§1.2), refusal conditions (§4), key derivation +
  claim protocol + leases + per-resource serialization (§5), receipt schema
  (§6), circuit breaker (§7), deterministic cold reconstruction (§8),
  acceptance battery 1–14 (§9), open questions Q1–Q8 (§10).

## Appendix B — Contradiction resolutions

1. **V2.1 status (draft lineage "RATIFIED #1186" vs draft §11 "still
   CANDIDATE #1185"):** RESOLVED — the draft contradicted itself. Binding
   merged into main (#1186/#1190/#1192, director-authorized); spec doc
   #1182 remains CANDIDATE. PDF's "canonical V2.1" (§7) is therefore
   defensible for the machinery; labeled precisely herein.
2. **Handoff target (PDF §67 "→ VERIFY" vs pipeline ACT→KNOW):** DRAFT
   WINS. Canonical handoff is ACT→KNOW (execution record as knowledge);
   VERIFY closes the loop via receipts. PDF §67 read as shorthand.
3. **Planning scope (PDF §10 "ACT MAY optimize" vs draft §1.3 "never
   decides"):** MERGED via the means-vs-verb rule — ACT decides *means*
   inside the authorized envelope, never the verb (§0.1).
4. **Value's role (PDF §11–§12 sufficiency/efficiency vs draft):** AGREE —
   minimum-sufficient-action and MPA are execution realizations of the
   already-governed decision, never gate inputs; efficiency never overrides
   LAW/safety/consent/truth/authority/proof.
5. **"Old config judges new config" (PDF §73–§74) vs draft:** AGREE —
   kept as the governed self-improvement boundary (LAW + authority +
   verification for material change).

## Appendix C — Red-team carry-forward (F01–F19, reconciled 2026-09-30 20:13 PDT)

The pre-PDF draft's 19 red-team findings were reconciled into the draft
before this merge. This appendix carries each forward into the merged spec —
COVERED items live in the body above; AMENDED items refine the body as stated.

- **F01 (MAJOR, master functions unbound):** COVERED — §0.1 (13-function
  binding), Appendix B #3 (means-vs-verb planning-scope rule).
- **F02 (MAJOR, TRANSIENT retry):** AMENDED — §7's retry law is refined:
  same-execution retry only with failure-carried new information; otherwise a
  NEW execution under the same idempotency key (fresh linearization, not a
  retry). Master §6 invariant ("never retry without new information") stands.
- **F03 (MAJOR, key claim overstated):** AMENDED — §5's key derivation is
  corrected: keys are REQUIRED for consequential actions (the repair's actual
  contract: nullable column, partial index, `IDEMPOTENCY_KEY_REQUIRED`); the
  contract mandates uniqueness scope + conflict semantics. Key format is
  illustrative.
- **F04 (four paths as states):** COVERED — §2, §7, §8 (ASK_SUSPENDED,
  READ_MORE loop bound).
- **F05 (async onset):** AMENDED — async onset splits into tool-declared (the
  tool's contract declares async) vs timeout-triggered escalation, with a
  declared boundary per tool; `onset` is recorded in the receipt.
- **F06 (claim supersession):** AMENDED — pre-check hit on a dead CLAIM
  returns INCONCLUSIVE + `IDEMPOTENT_REPLAY_OUTCOME_MISSING`; claims are
  superseded with a persisted pointer, never blind-overwritten (§5).
- **F07 (lineage enforceability):** AMENDED — `decision_lineage_id` +
  `traversal_count` are carried on the DecisionReceipt input and the
  ExecutionReceipt; the §2 k-bound is enforced at LAW intake and auditable
  from receipts.
- **F08 (coalescing):** AMENDED — coalesced losers receive a ticket VIEW with
  `cancel_handle: null`; cancel authority stays with the claim owner (§5).
- **F09 (revocation):** AMENDED — the revocation check is
  `law.grantStatus(authorityBasis)` against LAW's temporal-validity
  machinery, cached with a validity TTL (§1).
- **F10 (predicate language):** OPEN — added as §10 Q10: name the
  deterministic predicate language over the fixed context schema.
- **F11 (path/outcome map):** AMENDED — each §2 path maps to its terminal
  outcomes per the §7 state machine; candidate-only PENDING/CANCELLED
  outcomes are flagged as such.
- **F12 (breaker/lease cold reconstruction):** COVERED — §8 (lease check;
  breaker and lease-heartbeat rows are ledger-persisted).
- **F13 (edge type):** AMENDED — the KNOW handoff names the ratified V2 edge
  type `PRODUCES` (§1.2); no contract extension.
- **F14 (V2.1 lineage):** COVERED — Appendix B #1 (binding ratified in main
  via #1186/#1190/#1192).
- **F15 (cross-ref):** COVERED — §1.3 ref corrected.
- **F16 (notify channel):** AMENDED — the Director notify channel is
  `director_notify`, a governed kernel channel (transport
  implementation-open), §2.
- **F17 (registry order):** AMENDED — registry order is ascending
  `registration_index` (§5); the deadlock-avoidance claim is grounded.
- **F18 (false law label):** COVERED — the "AskHuman Consequential
  Irreversibility law" label is struck; restated as candidate V2.1 machinery.
- **F19 (receipt replay):** COVERED — §9.2 acceptance is same-receipt replay
  (byte-identical receipts are impossible; replay returns the canonical
  record).
