"""LADDER GATE — measures CONTRACT, UNIT, and INTEGRATION rungs.

The acceptance ladder in `BRAIN/03-KERNEL/0002-KERNEL-ACCEPTANCE-V1.md` is:

    STRUCTURAL -> CONTRACT -> UNIT -> INTEGRATION -> BEHAVIORAL
    -> OUTCOME -> CAUSAL -> PRODUCTION -> SUCCESSOR

Three of those rungs had NO gate at all, so they were UNKNOWN. UNKNOWN is a
finding, but it is not useful. This measures them honestly from the current tree
and reports the highest rung reached.

It never upgrades a rung. A rung is PROVEN only when there is a deterministic
check that currently passes. Absent evidence is UNKNOWN or MISSING, never PASS.
It changes nothing and grants no authority.

Run:  python -B kernel/verify_ladder.py [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "BRAIN" / "03-KERNEL" / "MANIFEST.json"
NODES_DIR = ROOT / "BRAIN" / "03-KERNEL" / "NODES"

# Sections the kernel's own acceptance contract requires of a node contract.
REQUIRED_CONTRACT_SECTIONS = ("Purpose", "Inputs", "Outputs")

# Executable surfaces that can constitute UNIT coverage for a node.
UNIT_SURFACES = ("tests/", "kernel/", "supabase/functions/", "verification/")


def _git(*a: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *a], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:  # noqa: BLE001
        return ""


def load_manifest() -> dict:
    if not MANIFEST.is_file():
        return {}
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def gate_contract(nodes: list[dict]) -> dict:
    """Every manifest node must resolve to a real contract carrying required sections."""
    if not nodes:
        return {"rung": "CONTRACT", "status": "UNKNOWN", "detail": "manifest carries no nodes"}
    missing, thin, mismatched = [], [], []
    for n in nodes:
        name = n.get("name", "")
        node_id = n.get("id", "")
        path = NODES_DIR / name / "0001-CONTRACT.md"
        if not path.is_file():
            missing.append(name)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        absent = [s for s in REQUIRED_CONTRACT_SECTIONS if s not in text]
        if absent:
            thin.append(f"{name}:{','.join(absent)}")
        if node_id and node_id not in text:
            mismatched.append(name)
    if missing:
        return {
            "rung": "CONTRACT",
            "status": "PARTIAL",
            "detail": f"{len(missing)} node contract(s) absent: {missing}",
            "evidence": missing,
        }
    if thin:
        return {
            "rung": "CONTRACT",
            "status": "PARTIAL",
            "detail": f"all {len(nodes)} contracts exist but {len(thin)} lack required "
            f"sections {list(REQUIRED_CONTRACT_SECTIONS)}: {thin}",
            "evidence": thin,
        }
    if mismatched:
        return {
            "rung": "CONTRACT",
            "status": "PARTIAL",
            "detail": f"contract id does not match the manifest for: {mismatched}",
            "evidence": mismatched,
        }
    return {
        "rung": "CONTRACT",
        "status": "PROVEN",
        "detail": f"all {len(nodes)} node contracts exist, carry the required sections, "
        f"and their ids match the manifest",
    }


def gate_unit(nodes: list[dict]) -> dict:
    """Each node needs an executable surface that exercises it in isolation."""
    if not nodes:
        return {"rung": "UNIT", "status": "UNKNOWN", "detail": "manifest carries no nodes"}
    haystack = ""
    for surface in UNIT_SURFACES:
        base = ROOT / surface.rstrip("/")
        if not base.is_dir():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in {".py", ".ts", ".js", ".json", ".md"}:
                haystack += "\n" + p.read_text(encoding="utf-8", errors="replace")
    covered = [n["name"] for n in nodes if n.get("id", "") in haystack or n.get("name", "") in haystack]
    if not covered:
        return {
            "rung": "UNIT",
            "status": "MISSING",
            "detail": f"no executable surface references any of the {len(nodes)} node ids or "
            f"names. Every node is specification-only with no unit coverage.",
        }
    return {
        "rung": "UNIT",
        "status": "PARTIAL",
        "detail": f"{len(covered)}/{len(nodes)} nodes are referenced by some executable "
        f"surface, but reference is not isolation: no per-node test was identified",
        "evidence": covered,
    }


def gate_integration() -> dict:
    """A composition test must exercise nodes together, not individually."""
    tests = ROOT / "tests"
    if not tests.is_dir():
        return {"rung": "INTEGRATION", "status": "MISSING", "detail": "no tests/ directory"}
    integration = [
        p.name
        for p in tests.rglob("*.py")
        if re.search(r"integrat|compos|chain|pipeline|end_to_end|end-to-end", p.name, re.I)
    ]
    if not integration:
        return {
            "rung": "INTEGRATION",
            "status": "MISSING",
            "detail": "no test composes multiple nodes; each node is verified, if at all, "
            "in isolation. Composition is exactly the birth requirement and is untested.",
        }
    return {
        "rung": "INTEGRATION",
        "status": "PARTIAL",
        "detail": f"integration-shaped tests exist ({integration[:4]}) but were not "
        f"confirmed to exercise a multi-node sequence",
        "evidence": integration[:6],
    }


def evaluate() -> dict:
    manifest = load_manifest()
    nodes = manifest.get("nodes", []) if isinstance(manifest, dict) else []
    results = [gate_contract(nodes), gate_unit(nodes), gate_integration()]
    proven = [r for r in results if r["status"] == "PROVEN"]
    binding = manifest.get("runtime_binding", {}) if isinstance(manifest, dict) else {}
    return {
        "schema": "naya/ladder-gate/v1",
        "head": _git("rev-parse", "HEAD"),
        "manifest_status": manifest.get("status") if isinstance(manifest, dict) else None,
        "runtime_binding": binding.get("status") if isinstance(binding, dict) else None,
        "rungs_measured": len(results),
        "rungs_proven": len(proven),
        "highest_rung": next((r["rung"] for r in results if r["status"] == "PROVEN"), "NONE"),
        "rungs": results,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        rep = evaluate()
    except Exception as exc:  # noqa: BLE001
        print(f"LADDER_GATE=ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(rep, indent=2))
    else:
        print("NAYA_LADDER_GATE")
        print(f"HEAD={rep['head']}  MANIFEST={rep['manifest_status']}  RUNTIME_BINDING={rep['runtime_binding']}")
        for r in rep["rungs"]:
            print(f"  [{r['status']:>7}] {r['rung']}: {r['detail']}")
        print(f"HIGHEST_PROVEN_RUNG={rep['highest_rung']}  ({rep['rungs_proven']}/{rep['rungs_measured']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
