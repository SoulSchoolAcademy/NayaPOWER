"""Contract 00 / North Star Section 20 - Contract -> Node -> Enforcement.

This gate makes `contracts/intelligent-block-v1.schema.json` machine-enforceable
instead of merely declared. It exists because the schema shipped for ~6 days as
INVALID JSON: 35 structural "\\n" sequences were written as literal backslash-n
inside three definition blocks, so no validator could ever load it. Nothing in
CI detected this, so "the contract is validated" was DOCUMENTED, not TRUE.

Rules enforced:
  G1  the schema file must parse as JSON
  G2  the schema must itself be a valid Draft 2020-12 schema
  G3  identity must permit every field live production actually attaches
  G4  the canonical production object shape must validate

Truth states are never collapsed: a passing structural check is IMPLEMENTED +
TESTED. It is not PRODUCTION-PROVEN unless a live block is validated by a
runtime path. See North Star Section 33.
"""

import json
import pathlib
import sys

from jsonschema import Draft202012Validator

REPO = pathlib.Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "contracts" / "intelligent-block-v1.schema.json"

# Fields the live receiver attaches to identity. Sourced from
# supabase/functions/v7-smart-note-canonical/index.ts (reads
# data.intelligent_block.identity.intelligent_block_id) and proven by
# live-canonical-ib-deeplink-proof.json db_provenance.intelligent_block_id.
PRODUCTION_IDENTITY_FIELDS = ["intelligent_block_id"]

results = []


def check(rule, description, passed, detail=""):
    results.append((rule, description, passed, detail))
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {rule}  {description}")
    if detail:
        print(f"         {detail}")
    return passed


# G1 --------------------------------------------------------------------
raw = SCHEMA_PATH.read_text(encoding="utf-8")
try:
    schema = json.loads(raw)
    check("G1", "schema file parses as JSON", True, f"{len(raw)} bytes")
except json.JSONDecodeError as exc:
    check("G1", "schema file parses as JSON", False, f"{exc}")
    print("\nGATE: BLOCKED. The canonical contract is not machine-readable.")
    sys.exit(1)

# G2 --------------------------------------------------------------------
try:
    Draft202012Validator.check_schema(schema)
    check("G2", "schema is a valid Draft 2020-12 schema", True)
except Exception as exc:  # noqa: BLE001
    check("G2", "schema is a valid Draft 2020-12 schema", False, str(exc)[:200])
    sys.exit(1)

# G3 --------------------------------------------------------------------
identity = schema["properties"]["identity"]
defined = set(identity.get("properties", {}))
missing = [f for f in PRODUCTION_IDENTITY_FIELDS if f not in defined]
check(
    "G3",
    "identity permits every field live production attaches",
    not missing,
    f"missing from schema: {missing}" if missing else "all production identity fields declared",
)

# G4 --------------------------------------------------------------------
production_identity = {
    "object_id": "event:probe",
    "event_id": "probe",
    "version": 1,
    "namespace": "nayanet",
    "schema_version": "NAYANET_INTELLIGENT_BLOCK_V1",
    **{f: "IB-000000" for f in PRODUCTION_IDENTITY_FIELDS},
}
probe = {"identity": production_identity, "type": {"object_type": "probe", "event_type": "probe"}}
errors = [e for e in Draft202012Validator(schema).iter_errors(probe) if e.validator == "additionalProperties"]
check(
    "G4",
    "canonical production identity shape validates",
    not errors,
    errors[0].message[:200] if errors else "accepted",
)

# REPORT ---------------------------------------------------------------
failed = [r for r in results if not r[2]]
print()
print(f"{len(results) - len(failed)}/{len(results)} gates passed")
print("truth_state: IMPLEMENTED+TESTED (contract-parity). NOT production-proven.")
if failed:
    print("CONTRACT/PRODUCTION CONFLICT - see Contract 00 Section 17.")
    sys.exit(1)
print("CONTRACT/PRODUCTION PARITY: PASS")
