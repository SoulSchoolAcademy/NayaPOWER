#!/usr/bin/env python3
"""Demo-1 ACT run: perform the first real bounded effect.

Wires the REAL staging.write_file executor behind ActNode's seam,
projects the tool entry from the CANONICAL Smart Door registry (no
parallel registry), executes one LAW-shaped decision, writes the
artifact, and persists the execution receipt as JSON.

Stated boundary: the ACT-verb decision receipt is built with the
suite's make_decision_receipt helper carrying authority_basis
director_order — the receipt shape the LAW runtime mints. Full
LAW-side minting inside the Python kernel is a named follow-up gap.

The receipt JSON persisted here is a LOCAL stand-in for the durable
seam (nayanet_execution_receipts via the persistence adapter), not the
seam itself.

Usage:
    python3 scripts/demo1/act_run.py [--root DIR]

Default root: ~/workspace/demo-staging
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from naya_kernel import smart_door
from naya_kernel.nodes import act_node

NOTE_CONTENT = """# Smart Note candidate — Demo-1 first governed effect (CANDIDATE — NOT RATIFIED)

Date: 2026-10-01
Source: Demo-1 P1 acceptance run, Naya 4 lane

## What happened
The first real bounded operation ran behind ACT's executor seam:
`staging.write_file` wrote this file to `demo-staging/`.

## Why it matters
Before this run, ACT's acceptance path used an echo/test executor — the
seam existed but no real operation stood behind it. Now:

- the capability is declared in the canonical Smart Door registry
  (DOOR-LOCAL-STAGING, status REGISTERED_DEMO — not production-live);
- the kernel projects that declaration into ACT's admission; no parallel
  registry was created;
- the executor enforces its bounds before any filesystem mutation
  (sandboxed path, name pattern, 64 KiB max, never overwrites);
- replay cannot produce a second effect (idempotency key + content hash);
- the execution receipt binds the artifact's sha256, so VERIFY can
  independently re-read and confirm what happened.

## Status
CANDIDATE. Auto-capture is not auto-ratification — only Shawn ratifies.
"""

FILENAME = "sn-candidate-demo1-first-effect-2026-10-01.md"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path.home() / "workspace"),
                    help="sandbox root; the executor writes under <root>/demo-staging/")
    args = ap.parse_args()
    root = Path(args.root)

    # 1. Capability declaration comes from the canonical registry.
    registry = smart_door.staging_tool_registry()
    entry = registry["staging.write_file"]
    print("door: DOOR-LOCAL-STAGING | status:", entry["registry_status"])
    print("tool: staging.write_file | class:", entry["authority_class"])

    # 2. LAW-shaped decision receipt (boundary stated in module docstring).
    receipt = act_node.make_decision_receipt(
        receipt_id="dec-demo1-live-001",
        issued_at="2026-10-01T15:55:00+00:00",
        valid_until="2026-10-02T00:00:00+00:00",
        winner={"tool_id": "staging.write_file", "version": "1.0",
                "params": {"filename": FILENAME, "content": NOTE_CONTENT}},
        authority_basis={"kind": "director_order", "ref": "order-demo-1",
                         "revoked": False},
    )

    # 3. ACT executes with the REAL bounded executor.
    node = act_node.ActNode(
        executor=smart_door.make_staging_executor(str(root)))
    state = {
        "decision_receipt": receipt,
        "tool_registry": registry,
        "execution_ledger": {},
        "now": "2026-10-01T15:55:00+00:00",
    }
    handoff = node.execute(state)
    print("path:", handoff["path"])
    print("execution_id:", handoff["execution_id"])
    print("effects_observed:", handoff["receipt"].get("effects_observed"))

    if handoff["path"] != "EXECUTED":
        print("REFUSED — no effect performed. reasons:",
              handoff["receipt"].get("error_class"),
              handoff["receipt"].get("outcome"))
        return 1

    # 4. Persist the execution receipt (local stand-in for the durable seam).
    receipts_dir = root / "demo-staging" / "receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipts_dir / (handoff["execution_id"] + ".json")
    receipt_path.write_text(
        json.dumps(handoff["receipt"], indent=2, sort_keys=True),
        encoding="utf-8")

    artifact = root / "demo-staging" / FILENAME
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    print("artifact:", artifact)
    print("artifact sha256:", digest)
    print("receipt:", receipt_path)
    print()
    print("Next: run scripts/demo1/fresh_verify.py", receipt_path,
          "in a fresh process.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
