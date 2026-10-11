"""Tests for tools/d65_joint_proof_gate.py.

These tests judge the gate against the REAL D65 engine
(drift_canary/strongly_connected_groups.py) — the wire branch is
stacked on the mechanism PR (#2327), so the real bytes are on the tree.
No fakes: a fake engine could diverge from the mechanism and the tests
would lie. On a tree without the mechanism the module skips with an
explicit reason (UNKNOWN, never PASS).
"""

import importlib.util
import json
from pathlib import Path

import pytest

MECH = pytest.importorskip(
    "drift_canary.strongly_connected_groups",
    reason="D65 mechanism absent on this tree — gate tests need the real "
           "engine (wire branch stacked on PR #2327)")

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
GATE_PATH = TOOLS_DIR / "d65_joint_proof_gate.py"
MANIFEST_PATH = TOOLS_DIR / "d65_joint_proof_manifest.json"


def _load_gate():
    spec = importlib.util.spec_from_file_location(
        "d65_joint_proof_gate", GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def gate():
    return _load_gate()


# ---------------------------------------------------------------------------
# Fixtures — the mechanism's own canonical 4-member cycle (same shape as
# drift_canary/tests/test_strongly_connected_groups.py).
# ---------------------------------------------------------------------------

BUDGET, RESOURCE, REPLENISH, LIFECYCLE = (
    "budget", "resource", "replenishment", "lifecycle")
MEMBERS = (BUDGET, RESOURCE, REPLENISH, LIFECYCLE)
CYCLE_PREREQ = {
    BUDGET: (LIFECYCLE,),
    RESOURCE: (BUDGET,),
    REPLENISH: (RESOURCE,),
    LIFECYCLE: (REPLENISH,),
}
S0, S1, S2, S3, S4 = (
    "s0_allocated", "s1_drawn", "s2_replenished", "s3_released", "s4_exited")


def _transitions(progress=1, with_exit=True, auth="treasury:auth-001"):
    ts = [
        MECH.JointTransition(S0, S1, MECH.KIND_ORDINARY, progress),
        MECH.JointTransition(S1, S2, MECH.KIND_REPLENISH, progress,
                             authorization=auth),
        MECH.JointTransition(S2, S3, MECH.KIND_ORDINARY, progress),
        MECH.JointTransition(S3, S0, MECH.KIND_ORDINARY, progress),
    ]
    if with_exit:
        ts.append(MECH.JointTransition(S3, S4, MECH.KIND_COMPLETE, progress))
    return ts


def _declaration(**over):
    kw = dict(
        name="AER-LIVE-010-SCC",
        members=MEMBERS,
        declared_by="treasury",
        prereq=CYCLE_PREREQ,
        initial_states={S0},
        authorized_initial={S0},
        transitions=_transitions(),
        exit_states={S4},
    )
    kw.update(over)
    return MECH.make_declaration(**kw)


def _model_dict(decl):
    return {
        "name": decl.name,
        "members": sorted(decl.members),
        "declared_by": decl.declared_by,
        "prereq": {k: sorted(v) for k, v in decl.prereq.items()},
        "initial_states": sorted(decl.initial_states),
        "authorized_initial": sorted(decl.authorized_initial),
        "transitions": [
            {"src": t.src, "dst": t.dst, "kind": t.kind,
             "progress": t.progress, "authorization": t.authorization,
             "capacity": t.capacity, "owner": t.owner}
            for t in decl.transitions
        ],
        "relation_digest": decl.relation_digest,
        "exit_states": sorted(decl.exit_states),
    }


def _claim(asserts, model, cid="D65-TEST-1",
           obligation_id="aer-live-010-test"):
    return {"id": cid, "obligation_id": obligation_id,
            "asserts": asserts, "model": model}


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": claims}), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# DORMANT — the honest empty state.
# ---------------------------------------------------------------------------

def test_absent_manifest_dormant(gate, tmp_path):
    assert gate.main(["--manifest", str(tmp_path / "nope.json")]) == 0


def test_empty_claims_dormant(gate, tmp_path):
    assert gate.main(["--manifest",
                      str(_write_manifest(tmp_path, []))]) == 0


def test_shipped_manifest_is_dormant(gate):
    # The manifest that ships with the wire registers zero claims.
    assert gate.main(["--manifest", str(MANIFEST_PATH)]) == 0


# ---------------------------------------------------------------------------
# PASS — honest claims certified by the cold engine.
# ---------------------------------------------------------------------------

def test_honest_positive_claim_passes(gate, tmp_path):
    decl = _declaration()
    assert MECH.verify_joint(decl).verdict == MECH.Verdict.EXIT_POSSIBLE_NOT_GUARANTEED
    p = _write_manifest(tmp_path, [
        _claim("EXIT_POSSIBLE_NOT_GUARANTEED", _model_dict(decl))])
    assert gate.main(["--manifest", str(p)]) == 0


def test_closed_cycle_repeatable_claim_passes(gate, tmp_path):
    decl = _declaration(transitions=_transitions(with_exit=False),
                        exit_states=frozenset())
    assert MECH.verify_joint(decl).verdict == MECH.Verdict.REPEATABLE_PROVEN
    p = _write_manifest(tmp_path, [
        _claim("REPEATABLE_PROVEN", _model_dict(decl))])
    assert gate.main(["--manifest", str(p)]) == 0


def test_honest_refusal_record_passes(gate, tmp_path):
    # An ungrounded joint asserted as JOINT_UNDETERMINED is an honest
    # refusal record — the gate certifies the honesty, not the joint.
    decl = _declaration(authorized_initial=frozenset())
    assert MECH.verify_joint(decl).verdict == MECH.Verdict.JOINT_UNDETERMINED
    p = _write_manifest(tmp_path, [
        _claim("JOINT_UNDETERMINED", _model_dict(decl))])
    assert gate.main(["--manifest", str(p)]) == 0


# ---------------------------------------------------------------------------
# VIOLATION — the law refuses the claim. This is the wiring proof: try to
# violate the mechanism through the gate and the gate blocks it.
# ---------------------------------------------------------------------------

def test_worked_example_blocks_when_registered(gate, tmp_path):
    # The manifest's own worked example: a zero-progress closed cycle
    # asserted REPEATABLE_PROVEN — the naive checker's exact fraud.
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    example = {k: v for k, v in manifest["_example"].items()
               if not k.startswith("_")}
    p = _write_manifest(tmp_path, [example])
    assert gate.main(["--manifest", str(p)]) == 1


def test_livelock_asserted_repeatable_blocked(gate, tmp_path):
    decl = _declaration(transitions=_transitions(progress=0, with_exit=False),
                        exit_states=frozenset())
    assert MECH.verify_joint(decl).verdict == \
        MECH.Verdict.LIVELOCK_COUNTEREXAMPLE
    p = _write_manifest(tmp_path, [
        _claim("REPEATABLE_PROVEN", _model_dict(decl))])
    assert gate.main(["--manifest", str(p)]) == 1


def test_self_certified_authority_blocked(gate, tmp_path):
    decl = _declaration(declared_by=BUDGET)
    v = MECH.verify_joint(decl)
    assert v.verdict == MECH.Verdict.JOINT_UNDETERMINED
    assert any("own external facts" in o for o in v.obstruction)
    p = _write_manifest(tmp_path, [
        _claim("REPEATABLE_PROVEN", _model_dict(decl))])
    assert gate.main(["--manifest", str(p)]) == 1


def test_digest_tamper_blocked(gate, tmp_path):
    honest = _declaration()
    tampered = MECH.JointDeclaration(
        **{**honest.__dict__,
           "transitions": honest.transitions + (
               MECH.JointTransition(S0, S4, MECH.KIND_COMPLETE, 9),)})
    # Digest still the honest one: the model drifted under the
    # authorization. The gate must refuse without pre-checking the digest
    # itself — the engine's verdict is the authority.
    assert MECH.verify_joint(tampered).verdict == \
        MECH.Verdict.JOINT_UNDETERMINED
    p = _write_manifest(tmp_path, [
        _claim("REPEATABLE_PROVEN", _model_dict(tampered))])
    assert gate.main(["--manifest", str(p)]) == 1


def test_deadlock_misjudged_as_repeatable_blocked(gate, tmp_path):
    ts = [
        MECH.JointTransition(S0, S1, MECH.KIND_ORDINARY, 1),
        MECH.JointTransition(S1, S2, MECH.KIND_REPLENISH, 1,
                             authorization="treasury:a"),
    ]  # S2 reachable, no outgoing, not an exit.
    decl = _declaration(transitions=ts, exit_states=frozenset())
    v = MECH.verify_joint(decl)
    assert v.verdict == MECH.Verdict.DEADLOCK_IN_SCOPE
    assert v.deadlock_state == S2
    p = _write_manifest(tmp_path, [
        _claim("REPEATABLE_PROVEN", _model_dict(decl))])
    assert gate.main(["--manifest", str(p)]) == 1


def test_member_authorized_replenishment_blocked(gate, tmp_path):
    decl = _declaration(transitions=_transitions(auth="budget:self-issued"))
    v = MECH.verify_joint(decl)
    assert v.verdict == MECH.Verdict.JOINT_UNDETERMINED
    assert v.safety_violations
    p = _write_manifest(tmp_path, [
        _claim("EXIT_POSSIBLE_NOT_GUARANTEED", _model_dict(decl))])
    assert gate.main(["--manifest", str(p)]) == 1


# ---------------------------------------------------------------------------
# BROKEN — fail closed. The manifest or the mechanism is untrustworthy.
# ---------------------------------------------------------------------------

def test_corrupt_manifest_broken(gate, tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json", encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_duplicate_claim_ids_broken(gate, tmp_path):
    decl = _declaration()
    p = _write_manifest(tmp_path, [
        _claim("REPEATABLE_PROVEN", _model_dict(decl), cid="DUP"),
        _claim("REPEATABLE_PROVEN", _model_dict(decl), cid="DUP"),
    ])
    assert gate.main(["--manifest", str(p)]) == 2


def test_unknown_assertion_broken(gate, tmp_path):
    decl = _declaration()
    p = _write_manifest(tmp_path, [
        _claim("PROBABLY_FINE", _model_dict(decl))])
    assert gate.main(["--manifest", str(p)]) == 2


def test_malformed_model_broken(gate, tmp_path):
    model = _model_dict(_declaration())
    del model["relation_digest"]  # the register entry is untrustworthy
    p = _write_manifest(tmp_path, [_claim("REPEATABLE_PROVEN", model)])
    assert gate.main(["--manifest", str(p)]) == 2


def test_mechanism_missing_with_claims_broken(gate, tmp_path, monkeypatch):
    decl = _declaration()
    p = _write_manifest(tmp_path, [
        _claim("REPEATABLE_PROVEN", _model_dict(decl))])

    def _missing():
        raise gate.MechanismMissing("gone")

    monkeypatch.setattr(gate, "_load_mechanism", _missing)
    assert gate.main(["--manifest", str(p)]) == 2


# ---------------------------------------------------------------------------
# Dogfood — the verdict must qualify exactly the presented model.
# ---------------------------------------------------------------------------

def test_dogfood_rejects_verdict_for_another_model(gate):
    decl = _declaration()
    other = _declaration(name="OTHER")
    verdict = MECH.verify_joint(other)
    with pytest.raises(gate.GateBroken):
        gate._dogfood_verdict("X", verdict, decl, MECH)
