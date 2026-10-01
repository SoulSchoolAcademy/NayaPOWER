#!/usr/bin/env python3
"""Demo-1 ACT run: perform the first real bounded effect.

Wires the REAL staging.write_file executor behind ActNode's seam,
projects the tool entry from the CANONICAL Smart Door registry (no
parallel registry), authorizes via the REAL LawNode.gate() against a
director-transcribed grant (scripts/demo1/demo_grant.json — the
director's written orders encoded, not created), executes, writes the
artifact, and persists the execution receipt as JSON.

Authorization (real, not fixture): law_authorize.authorize() builds the
LAW proposal from the demo intent + grant and runs LawNode.gate(); only
an ADMISSIBLE envelope becomes the decision receipt's authority.
ActNode._admit re-validates the grant (absent/expired/revoked) and the
envelope coverage (action/target/bounds) at invocation time against the
real clock. The receipt JSON persisted here is a LOCAL stand-in for the
durable seam (nayanet_execution_receipts via the persistence adapter),
not the seam itself.

Usage:
    python3 scripts/demo1/act_run.py [--root DIR]

Default root: ~/workspace/demo-staging
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from naya_kernel import smart_door
from naya_kernel.node_base import CALCULUS_V21_VERSION
from naya_kernel.nodes import act_node
from scripts.demo1 import law_authorize

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
    # The executor requires an existing trusted root; the demo
    # explicitly establishes it here rather than implying it.
    root.mkdir(parents=True, exist_ok=True)

    # 1. Capability declaration comes from the canonical registry.
    registry = smart_door.staging_tool_registry()
    entry = registry["staging.write_file"]
    print("door: DOOR-LOCAL-STAGING | status:", entry["registry_status"])
    print("tool: staging.write_file | class:", entry["authority_class"])

    # 2. REAL LAW authorization: proposal -> LawNode.gate() -> envelope.
    # The grant is transcribed from the director's written orders
    # (demo_grant.json provenance); the gate runs on the real clock.
    # Refusal here means: no authority, no execution. Ever.
    now = datetime.now(timezone.utc).isoformat()
    try:
        authz = law_authorize.authorize(FILENAME, NOTE_CONTENT.encode("utf-8"))
    except law_authorize.AuthorizationRefused as e:
        print("LAW REFUSED — no authority, no execution:", e)
        return 1
    print("LAW ADMISSIBLE: gate_receipt=%s" % authz["gate_receipt_id"])
    print("grant:", authz["authority_basis"]["ref"],
          "| constitution:", authz["constitution_hash"][:12])

    # 3. Decision receipt carrying the LAW envelope (not a fixture basis).
    # Real values throughout: calculusVersion is the ratified V2.1
    # (not the test helper's "v2.1-candidate" placeholder); configHash
    # binds the canonical decision inputs and is recomputable by any
    # verifier (not the "cfg-aaa" placeholder).
    config_canonical = json.dumps({
        "tool_id": "staging.write_file",
        "tool_version": "1.0",
        "bounds": entry.get("bounds", {}),
        "grant_ref": authz["grant"]["grant_ref"],
        "authority_basis": authz["authority_basis"],
    }, sort_keys=True)
    config_hash = hashlib.sha256(config_canonical.encode("utf-8")).hexdigest()
    # inputs_hash binds the canonical input state (P3) — the exact bytes
    # the execution will consume. A verifier recomputes it from
    # input_state.json; a mismatch means the receipt and the inputs differ.
    content_sha = hashlib.sha256(NOTE_CONTENT.encode("utf-8")).hexdigest()
    inputs_canonical = json.dumps({
        "filename": FILENAME,
        "content_sha256": content_sha,
        "tool_id": "staging.write_file",
        "params": {"filename": FILENAME, "content": NOTE_CONTENT},
    }, sort_keys=True)
    inputs_hash = hashlib.sha256(inputs_canonical.encode("utf-8")).hexdigest()
    receipt = act_node.make_decision_receipt(
        receipt_id="dec-demo1-live-001",
        issued_at=now,
        valid_until=authz["grant"]["expiry"],
        winner={"tool_id": "staging.write_file", "version": "1.0",
                "params": {"filename": FILENAME, "content": NOTE_CONTENT}},
        authority_basis=authz["authority_basis"],
        law_envelope=authz["envelope"],
        calculusVersion=CALCULUS_V21_VERSION,
        configHash=config_hash,
        configHashCurrent=config_hash,
        inputs_hash=inputs_hash,
    )

    # 4. ACT executes with the REAL bounded executor. The demo requires the
    # LAW envelope: a stripped or absent envelope never falls back to
    # fixture admission on this path. The grant expiry check uses the real
    # clock (no injected clock) — the invocation boundary resolves current
    # authority, not LAW's memory of it.
    node = act_node.ActNode(
        executor=smart_door.make_staging_executor(str(root)),
        require_law_envelope=True)
    state = {
        "decision_receipt": receipt,
        "tool_registry": registry,
        "grants": [authz["grant"]],
        "execution_ledger": {},
        "now": now,
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

    # 4. Persist the full receipt chain (local stand-in for the durable seam).
    # Three files, each content-addressed by its own id: the LAW gate
    # receipt (why ADMISSIBLE), the decision receipt (what was authorized),
    # and the execution receipt (what happened). The frozen evidence
    # package collects all three; the durable seam will carry them onward.
    receipts_dir = root / "demo-staging" / "receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)
    (receipts_dir / ("law-gate-" + authz["gate_receipt_id"] + ".json")).write_text(
        json.dumps(authz["gate_receipt"], indent=2, sort_keys=True),
        encoding="utf-8")
    (receipts_dir / ("decision-" + receipt["receipt_id"] + ".json")).write_text(
        json.dumps(receipt, indent=2, sort_keys=True),
        encoding="utf-8")
    print("law gate receipt:", authz["gate_receipt_id"])
    print("decision receipt:", receipt["receipt_id"])
    # Append-safe, idempotent: the filename IS the content-addressed
    # execution_id, so the first receipt is canonical evidence and a
    # replay never overwrites it. (A replay's receipt carries fresh
    # wall-clock fields, so seal comparison would false-positive; the
    # identity that matters here is the execution_id key itself.)
    receipts_dir = root / "demo-staging" / "receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipts_dir / (handoff["execution_id"] + ".json")
    if receipt_path.exists():
        try:
            prior = json.loads(receipt_path.read_text(encoding="utf-8"))
            same_key = (prior.get("execution_id") == handoff["execution_id"])
        except (OSError, ValueError):
            same_key = False
        if same_key:
            print("receipt already persisted at", receipt_path,
                  "— replay does not overwrite canonical evidence")
        else:
            print("REFUSED to overwrite", receipt_path,
                  "— existing file is not a receipt for",
                  handoff["execution_id"], "; canonical evidence preserved")
            return 1
    else:
        receipt_path.write_text(
            json.dumps(handoff["receipt"], indent=2, sort_keys=True),
            encoding="utf-8")

    artifact = root / "demo-staging" / FILENAME
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    print("artifact:", artifact)
    print("artifact sha256:", digest)
    print("receipt:", receipt_path)

    # 5. Persist the run context for the evidence package: the exact
    # proposal LAW admitted, the input state the decision bound, the
    # grant's provenance (transcribed from the director's orders, read
    # at invocation time), and the registry/constitution references.
    # Each file carries an explicit object_type; the frozen package
    # binds them by sha256 and records their relationships.
    context_files = {
        "proposal.json": {
            "object_type": "law_proposal",
            "proposal": authz["proposal"],
        },
        "input_state.json": {
            "object_type": "input_state",
            "filename": FILENAME,
            "content_sha256": content_sha,
            "tool_id": "staging.write_file",
            "registry_entry_id": "DOOR-LOCAL-STAGING",
            "config_hash": config_hash,
            "config_canonical": config_canonical,
            "inputs_hash": inputs_hash,
            "inputs_canonical": inputs_canonical,
        },
        "grant_provenance.json": {
            "object_type": "grant_provenance",
            "grant_ref": authz["grant"]["grant_ref"],
            "grant_path": str(law_authorize.GRANT_PATH),
            "grant_sha256": hashlib.sha256(
                law_authorize.GRANT_PATH.read_bytes()).hexdigest(),
            "read_at": now,
            "transcribed_from": "director's written orders (Demo-1 dispatch)",
            "note": "Naya 4 creates no authority; the grant is transcribed, "
                    "revocable, and expires 2026-10-08T00:00:00+00:00.",
        },
        "registry_ref.json": {
            "object_type": "registry_reference",
            "registry_id": "DOOR-LOCAL-STAGING",
            "tool_id": "staging.write_file",
            "registry_status": entry["registry_status"],
            "authority_class": entry["authority_class"],
            "constitution_hash": authz["constitution_hash"],
        },
    }
    for name, payload in context_files.items():
        (receipts_dir / name).write_text(
            json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        print("context:", receipts_dir / name)
    print()
    print("Next: run scripts/demo1/fresh_verify.py", receipt_path,
          "in a fresh process.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
