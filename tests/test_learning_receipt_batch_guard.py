"""Behavioral tests for the batch-generation guard (convergence item D hardening).

The #2524 defect (2026-10-13): 750 ledger rows stamped VERIFIED, all emitted
inside a 78-millisecond window, zero rows pointing to an existing receipt
file, agent names outside the named-seat roster. The D validators PASS such
receipts -- they verify internal consistency, not external grounding. These
tests exercise the distributional counterweight: the guard must flag the
#2524 pattern, stay silent on human-paced work, and never reject (legitimate
backfills trip the same signals; legitimacy is a caller judgment).

Boundary-pinning: test_batch_receipts_still_pass_d_validators documents the
known boundary -- validators != provenance detectors. If that test ever
starts FAILING because the validators changed, the boundary moved and the
guard's design contract must be re-examined.
"""

from datetime import datetime, timedelta, timezone

import pytest

from tools.learning_application_receipt import (
    emit_application_receipt,
    emit_outcome_record,
    emit_retrieval_receipt,
    qualifies_for_e2,
    qualifies_for_e3,
    validate_application_receipt,
    validate_outcome_record,
    validate_retrieval_receipt,
)
from tools.learning_receipt_batch_guard import assess_batch, summarize_assessment

T0 = datetime(2026, 10, 13, 14, 4, 57, 413934, tzinfo=timezone.utc)


def _mint_batch(n, window_ms=78, applier="Naya Verity", verifier="Naya Sage"):
    """Mint n internally-consistent application-receipt chains.

    window_ms: emission window for the whole set (the #2524 pattern uses 78).
    The receipts are fully valid by D's validators -- schema, id integrity,
    retrieval_ref binding, verifier != applier all hold.
    """
    receipts = []
    for i in range(n):
        ts = (T0 + timedelta(microseconds=int(window_ms * 1000 * i / max(n - 1, 1)))).isoformat()
        lesson_id = "LESSON-%04d" % i
        rr = emit_retrieval_receipt(
            lesson_id=lesson_id, retriever=applier, retrieved_at=ts,
            query_context="batch guard test", lesson_content_sha="ab" * 32,
            source_refs=["receipts/%04d.md" % i],
        )
        ar = emit_application_receipt(
            lesson_id=lesson_id, retrieval_ref=rr["receipt_id"],
            task_ref="task-%d" % i, applier=applier, applied_at=ts,
            applicability={"relevance_rationale": "r%d" % i, "task_match": "m%d" % i},
        )
        oc = emit_outcome_record(
            application_receipt_id=ar["receipt_id"], lesson_id=lesson_id,
            task_ref="task-%d" % i, measured_effect="effect %d" % i,
            observed_at=ts, outcome_ref="receipts/%04d.md" % i,
            independent_verification={"verifier": verifier, "verified_at": ts},
        )
        receipts.append((rr, ar, oc))
    return receipts


# ---------------------------------------------------------------------------
# The guard flags the #2524 pattern
# ---------------------------------------------------------------------------

def test_2524_pattern_is_suspect():
    chains = _mint_batch(25, window_ms=78)
    apps = [ar for _, ar, _ in chains]
    result = assess_batch(apps, ts_field="applied_at")
    assert result["verdict"] == "BATCH_SUSPECT"
    assert any(s.startswith("BATCH_WINDOW_NARROW") for s in result["signals"])
    assert result["ms_per_receipt"] < 1000.0
    assert result["parseable"] == 25
    assert result["unparseable"] == 0


def test_identical_timestamps_collide():
    chains = _mint_batch(10, window_ms=0)
    apps = [ar for _, ar, _ in chains]
    result = assess_batch(apps, ts_field="applied_at")
    assert result["verdict"] == "BATCH_SUSPECT"
    assert any(s.startswith("TIMESTAMP_COLLISIONS") for s in result["signals"])
    assert result["distinct_ts"] == 1


def test_roster_unknown_names_flagged():
    chains = _mint_batch(25, window_ms=78, applier="Naya Verity")
    apps = [ar for _, ar, _ in chains]
    roster = {"Naya Alpha", "Naya Beta", "Naya Gamma", "Naya Delta"}
    result = assess_batch(apps, ts_field="applied_at", known_seats=roster)
    assert result["verdict"] == "BATCH_SUSPECT"
    assert "Naya Verity" in result["roster_unknown"]
    assert any(s.startswith("ROSTER_UNKNOWN_NAMES") for s in result["signals"])


def test_roster_known_names_clean_on_distribution():
    chains = _mint_batch(25, window_ms=78, applier="Naya Alpha")
    apps = [ar for _, ar, _ in chains]
    roster = {"Naya Alpha", "Naya Beta"}
    result = assess_batch(apps, ts_field="applied_at", known_seats=roster)
    # Still batch-suspect (the window is real), but no roster signal.
    assert result["verdict"] == "BATCH_SUSPECT"
    assert result["roster_unknown"] == []
    assert not any(s.startswith("ROSTER_UNKNOWN_NAMES") for s in result["signals"])


def test_outcome_verifier_name_path():
    chains = _mint_batch(10, window_ms=78, verifier="Naya Invented")
    outcomes = [oc for _, _, oc in chains]
    result = assess_batch(
        outcomes, ts_field="observed_at",
        known_seats={"Naya Alpha"},
        name_fields=("independent_verification.verifier",),
    )
    assert "Naya Invented" in result["roster_unknown"]


# ---------------------------------------------------------------------------
# The guard stays silent on human-paced work
# ---------------------------------------------------------------------------

def test_human_paced_set_is_clean():
    chains = _mint_batch(25, window_ms=25 * 5 * 60 * 1000)  # 5 min spacing
    apps = [ar for _, ar, _ in chains]
    result = assess_batch(apps, ts_field="applied_at")
    assert result["verdict"] == "CLEAN"
    assert result["signals"] == []
    assert result["ms_per_receipt"] >= 300_000.0  # 5 min per receipt


def test_small_set_is_inconclusive_not_suspect():
    chains = _mint_batch(3, window_ms=78)
    apps = [ar for _, ar, _ in chains]
    result = assess_batch(apps, ts_field="applied_at")
    assert result["verdict"] == "INCONCLUSIVE"
    assert any(s.startswith("INSUFFICIENT_DATA") for s in result["signals"])


def test_unparseable_timestamps_tolerated():
    chains = _mint_batch(10, window_ms=10 * 60 * 1000)  # 1 min spacing, clean
    apps = [ar for _, ar, _ in chains]
    apps = apps + [{"applied_at": "not-a-timestamp"}, {"applied_at": None}, "junk"]
    result = assess_batch(apps, ts_field="applied_at")
    assert result["unparseable"] == 3
    assert result["parseable"] == 10
    assert result["verdict"] == "CLEAN"


# ---------------------------------------------------------------------------
# The guard annotates, never rejects (backfill honesty)
# ---------------------------------------------------------------------------

def test_backfill_is_flagged_not_rejected():
    # A legitimate backfill is bulk-emitted: the guard MUST flag the
    # distribution, and the underlying D validators MUST still report the
    # receipts valid. Legitimacy is a caller judgment, not a guard verdict.
    chains = _mint_batch(40, window_ms=4000, applier="Naya Beta")
    apps = [ar for _, ar, _ in chains]
    guard = assess_batch(apps, ts_field="applied_at")
    assert guard["verdict"] == "BATCH_SUSPECT"  # 100 ms/receipt < 1 s floor
    for (_, ar, _), (rr, _, oc) in zip(chains, chains):
        assert validate_application_receipt(ar, rr)["valid"]
        assert validate_outcome_record(oc, applier=ar["applier"])["valid"]
    # The guard's verdict is an annotation for the caller, not a rejection
    # of the receipts themselves.


# ---------------------------------------------------------------------------
# The known boundary, pinned (validators != provenance detectors)
# ---------------------------------------------------------------------------

def test_batch_receipts_still_pass_d_validators():
    """PINNED BOUNDARY. Batch-pattern receipts PASS every D validator.

    If this test ever fails because the validators changed, the design
    contract moved: re-examine whether the guard's annotation-only posture
    is still the right one, and update this test's rationale, never its
    assertion by weakening.
    """
    chains = _mint_batch(25, window_ms=78, applier="Naya Verity",
                         verifier="Naya Sage")
    for rr, ar, oc in chains:
        assert validate_retrieval_receipt(rr)["valid"]
        assert validate_application_receipt(ar, rr)["valid"]
        assert validate_outcome_record(oc, applier=ar["applier"])["valid"]
        assert qualifies_for_e2(ar)
        assert qualifies_for_e3(ar, oc)


# ---------------------------------------------------------------------------
# The documented limitation, pinned (P-011)
# ---------------------------------------------------------------------------

def test_embedded_cluster_not_detected():
    """PINNED LIMITATION. A batch cluster inside a wide set is invisible to
    the whole-set window. If cluster detection is ever added, this test
    must be replaced by a cluster-detection test, not deleted."""
    human = _mint_batch(10, window_ms=10 * 60 * 60 * 1000)  # 1 hr spacing
    batch = _mint_batch(10, window_ms=78)
    apps = [ar for _, ar, _ in human] + [ar for _, ar, _ in batch]
    result = assess_batch(apps, ts_field="applied_at")
    assert result["verdict"] == "CLEAN"


def test_summarize_assessment_one_line():
    chains = _mint_batch(25, window_ms=78)
    apps = [ar for _, ar, _ in chains]
    result = assess_batch(apps, ts_field="applied_at")
    line = summarize_assessment(result)
    assert "BATCH_SUSPECT" in line
    assert "signals=1" in line  # window narrow only; 25 distinct microsecond ts
