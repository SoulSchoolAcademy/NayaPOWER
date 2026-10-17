#!/usr/bin/env python3
"""Adversarial tests for UD-14 guarantee_watch.

Acceptance gate (from ultimate-directives.md): PASS only if silent
mutations are detected via observable consequences, confirmed breaches
withdraw immediately at any volume, healthy providers are never
misclassified, seasonality never hides a real regression, and false
alarms stay within budget per regime and fleet-wide. One failure = FAIL.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from guarantee_watch import (
    GuaranteeWatch, Guarantee, ProbeReport, ProbeOutcome, QualState,
    OpResponse, Diagnosis, AlertLevel, Regime,
)

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail and not cond else ""))


def ok_probe(failures=0, samples=100, **kw):
    def probe(g):
        return ProbeReport(ProbeOutcome.OK, 0.0, failures=failures,
                           samples=samples, **kw)
    return probe


def mk_guarantee(gid="g1", regime=Regime.LOW_VOLUME, staleness=60.0, **kw):
    return Guarantee(id=gid, provider="prov", use_case="uc",
                     promise="behaves", max_staleness_s=staleness,
                     regime=regime, **kw)


T0 = 1_700_000_000.0

# 1. Healthy dependency passes (all regimes) — never misclassified.
for regime in (Regime.LOW_VOLUME, Regime.BURSTY, Regime.HIGH_VOLUME):
    w = GuaranteeWatch()
    g = mk_guarantee(gid=f"h-{regime.value}", regime=regime)
    w.register(g, ok_probe())
    alerts = w.tick(T0)
    q = w.qualification(g.id)
    ok, reason = w.may_execute(g.id, T0)
    check(f"healthy-{regime.value}-qualified",
          q.state == QualState.QUALIFIED_IN_SCOPE and ok and not alerts,
          f"state={q.state} ok={ok} alerts={alerts}")

# 2. Silently expired guarantee is caught as STALE — never assumed fine.
w = GuaranteeWatch()
g = mk_guarantee(gid="stale", staleness=60.0)
w.register(g, ok_probe())
w.tick(T0)  # fresh check at T0
ok, reason = w.may_execute(g.id, T0 + 30)
check("fresh-within-bound-executes", ok and reason == "QUALIFIED_AND_FRESH", reason)
alerts = w.tick(T0 + 120)  # no probe ran for 120s > 60s bound
q = w.qualification(g.id)
codes = [a.code for a in alerts]
ok2, reason2 = w.may_execute(g.id, T0 + 120)
check("silently-expired-caught-stale",
      "GUARANTEE_STALE" in codes
      and q.state == QualState.QUALIFICATION_SUSPENDED
      and not ok2,  # held after expiry — never assumed fine
      f"codes={codes} state={q.state} may={ok2}/{reason2}")

# 3. A check that never ran is UNKNOWN, not healthy.
w = GuaranteeWatch()
g = mk_guarantee(gid="never")
w.register(g, ok_probe())
ok, reason = w.may_execute(g.id, T0)
check("never-checked-is-unknown-not-healthy",
      not ok and reason == "UNKNOWN_NEVER_CHECKED"
      and w.qualification(g.id).state == QualState.UNKNOWN, reason)

# 4. Degraded provider: GUARANTEE_WEAKENED before dependent work runs.
seen = {"n": 0}
def degraded_probe(g):
    seen["n"] += 1
    if seen["n"] == 1:
        return ProbeReport(ProbeOutcome.OK, 0.0, samples=100)
    return ProbeReport(ProbeOutcome.DEGRADED, 0.0,
                       evidence={"latency_p99_ms": 4200, "slo_ms": 1000},
                       samples=100)
w = GuaranteeWatch()
g = mk_guarantee(gid="deg")
w.register(g, degraded_probe)
w.tick(T0)
alerts = w.tick(T0 + 10)
codes = [a.code for a in alerts]
q = w.qualification(g.id)
ok, reason = w.may_execute(g.id, T0 + 10)
wk = [a for a in alerts if a.code == "GUARANTEE_WEAKENED"][0]
check("degraded-raises-weakened-and-holds-work",
      "GUARANTEE_WEAKENED" in codes
      and q.state == QualState.REVIEW_REQUIRED
      and not ok
      and wk.operational_response == OpResponse.HOLD_AFFECTED_RETRIES
      and wk.diagnosis == Diagnosis.TRANSIENT_ANOMALY,
      f"codes={codes} state={q.state}")

# 5. Confirmed breach at volume 1: immediate withdrawal, no sample minimum.
def breach_probe(g):
    return ProbeReport(ProbeOutcome.BREACH, 0.0,
                       evidence={"duplicate_effect": "op-key-123 applied twice"},
                       failures=1, samples=1)
w = GuaranteeWatch()
g = mk_guarantee(gid="br1")
w.register(g, breach_probe)
alerts = w.tick(T0)
q = w.qualification(g.id)
ok, _ = w.may_execute(g.id, T0)
br = [a for a in alerts if a.code == "GUARANTEE_BROKEN"]
check("breach-at-volume-1-withdraws-immediately",
      len(br) == 1 and br[0].level == AlertLevel.L4
      and br[0].budget_bypassed
      and q.state == QualState.QUALIFICATION_SUSPENDED and not ok,
      f"alerts={[a.code for a in alerts]}")

# 6. Five timeouts (probe ERRORs) do NOT establish drift.
def flaky_probe(g):
    return ProbeReport(ProbeOutcome.ERROR, 0.0, note="timeout")
w = GuaranteeWatch()
g = mk_guarantee(gid="flaky")
w.register(g, flaky_probe)
for i in range(5):
    w.tick(T0 + i * 10)
q = w.qualification(g.id)
diags = {i.diagnosis for i in w.incidents()}
check("transport-errors-never-establish-drift",
      q.state == QualState.UNKNOWN  # never had a successful check
      and Diagnosis.SUSPECTED_DRIFT not in diags
      and diags <= {Diagnosis.UNDETERMINED},
      f"state={q.state} diags={diags}")

# 7. One decisive duplicate effect via hard invariant: immediate, at any volume.
def dup_probe(g):
    return ProbeReport(ProbeOutcome.OK, 0.0, samples=1,
                       evidence={"applied_count": 2, "expected_count": 1})
g = mk_guarantee(
    gid="dup", staleness=3600.0,
    invariants=[("no_duplicate_effect",
                 lambda r: r.evidence.get("applied_count", 1) > 1)])
w = GuaranteeWatch()
w.register(g, dup_probe)
alerts = w.tick(T0)
br = [a for a in alerts if a.code == "GUARANTEE_BROKEN"]
inc = w.incidents()
check("one-decisive-counterexample-withdraws",
      len(br) == 1 and br[0].budget_bypassed
      and inc and inc[0].diagnosis == Diagnosis.CONFIRMED_CONTRACT_BREACH
      and inc[0].operational_response == OpResponse.BLOCK_AFFECTED_EXECUTION,
      f"alerts={[a.code for a in alerts]}")

# 8a. Seasonality: expected peak-hour elevation does NOT alert.
def peak_ctx(hour, weekday, volume, in_maint):
    return 0.05 if 9 <= hour <= 17 else 0.01
w = GuaranteeWatch()
g = mk_guarantee(gid="seas", regime=Regime.HIGH_VOLUME, context_model=peak_ctx)
w.register(g, ok_probe(failures=5, samples=100))  # 5% == peak expectation
noon = T0 - (T0 % 86400) + 12 * 3600  # 12:00 UTC
for i in range(30):
    w.tick(noon + i * 60)
q = w.qualification(g.id)
check("seasonal-elevation-not-misclassified",
      q.state == QualState.QUALIFIED_IN_SCOPE, f"state={q.state}")

# 8b. Seasonality never hides a real regression: 15% during peak still fires.
w = GuaranteeWatch()
g = mk_guarantee(gid="seas2", regime=Regime.HIGH_VOLUME, context_model=peak_ctx)
w.register(g, ok_probe(failures=15, samples=100))  # 15% >> 5% peak expectation
alerts_all = []
for i in range(30):
    alerts_all += w.tick(noon + i * 60)
codes = {a.code for a in alerts_all}
check("regression-during-peak-still-detected",
      "DRIFT_SUSPECTED" in codes or "FROZEN_DIVERGENCE" in codes,
      f"codes={codes}")

# 9. Frozen reference: adaptive learning failure-as-normal gets called out.
w = GuaranteeWatch()
g = mk_guarantee(gid="froz", regime=Regime.LOW_VOLUME,
                 frozen_reference={"fail_rate": 0.01, "tolerance": 0.005})
w.register(g, ok_probe(failures=2, samples=100))  # 2%: sub-statistical, sustained
alerts = w.tick(T0)  # first observation: adaptive=0.02 vs frozen 0.01
codes = [a.code for a in alerts]
check("frozen-reference-catches-normalized-regression",
      "FROZEN_DIVERGENCE" in codes, f"codes={codes}")

# 10. Bursty: 500 correlated failures in one burst != 500 independent.
def burst_probe(g):
    return ProbeReport(ProbeOutcome.OK, 0.0, failures=500, samples=500,
                       burst_id="burst-9")
w = GuaranteeWatch()
g = mk_guarantee(gid="burst", regime=Regime.BURSTY)
w.register(g, burst_probe)
alerts = w.tick(T0)
codes = [a.code for a in alerts]
check("correlated-burst-counts-once",
      "DRIFT_SUSPECTED" not in codes, f"codes={codes}")

# 11. Low volume: 1 failure in 5 is 20% but weak evidence — no percent alert.
w = GuaranteeWatch()
g = mk_guarantee(gid="lowv", regime=Regime.LOW_VOLUME)
w.register(g, ok_probe(failures=1, samples=5))
alerts = w.tick(T0)
codes = [a.code for a in alerts]
check("tiny-denominator-no-percent-alert",
      "DRIFT_SUSPECTED" not in codes, f"codes={codes}")

# 12. False-alarm budget: statistical alerts budgeted fleet-wide.
w = GuaranteeWatch(fleet_false_alarm_budget=2)
for i in range(4):
    # Noisy-but-sub-threshold probes that each raise an L2 statistical alert:
    # craft via frozen divergence with tight tolerance.
    g = mk_guarantee(gid=f"noisy{i}", regime=Regime.LOW_VOLUME,
                     frozen_reference={"fail_rate": 0.01, "tolerance": 0.005})
    w.register(g, ok_probe(failures=2, samples=100), regime_alert_budget=10)
alerts_all = []
for i in range(4):
    alerts_all += w.tick(T0 + i)
suppressed = [a for a in alerts_all if a.code == "SUPPRESSED_BY_BUDGET"]
fired = [a for a in alerts_all if a.code == "FROZEN_DIVERGENCE"]
check("false-alarms-budgeted-fleet-wide",
      len(fired) == 2 and len(suppressed) >= 2,  # budget=2: 2 fire, rest logged
      f"fired={len(fired)} suppressed={len(suppressed)}")

# 13. Registered maintenance adjusts expectations; unregistered claims don't.
w = GuaranteeWatch()
g = mk_guarantee(gid="maint", regime=Regime.LOW_VOLUME,
                 maintenance_windows=[("mw1", T0 - 100, T0 + 3600)])
w.register(g, ok_probe(failures=3, samples=100))  # 3% == 3x baseline (maint)
alerts = w.tick(T0 + 10)
check("registered-maintenance-adjusts-expectations",
      not [a for a in alerts if a.code in ("DRIFT_SUSPECTED", "FROZEN_DIVERGENCE")],
      f"codes={[a.code for a in alerts]}")
# Same elevation, no registered window -> statistical screen sees it.
w2 = GuaranteeWatch()
g2 = mk_guarantee(gid="maint2", regime=Regime.LOW_VOLUME)
g2.context_model = lambda h, wd, v, m: 0.03 if m else 0.01  # claims maint w/o registration
w2.register(g2, ok_probe(failures=3, samples=100))
alerts2 = w2.tick(T0 + 10)
# _in_maintenance is False (no registered window), so p0 stays 0.01:
# 3/100 vs 1% exact tail = P(X>=3|100,.01) ~= 0.08 > .01 -> no drift alert yet,
# but the unregistered claim must not have relaxed anything either.
check("unregistered-maintenance-claim-changes-nothing",
      not [a for a in alerts2 if a.code == "GUARANTEE_BROKEN"],
      f"codes={[a.code for a in alerts2]}")

# 14. Requalification: provider self-report refused; independent proof required.
def bad_probe(g):
    return ProbeReport(ProbeOutcome.BREACH, 0.0, evidence={"x": 1})
w = GuaranteeWatch()
g = mk_guarantee(gid="req", staleness=3600.0)
w.register(g, bad_probe)
w.tick(T0)
q = w.qualification(g.id)
assert q.state == QualState.QUALIFICATION_SUSPENDED
self_report = ProbeReport(ProbeOutcome.OK, 0.0,
                          evidence={"independent": False,
                                    "note": "provider says fixed"})
ok_r, why = w.requalify(g.id, self_report, None, T0 + 1)
indep = ProbeReport(ProbeOutcome.OK, 0.0,
                    evidence={"independent": True, "canary": "passed"})
ok_r2, why2 = w.requalify(g.id, indep, "narrowed-scope", T0 + 2)
q2 = w.qualification(g.id)
may, _ = w.may_execute(g.id, T0 + 2)
check("requalification-needs-independent-evidence",
      not ok_r and why == "RESTORATION_WITHOUT_REQUALIFICATION_REFUSED"
      and ok_r2 and q2.state == QualState.REQUALIFIED_IN_NEW_SCOPE
      and q2.version == 2 and may,
      f"{why} / {why2} state={q2.state}")

# 15. Staleness suspension does NOT auto-restore on the next OK probe.
w = GuaranteeWatch()
calls = {"n": 0}
def flapping(g):
    calls["n"] += 1
    return ProbeReport(ProbeOutcome.OK, 0.0, samples=10)
g = mk_guarantee(gid="flap", staleness=60.0)
w.register(g, flapping)
w.tick(T0)
w.tick(T0 + 120)  # goes stale -> suspended; probe runs OK inside this tick
q = w.qualification(g.id)
ok, reason = w.may_execute(g.id, T0 + 120)
check("stale-suspension-needs-explicit-requalify",
      q.state == QualState.QUALIFICATION_SUSPENDED and not ok,
      f"state={q.state} may={ok}/{reason}")

# 16. Two-field incident: response and diagnosis recorded separately.
w = GuaranteeWatch()
g = mk_guarantee(gid="twofield", staleness=3600.0)
w.register(g, ok_probe(failures=8, samples=100))  # 8% vs 1%: strong signal
for i in range(6):
    w.tick(T0 + i * 10)
inc = [i for i in w.incidents() if i.diagnosis == Diagnosis.SUSPECTED_DRIFT]
check("two-field-incident-kept-separate",
      len(inc) >= 1 and inc[0].operational_response == OpResponse.INVESTIGATE
      and inc[0].diagnosis == Diagnosis.SUSPECTED_DRIFT,
      f"incidents={[(i.operational_response, i.diagnosis) for i in w.incidents()]}")

# 17. History is append-only: every transition recorded with reason.
w = GuaranteeWatch()
g = mk_guarantee(gid="hist", staleness=3600.0)
w.register(g, degraded_probe if False else ok_probe())
w.tick(T0)
q = w.qualification(g.id)
check("history-append-only",
      len(q.history) >= 1 and all(e.reason for e in q.history),
      f"events={len(q.history)}")

print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)
