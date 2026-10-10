#!/usr/bin/env python3
"""Sealed-key custody: the math holds the keys (Phase 3A activation).

Shawn, 2026-10-10: "Who holds the keys to the sealed fixtures? The math and
the logic holds the keys — doing the most intelligent thing in any one
situation by zooming in, zooming out, being fully aware of all the elements,
and then making the best choice for the collective."

This module encodes that as an access-policy contract. There is deliberately
NO keyholder list here — no person, no role, no static roster. Every access
decision is purpose-bound, scope-bounded, and decided by the calculus over
the full situation. A seat's identity is recorded for audit but is NEVER
sufficient for a grant: who someone is does not decide; the math does.

Purposes (the only ones that may ever be granted):
  BLIND_TRIAL_EVALUATION  — the evaluator scores a blind trial against the
                            held key. Never the trial subject, never the
                            fixture author.
  COMMITMENT_VERIFICATION — pre-scoring check that in-repo commitments match
                            the held key (sealed_convention.verify_commitment).
  FAMILY_SEALING          — the fixture author generates tasks and seals the
                            key file. Sealing NEVER implies reading a sealed
                            family's keys.
  AUDIT                   — independent review of custody decisions themselves.

Hard denials (fail closed):
  - default: DENY. No purpose, no grant.
  - the trial subject may never read the keys, under any purpose.
  - the fixture author may never read a sealed family's keys (separation of
    duties: author seals, evaluator scores).
  - retired families grant nothing for blind use.
  - unbounded scope (no family, no trial, no expiry) is denied.
  - purpose drift: a grant for one purpose never authorizes another.

The decision record carries the calculus inputs so an independent auditor
can replay exactly why access was granted or denied.
"""

from dataclasses import dataclass, field

# Purposes that may ever be granted. Anything else -> DENY.
GRANTABLE_PURPOSES = frozenset({
    "BLIND_TRIAL_EVALUATION",
    "COMMITMENT_VERIFICATION",
    "FAMILY_SEALING",
    "AUDIT",
})

# Roles that may NEVER receive key material for a sealed family, regardless
# of purpose. This is a separation-of-duties rule, not a keyholder roster:
# it names who is excluded, never who is entitled.
NEVER_GRANT_ROLES = frozenset({
    "TRIAL_SUBJECT",   # the seat being qualified
    "FIXTURE_AUTHOR",  # the seat that designed/sealed the family
})


@dataclass(frozen=True)
class KeyAccessRequest:
    """Everything the calculus may consider. Identity is informational only:
    it is recorded for audit and it is NEVER sufficient for a grant."""
    purpose: str
    qualification_id: str            # e.g. QUAL-20261010-CIQ-012
    trial_id: str = ""               # bound trial, "" = unbounded
    expires_at_utc: str = ""         # "" = no expiry declared
    requester_seat: str = ""         # informational only
    requester_role: str = ""         # informational only; NEVER decisive
    justification: str = ""          # why this access serves the collective


@dataclass(frozen=True)
class AccessDecision:
    granted: bool
    reasons: tuple = field(default_factory=tuple)

    def __bool__(self):
        return self.granted


def evaluate_key_access(request: KeyAccessRequest, family: dict | None) -> AccessDecision:
    """Decide a key-access request. Fail-closed; deterministic: the same
    request against the same family record always yields the same decision."""
    deny = lambda *rs: AccessDecision(False, tuple(rs))

    if request.purpose not in GRANTABLE_PURPOSES:
        return deny(f"purpose {request.purpose!r} is not grantable")

    if family is None:
        return deny("unknown qualification family — fail closed")

    if request.requester_role in NEVER_GRANT_ROLES:
        return deny(
            f"role {request.requester_role!r} is excluded by separation of "
            "duties (author seals, evaluator scores, subject is blind)"
        )

    if family.get("state") == "retired":
        return deny(
            f"family {family.get('code')} is retired — no blind-use key "
            "access, for any purpose"
        )
    if not family.get("blind_eligible"):
        return deny("family is not blind-eligible")

    if request.purpose == "FAMILY_SEALING":
        # Sealing writes keys; it never reads another family's sealed keys.
        return deny("FAMILY_SEALING authorizes writing a new key file, never reading sealed keys")

    if not request.trial_id:
        return deny("unbounded scope: access must name the bound trial")
    if not request.expires_at_utc:
        return deny("no expiry: access must carry an expiry")
    if not request.justification.strip():
        return deny("no justification: access must state why it serves the collective")

    return AccessDecision(True, (
        f"purpose {request.purpose} is grantable",
        f"family {family.get('code')} is sealed and blind-eligible",
        f"requester role {request.requester_role!r} is not excluded",
        f"scope bounded to trial {request.trial_id} until {request.expires_at_utc}",
        "identity recorded for audit; the grant follows the calculus, not the seat",
    ))
