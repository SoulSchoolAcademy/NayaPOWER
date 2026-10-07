#!/usr/bin/env python3
"""Make an artifact receipt for tools/verify_builder_artifacts.py.

The sign-out-discipline wiring for ACT: when a builder reports completion,
the accepting seat generates the claimed-artifact receipt with this tool and
pipes it straight into the verifier — no hand-written JSON, no trust.

    python3 tools/make_artifact_receipt.py --pr 1767 --head <40hex> \\
        | python3 tools/verify_builder_artifacts.py /dev/stdin

Exit 0 from the verifier = every claimed artifact exists on the live remote.
Exit 1 = at least one phantom (claimed-but-missing). Never trust a completion
summary; verify the handles.

This tool only GENERATES the receipt (stdlib only). It never touches the
network and never modifies anything. Schema contract: the "artifacts" list
defined in tools/verify_builder_artifacts.py (PR #1767).
"""

from __future__ import annotations

import argparse
import json
import re
import sys

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA64 = re.compile(r"^[0-9a-f]{64}$")


def _die(msg: str) -> "NoReturn":  # noqa: F821
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def build_receipt(args) -> dict:
    artifacts: list[dict] = []

    for spec in args.pr or []:
        number_s, _, pins = spec.partition(":")
        try:
            number = int(number_s)
        except ValueError:
            _die(f"bad --pr spec {spec!r}: expected N or N:head=<sha>,state=<s>")
        if number <= 0:
            _die(f"bad --pr spec {spec!r}: PR number must be positive")
        art: dict = {"kind": "pr", "number": number}
        for pin in pins.split(","):
            if not pin:
                continue
            k, eq, v = pin.partition("=")
            if not eq:
                _die(f"bad --pr pin {pin!r} in {spec!r}: expected k=v")
            if k == "head":
                if not _SHA40.match(v):
                    _die(f"bad head pin {v!r}: expected 40 hex chars")
                art["head"] = v
            elif k == "state":
                if v not in ("open", "closed"):
                    _die(f"bad state pin {v!r}: expected open|closed")
                art["state"] = v
            else:
                _die(f"unknown --pr pin {k!r}: expected head|state")
        artifacts.append(art)

    for name in args.branch or []:
        if not name or ".." in name or name.startswith(("-", "/", ".")):
            _die(f"bad --branch {name!r}")
        artifacts.append({"kind": "branch", "name": name})

    for spec in args.commit or []:
        sha, _, ancestor = spec.partition(":")
        if not _SHA40.match(sha):
            _die(f"bad --commit {spec!r}: expected 40-hex SHA")
        art = {"kind": "commit", "sha": sha}
        if ancestor:
            art["ancestor_of"] = ancestor
        artifacts.append(art)

    for spec in args.file or []:
        # path[:ref][,sha256=..][,min_bytes=..]
        path, _, rest = spec.partition(":")
        if not path or ".." in path.split("/") or path.startswith("/"):
            _die(f"bad --file path in {spec!r}")
        art = {"kind": "file", "path": path}
        ref = None
        for part in rest.split(","):
            if not part:
                continue
            if "=" not in part and ref is None:
                ref = part
                continue
            k, eq, v = part.partition("=")
            if not eq:
                _die(f"bad --file part {part!r} in {spec!r}")
            if k == "sha256":
                if not _SHA64.match(v):
                    _die(f"bad sha256 {v!r}: expected 64 hex chars")
                art["sha256"] = v
            elif k == "min_bytes":
                try:
                    art["min_bytes"] = int(v)
                except ValueError:
                    _die(f"bad min_bytes {v!r}")
            else:
                _die(f"unknown --file key {k!r}")
        if ref:
            art["ref"] = ref
        artifacts.append(art)

    if not artifacts:
        _die("no artifacts given: pass at least one of --pr/--branch/--commit/--file")
    return {"artifacts": artifacts}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Generate a claimed-artifact receipt for "
                    "tools/verify_builder_artifacts.py (ACT sign-out wiring)."
    )
    ap.add_argument("--pr", action="append", metavar="N[:head=<sha>,state=<s>]",
                    help="PR claim, e.g. --pr 1767 --pr '1768:head=<40hex>,state=open'")
    ap.add_argument("--branch", action="append", metavar="NAME",
                    help="branch claim, e.g. --branch main")
    ap.add_argument("--commit", action="append", metavar="SHA[:ancestor_of]",
                    help="commit claim, e.g. --commit <40hex>")
    ap.add_argument("--file", action="append", metavar="PATH[:ref][,sha256=..,min_bytes=..]",
                    help="file claim, e.g. --file tools/x.py:main,min_bytes=100")
    ap.add_argument("--out", metavar="PATH",
                    help="write receipt JSON to PATH instead of stdout")
    ap.add_argument("--pretty", action="store_true",
                    help="pretty-print the JSON")
    args = ap.parse_args(argv)

    receipt = build_receipt(args)
    text = json.dumps(receipt, indent=2 if args.pretty else None)
    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(text + "\n")
        except OSError as e:
            _die(f"cannot write {args.out}: {e}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
