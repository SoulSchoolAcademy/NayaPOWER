#!/usr/bin/env python3
"""Fail-closed audit for canonical Smart Note / Intelligent Block projections."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL_ROOT = ROOT / ".naya" / "memory" / "smart-notes"
IB_RE = re.compile(r"^IB-\d{6}$")
PATH_RE = re.compile(r"^\.naya/memory/smart-notes/\d{4}/\d{2}/\d{2}/[a-z0-9-]+/[a-z0-9-]+/IB-\d{6}/smart-note\.md$")
HEADINGS = ("IN A NUTSHELL","DATE / TIME","WHAT","WHY IT MATTERS","HUMAN","CHILD","GRANDMA","NAYA","MACHINE","WHAT WE LEARNED","CONNECTIONS","HOW TO APPLY","WHAT IT ULTIMATELY MEANS","WHAT'S IN IT FOR YOU / US","NEXT ACTION")

def audit(root: Path = ROOT) -> list[str]:
    errors = []
    registry_path = root / ".naya" / "memory" / "smart-notes" / "REGISTRY.json"
    canonical_root = root / ".naya" / "memory" / "smart-notes"
    if not canonical_root.is_dir(): return ["missing canonical Smart Note root"]
    if not registry_path.is_file(): return ["missing canonical Smart Note registry"]
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registered = set()
    for entry in registry.get("entries", []):
        ib = str(entry.get("intelligent_block_id",""))
        rel = str(entry.get("path",""))
        registered.add(rel)
        if not IB_RE.fullmatch(ib): errors.append("invalid registry IB: "+ib)
        if not PATH_RE.fullmatch(rel): errors.append("noncanonical registry path: "+rel)
        elif not (root / rel).is_file(): errors.append("missing registry projection: "+rel)
    for path in canonical_root.rglob("*"):
        if not path.is_file() or path.name == "REGISTRY.json": continue
        rel = path.relative_to(root).as_posix()
        if not PATH_RE.fullmatch(rel): errors.append("noncanonical Smart Note projection: "+rel); continue
        if rel not in registered: errors.append("unregistered Smart Note projection: "+rel)
        text = path.read_text(encoding="utf-8")
        missing = [h for h in HEADINGS if "## "+h not in text]
        if missing: errors.append("missing Smart Note headings in "+rel+": "+", ".join(missing))
        match = re.search(r"\*\*Intelligent Block ID:\*\*\s*(IB-\d{6})", text)
        expected = rel.split("/")[9]
        if not match or match.group(1) != expected: errors.append("IB identity/path mismatch: "+rel)
    for path in (root / ".naya" / "memory").rglob("smart-note.md"):
        rel = path.relative_to(root).as_posix()
        if not rel.startswith(".naya/memory/smart-notes/"): errors.append("smart-note.md outside canonical root: "+rel)
    markers = ("**Intelligent Block ID:**", "## IN A NUTSHELL", "## WHAT WE LEARNED", "## NEXT ACTION")
    for path in root.rglob("*.md"):
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".naya/memory/smart-notes/") or ".git/" in rel: continue
        try: text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError): continue
        if sum(m in text for m in markers) >= 3: errors.append("canonical Smart Note artifact outside .naya/memory/smart-notes: "+rel)
    return sorted(set(errors))

if __name__ == "__main__":
    errors = audit()
    print("PASS — canonical Smart Note organization is GREEN" if not errors else "FAIL\n" + "\n".join("- "+e for e in errors))
    raise SystemExit(0 if not errors else 1)
