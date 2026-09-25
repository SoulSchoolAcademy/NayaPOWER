#!/usr/bin/env python3
"""Verify the 2026-09-25 canonical memory surface."""
from __future__ import annotations
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
MEMORY=ROOT/".naya"/"memory"
MANIFEST=ROOT/".naya"/"naya-context-manifest.json"
REQUIRED=(MEMORY/"NAYAPOWER-BRAIN-MAP.md",MEMORY/"BOOTSTRAP.md",MEMORY/"RETRIEVAL-MANIFEST.json",MEMORY/"smart-notes"/"REGISTRY.json",MEMORY/"archive"/"legacy-pre-2026-09-25")
LEGACY_ROOT=re.compile(r"^(AI-NOTE|HUMAN-NOTE|MACHINE-NOTE|NAYA-NOTE|SHAWN-NOTE|SMART-NOTE|SN-|DAILY-INTELLIGENCE)")
def verify():
    errors=[f"missing required memory surface: {p}" for p in REQUIRED if not p.exists()]
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    for rel in manifest.get("boot_order",[]):
        if not (ROOT/rel).exists(): errors.append(f"boot_order path does not exist: {rel}")
    if any(LEGACY_ROOT.match(p.name) for p in MEMORY.iterdir() if p.is_file()):
        errors.append("legacy note family remains at active memory root")
    if (ROOT/".naya"/"codex"/"NAYAPOWER-BRAIN").exists(): errors.append("obsolete codex Brain taxonomy still exists")
    retrieval=json.loads((MEMORY/"RETRIEVAL-MANIFEST.json").read_text(encoding="utf-8"))
    if retrieval.get("canonical_primary_store") != ".naya/memory/smart-notes/": errors.append("retrieval manifest points canonical primary store away from Smart Note/IB projections")
    if retrieval.get("canonical_registry") != ".naya/memory/smart-notes/REGISTRY.json": errors.append("retrieval manifest does not name the canonical IB registry")
    if retrieval.get("event_lineage_store") != ".naya/memory/events/": errors.append("retrieval manifest does not isolate event lineage store")
    registry=json.loads((MEMORY/"smart-notes"/"REGISTRY.json").read_text(encoding="utf-8"))
    if registry.get("status")!="CANONICAL": errors.append("Smart Note registry is not CANONICAL")
    for entry in registry.get("entries",[]):
        if not (ROOT/entry["path"]).is_file(): errors.append(f"registry entry missing: {entry['path']}")
        if not re.fullmatch(r"IB-[0-9]{6}",str(entry.get("intelligent_block_id",""))): errors.append(f"invalid IB identity: {entry.get('intelligent_block_id')}")
    return errors
if __name__=="__main__":
    e=verify()
    print("PASS — canonical memory surface is coherent" if not e else "FAIL\n"+"\n".join("- "+x for x in e))
    raise SystemExit(0 if not e else 1)
