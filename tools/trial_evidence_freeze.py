#!/usr/bin/env python3
"""trial_evidence_freeze.py — durable trial-evidence retention for NayaPOWER EVOLVE.

RULE (SN-0571): /tmp is not an evidence store. Every learning trial that makes a
claim must freeze its raw data into the repo under .naya/proof/trials/<trial-id>/
with a sha256 manifest, so any seat can independently re-verify the claim later.
Summary statistics alone are not verification.

Exit codes:
  0  success (freeze completed / verify intact)
  1  operational error (bad args, unreadable source, invalid claims JSON)
  2  fail-closed refusal: destination already exists (freeze), or
     manifest missing / tamper detected (verify)

Usage:
  freeze --trial-id TRIAL4 --source-dir /tmp/trial4 \\
      --claims claims.json [--dest-root .naya/proof/trials]
  verify --trial-id TRIAL4 [--dest-root .naya/proof/trials]

The freeze copies the source tree byte-for-byte (like the evolve rollback
snapshot, detection without recovery is half a rollback — and absence of raw
data is no verification at all).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone

SCHEMA = "NAYAPOWER_TRIAL_EVIDENCE_MANIFEST_V1"
TOOL_VERSION = "1.0.0"
DEFAULT_DEST_ROOT = os.path.join(".naya", "proof", "trials")


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _collect_files(source_dir: str):
    """Yield (relative_path, absolute_path) for every regular file under source_dir."""
    found = []
    for root, dirs, files in os.walk(source_dir):
        dirs.sort()
        for name in sorted(files):
            abs_path = os.path.join(root, name)
            if not os.path.isfile(abs_path) or os.path.islink(abs_path):
                continue  # symlinks are not evidence; skip fail-closed
            rel = os.path.relpath(abs_path, source_dir)
            found.append((rel, abs_path))
    return found


def cmd_freeze(args) -> int:
    source_dir = os.path.abspath(args.source_dir)
    if not os.path.isdir(source_dir):
        print(f"freeze: source dir not found: {args.source_dir}", file=sys.stderr)
        return 1
    if not args.trial_id or "/" in args.trial_id or "\\" in args.trial_id or args.trial_id in (".", ".."):
        print("freeze: --trial-id must be a single path-safe name", file=sys.stderr)
        return 1

    try:
        with open(args.claims, "r", encoding="utf-8") as f:
            claims = json.load(f)
    except FileNotFoundError:
        print(f"freeze: claims file not found: {args.claims}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"freeze: claims file is not valid JSON: {e}", file=sys.stderr)
        return 1
    if not isinstance(claims, dict):
        print("freeze: claims file must contain a JSON object", file=sys.stderr)
        return 1

    dest_dir = os.path.abspath(os.path.join(args.dest_root, args.trial_id))
    if os.path.lexists(dest_dir):
        # Fail closed: never silently overwrite frozen evidence. A re-run of a
        # trial is a new trial id; history is append-only.
        print(f"freeze: REFUSED — destination already exists: {dest_dir}", file=sys.stderr)
        print("freeze: frozen evidence is immutable; re-run the trial under a new --trial-id", file=sys.stderr)
        return 2

    files = _collect_files(source_dir)
    if not files:
        print(f"freeze: source dir contains no files: {args.source_dir}", file=sys.stderr)
        return 1

    raw_dir = os.path.join(dest_dir, "raw")
    os.makedirs(raw_dir, exist_ok=False)
    entries = []
    for rel, abs_path in files:
        target = os.path.join(raw_dir, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copyfile(abs_path, target)  # byte-for-byte, no metadata games
        entries.append({
            "path": rel.replace(os.sep, "/"),
            "sha256": _sha256(target),
            "bytes": os.path.getsize(target),
        })

    manifest = {
        "schema": SCHEMA,
        "tool_version": TOOL_VERSION,
        "trial_id": args.trial_id,
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "source_dir": source_dir,
        "file_count": len(entries),
        "files": entries,
        "claims": claims,
    }
    manifest_path = os.path.join(dest_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"freeze: trial {args.trial_id}: {len(entries)} files frozen -> {dest_dir}")
    return 0


def cmd_verify(args) -> int:
    dest_dir = os.path.abspath(os.path.join(args.dest_root, args.trial_id))
    manifest_path = os.path.join(dest_dir, "manifest.json")
    raw_dir = os.path.join(dest_dir, "raw")
    if not os.path.isfile(manifest_path) or not os.path.isdir(raw_dir):
        print(f"verify: no frozen evidence for trial {args.trial_id} under {args.dest_root}", file=sys.stderr)
        return 2
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"verify: manifest is not valid JSON: {e}", file=sys.stderr)
        return 1
    if manifest.get("schema") != SCHEMA:
        print(f"verify: unknown manifest schema: {manifest.get('schema')}", file=sys.stderr)
        return 1

    failures = []
    seen = set()
    for entry in manifest.get("files", []):
        rel = entry["path"]
        seen.add(rel)
        target = os.path.join(raw_dir, *rel.split("/"))
        if not os.path.isfile(target):
            failures.append(f"MISSING: {rel}")
            continue
        actual = _sha256(target)
        if actual != entry["sha256"]:
            failures.append(f"TAMPERED: {rel} (manifest {entry['sha256'][:12]}… != actual {actual[:12]}…)")

    # Extra files not in the manifest are also drift.
    for root, dirs, files in os.walk(raw_dir):
        dirs.sort()
        for name in sorted(files):
            rel = os.path.relpath(os.path.join(root, name), raw_dir).replace(os.sep, "/")
            if rel not in seen:
                failures.append(f"UNRECORDED: {rel}")

    if failures:
        print(f"verify: trial {args.trial_id}: EVIDENCE INTEGRITY FAILURE ({len(failures)}):", file=sys.stderr)
        for line in failures:
            print(f"verify:   {line}", file=sys.stderr)
        return 1

    print(f"verify: trial {args.trial_id}: intact ({len(seen)} files, hashes match)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Freeze and verify durable trial evidence (SN-0571).")
    sub = p.add_subparsers(dest="command", required=True)

    fz = sub.add_parser("freeze", help="copy a trial's raw data into the repo with a sha256 manifest")
    fz.add_argument("--trial-id", required=True)
    fz.add_argument("--source-dir", required=True)
    fz.add_argument("--claims", required=True, help="JSON object file stating the trial's claims")
    fz.add_argument("--dest-root", default=DEFAULT_DEST_ROOT)
    fz.set_defaults(func=cmd_freeze)

    vf = sub.add_parser("verify", help="re-hash frozen evidence and compare against the manifest")
    vf.add_argument("--trial-id", required=True)
    vf.add_argument("--dest-root", default=DEFAULT_DEST_ROOT)
    vf.set_defaults(func=cmd_verify)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
