import json

import tools.smart_note_v2 as smart_note_v2
from kernel.self_node import JsonContinuityStore, RuntimeIdentity, SelfNode, SelfNodeError


def test_self_cold_boot_establishes_identity_mission_and_checkpoint(tmp_path):
    node = SelfNode(JsonContinuityStore(tmp_path / "self.json"))
    receipt = node.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "Preserve intelligence across Naya generations", "Prove SELF continuity", "kernel")
    assert receipt["state"] == "READY"
    assert receipt["actor_id"] == "naya-1"
    assert receipt["checkpoint_id"].startswith("CHK-")


def test_self_persists_experience_and_cold_successor_inherits_it(tmp_path):
    store = JsonContinuityStore(tmp_path / "self.json")
    first = SelfNode(store)
    first.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "Preserve intelligence across Naya generations", "Use retained intelligence to improve future execution", "kernel")
    saved = first.record_experience(lesson="Use durable intelligence before planning the next action", observed_outcome="Later execution had the prior lesson available", next_objective="Continue from retained intelligence without reconstruction")
    packet = first.successor_packet()
    cold = SelfNode(store)
    receipt = cold.boot_successor(RuntimeIdentity("naya-2", "NayaPOWER", "naya"), packet)
    assert saved["status"] == "PRESERVED_UNVERIFIED"
    assert saved["warning"] == "unverified_lesson_not_governed"
    assert receipt["state"] == "READY"
    assert "unverified:Use durable intelligence before planning the next action" in cold.state.known
    assert receipt["inherited_checkpoint_id"] == saved["checkpoint_id"]
    assert receipt["inherited_experience_count"] == 1


def test_self_refuses_cross_system_continuity(tmp_path):
    store = JsonContinuityStore(tmp_path / "self.json")
    first = SelfNode(store)
    first.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "Mission", "Objective", "kernel")
    first.record_experience(lesson="Persist before handoff", observed_outcome="Checkpoint created")
    packet = first.successor_packet()
    cold = SelfNode(store)
    try:
        cold.boot_successor(RuntimeIdentity("naya-2", "OtherSystem", "naya"), packet)
    except SelfNodeError as exc:
        assert str(exc) == "system_identity_mismatch"
    else:
        raise AssertionError("cross-system successor must be rejected")


def test_self_requires_identity_and_objective(tmp_path):
    node = SelfNode(JsonContinuityStore(tmp_path / "self.json"))
    try:
        node.cold_boot(RuntimeIdentity("", "NayaPOWER", "naya"), "Mission", "Objective", "kernel")
    except SelfNodeError as exc:
        assert str(exc) == "identity_missing"
    else:
        raise AssertionError("missing identity must fail")
    try:
        node.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "Mission", "", "kernel")
    except SelfNodeError as exc:
        assert str(exc) == "objective_missing"
    else:
        raise AssertionError("missing objective must fail")


def test_self_does_not_allow_successor_packet_before_experience(tmp_path):
    node = SelfNode(JsonContinuityStore(tmp_path / "self.json"))
    node.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "Mission", "Objective", "kernel")
    try:
        node.successor_packet()
    except SelfNodeError as exc:
        assert str(exc) == "successor_not_ready"
    else:
        raise AssertionError("successor packet must require preserved experience")


def test_self_load_rejects_tampered_checkpoint(tmp_path):
    path = tmp_path / "self.json"
    store = JsonContinuityStore(path)
    node = SelfNode(store)
    node.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "Mission", "Objective", "kernel")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["mission"] = "TAMPERED-MISSION"
    path.write_text(json.dumps(payload), encoding="utf-8")
    try:
        store.load()
    except SelfNodeError as exc:
        assert str(exc) == "checkpoint_integrity_failed"
    else:
        raise AssertionError("tampered checkpoint payload must be rejected")


def test_self_load_rejects_tampered_checkpoint_id(tmp_path):
    path = tmp_path / "self.json"
    store = JsonContinuityStore(path)
    node = SelfNode(store)
    node.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "Mission", "Objective", "kernel")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["checkpoint_id"] = "CHK-000000000000000000000000"
    path.write_text(json.dumps(payload), encoding="utf-8")
    try:
        store.load()
    except SelfNodeError as exc:
        assert str(exc) == "checkpoint_integrity_failed"
    else:
        raise AssertionError("forged checkpoint id must be rejected")


def test_self_load_rejects_unparseable_store(tmp_path):
    path = tmp_path / "self.json"
    path.write_text("{not valid json", encoding="utf-8")
    try:
        JsonContinuityStore(path).load()
    except SelfNodeError as exc:
        assert str(exc) == "checkpoint_integrity_failed"
    else:
        raise AssertionError("unparseable store must be rejected as corrupt")


def test_self_cold_boot_fails_closed_on_corrupt_store(tmp_path):
    path = tmp_path / "self.json"
    store = JsonContinuityStore(path)
    first = SelfNode(store)
    first.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "True-Mission", "Objective", "kernel")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["mission"] = "TAMPERED-MISSION"
    path.write_text(json.dumps(payload), encoding="utf-8")
    cold = SelfNode(JsonContinuityStore(path))
    try:
        cold.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "True-Mission", "Objective", "kernel")
    except SelfNodeError as exc:
        assert str(exc) == "checkpoint_integrity_failed"
    else:
        raise AssertionError("cold boot must fail closed on a corrupt store")


def test_self_boot_receipt_reports_prior_integrity(tmp_path):
    path = tmp_path / "self.json"
    node = SelfNode(JsonContinuityStore(path))
    fresh = node.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "Mission", "Objective", "kernel")
    assert fresh["prior_checkpoint_integrity"] == "ABSENT"
    again = SelfNode(JsonContinuityStore(path))
    receipt = again.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "Mission", "Objective", "kernel")
    assert receipt["prior_checkpoint_integrity"] == "VERIFIED"


# ---- GAP 5 (Phase 4): governed lesson admission ----


def _boot_node(tmp_path):
    node = SelfNode(JsonContinuityStore(tmp_path / "self.json"))
    node.cold_boot(RuntimeIdentity("naya-1", "NayaPOWER", "naya"), "Mission", "Objective", "kernel")
    return node


def _fake_load_json(entries, fail=False):
    def _load(path):
        if fail:
            raise FileNotFoundError(str(path))
        return {"entries": entries}

    return _load


def test_self_raw_lesson_stored_as_unverified_with_warning(tmp_path):
    node = _boot_node(tmp_path)
    saved = node.record_experience(lesson="Raw ungoverned lesson", observed_outcome="It happened")
    assert saved["status"] == "PRESERVED_UNVERIFIED"
    assert saved["warning"] == "unverified_lesson_not_governed"
    assert "unverified:Raw ungoverned lesson" in node.state.known
    assert "Raw ungoverned lesson" not in node.state.known
    assert node.state.experience_count == 1
    assert node.state.successor_ready is True


def test_self_candidate_note_refused_without_state_change(tmp_path, monkeypatch):
    monkeypatch.setattr(
        smart_note_v2,
        "load_json",
        _fake_load_json(
            [{"smart_note_id": "SN-CAND-1", "intelligent_block_id": "IB-1", "truth_state": "CANDIDATE"}]
        ),
    )
    node = _boot_node(tmp_path)
    result = node.record_experience(smart_note_id="SN-CAND-1", observed_outcome="Observed")
    assert result["status"] == "REFUSED"
    assert result["reason"] == "truth_state_below_VERIFIED"
    assert result["truth_state"] == "CANDIDATE"
    assert node.state.experience_count == 0
    assert node.state.known == []
    assert node.state.lesson_refs == []
    assert node.state.successor_ready is False


def test_self_verified_note_preserved_with_reference(tmp_path, monkeypatch):
    monkeypatch.setattr(
        smart_note_v2,
        "load_json",
        _fake_load_json(
            [{"smart_note_id": "SN-VER-1", "intelligent_block_id": "IB-2", "truth_state": "VERIFIED"}]
        ),
    )
    node = _boot_node(tmp_path)
    result = node.record_experience(
        smart_note_id="SN-VER-1", observed_outcome="Outcome held", next_objective="Next"
    )
    assert result["status"] == "PRESERVED"
    assert result["truth_state"] == "VERIFIED"
    assert result["smart_note_id"] == "SN-VER-1"
    assert "sn:SN-VER-1" in node.state.known
    assert node.state.experience_count == 1
    refs = node.state.lesson_refs
    assert len(refs) == 1
    assert refs[0]["smart_note_id"] == "SN-VER-1"
    assert refs[0]["truth_state"] == "VERIFIED"
    assert "recorded_at" in refs[0]
    assert node.state.objective == "Next"
    assert node.state.successor_ready is True


def test_self_missing_note_refused_fail_closed(tmp_path, monkeypatch):
    monkeypatch.setattr(smart_note_v2, "load_json", _fake_load_json([]))
    node = _boot_node(tmp_path)
    result = node.record_experience(smart_note_id="SN-NOPE", observed_outcome="Outcome")
    assert result["status"] == "REFUSED"
    assert result["reason"] == "note_not_found"
    assert node.state.experience_count == 0
    assert node.state.known == []


def test_self_unreadable_registry_refused_fail_closed(tmp_path, monkeypatch):
    monkeypatch.setattr(smart_note_v2, "load_json", _fake_load_json([], fail=True))
    node = _boot_node(tmp_path)
    result = node.record_experience(smart_note_id="SN-ANY", observed_outcome="Outcome")
    assert result["status"] == "REFUSED"
    assert result["reason"] == "note_not_found"
    assert node.state.experience_count == 0


def test_self_requires_lesson_or_note(tmp_path):
    node = _boot_node(tmp_path)
    try:
        node.record_experience(observed_outcome="Outcome")
    except SelfNodeError as exc:
        assert str(exc) == "experience_incomplete"
    else:
        raise AssertionError("missing lesson and note must fail")


def test_self_governed_note_against_real_registry(tmp_path):
    # End-to-end proof that the lazy import and the real REGISTRY path work.
    # SN-016 is RATIFIED, SN-001 is CANDIDATE in the checked-in registry.
    node = _boot_node(tmp_path)
    accepted = node.record_experience(smart_note_id="SN-016", observed_outcome="Observed in this repo")
    assert accepted["status"] == "PRESERVED"
    assert accepted["truth_state"] == "RATIFIED"
    assert "sn:SN-016" in node.state.known
    refused = node.record_experience(smart_note_id="SN-001", observed_outcome="Observed")
    assert refused["status"] == "REFUSED"
    assert refused["reason"] == "truth_state_below_VERIFIED"
    assert refused["truth_state"] == "CANDIDATE"
    assert node.state.experience_count == 1
