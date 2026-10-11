#!/usr/bin/env python3
"""Tests for the D27 assumption-guarantee boundary — Naya 2 BUILD LANE.

Directive D27 (wave 6, owner naya2): every fairness guarantee names the
registered assumptions it rests on; every assumption is REGISTERED (id,
statement, relying components); the prover resolves every assumption through
the registry and FAILS CLOSED on a phantom (unregistered) assumption — no
verdict is ever emitted resting on one.

Every test uses REAL asserts against the REAL registry, boundary table, and
EligibilityProver. Negative controls sabotage the registry / boundary /
prover input and assert the suite then FAILS. If sabotage does not break the
test, the test is vacuous and must be rewritten, never weakened.
"""

import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import fairness_assumptions as fa
from fairness_assumptions import (
    Assumption,
    UnknownAssumptionError,
    BoundaryError,
    resolve,
    check_boundary,
    register_assumption,
    ASSUMPTIONS,
    BOUNDARY,
    FA_A1,
    FA_A2,
    FA_A3,
    FA_A4,
)
from fairness_eligibility import EligibilityProver, WorkItem
import merge_queue_fairness as mqf
from merge_queue_fairness import scan_queue, verdict_to_dict, merge_queue_registry

FIXED_NOW = datetime(2026, 10, 11, 5, 30, tzinfo=timezone.utc)


def _iso(dt):
    return dt.isoformat()


def _hours_ago(h):
    return _iso(FIXED_NOW - timedelta(hours=h))


# ---------------------------------------------------------------------------
# Registry shape
# ---------------------------------------------------------------------------

def test_registry_holds_exactly_the_four_operating_assumptions():
    assert set(ASSUMPTIONS.keys()) == {"FA-A1", "FA-A2", "FA-A3", "FA-A4"}


def test_every_assumption_resolves_to_a_nonempty_statement():
    for aid in ("FA-A1", "FA-A2", "FA-A3", "FA-A4"):
        asm = resolve(aid)
        assert isinstance(asm, Assumption)
        assert asm.id == aid
        assert asm.statement and len(asm.statement) > 20


def test_legacy_free_text_spellings_still_resolve():
    # Old snapshots / old code spelled these as free text. The boundary must
    # not silently break them -- they resolve to the canonical registration.
    assert resolve(
        "author seat undeclared; branch prefix fallback used").id == FA_A1
    assert resolve(
        "author seat not declared (no 'Seat: Naya N' in PR body and "
        "no nayaN/ branch prefix); cross-seat predicates accept any "
        "named reviewer seat").id == FA_A1


def test_boundary_table_is_closed():
    # Every guarantee names only registered assumptions; every assumption is
    # relied upon by at least one component and one guarantee. A dangling
    # reference anywhere is a broken boundary.
    report = check_boundary()
    assert report["closed"] is True
    assert report["guarantees"] == len(BOUNDARY)
    assert report["assumptions"] == len(ASSUMPTIONS)


# ---------------------------------------------------------------------------
# Negative controls -- sabotage must break the suite
# ---------------------------------------------------------------------------

def test_nc1_phantom_assumption_is_rejected_never_silently_named():
    # THE core D27 property: a verdict must never rest on an unregistered
    # assumption. The prover raises BEFORE constructing any verdict.
    reg = merge_queue_registry()
    prover = EligibilityProver(reg)
    work = WorkItem(item_id="PR-1", requirements=["merge_intent_recorded"])
    with pytest.raises(UnknownAssumptionError):
        prover.prove(work, {"intent_recorded": True}, "w1",
                     assumptions=["the moon is made of cheese"])


def test_nc2_duplicate_registration_is_rejected():
    dup = Assumption(id=FA_A1, statement="a second FA-A1",
                     relied_upon_by=("x",))
    with pytest.raises(BoundaryError):
        register_assumption(dup)
    # The canonical registration is untouched by the rejected duplicate.
    assert "second FA-A1" not in resolve(FA_A1).statement


def test_nc3_unknown_id_is_rejected():
    with pytest.raises(UnknownAssumptionError):
        resolve("FA-A99")


def test_nc4_empty_and_none_refs_are_rejected():
    with pytest.raises(UnknownAssumptionError):
        resolve("")
    with pytest.raises(UnknownAssumptionError):
        resolve(None)


def test_nc5_tampered_boundary_table_fails_the_closure_check():
    # Sabotage the boundary (not the registry): a guarantee resting on a
    # phantom assumption id must fail closure. Proves the import-time
    # self-check is not theater.
    tampered = dict(BOUNDARY)
    tampered["FG-GX"] = {"statement": "sabotaged guarantee",
                         "rests_on": ("FA-A99",)}
    with pytest.raises(BoundaryError):
        fa._check_tables_closed(ASSUMPTIONS, tampered)


def test_nc6_orphan_assumption_fails_the_closure_check():
    # An assumption no guarantee and no component relies on is dead weight --
    # the boundary refuses it.
    orphaned = dict(ASSUMPTIONS)
    orphaned["FA-A9"] = Assumption(id="FA-A9", statement="orphan",
                                   relied_upon_by=())
    with pytest.raises(BoundaryError):
        fa._check_tables_closed(orphaned, BOUNDARY)


def test_nc7_sabotaged_resolve_bypass_must_not_emit_verdict():
    # Even if a caller tries to smuggle a phantom past resolve by pre-seeding
    # the verdict, the prover is the choke point: prove() itself resolves.
    reg = merge_queue_registry()
    prover = EligibilityProver(reg)
    work = WorkItem(item_id="PR-1", requirements=["merge_intent_recorded"])
    with pytest.raises(UnknownAssumptionError):
        prover.prove(work, {"intent_recorded": True}, "w1",
                     assumptions=[FA_A1, "phantom-assumption"])


def test_nc8_tampered_module_copy_fails_at_import(tmp_path):
    # Copy the real module, tamper its BOUNDARY, import the copy: the
    # import-time self-check must kill the import. Proves the enforcement
    # point is the import itself, not just the check function.
    src = os.path.join(os.path.dirname(fa.__file__), "fairness_assumptions.py")
    dst = os.path.join(str(tmp_path), "fairness_assumptions_tampered.py")
    text = open(src).read()
    tampered = text.replace(
        '"FG-G1": {',
        '"FG-GX": {"statement": "sabotaged", "rests_on": ("FA-A99",)},\n'
        '    "FG-G1": {',
        1,
    )
    assert tampered != text, "sabotage did not apply -- test is vacuous"
    open(dst, "w").write(tampered)
    code = ("import sys; sys.path.insert(0, %r); "
            "import fairness_assumptions_tampered" % str(tmp_path))
    r = subprocess.run([sys.executable, "-c", code],
                       capture_output=True, text=True)
    assert r.returncode != 0, "tampered module imported cleanly -- no enforcement"
    assert "BoundaryError" in r.stderr


# ---------------------------------------------------------------------------
# End-to-end: the gate's real paths now carry registered ids
# ---------------------------------------------------------------------------

def _evidence(**kw):
    head = "abc123def456abc123def456abc123def456abcd"
    ev = {
        "pr_number": 9001,
        "head_sha": head,
        "author_seat": "Naya 2",
        "scorecard": {"seat": "Naya 4", "head_matches": True,
                      "verdict": 9.2, "merge_approved": True,
                      "at": _hours_ago(24 * 10)},
        "review": {"seat": "Naya 4", "head_matches": True,
                   "at": _hours_ago(24 * 10 - 1)},
        "check_runs": [
            {"name": "test", "status": "completed", "conclusion": "success",
             "completed_at": _hours_ago(24 * 10)},
        ],
        "checks_evidence_present": True,
        "intent_recorded": True,
    }
    ev.update(kw)
    return ev


def _item(pr=9001, **kw):
    d = {"pr_number": pr, "head_sha": "abc123", "author_seat": "Naya 2",
         "intent_recorded": True, "blocked_by": [], "parked": None,
         "evidence": _evidence()}
    d.update(kw)
    return d


def test_scan_blocked_pr_carries_FA_A2():
    v = scan_queue({"queue": [_item(blocked_by=[9004])]}, now=FIXED_NOW)[0]
    assert v.eligible is True and v.debt == 0 and v.violated is False
    assert FA_A2 in v.assumption_ids
    assert any("blocked" in s for s in v.assumptions)


def test_scan_parked_pr_carries_FA_A3():
    v = scan_queue(
        {"queue": [_item(parked={"reason": "awaiting Shawn's word"})]},
        now=FIXED_NOW)[0]
    assert v.eligible is True and v.debt == 0 and v.violated is False
    assert FA_A3 in v.assumption_ids


def test_scan_unprovable_ready_since_carries_FA_A4():
    ev = _evidence()
    ev["scorecard"] = dict(ev["scorecard"], at=None)
    v = scan_queue({"queue": [_item(evidence=ev)]}, now=FIXED_NOW)[0]
    assert v.eligible is True and v.ready_since is None
    assert FA_A4 in v.assumption_ids
    assert v.verdict_level == "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS"


def test_scan_undeclared_author_carries_FA_A1():
    item = _item()
    item["author_seat"] = None
    item["evidence"] = _evidence(author_seat=None)
    v = scan_queue({"queue": [item]}, now=FIXED_NOW)[0]
    assert FA_A1 in v.assumption_ids


def test_verdict_output_shape_is_backward_compatible():
    v = scan_queue({"queue": [_item(blocked_by=[9004])]}, now=FIXED_NOW)[0]
    d = verdict_to_dict(v)
    # "assumptions" stays a list of human-readable strings (existing
    # consumers unchanged); "assumption_ids" is the new machine-checked ref.
    assert isinstance(d["assumptions"], list)
    assert all(isinstance(s, str) for s in d["assumptions"])
    assert d["assumption_ids"] == v.assumption_ids
    assert set(d["assumption_ids"]) <= set(ASSUMPTIONS.keys())


def test_prover_with_no_assumptions_is_unchanged():
    reg = merge_queue_registry()
    prover = EligibilityProver(reg)
    work = WorkItem(item_id="PR-1", requirements=["merge_intent_recorded"])
    v = prover.prove(work, {"intent_recorded": True}, "w1")
    assert v.verdict_level == "MODEL_CHECK_PASSED_IN_SCOPE"
    assert v.assumptions == [] and v.assumption_ids == []


def test_prover_with_registered_id_caps_level_and_names_statement():
    reg = merge_queue_registry()
    prover = EligibilityProver(reg)
    work = WorkItem(item_id="PR-1", requirements=["merge_intent_recorded"])
    v = prover.prove(work, {"intent_recorded": True}, "w1",
                     assumptions=[FA_A2])
    assert v.verdict_level == "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS"
    assert v.assumption_ids == [FA_A2]
    assert v.assumptions == [resolve(FA_A2).statement]
