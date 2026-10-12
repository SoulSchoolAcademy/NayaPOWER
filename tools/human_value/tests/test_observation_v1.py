"""Tests for the observed-experience instrument v1.

Covers: schema v2 fail-closed validation, the candidate lifecycle
(promote/expire, append-only), the stated-vs-revealed conflict rule, the
report buckets, the adversarial attacks, the design doc's worked examples,
and the §5 calibration known-answer battery over the 2026-10-11 -> 2026-10-12
window (Shawn's own recorded words).

All fixtures are SYNTHETIC calibration vectors (fixture: true). They prove
the machinery works mechanically. They are not measurements of any human.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.human_value.observation_schema import (  # noqa: E402
    SchemaError,
    expired_candidates,
    fold_candidates,
    project_to_schema,
    validate_candidate,
    validate_event_v2,
    validate_observation_ledger,
    validate_sweep,
)
from tools.human_value.observe import (  # noqa: E402
    collect,
    observation_triples,
    resolve_conflict,
)

OBSERVE_PY = REPO_ROOT / "tools" / "human_value" / "observe.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def run_observe(*argv: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(OBSERVE_PY), *argv],
        capture_output=True,
        text=True,
        cwd=str(cwd or REPO_ROOT),
    )


def good_event(**overrides) -> dict:
    base = {
        "schema_version": "2",
        "event_id": "OBS-TEST-001",
        "recorded_at": "2026-10-12",
        "value_type": "useful_outcome",
        "value_units": 1,
        "unit_description": "one asserted experience of the test passing",
        "evidence": [{"kind": "content_hash", "ref": "sha256:" + "cd" * 32}],
        "observation_kind": "stated",
        "subject": "human_self",
        "observed_by": "naya-epsilon",
        "observed_at": "2026-10-12T06:00:00Z",
        "collected_at": "2026-10-12T07:00:00Z",
        "verbatim_hash": "sha256:" + "ab" * 32,
        "authorship": "direct",
        "collector_inference": "test: human asserts the test passed; 1 unit = 1 asserted experience",
        "promotion": None,
    }
    base.update(overrides)
    return base


def good_candidate(**overrides) -> dict:
    base = {
        "schema_version": "1",
        "candidate_id": "CAND-TEST-001",
        "graded_value_type": "useful_outcome",
        "graded_units": 9.2,
        "graded_by": "naya-mu",
        "graded_at": "2026-10-12T06:56:00Z",
        "expires_at": "2026-11-02T06:56:00Z",
        "status": "pending",
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# schema v2: fail-closed validation
# ---------------------------------------------------------------------------

class TestSchemaFailClosed:
    def test_valid_event_passes(self):
        assert validate_event_v2(good_event())["event_id"] == "OBS-TEST-001"

    def test_unknown_field_rejected(self):
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(surprise="field"))

    def test_missing_evidence_rejected(self):
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(evidence=[]))

    def test_uncertain_authorship_with_promotion_rejected(self):
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(authorship="uncertain", promotion="CAND-TEST-001"))

    def test_uncertain_authorship_standalone_allowed(self):
        # Uncertain authorship can be recorded as a standalone observation for
        # the review surface, but it can never promote.
        validate_event_v2(good_event(authorship="uncertain", promotion=None))

    def test_unknown_observation_kind_rejected(self):
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(observation_kind="vibes"))

    def test_corrected_requires_attention_demanded(self):
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(observation_kind="corrected", value_type="useful_outcome"))

    def test_attention_demanded_requires_corrected(self):
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(value_type="attention_demanded", observation_kind="stated"))

    def test_corrected_attention_demanded_passes(self):
        validate_event_v2(good_event(observation_kind="corrected", value_type="attention_demanded"))

    def test_bad_verbatim_hash_rejected(self):
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(verbatim_hash="not-a-hash"))

    def test_collected_before_observed_rejected(self):
        with pytest.raises(SchemaError):
            validate_event_v2(
                good_event(observed_at="2026-10-12T07:00:00Z", collected_at="2026-10-12T06:00:00Z")
            )

    def test_units_must_be_positive_int_counts(self):
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(value_units=0))
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(value_units=4.5))
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(value_units="one"))

    def test_self_observation_without_direct_statement_rejected(self):
        with pytest.raises(SchemaError):
            validate_event_v2(
                good_event(
                    observatory_subject=True,
                    authorship="inferred",
                    evidence=[{"kind": "receipt", "ref": "tools/human_value/ledgers/observation-sweeps.jsonl"}],
                )
            )

    def test_self_observation_with_direct_statement_allowed(self):
        # The one exception: a DIRECT human statement about the observatory.
        validate_event_v2(
            good_event(
                observatory_subject=True,
                authorship="direct",
                observation_kind="stated",
                evidence=[{"kind": "feed_comment", "ref": "https://github.com/x/y/issues/1#issuecomment-2"}],
            )
        )

    def test_assessor_equals_collector_rejected_at_promote(self):
        cand = good_candidate(graded_by="naya-epsilon")
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(observed_by="naya-epsilon"), candidate=cand)

    def test_builder_equals_collector_rejected_at_promote(self):
        cand = good_candidate(graded_by="naya-mu", built_by="naya-epsilon")
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(observed_by="naya-epsilon"), candidate=cand)

    def test_wrong_schema_version_rejected(self):
        with pytest.raises(SchemaError):
            validate_event_v2(good_event(schema_version="1"))

    def test_amendment_links_prior_event(self):
        ev = validate_event_v2(
            good_event(
                event_id="OBS-TEST-002",
                observation_kind="corrected",
                value_type="attention_demanded",
                supersedes="OBS-TEST-001",
            )
        )
        assert ev["supersedes"] == "OBS-TEST-001"


# ---------------------------------------------------------------------------
# candidates: lifecycle and append-only folding
# ---------------------------------------------------------------------------

class TestCandidates:
    def test_fold_takes_latest_status(self):
        records = [
            good_candidate(),
            {**good_candidate(), "status": "promoted", "note": "promoted by OBS-TEST-001"},
        ]
        folded = fold_candidates(records)
        assert folded["CAND-TEST-001"]["status"] == "promoted"

    def test_expire_marks_stale_candidates(self):
        folded = fold_candidates([good_candidate(candidate_id="C1", expires_at="2026-09-22T00:00:00Z")])
        assert expired_candidates(folded, "2026-10-12T00:00:00Z") == ["C1"]
        assert expired_candidates(folded, "2026-09-01T00:00:00Z") == []

    def test_valid_sweep_and_null_sweep(self):
        sweep = {
            "sweep_id": "SWEEP-20261012",
            "swept_at": "2026-10-12T08:00:00Z",
            "watermark_start": "2026-10-05T00:00:00Z",
            "watermark_end": "2026-10-12T08:00:00Z",
            "channels": ["c1", "c2", "c3"],
            "observations_found": 0,
            "promotions_proposed": 0,
            "null_sweep": True,
            "collector": "naya-mu",
            "note": "quiet week: searched, found nothing, logged it",
        }
        assert validate_sweep(sweep)["null_sweep"] is True
        with pytest.raises(SchemaError):
            validate_sweep({**sweep, "observations_found": 2, "null_sweep": True})


# ---------------------------------------------------------------------------
# collector rules: conflict resolution
# ---------------------------------------------------------------------------

class TestConflictRule:
    def test_stated_vs_revealed_conflict_labeled(self):
        obs = resolve_conflict(
            [
                {"observation_kind": "stated", "artifact": "dash", "verbatim_hash": "sha256:" + "aa" * 32},
                {"observation_kind": "revealed", "artifact": "dash", "verbatim_hash": "sha256:" + "bb" * 32},
            ]
        )
        assert all("conflict" in o for o in obs)
        assert "revealed governs continued value" in obs[0]["conflict"]["resolution"]

    def test_no_conflict_no_label(self):
        obs = resolve_conflict(
            [{"observation_kind": "stated", "artifact": "dash", "verbatim_hash": "sha256:" + "aa" * 32}]
        )
        assert "conflict" not in obs[0]


# ---------------------------------------------------------------------------
# worked examples from the design doc
# ---------------------------------------------------------------------------

class TestWorkedExamples:
    def test_grading_pass_units_come_from_observation_not_grader(self, tmp_path: Path):
        # Design worked example 1: PR #2455 graded 9.2 by naya-mu. If Shawn
        # says "the grading pass is exactly what I needed", the promoted
        # event credits 1 unit (one asserted experience) — never 9.2.
        ledgers = tmp_path / "ledgers"
        ledgers.mkdir()
        (ledgers / "pending-candidates.jsonl").write_text(
            json.dumps(good_candidate(candidate_id="CAND-20261012-001", pr=2455)) + "\n"
        )
        observation = good_event(
            event_id="OBS-20261012-001",
            observed_by="naya-epsilon",
            unit_description="one asserted experience of the grading pass being what the human needed",
            value_units=1,
            evidence=[{"kind": "content_hash", "ref": "sha256:" + "11" * 32}],
            promotion="CAND-20261012-001",
        )
        r = run_observe(
            "promote", "--ledgers", str(ledgers),
            "--candidate", "CAND-20261012-001",
            "--observation", json.dumps(observation),
        )
        assert r.returncode == 0, r.stderr
        events = read_jsonl(ledgers / "observed-events.jsonl")
        assert events[0]["value_units"] == 1  # the observation's count, not the grader's 9.2
        folded = fold_candidates(read_jsonl(ledgers / "pending-candidates.jsonl"))
        assert folded["CAND-20261012-001"]["status"] == "promoted"

    def test_promote_is_append_only(self, tmp_path: Path):
        ledgers = tmp_path / "ledgers"
        ledgers.mkdir()
        cand_line = json.dumps(good_candidate()) + "\n"
        (ledgers / "pending-candidates.jsonl").write_text(cand_line)
        r = run_observe(
            "promote", "--ledgers", str(ledgers),
            "--candidate", "CAND-TEST-001",
            "--observation", json.dumps(good_event(observed_by="naya-epsilon")),
        )
        assert r.returncode == 0, r.stderr
        lines = (ledgers / "pending-candidates.jsonl").read_text().splitlines()
        assert lines[0] == cand_line.rstrip("\n")  # original bytes untouched
        assert len(lines) == 2  # status change is a new line, not an edit

    def test_cold_successor_revealed_observation(self, tmp_path: Path):
        # Design worked example 2: "Tell me when you want me to run the test,
        # give me the list of questions." -> REVEALED, 1 unit.
        ledgers = tmp_path / "ledgers"
        ledgers.mkdir()
        (ledgers / "pending-candidates.jsonl").write_text(
            json.dumps(good_candidate(candidate_id="CAND-IOTA-001", graded_by="naya-epsilon",
                                     built_by="naya-iota")) + "\n"
        )
        observation = good_event(
            event_id="OBS-20261012-002",
            observation_kind="revealed",
            observed_by="naya-mu",
            unit_description="one observed act of the human volunteering as the test instrument",
            promotion="CAND-IOTA-001",
        )
        r = run_observe(
            "promote", "--ledgers", str(ledgers),
            "--candidate", "CAND-IOTA-001",
            "--observation", json.dumps(observation),
        )
        assert r.returncode == 0, r.stderr
        events = read_jsonl(ledgers / "observed-events.jsonl")
        assert events[0]["observation_kind"] == "revealed"
        assert events[0]["value_units"] == 1

    def test_expire_command(self, tmp_path: Path):
        ledgers = tmp_path / "ledgers"
        ledgers.mkdir()
        (ledgers / "pending-candidates.jsonl").write_text(
            json.dumps(good_candidate(expires_at="2026-09-22T00:00:00Z")) + "\n"
        )
        r = run_observe("expire", "--ledgers", str(ledgers), "--as-of", "2026-10-12T00:00:00Z")
        assert r.returncode == 0, r.stderr
        folded = fold_candidates(read_jsonl(ledgers / "pending-candidates.jsonl"))
        assert folded["CAND-TEST-001"]["status"] == "unobserved"

    def test_report_buckets_and_formative_banner(self, tmp_path: Path):
        ledgers = tmp_path / "ledgers"
        ledgers.mkdir()
        (ledgers / "observed-events.jsonl").write_text(json.dumps(good_event()) + "\n")
        (ledgers / "pending-candidates.jsonl").write_text(
            json.dumps(good_candidate(candidate_id="P1", status="pending")) + "\n"
            + json.dumps(good_candidate(candidate_id="U1", status="unobserved")) + "\n"
        )
        (ledgers / "observation-sweeps.jsonl").write_text(
            json.dumps({
                "sweep_id": "S1", "swept_at": "2026-10-12T08:00:00Z",
                "watermark_start": "2026-10-05T00:00:00Z", "watermark_end": "2026-10-12T08:00:00Z",
                "channels": ["c1", "c2", "c3"], "observations_found": 1,
                "promotions_proposed": 1, "null_sweep": False, "collector": "naya-mu",
            }) + "\n"
        )
        status = tmp_path / "cal.json"
        status.write_text(json.dumps({"known_answer": "pass"}))
        r = run_observe("report", "--ledgers", str(ledgers), "--week", "2026-10-12",
                        "--calibration-status", str(status))
        assert r.returncode == 0, r.stderr
        report = json.loads(r.stdout)
        assert len(report["buckets"]["OBSERVED"]) == 1
        assert len(report["buckets"]["PENDING"]) == 1
        assert len(report["buckets"]["UNOBSERVED"]) == 1
        assert "FORMATIVE" in report["banner"]  # banner lifts only when all three checks pass
        assert len(report["null_sweep_log"]) == 1


# ---------------------------------------------------------------------------
# adversarial attacks (self-administered; Coda 1's independent review deferred)
# ---------------------------------------------------------------------------

class TestAdversarial:
    @pytest.mark.parametrize("kind", ["graded_phantom", "uncertain_authorship", "self_observation"])
    def test_attack_rejected(self, kind: str):
        r = run_observe("attack", "--kind", kind)
        assert r.returncode == 0, r.stderr
        result = json.loads(r.stdout)
        assert result["rejected"] is True, f"SCHEMA HOLE: {kind} was accepted"


# ---------------------------------------------------------------------------
# §5 calibration: the pre-registered known-answer battery
# ---------------------------------------------------------------------------

class TestKnownAnswerBattery:
    def test_pin_then_run_exact_match(self, tmp_path: Path):
        # STEP 1 — pin the key BEFORE the instrument runs (no peeking).
        key = FIXTURES / "known_answer_key.json"
        pin_path = tmp_path / "key.pin.json"
        r = run_observe("calibrate", "pin", "--key", str(key),
                        "--key-id", "OBS-CAL-KEY-20261012", "--who", "naya-mu",
                        "--out", str(pin_path))
        assert r.returncode == 0, r.stderr
        pin = json.loads(pin_path.read_text())
        assert pin["key_sha256"].startswith("sha256:")

        # STEP 2 — the instrument runs over the fixture window.
        out_path = tmp_path / "battery.json"
        r = run_observe(
            "calibrate", "run",
            "--key", str(key),
            "--pin", str(pin_path),
            "--raw", str(FIXTURES / "known_answer_raw.jsonl"),
            "--candidates", str(FIXTURES / "known_answer_candidates.jsonl"),
            "--out", str(out_path),
        )
        assert r.returncode == 0, r.stderr
        result = json.loads(out_path.read_text())

        # STEP 3 — mechanical comparison: exact keyed set, zero phantoms.
        assert result["match"] is True, f"missing={result['missing']} phantoms={result['phantoms']}"
        assert result["expected"] == 6
        assert result["produced"] == 6
        assert result["phantoms"] == []
        assert result["dropped_by_collector"] + result["dropped_by_schema"] == 3

    def test_tampered_key_invalidates_calibration(self, tmp_path: Path):
        key = FIXTURES / "known_answer_key.json"
        pin_path = tmp_path / "key.pin.json"
        assert run_observe("calibrate", "pin", "--key", str(key), "--key-id", "K",
                           "--who", "naya-mu", "--out", str(pin_path)).returncode == 0
        tampered = tmp_path / "key.json"
        shutil.copy(key, tampered)
        tampered.write_text(tampered.read_text().replace("OBS-CAL-KEY-20261012", "OBS-CAL-KEY-TAMPERED"))
        r = run_observe(
            "calibrate", "run", "--key", str(tampered), "--pin", str(pin_path),
            "--raw", str(FIXTURES / "known_answer_raw.jsonl"),
            "--candidates", str(FIXTURES / "known_answer_candidates.jsonl"),
        )
        assert r.returncode != 0  # byte drift after pinning fails closed

    def test_sweep_marks_would_reject_proposals(self, tmp_path: Path):
        # The review surface pre-checks each proposal against promote-time
        # validation: the self-observation probe must show would_reject.
        ledgers = tmp_path / "ledgers"
        ledgers.mkdir()
        (ledgers / "pending-candidates.jsonl").write_text(
            "\n".join(open(FIXTURES / "known_answer_candidates.jsonl").read().splitlines()) + "\n"
        )
        r = run_observe(
            "sweep", "--raw", str(FIXTURES / "known_answer_raw.jsonl"),
            "--ledgers", str(ledgers), "--since", "2026-10-11", "--channels", "c1,c2,c3",
        )
        assert r.returncode == 0, r.stderr
        proposal = json.loads(r.stdout)
        by_id = {p["observation"]["event_id"]: p for p in proposal["proposed_promotions"]}
        assert by_id["OBS-FIX-20261012-903"]["promotion_validation"].startswith("would_reject")
        assert by_id["OBS-FIX-20261012-001"]["promotion_validation"] == "would_pass"
        # the uncertain-authorship probe never reaches the proposal surface
        assert "OBS-FIX-20261012-901" not in by_id
        assert any("uncertain authorship" in d["reason"] for d in proposal["dropped"])

    def test_calibration_report_one_shot(self, tmp_path: Path):
        out = tmp_path / "calibration-report.json"
        r = run_observe("calibration-report", "--fixtures", str(FIXTURES), "--out", str(out))
        assert r.returncode == 0, r.stderr
        report = json.loads(out.read_text())
        assert report["battery"]["match"] is True
        assert report["battery"]["phantoms"] == []
        assert report["agreement"]["pass"] is True
        assert all(a["rejected"] for a in report["attacks"])
        # The banner stays FORMATIVE until a real second seat runs agreement.
        assert "FORMATIVE" in report["banner"]
        assert report["calibration_status"]["two_seat_agreement"] == "provisional-pass"

    def test_inter_collector_agreement_two_passes(self):
        # Provisional: both passes below are authored by the calibration
        # runner (different collector seats, one fresh pass). The §5 check
        # requires two INDEPENDENT seats; that check is PENDING and the
        # report banner stays FORMATIVE until it runs.
        # Pass A: the 6 valid observations from the calibration raw set.
        # Pass B: an independently authored second pass (sweep_b.jsonl).
        sweep_a = [o for o in read_jsonl(FIXTURES / "known_answer_raw.jsonl")
                   if o["event_id"].startswith("OBS-FIX-20261012-00")]
        sweep_b = read_jsonl(FIXTURES / "sweep_b.jsonl")
        a, b = observation_triples(sweep_a), observation_triples(sweep_b)
        union = a | b
        jaccard = len(a & b) / len(union)
        assert jaccard >= 0.8, f"agreement {jaccard} below target"
        # Also through the CLI seam.
        a_path = FIXTURES / "_sweep_a_tmp.jsonl"
        a_path.write_text("\n".join(json.dumps(o) for o in sweep_a) + "\n")
        try:
            r = run_observe("agreement", "--sweep-a", str(a_path),
                            "--sweep-b", str(FIXTURES / "sweep_b.jsonl"))
            assert r.returncode == 0, r.stderr
            assert json.loads(r.stdout)["pass"] is True
        finally:
            a_path.unlink(missing_ok=True)


class TestPromoteRevalidateRoundTrip:
    """Regression: the first-light sweep (2026-10-12) found that `promote`
    validated the INPUT event but stored it with schema_version '1' (the v1
    seam's stamp leaking through `dict(base)`). The ledger then failed its own
    re-validation — the instrument could not read back what it had just
    written. The stored event must carry the version it was validated against.
    """

    def test_promote_stores_schema_version_2(self, tmp_path):
        ledgers = tmp_path / "ledgers"
        ledgers.mkdir()
        r = run_observe("promote", "--ledgers", str(ledgers),
                        "--observation", json.dumps(good_event(event_id="OBS-RT-001")))
        assert r.returncode == 0, r.stderr
        stored = read_jsonl(ledgers / "observed-events.jsonl")
        assert len(stored) == 1
        assert stored[0]["schema_version"] == "2", (
            f"stored schema_version is {stored[0]['schema_version']!r}, not '2'"
        )

    def test_promoted_ledger_revalidates(self, tmp_path):
        ledgers = tmp_path / "ledgers"
        ledgers.mkdir()
        for i in (1, 2):
            r = run_observe("promote", "--ledgers", str(ledgers),
                            "--observation",
                            json.dumps(good_event(event_id=f"OBS-RT-00{i}")))
            assert r.returncode == 0, r.stderr
        stored = read_jsonl(ledgers / "observed-events.jsonl")
        # This is the exact call the first-light sweep tripped on: it must not raise.
        validated = validate_observation_ledger(stored)
        assert len(validated) == 2
        assert all(e["schema_version"] == "2" for e in validated)

    def test_report_reads_promoted_ledger(self, tmp_path):
        ledgers = tmp_path / "ledgers"
        ledgers.mkdir()
        r = run_observe("promote", "--ledgers", str(ledgers),
                        "--observation", json.dumps(good_event(event_id="OBS-RT-009")))
        assert r.returncode == 0, r.stderr
        r2 = run_observe("report", "--ledgers", str(ledgers), "--week", "2026-10-12")
        assert r2.returncode == 0, r2.stderr
        report = json.loads(r2.stdout)
        assert report["metrics"]["hv_observed_units"] == 1
        assert report["buckets"]["OBSERVED"][0]["event_id"] == "OBS-RT-009"
