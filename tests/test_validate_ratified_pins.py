"""Battery for the ratified-pins validator (Naya Builder, 2026-10-14).

The incident: `.naya/governance/STANDING-PRODUCTION-PROMOTION-V1.json`
claimed `"status": "RATIFIED"` on a word-based authority with zero pin
fields — CLAIMED-UNVERIFIED, never ratified (NO-WORD RATIFICATION law).

The repair under test: `tools/validate_ratified_pins.py` FAILs any
`status: RATIFIED` governance JSON lacking scorecard pins (scorecard IDs +
content hash + reviewer seats). The strongest regression test pins the
historical bug itself: the original file bytes with status RATIFIED and no
pins MUST fail.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from validate_ratified_pins import (
    validate_file,
    validate_dir,
    record_content_sha256,
    main,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
REAL_POLICY = (
    REPO_ROOT / ".naya" / "governance" / "STANDING-PRODUCTION-PROMOTION-V1.json"
)

GOOD_HASH = "4c28293acb9b1181ebe92b0526ccfc31d9d0155f21240dec54fff6a27974dd6b"


def _activation(**overrides):
    act = {
        "authority": "SCORING_MATRIX",
        "recorded_at": "2026-10-14",
        "evidence_record": "BRAIN/06-PROOF/test.md",
    }
    act.update(overrides)
    act["record_content_sha256"] = record_content_sha256(act)
    return act


def _scorecard(**overrides):
    sc = {
        "scorecard_id": "venue-2537-9999999999",
        "reviewer_seat": "main seat (Naya 2)",
        "scored_at": "2026-10-14T13:45:03Z",
        "score": 9.6,
        "ratification_threshold": 9.5,
        "reviewed_content_sha256": GOOD_HASH,
        "artifact_sha256": GOOD_HASH,
    }
    sc.update(overrides)
    return sc


def _ratified_doc(**overrides):
    doc = {
        "schema": "TEST_GOVERNANCE_V1",
        "policy_id": "TEST-POLICY-V1",
        "status": "RATIFIED",
        "ratification": {
            "authority": "SCORING_MATRIX",
            "ratified_at": "2026-10-14",
            "pins": {"scorecards": [_scorecard()]},
        },
        "activation": _activation(),
    }
    doc.update(overrides)
    return doc


def _write(tmp_path, name, obj):
    p = tmp_path / name
    p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return p


# ---- PASS legs -----------------------------------------------------------

def test_ratified_with_complete_pins_passes(tmp_path):
    p = _write(tmp_path, "ok.json", _ratified_doc())
    assert validate_file(p) == []


def test_candidate_without_pins_passes(tmp_path):
    doc = _ratified_doc(status="CANDIDATE")
    doc.pop("ratification")
    doc.pop("activation")
    p = _write(tmp_path, "candidate.json", doc)
    assert validate_file(p) == []


def test_draft_without_pins_passes(tmp_path):
    p = _write(tmp_path, "draft.json", {"policy_id": "X", "status": "DRAFT"})
    assert validate_file(p) == []


def test_empty_governance_dir_passes_with_note(tmp_path):
    assert validate_dir(tmp_path) == {}


# ---- FAIL legs: the pin gap ----------------------------------------------

def test_ratified_missing_ratification_block_fails(tmp_path):
    doc = _ratified_doc()
    doc.pop("ratification")
    p = _write(tmp_path, "nopins.json", doc)
    errs = validate_file(p)
    assert errs and any("ratification" in e for e in errs)


def test_ratified_word_authority_fails(tmp_path):
    doc = _ratified_doc()
    doc["ratification"]["authority"] = "HUMAN_DIRECTOR"
    p = _write(tmp_path, "word.json", doc)
    errs = validate_file(p)
    assert errs and any("SCORING_MATRIX" in e for e in errs)


def test_ratified_below_bar_scorecard_fails(tmp_path):
    doc = _ratified_doc()
    doc["ratification"]["pins"]["scorecards"] = [_scorecard(score=6.9)]
    p = _write(tmp_path, "lowbar.json", doc)
    errs = validate_file(p)
    assert errs and any("below-bar" in e for e in errs)


def test_ratified_missing_reviewer_seat_fails(tmp_path):
    sc = _scorecard()
    sc.pop("reviewer_seat")
    doc = _ratified_doc()
    doc["ratification"]["pins"]["scorecards"] = [sc]
    p = _write(tmp_path, "noseat.json", doc)
    errs = validate_file(p)
    assert errs and any("reviewer_seat" in e for e in errs)


def test_ratified_malformed_hash_fails(tmp_path):
    doc = _ratified_doc()
    doc["ratification"]["pins"]["scorecards"] = [
        _scorecard(reviewed_content_sha256="not-a-hash")
    ]
    p = _write(tmp_path, "badhash.json", doc)
    errs = validate_file(p)
    assert errs and any("reviewed_content_sha256" in e for e in errs)


def test_ratified_tampered_activation_record_fails(tmp_path):
    doc = _ratified_doc()
    doc["activation"]["recorded_at"] = "2020-01-01"  # alter AFTER pinning
    p = _write(tmp_path, "tampered.json", doc)
    errs = validate_file(p)
    assert errs and any("record_content_sha256" in e for e in errs)


def test_ratified_missing_activation_block_fails(tmp_path):
    doc = _ratified_doc()
    doc.pop("activation")
    p = _write(tmp_path, "noact.json", doc)
    errs = validate_file(p)
    assert errs and any("activation" in e for e in errs)


# ---- fail-closed inputs ---------------------------------------------------

def test_invalid_json_fails_closed(tmp_path):
    p = tmp_path / "broken.json"
    p.write_text("{not json", encoding="utf-8")
    errs = validate_file(p)
    assert errs and any("FAIL CLOSED" in e for e in errs)


def test_missing_governance_dir_fails_closed(tmp_path):
    results = validate_dir(tmp_path / "does-not-exist")
    assert results and any("FAIL CLOSED" in e for v in results.values() for e in v)


# ---- revert leg: the gate actually gates ----------------------------------

def test_revert_proves_gating(tmp_path):
    p = _write(tmp_path, "flip.json", _ratified_doc())
    assert validate_file(p) == []                       # GREEN clean
    doc = json.loads(p.read_text(encoding="utf-8"))
    doc["ratification"].pop("pins")                     # plant the RED
    p.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    assert validate_file(p) != []                       # planted RED blocks
    p.write_text(json.dumps(_ratified_doc(), indent=2), encoding="utf-8")
    assert validate_file(p) == []                       # revert restores


# ---- the historical bug, pinned -------------------------------------------

def test_historical_bug_pin_stripped_ratified_fails(tmp_path):
    """The original production-promotion policy bytes: status RATIFIED,
    zero pin fields. The validator must FAIL them — this is the bug class."""
    historical = {
        "schema": "NAYAPOWER_STANDING_PRODUCTION_PROMOTION_POLICY_V1",
        "policy_id": "STANDING-PRODUCTION-PROMOTION-V1",
        "version": "1.0.0",
        "status": "RATIFIED",
        "ratification": {
            "authority": "HUMAN_DIRECTOR",
            "ratified_at": "2026-09-29",
            "ratification_scope": "Narrow standing authorization.",
            "constitutional_amendment": "STANDING-PRODUCTION-AUTHORIZATION-AMENDMENT-V1",
        },
        "activation": {"authority": "HUMAN_DIRECTOR", "recorded_at": "2026-09-29"},
    }
    p = _write(tmp_path, "historical.json", historical)
    errs = validate_file(p)
    assert len(errs) >= 3  # authority + scorecards + activation hash


@pytest.mark.skipif(not REAL_POLICY.exists(), reason="repo file not present")
def test_real_fixed_policy_file_passes():
    """The shipped fix: status CANDIDATE, score-derived authority, pins
    populated — the validator passes the real tree."""
    assert validate_file(REAL_POLICY) == []


# ---- CLI wiring (the exact command the workflow step runs) ----------------

def _cli(*args):
    tool = REPO_ROOT / "tools" / "validate_ratified_pins.py"
    return subprocess.run(
        [sys.executable, str(tool), *args],
        capture_output=True, text=True,
    )


def test_cli_clean_tree_exit_zero(tmp_path):
    _write(tmp_path, "ok.json", _ratified_doc())
    r = _cli("--governance-dir", str(tmp_path))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "PASS" in r.stdout


def test_cli_pin_stripped_exit_nonzero(tmp_path):
    doc = _ratified_doc()
    doc["ratification"].pop("pins")
    _write(tmp_path, "stripped.json", doc)
    r = _cli("--governance-dir", str(tmp_path))
    assert r.returncode != 0
    assert "FAIL" in r.stdout


def test_cli_json_report(tmp_path):
    _write(tmp_path, "ok.json", _ratified_doc())
    r = _cli("--governance-dir", str(tmp_path), "--json")
    assert r.returncode == 0
    report = json.loads(r.stdout)
    assert report["ok"] is True and report["files_checked"] == 1
