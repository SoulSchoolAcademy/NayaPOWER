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


def test_kernel_loads_ratified_machine_charter_as_governing():
    kernel = Kernel()
    assert kernel.system_charter_status == "RATIFIED_ACTIVE"
    assert kernel.system_charter_governing is True
    directive = kernel.system_charter_directive(Node.SELF)
    assert directive["node"] == "SELF"
    assert directive["governing"] is True


def test_kernel_can_compile_every_existing_node_without_creating_a_tenth():
    kernel = Kernel()
    directives = [kernel.system_charter_directive(node) for node in Node]
    assert len(directives) == 9
    assert {d["node"] for d in directives} == {node.value for node in Node}
