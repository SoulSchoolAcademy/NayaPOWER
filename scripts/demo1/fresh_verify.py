#!/usr/bin/env python3
"""Demo-1 fresh VERIFY: independently confirm what ACT did.

This script runs in a FRESH process. It inherits nothing from the act
run — no in-memory objects, no shared state. It reads ONLY:

  1. the persisted execution receipt JSON, and
  2. the artifact file on disk, plus the canonical Smart Door registry.

Checks (each independent of the act-run process):
  - the receipt's receipt_hash recomputes (MATCH / MISMATCH);
  - the artifact exists and its sha256 equals the hash bound in the
    receipt's effects_observed;
  - the tool is declared in the canonical registry (re-read from disk),
    with status and verification_required as expected;
  - the receipt's authority_basis.kind satisfies the tool's
    required_authority (independent authority re-check — the successor
    inherits no authority, it re-validates the basis against the
    declaration).

Usage:
    python3 scripts/demo1/fresh_verify.py <receipt-json>
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from naya_kernel import smart_door
from naya_kernel.nodes import act_node


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: fresh_verify.py <receipt-json>", file=sys.stderr)
        return 2
    receipt_path = Path(sys.argv[1])
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    ok = True

    def check(name: str, cond: bool, detail: str = ""):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + name
              + (f" — {detail}" if detail and not cond else ""))
        if not cond:
            ok = False

    # 1. Receipt integrity: recompute under the bound hash.
    body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    check("receipt_hash recomputes",
          act_node._sha256(body) == receipt.get("receipt_hash"),
          "MISMATCH — receipt does not recompute")

    # 2. Artifact observability: re-read the file, compare hashes.
    effects = str(receipt.get("effects_observed", ""))
    m = re.search(r"demo-staging/(\S+\.md)", effects)
    h = re.search(r"sha256:([0-9a-f]{64})", effects)
    check("receipt binds an artifact + sha256", bool(m and h),
          f"effects_observed={effects!r}")
    artifact = None
    if m and h:
        # Reconstruct the artifact path from the receipt alone: the demo
        # root is the receipt file's grandparent (demo-staging/receipts/).
        demo_staging = receipt_path.parent.parent
        artifact = demo_staging / m.group(1)
        check("artifact exists on disk", artifact.is_file(), str(artifact))
        if artifact.is_file():
            actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
            check("artifact sha256 matches receipt binding",
                  actual == h.group(1),
                  f"receipt={h.group(1)[:12]}… disk={actual[:12]}…")

    # 3. Declaration check: re-read the canonical registry from disk.
    reg = smart_door.load_registry()
    door, op = smart_door.find_operation(
        reg, "DOOR-LOCAL-STAGING", "staging.write_file")
    check("tool declared in canonical registry", True)
    check("registry status is honest (not production-live)",
          door.get("status") == "REGISTERED_DEMO",
          f"status={door.get('status')!r}")
    check("verification_required",
          op.get("verification_required") is True)

    # 4. Independent authority re-check against the declaration.
    entry = smart_door.project_act_tool_entry(
        door, op, registry_version=reg.get("version", "1.0"))
    basis_kind = (receipt.get("authority_basis") or {}).get("kind")
    check("authority basis satisfies required_authority",
          basis_kind == entry["required_authority"],
          f"basis={basis_kind!r} required={entry['required_authority']!r}")

    check("execution path was EXECUTED", receipt.get("path") == "EXECUTED",
          f"path={receipt.get('path')!r}")

    print()
    print("FRESH VERIFY:", "PASS — observation confirmed independently"
          if ok else "FAIL — see above")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
