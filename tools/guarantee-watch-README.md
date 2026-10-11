# Guarantee Watch — UD-14 "WATCH OUTSIDE GUARANTEES"

Every guarantee we depend on from the outside world is watched. When an
outside guarantee weakens or breaks, we know before it hurts us — never after.

## The job

`tools/guarantee_watch.py` (stdlib only) implements the watch registry:

1. **Register** each external dependency with its guarantee: what it
   promises, how we check it (an independent probe — never the provider's
   own word), and how fresh the check must be.
2. **Probe on schedule** (`tick(now)`); every result is recorded with
   append-only qualification history.
3. **Hold dependent work** on unknown or stale guarantees — never execute
   on them.

## The two decisions (D46) — never conflated

Every incident carries both fields separately:

| Field | Question | Values |
|---|---|---|
| Operational response | Is it safe to continue right now? | CONTINUE / OBSERVE / INVESTIGATE / HOLD_AFFECTED_RETRIES / BLOCK_AFFECTED_EXECUTION |
| Diagnosis | Has drift actually been established? | HEALTHY / TRANSIENT_ANOMALY / SUSPECTED_DRIFT / CONTRACT_SCOPE_CHANGE / CONFIRMED_CONTRACT_BREACH / UNDETERMINED |

Five timeouts never establish drift. One decisive duplicate effect
withdraws the guarantee immediately — no sample minimum.

## Fast gate, slow diagnosis

- **Fast safety gate:** a hard-invariant breach (or an observed breach)
  fires `GUARANTEE_BROKEN` at alert level L4 immediately, blocks affected
  execution, and bypasses the false-alarm budget entirely.
- **Slow diagnosis:** statistical suspicion fires `DRIFT_SUSPECTED` (L2,
  investigate). Suspicion alone never withdraws a guarantee.

## Calibration (D47)

Statistical thresholds adapt to the traffic regime:

- **LOW_VOLUME** — exact binomial tail tests on counts. Never percent
  thresholds on tiny denominators (1 failure in 5 is 20% but weak evidence).
- **BURSTY** — correlated bursts collapse to effective independent
  observations (one burst ≈ one observation). 500 related failures in one
  burst ≠ 500 independent confirmations.
- **HIGH_VOLUME** — paired short/long windows plus a minimum material
  effect; significance alone never pages.

False alarms are budgeted per regime and fleet-wide. Statistical alerts
beyond budget are logged (`SUPPRESSED_BY_BUDGET`), not paged. Safety
alerts (L3/L4) always fire.

## Contextual integrity (D48)

Providers are judged against what is expected under comparable conditions
(hour, weekday, volume, registered maintenance) via a declared,
inspectable context model. Expected fluctuations adjust statistical
expectations but **never relax hard invariants**. A frozen qualification
reference sits beside the adaptive forecast: if the adaptive model starts
treating elevated failure as normal while conditions say it isn't,
`FROZEN_DIVERGENCE` fires.

## Requalification

Provider restoration never restores authority automatically.
`requalify()` requires an independently verified passing probe
(`evidence["independent"] == True`) and bumps the qualification version.
A provider's own "we fixed it" is refused with
`RESTORATION_WITHOUT_REQUALIFICATION_REFUSED`.

## Quick start

```python
from guarantee_watch import *

w = GuaranteeWatch()
g = Guarantee(id="payments", provider="payprov", use_case="charge",
              promise="no duplicate charges; 24h retention",
              max_staleness_s=300.0, regime=Regime.HIGH_VOLUME,
              invariants=[("no_duplicate_effect",
                           lambda r: r.evidence.get("applied_count", 1) > 1)])
w.register(g, my_independent_probe)
alerts = w.tick(time.time())
ok, reason = w.may_execute("payments", time.time())
```

## Tests

`tools/test_guarantee_watch.py` — 22 adversarial cases, all green. Covers
the full acceptance gate: silent expiry caught as stale, breach at volume
1, transport errors never establishing drift, seasonality not hiding
regression, frozen reference catching normalized failure, burst
correlation, tiny denominators, false-alarm budgets, maintenance
scoping, independent requalification, and the two-field incident record.

## What this does NOT claim

The watcher judges the guarantees it is given via the probes it is given;
it cannot detect a provider behavior change that no probe observes. A
PASS covers only the checked use case, never the provider in general.
The contextual model is declared, not fitted; sequential detection is
paired windows, not CUSUM/EWMA.
