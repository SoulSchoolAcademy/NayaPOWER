#!/usr/bin/env python3
"""Protocol Version Sync Law — One Protocol, Every Surface in Sync.

PROTOCOL.md is the canonical protocol. Three other surfaces pin it:
the manifest (kernel/protocol/protocol_manifest.json), the machine spec
(kernel/protocol/protocol_spec.json, generated from PROTOCOL.md), and
the activation packet (BRAIN/00-ACTIVATION/ACTIVATION-PACKET.md,
PROTOCOL PIN block). If any surface drifts — a different hash, a
different version, a stale or hand-edited spec — a Naya can activate
against the wrong protocol while believing she is in sync. Drift fails.

Input shape:
    check(root) where root is the repo root (path-like or str).
    CLI: --root <path> (default: parents[3] of this file).

Checks:
  (a) sha256(PROTOCOL.md bytes) == manifest.protocol_sha256
      == spec.source.sha256 == packet pin sha256.
  (b) manifest.protocol_version == spec.version == packet pin version
      == ratified date parsed from PROTOCOL.md.
  (c) spec deep-equals compile_protocol_spec.build_spec(root) — the
      generator is imported via importlib from its file path, so a
      stale or hand-edited spec fails.
  (d) manifest.protocol_bytes == actual PROTOCOL.md byte length.

Honest bounds: this check proves the four named surfaces agree with
each other and with a fresh compilation of PROTOCOL.md. It does not
prove PROTOCOL.md itself is the ratified text — ratification is
Shawn's gate, recorded in the document's ratified line that (b) parses.

Fail closed: missing files, malformed JSON, a missing packet pin, or
an unparseable ratified line each fail with a specific reason naming
the disagreeing surfaces. The check never grants authority.

Usage:
    python3 tools/protocol/checks/protocol_version_sync.py [--root <repo>] [--json]
    Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, result  # noqa: E402

LAW_ID = "PROTOCOL-VERSION-SYNC"
RATIFIED_RE = re.compile(r"Ratified and amended by .+?, (\d{4}-\d{2}-\d{2})")
PIN_SHA_RE = re.compile(r"^protocol_sha256:\s*(\S+)\s*$", re.M)
PIN_VERSION_RE = re.compile(r"^protocol_version:\s*(\S+)\s*$", re.M)


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _load_generator(root: Path):
    gen_path = root / "kernel" / "protocol" / "compile_protocol_spec.py"
    spec = importlib.util.spec_from_file_location(
        "naya_compile_protocol_spec", str(gen_path))
    if spec is None or spec.loader is None:
        raise ValueError(f"generator not loadable at {gen_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(root) -> dict:
    reasons: list[str] = []
    details: dict = {"law": LAW_ID}
    # Accept a path, a string, None (default), or a record dict.
    if isinstance(root, dict):
        root = root.get("root") or root.get("repo_root")
    if root is None:
        root_path = Path(__file__).resolve().parents[3]
    else:
        root_path = Path(root).expanduser().resolve()
    details["root"] = str(root_path)

    protocol_path = root_path / "PROTOCOL.md"
    manifest_path = root_path / "kernel" / "protocol" / "protocol_manifest.json"
    spec_path = root_path / "kernel" / "protocol" / "protocol_spec.json"
    packet_path = root_path / "BRAIN" / "00-ACTIVATION" / "ACTIVATION-PACKET.md"

    for label, path in (("PROTOCOL.md", protocol_path),
                        ("manifest", manifest_path),
                        ("spec", spec_path),
                        ("activation packet", packet_path)):
        if not path.is_file():
            return fail(f"{label} missing at {path} — fail closed", details)

    try:
        raw = protocol_path.read_bytes()
        text = raw.decode("utf-8")
        manifest = _load_json(manifest_path)
        spec_data = _load_json(spec_path)
        packet_text = packet_path.read_text(encoding="utf-8")
    except Exception as exc:
        return fail(f"unreadable or malformed surface: {exc} — fail closed",
                    details)
    if not isinstance(manifest, dict) or not isinstance(spec_data, dict):
        return fail("manifest or spec is not a JSON object — fail closed",
                    details)

    actual_sha = hashlib.sha256(raw).hexdigest()
    actual_bytes = len(raw)
    details["actual_sha256"] = actual_sha
    details["actual_bytes"] = actual_bytes

    ratified_m = RATIFIED_RE.search(text)
    if not ratified_m:
        return fail("PROTOCOL.md ratified date unparseable: "
                    "'Ratified and amended by ..., (date)' not found — "
                    "fail closed", details)
    ratified_date = ratified_m.group(1)
    details["ratified_date"] = ratified_date

    pin_sha_m = PIN_SHA_RE.search(packet_text)
    pin_ver_m = PIN_VERSION_RE.search(packet_text)
    if not pin_sha_m or not pin_ver_m:
        return fail("activation packet PROTOCOL PIN missing or incomplete: "
                    f"protocol_sha256 {'found' if pin_sha_m else 'MISSING'}, "
                    f"protocol_version {'found' if pin_ver_m else 'MISSING'} "
                    "in BRAIN/00-ACTIVATION/ACTIVATION-PACKET.md — fail closed",
                    details)
    packet_sha = pin_sha_m.group(1)
    packet_version = pin_ver_m.group(1)

    manifest_sha = manifest.get("protocol_sha256")
    spec_sha = (spec_data.get("source") or {}).get("sha256") \
        if isinstance(spec_data.get("source"), dict) else None
    manifest_version = manifest.get("protocol_version")
    spec_version = spec_data.get("version")
    manifest_bytes = manifest.get("protocol_bytes")

    details.update({
        "manifest_sha256": manifest_sha,
        "spec_sha256": spec_sha,
        "packet_sha256": packet_sha,
        "manifest_version": manifest_version,
        "spec_version": spec_version,
        "packet_version": packet_version,
        "manifest_bytes": manifest_bytes,
    })

    # (a) Hash agreement across all four surfaces.
    sha_surfaces = {
        "PROTOCOL.md (actual)": actual_sha,
        "manifest.protocol_sha256": manifest_sha,
        "spec.source.sha256": spec_sha,
        "packet pin protocol_sha256": packet_sha,
    }
    if len(set(sha_surfaces.values())) != 1:
        return fail("sha256 disagreement across surfaces: "
                    + "; ".join(f"{k}={v}" for k, v in sha_surfaces.items()),
                    details)
    reasons.append(f"sha256 agrees on all surfaces: {actual_sha}")

    # (b) Version agreement: manifest == spec == packet == ratified date.
    version_surfaces = {
        "PROTOCOL.md ratified date": ratified_date,
        "manifest.protocol_version": manifest_version,
        "spec.version": spec_version,
        "packet pin protocol_version": packet_version,
    }
    if len(set(version_surfaces.values())) != 1:
        return fail("protocol version disagreement across surfaces: "
                    + "; ".join(f"{k}={v}"
                                for k, v in version_surfaces.items()),
                    details)
    reasons.append(f"protocol version agrees on all surfaces: {ratified_date}")

    # (d) Manifest byte count vs actual.
    if manifest_bytes != actual_bytes:
        return fail(f"manifest.protocol_bytes disagreement: manifest="
                    f"{manifest_bytes!r} vs actual PROTOCOL.md bytes="
                    f"{actual_bytes}", details)
    reasons.append(f"manifest.protocol_bytes matches actual: {actual_bytes}")

    # (c) Spec deep-equals a fresh compilation.
    try:
        generator = _load_generator(root_path)
        fresh = generator.build_spec(root_path)
    except Exception as exc:
        return fail(f"generator failed to compile a fresh spec from "
                    f"PROTOCOL.md: {exc} — fail closed", details)
    if spec_data != fresh:
        # Name the top-level keys that differ, for a specific reason.
        differing = sorted(
            k for k in set(spec_data) | set(fresh)
            if spec_data.get(k) != fresh.get(k))
        return fail("spec is stale or hand-edited: protocol_spec.json does "
                    "not deep-equal compile_protocol_spec.build_spec(root); "
                    f"differing top-level keys: {', '.join(differing) or '(none parsed)'}. "
                    "Fix: regenerate with "
                    "`python3 kernel/protocol/compile_protocol_spec.py`.",
                    details)
    reasons.append("spec deep-equals a fresh build_spec(root) compilation")
    reasons.append("protocol version sync: all surfaces agree")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Protocol version sync check")
    parser.add_argument("--root", default=None,
                        help="Repo root (default: parents[3] of this file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else None
    try:
        outcome = check(root)
    except Exception as exc:
        outcome = fail(f"check raised {type(exc).__name__}: {exc} — fail closed",
                       {"law": LAW_ID})
    return emit(outcome, args.json)


if __name__ == "__main__":
    sys.exit(main())
