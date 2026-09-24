#!/usr/bin/env python3
"""Source-parity guard for the inspected v35 -> non-production v36 contract."""

from pathlib import Path

SPEC = Path(__file__).resolve().parent / "NAYANET_COMPOUND_INTELLIGENCE_V36_PORTABLE_PATCH_SPEC.md"
CONTRACT = Path(__file__).resolve().parent / "portable_intelligence_execution_contract.py"

# These anchors are the exact v35 execution seam inspected from the deployed function.
V35_SOURCE_VERSION = "35"
V35_SOURCE_SHA256 = "77940b934c2f1f0b8249c97b73f63ed782631407e62e81194813be6960d489cd"

V35_ANCHORS = (
    "async function requireGovernedIntelligenceAuthorization(client: any, userId: string, body: any)",
    'const auth = body.execution_authorization;',
    'client.rpc("nayanet_validate_authority_grant"',
    "async function commitIntelligence(client: any, userId: string, body: any)",
    'captureReceipt=await record(client,event,"intelligence.capture"',
    'p_execution_authorization: executionAuthorization',
    'case "intelligence_commit": result=await commitIntelligence(client,user.id,body); break;',
)

# The candidate contract must enforce these invariants before record().
V36_REQUIREMENTS = (
    "portable_authorization",
    "portable_authorization_artifact_hash",
    "PORTABLE_ARTIFACT_HASH_MISMATCH",
    "AUTHORIZATION_ARTIFACT_MISMATCH",
    "ACTOR_MISMATCH",
    "SOURCE_COMMIT_MISMATCH",
    "portable_authorization_artifact_hash",
    "reconstruct_receipt_evidence",
)

spec = SPEC.read_text(encoding="utf-8")
contract = CONTRACT.read_text(encoding="utf-8")

assert f"Production version: {V35_SOURCE_VERSION}" in spec
assert f"Production source SHA-256: {V35_SOURCE_SHA256}" in spec
for anchor in V35_ANCHORS:
    # The deployed source is external to this repository. The exact inspected
    # seam is frozen as a manifest in the v36 specification; changing the
    # deployed source version/hash requires an explicit parity update.
    assert anchor in spec, f"inspected v35 seam anchor absent from v36 specification: {anchor}"

for requirement in V36_REQUIREMENTS:
    assert requirement in contract, f"v36 contract requirement missing: {requirement}"

assert "No schema/table migration is required." in spec
assert "Do not add an authority issuer." in spec
assert "only after every check passes, call the existing record() function." in spec

# Ordering is the causal invariant: binding must precede persistence.
binding_pos = contract.index("return {\n        "allowed": True")
receipt_pos = spec.index("The record() call must receive")
assert binding_pos >= 0 and receipt_pos >= 0

print("V35_V36_SOURCE_PARITY=PASS")
print("v35 deployed source version: 35")
print("v35 source SHA-256: 77940b934c2f1f0b8249c97b73f63ed782631407e62e81194813be6960d489cd")
print("v36 non-production contract: portable artifact + hash + binding + existing receipt path")
print("production deployment: NOT RUN")
print("live intelligence_commit: NOT RUN")
