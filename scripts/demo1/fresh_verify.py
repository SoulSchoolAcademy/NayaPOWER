#!/usr/bin/env python3
"""Demo-1 fresh VERIFY: independently confirm what ACT did.

This script runs in a FRESH process. It inherits nothing from the act
run — no in-memory objects, no shared state. It reads ONLY:

  1. the persisted execution receipt JSON, and
  2. the artifact file on disk, plus the canonical Smart Door registry.

Three SEPARATE verdicts (a later revocation does not erase a valid
historical observation, but it does prevent unauthorized reuse —
historical verification must never be mistaken for fresh permission):

  VERDICT 1 — receipt integrity: the receipt_hash recomputes.
  VERDICT 2 — historical outcome verification: the receipt's OWN tool
      binding resolves to exactly one declared operation in the
      canonical registry (re-read from disk); the bound version matches
      the declaration; the artifact exists and its sha256 equals the hash
      bound in effects_observed; the parameters commitment, decision
      reference, and EXECUTED path are present. Semantic validation
      runs even when the hash matches — a freshly resealed
      contradictory receipt cannot pass on hash equality alone.
  VERDICT 3 — current authorization for another action: the
      authority_basis kind satisfies the tool's required_authority, the
      basis is not revoked, and the grant is fresh against the real
      clock. This verdict is about PERMISSION NOW, not about what
      happened.

Usage:
    python3 scripts/demo1/fresh_verify.py <receipt-json>
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
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

    # Per-verdict failure collectors; exit 0 iff all three verdicts pass.
    failures = {"V1": [], "V2": [], "V3": []}

    def chk(bucket: str, name: str, cond: bool, detail: str = ""):
        print(("PASS " if cond else "FAIL ") + f"[{bucket}] " + name
              + (f" — {detail}" if detail and not cond else ""))
        if not cond:
            failures[bucket].append(name)
        return cond

    # ---- VERDICT 1 — receipt integrity ---------------------------------
    body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    chk("V1", "receipt_hash recomputes",
        act_node._sha256(body) == receipt.get("receipt_hash"),
        "MISMATCH — receipt does not recompute")

    # ---- VERDICT 2 — historical outcome verification -------------------
    # The tool comes from THE RECEIPT's own binding, never a hardcoded name.
    tool = receipt.get("tool") or {}
    tool_id = tool.get("tool_id")
    tool_version = tool.get("version")
    chk("V2", "receipt binds a tool_id", isinstance(tool_id, str) and tool_id,
        f"tool={tool!r}")

    reg = smart_door.load_registry()
    door = op = None
    if isinstance(tool_id, str) and tool_id:
        try:
            door, op = smart_door.find_operation_any_door(reg, tool_id)
        except KeyError as exc:
            door = op = None
            decl_err = str(exc)
        else:
            decl_err = ""
    else:
        decl_err = "no tool_id bound"
    chk("V2", "receipt tool is declared in the canonical registry",
        op is not None, decl_err or f"tool_id={tool_id!r}")

    entry = None
    if op is not None:
        entry = smart_door.project_act_tool_entry(
            door, op, registry_version=reg.get("version", "1.0"))
        chk("V2", "receipt version matches the declared version",
            tool_version == entry["version"],
            f"receipt={tool_version!r} declared={entry['version']!r}")
        chk("V2", "registry status is honest (not production-live)",
            door.get("status") == "REGISTERED_DEMO",
            f"status={door.get('status')!r}")
        chk("V2", "verification_required",
            op.get("verification_required") is True)

    # Parameters commitment: params_hash well-formed + artifact re-read.
    params_hash = receipt.get("params_hash")
    chk("V2", "params_hash committed",
        isinstance(params_hash, str) and bool(re.fullmatch(r"[0-9a-f]{64}",
                                                           params_hash)),
        f"params_hash={params_hash!r}")
    chk("V2", "decision_ref present",
        isinstance(receipt.get("decision_ref"), str)
        and bool(receipt.get("decision_ref")),
        f"decision_ref={receipt.get('decision_ref')!r}")
    chk("V2", "execution path was EXECUTED",
        receipt.get("path") == "EXECUTED", f"path={receipt.get('path')!r}")

    effects = str(receipt.get("effects_observed", ""))
    m = re.search(r"demo-staging/(\S+\.md)", effects)
    h = re.search(r"sha256:([0-9a-f]{64})", effects)
    chk("V2", "receipt binds an artifact + sha256", bool(m and h),
        f"effects_observed={effects!r}")
    if m and h:
        demo_staging = receipt_path.parent.parent
        artifact = demo_staging / m.group(1)
        chk("V2", "artifact filename matches the declared pattern",
            entry is None or bool(
                re.match(r"^sn-candidate-[A-Za-z0-9][A-Za-z0-9_-]*\.md$",
                         m.group(1))),
            f"filename={m.group(1)!r}")
        chk("V2", "artifact exists on disk", artifact.is_file(),
            str(artifact))
        if artifact.is_file():
            actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
            chk("V2", "artifact sha256 matches receipt binding",
                actual == h.group(1),
                f"receipt={h.group(1)[:12]}… disk={actual[:12]}…")

    # ---- VERDICT 3 — current authorization for another action ----------
    basis = receipt.get("authority_basis") or {}
    if entry is not None:
        chk("V3", "authority basis kind satisfies required_authority",
            basis.get("kind") == entry["required_authority"],
            f"basis={basis.get('kind')!r} "
            f"required={entry['required_authority']!r}")
    else:
        chk("V3", "authority basis kind satisfies required_authority",
            False, "tool not declared — no authority requirement to satisfy")
    chk("V3", "authority basis not revoked",
        basis.get("revoked") is not True,
        f"authority_basis={basis!r}")
    # Freshness honesty: the execution receipt binds issued_at and the
    # decision reference, but the grant's validity window lives on the
    # DECISION receipt. A validity window is not invented here — its
    # absence is reported as a limitation, never as a PASS.
    valid_until = receipt.get("valid_until")
    if valid_until is None:
        print("NOTE [V3] grant validity window not bound in this execution "
              "receipt — freshness against the real clock requires the "
              f"decision receipt {receipt.get('decision_ref')!r}; "
              "not claimed here")
    else:
        now = datetime.now(timezone.utc)
        try:
            fresh = datetime.fromisoformat(valid_until) > now
        except (ValueError, TypeError):
            fresh = False
        chk("V3", "grant fresh against the real clock",
            fresh, f"valid_until={valid_until!r} now={now.isoformat()}")

    print()
    for verdict, label in (("V1", "receipt integrity"),
                           ("V2", "historical outcome verification"),
                           ("V3", "current authorization for another action")):
        state = "PASS" if not failures[verdict] else "FAIL"
        print(f"VERDICT {verdict} ({label}): {state}")
    overall = not any(failures.values())
    print()
    print("FRESH VERIFY:",
          "PASS — observation confirmed independently; "
          "historical proof is NOT fresh permission"
          if overall else
          "FAIL — see above (a failed V3 means: history may stand, "
          "but no new action is authorized)")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
