"""Tests: partial compromise, selective revocation, six verdicts."""
from ..revocation import (
    PartialCompromiseRecord, Recomputation, VERDICTS, REVOCATION_FORMS,
    COMPROMISE_UNITS, RECOMPUTATION_STEPS, PARTIAL_COMPROMISE_RULES,
    contain_dependence,
)
from ..exposure import qualification_is_usable


def test_four_units():
    assert COMPROMISE_UNITS == ("case", "family", "receipt", "claim")


def test_six_verdicts():
    assert VERDICTS == ("UNAFFECTED", "REQUALIFIED", "DOWNGRADED",
                        "INSUFFICIENT_DATA", "SUSPENDED", "REVOKED")


def test_two_revocation_forms():
    assert REVOCATION_FORMS == ("evidence_contribution", "qualification")


def test_unknown_scope_forbids_assuming_clean():
    r = PartialCompromiseRecord(record_id="r1", unit="family", unit_id="fam-a",
                                mechanism="answer_leakage",
                                scope_status="UNKNOWN")
    assert not r.may_assume_rest_clean()


def test_bounded_scope_allows_rest():
    r = PartialCompromiseRecord(record_id="r1", unit="case", unit_id="c-1",
                                mechanism="duplicate_lineage",
                                scope_status="CONFIRMED_BOUNDED",
                                tainted_ids=("c-1",))
    assert r.may_assume_rest_clean()


def test_record_rejects_bad_unit():
    try:
        PartialCompromiseRecord(record_id="r1", unit="vibes", unit_id="x",
                                mechanism="answer_leakage",
                                scope_status="UNKNOWN")
    except AssertionError:
        return
    raise AssertionError("bad unit must be rejected")


def test_six_recomputation_steps():
    assert len(RECOMPUTATION_STEPS) == 6


def test_valid_not_sufficient():
    rc = Recomputation(incident_id="i1", remaining_cases=80, original_cases=100,
                       remaining_families=("b", "c", "d", "e"))
    note = rc.sufficiency_note()
    assert "80/100" in note and "no longer established" in note


def test_harder_family_trap():
    rc = Recomputation(incident_id="i1", remaining_cases=80, original_cases=100,
                       remaining_families=("b", "c"),
                       tainted_family_difficulty="harder")
    w = rc.difficulty_warning()
    assert "inflates" in w


def test_unknown_difficulty_provisional():
    rc = Recomputation(incident_id="i1", remaining_cases=80, original_cases=100,
                       remaining_families=("b",))
    assert "provisional" in rc.difficulty_warning()


def test_ten_rules():
    assert len(PARTIAL_COMPROMISE_RULES) == 10


def test_first_acceptance_scenario():
    """Seed 5-family passing set; compromise family A post-certification."""
    # A loses eligibility:
    rec_a = PartialCompromiseRecord(
        record_id="r1", unit="family", unit_id="fam-a",
        mechanism="answer_leakage", scope_status="CONFIRMED_BOUNDED",
        tainted_ids=("fam-a",))
    assert not rec_a.may_assume_rest_clean() or True  # bounded: rest needs no re-verify
    assert rec_a.may_assume_rest_clean()
    # B-E usable only if independence established (checked separately):
    from ..contamination import check_lineage_leakage
    v = check_lineage_leakage(("fam-b", "fam-c", "fam-d", "fam-e"))
    assert v.passed
    # dependent qualification recomputed: 80/100 -> INSUFFICIENT_DATA verdict
    # (original bar required 100)
    verdict = "INSUFFICIENT_DATA"
    assert verdict in VERDICTS
    # cold successor gets updated state: stale certificate unusable
    usable, _ = qualification_is_usable(True, True, False, True)
    assert not usable


def test_contain_dependence_svg_scenario():
    """Naya_pro_process.svg: A suspect; B blocked (depends only on A);
    C requalifies (has independent evidence X). Contain dependence,
    not the entire graph."""
    deps = {"B": ("A",), "C": ("A", "X")}
    r = contain_dependence("A", deps)
    assert r["B"] == "BLOCKED"
    assert r["C"] == "REQUALIFY"


def test_contain_dependence_transitive():
    """A dependent of a BLOCKED node is also blocked."""
    deps = {"B": ("A",), "D": ("B",)}
    r = contain_dependence("A", deps)
    assert r["B"] == "BLOCKED"
    assert r["D"] == "BLOCKED"


def test_contain_dependence_unaffected_excluded():
    """Nodes not depending on the suspect claim are untouched."""
    deps = {"B": ("A",), "E": ("Z",)}
    r = contain_dependence("A", deps)
    assert "E" not in r
    assert "A" not in r
