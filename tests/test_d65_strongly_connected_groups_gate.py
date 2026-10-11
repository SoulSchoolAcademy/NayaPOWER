"""Tests for tools/d65_strongly_connected_groups_gate.py.

Fake-mechanism injection: the D65 engine is not on this tree (PR #2327
unmerged), so tests inject a faithful fake of the mechanism's API surface
into sys.modules. The fire battery (not committed) judges the same gate
against the REAL #2327 bytes.
"""

import hashlib
import importlib.util
import json
import sys
import types
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
GATE_PATH = TOOLS_DIR / "d65_strongly_connected_groups_gate.py"

FAKE_KINDS = ("ordinary", "replenish", "reserve", "complete")


class FakeVerdict(Enum):
    REPEATABLE_PROVEN = "REPEATABLE_PROVEN"
    DEADLOCK_IN_SCOPE = "DEADLOCK_IN_SCOPE"
    LIVELOCK_COUNTEREXAMPLE = "LIVELOCK_COUNTEREXAMPLE"
    EXIT_POSSIBLE_NOT_GUARANTEED = "EXIT_POSSIBLE_NOT_GUARANTEED"
    JOINT_UNDETERMINED = "JOINT_UNDETERMINED"


@dataclass(frozen=True)
class FakeJointTransition:
    src: str
    dst: str
    kind: str = "ordinary"
    progress: int = 0
    authorization: str | None = None
    capacity: str | None = None
    owner: str | None = None


@dataclass(frozen=True)
class FakeJointDeclaration:
    name: str
    members: frozenset
    declared_by: str
    prereq: dict
    initial_states: frozenset
    authorized_initial: frozenset
    transitions: tuple
    relation_digest: str
    exit_states: frozenset = frozenset()


def _fake_digest(name, members, declared_by, prereq, initial_states,
                 authorized_initial, transitions, exit_states):
    payload = {
        "members": sorted(members),
        "declared_by": declared_by,
        "prereq": {k: sorted(v) for k, v in prereq.items()},
        "initial_states": sorted(initial_states),
        "authorized_initial": sorted(authorized_initial),
        "transitions": sorted(
            (t.src, t.dst, t.kind, t.progress, t.authorization,
             t.capacity, t.owner) for t in transitions),
        "exit_states": sorted(exit_states),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()).hexdigest()


def _fake_make_declaration(*, name, members, declared_by, prereq,
                           initial_states, authorized_initial,
                           transitions, exit_states=frozenset()):
    members = frozenset(members)
    prereq = {k: tuple(v) for k, v in prereq.items()}
    initial_states = frozenset(initial_states)
    authorized_initial = frozenset(authorized_initial)
    transitions = tuple(transitions)
    exit_states = frozenset(exit_states)
    digest = _fake_digest(name, members, declared_by, prereq,
                          initial_states, authorized_initial,
                          transitions, exit_states)
    return FakeJointDeclaration(
        name=name, members=members, declared_by=declared_by, prereq=prereq,
        initial_states=initial_states, authorized_initial=authorized_initial,
        transitions=transitions, relation_digest=digest,
        exit_states=exit_states)


@dataclass(frozen=True)
class FakeJointVerdict:
    verdict: FakeVerdict
    group: str
    model_digest: str
    obstruction: tuple = ()


class FakeEngineScript:
    # joint_name -> (verdict_name, obstruction tuple) or Exception
    script = {}

    @staticmethod
    def verify_joint(decl):
        honest = _fake_digest(
            decl.name, decl.members, decl.declared_by, decl.prereq,
            decl.initial_states, decl.authorized_initial,
            decl.transitions, decl.exit_states)
        if decl.relation_digest != honest:
            return FakeJointVerdict(
                FakeVerdict.JOINT_UNDETERMINED, decl.name, honest,
                ("relation digest mismatch: the presented model is not the "
                 "authorized one",))
        entry = FakeEngineScript.script.get(decl.name)
        if isinstance(entry, Exception):
            raise entry
        assert entry is not None, f"no script for {decl.name}"
        verdict_name, obstruction = entry
        return FakeJointVerdict(FakeVerdict(verdict_name), decl.name,
                                honest, tuple(obstruction))


def _install_fakes():
    pkg = types.ModuleType("drift_canary")
    pkg.__path__ = []
    mod = types.ModuleType("drift_canary.strongly_connected_groups")
    mod.Verdict = FakeVerdict
    mod.KINDS = FAKE_KINDS
    mod.JointTransition = FakeJointTransition
    mod.JointDeclaration = FakeJointDeclaration
    mod.make_declaration = _fake_make_declaration
    mod.verify_joint = FakeEngineScript.verify_joint
    sys.modules["drift_canary"] = pkg
    sys.modules["drift_canary.strongly_connected_groups"] = mod


def _remove_fakes():
    sys.modules.pop("drift_canary", None)
    sys.modules.pop("drift_canary.strongly_connected_groups", None)


@pytest.fixture()
def gate():
    _install_fakes()
    FakeEngineScript.script = {}
    spec = importlib.util.spec_from_file_location(
        "d65_gate_under_test", GATE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    yield module
    _remove_fakes()


def _claim(**over):
    base = {
        "id": "JP-0001",
        "joint_name": "test-joint",
        "asserted_verdict": "REPEATABLE_PROVEN",
        "declared_by": "treasury",
        "members": ["a", "b"],
        "prereq": {"a": ["b"], "b": ["a"]},
        "initial_states": ["s0"],
        "authorized_initial": ["s0"],
        "transitions": [
            {"src": "s0", "dst": "s1", "kind": "ordinary", "progress": 1},
            {"src": "s1", "dst": "s0", "kind": "ordinary", "progress": 1},
        ],
        "exit_states": [],
    }
    base.update(over)
    return base


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"claims": claims}), encoding="utf-8")
    return str(p)


# ---------------------------------------------------------------------------
# DORMANT — explicit, never a false green
# ---------------------------------------------------------------------------

def test_dormant_manifest_absent(gate, tmp_path):
    assert gate.main(["--manifest", str(tmp_path / "nope.json")]) == 0


def test_dormant_claims_empty(gate, tmp_path):
    assert gate.main(["--manifest", _write_manifest(tmp_path, [])]) == 0


# ---------------------------------------------------------------------------
# BROKEN — fail-closed on untrustworthy inputs
# ---------------------------------------------------------------------------

def test_broken_corrupt_json(gate, tmp_path):
    p = tmp_path / "m.json"
    p.write_text("{not json", encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_broken_claims_not_list(gate, tmp_path):
    p = tmp_path / "m.json"
    p.write_text(json.dumps({"claims": {}}), encoding="utf-8")
    assert gate.main(["--manifest", str(p)]) == 2


def test_broken_duplicate_ids(gate, tmp_path):
    c = _claim()
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c, c])]) == 2


def test_broken_missing_required_keys(gate, tmp_path):
    c = _claim()
    del c["declared_by"]
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_unknown_asserted_verdict(gate, tmp_path):
    c = _claim(asserted_verdict="PROBABLY_FINE")
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_empty_members(gate, tmp_path):
    c = _claim(members=[])
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_unknown_transition_kind(gate, tmp_path):
    c = _claim()
    c["transitions"][0]["kind"] = "teleport"
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_nonint_progress(gate, tmp_path):
    c = _claim()
    c["transitions"][0]["progress"] = "lots"
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_bad_presented_digest(gate, tmp_path):
    c = _claim(presented_digest="not-a-sha256")
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_prereq_nonmember(gate, tmp_path):
    c = _claim(prereq={"a": ["ghost"]})
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_empty_transitions(gate, tmp_path):
    c = _claim(transitions=[])
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 2


def test_broken_mechanism_missing_with_claims(gate, tmp_path):
    _remove_fakes()  # the engine is absent; claims exist -> fail closed
    try:
        assert gate.main(["--manifest",
                          _write_manifest(tmp_path, [_claim()])]) == 2
    finally:
        _install_fakes()


def test_broken_engine_raises(gate, tmp_path):
    FakeEngineScript.script = {
        "test-joint": RuntimeError("synthetic engine failure")}
    assert gate.main(["--manifest",
                      _write_manifest(tmp_path, [_claim()])]) == 2


# ---------------------------------------------------------------------------
# Certified vs violation — judged by the (fake) engine
# ---------------------------------------------------------------------------

def test_certified_honest_claim(gate, tmp_path):
    FakeEngineScript.script = {"test-joint": ("REPEATABLE_PROVEN", ())}
    assert gate.main(["--manifest",
                      _write_manifest(tmp_path, [_claim()])]) == 0


def test_violation_progress_laundering(gate, tmp_path, capsys):
    FakeEngineScript.script = {
        "test-joint": ("LIVELOCK_COUNTEREXAMPLE", ("zero-progress cycle",))}
    assert gate.main(["--manifest",
                      _write_manifest(tmp_path, [_claim()])]) == 1
    out = capsys.readouterr().out
    assert "progress-laundering" in out


def test_violation_exit_swallowing(gate, tmp_path, capsys):
    FakeEngineScript.script = {
        "test-joint": ("EXIT_POSSIBLE_NOT_GUARANTEED", ())}
    assert gate.main(["--manifest",
                      _write_manifest(tmp_path, [_claim()])]) == 1
    out = capsys.readouterr().out
    assert "exit-swallowing" in out


def test_violation_grounding_laundering(gate, tmp_path, capsys):
    FakeEngineScript.script = {
        "test-joint": ("JOINT_UNDETERMINED",
                       ("authority 'a' is a member",))}
    assert gate.main(["--manifest",
                      _write_manifest(tmp_path, [_claim()])]) == 1
    out = capsys.readouterr().out
    assert "grounding-laundering" in out


def test_certified_tamper_refusal(gate, tmp_path):
    # Wrong digest passed through untouched; the engine refuses; the claim
    # honestly asserts JOINT_UNDETERMINED -> certified.
    c = _claim(asserted_verdict="JOINT_UNDETERMINED",
               presented_digest="d" * 64)
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 0


def test_violation_tamper_asserted_proven(gate, tmp_path):
    c = _claim(asserted_verdict="REPEATABLE_PROVEN",
               presented_digest="d" * 64)
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 1


def test_violation_names_obstruction(gate, tmp_path, capsys):
    FakeEngineScript.script = {
        "test-joint": ("JOINT_UNDETERMINED",
                       ("no authorized initial allocation",))}
    c = _claim(asserted_verdict="EXIT_POSSIBLE_NOT_GUARANTEED")
    assert gate.main(["--manifest", _write_manifest(tmp_path, [c])]) == 1
    assert "no authorized initial allocation" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# main() end-to-end through real temp manifest files
# ---------------------------------------------------------------------------

def test_main_end_to_end_honest_then_violating_then_corrupt(
        gate, tmp_path, capsys):
    FakeEngineScript.script = {"test-joint": ("REPEATABLE_PROVEN", ())}
    honest = _write_manifest(tmp_path, [_claim()])
    assert gate.main(["--manifest", honest, "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["verdict"] == "PASS"
    assert payload["claims"][0]["verdict"] == "certified"

    bad = _write_manifest(tmp_path,
                          [_claim(asserted_verdict="DEADLOCK_IN_SCOPE")])
    assert gate.main(["--manifest", bad]) == 1

    corrupt = tmp_path / "c.json"
    corrupt.write_text("{{{", encoding="utf-8")
    assert gate.main(["--manifest", str(corrupt)]) == 2
