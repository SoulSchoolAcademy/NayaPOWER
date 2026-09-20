#!/usr/bin/env python3
"""Machine-detectable audit of production Superbrain event-write coverage.

The audit is intentionally conservative. It scans production source under
.naya/memory and .naya/runtime, excludes tests/fixtures/generated event data,
and reports only event-like persistence candidates. Ambiguous cases remain
visible as blockers rather than being silently treated as canonical.
"""
from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRODUCTION_ROOTS = (ROOT / ".naya" / "memory", ROOT / ".naya" / "runtime")
EXCLUDED_NAMES = {"canonical_write_inventory.py"}
EXCLUDED_PARTS = {"events", "fixtures", "__pycache__"}
DERIVED_FILES = {"INDEX.json", "VALIDATION-REPORT.json"}
CANONICAL_MODULE = ".naya/runtime/canonical_event_store.py"


@dataclass
class Finding:
    caller: str
    purpose: str
    write_sites: list[int]
    canonical_status: str
    classification: str
    bypass_risk: str
    evidence: list[str]


def _literal_strings(node: ast.AST) -> list[str]:
    return [n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def _call_name(node: ast.Call) -> str:
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def scan_file(path: Path) -> Finding | None:
    rel = path.relative_to(ROOT).as_posix()
    if path.name in EXCLUDED_NAMES or any(part in EXCLUDED_PARTS for part in path.parts):
        return None
    source = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source, filename=rel)
    except (OSError, SyntaxError) as exc:
        return Finding(rel, "unparseable production source", [], "E", "E", "HIGH", [str(exc)])

    imports_canonical = False
    direct_write_sites: list[int] = []
    evidence: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            text = ast.get_source_segment(source, node) or ""
            if "canonical_event_store" in text or "create_or_replay" in text:
                imports_canonical = True
                evidence.append(f"canonical import at line {node.lineno}")
        if isinstance(node, ast.Call):
            name = _call_name(node)
            strings = _literal_strings(node)
            eventish = any("SE-" in s or ".naya/memory/events" in s or "/events" in s for s in strings)
            writeish = name in {"write_text", "write_bytes", "open", "dump", "dumps", "fdopen", "open_os"}
            if eventish and writeish:
                direct_write_sites.append(node.lineno)
                evidence.append(f"event-like write at line {node.lineno}: {name}")

    if imports_canonical and not direct_write_sites:
        return Finding(rel, "canonical event caller", [], "A", "A", "LOW", evidence)
    if direct_write_sites:
        if rel == CANONICAL_MODULE:
            return Finding(rel, "canonical event persistence boundary", direct_write_sites, "A", "A", "LOW", evidence)
        return Finding(rel, "direct event-like persistence candidate", direct_write_sites, "B", "B", "HIGH", evidence)
    if any(name in source for name in DERIVED_FILES):
        return Finding(rel, "derived/audit artifact producer", [], "D", "D", "NONE", ["writes derived artifacts, not canonical event JSON"])
    return None


def scan() -> list[Finding]:
    findings: list[Finding] = []
    for root in PRODUCTION_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.py")):
            finding = scan_file(path)
            if finding:
                findings.append(finding)
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    findings = scan()
    blockers = [f for f in findings if f.classification in {"B", "C", "E"}]
    payload = {
        "schema_version": 1,
        "status": "GREEN" if not blockers else "RED",
        "production_roots": [str(p.relative_to(ROOT)) for p in PRODUCTION_ROOTS if p.exists()],
        "finding_count": len(findings),
        "blocker_count": len(blockers),
        "classifications": {k: sum(f.classification == k for f in findings) for k in "ABCDE"},
        "findings": [asdict(f) for f in findings],
    }
    print(json.dumps(payload, indent=2) if args.json else json.dumps(payload, indent=2))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
