import json
import sys

EXPECTED_NAYA = "NAYA-NODE-0001"
EXPECTED_OWNER = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f"
EXPECTED_BLOCK = "IB-NAYA-NODE-0001-0001"
EXPECTED_BEHAVIOR = "PRESERVE_PROVENANCE_BEFORE_APPLY"

def verify(receipt: dict) -> None:
    assert receipt["receipt_type"] == "NAYA-COLD-RUNTIME-RECEIPT-V1"
    assert receipt["naya_id"] == EXPECTED_NAYA
    assert receipt["owner_id"] == EXPECTED_OWNER
    assert receipt["block_id"] == EXPECTED_BLOCK
    assert receipt["block_owner_id"] == EXPECTED_OWNER
    assert receipt["behavior"] == EXPECTED_BEHAVIOR
    assert receipt["runtime_identity"] == "github-actions-oidc"
    assert receipt["retained_lesson"] == "Preserve provenance before applying retained intelligence; retrieval never grants authority."

def main() -> None:
    first = json.loads(open(sys.argv[1], encoding="utf-8").read())["receipt"]
    second = json.loads(open(sys.argv[2], encoding="utf-8").read())["receipt"]
    verify(first); verify(second)
    assert first["naya_id"] == second["naya_id"] == EXPECTED_NAYA
    assert first["owner_id"] == second["owner_id"] == EXPECTED_OWNER
    assert first["block_id"] == second["block_id"] == EXPECTED_BLOCK
    if first.get("token_jti") and second.get("token_jti"):
        assert first["token_jti"] != second["token_jti"]
    print("INDEPENDENT_COLD_RECEIPT_VERIFY=PASS")
    print(f"NAYA={EXPECTED_NAYA} OWNER={EXPECTED_OWNER} BLOCK={EXPECTED_BLOCK} BEHAVIOR={EXPECTED_BEHAVIOR}")

if __name__ == "__main__":
    main()
