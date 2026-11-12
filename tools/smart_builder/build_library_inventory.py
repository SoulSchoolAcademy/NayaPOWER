#!/usr/bin/env python3
"""Generate and verify the Smart Builder discovery index from source registries.

The source registries remain authoritative. This script only creates derived
inventory/gallery artifacts; it never edits or duplicates component source.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CATALOG_REL = Path("BRAIN/10-INTERFACES/DESIGN-BLOCKS/naya-design-catalog.json")
MANIFEST_REL = Path("smart-blocks/manifest.json")
REGISTRY_REL = Path("smart-blocks/REGISTRY.md")
INVENTORY_REL = Path("HUB/SMART-BUILDER-LIBRARY-INVENTORY.json")
GALLERY_REL = Path("HUB/SMART-BUILDER-LIBRARY.html")
CANONICAL_REF = "naya5/smart-blocks-library"
REPO = "SoulSchoolAcademy/NayaPOWER"

RULES = [
    "Source registries remain the source of truth; this file is a generated discovery index, not a replacement registry.",
    "The design catalog and Smart Blocks manifest are separate inventories with different IDs; do not sum their counts as unique components.",
    "Catalogued does not mean standalone-tested, build-compatible, or production-proven.",
    "Before assembly, resolve every selected block, dependency, and runtime behavior against the exact pinned source ref.",
    "If an entry cannot be resolved, fail closed and report the missing ID/path; never silently invent a substitute.",
]


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def build_inventory(repo_root: Path, canonical_root: Path) -> dict[str, Any]:
    catalog_path = repo_root / CATALOG_REL
    manifest_path = canonical_root / MANIFEST_REL
    registry_path = canonical_root / REGISTRY_REL
    catalog = read_json(catalog_path)
    manifest = read_json(manifest_path)
    registry_path.read_text(encoding="utf-8")  # fail closed if human registry is absent

    catalog_blocks = catalog.get("blocks", [])
    smart_blocks = manifest.get("blocks", [])
    if not isinstance(catalog_blocks, list) or not isinstance(smart_blocks, list):
        raise ValueError("Source registry 'blocks' fields must be arrays")

    entries: list[dict[str, Any]] = []
    for block in catalog_blocks:
        if not isinstance(block, dict) or not block.get("id"):
            raise ValueError("Every design catalog entry must be an object with an id")
        block_id = block["id"]
        entries.append({
            "inventory_key": f"design-catalog:{block_id}",
            "source_registry": "naya-design-catalog.json",
            "source_id": block_id,
            "name": block.get("name") or block_id,
            "category": block.get("category") or "uncategorized",
            "description": block.get("job") or block.get("description") or "",
            "use_when": block.get("when_to_use") or block.get("use_when") or "",
            "use_when_not": block.get("when_not_to_use") or "",
            "tags": block.get("tags") or [],
            "css_classes": block.get("selectors") or [],
            "states": block.get("states") or [],
            "source_file": block.get("source"),
            "files": block.get("files") or {},
            "source_url": f"https://github.com/{REPO}/blob/main/{CATALOG_REL.as_posix()}",
            "source_status": "catalogued; runtime availability must be checked by build verifier",
        })

    for block in smart_blocks:
        if not isinstance(block, dict) or not block.get("id"):
            raise ValueError("Every Smart Blocks entry must be an object with an id")
        block_id = block["id"]
        html_file = block.get("html_file")
        entries.append({
            "inventory_key": f"smart-blocks:{block_id}",
            "source_registry": "smart-blocks/manifest.json",
            "source_id": block_id,
            "name": block.get("name") or block_id,
            "category": block.get("category") or block.get("category_id") or "uncategorized",
            "description": block.get("description") or "",
            "use_when": block.get("use_when") or "",
            "use_when_not": "",
            "tags": [],
            "css_classes": block.get("css_classes") or [],
            "states": [],
            "tier": block.get("tier"),
            "html_file": html_file,
            "css_file": block.get("css_file"),
            "js_needed": bool(block.get("js_needed")),
            "js_file": block.get("js_file"),
            "dependencies": block.get("needs") or [],
            "source_url": f"https://github.com/{REPO}/blob/{CANONICAL_REF}/{html_file or 'smart-blocks/manifest.json'}",
            "manifest_url": f"https://github.com/{REPO}/blob/{CANONICAL_REF}/smart-blocks/manifest.json",
            "source_status": "catalogued on canonical library branch; not yet merged to main",
        })

    keys = [e["inventory_key"] for e in entries]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate composite inventory keys")

    categories = sorted({e["category"] for e in entries})
    return {
        "schema_version": "naya-smart-builder-library-inventory-v1",
        "generated_from": [
            {
                "id": "design-catalog",
                "path": CATALOG_REL.as_posix(),
                "ref": "main",
                "blob_sha": git_blob_sha(catalog_path),
                "declared_total": catalog.get("total_blocks"),
                "observed_entries": len(catalog_blocks),
            },
            {
                "id": "canonical-smart-blocks",
                "path": MANIFEST_REL.as_posix(),
                "ref": CANONICAL_REF,
                "blob_sha": git_blob_sha(manifest_path),
                "declared_total": len(smart_blocks),
                "observed_entries": len(smart_blocks),
            },
            {
                "id": "canonical-smart-blocks-registry",
                "path": REGISTRY_REL.as_posix(),
                "ref": CANONICAL_REF,
                "blob_sha": git_blob_sha(registry_path),
                "observed_status": "human registry read; counts intentionally not added as a separate unique-block total",
            },
        ],
        "inventory_rules": RULES,
        "counts": {
            "source_registries": 2,
            "entries": len(entries),
            "design_catalog_entries": len(catalog_blocks),
            "canonical_smart_blocks_entries": len(smart_blocks),
            "categories": len(categories),
        },
        "categories": categories,
        "entries": entries,
    }


def gallery_html(inventory: dict[str, Any], existing_html: str) -> str:
    """Refresh only derived data slots in the checked-in gallery shell."""
    entries_json = json.dumps(inventory["entries"], ensure_ascii=False, separators=(",", ":"))
    entries_json = entries_json.replace("<", r"\u003c").replace(">", r"\u003e").replace("&", r"\u0026")
    marker = re.compile(r"const items=.*?;\s*const q=document\.getElementById\('q'\)", re.S)
    replacement = f"const items={entries_json};\nconst q=document.getElementById('q')"
    updated, substitutions = marker.subn(lambda _: replacement, existing_html, count=1)
    if substitutions != 1:
        raise ValueError("Gallery data slot not found; refusing to overwrite unknown HTML")

    # Refresh the four visible counts, preserving the surrounding presentation.
    values = [
        inventory["counts"]["design_catalog_entries"],
        inventory["counts"]["canonical_smart_blocks_entries"],
        inventory["counts"]["entries"],
        inventory["counts"]["categories"],
    ]
    num_pattern = re.compile(r'(<div class="num">)\d+(</div>)')
    index = 0

    def replace_num(match: re.Match[str]) -> str:
        nonlocal index
        if index >= len(values):
            return match.group(0)
        result = f"{match.group(1)}{values[index]}{match.group(2)}"
        index += 1
        return result

    updated = num_pattern.sub(replace_num, updated, count=4)
    if index != 4:
        raise ValueError("Gallery stats slots not found; refusing to claim refreshed counts")

    categories = inventory["categories"]
    option_html = '<option value="">All categories</option>' + "".join(
        f'<option value="{escape(category, quote=True)}">{escape(category)}</option>'
        for category in categories
    )
    option_pattern = re.compile(r'(<select id="category"[^>]*>).*?(</select>)', re.S)
    updated, substitutions = option_pattern.subn(lambda m: m.group(1) + option_html + m.group(2), updated, count=1)
    if substitutions != 1:
        raise ValueError("Gallery category slot not found; refusing to overwrite unknown HTML")
    return updated


def generate(repo_root: Path, canonical_root: Path) -> tuple[str, str]:
    inventory = build_inventory(repo_root, canonical_root)
    inventory_text = json.dumps(inventory, ensure_ascii=False, indent=2) + "\n"
    gallery_path = repo_root / GALLERY_REL
    existing_html = gallery_path.read_text(encoding="utf-8")
    html = gallery_html(inventory, existing_html)
    return inventory_text, html


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--canonical-root", type=Path, default=ROOT / ".library-source",
                        help="checkout root containing smart-blocks/manifest.json")
    parser.add_argument("--check", action="store_true", help="fail if checked-in generated files are stale")
    args = parser.parse_args()

    try:
        inventory_text, html = generate(args.repo_root, args.canonical_root)
        inventory_path = args.repo_root / INVENTORY_REL
        gallery_path = args.repo_root / GALLERY_REL
        if args.check:
            stale = []
            if not inventory_path.exists() or inventory_path.read_text(encoding="utf-8") != inventory_text:
                stale.append(INVENTORY_REL.as_posix())
            if not gallery_path.exists() or gallery_path.read_text(encoding="utf-8") != html:
                stale.append(GALLERY_REL.as_posix())
            if stale:
                print("STALE generated inventory artifacts: " + ", ".join(stale), file=sys.stderr)
                return 1
            print("PASS: inventory and gallery match pinned source registries")
            return 0

        inventory_path.write_text(inventory_text, encoding="utf-8")
        gallery_path.write_text(html, encoding="utf-8")
        print(f"Wrote {INVENTORY_REL} and {GALLERY_REL}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: library inventory generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
