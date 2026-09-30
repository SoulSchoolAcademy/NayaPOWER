import json
import sys
from pathlib import Path


REQUIRED_RECEIPT_FIELDS = (
    "receipt_type", "naya_id", "block_id", "block_owner_match", "authorization_binding",
    "connect", "behavior", "authority_boundary", "production_mutation_performed",
    "rls_changed", "credentials_committed",
)
REQUIRED_CONNECT_FIELDS = ("connected", "relationship_count")
REQUIRED_BEHAVIOR_FIELDS = ("consequential", "allowed", "executed", "blocked_by")
REQUIRED_AUTHORITY_BOUNDARY_FIELDS = ("connect_grants_authority", "consequential_actions_authorized")

# Checked on the RESPONSE DOCUMENT, not inside the receipt: the deployed bundle
# cannot be inspected from outside, so the only way to know which canonical commit
# is serving traffic is for the runtime to report it. Without this, a source change
# that was never deployed is undetectable.
REQUIRED_DOCUMENT_FIELDS = ("deployed_source_revision",)
UNSTAMPED = "UNSTAMPED"

# NOTE: this module is the single source of truth for the CONNECT receipt contract.
# BRAIN/12-ENGINEERING/verify-deployed-runtime-parity.py imports the tuples above so
# that source/runtime parity is checked against the SAME contract that verifies the
# receipt. A detector with its own hand-copied field list would itself drift.


def _require(container: object, key: str, where: str):
    if not isinstance(container, dict) or key not in container:
        raise SystemExit(
            f"CONNECT_RECEIPT_CONTRACT_DRIFT: required field {where}.{key} is absent. "
            "The runtime did not emit the evidence this verifier requires. "
            "This is an implementation/contract mismatch, NOT an infrastructure failure."
        )
    return container[key]


def verify(path: Path) -> None:
    document = json.loads(path.read_text(encoding="utf-8"))
    for field in REQUIRED_DOCUMENT_FIELDS:
        _require(document, field, "document")
    # An UNSTAMPED marker is not a pass. The deployed bundle cannot be inspected
    # from outside, so a receipt that cannot name its source revision is
    # untraceable - and an untraceable receipt must never be certified as
    # conformant, because that is precisely how an undeployed change hides.
    if document["deployed_source_revision"] == UNSTAMPED:
        raise SystemExit(
            "CONNECT_RECEIPT_UNTRACEABLE: deployed_source_revision is UNSTAMPED. The runtime cannot "
            "declare which canonical commit is serving traffic, so this receipt cannot be tied to any "
            "source. Whoever deploys must set DEPLOYED_SOURCE_REVISION to the commit actually "
            "deployed and redeploy. This is an absence of evidence, not a pass."
        )
    receipt = document["receipt"]
    for field in REQUIRED_RECEIPT_FIELDS:
        _require(receipt, field, "receipt")
    behavior = receipt["behavior"]
    for field in REQUIRED_CONNECT_FIELDS:
        _require(receipt["connect"], field, "receipt.connect")
    for field in REQUIRED_BEHAVIOR_FIELDS:
        _require(behavior, field, "receipt.behavior")
    for field in REQUIRED_AUTHORITY_BOUNDARY_FIELDS:
        _require(receipt["authority_boundary"], field, "receipt.authority_boundary")
    assert receipt["receipt_type"] == "NAYA-LIVE-CONNECT-RUNTIME-RECEIPT-V1"
    assert receipt["naya_id"] == "NAYA-NODE-0001"
    assert receipt["block_id"] == "IB-NAYA-NODE-0001-0001"
    assert receipt["block_owner_match"] is True
    assert receipt["authorization_binding"]["status"] == "ACTIVE"
    assert receipt["authorization_binding"]["scope"]["target"] == "NAYA-NODE-0001"
    assert "naya_node_apply" in receipt["authorization_binding"]["actions"]
    assert receipt["connect"]["connected"] is True
    assert receipt["connect"]["relationship_count"] >= 1
    assert receipt["behavior"]["consequential"] is True
    assert receipt["behavior"]["allowed"] is False
    assert receipt["behavior"]["executed"] is False
    assert receipt["behavior"]["blocked_by"] == "LAW"
    assert receipt["authority_boundary"]["connect_grants_authority"] is False
    assert receipt["production_mutation_performed"] is False
    assert receipt["rls_changed"] is False
    assert receipt["credentials_committed"] is False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_connect_runtime_receipt.py RECEIPT")
    verify(Path(sys.argv[1]))
    print("CONNECT runtime receipt independently VERIFIED")
