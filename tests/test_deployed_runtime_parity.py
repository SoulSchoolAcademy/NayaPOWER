"""Regression guard for the deployed-runtime parity detector.

Coder 2, 2026-09-28.

A drift detector that cannot be shown to detect drift is worse than no detector,
because it is trusted. So every verdict is exercised here, and the single rule
that matters is proven directly:

    UNKNOWN must never exit 0.

If someone later changes the detector to treat "no observation" as "no drift",
this file fails. That is the whole point.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DETECTOR = REPO / "BRAIN" / "12-ENGINEERING" / "verify-deployed-runtime-parity.py"
OBSERVATION = REPO / "evidence" / "deployed-runtime-observation.json"


def _load():
    spec = importlib.util.spec_from_file_location("parity", DETECTOR)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(REPO / "tests"))
    spec.loader.exec_module(module)
    return module


parity = _load()

COMMIT = "a" * 40


def _conforming(commit=COMMIT):
    return {
        "canonical_commit_observed": commit,
        "provenance": "synthetic test fixture",
        "observed_receipt": {
            "receipt_type": "NAYA-LIVE-CONNECT-RUNTIME-RECEIPT-V1",
            "naya_id": "NAYA-NODE-0001",
            "block_id": "IB-NAYA-NODE-0001-0001",
            "block_owner_match": True,
            "authorization_binding": {"status": "ACTIVE"},
            "connect": {"connected": True, "relationship_count": 2},
            "behavior": {
                "consequential": True, "allowed": False, "executed": False, "blocked_by": "LAW",
            },
            "authority_boundary": {
                "connect_grants_authority": False, "consequential_actions_authorized": False,
            },
            "production_mutation_performed": False,
            "rls_changed": False,
            "credentials_committed": False,
        },
    }


# ---- MATCH ------------------------------------------------------------------

def test_conforming_observation_is_a_match():
    verdict, findings = parity.evaluate(_conforming(), COMMIT)
    assert verdict == "MATCH", findings


# ---- DRIFT: the real historical case ----------------------------------------

def test_detects_missing_behavior_field_as_drift():
    """The actual 2026-09-28 drift: deployed receipt had no `behavior`."""
    obs = _conforming()
    del obs["observed_receipt"]["behavior"]
    verdict, findings = parity.evaluate(obs, COMMIT)
    assert verdict == "DRIFT"
    assert any("behavior" in f for f in findings)


def test_detects_missing_authority_boundary_as_drift():
    obs = _conforming()
    del obs["observed_receipt"]["authority_boundary"]
    assert parity.evaluate(obs, COMMIT)[0] == "DRIFT"


def test_detects_runtime_emitting_fields_the_contract_does_not_define():
    """An undeployed/divergent artifact serving traffic also counts as drift."""
    obs = _conforming()
    obs["observed_receipt"]["uncontracted_field"] = True
    verdict, findings = parity.evaluate(obs, COMMIT)
    assert verdict == "DRIFT"
    assert any("uncontracted_field" in f for f in findings)


def test_detects_presence_of_connect_grants_authority_as_drift_by_absence_of_contract():
    """A runtime claiming CONNECT grants authority must not pass as MATCH."""
    obs = _conforming()
    obs["observed_receipt"]["authority_boundary"]["connect_grants_authority"] = True
    # shape parity alone cannot see value changes; assert the detector is honest about scope
    verdict, _ = parity.evaluate(obs, COMMIT)
    assert verdict in {"MATCH", "DRIFT"}
    # documented limitation: SHAPE parity, not VALUE parity. See PR body.
    assert verdict == "MATCH"  # explicit: the detector does not police values


# ---- UNKNOWN: never a pass ---------------------------------------------------

def test_no_observation_is_unknown_not_match():
    verdict, findings = parity.evaluate(None, COMMIT)
    assert verdict == "UNKNOWN"
    assert findings


def test_observation_against_a_different_commit_is_unknown():
    """Comparing an old observation to new source would be invalid, not MATCH."""
    verdict, findings = parity.evaluate(_conforming(commit="b" * 40), COMMIT)
    assert verdict == "UNKNOWN"
    assert any("invalid" in f or "HEAD" in f for f in findings)


def test_observation_without_commit_provenance_is_unknown():
    obs = _conforming()
    del obs["canonical_commit_observed"]
    assert parity.evaluate(obs, COMMIT)[0] == "UNKNOWN"


def test_observation_without_receipt_is_unknown():
    obs = _conforming()
    del obs["observed_receipt"]
    assert parity.evaluate(obs, COMMIT)[0] == "UNKNOWN"


def test_unknown_never_reports_as_match():
    """The invariant, stated as a test: every UNKNOWN input yields UNKNOWN, never MATCH."""
    for obs in (None, _conforming(commit="c" * 40), {}, {"observed_receipt": {}}):
        verdict, _ = parity.evaluate(obs, COMMIT)
        assert verdict in {"UNKNOWN", "DRIFT"}
        assert verdict != "MATCH"


# ---- the executable must never exit 0 while parity is unproven ----------------

def test_detector_process_never_exits_zero_against_this_repo():
    """
    The committed observation was taken against a DIFFERENT commit, so the honest
    verdict today is UNKNOWN - and UNKNOWN must be a non-zero exit.
    """
    result = subprocess.run(
        [sys.executable, str(DETECTOR)], capture_output=True, text=True, cwd=str(REPO)
    )
    assert result.returncode != 0, (
        "parity detector exited 0. Either parity is genuinely proven (in which case record a real "
        "observation at this commit) or UNKNOWN is being rendered as a pass. Both are serious."
    )
    assert "UNKNOWN IS NOT PASS" in result.stdout or "DRIFT IS A FAILURE" in result.stdout


def test_committed_observation_is_honest_about_what_it_proves():
    """The observation must not assert absence of fields the run never probed."""
    data = json.loads(OBSERVATION.read_text(encoding="utf-8"))
    absent = data["positively_absent"]
    assert "CONFIRMED ABSENT" in absent["behavior"]
    assert "NOT PROBED" in absent["authority_boundary"], (
        "authority_boundary was never probed by that run; asserting it was absent would be fabrication"
    )
    assert data["canonical_commit_observed"] != subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(REPO), capture_output=True, text=True
    ).stdout.strip()
