"""Tests for the anti-citogenesis claim-evidence gate.

The gate adjudicates verification attestations ("independently verified",
"proven", ...) in prose against structured evidence. Law: internal repetition
is not independent corroboration. Fail-closed: an attestation with no
admissible independent evidence fails.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from check_claim_evidence import Evidence, adjudicate, find_attestations  # noqa: E402


def exists(p):
    return p in {"tests/test_truth_state_poison.py", "tests/test_act_pipeline_two_phase.py"}


def run(text, author="Naya 5", evidence=None):
    return adjudicate(text, author, evidence or [], path_exists=exists)


# --- attestation discovery -------------------------------------------------

def test_finds_independently_verified():
    atts = find_attestations("The fix is independently verified by Naya 4.")
    assert len(atts) == 1
    assert "independently verified" in atts[0].text.lower()


def test_finds_proven():
    atts = find_attestations("Bug proven fixed on the exact head.")
    assert len(atts) == 1


def test_finds_verified_by():
    atts = find_attestations("Receipt verified by the merge queue lane.")
    assert len(atts) == 1


def test_ignores_code_identifiers():
    atts = find_attestations("outcome_verified=False  # UNKNOWN stays unknown")
    assert atts == [], f"code identifier must not count as an attestation: {atts}"


def test_plain_text_has_no_attestations():
    assert find_attestations("Shipped the re-stamp. Three files, no gate code.") == []


# --- happy paths ------------------------------------------------------------

def test_independent_seat_review_admits():
    r = run(
        "Independently verified by Naya 4 (review 5481542587).",
        author="Naya 5",
        evidence=[Evidence(kind="seat_review", seat="Naya 4", ref="review-5481542587")],
    )
    assert r["pass"] is True


def test_executable_evidence_admits():
    r = run(
        "Proven fixed: the falsifier test now passes.",
        author="Naya 5",
        evidence=[Evidence(kind="test", ref="tests/test_truth_state_poison.py")],
    )
    assert r["pass"] is True


def test_ci_run_admits():
    r = run(
        "Independently verified -- CI run 38089885628 green on the exact head.",
        author="Naya 5",
        evidence=[Evidence(kind="ci_run", ref="38089885628")],
    )
    assert r["pass"] is True


def test_no_attestation_passes_vacuously():
    r = run("Re-stamped the brain index. 3 files, official generator.")
    assert r["pass"] is True
    assert r["verdicts"] == []


# --- citogenesis traps (must FAIL) ------------------------------------------

def test_same_seat_note_is_self_attestation():
    """Author cites their own note as 'independent verification'."""
    r = run(
        "Independently verified -- see my verification note.",
        author="Naya 5",
        evidence=[Evidence(kind="note", seat="Naya 5", ref="IB-SMART-NOTE-...")],
    )
    assert r["pass"] is False
    assert any("self-attestation" in reason for v in r["verdicts"] for reason in v.reasons)


def test_repetition_chain_is_not_corroboration():
    """Naya 4's note merely repeats the author's claim -- telephone game."""
    r = run(
        "Independently verified by Naya 4.",
        author="Naya 5",
        evidence=[Evidence(kind="note", seat="Naya 4", ref="note-xyz", repeats=True)],
    )
    assert r["pass"] is False
    assert any("repetition is not corroboration" in reason for v in r["verdicts"] for reason in v.reasons)


def test_same_seat_review_is_not_independent():
    r = run(
        "Independently verified.",
        author="Naya 5",
        evidence=[Evidence(kind="seat_review", seat="Naya 5", ref="comment-123")],
    )
    assert r["pass"] is False


def test_different_seat_note_alone_is_supporting_only():
    """A note documents; it is not a verification act."""
    r = run(
        "Independently verified -- Naya 4's note confirms.",
        author="Naya 5",
        evidence=[Evidence(kind="note", seat="Naya 4", ref="note-abc")],
    )
    assert r["pass"] is False
    assert any("supporting only" in reason for v in r["verdicts"] for reason in v.reasons)


def test_nonexistent_test_is_not_evidence():
    r = run(
        "Proven by tests.",
        author="Naya 5",
        evidence=[Evidence(kind="test", ref="tests/test_does_not_exist_xyz.py")],
    )
    assert r["pass"] is False


def test_commit_alone_does_not_verify():
    """The change existing proves existence, never verification."""
    r = run(
        "Independently verified.",
        author="Naya 5",
        evidence=[Evidence(kind="commit", ref="a" * 40)],
    )
    assert r["pass"] is False


def test_unattested_claim_fails_closed():
    """Fail-closed: the words with zero evidence behind them."""
    r = run("The defect is independently verified.", author="Naya 5", evidence=[])
    assert r["pass"] is False
    assert len(r["verdicts"]) == 1
    assert r["verdicts"][0].admissible is False


def test_pooled_evidence_covers_attestations():
    # Pooled model (documented): one admissible item supports every
    # attestation in the text. Per-attestation linkage is future work.
    r = run(
        "Proven by tests/test_truth_state_poison.py. Also independently verified.",
        author="Naya 5",
        evidence=[Evidence(kind="test", ref="tests/test_truth_state_poison.py")],
    )
    assert r["pass"] is True
    assert len(r["verdicts"]) == 2
    assert all(v.admissible for v in r["verdicts"])


def test_one_bad_pool_fails_all_attestations():
    # The only "evidence" is the author's own note: every attestation fails.
    r = run(
        "Proven fixed. Independently verified -- see my note.",
        author="Naya 5",
        evidence=[Evidence(kind="note", seat="Naya 5", ref="note-1")],
    )
    assert r["pass"] is False
    assert len(r["verdicts"]) == 2
    assert not any(v.admissible for v in r["verdicts"])


def test_unattributable_review_fails():
    r = run(
        "Independently verified.",
        author="Naya 5",
        evidence=[Evidence(kind="seat_review", ref="comment-999")],
    )
    assert r["pass"] is False


def test_unknown_evidence_kind_fails():
    r = run(
        "Independently verified.",
        author="Naya 5",
        evidence=[Evidence(kind="vibes", ref="felt-right")],
    )
    assert r["pass"] is False
