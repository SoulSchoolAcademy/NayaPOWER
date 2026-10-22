"""Trust-boundary tests for kernel/protocol/read_receipt.py (B-40, wave 33).

Polarity these tests pin, proven by adversarial probe on live tip bytes:
- The receipt seal is an UNKEYED SHA-256 integrity seal, NOT a signature.
- Forgery axis: a forged receipt with a valid recomputed hash verifies
  identically to a genuine one. verify() == True NEVER means "issued by a
  trusted party" — it means "fields unaltered since sealing + passed flag".
- Integrity axis: tampering with ANY sealed field after sealing breaks the
  seal and verify() refuses.

The forged-verifies assertions below are documentation of the honest
boundary, not approval of forgery: they exist so no future change can
silently re-introduce authentication claims ("signed attestation") without
failing loudly. Real authentication needs a keyed signature (HMAC) or
server-side issuance — tracked as a KNOWN WEAKNESS in
.github/workflows/protocol-gates.yml. Same lesson class as SN-0362
(unkeyed seal != authentication), different seam.
"""
from __future__ import annotations

import pytest

from kernel.protocol.read_receipt import (
    AUTHORITY_QUESTIONS,
    PROTOCOL_VERSION,
    ReadReceipt,
    grade_answer,
    issue_receipt,
)


def _correct_answers() -> dict:
    out = {}
    for q in AUTHORITY_QUESTIONS:
        if "acceptable" in q:
            out[q["id"]] = q["acceptable"][0]
        else:
            out[q["id"]] = " ".join(q["acceptable_keywords"][: q.get("min_keywords", 1)])
    return out


def test_genuine_receipt_verifies():
    """Genuine path: correct answers -> graded passed -> seal -> verify."""
    receipt = issue_receipt("Naya Electrician", _correct_answers())
    assert receipt.passed is True
    assert receipt.verify() is True


def test_failed_grading_does_not_verify():
    """Honest grading refuses wrong answers; the failed receipt does not verify."""
    receipt = issue_receipt("Cheater", {q["id"]: "wrong" for q in AUTHORITY_QUESTIONS})
    assert receipt.passed is False
    assert receipt.verify() is False


def test_field_tampering_breaks_integrity_seal():
    """Integrity axis: any post-seal field change must be REFUSED."""
    receipt = issue_receipt("Naya Electrician", _correct_answers())
    assert receipt.verify() is True
    for mutate in (
        lambda r: setattr(r, "agent_id", "Impostor"),
        lambda r: setattr(r, "protocol_version", "1999-FAKE"),
        lambda r: setattr(r, "issued_at", 1.0),
    ):
        tampered = issue_receipt("Naya Electrician", _correct_answers())
        mutate(tampered)
        assert tampered.verify() is False, "tampered field must break the seal"


def test_forged_receipt_with_valid_recomputed_hash_verifies():
    """Forgery axis (B-40 adversarial polarity): the seal is integrity-only.

    An attacker who never answers a single question can construct the
    dataclass directly, set passed=True, recompute the hash, and verify()
    returns True — IDENTICAL standing to a genuine receipt. This assertion
    pins that polarity: the seal authenticates nothing and no one.
    """
    forged = ReadReceipt(
        agent_id="Naya Electrician",
        protocol_version=PROTOCOL_VERSION,
        answers={q["id"]: False for q in AUTHORITY_QUESTIONS},  # never graded
        passed=True,
        issued_at=1729000000.0,
    ).seal()
    assert forged.verify() is True  # integrity-only: forgery is undetectable


def test_flipped_passed_with_recomputed_hash_verifies():
    """A failed receipt with passed flipped and hash recomputed also verifies.

    Same polarity as the forgery axis: the passed flag is self-asserted,
    the hash binds it, and nothing binds the issuer.
    """
    receipt = issue_receipt("Cheater", {q["id"]: "wrong" for q in AUTHORITY_QUESTIONS})
    assert receipt.verify() is False
    receipt.passed = True
    receipt.seal()
    assert receipt.verify() is True


def test_impostor_identity_forges_valid_receipt():
    """The seal carries no issuer identity: any agent_id forges cleanly."""
    forged = ReadReceipt(
        agent_id="Totally-Not-An-Agent",
        protocol_version=PROTOCOL_VERSION,
        answers={},
        passed=True,
        issued_at=1729000000.0,
    ).seal()
    assert forged.verify() is True


def test_seal_is_not_named_sign():
    """The API no longer carries the authentication-flavored name 'sign'.

    B-40 description correction: 'sign' implies an unforgeable signature
    bound to an identity/key, which this mechanism cannot provide. The
    honest verb is 'seal' (tamper-evident, unkeyed).
    """
    assert not hasattr(ReadReceipt, "sign"), "sign() must not exist on ReadReceipt"
    assert callable(getattr(ReadReceipt, "seal"))


def test_verify_is_integrity_not_authorship():
    """verify() checks seal equality and the passed flag — nothing else.

    Two receipts with identical fields but different issuance histories
    (one graded, one forged) verify identically. The mechanism cannot
    distinguish them; no caller may treat it as authorship proof.
    """
    answers = _correct_answers()
    graded = issue_receipt("Naya Electrician", answers)
    forged = ReadReceipt(
        agent_id="Naya Electrician",
        protocol_version=PROTOCOL_VERSION,
        answers={q["id"]: True for q in AUTHORITY_QUESTIONS},
        passed=True,
        issued_at=graded.issued_at,
    ).seal()
    assert graded.verify() is True
    assert forged.verify() is True
    assert graded.receipt_hash == forged.receipt_hash  # indistinguishable by seal
