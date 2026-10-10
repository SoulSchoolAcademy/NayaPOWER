import json
from pathlib import Path


PROTOCOL = Path("NAYA-ACTIVATION/UNIVERSAL-WORKER-PROTOCOL-V1.json")


def load_protocol() -> dict:
    return json.loads(PROTOCOL.read_text(encoding="utf-8"))


def test_worker_contract_requires_explicit_learning_decision():
    protocol = load_protocol()

    assert "learning_decision" in protocol["worker_contract"]["required"]


def test_verified_completion_requires_learning_decision():
    protocol = load_protocol()

    assert "learning_decision_recorded" in protocol["completion_gate"]
