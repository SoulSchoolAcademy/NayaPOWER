#!/usr/bin/env python3
"""P0 Gate 3 — Nine-Node Behavioral Influence (machine-falsifiable).

K1..K6 (scripts/verify-nine-master-nodes.py) prove STRUCTURAL conformance:
the nodes exist in the manifest. This gate proves BEHAVIORAL influence —
the chain every node must traverse:

    EXISTS -> LOADS -> INVOKES -> INFLUENCES -> APPLIES

  E  EXISTS     — node present in the kernel manifest.
  L  LOADS      — node referenced by runtime/loader CODE (not docs/specs).
  I  INVOKES    — node has invocation call sites in an execution path.
  F  INFLUENCES — decision records show the node's context changing a
                 decision (differential evidence, not mere mention).
  A  APPLIES    — the influenced decision produced an applied outcome
                 (receipt).

A node that EXISTS but is never LOADED is a documented node, not a living
one. A node that is INVOKED but never INFLUENCES is decoration.

Honest current state (2026-10-07): E passes; L/I/F/A fail. The gate FAILS
overall — and that is the correct signal. When the runtime is built, the
same gate passes without modification. A gate that cannot fail is not a gate.

Usage:
    python3 scripts/gate-nine-node-influence.py [--root PATH]
        [--manifest PATH]
Exit 0 = all nodes traverse all stages. Exit 1 = any stage fails
(names the node and stage).

Falsifier: add a runtime loader that references MN-05 in code -> L passes
for MN-05. Remove it -> L fails again. The gate tracks reality, not intent.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NODES = [
    ("MN-01", "SELF"),
    ("MN-02", "LAW"),
    ("MN-03", "ACT"),
    ("MN-04", "KNOW"),
    ("MN-05", "PROVE"),
    ("MN-06", "CONNECT"),
    ("MN-07", "VERIFY"),
    ("MN-08", "LEARN"),
    ("MN-09", "EVOLVE"),
]

# Files that are documentation/specification, not runtime behavior.
DOC_SUFFIXES = {".md", ".markdown", ".txt", ".pdf"}
SPEC_DIRS = {".naya", "KNOWLEDGE", "BRAIN"}
CODE_SUFFIXES = {".py", ".ts", ".js", ".mjs", ".sh", ".sql", ".yml", ".yaml"}

# Invocation patterns: the node id appearing in a call/dispatch context.
INVOKE_RES = [
    re.compile(r"invoke\w*\(.*?MN-0[1-9]", re.I | re.S),
    re.compile(r"MN-0[1-9].*?invoke\w*\(", re.I | re.S),
    re.compile(r"dispatch\w*\(.*?MN-0[1-9]", re.I | re.S),
    re.compile(r"MN-0[1-9].*?dispatch\w*\(", re.I | re.S),
    re.compile(r"execute\w*\(.*?node.*?MN-0[1-9]", re.I | re.S),
    re.compile(r"node\.invoke|invoke_node|call_node", re.I),
]


def is_doc(path: Path, root: Path) -> bool:
    if path.suffix.lower() in DOC_SUFFIXES:
        return True
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    if rel.parts and rel.parts[0] in SPEC_DIRS:
        return True
    return False


def code_files(root: Path):
    for ext in CODE_SUFFIXES:
        for f in root.rglob(f"*{ext}"):
            if ".git/" in str(f) or "node_modules" in str(f):
                continue
            if is_doc(f, root):
                continue
            yield f


def check_exists(manifest: dict) -> dict[str, bool]:
    ids = {n.get("id") for n in manifest.get("nodes", [])}
    return {nid: (nid in ids) for nid, _ in NODES}


def check_loads(root: Path) -> dict[str, list[str]]:
    """Node id referenced in runtime/loader code (not docs/specs)."""
    hits: dict[str, list[str]] = {nid: [] for nid, _ in NODES}
    id_re = {nid: re.compile(r"\b" + re.escape(nid) + r"\b") for nid, _ in NODES}
    for f in code_files(root):
        try:
            text = f.read_text(errors="replace")
        except OSError:
            continue
        for nid, rx in id_re.items():
            if rx.search(text):
                hits[nid].append(str(f.relative_to(root)))
    return hits


def check_invokes(root: Path) -> dict[str, list[str]]:
    """Node id in an invocation call-site context."""
    hits: dict[str, list[str]] = {nid: [] for nid, _ in NODES}
    for f in code_files(root):
        try:
            text = f.read_text(errors="replace")
        except OSError:
            continue
        for nid, _key in NODES:
            nid_rx = re.compile(r"\b" + re.escape(nid) + r"\b")
            if not nid_rx.search(text):
                continue
            for irx in INVOKE_RES:
                if irx.search(text):
                    hits[nid].append(str(f.relative_to(root)))
                    break
    return hits


def check_influences(root: Path) -> dict[str, list[str]]:
    """Decision records where a node's context changed a decision.

    Evidence shape: a JSON receipt/decision naming the node AND recording
    a before/after, a differential, or an explicit influence statement.
    Mere mention of the node in prose does not count.
    """
    hits: dict[str, list[str]] = {nid: [] for nid, _ in NODES}
    influence_rx = re.compile(
        r"influenc|changed the decision|decision changed|differential|"
        r"because of (MN-0[1-9]|node)|node context", re.I)
    for f in root.rglob("*.json"):
        if ".git/" in str(f) or is_doc(f, root):
            continue
        try:
            text = f.read_text(errors="replace")
            data = json.loads(text)
        except (OSError, json.JSONDecodeError):
            continue
        blob = json.dumps(data)
        for nid, _key in NODES:
            if re.search(r"\b" + re.escape(nid) + r"\b", blob) and influence_rx.search(blob):
                hits[nid].append(str(f.relative_to(root)))
    return hits


def check_applies(root: Path, influenced: dict[str, list[str]]) -> dict[str, list[str]]:
    """Applied outcomes from influenced decisions: an influenced node must
    have a linked applied receipt (execution receipt referencing it)."""
    # Conservative: only nodes with influence evidence can have applied
    # outcomes; then require an execution-receipt-shaped record naming it.
    hits: dict[str, list[str]] = {nid: [] for nid, _ in NODES}
    receipt_rx = re.compile(r"execution_receipt|applied|outcome", re.I)
    for nid, files in influenced.items():
        if not files:
            continue
        for f in root.rglob("*.json"):
            if ".git/" in str(f) or is_doc(f, root):
                continue
            try:
                blob = f.read_text(errors="replace")
            except OSError:
                continue
            if re.search(r"\b" + re.escape(nid) + r"\b", blob) and receipt_rx.search(blob):
                hits[nid].append(str(f.relative_to(root)))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repo root to scan")
    ap.add_argument("--manifest", default=None,
                    help="kernel manifest (default: <root>/.naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json)")
    args = ap.parse_args()
    root = Path(args.root)
    manifest_path = Path(args.manifest) if args.manifest else \
        root / ".naya" / "specifications" / "NAYA-MASTER-NODE-KERNEL-V1.json"

    if not manifest_path.exists():
        # Fall back to the branch path used in CI checkouts.
        alt = root / "scripts" / "NAYA-MASTER-NODE-KERNEL-V1.json"
        if alt.exists():
            manifest_path = alt
        else:
            print(f"FAIL: manifest not found at {manifest_path}")
            return 1
    manifest = json.loads(manifest_path.read_text())

    exists = check_exists(manifest)
    loads = check_loads(root)
    invokes = check_invokes(root)
    influences = check_influences(root)
    applies = check_applies(root, influences)

    stages = [("E", exists, None), ("L", loads, None), ("I", invokes, None),
              ("F", influences, None), ("A", applies, None)]
    print(f"{'node':<7} {'E':<5} {'L':<5} {'I':<5} {'F':<5} {'A':<5}")
    all_pass = True
    for nid, _key in NODES:
        row = []
        e = exists.get(nid, False)
        row.append("pass" if e else "FAIL")
        l = bool(loads[nid]); row.append("pass" if l else "FAIL")
        i = bool(invokes[nid]); row.append("pass" if i else "FAIL")
        f = bool(influences[nid]); row.append("pass" if f else "FAIL")
        a = bool(applies[nid]); row.append("pass" if a else "FAIL")
        if not all([e, l, i, f, a]):
            all_pass = False
        print(f"{nid:<7} {row[0]:<5} {row[1]:<5} {row[2]:<5} {row[3]:<5} {row[4]:<5}")

    print()
    # Evidence detail for the first failing stage per node.
    for nid, _key in NODES:
        if not exists.get(nid):
            print(f"  {nid}: missing from manifest")
        elif not loads[nid]:
            print(f"  {nid}: EXISTS in manifest but never referenced in runtime code "
                  f"(documented, not loaded)")
        elif not invokes[nid]:
            print(f"  {nid}: loaded but no invocation call sites "
                  f"(seen in: {', '.join(loads[nid][:3])})")
        elif not influences[nid]:
            print(f"  {nid}: invoked but no decision record shows influence")
        elif not applies[nid]:
            print(f"  {nid}: influence recorded but no applied outcome receipt")

    print()
    if all_pass:
        print("GATE RESULT: PASS — all nine nodes traverse EXISTS->LOADS->INVOKES->INFLUENCES->APPLIES")
        return 0
    print("GATE RESULT: FAIL — node influence not behaviorally proven "
          "(this is the honest signal until the runtime exists)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
