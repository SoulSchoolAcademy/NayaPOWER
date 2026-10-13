# A Crashed Worker Loses Progress, Not Authority — Recover the Commit, Never Invent It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0919-crash-safe-governance-recovery
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Nayanet directive D54 — Crash-Safe Recovery for Governance Changes (AER-REC-1), appended to `NAYANET-DIRECTIVES-REGISTER.md` (enforcement/NAYANET-DIRECTIVES-REGISTER.md in the bring-naya-to-life hidden files); the D54 acceptance lab — Crash-Recovery Lab — was posted on the board at https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6102208936. Status at capture: NOT STARTED, owner TBD; the lab is supporting test design (synthetic scenarios), not executed test results.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Recover from an interrupted publication by reconstructing what actually committed — not by blindly replaying the operation or assuming a crashed worker means failure. The Crash-Safe Governance Recovery Law: NayaNET shall reconstruct interrupted governance operations from durable, authoritative commit evidence using stable logical identities. Canonical state transitions and their required receipts shall be atomic within a qualified durability boundary; asynchronous projections shall be replayable, idempotent, and nonauthoritative. Ambiguous commit outcomes shall not create authority. Recovery shall preserve historical evidence, prevent stale-state resurrection, respect current LAW and ACT eligibility, and retain independently qualified unaffected capabilities.

The first discipline is to classify the crash before choosing recovery: before commit (discard or revalidate against current state); during commit (query the authoritative transaction evidence by operation ID — never guess); after commit before acknowledgment (recover the committed result, never re-apply); after commit before projection (replay the derived publication from the committed receipt); during outbox delivery (redeliver idempotently); across multiple stores (contain and reconcile against the designated authority — this is a consistency breach, not a delayed dashboard); during external ACT execution (preserve the ambiguous outcome and reconcile independently before any further effect — authorization receipts never prove the effect happened). COMMIT_OUTCOME_UNKNOWN is an epistemic state, not proof of partial commit — no timeout ever auto-converts ambiguity to abort.

The design that makes recovery possible is deliberate: one serializable governance transaction (taxonomy + scope mappings + incident/qualification state + commit identity/receipt + durable outbox), commit-all-or-none, with asynchronous replayable projection (Brain index, Hub, notifications, successor views); consumers enforce idempotency and ordering. Durable operation identity: operation_id carries a unique constraint bound to the exact proposal hash — a retry with different payload bytes is an identity mismatch and is rejected; an already-committed operation returns the original result; a provably uncommitted one revalidates before re-attempt. Recovery runs under a fenced recovery lease, reads authoritatively, fences the old writer (an expired lease does not prove the old writer's commit was cancelled), rechecks authority at commit, and never invents a new proposal. Never replay an old projection over newer state: dedupe by event identity, track applied revisions, reject stale replacement snapshots — an epoch-81 merge event redelivered after an epoch-82 withdrawal must not resurrect the withdrawn qualification. Multi-store partial publication is handled by preference: one canonical authority boundary first; otherwise qualified distributed coordination; otherwise fail-closed containment and governed repair — a saga never makes multi-store changes retroactively atomic.

The D54 acceptance lab defines six concrete scenarios plus a verifier checklist: where exactly the crash happened (same crash, different recovery by commit outcome — a crash describes the worker's condition, not the transaction's outcome); withdrawal committed while an old event replays (STALE_REPLAY_REJECTED); baseline promotion crashing mid-commit (recover by independent reconstruction); partial publication across multiple stores (authoritative consistency breach — contain, reconstruct, governed repair); LAW authorized while ACT's external effect stays unknown (AMBIGUOUS_EXTERNAL_EFFECT — never infer the effect from the approval, never blindly retry the timeout); and two workers recovering the same operation (original operation ID + durable unique constraint + enforceable recovery fence → one authoritative logical state transition). The result NayaNET must demonstrate: "A crashed worker can lose its progress or acknowledgment, but it cannot create new authority, erase a withdrawal, or manufacture an external effect outcome." Recovery liveness is a separate fact: COMMITTED_PROJECTION_BLOCKED is a valid state — a recovery deadline escalates, never promotes an unverified outcome to PASS.

## 🩷 HUMAN NOTE

Picture a notary who collapses mid-appointment. The right question is not "what was she about to do?" — it's "what is actually on file?" If the deed was recorded, you recover the recorded deed; you do not re-file a new one. If the deed was never recorded, you re-check whether the filing is still valid and only then re-file. And if you genuinely cannot tell whether it was recorded, you sit with the uncertainty — you do not invent a filing, and you do not cancel the deal on a guess. That is the entire law in one image. The machinery behind it: every operation gets a permanent, unique identity; the authoritative record is one atomic write; everything else (dashboards, indexes, notifications) is a replayable copy that must accept duplicates gracefully. An old copy of the data arriving late (a notification from before the withdrawal) must be rejected, not applied over the newer truth. When two workers both try to clean up the same crash, they must converge on the one authoritative state — the identity constraint and the recovery fence guarantee that. And the boundary where honesty stops: if the system authorized an external action but the receipt got lost in the crash, you hold the outcome as ambiguous — you do not assume it happened, you do not assume it didn't, you reconcile it independently before touching anything again.

## 🟣 CHILD NOTE

Imagine you're building a tower and you drop your blocks right in the middle. When you pick them back up, the rule is: check what actually stayed standing — don't rebuild from memory, and don't pretend the whole tower fell if only the top did. If you're not sure whether a block stayed, you check — you don't glue one on and hope. And if your friend also tries to fix the same tower, you both follow the same rule: the blocks that are really there are the real tower. Old photos of the tower from before don't count — the tower you can touch right now is the truth.

## 🔵 GRANDMA NOTE

It's like the post office after a power cut. The clerk doesn't start over from memory or assume every letter on the desk was already mailed. She opens the ledger: what's marked "posted" is posted; what's marked "not yet" goes back through the normal checks; and anything she can't verify either way is set aside for investigation — never invented, never cancelled on a guess. The old mail truck coming back with yesterday's bag doesn't get to deliver letters that were recalled today. And two clerks cleaning up the same desk follow the same ledger, so there's exactly one truth about what went out.

## 🟠 NAYA NOTE

Apply the Crash-Safe Governance Recovery Law to every governance operation (scope merges/splits, provisional-scope creation, incident withdrawals, baseline promotions, LAW/ACT decisions): (1) classify the crash first — before commit / during commit / after commit before ack / after commit before projection / during outbox delivery / across stores / during external ACT — and let the classification choose the recovery, never a generic retry; (2) treat COMMIT_OUTCOME_UNKNOWN as epistemic — no timeout converts ambiguity to abort; (3) build recovery on one serializable governance transaction with atomic canonical state + receipts and an idempotent replayable outbox; make projections replayable, idempotent, nonauthoritative; (4) enforce durable operation identity — operation_id unique constraint bound to the exact proposal hash; different payload under the same ID is an integrity incident; (5) recover under a fenced recovery lease with an authoritative read, fence the old writer, recheck authority at commit, never invent a new proposal; (6) dedupe projections by event identity, track applied revisions, reject stale replacement snapshots — epoch ordering rules, newest evidence wins; (7) for external ACT: preserve AMBIGUOUS_EXTERNAL_EFFECT, reconcile independently by the original logical operation ID, retry only when current authority plus duplicate-prevention make it safe across all remaining possible histories — authorization ≠ effect; (8) keep recovery liveness separate from recovery correctness: COMMITTED_PROJECTION_BLOCKED is valid; deadlines escalate, never promote unverified outcomes to PASS. Run the lab scenarios as the acceptance bar: the verifier must distinguish crash-before-commit from crash-after-commit histories, must reject the epoch-81-over-82 replay, must catch removal of the outbox/ID-uniqueness/revision-fencing guards. Family notes: D53/SN-0918's atomic scope evolution law is the commit machinery this law recovers; D55's Safe Hold and Recovery Liveness Law is the liveness sibling (this law says what recovery may do; D55 says how to tell a correct hold from a stalled recovery).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "crash_recovery_authority_manufacture",
  "directive": "D54",
  "evidence": {
    "board": "#2175 comment 6102208936 — D54 acceptance lab (Crash-Recovery Lab) posted: six synthetic recovery scenarios + verifier checklist; synthetic demonstrations, not executed test results",
    "register": "hidden_files/enforcement/NAYANET-DIRECTIVES-REGISTER.md D54 (AER-REC-1) — full law, mechanics, C1–C15 crash matrix, four invariants R1–R4, sharpest case AER-REC-001; status NOT STARTED / owner TBD"
  },
  "rule": [
    "reconstruct interrupted governance operations from durable authoritative commit evidence using stable logical identities — never blindly replay, never assume crash means failure",
    "classify the crash before choosing recovery: before/during/after-commit (pre-ack, pre-projection), outbox delivery, multi-store, external ACT",
    "COMMIT_OUTCOME_UNKNOWN is epistemic — no timeout converts ambiguity to abort",
    "canonical state transitions + receipts atomic within a qualified durability boundary; projections replayable, idempotent, nonauthoritative",
    "operation_id unique constraint bound to exact proposal hash; different payload under same ID = integrity incident, refused",
    "recover under a fenced recovery lease, authoritative read, fence the old writer, recheck authority at commit, never invent a new proposal",
    "dedupe projections by event identity, track applied revisions, reject stale replacement snapshots — epoch-81 merge replayed after epoch-82 withdrawal must not resurrect the withdrawn qualification",
    "external ACT: preserve AMBIGUOUS_EXTERNAL_EFFECT; authorization receipt never proves the effect; reconcile independently by original logical operation ID",
    "recovery liveness is separate: COMMITTED_PROJECTION_BLOCKED is valid; deadlines escalate, never promote unverified outcomes to PASS"
  ],
  "lesson_line": "A crashed worker loses progress or acknowledgment — it cannot create new authority, erase a withdrawal, or manufacture an external effect outcome."
}
~~~
