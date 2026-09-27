from kernel.nayapower_kernel import (
    Authority,
    DecisionContext,
    Kernel,
    Node,
    TruthState,
)


def test_kernel_exposes_exactly_nine_master_nodes():
    assert Kernel.node_order() == (
        Node.SELF,
        Node.LAW,
        Node.ACT,
        Node.KNOW,
        Node.PROVE,
        Node.CONNECT,
        Node.VERIFY,
        Node.LEARN,
        Node.EVOLVE,
    )


def test_law_blocks_consequential_action_without_authority():
    kernel = Kernel()
    context = DecisionContext(
        action="publish_change",
        consequential=True,
        authority=None,
    )

    result = kernel.decide(context)

    assert result.allowed is False
    assert result.truth_state is TruthState.BLOCKED
    assert result.blocked_by is Node.LAW
    assert result.trace == (Node.SELF, Node.LAW)


def test_law_allows_scoped_authority_and_kernel_executes_without_claiming_verification():
    kernel = Kernel()
    context = DecisionContext(
        action="publish_change",
        consequential=True,
        authority=Authority(scope="publish_change"),
    )

    result = kernel.decide(context)

    assert result.allowed is True
    assert result.blocked_by is None
    assert result.executed is True
    assert result.truth_state is TruthState.UNKNOWN
    assert result.trace == Kernel.node_order()


def test_execution_records_observation_without_promoting_it_to_verified_outcome():
    kernel = Kernel()
    context = DecisionContext(
        action="reversible_change",
        consequential=True,
        authority=Authority(scope="reversible_change"),
    )

    result = kernel.decide(context)

    assert result.evidence
    assert result.outcome == "executed"
    assert result.next_state["last_action"] == "reversible_change"
    assert result.truth_state is TruthState.UNKNOWN


def test_learning_requires_verified_outcome():
    kernel = Kernel()
    blocked = DecisionContext(
        action="publish_change",
        consequential=True,
        authority=None,
    )

    result = kernel.decide(blocked)

    assert result.learning_candidate is None


def test_kernel_can_boot_from_canonical_brain_manifest():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    kernel = Kernel.from_brain(root)

    assert kernel.node_order() == Kernel.node_order()
    assert kernel.kernel_id == "NAYAPOWER-MASTER-KERNEL-V1"
    assert kernel.source_manifest == "BRAIN/03-KERNEL/MANIFEST.json"


def test_kernel_rejects_manifest_with_wrong_node_order(tmp_path):
    import json
    import shutil

    source = Path(__file__).resolve().parents[1]
    shutil.copytree(source / "BRAIN", tmp_path / "BRAIN")
    manifest = tmp_path / "BRAIN/03-KERNEL/MANIFEST.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["nodes"][0], data["nodes"][1] = data["nodes"][1], data["nodes"][0]
    manifest.write_text(json.dumps(data), encoding="utf-8")

    import pytest
    with pytest.raises(ValueError, match="canonical nine-node order"):
        Kernel.from_brain(tmp_path)


def test_kernel_manifest_declares_the_executable_cold_runtime_entrypoint():
    from pathlib import Path
    import json

    root = Path(__file__).resolve().parents[1]
    manifest = json.loads(
        (root / "BRAIN/03-KERNEL/MANIFEST.json").read_text(encoding="utf-8")
    )

    assert manifest["runtime_entrypoint"] == "runtime/cold_runtime.py"
    assert manifest["runtime_loader"] == "Kernel.from_brain"
    assert manifest["canonical_persistence_adapter"] == "runtime/canonical_memory.py"


def test_kernel_rejects_noncanonical_manifest_runtime_binding(tmp_path):
    from pathlib import Path
    import json
    import shutil
    import pytest

    source = Path(__file__).resolve().parents[1]
    shutil.copytree(source / "BRAIN", tmp_path / "BRAIN")
    manifest = tmp_path / "BRAIN/03-KERNEL/MANIFEST.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["runtime_entrypoint"] = "runtime/not-the-canonical-runtime.py"
    manifest.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="runtime entrypoint"):
        Kernel.from_brain(tmp_path)
