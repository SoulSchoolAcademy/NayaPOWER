#!/usr/bin/env python3
"""Tests for the Learning Loop — Layer 6 of the Ultimate Decision Machine.

Every test is a real execution: real subprocess CLI calls, real JSONL files,
hand-verified math. No mocks of the module's own code.
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest

TOOL = os.path.join(os.path.dirname(__file__), "..", "tools", "learning_loop.py")
TOOL = os.path.abspath(TOOL)

DIMENSIONS = ["mission_value", "evidence", "risk", "cost", "urgency"]
WEIGHTS = {"mission_value": 0.35, "evidence": 0.25, "risk": 0.20,
           "cost": 0.10, "urgency": 0.10}


def run_cli(*argv, ledger=None):
    """Run the real CLI. Returns (returncode, stdout_json, stderr_text)."""
    assert ledger is not None, "tests must always use an isolated ledger"
    # --ledger is per-subcommand: insert right after the subcommand name.
    full = ([sys.executable, TOOL, argv[0], "--ledger", ledger]
            + list(argv[1:]))
    p = subprocess.run(full, capture_output=True, text=True, timeout=60)
    try:
        out = json.loads(p.stdout) if p.stdout.strip() else None
    except json.JSONDecodeError:
        out = {"_raw_stdout": p.stdout}
    return p.returncode, out, p.stderr


def make_scored(dim_values, confidence=0.8, option_id="opt-1",
                with_recommendation=True):
    """Build a Layer-4-shaped scored dict with chosen dimension values."""
    dims = {d: {"value": dim_values.get(d, 0.5), "confidence": 0.7,
                "evidence": [f"ev-{d}"]} for d in DIMENSIONS}
    opt = {
        "id": option_id, "title": f"Option {option_id}", "source": "PR #1",
        "source_type": "pr", "gated": False, "gate_reasons": [], "rank": 1,
        "dimensions": dims, "total": 0.6, "total_confidence": confidence,
        "unknown_dimensions": [],
    }
    rec = ({"option_id": option_id, "title": f"Option {option_id}",
            "total": 0.6, "total_confidence": confidence}
           if with_recommendation else None)
    return {
        "ok": True, "intent_type": "which_option", "objective": "Pick one",
        "weights": dict(WEIGHTS), "weights_schema_version": "v1",
        "options": [opt], "recommendation": rec,
        "notes": [], "warnings": [], "scored_utc": "2026-10-12T00:00:00+00:00",
    }


def make_intent(intent_type="which_option"):
    return {"intent_type": intent_type, "objective": "Pick one",
            "decision_weight": 5, "stakes": "low"}


@pytest.fixture
def ledger():
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    os.close(fd)
    os.unlink(path)  # start nonexistent; tool must create
    yield path
    if os.path.exists(path):
        os.unlink(path)


def write_receipt(ledger, dim_values, confidence=0.8, intent_type="which_option",
                  option_id="opt-1", with_recommendation=True):
    rc, out, err = run_cli(
        "write-receipt",
        "--scored", json.dumps(make_scored(
            dim_values, confidence, option_id, with_recommendation)),
        "--intent", json.dumps(make_intent(intent_type)),
        ledger=ledger)
    assert rc == 0, f"write-receipt failed: {err} {out}"
    return out["receipt_id"]


def record_outcome(ledger, receipt_id, actual, observed_by="VERIFIED"):
    rc, out, err = run_cli(
        "record-outcome", "--receipt", receipt_id,
        "--actual", actual, "--observed-by", observed_by, ledger=ledger)
    assert rc == 0, f"record-outcome failed: {err} {out}"
    return out


# ---------------------------------------------------------------------------
# Receipt ledger: append-only, fingerprints, corrections
# ---------------------------------------------------------------------------

class TestReceiptLedger:
    def test_receipt_written_with_all_fields(self, ledger):
        rid = write_receipt(ledger, {"mission_value": 0.8})
        with open(ledger) as f:
            lines = f.read().strip().split("\n")
        assert len(lines) == 1
        rec = json.loads(lines[0])
        assert rec["record_type"] == "decision"
        assert rec["receipt_id"] == rid
        assert rec["predicted_confidence"] == 0.8
        assert rec["predicted_outcome"] == "success"
        assert rec["intent"]["intent_type"] == "which_option"
        assert rec["options"][0]["fingerprint"]
        assert len(rec["options"][0]["fingerprint"]) == 12
        assert rec["options"][0]["dimensions"]["mission_value"]["value"] == 0.8
        assert rec["options"][0]["dimensions"]["mission_value"]["evidence"] == ["ev-mission_value"]

    def test_append_only_second_write_preserves_first(self, ledger):
        rid1 = write_receipt(ledger, {"mission_value": 0.8})
        with open(ledger, "rb") as f:
            first_bytes = f.read()
        rid2 = write_receipt(ledger, {"mission_value": 0.2})
        with open(ledger, "rb") as f:
            all_bytes = f.read()
        assert all_bytes.startswith(first_bytes)  # first receipt untouched
        assert rid1 != rid2

    def test_fingerprint_stable_for_same_option(self, ledger):
        rid1 = write_receipt(ledger, {"mission_value": 0.8}, option_id="same-1")
        rid2 = write_receipt(ledger, {"mission_value": 0.1}, option_id="same-1")
        recs = [json.loads(l) for l in open(ledger).read().strip().split("\n")]
        fps = [r["options"][0]["fingerprint"] for r in recs]
        assert fps[0] == fps[1]  # same provenance → same fingerprint

    def test_correction_chaining_supersedes(self, ledger):
        rid1 = write_receipt(ledger, {"mission_value": 0.8})
        rc, out, err = run_cli(
            "write-receipt",
            "--scored", json.dumps(make_scored({"mission_value": 0.3})),
            "--intent", json.dumps(make_intent()),
            "--supersedes", rid1, ledger=ledger)
        assert rc == 0, err
        rid2 = out["receipt_id"]
        # Outcome observed against the ORIGINAL transfers to the live
        # correction — the decision is counted once, not twice, and the
        # outcome is not dropped.
        record_outcome(ledger, rid1, "FAILURE")
        rc, out, err = run_cli("calibrate", ledger=ledger)
        assert out["n_decisions"] == 1, f"wrong count: {out}"
        # the single sample is the live receipt (rid2) with the transferred
        # FAILURE → value 0.0
        assert out["status"] == "insufficient_data"  # n=1 < 10

    def test_no_recommendation_predicts_nothing(self, ledger):
        rid = write_receipt(ledger, {"mission_value": 0.8},
                            with_recommendation=False)
        rec = json.loads(open(ledger).read().strip().split("\n")[0])
        assert rec["recommendation"] is None
        assert rec["predicted_confidence"] is None
        assert rec["predicted_outcome"] is None
        record_outcome(ledger, rid, "SUCCESS")
        rc, out, err = run_cli("calibrate", ledger=ledger)
        assert out["n_decisions"] == 0  # excluded, not scored as a guess


# ---------------------------------------------------------------------------
# Outcomes: labels, validation, fail-closed
# ---------------------------------------------------------------------------

class TestOutcomes:
    def test_labels_preserved_canonical_uppercase(self, ledger):
        rid = write_receipt(ledger, {"mission_value": 0.8})
        out = record_outcome(ledger, rid, "success", "self_reported")
        assert out["actual"] == "SUCCESS"
        assert out["observed_by"] == "SELF_REPORTED"

    def test_all_labels_accepted(self, ledger):
        for actual, by in [("SUCCESS", "SELF_REPORTED"), ("PARTIAL", "OBSERVED"),
                           ("FAILURE", "VERIFIED"), ("UNKNOWN", "SELF_REPORTED")]:
            rid = write_receipt(ledger, {"mission_value": 0.5})
            out = record_outcome(ledger, rid, actual, by)
            assert out["actual"] == actual
            assert out["observed_by"] == by

    def test_invalid_actual_rejected(self, ledger):
        rid = write_receipt(ledger, {"mission_value": 0.5})
        rc, out, err = run_cli(
            "record-outcome", "--receipt", rid, "--actual", "maybe",
            "--observed-by", "VERIFIED", ledger=ledger)
        assert rc == 1
        assert "error" in err or (out and "error" in str(out)) or rc == 1

    def test_invalid_observed_by_rejected(self, ledger):
        rid = write_receipt(ledger, {"mission_value": 0.5})
        rc, out, err = run_cli(
            "record-outcome", "--receipt", rid, "--actual", "SUCCESS",
            "--observed-by", "RUMOR", ledger=ledger)
        assert rc == 1

    def test_unknown_receipt_rejected_not_dangled(self, ledger):
        rc, out, err = run_cli(
            "record-outcome", "--receipt", "rcpt-does-not-exist",
            "--actual", "SUCCESS", "--observed-by", "VERIFIED",
            ledger=ledger)
        assert rc == 1

    def test_unknown_outcomes_never_count_as_success(self, ledger):
        # 10 decisions, ALL outcomes UNKNOWN → insufficient_data, NOT 0% rate
        for _ in range(10):
            rid = write_receipt(ledger, {"mission_value": 0.9}, confidence=0.95)
            record_outcome(ledger, rid, "UNKNOWN")
        rc, out, err = run_cli("calibrate", ledger=ledger)
        assert rc == 2
        assert out["status"] == "insufficient_data"
        assert out["n_decisions"] == 0


# ---------------------------------------------------------------------------
# Calibration math — hand-verified
# ---------------------------------------------------------------------------

class TestCalibration:
    def _ten(self, ledger, confidences, actuals, intent_type="which_option"):
        assert len(confidences) == len(actuals) == 10
        for c, a in zip(confidences, actuals):
            rid = write_receipt(ledger, {"mission_value": 0.5},
                                confidence=c, intent_type=intent_type)
            record_outcome(ledger, rid, a)

    def test_perfect_calibration_hand_verified(self, ledger):
        # 10 decisions at 0.8 predicted, 8 SUCCESS + 2 FAILURE → rate 0.8,
        # gap 0.0, ECE 0.0 → calibrated.
        self._ten(ledger, [0.8] * 10, ["SUCCESS"] * 8 + ["FAILURE"] * 2)
        rc, out, err = run_cli("calibrate", ledger=ledger)
        assert rc == 0, err
        assert out["status"] == "ok"
        assert out["n_decisions"] == 10
        bin80 = next(b for b in out["bins"] if b["range"][0] == 0.8)
        assert bin80["n"] == 10
        assert bin80["mean_predicted"] == 0.8
        assert bin80["observed_rate"] == 0.8
        assert bin80["gap"] == 0.0
        assert out["expected_calibration_error"] == 0.0
        assert out["verdict"].startswith("calibrated")

    def test_miscalibration_hand_verified(self, ledger):
        # 10 decisions at 0.9 predicted, 5/5 → rate 0.5, gap 0.4, ECE 0.4.
        self._ten(ledger, [0.9] * 10, ["SUCCESS"] * 5 + ["FAILURE"] * 5)
        rc, out, err = run_cli("calibrate", ledger=ledger)
        assert rc == 0, err
        bin90 = next(b for b in out["bins"] if b["range"][0] == 0.9)
        assert bin90["observed_rate"] == 0.5
        assert bin90["gap"] == 0.4
        assert out["expected_calibration_error"] == 0.4
        assert out["verdict"].startswith("miscalibrated")

    def test_partial_counts_half(self, ledger):
        # 10 at 0.7: 5 SUCCESS + 5 PARTIAL → (5*1 + 5*0.5)/10 = 0.75
        self._ten(ledger, [0.7] * 10, ["SUCCESS"] * 5 + ["PARTIAL"] * 5)
        rc, out, err = run_cli("calibrate", ledger=ledger)
        bin70 = next(b for b in out["bins"] if b["range"][0] == 0.7)
        assert bin70["observed_rate"] == 0.75
        assert bin70["gap"] == 0.05

    def test_insufficient_data_is_honest(self, ledger):
        for _ in range(9):
            rid = write_receipt(ledger, {"mission_value": 0.5}, confidence=0.9)
            record_outcome(ledger, rid, "SUCCESS")
        rc, out, err = run_cli("calibrate", ledger=ledger)
        assert rc == 2
        assert out["status"] == "insufficient_data"
        assert "9" in out["verdict"] and "10" in out["verdict"]


# ---------------------------------------------------------------------------
# Overweighting signals — hand-verified
# ---------------------------------------------------------------------------

class TestOverweighting:
    def test_signal_fires_with_exact_numbers(self, ledger):
        # mission_value 0.9 on 3 failures, 0.3 on 5 successes → gap 0.6
        for _ in range(5):
            rid = write_receipt(ledger, {"mission_value": 0.3,
                                         "evidence": 0.5})
            record_outcome(ledger, rid, "SUCCESS")
        for _ in range(3):
            rid = write_receipt(ledger, {"mission_value": 0.9,
                                         "evidence": 0.5})
            record_outcome(ledger, rid, "FAILURE")
        # need 10 total for calibration; add 2 neutral successes
        for _ in range(2):
            rid = write_receipt(ledger, {"mission_value": 0.5,
                                         "evidence": 0.5})
            record_outcome(ledger, rid, "SUCCESS")
        rc, out, err = run_cli("calibrate", ledger=ledger)
        assert rc == 0, err
        sig = next(s for s in out["overweighting"]
                   if s["dimension"] == "mission_value")
        assert sig["status"] == "overweighted_signal"
        assert sig["n_success"] == 7 and sig["n_failure"] == 3
        assert sig["gap"] >= 0.15
        ev = next(s for s in out["overweighting"]
                  if s["dimension"] == "evidence")
        assert ev["status"] == "ok"  # 0.5 everywhere → no signal

    def test_small_groups_say_insufficient(self, ledger):
        for _ in range(10):
            rid = write_receipt(ledger, {"mission_value": 0.9})
            record_outcome(ledger, rid, "SUCCESS")
        rc, out, err = run_cli("calibrate", ledger=ledger)
        sig = next(s for s in out["overweighting"]
                   if s["dimension"] == "mission_value")
        assert sig["status"] == "insufficient_data"  # 0 failures < 3


# ---------------------------------------------------------------------------
# Blind spots
# ---------------------------------------------------------------------------

class TestBlindSpots:
    def test_blind_spot_flagged(self, ledger):
        for _ in range(6):
            rid = write_receipt(ledger, {"mission_value": 0.5},
                                intent_type="should_merge")
            record_outcome(ledger, rid, "FAILURE")
        for _ in range(4):
            rid = write_receipt(ledger, {"mission_value": 0.5},
                                intent_type="what_next")
            record_outcome(ledger, rid, "SUCCESS")
        rc, out, err = run_cli("calibrate", ledger=ledger)
        spots = {s["intent_type"]: s for s in out["blind_spots"]}
        assert spots["should_merge"]["status"] == "blind_spot"
        assert spots["should_merge"]["success_rate"] == 0.0
        assert spots["what_next"]["status"] == "insufficient_data"  # n=4 < 5


# ---------------------------------------------------------------------------
# Weight proposals — conservative, never silent
# ---------------------------------------------------------------------------

class TestWeightProposals:
    def _twenty_with_signal(self, ledger):
        # 14 successes at mission_value 0.3, 6 failures at 0.9 → gap 0.6
        for _ in range(14):
            rid = write_receipt(ledger, {"mission_value": 0.3})
            record_outcome(ledger, rid, "SUCCESS")
        for _ in range(6):
            rid = write_receipt(ledger, {"mission_value": 0.9})
            record_outcome(ledger, rid, "FAILURE")

    def test_proposal_created_with_bounded_adjustment(self, ledger):
        self._twenty_with_signal(ledger)
        rc, out, err = run_cli("propose-weights", ledger=ledger)
        assert rc == 0, f"{err} {out}"
        adj = out["adjustments"]["mission_value"]
        assert adj["old"] == 0.35
        assert adj["new"] == round(0.35 * 0.90, 4)  # shrink 10%
        assert adj["new"] >= 0.05  # floor respected
        # renormalized weights sum to 1.0
        total = sum(out["renormalized_weights"].values())
        assert abs(total - 1.0) < 0.001

    def test_proposal_changes_nothing_until_accepted(self, ledger):
        self._twenty_with_signal(ledger)
        rc, out, err = run_cli("propose-weights", ledger=ledger)
        pid = out["proposal_id"]
        # the ledger has a proposal record; no weights were "applied" anywhere
        # — the tool has no path that writes weights into scoring. Verify the
        # proposal record exists and is still 'proposed'.
        recs = [json.loads(l) for l in open(ledger).read().strip().split("\n")]
        props = [r for r in recs if r.get("record_type") == "weight_proposal"]
        assert len(props) == 1 and props[0]["status"] == "proposed"
        # accept it explicitly
        rc, out, err = run_cli(
            "accept-proposal", "--proposal", pid, "--by", "shawn-test",
            ledger=ledger)
        assert rc == 0, err
        assert out["decision"] == "accepted"
        # double-decide is rejected — append-only, not re-decided
        rc, out, err = run_cli(
            "reject-proposal", "--proposal", pid, "--by", "shawn-test",
            ledger=ledger)
        assert rc == 1

    def test_reject_path(self, ledger):
        self._twenty_with_signal(ledger)
        rc, out, err = run_cli("propose-weights", ledger=ledger)
        pid = out["proposal_id"]
        rc, out, err = run_cli(
            "reject-proposal", "--proposal", pid, "--by", "shawn-test",
            ledger=ledger)
        assert rc == 0 and out["decision"] == "rejected"

    def test_unknown_proposal_rejected(self, ledger):
        rc, out, err = run_cli(
            "accept-proposal", "--proposal", "prop-nope", "--by", "x",
            ledger=ledger)
        assert rc == 1

    def test_insufficient_data_no_proposal(self, ledger):
        for _ in range(19):
            rid = write_receipt(ledger, {"mission_value": 0.9})
            record_outcome(ledger, rid, "FAILURE")
        rc, out, err = run_cli("propose-weights", ledger=ledger)
        assert rc == 2
        assert out["status"] == "insufficient_data"

    def test_no_signal_no_adjustment(self, ledger):
        for _ in range(20):
            rid = write_receipt(ledger, {"mission_value": 0.5})
            record_outcome(ledger, rid, "SUCCESS" if _ % 2 == 0 else "FAILURE")
        rc, out, err = run_cli("propose-weights", ledger=ledger)
        assert rc == 2
        assert out["status"] == "no_adjustment"


# ---------------------------------------------------------------------------
# Corrupted ledger lines — quarantined, never optimistic
# ---------------------------------------------------------------------------

class TestCorruption:
    def test_corrupted_lines_quarantined(self, ledger):
        rid = write_receipt(ledger, {"mission_value": 0.8})
        with open(ledger, "a") as f:
            f.write("this is not json at all{{{\n")
            f.write('{"record_type": "mystery", "x": 1}\n')
            f.write('{"record_type": "decision", "schema_version": "99"}\n')
            f.write("\n")  # blank lines are fine, skipped
        record_outcome(ledger, rid, "SUCCESS")
        rc, out, err = run_cli("show-ledger", ledger=ledger)
        assert rc == 0, err
        assert out["records"] == 2  # only the 2 valid records load
        assert out["quarantined_lines"] == 3


# ---------------------------------------------------------------------------
# Ledger summary
# ---------------------------------------------------------------------------

class TestShowLedger:
    def test_summary_counts(self, ledger):
        r1 = write_receipt(ledger, {"mission_value": 0.8})
        r2 = write_receipt(ledger, {"mission_value": 0.2})
        record_outcome(ledger, r1, "SUCCESS")
        rc, out, err = run_cli("show-ledger", ledger=ledger)
        assert rc == 0
        assert out["by_type"] == {"decision": 2, "outcome": 1}
        assert out["decisions_with_known_outcomes"] == 1
        assert out["quarantined_lines"] == 0

# ---------------------------------------------------------------------------
# Outcome precedence and range robustness
# ---------------------------------------------------------------------------

class TestOutcomePrecedence:
    def test_latest_outcome_wins(self, ledger):
        # self-reported FAILURE, later VERIFIED as SUCCESS → SUCCESS counts
        rid = write_receipt(ledger, {"mission_value": 0.5}, confidence=0.8)
        record_outcome(ledger, rid, "FAILURE", "SELF_REPORTED")
        record_outcome(ledger, rid, "SUCCESS", "VERIFIED")
        for _ in range(9):
            r = write_receipt(ledger, {"mission_value": 0.5}, confidence=0.8)
            record_outcome(ledger, r, "SUCCESS")
        rc, out, err = run_cli("calibrate", ledger=ledger)
        assert rc == 0, err
        bin80 = next(b for b in out["bins"] if b["range"][0] == 0.8)
        assert bin80["observed_rate"] == 1.0  # 10/10 SUCCESS

    def test_out_of_range_confidence_clamped_not_dropped(self, ledger):
        # absurd confidence 1.5 → warning recorded, clamped to top bin,
        # still counted (n includes it)
        for _ in range(10):
            rid = write_receipt(ledger, {"mission_value": 0.5}, confidence=1.5)
            record_outcome(ledger, rid, "SUCCESS")
        rec = json.loads(open(ledger).read().strip().split("\n")[0])
        assert any("outside [0,1]" in w for w in rec["warnings"])
        rc, out, err = run_cli("calibrate", ledger=ledger)
        assert rc == 0, err
        assert out["n_decisions"] == 10
        top = next(b for b in out["bins"] if b["range"][0] == 0.9)
        assert top["n"] == 10  # clamped into the top bin, not vanished

# ---------------------------------------------------------------------------
# Cross-layer interface compatibility — real Layer 4 output, not invented shapes
# ---------------------------------------------------------------------------

class TestRealLayerInterfaces:
    def test_real_layer4_failclosed_output_makes_honest_receipt(self, ledger):
        # The REAL evidence_scorer.score_options, called for real, on its
        # fail-closed path (no options). The receipt must capture it without
        # inventing a recommendation.
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
        import evidence_scorer as es
        real_out = es.score_options({"intent_type": "x"}, [], None)
        assert real_out["ok"] is False  # the real tool refused, honestly
        rc, out, err = run_cli(
            "write-receipt",
            "--scored", json.dumps(real_out),
            "--intent", json.dumps({"intent_type": None}),
            ledger=ledger)
        assert rc == 0, err
        rec = json.loads(open(ledger).read().strip().split("\n")[0])
        assert rec["recommendation"] is None
        assert rec["predicted_confidence"] is None
        assert "nothing to score" in rec["notes"][0]

    def test_real_layer4_scored_output_roundtrips(self, ledger):
        # A realistic REAL-shaped scored output (shapes verified against the
        # actual score_options source): dimensions with value/confidence/
        # evidence, weights + weights_schema_version, unknown_dimensions.
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
        import evidence_scorer as es
        assert es.WEIGHTS_SCHEMA_VERSION  # the field really exists
        scored = {
            "ok": True, "exit_hint": 0, "intent_type": "should_merge",
            "objective": "Determine whether the change is safe",
            "weights": dict(es.WEIGHTS),
            "weights_schema_version": es.WEIGHTS_SCHEMA_VERSION,
            "options": [{
                "id": "pr-1", "title": "Merge PR #1", "source": "PR #1",
                "source_type": "pr", "gated": False, "gate_reasons": [],
                "dimensions": {
                    "mission_value": {"value": 0.8, "confidence": 0.9,
                                      "evidence": ["closes gap"]},
                    "evidence": {"value": 0.7, "confidence": 0.8,
                                 "evidence": []},
                    "risk": {"value": 0.6, "confidence": 0.7, "evidence": []},
                    "cost": {"value": 0.5, "confidence": 0.6, "evidence": []},
                    "urgency": {"value": 0.4, "confidence": 0.5,
                                "evidence": []},
                },
                "total": 0.66, "total_confidence": 0.82,
                "unknown_dimensions": [], "rank": 1,
            }],
            "recommendation": {"option_id": "pr-1", "title": "Merge PR #1",
                               "total": 0.66, "total_confidence": 0.82},
            "notes": [], "warnings": [],
            "scored_utc": "2026-10-12T00:00:00+00:00",
        }
        rc, out, err = run_cli(
            "write-receipt", "--scored", json.dumps(scored),
            "--intent", json.dumps({"intent_type": "should_merge"}),
            ledger=ledger)
        assert rc == 0, err
        assert out["predicted_confidence"] == 0.82
        rec = json.loads(open(ledger).read().strip().split("\n")[0])
        assert rec["weights_schema_version"] == es.WEIGHTS_SCHEMA_VERSION
        assert rec["options"][0]["dimensions"]["mission_value"]["value"] == 0.8
