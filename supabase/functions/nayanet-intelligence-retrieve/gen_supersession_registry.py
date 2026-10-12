#!/usr/bin/env python3
"""Generate supersession_registry.ts from tools/applicability_supersession.json.

THETA-NEXT-4: the JSON registry is the interim source of truth for
supersession links (lane-approved, auditable in its owning commit). The edge
function cannot read the repo JSON at runtime, so this script vendors the
links into a TS module that the function bundles.

Source of truth: <repo>/tools/applicability_supersession.json
Generated:       supabase/functions/nayanet-intelligence-retrieve/supersession_registry.ts

Regenerate whenever the JSON changes. The durable home for these links is the
block lineage table (superseded_by_block_id); this registry is the interim.
"""
import json
import sys
from pathlib import Path

FUNC_DIR = Path(__file__).resolve().parent
REPO_ROOT = FUNC_DIR.parents[2]
JSON_PATH = REPO_ROOT / "tools" / "applicability_supersession.json"
OUT_PATH = FUNC_DIR / "supersession_registry.ts"


def main() -> int:
    links = {}
    if JSON_PATH.exists():
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        raw = data.get("superseded_by") or {}
        links = {str(k): str(v) for k, v in raw.items() if v}
    else:
        print(f"note: {JSON_PATH} not present; emitting empty registry",
              file=sys.stderr)

    lines = [
        "// GENERATED — do not hand-edit.",
        "// Source: tools/applicability_supersession.json (lane-approved links).",
        "// Regenerate: python3 gen_supersession_registry.py",
        "// (No timestamp: the owning commit is the provenance. Regen is a",
        "// no-op when the links are unchanged.)",
        "//",
        "// THETA-NEXT-4 interim: the retrieve function reads these links from",
        "// this module (bundled with the function). The durable home is the",
        "// block lineage table (superseded_by_block_id), which wins on conflict.",
        f"export const SUPERSESSION_REGISTRY_SOURCE = {json.dumps(str(JSON_PATH.relative_to(REPO_ROOT)))};",
        "export const SUPERSESSION_REGISTRY: Record<string, string> = {",
    ]
    for k in sorted(links):
        lines.append(f"  {json.dumps(k)}: {json.dumps(links[k])},")
    lines.append("};")
    lines.append("")
    content = "\n".join(lines)
    if OUT_PATH.exists() and OUT_PATH.read_text(encoding="utf-8") == content:
        print(f"unchanged: {OUT_PATH} ({len(links)} links)")
        return 0
    OUT_PATH.write_text(content, encoding="utf-8")
    print(f"wrote {OUT_PATH} ({len(links)} links)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
