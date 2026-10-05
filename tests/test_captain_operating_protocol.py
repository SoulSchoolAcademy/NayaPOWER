"""Captain Operating Protocol V1 — enforcement regression.

The law is only real if a cold successor cannot miss it and a future change
cannot quietly delete it. This pins the four enforcement surfaces:

  1. AGENTS.md            - the boot contract every seat reads FIRST
  2. .ai.md               - normative law
  3. .human.md            - the human-readable view
  4. .machine.json        - the machine twin

and pins that the three files AGREE on the parts where disagreement would
be a silent authority defect: the human gates, and CANDIDATE truth ceiling.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOV = ROOT / "BRAIN" / "01-GOVERNANCE"
AI = GOV / "0005-CAPTAIN-OPERATING-PROTOCOL-V1.ai.md"
HUMAN = GOV / "0005-CAPTAIN-OPERATING-PROTOCOL-V1.human.md"
MACHINE = GOV / "0005-captain-operating-protocol-v1.machine.json"
AGENTS = ROOT / "AGENTS.md"

# The canonical human gates. Merge is included deliberately: a seat that
# "self-directs" its way through a merge has crossed a boundary, not saved time.
HUMAN_GATES = {
    "production_dispatch",
    "production_db_read",
    "production_db_write",
    "production_migration",
    "credentials",
    "money",
    "destructive_action",
    "merge",
    "constitutional_ratification",
    "evolve_charter_ratification",
}

SCORING_DIMENSIONS = [
    "mission_value",
    "human_value",
    "urgency",
    "leverage",
    "evidence",
    "risk",
    "cost",
    "dependencies",
    "reversibility",
    "compounding_continuity",
]


def load_machine():
    return json.loads(MACHINE.read_text(encoding="utf-8"))


def test_law_binds_to_the_restored_intelligence_object_not_a_new_one():
    """The Director issued ONE directive. SN-0359 is its intelligence object.
    The law file must not claim a second, parallel law identity - that would be
    the duplicate-brain failure the constitution forbids."""
    m = load_machine()
    assert m["law_id"] == "PROACTIVE-CAPTAIN-V1"
    assert "SN-0359" in m["extends"]
    assert m["role"] == "NORMATIVE_LAW_AND_MACHINE_ENFORCEMENT"
    assert "does NOT claim a separate law identity" in m["not_a_new_intelligence_object"]


def test_restored_objects_are_present_and_record_their_deletion():
    """Two Director-ratified objects were deleted in a2f103f4f. Restoration is
    only meaningful if the objects are actually back AND the deletion stays on
    the record rather than being quietly erased."""
    for capture_id, deleted_in in (
        ("SN-0358", "a2f103f4f"),
        ("SN-0359", "a2f103f4f"),
    ):
        # Filenames use the bare sequence (sn0358), the object uses SN-0358.
        token = capture_id.replace("-", "").lower()
        p = next((ROOT / ".naya" / "capture").glob(f"*{token}*.json"), None)
        assert p is not None, f"{capture_id} capture missing — restoration lost"
        obj = json.loads(p.read_text(encoding="utf-8"))
        assert obj["smart_note_id"] == capture_id
        rp = obj["source"]["restoration_provenance"]
        assert rp["status"] == "RESTORED_AFTER_UNLICENSED_DELETION"
        assert deleted_in in rp["deleted_in"]
        assert rp["recovered_from"]
        assert obj["intelligence"]["epistemic_state"] == "CANDIDATE"
        assert obj["intelligence"]["uncertainty"]
        assert obj["intelligence"]["falsifier"]


def test_restored_sn0359_falsifier_catches_the_degenerate_case():
    """The original v1 falsifier was satisfiable by a seat that merely stopped
    asking while producing nothing. Clause (b) is what makes it real."""
    p = next((ROOT / ".naya" / "capture").glob("*sn0359*.json"), None)
    obj = json.loads(p.read_text(encoding="utf-8"))
    falsifier = obj["intelligence"]["falsifier"]
    assert "no measurable increase" in falsifier
    assert "the questions stop but the value does not arrive" in falsifier


def test_all_four_surfaces_exist():
    for p in (AI, HUMAN, MACHINE, AGENTS):
        assert p.exists(), f"missing enforcement surface: {p.relative_to(ROOT)}"


def test_machine_twin_is_valid_and_shaped():
    m = load_machine()
    assert m["schema"] == "naya.governance.captain-operating-protocol.v1"
    assert m["status"] == "DIRECTOR-RATIFIED"
    assert m["ratified_by"] == "Shawn Vibert"
    assert m["automatic_truth_ceiling"] == "CANDIDATE"
    assert m["cycle"]["terminal"] is False
    assert m["cycle"]["declare_before_act"] is True


def test_declare_precedes_act_in_the_machine_cycle():
    """The load-bearing ordering. If DECLARE ever moves after ACT the law
    is decorative, because a seat would be reporting a plan it already ran."""
    m = load_machine()
    phases = m["cycle"]["phases"]
    order = [p["name"] for p in phases]
    assert order.index("DECLARE") < order.index("ACT")
    assert order.index("OBSERVE") < order.index("RANK_TEN") < order.index("DECLARE")
    # And the cycle must terminate in REPEAT, never in a resting state.
    assert order[-1] == "REPEAT"
    declare = next(p for p in phases if p["name"] == "DECLARE")
    assert "MANDATORY" in declare["rule"]


def test_report_back_is_unprompted():
    m = load_machine()
    report = next(p for p in m["cycle"]["phases"] if p["name"] == "REPORT_BACK")
    assert "UNPROMPTED" in report["trigger"]
    assert "MANDATORY" in report["rule"]
    for required in ("what_changed", "why_this_choice", "exactly_one_next_action"):
        assert required in report["requires"]


def test_human_gates_are_identical_across_machine_and_law():
    """Disagreement here would be a silent authority defect: one surface
    could read as permission the other forbids."""
    m = load_machine()
    assert set(m["invariants"]["human_gates_never_crossed"]) == HUMAN_GATES
    ai = AI.read_text(encoding="utf-8")
    for gate in ("production", "credentials", "money", "destructive", "merge", "constitutional"):
        assert gate in ai, f"law prose omits gate family: {gate}"


def test_never_ask_is_explicit_and_bounded():
    """The law forbids a phrase AND enumerates the only exceptions. A purely
    negative rule would be unusable; a purely positive one would be toothless."""
    m = load_machine()
    assert "Do not ask the Director what to do next" in m["never_ask"]["rule"]
    assert len(m["never_ask"]["forbidden"]) >= 4
    assert len(m["never_ask"]["permitted_asks"]) >= 5
    assert "what_should_i_do_next" in m["never_ask"]["forbidden"]
    assert "human_authority_boundary" in m["never_ask"]["permitted_asks"]


def test_scoring_dimensions_are_locked_and_gates_filter_first():
    m = load_machine()
    rank = next(p for p in m["cycle"]["phases"] if p["name"] == "RANK_TEN")
    assert rank["scores"] == SCORING_DIMENSIONS
    assert "hard gates filter before scoring" in rank["rule"]


def test_no_score_overrides_a_hard_gate():
    m = load_machine()
    assert "never an authority loophole" in m["invariants"]["no_score_overrides_a_hard_gate"]
    ai = AI.read_text(encoding="utf-8")
    assert "No score overrides a hard gate" in ai or "never an authority loophole" in ai


def test_prime_judgment_is_elevated_not_relaxed():
    """Self-direction removes human checkpoints. The law must therefore raise
    the duty to check consequences, or it has quietly removed a safeguard."""
    m = load_machine()
    assert "RAISES the duty to check consequences" in m["invariants"]["prime_judgment_elevated"]


def test_motion_is_not_value_is_named_as_the_antipattern():
    m = load_machine()
    assert "motion_is_not_value" in m["invariants"]
    for forbidden in ("note_count", "action_count", "apparent_busy"):
        assert forbidden in m["measurement"]["never_measure_by"]


def test_falsifier_exists_and_forbids_defence():
    m = load_machine()
    assert len(m["measurement"]["falsified_if"]) >= 3
    ai = AI.read_text(encoding="utf-8")
    assert "requires amendment" in ai
    assert "not defense" in ai or "not defence" in ai


def test_reactive_drift_is_named_as_the_failure_mode():
    m = load_machine()
    assert "reactive_drift" in m["failure_recovery"]
    assert "DECLARE" in m["failure_recovery"]["reactive_drift"]


def test_binds_all_nine_nodes():
    m = load_machine()
    assert m["scope"] == "all_nine_nodes_all_seats_all_lanes"
    nodes = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]
    ai = AI.read_text(encoding="utf-8")
    for n in nodes:
        assert n in ai, f"law prose omits node: {n}"


def test_agents_md_boot_contract_carries_the_law():
    """AGENTS.md is the first thing a cold seat reads. If the law is not
    there it is, in practice, optional."""
    a = AGENTS.read_text(encoding="utf-8")
    assert "CAPTAIN OPERATING PROTOCOL" in a
    assert "0005-CAPTAIN-OPERATING-PROTOCOL-V1" in a
    assert "Declare before you act" in a or "DECLARE BEFORE YOU ACT" in a
    assert "Never ask what to do next" in a
    assert "Report back" in a or "REPORT BACK" in a


def test_agents_md_extends_rather_than_replaces_the_nonstop_loop():
    a = AGENTS.read_text(encoding="utf-8")
    assert "0004-NONSTOP-LOOP-V1" in a
    assert "not stopping" in a


def test_law_creates_no_new_subsystem():
    """A governance protocol, not a new brain. If a future change adds a store
    or a graph here, this test is where it should be caught."""
    m = load_machine()
    assert "create no new store, graph, scorecard or authority system" in m["invariants"]["no_duplicate_brains"]


def test_human_view_exists_and_keeps_the_human_gates():
    h = HUMAN.read_text(encoding="utf-8")
    assert len(h) > 500
    for gate in ("production", "credentials", "money", "destructive", "constitutional"):
        assert gate in h.lower(), f"human view omits gate family: {gate}"
    assert "amended" in h
