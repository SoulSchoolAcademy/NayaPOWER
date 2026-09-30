#!/usr/bin/env python3
"""Deterministic current-truth resolver for NayaPOWER.

This is a projection over existing canonical owners, not a new source of truth.
It combines repository contracts with a caller-supplied live-evidence packet and
fails closed on contradictions while preserving UNKNOWN where live evidence is absent.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "BRAIN" / "90-OPERATIONS" / "0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.json"
BRAIN = ROOT / "BRAIN" / "NAYAPOWER-BRAIN-INDEX.json"
MANIFEST = ROOT / "BRAIN" / "03-KERNEL" / "MANIFEST.json"


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _git_head(root: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()


def resolve(live: dict[str, Any], repo_head: str | None = None) -> dict[str, Any]:
    ops = _load(OPS)
    brain = _load(BRAIN)
    manifest = _load(MANIFEST)

    repo_head = repo_head or _git_head()
    main_head = str(live.get("main_head") or "")
    production_branch_head = live.get("production_branch_head")
    issue_states = {
        str(k).lstrip("#"): str(v).upper()
        for k, v in (live.get("issue_states") or {}).items()
    }
    open_prs = live.get("open_prs") or []
    active_issue = str(brain["operations"]["active_issue"])
    active_issue_state = issue_states.get(active_issue, "UNKNOWN")

    hard_conflicts: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    unknowns: list[str] = []

    if not main_head:
        unknowns.append("LIVE_MAIN_HEAD")
    elif repo_head != main_head:
        hard_conflicts.append(
            {
                "code": "CHECKOUT_NOT_LIVE_MAIN",
                "repo_head": repo_head,
                "main_head": main_head,
            }
        )

    if active_issue_state == "UNKNOWN":
        unknowns.append("ACTIVE_ISSUE_STATE")
    elif active_issue_state != "OPEN":
        hard_conflicts.append(
            {
                "code": "ACTIVE_ISSUE_NOT_OPEN",
                "issue": int(active_issue),
                "observed_state": active_issue_state,
            }
        )

    latest_proof = live.get("latest_successful_runtime_proof") or {}
    latest_proof_head = latest_proof.get("head_sha")
    if not latest_proof_head:
        unknowns.append("LATEST_SUCCESSFUL_RUNTIME_PROOF_SOURCE")
        production_proof_current: bool | None = None
    else:
        production_proof_current = bool(main_head and latest_proof_head == main_head)
        if main_head and not production_proof_current:
            warnings.append(
                {
                    "code": "CURRENT_MAIN_NOT_LATEST_PROVEN_SOURCE",
                    "main_head": main_head,
                    "latest_proven_source": latest_proof_head,
                }
            )

    runtime_binding = manifest.get("runtime_binding", {})
    if runtime_binding.get("status") != "PROVEN":
        warnings.append(
            {
                "code": "UNIVERSAL_RUNTIME_BINDING_NOT_PROVEN",
                "status": runtime_binding.get("status", "UNKNOWN"),
            }
        )

    live_runtime_source = live.get("live_runtime_source")
    if not live_runtime_source:
        unknowns.append("LIVE_RUNTIME_SOURCE")
        source_runtime_parity: str = "UNKNOWN"
    elif not main_head:
        source_runtime_parity = "UNKNOWN"
    else:
        source_runtime_parity = "MATCH" if live_runtime_source == main_head else "MISMATCH"
        if source_runtime_parity == "MISMATCH":
            warnings.append(
                {
                    "code": "SOURCE_RUNTIME_PARITY_MISMATCH",
                    "main_head": main_head,
                    "live_runtime_source": live_runtime_source,
                }
            )

    top_10 = ops.get("top_10") or []
    linked_issue_states = {}
    for item in top_10:
        issue_id = str(item.get("id") or "").lstrip("#")
        if issue_id:
            linked_issue_states[issue_id] = issue_states.get(issue_id, "UNKNOWN")

    snapshot = ops.get("evidence_snapshot_base") or ops.get("source_main")
    status = (
        "CONFLICT"
        if hard_conflicts
        else "RESOLVED_WITH_UNKNOWNS"
        if unknowns or warnings
        else "RESOLVED"
    )

    return {
        "schema": "naya.current-truth-resolution.v1",
        "status": status,
        "projection_only": True,
        "authority_note": "Derived projection only; not a second authority source.",
        "source_precedence": [
            "live_git_main",
            "live_runtime_or_deployment_evidence",
            "current_authority",
            "persisted_proof_receipts",
            "canonical_repository_contracts",
            "dated_projections",
        ],
        "repository": {
            "checkout_head": repo_head,
            "live_main_head": main_head or None,
            "checkout_matches_live_main": bool(main_head and repo_head == main_head),
            "production_branch_head": production_branch_head,
            "projection_snapshot_base": snapshot,
            "snapshot_is_current_main": bool(main_head and snapshot == main_head),
        },
        "proof": {
            "bounded_production_source": ops.get("current_state", {}).get(
                "bounded_production_source"
            ),
            "latest_successful_runtime_proof": latest_proof or None,
            "current_main_is_latest_proven_source": production_proof_current,
            "live_runtime_source": live_runtime_source,
            "source_runtime_parity": source_runtime_parity,
            "universal_runtime_binding": runtime_binding.get("status", "UNKNOWN"),
        },
        "active_work": {
            "active_issue": int(active_issue),
            "active_issue_state": active_issue_state,
            "linked_issue_states": linked_issue_states,
            "open_prs": open_prs,
            "next_action": ops.get("next_action"),
            "top_10": top_10,
        },
        "hard_conflicts": hard_conflicts,
        "warnings": warnings,
        "unknowns": sorted(set(unknowns)),
    }



def render_markdown(result: dict[str, Any]) -> str:
    repo = result.get("repository", {})
    proof = result.get("proof", {})
    work = result.get("active_work", {})
    lines = [
        "# NayaPOWER Current Truth — Generated Continuation Brief",
        "",
        f"**Resolver status:** {result.get('status', 'UNKNOWN')}",
        f"**Live main:** `{repo.get('live_main_head') or 'UNKNOWN'}`",
        f"**Checkout:** `{repo.get('checkout_head') or 'UNKNOWN'}`",
        f"**Active issue:** #{work.get('active_issue', 'UNKNOWN')} ({work.get('active_issue_state', 'UNKNOWN')})",
        f"**Runtime/source parity:** {proof.get('source_runtime_parity', 'UNKNOWN')}",
        f"**Latest successful runtime proof source:** `{((proof.get('latest_successful_runtime_proof') or {}).get('head_sha')) or 'UNKNOWN'}`",
        "",
        "## One next action",
        "",
        str(work.get("next_action") or "UNKNOWN"),
        "",
        "## Warnings / unknowns",
        "",
    ]
    warnings = result.get("warnings") or []
    unknowns = result.get("unknowns") or []
    conflicts = result.get("hard_conflicts") or []
    if not warnings and not unknowns and not conflicts:
        lines.append("- None observed by this resolver.")
    else:
        for item in conflicts:
            lines.append(f"- **CONFLICT:** {item.get('code', 'UNKNOWN')} — `{json.dumps(item, sort_keys=True)}`")
        for item in warnings:
            lines.append(f"- **WARNING:** {item.get('code', 'UNKNOWN')} — `{json.dumps(item, sort_keys=True)}`")
        for item in unknowns:
            lines.append(f"- **UNKNOWN:** {item}")
    lines += ["", "## Open pull requests", ""]
    if work.get("open_prs"):
        for pr in work.get("open_prs") or []:
            lines.append(f"- #{pr.get('number', '?')} {pr.get('title', 'UNKNOWN')} — head `{pr.get('head_sha') or 'UNKNOWN'}` — draft={pr.get('draft')} — merge={pr.get('merge_state') or 'UNKNOWN'}")
    else:
        lines.append("- None reported by live collector.")
    lines += ["", "## Max-10", ""]
    for item in work.get("top_10") or []:
        lines.append(f"- {item.get('id', '?')}: {item.get('action', 'UNKNOWN')} [{item.get('status', 'UNKNOWN')}]")
    lines += ["", "> Projection only. Live GitHub/runtime evidence outranks this generated brief when newer.", ""]
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--fail-on-conflict", action="store_true")
    args = parser.parse_args()

    live = json.loads(args.live_evidence.read_text(encoding="utf-8"))
    result = resolve(live)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"

    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    if args.markdown_output:
        args.markdown_output.write_text(render_markdown(result), encoding="utf-8")

    if args.fail_on_conflict and result["hard_conflicts"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
