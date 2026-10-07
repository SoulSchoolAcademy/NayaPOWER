import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "BRAIN" / "03-KERNEL" / "0003-RUNTIME-REGISTRY-V1.json"

EXPECTED = {
    "SELF": ("tests/test_naya_identity_owner_binding.py", "identity-binding", "resolve_runtime_authorization", "py"),
    "LAW": ("tests/law_runtime_handler_scope.test.mjs", "authorize-refuse", "vm.runInNewContext", "mjs"),
    "ACT": ("tests/act_runtime_handler_time.test.mjs", "authorize-refuse", "vm.runInNewContext", "mjs"),
    "KNOW": ("tests/know_runtime_handler_freshness.test.mjs", "retrieve-refuse", "vm.runInNewContext", "mjs"),
    "PROVE": ("tests/prove-runtime.test.mjs", "assess-refuse", "assessKnowProof(", "mjs"),
    "CONNECT": ("tests/cold_graph_runtime_execution.test.mjs", "connect-verify-refuse", "vm.runInNewContext", "mjs"),
    "VERIFY": ("tests/causal_verify_runtime_execution.test.mjs", "causal-verify-refuse", "vm.runInNewContext", "mjs"),
    "LEARN": ("tests/learning_verify_guard_firing_proofs.test.mjs", "promote-refuse", "vm.Script", "mjs"),
    "EVOLVE": ("tests/cold_successor_generalization.test.mjs", "successor-reuse-refuse", "vm.runInNewContext", "mjs"),
}

def test_every_binding_declares_an_executable_behavior_contract():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    bindings = registry["node_runtime_bindings"]
    failures = []

    for node, (expected_test, expected_mode, marker, suffix) in EXPECTED.items():
        binding = bindings[node]
        contract = binding.get("behavioral_contract")
        if not isinstance(contract, dict):
            failures.append(f"{node}: behavioral_contract missing")
            continue

        if contract.get("test") != expected_test:
            failures.append(f"{node}: wrong test {contract.get('test')!r}; expected {expected_test!r}")
        if contract.get("mode") != expected_mode:
            failures.append(f"{node}: wrong mode {contract.get('mode')!r}; expected {expected_mode!r}")

        falsifier = contract.get("falsifier")
        if not isinstance(falsifier, str) or not falsifier.strip():
            failures.append(f"{node}: falsifier missing")

        boundary = str(contract.get("production_boundary") or "")
        if "production" not in boundary.lower() or "not" not in boundary.lower():
            failures.append(f"{node}: production boundary must explicitly say this is not production proof")

        test_file = ROOT / expected_test
        if not test_file.exists():
            failures.append(f"{node}: behavior test does not exist: {expected_test}")
            continue

        source = test_file.read_text(encoding="utf-8")
        if marker not in source:
            failures.append(f"{node}: mapped test lacks executable marker {marker!r}")
        cases = source.count("def test_") if suffix == "py" else source.count("test(")
        if cases < 1:
            failures.append(f"{node}: mapped test contains no executable test cases")

    assert not failures, "\n".join(failures)


def test_runtime_binding_behavior_contract_is_not_the_production_proof_claim():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    law = registry["binding_truth_rule"].lower()
    assert "production parity" in law
    for node, binding in registry["node_runtime_bindings"].items():
        contract = binding.get("behavioral_contract", {})
        assert "production" in str(contract).lower()
        assert "not" in str(contract).lower()
