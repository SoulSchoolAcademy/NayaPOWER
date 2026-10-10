"""
authority_gate.py — Machine law: enforce protected gates on proposed actions.

"Run the math and act" cannot grant permissions. This gate classifies
a proposed action against the protected gates BEFORE any score is read.
No score overrides a hard gate.

Verdicts: ALLOW | NEEDS_SHAWN | REFUSE
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Verdict(Enum):
    ALLOW = "ALLOW"
    NEEDS_SHAWN = "NEEDS_SHAWN"
    REFUSE = "REFUSE"


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
