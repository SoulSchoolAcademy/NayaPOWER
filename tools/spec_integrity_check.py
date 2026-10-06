#!/usr/bin/env python3
"""Spec-integrity check for ratified machine-readable governance specs.

Verifies that the machine-readable projections of ratified law (the Nonstop
Loop and Captain Protocol machine.json files, plus their human/AI sibling
projections) are intact and faithful to their ratified state:

  1. Pin check: every projection's current git blob SHA matches the manifest
     pin. Any drift (edit, deletion, replacement) fails loudly.
  2. Envelope check: status == DIRECTOR-RATIFIED and
     ratified_by == "Shawn Vibert" (only the Human Director ratifies).
  3. Structural check: phases form a clean 1..N sequence with unique,
     non-empty names; invariants present and non-empty.
  4. Coverage check: every *.machine.json under the governed directory is
     either pinned in the manifest or explicitly excluded with a reason.

This check does NOT enforce agent conduct and does NOT read agent behavior.
It attests one thing: the spec text the seats read is the spec text that was
ratified. A deliberate spec change must update the manifest pins in the same
PR (reviewed) — that is the intended workflow, not a failure mode.

Usage:
  python tools/spec_integrity_check.py [--manifest PATH] [--root PATH]
  python tools/spec_integrity_check.py --print-pins [--root PATH]
      Emit current blob pins for every *.machine.json found (manifest
      authoring helper). Does not modify anything.

Exit code 0 = all checks pass. Exit code 1 = at least one failure, with
each failure printed as FAIL: <what> -- <why>.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

DEFAULT_MANIFEST = Path(__file__).with_name("spec_integrity_manifest.json")

REQUIRED_ENVELOPE_KEYS = ("schema", "status", "ratified_by", "ratified_date")
EXPECTED_STATUS = "DIRECTOR-RATIFIED"
EXPECTED_RATIFIED_BY = "Shawn Vibert"

# Candidate JSON paths (in priority order) where a spec's phase list lives.
PHASE_PATHS = (("loop", "phases"), ("cycle", "phases"))


def blob_sha(path: Path) -> str | None:
    """Git blob SHA (sha1 of 'blob <len>\\0' + bytes), or None if unreadable."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    h = hashlib.sha1()
    h.update(b"blob " + str(len(data)).encode() + b"\0" + data)
    return h.hexdigest()


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def find_phases(spec: dict):
    for path in PHASE_PATHS:
        node = spec
        for key in path:
            if not isinstance(node, dict) or key not in node:
                node = None
                break
            node = node[key]
        if isinstance(node, list) and node:
            return node, ".".join(path)
    return None, None


def check_spec(entry: dict, root: Path) -> list[str]:
    """Run pin + envelope + structural checks for one manifest spec entry."""
    failures: list[str] = []
    law = entry.get("law", "<unnamed>")
    projections = entry.get("projections", {})

    # 1. Pin check on every projection.
    for proj_name, proj in projections.items():
        rel = proj.get("path", "")
        pinned = proj.get("blob_sha", "")
        full = root / rel
        current = blob_sha(full)
        if current is None:
            failures.append(
                f"FAIL: [{law}] projection '{proj_name}' missing at {rel} "
                "-- file deleted or unreadable"
            )
            continue
        if current != pinned:
            failures.append(
                f"FAIL: [{law}] projection '{proj_name}' drifted from ratified pin "
                f"({rel}): pinned {pinned[:8]}, now {current[:8]} -- "
                "if intentional, update the manifest pins in the same (reviewed) PR"
            )

    # 2+3. Envelope + structural checks on the machine projection.
    machine = projections.get("machine", {})
    mpath = root / machine.get("path", "")
    spec = load_json(mpath)
    if spec is None:
        failures.append(
            f"FAIL: [{law}] machine projection is not valid JSON: {machine.get('path')}"
        )
        return failures
    for key in REQUIRED_ENVELOPE_KEYS:
        if key not in spec:
            failures.append(
                f"FAIL: [{law}] machine projection missing envelope key '{key}'"
            )
    if spec.get("status") != EXPECTED_STATUS:
        failures.append(
            f"FAIL: [{law}] status is '{spec.get('status')}', expected "
            f"'{EXPECTED_STATUS}' -- only the Human Director's ratification counts"
        )
    if spec.get("ratified_by") != EXPECTED_RATIFIED_BY:
        failures.append(
            f"FAIL: [{law}] ratified_by is '{spec.get('ratified_by')}', expected "
            f"'{EXPECTED_RATIFIED_BY}'"
        )
    phases, where = find_phases(spec)
    if phases is None:
        failures.append(
            f"FAIL: [{law}] no phase list found (looked at "
            + ", ".join(".".join(p) for p in PHASE_PATHS) + ")"
        )
    else:
        names = [p.get("name") for p in phases if isinstance(p, dict)]
        numbers = [p.get("n") for p in phases if isinstance(p, dict)]
        if numbers != list(range(1, len(phases) + 1)):
            failures.append(
                f"FAIL: [{law}] phases at {where} are not a clean 1..N sequence: {numbers}"
            )
        if any(not n or not isinstance(n, str) for n in names):
            failures.append(f"FAIL: [{law}] phases at {where} have empty/non-string names")
        if len(set(names)) != len(names):
            failures.append(f"FAIL: [{law}] duplicate phase names at {where}: {names}")
    invariants = spec.get("invariants")
    if not isinstance(invariants, dict) or not invariants:
        failures.append(f"FAIL: [{law}] 'invariants' missing or empty")
    return failures


def check_coverage(manifest: dict, root: Path) -> list[str]:
    """Every *.machine.json under governed dirs must be pinned or excluded."""
    failures: list[str] = []
    gov_dirs = {Path(e["dir"]) for e in manifest.get("specs", []) if e.get("dir")}
    pinned = set()
    for entry in manifest.get("specs", []):
        for proj in entry.get("projections", {}).values():
            pinned.add(proj.get("path", ""))
    excluded = {x.get("path", ""): x.get("reason", "") for x in manifest.get("excluded", [])}
    for gdir in gov_dirs:
        full_dir = root / gdir
        if not full_dir.is_dir():
            failures.append(f"FAIL: governed dir missing: {gdir}")
            continue
        for mj in sorted(full_dir.glob("*.machine.json")):
            rel = str(mj.relative_to(root))
            if rel not in pinned and rel not in excluded:
                failures.append(
                    f"FAIL: unpinned machine spec {rel} -- pin it in the manifest "
                    "or record an exclusion with reason"
                )
    return failures


def cmd_check(manifest_path: Path, root: Path) -> int:
    manifest = load_json(manifest_path)
    if manifest is None:
        print(f"FAIL: cannot read manifest {manifest_path}")
        return 1
    failures: list[str] = []
    for entry in manifest.get("specs", []):
        failures.extend(check_spec(entry, root))
    failures.extend(check_coverage(manifest, root))
    if failures:
        print("\n".join(failures))
        print(f"\n{len(failures)} integrity failure(s).")
        return 1
    n = len(manifest.get("specs", []))
    print(f"OK: {n} ratified spec(s) intact (pins match, envelope ratified, structure sound).")
    return 0


def cmd_print_pins(root: Path) -> int:
    found = sorted(root.rglob("*.machine.json"))
    out = []
    for mj in found:
        rel = str(mj.relative_to(root))
        out.append({"path": rel, "blob_sha": blob_sha(mj)})
    print(json.dumps(out, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Ratified spec integrity check.")
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--root", type=Path, default=Path.cwd(),
                    help="Repo root the manifest paths resolve against.")
    ap.add_argument("--print-pins", action="store_true",
                    help="Emit current blob pins for manifest authoring; checks nothing.")
    args = ap.parse_args(argv)
    if args.print_pins:
        return cmd_print_pins(args.root)
    return cmd_check(args.manifest, args.root)


if __name__ == "__main__":
    raise SystemExit(main())
