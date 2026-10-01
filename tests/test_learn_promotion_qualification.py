"""Coda 1: LEARN promotion boundary qualification at frozen 73e17e81.

CURRENT TRUTH PROVEN HERE:
Promotion does NOT re-derive evidence authenticity. `_is_qualifying_verify`
accepts a receipt on exactly two caller-controlled fields:
    node_id == "NAYA-KERNEL-VERIFY"
    verification_state == "VERIFIED_PASS"
No signature, hash, provenance, issuer, or nonce is checked anywhere in
`register_verify_receipt`, `ingest_verify_receipt`, or
`_resolve_and_validate_refs`.

These tests document that boundary precisely. They do not assert forgery
currently PROMOTES a learning -- that depends on the remaining rungs, which
this suite does not fabricate. Each claim is classified, not assumed.

Classification used: UNKNOWN / IMPLEMENTED / UNIT_VERIFIED / INTEGRATION_VERIFIED
"""

from __future__ import annotations

import inspect

import pytest

from naya_kernel.nodes.learn_node import LearnNode

FROZEN_SHA = "73e17e81cd214a02c978c7da68e866c1790a7322"

_FORGED = {
    "receipt_id": "forged-1",
    "node_id": "NAYA-KERNEL-VERIFY",
    "verification_state": "VERIFIED_PASS",
}


# ==========================================================================
# RUNG: evidence authenticity is NOT derived
# ==========================================================================
def test_forged_two_field_receipt_qualifies():
    """PROVEN: qualifying is caller-asserted, not derived."""
    assert LearnNode()._is_qualifying_verify(dict(_FORGED)) is True


def test_qualification_ignores_all_provenance_fields():
    """PROVEN: a receipt with no provenance at all still qualifies."""
    receipt = dict(_FORGED)
    for absent in ("signature", "hash", "provenance", "issued_by", "nonce",
                   "ledger_ref", "receipt_hash"):
        assert absent not in receipt
    assert LearnNode()._is_qualifying_verify(receipt) is True


def test_non_verify_node_or_non_pass_state_is_refused():
    """PROVEN: the two fields are the entire gate."""
    n = LearnNode()
    assert n._is_qualifying_verify({**_FORGED, "node_id": "NAYA-KERNEL-LEARN"}) is False
    assert n._is_qualifying_verify({**_FORGED, "verification_state": "VERIFIED_FAIL"}) is False


@pytest.mark.parametrize(
    "symbol",
    ["register_verify_receipt", "ingest_verify_receipt", "_is_qualifying_verify",
     "_resolve_and_validate_refs"],
)
def test_no_integrity_verification_in_evidence_path(symbol):
    """PROVEN: no signature/hash/provenance check exists in the evidence path."""
    src = inspect.getsource(getattr(LearnNode, symbol))
    for kw in ("signature", "hmac", "provenance", "issued_by", "nonce",
               "sha256", "verify_signature"):
        assert kw not in src, (
            f"{symbol} now mentions {kw!r}; the evidence-integrity finding must "
            "be requalified and likely closed"
        )


def test_runtime_intake_shares_the_lab_store():
    """PROVEN: ingest_verify_receipt writes the same store register does.

    So the forge surface is reachable from the event-driven runtime path, not
    only the documented test/lab seam.
    """
    n = LearnNode()
    n.register_verify_receipt(dict(_FORGED, receipt_id="lab-1"))
    assert "lab-1" in n._verify_receipts
    src = inspect.getsource(LearnNode.ingest_verify_receipt)
    assert "_verify_receipts" in src


def test_frozen_sha_recorded():
    assert len(FROZEN_SHA) == 40
