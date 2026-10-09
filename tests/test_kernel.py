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
    # Phase 2 wiring: trace may include KNOW when applicable intelligence was
    # consulted, but must always begin at SELF -> LAW.
    assert result.trace[:2] == (Node.SELF, Node.LAW)
    assert len(result.trace) in (2, 3)
    assert result.outcome is None
    # Phase 2 wiring: next_state now carries the KNOW consultation record.
    assert result.next_state["intelligence_count"] == len(
        result.next_state["intelligence_consulted"]
    )
    assert "DECISION.authorized_not_executed" in result.evidence
    assert any(e.startswith("KNOW.intelligence:") for e in result.evidence)


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
    # Phase 2 wiring: evidence gains the KNOW consultation entry; the first
    # two entries are unchanged and nothing claims a nine-node runtime ran.
    assert result.evidence[:2] == (
        "LAW.authority:reversible_change",
        "DECISION.authorized_not_executed",
    )
    assert result.evidence[2].startswith("KNOW.intelligence:")
    assert result.evidence[2].endswith("_blocks_consulted")
    assert result.outcome is None
    assert result.next_state["intelligence_count"] == len(
        result.next_state["intelligence_consulted"]
    )
    assert result.trace[:2] == (Node.SELF, Node.LAW)
    assert len(result.trace) in (2, 3)
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
