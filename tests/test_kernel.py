from pathlib import Path

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


def test_kernel_boots_from_canonical_brain_manifest():
    root = Path(__file__).resolve().parents[1]

    kernel = Kernel(root)

    assert tuple(node.value for node in kernel.manifest["nodes"]) == (
        "SELF",
        "LAW",
        "ACT",
        "KNOW",
        "PROVE",
        "CONNECT",
        "VERIFY",
        "LEARN",
        "EVOLVE",
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
