# UD-16 — One Order for Changing Rules

**Plain words:** rules change through one ordered process, never by side
channels. A single writer, a clear sequence, every change authorized and
recorded. No seat rewrites the rules mid-game. And when a worker crashes
mid-change, recovery reconstructs what actually committed from durable
evidence — it never invents a new outcome and never treats ambiguity as
permission.

Absorbs D53, D54. Serves deal criterion 4.

## The one order

```
PROPOSED -> PREPARED -> VERIFIED -> AUTHORIZED -> COMMITTED -> PROPAGATED
```

Every committed change advances a monotonic governance epoch. Commits lock
the ledger and re-read governing state atomically.

## Guards

| Guard | Refusal code |
|---|---|
| Only authorized changers may propose/authorize | `UNAUTHORIZED_PROPOSER`, `UNAUTHORIZED_AUTHORITY` |
| One change in flight per rule | `RULE_IN_FLIGHT` |
| Proposal must match current rule text | `STALE_BASE` |
| Reason + evidence meet the bar | `INSUFFICIENT_EVIDENCE` |
| Verifier ≠ proposer | `SELF_VERIFY` |
| Commit only at the current epoch | `OUT_OF_ORDER` |
| Proposal bytes unchanged since prepare | `PROPOSAL_TAMPERED` |
| Stale events can't overwrite newer state | `STALE_REPLAY` |
| Decisions opened under old rules are voided on commit | `MID_DECISION_REWRITE` |

A prepared-but-uncommittable change (stale base epoch) is explicitly
`abort()`ed — journaled, rule freed — then re-proposed fresh. Rules can
never wedge in flight.

## Crash recovery (D54)

Recovery states: `PREPARED` / `COMMIT_OUTCOME_UNKNOWN` / `COMMITTED` /
`PROJECTION_PENDING` / `INDEPENDENTLY_VERIFIED`.

The durable store is ground truth: a `COMMIT_INTENT` in the journal with
no matching durable application means the commit did NOT happen. While an
outcome is unknown, `has_authority()` returns `False` — ambiguity is never
permission. Idempotent replay returns the original receipt, never
double-applies.

## Mid-game protection

A decision records the epoch it opened under. If a rule change commits
while it is open, the decision is voided (`VOIDED_MID_DECISION_REWRITE`)
and must re-run under the new epoch. Live demo:

```
decision D-101 opened at epoch 0 | valid: True
rule change committed -> epoch 1
decision D-101 status: VOIDED_MID_DECISION_REWRITE | valid: False
re-run D-102 at epoch 1 | valid: True
```

## Tests

`test_rule_change_order.py` — 27 adversarial tests, all green:
positive paths, all refusal codes, the crash matrix (crash at every
load-bearing point), race fixtures in both orders, and guard-removal
mutations proving each guard is load-bearing (removing one lets the
attack through — a detectable counterexample).

## What this does NOT claim

The gate proves a change followed the one order; it does not prove the
new rule text is wise. The crash matrix covers the load-bearing crash
points of this model, not a literal C1–C15 of every deployment. A PASS
certifies the tested interleavings only.
