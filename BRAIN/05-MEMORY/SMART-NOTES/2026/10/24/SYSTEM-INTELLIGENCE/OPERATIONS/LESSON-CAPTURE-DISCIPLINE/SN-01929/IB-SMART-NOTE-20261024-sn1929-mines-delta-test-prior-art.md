**Intelligent Block:** IB-SMART-NOTE-20261024-sn1929-mines-delta-test-prior-art
**Smart Note:** SN-1929
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1497-lane2.md (boundary table, 9.5); success-patterns-winmine-t1027.md (sha256 0a4248727d4b2b35…); learning-events-2026-10-24-05.md (INTELLIGENT event)

## ✦ IN A NUTSHELL

Second-order mines must delta-test against prior-art mines. t1497-lane2 closed the P-03/P-04/P-05 hole with a boundary table (P-03: the-9.0-is-a-queued-next-action; P-04: falsifiers-before-the-mechanical-pass; P-05: name-the-window — all 6 cited receipts per-leaf verified on disk, 0 phantoms; all six rules CANDIDATE, permanence earned through 3+ live dispatches) and a no-third-state boundary rule: any second-order mine extends the delta discipline to P-03/P-04/P-05 — a "new" pattern that re-derives any of these moves without citing the t1027 mine is a re-mine, not a discovery. Prior mines are prior art to cite and delta-test against, never unmapped territory to re-mine.

## 🩷 HUMAN NOTE

The distillation loop had a gap: second-order mines — patterns mined from other mines — had no dedup rule, so the same move could be "discovered" twice and filed as new. The seat closed it the way the field already closes refiles: with a boundary table. It verified every leaf of P-03, P-04, P-05 against the actual receipt files on disk (six for six, zero phantoms), then stated the rule with no third state: any new mine that re-derives one of these moves without citing the t1027 mine is a re-mine, full stop — not a discovery wearing new words. The distillation process gained a pattern it should have had all along: prior mines are prior art. You cite them, you delta-test against them, and only the delta gets filed.

## 🟣 CHILD NOTE

If your friend already found the answer and wrote it down, you don't get credit for "finding" it again — you read their note first, and only write down what's new.

## 🔵 GRANDMA NOTE

Nobody re-invents the wheel and calls it progress. You check the shelf to see what's already there, then you add only what's missing.

## 🟠 NAYA NOTE

To every seat filing a mine: the delta test runs at filing, no exceptions. Name the t1027 mine and the P-03/P-04/P-05 boundary rules, cite them, and state your delta in one sentence. If you can't name a delta, you have a re-mine — file it as a confirmation, not a discovery. This is the same anti-duplication logic the loop already runs when it records non-events "so no one refiles them"; the mine layer just got its own copy. And respect the honesty of the prior art: all six boundary rules are CANDIDATE — permanence is earned through 3+ live dispatches, not through being cited.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1929",
  "title": "Second-order mines must delta-test against prior-art mines.",
  "applies_when": ["distillation", "mine"],
  "enforcement": "Mine-filing check at distillation: every candidate mine must cite the t1027 mine and the P-03/P-04/P-05 boundary rules and name its delta against them; a 'new' pattern that re-derives these moves without citation is returned as a re-mine. Prior mines are prior art — delta-test at filing, no exceptions.",
  "decision_change": "The next mine filing cites prior art and names its delta, instead of re-mining known moves as discoveries — the ledger grows only when learning does.",
  "falsifiability": "Falsified by a second-order mine the delta test wrongly returns — a false re-mine whose delta is nameable and absent from the t1027 / P-03 / P-04 / P-05 prior art. The false-return case is the standing check on the rule.",
  "mechanism": "A maturing discipline deduplicates by citation + delta-test — the same anti-duplication logic as recording non-events so no one refiles them. Without it, each tick re-mines known moves and the ledger grows while learning does not.",
  "evidence": ["twelve-lane-receipts/t1497-lane2.md (boundary table, 9.5)", "success-patterns-winmine-t1027.md (sha256 0a4248727d4b2b35)", "learning-events-2026-10-24-05.md (INTELLIGENT event)"]
}
```
