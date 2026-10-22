#!/usr/bin/env python3
"""Materialize a reusable Smart Builder template into the common page contract."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "HUB/contracts/smart-builder-template-catalog-v1.json"
MANIFEST = ROOT / ".library-source/smart-blocks/manifest.json"


def materialize(catalog: dict, manifest: dict, template_id: str, title: str | None = None,
                description: str | None = None, mode: str = "preview") -> dict:
    if mode not in {"preview", "publish"}:
        raise ValueError("mode must be preview or publish")
    templates = [t for t in catalog.get("templates", []) if t.get("id") == template_id]
    if len(templates) != 1:
        raise ValueError(f"Unknown or duplicate template id: {template_id}")
    template = templates[0]
    known = {b.get("id") for b in manifest.get("blocks", []) if isinstance(b, dict)}
    selected = [block_id for section in template.get("sections", []) for block_id in section.get("block_ids", [])]
    missing = sorted(set(selected) - known)
    if missing:
        raise ValueError("BLOCKED: template references unresolved library IDs: " + ", ".join(missing))
    module_index = catalog.get("modules", {})
    modules = []
    for module_id in template.get("modules", []):
        if module_id not in module_index:
            raise ValueError(f"BLOCKED: unknown module contract {module_id}")
        spec = module_index[module_id]
        modules.append({
            "id": module_id,
            "label": spec["label"],
            "enabled": bool(spec.get("default_enabled", False)),
            "status": spec.get("status", "not_wired"),
            "required": bool(spec.get("required", False)),
            "release_gate": "BLOCK_PUBLISH_UNTIL_VERIFIED",
        })
    if mode == "publish":
        blocked = [m["id"] for m in modules if m["enabled"] and m["status"] != "verified"]
        if blocked:
            raise ValueError("BLOCKED: publish requires verified modules: " + ", ".join(blocked))
    safe_id = re.sub(r"[^a-z0-9-]+", "-", template_id.lower()).strip("-")
    return {
        "schema_version": "naya-smart-builder-page-contract-v1",
        "contract_id": f"smart-builder-template-{safe_id}",
        "template_id": template_id,
        "mode": mode,
        "title": title or template["name"],
        "description": description or template["description"],
        "source_registry": catalog["source_registry"],
        "source_ref": catalog["source_ref"],
        "output": f"HUB/generated/{safe_id}.html",
        "receipt": f"HUB/generated/{safe_id}.receipt.json",
        "sections": template["sections"],
        "modules": modules,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template-id", required=True)
    parser.add_argument("--title")
    parser.add_argument("--description")
    parser.add_argument("--mode", choices=["preview", "publish"], default="preview")
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--output-contract", type=Path, required=True)
    args = parser.parse_args()
    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        contract = materialize(catalog, manifest, args.template_id, args.title, args.description, args.mode)
        args.output_contract.parent.mkdir(parents=True, exist_ok=True)
        args.output_contract.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"MATERIALIZED: {contract['contract_id']} ({args.mode})")
        print(f"MODULES: {len(contract['modules'])}; default-enabled: {sum(m['enabled'] for m in contract['modules'])}")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: template materialization failed closed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
