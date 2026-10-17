#!/usr/bin/env python3
"""Checker for DESIGN/SPECIMENS: every input accounted for, every JSON entry real, JSON valid."""
import json, hashlib, os, sys

BASE = os.path.expanduser("~/workspace/nayapower-repo/DESIGN/SPECIMENS")
SRC_FILES = os.path.expanduser("~/workspace/user/files")
SRC_IMG = os.path.expanduser("~/workspace/user/media_library/image")

# All 29 inputs, keyed by basename -> (relative subdir used)
INPUTS = {
    "Naya_Design_Element_Set_N4.html": None, "Naya_Design_Elements_N2.html": None,
    "Naya_Design_Standard_Showcase__1.html": None, "Naya_Epic_Elements_-_Lego_pieces_N5.html": None,
    "Naya_Jewel_Library_-_N5.html": None, "Naya_Lego_Blocks_N4.html": None,
    "Naya_Smart_Hub_Design.html": None, "NayaPOWER-Reveal__18__0_0da3.html": None,
    "naya-smart-blocks.html": None, "Smart_Spaces_Page_Design.html": None,
    "Welcome_Page_Design.html": None, "naya-100-laws-elite-interfaces.pdf": None,
    "NayaNET_Design_Standard_V2_Review.zip": None,
    "NayaNET-Design-Code-Convergence-2026-10-08__1.pdf": None,
    "NayaNET-Master-Build-Plan-20261009__3.pdf": None,
    "SESSION-LEARNINGS-2026-10-08.pdf": None, "SPECIMEN-CARD-dial.pdf": None,
    "VISION-LAWS.pdf": None, "VISION-TO-CODE-PROTOCOL.md": None,
    "ultimate-decision-machine-spec-v1.md": None, "world-model-letter-from-shawn.md": None,
    "Naya_Ultimate_Design_System_-_Naya_2.html": None,
}
IMAGE_INPUTS = {
    "44/445e8d328a7bebd50f3fb3b69675e62efa030eab433517e40b34b090923097a5.jpg": "welcome-entrance.jpg",
    "32/32f83809ce7287cc67bd0c6f1b6c3bf840d5d032b1e626fbada85cd1910a6e3b.jpg": "intelligent-hub-smart-feed.jpg",
    "f2/f2f8c813ae5b3b4a1c6060ddbb69034e88df326b8196b7832d739df4c5066bdf.jpg": "reports.jpg",
    "28/2868a91fa1768f3a95d5d3c69e5934b9800fc0a671c0f416e8aad45327a20348.jpg": "smart-ledger.jpg",
    "06/062544dc24d6e5436c4e0c9f39773a921dfe297204669f99d4142cddf435a109.jpg": "spaces.jpg",
    "88/88a415f007d33031370fa8ac65ea49c32df2a04274d6f2d42cb45d7c2f312405.jpg": "connections.jpg",
    "a5/a568642fc8970ba3c23ded9fc4effcbb6143d10c8aff200d0fc3163fd1de6024.jpg": "crystal-n-mark.jpg",
}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

errors = []

# 1. JSON validates
try:
    spec = json.load(open(os.path.join(BASE, "specimens.json")))
except Exception as e:
    errors.append(f"specimens.json invalid: {e}")
    spec = None

if spec:
    pieces = spec["pieces"]
    # 2. every JSON entry's file exists
    lib_files = set()
    for p in pieces:
        fp = os.path.join(BASE, p["file"])
        lib_files.add(p["file"])
        if not os.path.isfile(fp):
            errors.append(f"JSON entry {p['id']} missing file {p['file']}")
        # required fields
        for fld in ("id", "category", "file", "what", "purpose", "source"):
            if not p.get(fld):
                errors.append(f"JSON entry {p['id']} missing field {fld}")
    # 3. unique ids
    ids = [p["id"] for p in pieces]
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids in specimens.json")

    # 4. every input accounted for by content hash in the library
    lib_hashes = {}
    for root, _, fs in os.walk(BASE):
        for f in fs:
            if f in ("specimens.json", "INDEX.md", "check_specimens.py"):
                continue
            p = os.path.join(root, f)
            lib_hashes[sha(p)] = os.path.relpath(p, BASE)
    missing = []
    for name in INPUTS:
        h = sha(os.path.join(SRC_FILES, name))
        if h not in lib_hashes:
            missing.append(name)
    for sub, newname in IMAGE_INPUTS.items():
        h = sha(os.path.join(SRC_IMG, sub))
        if h not in lib_hashes:
            missing.append(sub)
    if missing:
        errors.append(f"inputs not in library: {missing}")

    # 5. no unlisted files in library
    if len(lib_hashes) != len(pieces):
        errors.append(f"file/entry count mismatch: {len(lib_hashes)} files vs {len(pieces)} entries")

    print(f"pieces in JSON: {len(pieces)}")
    print(f"files in library (excl. index/json/checker): {len(lib_hashes)}")
    bycat = {}
    for p in pieces:
        bycat[p["category"]] = bycat.get(p["category"], 0) + 1
    print("by category:", bycat)

if errors:
    print("FAIL:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("CHECKER PASS: 0 missing, 0 unlisted, JSON valid")
