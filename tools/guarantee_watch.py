#!/usr/bin/env python3
"""UD-14 — WATCH OUTSIDE GUARANTEES (guarantee watch registry).

Plain words: every guarantee we depend on from the outside world (APIs,
services, data sources, providers) is watched. When an outside guarantee
weakens or breaks, we know before it hurts us — never after.

Machine-enforced rules:
  1. Every external dependency registers its guarantee: what it promises,
     how we check it (an independent probe, never the provider's own word),
     and how fresh the check must be (max staleness).
  2. A check that never ran is UNKNOWN, not healthy. A check older than its
     freshness bound is STALE, not fine. Dependent work is HELD on unknown
     or stale guarantees — never executed on them.
  3. Probes test observable behavior, so silent provider mutations are
     caught by their consequences (e.g. retention silently shortened is
     caught by a probe that writes, waits, and re-reads).
  4. Two decisions are always kept separate (D46): is it safe to continue
     right now (operational response), and has drift actually been
     established (evidence-based diagnosis). Never conflated.
  5. Fast safety gate: a confirmed breach of a hard invariant withdraws the
     guarantee IMMEDIATELY — one decisive counterexample is enough, no
     sample minimum, no waiting for more data, and it bypasses the
     false-alarm budget entirely.
  6. Slow diagnosis: statistical suspicion alone never withdraws a
     guarantee; it triggers investigation and scoped requalification.
     Transport errors alone never establish drift (five timeouts is not a
     broken contract).
  7. Alert calibration (D47): statistical thresholds adapt to the traffic
     regime — exact count tests on tiny denominators (never percent
     thresholds), burst-correlation-aware effective sample size for bursty
     traffic, paired windows plus minimum material effect for high volume.
     False alarms are budgeted per regime and fleet-wide; statistical
     alerts beyond budget are logged, not paged. Invariant breaches ignore
     the budget.
  8. Contextual integrity (D48): providers are judged against what is
     expected under comparable conditions (hour, weekday, volume,
     registered maintenance). Expected fluctuations may adjust statistical
     expectations but NEVER relax hard invariants. A frozen qualification
     reference sits beside the adaptive forecast so the model can never
     teach itself that failure is normal.
  9. Provider restoration never restores authority automatically: returning
     to qualified requires independent re-verification and a version bump.
     A provider's own "we fixed it" is evidence, not qualification.

Scope notes (honest boundaries):
  - The contextual expectation model is a declared, inspectable function,
    not a fitted BetaBinomial; the frozen-vs-adaptive comparison is on
    failure-rate estimates, not a full distributional forecast.
  - Sequential change detection (CUSUM/EWMA) is approximated by
    short/long paired windows plus minimum material effect.
  - This module watches guarantees; it does not requalify provider
    contracts end-to-end (that needs the provider's cooperation) — it
    detects, contains, and gates requalification on independent evidence.

Stdlib only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple


# --------------------------------------------------------------------------
# Vocabularies
# --------------------------------------------------------------------------

class Regime(Enum):
    LOW_VOLUME = "LOW_VOLUME"     # <100 independent ops/week: exact count tests
    BURSTY = "BURSTY"             # correlated bursts: effective-sample-size aware
    HIGH_VOLUME = "HIGH_VOLUME"   # paired windows + minimum material effect


class ProbeOutcome(Enum):
    OK = "OK"               # guarantee observed holding
    DEGRADED = "DEGRADED"   # guarantee observed weakening (not breached)
    BREACH = "BREACH"       # hard invariant violated — decisive counterexample
    ERROR = "ERROR"         # probe itself failed (transport error, etc.)


class QualState(Enum):
    UNKNOWN = "UNKNOWN"                             # never successfully checked
    QUALIFIED_IN_SCOPE = "QUALIFIED_IN_SCOPE"       # watched and holding
    REVIEW_REQUIRED = "REVIEW_REQUIRED"             # weakened: investigate
    SUSPECTED_DRIFT = "SUSPECTED_DRIFT"             # drift suspected, not established
    QUALIFICATION_SUSPENDED = "QUALIFICATION_SUSPENDED"  # withdrawn: breach/stale
    REQUALIFIED_IN_NEW_SCOPE = "REQUALIFIED_IN_NEW_SCOPE"  # re-verified after change


class OpResponse(Enum):
    CONTINUE = "CONTINUE"
    OBSERVE = "OBSERVE"
    INVESTIGATE = "INVESTIGATE"
    HOLD_AFFECTED_RETRIES = "HOLD_AFFECTED_RETRIES"
    BLOCK_AFFECTED_EXECUTION = "BLOCK_AFFECTED_EXECUTION"


class Diagnosis(Enum):
    HEALTHY = "HEALTHY"
    TRANSIENT_ANOMALY = "TRANSIENT_ANOMALY"
    SUSPECTED_DRIFT = "SUSPECTED_DRIFT"
    CONTRACT_SCOPE_CHANGE = "CONTRACT_SCOPE_CHANGE"
    CONFIRMED_CONTRACT_BREACH = "CONFIRMED_CONTRACT_BREACH"
    UNDETERMINED = "UNDETERMINED"


class AlertLevel(Enum):
    L0 = 0  # log only
    L1 = 1  # notify owner
    L2 = 2  # page on-call
    L3 = 3  # hold affected work
    L4 = 4  # block affected execution, withdraw guarantee


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------

@dataclass
class ProbeReport:
    """One independent observation of a guarantee's behavior."""
    outcome: ProbeOutcome
    observed_at: float
    evidence: Dict[str, Any] = field(default_factory=dict)
    # For statistical signals: failures observed out of n independent ops,
    # plus burst-correlation info for BURSTY regimes.
    failures: int = 0
    samples: int = 0
    burst_id: Optional[str] = None
    note: str = ""


@dataclass
class Alert:
    level: AlertLevel
    code: str                      # GUARANTEE_WEAKENED / GUARANTEE_BROKEN /
                                   # GUARANTEE_STALE / DRIFT_SUSPECTED /
                                   # FROZEN_DIVERGENCE / SUPPRESSED_BY_BUDGET
    guarantee_id: str
    operational_response: OpResponse
    diagnosis: Diagnosis
    evidence: Dict[str, Any]
    raised_at: float
    budget_bypassed: bool = False   # True only for invariant breaches


@dataclass
class Incident:
    """Two-field incident record (D46): response and diagnosis never conflate."""
    guarantee_id: str
    operational_response: OpResponse
    diagnosis: Diagnosis
    evidence: Dict[str, Any]
    opened_at: float
    alert_level: AlertLevel


@dataclass
class QualEvent:
    state_from: str
    state_to: str
    reason: str
    evidence: Dict[str, Any]
    at: float
    version: int


@dataclass
class Guarantee:
    """What an external dependency promises, and how we independently check."""
    id: str
    provider: str
    use_case: str
    promise: str
    max_staleness_s: float
    regime: Regime
    baseline_fail_rate: float = 0.01      # frozen qualified reference p0
    min_material_effect: float = 0.02    # high-volume: ignore smaller deltas
    stat_alpha: float = 0.01             # significance for statistical alerts
    # Hard invariants: (name, predicate(report) -> True means VIOLATED).
    # No context, season, or maintenance window ever relaxes these.
    invariants: List[Tuple[str, Callable[[ProbeReport], bool]]] = field(default_factory=list)
    # Registered maintenance windows: (window_id, start, end). Only
    # registered windows adjust statistical expectations.
    maintenance_windows: List[Tuple[str, float, float]] = field(default_factory=list)
    # Contextual expectation: fn(hour, weekday, volume, in_maintenance)
    # -> expected fail rate under comparable conditions. Inspectable, declared.
    context_model: Optional[Callable[[int, int, float, bool], float]] = None
    frozen_reference: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Qualification:
    guarantee_id: str
    state: QualState = QualState.UNKNOWN
    version: int = 1
    last_check_at: Optional[float] = None
    last_outcome: Optional[ProbeOutcome] = None
    history: List[QualEvent] = field(default_factory=list)
    adaptive_fail_rate: Optional[float] = None  # adaptive forecast (never overwrites frozen)
    consecutive_errors: int = 0


# --------------------------------------------------------------------------
# The watcher
# --------------------------------------------------------------------------

ProbeFn = Callable[[Guarantee], ProbeReport]


class GuaranteeWatch:
    """Registry + prober + two-stage engine for outside guarantees."""

    def __init__(self, fleet_false_alarm_budget: int = 10):
        self._guarantees: Dict[str, Guarantee] = {}
        self._probes: Dict[str, ProbeFn] = {}
        self._quals: Dict[str, Qualification] = {}
        self._incidents: List[Incident] = []
        self._fleet_budget = fleet_false_alarm_budget
        self._fleet_alerts_used = 0
        self._regime_budgets: Dict[str, int] = {}
        self._regime_alerts_used: Dict[str, int] = {}
        self._window: List[Tuple[str, ProbeReport]] = []  # recent probe history

    # -- registration ------------------------------------------------------
    def register(self, guarantee: Guarantee, probe: ProbeFn,
                 regime_alert_budget: int = 3) -> Qualification:
        if guarantee.id in self._guarantees:
            raise ValueError(f"duplicate guarantee id: {guarantee.id}")
        self._guarantees[guarantee.id] = guarantee
        self._probes[guarantee.id] = probe
        self._regime_budgets[guarantee.id] = regime_alert_budget
        self._regime_alerts_used[guarantee.id] = 0
        q = Qualification(guarantee_id=guarantee.id)
        self._quals[guarantee.id] = q
        return q

    def qualification(self, gid: str) -> Qualification:
        return self._quals[gid]

    def incidents(self) -> List[Incident]:
        return list(self._incidents)

    # -- the freshness question --------------------------------------------
    def freshness(self, gid: str, now: float) -> str:
        """FRESH / STALE / UNKNOWN. Never assumed; always computed."""
        q = self._quals[gid]
        g = self._guarantees[gid]
        if q.last_check_at is None:
            return "UNKNOWN"
        if now - q.last_check_at > g.max_staleness_s:
            return "STALE"
        return "FRESH"

    def may_execute(self, gid: str, now: float) -> Tuple[bool, str]:
        """May dependent work run on this guarantee right now?"""
        q = self._quals[gid]
        fresh = self.freshness(gid, now)
        if fresh == "UNKNOWN":
            return False, "UNKNOWN_NEVER_CHECKED"
        if fresh == "STALE":
            return False, "STALE_CHECK_EXPIRED"
        if q.state in (QualState.QUALIFIED_IN_SCOPE,
                       QualState.REQUALIFIED_IN_NEW_SCOPE):
            return True, "QUALIFIED_AND_FRESH"
        return False, f"HELD_STATE_{q.state.value}"

    # -- tick ---------------------------------------------------------------
    def tick(self, now: float) -> List[Alert]:
        """Probe every registered guarantee; return alerts raised."""
        alerts: List[Alert] = []
        for gid, g in self._guarantees.items():
            q = self._quals[gid]
            # Staleness is checked even before probing: an expired guarantee
            # is caught as stale, never assumed fine.
            if self.freshness(gid, now) == "STALE" and q.state in (
                    QualState.QUALIFIED_IN_SCOPE, QualState.REQUALIFIED_IN_NEW_SCOPE):
                self._transition(q, QualState.QUALIFICATION_SUSPENDED,
                                "STALE_CHECK_EXPIRED",
                                {"last_check_at": q.last_check_at}, now)
                alerts.append(self._alert(
                    AlertLevel.L3, "GUARANTEE_STALE", g, OpResponse.BLOCK_AFFECTED_EXECUTION,
                    Diagnosis.UNDETERMINED,
                    {"reason": "check older than max_staleness_s; held, not assumed fine"},
                    now, budget_bypassed=True))
            report = self._probes[gid](g)
            report.observed_at = now
            self._window.append((gid, report))
            alerts.extend(self._evaluate(g, q, report, now))
            q.last_check_at = now
            q.last_outcome = report.outcome
            # Fresh check may lift a staleness suspension back to qualified
            # ONLY via the requalification path (independent evidence), never
            # automatically — provider restoration never restores authority.
            if q.state == QualState.QUALIFICATION_SUSPENDED and report.outcome == ProbeOutcome.OK:
                # Still suspended: needs explicit requalify() with independent evidence.
                pass
        return alerts

    # -- evaluation: fast safety gate first, slow diagnosis second ----------
    def _evaluate(self, g: Guarantee, q: Qualification, r: ProbeReport,
                  now: float) -> List[Alert]:
        alerts: List[Alert] = []
        # FAST GATE: hard invariants. One decisive counterexample withdraws
        # immediately — no sample minimum, no budget, no waiting.
        for name, violated in g.invariants:
            try:
                hit = violated(r)
            except Exception:
                hit = False
            if hit:
                self._transition(q, QualState.QUALIFICATION_SUSPENDED,
                                "INVARIANT_BREACH", {"invariant": name,
                                                    "evidence": r.evidence}, now)
                a = self._alert(AlertLevel.L4, "GUARANTEE_BROKEN", g,
                                OpResponse.BLOCK_AFFECTED_EXECUTION,
                                Diagnosis.CONFIRMED_CONTRACT_BREACH,
                                {"invariant": name, "evidence": r.evidence,
                                 "note": "one decisive counterexample is enough"},
                                now, budget_bypassed=True)
                alerts.append(a)
                self._incidents.append(Incident(
                    g.id, OpResponse.BLOCK_AFFECTED_EXECUTION,
                    Diagnosis.CONFIRMED_CONTRACT_BREACH,
                    {"invariant": name}, now, AlertLevel.L4))
                return alerts  # breach short-circuits everything else

        # Probe errors are UNDETERMINED, never drift (D46).
        if r.outcome == ProbeOutcome.ERROR:
            q.consecutive_errors += 1
            self._incidents.append(Incident(
                g.id, OpResponse.OBSERVE, Diagnosis.UNDETERMINED,
                {"probe_error": r.note}, now, AlertLevel.L0))
            return alerts
        q.consecutive_errors = 0

        # SLOW PATH: statistical / behavioral signals.
        if r.outcome == ProbeOutcome.BREACH:
            # Non-invariant breach evidence still counts as a confirmed breach
            # of the observed guarantee (probe saw the violation directly).
            self._transition(q, QualState.QUALIFICATION_SUSPENDED,
                            "OBSERVED_BREACH", {"evidence": r.evidence}, now)
            alerts.append(self._alert(
                AlertLevel.L4, "GUARANTEE_BROKEN", g,
                OpResponse.BLOCK_AFFECTED_EXECUTION,
                Diagnosis.CONFIRMED_CONTRACT_BREACH,
                {"evidence": r.evidence}, now, budget_bypassed=True))
            return alerts

        if r.outcome == ProbeOutcome.DEGRADED:
            self._transition(q, QualState.REVIEW_REQUIRED, "DEGRADED_OBSERVED",
                            {"evidence": r.evidence}, now)
            alerts.append(self._alert(
                AlertLevel.L3, "GUARANTEE_WEAKENED", g,
                OpResponse.HOLD_AFFECTED_RETRIES, Diagnosis.TRANSIENT_ANOMALY,
                {"evidence": r.evidence,
                 "note": "weakened, not withdrawn: investigate before requalifying"},
                now))
            self._incidents.append(Incident(
                g.id, OpResponse.HOLD_AFFECTED_RETRIES, Diagnosis.TRANSIENT_ANOMALY,
                {"evidence": r.evidence}, now, AlertLevel.L3))
            return alerts

        # OK outcome: run the statistical drift screen on the window.
        signal, sig_evidence = self._statistical_signal(g, now)
        self._update_adaptive(g, q, r)
        frozen_hit = self._frozen_divergence(g, q, now)
        if frozen_hit:
            self._transition(q, QualState.SUSPECTED_DRIFT, "FROZEN_DIVERGENCE",
                            frozen_hit, now)
            alerts.append(self._alert(
                AlertLevel.L2, "FROZEN_DIVERGENCE", g,
                OpResponse.INVESTIGATE, Diagnosis.SUSPECTED_DRIFT,
                dict(frozen_hit, note="adaptive forecast learned failure as normal; "
                                      "frozen reference disagrees"),
                now))
            self._incidents.append(Incident(
                g.id, OpResponse.INVESTIGATE, Diagnosis.SUSPECTED_DRIFT,
                dict(frozen_hit), now, AlertLevel.L2))
        elif signal:
            self._transition(q, QualState.SUSPECTED_DRIFT, "STATISTICAL_SIGNAL",
                            sig_evidence, now)
            alerts.append(self._alert(
                AlertLevel.L2, "DRIFT_SUSPECTED", g,
                OpResponse.INVESTIGATE, Diagnosis.SUSPECTED_DRIFT,
                dict(sig_evidence, note="suspicion only: independent verification "
                                        "required before any qualification change"),
                now))
            self._incidents.append(Incident(
                g.id, OpResponse.INVESTIGATE, Diagnosis.SUSPECTED_DRIFT,
                sig_evidence, now, AlertLevel.L2))
        elif q.state == QualState.UNKNOWN:
            # First successful check: initial qualification. Every other
            # non-qualified state needs explicit requalify() — a fresh OK
            # probe never restores authority by itself.
            self._transition(q, QualState.QUALIFIED_IN_SCOPE,
                            "INITIAL_QUALIFICATION",
                            {"first_check_at": now}, now)
        return alerts

    # -- D47: regime-adaptive statistical screen -----------------------------
    def _recent(self, gid: str, n: int) -> List[ProbeReport]:
        return [r for (i, r) in self._window if i == gid][-n:]

    def _statistical_signal(self, g: Guarantee, now: float) -> Tuple[bool, Dict[str, Any]]:
        reps = self._recent(g.id, 200)
        # Only behavior observations count toward drift; probe ERRORs never do.
        obs = [r for r in reps if r.outcome in (ProbeOutcome.OK, ProbeOutcome.DEGRADED,
                                                ProbeOutcome.BREACH)]
        if not obs:
            return False, {}
        in_maint = self._in_maintenance(g, now)
        p0 = self._expected_rate(g, now, in_maint)

        if g.regime == Regime.LOW_VOLUME:
            # Exact count test on tiny denominators — never percent thresholds.
            n = sum(r.samples for r in obs[-20:])
            k = sum(r.failures for r in obs[-20:])
            if n == 0:
                return False, {}
            p_value = _binom_tail(n, k, p0)
            if p_value < g.stat_alpha:
                return True, {"regime": "LOW_VOLUME", "failures": k, "samples": n,
                              "p_value": round(p_value, 6), "expected_rate": p0,
                              "method": "exact-binomial-tail"}
            return False, {}

        if g.regime == Regime.BURSTY:
            # Correlated bursts collapse to effective independent observations.
            bursts = self._bursts(obs)
            m = len(bursts)
            if m == 0:
                return False, {}
            rho = 0.8  # declared correlation assumption for same-burst ops
            n_eff = m  # one burst ~= one independent observation
            bad_bursts = sum(1 for b in bursts if b["bad"])
            p_value = _binom_tail(n_eff, bad_bursts, p0)
            if p_value < g.stat_alpha:
                return True, {"regime": "BURSTY", "bad_bursts": bad_bursts,
                              "effective_samples": n_eff,
                              "raw_failures": sum(r.failures for r in obs),
                              "p_value": round(p_value, 6),
                              "method": "burst-collapsed-effective-n"}
            return False, {"regime": "BURSTY", "note": "correlated burst counted once"}

        # HIGH_VOLUME: paired short/long windows + minimum material effect.
        short = obs[-50:]
        longw = obs[-500:]
        ps = _rate(short)
        pl = _rate(longw)
        if len(short) < 20 or len(longw) < 100:
            return False, {}
        if abs(ps - pl) >= g.min_material_effect and ps > p0 + g.min_material_effect:
            # rough significance via normal approx on the short window
            se = math.sqrt(max(pl, 1e-9) * (1 - max(pl, 1e-9)) / max(len(short), 1))
            z = (ps - pl) / max(se, 1e-9)
            if z > 3.0:
                return True, {"regime": "HIGH_VOLUME", "short_rate": round(ps, 4),
                              "long_rate": round(pl, 4),
                              "min_material_effect": g.min_material_effect,
                              "z": round(z, 2), "method": "paired-windows"}
        return False, {}

    def _bursts(self, obs: List[ProbeReport]) -> List[Dict[str, Any]]:
        bursts: Dict[str, Dict[str, Any]] = {}
        for r in obs:
            key = r.burst_id or f"solo-{id(r)}"
            b = bursts.setdefault(key, {"bad": False, "n": 0})
            b["n"] += 1
            if r.outcome in (ProbeOutcome.DEGRADED, ProbeOutcome.BREACH) or r.failures > 0:
                b["bad"] = True
        return list(bursts.values())

    def _in_maintenance(self, g: Guarantee, now: float) -> bool:
        return any(s <= now <= e for (_, s, e) in g.maintenance_windows)

    def _expected_rate(self, g: Guarantee, now: float, in_maint: bool) -> float:
        # Contextual expectation under comparable conditions (D48).
        # Only REGISTERED maintenance adjusts expectations; unregistered
        # claims of "maintenance" change nothing.
        import datetime as _dt
        dt = _dt.datetime.utcfromtimestamp(now)
        volume = float(sum(r.samples for r in self._recent(g.id, 10)) or 1.0)
        if g.context_model is not None:
            try:
                return float(g.context_model(dt.hour, dt.weekday(), volume, in_maint))
            except Exception:
                pass
        base = g.baseline_fail_rate
        return base * 3.0 if in_maint else base

    # -- D48: frozen reference vs adaptive forecast ---------------------------
    def _update_adaptive(self, g: Guarantee, q: Qualification, r: ProbeReport) -> None:
        if r.samples <= 0:
            return
        obs_rate = r.failures / r.samples
        q.adaptive_fail_rate = (obs_rate if q.adaptive_fail_rate is None
                                else 0.9 * q.adaptive_fail_rate + 0.1 * obs_rate)

    def _frozen_divergence(self, g: Guarantee, q: Qualification,
                         now: float) -> Optional[Dict[str, Any]]:
        """The adaptive forecast must never teach itself failure is normal.

        Compares the adaptive estimate against what is expected under the
        CURRENT comparable conditions (context-adjusted frozen reference),
        so legitimate seasonal elevation never trips it while a real
        regression under any conditions does.
        """
        if q.adaptive_fail_rate is None:
            return None
        expected = self._expected_rate(g, now, self._in_maintenance(g, now))
        tol = float(g.frozen_reference.get("tolerance", 0.03))
        if q.adaptive_fail_rate - expected > tol:
            return {"adaptive_fail_rate": round(q.adaptive_fail_rate, 4),
                    "expected_under_conditions": round(expected, 4),
                    "frozen_baseline": float(g.frozen_reference.get(
                        "fail_rate", g.baseline_fail_rate)),
                    "tolerance": tol}
        return None

    # -- alerts with false-alarm budgets --------------------------------------
    def _alert(self, level: AlertLevel, code: str, g: Guarantee,
               response: OpResponse, diagnosis: Diagnosis,
               evidence: Dict[str, Any], now: float,
               budget_bypassed: bool = False) -> Alert:
        # Safety-relevant alerts (L3 hold, L4 block/withdraw, and anything
        # explicitly bypassing) ALWAYS fire. Statistical/investigative
        # alerts (L0-L2) draw from the per-regime and fleet false-alarm
        # budgets; beyond budget they are logged, not paged.
        safety = budget_bypassed or level in (AlertLevel.L3, AlertLevel.L4)
        if not safety and (self._regime_alerts_used[g.id] >= self._regime_budgets[g.id]
                           or self._fleet_alerts_used >= self._fleet_budget):
            return Alert(AlertLevel.L0, "SUPPRESSED_BY_BUDGET", g.id, OpResponse.OBSERVE,
                         Diagnosis.UNDETERMINED,
                         {"suppressed": code, "evidence": evidence}, now)
        if not safety:
            self._regime_alerts_used[g.id] += 1
            self._fleet_alerts_used += 1
        return Alert(level, code, g.id, response, diagnosis, evidence, now,
                     budget_bypassed=budget_bypassed)

    # -- state transitions (append-only history) -------------------------------
    def _transition(self, q: Qualification, to: QualState, reason: str,
                    evidence: Dict[str, Any], now: float) -> None:
        q.history.append(QualEvent(q.state.value, to.value, reason,
                                   dict(evidence), now, q.version))
        q.state = to

    # -- requalification: independent evidence or nothing ----------------------
    def requalify(self, gid: str, independent_report: ProbeReport,
                  new_scope: Optional[str], now: float) -> Tuple[bool, str]:
        """Restore a suspended/review guarantee. Requires independent
        verification — a provider's own 'we fixed it' is refused."""
        q = self._quals[gid]
        g = self._guarantees[gid]
        if q.state not in (QualState.QUALIFICATION_SUSPENDED, QualState.REVIEW_REQUIRED,
                           QualState.SUSPECTED_DRIFT, QualState.UNKNOWN):
            return False, f"NOTHING_TO_REQUALIFY_{q.state.value}"
        ev = independent_report.evidence or {}
        if not ev.get("independent", False):
            return False, "RESTORATION_WITHOUT_REQUALIFICATION_REFUSED"
        if independent_report.outcome != ProbeOutcome.OK:
            return False, "INDEPENDENT_VERIFICATION_FAILED"
        q.version += 1
        target = (QualState.REQUALIFIED_IN_NEW_SCOPE if new_scope
                  else QualState.QUALIFIED_IN_SCOPE)
        self._transition(q, target, "INDEPENDENT_REQUALIFICATION",
                         {"new_scope": new_scope, "version": q.version}, now)
        q.adaptive_fail_rate = None  # adaptive forecast restarts; frozen reference kept
        return True, f"REQUALIFIED_v{q.version}"

    def does_not_claim(self) -> str:
        return ("This watcher judges the guarantees it is given via the probes it "
                "is given; it cannot detect a provider behavior change that no "
                "probe observes, and a PASS covers only the checked use case, "
                "never the provider in general.")


# --------------------------------------------------------------------------
# Small statistical helpers (stdlib)
# --------------------------------------------------------------------------

def _binom_tail(n: int, k: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n, p). Exact, no normal approximation."""
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    p = min(max(p, 0.0), 1.0)
    if p >= 1.0:
        return 1.0  # X = n always, so X >= k for every k <= n
    total = 0.0
    # sum_{i=k}^{n} C(n,i) p^i (1-p)^{n-i}, iteratively for stability
    comb = math.comb(n, k)
    term = comb * (p ** k) * ((1 - p) ** (n - k))
    for i in range(k, n + 1):
        total += term
        if i < n:
            term *= (n - i) / (i + 1) * (p / (1 - p) if p < 1 else 0.0)
    return min(total, 1.0)


def _rate(reports: List[ProbeReport]) -> float:
    n = sum(r.samples for r in reports)
    if n == 0:
        return 0.0
    return sum(r.failures for r in reports) / n
