#!/usr/bin/env python3
"""owner_backfill.py — derive and apply `owner`/`owner_basis` across the
knowledge corpus per BRAIN/05-MEMORY/OWNER-FIELD-SPEC-V1.md.

Corpora:
  (a) .naya/capture/*.json      (naya.smart-note-capture.v2 -> v3)
  (b) .naya/memory/smart-notes/index.json entries (v1 -> v2)
  (c) BRAIN/REAL-TREE.json files entries (v1 -> v2)  [dry-run only: the regen
      tool owns this file; this script reports what it WOULD emit so the
      regen-tool update (§5) can be verified against it]

Derivation (ordered, first match wins):
  1. provenance: source.captured_by / ingest notes name a current Naya seat
  2. collective: IB capture corpus, no provenance -> "Naya" (Shawn's ruling)
  3. area_lead: DOMAIN_OWNER v1 by first BRAIN/ path segment; UNMAPPED -> TEAM

Idempotent: re-running on an applied corpus yields ZERO diff. Prove it:
  python3 tools/owner_backfill.py --apply && python3 tools/owner_backfill.py --apply
  -> second run prints "diffs: 0".

Usage: python3 tools/owner_backfill.py [--root PATH] [--apply] [--corpus a,b,c]
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

SEATS = ["Alpha","Beta","Gamma","Delta","Epsilon","Zeta","Eta","Theta","Iota",
         "Kappa","Lambda","Mu"]
LEADS = {"Naya Clarity Narzan","Naya Verity Narzan","Naya Resolve Narzan"}
SEAT_RE = re.compile(r"\bNaya\s+(Alpha|Beta|Gamma|Delta|Epsilon|Zeta|Eta|Theta|Iota|Kappa|Lambda|Mu)\b")

DOMAIN_OWNER = {
    "00-ACTIVATION": "Naya Gamma", "01-GOVERNANCE": "Naya Delta",
    "02-ARCHITECTURE": "Naya Beta", "03-KERNEL": "Naya Beta",
    "04-INTELLIGENCE": "Naya Zeta", "05-MEMORY": "Naya Beta",
    "06-PROOF": "Naya Epsilon", "07-LEARNING": "Naya Alpha",
    "08-SUCCESSION": "Naya Iota", "09-EVOLUTION": "Naya Alpha",
    "10-INTERFACES": "Naya Mu", "11-KNOWLEDGE": "Naya Beta",
    "12-ENGINEERING": "Naya Lambda", "90-OPERATIONS": "Naya Kappa",
    "99-ARCHIVE": "Naya Kappa",
}
PATH_OWNER = [  # (prefix, owner) for non-BRAIN paths
    (".naya/", "Naya Kappa"), ("tools/", "Naya Lambda"),
    ("kernel/", "Naya Beta"), ("CONSTITUTION/", "Naya Delta"),
]


def domain_of(path: str) -> str | None:
    parts = (path or "").split("/")
    if parts and parts[0] == "BRAIN" and len(parts) > 1:
        return parts[1]
    return None


def area_lead_owner(path: str) -> tuple[str, str]:
    dom = domain_of(path)
    if dom and dom in DOMAIN_OWNER:
        return DOMAIN_OWNER[dom], f"area_lead:{dom}"
    for prefix, owner in PATH_OWNER:
        if path.startswith(prefix):
            return owner, f"area_lead:{prefix}"
    return "Naya Kappa", "area_lead:UNMAPPED"


def provenance_seat(doc: dict) -> str | None:
    """Named seat from provenance bytes only. None = no attributable seat."""
    src = doc.get("source") or {}
    cand = src.get("captured_by") if isinstance(src, dict) else None
    if cand and isinstance(cand, str):
        m = SEAT_RE.search(cand)
        if m:
            return f"Naya {m.group(1)}"
        cand_stripped = cand.strip()
        if cand_stripped in LEADS:
            return cand_stripped
    # ingest / provenance notes that cite a seat
    blob = json.dumps({"i": doc.get("intelligence"), "s": doc.get("source")})
    m = SEAT_RE.search(blob)
    if m:
        return f"Naya {m.group(1)}"
    return None


def derive_capture(doc: dict, fname: str) -> tuple[str, str]:
    seat = provenance_seat(doc)
    if seat:
        return seat, "provenance"
    return "Naya", "collective"  # Shawn: IB owners = NAYA


def derive_index_entry(entry: dict) -> tuple[str, str]:
    blob = json.dumps(entry.get("provenance", {})) + " " + json.dumps(entry.get("backfill", {}))
    m = SEAT_RE.search(blob)
    if m:
        return f"Naya {m.group(1)}", "provenance"
    path = entry.get("projection_path") or entry.get("canonical_brain_path") or ""
    return area_lead_owner(path)


def derive_real_tree(entry: dict) -> tuple[str, str]:
    return area_lead_owner(entry.get("path", ""))


# §5 of OWNER-FIELD-SPEC-V1: the regen tool is the canonical emitter of
# owner/owner_basis on REAL-TREE entries. regenerate_brain_index.py imports
# this schema constant and derive_real_tree() from here — ONE derivation rule
# shared by backfill and regen, so their outputs agree by construction
# (a second re-apply can only ever be a zero diff).
REAL_TREE_SCHEMA_V2 = "naya.brain.real_tree.v2"


def _indent_of_schema_line(text: str) -> str:
    import re as _re
    m = _re.search(r'^(\s*)"schema":\s*"naya\.smart-note-capture\.v2"', text,
                   _re.M)
    return m.group(1) if m else "  "


def textual_capture_patch(text: str, owner: str, basis: str) -> str:
    """Insert owner fields right after the top-level opening brace; bump
    v2->v3 in place. Byte-preserving otherwise (no re-encode of mixed
    raw/escaped unicode). Works for pretty-printed and single-line files."""
    stripped = text.lstrip()
    assert stripped.startswith("{"), "unexpected capture layout"
    indent = "  "
    owner_block = f'{indent}"owner": {json.dumps(owner)},\n{indent}"owner_basis": {json.dumps(basis)},'
    if text.startswith("{\n"):
        out = "{\n" + owner_block + "\n" + text[2:]
    else:
        out = "{" + owner_block + stripped[1:]
    return out.replace('"naya.smart-note-capture.v2"', '"naya.smart-note-capture.v3"')


def _restamp_manifest(text: str, manifest: str) -> str:
    """Replace the corpus_manifest_hash value in place (textual, byte-preserving).

    The writer contract (tools/smart_note_v2.py, B-51 step 3) anchors the manifest
    over the FULL entry list as committed. Any entry mutation without a re-stamp
    fails closed at read time as MANIFEST_STALE.
    """
    new_text, n = re.subn(r'"corpus_manifest_hash":\s*"[0-9a-f]+"',
                          '"corpus_manifest_hash": "%s"' % manifest,
                          text, count=1)
    assert n == 1, "corpus_manifest_hash line not found for re-stamp"
    return new_text


def textual_index_patch(text: str, owners: list[tuple[str, str]]) -> str:
    """Insert owner/owner_basis after each entry's opening brace; bump
    top-level schema+version in place. entries appear in list order."""
    lines = text.split("\n")
    out, ei, in_entries = [], 0, False
    for ln in lines:
        out.append(ln)
        s = ln.strip()
        if s == '"entries": [':
            in_entries = True
            continue
        if in_entries and s == "{" and ln.startswith("    {"):
            # entry objects are the only `  {` lines in the file
            owner, basis = owners[ei]; ei += 1
            out.append(f'    "owner": {json.dumps(owner)},')
            out.append(f'    "owner_basis": {json.dumps(basis)},')
        if in_entries and s == "]" and not ln.startswith(" "):
            in_entries = False
    txt = "\n".join(out)
    txt = txt.replace('"schema": "naya.smart-note-projection-index.v1"',
                      '"schema": "naya.smart-note-projection-index.v2"')
    txt = txt.replace('"version": "1.0"', '"version": "2.0"')
    assert ei == len(owners), f"patched {ei} entries, expected {len(owners)}"
    return txt


def process(root: Path, apply: bool, corpora: set[str]) -> dict:
    stats = {"a_scanned":0,"a_diffs":0,"a_basis":{},"b_scanned":0,"b_diffs":0,
             "b_basis":{},"c_scanned":0,"c_diffs":0,"c_basis":{}}
    if "a" in corpora:
        for f in sorted((root/".naya"/"capture").glob("*.json")):
            text = f.read_text(encoding="utf-8")
            doc = json.loads(text)
            stats["a_scanned"] += 1
            owner, basis = derive_capture(doc, f.name)
            stats["a_basis"][basis] = stats["a_basis"].get(basis, 0) + 1
            changed = doc.get("owner") != owner or doc.get("owner_basis") != basis
            if changed:
                stats["a_diffs"] += 1
            if apply and changed:
                f.write_text(textual_capture_patch(text, owner, basis),
                             encoding="utf-8")
    if "b" in corpora:
        idx_p = root/".naya"/"memory"/"smart-notes"/"index.json"
        text = idx_p.read_text(encoding="utf-8")
        idx = json.loads(text)
        owners = []
        for e in idx.get("entries", []):
            stats["b_scanned"] += 1
            owner, basis = derive_index_entry(e)
            bkey = basis.split(":")[0]
            stats["b_basis"][bkey] = stats["b_basis"].get(bkey, 0) + 1
            owners.append((owner, basis))
            if e.get("owner") != owner or e.get("owner_basis") != basis:
                stats["b_diffs"] += 1
        if apply and stats["b_diffs"]:
            patched = textual_index_patch(text, owners)
            # Re-anchor the manifest: the textual patch mutates entries, so the
            # old manifest no longer anchors what is committed. Without this,
            # the next fail-closed read dies MANIFEST_STALE (the w211 14-red).
            import smart_note_v2 as _snv2  # lazy sibling import: no cycle
            reanchored = json.loads(patched)
            manifest = _snv2._corpus_manifest_hash(reanchored["entries"])
            patched = _restamp_manifest(patched, manifest)
            idx_p.write_text(patched, encoding="utf-8")
        elif apply:
            pass  # nothing to change; leave bytes alone
    if "c" in corpora:
        rt_p = root/"BRAIN"/"REAL-TREE.json"
        rt = json.loads(rt_p.read_text(encoding="utf-8"))
        files = rt.get("files", [])
        for e in files:
            stats["c_scanned"] += 1
            owner, basis = derive_real_tree(e)
            bkey = basis.split(":")[0]
            stats["c_basis"][bkey] = stats["c_basis"].get(bkey, 0) + 1
            if e.get("owner") != owner or e.get("owner_basis") != basis:
                stats["c_diffs"] += 1
        # never writes: the regen tool owns REAL-TREE.json (§5)
    return stats


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", type=Path)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--corpus", default="a,b,c")
    args = ap.parse_args(argv)
    stats = process(args.root.resolve(), args.apply, set(args.corpus.split(",")))
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"{mode}: {json.dumps(stats, indent=1, sort_keys=True)}")
    total_diffs = stats["a_diffs"] + stats["b_diffs"] + stats["c_diffs"]
    print(f"total_diffs: {total_diffs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
