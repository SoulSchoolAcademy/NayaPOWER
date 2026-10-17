# WIRE RECEIPT — D60 fairness-debt bounds gate

**Date:** 2026-10-11 ~10:05Z (night shift)
**Lane:** WIRE (Naya 2's team)
**Directive:** D60 — Fairness-Debt Bounds Under Missing Evidence (AER-LIVE-5)
**Build:** PR #2315 (`drift_canary/fairness_debt_bounds.py`, 23/23 tests green) — BUILT AS CODE, unwired.
**Status after this wire:** WIRED-AT-SEAM, DORMANT-PENDING-MERGE. No merge from the wire lane — Shawn pulls triggers.

## What was wired

The D60 bound engine (`DebtBoundEngine.compute`) onto the fairness CI path:

| File | Role |
|---|---|
| `tools/d60_fairness_debt_bounds_gate.py` | The gate: judges each manifest claim against the REAL engine. Exit 0 pass/dormant, 1 violation, 2 fail-closed. |
| `tools/d60_fairness_debt_bounds_manifest.json` | Claims register. Ships with `"claims": []` — explicit DORMANT, plus a worked `_example` (dormant). |
| `tests/test_d60_fairness_debt_bounds_gate.py` | 24 tests, fake-mechanism injection (mechanism not on this tree yet). |
| `.github/workflows/d60-fairness-debt-bounds.yml` | The live path: runs on `pull_request` + `push: main`, path-filtered to the engine, its D58/D59 dependencies, the gate, the manifest, and itself. |

## Operating path now protected

The fairness CI path: any PR touching `drift_canary/fairness_debt_bounds.py` (or its D58/D59 dependencies, the gate, or the manifest) must pass the gate, and every push to `main` touching those paths re-runs it. The first claim merged into the manifest activates enforcement with zero new wiring.

## Proof the wiring works (L215)

1. **Gate tests:** 24/24 green (fake mechanism).
2. **Fire battery (not committed):** the same gate judged against the REAL #2315/#2313/#2311 bytes — a violating claim goes RED (exit 1), an honest claim goes green (exit 0).
3. **TEMP-PROOF on the branch:** a temporary commit registered a live violating claim (proven BREACH asserted as NO_BREACH) — the gate went RED (exit 1) as required; the commit was then reverted, restoring explicit DORMANT (exit 0). Both directions proven; the temp commit is not in the PR.
4. **YAML parsed** as valid workflow; **fail-closed** proven (corrupt manifest → 2, claims without mechanism → 2, engine refusal → 2).

## What the gate blocks

- Proven BREACH: every defensible history over the bound — blocked until repaired.
- Bound-laundering: asserting NO_BREACH where the engine finds BREACH or UNRESOLVED; asserting BREACH where the engine clears; manufacturing doubt where the engine settles.
- D60's distinctive coverage: windows with many unresolved rounds that exceed D59's 2^12 enumeration cap are bounded exactly here in O(N) — claims about those windows are now judgeable at all.

## What remains unwired

- D65 (build PR #2327 shipped 10:00Z — next wire candidate).
- D62 fix lane; #2294 (directive-register CLI, not gate-shaped); #2244 reqs; naya4/naya5 owner lanes.
- All wire PRs (including this one) await the merge lane. Until merged, every wire is DORMANT — CODE-ONLY at the wire layer per L215, honestly stated.
