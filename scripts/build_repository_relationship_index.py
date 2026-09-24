#!/usr/bin/env python3
"""Build a deterministic relationship/navigation index from repository records.

Derived projection only: never an authority source, event store, or memory system.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / ".naya/control-plane/RELATIONSHIP-INDEX.json"
OUT_MD = ROOT / "SUPERBRAIN/NAYA-ACTIVITY/RELATIONSHIP-INDEX.md"
DERIVED_OUTPUTS = {OUT_JSON.relative_to(ROOT).as_posix(), OUT_MD.relative_to(ROOT).as_posix()}
SKIP = {".git", "node_modules", ".venv", "__pycache__"}
EXTS = {".md", ".json", ".py", ".yml", ".yaml", ".html", ".ts", ".js"}

CLASS_RULES = [
    ("CONTROL_PLANE", ".naya/control-plane/"),
    ("GOVERNANCE", ".naya/governance/"),
    ("RUNTIME", ".naya/runtime/"),
    ("EVENT", ".naya/memory/events/"),
    ("ACTIVITY", "SUPERBRAIN/NAYA-ACTIVITY/"),
    ("TEAM_NAYA", "NAYA-TEAM/"),
    ("PROJECT", "NAYA-TEAM/PROJECTS/"),
    ("WORKFLOW", ".github/workflows/"),
    ("TEST", "tests/"),
]

AREAS = {
    "INTELLIGENT-HUB", "SMART-FEED", "YOUR-INTELLIGENCE-TODAY", "SMART-NOTES",
    "INTELLIGENCE-REPORTS", "INTELLIGENCE-LIBRARY", "SMART-LISTS", "CONNECTIONS",
    "SMART-MAIL", "SMART-SPACES", "SMART-SHARE", "SMART-LEDGER",
    "PERSONAL-INTELLIGENCE", "COLLECTIVE-INTELLIGENCE", "ACTIVITY",
    "IDENTITY-PRIVACY", "PIS", "CIS", "SMART-FLOW",
}

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def node_class(path: str) -> str:
    if path.startswith("NAYA-TEAM/PROJECTS/NAYANET/"):
        parts = path.split("/")
        if len(parts) >= 4 and parts[3] in AREAS:
            return "SUBPROJECT"
    for cls, prefix in CLASS_RULES:
        if path.startswith(prefix):
            return cls
    if path == "2026 09 17 NAYANET HUB.html":
        return "SOURCE"
    return "OTHER"

def project_for(path: str) -> str | None:
    if path.startswith("NAYA-TEAM/PROJECTS/NAYANET/"):
        return "NAYANET"
    if "NAYANET" in path.upper():
        return "NAYANET"
    return None

def subproject_for(path: str) -> str | None:
    prefix = "NAYA-TEAM/PROJECTS/NAYANET/"
    if not path.startswith(prefix):
        return None
    parts = path.split("/")
    return parts[3] if len(parts) >= 4 and parts[3] in AREAS else None

def timestamp_for(path: str) -> str | None:
    patterns = [
        r"(20\d{2})[-_](\d{2})[-_](\d{2})T([0-2]\d)[-_:]([0-5]\d)(?:[-_:]([0-5]\d))?",
        r"(20\d{2})[-_](\d{2})[-_](\d{2})/(?:([0-2]\d)[-_])?([0-5]\d)(?:[-_]([0-5]\d))?",
        r"(20\d{2})/(\d{2})/(\d{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, path)
        if match:
            return "-".join(x for x in match.groups() if x is not None)
    return None

def existing_paths() -> set[str]:
    return {
        path for path in (
            rel(p) for p in ROOT.rglob("*")
            if p.is_file() and not any(part in SKIP for part in p.parts)
        )
        if path not in DERIVED_OUTPUTS
    }

def extract_refs(text: str, paths: set[str]) -> list[str]:
    refs = set()
    for match in re.finditer(r"(?:\.\.?/)?[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+", text):
        candidate = match.group(0).lstrip("./")
        if candidate in paths:
            refs.add(candidate)
    for path in paths:
        name = Path(path).name
        if len(name) >= 18 and name in text:
            refs.add(path)
    return sorted(refs)

def generated_at_value() -> str:
    source_date_epoch=os.environ.get("SOURCE_DATE_EPOCH")
    if source_date_epoch:
        return datetime.fromtimestamp(int(source_date_epoch),timezone.utc).replace(microsecond=0).isoformat()
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> None:
    paths = sorted(existing_paths())
    path_set = set(paths)
    nodes = []
    edges = []

    for path in paths:
        source = ROOT / path
        if source.suffix.lower() not in EXTS:
            continue
        try:
            content = source.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        nodes.append({
            "id": path,
            "class": node_class(path),
            "project": project_for(path),
            "subproject": subproject_for(path),
            "timestamp": timestamp_for(path),
        })

        for target in extract_refs(content, path_set):
            if target != path:
                edges.append({"from": path, "to": target, "relationship": "references"})

        subproject = subproject_for(path)
        if subproject:
            boundary = f"NAYA-TEAM/PROJECTS/NAYANET/{subproject}/README.md"
            if boundary in path_set and path != boundary:
                edges.append({"from": path, "to": boundary, "relationship": "applies-to"})

        if path.startswith("NAYA-TEAM/2026/09/17/"):
            target = "NAYA-TEAM/PROJECTS/NAYANET/NAYANET-GITHUB-OPERATING-MAP.md"
            if target in path_set:
                edges.append({"from": path, "to": target, "relationship": "recorded-in"})

    unique = {(e["from"], e["to"], e["relationship"]): e for e in edges}
    edges = [unique[key] for key in sorted(unique)]

    generated_at = generated_at_value()
    payload = {
        "schema": "NAYA_REPOSITORY_RELATIONSHIP_INDEX_V1",
        "generated_at": generated_at,
        "authority": "DERIVED_NAVIGATION_ONLY",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "rules": {
            "one_truth": "ONE RECORD → MANY EXPLICIT LINKS → ONE CANONICAL TRUTH",
            "no_new_store": True,
            "unknown_is_explicit": True,
            "source_records_unchanged": True,
        },
        "counts": {"nodes": len(nodes), "edges": len(edges)},
        "nodes": nodes,
        "edges": edges,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    classes = {}
    for node in nodes:
        classes[node["class"]] = classes.get(node["class"], 0) + 1

    md = [
        "# Repository Relationship Index",
        "",
        "**STATUS:** DERIVED NAVIGATION PROJECTION V1",
        "",
        "Generated from repository records. This file is not an authority source.",
        "",
        "## What this gives a Naya",
        "",
        "RECORD → PROJECT → SUB-PROJECT → RELATED RECORDS → STATE / EVIDENCE → SUCCESSOR",
        "",
        "## Index statistics",
        "",
        f"- Nodes indexed: **{len(nodes)}**",
        f"- Relationships indexed: **{len(edges)}**",
        f"- Generated: **{generated_at}**",
        "",
        "## Node classes",
        "",
    ]
    md.extend(f"- **{key}** — {classes[key]}" for key in sorted(classes))
    md += [
        "",
        "## Relationship law",
        "",
        "**ONE RECORD → MANY EXPLICIT LINKS → ONE CANONICAL TRUTH.**",
        "",
        "Links are derived from explicit repository references and conservative structural boundaries. Missing evidence is not converted into a guessed relationship.",
        "",
        "## Canonical sources remain authoritative",
        "",
        "- .naya/control-plane/STATE.json",
        "- .naya/control-plane/BLOCKS.json",
        "- .naya/control-plane/MAP.json",
        "- .naya/control-plane/PROOF.json",
        "- .naya/governance/",
        "- .naya/memory/events/",
        "- SUPERBRAIN/NAYA-ACTIVITY/",
        "- NAYA-TEAM/PROJECTS/",
        "",
        "## Regenerate",
        "",
        "python scripts/build_repository_relationship_index.py",
        "",
        "Do not edit this generated projection by hand.",
    ]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
