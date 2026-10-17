#!/usr/bin/env python3
"""Deterministic, fail-closed assembler for pages composed from Smart Blocks."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

VERSION = "smart-block-assembler/0.1.0"
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT = ROOT / "HUB/contracts/smart-builder-library-demo-v1.json"
DEFAULT_LIBRARY = ROOT / ".library-source"
ALLOWED_SOURCE_ROOT = "smart-blocks"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def safe_source_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    resolved_root = root.resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ValueError(f"Source path escapes library root: {relative}")
    if not candidate.is_file():
        raise FileNotFoundError(f"Missing registered dependency: {relative}")
    return candidate


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def assemble(contract_path: Path, library_root: Path) -> tuple[str, dict[str, Any]]:
    contract_bytes = contract_path.read_bytes()
    contract = json.loads(contract_bytes.decode("utf-8"))
    if contract.get("schema_version") != "naya-smart-builder-page-contract-v1":
        raise ValueError("Unsupported page contract schema")
    if contract.get("source_registry") != "smart-blocks/manifest.json":
        raise ValueError("Unsupported source registry; no silent source substitution")
    manifest_path = safe_source_path(library_root, contract["source_registry"])
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    blocks = manifest.get("blocks")
    if not isinstance(blocks, list):
        raise ValueError("Source manifest has no blocks array")
    by_id: dict[str, dict[str, Any]] = {}
    for block in blocks:
        block_id = block.get("id") if isinstance(block, dict) else None
        if not block_id or block_id in by_id:
            raise ValueError(f"Missing or duplicate block id in source manifest: {block_id}")
        by_id[block_id] = block

    selected: list[dict[str, Any]] = []
    selected_ids: list[str] = []
    section_ids: set[str] = set()
    for section in contract.get("sections", []):
        sid = section.get("id")
        if not sid or sid in section_ids:
            raise ValueError(f"Missing or duplicate section id: {sid}")
        section_ids.add(sid)
        for block_id in section.get("block_ids", []):
            if block_id not in by_id:
                raise ValueError(f"BLOCKED: unresolved block id {block_id}")
            selected.append(by_id[block_id])
            selected_ids.append(block_id)
    if not selected:
        raise ValueError("BLOCKED: contract selects no blocks")
    if len(selected_ids) != len(set(selected_ids)):
        raise ValueError("Duplicate block selection is not allowed in this demo contract")

    dependency_order: list[str] = []
    for block in selected:
        needs = block.get("needs") or []
        for dep in needs:
            if dep not in dependency_order:
                dependency_order.append(dep)
        if block.get("html_file") and block["html_file"] not in dependency_order:
            dependency_order.append(block["html_file"])
    if "smart-blocks/icons.svg" not in dependency_order:
        dependency_order.append("smart-blocks/icons.svg")

    css_parts: list[str] = []
    dependency_hashes: list[dict[str, str]] = []
    js_parts: list[str] = []
    for dep in dependency_order:
        path = safe_source_path(library_root, dep)
        data = path.read_bytes()
        dependency_hashes.append({
            "path": dep,
            "sha256": sha256(data),
            "git_blob_sha": git_blob_sha(data),
        })
        if dep.endswith(".css"):
            css_parts.append(f"\n/* SOURCE: {dep} · SHA256 {sha256(data)} */\n" + data.decode("utf-8"))
        elif dep.endswith(".js"):
            if dep not in [d["path"] for d in dependency_hashes[:-1]]:
                js_parts.append(f"\n/* SOURCE: {dep} · SHA256 {sha256(data)} */\n" + data.decode("utf-8"))

    icons_path = safe_source_path(library_root, "smart-blocks/icons.svg")
    icons = icons_path.read_text(encoding="utf-8")
    if not re.search(r"<svg\b", icons) or "</svg>" not in icons:
        raise ValueError("BLOCKED: icons.svg is not a valid inline SVG sprite")

    rendered_sections: list[str] = []
    for section in contract["sections"]:
        fragments = []
        for block_id in section["block_ids"]:
            block = by_id[block_id]
            html_file = block.get("html_file")
            if not html_file:
                raise ValueError(f"BLOCKED: {block_id} has no source HTML file")
            snippet = safe_source_path(library_root, html_file).read_text(encoding="utf-8")
            # Remove source comments from the visible specimen, preserve component markup.
            snippet = re.sub(r"<!--.*?-->", "", snippet, flags=re.S).strip()
            if not snippet:
                raise ValueError(f"BLOCKED: empty HTML specimen for {block_id}")
            fragments.append(f'<div class="assembled-block" data-block-id="{html.escape(block_id, quote=True)}">{snippet}</div>')
        rendered_sections.append(
            f'<section class="assembly-section" id="{html.escape(section["id"], quote=True)}">'
            f'<div class="section-head"><p class="eyebrow">LIBRARY COMPOSITION</p>'
            f'<h2>{html.escape(section["title"])}</h2><p>{html.escape(section.get("intro", ""))}</p></div>'
            f'<div class="section-parts">{"".join(fragments)}</div></section>'
        )

    title = html.escape(contract.get("title", "Smart App"))
    description = html.escape(contract.get("description", ""))
    shell_css = """
:root{color-scheme:dark}body{margin:0;min-height:100vh;background:#08070c;color:#f7f4ff}
.assembly-page{max-width:1180px;margin:auto;padding:clamp(18px,4vw,44px)}
.assembly-hero{padding:28px 0 34px}.eyebrow{font-size:11px;font-weight:850;letter-spacing:.17em;color:var(--purple,#a78bfa);text-transform:uppercase}
.assembly-hero h1{font-size:clamp(32px,5vw,58px);line-height:1.03;letter-spacing:-.04em;max-width:900px;margin:10px 0}
.assembly-hero .lead{font-size:18px;line-height:1.6;color:var(--ink-dim,#c8c0d5);max-width:780px}
.assembly-section{margin:22px 0 32px;padding:clamp(16px,3vw,26px);border:1px solid rgba(255,255,255,.17);border-radius:22px;background:linear-gradient(145deg,#171420,#0c0b11);box-shadow:inset 0 1px rgba(255,255,255,.08),0 20px 40px #0008}
.section-head h2{font-size:clamp(22px,3vw,30px);margin:4px 0}.section-head>p:last-child{color:var(--ink-dim,#c8c0d5);max-width:740px}
.section-parts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:18px;align-items:start;margin-top:18px}
.assembled-block{min-width:0;max-width:100%;overflow-wrap:anywhere}.assembled-block>svg{max-width:100%}
.assembled-block button,.assembled-block input,.assembled-block a{max-width:100%}
.assembly-footer{margin-top:36px;padding:18px 0;border-top:1px solid rgba(255,255,255,.18);color:var(--ink-dim,#c8c0d5);font-size:13px}
@media(max-width:560px){.assembly-page{padding:16px}.assembly-section{padding:15px;border-radius:17px}.section-parts{grid-template-columns:1fr}.assembled-block{width:100%}}
"""
    output = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="theme-color" content="#08070c">\n'
        f"<title>{title}</title>\n<meta name=\"description\" content=\"{description}\">\n"
        "<style>\n" + "\n".join(css_parts) + "\n" + shell_css + "\n</style>\n</head>\n<body>\n"
        + icons + "\n<main class=\"assembly-page\">\n"
        + f'<header class="assembly-hero"><p class="eyebrow">BUILT FROM REGISTERED PARTS</p><h1>{title}</h1><p class="lead">{description}</p></header>\n'
        + "\n".join(rendered_sections)
        + '\n<footer class="assembly-footer">Assembly specimen · source parts and dependencies are recorded in the receipt. '
        + "Catalogued does not mean production-proven.</footer>\n</main>\n"
    )
    if js_parts:
        output += "\n<script>\n" + "\n".join(js_parts) + "\n</script>\n"
    output += "\n</body>\n</html>\n"

    receipt = {
        "schema_version": "naya-smart-builder-build-receipt-v1",
        "status": "ASSEMBLED_NOT_VISUALLY_VERIFIED",
        "contract_id": contract.get("contract_id"),
        "contract_sha256": sha256(contract_bytes),
        "source_ref": contract.get("source_ref"),
        "source_manifest_path": contract["source_registry"],
        "source_manifest_git_blob_sha": git_blob_sha(manifest_bytes),
        "assembler_version": VERSION,
        "selected_block_ids": selected_ids,
        "resolved_dependency_count": len(dependency_hashes),
        "dependencies": dependency_hashes,
        "output_path": contract.get("output"),
        "output_sha256": sha256(output.encode("utf-8")),
        "verification": {
            "all_selected_ids_resolved": True,
            "all_declared_dependencies_exist": True,
            "css_javascript_and_svg_inlined": True,
            "consumer_render_verified": False,
            "interactions_verified": False,
            "production_proven": False,
        },
    }
    return output, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--library-root", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--receipt", type=Path, default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        output, receipt = assemble(args.contract, args.library_root)
        contract = load_contract = json.loads(args.contract.read_text(encoding="utf-8"))
        output_path = args.output or ROOT / contract.get("output", "HUB/SMART-BUILDER-ASSEMBLY-DEMO.html")
        receipt_path = args.receipt or ROOT / contract.get("receipt", "HUB/SMART-BUILDER-ASSEMBLY-DEMO.receipt.json")
        receipt_text = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
        if args.check:
            if not output_path.exists() or output_path.read_text(encoding="utf-8") != output:
                raise ValueError(f"Generated HTML is stale: {output_path}")
            if not receipt_path.exists() or receipt_path.read_text(encoding="utf-8") != receipt_text:
                raise ValueError(f"Build receipt is stale: {receipt_path}")
            print("PASS: assembled HTML and receipt match the pinned contract and library source")
            return 0
        output_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        receipt_path.write_text(receipt_text, encoding="utf-8")
        print(f"ASSEMBLED: {output_path}")
        print(f"RECEIPT: {receipt_path}")
        print(f"BLOCKS: {len(receipt['selected_block_ids'])}; DEPENDENCIES: {receipt['resolved_dependency_count']}")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: assembly failed closed: {exc}", file=sys.stderr)
        return 2


def load_contract(path: Path) -> dict[str, Any]:
    return load_json(path)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    raise SystemExit(main())
