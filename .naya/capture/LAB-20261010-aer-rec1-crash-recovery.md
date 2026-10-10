# Crash-Recovery Lab — companion to SN-0806 (AER-REC-1)

Source: Shawn, main chat, 2026-10-10. His word IS the verification.
Status: synthetic demonstrations of the proposed AER-REC-1 recovery contract —
NOT results from an executed NayaPOWER test. Fixture material for AER-REC-001.

## 0. The key distinction (interactive case)

The same worker crash requires very different recovery depending on whether the
authoritative transaction committed. A crash describes the worker's condition,
not the transaction's outcome.

- Crash BEFORE commit → establish whether it committed; otherwise discard or revalidate.
- Crash outcome UNKNOWN → reconcile authoritatively; hold dependents.
- Crash AFTER commit → recover the committed result; do not reapply.

Case C: withdrawal of B's qualification commits at epoch 82; worker crashes before
the Brain index refreshes (still shows epoch 81). Cached projections are stale, not
authoritative. Recovery: reconcile from the committed withdrawal receipt, replay its
outbox event. ACT refuses any new action relying on B's old certificate.

## 1. Withdrawal committed, old event replays

1. Epoch 81 publishes a shared statistical baseline for A and B.
2. Epoch 82 commits withdrawal of B's provider guarantee.
3. Projection worker crashes.
4. Old epoch-81 merge notification redelivered.
5. Restarted worker processes the epoch-82 withdrawal notification.

Result: A remains qualified if independently supported; B's withdrawal remains
authoritative. The consumer must not let epoch 81 overwrite epoch 82: deduplicate
event identities, reject stale snapshots, reconcile ordering from canonical state.
Expected: STALE_REPLAY_REJECTED, no resurrection of B's qualification.

## 2. Baseline promotion crashes during commit

Promotion of MODEL-20 prepared on taxonomy rev 14 / incident rev 27; connection drops
during commit.

| Independent reconstruction | Recovery decision |
|---|---|
| Durable record confirms MODEL-20 at baseline rev 20 | Recover the committed publication; do not promote again |
| Reliably established as aborted | Revalidate proposal against current state |
| Neither commit nor abort establishable | Keep COMMIT_OUTCOME_UNKNOWN; block dependent use if no sufficient current baseline |
| Another incident advanced the revision meanwhile | Reject stale proposal; reassess against new incident state |
| Same operation ID, different proposal hash | Integrity incident; refuse replay |

Success = correct canonical version + applicable qualifications + authorized promotion
receipt, without double-publishing or bypassing a newer incident.

## 3. Multiple authoritative stores partially commit (the hard case)

Taxonomy DB: new split committed. Qualification DB: old parent certificate still active.
ACT permission DB: old execution permission still active. This is NOT a stale cache —
authoritative systems disagree about whether a consequential operation is permitted.

Required: contain affected execution, reconstruct committed operations, determine
authoritative precedence, perform a governed repair. Never best-effort replay guessing
which database wins. Preferred prevention: one canonical transactional permission
boundary, other databases as projections. A saga may repair afterward but cannot
retroactively guarantee no stale authorization was exercised.

## 4. LAW authorized, ACT's external effect unknown

LAW authorization receipt and external effect receipt prove different things.
LAW committed + ACT request sent + acknowledgment lost ⇒ two possible histories
(provider committed / did not commit). Expected: AMBIGUOUS_EXTERNAL_EFFECT.
Do not infer the effect from LAW approval; do not blindly retry on ACT timeout.
Reconcile with the provider under the original logical operation ID. Another attempt
only if current authority + independently verified duplicate-prevention make it safe
across remaining possible histories. Governance recovery cannot manufacture
provider-side exactly-once.

## 5. Two workers recover the same operation

Two Nayas restart, both discover GOV-OP-904. Protocol: original operation ID + durable
unique constraint + enforceable recovery fence. Worker A acquires the fence and
recovers/commits the exact proposal; Worker B cannot become an independent writer —
reads the committed result or waits. An expired local lease does not prove Worker A's
submitted DB commit was cancelled; the DB protocol must serialize/fence the old writer.
Acceptance: ONE authoritative logical state transition.

## 6. Chaos-test checklist (AER-REC-001 planning)

- [ ] Crash immediately before a governance commit.
- [ ] Drop the acknowledgment after the commit succeeds.
- [ ] Crash after withdrawal commits but before index refresh.
- [ ] Replay an older merge after a newer withdrawal.
- [ ] Restart two recovery workers simultaneously.
- [ ] Simulate an authoritative multi-store partial publication.
- [ ] Send an external ACT request and lose its receipt.
- [ ] Verify unaffected scope A remains independently qualified.

Planning checklist only — marking a case does not run a test or constitute a
verification receipt.

## 7. What the independent verifier must prove

| Invariant | Expected result |
|---|---|
| Atomic authoritative publication | No partial canonical transaction state |
| Replay idempotency | One logical change under repeated recovery |
| Monotone eligibility | Withdrawn qualification never resurrected by older events |
| Evidence-preserving split | No child inherits unsupported proof |
| Ambiguous-outcome integrity | Unknown external effects stay unknown until independently resolved |
| Selective recovery | Unaffected independently qualified scopes stay available |
| Crash reconstruction | A cold successor reaches the same supported decision from durable evidence |

Mutation test: remove the projection revision guard → verifier must find a minimal
execution where an old event overwrites a newer withdrawal; restoring the guard
must prevent that trace.

## First executable fixture (AER-REC-001)

Crash After Withdrawal Commit, Before Publication. Scopes A and B; withdraw B's
qualification; crash immediately after canonical commit; replay an old merge event;
restart two recovery workers. Verifier: B stays unqualified, A preserves eligibility,
epoch never rolls backward, no new ACT permission from the stale merge. Then move
the crash before the authoritative commit and require a DIFFERENT reconstructed
outcome. The demonstrated result: "A crashed worker can lose its progress or
acknowledgment, but it cannot create new authority, erase a withdrawal, or
manufacture an external effect outcome."
