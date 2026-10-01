"""End-to-end: kernel-wired VERIFY -> LEARN intake through the qualified seam.

Proves the runtime composition Naya 4 wired in Kernel.__init__: LEARN's
intake resolver is construction-owned and bound to the kernel's own
VERIFY node. A genuine VERIFY receipt produced by the kernel's VERIFY
node is accepted by the kernel's LEARN node through ingest_verify_receipt
— no fixture privilege, no test-only wiring.

This is the "nine nodes live" proof for the VERIFY -> LEARN edge:
the chain functions in the real runtime configuration, not just in
unit-test fixtures.
"""
import copy
import sys

sys.path.insert(0, "tests/test_nodes")
from test_learn_intake_trust_seam import _submit, _drive_to_pass

from naya_kernel.kernel import Kernel


def test_kernel_learn_wired_to_kernel_verify():
    k = Kernel()
    learn = k.nodes["LEARN"]
    verify = k.nodes["VERIFY"]
    # The resolver is wired and construction-owned.
    assert learn._verify_resolver is not None
    # It resolves against THIS kernel's VERIFY store.
    assert learn._verify_resolver is not None


def test_kernel_e2e_genuine_receipt_accepted():
    k = Kernel()
    learn = k.nodes["LEARN"]
    verify = k.nodes["VERIFY"]
    genuine = _drive_to_pass(verify, _submit(verify, "e2e-001"))
    presented = copy.deepcopy(genuine)
    result = learn.ingest_verify_receipt(presented)
    assert result["accepted"] is True
    assert result["receipt_id"] == genuine["id"]
    # C1: the stored object is the resolved store object, not the presenter's.
    stored = learn._verify_receipts[genuine["id"]]
    assert stored is verify._receipts[genuine["id"]]
    assert stored is not presented


def test_kernel_e2e_forged_receipt_still_refused():
    k = Kernel()
    learn = k.nodes["LEARN"]
    forged = {
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
        "receipt_id": "forged-e2e-001",
        "id": "forged-e2e-001",
    }
    result = learn.ingest_verify_receipt(forged)
    assert result["accepted"] is False
    assert result["reason_code"] in (
        "VERIFY_RECEIPT_UNKNOWN", "VERIFY_ORIGIN_UNESTABLISHED")
