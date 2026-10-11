"""
cold_successor_test.py — Machine law: acceptance test that state survives the agent.

The ultimate test of NayaPOWER: does intelligence survive the Naya?
A handoff passes only if a fresh agent can answer, from the handoff alone:
what happened, what is true, what proof exists, what is blocked, what is next.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .work_cycle_receipt import check_sign_out


@dataclass
class Handoff:
    what_happened: str
    what_is_true: str
    authority_used: str
    proof: str            # evidence locations: SHAs, links, test counts
    what_is_open: str
    what_is_blocked: str
    next_action: str
    sign_in_receipt: dict | None = None
    sign_out_receipt: dict | None = None
    current_main_sha: str = ""
    live_feed_issues: list[int] | None = None


@dataclass
class SuccessorResult:
    passed: bool
    failures: list = field(default_factory=list)


def _nonempty(h: Handoff, attr: str, label: str, failures: list) -> None:
    if not getattr(h, attr).strip():
        failures.append(f"Handoff missing: {label}.")


def check_handoff(h: Handoff) -> SuccessorResult:
    failures: list[str] = []
    _nonempty(h, "what_happened", "what happened", failures)
    _nonempty(h, "what_is_true", "current truth", failures)
    _nonempty(h, "authority_used", "authority used", failures)
    _nonempty(h, "proof", "proof / evidence locations", failures)
    _nonempty(h, "what_is_open", "open work", failures)
    _nonempty(h, "next_action", "next executable action", failures)
    # what_is_blocked may legitimately be "none" — but must be stated.
    if not h.what_is_blocked.strip():
        failures.append("Handoff missing: blockers (state 'none' if unblocked).")
    # A continuity handoff does not close the cycle unless its same-feed
    # sign-in/sign-out receipt pair validates against the observed current main.
    if h.sign_in_receipt is None or h.sign_out_receipt is None:
        failures.append("Handoff missing: validated sign-in and sign-out feed receipts.")
    else:
        cycle = check_sign_out(
            h.sign_in_receipt, h.sign_out_receipt, h.current_main_sha,
            set(h.live_feed_issues) if h.live_feed_issues is not None else None,
        )
        failures.extend(cycle.failures)
    return SuccessorResult(passed=not failures, failures=failures)
