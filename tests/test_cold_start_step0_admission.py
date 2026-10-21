"""Adversarial cold-start Step 0 admission tests.

This is the *governed admission* boundary, not a proof that an agent
actually spoke or understood an oath. Real refusal must be in
run_cold_start(), not only in an optional checklist CLI flag.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from kernel.protocol.cold_start_gate import ColdStartState, run_cold_start
from kernel.protocol.read_receipt import issue_receipt
from tools.protocol_pin import issue_declaration_receipt

ROOT = Path(__file__).resolve().parents[1]


def ready_state():
    agent_id = "naya-step0-test"
    state = ColdStartState(
        agent_id=agent_id,
        human_director="Shawn Vibert",
        lane="verify",
        authority_summary="Protected production, credential, money and privacy gates; "
                          "Law 11 (do no harm) is the only hard law",
        current_truth_location="mission #2154 and current main",
        next_action="verify Step 0's required receipt",
        receipt=issue_receipt(agent_id, {
            "q1": "Shawn Vibert",
            "q2": "production, credential, money, destructive, ratification, privacy, security",
            "q3": "No",
            "q4": "9.0",
            "q5": "independent proof",
        }),
    )
    # Establish an explicit, current receipt. Existing API initially has
    # no dataclass field, so setting it post-init tests true API behavior.
    state.declaration_receipt = issue_declaration_receipt(ROOT, agent_id)
    return state


def denied(state, expected_marker="declaration"):
    outcome = run_cold_start(state)
    assert not outcome.passed, outcome
    assert any(expected_marker.lower() in f.lower() for f in outcome.failures), outcome.failures


def test_fresh_explicit_step0_receipt_is_accepted():
    state = ready_state()
    result = run_cold_start(state)
    assert result.passed, result.failures


def test_no_step0_receipt_blocks_entire_cold_start():
    state = ready_state()
    state.declaration_receipt = None
    denied(state)


@pytest.mark.parametrize("field,bad", [
    ("schema", "invalid"),
    ("protocol_sha256", "0" * 64),
    ("step0_sha256", "0" * 64),
    ("protocol_version", "2001-01-01"),
    ("agent_id", "different-naya"),
])
def test_invalid_or_other_agent_receipt_refuses(field, bad):
    state = ready_state()
    state.declaration_receipt[field] = bad
    denied(state)


def test_old_receipt_refused_without_caller_opt_in():
    state = ready_state()
    state.declaration_receipt["declared_at"] = (
        datetime.now(timezone.utc) - timedelta(hours=25)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    denied(state)


def test_future_receipt_refused():
    state = ready_state()
    state.declaration_receipt["declared_at"] = (
        datetime.now(timezone.utc) + timedelta(hours=2)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    denied(state)


def test_unreadable_canonical_declaration_tool_denies(monkeypatch):
    import kernel.protocol.cold_start_gate as gate
    state = ready_state()
    monkeypatch.setattr(gate, "_DECLARATION_TOOL",
                        Path("/nonexistent/declaration-tool.py"))
    denied(state)
