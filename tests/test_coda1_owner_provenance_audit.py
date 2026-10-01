"""Coda 1: owner provenance audit on the VERIFY -> LEARN seam.

Review target: 8c02792873073ac6bc15185c82460ff1c72596f6

Answers the standing question: can requesting_owner and owner_id diverge, and
is owner_id actually authenticated?

MEASURED FINDINGS (each test asserts what is TRUE, and fails loudly if the
implementation changes so the finding must be requalified):

1. owner_id is ASSIGNED from request["requesting_owner"] in _new_receipt. The two
   fields cannot diverge at creation because one is a copy of the other.

2. owner_id IS in the C3 tamper-detection allowlist, so a caller cannot alter
   it in a presented receipt without VERIFY_RECEIPT_TAMPERED.

3. requesting_owner is NOT separately in the allowlist. It is currently safe
   only because it is not security-relevant at LEARN (owner_id is). If a future
   change makes the runtime read requesting_owner, the allowlist would silently
   under-cover it.

4. NEITHER field is authenticated. VerifyNode.submit contains no principal,
   auth, or caller-identity binding. owner_id is caller-ASSERTED at receipt creation and
   sealed thereafter. The seal proves the receipt was not altered after close;
   it does NOT prove the submitter was that owner.

Distinction that must not be collapsed: content integrity is PROVEN; owner
AUTHENTICITY is NOT established. An unkeyed seal is evidence of consistency,
not of authorship.

Reviewer evidence only. No node, kernel, or Naya 4 file is modified.
"""

from __future__ import annotations

import inspect

from naya_kernel.nodes.learn_node import _VERIFY_INTAKE_COMPARE_FIELDS
from naya_kernel.nodes.verify_node import VerifyNode

REVIEW_TARGET = "8c02792873073ac6bc15185c82460ff1c72596f6"


# ==========================================================================
# 1. DIVERGENCE -- owner_id is a copy, so the two cannot diverge
# ==========================================================================
def test_owner_id_is_assigned_from_requesting_owner():
    src = inspect.getsource(VerifyNode._new_receipt)
    assert '"requesting_owner": request.get("requesting_owner")' in src, (
        "_new_receipt no longer records requesting_owner; requalify divergence"
    )
    assert '"owner_id": request.get("requesting_owner")' in src, (
        "owner_id assignment changed; requalify whether the fields can diverge"
    )


# ==========================================================================
# 2/3. ALLOWLIST COVERAGE
# ==========================================================================
def test_owner_id_is_covered_by_tamper_detection():
    assert "owner_id" in _VERIFY_INTAKE_COMPARE_FIELDS


def test_requesting_owner_not_independently_allowlisted():
    """Documented gap-in-waiting: safe only while owner_id is what's read."""
    assert "requesting_owner" not in _VERIFY_INTAKE_COMPARE_FIELDS, (
        "requesting_owner is now allowlisted; the C3 coverage note in this "
        "module docstring needs updating"
    )


# ==========================================================================
# 4. AUTHENTICATION -- asserted, not authenticated
# ==========================================================================
def test_submit_has_no_principal_or_caller_identity_binding():
    """No authenticated identity backs owner_id at submit time."""
    src = inspect.getsource(VerifyNode.submit)
    for kw in ("principal", "authenticate", "caller_id", "identity_proof"):
        assert kw not in src, (
            f"submit now references {kw!r}; owner authenticity may be "
            "established and this finding must be requalified"
        )


def test_owner_id_is_caller_supplied_at_submission():
    """owner_id originates from the request, so it is asserted, not proven."""
    src = inspect.getsource(VerifyNode._new_receipt)
    assert '"owner_id": request.get("requesting_owner")' in src
    # Read straight from the caller-supplied request dict: asserted, not proven.


def test_review_target_recorded():
    assert len(REVIEW_TARGET) == 40
