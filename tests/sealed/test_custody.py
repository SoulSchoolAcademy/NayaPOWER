#!/usr/bin/env python3
"""Tests for the key-custody contract (custody.py).

What these prove:
  - default is DENY (fail closed);
  - there is no static keyholder list — identity never decides;
  - the fixture author and the trial subject can never read sealed keys;
  - grants are purpose-bound AND scope-bounded (trial + expiry + justification);
  - the same request always yields the same decision (replayable by auditors);
  - retired families grant nothing for blind use.
"""

import pytest

from family_registry import FAMILIES
from custody import (
    GRANTABLE_PURPOSES,
    NEVER_GRANT_ROLES,
    AccessDecision,
    KeyAccessRequest,
    evaluate_key_access,
)


def _req(**kw):
    base = dict(
        purpose="BLIND_TRIAL_EVALUATION",
        qualification_id="QUAL-20261010-CIQ-012",
        trial_id="TRIAL-001",
        expires_at_utc="2026-10-11T00:00:00Z",
        requester_seat="naya-2",
        requester_role="EVALUATOR",
        justification="score the blind trial against the held key",
    )
    base.update(kw)
    return KeyAccessRequest(**base)


def test_no_static_keyholder_list():
    """Custody = the math. The module must not name who IS entitled."""
    import custody as m
    names = [n for n in dir(m) if "KEYHOLDER" in n.upper() or "OWNER" in n.upper()]
    assert not names, f"static keyholder-style constants found: {names}"
    # The exclusion set exists (separation of duties), the entitlement set does not.
    assert NEVER_GRANT_ROLES == {"TRIAL_SUBJECT", "FIXTURE_AUTHOR"}


def test_default_deny_unknown_purpose():
    d = evaluate_key_access(_req(purpose="JUST_CURIOUS"), FAMILIES["QUAL-20261010-CIQ-012"])
    assert isinstance(d, AccessDecision) and not d


def test_default_deny_unknown_family():
    d = evaluate_key_access(_req(), None)
    assert not d


def test_trial_subject_never_reads():
    d = evaluate_key_access(_req(requester_role="TRIAL_SUBJECT"), FAMILIES["QUAL-20261010-CIQ-012"])
    assert not d
    assert any("separation of duties" in r for r in d.reasons)


def test_fixture_author_never_reads_sealed_keys():
    d = evaluate_key_access(_req(requester_role="FIXTURE_AUTHOR"), FAMILIES["QUAL-20261010-CIQ-012"])
    assert not d


def test_retired_family_grants_nothing():
    d = evaluate_key_access(_req(qualification_id="QUAL-20261010-CIQ-001"), FAMILIES["QUAL-20261010-CIQ-001"])
    assert not d
    assert any("retired" in r for r in d.reasons)


def test_unbounded_scope_denied():
    assert not evaluate_key_access(_req(trial_id=""), FAMILIES["QUAL-20261010-CIQ-012"])
    assert not evaluate_key_access(_req(expires_at_utc=""), FAMILIES["QUAL-20261010-CIQ-012"])
    assert not evaluate_key_access(_req(justification="  "), FAMILIES["QUAL-20261010-CIQ-012"])


def test_identity_is_not_sufficient():
    """Two different seats, same purpose+scope: the decision must not depend
    on who is asking. (Identity is recorded, never decisive.)"""
    fam = FAMILIES["QUAL-20261010-CIQ-012"]
    a = evaluate_key_access(_req(requester_seat="naya-2"), fam)
    b = evaluate_key_access(_req(requester_seat="coda-1"), fam)
    assert bool(a) == bool(b) == True


def test_evaluator_grant_is_bounded_and_reasoned():
    d = evaluate_key_access(_req(), FAMILIES["QUAL-20261010-CIQ-012"])
    assert d
    text = " ".join(d.reasons)
    assert "TRIAL-001" in text and "2026-10-11" in text
    assert "not the seat" in text


def test_decisions_are_deterministic():
    fam = FAMILIES["QUAL-20261010-CIQ-012"]
    r = _req()
    assert evaluate_key_access(r, fam) == evaluate_key_access(r, fam)


def test_grantable_purposes_are_exactly_the_four():
    assert GRANTABLE_PURPOSES == {
        "BLIND_TRIAL_EVALUATION",
        "COMMITMENT_VERIFICATION",
        "FAMILY_SEALING",
        "AUDIT",
    }
