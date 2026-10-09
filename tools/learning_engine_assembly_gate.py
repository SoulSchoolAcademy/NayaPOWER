"""Fail-closed readiness gate for end-to-end Naya learning experiments."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

REQUIRED_CONNECTIONS = (
    "NINE_NODE_RUNTIME_BINDINGS",
    "CANONICAL_CAPTURE_INTAKE",
    "LEARNING_EXPERIMENT_ADMISSION",
    "VERIFIED_LESSON_TO_ACT",
    "VERIFIED_LESSON_TO_SELF",
    "SOURCE_RUNTIME_PARITY",
    "PROMOTION_BACKSYNC",
    "RLS_POLICIES",
    "COLD_SUCCESSOR_BEHAVIORAL_PROOF",
)


@dataclass(frozen=True)
class AssemblyVerdict:
    ready: bool
    blockers: tuple[str, ...]


def _object(value: Any) -> bool:
    return isinstance(value, dict)


def assess_assembly(manifest: Any, source_sha: str, *, changed_paths: list[str] | tuple[str, ...] = (), verified_is_ancestor: bool = True) -> AssemblyVerdict:
    """Only an evidence-backed manifest for unchanged verified code can arm E2E work."""
    blockers: list[str] = []
    if not _object(manifest):
        return AssemblyVerdict(False, ("ASSEMBLY_MANIFEST_MUST_BE_OBJECT",))
    if manifest.get("schema") != "naya.learning-engine-assembly-gate.v1":
        blockers.append("ASSEMBLY_SCHEMA_MISMATCH")
    verified_sha = manifest.get("verified_source_sha")
    if not isinstance(verified_sha, str) or re.fullmatch(r"[0-9a-f]{40}", verified_sha) is None:
        blockers.append("VERIFIED_SOURCE_SHA_INVALID")
    if not isinstance(source_sha, str) or re.fullmatch(r"[0-9a-f]{40}", source_sha) is None:
        blockers.append("RUN_SOURCE_SHA_INVALID")
    if not verified_is_ancestor:
        blockers.append("VERIFIED_SOURCE_NOT_ANCESTOR")
    allowed_delta = {"BRAIN/03-KERNEL/ASSEMBLY-STATUS.json"}
    unexpected_delta = sorted(set(changed_paths) - allowed_delta)
    if unexpected_delta:
        blockers.append("CODE_CHANGED_AFTER_ASSEMBLY_PROOF:" + ",".join(unexpected_delta))
    if manifest.get("status") != "READY_FOR_END_TO_END":
        blockers.append(f"ASSEMBLY_STATUS_NOT_READY:{manifest.get('status')!r}")

    raw = manifest.get("required_connections")
    if not isinstance(raw, list):
        return AssemblyVerdict(False, tuple(blockers + ["REQUIRED_CONNECTIONS_MUST_BE_LIST"]))
    by_id: dict[str, dict[str, Any]] = {}
    for item in raw:
        if not _object(item) or not isinstance(item.get("id"), str):
            blockers.append("INVALID_CONNECTION_ENTRY")
            continue
        cid = item["id"]
        if cid in by_id:
            blockers.append(f"DUPLICATE_CONNECTION_ID:{cid}")
        by_id[cid] = item

    for cid in REQUIRED_CONNECTIONS:
        item = by_id.get(cid)
        if item is None:
            blockers.append(f"REQUIRED_CONNECTION_MISSING:{cid}")
            continue
        if item.get("status") != "PROVEN":
            blockers.append(f"CONNECTION_NOT_PROVEN:{cid}:{item.get('status')!r}")
        evidence = item.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            blockers.append(f"CONNECTION_EVIDENCE_MISSING:{cid}")
            continue
        for index, receipt in enumerate(evidence):
            if not _object(receipt):
                blockers.append(f"INVALID_EVIDENCE_OBJECT:{cid}:{index}")
                continue
            if receipt.get("source_sha") != verified_sha:
                blockers.append(f"EVIDENCE_SOURCE_SHA_MISMATCH:{cid}:{index}")
            if not isinstance(receipt.get("independent_verifier"), str) or not receipt["independent_verifier"].strip():
                blockers.append(f"INDEPENDENT_VERIFIER_REQUIRED:{cid}:{index}")
            digest = receipt.get("artifact_sha256")
            if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
                blockers.append(f"EVIDENCE_HASH_INVALID:{cid}:{index}")
            timestamp = receipt.get("verified_at")
            try:
                if not isinstance(timestamp, str) or not timestamp.strip():
                    raise ValueError("missing")
                datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                blockers.append(f"EVIDENCE_TIMESTAMP_INVALID:{cid}:{index}")

    unknown = sorted(set(by_id) - set(REQUIRED_CONNECTIONS))
    if unknown:
        blockers.append("UNDOCUMENTED_CONNECTION_CLASSES:" + ",".join(unknown))

    return AssemblyVerdict(not blockers, tuple(blockers))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--verified-is-ancestor", choices=("true", "false"), required=True)
    parser.add_argument("--changed-paths", default="")
    parser.add_argument("--github-output", required=True)
    args = parser.parse_args()
    blockers: tuple[str, ...]
    try:
        with open(args.manifest, encoding="utf-8") as f:
            manifest = json.load(f)
        changed_paths = [line.strip() for line in args.changed_paths.splitlines() if line.strip()]
        verdict = assess_assembly(
            manifest, args.source_sha, changed_paths=changed_paths,
            verified_is_ancestor=args.verified_is_ancestor == "true",
        )
        ready, blockers = verdict.ready, verdict.blockers
    except (OSError, ValueError, TypeError) as exc:
        ready = False
        blockers = (f"ASSEMBLY_MANIFEST_READ_FAILED:{type(exc).__name__}",)
    with open(args.github_output, "a", encoding="utf-8") as f:
        f.write(f"ready={'true' if ready else 'false'}\n")
        f.write("blockers=" + ";".join(blockers).replace("\n", " ") + "\n")
    print("ASSEMBLY_READY" if ready else "LEARNING_E2E_HELD: " + "; ".join(blockers))
    # A held gate is an intentional BLOCKED state, not a failed workflow.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
