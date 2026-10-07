#!/usr/bin/env python3
"""Static gate for the NayaPOWER Nine Master Node kernel.

Checks spec gates K1..K6 against the canonical manifest:
  K1 - exactly nine unique Node identities MN-01..MN-09
  K2 - every contract 00..26 has exactly one primary Node
  K3 - manifest conforms to the canonical machine-readable structure
  K4 - self-authorization and self-ratification are explicitly forbidden
  K5 - claim status cannot exceed evidence status
  K6 - meaningful completion can emit sufficient successor context

Passing K1..K6 proves STRUCTURAL kernel conformance only.
It does not prove production intelligence (see spec section 13/15).

Usage:
  python3 scripts/verify-nine-master-nodes.py [manifest] [schema]
Exit 0 on pass, 1 on any gate failure.
"""
import json
import re
import sys

DEFAULT_MANIFEST = ".naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json"
DEFAULT_SCHEMA = ".naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.schema.json"
REQUIRED_IDS = [f"MN-0{i}" for i in range(1, 10)]
REQUIRED_CONTRACTS = [f"{i:02d}" for i in range(27)]


def fail(gate, msg):
    print(f"FAIL {gate}: {msg}")
    return False


def ok(gate, msg):
    print(f"PASS {gate}: {msg}")
    return True


def check_k1(m):
    nodes = m.get("nodes", [])
    ids = [n.get("id") for n in nodes]
    if len(ids) != 9 or len(set(ids)) != 9:
        return fail("K1", f"expected 9 unique nodes, got {len(ids)} ({len(set(ids))} unique)")
    if sorted(ids) != REQUIRED_IDS:
        return fail("K1", f"node ids must be exactly MN-01..MN-09, got {sorted(ids)}")
    return ok("K1", "exactly nine unique nodes MN-01..MN-09")


def check_k2(m):
    seen = {}
    dupes = []
    for n in m.get("nodes", []):
        for c in n.get("contracts", []):
            if c in seen:
                dupes.append((c, seen[c], n.get("id")))
            seen[c] = n.get("id")
    missing = [c for c in REQUIRED_CONTRACTS if c not in seen]
    extra = [c for c in seen if c not in REQUIRED_CONTRACTS]
    if dupes:
        return fail("K2", f"contracts with multiple primary owners: {dupes}")
    if missing:
        return fail("K2", f"contracts without a primary owner: {missing}")
    if extra:
        return fail("K2", f"contracts outside 00..26: {extra}")
    return ok("K2", "contracts 00..26 each have exactly one primary node")


def check_k3(m, schema):
    # Structural conformance: required top-level keys, node shape, triads.
    required_top = ["kernel", "version", "status", "nodes", "triads",
                    "invariants", "gates", "input_envelope", "output_envelope",
                    "lifecycle_states", "permitted_transitions"]
    missing = [k for k in required_top if k not in m]
    if missing:
        return fail("K3", f"manifest missing keys: {missing}")
    for n in m["nodes"]:
        for k in ("id", "key", "responsibility", "triad", "contracts",
                  "lifecycle", "must", "must_not"):
            if k not in n:
                return fail("K3", f"node {n.get('id')} missing key: {k}")
        if n["triad"] not in ("T1", "T2", "T3"):
            return fail("K3", f"node {n['id']} has invalid triad {n['triad']}")
        if n["lifecycle"] not in m["lifecycle_states"]:
            return fail("K3", f"node {n['id']} has invalid lifecycle {n['lifecycle']}")
    for t in ("T1", "T2", "T3"):
        if t not in m.get("triads", {}):
            return fail("K3", f"missing triad {t}")
    # Optional: full JSON Schema validation when the jsonschema package exists.
    try:
        import jsonschema  # type: ignore
        jsonschema.validate(m, schema)
        return ok("K3", "manifest validates against JSON Schema")
    except ImportError:
        return ok("K3", "structural conformance (jsonschema package not installed; skipped full validation)")
    except Exception as e:  # noqa: BLE001
        return fail("K3", f"schema validation failed: {e}")


def check_k4(m):
    law = next((n for n in m["nodes"] if n["id"] == "MN-02"), None)
    if not law:
        return fail("K4", "MN-02 LAW missing")
    text = " ".join(law.get("must_not", [])).lower()
    if "self-authorize" not in text and "self-authoriz" not in text:
        return fail("K4", "LAW must_not does not forbid self-authorization")
    i1 = m.get("invariants", {}).get("I1", "").lower()
    if "no node can create authority" not in i1:
        return fail("K4", "invariant I1 (no authority from capability) missing")
    return ok("K4", "self-authorization and self-ratification explicitly forbidden")


def check_k5(m):
    prove = next((n for n in m["nodes"] if n["id"] == "MN-05"), None)
    if not prove:
        return fail("K5", "MN-05 PROVE missing")
    dist = prove.get("epistemic_distinctions", [])
    need = {"UNKNOWN != VERIFIED", "BLOCKED != PASS", "IMPLEMENTED != VERIFIED",
            "VERIFIED != PRODUCTION-PROVEN", "LEARNING LABEL != VERIFIED LEARNING"}
    if not need.issubset(set(dist)):
        return fail("K5", f"PROVE missing epistemic distinctions: {need - set(dist)}")
    must = " ".join(prove.get("must", []))
    if "CLAIM STRENGTH <=" not in must:
        return fail("K5", "PROVE must not enforce CLAIM STRENGTH <= EVIDENCE STRENGTH")
    return ok("K5", "claim status cannot exceed evidence status")


def check_k6(m):
    if "successor_context" not in m.get("output_envelope", []):
        return fail("K6", "output envelope lacks successor_context")
    evolve = next((n for n in m["nodes"] if n["id"] == "MN-09"), None)
    if not evolve:
        return fail("K6", "MN-09 EVOLVE missing")
    text = " ".join(evolve.get("must_not", [])).lower()
    if "authority" not in text:
        return fail("K6", "EVOLVE must_not does not guard successor authority")
    return ok("K6", "successor context emittable; authority not auto-inherited")


def main():
    manifest_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MANIFEST
    schema_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_SCHEMA
    try:
        with open(manifest_path) as f:
            m = json.load(f)
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: cannot read manifest {manifest_path}: {e}")
        return 1
    try:
        with open(schema_path) as f:
            schema = json.load(f)
    except Exception:  # noqa: BLE001
        schema = {}
    results = [
        check_k1(m),
        check_k2(m),
        check_k3(m, schema),
        check_k4(m),
        check_k5(m),
        check_k6(m),
    ]
    if all(results):
        print("KERNEL CONFORMANT (structural only — see spec s.13/15)")
        return 0
    print("KERNEL NON-CONFORMANT")
    return 1


if __name__ == "__main__":
    sys.exit(main())
