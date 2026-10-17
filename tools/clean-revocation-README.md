# UD-11 — Withdraw Bad Evidence Cleanly, Keep the Good

When evidence loses its right to certify, we revoke at the smallest
defensible unit, recompute exactly what depended on it, and keep everything
independently supported. Crashes and replays can never resurrect what was
withdrawn.

## What it is

`clean_revocation.py` (stdlib only) unifies the D11/D33/D34/D35/D36
machinery into one executable engine:

1. **Append-only eligibility ledger.** Evidence content is immutable history;
   only eligibility changes, as receipts. Claims carry explicit AND/OR
   support paths. Revocation is two-stage: *impact discovery* (the affected
   closure, including derivation taint) → *topological requalification*
   under one consistent evidence-policy snapshot.
2. **Per-surface projection manifests** (summary, note, index, successor)
   with qualification generations and a **read-time gate** on every
   authority-bearing route. Stale projections are refused as current —
   including mid-refresh.
3. **Atomic compare-and-swap publication with fencing tokens.** A delayed
   writer's old PASS can never be published over a newer revocation.
   Writers rebase and recompute; they never blindly retry. The fencing
   token proves *when* a worker read — it never overrides version checks.
4. **The Revocation Linearization Law, model-checked.** One commit point
   (the revocation commit). An executable bounded model enumerates every
   distinct interleaving of six race scenarios and checks S1–S6:
   no stale certification (S1), no stale publication (S2), no stale
   action (S3), revision monotonicity / no ABA reuse (S4), no replay
   resurrection (S5), independent-support preservation (S6).
   Four guard-removal mutants (publication check, action fence, revision
   monotonicity, replay reconciliation) each yield a counterexample.
5. **Smallest-unit compromise.** Evidence carries fragments; revoking one
   fragment invalidates exactly the paths that required it.

Verdict vocabulary is shared with `drift_canary.revocation` on main
(UNAFFECTED / REQUALIFIED / DOWNGRADED / INSUFFICIENT_DATA / SUSPENDED /
REVOKED) — same names, same meaning, not redefined.

## What it proves (acceptance gate)

- Revocation recomputes **exactly** the affected closure; unrelated claims
  are not even visited, let alone revoked.
- Stale publications are rejected (write-conflict and stale-dependency).
- Replay cannot resurrect withdrawn eligibility (idempotent, monotonic,
  resurrection refused); crash recovery reconstructs the committed state
  from the receipt log.
- Independent requalification is permitted (new evidence, higher revision
  — never ABA reuse).
- S1–S6 hold across all enumerated interleavings on the clean machine;
  every mutant yields a counterexample.
- A mark-everything-REVOKED engine and an ignore-the-revocation engine
  both fail this suite — selectivity is what's under test.

## Run

```
python3 tools/test_clean_revocation.py
```

## What this does NOT claim

- The model checker is **bounded** (six scenarios, small op multisets) —
  it is not TLA+/TLC and does not prove the unbounded system.
- This is SPEC + executable machinery. It is **not wired** into kernel/,
  KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word.
- The refinement proof (concrete engine implements the abstract law on a
  real store, with real-concurrency fault injection) belongs to UD-12's
  machinery, not this module.
- Requalification judges **certification standing, not truth**. Revoking
  "scheduler caused this outage" does not establish it didn't.
