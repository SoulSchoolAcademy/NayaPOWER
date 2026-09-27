from datetime import datetime, timedelta, timezone

from kernel.nayapower_kernel import (
    Authority,
    DecisionContext,
    Kernel,
    LawDecision,
    TruthState,
)


def test_law_explicitly_denies_missing_authority():
    result = Kernel().decide(
        DecisionContext(action="publish_change", consequential=True, authority=None)
    )

    assert result.law_decision is LawDecision.DENIED
    assert result.allowed is False
    assert result.blocked_by.value == "LAW"
    assert result.audit_receipt["decision"] == "DENIED"


def test_law_requires_confirmation_when_authority_requires_it():
    result = Kernel().decide(
        DecisionContext(
            action="publish_change",
            consequential=True,
            authority=Authority(scope="publish_change", requires_confirmation=True),
        )
    )

    assert result.law_decision is LawDecision.REQUIRES_CONFIRMATION
    assert result.allowed is False
    assert result.executed is False


def test_law_rejects_revoked_authority():
    result = Kernel().decide(
        DecisionContext(
            action="publish_change",
            consequential=True,
            authority=Authority(scope="publish_change", revoked=True),
        )
    )

    assert result.law_decision is LawDecision.REVOKED
    assert result.allowed is False
    assert result.executed is False


def test_law_rejects_expired_authority():
    expired = datetime.now(timezone.utc) - timedelta(seconds=1)

    result = Kernel().decide(
        DecisionContext(
            action="publish_change",
            consequential=True,
            authority=Authority(scope="publish_change", expires_at=expired),
        )
    )

    assert result.law_decision is LawDecision.EXPIRED
    assert result.allowed is False
    assert result.executed is False


def test_law_returns_out_of_scope_instead_of_generic_block():
    result = Kernel().decide(
        DecisionContext(
            action="publish_change",
            consequential=True,
            authority=Authority(scope="read_only"),
        )
    )

    assert result.law_decision is LawDecision.OUT_OF_SCOPE
    assert result.allowed is False
    assert result.executed is False


def test_law_authorizes_exact_live_scope_and_emits_auditable_receipt():
    result = Kernel().decide(
        DecisionContext(
            action="publish_change",
            consequential=True,
            authority=Authority(scope="publish_change"),
        )
    )

    assert result.law_decision is LawDecision.AUTHORIZED
    assert result.allowed is True
    assert result.executed is True
    assert result.audit_receipt["node"] == "LAW"
    assert result.audit_receipt["action"] == "publish_change"
    assert result.audit_receipt["decision"] == "AUTHORIZED"
    assert result.truth_state is TruthState.UNKNOWN
