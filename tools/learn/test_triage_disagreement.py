"""Unit tests for tools/learn/triage_disagreement.py.

Covers the three fixture classes from the mission spec:
  1. dissolves-on-reread  -> READER_VARIANCE (Battery D TR-8DB748, real case)
  2. persists-on-reread    -> RUBRIC_REVIEW
  3. escalate-with-evidence -> the evidence pack is complete and honest
plus the machine-enforced guards: genuine-disagreement-only, frozen rubric,
sha match, reader information isolation, and the "na" edge.
"""
import dataclasses
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from triage_disagreement import (  # noqa: E402
    READER_VARIANCE,
    RUBRIC_REVIEW,
    DisagreementRecord,
    ReadRequest,
    TriageError,
    Vote,
    clear_frozen_rubrics,
    register_frozen_rubric,
    triage_disagreement,
)

HERE = os.path.dirname(os.path.abspath(__file__))


def load_fixture(name):
    return json.load(open(os.path.join(HERE, "fixtures", name)))


def build_record(fx):
    sha = register_frozen_rubric(fx["record"]["rubric_id"], fx["rubric_text"])
    return (
        DisagreementRecord(
            item_id=fx["record"]["item_id"],
            cell=fx["record"]["cell"],
            rubric_id=fx["record"]["rubric_id"],
            rubric_sha256=sha,
            votes=[Vote(**v) for v in fx["record"]["votes"]],
        ),
        fx["item_text"],
        fx["rubric_text"],
    )


def replay_reader(votes):
    it = iter(votes)

    def _read(req: ReadRequest) -> Vote:
        return next(it)

    return _read


@pytest.fixture(autouse=True)
def _clean_registry():
    clear_frozen_rubrics()
    yield
    clear_frozen_rubrics()


# --- 1. dissolves-on-reread -------------------------------------------------

def test_dissolves_on_reread_gives_reader_variance():
    fx = load_fixture("battery_d_TR-8DB748.json")
    record, item_text, rubric_text = build_record(fx)
    verdict = triage_disagreement(
        record,
        replay_reader([Vote(**v) for v in fx["fresh_votes"]]),
        n_readers=3,
        item_text=item_text,
        rubric_text=rubric_text,
    )
    assert verdict.verdict == READER_VARIANCE == fx["expected_verdict"]
    assert verdict.fresh_unanimous is True
    assert verdict.evidence["instrument_change"] is None
    assert verdict.evidence["no_regrade_performed"] is True


# --- 2. persists-on-reread ---------------------------------------------------

def test_persists_on_reread_escalates_to_rubric_review():
    fx = load_fixture("disagreement_persists.json")
    record, item_text, rubric_text = build_record(fx)
    verdict = triage_disagreement(
        record,
        replay_reader([Vote(**v) for v in fx["fresh_votes"]]),
        n_readers=3,
        item_text=item_text,
        rubric_text=rubric_text,
    )
    assert verdict.verdict == RUBRIC_REVIEW == fx["expected_verdict"]
    assert verdict.fresh_unanimous is False


# --- 3. escalate-with-evidence ------------------------------------------------

def test_escalation_evidence_pack_is_complete():
    fx = load_fixture("disagreement_persists.json")
    record, item_text, rubric_text = build_record(fx)
    verdict = triage_disagreement(
        record,
        replay_reader([Vote(**v) for v in fx["fresh_votes"]]),
        n_readers=3,
        item_text=item_text,
        rubric_text=rubric_text,
    )
    ev = verdict.evidence
    # The full evidence pack a rubric reviewer needs:
    assert verdict.rubric_sha256  # frozen instrument proof
    assert len(verdict.original_votes) == 2
    assert len(verdict.fresh_votes) == 3
    assert "split_pattern" in ev and ev["split_pattern"]["0"] and ev["split_pattern"]["1"]
    assert "reviewer_instructions" in ev and ev["reviewer_instructions"]
    assert ev["no_regrade_performed"] is True
    # Honesty guard: the pack must not claim the split's cause is known.
    joined = json.dumps(ev).lower()
    assert "reader variance" not in joined or "cannot explain" in joined


def test_na_fresh_vote_breaks_convergence_and_escalates():
    fx = load_fixture("disagreement_persists.json")
    record, item_text, rubric_text = build_record(fx)
    fresh = [Vote(reader_id="FRESH-001", vote=0), Vote(reader_id="FRESH-002", vote="na"),
             Vote(reader_id="FRESH-003", vote=0)]
    verdict = triage_disagreement(record, replay_reader(fresh), n_readers=3,
                                  item_text=item_text, rubric_text=rubric_text)
    assert verdict.verdict == RUBRIC_REVIEW
    assert verdict.fresh_unanimous is False


def test_append_ledger_writes_jsonl_receipt(tmp_path):
    from triage_disagreement import append_ledger
    fx = load_fixture("battery_d_TR-8DB748.json")
    record, item_text, rubric_text = build_record(fx)
    verdict = triage_disagreement(
        record,
        replay_reader([Vote(**v) for v in fx["fresh_votes"]]),
        n_readers=3,
        item_text=item_text,
        rubric_text=rubric_text,
    )
    ledger = str(tmp_path / "ledger.jsonl")
    append_ledger(ledger, verdict)
    append_ledger(ledger, verdict)
    lines = open(ledger).read().strip().split("\n")
    assert len(lines) == 2  # append-only, one line per verdict
    for line in lines:
        row = json.loads(line)
        assert row["verdict"] == READER_VARIANCE
        assert row["schema_version"] == "triage_disagreement/v1"
        assert row["n_readers"] == 3


def test_verdict_carries_confidence_note():
    fx = load_fixture("battery_d_TR-8DB748.json")
    record, item_text, rubric_text = build_record(fx)
    verdict = triage_disagreement(
        record,
        replay_reader([Vote(**v) for v in fx["fresh_votes"]]),
        n_readers=3,
        item_text=item_text,
        rubric_text=rubric_text,
    )
    assert verdict.n_readers == 3
    assert "confidence_note" in verdict.evidence
    assert "not proof" in verdict.evidence["confidence_note"]


def test_frozen_rubric_conflict_raises():
    register_frozen_rubric("r3", "rubric text v1")
    register_frozen_rubric("r3", "rubric text v1")  # idempotent: fine
    with pytest.raises(TriageError, match="already frozen with a different sha"):
        register_frozen_rubric("r3", "rubric text v2 -- silently sharpened")


def test_invalid_fresh_vote_is_refused_not_folded():
    fx = load_fixture("disagreement_persists.json")
    record, item_text, rubric_text = build_record(fx)
    with pytest.raises(TriageError, match="invalid vote"):
        triage_disagreement(record, replay_reader([Vote("c", 7), Vote("d", 0)]),
                            n_readers=2, item_text=item_text,
                            rubric_text=rubric_text)


# --- machine-enforced guards --------------------------------------------------

def test_refuses_non_disagreement():
    sha = register_frozen_rubric("r1", "rubric text")
    record = DisagreementRecord(
        item_id="X", cell="M1", rubric_id="r1", rubric_sha256=sha,
        votes=[Vote("a", 1), Vote("b", 1)],
    )
    with pytest.raises(TriageError, match="not a genuine disagreement"):
        triage_disagreement(record, replay_reader([Vote("c", 1), Vote("d", 1)]),
                            n_readers=2)


def test_refuses_unfrozen_rubric():
    record = DisagreementRecord(
        item_id="X", cell="M1", rubric_id="never-registered",
        rubric_sha256="deadbeef",
        votes=[Vote("a", 1), Vote("b", 0)],
    )
    with pytest.raises(TriageError, match="not registered as frozen"):
        triage_disagreement(record, replay_reader([Vote("c", 1), Vote("d", 1)]),
                            n_readers=2)


def test_refuses_sha_mismatch():
    register_frozen_rubric("r2", "rubric text v1")
    record = DisagreementRecord(
        item_id="X", cell="M1", rubric_id="r2", rubric_sha256="0" * 64,
        votes=[Vote("a", 1), Vote("b", 0)],
    )
    with pytest.raises(TriageError, match="sha mismatch"):
        triage_disagreement(record, replay_reader([Vote("c", 1), Vote("d", 1)]),
                            n_readers=2)


def test_reader_seam_carries_no_original_votes():
    """The ReadRequest dataclass structurally cannot carry the original
    votes -- information isolation is enforced by the type itself."""
    field_names = {f.name for f in dataclasses.fields(ReadRequest)}
    assert "original_votes" not in field_names
    assert "votes" not in field_names
    assert field_names == {"item_id", "cell", "item_text", "rubric_id",
                           "rubric_text", "blind_reader_id"}


def test_reader_fn_return_type_enforced():
    fx = load_fixture("disagreement_persists.json")
    record, item_text, rubric_text = build_record(fx)
    with pytest.raises(TriageError, match="must return a Vote"):
        triage_disagreement(record, lambda req: 1, n_readers=2)


def test_requires_at_least_two_fresh_readers():
    fx = load_fixture("disagreement_persists.json")
    record, item_text, rubric_text = build_record(fx)
    with pytest.raises(TriageError, match="at least 2 fresh readers"):
        triage_disagreement(record, replay_reader([Vote("c", 1)]), n_readers=1)


# --- E2E: the real Battery D borderline case ----------------------------------

def test_e2e_battery_d_borderline_case():
    """Full replay of the recorded TR-8DB748/M1 disagreement through the
    module exactly as the dry-run script does. Provenance: real Battery D
    scores + the rubric-sharpening probe (2026-10-12)."""
    import subprocess
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, "dryrun_battery_d.py"),
         "--ledger", ""],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0, f"dry-run failed:\n{r.stdout}\n{r.stderr}"
    verdict = json.loads(r.stdout.split("DRY-RUN OK:")[0])
    assert verdict["verdict"] == READER_VARIANCE
    assert verdict["item_id"] == "TR-8DB748"
    assert verdict["schema_version"] == "triage_disagreement/v1"
