# UD-01 — Learning-Trial Harness

**Plain words:** a lesson isn't learned when it's stored — it's learned when behavior
measurably improves. This is the trial machinery that proves it: three arms
(control / correct lesson / wrong lesson), blind scoring, sealed fixtures, six
scripted gate checks, and a net-value ledger.

## Files

- `tools/learning_trial.py` — the harness (stdlib only)
- `tools/test_learning_trial.py` — 28 adversarial checks, all green
- `tools/learning-trial-README.md` — this file

Built on the frozen D1 Trial 1 pilot fixtures
(`hidden_files/d1-trial/fixtures/`); duplicates nothing.

## The protocol (enforced in code, not just documented)

1. **Runner** receives `tasks.json` + `lessons.json` ONLY. Hashes are verified
   against `seal-receipt.json` before any trial runs; any mismatch →
   `TAMPERED_FIXTURES`, no trials run. The runner never opens
   `answer-keys.sealed.json` (every file it opens is audited).
2. Results are keyed by blind IDs (`B001…B036`). The arm→task mapping is written
   to a separate sealed file the scorer only receives at scoring time.
3. **Scorer** (a different seat) verifies the sealed-keys hash first — mismatch →
   the trial is `VOID`, not scored. Unblinded input (arm/task labels in results)
   → `UNBLINDED_INPUT`, refused. The reveal (timestamp, scorer identity,
   hash-check result) is logged in the scoring receipt.
4. **Six gates** (truth / understanding / effect / causality / durability /
   transfer) run over the scored trial. Overall PASS only if all six hold.
   Durability FAILs honestly (`DURABILITY_NOT_RUN`) until the +7d delayed
   repeat exists — absence is never a silent pass.
5. **Net value ledger**: verified value (effect × value-per-point, declared
   estimated model) minus trial cost. Positive net required.

## The six gates

| Gate | What it checks |
|---|---|
| truth | every observed verdict matches the sealed expected verdict |
| understanding | treatment arm's per-span classifications match the lesson's mechanism (not just the verdict) |
| effect | Newcombe 95% CI for (treatment − control) excludes zero, diff > 0 |
| causality | wrong-lesson arm does not beat control; control ran first (no leakage) |
| durability | delayed-repeat receipt exists, hash-consistent, effect holds |
| transfer | guard tasks (sealed truth FAIL) stay FAIL under treatment — no blind PASSing |

## Demonstrated on the sealed pilot fixtures

With faithful arm-theory simulators (no sealed keys in the simulators):
CONTROL 0/12, TREATMENT 7/12, WRONG_LESSON 0/12; effect diff = 0.583,
95% CI [0.225, 0.807] — excludes zero. Gates: truth, understanding, effect,
causality, transfer PASS; durability FAILs honestly (delayed repeat not run).

## Honest findings and non-claims

- **Stale prose in the fixture README:** it claims an expected "CONTROL 5/12,
  TREATMENT 12/12, WRONG_LESSON 5/12", but its own task table and the sealed
  key say 0/12, 7/12, 0/12. The sealed key governs; the harness follows the
  key, not the prose. The fixtures themselves were NOT altered (sealed means
  sealed) — this is flagged for the trial owner.
- The simulators implement arm theories, not agents. A green harness proves the
  machinery (blinding, scoring, gates, refusals) — not that learning occurred.
  The live trial still needs real agents, the delayed repeat, and ≥30 tasks.
- The net-value model is declared-estimated, not measured. Parameters are
  explicit so the verdict is auditable.
- The six gates are scripted checks a verifier runs; "a different seat's
  verifier" is a procedural requirement the code supports (separate scorer
  identity, logged) but cannot itself enforce.
