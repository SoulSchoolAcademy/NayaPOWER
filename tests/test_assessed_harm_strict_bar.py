"""Strict assessed-harm bar — Shawn 2026-10-11 bar decision (KEEP THE STRICT BAR).

The retired DecisionEngine disqualified assessed harm at severity >= 7.0 and
probability > 0.05. The t912 consolidation mapped this to the configurable
RiskPolicy tail path (default 9.0/0.01); Lane 8's t942 cross-seat scorecard
proved the F1 band — severity in [7.0, 9.0), probability > 0.05 — was
ADMISSIBLE under canonical defaults (protection loss). This file pins the
policy override in the canonical engine: the strict bar fires before the
configurable path, verdict PROHIBITED (the canonical verdict class for the
retired engine's DISQUALIFIED, per the t912 verdict mapping; downstream
consumers key exclusion on PROHIBITED).

Deliberate differences from the retired bytes (documented):
- The retired engine ADMITTED this band on informed_consent+harm_mitigated;
  the canonical engine has no consent-admission fields and does not admit it.
- Fail-closed edge case: severity >= 7.0 with UNKNOWN probability (None) is
  treated as meeting the bar. The retired engine deferred on unknown.
"""

import pytest

from kernel.value_calculus import (
    ADMISSIBLE,
    PROHIBITED,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    TailRisk,
    gate_candidate,
)


@pytest.fixture
def profile():
    return QualityProfile(
        profile_id="STRICT-BAR",
        version="v1",
        objective="strict bar proof",
        min_evidence_count=2,
    )


def _q(score=9.5, conf=0.95):
    dims = {
        "objective_fit": score,
        "evidence_sufficiency": score,
        "applicability": score,
        "robustness": score,
        "reversibility": score,
        "blast_containment": score,
        "simplicity": score,
    }
    return dims, {k: conf for k in dims}


def _pv():
    return PVEstimate(8, 0, 1, 0.2, {k: 0.95 for k in ("B", "H", "C", "R")}, 3)


def _cand(sev, prob, harm_class="probe"):
    q, c = _q()
    return Candidate(
        "probe", q, c, _pv(), reversible=True,
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
        authorized=True, human_authorized=True,
        tails=(TailRisk(severity=sev, probability=prob, harm_class=harm_class),),
    )


def _gate(sev, prob, profile):
    return gate_candidate(_cand(sev, prob), profile, RiskPolicy())


# ---------------------------------------------------------------------------
# The protected band: every sev in [7.0, 9.0) with prob > 0.05 is excluded
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("sev,prob", [
    (7.0, 0.06),    # Lane 8's c1 case: old DISQUALIFIED, was new ADMISSIBLE
    (7.0, 0.051),   # just above the probability bar
    (7.5, 0.5),
    (8.0, 0.5),
    (8.99, 0.99),
    (7.0, 1.0),
    (9.0, 0.06),    # at the old upper edge, still below canonical 9.0 bar prob logic
])
def test_f1_band_excluded(profile, sev, prob):
    gate, reasons, _ = _gate(sev, prob, profile)
    assert gate == PROHIBITED
    assert any(r.startswith("ASSESSED_HARM_STRICT_BAR") for r in reasons), reasons


def test_strict_bar_reason_names_harm_class(profile):
    gate, reasons, _ = _gate(7.5, 0.5, profile)
    assert reasons == ["ASSESSED_HARM_STRICT_BAR:probe"]


# ---------------------------------------------------------------------------
# Boundary operators preserved byte-for-byte from the retired engine:
# severity >= 7.0, probability > 0.05 (prob == 0.05 does NOT trip the bar)
# ---------------------------------------------------------------------------

def test_boundary_probability_equal_does_not_trip(profile):
    # prob == 0.05 is NOT > 0.05: falls through to the configurable tail path;
    # severity 7.0 < canonical 9.0, so an otherwise-clean candidate admits.
    gate, reasons, _ = _gate(7.0, 0.05, profile)
    assert gate == ADMISSIBLE, reasons


def test_boundary_severity_below_bar_admits(profile):
    gate, reasons, _ = _gate(6.99, 0.9, profile)
    assert gate == ADMISSIBLE, reasons


# ---------------------------------------------------------------------------
# Fail-closed edge case: unknown probability never weakens the strict bar
# ---------------------------------------------------------------------------

def test_unknown_probability_with_high_severity_is_excluded(profile):
    gate, reasons, _ = _gate(8.0, None, profile)
    assert gate == PROHIBITED
    assert any(r.startswith("ASSESSED_HARM_STRICT_BAR") for r in reasons), reasons


def test_unknown_probability_below_bar_keeps_existing_validation(profile):
    # Severity below the bar with unknown probability: existing tail-loop
    # behavior is unchanged (the old ValueError on non-finite probability).
    with pytest.raises((TypeError, ValueError)):
        _gate(5.0, None, profile)


# ---------------------------------------------------------------------------
# No weakening of the existing paths: old-DISQUALIFIED stays excluded,
# the canonical tail path still fires above the bar
# ---------------------------------------------------------------------------

def test_old_exclusion_above_canonical_bar_still_excludes(profile):
    # Old engine: DISQUALIFIED (assessed). New: still excluded.
    gate, reasons, _ = _gate(9.5, 0.5, profile)
    assert gate == PROHIBITED
    assert any(r.startswith("ASSESSED_HARM_STRICT_BAR") for r in reasons), reasons


def test_canonical_tail_path_still_fires_outside_strict_band(profile):
    # (9.5, 0.03): above canonical severity, below strict probability —
    # the RiskPolicy tail path (not the override) excludes it.
    gate, reasons, _ = _gate(9.5, 0.03, profile)
    assert gate == PROHIBITED
    assert any(r.startswith("TAIL_RISK") for r in reasons), reasons
    assert not any(r.startswith("ASSESSED_HARM_STRICT_BAR") for r in reasons)
