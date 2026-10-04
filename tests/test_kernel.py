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


def test_law_allows_scoped_authority_without_fabricating_execution():
    kernel = Kernel()
    context = DecisionContext(
        action="publish_change",
        consequential=True,
        authority=Authority(scope="publish_change"),
    )

    result = kernel.decide(context)

    assert result.allowed is True
    assert result.blocked_by is None
    assert result.executed is False
    assert result.truth_state is TruthState.UNKNOWN
    assert result.trace == (Node.SELF, Node.LAW)
    assert result.outcome is None
    assert result.next_state == {}
    assert "DECISION.authorized_not_executed" in result.evidence


def test_decision_does_not_masquerade_as_nine_node_runtime_or_observation():
    kernel = Kernel()
    context = DecisionContext(
        action="reversible_change",
        consequential=True,
        authority=Authority(scope="reversible_change"),
    )

    result = kernel.decide(context)

    assert result.allowed is True
    assert result.executed is False
    assert result.evidence == (
        "LAW.authority:reversible_change",
        "DECISION.authorized_not_executed",
    )
    assert result.outcome is None
    assert result.next_state == {}
    assert result.trace == (Node.SELF, Node.LAW)
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


def test_kernel_loads_candidate_machine_charter_without_activating_it():
    kernel = Kernel()
    assert kernel.system_charter_status == "CANDIDATE_NON_GOVERNING"
    assert kernel.system_charter_governing is False
    preview = kernel.system_charter_directive(Node.SELF, require_governing=False)
    assert preview["node"] == "SELF"
    assert preview["governing"] is False


def test_kernel_refuses_governing_charter_directive_before_ratification():
    kernel = Kernel()
    import pytest
    from kernel.system_charter import CharterContractError

    with pytest.raises(CharterContractError, match="SYSTEM_CHARTER_NOT_RATIFIED_ACTIVE"):
        kernel.system_charter_directive(Node.LAW)
