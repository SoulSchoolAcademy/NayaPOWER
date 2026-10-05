"""Executable form of the six universal verifier properties.

WHY
---
PR #1427 codifies the verifier method in three canonical contracts. Those six
properties are correct, and they are PROSE. Nothing checks them. This is the
same failure class the conformance gate addressed for Smart Notes: a law stated
in a document drifts from behaviour until someone enforces it.

So this makes the six properties executable. It is the companion to #1427, not
a second authority: #1427 states the law, this proves a claim obeys it.

THE SIX PROPERTIES
------------------
P1 branch != main            "canonical" requires ref == main
P2 citation != substance     cited artifacts must resolve
P3 untested != certified     a security score requires an adversarial test to
                             EXIST; never-attacked is NOT_PROVEN
P4 truncated != absence      a NOT_FOUND claim must carry command, exit
                             status, and search scope
P5 builder report != proof   acceptance requires a non-builder verifier
P6 verification != authority VERIFIED confers no permission to act

Three-valued verdicts on purpose. An unresolved citation is NOT_PROVEN, not
REJECTED -- unknown is not false. Collapsing those two would make the law
reject honest uncertainty, which is how a verification culture starts hiding
unknowns.
"""

from __future__ import annotations

from dataclasses import dataclass, field

SECURITY_TIERS = frozenset({"security", "authority", "poisoning", "rollback",
                            "recovery", "causality", "learning", "production"})


@dataclass
class Claim:
    """One assertion a verifier wants to certify."""

    text: str
    ref: str | None = None
    is_main: bool | None = None
    citations: list[str] = field(default_factory=list)
    citations_resolve: dict[str, bool] = field(default_factory=dict)
    substance_holds: bool | None = None
    security_tier: bool = False
    adversarial_test_exists: bool = False
    security_score: float | None = None
    command: str | None = None
    exit_status: int | None = None
    search_scope: str | None = None
    claims_absence: bool = False
    builder: str | None = None
    independent_verifier: str | None = None
    verification_state: str | None = None
    grants_authority: bool = False

    def tier(self) -> str:
        low = (self.text or "").lower()
        return "security" if any(k in low for k in SECURITY_TIERS) else "general"


@dataclass
class Verdict:
    claim: Claim
    failures: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)

    @property
    def certified(self) -> bool:
        return not self.failures and not self.unknowns

    @property
    def state(self) -> str:
        if self.failures:
            return "REJECTED"
        if self.unknowns:
            return "NOT_PROVEN"
        return "CERTIFIED"


def verify(claim: Claim) -> Verdict:
    """Apply all six properties. Never raises; returns explicit unknowns."""
    v = Verdict(claim=claim)
    c = claim

    # P1 -- branch != main
    if c.is_main is False:
        v.failures.append(f"P1: ref {c.ref!r} is not main; 'canonical' is unearned")
    elif c.is_main is None and c.ref is not None:
        v.unknowns.append("P1: main-vs-branch status not stated")

    # P2 -- citation != substance
    bad = [k for k, ok in c.citations_resolve.items() if not ok]
    for cite in c.citations:
        if cite not in c.citations_resolve:
            v.unknowns.append(f"P2: citation {cite!r} unresolved -- cannot judge")
    if bad:
        v.failures.append(
            f"P2: citation(s) do not resolve {bad}; substance may still hold"
        )
    if c.substance_holds is None:
        v.unknowns.append("P2: substance not assessed")

    # P3 -- untested != certified
    if c.security_tier:
        if not c.adversarial_test_exists:
            v.failures.append(
                "P3: security-tier claim with NO adversarial test is NOT_PROVEN; "
                "a never-attacked defense has no security score"
            )
        elif c.security_score is None:
            v.unknowns.append("P3: adversarial test exists but no score recorded")

    # P4 -- truncated != absence
    if c.claims_absence:
        missing = [n for n, val in (("command", c.command),
                                    ("exit status", c.exit_status),
                                    ("search scope", c.search_scope))
                   if val is None]
        if missing:
            v.failures.append(
                f"P4: absence claim without {missing}; truncated or mis-scoped "
                "output cannot establish absence"
            )

    # P5 -- builder report != proof
    if c.independent_verifier is None:
        v.failures.append("P5: no independent verifier; a builder report is not proof")
    elif c.builder and c.independent_verifier == c.builder:
        v.failures.append(
            "P5: verifier is the builder; self-verification is not independent"
        )

    # P6 -- verification != authority
    if c.verification_state and c.verification_state.upper() == "VERIFIED" \
            and c.grants_authority:
        v.failures.append(
            "P6: VERIFIED must not grant authority; scores rank, they do not permit"
        )

    return v


def is_independent(builder: str | None, verifier: str | None) -> bool:
    return bool(verifier) and verifier != builder