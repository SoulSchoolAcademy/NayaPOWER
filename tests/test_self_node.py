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
    assert saved["status"] == "PRESERVED"
    assert receipt["state"] == "READY"
    assert "Use durable intelligence before planning the next action" in cold.state.known
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
