"""
authority_gate.py — Machine law: enforce protected gates on proposed actions.

"Run the math and act" cannot grant permissions. This gate classifies
a proposed action against the protected gates BEFORE any score is read.
No score overrides a hard gate.

Verdicts: ALLOW | NEEDS_SHAWN | REFUSE

Law 11 wiring (2026-10-11): classify_typed_action() evaluates a TypedAction
on its structured fields (operation, environment, resource, authority_ref)
— not on keyword matching of free text. Rewording a request cannot bypass
the gate. The legacy classify_action(action_text) remains for backward
compatibility but is deprecated for consequential decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .typed_action import (
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    TypedAction,
    execution_door_check,
    law11_gate,
)


class Verdict(Enum):
    ALLOW = "ALLOW"
    NEEDS_SHAWN = "NEEDS_SHAWN"
    REFUSE = "REFUSE"


# Law 11 four-state verdict -> legacy three-state verdict.
_LAW11_TO_LEGACY = {
    ADMISSIBLE: Verdict.ALLOW,
    NEEDS_EVIDENCE: Verdict.NEEDS_SHAWN,
    NEEDS_AUTHORITY: Verdict.NEEDS_SHAWN,
    PROHIBITED: Verdict.REFUSE,
}


# (gate_id, human description, keyword signals in action text)
#
# Authority Coverage Audit (Gate 2 of 7, 2026-10-10): every Domain 5
# human-only gate of Operating Code V2 is encoded here. Signals are
# fail-closed tripwires — a false NEEDS_SHAWN asks Shawn, a miss lets a
# human-only action through. When in doubt the signal stays.
PROTECTED_GATES = [
    ("production", "Production deploys/dispatches and production database "
     "reads, writes, migrations",
     ["production deploy", "deploy to production", "prod db", "prod database",
      "production database", "supabase production", "migrate production",
      "migrate the production", "promote to production", "production dispatch",
      "dispatch to production", "dispatch the production", "workflow dispatch",
      "production migration", "migration to production", "to production",
      "into production", "live database",
      "production schema", "production data", "export production"]),
    ("workflows", "GitHub workflow files (.github/workflows/)",
     [".github/workflows", "github workflow", "actions workflow"]),
    ("credentials_money", "Credentials, money, payments",
     ["credential", "api key", "secret", "password", "payment", "charge",
      "money", "billing", "invoice", "refund", "token", "private key",
      "ssh key", "access key", "secret key"]),
    ("destructive", "Destructive or irreversible actions",
     ["delete production", "drop table", "drop database", "rm -rf",
      "force push main", "irreversible", "wipe", "wipe out", "destroy",
      "destroy the", "truncate", "delete from", "delete all", "nuke",
      "purge", "format the disk", "delete the repository", "delete repo"]),
    ("ratification", "Constitutional ratification",
     ["mark ratified", "ratify", "ratified", "ratification"]),
    ("security_privacy", "Security, privacy, consent, authority-envelope changes",
     ["disable rls", "bypass auth", "pii", "privacy policy", "consent",
      "change authority", "elevate privilege", "disable gate",
      "authentication", "grant admin", "admin access", "change permission",
      "access control", "revoke access", "modify permissions",
      "security change"]),
]

# Actions that are never allowed regardless of who asks.
HARD_REFUSALS = [
    "harm", "illegal", "destroy evidence", "break trust",
    "fabricate evidence", "weaken test", "merge red",
]


@dataclass
class GateResult:
    verdict: Verdict
    gate_id: str | None
    reason: str


def classify_action(action_text: str) -> GateResult:
    """Classify a proposed action. Gate check runs BEFORE scoring."""
    text = action_text.lower()

    for refusal in HARD_REFUSALS:
        if refusal in text:
            return GateResult(
                Verdict.REFUSE, "hard-stop",
                f"Hard stop: action matches prohibited pattern '{refusal}'.",
            )

    for gate_id, description, signals in PROTECTED_GATES:
        for signal in signals:
            if signal in text:
                return GateResult(
                    Verdict.NEEDS_SHAWN, gate_id,
                    f"Protected gate '{description}': requires Shawn's explicit word. "
                    "No scorecard overrides this.",
                )

    return GateResult(Verdict.ALLOW, None, "Within standing authority.")


def is_authorized(action_text: str) -> bool:
    return classify_action(action_text).verdict == Verdict.ALLOW


def classify_typed_action(action: TypedAction) -> GateResult:
    """Classify a typed action via the Law 11 gate.

    This is the preferred entry point for consequential decisions. The verdict
    is derived from the action's structured fields — operation, environment,
    resource, authority_ref, reversibility, and the Law 11 safety dimensions
    — never from keyword matching on the description text.

    Law 11 runs BEFORE Value Calculus scoring: a PROHIBITED verdict here is
    final. No value score can override it. ("A good calculation cannot create
    permission.")

    Verdict mapping:
      ADMISSIBLE      -> ALLOW
      NEEDS_EVIDENCE  -> NEEDS_SHAWN (investigate; human only when necessary)
      NEEDS_AUTHORITY -> NEEDS_SHAWN (preserve work, request exact authorization)
      PROHIBITED      -> REFUSE (no approval can permit)
    """
    law11 = law11_gate(action)
    legacy = _LAW11_TO_LEGACY[law11.verdict]
    gate_id = law11.reasons[0] if law11.reasons else None
    reason = (
        f"Law 11 gate verdict={law11.verdict}"
        + (f" [{', '.join(law11.reasons)}]" if law11.reasons else "")
        + f" (policy {law11.policy_version}; actor {action.actor_id}; "
        f"operation {action.operation}; environment {action.environment}; "
        f"resource {action.resource})"
    )
    if legacy == Verdict.REFUSE:
        reason += " No score overrides a hard gate."
    elif legacy == Verdict.NEEDS_SHAWN:
        reason += " No scorecard overrides this."
    return GateResult(legacy, gate_id, reason)


def is_typed_action_authorized(action: TypedAction) -> bool:
    """True only when the Law 11 gate returns ADMISSIBLE."""
    return classify_typed_action(action).verdict == Verdict.ALLOW


__all__ = [
    "Verdict",
    "GateResult",
    "PROTECTED_GATES",
    "HARD_REFUSALS",
    "classify_action",
    "is_authorized",
    "classify_typed_action",
    "is_typed_action_authorized",
    "execution_door_check",
]
