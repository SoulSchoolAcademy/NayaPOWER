import json
import sys
from pathlib import Path


def verify(path: Path) -> None:
    receipt = json.loads(path.read_text(encoding="utf-8"))["receipt"]
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
